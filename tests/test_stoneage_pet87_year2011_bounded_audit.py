"""PET87: 2011 original PC official pet annual source-bounded review, not completion."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REC = ROOT / "research" / "recovered"


def read(filename):
    return json.loads((REC / filename).read_text(encoding="utf-8"))


class PET87Year2011(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = read("STONEAGE-PET87-YEAR2011-CN-TW-HKMO-JP-KR-OTHER-SOURCE-BOUNDED-ANNUAL-AUDIT-R1.json")
        cls.q = read("STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json")

    def test_year_closure_without_historical_completeness(self):
        a, q = self.a, self.q
        year = q["yearly_work_queue"][2011 - 1999]
        new_year = q["yearly_work_queue"][2012 - 1999]
        self.assertEqual((a["year"], a["year_frontier_before"], a["year_frontier_after"]), (2011, 2011, 2012))
        self.assertGreaterEqual(q["current_frontier"]["year"], 2012)
        self.assertEqual(year["research_gate"], "SOURCE_BOUNDED_REVIEWED")
        self.assertFalse(year["historically_complete"])
        self.assertIsNone(year["historical_species_count"])
        self.assertEqual(year["source_bounded_review_receipt"], "research/recovered/STONEAGE-PET87-YEAR2011-CN-TW-HKMO-JP-KR-OTHER-SOURCE-BOUNDED-ANNUAL-AUDIT-R1.json")
        self.assertIn(new_year["research_gate"], ("NOT_YEAR_AUDITED", "SOURCE_BOUNDED_REVIEWED"))
        self.assertFalse(a["historically_complete"])
        self.assertTrue(a["year_source_bounded_closed"])
        self.assertTrue(a["year_can_reopen_on_authentic_original_client_or_first_party_operator_evidence"])
        self.assertIsNone(a["year_first_new_official_species_count"])
        self.assertIsNone(a["global_official_2011_species_population"])

    def test_forward_only_annual_receipts(self):
        a, q = self.a, self.q
        year = q["yearly_work_queue"][12]
        ids = [x["id"] for x in year["partial_source_review_receipts"]]
        self.assertEqual(ids[-3:], a["prior_partial_receipts"] + [a["id"]])
        self.assertEqual(sum(x["id"] == a["id"] for x in q["root_source_census_receipts"]), 1)
        self.assertEqual(sum(x["id"] == a["id"] for x in year["partial_source_review_receipts"]), 1)
        self.assertEqual(len({x["id"] for x in q["root_source_census_receipts"]}), len(q["root_source_census_receipts"]))
        self.assertEqual(year["residual_reopen_triggers"], a["five_region_and_hkmo_reopen_triggers"])

    def test_six_independent_region_source_limits(self):
        a, q = self.a, self.q
        self.assertEqual(set(a["region_reviews"]), {"CN", "TW", "HK_MO", "JP", "KR", "OTHER"})
        self.assertEqual(set(q["yearly_work_queue"][12]["region_source_reviews"]), {"CN", "TW", "JP", "KR", "OTHER"})
        self.assertIn("HK_MO", q["yearly_work_queue"][12]["additional_region_reviews"])
        self.assertEqual(len(a["five_region_and_hkmo_reopen_triggers"]), 6)
        self.assertEqual(len(set(a["five_region_and_hkmo_reopen_triggers"])), 6)
        for region, entry in a["region_reviews"].items():
            self.assertEqual(entry["review_status"], "SOURCE_BOUNDED_REVIEWED")
            self.assertFalse(entry["historically_complete"])
            self.assertIsNone(entry["pet_population"])
            self.assertEqual(entry["native_pet_id_rows_verified_in_2011_audit"], 0)
            yentry = (q["yearly_work_queue"][12]["region_source_reviews"].get(region)
                      or q["yearly_work_queue"][12]["additional_region_reviews"].get(region))
            self.assertEqual(yentry["reopen_trigger"], entry["reopen_trigger"])

    def test_original_client_and_historical_date_negative_evidence(self):
        a = self.a
        s = {x["id"]: x for x in a["source_audit"]}
        self.assertEqual(len(s), 9)
        self.assertEqual(s["2011-CN-JAN13-DOWNLOAD-ANNOUNCED-NO-BINARY"]["archive_url_current_status"], "TIMEOUT")
        self.assertEqual(s["2011-CN-JUN22-ZOL-CLIENT-UNREADABLE"]["download_result"], "403_FORBIDDEN")
        self.assertEqual(s["2011-TW-APR20-OPERATOR-SCHEDULE-AND-SEP08-RETROSPECTIVE"]["operator_apr20_nonwipe_planned"], "2011-04-29")
        self.assertEqual(s["2011-TW-APR20-OPERATOR-SCHEDULE-AND-SEP08-RETROSPECTIVE"]["operator_sep08_uses_past_tense_launch"], "2011-04-28")
        self.assertTrue(s["2011-TW-APR20-OPERATOR-SCHEDULE-AND-SEP08-RETROSPECTIVE"]["dates_not_collapsed"])
        self.assertEqual(s["2011-TW-LATE-TIMELINE-NOT-OPERATOR"]["original_2011_operator_notice_obtained"], False)
        self.assertEqual(s["2011-KR-AUTUMN-NAMED-PETS-NONPERIOD"]["candidate_names"], ["메가죠", "바렌이노"])
        self.assertEqual(s["2011-KR-AUTUMN-NAMED-PETS-NONPERIOD"]["count_as_2011_official_confirmed_new_species"], 0)
        self.assertEqual(s["2009-KR-CONTEMPORANEOUS-FESTIVAL-MUST_NOT_BACKDATE"]["date"], "2009-09-29")
        self.assertFalse(s["2009-KR-CONTEMPORANEOUS-FESTIVAL-MUST_NOT_BACKDATE"]["is_2011_source"])
        self.assertTrue(all(a["release_source_boundaries"].values()))
        self.assertEqual((a["new_authenticated_2011_original_client_bytes"],
                          a["new_native_2011_pet_identity_ids"],
                          a["new_2011_original_2d_spr_pixels_verified"],
                          a["new_2011_original_server_reward_execution_logs"]), (0, 0, 0, 0))

    def test_original_historical_blob_and_stage_gates(self):
        a = self.a
        raw = (ROOT / "docs" / "CURRENT-STATE.md").read_bytes()
        self.assertEqual(len(raw), 2709173)
        native_sha = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\x00" + raw).hexdigest()
        self.assertEqual(native_sha, a["startup"]["unchanged_original_current_git_blob"])
        self.assertTrue(a["historical_CURRENT_untouched"])
        self.assertEqual((a["stage_A"], a["stage_B_wiki"], a["r79"], a["overall_percent"]),
                         ("7_PARTIAL_2_OPEN", "GATED", "PAUSED_NON_BLOCKING", None))


if __name__ == "__main__":
    unittest.main()
