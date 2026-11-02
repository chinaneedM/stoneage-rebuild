"""CHAR02 receipt only: original character candidate source boundaries, not replay of commercial RD pixels in CI."""
import copy,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
F=ROOT/'research/recovered/STONEAGE-CHARACTER-NPC-MODULE-02-TW1-12-ACTOR-ACTION2-RECEIPT-R1.json'
P=ROOT/'research/recovered/STONEAGE-SCENE23-BODY-VISUALS-R1.json'
def certify(r,old):
 assert r["schema"]=="stoneage.character_npc_module_02_TW1_original_character_12_groups_action2_full_pixel_batch_receipt.r1"
 assert r["source_scope"].startswith("ACCEPTED_TW1_RETAIL_SAME_CARRIER_")
 assert r["baseline"]["unchanged_current_state_blob"]=="20050acf279a01555ab06a381dfcdc936bd381a6"
 assert r["original_retained_client_package"]=={"bytes":372626292,"sha256":"3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24"}
 assert r["original_source_member_full_sha256"]==old["source_files"]
 assert r["source_action_numeric"]==2 and r["source_directions"]==list(range(8))
 assert old["groups"] and len(r["original_source_groups"])==len(old["groups"])==12
 total=0
 for i,(record,prior) in enumerate(zip(r["original_source_groups"],old["groups"])):
  no,source_index,group_sha,per_direction,occurrences=record
  assert no==100000+i*20==prior["spr_no"]
  assert source_index==prior["source_group_index"]
  assert group_sha==prior["full_segment_sha256"]
  assert [x["direction"] for x in prior["directions"]]==list(range(8))
  assert [x["source_frame_count"] for x in prior["directions"]]==[per_direction]*8
  assert occurrences==per_direction*8
  total+=occurrences
 assert total==r["source_metrics"]["original_ordered_frame_positions"]==728
 m=r["source_metrics"]
 assert m["source_TW1_body_graphic_candidate_groups"]==12
 assert m["original_animation_action2_direction_sequences"]==96
 assert m["distinct_original_RD_bitmap_numbers"]==576
 assert m["actual_private_source_RD_decoded_bitmap_count"]==576
 assert m["strict_RD_decode_failures"]==0
 assert m["prior_SCENE23_first_frames_sha_cross_checked"]==old["first_frame_occurrences"]==96
 assert m["prior_SCENE23_first_frame_positions_reused"]==96
 assert m["unobserved_later_positions_relative_only_to_SCENE23"]==728-96
 assert r["private_material"]["original_full_source_derived_metadata_receipt"]["included_in_this_git_commit"] is False
 assert r["private_material"]["original_576_bitmap_two_candidate_palette_self_contained_html"]["included_in_public_git"] is False
 assert r["private_material"]["actual_local_chromium_static_original_png_load"]["sequences_tested"]==96
 assert r["private_material"]["actual_local_chromium_static_original_png_load"]["external_requests"]==0
 assert r["private_material"]["actual_local_chromium_static_original_png_load"]["javascript_errors"]==0
 assert r["private_material"]["original_2_SAP_palette_selection_at_runtime_verified"] is False
 assert all(x is False for k,x in r["scope_negations"].items() if k!="total_project_restoration_percent")
 assert r["scope_negations"]["total_project_restoration_percent"] is None
 assert r["other_TW1_NPC_like_resource_source_not_promoted"]["original_resource_occurrences"]==101
 assert r["other_TW1_NPC_like_resource_source_not_promoted"]["official_NPC_identity_or_world_coordinates_proven"] is False
 assert r["next"].startswith("CHARACTER_NPC_MODULE_03")
class CHAR02(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.rec=json.loads(F.read_text(encoding="utf-8"))
  cls.old=json.loads(P.read_text(encoding="utf-8"))
 def check(self,d):certify(d,self.old)
 def test_all_bounded_source_metadata(self):self.check(self.rec)
 def test_no_fake_character_roster(self):
  r=copy.deepcopy(self.rec);r["scope_negations"]["all_12_graphic_numbers_are_official_separate_characters"]=True
  with self.assertRaises(AssertionError):self.check(r)
 def test_no_fake_action_label(self):
  r=copy.deepcopy(self.rec);r["scope_negations"]["native_action2_semantic_label_authenticated"]=True
  with self.assertRaises(AssertionError):self.check(r)
 def test_no_fake_pixel_recovery(self):
  r=copy.deepcopy(self.rec);r["source_metrics"]["actual_private_source_RD_decoded_bitmap_count"]=575
  with self.assertRaises(AssertionError):self.check(r)
 def test_no_frame_dropping(self):
  r=copy.deepcopy(self.rec);r["original_source_groups"][1][4]-=1
  with self.assertRaises(AssertionError):self.check(r)
 def test_no_fake_runtime_color_proof(self):
  r=copy.deepcopy(self.rec);r["private_material"]["original_2_SAP_palette_selection_at_runtime_verified"]=True
  with self.assertRaises(AssertionError):self.check(r)
if __name__=="__main__":unittest.main()
