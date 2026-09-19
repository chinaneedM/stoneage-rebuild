import unittest

from tools.stoneage_gamepia_transition_disc_scan import selected_name


class GamePiaTransitionDiscScanTests(unittest.TestCase):
    def test_accepts_transition_issue_images(self):
        self.assertTrue(selected_name("No.58/CD2/0007101814.bin"))
        self.assertTrue(selected_name("No.61/CD1/IMAGE.img"))
        self.assertTrue(selected_name("No.64/CD2/bonus.mdf"))

    def test_rejects_outside_issues_and_sidecars(self):
        self.assertFalse(selected_name("No.57/CD1/Sin.bin"))
        self.assertFalse(selected_name("No.65/CD1/NEW.mdf"))
        self.assertFalse(selected_name("No.61/CD1/IMAGE.ccd"))


if __name__=="__main__":
    unittest.main()
