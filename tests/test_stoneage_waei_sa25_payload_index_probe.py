import json
import unittest
import urllib.parse

from tools.stoneage_waei_sa25_payload_index_probe import (
    DATE_FROM,
    DATE_TO,
    PREFIXES,
    candidate_score,
    cdx_url,
    parse_cdx,
)

class WaeiSA25PayloadIndexProbeTests(unittest.TestCase):
    def test_window_and_prefixes_are_pinned(self):
        self.assertEqual(DATE_FROM,"20020115")
        self.assertEqual(DATE_TO,"20020315")
        self.assertTrue(any("stoneage2" in p.lower() for _,p in PREFIXES))

    def test_cdx_prefix_query(self):
        parsed=urllib.parse.urlparse(cdx_url(PREFIXES[0][1]))
        q=urllib.parse.parse_qs(parsed.query)
        self.assertEqual(q["matchType"],["prefix"])
        self.assertEqual(q["from"],[DATE_FROM])
        self.assertEqual(q["to"],[DATE_TO])

    def test_payload_scores_high(self):
        row={"original":"http://x/stoneage2/download/sa25setup.exe","mimetype":"application/octet-stream"}
        self.assertGreaterEqual(candidate_score(row),8)

    def test_qqskin_is_demoted(self):
        good={"original":"http://x/stoneage2/download/sa25setup.exe","mimetype":"application/octet-stream"}
        skin={"original":"http://x/stoneage2/qqskin/160.zip","mimetype":"application/zip"}
        self.assertGreater(candidate_score(good),candidate_score(skin))

    def test_parse_cdx(self):
        body=json.dumps([
            ["timestamp","original","statuscode","mimetype","digest","length"],
            ["20020201000000","http://x/a.exe","200","application/octet-stream","ABC","1"],
        ]).encode()
        self.assertEqual(parse_cdx(body)[0]["digest"],"ABC")

if __name__=="__main__":
    unittest.main()
