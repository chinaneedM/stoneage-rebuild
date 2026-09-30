import struct
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from tools.stoneage_map_collision_model import DynamicOccupant
from tools.stoneage_recovered25_server_collision_provider import (
    DIVERGENT_SERVER_DUPLICATE,
    NO_SERVER_MAP,
    SERVER_COLLISION_CLOSED,
    Recovered25ServerCollisionProvider,
)
from tools.stoneage_singleplayer_domain import MapPosition
from tools.stoneage_singleplayer_world import (
    HistoricalMapDefinition,
    HistoricalWorldTopology,
)


def _ls2map(floor, width, height, tiles, objects):
    header = (
        b"LS2MAP"
        + struct.pack(">H", floor)
        + b"test"
        + (b"\0" * 28)
        + struct.pack(">HH", width, height)
    )
    return (
        header
        + struct.pack(f">{len(tiles)}H", *tiles)
        + struct.pack(f">{len(objects)}H", *objects)
    )


class Recovered25ServerCollisionProviderTests(unittest.TestCase):

    def _provider(self, root: Path):
        profile = SimpleNamespace(contract_id="test-contract")
        topology = HistoricalWorldTopology(
            maps={
                7: HistoricalMapDefinition(7, 3, 2),
                8: HistoricalMapDefinition(8, 1, 1),
                9: HistoricalMapDefinition(9, 1, 1),
            }
        )
        adapter = SimpleNamespace(profile=profile, topology=topology)
        mapset = root / "mapset.txt"
        mapset.write_bytes(
            b"\n".join(
                [
                    b"1 x x 1 0",
                    b"2 x x 1 0",
                    b"3 x x 0 0",
                ]
            )
        )
        return Recovered25ServerCollisionProvider(
            profile=profile,
            adapter=adapter,
            server_map_root=root,
            mapset_path=mapset,
        )

    def test_supported_floor_returns_descendant_collision_verdict(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            # width=3, height=2. Destination (1,0) uses object 2 (defer to
            # walkable tile 1), while (2,0) uses object 3 (block).
            (root / "floor7").write_bytes(
                _ls2map(
                    7,
                    3,
                    2,
                    (1, 1, 1, 1, 1, 1),
                    (2, 2, 3, 2, 2, 2),
                )
            )
            provider = self._provider(root)
            self.assertEqual(provider.floor_status(7), SERVER_COLLISION_CLOSED)
            allowed = provider.ordinary_step_verdict(
                origin=MapPosition(7, 0, 0),
                destination=MapPosition(7, 1, 0),
            )
            self.assertTrue(allowed.allowed)
            blocked = provider.ordinary_step_verdict(
                origin=MapPosition(7, 1, 0),
                destination=MapPosition(7, 2, 0),
            )
            self.assertFalse(blocked.allowed)

    def test_dynamic_occupant_is_not_silently_ignored(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "floor7").write_bytes(
                _ls2map(
                    7,
                    3,
                    2,
                    (1, 1, 1, 1, 1, 1),
                    (2, 2, 2, 2, 2, 2),
                )
            )
            provider = self._provider(root)
            verdict = provider.ordinary_step_verdict(
                origin=MapPosition(7, 0, 0),
                destination=MapPosition(7, 1, 0),
                destination_occupants=(
                    DynamicOccupant(kind="character", overable=False),
                ),
            )
            self.assertFalse(verdict.allowed)
            self.assertEqual(verdict.reason, "non_overable_character")

    def test_no_server_map_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            provider = self._provider(Path(td))
            self.assertEqual(provider.floor_status(8), NO_SERVER_MAP)
            with self.assertRaisesRegex(ValueError, "NO_SERVER_MAP"):
                provider.ordinary_step_verdict(
                    origin=MapPosition(8, 0, 0),
                    destination=MapPosition(8, 0, 0),
                )

    def test_divergent_duplicates_fail_closed_but_identical_duplicates_do_not(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            # Floor 8: byte-identical duplicates are safe.
            raw8 = _ls2map(8, 1, 1, (1,), (2,))
            (root / "8a").write_bytes(raw8)
            (root / "8b").write_bytes(raw8)
            # Floor 9: divergent duplicate bytes must remain unresolved.
            (root / "9a").write_bytes(_ls2map(9, 1, 1, (1,), (2,)))
            (root / "9b").write_bytes(_ls2map(9, 1, 1, (1,), (3,)))
            provider = self._provider(root)
            self.assertEqual(provider.floor_status(8), SERVER_COLLISION_CLOSED)
            self.assertEqual(
                provider.floor_status(9),
                DIVERGENT_SERVER_DUPLICATE,
            )
            self.assertTrue(
                provider.ordinary_step_verdict(
                    origin=MapPosition(8, 0, 0),
                    destination=MapPosition(8, 0, 0),
                ).allowed is False
            )
            with self.assertRaisesRegex(ValueError, "DIVERGENT_SERVER_DUPLICATE"):
                provider.ordinary_step_verdict(
                    origin=MapPosition(9, 0, 0),
                    destination=MapPosition(9, 0, 0),
                )

    def test_coverage_counts_keep_uncovered_floors_explicit(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "floor7").write_bytes(
                _ls2map(
                    7,
                    3,
                    2,
                    (1, 1, 1, 1, 1, 1),
                    (2, 2, 2, 2, 2, 2),
                )
            )
            provider = self._provider(root)
            counts = provider.coverage_counts()
            self.assertEqual(counts["materializable_floors"], 3)
            self.assertEqual(counts["server_collision_closed"], 1)
            self.assertEqual(counts["server_collision_uncovered"], 2)
            self.assertEqual(counts[NO_SERVER_MAP], 2)


if __name__ == "__main__":
    unittest.main()
