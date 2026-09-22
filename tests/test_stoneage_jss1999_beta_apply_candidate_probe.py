import unittest

from tools.stoneage_jss1999_beta_apply_candidate_probe import (
    CANDIDATES,
    KEY_DATES,
    candidate_period_hit,
    parse_closest,
    query_url,
)


class Jss1999BetaApplyCandidateProbeTests(unittest.TestCase):
    def test_candidate_set_is_explicit_and_small(self):
        urls=dict(CANDIDATES)
        self.assertEqual(
            urls["tilde-userdir"],
            "http://www.dp.gamersdream.ne.jp/~PO/sa_apply.html",
        )
        self.assertEqual(
            urls["plain-po"],
            "http://www.dp.gamersdream.ne.jp/PO/sa_apply.html",
        )
        self.assertLessEqual(len(CANDIDATES),5)

    def test_dates_are_only_beta_application_window(self):
        self.assertEqual(KEY_DATES[0],"19990801")
        self.assertEqual(KEY_DATES[-1],"19990930")
        self.assertTrue(all(date.startswith("1999") for date in KEY_DATES))

    def test_parse_closest_and_period_gate(self):
        row=parse_closest({
            "archived_snapshots":{
                "closest":{
                    "available":True,
                    "timestamp":"19990819123456",
                    "status":"200",
                    "url":"http://web.archive.org/web/19990819123456/http://x/",
                }
            }
        })
        self.assertTrue(candidate_period_hit(row))
        self.assertFalse(candidate_period_hit({
            "timestamp":"20010101000000",
            "status":"200",
            "url":"http://x/",
        }))
        self.assertFalse(candidate_period_hit(None))

    def test_query_url_keeps_candidate_literal(self):
        url=query_url(
            "http://www.dp.gamersdream.ne.jp/~PO/sa_apply.html",
            "19990820",
        )
        self.assertIn("timestamp=19990820",url)
        self.assertIn("%7EPO",url.upper())


if __name__=="__main__":
    unittest.main()
