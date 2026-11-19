"""PET125: 2025 classic PC only, three TW player sources, independent PC remake boundary."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / "research/recovered/STONEAGE-PET125-YEAR2025-SIX-REGION-CLASSIC-PC-BOUNDED-AUDIT-R1.json"
Q = ROOT / "research/recovered/STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json"
REPORT = ROOT / "docs/continuity/STONEAGE-PET125-YEAR2025-SIX-REGION-CLASSIC-PC-BOUNDED-AUDIT-20261119.md"
REGIONS = {"CN","TW","HK_MO","KR","JP","OTHER"}


class Pet125Year2025PCBoundedAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = json.loads(A.read_text(encoding="utf-8"))
        cls.q = json.loads(Q.read_text(encoding="utf-8"))
        cls.sources = {s["id"]:s for s in cls.a["sources"]}

    def test_2025_year_and_2026_cursor_without_invented_species(self):
        a,q = self.a,self.q
        y = next(v for v in q["yearly_work_queue"] if v["year"] == 2025)
        n = next(v for v in q["yearly_work_queue"] if v["year"] == 2026)
        self.assertEqual((a["year_frontier_before"],a["year_frontier_after"]), (2025,2026))
        self.assertEqual((a["active_module"],q["active_module"]),("PET","PET"))
        self.assertEqual((a["review_status"],y["research_gate"]),("SOURCE_BOUNDED_REVIEWED","SOURCE_BOUNDED_REVIEWED"))
        self.assertEqual(n["research_gate"],"NOT_YEAR_AUDITED")
        self.assertEqual(q["current_frontier"]["year"],2026)
        self.assertTrue(q["current_frontier"]["next"].startswith("PET126"))
        self.assertFalse(y["historically_complete"])
        self.assertTrue(y["year_reopenable"])
        self.assertIsNone(y["historical_species_count"])
        self.assertIsNone(a["original_pc_global_2025_species_count"])
        self.assertIsNone(a["original_pc_2025_first_release_species_count"])
        self.assertEqual(y["source_bounded_review_receipt"],str(A.relative_to(ROOT)))
        self.assertEqual(y["source_bounded_review_report"],str(REPORT.relative_to(ROOT)))
        self.assertIn(a["id"],[x["id"] for x in q["root_source_census_receipts"]])
        self.assertTrue(all(v["research_gate"]!="NOT_YEAR_AUDITED" for v in q["yearly_work_queue"] if v["year"]<2026))

    def test_six_region_reopen_and_evidence_zero_not_pets_zero(self):
        a,q=self.a,self.q
        self.assertEqual(set(a["region_reviews"]),REGIONS)
        y=next(v for v in q["yearly_work_queue"] if v["year"]==2025)
        self.assertEqual(set(y["region_source_reviews"]),REGIONS-{"HK_MO"})
        self.assertEqual(set(y["additional_region_reviews"]),{"HK_MO"})
        self.assertEqual(len(set(y["residual_reopen_triggers"])),6)
        for region,rec in a["region_reviews"].items():
            copy=y["region_source_reviews"].get(region) or y["additional_region_reviews"][region]
            self.assertEqual(copy,rec)
            self.assertTrue(rec["year_reopenable"])
            self.assertFalse(rec["historically_complete"])
            self.assertIsNone(rec["pet_population"])
            self.assertIsNone(rec["official_2025_first_release_species_count"])
            self.assertEqual(rec["native_pet_id_rows_verified"],0)
        for field in ("new_original_pc_client_bytes","new_original_pc_patch_bytes","new_native_pet_id_rows","new_original_pc_spr_frames","new_native_skill_functions","new_original_server_pet_grants"):
            self.assertEqual(a[field],0)
        self.assertTrue(all(a["negative_controls"].values()))

    def test_taiwan_candidate_names_are_not_new_species(self):
        a=self.a
        self.assertEqual(len(a["sources"]),3)
        self.assertTrue(all("CLASSIC_2D_PC" in x["product"] for x in a["sources"]))
        self.assertTrue(all(not x["first_release_year_proved"] for x in a["sources"]))
        spring=self.sources["TW2025-JAN16-SNAKE-NEWYEAR-PLAYER-OPERATOR-RELAY"]
        self.assertEqual(spring["player_named_reward_count"],4)
        self.assertEqual(len(spring["player_listed_reward_pet_names"]),4)
        summer=self.sources["TW2025-SUMMER-SEVEN-REWARD-POOL-PLAYER-INDEX"]
        self.assertEqual(summer["player_claimed_reward_pool_count"],7)
        self.assertEqual(len(summer["player_listed_reward_pet_names"]),7)
        self.assertIn("凱恩強化血清",summer["consumable_or_upgrade_labels"])
        autumn=self.sources["TW2025-AUTUMN-YINI-PLAYER-GUIDE-INDEX"]
        self.assertEqual(autumn["task_pet_label"],"依妮")
        self.assertEqual(autumn["end_reward_item_label"],"烏寶依布偶盾")
        self.assertTrue(all(s["native_pet_ids_verified"]==0 for s in a["sources"]))
        self.assertIn("PET125",REPORT.read_text(encoding="utf-8"))

    def test_independent_remake_not_original_pc_record(self):
        a=self.a
        b=a["pc_native_independent_remake_lineage_boundary"]
        self.assertFalse(b["active_classic_pc_pet_roster_inclusion"])
        self.assertIn("SEPARATE",b["classification"])
        self.assertEqual(b["first_party_announcement"]["date"],"2025-11-28")
        self.assertEqual(b["first_party_beta_report"]["date"],"2025-12-29")
        self.assertFalse(any("8yx.com" in s["url"] for s in a["sources"]))
        self.assertEqual(next(v for v in self.q["yearly_work_queue"] if v["year"]==2025)["documentary_event_count_NOT_species"],0)

    def test_original_current_state_and_stage_locked(self):
        a=self.a
        raw=(ROOT/"docs/CURRENT-STATE.md").read_bytes()
        self.assertEqual(len(raw),2709173)
        self.assertEqual(hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\x00"+raw).hexdigest(),a["baseline"]["current_state_blob"])
        self.assertEqual((a["stage_A"],a["stage_B_wiki"],a["r79"],a["overall_percent"]),(self.q["stage_A"],self.q["stage_B_wiki"],self.q["r79"],self.q["overall_game_completion_percent"]))


if __name__=="__main__":unittest.main()
