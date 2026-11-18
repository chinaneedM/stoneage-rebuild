"""PET84 annual 2010 official-PC-source-bounded review, not historical completeness."""
import json, hashlib, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REC=ROOT/"research"/"recovered"
def read(name):return json.loads((REC/name).read_text(encoding="utf-8"))
class PET84Audit(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.a=read("STONEAGE-PET84-YEAR2010-DRAGONS-FIVE-REGION-BOUNDED-AUDIT-R1.json")
  cls.q=read("STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json")
 def test_forward_only_source_bounded_year_gate(self):
  a,q=self.a,self.q;y=q["yearly_work_queue"][11];n=q["yearly_work_queue"][12]
  self.assertEqual((a["year"],a["year_frontier_before"],a["year_frontier_after"]),(2010,2010,2011))
  self.assertGreaterEqual(q["current_frontier"]["year"],2011)
  self.assertEqual(y["research_gate"],"SOURCE_BOUNDED_REVIEWED")
  self.assertEqual(n["research_gate"],"NOT_YEAR_AUDITED" if q["current_frontier"]["year"]==2011 else "SOURCE_BOUNDED_REVIEWED")
  self.assertFalse(y["historically_complete"])
  self.assertIsNone(y["historical_species_count"])
  self.assertEqual(y["source_bounded_review_receipt"],"research/recovered/STONEAGE-PET84-YEAR2010-DRAGONS-FIVE-REGION-BOUNDED-AUDIT-R1.json")
  self.assertEqual([x["id"] for x in y["partial_source_review_receipts"]][-2:],a["prior_partial_receipts"]+[a["id"]])
  self.assertEqual(sum(x["id"]==a["id"] for x in q["root_source_census_receipts"]),1)
  self.assertEqual(len({x["id"] for x in q["root_source_census_receipts"]}),len(q["root_source_census_receipts"]))
 def test_dragon_names_not_2010_species_releases(self):
  a=self.a;d=a["dragon_source"]
  self.assertEqual([x["name"] for x in d["names"]],["邦恩多斯","斯天多斯"])
  self.assertEqual([x["elements"] for x in d["names"]],[["风","火"],["地","水"]])
  self.assertEqual(d["names"][0]["promotional_location"],"50年前的波拉岛")
  self.assertEqual(d["names"][1]["promotional_quest"],"英雄岛后传")
  self.assertEqual(d["operator_origin_count"],1)
  self.assertFalse(d["first_release_proven"])
  self.assertTrue(all(x["pet_id"] is None for x in d["names"]))
  self.assertIsNone(a["first_release_2010_species_count"])
 def test_raw_client_and_cross_year_gates(self):
  a=self.a;b=a["source_boundaries"]
  self.assertEqual(b["china_client_md5"],"cd0ac0c0bc26bcfefdd08957d8d86e7c")
  self.assertFalse(b["china_client_md5_recomputed"])
  self.assertTrue(b["china_2010_second_test_wiping"])
  self.assertEqual(b["first_nonwipe_beta"],"2011-01-15")
  self.assertTrue(b["jp_jan_planned_not_verified_applied"])
  self.assertTrue(b["kr_later_community_names_unverified"])
  self.assertTrue(b["tw_2010_license_only"])
  self.assertTrue(b["stoneage2_separate"])
  self.assertTrue(a["historical_CURRENT_untouched"])
  self.assertEqual((a["new_original_2010_client_bytes"],a["new_2010_native_pet_ids"],a["new_actual_2010_original_server_pet_grants"]),(0,0,0))
  self.assertEqual(set(a["region_reviews"]),{"CN","TW","JP","KR","OTHER"})
  self.assertEqual(a["five_region_reopen_triggers"],self.q["yearly_work_queue"][11]["residual_reopen_triggers"])
  for region,rd in a["region_reviews"].items():
   self.assertFalse(rd["historically_complete"])
   self.assertIsNone(rd["pet_population"])
   self.assertEqual(rd["reopen_trigger"],self.q["yearly_work_queue"][11]["region_source_reviews"][region]["reopen_trigger"])
   self.assertEqual(rd["native_pet_id_rows_verified"],0)
  self.assertIsNone(a["global_2010_historical_species_population"])
 def test_native_current_blob_unchanged(self):
  a=self.a;raw=(ROOT/"docs"/"CURRENT-STATE.md").read_bytes()
  self.assertEqual(len(raw),2709173)
  self.assertEqual(hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\x00"+raw).hexdigest(),a["startup"]["current_blob"])
  self.assertEqual((a["stage_A"],a["stage_B_wiki"],a["r79"]),("7_PARTIAL_2_OPEN","GATED","PAUSED_NON_BLOCKING"))
if __name__=="__main__":unittest.main()
