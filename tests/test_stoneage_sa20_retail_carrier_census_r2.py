import unittest
from tools.stoneage_sa20_retail_carrier_census_r2 import IA_QUERIES,DM_QUERIES,strict_text

class SA20RetailCarrierCensusR2Tests(unittest.TestCase):
    def test_refined_queries_cover_both_packages_label_and_filename(self):
        joined="\n".join(q for _,q in IA_QUERIES)+"\n"+"\n".join(DM_QUERIES)
        self.assertIn("新手报到包",joined)
        self.assertIn("老手削暴包",joined)
        self.assertIn("家族开拓史",joined)
        self.assertIn("stoneage2.0setup",joined.lower())
        self.assertIn("year:2001",joined)

    def test_strict_classifier(self):
        self.assertTrue(strict_text("石器时代2.0 家族开拓史 客户端光盘"))
        self.assertTrue(strict_text("STONEAGE2.0SETUP.EXE"))
        self.assertFalse(strict_text("unrelated Stone Age board game"))

if __name__=="__main__":
    unittest.main()
