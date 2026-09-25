import unittest
from tools.stoneage_ia_uploader_hidden40_probe import hit_terms
class Hidden40Tests(unittest.TestCase):
    def test_package_name_hit(self):
        d={"identifier":"disc-x","title":"新九大家族 光盘"}
        self.assertIn("新九大家族",hit_terms(d))
    def test_sta4_hit(self):
        self.assertIn("sta4",hit_terms({"identifier":"CD_STA4"}))
if __name__=="__main__": unittest.main()
