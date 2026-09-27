import unittest
from tools.stoneage_yegame_product_code_filename_residual import CODE, url

class T(unittest.TestCase):
    def test_query(self):
        self.assertEqual(CODE,"EN0ZGKJ0002")
        u=url()
        self.assertIn("qfields=name",u)
        self.assertIn("EN0ZGKJ0002",u)

if __name__=="__main__":
    unittest.main()
