import unittest
import urllib.parse

from tools.stoneage_yegame_2000_testcd_archive_probe import (
    FROM,
    ROOT_FROM,
    ROOT_TO,
    TARGETS,
    TO,
    cdx_url,
    is_binary,
    score,
)


class Yegame2000TestCDArchiveProbeTests(unittest.TestCase):
    def test_launch_window_covers_jhpop_redirect_and_public_test(self):
        self.assertLessEqual(FROM, "20001204")
        self.assertLessEqual(FROM, "20001215")
        self.assertGreaterEqual(TO, "20010110")

    def test_root_control_covers_redirect_date(self):
        self.assertLessEqual(ROOT_FROM, "20001204")
        self.assertGreaterEqual(ROOT_TO, "20001204")

    def test_domain_and_root_targets_present(self):
        self.assertTrue(any(t[1] == "yegame.com" and t[2] == "domain" for t in TARGETS))
        self.assertTrue(any(t[1] == "http://www.yegame.com/" and t[2] == "exact" for t in TARGETS))

    def test_cdx_keeps_statuses_and_collapses_urlkey(self):
        url = cdx_url("yegame.com", "domain", FROM, TO)
        q = urllib.parse.parse_qs(urllib.parse.urlsplit(url).query)
        self.assertNotIn("filter", q)
        self.assertEqual(q["collapse"], ["urlkey"])
        self.assertIn("redirect", q["fl"][0])

    def test_scoring_does_not_count_game_from_hostname(self):
        value, tokens = score("http://www.yegame.com/")
        self.assertEqual(value, 0)
        self.assertEqual(tokens, ())

    def test_high_value_path_scoring(self):
        value, tokens = score("http://www.yegame.com/download/stoneage_beta.exe")
        self.assertTrue(is_binary("http://www.yegame.com/download/stoneage_beta.exe"))
        self.assertGreaterEqual(value, 60)
        self.assertIn("stoneage", tokens)
        self.assertIn("beta", tokens)
        self.assertIn("download", tokens)
        self.assertIn("binary-ext", tokens)


if __name__ == "__main__":
    unittest.main()
