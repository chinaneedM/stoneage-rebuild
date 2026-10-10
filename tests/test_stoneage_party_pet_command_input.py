"""Original parser preservation and complete bounded admission oracles."""
import unittest
from unittest.mock import patch
from tools.stoneage_party_pet_command_input_audit import (
 ACTUAL_NAMES,INPUT_OBSERVATIONS,input_native,definition,EXIT_ANCHOR,
)

COMMAND='''void BattleCommandDispach(int fd,char *s){BATTLE_ActSettingSend(fd);}
int checkErrorStatus(int c){return 0;}
int BATTLE_MpDown(int c,int n){return 0;}
BOOL BATTLE_PetDefaultCommand(int p){return 1;}'''
BASE='int main(int argc,char **argv){\n'+EXIT_ANCHOR+'\nreturn 0;}\n'
class CommandInputTests(unittest.TestCase):
 def build(self,profile='gavin',base=BASE,command=COMMAND):
  with patch('tools.stoneage_party_pet_command_input_audit.extend_native',return_value=(base,False)),patch('tools.stoneage_party_pet_command_input_audit.pp_file',side_effect=lambda profile,root,path: command if 'battle_command' in str(path) else 'int CHAR_CHECKCHARDATAINDEX(int i){return 1;} char *_CHAR_getChar(int i){return 0;} char *CHAR_getUseName(int i){return 0;}'):
   return input_native(profile,'','','','/tmp')[0]
 def test_full_original_parser_bodies_unchanged(self):
  native=self.build()
  for name in ACTUAL_NAMES:
   self.assertEqual(definition(native,name),definition(COMMAND,name))
 def test_source_profile_receive_and_partial_timer_delta(self):
  g=self.build('gavin');b=self.build('bismarck')
  self.assertIn('partial_expected.PartTime=1120;',g)
  self.assertNotIn('partial_expected.PartTime=1120;',b)
  self.assertIn('recv_count==before_recv+3',g)
  self.assertIn('recv_count==before_recv+0',b)
 def test_drift_missing_exit_blocked(self):
  with self.assertRaises(ValueError):self.build(base='int main(int argc,char **argv){}')
 def test_drift_missing_output_call_blocked(self):
  with self.assertRaises(ValueError):self.build(command=COMMAND.replace('BATTLE_ActSettingSend(fd);',''))
 def test_all_actor_and_arena_snapshots(self):
  self.assertIn('input_before[7]',INPUT_OBSERVATIONS)
  self.assertIn('memcmp(submitted_before,slots,sizeof submitted_before)',INPUT_OBSERVATIONS)
  self.assertIn('memcmp(&partial_expected,battle,sizeof(BATTLE))',INPUT_OBSERVATIONS)
 def test_malformed_and_pet_inputs_explicit(self):
  for packet in ('H|oops','H|14','W|FFFF'):
   self.assertIn(packet,INPUT_OBSERVATIONS)
  self.assertIn('BATTLE_PetDefaultCommand(-1)==FALSE',INPUT_OBSERVATIONS)
 def test_ready_predicate_is_not_round_claim(self):
  self.assertIn('BATTLE_CommandWait(battle_at,0)==TRUE',INPUT_OBSERVATIONS)
  self.assertIn('round_executed=0',INPUT_OBSERVATIONS)
  self.assertNotIn('BATTLE_Battling(',INPUT_OBSERVATIONS)
if __name__=='__main__':unittest.main()
