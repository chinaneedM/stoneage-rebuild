import json
import unittest

from tools.stoneage_sa25_21cn_native_record_probe import (
    PREFIX, TOKENS, matching_tokens, parse_cdx, relevant_hrefs
)


class SA2521CNNativeRecordProbeTests(unittest.TestCase):
    def test_prefix_is_native_detail_route(self):
        self.assertEqual(PREFIX,"http://202.104.32.168/list.php?id=")

    def test_tokens_cover_chinese_and_ascii(self):
        self.assertIn("石器时代",TOKENS)
        self.assertIn("精灵王",TOKENS)
        self.assertIn("StoneAge",TOKENS)
        self.assertIn("sa25up",TOKENS)

    def test_parse_only_numeric_list_ids(self):
        body=json.dumps([
            ["timestamp","original","statuscode","mimetype","digest","length"],
            ["20020201000000","http://202.104.32.168/list.php?id=123","200","text/html","A","1"],
            ["20020201000001","http://202.104.32.168/list.php?id=x","200","text/html","B","1"],
        ]).encode()
        rows=parse_cdx(body)
        self.assertEqual(len(rows),1)
        self.assertTrue(rows[0]["original"].endswith("id=123"))

    def test_matching_tokens_gb2312(self):
        body="石器时代2.5 精灵王传说".encode("gb2312")
        text=body.decode("gb2312")
        hits=matching_tokens(body,text)
        self.assertIn("石器时代",hits)
        self.assertIn("精灵王",hits)

    def test_relevant_hrefs(self):
        text='<a href="downit.php?id=123&num=0">x</a><a href="http://x/a">y</a>'
        self.assertEqual(relevant_hrefs(text),("downit.php?id=123&num=0",))


if __name__=="__main__":
    unittest.main()
