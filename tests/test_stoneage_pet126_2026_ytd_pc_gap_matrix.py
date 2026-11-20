"""PET126: 2026 YTD original-classic-PC source-only audit, no year closure, no module unlock."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R = ROOT / "research/recovered"
AUDIT = R / "STONEAGE-PET126-YEAR2026-YTD-CLASSIC-PC-SOURCE-AND-MODULE-GAPS-R1.json"
Q = R / "STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json"
P20 = R / "STONEAGE-PET-MODULE-20-FIELD-COVERAGE-AND-SOURCE-STOP-MATRIX-R1.json"
P38 = R / "STONEAGE-PET38-CLIENT-FIRST-AVAILABLE-SOURCE-INVENTORY-R1.json"
REPORT = ROOT / "docs/continuity/STONEAGE-PET126-YEAR2026-YTD-CLASSIC-PC-SOURCE-AND-MODULE-GAPS-20261120.md"


class PET126PCYearToDateBoundary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = json.loads(AUDIT.read_text(encoding="utf-8"))
        cls.q = json.loads(Q.read_text(encoding="utf-8"))
        cls.p20 = json.loads(P20.read_text(encoding="utf-8"))
        cls.p38 = json.loads(P38.read_text(encoding="utf-8"))

    def test_cursor_stays_in_current_year(self):
        a, q = self.a, self.q
        self.assertEqual(a["year"], 2026)
        self.assertEqual(a["as_of_date"], "2026-11-20")
        self.assertEqual(a["scope"], "OFFICIAL_ORIGINAL_CLASSIC_2D_PC_ONLY")
        self.assertEqual(a["active_module"], q["active_module"])
        self.assertEqual(q["current_frontier"]["year"], 2026)
        self.assertEqual(q["current_frontier"]["status"], "OPEN_NOT_YEAR_CLOSED")
        self.assertEqual((a["annual_review"]["frontier_before"], a["annual_review"]["frontier_after"]), (2026, 2026))
        self.assertFalse(a["annual_review"]["annual_closeout_allowed"])
        year = next(y for y in q["yearly_work_queue"] if y["year"] == 2026)
        prior = next(y for y in q["yearly_work_queue"] if y["year"] == 2025)
        self.assertEqual(year["research_gate"], "NOT_YEAR_AUDITED")
        self.assertEqual(prior["research_gate"], "SOURCE_BOUNDED_REVIEWED")
        self.assertFalse(prior["historically_complete"])
        self.assertEqual(q["current_frontier"]["latest_partial_root_review"], a["id"])
        self.assertTrue(q["current_frontier"]["next"].startswith("PET126B"))
        self.assertIsNone(a["annual_review"]["official_original_pc_global_species_count"])
        self.assertIsNone(a["annual_review"]["official_2026_first_release_species_count"])
        self.assertIsNone(year["historical_species_count"])
        self.assertTrue(any(x["id"] == a["id"] for x in q["root_source_census_receipts"]))

    def test_six_regions_are_open_not_zero_species(self):
        a = self.a
        self.assertEqual(set(a["region_reviews"]), {"CN", "TW", "HK_MO", "KR", "JP", "OTHER"})
        for x in a["region_reviews"].values():
            self.assertEqual(x["review_status"], "YTD_PARTIAL_OPEN")
            self.assertFalse(x["year_closeout_allowed"])
            self.assertFalse(x["historically_complete"])
            self.assertIsNone(x["pet_population"])
            self.assertIsNone(x["first_2026_release_species_count"])
            self.assertEqual(x["new_native_pet_identity_rows"], 0)
            self.assertTrue(x["reopen_trigger"])
        for k in ("live_original_pet_master_rows_newly_verified", "original_client_bytes_newly_acquired",
                  "original_patch_bytes_newly_acquired", "original_spr_frames_newly_verified",
                  "original_skill_handlers_newly_verified", "original_live_reward_grants_newly_verified"):
            self.assertEqual(a["annual_review"][k], 0)

    def test_player_index_and_pc_remake_never_become_original_live_pet_proof(self):
        a = self.a
        self.assertEqual(len(a["source_leads"]), 4)
        self.assertTrue(all(s["region"] == "TW" for s in a["source_leads"]))
        self.assertTrue(all("PLAYER_" in s["grade"] for s in a["source_leads"]))
        self.assertTrue(all(s["native_pet_id"] is None for s in a["source_leads"]))
        self.assertTrue(all(s["source_page_sha256"] is None for s in a["source_leads"]))
        self.assertTrue(all(not s["first_official_release_proven"] for s in a["source_leads"]))
        self.assertTrue(all(not s["official_operator_html_verified"] for s in a["source_leads"]))
        self.assertEqual(len(a["excluded_other_pc_product_line_evidence"]), 1)
        remake = a["excluded_other_pc_product_line_evidence"][0]
        self.assertFalse(remake["classic_original_roster_inclusion"])
        self.assertFalse(remake["counts_as_original_PC_2026_pet"])
        self.assertTrue(all(a["negative_controls"].values()))

    def test_seven_dimension_matrix_reuses_actual_verified_legacy_boundaries(self):
        a, p20, p38 = self.a, self.p20, self.p38
        gap = a["module_gap_review"]
        self.assertEqual(len(gap["seven_dimensions"]), 7)
        self.assertEqual({x["id"] for x in gap["seven_dimensions"]}, {x["id"] for x in p20["seven_pet_dimensions"]})
        self.assertEqual(gap["inventory_not_pet_species"]["source_namespace_rows"],
                         p20["source_coverage_observed"]["PET16_namespaces_sum_NOT_species"])
        self.assertEqual(gap["inventory_not_pet_species"]["tw10_selected_spr_groups"],
                         p20["source_coverage_observed"]["TW10_selected_source_SPR_groups"])
        self.assertEqual(gap["inventory_not_pet_species"]["tw10_strict_decodable_bitmap_keys"],
                         p20["source_coverage_observed"]["TW10_strict_pixel_bits"])
        self.assertEqual(gap["inventory_not_pet_species"]["tw10_bounded_bitmap_keys"],
                         p20["source_coverage_observed"]["TW10_bounded_pixel_bits"])
        self.assertTrue(any(x["id"] == "TW_WAEI_JSS_1_0_RETAIL" and
                            not x["verified_bytes_in_current_session"] for x in p38["records"]))
        self.assertEqual(gap["module_status"], "SOURCE_BOUNDED_PARTIAL")
        self.assertFalse(gap["source_bounded_closed"])
        self.assertFalse(gap["permitted_to_switch_content_module"])
        self.assertTrue(gap["closure_gate"]["requires_explicit_user_source_bounded_stop_decision"])
        self.assertFalse(gap["closure_gate"]["source_bounded_closed"])
        self.assertFalse(p20["allowed_to_unlock_next_module"])

    def test_historical_current_state_immutable(self):
        raw = (ROOT / "docs/CURRENT-STATE.md").read_bytes()
        self.assertEqual(len(raw), 2709173)
        git_blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\\x00" + raw).hexdigest()
        self.assertEqual(git_blob, self.a["baseline"]["historical_current_state_blob"])
        self.assertEqual(git_blob, "c89e0e33537990aa2132b47c40fef49a985a935c")
        self.assertEqual((self.a["stage_A"], self.a["stage_B_wiki"],
                          self.a["r79"], self.a["overall_percent"]),
                         (self.q["stage_A"], self.q["stage_B_wiki"],
                          self.q["r79"], self.q["overall_game_completion_percent"]))
        self.assertIn("PET126", REPORT.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
