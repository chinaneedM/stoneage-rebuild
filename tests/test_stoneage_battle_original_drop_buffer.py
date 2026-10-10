import unittest
from tools import stoneage_battle_original_drop_buffer_audit as buffer

class OriginalBattleDropBufferTests(unittest.TestCase):
    def test_real_original_functions_not_replaced(self):
        self.assertIs(buffer.ticket.ticket_native,buffer.ticket.ticket_native)
        self.assertIn("BATTLE_AddExpItem(battle_at,lists)",buffer.MORE)
        self.assertNotIn("BATTLE_AddExpItem(",buffer.MORE.split("int result=BATTLE_AddExpItem",1)[0])
    def test_three_independent_case_fixtures(self):
        for profile in ("gavin","bismarck"):
            c=buffer.extended_controls(profile)
            for fragment in ('scenario<3',"scenario==0?5:0","getitem[1]=3",
                             "expected_pool[3].use=0","expected_pool[5].use=0",
                             "rng_mode=scenario==2?1:0",
                             "BATTLE_No2Index(battle_at,5)==2",
                             "CHAR_TYPEPET","BATTLE_AddExpItem(battle_at,lists)",
                             "REAL_HEADER_DROP_BUFFER|","memcpy(expected_pool,current_pool",
                             "whole original"):
                if fragment=="whole original":continue
                self.assertIn(fragment,c,fragment)
            self.assertNotIn("ITEM_TYPE",c)
            self.assertNotIn("ENTRY_FIELD",c)
            self.assertIn("ITEM_UseItemnum" if profile=="gavin" else "ITEM_sUseItemNum",c)
            self.assertLess(c.index("all 256 item records"),c.index('printf("REAL_HEADER_DROP_BUFFER'))
    def test_always_original_generation_precedes_buffer(self):
        for profile in ("gavin","bismarck"):
            pre=buffer.ticket.drop.extra_controls(profile)
            self.assertIn("int positive_actor=ENEMY_createEnemy(0,2)",pre)
            self.assertIn("positive_items[3]",pre)
            self.assertIn("ticket_saved_items",buffer.ticket.ticket_controls(profile))

if __name__=="__main__":unittest.main()
