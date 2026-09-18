import unittest

from tools.stoneage_janken_core_model import (
    EntryToken,entry_check,entry_delete,judge,parse_item_tokens,
    player_hand_from_selection,result_flow,start_after_yes,warp_tuple,
)

class JankenCoreTests(unittest.TestCase):
    def test_parse_plain_and_star(self):
        self.assertEqual(
            parse_item_tokens("10*2,20"),
            (EntryToken(10,2),EntryToken(20,None)),
        )

    def test_plain_entry_needs_one(self):
        self.assertTrue(entry_check((EntryToken(10,None),),[10]))
        self.assertFalse(entry_check((EntryToken(10,None),),[]))

    def test_star_entry_needs_count(self):
        self.assertTrue(entry_check((EntryToken(10,2),),[10,10]))
        self.assertFalse(entry_check((EntryToken(10,2),),[10]))

    def test_duplicate_check_can_reuse_same_item(self):
        self.assertTrue(
            entry_check((EntryToken(10,None),EntryToken(10,None)),[10])
        )

    def test_plain_delete_removes_all_copies(self):
        result=entry_delete((EntryToken(10,None),),[10,20,10])
        self.assertEqual(result["items_after"],(20,))
        self.assertEqual(result["deleted_count"],2)

    def test_star_delete_removes_up_to_count(self):
        result=entry_delete((EntryToken(10,2),),[10,10,10])
        self.assertEqual(result["items_after"],(10,))
        self.assertEqual(result["deleted_count"],2)

    def test_insufficient_star_delete_still_removes_available(self):
        result=entry_delete((EntryToken(10,3),),[10,10])
        self.assertEqual(result["deleted_count"],2)

    def test_failed_entry_check_still_deletes_and_continues(self):
        result=start_after_yes("10*3",[10,10])
        self.assertFalse(result["entry_check_passed"])
        self.assertEqual(result["deleted_count"],2)
        self.assertTrue(result["continues_to_game"])
        self.assertEqual(result["events"][0],"send_no_item_window")
        self.assertEqual(result["events"][-1],"send_janken_selection")

    def test_failed_later_requirement_keeps_prior_deletion(self):
        result=start_after_yes("10,20",[10])
        self.assertFalse(result["entry_check_passed"])
        self.assertEqual(result["items_after"],())
        self.assertTrue(result["continues_to_game"])

    def test_no_entry_item_is_free(self):
        result=start_after_yes(None,[10])
        self.assertTrue(result["entry_check_passed"])
        self.assertEqual(result["items_after"],(10,))

    def test_selection_mapping(self):
        self.assertEqual(player_hand_from_selection(3),0)
        self.assertEqual(player_hand_from_selection(5),1)
        self.assertEqual(player_hand_from_selection(7),2)
        self.assertEqual(player_hand_from_selection(4),-1)

    def test_standard_janken_results(self):
        self.assertEqual(judge(7,0),"win")
        self.assertEqual(judge(5,0),"lose")
        self.assertEqual(judge(3,0),"tie")

    def test_invalid_selection_becomes_tie(self):
        self.assertEqual(judge(4,2),"tie")

    def test_tie_reopens_without_warp_or_reward(self):
        result=result_flow(
            3,0,win_item_configured=True,win_warp=(1,2,3)
        )
        self.assertEqual(result["events"],("send_tie_selection",))
        self.assertIsNone(result["warp"])

    def test_win_reward_attempt_precedes_warp(self):
        result=result_flow(
            7,0,win_item_configured=True,win_warp=(1,2,3)
        )
        self.assertEqual(
            result["events"][:2],
            ("attempt_reward_item_ignored_return","warp_player"),
        )
        self.assertEqual(result["warp"],(1,2,3))

    def test_lose_reward_attempt_precedes_warp(self):
        result=result_flow(
            5,0,lose_item_configured=True,lose_warp=(4,5,6)
        )
        self.assertEqual(result["result"],"lose")
        self.assertEqual(
            result["events"][:2],
            ("attempt_reward_item_ignored_return","warp_player"),
        )

    def test_reward_failure_does_not_block_warp(self):
        result=result_flow(
            7,0,win_item_configured=True,reward_add_succeeds=False,
            win_warp=(1,2,3)
        )
        self.assertEqual(result["warp"],(1,2,3))
        self.assertIn("warp_player",result["events"])

    def test_missing_reward_key_still_warps(self):
        result=result_flow(
            7,0,win_item_configured=False,win_warp=(1,2,3)
        )
        self.assertEqual(result["events"][0],"warp_player")

    def test_warp_parser_three_fields(self):
        self.assertEqual(warp_tuple("1,2,3"),(1,2,3))

    def test_warp_parser_missing_fields_zero(self):
        self.assertEqual(warp_tuple("1"),(1,0,0))

if __name__=="__main__":
    unittest.main()
