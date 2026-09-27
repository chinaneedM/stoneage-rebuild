import unittest

from tools.stoneage_mainland_2000_testcd_probe import strict, interesting_files

class Mainland2000TestCDProbeTests(unittest.TestCase):
    def test_strict_requires_title_and_test_or_channel_marker(self):
        self.assertTrue(strict({"title": "石器时代 测试光盘"}))
        self.assertTrue(strict({"description": "StoneAge beta Waei"}))
        self.assertTrue(strict({"title": "StoneAge", "description": "Jinghe test distribution"}))
        self.assertFalse(strict({"title": "StoneAge retail client"}))
        self.assertFalse(strict({"title": "Other game", "description": "测试光盘"}))

    def test_interesting_files(self):
        rows = interesting_files({"files": [
            {"name": "disc.iso"},
            {"name": "manual.pdf"},
            {"name": "setup.exe"},
            {"name": "readme.txt"},
        ]})
        self.assertEqual([x["name"] for x in rows], ["disc.iso", "setup.exe"])

if __name__ == "__main__":
    unittest.main()
