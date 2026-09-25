import unittest
from tools.stoneage_sa20_retail_carrier_residual import QUERIES,strict

class SA20RetailResidualTests(unittest.TestCase):
    def test_queries_are_fielded(self):
        for _,q in QUERIES:
            self.assertTrue(any(f in q for f in ("title:","description:","identifier:")))
        self.assertIn("老手削暴包","\n".join(q for _,q in QUERIES))

    def test_strict(self):
        self.assertTrue(strict({"title":"石器时代2.0老手削暴包"}))
        self.assertTrue(strict({"description":"mirror stoneage2.0setup.exe"}))
        self.assertFalse(strict({"title":"unrelated software"}))

if __name__=="__main__":
    unittest.main()
