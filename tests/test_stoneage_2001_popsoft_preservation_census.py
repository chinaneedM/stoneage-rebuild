import unittest
from tools.stoneage_2001_popsoft_preservation_census import (
    parse_year_month, metadata_exists, interesting_file
)

class PopsoftPreservationCensusTests(unittest.TestCase):
    def test_parse_year_month(self):
        self.assertEqual(parse_year_month("popsoftcd-1998-11"),(1998,11))
        self.assertEqual(parse_year_month("popsoftcd-2001-11-alt"),(2001,11))
        self.assertEqual(parse_year_month("other"),(None,None))

    def test_metadata_exists(self):
        self.assertTrue(metadata_exists({"metadata":{"identifier":"popsoftcd-2001-11"}},"popsoftcd-2001-11"))
        self.assertFalse(metadata_exists({"metadata":{"identifier":"other"}},"popsoftcd-2001-11"))

    def test_interesting_file(self):
        self.assertTrue(interesting_file("GAMES/StoneAge/SETUP.EXE"))
        self.assertTrue(interesting_file("soft/stoneage2.0setup.exe"))
        self.assertFalse(interesting_file("images/logo.jpg"))

if __name__=="__main__":
    unittest.main()
