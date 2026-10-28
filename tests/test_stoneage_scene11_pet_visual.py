"""SCENE11 fixed material, pairwise pixel and negative provenance tests (no original assets)."""
import copy,json,unittest
from tools.stoneage_scene11_pet_action2_visual import S,R40,validate
class TestScene11(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.report=json.loads(S.read_text());cls.mat=json.loads(R40.read_text())
 def test_positive(self):
  x=validate(self.report,self.mat)
  self.assertEqual(x['source_frames'],256);self.assertEqual(x['paired_frames'],48)
 def mutation(self,fn):
  m=copy.deepcopy(self.report);fn(m)
  with self.assertRaises(ValueError):validate(m,self.mat)
 def test_no_world_promotion(self):self.mutation(lambda r:r.update(original_game_world_entered=True))
 def test_no_names_promotion(self):self.mutation(lambda r:r.update(official_species_identity_proven=True))
 def test_no_client_promotion(self):self.mutation(lambda r:r.update(original_native_client_render_verified=True))
 def test_no_raw_asset_leak(self):self.mutation(lambda r:r.update(private_proprietary_png_published=True))
 def test_repeated_frame_denominator(self):self.mutation(lambda r:r['groups'][2].update(repeated_frame_positions=0))
 def test_source_segment_sha(self):self.mutation(lambda r:r['groups'][0].update(full_group_SHA256='0'*64))
 def test_frame_pattern(self):self.mutation(lambda r:r['graphic_100252_direction_frame_pattern'].reverse())
 def test_alpha_mutation(self):self.mutation(lambda r:r['groups'][0]['direction_visible_pixel_totals'].__setitem__(0,0))
 def test_palette_determinism_promotion(self):self.mutation(lambda r:r['fixed_global_color_remap_negative'].update(a_single_source_RGBA_to_target_RGBA_mapping_can_reproduce_all_visible_pairs=True))
 def test_color_count_mutation(self):self.mutation(lambda r:r['fixed_global_color_remap_negative'].update(source_rgba_colors_multiple_targets=0))
 def test_bad_visible_pixel_accounting(self):self.mutation(lambda r:r['fixed_global_color_remap_negative'].update(B_only_visible=9))
 def test_pair_delta(self):self.mutation(lambda r:r['pair_100250_100251'].update(total_rgba_pixel_differences=0))
 def test_visual_bbox(self):self.mutation(lambda r:r['groups'][1]['direction_union_bbox_xyxy'][1].__setitem__(2,0))
 def test_no_actual_private_pictures_in_repo(self):
  self.assertTrue(self.report['private_proprietary_png_published'] is False)
  for x in ('actor_images','original_sprite_data','private_file_id','raw_png_base64'):
   self.assertNotIn(x,self.report)
if __name__=='__main__':unittest.main()
