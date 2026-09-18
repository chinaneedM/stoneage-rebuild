import unittest

from tools.stoneage_exchangeman_mutation_model import (
    accept_del_trace,
    apply_flag_mutations,
    delitem_scan_domain,
    evdel_nonstar_effective_item_id,
    event_add_trace,
    item_capacity_projection,
    source_pet_random_choice,
)


class ExChangeManMutationCoreTests(unittest.TestCase):
    def test_capacity_counts_getitem_and_random(self):
        arg = "EVENT:LV=1|GetItem:10,20*2|GetRandItem:30,31"
        r = item_capacity_projection(arg, mode=0, event_branch_index=1, carried_item_ids=(None, None, None, None))
        self.assertTrue(r.allowed)
        self.assertEqual(r.projected_net_slots, 4)

    def test_capacity_rejects_exactly_full_random_only(self):
        arg = "EVENT:LV=1|GetRandItem:30,31"
        r = item_capacity_projection(arg, mode=0, event_branch_index=1, carried_item_ids=(1, 2))
        self.assertFalse(r.allowed)
        self.assertEqual(r.reason, "random_item_no_room")

    def test_nonstar_delitem_stops_capacity_scan_after_first_token(self):
        arg = "EVENT:LV=1|DelItem:10,20|GetItem:99"
        r = item_capacity_projection(arg, mode=0, event_branch_index=1, carried_item_ids=(10, 20))
        self.assertTrue(r.allowed)
        self.assertEqual(r.projected_net_slots, 0)

    def test_star_delitem_forecasts_slot_per_unit_without_inventory_check(self):
        arg = "EVENT:LV=1|DelItem:10*3|GetItem:99*3"
        r = item_capacity_projection(arg, mode=0, event_branch_index=1, carried_item_ids=(10, 20))
        self.assertTrue(r.allowed)
        self.assertEqual(r.projected_net_slots, 0)

    def test_evdel_uses_one_based_selected_event_branch(self):
        arg = "EVENT:ITEM=10,ITEM=20*2|DelItem:EVDEL|GetItem:99"
        r = item_capacity_projection(arg, mode=0, event_branch_index=2, carried_item_ids=(20, 20))
        self.assertTrue(r.allowed)
        self.assertEqual(r.projected_net_slots, -1)

    def test_evdel_notdel_excludes_forecasted_deletion(self):
        arg = "EVENT:ITEM=20*2|DelItem:EVDEL|NotDel:20|GetItem:99"
        r = item_capacity_projection(arg, mode=0, event_branch_index=1, carried_item_ids=(20, 20))
        self.assertFalse(r.allowed)

    def test_mode_one_skips_reward_capacity_forecast(self):
        arg = "EVENT:LV=1|GetItem:10*5|GetRandItem:20"
        r = item_capacity_projection(arg, mode=1, event_branch_index=1, carried_item_ids=(1, 2))
        self.assertTrue(r.allowed)
        self.assertEqual(r.projected_net_slots, 0)

    def test_delitem_scan_domain_changes_with_star_break_and_piles(self):
        self.assertEqual(delitem_scan_domain(starred=True, break_flag=False, pile_enabled=True), "carried_only")
        self.assertEqual(delitem_scan_domain(starred=True, break_flag=True, pile_enabled=True), "all_item_slots")
        self.assertEqual(delitem_scan_domain(starred=False, break_flag=False, pile_enabled=True), "all_item_slots")

    def test_active_pile_branch_breaks_nonstar_evdel_target(self):
        self.assertEqual(evdel_nonstar_effective_item_id(123, pile_enabled=True), -1)
        self.assertEqual(evdel_nonstar_effective_item_id(123, pile_enabled=False), 123)

    def test_pet_random_first_slot_zero_collapses_to_first_candidate(self):
        self.assertEqual(source_pet_random_choice(4, 0, 12345), 1)

    def test_pet_random_normal_when_first_empty_is_within_candidate_range(self):
        self.assertEqual(source_pet_random_choice(4, 2, 5), 2)

    def test_pet_random_can_select_beyond_list_when_first_empty_exceeds_count(self):
        self.assertIsNone(source_pet_random_choice(2, 5, 3))

    def test_event_add_checks_delstone_before_mutation(self):
        arg = "EVENT:LV=1|DelStone:100|GetPet:5"
        r = event_add_trace(arg, mode=0, level=1, gold=99, carried_item_ids=(None,), event_branch_index=1)
        self.assertFalse(r["success"])
        self.assertEqual(r["trace"], ("item_capacity_preflight", "delstone_affordability_check"))

    def test_event_add_pet_can_be_granted_before_later_item_capacity_failure(self):
        arg = "EVENT:LV=1|GetPet:5|GetItem:10"
        r = event_add_trace(
            arg, mode=0, level=1, gold=0, carried_item_ids=(None,),
            event_branch_index=1, post_delete_empty_slots=0
        )
        self.assertFalse(r["success"])
        self.assertIn("add_pet_event_marked", r["trace"])
        self.assertEqual(r["reason"], "post_delete_item_full")

    def test_event_add_mode_two_skips_preflight_reward_count_then_becomes_mode_zero(self):
        arg = "EVENT:LV=1|GetPet:5|GetItem:10*2"
        r = event_add_trace(
            arg, mode=2, level=1, gold=0, carried_item_ids=(1,),
            event_branch_index=1, post_delete_empty_slots=0
        )
        self.assertFalse(r["success"])
        self.assertIn("mode2_rewritten_to_mode0_after_preflight", r["trace"])
        self.assertIn("add_pet_event_marked", r["trace"])

    def test_event_add_getitem_failure_is_propagated(self):
        arg = "EVENT:LV=1|GetItem:10"
        r = event_add_trace(
            arg, mode=0, level=1, gold=0, carried_item_ids=(None,),
            event_branch_index=1, post_delete_empty_slots=1,
            outcomes={"add_item": False}
        )
        self.assertFalse(r["success"])
        self.assertEqual(r["reason"], "add_item_failed")

    def test_event_add_random_failure_is_ignored(self):
        arg = "EVENT:LV=1|GetRandItem:10"
        r = event_add_trace(
            arg, mode=0, level=1, gold=0, carried_item_ids=(None,),
            event_branch_index=1, post_delete_empty_slots=1,
            outcomes={"rand_item": False}
        )
        self.assertTrue(r["success"])
        self.assertIn("grant_random_item_ignored_return", r["trace"])

    def test_accept_prechecks_delstone_before_getstone_so_netting_does_not_rescue(self):
        arg = "EVENT:LV=1|DelStone:100|GetStone:200"
        r = accept_del_trace(
            arg, mode=0, level=1, gold=50, max_gold=1000,
            carried_item_ids=(None,), event_branch_index=1
        )
        self.assertFalse(r["success"])
        self.assertEqual(r["reason"], "insufficient_stone")

    def test_accept_prechecks_getstone_cap_before_later_delstone(self):
        arg = "EVENT:LV=1|GetStone:100|DelStone:100"
        r = accept_del_trace(
            arg, mode=0, level=1, gold=900, max_gold=1000,
            carried_item_ids=(None,), event_branch_index=1
        )
        self.assertFalse(r["success"])
        self.assertEqual(r["reason"], "stone_cap")

    def test_accept_getstone_mutation_survives_later_pet_failure(self):
        arg = "EVENT:LV=1|GetStone:100|GetPet:5"
        r = accept_del_trace(
            arg, mode=0, level=1, gold=10, max_gold=1000,
            carried_item_ids=(None,), event_branch_index=1,
            outcomes={"add_pet": False}
        )
        self.assertFalse(r["success"])
        self.assertEqual(r["gold_after"], 110)
        self.assertEqual(r["trace"][-2:], ("add_stone", "add_pet_unmarked"))

    def test_accept_item_grant_return_values_are_ignored(self):
        arg = "EVENT:LV=1|GetRandItem:20|GetItem:10"
        r = accept_del_trace(
            arg, mode=1, level=1, gold=0, max_gold=1000,
            carried_item_ids=(1,), event_branch_index=1,
            outcomes={"rand_item": False, "add_item": False}
        )
        self.assertTrue(r["success"])
        self.assertIn("grant_random_item_ignored_return", r["trace"])
        self.assertIn("grant_getitem_ignored_return", r["trace"])

    def test_accept_order_is_pet_delete_then_gold_then_pet_grants_then_items(self):
        arg = "EVENT:LV=1|DelPet:PET=1-1|GetStone:5|GetPet:2|GetEgg:3;4;1|DelItem:10|DelStone:2|GetRandItem:20|GetItem:30"
        r = accept_del_trace(
            arg, mode=1, level=1, gold=100, max_gold=1000,
            carried_item_ids=(10, None), event_branch_index=1
        )
        expected = (
            "item_capacity_preflight", "delstone_affordability_check", "getstone_cap_check",
            "delete_pet", "add_stone", "add_pet_unmarked", "add_egg_unmarked",
            "delete_delitem_ignored_return", "deduct_stone",
            "grant_random_item_ignored_return", "grant_getitem_ignored_return",
            "recompute_player_parameters",
        )
        self.assertEqual(r["trace"], expected)

    def test_endset_toggle_clears_when_now_was_primed(self):
        r = apply_flag_mutations(event_no=7, prime_now=True, end_set=(8,))
        self.assertNotIn(7, r["now_flags"])
        self.assertIn(8, r["end_flags"])

    def test_endset_toggle_sets_now_when_not_preexisting(self):
        r = apply_flag_mutations(event_no=7, prime_now=False, end_set=(8,))
        self.assertIn(7, r["now_flags"])
        self.assertIn(8, r["end_flags"])

    def test_clean_clears_both_domains_conditionally(self):
        r = apply_flag_mutations(now_flags=(3, 4), end_flags=(3, 5), clean=(3,))
        self.assertNotIn(3, r["now_flags"])
        self.assertNotIn(3, r["end_flags"])
        self.assertIn(4, r["now_flags"])
        self.assertIn(5, r["end_flags"])


if __name__ == "__main__":
    unittest.main()
