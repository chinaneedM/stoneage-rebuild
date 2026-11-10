"""INTEGRATION36 exact original quiz controls and unreferenced BAK boundaries."""
import json,hashlib,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/recovered/STONEAGE-INTEGRATION36-QUIZ-THREE-BROTHERS-ORIGINAL-SOURCE-R1.json"
def blob(data):return hashlib.sha1(b"blob "+str(len(data)).encode()+bytes([0])+data).hexdigest()
class Integration36(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.r=json.loads(REPORT.read_text(encoding="utf8"));cls.up={}
  for k,v in cls.r["upstream"].items():
   data=(ROOT/v["path"]).read_bytes()
   assert blob(data)==v["git_blob"],k
   cls.up[k]=json.loads(data)
 def test_current_full_history(self):
  p=self.r["base"];v=(ROOT/"docs/CURRENT-STATE.md").read_bytes()
  self.assertEqual(p["old_CURRENT_bytes"],2709173)
  self.assertEqual(blob(v[:p["old_CURRENT_bytes"]]),p["old_CURRENT_sha256_git_blob"])
 def test_private_verification_receipts_not_source_runtime(self):
  p=self.r["private_verified"]
  self.assertEqual((p["npc_zip"]["members"],p["item_zip"]["members"]),(2205,838))
  self.assertTrue(p["npc_zip"]["all_crc"] and p["item_zip"]["all_crc"])
  self.assertEqual(len(p["item_catalog_sha256"]),64)
 def test_six_original_scripts_from_quest01(self):
  z=self.up["catalog"]["source_scripts"];r=self.r["six_active_scripts"]
  self.assertEqual(len(r),6)
  self.assertEqual(sum(sum(x["source_type_counts"].values()) for x in r),23)
  for x in r:
   orig=next(y for y in z if y["path"]==x["path"])
   self.assertEqual((x["bytes"],x["sha256"],x["crc32"]),(orig["original_size"],orig["original_sha256"],orig["original_crc32"]))
   self.assertEqual(x["source_type_counts"],orig["actual_block_type_counts"])
 def test_eleven_CREATE_and_distinct_placements(self):
  rows=self.r["eleven_CREATE_refs"];orig=self.up["catalog"]["source_creation_references"]
  self.assertEqual(len(rows),11)
  self.assertEqual([(x["floorid"],x["source_xy"]) for x in rows],[(812,[32,24]),(810,[29,16]),(810,[28,16]),(810,[27,16]),(850,[29,16]),(850,[28,16]),(850,[27,16]),(2020,[18,13]),(2020,[18,11]),(4020,[18,13]),(4020,[18,11])])
  for x in rows:
   z=next(y for y in orig if y["create_source_path"]==x["create_source_path"] and y["create_brace_ordinal"]==x["create_brace_ordinal"])
   self.assertEqual((x["original_script_path"],x["original_script_sha"],x["floorid"],x["graphic_alias_numeric"]),(z["original_script_path"],z["original_script_sha"],z["floorid"],z["graphic_alias_numeric"]))
 def test_twenty_three_script_sections_in_catalog(self):
  r=self.r["twenty_three_source_blocks"];z=self.up["catalog"]["source_event_blocks"]
  self.assertEqual(len(r),23)
  for x in r:
   y=next(t for t in z if t["script_path"]==x["script_path"] and t["script_block_ordinal"]==x["ordinal"])
   self.assertEqual((x["event_number"],x["type"],x["source_section_sha256"],x["condition_sha256"]),(y["event_number"],y["raw_type"],y["source_section_decoded_cp950_normalized_UTF8_sha256"],y["condition_expression_decoded_cp950_UTF8_sha256"]))
   self.assertEqual(x["operation_counts"],y["source_operations"])
   self.assertEqual(x["item_refs"],y["item_numeric_refs"])
 def test_message_getitem_and_exact_GetPet_control(self):
  x=self.r["exact_original_ascii_control_fragments"]
  self.assertIn(("MESSAGE","2753"),[(t["type"],t.get("GetItem")) for t in x if t["path"]=="quiz/equiz_02"])
  self.assertIn(("ACCEPT","351","47"),[(t["type"],t.get("GetPet"),t.get("EndSetFlg")) for t in x if t["path"]=="quiz/equiz_04"])
  self.assertEqual([t["GetItem"] for t in x if t["path"].startswith("quiz/uketuke") and "GetItem" in t],["2756","2755","2757"])
 def test_backup_is_real_different_and_unreferenced(self):
  r=self.r["unreferenced_BAK"];a=next(x for x in self.r["six_active_scripts"] if x["path"]=="quiz/equiz_04")
  self.assertEqual((r["bytes"],r["crc32"]),(801,"22c0fd4a"))
  self.assertNotEqual(r["sha256"],a["sha256"])
  self.assertFalse(r["direct_reference_from_active_CREATE"])
  self.assertFalse(r["original_whole_CP950_decode_success"])
  self.assertEqual((r["ascii_control_rows"][1]["EventNo"],r["ascii_control_rows"][1]["GetPet"],r["ascii_control_rows"][1]["EndSetFlg"]),("45","352","45"))
  self.assertFalse(any(x["original_script_path"]==r["path"] for x in self.r["eleven_CREATE_refs"]))
 def test_qualified_floor_gaps_are_not_claimed_absent(self):
  r=self.r["floor_source_status"];self.assertEqual([x["floor"] for x in r if x["in_MAP09"]],[812,2020,4020])
  for x in r:
   if x["in_MAP09"]:self.assertEqual(x["source_DAT_SHA256"],self.up["map09"]["maps"][str(x["floor"])]["source_sha256"])
  self.assertNotEqual(r[3]["source_DAT_SHA256"],r[4]["source_DAT_SHA256"])
  self.assertEqual(r[3]["prior_candidate_canvas_SHA256"],r[4]["prior_candidate_canvas_SHA256"])
 def test_49_numeric_item_candidates_and_empty_token(self):
  p=self.r["item_private_row_source_qualification"];q=p["random_pools"]
  self.assertEqual([x["raw_token_count"] for x in q],[13,20,17])
  self.assertEqual([x["blank_positions"] for x in q],[[1],[],[]])
  self.assertEqual(len(p["source_49_random_item_ids"]),49)
  self.assertEqual(p["source_49_random_item_ids"],sorted(set(n for x in q for n in x["numeric_ids"])))
  self.assertEqual(p["original_49_random_row_sha_manifest_digest"],"642b85fcc88d383afaa0877261e77d6fa194a1aadc25c628d9a103013e95f7d7")
  self.assertEqual([x["alias"] for x in self.r["original_six_item_rows"]],[24222,24222,24314,24314,24314,24309])
 def test_same_source_pet_template_identity_must_remain_distinct(self):
  r=self.r["GetPet_past_and_same_carrier"];rows=r["pet10_same_community_original_template_rows"]
  self.assertEqual([x["id"] for x in rows],[14,351,352])
  self.assertEqual([x["graphic"] for x in rows],[100257,100040,100040])
  self.assertEqual([x["PETFLG_literal"] for x in rows],[1,0,0])
  self.assertNotEqual(rows[1]["primary_original_row_SHA256"],rows[2]["primary_original_row_SHA256"])
  self.assertEqual(r["previous_I05_numeric_occurrences"],[14,14,351])
  for x in rows:
   y=next(y for y in self.up["pet10"]["source_rows"]["enemybase.txt"] if y[1]==x["id"])
   self.assertEqual((x["graphic"],x["PETFLG_literal"],x["primary_original_row_SHA256"]),(y[2],y[3],y[-1]))
  self.assertEqual(r["TW1_PET07_previous_original_pixel_source_group100257"],next(x for x in self.up["pet07"]["source_groups"] if x[0]==100257))
 def test_no_native_execution_or_original_official_deployment_promotion(self):
  x=self.r["bounded_status"]
  for k,v in x.items():
   if k.endswith("_proven") or k.endswith("_committed"):
    self.assertFalse(v,k)
  self.assertEqual(x["Stage_A"],"7_PARTIAL_2_OPEN")
  self.assertIsNone(x["overall_percent"])
if __name__=="__main__":unittest.main()
