"""PET114: source-bounded 2018 Taiwan dual realms, summer pet tasks and independent mobile."""
import json,hashlib,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
A=ROOT/"research/recovered/STONEAGE-PET114-TW2018-PC-TWO-REALM-SUMMER-PET-SOURCE-BOUNDARY-R1.json"
Q=ROOT/"research/recovered/STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json"
R=ROOT/"docs/continuity/STONEAGE-PET114-TW2018-TWO-REALM-SUMMER-PET-AND-MOBILE-BOUNDARY-20261118.md"

class Pet114Tw2018PetSources(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.a=json.loads(A.read_text(encoding="utf-8"));cls.q=json.loads(Q.read_text(encoding="utf-8"))
 def test_2018_year_stays_open_with_forward_partial_receipt(self):
  a,q=self.a,self.q
  y=next(v for v in q["yearly_work_queue"] if v["year"]==2018)
  self.assertEqual((a["year_frontier_before"],a["year_frontier_after"]),(2018,2018))
  self.assertEqual(a["year_gate"],"NOT_YEAR_AUDITED") # PET114 historical source gate remains, PET115 later reviewed year
  self.assertEqual(y["research_gate"],"SOURCE_BOUNDED_REVIEWED")
  self.assertEqual((q["active_module"],a["active_module"]),( "PET","PET"))
  self.assertEqual(q["current_frontier"]["year"],2019)
  self.assertEqual(q["current_frontier"]["latest_2018_partial_source_receipt"],a["id"])
  self.assertTrue(q["current_frontier"]["next"].startswith(("PET115:","PET116:","PET117:","PET118:")))
  self.assertEqual(y["partial_source_review_receipts"][0]["id"],a["id"])
  self.assertFalse(a["year_closed"])
  self.assertFalse(a["historically_complete"])
  self.assertIn(a["baseline"]["prior_latest_source_bounded_review"],[v["id"] for v in q["root_source_census_receipts"]])

 def test_period_source_grades_and_pets_not_items(self):
  a=self.a
  self.assertEqual(len(a["sources"]),6)
  self.assertEqual(len({x["id"] for x in a["sources"]}),6)
  self.assertTrue(all(x.get("url") for x in a["sources"]))
  self.assertTrue(any("PLAYER" in x["grade"] for x in a["sources"]))
  self.assertTrue(any("MOBILE_NOT_CLASSIC_PC" in x["grade"] for x in a["sources"]))
  self.assertEqual(len(a["player_summer_task_candidate_pet_mentions"]),6)
  self.assertTrue(all(x["first_2018_release_proved"] is False for x in a["player_summer_task_candidate_pet_mentions"]))
  self.assertEqual(len(a["player_summer_item_mentions_not_native_pets"]),3)
  self.assertEqual(a["player_summer_task_candidate_pet_mentions"][2]["canonical_native_pet_id"],None)
  self.assertTrue(all(a["negative_controls"].values()))
  self.assertFalse(a["mobile_boundary"]["classic_pc_pet_backfill_permitted"])
  self.assertEqual(a["mobile_boundary"]["launch_date_reported"],"2018-07-17")

 def test_2018_no_native_recovery_and_immutable_history(self):
  a,q=self.a,self.q
  for key in ("new_original_2018_pc_client_bytes","new_original_2018_pc_patch_bytes","new_2018_native_pet_ids","new_original_spr_frames","new_original_native_pet_skill_functions","new_original_pc_pet_issuance_logs"):
   self.assertEqual(a[key],0)
  self.assertIsNone(a["global_2018_original_pc_species_count"])
  self.assertIsNone(a["first_released_2018_original_pc_species_count"])
  raw=(ROOT/"docs/CURRENT-STATE.md").read_bytes()
  self.assertEqual(len(raw),a["baseline"]["unchanged_current_state_bytes"])
  blob=hashlib.sha1(b"blob "+str(len(raw)).encode("ascii")+b"\x00"+raw).hexdigest()
  self.assertEqual(blob,a["baseline"]["unchanged_current_state_blob"])
  self.assertEqual((a["stage_A"],a["stage_B_wiki"],a["r79"],a["overall_percent"]),(q["stage_A"],q["stage_B_wiki"],q["r79"],q["overall_game_completion_percent"]))
  self.assertIn("PET114",R.read_text(encoding="utf-8"))

if __name__=="__main__":unittest.main()
