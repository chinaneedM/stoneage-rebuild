"""Original command-wait admission and source preservation drift tests."""
import unittest
from unittest.mock import patch
from tools.stoneage_party_pet_command_wait_audit import (
    ACTUAL_NAMES,NEW_UNREACHED,WAIT_OBSERVATIONS,EXIT_ANCHOR,extend_native,
)
class CommandWaitTests(unittest.TestCase):
 def test_original_three_function_graph(self):
  self.assertEqual(ACTUAL_NAMES,("BATTLE_CommandWait","BATTLE_TimeOutCheck","BATTLE_Command"))
 def test_no_fake_action_or_profit(self):
  self.assertIn("BATTLE_Battling",NEW_UNREACHED)
  self.assertIn("BATTLE_ai_all",NEW_UNREACHED)
  self.assertIn("BATTLE_Loop()==1",WAIT_OBSERVATIONS)
  self.assertIn("battle->turn==previous_turn",WAIT_OBSERVATIONS)
  self.assertNotIn("BATTLE_GetProfit",WAIT_OBSERVATIONS)
 def test_all_actor_wait_and_ownership(self):
  for k in ("slots[0].workint[CHAR_WORKBATTLEMODE]", "slots[1].workint[CHAR_WORKBATTLEMODE]", "slots[2].workint[CHAR_WORKBATTLEMODE]", "CHAR_getCharPet(0,0)", "Battle_getTotalBattleNum()"):
   self.assertIn(k,WAIT_OBSERVATIONS)
 def test_existing_exit_boundary(self):
  self.assertIn("BATTLE_Exit(0,battle_at)",EXIT_ANCHOR)
 def test_drift_rejects_missing_previous_exit(self):
  with patch("tools.stoneage_party_pet_command_wait_audit.original_loop",return_value=("changed",False)):
   with self.assertRaises(ValueError):
    extend_native("gavin","","","","/")
if __name__=="__main__": unittest.main()
