"""Original physical-body preservation and strict native attack boundaries."""
import unittest
from types import SimpleNamespace
from unittest.mock import patch
from tools.stoneage_party_pet_original_attack_audit import attack_native,attack_originals,ATTACK_OBSERVATIONS,ATTACK_SETUP,ROUND_OBSERVATIONS,definition
from tools.stoneage_enemy_entry_exit_audit import compile_probe
BODIES={'BATTLE_Attack':'int BATTLE_Attack(int b,int a,int d){return BATTLE_DamageSub(a,d,0,0,0);}', 'BATTLE_DamageSub':'int BATTLE_DamageSub(int a,int d,int*x,int*y,int*z){return 0;}'}
EVENT='float gKawashiPara=0.02;\nfloat gCriticalPara=0.09;\nfloat gCounterPara=0.08;\nchar *aszStatus[]={"all"};\nint BATTLE_CounterCheckPlayer(int a,int b,int*p){return 0;}\nint BATTLE_CounterCheckPet(int a,int b,int*p){return 0;}\nint BATTLE_ItemCrush(int a,int b,int c,int d){return 0;}'
BASE='int main(int argc,char **argv){'+ROUND_OBSERVATIONS+'return 0;}'
class AttackTests(unittest.TestCase):
 def build(self,event=EVENT,base=BASE):
  with patch('tools.stoneage_party_pet_original_attack_audit.round_native',return_value=(base,False)),patch('tools.stoneage_party_pet_original_attack_audit.attack_originals',return_value=dict(BODIES)),patch('tools.stoneage_party_pet_original_attack_audit.pp_file',return_value='void *CHAR_getFunctionPointer(int a,int b){return 0;}'):
   return attack_native('gavin','', '',event,'/tmp')[0]
 def test_complete_original_physical_bodies_preserved(self):
  native=self.build()
  for n,b in BODIES.items():self.assertEqual(definition(native,n),b)
  self.assertIn('float gCriticalPara=0.09;',native)
 def test_original_physical_global_drift_rejected(self):
  with self.assertRaises(ValueError):self.build(event=EVENT.replace('gCriticalPara','WRONG_GLOBAL'))
 def test_accepted_guard_anchor_required(self):
  with self.assertRaises(ValueError):self.build(base=BASE.replace(ROUND_OBSERVATIONS,''))
 def test_guard_and_attack_coexist_before_original_exit(self):
  native=self.build();self.assertIn(ROUND_OBSERVATIONS,native);self.assertIn(ATTACK_OBSERVATIONS.replace("ENTRY_FIELD","charaindex"),native)
  self.assertIn('BATTLE_Index2No(battle_at,enemy_actor)',ATTACK_SETUP)
  self.assertIn('BATTLE_No2Index(battle_at,enemy_no)==enemy_actor',ATTACK_SETUP)
 def test_full_effect_oracles_and_nonterminal_boundary(self):
  for s in ('memcmp(expected_round,slots,sizeof expected_round)','memcmp(&expected_round_arena,battle,sizeof(BATTLE))','CHAR_DAMAGECOUNT','CHAR_ISATTACKED','BATTLE_Loop()==1','attack_round=1','damage_executed=1','next_wait=1'):
   self.assertIn(s,ATTACK_OBSERVATIONS)
 def test_math_linkage_is_opt_in_and_follows_source(self):
  for libraries in ((),('-lm',)):
   with patch('tools.stoneage_enemy_entry_exit_audit.trap_definitions',return_value=''),patch('tools.stoneage_enemy_entry_exit_audit.include_args',return_value=[]),patch('tools.stoneage_enemy_entry_exit_audit.subprocess.run',return_value=SimpleNamespace(returncode=0,stderr='')) as run:
    compile_probe('gavin','/tmp','', '/tmp/probe','-O0',link_libraries=libraries)
    args=run.call_args.args[0]
    self.assertEqual('-lm' in args,bool(libraries))
    if libraries:self.assertGreater(args.index('-lm'),args.index('-'))
 def test_bismarck_uses_its_original_magic_attribute_body(self):
  body='int BATTLE_AttrCalc(int a){return a;}'
  with patch('tools.stoneage_party_pet_original_attack_audit.ATTACK_NAMES',('BATTLE_ArrangeCheck','BATTLE_AttrCalc')),patch('tools.stoneage_party_pet_original_attack_audit.pp_file',return_value=body) as pp:
   self.assertEqual(attack_originals('bismarck','','','/tmp'),{'BATTLE_AttrCalc':body})
   self.assertTrue(str(pp.call_args.args[2]).endswith('battle/battle_magic.c'))
   with self.assertRaises(ValueError):attack_originals('bismarck','','int BATTLE_ArrangeCheck(int a){return 0;}','/tmp')
if __name__=='__main__':unittest.main()
