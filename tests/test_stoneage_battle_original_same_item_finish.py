import unittest
from tools import stoneage_battle_original_same_item_finish_audit as target

class OriginalSameItemFinish(unittest.TestCase):
    def test_actual_source_finish_contract(self):
        for p in ("gavin","bismarck"):
            c=target.second_controls(p)
            for term in ("BATTLE_Loop()","BATTLE_MODE_FINISH",
                         "Total_BattleNum=1","Total_BattleNum==0",
                         "arena->use==0","ITEM_COUNT==baseline_count",
                         "memcmp(baseline_items,reward_items","memcmp(baseline_actors,slots",
                         "REAL_HEADER_SAME_ITEM_FINISH|","indexOfExistItems[first_empty]=3"):
                if term=="ITEM_COUNT==baseline_count":term="==baseline_count"
                self.assertIn(term,c,term)
            self.assertNotIn("ENTRY_FIELD",c)
            self.assertNotIn("WIN_SIDE",c)
    def test_no_gameplay_function_reimplementation(self):
        self.assertIsNotNone(target.payout.payout_native)
