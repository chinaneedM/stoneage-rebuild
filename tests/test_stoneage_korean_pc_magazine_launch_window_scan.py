import unittest

from tools.stoneage_korean_pc_magazine_launch_window_scan import selected_name


class KoreanPcMagazineLaunchWindowScanTests(unittest.TestCase):
    def test_accepts_dated_launch_window_images(self):
        self.assertTrue(selected_name("200010/CD1/990915_1453.mdf"))
        self.assertTrue(selected_name("200103/CD2/FarLand_Tactics.mdf"))
        self.assertTrue(selected_name("200112/CD1/NEW.mdf"))

    def test_accepts_legacy_issue_window_images(self):
        self.assertTrue(selected_name("No.61/CD1/IMAGE.img"))
        self.assertTrue(selected_name("No.64/CD2/bonus.bin"))

    def test_rejects_outside_window_and_sidecars(self):
        self.assertFalse(selected_name("200205/CD1/NEW.mdf"))
        self.assertFalse(selected_name("No.57/CD1/Sin.bin"))
        self.assertFalse(selected_name("No.61/CD1/IMAGE.ccd"))


if __name__=="__main__":
    unittest.main()
