import unittest
from tools.stoneage_2001_discmaster_item41879_probe import ITEM, QUERIES, search_url, classify_paths

class DiscMaster41879Tests(unittest.TestCase):
    def test_item_is_pinned(self):
        self.assertEqual(ITEM,"41879")
        u=search_url("setup.exe")
        self.assertIn("itemid=41879",u)
        self.assertIn("mode=deep",u)

    def test_bare_node_is_not_promoted_to_client(self):
        rows=[{"fileid":"STONEAGE2"}]
        bare,descendants,exact=classify_paths(rows)
        self.assertEqual(len(bare),1)
        self.assertEqual(descendants,[])
        self.assertEqual(exact,[])

    def test_descendant_and_exact_identity_are_distinct(self):
        rows=[{"fileid":"disc/STONEAGE2/readme.txt"},{"fileid":"disc/STONEAGE2/stoneage.exe"}]
        bare,descendants,exact=classify_paths(rows)
        self.assertEqual(bare,[])
        self.assertEqual(len(descendants),2)
        self.assertEqual(len(exact),1)

    def test_queries_include_exact_client_and_directory(self):
        self.assertIn("STONEAGE2",QUERIES)
        self.assertIn("stoneage2.0setup.exe",QUERIES)
        self.assertIn("setup.exe",QUERIES)

if __name__=="__main__":
    unittest.main()
