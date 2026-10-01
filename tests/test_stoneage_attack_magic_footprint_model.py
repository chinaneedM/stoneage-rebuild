import unittest

from tools.stoneage_attack_magic_footprint_model import (
    CHAR_TABLE,
    SLOT_COORD,
    TARGET_SIDE_0,
    TARGET_SIDE_0_B_ROW,
    TARGET_SIDE_0_F_ROW,
    TARGET_SIDE_1,
    footprint_target_set,
    matrix_from_attmagic_record,
    normalize_attack_magic_selector,
    record_index_for_attacker,
    resolve_attack_magic_footprint,
    source_sort_compare,
    source_sort_is_portable,
    source_sorted_targets,
)


def record(matrix):
    return tuple([0] * 18 + [x for row in matrix for x in row])


class StoneAgeAttackMagicFootprintModelTests(unittest.TestCase):
    def test_fixed_battle_geometry(self):
        self.assertEqual(CHAR_TABLE[3], (3, 1, 0, 2, 4))
        self.assertEqual(SLOT_COORD[0], (3, 2))
        self.assertEqual(SLOT_COORD[10], (0, 2))

    def test_side_record_selection_is_adjacent_pair(self):
        self.assertEqual(
            record_index_for_attacker(magic_idx=2, attacker_slot=0),
            5,
        )
        self.assertEqual(
            record_index_for_attacker(magic_idx=2, attacker_slot=15),
            4,
        )

    def test_matrix_decode_is_three_by_five(self):
        matrix = (
            (1, 2, 3, 4, 5),
            (6, 7, 8, 9, 10),
            (11, 12, 13, 14, 15),
        )
        self.assertEqual(matrix_from_attmagic_record(record(matrix)), matrix)

    def test_dead_single_target_uses_source_rejection_sampling(self):
        self.assertEqual(
            normalize_attack_magic_selector(
                0,
                alive_slots={1, 4},
                retarget_rolls_0_9=(9, 8, 1),
            ),
            4,
        )
        with self.assertRaises(ValueError):
            normalize_attack_magic_selector(
                0,
                alive_slots={1},
                retarget_rolls_0_9=(9,),
            )

    def test_empty_row_falls_to_other_row(self):
        self.assertEqual(
            normalize_attack_magic_selector(
                TARGET_SIDE_0_B_ROW,
                alive_slots={5},
            ),
            TARGET_SIDE_0_F_ROW,
        )
        self.assertIsNone(
            normalize_attack_magic_selector(
                TARGET_SIDE_0_B_ROW,
                alive_slots={10},
            )
        )

    def test_single_center_column_hits_same_column_across_side_rows(self):
        matrix = (
            (0, 0, 1, 0, 0),
            (0, 0, 1, 0, 0),
            (0, 0, 1, 0, 0),
        )
        self.assertEqual(
            footprint_target_set(
                selector=0,
                matrix=matrix,
                alive_slots=range(20),
            ),
            (5, 0),
        )
        self.assertEqual(
            footprint_target_set(
                selector=10,
                matrix=matrix,
                alive_slots=range(20),
            ),
            (10, 15),
        )

    def test_whole_side_uses_first_two_matrix_rows(self):
        matrix = (
            (1, 1, 1, 1, 1),
            (1, 1, 1, 1, 1),
            (0, 0, 0, 0, 0),
        )
        self.assertEqual(
            set(
                footprint_target_set(
                    selector=TARGET_SIDE_0,
                    matrix=matrix,
                    alive_slots=range(20),
                )
            ),
            set(range(10)),
        )
        self.assertEqual(
            set(
                footprint_target_set(
                    selector=TARGET_SIDE_1,
                    matrix=matrix,
                    alive_slots=range(20),
                )
            ),
            set(range(10, 20)),
        )

    def test_source_sort_bug_is_detected_not_normalized(self):
        self.assertLess(source_sort_compare(0, 1), 0)
        self.assertLess(source_sort_compare(1, 0), 0)
        self.assertFalse(source_sort_is_portable((0, 1)))
        self.assertIsNone(source_sorted_targets((0, 1)))
        self.assertFalse(source_sort_is_portable((0, 5)))
        self.assertIsNone(source_sorted_targets((5, 0)))
        self.assertTrue(source_sort_is_portable((10, 15)))
        self.assertEqual(source_sorted_targets((15, 10)), (10, 15))

    def test_resolved_footprint_keeps_order_boundary_explicit(self):
        all_one = ((1, 1, 1, 1, 1),) * 3
        result = resolve_attack_magic_footprint(
            magic_idx=2,
            attacker_slot=15,
            selector=TARGET_SIDE_0,
            record=record(all_one),
            alive_slots=range(20),
        )
        self.assertEqual(result.record_index, 4)
        self.assertEqual(
            set(result.targets_in_source_build_order),
            set(range(10)),
        )
        self.assertFalse(result.source_sort_portable)
        self.assertIsNone(result.source_sorted_targets)


if __name__ == "__main__":
    unittest.main()
