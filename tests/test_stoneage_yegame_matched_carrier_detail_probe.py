import unittest
from tools.stoneage_yegame_matched_carrier_detail_probe import TARGET, LEVELS, walk

class T(unittest.TestCase):
    def test_target(self):
        self.assertEqual(TARGET,"22636573895893")
        self.assertIn("simple",LEVELS)

    def test_public_product_fields(self):
        rows=dict(walk({"data":[{"name":"StoneAge","product_code":"ABC123"}]}))
        self.assertEqual(rows["data[0].name"],"StoneAge")
        self.assertEqual(rows["data[0].product_code"],"ABC123")

if __name__=="__main__":
    unittest.main()
