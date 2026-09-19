import json
import unittest

from tools.stoneage_korean_distribution_cdx_prefix_probe import (
    TARGETS,
    cdx_url,
    parse_response,
    relevant,
)


class KoreanDistributionCdxPrefixProbeTests(unittest.TestCase):
    def test_cdx_url_is_prefix_scoped_and_dated(self):
        url=cdx_url("http://stoneage.hananet.net/down/")
        self.assertIn("matchType=prefix",url)
        self.assertIn("from=2000",url)
        self.assertIn("to=2002",url)

    def test_parse_response_maps_header(self):
        body=json.dumps([
            ["timestamp","original","mimetype","statuscode","digest","length"],
            ["20010101000000","http://stoneage.hananet.net/down/sa.exe","application/octet-stream","200","ABC","123"],
        ]).encode()
        rows=parse_response(body)
        self.assertEqual(rows[0]["original"],"http://stoneage.hananet.net/down/sa.exe")
        self.assertEqual(rows[0]["length"],"123")

    def test_relevant_prefers_payload_like_tail(self):
        self.assertTrue(relevant({"original":"http://x/down/sa_demo.exe"}))
        self.assertTrue(relevant({"original":"http://x/down/patch101.zip"}))
        self.assertTrue(relevant({"original":"http://www.gametime.co.kr/images/Online/pds/2001/02/onlStoneAge.zip"}))
        self.assertFalse(relevant({"original":"http://x/down/banner.gif"}))

    def test_gametime_image_pds_prefix_registered(self):
        urls={url for _,url in TARGETS}
        self.assertIn("http://www.gametime.co.kr/images/Online/pds/2001/02/",urls)


if __name__=="__main__":
    unittest.main()
