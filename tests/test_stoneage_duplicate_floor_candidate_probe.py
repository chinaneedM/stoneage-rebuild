import struct
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.stoneage_duplicate_floor_candidate_probe import (
    EXACT_DAT_STATIC_MATCH,
    NO_EXACT_DAT_STATIC_MATCH,
    analyze,
)


def _dat(tile, parts):
    return (
        struct.pack("<II", 1, 1)
        + struct.pack("<H", tile)
        + struct.pack("<H", parts)
        + struct.pack("<H", 0)
    )


def _client_map(value):
    return struct.pack("<IIH", 1, 1, value)


def _server(floor, tile, obj):
    return (
        b"LS2MAP"
        + struct.pack(">H", floor)
        + b"test" + (b"\0" * 28)
        + struct.pack(">HH", 1, 1)
        + struct.pack(">HH", tile, obj)
    )


class _Warp:
    def __init__(
        self,
        source_floor,
        destination_floor,
        destination_x=0,
        destination_y=0,
        source_rect=(0, 0, 0, 0),
    ):
        self.source_floor = source_floor
        self.destination_floor = destination_floor
        self.destination_x = destination_x
        self.destination_y = destination_y
        self.source_rect = source_rect


class DuplicateFloorCandidateProbeTests(unittest.TestCase):

    def _run(self, *, dat=(1, 10), copies=((1, 10), (2, 11))):
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        root = Path(td.name)
        client = root / "client"
        server = root / "server"
        npc = root / "npc"
        client.mkdir()
        server.mkdir()
        npc.mkdir()
        (server / "a").mkdir()
        (server / "b").mkdir()
        (client / "130.dat").write_bytes(_dat(*dat))
        (client / "130.MAP").write_bytes(_client_map(1))
        (server / "a" / "130").write_bytes(_server(130, *copies[0]))
        (server / "b" / "130").write_bytes(_server(130, *copies[1]))
        mapset = root / "mapset.txt"
        mapset.write_bytes(
            b"1 x x 1 0\n2 x x 1 0\n10 x x 1 0\n11 x x 0 0\n"
        )
        warps = (
            _Warp(100, 130),
            _Warp(130, 200),
        )
        with patch(
            "tools.stoneage_duplicate_floor_candidate_probe."
            "_parse_create_geometry",
            return_value=((), warps),
        ):
            return analyze(
                floor_id=130,
                client_map_root=client,
                server_map_root=server,
                mapset_path=mapset,
                npc_dir=npc,
            )

    def test_unique_exact_dat_static_match_is_decisive(self):
        audit = self._run()
        self.assertEqual(audit.resolution, EXACT_DAT_STATIC_MATCH)
        self.assertEqual(audit.selected_path, "a/130")
        by_path = {row.path: row for row in audit.candidates}
        self.assertTrue(by_path["a/130"].dat_static_exact)
        self.assertFalse(by_path["b/130"].dat_static_exact)
        self.assertEqual(audit.incoming_classic_warps, 1)
        self.assertEqual(audit.outgoing_classic_warps, 1)

    def test_no_exact_static_match_remains_unresolved(self):
        audit = self._run(dat=(2, 10))
        self.assertEqual(audit.resolution, NO_EXACT_DAT_STATIC_MATCH)
        self.assertIsNone(audit.selected_path)
        self.assertFalse(any(row.dat_static_exact for row in audit.candidates))


if __name__ == "__main__":
    unittest.main()
