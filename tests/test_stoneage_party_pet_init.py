import unittest
from unittest.mock import patch
from tools.stoneage_party_pet_init_audit import (
    ACTUAL_FUNCTIONS, OUTPUT_BOUNDARY, LUA_BOUNDARY,
    ENTRY_ANCHOR, INIT_OBSERVATIONS, make_native,
)
class OriginalInitTests(unittest.TestCase):
    def test_exact_source_function_list(self):
        self.assertEqual(len(ACTUAL_FUNCTIONS),8)
        self.assertIn("BATTLE_SurpriseCheck",ACTUAL_FUNCTIONS)
        self.assertIn("BATTLE_PreCommandSeq",ACTUAL_FUNCTIONS)
        self.assertIn("BATTLE_CharaBackUp",ACTUAL_FUNCTIONS)
        self.assertIn("BATTLE_Init",ACTUAL_FUNCTIONS)
    def test_typed_output_only_and_state_oracles(self):
        self.assertIn("BATTLE_CharSendAll",OUTPUT_BOUNDARY)
        self.assertIn("BATTLE_ActSettingSend",OUTPUT_BOUNDARY)
        self.assertIn("BattleStartFunction",LUA_BOUNDARY)
        for s in ("BATTLE_Init(battle_at)", "BATTLE_MODE_BATTLE",
                  "BATTLE_CHARMODE_C_WAIT","BATTLE_FLG_FREEDP",
                  "iEntryBack[1]","CHAR_getCharPet(0,0)"):
            self.assertIn(s,INIT_OBSERVATIONS)
        self.assertNotIn("BATTLE_GetProfit",INIT_OBSERVATIONS)
    def test_drift_unsafe_original_graph_blocked(self):
        with patch("tools.stoneage_party_pet_init_audit.make_reentry_native",return_value="changed"):
            with self.assertRaises(ValueError):
                make_native("gavin","", "", "")
    def test_lua_boundary_not_silently_ignored(self):
        self.assertIn("lua_start_calls++",LUA_BOUNDARY)
        self.assertIn("lua_boundary",INIT_OBSERVATIONS)
    def test_prior_original_exit_anchor(self):
        self.assertIn("BATTLE_Exit(0,battle_at)",ENTRY_ANCHOR)

if __name__=="__main__":
    unittest.main()
