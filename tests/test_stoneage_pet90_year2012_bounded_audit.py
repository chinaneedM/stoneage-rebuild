"""PET90: 2012 source-bounded review and 2013 frontier, preserving unverified PC pets."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "research" / "recovered"


def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


class Pet90Year2012(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = load("STONEAGE-PET90-YEAR2012-CN-TW-HKMO-KR-JP-OTHER-BOUNDED-ANNUAL-AUDIT-R1.json")
        cls.q = load("STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json")

    def test_2012_source_bound_gate_and_2013_next(self):
        a, q = self.a, self.q
        y = q["yearly_work_queue"][2012 - 1999]
        y2013 = q["yearly_work_queue"][2013 - 1999]
        self.assertEqual((a["year"], a["year_frontier_before"], a["year_frontier_after"]), (2012, 2012, 2013))
        self.assertGreaterEqual(q["current_frontier"]["year"], 2013)
        self.assertEqual(y["research_gate"], "SOURCE_BOUNDED_REVIEWED")
        self.assertFalse(y["historically_complete"])
        self.assertIsNone(y["historical_species_count"])
        self.assertEqual(y["source_bounded_review_receipt"],
                         "research/recovered/STONEAGE-PET90-YEAR2012-CN-TW-HKMO-KR-JP-OTHER-BOUNDED-ANNUAL-AUDIT-R1.json")
        self.assertIn(y2013["research_gate"], ("NOT_YEAR_AUDITED", "SOURCE_BOUNDED_REVIEWED"))
        self.assertFalse(a["historically_complete"])
        self.assertTrue(a["source_bounded_only"])
        self.assertTrue(a["year_source_bounded_closed"])
        self.assertTrue(a["year_reopenable_when_authentic_2012_native_clients_or_operator_sources_arrive"])
        self.assertIsNone(a["global_original_pc_pet_species_count_2012"])
        self.assertIsNone(a["first_release_2012_species_count"])

    def test_forward_only_receipts_and_reopen_conditions(self):
        a, q = self.a, self.q
        y = q["yearly_work_queue"][13]
        ids = [x["id"] for x in y["partial_source_review_receipts"]]
        self.assertEqual(ids[-3:], a["prior_receipts"] + [a["id"]])
        self.assertEqual(sum(x["id"] == a["id"] for x in q["root_source_census_receipts"]), 1)
        self.assertEqual(sum(x["id"] == a["id"] for x in y["partial_source_review_receipts"]), 1)
        self.assertEqual(len({x["id"] for x in q["root_source_census_receipts"]}), len(q["root_source_census_receipts"]))
        self.assertEqual(y["residual_reopen_triggers"], a["reopen_triggers"])
        self.assertEqual(len(set(a["reopen_triggers"])), 6)

    def test_all_six_regions_separate(self):
        a, q = self.a, self.q
        self.assertEqual(set(a["region_reviews"]), {"CN", "TW", "HK_MO", "KR", "JP", "OTHER"})
        self.assertEqual(set(q["yearly_work_queue"][13]["region_source_reviews"]), {"CN", "TW", "JP", "KR", "OTHER"})
        self.assertEqual(set(q["yearly_work_queue"][13]["additional_region_reviews"]), {"HK_MO"})
        for region, info in a["region_reviews"].items():
            self.assertEqual(info["review_status"], "SOURCE_BOUNDED_REVIEWED")
            self.assertFalse(info["historically_complete"])
            self.assertIsNone(info["pet_population"])
            self.assertEqual(info["native_pet_id_rows_verified_in_review"], 0)
            self.assertFalse(info["real_original_server_pet_grant_verified"])
            yinfo = (q["yearly_work_queue"][13]["region_source_reviews"].get(region)
                     or q["yearly_work_queue"][13]["additional_region_reviews"].get(region))
            self.assertEqual(yinfo["reopen_trigger"], info["trigger"])

    def test_taiwan_maintenance_forward_correction(self):
        a = self.a
        s = {x["id"]: x for x in a["source_audit"]}
        self.assertEqual(len(s), 10)
        tw = s["2012-TW-MAY22-CHANGE-OF-SCHEDULE-ERRATUM"]
        self.assertEqual(tw["old_planned_maintenance"], "2012-05-23")
        self.assertEqual(tw["announced_deferred_start"], "2012-05-24T22:00")
        self.assertEqual(tw["announced_deferred_end"], "2012-05-25T14:00")
        self.assertTrue(tw["correction_forward_only"])
        self.assertFalse(tw["original_operator_page_readable_now"])
        self.assertFalse(tw["actual_patch_execution_verified"])
        self.assertEqual(tw["original_official_page"], "http://www.stoneage.tw/news.php?id=1071")
        self.assertTrue(a["source_negative_controls"]["tw_20120523_was_planned_but_deferred_not_observed_patch"])
        self.assertFalse(s["2012-TW-MAY25-V189-INDEX"]["official_version_binary_verified"])
        self.assertEqual(s["2012-TW-DEC28-BINARY-CANDIDATE-NONCUSTODY"]["bytes_acquired"], 0)

    def test_2012_original_client_and_sequel_exclusion(self):
        a = self.a
        self.assertEqual((a["native_client_custody"]["actual_new_authenticated_2012_original_pc_bytes"],
                          a["native_client_custody"]["original_pc_native_pet_id_rows"],
                          a["native_client_custody"]["original_2012_spr_pixels_verified"],
                          a["native_client_custody"]["native_2012_encounter_records"],
                          a["native_client_custody"]["actual_server_pet_reward_receipts"]), (0, 0, 0, 0, 0))
        self.assertTrue(all(a["source_negative_controls"].values()))
        self.assertTrue(a["native_client_custody"]["tw_historical_download_binary_candidates_unread"])
        self.assertTrue(a["native_client_custody"]["cn_download_metadata_not_file"])
        self.assertEqual(a["novel_historical_findings"]["additional_2012_confirmed_new_species_from_later_fan_roster"], 0)

    def test_full_original_current_state_git_blob_unchanged(self):
        a = self.a
        raw = (ROOT / "docs" / "CURRENT-STATE.md").read_bytes()
        self.assertEqual(len(raw), 2709173)
        sha = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\x00" + raw).hexdigest()
        self.assertEqual(sha, a["startup"]["original_current_git_blob"])
        self.assertTrue(a["historical_CURRENT_untouched"])
        self.assertEqual((a["stage_A"], a["stage_B_wiki"], a["r79"], a["overall_percent"]),
                         ("7_PARTIAL_2_OPEN", "GATED", "PAUSED_NON_BLOCKING", None))


if __name__ == "__main__":
    unittest.main()
