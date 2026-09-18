import struct
import tempfile
import unittest
from pathlib import Path

from tools.stoneage_map_pair_probe import analyze


class StoneAgeMapPairProbeTests(unittest.TestCase):
    def test_map_matches_dat_tile_layer(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            width, height = 3, 2
            tile = struct.pack("<6H", 1, 2, 3, 4, 5, 6)
            parts = struct.pack("<6H", 10, 11, 12, 13, 14, 15)
            event = struct.pack("<6H", 20, 21, 22, 23, 24, 25)
            header = struct.pack("<II", width, height)

            (root / "100.MAP").write_bytes(header + tile)
            (root / "100.DAT").write_bytes(header + tile + parts + event)
            (root / "200.MAP").write_bytes(header + tile)

            result = analyze(root)
            self.assertEqual(result["map_count"], 2)
            self.assertEqual(result["dat_count"], 1)
            self.assertEqual(result["counts"]["paired"], 1)
            self.assertEqual(result["counts"]["tile_match"], 1)
            self.assertEqual(result["counts"]["parts_match"], 0)
            self.assertEqual(result["counts"]["event_match"], 0)
            self.assertEqual(result["map_only"], ["200"])


if __name__ == "__main__":
    unittest.main()
