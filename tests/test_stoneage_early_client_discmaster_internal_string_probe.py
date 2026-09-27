import unittest
from tools.stoneage_early_client_discmaster_internal_string_probe import SIGNATURES, search_url


class TestEarlyClientInternalStrings(unittest.TestCase):
    def test_anchor_terms(self):
        terms={term for _,term,kind in SIGNATURES if kind=="anchor"}
        self.assertIn("stoneage.waei.net",terms)
        self.assertIn("/saupdate/newest.txt",terms)

    def test_fulltext_early_window(self):
        url=search_url("stoneage.waei.net")
        self.assertIn("qfields=t",url)
        self.assertIn("tsMin=1999",url)
        self.assertIn("tsMax=2002",url)


if __name__=="__main__":
    unittest.main()
