import unittest
from unittest.mock import patch
from tools.stoneage_party_pet_loop_dispatch_audit import DIRECT_INIT,LOOP_INIT,UNREACHED,code
class LoopInitTests(unittest.TestCase):
 def test_original_dispatch(self):
  self.assertIn("BATTLE_Init(battle_at)",DIRECT_INIT)
  self.assertIn("BATTLE_Loop()==1",LOOP_INIT)
  self.assertIn("BATTLE_Command",UNREACHED)
  self.assertIn("BATTLE_Finish",UNREACHED)
 def test_prior_drift_guard(self):
  with patch("tools.stoneage_party_pet_loop_dispatch_audit.init_native",return_value=("changed",False)):
   with self.assertRaises(ValueError):code("gavin","", "", "")
if __name__=="__main__":unittest.main()
