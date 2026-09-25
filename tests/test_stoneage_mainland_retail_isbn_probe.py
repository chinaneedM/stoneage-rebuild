import unittest
from tools.stoneage_mainland_retail_isbn_probe import QUERIES,strict_match

class MainlandRetailISBNProbeTests(unittest.TestCase):
    def test_exact_identifiers_present(self):
        self.assertIn("7-900032-57-0",QUERIES)
        self.assertIn("9787900032570",QUERIES)

    def test_exact_identifier_is_strict(self):
        self.assertTrue(strict_match("ISBN 7-900032-57-0"))
        self.assertTrue(strict_match("barcode 9787900032570"))

    def test_operator_plus_title_is_strict(self):
        self.assertTrue(strict_match("北京华义 StoneAge 石器时代"))
        self.assertFalse(strict_match("StoneAge unrelated fan package"))

if __name__=="__main__":
    unittest.main()
