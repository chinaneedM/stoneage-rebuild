import hashlib
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
def chain(v):return hashlib.sha256("".join(v).encode("ascii")).hexdigest()

class FiveBrothers2DSourceBridge(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.d=load("research/recovered/STONEAGE-INTEGRATION92-FIVE-BROTHERS-ORIGINAL-2D-R1.json")
  cls.q=load("research/recovered/STONEAGE-QUEST20-FIVE-BROTHERS-MODULE-REVIEW-R1.json")
  cls.p=load("research/recovered/STONEAGE-PET-MODULE-07-TW10-BATCH-PUBLIC-R1.json")
 def test_01_original_npc_bytes_and_30_script_count(self):
  a=self.d["private_original_source"];q=self.q
  self.assertEqual(a["NPC_CREATE_sha256"],q["original_source_create"]["sha256"])
  self.assertEqual((a["NPC_CREATE_bytes"],a["original_NPC_CREATE_count"]),(5199,30))
  self.assertEqual(len(q["source_create_positions"]),30)
  self.assertEqual(len(q["original_scripts"]),30)
  self.assertEqual(a["original_SCRIPT_total_bytes"],sum(x["bytes"] for x in q["original_scripts"]))
 def test_02_script_sha_lineage_from_original_quest20(self):
  src=self.d["private_original_source"]
  q=sorted(self.q["original_scripts"],key=lambda x:x["path"])
  self.assertEqual(src["original_SCRIPT_sha_text_chain_sorted_by_path"],chain(x["sha256"] for x in q))
  self.assertEqual(len(src["original_NPC_CREATE_exact_span_sha_text_chain_PRIVATE_ONLY"]),64)
 def test_03_six_floor_original_geometry_source(self):
  a=self.d["quest_static"]
  self.assertEqual(a["six_DAT_geometries_prior_QUEST20_no_new_DAT_byte_read"],self.q["six_original_map_geometries"])
  self.assertEqual(a["source_30_CREATE_positions_prior_QUEST20"],self.q["source_create_positions"])
  self.assertEqual([x["original_NPC_count"] for x in a["six_DAT_geometries_prior_QUEST20_no_new_DAT_byte_read"]],[6,3,5,5,6,5])
 def test_04_prior_original_choices_unchanged(self):
  a=self.d["quest_static"]
  self.assertEqual(a["five_choices_source_prior_QUEST20"],self.q["five_original_choice_layers"])
  self.assertEqual([x["needed"] for x in a["five_choices_source_prior_QUEST20"]],[2507,2509,2511,2513,2515])
  self.assertTrue(a["original_23_choices_source_prior_QUEST20"])
 def test_05_five_reward_original_numeric_enemy_links(self):
  a=self.d["quest_static"]
  self.assertEqual(a["five_reward_NPCs_prior_QUEST20"],self.q["reward_five_NPCs"])
  rows=a["five_reward_NPCs_prior_QUEST20"]
  self.assertEqual([r["GetPet_enemy_instance"] for r in rows],[54,57,55,56,481])
  self.assertEqual([r["linked_enemy_template"] for r in rows],[91,94,92,93,95])
  self.assertEqual([r["source_npc_graphic_alias"] for r in rows],[100287,100290,100288,100289,100394])
  self.assertTrue(a["actual_5_GetPet_directives_already_WORLD21"])
 def test_06_exact_TW1_full_original_SPR_source_sha(self):
  a=self.d["TW1_cross_version_candidate"];base={x[0]:x for x in self.p["source_groups"]}
  for row in a["source_five_exact_PET07_original_SPR_group_rows"]:
   self.assertEqual(row,base[row[0]])
   self.assertEqual(row[3],56)
  self.assertEqual(a["graphic_order"],[100287,100290,100288,100289,100394])
  self.assertEqual(a["source_full_original_SPR_animations_metadata_not_rendered_total"],280)
 def test_07_selected_15_animation_records_and_123_positions(self):
  a=self.d["TW1_cross_version_candidate"];g=a["source_five_exact_PET07_original_SPR_group_rows"]
  self.assertEqual(sum(len(x[5]) for x in g),15)
  self.assertEqual(sum(x[4] for x in g),123)
  self.assertEqual(sum(x[6] for x in g),86)
  self.assertEqual([[(e[0],e[1]) for e in x[5]] for x in g],[[ (0,0),(2,0),(1,0)]]*5)
 def test_08_source86_pixel_PNG_sha256_receipts(self):
  a=self.d["TW1_cross_version_candidate"]
  ids=a["original_86_bitmap_numbers_sorted"];assert len(ids)==86
  self.assertEqual(sorted(set(ids)),ids)
  p={x[0]:x for x in self.p["source_actual_pixel_receipts"]}
  self.assertTrue(all(x in p for x in ids))
  self.assertEqual(chain(p[i][8] for i in ids),a["original_86_PNG_SHA256_concatenation_chain"])
 def test_09_source86_raw_RD_SHA256_receipts(self):
  a=self.d["TW1_cross_version_candidate"]
  p={x[0]:x for x in self.p["source_actual_pixel_receipts"]}
  self.assertEqual(chain(p[i][2] for i in a["original_86_bitmap_numbers_sorted"]),a["original_86_RD_block_SHA256_concatenation_chain"])
  self.assertEqual(a["new_original_RD_decoded_in_current_unit"],0)
 def test_10_original_duration_differences_kept(self):
  rows={x[0]:x for x in self.d["TW1_cross_version_candidate"]["source_five_exact_PET07_original_SPR_group_rows"]}
  self.assertEqual(rows[100394][5][2][4],1000)
  self.assertEqual([rows[i][5][2][4] for i in (100287,100290,100288,100289)],[100]*4)
 def test_11_private_delivery_and_actual_offline_browser(self):
  a=self.d["private_delivery"]
  self.assertEqual((a["zip_bytes"],a["zip_members"]),(660522,36))
  self.assertEqual(a["zip_sha256"],"b734904c42a8228e6b3127997d33440a39a5446dfa4a1360f5eee4c55e880d50")
  self.assertTrue(a["library_uploaded_and_independently_downloaded_exact_SHA"])
  self.assertEqual(a["six_floor_static_original_coordinate_marker_counts"],[6,3,5,5,6,5])
  self.assertEqual(a["source_15_next_frame_interactions_pass"],15)
  self.assertEqual((a["JS_errors"],a["external_HTTP_requests"]),(0,0))
  self.assertFalse(a["original_copyrighted_NPC_scripts_and_2d_bitmaps_publicly_uploaded"])
 def test_12_no_native_runtime_or_same_deployment_inference(self):
  a=self.d["negative_evidence"]
  self.assertFalse(a["native_original_quest_branch_and_GetPet_reward_execution_verified"])
  self.assertFalse(a["native_original_map_movement_DAT_collision_verified"])
  self.assertFalse(a["original_palettes_and_audio_FPS_verified"])
  self.assertFalse(self.d["TW1_cross_version_candidate"]["original_tw1_official_reward_pet_or_later_server_deployment_PROVEN"])
  self.assertIsNone(a["overall_percent"])
if __name__=="__main__": unittest.main()
