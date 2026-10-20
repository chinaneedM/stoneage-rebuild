import copy,json,unittest
from tools.stoneage_tw2004_mage_attribute_plan import *
class MageAttributePlan(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=json.loads(REPORT.read_text())
 def reject(self,fn):
  r=copy.deepcopy(self.r);fn(r)
  with self.assertRaises(ValueError):validate(r)
 def test_eight_archive_records_without_game_ids(self):
  validate(self.r);c=json.loads((REPORT.parent/'STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json').read_text())['future_website'];self.assertEqual(len(self.r['records']),8)
  for row in self.r['records']:
   self.assertTrue(set(c['record_contract']['required'])<=row.keys());self.assertIn(row['collection'],c['required_collections']);self.assertIsNone(row['game_ids'])
 def test_index_date_template_title_and_unnumbered_version_are_distinct(self):
  self.assertEqual(self.r['extracted'][0]['selected']['index_date_as_written'],'2004-4-5')
  for k,v in [('version_number','7.5'),('page_template_title_is_article_title',True),('index_date_is_deployment',True)]:self.reject(lambda r:r['boundaries'].__setitem__(k,v))
 def test_four_physical_three_magic_elements_and_separate_fire(self):
  f=facts();self.assertEqual(len(f['diagnosis']['character_elements']),4);self.assertEqual(len(f['diagnosis']['mage_attack_elements']),3)
  self.reject(lambda r:r['boundaries'].__setitem__('physical_fire_equals_magic_fire',True))
 def test_reported_bug_not_verified_rng_or_species_identity(self):
  self.reject(lambda r:r['boundaries'].__setitem__('bug_randomness_is_verified_probability_distribution',True))
  self.reject(lambda r:r['boundaries'].__setitem__('gold_flying_alias_is_original_species_id',True))
 def test_proposed_default_split_not_unconditional_damage_engine(self):
  for k,v in [('mage_damage_is_unconditionally_half_to_each',True),('exact_damage_formula','damage/2'),('proposal_is_deployed_patch',True)]:self.reject(lambda r:r['boundaries'].__setitem__(k,v))
 def test_directional_examples_preserve_opposite_subjects(self):
  rows=facts()['directional_examples']['examples'];self.assertEqual([(x['spirit'],x['from_subject'],x['to_subject']) for x in rows],[('地的精靈','RIDER','MOUNT'),('風的精靈','MOUNT','RIDER')])
  self.reject(lambda r:r['records'][4]['source_reported']['examples'][0].__setitem__('to_subject','RIDER'))
 def test_same_elements_not_same_species_or_stats(self):
  self.assertEqual(facts()['equality_condition']['condition'],'CHARACTER_ELEMENTS_EXACTLY_MATCH_MOUNT_ELEMENTS')
  self.reject(lambda r:r['boundaries'].__setitem__('attribute_equality_is_stat_or_species_equality',True))
 def test_two_planned_unnamed_wines_not_actual_quest_rewards(self):
  self.assertEqual(facts()['wine_plan']['planned_new_wines'],2)
  for k,v in [('wines_have_verified_names',True),('wine_attribute_directions_or_amounts',[-1,1]),('quest_script_dialogue_or_reward_flags_verified',True)]:self.reject(lambda r:r['boundaries'].__setitem__(k,v))
 def test_image_capture_2015_thumbnail_and_2004_full_size_not_one_build(self):
  self.assertEqual([x['capture_timestamp'] for x in self.r['inputs']][2:],['20150408182032','20040408015726'])
  self.reject(lambda r:r['inputs'][2].__setitem__('capture_timestamp','20040408015726'))
  for k in ['thumbnail_2015_bytes_are_contemporary_2004','pictured_mount_is_identified_as_金飛','pictured_character_is_identified_quest_npc','pictured_chat_is_quest_dialogue']:self.reject(lambda r:r['boundaries'].__setitem__(k,True))
 def test_eleven_real_body_mutations_reject_without_byte_pin(self):
  a=json.loads(REPORT.with_name('STONEAGE-TW2004-MAGE-ATTRIBUTE-PLAN-NEGATIVE-AUDIT-R1.json').read_text());self.assertEqual(len(a['cases']),11);self.assertTrue(a['byte_pin_bypassed_to_test_semantic_extractor']);self.assertTrue(all(x['semantic_extract_rejected'] and x['original_sha256']!=x['mutated_sha256'] for x in a['cases']))
  for f in [extract_index,extract_body]:
   with self.assertRaises((ValueError,StopIteration)):f(b'<html>Partial</html>')
  with self.assertRaises(ValueError):replay(self.r,[b'']*3)
if __name__=='__main__':unittest.main()
