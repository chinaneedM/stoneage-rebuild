import json
import unittest
from tools.stoneage_sa25_21cn_category_probe import (
    PREFIX, extract_list_ids, parse_cdx, relevant_hrefs, token_hits
)

class SA2521CNCategoryProbeTests(unittest.TestCase):
    def test_prefix(self):
        self.assertEqual(PREFIX,"http://202.104.32.168/second.php")

    def test_parse(self):
        body=json.dumps([
            ["timestamp","original","statuscode","mimetype","digest","length"],
            ["20020101000000","http://202.104.32.168/second.php?id=1","200","text/html","A","1"],
            ["20020101000001","http://202.104.32.168/list.php?id=1","200","text/html","B","1"],
        ]).encode()
        self.assertEqual(len(parse_cdx(body)),1)

    def test_extract_list_ids(self):
        text='<a href="list.php?id=123">石器时代</a><a href="/list.php?foo=1&id=456">x</a>'
        self.assertEqual(extract_list_ids(text),("123","456"))

    def test_token_hits(self):
        body="石器时代2.5 精灵王传说".encode("gb2312")
        text=body.decode("gb2312")
        hits=token_hits(body,text)
        self.assertIn("石器时代",hits)
        self.assertIn("精灵王",hits)

    def test_relevant_hrefs(self):
        self.assertEqual(relevant_hrefs('<a href="list.php?id=9">x</a><a href="x">y</a>'),("list.php?id=9",))

if __name__=="__main__":
    unittest.main()
