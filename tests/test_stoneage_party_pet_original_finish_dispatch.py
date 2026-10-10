import unittest
from unittest.mock import patch
from tools import stoneage_party_pet_original_finish_dispatch_audit as finish
from tools import stoneage_party_pet_original_lethal_loop_audit as lethal

class FinishTests(unittest.TestCase):
 def test_original_lethal_driver_is_unchanged(self):
  self.assertIn('memcpy(slots,round_baseline',lethal.LETHAL_ROUND_OBSERVATIONS)
 def test_terminal_state_is_not_resurrected(self):
  for profile in ('gavin','bismarck'):
   text=finish.finish_observations(profile)
   self.assertNotIn('memcpy(slots,round_baseline',text)
   self.assertNotIn('Total_BattleNum=final_total;',text)
   self.assertIn('whole seven actor terminal oracle',text)
   self.assertIn('whole arena terminal oracle',text)
 def test_exact_reward_and_profile_caps_remain_separate(self):
  g=finish.finish_observations('gavin');b=finish.finish_observations('bismarck')
  self.assertIn('"-2|0|1,,,,,|||"',g)
  self.assertIn('"-2|0|0,,,,,|||"',g)
  self.assertIn('"-2|0|4c92,,,,,|||"',b)
  self.assertIn('CHAR_WORKNOCAST]=0;',b)
  self.assertIn('CHAR_DOOMTIME]=0;',g)
  self.assertNotIn('EXPECTED_LEADER_EXP',g+b)
 def test_reward_owner_and_pool_counter_asserted(self):
  for p in ('gavin','bismarck'):
   t=finish.finish_observations(p)
   self.assertIn('final_total-1',t)
   self.assertIn('expected_finish[final_enemy].use=0',t)
   self.assertIn('finish_rs_count==2&&finish_status_count==1',t)
 def test_missing_restoration_anchor_fails_closed(self):
  with patch.object(lethal,'LETHAL_ROUND_OBSERVATIONS','wrong'):
   with self.assertRaisesRegex(ValueError,'drift'):finish.finish_observations('gavin')
 def test_independent_base62_literal(self):
  alphabet='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
  n=1000000;digits=''
  while n:n,r=divmod(n,62);digits=alphabet[r]+digits
  self.assertEqual(digits,'4c92')

if __name__=='__main__':unittest.main()
