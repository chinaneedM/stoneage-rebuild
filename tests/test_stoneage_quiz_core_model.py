import unittest

from tools.stoneage_quiz_core_model import (
    MEPLAYER,
    OLDNO,
    QuestionMeta,
    can_allocate_player_slot,
    can_record_question_history,
    choice_correct,
    delete_entry_items,
    delete_entry_stone,
    entry_stone_check,
    free_text_correct,
    item_full_gate,
    item_requirements_satisfied,
    party_gate,
    persistence_boundary,
    question_matches,
    question_row_status,
    threshold_value,
)


class QuizCoreModelTests(unittest.TestCase):
    def test_default_nonpositive_masks_match_all_normal_question_bits(self):
        q = QuestionMeta(q_type=1, level=16, answer_type=4, answer_no=1)
        self.assertTrue(question_matches(q, type_mask=0, answer_mask=0, level_mask=0))

    def test_question_filters_are_bit_masks(self):
        q = QuestionMeta(q_type=2, level=4, answer_type=2, answer_no=1)
        self.assertTrue(question_matches(q, type_mask=2, answer_mask=2, level_mask=4))
        self.assertFalse(question_matches(q, type_mask=1, answer_mask=2, level_mask=4))

    def test_loader_skips_short_rows(self):
        self.assertEqual(question_row_status(8, 2, 1), "skip_short_row")
        self.assertEqual(question_row_status(9, 2, 1), "loaded")

    def test_loader_hard_rejects_impossible_answer_shapes(self):
        self.assertEqual(
            question_row_status(9, 1, 3), "fatal_two_choice_answer_3"
        )
        self.assertEqual(
            question_row_status(9, 4, 2), "fatal_free_text_answer_not_1"
        )

    def test_threshold_scan_uses_configuration_order(self):
        pairs = [(2, "low-first"), (5, "high-second")]
        self.assertEqual(threshold_value(6, pairs), "low-first")
        self.assertIsNone(threshold_value(1, pairs))

    def test_free_text_uses_substring_not_exact_equality(self):
        self.assertTrue(free_text_correct("prefix-answer-suffix", "answer"))
        self.assertFalse(free_text_correct("other", "answer"))

    def test_zero_choice_is_ignored(self):
        self.assertIsNone(choice_correct("0", 2))
        self.assertTrue(choice_correct("2", 2))
        self.assertFalse(choice_correct("1", 2))

    def test_party_gate_warns_but_does_not_block(self):
        self.assertEqual(party_gate(True), "warn_and_continue")
        self.assertEqual(party_gate(False), "continue")

    def test_starred_requirement_counts_matches(self):
        inv = ["a", "a", "b"]
        self.assertTrue(item_requirements_satisfied(inv, [("a", 2)]))
        self.assertFalse(item_requirements_satisfied(inv, [("a", 3)]))

    def test_duplicate_requirements_can_reuse_same_items_during_validation(self):
        inv = ["a"]
        self.assertTrue(
            item_requirements_satisfied(inv, [("a", 1), ("a", 1)])
        )
        self.assertEqual(
            delete_entry_items(inv, [("a", 1), ("a", 1)]),
            [],
        )

    def test_plain_requirement_deletes_all_matching_copies(self):
        self.assertEqual(
            delete_entry_items(["a", "b", "a"], [("a", None)]),
            ["b"],
        )

    def test_full_inventory_can_pass_if_entry_item_will_be_consumed(self):
        self.assertTrue(
            item_full_gate(
                has_empty_item_slot=False,
                inventory=["ticket", "x"],
                entry_requirements=[("ticket", 1)],
            )
        )
        self.assertFalse(
            item_full_gate(
                has_empty_item_slot=False,
                inventory=["x", "y"],
                entry_requirements=[("ticket", 1)],
            )
        )

    def test_full_inventory_without_entry_item_is_rejected(self):
        self.assertFalse(
            item_full_gate(
                has_empty_item_slot=False,
                inventory=["x"],
                entry_requirements=[],
            )
        )

    def test_entry_stone_normal_and_negative_cost_semantics(self):
        self.assertTrue(entry_stone_check(100, 50))
        self.assertFalse(entry_stone_check(49, 50))
        self.assertEqual(delete_entry_stone(100, 50), 50)
        self.assertEqual(delete_entry_stone(100, -50), 150)

    def test_session_capacity_is_eight(self):
        self.assertEqual(MEPLAYER, 8)
        self.assertTrue(can_allocate_player_slot(7))
        self.assertFalse(can_allocate_player_slot(8))

    def test_question_history_capacity_is_one_hundred(self):
        self.assertEqual(OLDNO, 100)
        self.assertTrue(can_record_question_history(99))
        self.assertFalse(can_record_question_history(100))

    def test_quiz_mutations_use_normal_deferred_character_save(self):
        self.assertEqual(
            persistence_boundary(), "deferred_standard_character_save"
        )


if __name__ == "__main__":
    unittest.main()
