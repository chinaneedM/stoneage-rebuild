import unittest

from tools.stoneage_combined_model import (
    COMMAND_VALUE,
    CombinedSourceDomain,
    normalize_declared_count,
    resolve_combined_selection,
)


class CombinedModelTests(unittest.TestCase):
    def test_selects_explicit_reduced_rand_index_and_clears_high_half(self):
        result=resolve_combined_selection(
            target_slot=3,
            declared_count=3,
            magic_ids=(301,302,303),
            draw_index=2,
        )
        self.assertEqual(result.selected_magic_id,303)
        self.assertEqual(result.packed_com3,303)
        self.assertEqual(result.rng_draws_consumed,1)
        self.assertEqual(result.command_value,COMMAND_VALUE)
        self.assertEqual(result.target_slot,3)

    def test_source_clamps_declared_count_above_ten(self):
        result=resolve_combined_selection(
            target_slot=0,
            declared_count=12,
            magic_ids=tuple(range(100,112)),
            draw_index=9,
        )
        self.assertEqual(result.effective_count,10)
        self.assertEqual(result.magic_ids,tuple(range(100,110)))
        self.assertEqual(result.selected_magic_id,109)

    def test_nonpositive_count_is_fail_closed(self):
        for value in (0,-1):
            with self.assertRaises(CombinedSourceDomain):
                normalize_declared_count(value)

    def test_missing_magic_tokens_are_fail_closed(self):
        with self.assertRaises(CombinedSourceDomain):
            resolve_combined_selection(
                target_slot=0,
                declared_count=3,
                magic_ids=(1,2),
                draw_index=0,
            )

    def test_draw_is_reduced_modulo_domain_not_python_rng(self):
        for draw in (-1,3,1.0):
            with self.assertRaises(CombinedSourceDomain):
                resolve_combined_selection(
                    target_slot=0,
                    declared_count=3,
                    magic_ids=(1,2,3),
                    draw_index=draw,
                )


if __name__=="__main__":
    unittest.main()
