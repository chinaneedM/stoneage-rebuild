"""O8 regression: synthetic mutations of PUBLIC numerical receipts, no original copyrighted data."""
import copy
import unittest
from tools import stoneage_o8_source_contract as m

class O8SourceGate(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.records=m.read()
 def check_failure(self,key,mutator,expect):
  records=copy.deepcopy(self.records);mutator(records[key])
  with self.assertRaisesRegex(ValueError,expect):m.validate(records)
 def test_accept_source_bound_original_two_room_windows(self):
  result=m.validate(self.records);self.assertEqual(result["unique_two_view_source_placements"],52)
  self.assertEqual(result["source_1001_shop_cells"],25);self.assertFalse(result["native_world_entered"])
 def test_source_shop_has_30_real_original_map_placements(self):
  s=self.records["o8"];self.assertEqual(s["original_shop_placements"],30);self.assertEqual(s["original_shop_unique_bitmap_ids"],10)
 def test_missing_map_part_rejected(self):
  self.check_failure("o8",lambda x:x.__setitem__("original_shop_part_occurrences",4),"30 source map")
 def test_wrong_original_shop_crop_rejected(self):
  self.check_failure("o8",lambda x:x.__setitem__("source_shop_crop",[12,12,17,17]),"shop crop")
 def test_wrong_original_source_map_hash_rejected(self):
  self.check_failure("o8",lambda x:x.__setitem__("raw_1001_DAT_sha256","0"*64),"DAT SHA")
 def test_only_five_source_overlap_cells(self):
  self.check_failure("o8",lambda x:x["common_exact_source_cell_layer_id_placements"].pop(),"overlap conservation")
 def test_wrong_shared_cell_id_rejected(self):
  self.check_failure("o8",lambda x:x["common_exact_source_cell_layer_id_placements"][1].__setitem__(2,5015),"five source cell")
 def test_source_unique_placement_count_cannot_double_count(self):
  self.check_failure("o8",lambda x:x.__setitem__("unique_entrance_plus_shop_placements",57),"overlap conservation")
 def test_wrong_cross_source_original_png_sha_rejected(self):
  self.check_failure("o8",lambda x:x["shared_bitmap_full_sha256"].__setitem__("5000","0"*64),"sprite identity")
 def test_new_original_png_fake_NPC_rejected(self):
  self.check_failure("o8",lambda x:x["added_private_real_png_sha256"].__setitem__("npc-5863","0"*64),"NPC PNG SHA")
 def test_wrong_NPC_shop_coordinate_rejected(self):
  self.check_failure("o8",lambda x:x["source_npc_shop"].__setitem__("xy",[13,13]),"NPC coordinate")
 def test_misleading_shop_NPC_native_render_rejected(self):
  self.check_failure("o8",lambda x:x["source_npc_shop"].__setitem__("native_render_authenticated",True),"unproven original shop")
 def test_shop_NPC_visible_by_default_rejected(self):
  self.check_failure("o8",lambda x:x["source_npc_shop"].__setitem__("overlay_opt_in_default_off",False),"unproven original shop")
 def test_official_TW1_lineage_promotion_rejected(self):
  self.check_failure("o8",lambda x:x.__setitem__("source_grade","OFFICIAL_TW1"),"official lineage")
 def test_wrong_original_private_parent_rejected(self):
  self.check_failure("o8",lambda x:x["private_inputs"]["O7"].__setitem__("sha256","0"*64),"O7 original")
 def test_original_O7_parent_stays_byte_exact(self):
  self.check_failure("o8",lambda x:x["private_archive"].__setitem__("inherited_O7_files_byte_unchanged",286),"O7 existing")
 def test_no_invented_extra_shop_pngs(self):
  self.check_failure("o8",lambda x:x["private_archive"].__setitem__("additional_original_PNGs",5),"bitmap conservation")
 def test_no_native_collision_inference(self):
  self.check_failure("o8",lambda x:x.__setitem__("native_collision_or_occlusion_authenticated",True),"unproven historical")
 def test_no_original_shop_transaction_inference(self):
  self.check_failure("o8",lambda x:x.__setitem__("native_shop_dialogue_or_transaction_authenticated",True),"unproven historical")
 def test_browser_pets_only_source_positions(self):
  self.check_failure("o8",lambda x:x["private_browser"].__setitem__("pet_frame_positions_decoded",351),"frame total")
 def test_browser_anti_network(self):
  self.check_failure("o8",lambda x:x["private_browser"].__setitem__("external_requests",1),"external network")
 def test_browser_legacy_execution_cannot_be_assumed(self):
  self.check_failure("o8",lambda x:x["private_browser"].__setitem__("historic_original_game_executable_entered",True),"false original client")
 def test_private_library_sha_guard(self):
  self.check_failure("o8",lambda x:x["private_archive"].__setitem__("sha256","0"*64),"archived SHA")
 def test_completion_percent_unknown(self):
  self.check_failure("o8",lambda x:x.__setitem__("overall_percent",89),"false restoration progress")
 def test_private_commercial_pngs_never_in_public_repository(self):
  self.assertFalse(self.records["o8"]["copyrighful_original_art_public_distribution"])
  self.assertEqual(len(self.records["o8"]["added_private_real_png_sha256"]),4)

if __name__=="__main__":unittest.main()
