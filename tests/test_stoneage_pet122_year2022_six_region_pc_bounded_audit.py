"""PET122: six-region 2022 original-PC pet source-bounded audit, 2023 year handoff."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / "research/recovered/STONEAGE-PET122-YEAR2022-SIX-REGION-CLASSIC-PC-BOUNDED-AUDIT-R1.json"
Q = ROOT / "research/recovered/STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json"
REPORT = ROOT / "docs/continuity/STONEAGE-PET122-YEAR2022-SIX-REGION-CLASSIC-PC-BOUNDED-AUDIT-20261119.md"
REGIONS = {"CN", "TW", "HK_MO", "KR", "JP", "OTHER"}


class Pet122Year2022SourceBoundedAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = json.loads(A.read_text(encoding="utf-8"))
        cls.q = json.loads(Q.read_text(encoding="utf-8"))

    def test_year_2022_source_bounded_reopenable_and_2023_handoff(self):
        a, q = self.a, self.q
        y = next(x for x in q["yearly_work_queue"] if x["year"] == 2022)
        n = next(x for x in q["yearly_work_queue"] if x["year"] == 2023)
        self.assertEqual((a["year_frontier_before"], a["year_frontier_after"]), (2022, 2023))
        self.assertEqual((a["active_module"], q["active_module"]), ("PET", "PET"))
        self.assertEqual((a["review_status"], y["research_gate"]),
                         ("SOURCE_BOUNDED_REVIEWED", "SOURCE_BOUNDED_REVIEWED"))
        self.assertIn(n["research_gate"], {"NOT_YEAR_AUDITED", "SOURCE_BOUNDED_REVIEWED"})
        self.assertGreaterEqual(q["current_frontier"]["year"], 2023)
        self.assertGreaterEqual(int(q["current_frontier"]["next"].split(":")[0][3:]), 123)
        self.assertFalse(a["historically_complete"])
        self.assertFalse(y["historically_complete"])
        self.assertTrue(a["year_reopenable"])
        self.assertTrue(y["year_reopenable"])
        self.assertIsNone(a["original_pc_global_2022_species_count"])
        self.assertIsNone(a["original_pc_2022_first_release_species_count"])
        self.assertIsNone(y["historical_species_count"])
        self.assertEqual(y["source_bounded_review_receipt"], str(A.relative_to(ROOT)))
        self.assertIn(a["id"], [x["id"] for x in y["partial_source_review_receipts"]])
        self.assertIn(a["id"], [x["id"] for x in q["root_source_census_receipts"]])

    def test_all_six_regions_source_native_limits_and_reopen_triggers(self):
        a, q = self.a, self.q
        y = next(z for z in q["yearly_work_queue"] if z["year"] == 2022)
        self.assertEqual(set(a["region_reviews"]), REGIONS)
        self.assertEqual(set(y["region_source_reviews"]), REGIONS - {"HK_MO"})
        self.assertEqual(set(y["additional_region_reviews"]), {"HK_MO"})
        self.assertEqual(len(set(y["residual_reopen_triggers"])), 6)
        self.assertEqual(y["residual_reopen_triggers"],
                         [x["reopen_trigger"] for x in a["region_reviews"].values()])
        for region, v in a["region_reviews"].items():
            qr = y["region_source_reviews"].get(region) or y["additional_region_reviews"][region]
            self.assertEqual(qr["reopen_trigger"], v["reopen_trigger"])
            self.assertEqual(qr["source_boundary"], v["source_boundary"])
            self.assertEqual(qr["review_status"], "SOURCE_BOUNDED_REVIEWED")
            self.assertFalse(qr["historically_complete"])
            self.assertIsNone(qr["pet_population"])
            self.assertIsNone(qr["official_2022_first_release_species_count"])
            self.assertEqual(qr["native_pet_id_rows_verified"], 0)
        for key in ("new_original_pc_client_bytes", "new_original_pc_patch_bytes",
                    "new_native_pet_id_rows", "new_original_pc_spr_frames",
                    "new_native_skill_functions", "new_original_server_pet_grants"):
            self.assertEqual(a[key], 0)
        self.assertTrue(all(a["negative_controls"].values()))

    def test_taiwan_firsthand_vs_pool_and_2024_retrospective_and_korean_mobile(self):
        a = self.a
        ss = {x["id"]: x for x in a["sources"]}
        self.assertEqual(len(ss), len(a["sources"]))
        self.assertGreaterEqual(len(ss), 9)
        tiger = ss["TW2022-JAN29-TIGER-PLAYER-FIRSTHAND"]
        self.assertEqual(tiger["firsthand_reward"]["pet_label"], "莫可")
        self.assertEqual(tiger["firsthand_reward"]["consumed_item"], "銀色虎牙")
        self.assertFalse(tiger["firsthand_reward"]["original_server_log_verified"])
        self.assertFalse(tiger["same_player_reported_prize_candidates"][0]["firsthand_this_player_obtained"])
        self.assertIn("莫洛特", tiger["same_player_reported_prize_candidates"][0]["summoned_pet_claim"])
        older = ss["TW2022-MIDAUTUMN-RETROSPECT-2024"]
        self.assertEqual(older["claimed_game_event_year"], 2022)
        self.assertTrue(older["source_last_edit_display"].startswith("2024-11-05"))
        self.assertEqual(older["player_claim_obtainable_pet_labels"], ["阿道夫狼", "人寵阿道夫"])
        self.assertIn("白狼扣環", older["item_labels"])
        self.assertFalse(older["native_2022_bytes_obtained"])
        copy = ss["TW2022-MIDAUTUMN-COPY-2024-C-INDEX"]
        self.assertEqual(copy["not_independent_from"], older["id"])
        link = ss["TW2022-FEB17-COMMUNITY-CLIENT-LINK"]
        self.assertFalse(link["actual_file_downloaded"])
        self.assertFalse(link["official_distribution_proved"])
        self.assertIsNone(link["sha256"])
        mobile = ss["KR2022-FEB07-WORLD-MOBILE-OPERATOR"]
        self.assertEqual(mobile["product"], "NETMARBLE_STONEAGE_WORLD_MOBILE")
        self.assertEqual(mobile["announced_new_pet_labels"], ["사루아치"])
        self.assertEqual(len(mobile["six_star_upgraded_mecha_pets"]), 5)
        self.assertIn("2022", REPORT.read_text(encoding="utf-8"))
        self.assertIn("PET122", (ROOT / "docs/STONEAGE-PET-CHRONOLOGICAL-RESTORATION-ORDER-R1.md").read_text(encoding="utf-8"))
        self.assertIn("PET122", (ROOT / "README.md").read_text(encoding="utf-8"))

    def test_original_git_blob_full_bytes_preserved(self):
        a, q = self.a, self.q
        raw = (ROOT / "docs/CURRENT-STATE.md").read_bytes()
        self.assertEqual(len(raw), a["baseline"]["current_state_bytes"])
        git_sha = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\x00" + raw).hexdigest()
        self.assertEqual(git_sha, a["baseline"]["current_state_blob"])
        self.assertEqual((a["stage_A"], a["stage_B_wiki"], a["r79"], a["overall_percent"]),
                         (q["stage_A"], q["stage_B_wiki"], q["r79"], q["overall_game_completion_percent"]))


if __name__ == "__main__":
    unittest.main()
