import json, unittest
from tools.stoneage_sa25_21cn_record20165_probe import ID,parse,relevant_attrs,token_hits
class T(unittest.TestCase):
    def test_id(self): self.assertEqual(ID,"20165")
    def test_parse(self):
        b=json.dumps([["timestamp","original"],["20020501000000","http://x/list.php?id=20165"]]).encode()
        self.assertEqual(parse(b)[0]["original"],"http://x/list.php?id=20165")
    def test_attrs(self):
        x=relevant_attrs('<a href="./downit.php?id=20165&num=0">d</a><img src="/file/game/maoxian/sa25up.jpg">')
        self.assertEqual(len(x),2)
    def test_token(self):
        b="石器时代2.5-精灵王传说".encode("gb2312")
        t=token_hits(b,b.decode("gb2312"))
        self.assertIn("石器时代2.5",t); self.assertIn("精灵王",t)
if __name__=="__main__": unittest.main()
