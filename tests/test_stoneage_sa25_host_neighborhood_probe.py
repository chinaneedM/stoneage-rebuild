import json
import unittest
import urllib.parse

from tools.stoneage_sa25_host_neighborhood_probe import (
    HOST, cdx_url, html_identity_candidate, parse_cdx, same_host_anchors
)


class SA25HostNeighborhoodProbeTests(unittest.TestCase):
    def test_same_host_anchor_extraction(self):
        text=(
            '<a href="http://202.104.32.168/file/game/maoxian/sa25up.zip">石器時代2.5</a>'
            '<a href="http://example.com/x">other</a>'
        )
        rows=same_host_anchors(text)
        self.assertEqual(len(rows),1)
        self.assertEqual(rows[0][1],"石器時代2.5")

    def test_cdx_window_and_prefix(self):
        u=cdx_url(f"http://{HOST}/",True,3000)
        q=urllib.parse.parse_qs(urllib.parse.urlparse(u).query)
        self.assertEqual(q["matchType"],["prefix"])
        self.assertEqual(q["from"],["2001"])
        self.assertEqual(q["to"],["2004"])
        self.assertEqual(q["filter"],["statuscode:200"])

    def test_parse_cdx(self):
        body=json.dumps([
            ["timestamp","original","statuscode","mimetype","digest","length","redirect"],
            ["20030101000000","http://202.104.32.168/","200","text/html","A","1",""],
        ]).encode()
        self.assertEqual(parse_cdx(body)[0]["statuscode"],"200")

    def test_identity_candidate(self):
        self.assertTrue(html_identity_candidate({"original":"http://202.104.32.168/index.htm","mimetype":"text/html"}))
        self.assertFalse(html_identity_candidate({"original":"http://202.104.32.168/file/game/x.zip","mimetype":"application/zip"}))


if __name__=="__main__":
    unittest.main()
