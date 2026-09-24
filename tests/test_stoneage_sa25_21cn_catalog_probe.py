import json
import unittest
import urllib.parse

from tools.stoneage_sa25_21cn_catalog_probe import (
    PREFIX, cdx_url, page_id, parse_cdx, strong_match, interesting_hrefs
)


class SA2521CNCatalogProbeTests(unittest.TestCase):
    def test_cdx_scope(self):
        p=urllib.parse.urlparse(cdx_url())
        q=urllib.parse.parse_qs(p.query)
        self.assertEqual(q["url"],[PREFIX])
        self.assertEqual(q["matchType"],["prefix"])
        self.assertEqual(q["from"],["2001"])
        self.assertEqual(q["to"],["2004"])

    def test_parse_list_rows_only(self):
        body=json.dumps([
            ["timestamp","original","statuscode","mimetype","digest","length"],
            ["20020201000000","http://202.104.32.168/list.php?id=99","200","text/html","A","1"],
            ["20020201000001","http://202.104.32.168/file/x","200","text/html","B","1"],
        ]).encode()
        rows=parse_cdx(body)
        self.assertEqual(len(rows),1)
        self.assertEqual(page_id(rows[0]["original"]),"99")

    def test_strong_tokens(self):
        self.assertTrue(strong_match("<title>石器时代2.5</title>",""))
        self.assertTrue(strong_match("x","http://x/sa25up.zip"))
        self.assertFalse(strong_match("ordinary software","ordinary software"))

    def test_interesting_hrefs(self):
        text='<a href="http://202.104.32.168/file/game/maoxian/sa25up.zip">x</a><a href="x">y</a>'
        self.assertEqual(
            interesting_hrefs(text),
            ("http://202.104.32.168/file/game/maoxian/sa25up.zip",),
        )


if __name__=="__main__":
    unittest.main()
