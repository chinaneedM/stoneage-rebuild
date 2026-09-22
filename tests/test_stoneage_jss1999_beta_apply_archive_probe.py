import json
import unittest

from tools.stoneage_jss1999_beta_apply_archive_probe import (
    PATTERNS,
    arquivo_url,
    candidate_detail,
    parse_arquivo,
    parse_wayback,
    wayback_url,
)


class Jss1999BetaApplyArchiveProbeTests(unittest.TestCase):
    def test_patterns_preserve_wildcard_instead_of_guessing_character(self):
        self.assertIn(
            ("www-dp-tail","www.dp.gamersdream.ne.jp/*PO/sa_apply.html"),
            PATTERNS,
        )
        self.assertFalse(any("~PO/sa_apply.html" in pattern for _,pattern in PATTERNS))

    def test_candidate_detail_reports_literal_character_only(self):
        detail=candidate_detail(
            "http://www.dp.gamersdream.ne.jp/~PO/sa_apply.html"
        )
        self.assertTrue(detail["matches_tail"])
        self.assertEqual(detail["path"],"/~PO/sa_apply.html")
        self.assertEqual(detail["prefix_before_po"],"/~")
        self.assertEqual(detail["immediate_before_po"],"~")

    def test_nonmatching_path_is_not_promoted(self):
        detail=candidate_detail(
            "http://www.dp.gamersdream.ne.jp/PO/other.html"
        )
        self.assertFalse(detail["matches_tail"])

    def test_wayback_json_rows_are_normalized_by_header(self):
        raw=json.dumps([
            ["timestamp","original","statuscode"],
            ["19990801010101","http://x/~PO/sa_apply.html","200"],
        ]).encode()
        self.assertEqual(
            parse_wayback(raw)[0]["original"],
            "http://x/~PO/sa_apply.html",
        )

    def test_arquivo_ndjson_is_accepted(self):
        raw=(
            b'{"timestamp":"19990801010101",'
            b'"url":"http://x/~PO/sa_apply.html","status":"200"}\n'
        )
        self.assertEqual(
            parse_arquivo(raw)[0]["url"],
            "http://x/~PO/sa_apply.html",
        )

    def test_queries_are_bounded_to_1999(self):
        self.assertIn("from=1999",wayback_url(PATTERNS[0][1]))
        self.assertIn("to=1999",wayback_url(PATTERNS[0][1]))
        self.assertIn("from=1999",arquivo_url(PATTERNS[0][1]))
        self.assertIn("to=1999",arquivo_url(PATTERNS[0][1]))


if __name__=="__main__":
    unittest.main()
