import json
import unittest
import urllib.parse

from tools.stoneage_sa25_sa25up_neighborhood_probe import (
    DIR, GAME_DIR, PAYLOAD, SOURCE, SOURCE_WWW, cdx_url, parse_available, parse_cdx
)


class SA25Sa25upNeighborhoodProbeTests(unittest.TestCase):
    def test_targets_are_pinned(self):
        self.assertEqual(PAYLOAD,"http://202.104.32.168/file/game/maoxian/sa25up.zip")
        self.assertEqual(DIR,"http://202.104.32.168/file/game/maoxian/")
        self.assertEqual(GAME_DIR,"http://202.104.32.168/file/game/")
        self.assertEqual(SOURCE,"http://pcpc.idv.tw/soft/soft.htm")
        self.assertEqual(SOURCE_WWW,"http://www.pcpc.idv.tw/soft/soft.htm")

    def test_cdx_prefix_query(self):
        p=urllib.parse.urlparse(cdx_url(DIR,"prefix",5000))
        q=urllib.parse.parse_qs(p.query)
        self.assertEqual(q["url"],[DIR])
        self.assertEqual(q["matchType"],["prefix"])
        self.assertEqual(q["from"],["2001"])
        self.assertEqual(q["to"],["2006"])

    def test_parse_cdx(self):
        b=json.dumps([
            ["timestamp","original","statuscode","mimetype","digest","length","redirect"],
            ["20020201000000",PAYLOAD,"200","application/zip","ABC","123",""],
        ]).encode()
        row=parse_cdx(b)[0]
        self.assertEqual(row["original"],PAYLOAD)
        self.assertEqual(row["digest"],"ABC")

    def test_parse_available(self):
        b=json.dumps({"archived_snapshots":{"closest":{"available":True,"timestamp":"20020201000000","status":"200","url":"x"}}}).encode()
        self.assertEqual(parse_available(b)["timestamp"],"20020201000000")

    def test_parse_unavailable(self):
        b=json.dumps({"archived_snapshots":{}}).encode()
        self.assertIsNone(parse_available(b))


if __name__=="__main__":
    unittest.main()
