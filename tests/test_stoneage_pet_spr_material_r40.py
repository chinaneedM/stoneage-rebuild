import copy
import json
import unittest
from tools.stoneage_pet_spr_material_r40 import SOURCE,MATERIAL,validate,build

class SPRMaterialTests(unittest.TestCase):
 def setUp(self):self.report=json.loads(SOURCE.read_text())
 def test_complete_source_index_and_frame_reencoding(self):
  m=validate(self.report)
  self.assertEqual(m['index_rows_count'],847)
  self.assertEqual(m['unmatched_graphic_keys'],[])
  self.assertEqual(sorted(g['spr_no'] for g in m['selected_groups']),[100250,100251,100252])
 def test_actual_action_header_differences_are_retained(self):
  profiles={g['spr_no']:{a['anim_no']:a for a in g['action_headers']} for g in build(self.report)['per_group_action_header_profiles']}
  self.assertEqual(profiles[100250][0]['frame_count_values'],[9])
  self.assertEqual(profiles[100252][0]['frame_count_values'],[26])
  self.assertEqual(profiles[100250][4]['duration_values'],[800])
  self.assertEqual(profiles[100252][4]['duration_values'],[100])
  self.assertEqual(profiles[100252][2]['direction_values'],list(range(8)))
 def test_exact_persistent_material_replay(self):
  self.assertEqual(build(self.report),json.loads(MATERIAL.read_text()))
 def test_no_original_official_or_runtime_promotion(self):
  for key in ('original_payload_published','original_program_executed','same_deployed_build_proven','official_species_identity_authenticated','actual_render_or_audio_proven'):
   bad=copy.deepcopy(self.report);bad[key]=True
   with self.assertRaises(ValueError):validate(bad)
 def test_index_reserved_or_order_change_breaks_original_sha(self):
  for col in (1,2,3,4):
   bad=copy.deepcopy(self.report);bad['material']['all_index_rows'][0][col]+=1
   with self.assertRaises(ValueError):validate(bad)
 def test_frame_and_sound_and_duration_mutations_refused(self):
  for field in range(4):
   bad=copy.deepcopy(self.report)
   bad['material']['selected_groups'][0]['animations'][0]['frames'][0][field]+=1
   with self.assertRaises((ValueError,OverflowError)):validate(bad)
  bad=copy.deepcopy(self.report);bad['material']['selected_groups'][0]['animations'][0]['duration']+=1
  with self.assertRaises(ValueError):validate(bad)
 def test_source_occurrence_cannot_be_dropped_or_duplicated(self):
  for variant in ('group','animation','frame'):
   bad=copy.deepcopy(self.report);m=bad['material']
   if variant=='group':m['selected_groups'].pop()
   elif variant=='animation':m['selected_groups'][0]['animations'].pop()
   else:m['selected_groups'][0]['animations'][0]['frames'].pop()
   with self.assertRaises(ValueError):validate(bad)
 def test_old_six_index_duplicates_must_survive(self):
  bad=copy.deepcopy(self.report);bad['material']['duplicate_group_keys']={}
  with self.assertRaises(ValueError):validate(bad)
if __name__=='__main__':unittest.main()
