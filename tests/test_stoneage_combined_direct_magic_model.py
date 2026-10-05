import unittest

from tools.stoneage_combined_direct_magic_model import (
    CombinedDirectMagicDomain, RuntimeItemZeroWitness,
    resolve_combined_direct_magic_route as route,
)
from tools.stoneage_combined_model import resolve_combined_selection
from tools.stoneage_enemy_ai_combined_bridge import (
    CombinedMagicCrosslink, EnemyAiCombinedSubmission,
)


class CombinedDirectMagicTests(unittest.TestCase):
    def test_submission_selection_stays_consumed_when_nocast_blocks_direct_use(self):
        selection = resolve_combined_selection(target_slot=0, declared_count=1,
                                              magic_ids=(240,), draw_index=0)
        submission = EnemyAiCombinedSubmission(
            "enemy", 0, 632, "PETSKILL_Combined", 0, selection,
            CombinedMagicCrosslink(240,"MAGIC_AttReverse",1,1,0,None),
        )
        blocked = submission.direct_magic_route(current_mp=10, nocast=2)
        self.assertFalse(blocked.accepted)
        self.assertEqual(blocked.item_reads, 0)
        self.assertEqual(submission.selection.rng_draws_consumed, 1)
        with self.assertRaisesRegex(CombinedDirectMagicDomain, "slot 0 witness"):
            submission.direct_magic_route(current_mp=10)
        accepted = submission.direct_magic_route(current_mp=10, item_zero=RuntimeItemZeroWitness(False))
        self.assertEqual(accepted.remaining_mp, 11)

    def test_unknown_item_pool_cannot_be_fabricated_as_zero_mp(self):
        with self.assertRaisesRegex(CombinedDirectMagicDomain, "slot 0 witness"):
            route(effect="att_reverse", current_mp=0)

    def test_witnessed_invalid_item_preserves_negative_accessor_and_mp_gain(self):
        for effect in ("recovery", "status_change", "status_recovery", "att_reverse"):
            result = route(effect=effect, current_mp=10, item_zero=RuntimeItemZeroWitness(False))
            self.assertEqual(result.mp_argument, -1)
            self.assertEqual(result.remaining_mp, 11)
            self.assertTrue(result.accepted)

    def test_real_positive_mp_cost_can_reject_or_deduct(self):
        for mp, accepted, after in ((6, False, 6), (7, True, 0), (10, True, 3)):
            result = route(effect="status_recovery", current_mp=mp,
                           item_zero=RuntimeItemZeroWitness(True, 7))
            self.assertEqual((result.accepted, result.remaining_mp), (accepted, after))

    def test_nocast_precedes_item_read_even_with_absent_pool_witness(self):
        result = route(effect="recovery", current_mp=10, nocast=1)
        self.assertEqual((result.item_reads, result.wrapper_calls, result.remaining_mp), (0, 0, 10))

    def test_recovery_all_selector_rejects_after_mp_deduction(self):
        result = route(effect="recovery", current_mp=10, target_slot=22,
                       item_zero=RuntimeItemZeroWitness(True, 3))
        self.assertEqual((result.accepted, result.remaining_mp, result.battle_effect_calls), (False, 7, 0))

    def test_recovery_discards_helper_failure_others_propagate_it(self):
        for effect, accepted in (("recovery", True), ("status_change", False),
                                 ("status_recovery", False), ("att_reverse", False)):
            result = route(effect=effect, current_mp=10,
                           item_zero=RuntimeItemZeroWitness(True, 0), battle_effect_return=False)
            self.assertEqual(result.accepted, accepted)

    def test_missing_function_still_reads_item_but_does_not_call_wrapper(self):
        result = route(effect="recovery", current_mp=10,
                       item_zero=RuntimeItemZeroWitness(False), function_present=False)
        self.assertEqual((result.item_reads, result.wrapper_calls, result.remaining_mp), (1, 0, 10))

    def test_invalid_caster_or_init_does_not_deduct_mp(self):
        for flags in ({"caster_valid": False}, {"battle_mode_init": True}):
            result = route(effect="att_reverse", current_mp=10,
                           item_zero=RuntimeItemZeroWitness(True, 3), **flags)
            self.assertEqual(result.remaining_mp, 10)
            self.assertEqual(result.battle_effect_calls, 0)

    def test_outside_bounded_routes_reject(self):
        for flags in ({"family_index": 1}, {"battling": False}, {"current_mp": 2**31-1}):
            args = dict(effect="att_reverse", current_mp=10, item_zero=RuntimeItemZeroWitness(False))
            args.update(flags)
            with self.assertRaises(CombinedDirectMagicDomain):
                route(**args)

    def test_item_witness_distinguishes_invalid_unknown_and_valid(self):
        for args in ((True,), (False, 0), (1, 0), (True, 2**31)):
            with self.assertRaises(CombinedDirectMagicDomain):
                RuntimeItemZeroWitness(*args)


if __name__ == "__main__":
    unittest.main()
