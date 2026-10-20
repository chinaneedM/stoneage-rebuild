import copy,json,unittest
from tools.stoneage_jp2008_tiger_quest_source import *
class TigerQuestSource(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=json.loads(REPORT.read_text())
 def reject(self,k,v):
  r=copy.deepcopy(self.r);r['boundaries'][k]=v
  with self.assertRaises(ValueError):validate(r)
 def test_ten_named_content_records_follow_archive_contract_without_original_ids(self):
  validate(self.r);self.assertEqual(len(self.r['records']),10);c=json.loads((REPORT.parent/'STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json').read_text())['future_website']
  for row in self.r['records']:
   self.assertTrue(set(c['record_contract']['required'])<=row.keys());self.assertIn(row['collection'],c['required_collections']);self.assertIsNone(row['game_ids'])
 def test_june_announcement_september_official_capture_and_current_media_separate(self):
  self.assertEqual(facts()['announcement']['announced_update_date'],'2008-06-24');self.assertEqual(self.r['inputs'][1]['capture_timestamp'],'20080929194642')
  for k in ['announced_date_is_verified_rollout','official_september_capture_is_june_launch_bytes','current_media_images_are_2008_captured_bytes']:self.reject(k,True)
 def test_seven_poem_chapters_not_seven_quest_stages_or_full_poem(self):
  self.assertEqual(facts()['named_content']['poem_reported_chapters'],7);self.assertIsNone(facts()['poem_context']['quest_chapter_count'])
  for k in ['seven_poem_chapters_are_seven_quest_chapters','full_seven_chapter_poem_recovered']:self.reject(k,True)
 def test_three_tigers_not_species_roster_or_capture_probability(self):
  self.assertEqual(facts()['named_content']['mountain_reported_resident_tigers'],3)
  self.reject('three_tigers_are_three_species_or_complete_roster',True);self.reject('capture_steps_or_probability',1.0)
 def test_poem_circulation_on_geel_not_proven_mountain_coordinates(self):
  self.assertEqual(facts()['poem_context']['place_of_recirculation'],'ギール島');self.reject('mountain_is_proven_on_geel_island',True);self.reject('original_map_coordinates',[100,100])
 def test_story_incident_and_unknown_arrival_not_invented_worldline_entity(self):
  self.assertEqual(facts()['world_story']['incident_label'],'ニースの異変');self.assertIsNone(facts()['world_story']['arrival_identity']);self.reject('mysterious_arrival_named_or_caused_by_known_entity',True);self.reject('nisu_incident_identified_or_dated',True)
 def test_enigma_water_weapon_armor_not_actual_reward_table(self):
  self.assertEqual(len(facts()['official_enigma']['motifs']),4)
  for k in ['riddle_motifs_are_verified_quest_rewards','pure_water_is_verified_item_name_or_pet']:self.reject(k,True)
  self.reject('weapon_armor_names_stats_or_reward_chances',{'name':'tiger_sword','attack':100})
 def test_six_original_image_failures_do_not_substitute_media_pixels(self):
  self.assertEqual(len(self.r['official_image_attempts']),6);self.assertTrue(all(x['status']==404 for x in self.r['official_image_attempts']))
  self.reject('six_official_image_404s_prove_global_absence',True);self.reject('media_images_substitute_for_missing_official_gif_bytes',True)
 def test_four_scene_observations_do_not_identify_npcs_or_prove_capture(self):
  self.assertEqual(len(observations()),4)
  for k in ['image_party_count_is_party_capacity','image_figures_have_verified_npc_or_pet_identity','screenshot_is_successful_capture_or_reward_delivery','image_is_native_client_resolution']:self.reject(k,True)
 def test_official_disclaimers_and_unknowns_preserved(self):
  self.assertTrue(facts()['official_disclaimers']['images_are_illustrative_may_differ']);self.assertTrue(facts()['official_disclaimers']['future_balance_may_change_content']);self.reject('entry_level_or_prerequisite',80);self.reject('script_dialogue_branch_or_save_flags',{'done':True})
 def test_thirteen_actual_document_mutations_two_wrapper_positive_and_partial_rejection(self):
  a=json.loads(REPORT.with_name('STONEAGE-JP2008-TIGER-QUEST-NEGATIVE-AUDIT-R1.json').read_text());self.assertEqual(len(a['cases']),13);self.assertEqual(len(a['positive_cases']),2);self.assertTrue(a['full_byte_pin_bypassed_for_semantic_check']);self.assertTrue(all(x['semantic_extract_rejected'] and x['original_sha256']!=x['mutated_sha256'] for x in a['cases']))
  for f in [extract_media,extract_official]:
   with self.assertRaises(ValueError):f(b'<html>Partial</html>')
  with self.assertRaises(ValueError):replay(self.r,[b'']*5)
 def test_missing_original_image_alt_and_dimensions_are_declared_metadata_only(self):
  m=json.loads(REPORT.with_name('STONEAGE-JP2008-TIGER-QUEST-IMAGE-LINK-METADATA-R1.json').read_text());validate_link_metadata(m,self.r)
  self.assertEqual([x['alt_as_written'] for x in m['rows']],[None,'uta_osa','tora_in','tora_map1','tora_map2','tora_map3']);self.assertEqual([x['declared_width'] for x in m['rows']],[None,250,250,150,150,150])
  for key in ['declared_dimensions_are_actual_pixel_measurements','alt_labels_are_original_entity_names','missing_images_recovered']:
   changed=copy.deepcopy(m);changed[key]=True
   with self.assertRaises(ValueError):validate_link_metadata(changed,self.r)
 def test_downloaded_dual_ci_reports_and_five_permanent_native_blob_pins(self):
  from hashlib import sha1
  c=json.loads(REPORT.with_name('STONEAGE-JP2008-TIGER-QUEST-CUSTODY-R1.json').read_text());self.assertEqual([len(c['runs'][k]) for k in ['candidate','main']],[10,11]);self.assertEqual(len(c['pins']),5)
  for rows in c['runs'].values():self.assertTrue(all(x['conclusion']=='success' and x['head_sha']==c['content_head'] for x in rows))
  for pin in c['pins']:
   b=(ROOT/pin['path']).read_bytes();self.assertEqual(len(b),pin['bytes']);self.assertEqual(sha256(b).hexdigest(),pin['sha256']);self.assertEqual(sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),pin['git_blob'])
  bs=[]
  for a in c['artifacts']:
   self.assertEqual(a['head_sha'],c['content_head']);self.assertIn(a['run_id'],[x['id'] for x in c['runs'][a['branch']]]);b=(ROOT/a['derived_path']).read_bytes();bs.append(b);self.assertEqual(len(b),a['member_bytes']);self.assertEqual(sha256(b).hexdigest(),a['member_sha256']);r=json.loads(b);self.assertEqual(r['extracted'],self.r['extracted']);self.assertEqual(r['manual_image_observations'],observations());self.assertFalse(r['full_seven_chapter_poem_recovered']);self.assertFalse(r['quest_rewards_verified']);self.assertEqual(r['official_gif_bytes_obtained'],0)
  self.assertEqual(bs[0],bs[1]);self.assertTrue(c['candidate_main_and_local_raw_json_equal']);self.assertFalse(c['original_server_execution_verified']);self.assertTrue(c['link_metadata_supplement_added_after_content_ci']);self.assertFalse(c['raw_sources_committed'])
if __name__=='__main__':unittest.main()
