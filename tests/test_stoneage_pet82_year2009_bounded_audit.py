"""PET82: complete source-bounded 2009 five-region audit, not historical pet completeness."""
import json,hashlib,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"research"/"recovered"
def get(name):return json.loads((DATA/name).read_text(encoding="utf-8"))
class PET82AnnualReview(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.a=get("STONEAGE-PET82-YEAR2009-FIVE-REGION-SOURCE-BOUNDED-AUDIT-R1.json")
  cls.q=get("STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json")
 def test_frontier_is_2010_and_year2009_reopenable(self):
  a,q=self.a,self.q;y=q["yearly_work_queue"][10];n=q["yearly_work_queue"][11]
  self.assertEqual((a["year"],a["year_frontier_before"],a["year_frontier_after"]),(2009,2009,2010))
  self.assertGreaterEqual(q["current_frontier"]["year"],2010)
  self.assertEqual(y["research_gate"],"SOURCE_BOUNDED_REVIEWED")
  self.assertEqual(n["research_gate"],"NOT_YEAR_AUDITED" if q["current_frontier"]["year"]==2010 else "SOURCE_BOUNDED_REVIEWED")
  self.assertFalse(y["historically_complete"])
  self.assertIsNone(y["historical_species_count"])
  self.assertEqual(y["source_bounded_review_receipt"],"research/recovered/STONEAGE-PET82-YEAR2009-FIVE-REGION-SOURCE-BOUNDED-AUDIT-R1.json")
  self.assertEqual([r["id"] for r in y["partial_source_review_receipts"]][-3:],a["prior_partial_receipts"]+[a["id"]])
  self.assertEqual(sum(r["id"]==a["id"] for r in q["root_source_census_receipts"]),1)
  self.assertEqual(len({r["id"] for r in q["root_source_census_receipts"]}),len(q["root_source_census_receipts"]))
  self.assertEqual(y["documented_release_event_ids_from_existing_PET25_PET26"],["JP-2009-HAKUEN","JP-2009-KOKUEN"])
 def test_version_boundary_not_crossed_and_no_fake_species_totals(self):
  a=self.a;s={r["id"]:r for r in a["source_records"]}
  self.assertTrue(s["CN2009-SHENGSI-STONEAGE2"]["does_not_prove_2009_original_pc_8_5_live"])
  self.assertEqual(s["CN2009-SHENGSI-STONEAGE2"]["actual_product_line"],"StoneAge2")
  self.assertEqual(s["CN2010-SHENGSI-ORIGINAL-8_5-ANNOUNCEMENT"]["attestation_date"],"2010-05-21")
  self.assertFalse(s["CN2010-SHENGSI-ORIGINAL-8_5-ANNOUNCEMENT"]["new_2009_pet_release_derived"])
  self.assertEqual(s["TW2009-INSREA-STONEAGE2-SUSPENSION"]["actual_product_line"],"StoneAge2")
  self.assertFalse(s["TW2009-INSREA-STONEAGE2-SUSPENSION"]["post_stop_execution_verified"])
  self.assertTrue(s["KR2008-DANGUN-NOT_2009"]["not_2009"])
  self.assertTrue(all(a["evidence_boundaries"].values()))
  self.assertIsNone(a["global_official_species_population"])
  self.assertIsNone(a["confirmed_first_year_species_count"])
  self.assertEqual((a["new_authentic_2009_original_client_bytes"],a["new_original_2009_native_pet_ids"],a["new_actual_2009_original_server_grant_logs"]),(0,0,0))
 def test_five_region_reopening_and_current_blob(self):
  a,q=self.a,self.q;y=q["yearly_work_queue"][10]
  self.assertEqual(set(a["region_reviews"]),{"CN","TW","JP","KR","OTHER"})
  self.assertEqual(y["residual_reopen_triggers"],a["five_region_reopen_triggers"])
  self.assertEqual(len(a["five_region_reopen_triggers"]),5)
  for reg,v in a["region_reviews"].items():
   self.assertEqual(v["review_status"],"SOURCE_BOUNDED_REVIEWED")
   self.assertFalse(v["historically_complete"])
   self.assertIsNone(v["pet_population"])
   self.assertEqual(v["reopen_trigger"],y["region_source_reviews"][reg]["reopen_trigger"])
   self.assertEqual(v["native_pet_id_rows_verified"],0)
  raw=(ROOT/"docs"/"CURRENT-STATE.md").read_bytes()
  self.assertEqual(len(raw),2709173)
  self.assertEqual(hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\x00"+raw).hexdigest(),a["startup"]["current_native_blob"])
  self.assertTrue(a["historical_current_unmodified"])
  self.assertEqual((a["stage_A"],a["stage_B_wiki"],a["r79"]),("7_PARTIAL_2_OPEN","GATED","PAUSED_NON_BLOCKING"))
if __name__=="__main__":unittest.main()
