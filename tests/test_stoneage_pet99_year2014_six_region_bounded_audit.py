"""PET99: 2014 six-region original PC PET evidence was audited, not historically completed."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REC = ROOT / "research/recovered"
A = REC / "STONEAGE-PET99-YEAR2014-SIX-REGION-ORIGINAL-PC-PET-BOUNDED-AUDIT-R1.json"
Q = REC / "STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json"
REPORT = ROOT / "docs/continuity/STONEAGE-PET99-YEAR2014-SIX-REGION-ORIGINAL-PC-PET-BOUNDED-AUDIT-20261118.md"

class Pet99Year2014BoundedAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = json.loads(A.read_text(encoding="utf-8"))
        cls.q = json.loads(Q.read_text(encoding="utf-8"))

    def test_year_advance_does_not_mean_pets_are_complete(self):
        a,q=self.a,self.q
        y=q["yearly_work_queue"][15]
        self.assertEqual((a["year_frontier_before"],a["year_frontier_after"]),(2014,2015))
        self.assertEqual(a["review_status"],"SOURCE_BOUNDED_REVIEWED")
        self.assertTrue(a["year_source_bounded_closed"])
        self.assertTrue(a["year_reopenable"])
        self.assertTrue(a["source_bounded_only"])
        self.assertFalse(a["historically_complete"])
        self.assertEqual(y["research_gate"],"SOURCE_BOUNDED_REVIEWED")
        self.assertFalse(y["historically_complete"])
        self.assertIsNone(y["historical_species_count"])
        self.assertEqual(y["source_bounded_review_receipt"],str(A.relative_to(ROOT)))
        self.assertEqual(q["yearly_work_queue"][16]["research_gate"],"SOURCE_BOUNDED_REVIEWED")
        self.assertGreaterEqual(q["current_frontier"]["year"],2015)
        self.assertTrue(a["next"].startswith("PET100:"))
        self.assertEqual(q["active_module"],"PET")
        self.assertIn("PET99",REPORT.read_text(encoding="utf-8"))

    def test_original_receipts_preserved_and_six_regions_are_reopenable(self):
        a,q=self.a,self.q
        self.assertEqual(len(a["prior_receipts"]),4)
        y=q["yearly_work_queue"][15]
        self.assertEqual([x["id"] for x in y["partial_source_review_receipts"]][:4],a["prior_receipts"])
        self.assertEqual(y["partial_source_review_receipts"][-1]["id"],a["id"])
        self.assertIn(a["id"],[x["id"] for x in q["root_source_census_receipts"]])
        self.assertEqual(len(q["root_source_census_receipts"]),len({x["id"] for x in q["root_source_census_receipts"]}))
        self.assertEqual(set(a["region_reviews"]),{"CN","TW","HK_MO","KR","JP","OTHER"})
        self.assertEqual(len(a["reopen_triggers"]),6)
        self.assertEqual(len(set(a["reopen_triggers"])),6)
        self.assertEqual(y["residual_reopen_triggers"],a["reopen_triggers"])
        self.assertEqual(set(y["region_source_reviews"]),{"CN","TW","KR","JP","OTHER"})
        self.assertEqual(set(y["additional_region_reviews"]),{"HK_MO"})
        for region,info in a["region_reviews"].items():
            row=y["region_source_reviews"].get(region) or y["additional_region_reviews"].get(region)
            self.assertEqual(row["reopen_trigger"],info["trigger"])
            self.assertEqual(row["review_status"],"SOURCE_BOUNDED_REVIEWED")
            self.assertFalse(row["historically_complete"])
            self.assertIsNone(row["pet_population"])
            self.assertEqual(row["native_pet_id_rows_verified"],0)

    def test_later_rescued_quest_text_is_not_pet_id_or_2014_operator(self):
        a=self.a
        self.assertEqual(len(a["new_source_audit"]),1)
        src=a["new_source_audit"][0]
        self.assertEqual(src["document_edit_date"],"2015-04-08")
        self.assertFalse(src["original_operator_2014"])
        self.assertFalse(src["original_2014_pet_grant_verified"])
        self.assertFalse(src["box_contents_verified"])
        self.assertFalse(src["exact_revision_date_verified"])
        self.assertIn("4236",src["url"])
        self.assertIn("端午蛇盒子"," ".join(src["claims"]))
        self.assertIn("沒有寵物"," ".join(src["claims"]))
        self.assertTrue(all(a["negative_controls"].values()))
        self.assertIn("NOT_PROVEN",a["grade_disambiguation"]["gift_box_name"])

    def test_no_native_source_issuance_and_exact_current_history(self):
        a,q=self.a,self.q
        for k in ["new_native_client_bytes","new_patch_bytes","new_native_pet_ids","new_native_spr_pixels","new_skill_functions","new_server_grants"]:
            self.assertEqual(a[k],0)
        self.assertIsNone(a["global_original_pc_pet_species_count_2014"])
        self.assertIsNone(a["first_release_species_count_2014"])
        raw=(ROOT/"docs/CURRENT-STATE.md").read_bytes()
        self.assertEqual(len(raw),2709173)
        gitblob=hashlib.sha1(b"blob "+str(len(raw)).encode("ascii")+b"\x00"+raw).hexdigest()
        self.assertEqual(gitblob,a["starting_remote"]["original_current_blob"])
        self.assertTrue(a["historical_current_unchanged"])
        self.assertEqual((q["stage_A"],q["stage_B_wiki"],q["r79"],q["overall_game_completion_percent"]),("7_PARTIAL_2_OPEN","GATED","PAUSED_NON_BLOCKING",None))
        self.assertEqual((a["stage_A"],a["stage_B_wiki"],a["r79"],a["overall_percent"]),(q["stage_A"],q["stage_B_wiki"],q["r79"],q["overall_game_completion_percent"]))

if __name__ == "__main__":
    unittest.main()
