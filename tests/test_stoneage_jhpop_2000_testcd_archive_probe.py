import unittest
import urllib.parse

from tools.stoneage_jhpop_2000_testcd_archive_probe import (
    CONTROL_FROM,
    CONTROL_TO,
    FROM,
    TO,
    TARGETS,
    cdx_url,
    is_binary,
    score,
)


class JHPOP2000TestCDArchiveProbeTests(unittest.TestCase):
    def test_launch_window_covers_public_test(self):
        self.assertLessEqual(FROM, "20001215")
        self.assertGreaterEqual(TO, "20010110")

    def test_control_extends_beyond_launch_window(self):
        self.assertLessEqual(CONTROL_FROM, "20010101")
        self.assertGreaterEqual(CONTROL_TO, "20010315")

    def test_domain_target_present(self):
        self.assertTrue(any(row[2] == "domain" and row[1] == "jhpop.com" for row in TARGETS))

    def test_cdx_keeps_all_statuses_but_collapses_urlkey(self):
        url = cdx_url("jhpop.com", "domain", FROM, TO)
        q = urllib.parse.parse_qs(urllib.parse.urlsplit(url).query)
        self.assertNotIn("filter", q)
        self.assertEqual(q["collapse"], ["urlkey"])
        self.assertIn("redirect", q["fl"][0])

    def test_candidate_scoring_and_binary_detection(self):
        self.assertTrue(is_binary("http://www.jhpop.com/download/StoneAgeBeta.exe"))
        value, tokens = score("http://www.jhpop.com/download/StoneAgeBeta.exe")
        self.assertGreaterEqual(value, 30)
        self.assertIn("stoneage", tokens)
        self.assertIn("binary-ext", tokens)


if __name__ == "__main__":
    unittest.main()
