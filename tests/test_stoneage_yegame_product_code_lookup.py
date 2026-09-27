import unittest
from tools.stoneage_yegame_product_code_lookup import CODE, QUERIES

class T(unittest.TestCase):
    def test_code(self):
        self.assertEqual(CODE,"EN0ZGKJ0002")
        self.assertIn(CODE,QUERIES)

if __name__=="__main__":
    unittest.main()
