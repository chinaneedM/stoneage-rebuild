import unittest
from tools.stoneage_2001_discmaster_item41879_probe import ITEM, QUERIES, search_url

class DiscMaster41879Tests(unittest.TestCase):
    def test_item_is_pinned(self):
        self.assertEqual(ITEM,"41879")
        u=search_url("setup.exe")
        self.assertIn("itemid=41879",u)
        self.assertIn("mode=deep",u)

    def test_queries_include_exact_client_and_directory(self):
        self.assertIn("STONEAGE2",QUERIES)
        self.assertIn("stoneage2.0setup.exe",QUERIES)
        self.assertIn("setup.exe",QUERIES)

if __name__=="__main__":
    unittest.main()
