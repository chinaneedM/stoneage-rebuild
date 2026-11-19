"""PET116-117: 2019 classic-PC six-region initial PET source gate and 2019 Taiwan relayed issue."""
import hashlib, json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P116=ROOT/"research/recovered/STONEAGE-PET116-TW2019-PLAYER-PET-EVIDENCE-R1.json"
P117=ROOT/"research/recovered/STONEAGE-PET117-YEAR2019-SIX-REGION-PC-INITIAL-PET-SOURCE-REVIEW-R1.json"
Q=ROOT/"research/recovered/STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json"
R=ROOT/"docs/continuity/STONEAGE-PET117-YEAR2019-SIX-REGION-ORIGINAL-PC-FIRST-PASS-20261118.md"
REGIONS={"CN","TW","HK_MO","KR","JP","OTHER"}

class Pet117Year2019SourceInitial(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.b=json.loads(P116.read_text(encoding="utf-8"))
  cls.a=json.loads(P117.read_text(encoding="utf-8"))
  cls.q=json.loads(Q.read_text(encoding="utf-8"))

 def test_partial_source_no_forwarding_before_year_audit(self):
  a,q=self.a,self.q
  y=next(v for v in q["yearly_work_queue"] if v["year"]==2019)
  old=next(v for v in q["yearly_work_queue"] if v["year"]==2018)
  self.assertEqual((a["year_frontier_before"],a["year_frontier_after"]),(2019,2019))
  self.assertEqual(a["review_status"],"NOT_YEAR_AUDITED")
  self.assertEqual(y["research_gate"],"SOURCE_BOUNDED_REVIEWED") # PET118 later annual review
  self.assertGreaterEqual(q["current_frontier"]["year"],2020)
  self.assertEqual(q["active_module"],"PET")
  self.assertEqual(old["research_gate"],"SOURCE_BOUNDED_REVIEWED")
  self.assertFalse(a["historically_complete"])
  self.assertIsNone(a["global_2019_species_count"])
  self.assertIsNone(a["official_2019_first_release_species_count"])

 def test_distinct_regions_and_reopen_triggers(self):
  a=self.a
  self.assertEqual(set(a["region_reviews"]),REGIONS)
  self.assertEqual(len(a["reopen_triggers"]),6)
  self.assertEqual(len(set(a["reopen_triggers"])),6)
  for k,v in a["region_reviews"].items():
   self.assertEqual(v["status"],"NOT_YEAR_AUDITED")
   self.assertFalse(v["historically_complete"])
   self.assertIsNone(v["pet_population"])
   self.assertIsNone(v["official_2019_first_release_species_count"])
   self.assertEqual(v["native_pet_ids_verified"],0)
   self.assertEqual(v["reopen_trigger"],a["reopen_triggers"][list(a["region_reviews"]).index(k)])

 def test_spring_pig_original_relay_not_native_and_mobile_separate(self):
  a=self.a
  ids=[s["id"] for s in a["sources"]]
  self.assertEqual(len(ids),len(set(ids)))
  relay=next(s for s in a["sources"] if s["id"]=="TW-2019-0129-SPRING-OPERATOR-VOICE-RELAY")
  player=next(s for s in a["sources"] if s["id"]=="TW-2019-0131-FEB15-MAR11-PLAYER-QUEST-REPLIES")
  mobile=next(s for s in a["sources"] if s["id"]=="NETMARBLE-STONEAGE-M-2019-0123")
  self.assertTrue(relay["not_official_original_html"])
  self.assertEqual(relay["region"],"TW")
  self.assertIn("PLAYER",player["grade"])
  self.assertEqual(player["url"],relay["url"])
  self.assertEqual(mobile["region"],"TW_HK_MO_MOBILE")
  self.assertTrue(mobile["not_original_classic_pc"])
  self.assertTrue(any("豬年寵物袋" in c for c in relay["claims"]))
  self.assertTrue(any("烏力王 already quest-recorded" in s.get("claim","") for s in a["sources"]))
  self.assertTrue(all(a["negative_controls"].values()))
  self.assertFalse(self.b["official_in_game_release_confirmed"])
  self.assertEqual(self.b["year_review_status"],"NOT_YEAR_AUDITED")

 def test_zero_new_original_bytes_and_immutable_current(self):
  a=self.a
  for k in ("new_2019_original_pc_client_bytes","new_2019_original_pc_patch_bytes",
            "new_2019_native_pet_ids","new_2019_original_spr_bytes",
            "new_2019_native_skill_functions","new_2019_native_server_pet_grants"):
   self.assertEqual(a[k],0)
  raw=(ROOT/"docs/CURRENT-STATE.md").read_bytes()
  self.assertEqual(len(raw),a["original_state_bytes"])
  git_sha=hashlib.sha1(b"blob "+str(len(raw)).encode("ascii")+b"\x00"+raw).hexdigest()
  self.assertEqual(git_sha,a["original_state_blob"])
  self.assertIn("PET118",R.read_text(encoding="utf-8"))
  self.assertEqual(a["overall_percent"],None)

if __name__=="__main__": unittest.main()
