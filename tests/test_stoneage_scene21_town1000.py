import copy,json,unittest
from pathlib import Path
from tools.stoneage_scene21_town1000 import REPORT,FALSE,validate,validate_actual_replay,prefix_evidence,map_cells,query

class Scene21Source(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.r=json.loads(REPORT.read_bytes());cls.a=json.loads((REPORT.parent/'STONEAGE-SCENE21-ACTUAL-PIXEL-ACCEPTANCE-R1.json').read_bytes())
 def reject(self,change):
  r=copy.deepcopy(self.r);change(r)
  with self.assertRaises((ValueError,KeyError)):validate(r)
 def test_full_original_source_metadata(self):self.assertEqual(validate(self.r)['new_map_images'],19)
 def test_archived_prefix_report_cannot_be_invented(self):
  with self.assertRaises(ValueError):prefix_evidence(b'REAL_DIFF|common_prefix_bytes=315842228')
 def test_corpus_match_not_official_or_native_claim(self):
  for k in FALSE:
   with self.subTest(field=k):self.reject(lambda r:r.update({k:True}))
 def test_no_false_current_full_REAL_read(self):self.reject(lambda r:r.update(current_mixed_REAL_bytes_read=315842228))
 def test_wrong_prefix_parent_rejected(self):self.reject(lambda r:r['prefix_bridge'].update(mixed_REAL_sha256='0'*64))
 def test_NPC_cell_outside_old_view(self):self.reject(lambda r:r.update(NPC_cell_old_window_covered=True))
 def test_unknown_map_word_not_collision(self):self.assertEqual(self.r['NPC_cell_original_three_u16'],[187,0,49152])
 def test_wrong_coordinates_rejected(self):self.reject(lambda r:r['NPC_source'].update(xy=[63,102]))
 def test_source_image_not_NPC_identity(self):self.reject(lambda r:r.update(original_NPC_name_or_dialogue_authenticated=True))
 def test_new_alias_record_cannot_drift(self):self.reject(lambda r:r['resources']['187'].update(index=20))
 def test_new_RD_digest_cannot_drift(self):self.reject(lambda r:r['resources']['187'].update(RD_sha256='0'*64))
 def test_missing_cells_not_dropped(self):self.reject(lambda r:r['cells'].pop())
 def test_source_placement_not_replaced(self):self.reject(lambda r:r['placements'][0].update(image_key=100000))
 def test_finite_coverage_not_overall_completion(self):self.reject(lambda r:r.update(overall_completion_percent=100))
 def test_fake_source_run_rejected(self):self.reject(lambda r:r.update(source_CI_run_id=1))
 def test_current_map_must_match_whole_source(self):
  with self.assertRaises(ValueError):map_cells(b'\0'*153608)
 def test_current_ADRN_must_match_whole_source(self):
  with self.assertRaises(ValueError):query(b'\0'*80,set(range(56)))
 def test_all_actual_pixel_frames_replayed(self):self.assertEqual(validate_actual_replay(self.a,self.r)['full_canvas_states'],8)
 def test_one_changed_canvas_pixel_hash_rejected(self):
  a=copy.deepcopy(self.a);a['frames']['expanded_parts1_npc1']='0'*64
  with self.assertRaises(ValueError):validate_actual_replay(a,self.r)
 def test_source_view_not_browser_execution(self):
  a=copy.deepcopy(self.a);a['actual_source_browser_verified']=True
  with self.assertRaises(ValueError):validate_actual_replay(a,self.r)
 def test_old_NPC_option_states_preserve_duplicate_pixels(self):
  for parts in (0,1):self.assertEqual(self.r['frames'][f'old_parts{parts}_npc0']['RGBA_sha256'],self.r['frames'][f'old_parts{parts}_npc1']['RGBA_sha256'])
 def test_public_template_contains_no_original_image(self):
  text=Path(__file__).resolve().parents[1].joinpath('tools/stoneage_scene21_observer.html').read_text();self.assertEqual(text.count('__PRIVATE_SCENE_JSON__'),1);self.assertNotIn('iVBORw0KGgo',text)
if __name__=='__main__':unittest.main()
