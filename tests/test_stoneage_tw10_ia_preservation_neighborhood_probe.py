import unittest

from tools.stoneage_tw10_ia_preservation_neighborhood_probe import (
    MAP_RE,SIGNATURES,inspect_files,leaf
)


class TaiwanV1IAPreservationNeighborhoodProbeTests(unittest.TestCase):
    def test_signature_set_contains_accepted_v1_markers(self):
        self.assertIn("sa_3.exe",SIGNATURES)
        self.assertIn("adrn_1.bin",SIGNATURES)
        self.assertIn("waei.bin",SIGNATURES)

    def test_map_shape_is_strict(self):
        self.assertIsNotNone(MAP_RE.search("StoneAge/map/100.dat"))
        self.assertIsNone(MAP_RE.search("StoneAge/data/100.dat"))
        self.assertIsNone(MAP_RE.search("StoneAge/map/BGM0.dat"))

    def test_inspect_files_separates_signature_and_map_rows(self):
        files=[
            {"name":"root/StoneAge/sa_3.exe"},
            {"name":"root/StoneAge/data/adrn_1.bin"},
            {"name":"root/StoneAge/map/42.dat"},
        ]
        sig,maps=inspect_files(files)
        self.assertEqual({leaf(x["name"]) for x in sig},{"sa_3.exe","adrn_1.bin"})
        self.assertEqual(len(maps),1)


if __name__=="__main__":
    unittest.main()
