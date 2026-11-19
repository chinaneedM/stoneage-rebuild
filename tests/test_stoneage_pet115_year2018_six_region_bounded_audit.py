"""PET115 2018 six-region classic-PC source-bounded review, mobile independent product."""
import json,hashlib,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
A=ROOT/"research/recovered/STONEAGE-PET115-YEAR2018-SIX-REGION-ORIGINAL-PC-PET-SOURCE-AUDIT-R1.json";Q=ROOT/"research/recovered/STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json";R=ROOT/"docs/continuity/STONEAGE-PET115-YEAR2018-SIX-REGION-CLASSIC-PC-PET-BOUNDED-AUDIT-20261118.md"
REGIONS={"CN","TW","HK_MO","KR","JP","OTHER"}
class Pet115Year2018Annual(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.a=json.loads(A.read_text(encoding="utf-8"));cls.q=json.loads(Q.read_text(encoding="utf-8"))
 def test_forward_year_2019_is_source_bounded_not_historically_closed(self):
  a,q=self.a,self.q
  y=next(x for x in q["yearly_work_queue"] if x["year"]==2018)
  n=next(x for x in q["yearly_work_queue"] if x["year"]==2019)
  self.assertEqual((a["year_frontier_before"],a["year_frontier_after"]),(2018,2019))
  self.assertEqual((q["active_module"],a["active_module"]),("PET","PET"))
  self.assertEqual((a["review_status"],y["research_gate"]),("SOURCE_BOUNDED_REVIEWED","SOURCE_BOUNDED_REVIEWED"))
  self.assertGreaterEqual(q["current_frontier"]["year"],2020)
  self.assertEqual(n["research_gate"],"SOURCE_BOUNDED_REVIEWED") # PET118 subsequent year review, PET115 handoff remains 2019
  self.assertIn(a["id"],[r["id"] for r in q["root_source_census_receipts"]])
  self.assertTrue(q["current_frontier"]["next"].startswith(("PET116:","PET117:","PET118:","PET119:")))
  self.assertEqual(y["source_bounded_review_receipt"],str(A.relative_to(ROOT)))
  self.assertFalse(y["historically_complete"])
  self.assertTrue(a["source_bounded_only"] and a["year_reopenable"])
  self.assertIsNone(y["historical_species_count"])
  self.assertIsNone(a["original_pc_global_2018_species_count"])
  self.assertIsNone(a["original_pc_2018_first_release_species_count"])
 def test_six_regions_separate_with_unresolved_native_and_reopen_triggers(self):
  a,q=self.a,self.q
  y=next(x for x in q["yearly_work_queue"] if x["year"]==2018)
  self.assertEqual(set(a["region_reviews"]),REGIONS)
  self.assertEqual(set(y["region_source_reviews"]),REGIONS-{"HK_MO"})
  self.assertEqual(set(y["additional_region_reviews"]),{"HK_MO"})
  self.assertEqual(y["residual_reopen_triggers"],a["reopen_triggers"])
  self.assertEqual(len(set(a["reopen_triggers"])),6)
  for k,v in a["region_reviews"].items():
   r=y["region_source_reviews"].get(k) or y["additional_region_reviews"].get(k)
   self.assertEqual(r["reopen_trigger"],v["reopen_trigger"])
   self.assertEqual(r["review_status"],"SOURCE_BOUNDED_REVIEWED")
   self.assertFalse(r["historically_complete"])
   self.assertIsNone(r["pet_population"])
   self.assertIsNone(r["official_2018_first_release_species_count"])
   self.assertEqual(r["native_pet_id_rows_verified"],0)
 def test_prior_receipt_and_source_relay_grades_preserved(self):
  a,q=self.a,self.q
  y=next(x for x in q["yearly_work_queue"] if x["year"]==2018)
  self.assertEqual(a["prior_partial_receipts"],[x["id"] for x in y["partial_source_review_receipts"]][:1])
  self.assertEqual(y["partial_source_review_receipts"][-1]["id"],a["id"])
  self.assertIn(a["id"],[r["id"] for r in q["root_source_census_receipts"]])
  self.assertEqual(len(a["sources"]),len(set(s["id"] for s in a["sources"])))
  self.assertEqual(set(x["region"] for x in a["sources"])|{"OTHER"},REGIONS|{"TW_HK_MO_MOBILE"})
  self.assertTrue(all(a["negative_controls"].values()))
  self.assertEqual(a["product_line_boundary"]["mobile_announced_release"],"2018-07-18")
  self.assertEqual(a["product_line_boundary"]["mobile_japanese_later_press_date"],"2018-07-17")
  self.assertEqual(a["product_line_boundary"]["operator_press_mobile_reward_pet_label"],"3星卡米魯")
  self.assertFalse(a["product_line_boundary"]["original_appstore_first_listed_datetime_verified"])
  self.assertTrue(a["product_line_boundary"]["mobile_marketing_population_not_2018_classic_pc_population"])
 def test_zero_new_native_unchanged_big_blob_and_stage(self):
  a,q=self.a,self.q
  for k in ("new_2018_original_pc_client_bytes","new_2018_original_pc_patch_bytes","new_2018_native_pet_ids","new_2018_original_spr_frames","new_2018_native_skill_functions","new_2018_server_pet_grants"):
   self.assertEqual(a[k],0)
  raw=(ROOT/"docs/CURRENT-STATE.md").read_bytes()
  self.assertEqual(len(raw),a["baseline"]["original_state_bytes"])
  blob=hashlib.sha1(b"blob "+str(len(raw)).encode("ascii")+b"\x00"+raw).hexdigest()
  self.assertEqual(blob,a["baseline"]["original_state_blob"])
  self.assertEqual((a["stage_A"],a["stage_B_wiki"],a["r79"],a["overall_percent"]),(q["stage_A"],q["stage_B_wiki"],q["r79"],q["overall_game_completion_percent"]))
  self.assertIn("PET115",R.read_text(encoding="utf-8"))
if __name__=="__main__":unittest.main()
