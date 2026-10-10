"""Fail-closed mutation of accepted native ordinary attack observations."""
import unittest
from unittest.mock import patch
from tools.stoneage_party_pet_original_attack_audit import ATTACK_OBSERVATIONS
from tools.stoneage_party_pet_original_lethal_loop_audit import (
    LETHAL_ROUND_OBSERVATIONS, observed_lethal_round, lethal_round_native,
)

class LethalLoopTests(unittest.TestCase):
 def test_lethal_input_and_original_full_loop(self):
  for token in ("CHAR_HP]=60","BATTLE_Loop()","LETHAL_LOOP_MODE|",
      "original full-loop lethal HP floor", "REAL_HEADER_LETHAL_LOOP|"):
   self.assertIn(token,LETHAL_ROUND_OBSERVATIONS)
  self.assertNotIn("slots[enemy_actor].data[CHAR_HP]=500;",LETHAL_ROUND_OBSERVATIONS)
 def test_mutation_protects_existing_driver(self):
  self.assertIn("CHAR_HP]=500;",ATTACK_OBSERVATIONS)
  self.assertEqual(LETHAL_ROUND_OBSERVATIONS,observed_lethal_round())
 def test_both_profile_source_injection(self):
  for profile,entry in (("gavin","charaindex"),("bismarck","char_index")):
   accepted=ATTACK_OBSERVATIONS.replace("ENTRY_FIELD",entry)
   with patch("tools.stoneage_party_pet_original_lethal_loop_audit.attack.attack_native",return_value=("prefix"+accepted+"suffix\nint main(int argc,char **argv){",False)),patch("tools.stoneage_party_pet_original_lethal_loop_audit.attack.pp_file",return_value="int CHAR_setMaxExp(int x,unsigned long y){return y;}"):
    compiled,has_lua=lethal_round_native(profile,"","void Pet_Check_Die(int x){return;}\nint BATTLE_NormalDeadExtra(int b,int a,int c){return 0;}","","")
   self.assertIn(accepted,compiled)
   self.assertIn("REAL_HEADER_LETHAL_LOOP|",compiled)
   self.assertFalse(has_lua)
 def test_missing_anchor_rejected(self):
  with patch("tools.stoneage_party_pet_original_lethal_loop_audit.attack.attack_native",return_value=("invalid",False)):
   with self.assertRaisesRegex(ValueError,"drift"):
    lethal_round_native("gavin","","","","")

if __name__=="__main__":
 unittest.main()
