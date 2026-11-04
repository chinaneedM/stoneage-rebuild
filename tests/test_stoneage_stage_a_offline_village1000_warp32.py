"""Verify derived original village1000 32-source Warp/DAT closure, without claiming native gameplay."""
import json,unittest
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parents[1]/"research"/"recovered"
def load(name):return json.loads((R/name).read_text(encoding="utf-8"))
class Village1000Warp32(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.r=load("STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-03-VILLAGE1000-32-WARP-DAT-SOURCE-R1.json")
  cls.p=load("STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-02-VILLAGE1000-NPC-SOURCE-BRIDGE-R1.json")
  cls.m=load("STONEAGE-MAP-SCENE-MODULE-01-ORIGINAL-SOURCE-MANIFEST-R1.json")
  cls.a=load("STONEAGE-STAGE-A-INDEPENDENT-RAR-MAP-PIXEL-RECOVERY-R1.json")
  cls.o31=load("STONEAGE-O31-FIVE-DOORWAY-SOURCE-R1.json")
  cls.o41=load("STONEAGE-O41-TWO-SPECIAL-WARP-SOURCE-R1.json")
 def test_original_create_all32_conserved(self):
  old={tuple(x["coordinate_anchor"]):x for x in self.p["rows"] if x["source_function_token"]=="npcgen_warp"}
  rows=self.r["source_CREATE_rows"]
  self.assertEqual(len(old),32);self.assertEqual(len(rows),32)
  self.assertEqual(len({tuple(z["source"]) for z in rows}),32)
  for z in rows:
   o=old[tuple(z["source"][1:])]
   self.assertEqual([z["source_path"],z["source_file_sha256"],z["CREATE_ordinal"],z["CREATE_block_sha256"]],[o["source_file"],o["source_sha256"],o["original_block_ordinal"],o["original_block_sha256"]])
  self.assertEqual(Counter(z["source_path"] for z in rows),Counter({"genout/warp_y.create":22,"genout/100warp.create":9,"poru/dragon_warp.create":1}))
 def test_full_event_code_consistency_and_negative_scope(self):
  r=self.r;rows=r["source_CREATE_rows"];hist={int(k):v for k,v in r["original_DAT_1000_full_event_code_counts"].items()}
  self.assertEqual(hist,{0:1280,16384:140,49152:24148,49155:30,49158:1,49159:1})
  self.assertEqual(sum(hist.values()),160*160)
  self.assertEqual(Counter(z["original_DAT_cell"][2] for z in rows),Counter({49155:30,49158:1,49159:1}))
  self.assertEqual(r["original_DAT_1000_SHA256"],self.o31["provenance"]["map1000_dat_sha256"])
  self.assertEqual(self.o31["collision_review"]["exact_full_DAT_event_49155_counts"]["map1000"],30)
  self.assertTrue(r["claims"]["exact_32_DAT_event_49155_49158_49159_coordinate_set_equals_32_CREATE_centers"])
  self.assertFalse(r["claims"]["original_client_executed"])
  self.assertFalse(r["claims"]["original_warp_trigger_verified"])
  self.assertFalse(r["claims"]["all_original_official_versions_same_deployment"])
 def test_original_target_DATS_exist_as_previously_verified_sources_and_coords_fit(self):
  rr=self.r["source_CREATE_rows"];targets=self.r["verified_original_DAT_target_floors"];self.assertEqual(len(targets),13)
  manifest={x[5]:x for x in self.m["original_decoded_source_rows"] if x[0]==0 and x[5] is not None and str(x[1]).lower().endswith(".dat")}
  for t in targets:
   f=t["floor"];self.assertEqual(t["configured_sources"],sum(x["target"][0]==f for x in rr))
   if f==100:
    source=self.a["priority_four_floors"]["100"]
    self.assertEqual([t["sha256"],t["bytes"],t["dimensions"]],[source["sha256"],source["bytes"],source["dimensions"]])
   else:
    source=manifest[f];self.assertEqual([t["sha256"],t["bytes"],t["dimensions"]],[source[3],source[2],[source[6],source[7]]])
   for x in rr:
    if x["target"][0]==f:
     self.assertTrue(0<=x["target"][1]<t["dimensions"][0])
     self.assertTrue(0<=x["target"][2]<t["dimensions"][1])
 def test_O31_and_O41_prior_raw_source_matches(self):
  rows=self.r["source_CREATE_rows"]
  for q in self.o31["source_order_edges"]:
   if q["source"][0]!=1000:continue
   a=next(x for x in rows if x["source"]==q["source"])
   self.assertEqual(a["target"],q["target"])
   self.assertEqual(a["original_DAT_cell"],q["original_DAT_tile_parts_event"])
  for q in self.o41["six_newly_source_qualified_special_door_blocks"]:
   if q["floor"]!=1000:continue
   a=next(x for x in rows if x["source"]==[1000,*q["from"]])
   self.assertEqual(a["target"],q["to"])
   self.assertEqual(a["original_DAT_cell"],q["original_map1000_planes"])
  self.assertEqual(next(a["original_extra_token"] for a in rows if a["original_DAT_cell"][2]==49158),"M")
  self.assertEqual(next(a["original_extra_token"] for a in rows if a["original_DAT_cell"][2]==49159),"A")
 def test_no_asset_or_historical_promotion(self):
  r=self.r;self.assertIn("COMMUNITY_MIXED25",r["source_scope"])
  self.assertEqual(r["stage_a"],"7_PARTIAL_2_OPEN")
  self.assertEqual(r["stage_b"],"GATED")
  self.assertEqual(r["R79"],"PAUSED_NON_BLOCKING")
  self.assertIsNone(r["overall_percent"])
  self.assertNotIn("original_CREATE_text",r)
  self.assertNotIn("original_DAT_raw",r)
  self.assertEqual([r["private_observer"]["console_errors"],r["private_observer"]["external_requests"]],[0,0])
if __name__=="__main__":unittest.main()
