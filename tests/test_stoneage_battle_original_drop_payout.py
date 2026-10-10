"""Verify original reward factory -> AddExpItem -> GetExpGold fixture contracts."""
import unittest
from tools import stoneage_battle_original_drop_payout_audit as payout

class OriginalLootPayoutTests(unittest.TestCase):
    def test_two_distinct_runtime_oracles(self):
        for p in ("gavin","bismarck"):
            c=payout.observations(p)
            for term in ("payout_scenario<2", "BATTLE_GetExpGold(battle_at,0,0)",
               "CHAR_findEmptyItemBox(0)==-1","==expected_live",
               "expected_arena.Side[0].Entry[0].getitem[0]=-1",
               "expected_items[3].use=0","workint[ITEM_WORKCHARAINDEX]=0",
               "expected_actors[0].indexOfExistItems[empty]=3",
               "memcpy(expected_items,reward_items", "memcmp(expected_actors,slots",
               "memcmp(expected_arena,arena", "REAL_HEADER_DROP_PAYOUT|"):
                self.assertIn(term,c,term)
            self.assertNotIn("ITEM_TYPE",c)
            self.assertIn("1" if p=="bismarck" else "0",c)
    def test_no_false_second_loop_claim(self):
        self.assertNotIn("BATTLE_Loop(",payout.PAYOUT)
        self.assertIn("BATTLE_GetExpGold",payout.PAYOUT)
    def test_no_reimplementation_of_gameplay(self):
        self.assertIsNotNone(payout.ticket.ticket_native)
        self.assertIsNotNone(payout.ticket.drop.positive_drop_native)
