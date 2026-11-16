"""PET64 2002 official PET source-bounded annual audit and frontier 2003."""
import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REC=ROOT/"research"/"recovered"
def read(s):return json.loads((REC/s).read_text(encoding="utf8"))
class PET64Audit(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.d=read("STONEAGE-PET64-YEAR2002-SOURCE-BOUNDED-AUDIT-R1.json")
  cls.q=read("STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json")
 def test_operator_press_release_does_not_count_unreleased_pet(self):
  a=self.d["new_primary_operator_source"]
  self.assertEqual(a["published"],"2002-11-11")
  self.assertTrue(a["direct_full_text_read"])
  self.assertEqual(a["publisher_as_stated"],"華義國際數位娛樂股份有限公司")
  self.assertTrue(a["press_release_text_says_unopened_new_pet_scratch_chance"])
  self.assertTrue(a["marketing_promise_not_live_award"])
  self.assertFalse(a["actually_awarded_pet_identity_confirmed"])
  self.assertIsNone(a["named_pet_in_release"])
  self.assertFalse(a["original_client_included_obtained"])
 def test_2002_five_region_annual_review_and_reopen(self):
  d,q=self.d,self.q
  self.assertEqual((d["year"],d["status"]),(2002,"SOURCE_BOUNDED_REVIEWED"))
  self.assertFalse(d["historically_complete"])
  self.assertEqual(set(d["region_source_reviews"]),{"CN","TW","JP","KR","OTHER"})
  self.assertEqual(len(d["residual_reopen_triggers"]),5)
  y=q["yearly_work_queue"][3]
  self.assertEqual(y["research_gate"],"SOURCE_BOUNDED_REVIEWED")
  self.assertFalse(y["historically_complete"])
  self.assertIsNone(y["historical_species_count"])
  self.assertEqual(y["source_bounded_review_receipt"],"research/recovered/STONEAGE-PET64-YEAR2002-SOURCE-BOUNDED-AUDIT-R1.json")
  for r,v in d["region_source_reviews"].items():
   self.assertIsNone(v["pet_population"],r)
   self.assertFalse(v["named_native_pet_roster_verified"],r)
   self.assertTrue(v["reopen"] and v["reopen_trigger"],r)
  self.assertEqual(q["current_frontier"]["year"],2003)
  self.assertEqual(q["yearly_work_queue"][4]["research_gate"],"NOT_YEAR_AUDITED")
  self.assertEqual(q["current_frontier"]["latest_partial_root_review"],d["id"])
  self.assertTrue(q["current_frontier"]["next"].startswith("PET65:"))
 def test_keeps_historical_receipts_and_event_count(self):
  d,q=self.d,self.q
  rs=[x["id"] for x in q["root_source_census_receipts"]]
  self.assertTrue(all(rs.count(x)==1 for x in d["prior_2002_receipt_ids"]))
  self.assertEqual(rs.count(d["id"]),1)
  self.assertEqual(q["yearly_work_queue"][3]["documentary_event_count_NOT_species"],4)
  self.assertTrue(d["prior_four_event_records_unchanged"])
  self.assertEqual(d["new_official_live_2002_pets_verified"],0)
  self.assertEqual(d["new_original_2002_client_bytes"],0)
  self.assertIsNone(d["global_2002_pet_population"])
  self.assertIsNone(q["yearly_work_queue"][3]["historical_species_count"])
 def test_rights(self):
  d=self.d
  self.assertTrue(d["no_paid_marketplace"])
  self.assertFalse(d["copyrighted_original_assets_published"])
  self.assertTrue(d["current_state_original_unchanged"])
  self.assertEqual(d["start"]["original_current_blob"],"c89e0e33537990aa2132b47c40fef49a985a935c")
  self.assertEqual((d["stage_A"],d["stage_B_wiki"],d["r79"]),("7_PARTIAL_2_OPEN","GATED","PAUSED_NON_BLOCKING"))
  self.assertIsNone(d["overall_percent"])
if __name__=="__main__":unittest.main()
