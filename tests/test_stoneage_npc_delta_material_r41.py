import copy
import json
import unittest
from tools.stoneage_npc_delta_material_r41 import SOURCE,MATERIAL,LOCAL,validate,validate_local,build,blocks

class NPCMaterialTests(unittest.TestCase):
 def setUp(self):self.report=json.loads(SOURCE.read_text())
 def test_actual_byte_and_character_change_counts(self):
  d=validate(self.report);local=validate_local(json.loads(LOCAL.read_text()),self.report)
  self.assertEqual(len(d['different_byte_offsets']),114);self.assertEqual(d['exact_transcode_candidates'],[])
  self.assertEqual(len(local['character_differences']),14);self.assertEqual(len(local['observed_character_map']),9)
 def test_three_original_records_and_two_scoped_modern_rows(self):
  result=build(self.report);rows=result['original_create_records']
  self.assertEqual([(r['floorid_values'],r['borncenter_values'][:2]) for r in rows],[([11208],[26,40]),([11208],[42,38]),([11214],[41,36])])
  self.assertEqual([r['argument_path'] for r in rows],['100/sb_kbu.arg','100/sb_kbu.arg','100/sb_kgi.arg'])
  self.assertEqual([r['same_carrier_spr_index_numeric_candidates'][0][0] for r in rows],[360,360,313])
  self.assertEqual(len(result['modern_npc_occurrences']),2);self.assertEqual(result['modern_warp_count'],3)
  self.assertFalse(result['limits']['third_record_deleted_in_modern_proven'])
 def test_exact_material_replay(self):self.assertEqual(build(self.report),json.loads(MATERIAL.read_text()))
 def test_no_pure_transcode_relabel(self):
  bad=copy.deepcopy(self.report);bad['argument_delta']['decode_candidates'][0]['exact_transcode_to_modern_gb18030']=True
  with self.assertRaises(ValueError):validate(bad)
 def test_numerical_change_not_hidden_in_text_conversion(self):
  bad=copy.deepcopy(self.report);next(f for f in bad['argument_delta']['modern_fields'] if f['key']=='time')['numbers']=[181]
  with self.assertRaises(ValueError):validate(bad)
 def test_no_official_base_quest_or_execution_promotion(self):
  for key in ('official_same_build_authenticated','original_server_executed','raw_script_bodies_published','verified_base_quests_added'):
   bad=copy.deepcopy(self.report);bad[key]=True
   with self.assertRaises(ValueError):validate(bad)
  bad=copy.deepcopy(self.report);bad['origin_class']='BASE_GAME_QUEST'
  with self.assertRaises(ValueError):validate(bad)
 def test_wrong_original_sha_and_over_budget_rejected(self):
  for kind in ('sha','budget'):
   bad=copy.deepcopy(self.report)
   if kind=='sha':bad['receipt']['members'][0]['sha256']='0'*64
   else:bad['receipt']['actual_range_bytes']=20*1024*1024
   with self.assertRaises(ValueError):validate(bad)
 def test_character_pair_loss_and_false_official_local_claim(self):
  for kind in ('loss','official'):
   bad=json.loads(LOCAL.read_text())
   if kind=='loss':bad['character_differences'].pop()
   else:bad['official_same_build_authenticated']=True
   with self.assertRaises(ValueError):validate_local(bad,self.report)
 def test_unknown_configuration_syntax_is_not_dropped(self):
  p=copy.deepcopy(self.report['configuration_profiles']['sb_geno.create'][0]);p['line_profiles'][3]['kind']='UNCLASSIFIED_FINGERPRINT'
  with self.assertRaises(ValueError):blocks(p,'NPCCREATE')
if __name__=='__main__':unittest.main()
