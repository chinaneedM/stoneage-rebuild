"""PET71: source-bounded annual audit for 2004 across five official PC StoneAge regions."""
import json,unittest
from pathlib import Path
REC=Path(__file__).resolve().parents[1]/"research"/"recovered"
def read(n): return json.loads((REC/n).read_text(encoding="utf8"))
class PET71Annual(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.a=read("STONEAGE-PET71-YEAR2004-FIVE-REGION-AUDIT-R1.json")
  cls.q=read("STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json")
  cls.prior69=read("STONEAGE-PET69-YEAR2004-TW75-CNMONKEY-JPAVATAR-R1.json")
  cls.prior70=read("STONEAGE-PET70-2004-KR-RIDES-CN75-STAGED-TW-XUANWU-R1.json")
 def test_JP_2004_contemporaneous_pet_cook_skill_vs_species(self):
  x=self.a["new_2004_original_period_source"]
  self.assertEqual(x["date"],"2004-02-10")
  self.assertEqual(x["scheduled_event_date"],"2004-02-13")
  self.assertEqual(x["operator"],"BOTHTEC")
  self.assertEqual(x["product_stage"],"JAPAN_2004_OPEN_BETA")
  self.assertEqual(x["operator_named_servers"],["月","水星","金星"])
  self.assertTrue(x["direct_original_2004_period_news_read"])
  self.assertTrue(x["player_participation_requires_pet_with_cooking_skill"])
  self.assertIsNone(x["player_quest_pet_name_or_species_id"])
  self.assertFalse(x["pet_skill_natively_verified_from_original_2004_client"])
  self.assertFalse(x["is_first_official_pet_release_event"])
  self.assertFalse(x["operator_pet_full_roster_in_article"])
  self.assertEqual(x["original_client_bytes_recovered"],0)
 def test_region_2004_source_boundaries_not_exact_global_pet_species(self):
  d,q=self.a,self.q
  y=q["yearly_work_queue"][2004-1999]
  self.assertEqual((d["year"],d["review_status"]),(2004,"SOURCE_BOUNDED_REVIEWED"))
  self.assertFalse(d["historically_complete"])
  self.assertEqual(set(d["region_source_reviews"]),{"CN","TW","JP","KR","OTHER"})
  self.assertEqual(set(y["region_source_reviews"]),set(d["region_source_reviews"]))
  self.assertEqual(len(d["residual_reopen_triggers"]),5)
  self.assertEqual(d["residual_reopen_triggers"],y["residual_reopen_triggers"])
  self.assertEqual(y["research_gate"],"SOURCE_BOUNDED_REVIEWED")
  self.assertFalse(y["historically_complete"])
  self.assertIsNone(y["historical_species_count"])
  self.assertEqual(y["source_bounded_review_receipt"],"research/recovered/STONEAGE-PET71-YEAR2004-FIVE-REGION-AUDIT-R1.json")
  for reg,x in d["region_source_reviews"].items():
   self.assertTrue(x["reopen"] and x["reopen_trigger"],reg)
   self.assertFalse(x["original_complete_2004_client_build_available"],reg)
   self.assertFalse(x["native_pet_master_verified"],reg)
   self.assertFalse(x["actual_native_reward_log_recovered"],reg)
   self.assertIsNone(x["pet_population"],reg)
   self.assertIsNone(x["official_live_named_2004_released_species_count"],reg)
   self.assertIsNone(y["region_source_reviews"][reg]["pet_population"],reg)
   self.assertTrue(y["region_source_reviews"][reg]["authentic_2004_full_original_client_missing"],reg)
  self.assertFalse(d["region_source_reviews"]["OTHER"]["all_other_regions_absent_proven"])
  self.assertIsNone(d["global_2004_official_species_population"])
 def test_operator_KR_four_names_approx120_unidentified_three(self):
  kr=self.a["region_source_reviews"]["KR"]
  self.assertEqual(kr["period_four_named_ride_labels"],["라고고","무이","도라비스","고르돈"])
  self.assertEqual(kr["period_newly_added_huntable_pets_unnamed_count"],3)
  self.assertEqual(kr["period_operator_approx_pet_varieties"],"120여종")
  self.assertFalse(kr["four_ride_names_are_four_2004_new_species"])
  self.assertTrue(kr["three_unnamed_not_inferred_to_four_ride_names"])
  self.assertTrue(self.a["source_evidence_exclusions"]["KR_about_120_is_not_exact_total"])
  self.assertEqual(kr["period_four_named_ride_labels"],self.prior70["operator_2004_KR_four_named_mount_pets"])
 def test_CN_TW_JP_cross_version_and_avatar_exclusions(self):
  x=self.a["source_evidence_exclusions"]
  self.assertTrue(all(x.values()))
  self.assertEqual(self.a["region_source_reviews"]["TW"]["period_named_operator_gift_labels"],["弗麗露","弗麗雅","火風鷹人"])
  self.assertEqual(self.a["region_source_reviews"]["TW"]["claimed_hawk_live_quantity_less_than"],20)
  self.assertFalse(self.a["region_source_reviews"]["JP"]["is_2004_Hangame_avatar_in_game_species"])
  self.assertIsNone(self.a["region_source_reviews"]["CN"]["pet_population"])
  self.assertEqual(len(self.prior69["region_sources"]),8)
  self.assertEqual(self.prior69["region_sources"][0]["region"],"TW")
 def test_year_2005_frontier_retains_all_prior_2004_receipts(self):
  a,q=self.a,self.q
  self.assertEqual((a["year_frontier_before"],a["year_frontier_after"]),(2004,2005))
  self.assertEqual(q["current_frontier"]["year"],2005)
  self.assertRegex(q["current_frontier"]["next"],r"^PET[0-9]+:")
  self.assertEqual(q["yearly_work_queue"][6]["research_gate"],"NOT_YEAR_AUDITED")
  self.assertEqual(q["yearly_work_queue"][5]["documentary_event_count_NOT_species"],0)
  self.assertEqual(a["historical_2004_PET25_PET26_documentary_event_count_unchanged"],0)
  ids=[r["id"] for r in q["root_source_census_receipts"]]
  self.assertEqual(len(ids),len(set(ids)))
  self.assertEqual(ids.count(a["id"]),1)
  for id in a["prior_2004_root_receipts"]:
   self.assertEqual(ids.count(id),1)
  self.assertEqual(self.prior69["year"],2004)
  self.assertEqual(self.prior70["year"],2004)
  self.assertEqual(self.prior69["id"],a["prior_2004_root_receipts"][0])
  self.assertEqual(self.prior70["id"],a["prior_2004_root_receipts"][1])
  y=q["yearly_work_queue"][5]
  self.assertEqual(len(y["partial_source_review_receipts"]),3)
  self.assertEqual(sum(x["id"]==a["id"] for x in y["partial_source_review_receipts"]),1)
  self.assertEqual(q["yearly_work_queue"][4]["research_gate"],"SOURCE_BOUNDED_REVIEWED")
  self.assertFalse(q["yearly_work_queue"][4]["historically_complete"])
 def test_historical_original_rights_and_zero_new_native_bytes(self):
  a=self.a
  self.assertEqual(a["new_2004_original_client_bytes"],0)
  self.assertEqual(a["new_2004_native_pet_id_rows"],0)
  self.assertEqual(a["new_2004_original_server_reward_logs"],0)
  self.assertTrue(a["all_regions_pet_population_null"])
  self.assertFalse(a["copyright_original_assets_published"])
  self.assertTrue(a["no_paid_marketplace"])
  self.assertTrue(a["historical_CURRENT_blob_unchanged"])
  self.assertEqual(a["startup"]["original_CURRENT_blob"],"c89e0e33537990aa2132b47c40fef49a985a935c")
  self.assertEqual((a["stage_A"],a["stage_B_wiki"],a["r79"]),("7_PARTIAL_2_OPEN","GATED","PAUSED_NON_BLOCKING"))
  self.assertIsNone(a["overall_percent"])
if __name__=="__main__":unittest.main()
