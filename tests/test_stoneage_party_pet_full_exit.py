import unittest
from tools.stoneage_party_pet_full_exit_audit import EXPECTED_INSERT, MARKER, make_native
class PartyPetExitTests(unittest.TestCase):
 def test_ownership_and_paired_pet_slot(self):
  for check in ("BATTLE_Exit(0,battle_at)", "BATTLE_Exit(1,battle_at)",
                "Entry[5].ENTRY_FIELD==-1","BATTLE_ExitAll(battle_at)",
                "BATTLE_DeleteBattle(battle_at)","CHAR_WORKBATTLEMODE",
                "CHAR_DEFAULTPET", "searchObjectFromCharaIndex"):
   self.assertIn(check,EXPECTED_INSERT)
 def test_no_profit_overclaim(self):
  self.assertIn("REAL_HEADER_EXIT",EXPECTED_INSERT)
  self.assertNotIn("BATTLE_GetProfit",EXPECTED_INSERT)
 def test_original_admission_drift_guard(self):
  from unittest.mock import patch
  with patch("tools.stoneage_party_pet_full_exit_audit.admission_native",return_value="missing accepted marker"):
   with self.assertRaises(ValueError):make_native("gavin","placeholder")
 def test_exact_marker(self):self.assertIn("Exit is intentionally not asserted",MARKER)
if __name__=="__main__":unittest.main()
