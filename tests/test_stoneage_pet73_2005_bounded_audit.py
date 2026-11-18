"""PET73: 2005 five-region source-bounded official PET annual audit and 2006 frontier."""
import json,unittest
from pathlib import Path
REC=Path(__file__).resolve().parents[1]/"research"/"recovered"
def rd(n): return json.loads((REC/n).read_text(encoding="utf8"))
class PET73Annual(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.a=rd("STONEAGE-PET73-YEAR2005-FIVE-REGION-AUDIT-R1.json")
  cls.q=rd("STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json")
  cls.prev=rd("STONEAGE-PET72-YEAR2005-CN-TW-JP-KR-SOURCE-R1.json")
 def test_new_JP_period_source_and_patch_stage_not_claimed_real(self):
  d=self.a
  x=d["new_source"]
  self.assertEqual((x["period_date"],x["planned_capture_monster_update_time"]),("2005-06-13","2005-07-mid"))
  self.assertEqual(x["operator"],"GAIAX")
  self.assertEqual(x["planned_new_huntable_species_count_unnamed"],"multiple")
  self.assertTrue(x["report_does_not_confirm_actual_July12_live_patch"])
  self.assertEqual(x["authentic_JP_2005_original_patched_pet_binary_acquired"],0)
  self.assertTrue(d["region_reviews"]["JP"]["art_preload_is_not_field_spawn_proof"])
  self.assertTrue(d["region_reviews"]["JP"]["black_tiger_as_of_july22_still_unidentified"])
 def test_regions_source_bounded_original_population_unknown(self):
  d,q=self.a,self.q
  y=next(x for x in q["yearly_work_queue"] if x["year"]==2005)
  self.assertEqual(d["review_status"],"SOURCE_BOUNDED_REVIEWED")
  self.assertFalse(d["historically_complete"])
  self.assertEqual(set(d["region_reviews"]),{"CN","TW","JP","KR","OTHER"})
  self.assertEqual(set(y["region_source_reviews"]),set(d["region_reviews"]))
  self.assertEqual(d["residual_reopen_triggers"],y["residual_reopen_triggers"])
  self.assertEqual(len(d["residual_reopen_triggers"]),5)
  self.assertEqual(y["research_gate"],"SOURCE_BOUNDED_REVIEWED")
  self.assertFalse(y["historically_complete"])
  self.assertIsNone(y["historical_species_count"])
  self.assertEqual(y["source_bounded_review_receipt"],"research/recovered/STONEAGE-PET73-YEAR2005-FIVE-REGION-AUDIT-R1.json")
  for reg,v in d["region_reviews"].items():
   self.assertTrue(v["reopen_trigger"],reg)
   self.assertFalse(v["historical_original_full_client_available"],reg)
   self.assertFalse(v["native_pet_master_verified"],reg)
   self.assertFalse(v["actual_native_award_log_verified"],reg)
   self.assertFalse(v["original_2005_production_issuance_confirmed"],reg)
   self.assertIsNone(v["historical_species_count"],reg)
   self.assertIsNone(y["region_source_reviews"][reg]["pet_population"],reg)
   self.assertTrue(y["region_source_reviews"][reg]["authentic_2005_complete_original_client_missing"],reg)
  self.assertFalse(d["region_reviews"]["OTHER"]["independently_proven_no_2005_official_pc_release"])
  self.assertIsNone(d["historical_global_2005_official_species_count"])
  self.assertTrue(d["all_region_pet_population_unknown"])
 def test_named_region_versions_and_no_historical_species_inflation(self):
  d=self.a
  self.assertEqual(d["region_reviews"]["CN"]["period_2005_pet_labels"],["牛头人","鸡年兽"])
  self.assertEqual(d["region_reviews"]["TW"]["period_2005_pet_labels"],["麒麟","萊福"])
  self.assertEqual(d["region_reviews"]["JP"]["period_2005_pet_labels"],["クロウリ","ガーヴィ","ヴァンレム"])
  self.assertEqual(d["region_reviews"]["KR"]["period_2005_pet_labels"],["고르고르","타쿠"])
  self.assertTrue(all(d["source_weight_separation"].values()))
  self.assertEqual(len(d["unresolved"]),9)
  self.assertEqual(len(self.prev["source_records"]),12)
  self.assertEqual(self.prev["year_research_gate_after"],"NOT_YEAR_AUDITED")
 def test_forward_year_2006_and_prior_receipts(self):
  d,q=self.a,self.q
  self.assertEqual((d["year_frontier_before"],d["year_frontier_after"]),(2005,2006))
  # The PET73 historical 2005->2006 handoff remains true after later annual audits.
  self.assertGreaterEqual(q["current_frontier"]["year"],2006)
  if q["current_frontier"]["year"]==2006:
   self.assertEqual(q["yearly_work_queue"][7]["research_gate"],"NOT_YEAR_AUDITED")
  else:
   self.assertEqual(q["yearly_work_queue"][7]["research_gate"],"SOURCE_BOUNDED_REVIEWED")
  self.assertEqual(q["yearly_work_queue"][2005-1999]["documentary_event_count_NOT_species"],0)
  self.assertEqual(d["previous_2005_PET25_PET26_documentary_event_count_unchanged"],0)
  receipts=q["root_source_census_receipts"]
  self.assertEqual(sum(x["id"]==d["id"] for x in receipts),1)
  self.assertEqual(sum(x["id"]==self.prev["id"] for x in receipts),1)
  self.assertEqual(len({x["id"] for x in receipts}),len(receipts))
  y=q["yearly_work_queue"][2005-1999]
  self.assertEqual(len(y["partial_source_review_receipts"]),2)
  self.assertEqual(sum(x["id"]==d["id"] for x in y["partial_source_review_receipts"]),1)
  self.assertEqual(q["yearly_work_queue"][2004-1999]["research_gate"],"SOURCE_BOUNDED_REVIEWED")
  self.assertFalse(q["yearly_work_queue"][2004-1999]["historically_complete"])
 def test_rights_and_source_zero_native_bytes(self):
  a=self.a
  self.assertEqual((a["new_original_2005_client_bytes"],a["new_same_build_original_pet_IDs"],a["new_actual_server_reward_grant_logs"]),(0,0,0))
  self.assertTrue(a["no_paid_marketplace"])
  self.assertTrue(a["no_original_commercial_material_published"])
  self.assertTrue(a["historical_CURRENT_unchanged"])
  self.assertEqual(a["startup"]["CURRENT_original_blob"],"c89e0e33537990aa2132b47c40fef49a985a935c")
  self.assertEqual((a["stage_A"],a["stage_B_wiki"],a["r79"]),("7_PARTIAL_2_OPEN","GATED","PAUSED_NON_BLOCKING"))
  self.assertIsNone(a["overall_percent"])
if __name__=="__main__":unittest.main()
