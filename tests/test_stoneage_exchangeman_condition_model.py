import unittest

from tools.stoneage_exchangeman_condition_model import (
    ExchangeState,
    ItemState,
    PetState,
    c_atoi,
    compare_source,
    evaluate_event_expression,
    evaluate_term,
    event_cost,
    event_warp_step,
    get_arg_field,
    merge_arg_file_lines,
)


class ExChangeManConditionCoreTests(unittest.TestCase):
    def test_arg_file_lines_are_joined_by_pipe(self):
        self.assertEqual(
            merge_arg_file_lines(["EventNo:1\n", "EVENT:LV>10\r\n", "EventEnd\n"]),
            "EventNo:1|EVENT:LV>10|EventEnd",
        )

    def test_field_lookup_is_substring_based_like_source(self):
        arg = "NomalWindowMsg1:first|NomalWindowMsg:second"
        self.assertEqual(get_arg_field(arg, "NomalWindowMsg"), "first")

    def test_c_atoi_stops_at_first_non_digit(self):
        self.assertEqual(c_atoi("  -12xyz"), -12)
        self.assertEqual(c_atoi("xyz"), 0)

    def test_comparison_helper(self):
        self.assertTrue(compare_source(10, 10, 0))
        self.assertTrue(compare_source(10, 9, 1))
        self.assertTrue(compare_source(10, 11, 2))
        self.assertTrue(compare_source(10, 11, 3))

    def test_event_expression_uses_or_between_commas(self):
        state = ExchangeState(level=20)
        self.assertEqual(evaluate_event_expression("LV=1,LV>10", state), 2)

    def test_event_expression_uses_and_inside_branch(self):
        state = ExchangeState(level=20, end_flags=frozenset({3}))
        self.assertEqual(evaluate_event_expression("LV>10&ENDEV=3,LV=1", state), 1)
        self.assertEqual(evaluate_event_expression("LV>10&ENDEV=4,LV=1", state), -1)

    def test_level_relations_follow_source(self):
        state = ExchangeState(level=20)
        self.assertTrue(evaluate_term("LV<21", state))
        self.assertTrue(evaluate_term("LV>19", state))
        self.assertTrue(evaluate_term("LV=20", state))

    def test_level_not_equal_is_inverted_by_old_source(self):
        self.assertTrue(evaluate_term("LV!=20", ExchangeState(level=20)))
        self.assertFalse(evaluate_term("LV!=20", ExchangeState(level=21)))

    def test_item_equality_checks_carried_slots_only(self):
        state = ExchangeState(items=(ItemState(100, carried=False), ItemState(200, carried=True)))
        self.assertFalse(evaluate_term("ITEM=100", state))
        self.assertTrue(evaluate_term("ITEM=200", state))

    def test_item_not_equal_means_target_absent_from_carried_slots(self):
        self.assertTrue(evaluate_term("ITEM!=100", ExchangeState(items=(ItemState(200),))))
        self.assertFalse(evaluate_term("ITEM!=100", ExchangeState(items=(ItemState(100),))))
        self.assertTrue(evaluate_term("ITEM!=100", ExchangeState()))

    def test_item_less_and_greater_never_succeed(self):
        state = ExchangeState(items=(ItemState(10), ItemState(20)))
        self.assertFalse(evaluate_term("ITEM<99", state))
        self.assertFalse(evaluate_term("ITEM>1", state))

    def test_item_quantity_counts_equipment_and_piles(self):
        state = ExchangeState(
            items=(ItemState(50, pile=2, carried=False), ItemState(50, pile=0, carried=True))
        )
        self.assertTrue(evaluate_term("ITEM=50*3", state))
        self.assertFalse(evaluate_term("ITEM=50*4", state))

    def test_star_equality_dispatches_to_item_quantity_even_for_other_left_token(self):
        state = ExchangeState(items=(ItemState(50, pile=2),))
        self.assertTrue(evaluate_term("WHATEVER=50*2", state))

    def test_end_event_negation_is_normal(self):
        set_state = ExchangeState(end_flags=frozenset({5}))
        clear_state = ExchangeState()
        self.assertTrue(evaluate_term("ENDEV=5", set_state))
        self.assertFalse(evaluate_term("ENDEV!=5", set_state))
        self.assertTrue(evaluate_term("ENDEV!=5", clear_state))

    def test_end_event_relational_operators_collapse_to_bit_presence(self):
        state = ExchangeState(end_flags=frozenset({5}))
        self.assertTrue(evaluate_term("ENDEV<5", state))
        self.assertTrue(evaluate_term("ENDEV>5", state))

    def test_now_event_not_equal_is_tautological(self):
        self.assertTrue(evaluate_term("NOWEV!=5", ExchangeState(now_flags=frozenset({5}))))
        self.assertTrue(evaluate_term("NOWEV!=5", ExchangeState()))

    def test_savepoint_condition_uses_bit_presence(self):
        state = ExchangeState(savepoint_bits=(1 << 4))
        self.assertTrue(evaluate_term("SP=4", state))
        self.assertFalse(evaluate_term("SP!=4", state))
        self.assertTrue(evaluate_term("SP!=3", state))

    def test_time_relations_use_current_ls_time(self):
        state = ExchangeState(lstime=12)
        self.assertTrue(evaluate_term("TIME<13", state))
        self.assertTrue(evaluate_term("TIME>11", state))

    def test_image_relational_arguments_are_reversed_in_source(self):
        state = ExchangeState(image=20)
        self.assertTrue(evaluate_term("IMAGE<10", state))
        self.assertFalse(evaluate_term("IMAGE>10", state))
        self.assertTrue(evaluate_term("IMAGE=20", state))

    def test_pet_condition_supports_id_level_and_count(self):
        state = ExchangeState(
            pets=(PetState(7, 20), PetState(7, 30), PetState(8, 40))
        )
        self.assertTrue(evaluate_term("PET>10-7*2", state))
        self.assertFalse(evaluate_term("PET>25-7*2", state))

    def test_pet_event_mode_and_name_gate(self):
        state = ExchangeState(pets=(PetState(7, 20, endevent=1, use_name="A"),))
        self.assertTrue(evaluate_term("PETEV>10-7", state, required_pet_name="A"))
        self.assertFalse(evaluate_term("PETEV>10-7", state, required_pet_name="B"))
        self.assertFalse(evaluate_term("PET>10-7", state, required_pet_name="A"))

    def test_pet_not_equal_is_treated_as_equality(self):
        state = ExchangeState(pets=(PetState(7, 20),))
        self.assertTrue(evaluate_term("PET!=20-7", state))
        self.assertFalse(evaluate_term("PET!=21-7", state))

    def test_event_cost_supports_level_multiplier(self):
        self.assertEqual(event_cost("LV*25", 10), 250)
        self.assertEqual(event_cost("300", 10), 300)

    def test_warp_destinations_cycle_with_npc_local_counter(self):
        counter, dest = event_warp_step("100.1.2,200.3.4", 1)
        self.assertEqual((counter, dest), (2, (100, 1, 2)))
        counter, dest = event_warp_step("100.1.2,200.3.4", counter)
        self.assertEqual((counter, dest), (3, (200, 3, 4)))
        counter, dest = event_warp_step("100.1.2,200.3.4", counter)
        self.assertEqual((counter, dest), (2, (100, 1, 2)))

    def test_warp_skips_malformed_entries(self):
        counter, dest = event_warp_step("bad,200.3.4", 1)
        self.assertEqual((counter, dest), (3, (200, 3, 4)))

    def test_unknown_condition_is_false(self):
        self.assertFalse(evaluate_term("UNKNOWN=1", ExchangeState()))


if __name__ == "__main__":
    unittest.main()
