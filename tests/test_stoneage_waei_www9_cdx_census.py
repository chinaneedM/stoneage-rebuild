import json,unittest
from tools.stoneage_waei_www9_cdx_census import parse,binary,params
class Tests(unittest.TestCase):
    def test_parse(self):
        b=json.dumps([["timestamp","original"],["1","http://x"]]).encode();self.assertEqual(len(parse(b)),1)
    def test_binary(self):self.assertTrue(binary("http://x/A.EXE"));self.assertFalse(binary("http://x/a.php"))
    def test_params(self):self.assertIn("Dcat_ID=5",params("http://x/download.php?Dcat_ID=5"))
if __name__=="__main__":unittest.main()
