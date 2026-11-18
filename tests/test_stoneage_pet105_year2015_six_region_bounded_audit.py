"""PET105: six-region 2015 source-bounded year review, not population completeness."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REC=ROOT/"research/recovered"
A=REC/"STONEAGE-PET105-YEAR2015-SIX-REGION-ORIGINAL-PC-PET-BOUNDED-AUDIT-R1.json"
Q=REC/"STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json"
REPORT=ROOT/"docs/continuity/STONEAGE-PET105-YEAR2015-SIX-REGION-ORIGINAL-PC-PET-SOURCE-BOUNDED-AUDIT-20261118.md"

class Pet105Year2015SixRegionBoundedReview(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a=json.loads(A.read_text(encoding="utf-8"))
        cls.q=json.loads(Q.read_text(encoding="utf-8"))

    def test_2015_closed_only_for_reviewed_source_scope(self):
        a,q=self.a,self.q
        y=q["yearly_work_queue"][16]
        self.assertEqual((a["year_frontier_before"],a["year_frontier_after"]),(2015,2016))
        self.assertEqual(a["active_module"],"PET")
        self.assertEqual(a["review_status"],"SOURCE_BOUNDED_REVIEWED")
        self.assertTrue(a["year_source_bounded_closed"])
        self.assertTrue(a["source_bounded_only"])
        self.assertTrue(a["year_reopenable"])
        self.assertFalse(a["historically_complete"])
        self.assertEqual(y["research_gate"],"SOURCE_BOUNDED_REVIEWED")
        self.assertFalse(y["historically_complete"])
        self.assertIsNone(y["historical_species_count"])
        self.assertEqual(y["source_bounded_review_receipt"],str(A.relative_to(ROOT)))
        self.assertEqual(q["yearly_work_queue"][15]["research_gate"],"SOURCE_BOUNDED_REVIEWED")
        self.assertEqual(q["yearly_work_queue"][17]["research_gate"],"SOURCE_BOUNDED_REVIEWED")
        self.assertGreaterEqual(q["current_frontier"]["year"],2016)
        self.assertIn(a["id"],[v["id"] for v in q["root_source_census_receipts"]])
        self.assertIn(a["id"],[v["id"] for v in q["root_source_census_receipts"]])
        self.assertEqual(q["root_source_census_receipts"][-2]["id"],a["id"])  # 2016 PET110 follows
        self.assertEqual(next(v for v in q["root_source_census_receipts"] if v["id"]==a["id"])["year_frontier_after"],2016)
        self.assertEqual(q["active_module"],"PET")
        self.assertTrue(a["next"].startswith("PET106:"))
        self.assertTrue(q["current_frontier"]["next"].startswith("PET"))  # later PET batches may supersede a historical NEXT
        self.assertIn("PET105",REPORT.read_text(encoding="utf-8"))

    def test_five_prior_receipts_preserved_and_six_reopen_triggers(self):
        a,q=self.a,self.q
        y=q["yearly_work_queue"][16]
        self.assertEqual(len(a["prior_receipts"]),5)
        self.assertEqual([r["id"] for r in y["partial_source_review_receipts"]][:5],a["prior_receipts"])
        self.assertEqual(y["partial_source_review_receipts"][-1]["id"],a["id"])
        self.assertEqual([v["id"] for v in q["root_source_census_receipts"]][-7:-1],a["prior_receipts"]+[a["id"]])
        self.assertEqual(len(q["root_source_census_receipts"]),len({r["id"] for r in q["root_source_census_receipts"]}))
        self.assertEqual(set(a["region_reviews"]),{"CN","TW","HK_MO","KR","JP","OTHER"})
        self.assertEqual(len(a["reopen_triggers"]),6)
        self.assertEqual(len(set(a["reopen_triggers"])),6)
        self.assertEqual(y["residual_reopen_triggers"],a["reopen_triggers"])
        self.assertEqual(set(y["region_source_reviews"]),{"CN","TW","KR","JP","OTHER"})
        self.assertEqual(set(y["additional_region_reviews"]),{"HK_MO"})
        for region,info in a["region_reviews"].items():
            row=y["region_source_reviews"].get(region) or y["additional_region_reviews"].get(region)
            self.assertEqual(info["trigger"],row["reopen_trigger"])
            self.assertEqual(row["region"],region)
            self.assertEqual(row["review_status"],"SOURCE_BOUNDED_REVIEWED")
            self.assertFalse(row["historically_complete"])
            self.assertIsNone(row["pet_population"])
            self.assertEqual(row["native_pet_id_rows_verified"],0)
        self.assertTrue(any(x.startswith("PET105:") for x in y["source_bounded_partial_review_notes_forward_only"]))

    def test_later_guides_are_not_2015_official_pet_issuance(self):
        a=self.a
        src=a["new_source_audit"]
        self.assertEqual(len(src),3)
        self.assertEqual(len({s["id"] for s in src}),3)
        self.assertEqual(src[0]["date"],"2025-10-23")
        self.assertFalse(src[0]["independent_2015_original"])
        self.assertFalse(src[0]["original_native_pet_identity_2015"])
        self.assertEqual(src[1]["date"],"2016-06-13")
        self.assertTrue(src[1]["not_backfill_2015_reward_table"])
        self.assertTrue(src[1]["not_original_2015_pc_pet_records"])
        self.assertEqual(src[2]["date"],"2015-06-21 11:48:23")
        self.assertIn("好像",src[2]["text_claim"])
        self.assertFalse(src[2]["verified_server_build"])
        self.assertFalse(src[2]["first_2015_pet_issuance"])
        self.assertTrue(all(a["prior_source_limits"].values()))
        self.assertTrue(all(a["negative_controls"].values()))

    def test_no_original_pet_material_and_current_history_unchanged(self):
        a,q=self.a,self.q
        for k in ["new_native_client_bytes","new_patch_bytes","new_native_pet_ids","new_native_spr_pixels","new_skill_functions","new_server_grants"]:
            self.assertEqual(a[k],0)
        self.assertIsNone(a["global_original_pc_pet_species_count_2015"])
        self.assertIsNone(a["first_release_species_count_2015"])
        raw=(ROOT/"docs/CURRENT-STATE.md").read_bytes()
        self.assertEqual(len(raw),a["starting_remote"]["original_current_bytes"])
        digest=hashlib.sha1(b"blob "+str(len(raw)).encode("ascii")+b"\x00"+raw).hexdigest()
        self.assertEqual(digest,a["starting_remote"]["original_current_blob"])
        self.assertTrue(a["historical_current_unchanged"])
        self.assertEqual((q["stage_A"],q["stage_B_wiki"],q["r79"],q["overall_game_completion_percent"]),("7_PARTIAL_2_OPEN","GATED","PAUSED_NON_BLOCKING",None))
        self.assertEqual((a["stage_A"],a["stage_B_wiki"],a["r79"],a["overall_percent"]),(q["stage_A"],q["stage_B_wiki"],q["r79"],q["overall_game_completion_percent"]))

if __name__=="__main__":
    unittest.main()
