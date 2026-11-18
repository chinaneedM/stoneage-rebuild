"""PET76: 2007 source-bounded official five-region pet audit and 2008 cursor."""
import json,unittest
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]/"research"/"recovered"
def rd(name):return json.loads((BASE/name).read_text(encoding="utf8"))
class PET76Annual(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.a=rd("STONEAGE-PET76-YEAR2007-FIVE-REGION-BOUNDED-AUDIT-R1.json")
  cls.p=rd("STONEAGE-PET75-YEAR2006-FIVE-REGION-BOUNDED-AUDIT-R1.json")
  cls.q=rd("STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json")
 def test_historical_2007_bounded_with_future_cursor(self):
  a,q=self.a,self.q;year=q["yearly_work_queue"][2007-1999]
  self.assertEqual(a["year"],2007)
  self.assertEqual((a["year_frontier_before"],a["year_frontier_after"]),(2007,2008))
  self.assertGreaterEqual(q["current_frontier"]["year"],2008)
  self.assertEqual(year["research_gate"],"SOURCE_BOUNDED_REVIEWED")
  self.assertFalse(year["historically_complete"])
  self.assertIsNone(year["historical_species_count"])
  self.assertEqual(year["source_bounded_review_receipt"],"research/recovered/STONEAGE-PET76-YEAR2007-FIVE-REGION-BOUNDED-AUDIT-R1.json")
  self.assertEqual(q["yearly_work_queue"][2008-1999]["research_gate"],"NOT_YEAR_AUDITED")
  self.assertEqual(a["year_2007_existing_PET25_PET26_documentary_events_NOT_species"],0)
  self.assertEqual(year["documentary_event_count_NOT_species"],0)
 def test_japan_six_named_original_official_pool_not_six_new(self):
  a=self.a
  jp=a["region_reviews"]["JP"]
  n=["ギガドラン","ドルーザス","パンダホーン","クロウリ","ムールロス","ウロボス"]
  self.assertEqual(jp["period_operator_named_pet_pool"],n)
  self.assertEqual(jp["period_operator_named_pet_pool_count_not_new_species"],6)
  self.assertIn("クロウリ",jp["known_prior_attestation_name_overlap"])
  self.assertIsNone(jp["confirmed_first_releases_2007"])
  self.assertFalse(jp["actual_numeric_probability_verified"])
  self.assertFalse(jp["individual_delivery_log_verified"])
  self.assertTrue(jp["stoneage2_riding_is_not_stoneage1_pet"])
  self.assertTrue(all(a["source_consistency_guards"].values()))
 def test_korean_and_taiwan_line_division(self):
  a=self.a
  self.assertTrue(a["region_reviews"]["KR"]["original_2007_riding_mechanism_advertised"])
  self.assertTrue(a["region_reviews"]["KR"]["original_christmas_event_pet_reward_advertised"])
  self.assertTrue(a["region_reviews"]["KR"]["ice_castle_in_2007_press_future_only"])
  self.assertTrue(a["region_reviews"]["KR"]["ice_castle_2008_news_not_2007_issuance"])
  self.assertEqual(len(a["region_reviews"]["TW"]["retrospective_only_product_titles"]),3)
  self.assertFalse(a["region_reviews"]["TW"]["dated_2007_period_operator_original_pet_issuance_verified"])
  self.assertFalse(a["region_reviews"]["CN"]["dated_2007_period_operator_original_pet_issuance_verified"])
  self.assertTrue(a["region_reviews"]["OTHER"]["no_independent_2007_primary_pet_data_found_not_proof_no_service"])
  self.assertEqual(set(a["region_reviews"]),{"CN","TW","JP","KR","OTHER"})
 def test_no_species_promotion_and_real_client_missing(self):
  a=self.a
  self.assertEqual(len(a["sources"]),11)
  self.assertEqual(len({x["id"] for x in a["sources"]}),11)
  self.assertTrue(all(not x["actual_new_species_proven"] for x in a["sources"]))
  self.assertTrue(all(x["pet_population"] is None for x in a["region_reviews"].values()))
  self.assertTrue(all(x["native_pet_id_rows_verified"]==0 for x in a["region_reviews"].values()))
  self.assertEqual((a["original_2007_client_bytes_acquired"],a["new_2007_native_pet_ids"],a["real_2007_reward_grant_logs"]),(0,0,0))
  self.assertIsNone(a["global_2007_historical_species_count"])
  self.assertIsNone(a["confirmed_2007_first_new_species_count"])
  self.assertFalse(a["client_first_finite_search"]["original_2007_installer_exact_file_url_confirmed"])
  self.assertIsNone(a["client_first_finite_search"]["original_client_SHA256"])
  self.assertTrue(a["no_paid_marketplace"])
  self.assertTrue(a["no_private_server_only_pet_included"])
  self.assertTrue(a["no_original_commercial_art_published"])
  self.assertTrue(a["historical_CURRENT_untouched"])
  self.assertEqual(a["startup"]["original_CURRENT_blob"],"c89e0e33537990aa2132b47c40fef49a985a935c")
 def test_reopen_and_append_only(self):
  a,p,q=self.a,self.p,self.q
  y=q["yearly_work_queue"][8]
  self.assertEqual(len(a["reopen_triggers"]),5)
  self.assertEqual(y["residual_reopen_triggers"],a["reopen_triggers"])
  self.assertEqual(set(y["region_source_reviews"]),set(a["region_reviews"]))
  for reg,r in a["region_reviews"].items():
   self.assertEqual(y["region_source_reviews"][reg]["reopen_trigger"],r["reopen_trigger"])
  for k in [a["id"],p["id"]]:
   self.assertEqual(sum(x["id"]==k for x in q["root_source_census_receipts"]),1)
  self.assertEqual(len({x["id"] for x in q["root_source_census_receipts"]}),len(q["root_source_census_receipts"]))
  self.assertEqual(sum(x["id"]==a["id"] for x in y["partial_source_review_receipts"]),1)
  self.assertEqual((a["stage_A"],a["stage_B_wiki"],a["r79"]),("7_PARTIAL_2_OPEN","GATED","PAUSED_NON_BLOCKING"))
  self.assertIsNone(a["overall_percent"])
if __name__=="__main__":unittest.main()
