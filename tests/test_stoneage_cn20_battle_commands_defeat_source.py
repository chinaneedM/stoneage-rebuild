import copy
import json
import unittest
from tools.stoneage_cn20_battle_commands_defeat_source import REPORT,LABELS,POSITIONS,validate,extract_nav,extract_body,replay,image_metadata
class BattleCommandsDefeat(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=json.loads(REPORT.read_text())
 def reject(self,fn):
  r=copy.deepcopy(self.r);fn(r)
  with self.assertRaises(ValueError):validate(r)
 def test_fourteen_source_records_follow_archive_contract(self):
  validate(self.r);c=json.loads((REPORT.parent/'STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json').read_text())['future_website'];self.assertEqual(len(self.r['records']),14)
  for row in self.r['records']:
   self.assertTrue(set(c['record_contract']['required'])<=row.keys());self.assertIn(row['collection'],c['required_collections']);self.assertIsNone(row['game_ids'])
 def test_eight_command_relative_positions_not_pixel_or_wire_bindings(self):
  rows=self.r['records'][:8];self.assertEqual([r['source_reported']['label'] for r in rows],LABELS);self.assertEqual([r['source_reported']['relative_position'] for r in rows],POSITIONS)
  self.reject(lambda r:r['records'][0]['source_reported'].__setitem__('wire_or_pixel_binding',[20,30]))
 def test_input_loop_is_not_agility_order_or_fixed_timer(self):
  self.assertEqual(self.r['records'][8]['source_reported']['loop'][-1],'IF_UNFINISHED_WAIT_AGAIN')
  self.reject(lambda r:r['boundaries'].__setitem__('player_round_input_is_agility_execution_order',True))
  self.reject(lambda r:r['records'][8]['source_reported'].__setitem__('timeout_seconds',30))
 def test_equipment_magic_does_not_prove_natural_skill_catalog(self):
  self.assertEqual(self.r['records'][1]['source_reported']['meaning'],'SPIRIT_MAGIC_ATTACHED_TO_EQUIPMENT')
  self.reject(lambda r:r['records'][1]['source_reported'].__setitem__('meaning','ALL_INTRINSIC_PLAYER_SPELLS'))
 def test_capture_five_before_rebirth_does_not_fix_later_cap_or_rate(self):
  x=self.r['records'][2]['source_reported']['meaning'];self.assertEqual(x['pre_rebirth_capacity'],5);self.assertTrue(x['full_capacity_blocks_capture'])
  self.reject(lambda r:r['boundaries'].__setitem__('post_rebirth_capacity',6));self.reject(lambda r:r['boundaries'].__setitem__('capture_success_rate',1))
 def test_help_symbol_not_unrestricted_entry_or_free_action(self):
  self.assertEqual(self.r['records'][3]['source_reported']['meaning']['symbol'],'HELP')
  self.reject(lambda r:r['boundaries'].__setitem__('help_is_unrestricted_join',True))
  self.reject(lambda r:r['boundaries'].__setitem__('help_turn_cost',0))
 def test_defense_often_not_guaranteed_or_half_damage(self):
  self.assertIn('OFTEN',self.r['records'][4]['source_reported']['meaning'])
  self.reject(lambda r:r['boundaries'].__setitem__('defense_is_guaranteed_or_half_damage',True))
 def test_escape_party_disband_is_conditional_on_actual_exit(self):
  e=self.r['records'][7]['source_reported']['meaning'];self.assertEqual(e['after_member_leaves_battle'],'LEAVES_PARTY');self.assertEqual(e['after_leader_leaves_battle'],'PARTY_DISBANDS')
  self.reject(lambda r:r['boundaries'].__setitem__('escape_success_probability',1))
  self.reject(lambda r:r['boundaries'].__setitem__('leader_flee_is_automatic_leader_transfer',True))
 def test_pet_standby_wording_is_not_numeric_state_and_protection_is_qualified(self):
  self.assertEqual(self.r['records'][6]['source_reported']['meaning']['command_eligible_state_as_written'],'待机')
  self.assertIn('SOME',self.r['records'][9]['source_reported']['protection']);self.assertEqual(self.r['records'][9]['source_reported']['source_typo_as_written'],'宠物义何中技能')
  self.reject(lambda r:r['boundaries'].__setitem__('protect_loyalty_threshold_or_probability',100))
  self.reject(lambda r:r['boundaries'].__setitem__('source_typo_silently_corrected',True))
 def test_solo_zero_hp_return_one_not_savepoint_or_max_hp(self):
  d=self.r['records'][10]['source_reported'];self.assertEqual((d['hp_trigger'],d['on_return_to_scene_hp']),(0,1));self.assertIsNone(d['return_location'])
  self.reject(lambda r:r['records'][10]['source_reported'].__setitem__('on_return_to_scene_hp',100))
  self.reject(lambda r:r['boundaries'].__setitem__('all_faints_go_to_record_point',True))
 def test_team_or_wording_not_formal_boolean_or_no_penalties(self):
  self.assertIn('_OR_',self.r['records'][11]['source_reported']['continuation'])
  self.reject(lambda r:r['records'][11]['source_reported'].__setitem__('formal_boolean','ANY_ACTIVE_TEAMMATE'))
  self.reject(lambda r:r['boundaries'].__setitem__('no_death_means_no_penalties',True))
 def test_overkill_to_record_point_not_numeric_threshold_or_solo_faint(self):
  o=self.r['records'][12]['source_reported'];self.assertEqual(o['destination'],'纪录点');self.assertIsNone(o['exact_threshold'])
  self.reject(lambda r:r['boundaries'].__setitem__('overkill_damage_multiplier',3))
 def test_earlier_outdoor_riding_image_does_not_restore_battle_screen(self):
  self.assertEqual(self.r['inputs'][2]['capture_timestamp'],'20011023202109')
  self.assertFalse(self.r['records'][13]['source_reported']['battle_ui_verified'])
  self.reject(lambda r:r['boundaries'].__setitem__('image_is_battle_command_screen',True));self.reject(lambda r:r['boundaries'].__setitem__('image_english_labels_authenticate_region_or_language',True))
 def test_ten_real_semantic_mutations_and_unsigned_hosting_boundaries(self):
  a=json.loads((REPORT.parent/'STONEAGE-CN20-BATTLE-COMMANDS-DEFEAT-NEGATIVE-AUDIT-R1.json').read_text());self.assertEqual(len(a['cases']),10)
  self.assertTrue(all(x['semantic_extract_rejected'] and x['original_sha256']==self.r['inputs'][1]['sha256'] and x['original_sha256']!=x['mutated_sha256'] for x in a['cases']))
  self.assertTrue(any('exactly one' in x['reason'] for x in a['cases']))
  self.reject(lambda r:r['boundaries'].__setitem__('operator_authorship_verified',True));self.reject(lambda r:r['boundaries'].__setitem__('original_server_execution_verified',True))
  for f in [extract_nav,extract_body,image_metadata]:
   with self.assertRaises(ValueError):f(b'<html>not source</html>')
  with self.assertRaises(ValueError):replay(self.r,[b'']*2)
if __name__=='__main__':unittest.main()
