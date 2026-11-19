"""PET119: 2020 Taiwan rat-year classic PC operator-voice relay vs Netmarble independent mobile."""
import unittest, json, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"research/recovered/STONEAGE-PET119-TW2020-RAT-AND-KR-STONEAGE-WORLD-MOBILE-SOURCE-GRADES-R1.json"
Q=ROOT/"research/recovered/STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json"
R=ROOT/"docs/continuity/STONEAGE-PET119-TW2020-RAT-FESTIVAL-KR-WORLD-MOBILE-SOURCE-20261119.md"
class Pet119Year2020Sources(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.a=json.loads(P.read_text(encoding="utf-8"))
  cls.q=json.loads(Q.read_text(encoding="utf-8"))
 def test_2020_still_open_and_pet118_2019_boundary_preserved(self):
  a,q=self.a,self.q
  y=next(x for x in q["yearly_work_queue"] if x["year"]==2020)
  prev=next(x for x in q["yearly_work_queue"] if x["year"]==2019)
  self.assertEqual((a["year_frontier_before"],a["year_frontier_after"]),(2020,2020))
  self.assertEqual((q["current_frontier"]["year"],y["research_gate"]),(2020,"NOT_YEAR_AUDITED"))
  self.assertEqual(prev["research_gate"],"SOURCE_BOUNDED_REVIEWED")
  self.assertFalse(prev["historically_complete"])
  self.assertTrue(q["current_frontier"]["next"].startswith("PET120:"))
  self.assertEqual(y["partial_source_review_receipts"][-1]["id"],a["id"])
  self.assertEqual(q["current_frontier"]["latest_2020_partial_source_receipt"],a["id"])
  self.assertEqual(q["root_source_census_receipts"][-1]["id"],a["prior_annual"])
  self.assertFalse(a["historically_complete"])
  self.assertIsNone(a["original_pc_2020_first_release_species_count"])
  self.assertIsNone(a["original_pc_2020_global_species_count"])
 def test_same_thread_relay_and_native_pc_exclusions(self):
  a=self.a
  ids=[x["id"] for x in a["sources"]]
  self.assertEqual(len(ids),len(set(ids)))
  t=[x for x in a["sources"] if x["product"]=="CLASSIC_2D_PC"]
  self.assertEqual(len(t),4)
  self.assertEqual(len({x["url"] for x in t}),1) # same player thread, NOT four independent operator notices
  self.assertTrue(any("2020-02-19" in " ".join(x.get("claims",[])) for x in t))
  self.assertEqual(len(a["candidate_village_rat_labels"]),4)
  self.assertEqual(len(a["candidate_pc_reward_labels"]),3)
  self.assertTrue(all(a["negative_controls"].values()))
 def test_first_party_mobile_titles_not_2020_classic_pc(self):
  a=self.a
  s={x["id"]:x for x in a["sources"]}
  l=s["NETMARBLE2020-JUNE18-WORLD_LIVE"]
  n=s["NETMARBLE2020-JULY31-WORLD_TWO_PETS"]
  self.assertEqual(l["product"],"STONEAGE_WORLD_MOBILE")
  self.assertEqual(n["grade"],"FIRSTPARTY_OPERATOR_MOBILE_UPDATE_ANNOUNCED_ADDED_PETS")
  self.assertEqual(n["named_pet_labels"],["푸곤","칼로"])
  self.assertEqual(a["mobile_confirmed_announcement_named_labels"][:2],n["named_pet_labels"])
  self.assertEqual(a["mobile_advertised_unnamed_giro_variants"],6)
  self.assertTrue(a["product_lines"]["KR_GLOBAL_STONEAGE_WORLD_2020_MOBILE"]["firstparty_mobile_launch_confirmed"])
  self.assertIsNone(a["product_lines"]["TW_2020_CLASSIC_PC"]["actual_native_released_pet_population"])
 def test_original_pc_additions_zero_and_historical_blob_invariant(self):
  a,q=self.a,self.q
  for k in ("new_2020_original_pc_client_bytes","new_2020_original_pc_patch_bytes","new_2020_native_pet_ids",
            "new_2020_original_sprite_bytes","new_2020_native_skill_functions","new_2020_native_server_grant_logs"):
   self.assertEqual(a[k],0)
  raw=(ROOT/"docs/CURRENT-STATE.md").read_bytes()
  self.assertEqual(len(raw),a["original_state_bytes"])
  self.assertEqual(hashlib.sha1(b"blob "+str(len(raw)).encode("ascii")+b"\x00"+raw).hexdigest(),a["original_state_blob"])
  self.assertEqual((a["stage_A"],a["stage_B_wiki"],a["r79"],a["overall_percent"]),(q["stage_A"],q["stage_B_wiki"],q["r79"],q["overall_game_completion_percent"]))
  self.assertIn("PET120",R.read_text(encoding="utf-8"))
if __name__=="__main__": unittest.main()
