import unittest
from tools.stoneage_old_disc_torrent_signature_probe import basename, classify

class SignatureProbeTests(unittest.TestCase):
    def test_exact_client_signature(self):
        exact, lexical=classify("disc/data/StoneAge.exe")
        self.assertIn("stoneage.exe",exact)
        self.assertIn("stoneage",lexical)
    def test_resource_signature(self):
        exact,_=classify("SA/data/adrn_1.bin")
        self.assertEqual(exact,("adrn_1.bin",))
    def test_chinese_title(self):
        exact,lexical=classify("收藏/石器时代2.5/客户端.iso")
        self.assertFalse(exact)
        self.assertIn("石器时代",lexical)
    def test_unrelated_stone_age_words(self):
        exact,lexical=classify("docs/stone_age_history.pdf")
        self.assertFalse(exact)
        self.assertFalse(lexical)
    def test_wanfang_identifier(self):
        _,lexical=classify("catalog/9787900096074.jpg")
        self.assertIn("9787900096074",lexical)
    def test_backslash_basename(self):
        self.assertEqual(basename(r"DATA\\SPRADRN_1.BIN"),"spradrn_1.bin")

if __name__=="__main__":
    unittest.main()
