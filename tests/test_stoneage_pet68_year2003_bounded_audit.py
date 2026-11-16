"""PET68 strict five-region 2003 historical source-bounded review with official GM award reportage."""
import json
import unittest
from pathlib import Path

R=Path(__file__).resolve().parents[1]/"research"/"recovered"
def load(s): return json.loads((R/s).read_text(encoding="utf8"))

class PET68YearAudit(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.a=load("STONEAGE-PET68-YEAR2003-SOURCE-BOUNDED-AUDIT-R1.json")
  cls.q=load("STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json")
  cls.old=[load(x) for x in [
   "STONEAGE-PET65-CN2003-WAEI-PET-PROMO-R1.json",
   "STONEAGE-PET66-2003-TW6-CN7-PET-SOURCE-R1.json",
   "STONEAGE-PET67-2003-JPKR-OPERATOR-CLIENT-BOUNDARY-R1.json"]]
 def src(self,source_id):
  return next(x for x in self.a["new_2003_directly_readable_period_operator_relays"] if x["id"]==source_id)
 def test_actual_operator_reported_award_not_promotional_promise(self):
  a=self.a
  p=a["first_party_reported_live_pet_prize"]
  self.assertEqual((p["name"],p["kind"],p["region"]),("波比","松鼠","CN"))
  self.assertEqual(p["independent_report_documents"],4)
  self.assertEqual(p["independent_named_pet_identities"],1)
  self.assertEqual(p["source_bounded_minimum_named_award_reported_count"],1)
  self.assertTrue(p["named_operator_reported_award_under_official_only_scope"])
  self.assertTrue(p["award_mentioned_in_multiple_2003_dates_not_four_species"])
  self.assertEqual(p["actual_reported_exchange_date"],"2003-11-12")
  self.assertEqual(p["exchange_input_actual_reported"],"奇娜")
  self.assertEqual(p["two_other_eligible_exchange_inputs_as_promised"],["多鲁宝","洛卡伦恩"])
  self.assertFalse(p["raw_original_award_database_proven"])
  self.assertIsNone(p["same_build_native_species_identifier"])
  self.assertIsNone(p["game_client_original_spr_sha256"])
  self.assertIsNone(p["confirmed_official_live_award_count_by_raw_server_logs"])
  self.assertEqual(self.src("CN2003_WAEI_1113_BOBI")["actually_submitted_input_in_narrative"],"奇娜")
  self.assertEqual(self.src("CN2003_WAEI_1113_BOBI")["report_on_activity_date"],"2003-11-12")
  self.assertIsNone(self.src("CN2003_WAEI_1111_BOBI")["actually_submitted_input_in_narrative"])
  for k in ["CN2003_WAEI_1107_BOBI","CN2003_WAEI_1110_BOBI","CN2003_WAEI_1111_BOBI","CN2003_WAEI_1113_BOBI"]:
   self.assertTrue(self.src(k)["actual_reward_reported"])
   self.assertFalse(self.src(k)["native_receipt_seen"])
 def test_2003_sourced_versions_not_fictitious_count(self):
  a=self.a
  q=a["other_obligations"]
  self.assertTrue(q["CN5_server_first_rollout_cannot_be_all_2003_CN_same_version"])
  self.assertTrue(q["china_182_retro_server_not_same_deployment_as_CN5"])
  self.assertTrue(q["CN_2003_official_5_0_three_card_categories_not_species_count"])
  self.assertTrue(q["CN2003_mobile_companion_announced_not_shipped_proven"])
  self.assertTrue(q["physical_magic_card_two_pet_cards_not_2_native_pets"])
  self.assertTrue(q["JP2004_formal_release_not_2003_beta_pet_delivery"])
  self.assertTrue(q["KR_inium_to_netmarble_source_roster_identity_unproven"])
  self.assertEqual(self.src("CN2003_WAEI_0120_ROLLOUT")["first_server_groups"],["中国网通9","西安网通2"])
  self.assertEqual(self.src("CN2003_WAEI_0120_ROLLOUT")["associated_card_categories"],["狼人卡","魔兽卡","新年兽卡"])
  self.assertEqual(self.src("CN2003_WAEI_0320_182_ANNIVERSARY")["planned_182_server_start"],"2003-03-21T12:00")
  self.assertFalse(self.src("CN2003_WAEI_1103_ELEMENT_BEAST")["actual_winner_pet_proven"])
 def test_five_independent_region_reopen_and_no_population_inference(self):
  a,q=self.a,self.q
  y=next(z for z in q["yearly_work_queue"] if z["year"]==2003)
  self.assertEqual((a["year"],a["review_status"]),(2003,"SOURCE_BOUNDED_REVIEWED"))
  self.assertFalse(a["historically_complete"])
  self.assertEqual(set(a["region_source_reviews"]),{"CN","TW","JP","KR","OTHER"})
  self.assertEqual(set(y["region_source_reviews"]),set(a["region_source_reviews"]))
  self.assertEqual(len(a["residual_reopen_triggers"]),5)
  self.assertEqual(a["residual_reopen_triggers"],y["residual_reopen_triggers"])
  self.assertEqual(y["research_gate"],"SOURCE_BOUNDED_REVIEWED")
  self.assertFalse(y["historically_complete"])
  self.assertIsNone(y["historical_species_count"])
  self.assertEqual(y["source_bounded_review_receipt"],"research/recovered/STONEAGE-PET68-YEAR2003-SOURCE-BOUNDED-AUDIT-R1.json")
  self.assertEqual(y["official_operator_reported_actual_award_name_labels"],["波比"])
  for region,x in a["region_source_reviews"].items():
   self.assertIsNone(x["official_2003_species_population"],region)
   self.assertTrue(x["reopen"] and x["reopen_trigger"],region)
   self.assertFalse(x["original_same_year_complete_client_recovered"],region)
   self.assertFalse(x["actual_native_server_reward_log_retrieved"],region)
   self.assertIsNone(y["region_source_reviews"][region]["pet_population"],region)
   self.assertTrue(y["region_source_reviews"][region]["authentic_2003_full_original_client_missing"],region)
  self.assertFalse(a["region_source_reviews"]["OTHER"]["all_other_regions_absent_proven"])
  self.assertIsNone(a["historical_global_2003_official_species_population"])
  self.assertEqual(a["new_first_party_reported_actual_2003_awarded_pet_names"],["波比"])
  self.assertEqual(a["new_2003_native_server_log_verified_award_count"],0)
  self.assertEqual(a["new_2003_original_client_bytes"],0)
  self.assertEqual(a["newly_verified_2003_native_pet_IDs"],0)
 def test_year_progression_and_all_three_2003_receipts_retained(self):
  a,q=self.a,self.q
  self.assertEqual((a["year_frontier_before"],a["year_frontier_after"]),(2003,2004))
  self.assertEqual(q["current_frontier"]["year"],2004)
  self.assertTrue(q["current_frontier"]["next"].startswith("PET69:"))
  self.assertEqual(q["yearly_work_queue"][5]["research_gate"],"NOT_YEAR_AUDITED")
  self.assertEqual(q["yearly_work_queue"][4]["documentary_event_count_NOT_species"],1)
  self.assertEqual(a["old_2003_PET25_PET26_documentary_event_count_unchanged"],1)
  ids=[z["id"] for z in q["root_source_census_receipts"]]
  self.assertEqual(len(set(ids)),len(ids))
  self.assertEqual(ids.count(a["id"]),1)
  for n in a["previous_2003_receipts"]:
   self.assertEqual(ids.count(n),1)
  y=q["yearly_work_queue"][4]
  self.assertEqual(len(y["partial_source_review_receipts"]),4)
  self.assertEqual(sum(z["id"]==a["id"] for z in y["partial_source_review_receipts"]),1)
  for source in self.old:
   self.assertEqual(source["year"],2003)
   self.assertEqual(ids.count(source["id"]),1)
 def test_rights_and_historical_blob_retained(self):
  a=self.a
  self.assertTrue(a["other_obligations"]["no_payment_gated_or_secondhand_disc_search"])
  self.assertTrue(a["historical_CURRENT_unchanged"])
  self.assertTrue(a["no_original_commercial_media_published"])
  self.assertEqual(a["start"]["historical_current_blob"],"c89e0e33537990aa2132b47c40fef49a985a935c")
  self.assertEqual(a["start"]["historical_current_bytes"],2709173)
  self.assertEqual((a["stage_A"],a["stage_B_wiki"],a["r79"]),("7_PARTIAL_2_OPEN","GATED","PAUSED_NON_BLOCKING"))
  self.assertIsNone(a["overall_percent"])

if __name__=="__main__":unittest.main()
