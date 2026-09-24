import json, unittest
from tools.stoneage_sa25_21cn_record8831_probe import ID,attrs,parse,token_hits
class T(unittest.TestCase):
    def test_id(self): self.assertEqual(ID,"8831")
    def test_parse(self):
        b=json.dumps([["timestamp","original"],["20020517231252","http://x/list.php?id=8831"]]).encode()
        self.assertEqual(parse(b)[0]["timestamp"],"20020517231252")
    def test_attrs(self):
        self.assertEqual(attrs('<img src="http://x/file/game/maoxian/sa25up.jpg">'),("http://x/file/game/maoxian/sa25up.jpg",))
    def test_token(self):
        b="石器时代".encode("gb2312"); self.assertIn("石器时代",token_hits(b,b.decode("gb2312")))
if __name__=="__main__": unittest.main()
