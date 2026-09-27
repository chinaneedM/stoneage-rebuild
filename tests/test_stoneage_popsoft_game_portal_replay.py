import unittest
from tools.stoneage_popsoft_game_portal_replay import CAPTURES,score,hits
class ReplayTests(unittest.TestCase):
    def test_capture_count(self):self.assertEqual(len(CAPTURES),6)
    def test_score(self):self.assertGreater(score("ftp://x/stoneage/setup.exe","下载"),2)
    def test_hits(self):self.assertIn("石器时代",hits("石器时代 试玩 下载"))
if __name__=="__main__":unittest.main()
