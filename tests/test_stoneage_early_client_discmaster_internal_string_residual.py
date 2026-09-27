import unittest
from tools.stoneage_early_client_discmaster_internal_string_residual import TERMS, search_url


class TestInternalStringResidual(unittest.TestCase):
    def test_failed_terms_only(self):
        terms={term for _,term,_ in TERMS}
        self.assertEqual(terms,{
            "/saupdate/newest.txt",
            "spradrn_1.bin",
            "battletxt_1.txt",
            "soundaddr_1.txt",
        })

    def test_fulltext_query(self):
        url=search_url("/saupdate/newest.txt")
        self.assertIn("qfields=t",url)
        self.assertIn("tsMin=1999",url)
        self.assertIn("tsMax=2002",url)


if __name__=="__main__":
    unittest.main()
