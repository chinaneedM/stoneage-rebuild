"""PET118: source-bounded 2019 six-region classic PC review and forward-only 2020 chronology."""
import json, hashlib, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"research/recovered/STONEAGE-PET118-YEAR2019-SIX-REGION-CLASSIC-PC-BOUNDED-AUDIT-R1.json"
Q=ROOT/"research/recovered/STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json"
R=ROOT/"docs/continuity/STONEAGE-PET118-YEAR2019-SIX-REGION-CLASSIC-PC-SOURCE-BOUNDED-AUDIT-20261119.md"
REGIONS=("CN","TW","HK_MO","KR","JP","OTHER")
class Pet118Year2019Annual(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.a=json.loads(P.read_text(encoding="utf-8"))
  cls.q=json.loads(Q.read_text(encoding="utf-8"))
 def test_2019_source_bounded_handoff_not_historical_closure(self):
  a,q=self.a,self.q
  y=next(x for x in q["yearly_work_queue"] if x["year"]==2019)
  n=next(x for x in q["yearly_work_queue"] if x["year"]==2020)
  self.assertEqual((a["year_frontier_before"],a["year_frontier_after"]),(2019,2020))
  self.assertEqual((a["review_status"],y["research_gate"]),("SOURCE_BOUNDED_REVIEWED","SOURCE_BOUNDED_REVIEWED"))
  self.assertEqual((q["active_module"],a["active_module"]),( "PET","PET"))
  self.assertEqual(q["current_frontier"]["year"],2020)
  self.assertEqual(n["research_gate"],"NOT_YEAR_AUDITED")
  self.assertTrue(q["current_frontier"]["next"].startswith("PET119:"))
  self.assertEqual(q["current_frontier"]["latest_source_bounded_annual_review"],a["id"])
  self.assertTrue(a["source_bounded_only"] and a["year_source_bounded_closed"] and a["year_reopenable"])
  self.assertFalse(a["historically_complete"])
  self.assertFalse(y["historically_complete"])
  self.assertIsNone(y["historical_species_count"])
  self.assertIsNone(a["original_pc_global_2019_species_count"])
  self.assertIsNone(a["original_pc_2019_first_release_species_count"])
 def test_six_regions_preserve_exact_source_gaps(self):
  a,q=self.a,self.q
  y=next(x for x in q["yearly_work_queue"] if x["year"]==2019)
  self.assertEqual(set(a["region_reviews"]),set(REGIONS))
  self.assertEqual(set(y["region_source_reviews"]),set(REGIONS)-{"HK_MO"})
  self.assertEqual(set(y["additional_region_reviews"]),{"HK_MO"})
  self.assertEqual(a["reopen_triggers"],y["residual_reopen_triggers"])
  self.assertEqual(len(set(a["reopen_triggers"])),len(REGIONS))
  for k,v in a["region_reviews"].items():
   saved=y["region_source_reviews"].get(k) or y["additional_region_reviews"].get(k)
   self.assertEqual(saved["review_status"],"SOURCE_BOUNDED_REVIEWED")
   self.assertFalse(saved["historically_complete"])
   self.assertIsNone(saved["pet_population"])
   self.assertIsNone(saved["official_2019_first_release_species_count"])
   self.assertEqual(saved["native_pet_id_rows_verified"],0)
   self.assertEqual(saved["reopen_trigger"],v["reopen_trigger"])
 def test_source_classes_no_duplicate_official_relay_or_mobile_backdating(self):
  a,q=self.a,self.q
  ids=[s["id"] for s in a["sources"]]
  self.assertEqual(len(ids),len(set(ids)))
  primary=next(x for x in a["sources"] if x["id"]=="TW2019-SPRING-PLAYER-OPERATOR-RELAY-PET117")
  repeat=next(x for x in a["sources"] if x["id"]=="TW2019-SPRING-G2-SAME-COPY-NOT-INDEPENDENT")
  mobile=next(x for x in a["sources"] if x["id"]=="NETMARBLE2019-STONEAGE-M-NOT-PC")
  self.assertEqual(primary["region"],"TW")
  self.assertIn("PLAYER",primary["grade"])
  self.assertIn("NOT_INDEPENDENT",repeat["grade"])
  self.assertTrue(mobile["not_original_pc"])
  self.assertTrue(a["product_line_separation"]["mobile_official_pets_not_pc_roster"])
  self.assertTrue(all(a["negative_controls"].values()))
  y=next(x for x in q["yearly_work_queue"] if x["year"]==2019)
  self.assertEqual([x["id"] for x in y["partial_source_review_receipts"]][-3:],[*a["prior_partial_receipts"],a["id"]])
  self.assertEqual(y["source_bounded_review_receipt"],str(P.relative_to(ROOT)))
  self.assertEqual(q["root_source_census_receipts"][-1]["id"],a["id"])
 def test_original_client_zero_only_new_evidence_and_current_immutable(self):
  a,q=self.a,self.q
  for k in ("new_2019_original_pc_client_bytes","new_2019_original_pc_patch_bytes","new_2019_native_pet_ids",
            "new_2019_original_spr_frames","new_2019_native_skill_functions","new_2019_server_pet_grants"):
   self.assertEqual(a[k],0)
  raw=(ROOT/"docs/CURRENT-STATE.md").read_bytes()
  self.assertEqual(len(raw),a["baseline"]["original_state_bytes"])
  sha=hashlib.sha1(b"blob "+str(len(raw)).encode("ascii")+b"\x00"+raw).hexdigest()
  self.assertEqual(sha,a["baseline"]["original_state_blob"])
  self.assertEqual((a["stage_A"],a["stage_B_wiki"],a["r79"],a["overall_percent"]),(q["stage_A"],q["stage_B_wiki"],q["r79"],q["overall_game_completion_percent"]))
  self.assertIn("PET119",R.read_text(encoding="utf-8"))
if __name__=="__main__":unittest.main()
