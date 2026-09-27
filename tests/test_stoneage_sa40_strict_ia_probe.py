import unittest
from tools.stoneage_sa40_strict_ia_probe import QUERIES,strict

class SA40StrictIATests(unittest.TestCase):
    def test_queries_are_bounded(self):
        s=" ".join(q for _,q in QUERIES)
        self.assertIn("shiqi4updatex_02_11_08",s)
        self.assertIn("xinhaonanhai",s)
        self.assertIn("mediatype:software",s)

    def test_strict_metadata(self):
        self.assertTrue(strict({"title":"石器时代4.0 新九大家族"}))
        self.assertFalse(strict({"title":"Stone Age archaeology documentary"}))

if __name__=="__main__":
    unittest.main()
