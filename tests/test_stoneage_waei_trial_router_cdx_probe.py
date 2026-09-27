import unittest
import urllib.parse

from tools.stoneage_waei_trial_router_cdx_probe import (
    CONTROL_FROM,
    CONTROL_TO,
    EARLY_FROM,
    EARLY_TO,
    TARGETS,
    cdx_url,
    fileid,
    is_file,
    is_router,
    stone_hint,
)


class WaeiTrialRouterCdxProbeTests(unittest.TestCase):
    def test_early_window_covers_trial_date(self):
        self.assertLessEqual(EARLY_FROM, "20010104")
        self.assertGreaterEqual(EARLY_TO, "20010104")

    def test_control_window_covers_known_fileid133_capture(self):
        self.assertLessEqual(CONTROL_FROM, "20010605")
        self.assertGreaterEqual(CONTROL_TO, "20010605")

    def test_cdx_query_keeps_redirects_and_capture_history(self):
        url = cdx_url(
            "http://www7.waei.net/download/download.asp",
            "prefix",
            EARLY_FROM,
            EARLY_TO,
        )
        parsed = urllib.parse.urlsplit(url)
        q = urllib.parse.parse_qs(parsed.query)
        self.assertNotIn("filter", q)
        self.assertNotIn("collapse", q)
        self.assertEqual(q["matchType"], ["prefix"])
        self.assertIn("statuscode", q["fl"][0])
        self.assertIn("redirect", q["fl"][0])

    def test_known_302_route_is_positive_control(self):
        urls = [row[1] for row in TARGETS if row[0].startswith("control-fileid133")]
        self.assertTrue(any("fileid=133" in url.lower() for url in urls))
        self.assertEqual(fileid("http://x/download.asp?fileid=133"), "133")

    def test_route_classification(self):
        self.assertTrue(is_router("http://www7.waei.net/download/download.asp?fileid=133"))
        self.assertTrue(is_file("http://www7.waei.net/download/file/x/spr_1.bin"))
        self.assertTrue(stone_hint("http://x/file/StoneAgeTrial.exe"))
        self.assertFalse(stone_hint("http://x/file/railway.zip"))


if __name__ == "__main__":
    unittest.main()
