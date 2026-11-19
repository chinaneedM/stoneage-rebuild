"""PET123: 2023 six-region original classic PC source-bounded audit and 2024 handoff."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "research/recovered/STONEAGE-PET123-YEAR2023-SIX-REGION-CLASSIC-PC-BOUNDED-AUDIT-R1.json"
QUEUE = ROOT / "research/recovered/STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json"
REPORT = ROOT / "docs/continuity/STONEAGE-PET123-YEAR2023-SIX-REGION-CLASSIC-PC-BOUNDED-AUDIT-20261119.md"
REGIONS = {"CN", "TW", "HK_MO", "KR", "JP", "OTHER"}


class Pet123Year2023SourceBoundedAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = json.loads(AUDIT.read_text(encoding="utf-8"))
        cls.q = json.loads(QUEUE.read_text(encoding="utf-8"))
        cls.s = {s["id"]: s for s in cls.a["sources"]}

    def test_year_handoff_preserves_all_prior_years_and_null_counts(self):
        a, q = self.a, self.q
        y = next(x for x in q["yearly_work_queue"] if x["year"] == 2023)
        following = next(x for x in q["yearly_work_queue"] if x["year"] == 2024)
        self.assertEqual((a["active_module"], q["active_module"]), ("PET", "PET"))
        self.assertEqual((a["year_frontier_before"], a["year_frontier_after"]), (2023, 2024))
        self.assertEqual((a["review_status"], y["research_gate"]), ("SOURCE_BOUNDED_REVIEWED", "SOURCE_BOUNDED_REVIEWED"))
        self.assertFalse(a["historically_complete"])
        self.assertFalse(y["historically_complete"])
        self.assertTrue(y["year_reopenable"])
        self.assertIn(following["research_gate"], {"NOT_YEAR_AUDITED", "SOURCE_BOUNDED_REVIEWED"})
        self.assertGreaterEqual(q["current_frontier"]["year"], 2024)
        self.assertGreaterEqual(int(q["current_frontier"]["next"].split(":")[0][3:]), 124)
        self.assertIsNone(y["historical_species_count"])
        self.assertIsNone(a["original_pc_global_2023_species_count"])
        self.assertIsNone(a["original_pc_2023_first_release_species_count"])
        self.assertEqual(y["source_bounded_review_receipt"], str(AUDIT.relative_to(ROOT)))
        self.assertEqual(y["source_bounded_review_report"], str(REPORT.relative_to(ROOT)))
        self.assertEqual(y["partial_source_review_receipts"][0]["id"], a["id"])
        self.assertIn(a["id"], [x["id"] for x in q["root_source_census_receipts"]])
        for year in range(1999, 2023):
            earlier = next(x for x in q["yearly_work_queue"] if x["year"] == year)
            self.assertNotEqual(earlier["research_gate"], "NOT_YEAR_AUDITED")

    def test_all_regions_independently_reopenable_and_source_limited(self):
        a, q = self.a, self.q
        self.assertEqual(set(a["region_reviews"]), REGIONS)
        self.assertEqual(len(a["region_reviews"]), a["independent_region_reviews"])
        y = next(x for x in q["yearly_work_queue"] if x["year"] == 2023)
        self.assertEqual(set(y["region_source_reviews"]), REGIONS - {"HK_MO"})
        self.assertEqual(set(y["additional_region_reviews"]), {"HK_MO"})
        self.assertEqual(len(set(y["residual_reopen_triggers"])), 6)
        for region, record in a["region_reviews"].items():
            copied = y["region_source_reviews"].get(region) or y["additional_region_reviews"][region]
            self.assertEqual(copied, record)
            self.assertEqual(record["review_status"], "SOURCE_BOUNDED_REVIEWED")
            self.assertFalse(record["historically_complete"])
            self.assertIsNone(record["pet_population"])
            self.assertIsNone(record["official_2023_first_release_species_count"])
            self.assertEqual(record["native_pet_id_rows_verified"], 0)
            self.assertTrue(record["reopen_trigger"])
        for field in ("new_original_pc_client_bytes", "new_original_pc_patch_bytes",
                      "new_native_pet_id_rows", "new_original_pc_spr_frames",
                      "new_native_skill_functions", "new_original_server_pet_grants"):
            self.assertEqual(a[field], 0)
        self.assertTrue(all(a["negative_controls"].values()))

    def test_rabbit_candidate_rings_are_items_and_new_pc_platform_is_not_old_client(self):
        s = self.s
        self.assertEqual(len(s), len(self.a["sources"]))
        self.assertGreaterEqual(len(s), 7)
        rabbit = s["TW2023-RABBIT-PLAYER-GUIDE-INDEX"]
        self.assertIn("里拉拉", rabbit["candidate_pet_labels"])
        self.assertFalse(rabbit["actual_official_first_release_proved"])
        self.assertIsNone(rabbit["classic_same_build_pet_id"])
        rings = s["TW2023-MIDAUTUMN-HALLOWEEN-GUIDE"]
        self.assertEqual(set(rings["event_reward_items"]), {"克達達之戒", "里拉拉之戒"})
        self.assertFalse(rings["native_pet_reward_confirmed"])
        duplicate = s["TW2023-MIDAUTUMN-HALLOWEEN-SAME-EVENT-RELAY"]
        self.assertEqual(duplicate["not_independent_from"], rings["id"])
        self.assertTrue(all("MOBILE" not in (r.get("product") or "") for r in s.values()))
        self.assertTrue(all("AWAKENING" not in (r.get("product") or "") for r in s.values()))
        self.assertEqual(len(s), 6)
        operator_lead = s["TW2023-SEP27-OPERATOR-LINK-CITED-UNREADABLE"]
        self.assertTrue(operator_lead["claimed_original_operator_url"].endswith("id=1849"))
        self.assertFalse(operator_lead["original_html_actually_obtained"])
        self.assertFalse(operator_lead["original_patch_actually_obtained"])
        self.assertIn("2023", REPORT.read_text(encoding="utf-8"))
        self.assertIn("PET123", (ROOT / "README.md").read_text(encoding="utf-8"))
        self.assertIn("PET123", (ROOT / "docs/STONEAGE-PET-CHRONOLOGICAL-RESTORATION-ORDER-R1.md").read_text(encoding="utf-8"))

    def test_original_current_blob_is_preserved_and_stage_gates_unchanged(self):
        raw = (ROOT / "docs/CURRENT-STATE.md").read_bytes()
        self.assertEqual(len(raw), self.a["baseline"]["current_state_bytes"])
        got = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\x00" + raw).hexdigest()
        self.assertEqual(got, self.a["baseline"]["current_state_blob"])
        self.assertEqual((self.a["stage_A"], self.a["stage_B_wiki"], self.a["r79"], self.a["overall_percent"]),
                         (self.q["stage_A"], self.q["stage_B_wiki"], self.q["r79"], self.q["overall_game_completion_percent"]))


if __name__ == "__main__":
    unittest.main()
