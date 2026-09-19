import json
import unittest

from tools.stoneage_gametime_download_redirect_cdx_probe import (
    cdx_url,
    interesting,
    parse,
)


class GameTimeDownloadRedirectCdxProbeTests(unittest.TestCase):
    def test_cdx_query_keeps_redirects_and_has_no_200_filter(self):
        url=cdx_url("http://www.gametime.co.kr/data/download.asp")
        self.assertIn("matchType=prefix",url)
        self.assertIn("redirect",url)
        self.assertNotIn("statuscode%3A200",url)

    def test_parse_includes_redirect_field(self):
        body=json.dumps([
            ["urlkey","timestamp","original","mimetype","statuscode","digest","length","redirect"],
            ["k","20010101000000","http://www.gametime.co.kr/data/download.asp?GW_IDX=9&GW_Name=Online",
             "text/html","302","-","0","http://pds.gametime.co.kr/files/stone.exe"],
        ]).encode()
        rows=parse(body)
        self.assertEqual(rows[0]["statuscode"],"302")
        self.assertIn("stone.exe",rows[0]["redirect"])
        self.assertTrue(interesting(rows[0]))

    def test_unrelated_redirect_is_not_interesting(self):
        self.assertFalse(interesting({
            "original":"http://www.gametime.co.kr/data/download.asp?GW_IDX=55&GW_Name=Online",
            "redirect":"http://example.com/foo.bin",
        }))


if __name__=="__main__":
    unittest.main()
