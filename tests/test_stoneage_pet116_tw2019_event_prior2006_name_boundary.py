"""PET116: 2019 TW pet event evidence is player-grade; 2006 name matches preclude 2019 first-issue inference."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "research/recovered/STONEAGE-PET116-TW2019-DRAGONBOAT-SUMMER-2006-NAME-BOUNDARY-R1.json"
Q = ROOT / "research/recovered/STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json"
R = ROOT / "docs/continuity/STONEAGE-PET116-TW2019-DRAGONBOAT-SUMMER-PET-REISSUE-2006-NAME-BOUNDARY-20261118.md"


class Pet116Taiwan2019Boundary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.e = json.loads(E.read_text(encoding="utf-8"))
        cls.q = json.loads(Q.read_text(encoding="utf-8"))

    def test_no_year_advancement_and_single_pet_module(self):
        e, q = self.e, self.q
        year = next(y for y in q["yearly_work_queue"] if y["year"] == 2019)
        annual_2018 = next(y for y in q["yearly_work_queue"] if y["year"] == 2018)
        self.assertEqual(e["active_module"], q["active_module"])
        self.assertEqual(e["active_module"], "PET")
        self.assertEqual((e["year_frontier_before"], e["year_frontier_after"]), (2019, 2019))
        self.assertEqual(year["research_gate"], "NOT_YEAR_AUDITED")
        self.assertEqual(q["current_frontier"]["year"], 2019)
        self.assertTrue(q["current_frontier"]["next"].startswith("PET117:"))
        self.assertEqual(annual_2018["research_gate"], "SOURCE_BOUNDED_REVIEWED")
        self.assertFalse(annual_2018["historically_complete"])
        self.assertEqual(q["current_frontier"]["latest_source_bounded_annual_review"], "PET115-YEAR2018-SIX-REGION-CLASSIC-PC-SOURCE-BOUNDED-AUDIT-20261118")
        self.assertFalse(e["historically_complete"])
        self.assertIsNone(e["official_2019_first_release_species_count"])

    def test_exact_eight_earlier_name_counterevidence_without_proven_identity(self):
        e = self.e
        seasons = {x["id"]: x for x in e["seasonal_groups"]}
        self.assertEqual(len(seasons), 2)
        fat = seasons["TW2019-DRAGONBOAT-FAT_DRAGON"]["names"]
        sea = seasons["TW2019-SUMMER-SEA_DRAGON"]["names"]
        earlier = e["cross_year_2006_player_name_counterevidence"]
        self.assertEqual(len(fat), 4)
        self.assertEqual(len(sea), 4)
        self.assertEqual(len(set(fat + sea)), 8)
        self.assertEqual(fat, earlier["fat_dragon_names"])
        self.assertEqual(sea, earlier["sea_monster_names"])
        self.assertEqual(earlier["source_date"], "2006-11-29")
        self.assertEqual(earlier["matching_literal_name_count"], 8)
        self.assertFalse(seasons["TW2019-SUMMER-SEA_DRAGON"]["same_native_identity_between_years_verified"])
        self.assertFalse(seasons["TW2019-DRAGONBOAT-FAT_DRAGON"]["official_release_first_2019_proved"])
        self.assertFalse(seasons["TW2019-SUMMER-SEA_DRAGON"]["official_release_first_2019_proved"])
        self.assertTrue(all(e["negative_controls"].values()))
        self.assertEqual(e["player_summer_quest_candidate"]["strengthen_fruit_count_player_claim"], 3)
        self.assertFalse(e["player_summer_quest_candidate"]["native_pet_skill_function_verified"])

    def test_client_and_official_issuance_missing_but_not_species_zero(self):
        e = self.e
        for k in ("new_original_2019_classic_pc_installer_bytes", "new_original_2019_classic_pc_patch_bytes",
                  "new_original_same_build_native_pet_ids", "new_original_spr_frames",
                  "new_native_same_build_skill_functions", "new_original_official_live_pet_issuance_logs"):
            self.assertEqual(e[k], 0)
        self.assertIsNone(e["global_2019_original_classic_pc_species_population"])
        self.assertEqual(len(e["sources"]), len({x["id"] for x in e["sources"]}))
        self.assertEqual(len(e["remaining_region_audit"]), 6)
        self.assertTrue(e["reject_mobile_backfill"]["not_original_pc"])

    def test_forward_only_queue_and_large_state_preservation(self):
        e, q = self.e, self.q
        year = next(y for y in q["yearly_work_queue"] if y["year"] == 2019)
        self.assertEqual(len(year["partial_source_review_receipts"]), 1)
        self.assertEqual(year["partial_source_review_receipts"][0]["id"], e["id"])
        self.assertEqual(q["current_frontier"]["latest_2019_partial_source_receipt"], e["id"])
        self.assertTrue(year["partial_source_review_receipts"][0]["year_not_closed"])
        self.assertEqual((e["stage_A"], e["stage_B_wiki"], e["r79"], e["overall_percent"]),
                         (q["stage_A"], q["stage_B_wiki"], q["r79"], q["overall_game_completion_percent"]))
        raw = (ROOT / "docs/CURRENT-STATE.md").read_bytes()
        self.assertEqual(len(raw), e["baseline"]["current_original_bytes"])
        blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        self.assertEqual(blob, e["baseline"]["current_original_blob"])
        report = R.read_text(encoding="utf-8")
        self.assertIn("2006-11-29", report)
        self.assertIn("NOT_YEAR_AUDITED", report)
        self.assertIn("NEXT `PET117`", report)


if __name__ == "__main__":
    unittest.main()
