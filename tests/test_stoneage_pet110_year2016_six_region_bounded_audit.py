"""PET110: 2016 classic-PC six-region source-bounded review is not pet-roster completeness."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REC = ROOT / "research/recovered"
AUDIT = REC / "STONEAGE-PET110-YEAR2016-SIX-REGION-ORIGINAL-PC-PET-BOUNDED-AUDIT-R1.json"
QUEUE = REC / "STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json"
REPORT = ROOT / "docs/continuity/STONEAGE-PET110-YEAR2016-SIX-REGION-ORIGINAL-PC-SOURCE-BOUNDED-AUDIT-20261118.md"
REGIONS = {"CN", "TW", "HK_MO", "KR", "JP", "OTHER"}

class TestPet110Year2016SourceBoundedReview(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = json.loads(AUDIT.read_text(encoding="utf-8"))
        cls.q = json.loads(QUEUE.read_text(encoding="utf-8"))

    def test_2016_source_review_complete_not_historically_complete(self):
        a, q = self.a, self.q
        year = next(y for y in q["yearly_work_queue"] if y["year"] == 2016)
        next_year = next(y for y in q["yearly_work_queue"] if y["year"] == 2017)
        self.assertEqual((a["year_frontier_before"], a["year_frontier_after"]), (2016, 2017))
        self.assertEqual((q["active_module"], a["active_module"]), ("PET", "PET"))
        self.assertEqual(a["review_status"], "SOURCE_BOUNDED_REVIEWED")
        self.assertEqual(year["research_gate"], a["review_status"])
        self.assertEqual(year["source_bounded_review_receipt"], str(AUDIT.relative_to(ROOT)))
        self.assertTrue(a["source_bounded_only"])
        self.assertTrue(a["year_source_bounded_closed"])
        self.assertTrue(a["year_reopenable"])
        self.assertTrue(year["year_reopenable"])
        self.assertFalse(a["historically_complete"])
        self.assertFalse(year["historically_complete"])
        self.assertIsNone(year["historical_species_count"])
        self.assertIsNone(a["original_pc_global_2016_species_count"])
        self.assertIsNone(a["original_pc_2016_first_release_count"])
        self.assertEqual(next_year["research_gate"], "SOURCE_BOUNDED_REVIEWED")  # PET113 forward-only later year review
        self.assertGreaterEqual(q["current_frontier"]["year"], 2017)
        self.assertIn(a["id"],[z["id"] for z in q["root_source_census_receipts"]])
        self.assertIn(a["id"],[z["id"] for z in q["root_source_census_receipts"]])
        self.assertTrue(a["next"].startswith("PET111:"))  # historical 2016 closure NEXT not current live NEXT
        self.assertIn("2017", REPORT.read_text(encoding="utf-8"))

    def test_all_six_independent_regions_and_reopening_triggers(self):
        a, q = self.a, self.q
        y = next(z for z in q["yearly_work_queue"] if z["year"] == 2016)
        self.assertEqual(set(a["region_reviews"]), REGIONS)
        self.assertEqual(set(y["region_source_reviews"]), REGIONS - {"HK_MO"})
        self.assertEqual(set(y["additional_region_reviews"]), {"HK_MO"})
        self.assertEqual(len(a["reopen_triggers"]), 6)
        self.assertEqual(len(set(a["reopen_triggers"])), 6)
        self.assertEqual(y["residual_reopen_triggers"], a["reopen_triggers"])
        for region, info in a["region_reviews"].items():
            row = y["region_source_reviews"].get(region) or y["additional_region_reviews"].get(region)
            self.assertEqual(row["region"], region)
            self.assertEqual(row["review_status"], "SOURCE_BOUNDED_REVIEWED")
            self.assertEqual(row["reopen_trigger"], info["reopen_trigger"])
            self.assertFalse(row["historically_complete"])
            self.assertIsNone(row["pet_population"])
            self.assertIsNone(row["official_2016_first_release_species_count"])
            self.assertEqual(row["native_pet_id_rows_verified"], 0)

    def test_forward_only_year_receipts_and_unique_source_layers(self):
        a, q = self.a, self.q
        y = next(z for z in q["yearly_work_queue"] if z["year"] == 2016)
        self.assertEqual(len(a["prior_partial_receipts"]), 4)
        self.assertEqual([r["id"] for r in y["partial_source_review_receipts"]][:4], a["prior_partial_receipts"])
        self.assertEqual(y["partial_source_review_receipts"][-1]["id"], a["id"])
        self.assertIn(a["id"],[z["id"] for z in q["root_source_census_receipts"]])
        self.assertEqual(next(z for z in q["root_source_census_receipts"] if z["id"] == a["id"])["year_frontier_after"], 2017)
        self.assertEqual(len(q["root_source_census_receipts"]),
                         len({z["id"] for z in q["root_source_census_receipts"]}))
        self.assertEqual(q["current_frontier"]["latest_2016_partial_source_receipt"], a["prior_partial_receipts"][-1])
        self.assertEqual(y["source_bounded_partial_review_notes_forward_only"][-1].split(":")[0], "PET110")
        self.assertEqual(len(a["sources"]), len({z["id"] for z in a["sources"]}))
        self.assertEqual(len(a["sources"]), 12)
        self.assertTrue(a["sources"][0]["grade"].startswith("CONTEMPORANEOUS_THIRD_PARTY"))
        self.assertTrue(any(s["grade"].startswith("RETROSPECTIVELY_EDITED") for s in a["sources"]))
        self.assertTrue(any(s["grade"].startswith("2016_FIRST_PARTY_OPERATOR_MOBILE") for s in a["sources"]))
        self.assertTrue(all(a["negative_controls"].values()))

    def test_stoneage_classic_pet_count_and_rights_safety(self):
        a,q = self.a,self.q
        self.assertEqual(len(a["candidate_labels_by_grade"]["TW_period_player_encounter_monster_labels_not_pet_releases"]), 10)
        self.assertEqual(a["candidate_labels_by_grade"]["CN_2016_native_pet_names_verified"], [])
        self.assertEqual(a["candidate_labels_by_grade"]["JP_2016_original_pc_pet_names_verified"], [])
        self.assertEqual(a["candidate_labels_by_grade"]["KR_2016_original_pc_pet_names_verified"], [])
        for field in (
            "new_2016_original_pc_client_bytes",
            "new_2016_original_pc_patch_bytes",
            "new_2016_native_pet_ids",
            "new_2016_original_spr_frames",
            "new_2016_native_pet_skills",
            "new_2016_server_pet_grant_logs",
        ):
            self.assertEqual(a[field],0)
        raw=(ROOT/"docs/CURRENT-STATE.md").read_bytes()
        self.assertEqual(len(raw),a["starting_remote"]["current_state_bytes"])
        blob=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\x00"+raw).hexdigest()
        self.assertEqual(blob,a["starting_remote"]["current_state_git_blob"])
        self.assertTrue(a["current_state_original_blob_unchanged"])
        self.assertEqual((a["stage_A"],a["stage_B_wiki"],a["r79"],a["overall_percent"]),
                         (q["stage_A"],q["stage_B_wiki"],q["r79"],q["overall_game_completion_percent"]))
        self.assertEqual((a["stage_A"],a["stage_B_wiki"],a["r79"],a["overall_percent"]),
                         ("7_PARTIAL_2_OPEN","GATED","PAUSED_NON_BLOCKING",None))

if __name__ == "__main__":
    unittest.main()
