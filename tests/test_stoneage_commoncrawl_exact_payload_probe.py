import unittest
from tools.stoneage_commoncrawl_exact_payload_probe import (
    EXACT_TARGETS,
    PREFIX_TARGETS,
    clean,
    is_relevant,
    query_url,
)


class CommonCrawlExactPayloadProbeTests(unittest.TestCase):
    def test_clean(self):
        self.assertEqual(clean("a|b\n c"),"a%7Cb c")

    def test_prefix_query_requests_prefix_mode_and_limit(self):
        url=query_url("https://index.commoncrawl.org/CC-MAIN-X-index","http://example.com/down/","prefix")
        self.assertIn("matchType=prefix",url)
        self.assertIn("limit=100",url)

    def test_japan_174a_official_launch_targets_are_pinned(self):
        self.assertIn(
            (
                "japan174a-hangame-launch",
                "http://hangame.gamania.co.jp/stoneage/sa174hg.exe",
            ),
            EXACT_TARGETS,
        )
        self.assertIn(
            (
                "japan174a-hangame-prefix",
                "http://hangame.gamania.co.jp/stoneage/",
            ),
            PREFIX_TARGETS,
        )

    def test_relevant_mirror_tokens(self):
        self.assertTrue(is_relevant("http://stoneage.hananet.net/down/sa_demo.exe"))
        self.assertTrue(is_relevant("http://www.gagamel.com/web_data/download/stoneagebeta.zip"))
        self.assertTrue(is_relevant("http://pds.hananet.net/view.asp?app_id=20001031524596220&type=C03"))
        self.assertTrue(is_relevant("http://www.gametime.co.kr/images/Online/pds/2001/02/onlStoneAge.zip"))
        self.assertTrue(is_relevant("http://www.gametime.co.kr/images/Online/pds/2001/02/stone_demo.exe"))
        self.assertTrue(
            is_relevant("http://hangame.gamania.co.jp/stoneage/sa174hg.exe")
        )
        self.assertFalse(is_relevant("http://korea.cnet.com/pc/games/online/unrelated.zip"))


if __name__=="__main__":
    unittest.main()
