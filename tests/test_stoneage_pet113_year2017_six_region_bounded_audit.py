"""PET113: 2017 global original-classic-PC annual review preserves source/region/legal distinctions."""
import hashlib,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
A=ROOT/"research/recovered/STONEAGE-PET113-YEAR2017-SIX-REGION-CLASSIC-PC-BOUNDED-AUDIT-R1.json"
Q=ROOT/"research/recovered/STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json"
R=ROOT/"docs/continuity/STONEAGE-PET113-YEAR2017-SIX-REGION-ORIGINAL-PC-BOUNDED-AUDIT-20261118.md"
REGIONS={"CN","TW","HK_MO","KR","JP","OTHER"}

class Pet113Year2017SourceBounded(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.a=json.loads(A.read_text(encoding="utf-8"));cls.q=json.loads(Q.read_text(encoding="utf-8"))

 def test_year_handoff_not_historical_completion(self):
  a,q=self.a,self.q
  y=next(z for z in q["yearly_work_queue"] if z["year"]==2017)
  n=next(z for z in q["yearly_work_queue"] if z["year"]==2018)
  self.assertEqual((a["year_frontier_before"],a["year_frontier_after"]),(2017,2018))
  self.assertEqual((a["review_status"],y["research_gate"]),("SOURCE_BOUNDED_REVIEWED","SOURCE_BOUNDED_REVIEWED"))
  self.assertEqual(q["current_frontier"]["year"],2019)
  self.assertEqual(n["research_gate"],"SOURCE_BOUNDED_REVIEWED") # PET115 reviewed 2018 forward-only
  self.assertIn(a["id"],[v["id"] for v in q["root_source_census_receipts"]])
  self.assertTrue(q["current_frontier"]["next"].startswith(("PET114:","PET115:","PET116:","PET117:","PET118:")))
  self.assertEqual(y["source_bounded_review_receipt"],str(A.relative_to(ROOT)))
  self.assertTrue(a["source_bounded_only"] and a["year_reopenable"])
  self.assertFalse(a["historically_complete"])
  self.assertFalse(y["historically_complete"])
  self.assertIsNone(y["historical_species_count"])
  self.assertIsNone(a["original_pc_global_2017_species_count"])
  self.assertIsNone(a["original_pc_2017_first_release_count"])

 def test_regions_boundaries_and_reopen(self):
  a,q=self.a,self.q
  y=next(z for z in q["yearly_work_queue"] if z["year"]==2017)
  self.assertEqual(set(a["region_reviews"]),REGIONS)
  self.assertEqual(set(y["region_source_reviews"]),REGIONS-{"HK_MO"})
  self.assertEqual(set(y["additional_region_reviews"]),{"HK_MO"})
  self.assertEqual(len(set(a["reopen_triggers"])),6)
  self.assertEqual(y["residual_reopen_triggers"],a["reopen_triggers"])
  for k,v in a["region_reviews"].items():
   r=y["region_source_reviews"].get(k) or y["additional_region_reviews"][k]
   self.assertEqual(r["review_status"],"SOURCE_BOUNDED_REVIEWED")
   self.assertEqual(r["reopen_trigger"],v["reopen_trigger"])
   self.assertEqual(r["native_pet_id_rows_verified"],0)
   self.assertFalse(r["historically_complete"])
   self.assertIsNone(r["pet_population"])
   self.assertIsNone(r["official_2017_first_release_species_count"])

 def test_prior_two_and_court_license_cannot_promote_pets(self):
  a,q=self.a,self.q
  y=next(z for z in q["yearly_work_queue"] if z["year"]==2017)
  self.assertEqual([z["id"] for z in y["partial_source_review_receipts"]][:2],a["prior_partial_receipts"])
  self.assertEqual(y["partial_source_review_receipts"][-1]["id"],a["id"])
  self.assertIn(a["id"],[v["id"] for v in q["root_source_census_receipts"]])
  self.assertEqual(len(a["sources"]),len({s["id"] for s in a["sources"]}))
  self.assertTrue(any("JUDICIAL_TEXT_PUBLIC_WIKISOURCE_TRANSCRIPTION" in s["grade"] for s in a["sources"]))
  self.assertTrue(any("THIRD_PARTY" in s["grade"] and s["region"]=="TW" for s in a["sources"]))
  self.assertTrue(all(a["legal_boundary"].values()))
  self.assertTrue(all(a["negative_controls"].values()))
  self.assertEqual(a["candidate_labels_by_grade"]["TW_period_relay_event_named_pet_not_verified_native"],["藍虎"])

 def test_new_native_zero_and_immutable_current(self):
  a,q=self.a,self.q
  for key in ("new_2017_original_pc_client_bytes","new_2017_original_pc_patch_bytes",
     "new_2017_native_pet_ids","new_2017_original_spr_frames",
     "new_2017_native_pet_skills","new_2017_server_pet_grant_logs"):
   self.assertEqual(a[key],0)
  raw=(ROOT/"docs/CURRENT-STATE.md").read_bytes()
  self.assertEqual(len(raw),a["starting_remote"]["current_state_bytes"])
  sha=hashlib.sha1(b"blob "+str(len(raw)).encode("ascii")+b"\x00"+raw).hexdigest()
  self.assertEqual(sha,a["starting_remote"]["current_state_git_blob"])
  self.assertEqual((a["stage_A"],a["stage_B_wiki"],a["r79"],a["overall_percent"]),
     (q["stage_A"],q["stage_B_wiki"],q["r79"],q["overall_game_completion_percent"]))
  self.assertIn("PET113",R.read_text(encoding="utf-8"))

if __name__=="__main__":unittest.main()
