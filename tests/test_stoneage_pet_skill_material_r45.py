import copy
import hashlib
import json
import unittest
from tools.stoneage_pet_skill_material_r45 import (
 ROOT,REPORT,REPORT_SHA,CROSSWALK,replay,verify_custody,build_crosswalk,
 decimal_option_witness,parse_prior_pressure,model_crosswalk)

class SourceQualifiedSkillContract(unittest.TestCase):
 def setUp(self):self.d=json.loads((ROOT/REPORT).read_bytes())
 def rejected(self,change):
  d=copy.deepcopy(self.d);change(d)
  with self.assertRaises(ValueError):replay(d)
 def test_exact_source_and_crosswalk(self):
  self.assertTrue(verify_custody())
  self.assertEqual(hashlib.sha256((ROOT/REPORT).read_bytes()).hexdigest(),REPORT_SHA)
  self.assertEqual(replay(self.d)['selected_ids'],[0,1,2,3,10,11])
  self.assertEqual(build_crosswalk(),json.loads((ROOT/CROSSWALK).read_bytes()))
 def test_first_green_source_job_is_not_material_success(self):
  d=json.loads((ROOT/'research/recovered/STONEAGE-PRESERVED-PET-SKILL-SOURCE-ATTEMPT1-R45.json').read_bytes())
  self.assertEqual(len(d['receipt']['members']),2)
  self.assertEqual(d['status'],'ORIGINAL_MEMBERS_ACQUIRED_DERIVATION_PENDING')
  with self.assertRaises(ValueError):replay(d)
 def test_source_sha_and_independent_decode_guards(self):
  self.rejected(lambda d:d['receipt']['members'][0].update(sha256='0'*64))
  self.rejected(lambda d:d['receipt']['members'][0].update(independent_decoded_bytes_equal=False))
 def test_id_zero_not_dropped_as_empty(self):
  self.rejected(lambda d:d['material']['selected_rows'].pop(0))
 def test_name_relabel_or_simplification_rejected(self):
  self.rejected(lambda d:d['material']['selected_rows'][1]['name'].update(text_cp950_big5='攻击'))
 def test_extra_column_is_not_usetype_or_callback(self):
  self.rejected(lambda d:d['material'].update(trailing_field_equals_callback_rows=147))
 def test_config_alternative_drift_rejected(self):
  self.rejected(lambda d:d['material']['configured_skill_paths_as_written'].update(petskillfile2='./data/petskill1.txt'))
 def test_illegal_is_not_boolean(self):
  self.assertEqual(self.d['material']['selected_rows'][0]['numeric_fields']['ILLEGAL'],500)
  self.rejected(lambda d:d['material']['selected_rows'][0]['numeric_fields'].update(ILLEGAL=True))
 def test_cost_not_mp_or_learning_price(self):
  self.rejected(lambda d:d['material'].update(cost_is_mp_or_training_price_proven=True))
 def test_native_runtime_or_official_promotion_rejected(self):
  self.rejected(lambda d:d.update(original_server_executed=True))
  self.rejected(lambda d:d.update(official_tw10_skills_authenticated=6))
 def test_prose_or_full_table_payload_rejected(self):
  self.rejected(lambda d:d['material'].update(raw_option='synthetic prohibited raw payload'))
 def test_positive_enemy_stat_absence_does_not_erase_id0(self):
  c=build_crosswalk();zero=c['rows'][0]
  self.assertEqual(zero['original_skill_id'],0)
  self.assertIsNone(zero['prior_positive_enemy_reference'])
  self.assertTrue(zero['stable_common_reference_model_available'])
 def test_prior_id_callback_conflict_is_rejected(self):
  c=build_crosswalk();prior={1:{'declared_callback':'PETSKILL_NormalGuard'}}
  with self.assertRaises(ValueError):model_crosswalk(self.d['material']['selected_rows'],prior,set())
 def test_prior_duplicate_id_reference_rejected(self):
  line=b'RANK|rank=1|callback=PETSKILL_NormalAttack|ids=1|slot_uses=1|templates=1|status=closed_runtime\n'
  with self.assertRaises(ValueError):parse_prior_pressure(line+line)
 def test_option_witness_does_not_guess_unknown_payload(self):
  for raw in (b'x',b'12'):
   self.assertEqual(decimal_option_witness({'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})['kind'],'NOT_DECODED')
 def test_original_options_join_existing_command_and_round_models(self):
  from tools.stoneage_petskill_core_model import continuation_attack_command
  from tools.stoneage_petskill_round_bridge import bridge_stable_pet_skill_command
  from tools.stoneage_battle_round_model import BATTLE_COM_S_RENZOKU
  c=build_crosswalk();chosen={r['original_skill_id']:r for r in c['rows']}
  for skill_id,count in ((10,2),(11,3)):
   with self.subTest(skill=skill_id):
    witness=chosen[skill_id]['option_decimal_witness']
    self.assertEqual(witness['integer'],count)
    command=continuation_attack_command(target=10,option=str(witness['integer']),prior_high=0)
    submission=bridge_stable_pet_skill_command(command)
    self.assertEqual(submission.battle_command.command1,BATTLE_COM_S_RENZOKU)
    self.assertEqual(submission.battle_command.command3 & 65535,count)
  # All six COST fields happen to be2; OPTION witnesses remain independently2/3.
  self.assertEqual({r['numeric_fields']['COST'] for r in self.d['material']['selected_rows']},{2})

if __name__=='__main__':unittest.main()
