import unittest
from tools.stoneage_sa40_global_ia_probe import QUERIES
class GlobalIATests(unittest.TestCase):
    def test_product_tokens_present(self):
        s=" ".join(QUERIES)
        self.assertIn("新九大家族",s);self.assertIn("新满意足",s);self.assertIn("新高采烈",s)
if __name__=="__main__":unittest.main()
