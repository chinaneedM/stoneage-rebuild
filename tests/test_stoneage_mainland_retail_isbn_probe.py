import unittest
from tools.stoneage_mainland_retail_isbn_probe import HYPOTHESIS_QUERIES,QUERIES,query_kind,strict_match

class MainlandRetailISBNProbeTests(unittest.TestCase):
    def test_initial_and_checksum_hypotheses_present(self):
        self.assertIn("7-900032-57-0",QUERIES)
        self.assertIn("9787900032570",QUERIES)
        self.assertIn("7-900032-57-6",HYPOTHESIS_QUERIES)
        self.assertIn("9787900032577",HYPOTHESIS_QUERIES)
        self.assertEqual(query_kind("9787900032577"),"checksum-consistent-hypothesis")

    def test_identifier_strings_are_strict_search_leads(self):
        self.assertTrue(strict_match("ISBN 7-900032-57-0"))
        self.assertTrue(strict_match("barcode 9787900032570"))
        self.assertTrue(strict_match("ISBN 7-900032-57-6"))
        self.assertTrue(strict_match("barcode 9787900032577"))

    def test_operator_plus_title_is_strict(self):
        self.assertTrue(strict_match("北京华义 StoneAge 石器时代"))
        self.assertFalse(strict_match("StoneAge unrelated fan package"))

if __name__=="__main__":
    unittest.main()
