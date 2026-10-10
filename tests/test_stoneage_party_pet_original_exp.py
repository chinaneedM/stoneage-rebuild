import hashlib
import unittest
from tools.stoneage_party_pet_original_exp_audit import validate_parts, exp_observations, getter_definition

class OriginalExpTests(unittest.TestCase):
 def setUp(self):
  self.decl='original whole declarations'
  self.bodies={'BATTLE_GetExp':'original whole exp body','getBattleexp':'active original getter'}
  self.frozen={'declarations_sha256':hashlib.sha256(self.decl.encode()).hexdigest(),'bodies':{n:hashlib.sha256(b.encode()).hexdigest() for n,b in self.bodies.items()}}
 def test_exact_source(self):
  self.assertEqual(validate_parts(self.decl,self.bodies,self.frozen),self.frozen)
 def test_changed_getter_rejected(self):
  bodies=dict(self.bodies,getBattleexp='inactive getter')
  with self.assertRaisesRegex(ValueError,'drift'):validate_parts(self.decl,bodies,self.frozen)
 def test_missing_exp_rejected(self):
  with self.assertRaisesRegex(ValueError,'drift'):validate_parts(self.decl,{'getBattleexp':self.bodies['getBattleexp']},self.frozen)
 def test_changed_level_table_rejected(self):
  with self.assertRaisesRegex(ValueError,'drift'):validate_parts(self.decl+'changed table',self.bodies,self.frozen)
 def test_added_gameplay_stub_rejected(self):
  with self.assertRaisesRegex(ValueError,'drift'):validate_parts(self.decl,dict(self.bodies,CHAR_LevelUpCheck='return 0;'),self.frozen)
 def test_original_unsigned_getter_signature_preserved(self):
  source='unsigned int getBattleexp(void) { return 1; }'
  self.assertEqual(getter_definition(source),source)
 def test_profiles_do_not_share_exp_oracle(self):
  g=exp_observations('gavin');b=exp_observations('bismarck')
  self.assertIn('config.battleexp=(case_id==8)?3:1;',g)
  self.assertNotIn('config.battleexp',b)
  self.assertIn('0:1000000',b)
  self.assertIn('(raw*bonus)/100',g)
  for text in (g,b):
   self.assertNotIn('PROFILE_EXPECTED',text)
   self.assertNotIn('SET_MULTIPLIER',text)
   self.assertIn('complete seven actor EXP write oracle',text)
   self.assertIn('BATTLE_GetExp(-1,0)',text)

if __name__=='__main__':unittest.main()
