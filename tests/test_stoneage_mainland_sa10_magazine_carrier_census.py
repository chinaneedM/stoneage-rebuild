import unittest
from tools.stoneage_mainland_sa10_magazine_carrier_census import (
    CANDIDATES, STONE_TERMS, YEAR_MIN, YEAR_MAX, ia_url, discm_url
)

class T(unittest.TestCase):
    def test_window(self):
        self.assertEqual((YEAR_MIN,YEAR_MAX),("1999","2002"))

    def test_candidate_controls(self):
        vals={v for _,v in CANDIDATES}
        self.assertIn("电脑报 游戏世界",vals)
        self.assertIn("家用电脑与游戏",vals)
        self.assertIn("晶合秘藏",vals)

    def test_stone_terms(self):
        self.assertIn("石器时代",STONE_TERMS)
        self.assertIn("StoneAge",STONE_TERMS)

    def test_urls(self):
        self.assertIn("advancedsearch.php",ia_url("电脑报 游戏世界","石器时代"))
        self.assertIn("qfields=t",discm_url("电脑报 游戏世界","石器时代","t"))
        self.assertIn("qfields=name",discm_url("电脑报 游戏世界","石器时代","name"))

if __name__=="__main__":
    unittest.main()
