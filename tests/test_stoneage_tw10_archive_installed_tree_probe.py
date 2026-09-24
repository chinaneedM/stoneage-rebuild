import unittest

from tools.stoneage_tw10_archive_installed_tree_probe import (
    SIGNATURES, MAP_RE, inspect_files
)


class TaiwanV1ArchiveInstalledTreeProbeTests(unittest.TestCase):
    def test_signature_set_is_pinned(self):
        self.assertIn("sa_3.exe",SIGNATURES)
        self.assertIn("adrn_1.bin",SIGNATURES)
        self.assertIn("waei.bin",SIGNATURES)

    def test_map_pattern_requires_map_directory_and_numeric_leaf(self):
        self.assertIsNotNone(MAP_RE.search("StoneAge/map/1.dat"))
        self.assertIsNotNone(MAP_RE.search(r"StoneAge\map\123.dat"))
        self.assertIsNone(MAP_RE.search("StoneAge/map/foo.dat"))
        self.assertIsNone(MAP_RE.search("StoneAge/data/123.dat"))

    def test_file_inspection_groups_signatures_and_maps(self):
        files=[
            {"name":"StoneAge/sa_3.exe"},
            {"name":"StoneAge/data/adrn_1.bin"},
            {"name":"StoneAge/map/42.dat"},
        ]
        sig,maps=inspect_files(files)
        self.assertEqual(set(sig),{"sa_3.exe","adrn_1.bin"})
        self.assertEqual(len(maps),1)


if __name__=="__main__":
    unittest.main()
