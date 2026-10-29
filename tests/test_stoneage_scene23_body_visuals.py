import copy,json,unittest
from tools.stoneage_scene23_body_visuals import REPORT,FALSE,validate,KEYS
class Scene23(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.base=json.loads(REPORT.read_bytes())
 def reject(self,fn):
  r=copy.deepcopy(self.base);fn(r)
  with self.assertRaises(ValueError):validate(r)
 def test_actual_96_first_frames(self):self.assertEqual(validate(self.base)['distinct_original_bitmaps'],96)
 def test_every_runtime_identity_boundary(self):
  for k in FALSE:
   with self.subTest(flag=k):self.reject(lambda r:r.update({k:True}))
 def test_cannot_invent_original_roster_count(self):self.reject(lambda r:r.update(original_selectable_character_count=12))
 def test_cannot_invent_source_Action(self):self.reject(lambda r:r.update(source_action_run_id=123))
 def test_cannot_invent_completion(self):self.reject(lambda r:r.update(overall_completion_percent=100))
 def test_source_table_order(self):self.reject(lambda r:r['groups'].reverse())
 def test_missing_candidate(self):self.reject(lambda r:r['groups'].pop())
 def test_extra_candidate(self):self.reject(lambda r:r['groups'].append(r['groups'][0]))
 def test_not_all_actions(self):self.reject(lambda r:r.update(action_code=0))
 def test_not_all_frames(self):self.reject(lambda r:r.update(observed_frame_index=1))
 def test_direction_omission(self):self.reject(lambda r:r['groups'][0]['directions'].pop())
 def test_first_frame_offset(self):self.reject(lambda r:r['groups'][0]['directions'][0].update(first_frame_offset=0))
 def test_bitmap_identity(self):self.reject(lambda r:r['groups'][0]['directions'][0]['first_frame'].__setitem__(0,10188))
 def test_source_duration_not_180_ms(self):self.reject(lambda r:r['groups'][0]['directions'][0].update(duration_word=180))
 def test_source_six_frames_not_universal(self):
  self.assertEqual(sorted({a['source_frame_count']for g in self.base['groups']for a in g['directions']}),[6,9,11,14]);self.assertEqual(sum(a['source_frame_count']for g in self.base['groups']for a in g['directions']),728)
 def test_invalid_uniform_frame_count(self):self.reject(lambda r:r['groups'][1]['directions'][0].update(source_frame_count=6))
 def test_original_full_animation_span(self):self.reject(lambda r:r['groups'][0]['directions'][0].update(animation_span_sha256='0'*64))
 def test_wrong_original_full_group(self):self.reject(lambda r:r['groups'][0].update(full_segment_sha256='0'*64))
 def test_palette_not_runtime_selected(self):self.reject(lambda r:r.update(palette_mode='ACTUAL_GAME_COLOR'))
 def test_no_palette_fingerprint_change(self):self.reject(lambda r:r['source_files']['Palet_1.sap'].update(sha256='0'*64))
 def test_no_original_pixel_metadata_change(self):self.reject(lambda r:r['bitmaps'][0]['palette_candidates']['0'].update(RGBA_sha256='0'*64))
 def test_no_source_RD_change(self):self.reject(lambda r:r['bitmaps'][0].update(RD_sha256='0'*64))
 def test_duplicate_cannot_hide_missing_pixel(self):self.reject(lambda r:r['bitmaps'].__setitem__(1,r['bitmaps'][0]))
 def test_no_dedup_claim(self):self.reject(lambda r:r.update(repeated_first_frame_positions=96))
if __name__=='__main__':unittest.main()
