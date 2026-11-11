"""Source-qualified three-pet ranch and real TW1 original-pixel metadata without private assets."""
from pathlib import Path
import json,hashlib,unittest

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/recovered/STONEAGE-INTEGRATION55-DINO-RANCH-THREE-PETS-TW1-48-REAL-PIXELS-R1.json"
def gitblob(raw):return hashlib.sha1(b"blob "+str(len(raw)).encode()+bytes([0])+raw).hexdigest()
class TestIntegration55RanchSourceAndPixelBoundaries(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.r=json.loads(REPORT.read_text(encoding="utf8"));cls.input={}
  for k,e in cls.r["qualified_input_git_blobs"].items():
   raw=(ROOT/e["path"]).read_bytes()
   assert gitblob(raw)==e["git_blob_sha"],f"{k} Git source changed"
   cls.input[k]=json.loads(raw)
 def test_preserve_full_historical_current(self):
  h=self.r["history_original_current_blob_preserved"]
  self.assertEqual((h["blob"],h["bytes"]),("c89e0e33537990aa2132b47c40fef49a985a935c",2709173))
  self.assertTrue(h["full_remote_blob_retrieved"]);self.assertFalse(h["edited"])
 def test_real_source_quest17_original_private_archive_identity(self):
  a=self.r["private_original_source_custody_replay"]
  self.assertEqual((a["quest17"]["bytes"],a["quest17"]["member_count"],a["quest17"]["CRC_pass"]),(29802,32,True))
  self.assertEqual(a["quest17"]["embedded_source_git_blob_sha"],self.r["qualified_input_git_blobs"]["quest17"]["git_blob_sha"])
  self.assertEqual(a["pet07"]["sha256"],self.input["pet07"]["private_artifacts"]["catalog"]["sha256"])
  self.assertEqual(a["pet07"]["bytes"],self.input["pet07"]["private_artifacts"]["catalog"]["bytes"])
  self.assertEqual(a["pet07_original_source_receipt"]["bytes"],1617404)
 def test_original_six_create_locations_and_two_prior_map_provenances(self):
  q=self.input["quest17"]
  self.assertEqual(self.r["source_original_ranch_all_six_CREATEs"],q["source_creates"])
  self.assertEqual(len(q["source_creates"]),6)
  self.assertEqual(self.r["source_prior_MAP09_two_DAT_metadata_ONLY"],q["source_map_qualification"])
  self.assertEqual([x["floor"] for x in q["source_map_qualification"]["previously_verified_map09_DAT"]],[201,20901])
  self.assertTrue(all(not x["source_DAT_bytes_replayed_this_round"] for x in q["source_map_qualification"]["previously_verified_map09_DAT"]))
  self.assertEqual(self.r["new_qualified_work"]["private_source_map_DAT_201_20901_reopened_this_work"],0)
 def test_three_original_active_scripts_and_wristbands(self):
  q=self.input["quest17"];bs=self.r["three_source_bounded_pets_with_48_actual_real_PNG_observations"]
  self.assertEqual([x["source_quest_PET_predicate_numeric"] for x in bs],[560,559,558])
  self.assertEqual([x["source_item_wristband"]["id"] for x in bs],[2594,2595,2596])
  for b in bs:
   original=next(x for x in q["pet_certificate_branches"] if x["pet_predicate_numeric"]==b["source_quest_PET_predicate_numeric"])
   self.assertEqual(b["source_active_script"]["branch_metadata"],original)
   manifest=next(x for x in q["source_manifest"] if x["path"]==b["source_active_script"]["path"])
   self.assertEqual(b["source_active_script"]["full_original_file_sha256"],manifest["sha256"])
   self.assertEqual(b["source_active_script"]["original_bytes"],manifest["bytes"])
   self.assertEqual(b["source_CREATE_NPC"],next(x for x in q["source_creates"] if x["script_ref"]==manifest["path"]))
   self.assertEqual(b["source_CREATE_NPC"]["floor"],201)
   self.assertEqual(b["source_active_script"]["source_DelPet_literal_patterns"],
      [f'DelPet:PET>0-{original["pet_predicate_numeric"]}*{n}' for n in (4,3,2,1)])
   self.assertEqual(b["source_active_script"]["initial_EVDEL_requires_source_semantics"],"UNVERIFIED")
 def test_source_pet_template_two_tables_and_alias_many_to_one(self):
  p=self.input["pet10"]
  for b in self.r["three_source_bounded_pets_with_48_actual_real_PNG_observations"]:
   template=b["source_quest_PET_predicate_numeric"]
   for f,key in (("enemybase.txt","source_mixed25_template_main"),("enemybase2.txt","source_mixed25_template_alternative")):
    old=next(x for x in p["source_rows"][f] if x[1]==template)
    got=b[key]
    self.assertEqual([got["physical_source_row"],got["template_id"],got["graphic"],got["PETFLG"],got["original_source_line_sha256"]],
       [old[0],old[1],old[2],old[3],old[16]])
    self.assertEqual(old[3],1)
    allrows=[x for x in p["source_rows"][f] if x[2]==old[2]]
    self.assertEqual(b["source_graphic_other_candidate_template_rows"][f],
       [dict(physical_source_row=x[0],template=x[1],graphic=x[2],pet_flag=x[3],original_source_line_sha256=x[16]) for x in allrows])
    self.assertGreater(len(allrows),1)
   self.assertEqual(b["source_mixed25_template_main"]["original_source_line_sha256"],b["source_mixed25_template_alternative"]["original_source_line_sha256"])
 def test_TW1_real_source_group_SPR_and_motion_census(self):
  p7=self.input["pet07"];p15=self.input["pet15"]
  for b in self.r["three_source_bounded_pets_with_48_actual_real_PNG_observations"]:
   g=b["source_qualified_TW1_SPR"];id=g["graphic_alias"]
   self.assertEqual(g["source_group"],next(x for x in p7["source_groups"] if x[0]==id))
   p=next(x for x in p15["groups"] if x["graphic"]==id)
   self.assertEqual((g["source_group"][1],g["source_group"][2]),(p["group_index"],p["segment_sha256"]))
   self.assertEqual(g["complete_PET15_selected_motion"]["source_sequences"],56)
   self.assertEqual(g["complete_PET15_selected_motion"]["total_frame_positions"],p["frame_positions"])
   self.assertEqual(g["complete_PET15_selected_motion"]["distinct_bitmap_numbers_within_group"],p["distinct_bitmaps"])
   self.assertEqual([x[0] for x in g["source_group"][5]],[0,2,1])
   self.assertEqual(g["source_group"][6],16)
 def test_all_48_prior_private_png_evidence_rows_match_exact_public_RD_receipts(self):
  p7=self.input["pet07"]
  got=self.r["three_source_bounded_pets_with_48_actual_real_PNG_observations"]
  self.assertEqual([len(x["source_real_original_PNG_evidence"]["source_bitmap_ids"]) for x in got],[16,16,16])
  expected=[[x for x in p7["source_actual_pixel_receipts"] if base<=x[0]<base+16] for base in (101451,114011,121107)]
  for b,e in zip(got,expected):
   r=b["source_real_original_PNG_evidence"]
   self.assertEqual(r["source_pet07_actual_original_RD_to_PNG_receipts"],e)
   self.assertEqual(r["source_bitmap_ids"],[x[0] for x in e])
   self.assertTrue(r["private_actual_byte_sha256_independently_verified"])
   self.assertTrue(all(len(x[2])==64 and len(x[8])==64 and x[5]>0 and x[6]>0 for x in e))
  self.assertEqual(sum(len(x) for x in expected),48)
 def test_no_unrenderable_native_sequence_among_three_selected(self):
  excluded=self.input["pet07"]["source_renderable_sequences_excluded"]
  ids={100271,100335,100368}
  self.assertFalse(any(x["graphic"] in ids for x in excluded))
  self.assertEqual(self.r["new_qualified_work"]["new_original_source_RD_blocks_decoded_this_work"],0)
 def test_four_original_icons_and_multi_item_alias_are_not_four_items(self):
  q=self.input["quest17"]
  self.assertEqual(self.r["four_source_qualified_item_PNG_candidates"],q["original_tw1_cross_carrier_candidate_images"])
  self.assertEqual([x["alias"] for x in q["original_tw1_cross_carrier_candidate_images"]],[22114,22118,22120,24222])
  self.assertEqual(self.r["source_quest17_original_item_table_8_records"],q["source_items"])
  b=self.r["three_source_bounded_pets_with_48_actual_real_PNG_observations"]
  for x in b:
   w=next(y for y in q["source_items"] if y["item_id"]==x["source_item_wristband"]["id"])
   icon=next(y for y in q["original_tw1_cross_carrier_candidate_images"] if y["alias"]==w["source_image_alias"])
   self.assertEqual(x["source_item_wristband"]["source_TW1_PNG_sha256"],icon["private_png_sha256"])
   self.assertEqual(x["source_item_wristband"]["exact_previous_ICON_source"],icon)
  self.assertGreater(len([x for x in q["source_items"] if x["source_image_alias"]==24222]),1)
 def test_private_gallery_custody_and_rights_guards(self):
  g=self.r["private_gallery_archived_and_reread"]
  self.assertEqual((g["bytes"],g["member_count"],g["animation_PNG_assets"],g["item_icon_PNG_assets"]),(582786,54,48,4))
  self.assertEqual((len(g["sha256"]),len(g["atlas"]["sha256"])),(64,64))
  self.assertTrue(g["all_member_crc_pass"] and g["uploaded_personal_Library_and_independently_retrieved_matching_full_sha_and_54_CRC"] and g["original_PNG_48_individual_hashes_reverified_after_download"])
  self.assertEqual((g["atlas"]["size_px"],g["atlas"]["bytes"]),([1690,1260],327095))
  self.assertTrue(all(x is False for x in self.r["important_negative_guards"].values()))
  self.assertEqual(self.r["source_version_scope"]["source_same_deployment_authenticated"],False)
  self.assertEqual(self.r["stage_A"],{"PARTIAL":7,"OPEN":2})
  self.assertEqual((self.r["stage_B"],self.r["wiki"],self.r["R79"]),("GATED","GATED","PAUSED_NON_BLOCKING"))
  self.assertIsNone(self.r["overall_percent"])
if __name__=="__main__":unittest.main()
