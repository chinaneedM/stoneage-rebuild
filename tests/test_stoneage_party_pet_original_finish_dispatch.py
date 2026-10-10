"""Source preservation and non-promotion for original Finish diagnostic."""
import unittest
from unittest.mock import patch
from tools.stoneage_party_pet_original_finish_dispatch_audit import (
    finish_observations,finish_native,FINISH_OBSERVATION,
)
from tools.stoneage_party_pet_original_lethal_loop_audit import LETHAL_ROUND_OBSERVATIONS

class OriginalFinishDispatchTests(unittest.TestCase):
 def test_next_original_loop_and_independent_release_oracle(self):
  for token in ("BATTLE_Loop();","BATTLE_MODE_FINISH","BATTLE_MODE_NONE",
     "Total_BattleNum==final_total-1","REAL_HEADER_FINISH_DISPATCH|"):
   self.assertIn(token,FINISH_OBSERVATION)
 def test_prior_lethal_observation_untouched(self):
  self.assertEqual(LETHAL_ROUND_OBSERVATIONS.count("REAL_HEADER_LETHAL_LOOP|"),1)
  for profile,sentinel in (("gavin","0"),("bismarck","-1")):
   script=finish_observations(profile)
   self.assertIn("final_winner=="+sentinel,script)
   self.assertIn("ORIGINAL_FINISH_NEXT_LOOP|",script)
 def test_original_finish_body_preserved(self):
  for profile,entry in (("gavin","charaindex"),("bismarck","char_index")):
   old=LETHAL_ROUND_OBSERVATIONS.replace("EXPECTED_WIN_SIDE","-1" if profile=="bismarck" else "0").replace("ENTRY_FIELD",entry)
   b="static int BATTLE_Finish(int b){return BATTLE_GetProfit(b,0,0);}"
   p="int BATTLE_GetProfit(int b,int s,int n){return BATTLE_GetExpGold(b,s,n);}"
   e="int BATTLE_GetExpGold(int b,int s,int n){return 0;}"
   with patch("tools.stoneage_party_pet_original_finish_dispatch_audit.lethal.lethal_round_native",return_value=("prefix"+old+"int main(int argc,char **argv){",False)),patch("tools.stoneage_party_pet_original_finish_dispatch_audit.attack.definition",side_effect=lambda src,name:{"BATTLE_Finish":b,"BATTLE_GetProfit":p,"BATTLE_GetExpGold":e}[name] if src=="original" else (_ for _ in ()).throw(ValueError("missing"))):
    code,_=finish_native(profile,"","original","","")
   for body in (b,p,e):self.assertIn(body,code)
   self.assertIn("ORIGINAL_FINISH_NEXT_LOOP|",code)
 def test_missing_lethal_anchor_fail_closed(self):
  with patch("tools.stoneage_party_pet_original_finish_dispatch_audit.lethal.lethal_round_native",return_value=("invalid",False)):
   with self.assertRaisesRegex(ValueError,"drift"):
    finish_native("gavin","","","","")
if __name__=="__main__":unittest.main()
