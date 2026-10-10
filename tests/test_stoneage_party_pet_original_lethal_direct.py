"""Direct lethal original physical path additive validation."""
import unittest
from unittest.mock import patch
from tools.stoneage_party_pet_original_attack_audit import ATTACK_OBSERVATIONS
from tools.stoneage_party_pet_original_lethal_direct_audit import (
    LETHAL_OBSERVATIONS,lethal_native,
)

class LethalDirectTests(unittest.TestCase):
 def test_fixed_lethal_fixture_not_finish_equivalence(self):
  for row in ('CHAR_HP]=60','BATTLE_Attack(battle_at,0,enemy_no)','CHAR_HP]==0',
              'before_count+1','Finish_executed=0','memcpy(slots,lethal_baseline'):
   self.assertIn(row,LETHAL_OBSERVATIONS)
 def test_existing_observations_preserved(self):
  native='prologue'+ATTACK_OBSERVATIONS.replace('ENTRY_FIELD','charaindex')+'epilogue'
  with patch('tools.stoneage_party_pet_original_lethal_direct_audit.attack.attack_native',return_value=(native,False)):
   out,lua=lethal_native('gavin','','','','')
  self.assertEqual(out.count(ATTACK_OBSERVATIONS.replace('ENTRY_FIELD','charaindex')),1)
  self.assertEqual(out.count('REAL_HEADER_LETHAL_DIRECT|'),1)
  self.assertFalse(lua)
 def test_missing_accepted_anchor_is_fail_closed(self):
  with patch('tools.stoneage_party_pet_original_lethal_direct_audit.attack.attack_native',return_value=('no accepted source',False)):
   with self.assertRaises(ValueError):lethal_native('bismarck','','','','')

if __name__=='__main__':unittest.main()
