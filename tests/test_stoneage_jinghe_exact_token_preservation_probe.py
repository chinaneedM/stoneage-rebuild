import unittest
from tools.stoneage_jinghe_exact_token_preservation_probe import TOKENS,ia_url,dm_url
class ExactTokenTests(unittest.TestCase):
    def test_tokens(self):
        vals=dict(TOKENS)
        self.assertEqual(vals["client-code"],"EN0ZGKJ0002")
        self.assertEqual(vals["cover-md5"],"980e7d3336fa7557c166f2ff8ba3957c")
    def test_urls(self):
        self.assertIn("advancedsearch.php",ia_url("EN0ZGKJ0002"))
        self.assertIn("qfields=name",dm_url("EN0ZGKJ0002","name"))
if __name__=="__main__": unittest.main()
