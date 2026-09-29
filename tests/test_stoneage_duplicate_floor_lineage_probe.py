import struct
import tempfile
import unittest
from pathlib import Path

from tools.stoneage_duplicate_floor_lineage_probe import analyze


def _dat(tile, parts, event=0):
    return (
        struct.pack("<II", 1, 1)
        + struct.pack("<H", tile)
        + struct.pack("<H", parts)
        + struct.pack("<H", event)
    )


def _server(floor, tile, obj):
    return (
        b"LS2MAP"
        + struct.pack(">H", floor)
        + b"test" + (b"\0" * 28)
        + struct.pack(">HH", 1, 1)
        + struct.pack(">HH", tile, obj)
    )


class DuplicateFloorLineageProbeTests(unittest.TestCase):

    def test_changed_cell_alignment_distinguishes_lineage_values(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            old = root / "old"
            new = root / "new"
            server = root / "server"
            old.mkdir()
            new.mkdir()
            (server / "a").mkdir(parents=True)
            (server / "b").mkdir(parents=True)

            (old / "130.dat").write_bytes(_dat(1, 10))
            (new / "130.dat").write_bytes(_dat(2, 11))
            (server / "a" / "130").write_bytes(_server(130, 1, 10))
            (server / "b" / "130").write_bytes(_server(130, 2, 11))

            audit = analyze(
                floor_id=130,
                historical_root=old,
                recovered25_root=new,
                server_map_root=server,
            )
            by_path = {row.path: row for row in audit.candidates}
            self.assertTrue(by_path["a/130"].historical_static_exact)
            self.assertFalse(by_path["a/130"].recovered25_static_exact)
            self.assertEqual(
                by_path["a/130"].changed_tile_match_historical,
                1,
            )
            self.assertEqual(
                by_path["b/130"].changed_tile_match_recovered25,
                1,
            )
            self.assertTrue(by_path["b/130"].recovered25_static_exact)
            self.assertEqual(audit.dat_tile_diff, 1)
            self.assertEqual(audit.dat_parts_diff, 1)


if __name__ == "__main__":
    unittest.main()
