"""Public-derived verification of WORLD04 3 original source-villages and one missing inline signboard."""
from pathlib import Path
from collections import Counter
import json,unittest
R=Path(__file__).resolve().parents[1]/"research"/"recovered"
def load(filename):return json.loads((R/filename).read_text(encoding="utf-8"))
class World04Source(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.w=load("STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-04-THREE-VILLAGE-NPC-TEXT-SOURCE-R1.json")
  cls.char=load("STONEAGE-CHARACTER-NPC-MODULE-07-TOWNPEOPLE-SIGNBOARD-SOURCE-CATALOG-R1.json")
  cls.char01=load("STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json")
  cls.map=load("STONEAGE-MAP-SCENE-MODULE-01-ORIGINAL-SOURCE-MANIFEST-R1.json")
  cls.ind=load("STONEAGE-STAGE-A-INDEPENDENT-RAR-MAP-PIXEL-RECOVERY-R1.json")
 def test_46_existing_original_ARG_references_not_reinvented(self):
  old=[r for r in self.char["records"] if r["source_floorid_raw"] in ("2000","3000","4000")]
  assert len(old)==46
  prior={(r["create_path"],r["create_ordinal"]):r for r in old}
  rows=self.w["rows"]
  self.assertEqual(len(rows),47);self.assertEqual(len(prior),46)
  self.assertEqual(len({z["original_arg_path"] for z in rows}),47)
  recheck=0
  for r in rows:
   key=(r["source_CREATE_path"],r["source_CREATE_ordinal"])
   if key not in prior:continue
   o=prior[key]
   self.assertEqual([r["floor"],r["role"],r["source_CREATE_file_sha256"],r["original_arg_path"],r["original_arg_sha256"],r["original_arg_bytes"],r["original_CREATE_block_sha256_prior_CHAR07"]],
    [int(o["source_floorid_raw"]),o["role"],o["create_source_sha256"],o["original_arg_path"],o["original_arg_sha256"],o["original_arg_size"],o["create_block_sha256"]])
   self.assertEqual(r["position"],list(map(int,o["source_borncorner_raw"].split(",")))[:2])
   recheck+=1
  self.assertEqual(recheck,46)
  keys=sorted(old,key=lambda x:(x["create_path"],x["create_ordinal"]))
  s="".join("|".join([x["source_floorid_raw"],x["create_path"],str(x["create_ordinal"]),x["original_arg_path"],x["original_arg_sha256"]])+"\n" for x in keys)
  h=2166136261
  for c in s.encode("ascii"):h=((h^c)*16777619)&0xffffffff
  self.assertEqual(f"{h:08x}","a53e22e0")
  self.assertEqual(self.w["counts"]["prior_CHAR07_46_source_key_fnv1a32"],"a53e22e0")
 def test_additional_original_inline_create_and_one_byte_arg(self):
  row=next(r for r in self.w["rows"] if r["original_arg_path"]=="genout/signb_2000_87_78")
  old=[a for a in self.char01["create_rows"] if a[0]==row["source_CREATE_path"] and a[1]==row["source_CREATE_ordinal"]]
  self.assertEqual(len(old),1);a=old[0]
  self.assertEqual(a[5],2000);self.assertEqual(a[6],10061)
  self.assertEqual(a[4],row["original_CREATE_block_sha256_prior_CHAR01"])
  self.assertEqual(a[15][0][0],row["original_arg_path"])
  self.assertEqual(a[15][0][2],row["original_arg_sha256"])
  self.assertEqual(row["position"],[87,78])
  self.assertEqual(row["original_arg_bytes"],1)
  self.assertTrue(self.w["newly_delineated_inline_signboard"]["ARG_is_exactly_one_linefeed"])
  self.assertEqual(self.w["newly_delineated_inline_signboard"]["original_CREATE_NAME_contains_escaped_literal_newlines"],4)
  self.assertNotIn(row["original_arg_path"],{x["original_arg_path"] for x in self.char["records"]})
 def test_floors_map_DAT_sha_qualifications(self):
  w=self.w;floor_rows=Counter(r["floor"] for r in w["rows"])
  self.assertEqual(floor_rows,{2000:14,3000:17,4000:16})
  self.assertEqual(Counter(r["role"] for r in w["rows"]),{"TownPeople":35,"SignBoard":12})
  manifest={int(r[5]):r for r in self.map["original_decoded_source_rows"] if r[0]==0 and r[5] is not None and str(r[1]).lower().endswith(".dat")}
  for r in w["floor_original_DAT_receipts"]:
   floor=r["floor"];self.assertEqual(r["dimensions"],[150,150])
   for entry in w["rows"]:
    if entry["floor"]==floor:self.assertTrue(0<=entry["position"][0]<150 and 0<=entry["position"][1]<150)
   if floor==3000:
    a=self.ind["priority_four_floors"]["3000"]
    self.assertEqual([r["original_DAT_sha256"],r["original_DAT_crc32"],r["original_DAT_bytes"]],[a["sha256"],a["crc32"],a["bytes"]])
   else:
    a=manifest[floor]
    self.assertEqual([r["original_DAT_sha256"],r["original_DAT_crc32"],r["original_DAT_bytes"]],[a[3],a[4],a[2]])
 def test_private_original_sources_remain_private_and_limits(self):
  w=self.w
  self.assertEqual(w["counts"]["original_config_and_arg_rows"],47)
  self.assertEqual(w["counts"]["original_ARG_raw_bytes_total"],5634)
  self.assertEqual(w["counts"]["original_CREATE_source_files"],11)
  self.assertEqual(w["private_deliverable"]["browser_assertions_passed"],16)
  self.assertEqual(w["private_deliverable"]["browser_js_errors"],0)
  self.assertEqual(w["private_deliverable"]["browser_external_HTTP_requests"],0)
  self.assertEqual(w["stage_a"],"7_PARTIAL_2_OPEN")
  self.assertIsNone(w["overall_percent"])
  self.assertIn("MIXED25",w["scope"])
  self.assertTrue(all(w["bounds"].values()))
  self.assertFalse(any("original_cp950_decoded_text" in r or "original_name_raw" in r for r in w["rows"]))
  self.assertNotIn("original_CREATE_full_text",w)
if __name__=="__main__":unittest.main()
