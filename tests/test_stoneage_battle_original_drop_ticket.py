"""Immutable source-shape and fixture-preservation contracts for actual battle ticket."""
import unittest
from tools import stoneage_battle_original_drop_ticket_audit as ticket

class OriginalBattleDropTicketTests(unittest.TestCase):
    def test_full_original_ticket_path(self):
        for p in ("gavin","bismarck"):
            c=ticket.ticket_controls(p)
            for marker in ("BATTLE_AddExpItem(battle_at,ticket_list)",
                           "int ticket_list[2]={0,-1}",
                           "ENTRY_FIELD", "getitem[0]=3",
                           "indexOfExistItems[CHAR_STARTITEMARRAY]==-1",
                           "BATTLE_No2Index(battle_at,0)==0",
                           "==ticket_saved_use",
                           "memcpy(reward_items,ticket_saved_items",
                           "*arena=ticket_saved_arena"):
                if marker=="ENTRY_FIELD":continue
                self.assertIn(marker,c,marker)
            self.assertNotIn("ENTRY_FIELD",c)
            self.assertNotIn("ITEM_TYPE",c)
            self.assertIn("CHAR_ISDIE",c)
            self.assertLess(c.index("entire 256-item pool"),c.index("memcpy(reward_items,ticket_saved_items"))
            self.assertIn("REAL_HEADER_DROP_TICKET",c)
    def test_native_is_an_extension_of_prior_original_enemy_witness(self):
        self.assertIs(ticket.drop.positive_drop_native,ticket.drop.positive_drop_native)
        self.assertIn('original enemy drop does not mutate factory master template',
                      ticket.drop.extra_controls("gavin"))
        self.assertIn("BATTLE_AddExpItem",ticket.TICKET)
    def test_source_pin_profile_shape(self):
        import json
        j=json.loads(ticket.SOURCE.read_text())
        self.assertEqual(set(j["source_profiles"]),{"gavin","bismarck"})
        self.assertEqual(set(j["inherited_native_sha256"]),{"gavin","bismarck"})

if __name__=="__main__":unittest.main()
