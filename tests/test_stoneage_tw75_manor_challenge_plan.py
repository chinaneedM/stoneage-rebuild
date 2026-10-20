import copy,json,unittest
from tools.stoneage_tw75_manor_challenge_plan import REPORT,validate,extract_body,extract_index,replay,compare_derived
class ManorChallengePlan(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=json.loads(REPORT.read_text())
 def reject(self,fn):
  r=copy.deepcopy(self.r);fn(r)
  with self.assertRaises(ValueError):validate(r)
 def test_thirteen_source_records_follow_archive_without_game_ids(self):
  validate(self.r);c=json.loads((REPORT.parent/'STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json').read_text())['future_website'];self.assertEqual(len(self.r['records']),13)
  for row in self.r['records']:
   self.assertTrue(set(c['record_contract']['required'])<=row.keys());self.assertIn(row['collection'],c['required_collections']);self.assertIsNone(row['game_ids'])
 def test_dated_plan_not_verified_patch_or_index_web_key_as_game_id(self):
  self.assertEqual(self.r['extracted'][0]['selected']['index_date_as_written'],'2004-6-17');self.assertEqual(self.r['inputs'][1]['capture_timestamp'],'20041206162649')
  self.reject(lambda r:r['boundaries'].__setitem__('proposal_is_verified_patch',True))
 def test_worked_example_1501_not_general_headcount_formula_or_five_points_per_day(self):
  x=self.r['records'][2]['source_reported'];self.assertEqual((x['reported_result'],x['arithmetic_result']),(1501,1501));self.assertTrue(x['arithmetic_check_only'])
  self.reject(lambda r:r['boundaries'].__setitem__('general_headcount_formula','N*N/10+1+R'))
  self.reject(lambda r:r['boundaries'].__setitem__('member_fame_is_five_per_day',True))
 def test_strict_ninety_percent_wording_and_equal_example_conflict_preserved(self):
  x=self.r['records'][3]['source_reported'];self.assertEqual((x['challenger_example'],x['owner_example']),(900,1000));self.assertEqual(x['example_ratio'],[9,10]);self.assertTrue(x['example_eligible']);self.assertIsNone(x['chosen_comparator'])
  self.reject(lambda r:r['records'][3]['source_reported'].__setitem__('chosen_comparator','>='))
  self.reject(lambda r:r['boundaries'].__setitem__('threshold_conflict_silently_repaired',True))
 def test_higher_challenger_replacement_not_fifo_or_tie_policy(self):
  x=self.r['records'][4]['source_reported'];self.assertTrue(x['existing_challenger_can_be_replaced']);self.assertIsNone(x['tie_policy'])
  self.reject(lambda r:r['records'][4]['source_reported'].__setitem__('tie_policy','EARLIEST_WINS'))
 def test_declaration_window_and_24_hours_not_22_oclock_plus_day(self):
  x=self.r['records'][5]['source_reported'];self.assertEqual(x['normalized_hours'],[18,22]);self.assertEqual(x['start_after_successful_declaration_hours'],24)
  self.reject(lambda r:r['boundaries'].__setitem__('replaced_challenger_resets_24h_timer',True))
  self.reject(lambda r:r['boundaries'].__setitem__('timezone','UTC+08'))
 def test_reset_is_both_families_accumulated_fame_not_lifetime_character_fame(self):
  x=self.r['records'][6]['source_reported'];self.assertEqual((x['subject'],x['value']),('BOTH_FAMILIES_ACCUMULATED_FAME',0))
  self.reject(lambda r:r['boundaries'].__setitem__('reset_is_all_character_lifetime_fame',True))
 def test_online_payout_coefficients_do_not_create_account_transactions(self):
  x=self.r['records'][7]['source_reported'];self.assertEqual((x['momentum_to_stone_multiplier'],x['stone_per_point']),(10000,5000));self.assertEqual(x['remainder'],'FAMILY_BANK')
  self.reject(lambda r:r['boundaries'].__setitem__('offline_payment_policy','ALL_OFFLINE_MEMBERS_GET_ZERO'))
  self.reject(lambda r:r['boundaries'].__setitem__('reward_uses_pre_or_post_reset_momentum','AFTER_RESET'))
 def test_four_day_ceasefire_then_day_five_and_six_not_weekly_or_exact_96_hours(self):
  x=self.r['records'][8]['source_reported'];self.assertEqual((x['ceasefire_days'],x['declaration_day_ordinal'],x['battle_day_ordinal']),(4,5,6))
  for k in ['cycle_is_weekly','ceasefire_is_exact_96hours']:self.reject(lambda r:r['boundaries'].__setitem__(k,True))
 def test_no_challenger_counts_as_defense_reward_not_invented_reset_or_challenger_prize(self):
  self.assertIsNone(self.r['records'][9]['source_reported']['reset_rule'])
  self.reject(lambda r:r['boundaries'].__setitem__('no_challenge_reset_rule','RESET_BOTH'))
  self.reject(lambda r:r['boundaries'].__setitem__('challenger_reward',10000))
 def test_crafting_cooking_fame_removal_is_not_crafting_function_removal(self):
  x=self.r['records'][10]['source_reported'];self.assertFalse(x['crafting_and_cooking_removed'])
  self.reject(lambda r:r['boundaries'].__setitem__('crafting_cooking_functions_removed',True))
 def test_old_rank_menu_labels_not_proof_of_deployed_retention_or_resolution(self):
  x=self.r['manual_image_observation'];self.assertEqual(x['selected_label'],'十大家族氣勢');self.assertIn('十大合成家族',x['other_visible_labels']);self.assertIn('十大料理家族',x['other_visible_labels'])
  self.reject(lambda r:r['boundaries'].__setitem__('image_old_ranking_entries_prove_deployed_retention',True))
  self.reject(lambda r:r['boundaries'].__setitem__('image_native_client_resolution_proven',True))
 def test_cn40_rank_limit_not_imported_to_taiwan75(self):
  x=compare_derived(self.r);self.assertEqual(x['cn40_challenge_rank_change'],[10,20]);self.assertFalse(x['cn40_top20_applies_to_tw75'])
  self.reject(lambda r:r['boundaries'].__setitem__('cn40_top20_rule_transferred_to_tw75',True))
  r=copy.deepcopy(self.r);r['derived_input']['git_blob']='0'*40
  with self.assertRaises(ValueError):compare_derived(r)
 def test_twelve_real_semantic_mutations_and_partial_source_rejection(self):
  a=json.loads((REPORT.parent/'STONEAGE-TW75-MANOR-CHALLENGE-PLAN-NEGATIVE-AUDIT-R1.json').read_text());self.assertEqual(len(a['cases']),12)
  self.assertTrue(all(x['semantic_extract_rejected'] and x['original_sha256']==self.r['inputs'][1]['sha256'] and x['original_sha256']!=x['mutated_sha256'] for x in a['cases']))
  for f in [extract_body,extract_index]:
   with self.assertRaises((ValueError,StopIteration)):f(b'<html>Not source</html>')
  with self.assertRaises(ValueError):replay(self.r,[b'']*2)
if __name__=='__main__':unittest.main()
