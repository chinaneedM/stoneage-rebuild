import unittest
from tools.stoneage_early_client_discmaster_signature_probe import SIGNATURES, search_url, exact_leaf


class TestEarlyClientDiscMasterSignatures(unittest.TestCase):
    def test_verified_signature_set(self):
        names={name for _,name,_ in SIGNATURES}
        self.assertIn("real_1.bin",names)
        self.assertIn("adrn_1.bin",names)
        self.assertIn("spr_1.bin",names)
        self.assertIn("spradrn_1.bin",names)
        self.assertIn("sa_3.exe",names)

    def test_query_is_filename_index_and_early_window(self):
        url=search_url("real_1.bin")
        self.assertIn("qfields=name",url)
        self.assertIn("tsMin=1999",url)
        self.assertIn("tsMax=2002",url)

    def test_exact_leaf(self):
        self.assertTrue(exact_leaf({"fileid":"StoneAge/data/real_1.bin"},"real_1.bin"))
        self.assertFalse(exact_leaf({"fileid":"StoneAge/data/real_10.bin"},"real_1.bin"))


if __name__=="__main__":
    unittest.main()
