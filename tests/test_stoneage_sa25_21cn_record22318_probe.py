import json
import unittest
import urllib.parse

from tools.stoneage_sa25_21cn_record22318_probe import (
    CONTROL_ID, TARGET_ID, cdx_url, parse_cdx, relevant_attrs
)


class SA2521CNRecord22318Tests(unittest.TestCase):
    def test_ids_pinned(self):
        self.assertEqual(TARGET_ID,"22318")
        self.assertEqual(CONTROL_ID,"8247")

    def test_cdx_prefix_for_downit(self):
        u=cdx_url("http://202.104.32.168/downit.php?id=22318","prefix",500)
        q=urllib.parse.parse_qs(urllib.parse.urlparse(u).query)
        self.assertEqual(q["matchType"],["prefix"])
        self.assertEqual(q["from"],["2001"])
        self.assertEqual(q["to"],["2005"])

    def test_parse_cdx_redirect(self):
        body=json.dumps([
            ["timestamp","original","statuscode","mimetype","digest","length","redirect"],
            ["20020825000000","http://x/downit.php?id=22318&num=0","302","text/html","A","1","http://x/file/game/a.zip"],
        ]).encode()
        row=parse_cdx(body)[0]
        self.assertEqual(row["redirect"],"http://x/file/game/a.zip")

    def test_relevant_attrs(self):
        text='<a href="./downit.php?id=22318&num=0">x</a><img src="/file/game/maoxian/sa25up.jpg">'
        got=relevant_attrs(text)
        self.assertEqual(len(got),2)


if __name__=="__main__":
    unittest.main()
