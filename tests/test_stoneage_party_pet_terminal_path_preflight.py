"""Terminal source-only acceptance contracts: do not promote call reachability."""
import unittest

from tools.stoneage_party_pet_terminal_path_preflight import (
    NAMES, inspect_terminal,
)

FIXTURES = {
    "BATTLE_FinishSet": "int BATTLE_FinishSet(int battleindex){ BattleArray[battleindex].mode=BATTLE_MODE_FINISH; return 0;}",
    "BATTLE_Finish": """static int BATTLE_Finish(int battleindex) {
      if(BattleArray[battleindex].winside == 0 &&
         BattleArray[battleindex].WinFunc != NULL) BATTLE_GetProfit(battleindex,0,0);
      BATTLE_GetProfit(battleindex,0,0);
      BATTLE_Exit(0,battleindex);
      BATTLE_DeleteBattle(battleindex);
      return 0;
    }""",
    "BATTLE_GetProfit": "int BATTLE_GetProfit(int b,int s,int n) {if(b) return BATTLE_GetDuelPoint(b,s,n);return BATTLE_GetExpGold(b,s,n);}",
    "BATTLE_GetExpGold": "int BATTLE_GetExpGold(int b,int s,int n){BATTLE_GetExp(b,s,n); CHAR_LevelUpCheck(n);CHAR_PetLevelUp(n);return 0;}",
    "BATTLE_GetDuelPoint": "int BATTLE_GetDuelPoint(int b,int s,int n){return 0;}",
    "BATTLE_AddProfit": "int BATTLE_AddProfit(int b,int s,int n){return 0;}",
    "BATTLE_CountAlive": "int BATTLE_CountAlive(int b,int s){return 1;}",
    "BATTLE_getBattleDieIndex": "int BATTLE_getBattleDieIndex(int b,int s){return 0;}",
}

class TerminalPreflightTests(unittest.TestCase):
    def fixtures(self, profile="gavin"):
        d = FIXTURES.copy()
        if profile == "bismarck":
            d["BATTLE_Finish"] = d["BATTLE_Finish"].replace(".winside == 0", ".winside == -1")
        return d

    def test_source_routes_are_explicitly_not_runtime_closure(self):
        result = inspect_terminal("gavin", self.fixtures(), check_fingerprints=False)
        self.assertEqual(result["original_profile_winsidе_in_WinFunc_condition"], "0")
        self.assertIn("BATTLE_Exit", result["body_checks"]["BATTLE_Finish"]["named_call_inventory"])
        self.assertNotIn("BATTLE_Finish", result["body_checks"]["BATTLE_Finish"]["named_call_inventory"])

    def test_profile_specific_winfunc_sentinel(self):
        result = inspect_terminal("bismarck", self.fixtures("bismarck"), check_fingerprints=False)
        self.assertEqual(result["original_profile_winsidе_in_WinFunc_condition"], "-1")
        with self.assertRaisesRegex(ValueError, "sentinel"):
            inspect_terminal("gavin", self.fixtures("bismarck"), check_fingerprints=False)

    def test_missing_finisher_rejected(self):
        d = self.fixtures()
        del d["BATTLE_FinishSet"]
        with self.assertRaisesRegex(ValueError, "missing original terminal"):
            inspect_terminal("gavin", d, check_fingerprints=False)

    def test_no_prohibited_source_drift_promotion(self):
        with self.assertRaisesRegex(ValueError, "drift"):
            inspect_terminal("gavin", self.fixtures(), check_fingerprints=True)

    def test_reward_and_exit_paths_fail_closed(self):
        for key, token in (
            ("BATTLE_GetProfit", "BATTLE_GetDuelPoint"),
            ("BATTLE_Finish", "BATTLE_DeleteBattle"),
            ("BATTLE_GetExpGold", "CHAR_PetLevelUp"),
            ("BATTLE_FinishSet", "BATTLE_MODE_FINISH"),
        ):
            with self.subTest(key=key, token=token):
                d = self.fixtures()
                d[key] = d[key].replace(token, "MISSING_DEP")
                with self.assertRaises(ValueError):
                    inspect_terminal("gavin", d, check_fingerprints=False)

    def test_all_required_functions_versioned(self):
        self.assertEqual(len(NAMES), 8)


if __name__ == "__main__":
    unittest.main()
