"""INTEGRATION89 source- and version-bounded original dino cave records."""
import json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]/"research"/"recovered"
def load(path): return json.loads((ROOT/path).read_text(encoding="utf-8"))
class TestDinoCaveSource(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.r=load("STONEAGE-INTEGRATION89-DINO-CAVE-GATES-SHOPS-ORIGINAL-2D-R1.json")
  cls.npc=load("STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json")
  cls.sprite=load("STONEAGE-PET-MODULE-07-TW10-BATCH-PUBLIC-R1.json")
  cls.items2=load("item-module-01/STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-02-R1.json")
  cls.items5=load("item-module-01/STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-05-R1.json")
 def test_original_5743_byte_parent_file_digest_and_crc(self):
  old=next(x for x in self.npc["source_files"] if x[0]=="genout/bait_01.create")
  src=self.r["preservation_source"]
  self.assertEqual([5743,src["original_source_file_sha256"],src["original_source_file_crc32"]],old[1:4])
 def test_all_35_original_create_span_digest_and_original_fields_conserved(self):
  old=[x for x in self.npc["create_rows"] if x[0]=="genout/bait_01.create"]
  rows=self.r["original_35_source_CREATE_rows"]
  self.assertEqual(35,len(old));self.assertEqual(35,len(rows))
  self.assertEqual(list(range(35)),[x["ordinal"] for x in rows])
  for o,r in zip(old,rows):
   self.assertEqual([o[1],[o[2],o[3]],*o[4:16]],[r[k] for k in ("ordinal","original_byte_range","original_CREATE_block_sha256","source_floor","source_graphic_numeric","source_borncorner","source_borncenter","source_createnum","source_dir","source_npc_function","same_source_template_class","same_source_template_candidates","original_name_utf8_sha256","exact_same_archive_reference_paths_and_sha256")])
 def test_exact_five_original_floor_numeric_spaces_and_function_split(self):
  c=self.r["source_counts"]
  self.assertEqual([200,201,20901,20902,20903],c["original_floors"])
  self.assertEqual({"npcgen_man":20,"npcgen_signboard":7,"npcgen_warpman":3,"npcgen_limitshop":3,"npcgen_dengon":1,"npcgen_shop":1},c["original_function_counts"])
  self.assertEqual(35,sum(c["original_function_counts"].values()))
 def test_16_direct_original_references_all_same_archive_targets(self):
  refs=[ref for r in self.r["original_35_source_CREATE_rows"] for ref in r["exact_same_archive_reference_paths_and_sha256"]]
  self.assertEqual(16,len(refs));self.assertEqual(16,len({x[0] for x in refs}))
  self.assertTrue(all(x[1]=="EXACT_SAME_NPC_SUBTREE_PATH" and len(x[2])==64 for x in refs))
 def test_three_original_warpman_gates_have_unique_source_sha_and_conditions(self):
  d=self.r["three_original_warpman_NPC_source_arguments"]
  self.assertEqual([0,3,5],[x["ordinal"] for x in d])
  self.assertEqual(["LV>4","ITEM=2595","ITEM=2596"],[x["literal_FREE"] for x in d])
  self.assertEqual([[20901,0,8],[20902,53,51],[20903,5,5]],[x["literal_WARP"] for x in d])
  by={r["ordinal"]:r for r in self.r["original_35_source_CREATE_rows"]}
  for x in d:
   original=by[x["ordinal"]]
   self.assertEqual(x["source_xy"],original["source_borncorner"][:2])
   self.assertEqual("npcgen_warpman",original["source_npc_function"])
   self.assertEqual(x["original_arg_SHA256"],original["exact_same_archive_reference_paths_and_sha256"][0][2])
   self.assertEqual("-1",x["literal_MONEY"])
 def test_4_original_shop_parameters_rates_and_item_number_literal_preserved(self):
  d=self.r["four_original_shop_and_meat_purchase_arg_literals"]
  self.assertEqual([31,32,33,34],[x["ordinal"] for x in d])
  self.assertEqual(["0.6","0.8","0.7","0.6"],[x["literal_sell_rate"] for x in d])
  self.assertEqual(["12856","1234-1249","1234-1249","1234-1249"],[x["literal_LimitItemNo"] for x in d])
  self.assertEqual(["0.6","1.0","1.0","1.0"],[x["literal_special_rate"] for x in d])
  self.assertEqual("12856",d[0]["literal_ItemList"])
  self.assertTrue(all(x["literal_ItemList"] is None for x in d[1:]))
  by={r["ordinal"]:r for r in self.r["original_35_source_CREATE_rows"]}
  for x in d:
   o=by[x["ordinal"]]
   self.assertEqual(x["original_arg_SHA256"],o["exact_same_archive_reference_paths_and_sha256"][0][2])
 def test_all_three_static_item_ids_in_both_94_column_original_masters(self):
  r=self.r["three_existing_original_itemset_full_row_SHA_and_different_carrier_icon_candidates"]
  self.assertEqual([2595,2596,12856],[x["original_ID"] for x in r])
  self.assertEqual([22114,22118,24045],[x["same_archive_mixed25_original_image_alias"] for x in r])
  for x in r:
   s=self.items5 if x["original_ID"]==12856 else self.items2
   old=next(z for z in s["rows"] if z[0]==x["original_ID"])
   self.assertEqual([x["original_ID"],x["source_a_original_94_field_row_sha256"],x["source_b_original_94_field_row_sha256"],x["same_archive_mixed25_original_image_alias"],x["same_archive_mixed25_original_image_alias"],x["original_B_cost_literal"],x["original_B_type_literal"],x["original_B_level_literal"],x["different_carrier_TW1_original_pixel_qualification_from_prior_ITEM01"],x["different_carrier_TW1_original_pixel_qualification_from_prior_ITEM01"],x["original_changed_field_numbers_between_two_mixed25_itemsets"]],old)
 def test_original_TW1_cross_carrier_graphic_replay_10_groups_18_rows_30_actions(self):
  g=self.r["ten_graphic_number_cross_carrier_2D_source_groups"]
  old={x[0]:x for x in self.sprite["source_groups"]}
  by={x["ordinal"]:x for x in self.r["original_35_source_CREATE_rows"]}
  self.assertEqual([100250,100251,100252,100271,100275,100276,100278,100335,100368,100393],[x["same_number_cross_carrier_source_graphic"] for x in g])
  self.assertEqual(18,sum(len(x["mixed25_original_CONFIG_block_ordinals"]) for x in g))
  self.assertEqual(250,sum(x["selected_source_action_direction0_frame_occurrences"] for x in g))
  self.assertEqual(168,sum(x["selected_source_distinct_original_bitmap_count"] for x in g))
  for x in g:
   src=old[x["same_number_cross_carrier_source_graphic"]]
   self.assertEqual([src[1],src[2],src[3],src[4],src[5],src[6]],[x["separate_TW1_original_SPR_source_index"],x["separate_TW1_full_SPR_group_SHA256"],x["TW1_source_total_animation_records"],x["selected_source_action_direction0_frame_occurrences"],x["selected_source_action_direction0_digest_records"],x["selected_source_distinct_original_bitmap_count"]])
   for idx in x["mixed25_original_CONFIG_block_ordinals"]:
    self.assertEqual(x["same_number_cross_carrier_source_graphic"],by[idx]["source_graphic_numeric"])
 def test_original_palette_counterexample_52_and_scope_364_not_source_verified(self):
  c=self.r["source_counts"]
  g=self.r["ten_graphic_number_cross_carrier_2D_source_groups"]
  first=[x for x in g if x["same_number_cross_carrier_source_graphic"] in (100250,100251,100252)]
  other=[x for x in g if x not in first]
  self.assertEqual(52,sum(x["selected_source_distinct_original_bitmap_count"] for x in first))
  self.assertEqual(116,sum(x["selected_source_distinct_original_bitmap_count"] for x in other))
  self.assertTrue(all(x["actual_private_previous_gallery_png_SHA_qualification"].startswith("OLDER_PRIVATE_GALLERY_PALETTE_PNG_SHA_DIFFERS") for x in first))
  self.assertTrue(all(x["actual_private_previous_gallery_png_SHA_qualification"].endswith("MATCHES_NEWER_TW1_SOURCE_RECEIPT") for x in other))
  self.assertEqual(532,c["private_OLD_PET07_gallery_distinct_embedded_PNG_candidates"])
  self.assertEqual(364,c["private_gallery_other_bitmap_PNG_not_in_newer_selected_source_report"])
  self.assertEqual(93,c["private_OLD_PET07_gallery_all_directions_sequences"])
  self.assertEqual(852,c["private_OLD_PET07_gallery_all_directions_frames"])
 def test_private_browser_execution_not_falsely_certified(self):
  v=self.r["private_visual_test_actual"]
  self.assertTrue(v["private_HTML_inline_javascript_Node_syntax_check_passed"])
  self.assertFalse(v["private_Browser_Chromium_UI_execution_test_passed"])
  self.assertTrue(v["private_Browser_Chromium_launch_blocked_or_timed_out"])
  self.assertTrue(v["private_ZIP_saved_library_and_reloaded"])
 def test_no_live_game_runtime_or_official_same_deployment_claims(self):
  n=self.r["historical_limit"]
  for k in ("late_mixed25_quest_and_original_TW1_art_same_official_build_proven","source_WARP_FREE_gate_executed_by_native_game","source_MONEY_minus_one_native_payment_semantics_proven","source_shop_sell_rate_effect_in_running_economy_proven","original_commercial_images_and_script_text_uploaded_public"):
   self.assertFalse(n[k],k)
  self.assertEqual(0,self.r["source_counts"]["new_original_RD_byte_blocks_decoded"])
  self.assertEqual("7 PARTIAL + 2 OPEN",n["stageA"]);self.assertIsNone(n["overall_percent"])
if __name__=="__main__": unittest.main()
