"""PET124: six-region 2024 classic-PC source-bounded audit; new Awakening must stay separate."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / "research/recovered/STONEAGE-PET124-YEAR2024-SIX-REGION-CLASSIC-PC-BOUNDED-AUDIT-R1.json"
Q = ROOT / "research/recovered/STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json"
REPORT = ROOT / "docs/continuity/STONEAGE-PET124-YEAR2024-SIX-REGION-CLASSIC-PC-BOUNDED-AUDIT-20261119.md"
REGIONS = {"CN", "TW", "HK_MO", "KR", "JP", "OTHER"}


class Pet124Year2024SourceBoundedAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = json.loads(A.read_text(encoding="utf-8"))
        cls.q = json.loads(Q.read_text(encoding="utf-8"))
        cls.ss = {s["id"]: s for s in cls.a["sources"]}

    def test_2024_bounded_and_2025_cursor_forward_only(self):
        a, q = self.a, self.q
        y = next(x for x in q["yearly_work_queue"] if x["year"] == 2024)
        n = next(x for x in q["yearly_work_queue"] if x["year"] == 2025)
        prev = next(x for x in q["yearly_work_queue"] if x["year"] == 2023)
        self.assertEqual((a["year_frontier_before"], a["year_frontier_after"]), (2024, 2025))
        self.assertEqual((a["active_module"], q["active_module"]), ("PET", "PET"))
        self.assertEqual((a["review_status"], y["research_gate"]), ("SOURCE_BOUNDED_REVIEWED", "SOURCE_BOUNDED_REVIEWED"))
        self.assertFalse(a["historically_complete"])
        self.assertFalse(y["historically_complete"])
        self.assertTrue(a["year_reopenable"])
        self.assertTrue(y["year_reopenable"])
        self.assertIn(n["research_gate"], {"NOT_YEAR_AUDITED", "SOURCE_BOUNDED_REVIEWED"})
        self.assertGreaterEqual(q["current_frontier"]["year"], 2025)
        self.assertGreaterEqual(int(q["current_frontier"]["next"].split(":")[0][3:]), 125)
        self.assertEqual(prev["research_gate"], "SOURCE_BOUNDED_REVIEWED")
        self.assertEqual(y["source_bounded_review_receipt"], str(A.relative_to(ROOT)))
        self.assertEqual(y["source_bounded_review_report"], str(REPORT.relative_to(ROOT)))
        self.assertEqual(y["partial_source_review_receipts"][0]["id"], a["id"])
        self.assertIn(a["id"], [x["id"] for x in q["root_source_census_receipts"]])
        self.assertIsNone(y["historical_species_count"])
        self.assertIsNone(a["original_pc_global_2024_species_count"])
        self.assertIsNone(a["original_pc_2024_first_release_species_count"])
        for year in range(1999, 2025):
            earlier = next(x for x in q["yearly_work_queue"] if x["year"] == year)
            self.assertNotEqual(earlier["research_gate"], "NOT_YEAR_AUDITED")

    def test_independent_six_region_reopening_and_zero_new_authenticated_bytes(self):
        a, q = self.a, self.q
        self.assertEqual(set(a["region_reviews"]), REGIONS)
        y = next(x for x in q["yearly_work_queue"] if x["year"] == 2024)
        self.assertEqual(set(y["region_source_reviews"]), REGIONS - {"HK_MO"})
        self.assertEqual(set(y["additional_region_reviews"]), {"HK_MO"})
        self.assertEqual(len(set(y["residual_reopen_triggers"])), 6)
        for region, record in a["region_reviews"].items():
            copy = y["region_source_reviews"].get(region) or y["additional_region_reviews"][region]
            self.assertEqual(copy, record)
            self.assertTrue(copy["year_reopenable"])
            self.assertEqual(copy["review_status"], "SOURCE_BOUNDED_REVIEWED")
            self.assertFalse(copy["historically_complete"])
            self.assertIsNone(copy["pet_population"])
            self.assertIsNone(copy["official_2024_first_release_species_count"])
            self.assertEqual(copy["native_pet_id_rows_verified"], 0)
            self.assertTrue(copy["reopen_trigger"])
        for field in ("new_original_pc_client_bytes", "new_original_pc_patch_bytes",
                      "new_native_pet_id_rows", "new_original_pc_spr_frames",
                      "new_native_skill_functions", "new_original_server_pet_grants"):
            self.assertEqual(a[field], 0)
        self.assertTrue(all(a["negative_controls"].values()))

    def test_taiwan_pool_count_not_new_species_and_duplicate_relay(self):
        self.assertEqual(len(self.ss), len(self.a["sources"]))
        guide = self.ss["TW2024-AUTUMN-C-PLAYER-FIRSTHAND-GUIDE-INDEX"]
        self.assertEqual(guide["mentioned_pool_count"], 21)
        self.assertEqual(guide["named_reward_pet_ids_verified"], 0)
        self.assertIsNone(guide["reward_pool_actual_member_names"])
        self.assertIn("里拉拉", guide["task_npc_labels"])
        mirror = self.ss["TW2024-AUTUMN-INDEX-MIRROR"]
        self.assertEqual(mirror["not_independent_from"], guide["id"])
        dragon = self.ss["TW2024-DRAGON-PLAYER-RELAY-INDEX"]
        self.assertFalse(dragon["actual_2024_first_new_species_proved"])
        self.assertIsNone(dragon["native_new_pet_id"])
        self.assertIn("木笛", dragon["task_object_labels"])

    def test_awakening_narrative_21_plus_9_are_distinct_product_only(self):
        s = self.ss
        b1 = s["CN2024-APR02-AWAKENING-OFFICIAL-EDEN-BATCH"]
        b2 = s["CN2024-APR25-AWAKENING-OFFICIAL-EDEN-BATCH"]
        expected1, expected2 = (7, 11, 3), (4, 4, 1)
        for batch, expected in ((b1, expected1), (b2, expected2)):
            self.assertEqual(batch["product"], "STONEAGE_AWAKENING_DUAL_END_CN_2023_ONWARD")
            c = batch["named_pet_categories"]
            self.assertEqual(tuple(len(c[k]) for k in ("quest", "catchable", "event")), expected)
            self.assertEqual(sum(len(v) for v in c.values()), batch["named_pet_listing_positions"])
            self.assertEqual(batch["actual_original_pc_2024_native_grants"], 0)
        self.assertEqual(b1["white_tiger_album_display_only"], "白虎佩露夏")
        self.assertIn("里拉拉", b1["named_pet_categories"]["quest"])
        self.assertIn("迪基格斯", b2["named_pet_categories"]["event"])
        p = self.a["separate_product_line_evidence"]
        self.assertEqual((p["april02_named_positions"], p["april25_named_positions"]), (21, 9))
        self.assertEqual(p["total_2024_official_announcement_named_positions"], 30)
        self.assertIsNone(p["actual_legacy_original_pc_species_from_these_entries"])
        self.assertEqual(p["actual_native_award_logs_obtained"], 0)
        self.assertIn("2024", REPORT.read_text(encoding="utf-8"))
        self.assertIn("PET124", (ROOT / "README.md").read_text(encoding="utf-8"))
        self.assertIn("PET124", (ROOT / "docs/STONEAGE-PET-CHRONOLOGICAL-RESTORATION-ORDER-R1.md").read_text(encoding="utf-8"))

    def test_original_current_blob_and_stage_gates_unchanged(self):
        raw = (ROOT / "docs/CURRENT-STATE.md").read_bytes()
        self.assertEqual(len(raw), self.a["baseline"]["current_state_bytes"])
        got = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\x00" + raw).hexdigest()
        self.assertEqual(got, self.a["baseline"]["current_state_blob"])
        self.assertEqual((self.a["stage_A"], self.a["stage_B_wiki"], self.a["r79"], self.a["overall_percent"]),
                         (self.q["stage_A"], self.q["stage_B_wiki"], self.q["r79"], self.q["overall_game_completion_percent"]))


if __name__ == "__main__":
    unittest.main()
