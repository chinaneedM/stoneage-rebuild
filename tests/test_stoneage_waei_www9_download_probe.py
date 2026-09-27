import json,unittest
from tools.stoneage_waei_www9_download_probe import parse,is_binary,score_row,semantic
class Www9Tests(unittest.TestCase):
    def test_parse(self):
        b=json.dumps([["timestamp","original"],["20010101","http://x/a"]]).encode()
        self.assertEqual(parse(b)[0]["timestamp"],"20010101")
    def test_binary(self):
        self.assertTrue(is_binary("http://x/sa.exe"));self.assertFalse(is_binary("http://x/a.php"))
    def test_score(self):
        self.assertGreater(score_row({"original":"http://x/download.php","timestamp":"20010101"}),0)
    def test_semantic(self):
        _,s,t,z=semantic("<html>StoneAge 試玩版 274MB</html>")
        self.assertTrue(s);self.assertTrue(t);self.assertIn("274",z)
if __name__=="__main__":unittest.main()
