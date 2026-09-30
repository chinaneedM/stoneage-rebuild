import struct
import tempfile
import unittest
from pathlib import Path

from tools.stoneage_recovered25_server_collision_coverage_probe import (
    DIVERGENT_SERVER_DUPLICATE,
    MISSING_MAPSET_METADATA,
    NO_SERVER_MAP,
    SERVER_COLLISION_CLOSED,
    SERVER_DIMENSION_MISMATCH,
    _classify_floor,
    _scan_server_maps,
)
from tools.stoneage_server_static_map import (
    parse_ls2map,
    parse_mapset_collision_profile,
)
from tools.stoneage_singleplayer_world import HistoricalMapDefinition


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


class Recovered25ServerCollisionCoverageTests(unittest.TestCase):

    def setUp(self):
        self.mapset = parse_mapset_collision_profile(
            b"\n".join(
                [
                    b"1 x x 1 0",
                    b"2 x x 1 0",
                    b"3 x x 0 0",
                ]
            )
        )

    def test_unique_matching_payload_closes_server_collision(self):
        definition = HistoricalMapDefinition(7, 2, 1)
        parsed = parse_ls2map(_ls2map(7, 2, 1, (1, 1), (2, 3)))
        row = _classify_floor(definition, (parsed,), self.mapset)
        self.assertEqual(row.status, SERVER_COLLISION_CLOSED)
        self.assertEqual(row.total_cells, 2)
        self.assertEqual(row.ordinary_walkable_cells, 1)

    def test_no_server_payload_stays_explicit(self):
        row = _classify_floor(
            HistoricalMapDefinition(7, 2, 1),
            (),
            self.mapset,
        )
        self.assertEqual(row.status, NO_SERVER_MAP)

    def test_divergent_duplicate_is_not_silently_selected(self):
        a = parse_ls2map(_ls2map(7, 1, 1, (1,), (2,)))
        b = parse_ls2map(_ls2map(7, 1, 1, (2,), (2,)))
        row = _classify_floor(
            HistoricalMapDefinition(7, 1, 1),
            (a, b),
            self.mapset,
        )
        self.assertEqual(row.status, DIVERGENT_SERVER_DUPLICATE)
        self.assertEqual(row.unique_payload_count, 2)

    def test_identical_duplicate_is_payload_unambiguous(self):
        raw = _ls2map(7, 1, 1, (1,), (2,))
        a = parse_ls2map(raw)
        b = parse_ls2map(raw)
        row = _classify_floor(
            HistoricalMapDefinition(7, 1, 1),
            (a, b),
            self.mapset,
        )
        self.assertEqual(row.status, SERVER_COLLISION_CLOSED)
        self.assertEqual(row.server_copy_count, 2)
        self.assertEqual(row.unique_payload_count, 1)

    def test_dimension_and_metadata_gaps_have_distinct_statuses(self):
        parsed = parse_ls2map(_ls2map(7, 1, 1, (1,), (2,)))
        mismatch = _classify_floor(
            HistoricalMapDefinition(7, 2, 1),
            (parsed,),
            self.mapset,
        )
        self.assertEqual(mismatch.status, SERVER_DIMENSION_MISMATCH)

        missing = parse_ls2map(_ls2map(8, 1, 1, (1,), (9,)))
        missing_row = _classify_floor(
            HistoricalMapDefinition(8, 1, 1),
            (missing,),
            self.mapset,
        )
        self.assertEqual(missing_row.status, MISSING_MAPSET_METADATA)

    def test_scanner_uses_embedded_floor_id_and_counts_invalid_files(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "a").write_bytes(_ls2map(77, 1, 1, (1,), (2,)))
            (root / "bad").write_bytes(b"not-a-map")
            (root / "mapset.txt").write_text("ignored", encoding="utf-8")
            rows, valid, invalid = _scan_server_maps(root)
        self.assertEqual(valid, 1)
        self.assertEqual(invalid, 1)
        self.assertEqual(set(rows), {77})


if __name__ == "__main__":
    unittest.main()
