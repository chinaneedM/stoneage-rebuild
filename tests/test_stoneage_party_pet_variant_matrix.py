"""Drift guards for the bounded real-header negative party/pet matrix."""
import unittest
from unittest.mock import patch

from tools.stoneage_party_pet_variant_matrix_audit import (
    SCENARIOS, PRECONDITIONS, OBSERVATIONS, ENTRY_RESET,
    DRIVER_START, DRIVER_END, native,
)

class PartyPetVariantTests(unittest.TestCase):
    def test_exact_noncollapsed_profile_matrix(self):
        self.assertEqual(len(SCENARIOS),8)
        self.assertEqual(len(set(SCENARIOS)),8)
        self.assertIn("scenario!=2||IS_BISMARCK",OBSERVATIONS)
        self.assertIn("BATTLE_CHARMODE_C_WAIT",PRECONDITIONS)
        self.assertIn("BATTLE_CHARMODE_FINAL",PRECONDITIONS)

    def test_dead_and_zero_hp_not_conflated(self):
        self.assertIn("slots[2].data[CHAR_HP]=0",PRECONDITIONS)
        self.assertIn("slots[2].flg[CHAR_ISDIE/8] |=",PRECONDITIONS)
        self.assertIn("slots[0].data[CHAR_DEFAULTPET]=-1",PRECONDITIONS)
        self.assertIn("slots[0].unionTable.indexOfPet[0]=-1",PRECONDITIONS)

    def test_actual_exit_and_complete_actor_state(self):
        for expr in (
            "BATTLE_Exit(0,battle_at)", "BATTLE_Exit(1,battle_at)",
            "BATTLE_ExitAll(battle_at)", "BATTLE_DeleteBattle(battle_at)",
            "slots[1].workint[CHAR_WORKGETEXP]", "slots[2].workint[CHAR_WORKGETEXP]",
            "slots[2].data[CHAR_HP]", "slots[0].data[CHAR_DEFAULTPET]",
            "searchObjectFromCharaIndex",
        ):
            self.assertIn(expr,OBSERVATIONS)
        self.assertNotIn("BATTLE_GetProfit",OBSERVATIONS)

    def test_one_shot_fixture_drift_guards(self):
        beginning='int array,mode;\n while(scanf("%d%d",&array,&mode)==2){'
        original="prefix\n"+ENTRY_RESET+"\n"+beginning+"\n"+DRIVER_START+"old assertions\n"+DRIVER_END+"\n"
        with patch("tools.stoneage_party_pet_variant_matrix_audit.make_reentry_native",return_value=original):
            a=native("gavin","test")
            b=native("bismarck","test")
        self.assertIn("int array,mode,scenario;",a)
        self.assertIn("charaindex",a)
        self.assertIn("char_index",b)
        self.assertIn("scenario!=2||0",a)
        self.assertIn("scenario!=2||1",b)
        self.assertNotIn("old assertions",a)
        with patch("tools.stoneage_party_pet_variant_matrix_audit.make_reentry_native",return_value="changed"):
            with self.assertRaises(ValueError):native("gavin","test")
        with patch("tools.stoneage_party_pet_variant_matrix_audit.make_reentry_native",return_value=original+ENTRY_RESET):
            with self.assertRaises(ValueError):native("gavin","test")

if __name__=="__main__":
    unittest.main()
