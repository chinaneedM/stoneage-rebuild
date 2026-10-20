import copy
import json
import unittest
from tools.stoneage_tw75_spirit_summon_preview import REPORT,validate,extract_body,extract_index,replay
class SummonPreview(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=json.loads(REPORT.read_text())
 def reject(self,fn):
  r=copy.deepcopy(self.r);fn(r)
  with self.assertRaises(ValueError):validate(r)
 def test_ten_source_records_archive_contract(self):
  validate(self.r);c=json.loads((REPORT.parent/'STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json').read_text())['future_website']
  self.assertEqual(len(self.r['records']),10)
  for row in self.r['records']:
   self.assertTrue(set(c['record_contract']['required'])<=row.keys());self.assertIn(row['collection'],c['required_collections']);self.assertIsNone(row['game_ids'])
 def test_index_date_body_capture_and_three_image_captures_stay_separate(self):
  self.assertEqual(self.r['source_dates']['index_label'],'2004-5-28');self.assertEqual(self.r['source_dates']['body_capture'],'20051129125915')
  self.assertTrue(all(x.startswith('20041211') for x in self.r['source_dates']['image_captures']))
  self.reject(lambda r:r['source_dates'].__setitem__('body_capture','20040528000000'))
 def test_preview_nearing_completion_not_verified_deployment(self):
  self.assertIn('NEARING_COMPLETION',self.r['records'][0]['source_reported']['preview_development_state'])
  self.reject(lambda r:r['boundaries'].__setitem__('preview_proves_actual_release',True))
 def test_messenger_and_hero_are_player_roles_not_named_npcs(self):
  self.assertEqual([x['source_reported']['role'] for x in self.r['records'][1:3]],['使者','勇者'])
  self.reject(lambda r:r['records'][1]['source_reported'].__setitem__('named_npc',True))
  self.reject(lambda r:r['boundaries'].__setitem__('hero_min_level_or_rebirth',120))
 def test_both_roles_reward_does_not_prove_equal_or_named_reward_set(self):
  self.assertEqual(self.r['records'][0]['source_reported']['flow'][-1],'BOTH_ROLES_REPORTED_TO_RECEIVE_REWARDS')
  self.reject(lambda r:r['records'][0]['source_reported'].__setitem__('rewards','BOTH_GET_SPEAR'))
  self.reject(lambda r:r['boundaries'].__setitem__('all_quests_reward_spear',True))
 def test_generic_token_and_image_token_do_not_become_canonical_alias(self):
  self.assertEqual(self.r['records'][3]['source_reported']['label'],'精靈信物');self.assertEqual(self.r['records'][9]['source_reported']['label'],'精靈勇者信物')
  self.reject(lambda r:r['records'][9]['source_reported'].__setitem__('alias_of_prose_token_verified',True))
 def test_ancient_gu_is_a_mission_label_without_spawn_or_dialogue(self):
  x=self.r['manual_image_observations'][1];self.assertEqual(x['mission_target_label'],'古瓜');self.assertIsNone(x['npc_spawn_or_id'])
  self.reject(lambda r:r['boundaries'].__setitem__('ancient_gu_label_proves_spawn_or_dialogue',True))
 def test_two_visible_countdowns_are_not_a_single_continuous_run_or_initial_duration(self):
  self.assertEqual(self.r['manual_image_observations'][1]['remaining_time_display'],{'hours':6,'minutes':33})
  self.assertEqual(self.r['manual_image_observations'][2]['remaining_time_visible_hours'],0)
  for k in ['figure2_timer_is_initial_duration','three_images_same_character_continuous_run']:
   self.reject(lambda r:r['boundaries'].__setitem__(k,True))
 def test_spear_panel_stats_are_local_observation_not_formula_or_quest_level(self):
  p=self.r['manual_image_observations'][2]['item_panel'];self.assertEqual((p['attack_modifier'],p['agility_modifier']),(85,-18));self.assertEqual((p['spell_label'],p['spell_level']),('毒霧的精靈',6))
  self.reject(lambda r:r['records'][8]['source_reported']['panel'].__setitem__('agility_modifier',18))
  self.reject(lambda r:r['boundaries'].__setitem__('spear_spell_level_is_quest_requirement',True))
 def test_money_display_and_completion_prompt_are_not_actual_transaction(self):
  self.assertEqual(self.r['manual_image_observations'][2]['money_display'],8198620)
  self.reject(lambda r:r['manual_image_observations'][2].__setitem__('money_is_reward',True))
  self.reject(lambda r:r['boundaries'].__setitem__('quest_completion_or_reward_transaction_verified',True))
 def test_actual_eight_semantic_source_mutations_rejected(self):
  a=json.loads((REPORT.parent/'STONEAGE-TW75-SPIRIT-SUMMON-PREVIEW-NEGATIVE-AUDIT-R1.json').read_text());self.assertEqual(len(a['cases']),8)
  self.assertTrue(all(x['semantic_extract_rejected'] and x['original_sha256']==self.r['inputs'][1]['sha256'] and x['original_sha256']!=x['mutated_sha256'] for x in a['cases']))
  for f in [extract_body,extract_index]:
   with self.assertRaises((ValueError,StopIteration)):f(b'<html>No source</html>')
  with self.assertRaises(ValueError):replay(self.r,[b'']*4)
 def test_spirit_demon_and_later_region_worldlines_are_not_merged(self):
  for k in ['spirit_is_named_spirit_king','demon_invasion_is_cross_region_canon','summon_is_player_pet_summoning','original_server_execution_verified']:
   self.reject(lambda r:r['boundaries'].__setitem__(k,True))
 def test_downloaded_two_ci_reports_have_durable_exact_source_custody(self):
  from hashlib import sha256,sha1
  c=json.loads((REPORT.parent/'STONEAGE-TW75-SPIRIT-SUMMON-PREVIEW-CUSTODY-R1.json').read_text())
  self.assertEqual([len(c['runs'][k]) for k in ['candidate','main']],[10,11])
  for rows in c['runs'].values():self.assertTrue(all(x['head_sha']==c['content_head'] and x['conclusion']=='success' for x in rows))
  for pin in c['pins']:
   b=(REPORT.parents[2]/pin['path']).read_bytes();self.assertEqual(len(b),pin['bytes']);self.assertEqual(sha256(b).hexdigest(),pin['sha256']);self.assertEqual(sha1(b'blob '+str(len(b)).encode()+bytes([0])+b).hexdigest(),pin['git_blob'])
  payloads=[]
  for a in c['artifacts']:
   b=(REPORT.parents[2]/a['derived_path']).read_bytes();self.assertEqual(len(b),a['member_bytes']);self.assertEqual(sha256(b).hexdigest(),a['member_sha256']);payloads.append(b)
   r=json.loads(b);self.assertEqual(r['extracted'],self.r['extracted']);self.assertEqual(r['manual_image_observations'],self.r['manual_image_observations']);self.assertEqual(r['inputs'],[dict(id=x['id'],bytes=x['bytes'],sha256=x['sha256']) for x in self.r['inputs']])
  self.assertEqual(payloads[0],payloads[1]);self.assertTrue(c['candidate_and_main_and_local_raw_json_equal']);self.assertFalse(c['original_server_execution_verified']);self.assertFalse(c['raw_sources_committed'])
if __name__=='__main__':unittest.main()
