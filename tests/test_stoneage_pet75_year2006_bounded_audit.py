"""PET75: 2006 five-region source-bounded review, no species-count or source-date promotion."""
import json,unittest
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]/"research"/"recovered"
def rd(s):return json.loads((BASE/s).read_text(encoding="utf-8"))
class PET75Annual(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.a=rd("STONEAGE-PET75-YEAR2006-FIVE-REGION-BOUNDED-AUDIT-R1.json")
  cls.p=rd("STONEAGE-PET74-YEAR2006-CN-TW-JP-KR-PARTIAL-R1.json")
  cls.q=rd("STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json")
 def test_chronology_moves_bounded_not_complete(self):
  a,p,q=self.a,self.p,self.q
  y=q["yearly_work_queue"][2006-1999]
  self.assertEqual((a["year_frontier_before"],a["year_frontier_after"]),(2006,2007))
  self.assertEqual(q["current_frontier"]["year"],2007)
  self.assertTrue(q["current_frontier"]["next"].startswith("PET76:"))
  self.assertEqual(y["research_gate"],"SOURCE_BOUNDED_REVIEWED")
  self.assertFalse(y["historically_complete"])
  self.assertIsNone(y["historical_species_count"])
  self.assertEqual(y["source_bounded_review_receipt"],"research/recovered/STONEAGE-PET75-YEAR2006-FIVE-REGION-BOUNDED-AUDIT-R1.json")
  self.assertEqual(q["yearly_work_queue"][2007-1999]["research_gate"],"NOT_YEAR_AUDITED")
  self.assertEqual((p["year_frontier_after"],p["year_research_gate_after"]),(2006,"NOT_YEAR_AUDITED"))
  self.assertEqual(y["documentary_event_count_NOT_species"],1)
  self.assertEqual(y["documented_release_event_ids_from_existing_PET25_PET26"],["JP-2006-TWO-MYSTERY"])
 def test_five_regions_missing_native_and_qualified_reopening(self):
  a,q=self.a,self.q
  self.assertEqual(set(a["region_reviews"]),{"CN","TW","JP","KR","OTHER"})
  y=q["yearly_work_queue"][7]
  self.assertEqual(set(y["region_source_reviews"]),set(a["region_reviews"]))
  self.assertEqual(len(y["residual_reopen_triggers"]),5)
  self.assertEqual(y["residual_reopen_triggers"],a["five_region_residual_reopen_triggers"])
  for region,x in a["region_reviews"].items():
   self.assertIsNone(x["pet_population"])
   self.assertIsNone(y["region_source_reviews"][region]["pet_population"])
   self.assertTrue(x["authentic_2006_complete_original_client_missing"])
   self.assertEqual(x["native_pet_id_rows_verified"],0)
   self.assertFalse(x["actual_reward_grant_log_verified"])
   self.assertEqual(x["reopen_trigger"],y["region_source_reviews"][region]["reopen_trigger"])
  self.assertTrue(a["all_region_2006_pet_populations_unknown"])
 def test_false_identity_promotions_guarded(self):
  a=self.a
  self.assertTrue(all(a["evidence_boundaries"].values()) if all(isinstance(v,bool) for v in a["evidence_boundaries"].values()) else all(v is True or v==0 for v in a["evidence_boundaries"].values()))
  self.assertEqual(a["region_reviews"]["TW"]["retrospective_only_dog_names"],["布魯多基","哈斯多基","畢格多基","普格多基"])
  self.assertTrue(a["region_reviews"]["TW"]["dog_pack_date_2005_later_chronology_only"])
  self.assertTrue(a["region_reviews"]["JP"]["stoneage2_separate_product_line"])
  self.assertTrue(a["region_reviews"]["KR"]["same_original_release_semantics_enriched_not_new_independent_witness"])
  self.assertTrue(a["region_reviews"]["CN"]["distinct_live_service_tracks"])
  self.assertIsNone(a["global_official_2006_unique_species_count"])
 def test_source_inventory_and_bytes(self):
  a=self.a
  self.assertEqual(len(a["new_evidence_and_prior_reinspection"]),9)
  self.assertEqual(len({s["id"] for s in a["new_evidence_and_prior_reinspection"]}),9)
  self.assertTrue(all(not s["native_pet_species_count_eligible"] for s in a["new_evidence_and_prior_reinspection"]))
  self.assertEqual((a["new_2006_original_client_bytes"],a["new_native_2006_pet_ids"],a["new_native_reward_grant_logs"]),(0,0,0))
  self.assertEqual(a["official_free_client_check"]["original_binary_bytes_read"],0)
  self.assertIsNone(a["official_free_client_check"]["original_SHA256"])
  self.assertFalse(a["official_free_client_check"]["carrier_official_authentication"])
  self.assertTrue(a["no_paid_marketplace"])
  self.assertTrue(a["historical_CURRENT_unchanged"])
  self.assertEqual(a["startup"]["historical_CURRENT_blob"],"c89e0e33537990aa2132b47c40fef49a985a935c")
 def test_single_forward_only_receipt(self):
  a,p,q=self.a,self.p,self.q
  arr=q["root_source_census_receipts"]
  self.assertEqual(sum(x["id"]==a["id"] for x in arr),1)
  self.assertEqual(sum(x["id"]==p["id"] for x in arr),1)
  self.assertEqual(len({x["id"] for x in arr}),len(arr))
  self.assertEqual(q["yearly_work_queue"][7]["partial_source_review_receipts"][0]["id"],p["id"])
  self.assertIsNone(q["root_source_census_receipts"][-1]["historical_species_count"])
  self.assertEqual((a["stage_A"],a["stage_B_wiki"],a["r79"] ),("7_PARTIAL_2_OPEN","GATED","PAUSED_NON_BLOCKING"))
  self.assertIsNone(a["overall_percent"])
if __name__=="__main__":unittest.main()
