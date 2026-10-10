"""Original command-wait admission and source preservation drift tests."""
import unittest
from unittest.mock import patch
from tools.stoneage_party_pet_command_wait_audit import (
    ACTUAL_NAMES,NEW_UNREACHED,WAIT_OBSERVATIONS,EXIT_ANCHOR,extend_native,has_function_body,
)
class CommandWaitTests(unittest.TestCase):
 def test_nested_call_is_not_a_definition(self):
  self.assertFalse(has_function_body('if(BATTLE_OnlyRescue(battleindex,0,&flag)==0){abort();}', 'BATTLE_OnlyRescue'))
  self.assertFalse(has_function_body('int BATTLE_OnlyRescue(int,int,int *);', 'BATTLE_OnlyRescue'))
  self.assertTrue(has_function_body('int BATTLE_OnlyRescue(int i,int s,int *p){abort();return 0;}', 'BATTLE_OnlyRescue'))
 def test_private_static_body_is_detected(self):
  self.assertTrue(has_function_body('static int BATTLE_Battling(int i)\n{abort();return 0;}', 'BATTLE_Battling'))
 def test_timeout_equality_and_complete_state_oracles(self):
  self.assertIn('waiting_offsets[3]={0,BATTLE_TIME_LIMIT-1,BATTLE_TIME_LIMIT}',WAIT_OBSERVATIONS)
  self.assertIn('memcmp(&expected_waiting_arena,battle,sizeof(expected_waiting_arena))',WAIT_OBSERVATIONS)
  self.assertIn('SOURCE_PROFILE_WAIT_DELTA',WAIT_OBSERVATIONS)
  self.assertIn('controlled initial PartTime zero',WAIT_OBSERVATIONS)
  self.assertIn('memcmp(&waiting_actors[actor],&slots[actor],sizeof(Char))',WAIT_OBSERVATIONS)
  self.assertIn('NowTime.tv_sec=waiting_clock',WAIT_OBSERVATIONS)
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
