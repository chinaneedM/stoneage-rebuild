"""INTEGRATION38 immutable source-contract regression; no proprietary bytes in Git."""
import json,hashlib,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"research/recovered/STONEAGE-INTEGRATION38-SBC-JBA-CERTIFICATE-ACCESS-ORIGINAL-SOURCE-R1.json"
def gitblob(raw):
 return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
class Integration38(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.r=json.loads(OUT.read_text(encoding="utf8"));cls.up={}
  for k,v in cls.r["upstream"].items():
   b=(ROOT/v["path"]).read_bytes();assert gitblob(b)==v["git_blob"],k
   cls.up[k]=json.loads(b)
 def test_existing_full_current_preserved(self):
  q=self.r["remote_start"];v=(ROOT/"docs/CURRENT-STATE.md").read_bytes()
  self.assertEqual(q["original_CURRENT_bytes"],2709173)
  self.assertEqual(gitblob(v[:2709173]),q["original_CURRENT_git_blob"])
 def test_eight_original_files_present_in_prior_real_source_index(self):
  d={x[0]:x for x in self.up["char01"]["source_files"]}
  f=self.r["eight_private_original_NPC_source_files"];self.assertEqual(len(f),8)
  for x in f:
   y=d[x["path"]];self.assertEqual([x["bytes"],x["sha256"],x["crc32"]],y[1:4])
 def test_five_create_identity_and_precise_script_refs(self):
  rows=self.r["five_original_CREATE_rows"];self.assertEqual(len(rows),5)
  ref={(x[0],x[1]):x for x in self.up["char01"]["create_rows"]}
  for x in rows:
   y=ref[(x["path"],x["ordinal"])]
   self.assertEqual([x["full_original_block_sha256"],x["floor"],x["graphic"],x["original_borncorner"],x["template_function"],x["exact_source_file_refs"]],[y[4],y[5],y[6],y[7],y[11],y[15]])
  self.assertEqual([x["floor"] for x in rows],[10920,10920,20712,10913,20704])
  self.assertEqual([x["graphic"] for x in rows][:3],[16035,16068,16035])
 def test_four_old_quest_sections_and_reciprocal_certificate_controls(self):
  groups=self.r["previously_QUEST01_indexed_two_original_scripts_and_four_ACCEPT"]
  old=self.up["quest01"];self.assertEqual(sum(len(x["blocks"]) for x in groups),4)
  for x in groups:
   s=next(y for y in old["source_scripts"] if y["path"]==x["path"])
   self.assertEqual([x["original_sha256"],x["bytes"],x["crc32"]],[s["original_sha256"],s["original_size"],s["original_crc32"]])
   for b in x["blocks"]:
    y=next(z for z in old["source_event_blocks"] if z["script_path"]==x["path"] and z["script_block_ordinal"]==b["ordinal"])
    self.assertEqual([b["previous_indexed_section_sha256"],b["previous_indexed_condition_sha256"]],[y["source_section_decoded_cp950_normalized_UTF8_sha256"],y["condition_expression_decoded_cp950_UTF8_sha256"]])
    self.assertEqual([b["GetItem"]],y["item_numeric_refs"]["GetItem"])
    self.assertEqual([] if b["DelItem"] is None else [b["DelItem"]],y["item_numeric_refs"].get("DelItem",[]))
  self.assertEqual([(x["blocks"][1]["DelItem"],x["blocks"][1]["GetItem"]) for x in groups],[(2480,2479),(2479,2480)])
 def test_two_original_certificates_are_distinct_and_source_pinned(self):
  old={x[0]:x for x in self.up["item02"]["rows"]}
  rows=self.r["two_certificate_item_original_rows_and_TW1_pixel_candidates"]
  self.assertEqual([x["id"] for x in rows],[2479,2480])
  self.assertEqual([x["original_image_alias"] for x in rows],[22014,22013])
  for x in rows:
   y=old[x["id"]];self.assertEqual([x["original_both_itemset_sha256"],x["original_image_alias"],x["source_raw_type"],x["source_raw_price"],x["source_raw_level"]],[y[1],y[4],y[6],y[5],y[7]])
   self.assertEqual(y[1],y[2])
   self.assertFalse(x["cross_carrier_TW1"]["same_deployment_proven"])
 def test_two_gate_parameters_and_three_original_DAT_bounds(self):
  g=self.r["two_original_membership_gates"]
  self.assertEqual([(x["floor"],x["xy"],x["FREE"],x["WARP"]) for x in g],[(10913,[37,11],"ITEM=2479",[10920,57,79]),(20704,[14,14],"ITEM=2480",[20712,4,5])])
  m={x["floor"]:x for x in self.r["three_original_DAT_rechecked"]}
  self.assertEqual(set(m),{20712,10913,20704})
  for n in [10913,20704]:self.assertEqual(m[n]["sha256"],self.up["map09"]["maps"][str(n)]["source_sha256"])
  self.assertNotIn("20712",self.up["map09"]["maps"])
  self.assertEqual(m[20712]["cells"][0],[[27,24],[400,0,49152]])
  self.assertFalse(self.r["bounded_missing_original_floor"]["in_selected_955_DAT"])
  self.assertTrue(self.r["bounded_missing_original_floor"]["not_absent_from_historical_game"])
 def test_no_real_runtime_or_false_promotion(self):
  p=self.r["limits"]
  for k in ("active_server_deployment_proven","original_script_condition_semantics_executed","original_certificate_issue_or_exchange_executed","mutual_exclusion_in_native_player_inventory_proven","native_warp_execution_proven","mixed25_server_TW1_retail_pixel_same_deployment"):self.assertFalse(p[k])
  self.assertEqual(p["stage_A"],"7_PARTIAL_2_OPEN")
  self.assertIsNone(p["overall_percent"])
  self.assertEqual(self.r["summary"]["new_native_game_execution"],0)
if __name__=="__main__":unittest.main()
