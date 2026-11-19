"""PET121: six-region 2021 original-PC annual source-bounded review, mobile segregation."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / "research/recovered/STONEAGE-PET121-YEAR2021-SIX-REGION-CLASSIC-PC-BOUNDED-AUDIT-R1.json"
Q = ROOT / "research/recovered/STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json"
REPORT = ROOT / "docs/continuity/STONEAGE-PET121-YEAR2021-SIX-REGION-CLASSIC-PC-BOUNDED-AUDIT-20261119.md"
REGIONS = {"CN", "TW", "HK_MO", "KR", "JP", "OTHER"}


class Pet121Year2021BoundedAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = json.loads(A.read_text(encoding="utf-8"))
        cls.q = json.loads(Q.read_text(encoding="utf-8"))

    def test_source_bounded_year_handoff(self):
        a, q = self.a, self.q
        y = next(v for v in q["yearly_work_queue"] if v["year"] == 2021)
        n = next(v for v in q["yearly_work_queue"] if v["year"] == 2022)
        self.assertEqual((a["year_frontier_before"], a["year_frontier_after"]), (2021, 2022))
        self.assertEqual(y["research_gate"], "SOURCE_BOUNDED_REVIEWED")
        self.assertIn(n["research_gate"], {"NOT_YEAR_AUDITED", "SOURCE_BOUNDED_REVIEWED"})
        self.assertGreaterEqual(q["current_frontier"]["year"], 2022)
        self.assertGreaterEqual(int(q["current_frontier"]["next"].split(":")[0][3:]), 122)
        self.assertEqual((a["active_module"], q["active_module"]), ("PET", "PET"))
        self.assertTrue(a["year_reopenable"])
        self.assertFalse(a["historically_complete"])
        self.assertFalse(y["historically_complete"])
        self.assertIsNone(a["original_pc_global_2021_species_count"])
        self.assertIsNone(a["original_pc_2021_first_release_species_count"])
        self.assertIsNone(y["historical_species_count"])
        self.assertEqual(y["source_bounded_review_receipt"], str(A.relative_to(ROOT)))
        self.assertIn(a["id"], [z["id"] for z in y["partial_source_review_receipts"]])
        self.assertIn(a["id"], [z["id"] for z in q["root_source_census_receipts"]])
        self.assertEqual(q["yearly_work_queue"][22]["year"], 2021)

    def test_all_six_region_reopen_guards(self):
        a, q = self.a, self.q
        y = next(z for z in q["yearly_work_queue"] if z["year"] == 2021)
        self.assertEqual(set(a["region_reviews"]), REGIONS)
        self.assertEqual(set(y["region_source_reviews"]), REGIONS - {"HK_MO"})
        self.assertEqual(set(y["additional_region_reviews"]), {"HK_MO"})
        self.assertEqual(len(set(y["residual_reopen_triggers"])), 6)
        for region, value in a["region_reviews"].items():
            actual = y["region_source_reviews"].get(region) or y["additional_region_reviews"][region]
            self.assertEqual(actual["reopen_trigger"], value["reopen_trigger"])
            self.assertEqual(actual["source_boundary"], value["source_boundary"])
            self.assertEqual(actual["review_status"], "SOURCE_BOUNDED_REVIEWED")
            self.assertEqual(actual["native_pet_id_rows_verified"], 0)
            self.assertIsNone(actual["pet_population"])
            self.assertIsNone(actual["official_2021_first_release_species_count"])
            self.assertFalse(actual["historically_complete"])
        for key in ("new_original_pc_client_bytes", "new_original_pc_patch_bytes",
                    "new_native_pet_id_rows", "new_original_pc_spr_frames",
                    "new_native_skill_functions", "new_original_server_pet_grants"):
            self.assertEqual(a[key], 0)
        self.assertTrue(all(a["negative_controls"].values()))

    def test_player_quest_enemies_temporary_wolves_and_mobile_line(self):
        a = self.a
        s = {x["id"]: x for x in a["sources"]}
        self.assertEqual(len(s), len(a["sources"]))
        spring = s["TW2021-SPRING-FESTIVAL-PLAYER-G2"]
        autumn = s["TW2021-MIDAUTUMN-PLAYER-G2"]
        self.assertIn("布爾摩", spring["candidate_enemy_labels"])
        self.assertIn("牛年挑戰券", spring["candidate_item_labels"])
        self.assertIn("12_25", a["source_boundaries"]["tw_player_guides"])
        self.assertEqual(autumn["reward_kind"], "REWARD_OBJECT_KIND_UNVERIFIED")
        self.assertIn("牛人布偶", autumn["candidate_reward_labels"])
        self.assertIn("UNVERIFIED", a["source_boundaries"]["tw_legal_authorisation"])
        self.assertIn("FIRSTPARTY_MOBILE", s["KR2021-MOBILE-MAR-LEVIATHAN"]["grade"])
        self.assertIn("FIRSTPARTY_MOBILE", s["KR2021-MOBILE-JUN-AQUDON"]["grade"])
        self.assertIn("FIRSTPARTY_MOBILE", s["KR2021-MOBILE-DEC-MECHA"]["grade"])
        self.assertIn("29日", s["KR2021-MOBILE-SHUI-DATE-CONFLICT"]["body_date_expression"])
        self.assertIn("2021", REPORT.read_text(encoding="utf-8"))
        self.assertIn("PET121", (ROOT / "README.md").read_text(encoding="utf-8"))

    def test_full_historical_git_blob_unchanged(self):
        a, q = self.a, self.q
        raw = (ROOT / "docs/CURRENT-STATE.md").read_bytes()
        self.assertEqual(len(raw), a["baseline"]["current_state_bytes"])
        sha = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\x00" + raw).hexdigest()
        self.assertEqual(sha, a["baseline"]["current_state_blob"])
        self.assertEqual((a["stage_A"], a["stage_B_wiki"], a["r79"], a["overall_percent"]),
                         (q["stage_A"], q["stage_B_wiki"], q["r79"], q["overall_game_completion_percent"]))


if __name__ == "__main__":
    unittest.main()
