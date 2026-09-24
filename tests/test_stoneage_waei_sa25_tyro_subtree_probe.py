import json
import unittest
import urllib.parse

from tools.stoneage_waei_sa25_tyro_subtree_probe import (
    DATE_FROM, DATE_TO, PREFIXES, cdx_url, parse_cdx, score,
)

class WaeiSA25TyroSubtreeProbeTests(unittest.TestCase):
    def test_grounded_window_and_prefix(self):
        self.assertEqual(DATE_FROM,"20020101")
        self.assertEqual(DATE_TO,"20020630")
        self.assertTrue(all("/stoneage2/tyro/" in p.lower() for _,p in PREFIXES))

    def test_cdx_includes_redirect_and_all_statuses(self):
        parsed=urllib.parse.urlparse(cdx_url(PREFIXES[0][1]))
        q=urllib.parse.parse_qs(parsed.query)
        self.assertEqual(q["matchType"],["prefix"])
        self.assertIn("redirect",q["fl"][0])
        self.assertNotIn("filter",q)

    def test_redirect_payload_scores_high(self):
        row={
            "original":"http://x/stoneage2/tyro/upgrade.asp",
            "statuscode":"302",
            "mimetype":"text/html",
            "redirect":"http://download.x/sa25.exe",
        }
        self.assertGreaterEqual(score(row),8)

    def test_parse_cdx(self):
        body=json.dumps([
            ["timestamp","original","statuscode","mimetype","digest","length","redirect"],
            ["20020201000000","http://x/upgrade.asp","302","text/html","A","1","http://x/a.exe"],
        ]).encode()
        self.assertEqual(parse_cdx(body)[0]["redirect"],"http://x/a.exe")

if __name__=="__main__":
    unittest.main()
