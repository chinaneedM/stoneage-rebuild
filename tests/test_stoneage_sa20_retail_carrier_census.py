import unittest
from tools.stoneage_sa20_retail_carrier_census import IA_QUERIES,DM_QUERIES,strict_text

class SA20RetailCarrierCensusTests(unittest.TestCase):
    def test_queries_cover_both_packages_and_sina_filename(self):
        joined="\n".join(q for _,q in IA_QUERIES)+"\n"+"\n".join(DM_QUERIES)
        self.assertIn("新手报到包",joined)
        self.assertIn("老手削暴包",joined)
        self.assertIn("stoneage2.0setup",joined.lower())

    def test_strict_classifier(self):
        self.assertTrue(strict_text("石器时代2.0新手报到包 光盘"))
        self.assertTrue(strict_text("STONEAGE2.0SETUP.EXE"))
        self.assertFalse(strict_text("Stone Age unrelated game"))

if __name__=="__main__":
    unittest.main()
