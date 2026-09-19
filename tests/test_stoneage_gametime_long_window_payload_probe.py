import unittest

from tools.stoneage_gametime_long_window_payload_probe import query_url, variants


class GameTimeLongWindowPayloadProbeTests(unittest.TestCase):
    def test_variants_cover_payloads_and_host_forms(self):
        rows=variants()
        urls={url for _,url in rows}
        self.assertIn(
            "http://www.gametime.co.kr/images/Online/pds/2001/02/onlStoneAge.zip",
            urls,
        )
        self.assertIn(
            "https://gametime.co.kr/images/Online/pds/2001/02/stone_demo.exe",
            urls,
        )
        self.assertIn(
            "http://www.gametime.co.kr:80/images/Online/pds/2001/02/onlStoneAge.zip",
            urls,
        )

    def test_query_uses_long_window_without_status_filter(self):
        url=query_url(
            "http://www.gametime.co.kr/images/Online/pds/2001/02/onlStoneAge.zip"
        )
        self.assertIn("from=2000",url)
        self.assertIn("to=2012",url)
        self.assertNotIn("filter=",url)


if __name__=="__main__":
    unittest.main()
