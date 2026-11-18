"""PET94: 2013 original-PC source-bounded six-region annual audit; 2014 handoff only."""
import hashlib
import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
REC = ROOT / "research/recovered"
def load(n): return json.loads((REC / n).read_text(encoding='utf-8'))
class Pet94Year2013(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a=load("STONEAGE-PET94-YEAR2013-SIX-REGION-ORIGINAL-PC-PET-BOUNDED-AUDIT-R1.json")
        cls.q=load("STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json")
    def test_2013_documentary_gate_to_2014_not_historical_complete(self):
        a,q=self.a,self.q
        y=q["yearly_work_queue"][14]
        self.assertEqual((a["year"],a["year_frontier_before"],a["year_frontier_after"]),(2013,2013,2014))
        self.assertGreaterEqual(q["current_frontier"]["year"],2014)
        self.assertEqual(q["yearly_work_queue"][15]["research_gate"],"SOURCE_BOUNDED_REVIEWED")
        self.assertEqual(y["research_gate"],"SOURCE_BOUNDED_REVIEWED")
        self.assertEqual(y["source_bounded_review_receipt"],"research/recovered/STONEAGE-PET94-YEAR2013-SIX-REGION-ORIGINAL-PC-PET-BOUNDED-AUDIT-R1.json")
        self.assertFalse(y["historically_complete"])
        self.assertIsNone(y["historical_species_count"])
        self.assertFalse(a["historically_complete"])
        self.assertTrue(a["source_bounded_only"])
        self.assertTrue(a["year_source_bounded_closed"])
        self.assertTrue(a["year_reopenable"])
        self.assertIsNone(a["global_original_pc_pet_species_count_2013"])
        self.assertIsNone(a["first_release_2013_species_count"])
        self.assertGreaterEqual(int(q["current_frontier"]["next"].split(":")[0][3:]),97)
    def test_2013_receipts_prefix_preserved_and_six_gates(self):
        a,q=self.a,self.q
        self.assertEqual(len(a["prior_receipts"]),3)
        self.assertEqual([x["id"] for x in q["yearly_work_queue"][14]["partial_source_review_receipts"]],a["prior_receipts"]+[a["id"]])
        self.assertIn(a["id"],[x["id"] for x in q["root_source_census_receipts"]])
        self.assertEqual(len({x["id"] for x in q["root_source_census_receipts"]}),len(q["root_source_census_receipts"]))
        self.assertEqual(len(set(a["reopen_triggers"])),6)
        self.assertEqual(set(a["region_reviews"]),{"CN","TW","HK_MO","KR","JP","OTHER"})
        self.assertEqual(set(q["yearly_work_queue"][14]["region_source_reviews"]),{"CN","TW","KR","JP","OTHER"})
        self.assertEqual(set(q["yearly_work_queue"][14]["additional_region_reviews"]),{"HK_MO"})
        self.assertEqual(q["yearly_work_queue"][14]["residual_reopen_triggers"],a["reopen_triggers"])
        self.assertEqual(q["yearly_work_queue"][13]["research_gate"],"SOURCE_BOUNDED_REVIEWED")
        self.assertEqual(q["active_module"],"PET")
    def test_each_region_unknown_population_and_reopen_trigger(self):
        a,q=self.a,self.q
        self.assertEqual(len(a["region_reviews"]),6)
        for region,info in a["region_reviews"].items():
            self.assertEqual(info["region"],region)
            self.assertEqual(info["review_status"],"SOURCE_BOUNDED_REVIEWED")
            self.assertFalse(info["historically_complete"])
            self.assertIsNone(info["pet_population"])
            self.assertEqual(info["native_pet_id_rows_verified_in_review"],0)
            self.assertFalse(info["real_original_server_pet_grant_verified"])
            row=q["yearly_work_queue"][14]["region_source_reviews"].get(region) or q["yearly_work_queue"][14]["additional_region_reviews"].get(region)
            self.assertEqual(row["reopen_trigger"],info["trigger"])
    def test_new_corroboration_not_original_official_issue(self):
        a=self.a
        self.assertEqual(a["source_count"],6)
        self.assertEqual(len(a["source_audit"]),6)
        self.assertEqual(len({x["url"] for x in a["source_audit"]}),6)
        tw=[x for x in a["source_audit"] if x["region"]=="TW"]
        self.assertEqual(len(tw),5)
        self.assertEqual(len(tw[0]["labels"]),13)
        self.assertFalse(tw[0]["official_new_pet_verified"])
        self.assertTrue(tw[3]["crowd_data_loss_acknowledged"])
        self.assertFalse(tw[3]["official_live_issue_verified"])
        jp=[x for x in a["source_audit"] if x["region"]=="JP"][0]
        self.assertTrue(jp["first_party"])
        self.assertEqual(jp["product_line"],"STONEAGE_MOBILE")
        self.assertFalse(jp["original_pc_relaunch_verified"])
        self.assertFalse(jp["actual_mobile_launch_verified"])
        self.assertTrue(all(a["source_negative_controls"].values()))
    def test_no_original_binary_or_runtime_added(self):
        a=self.a
        self.assertEqual((a["new_native_client_bytes"],a["new_native_pet_ids"],a["new_spr_pixels"],a["new_skill_functions"],a["new_server_grants"]),(0,0,0,0,0))
        self.assertEqual(a["prior_source_rows_not_unique_species"],21)
        self.assertEqual(len(a["related_prior_source_controls"]),3)
    def test_current_native_blob_unchanged_and_stage_guard(self):
        a,q=self.a,self.q
        raw=(ROOT/"docs/CURRENT-STATE.md").read_bytes()
        self.assertEqual(len(raw),2709173)
        self.assertEqual(hashlib.sha1(b"blob "+str(len(raw)).encode("ascii")+b"\x00"+raw).hexdigest(),a["original_current_blob"])
        self.assertTrue(a["historical_CURRENT_untouched"])
        self.assertEqual((q["stage_A"],q["stage_B_wiki"],q["r79"],q["overall_game_completion_percent"]),("7_PARTIAL_2_OPEN","GATED","PAUSED_NON_BLOCKING",None))
if __name__ == "__main__": unittest.main()
