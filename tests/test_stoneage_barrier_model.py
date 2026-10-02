import unittest
from dataclasses import replace

from tools.stoneage_barrier_model import (
    BarrierCheckInputs,
    BarrierOption,
    BarrierUndefinedSourceDomain,
    barrier_blocks_action,
    barrier_probability_value,
    parse_barrier_option,
    resolve_barrier_multilist,
    resolve_barrier_self_tick,
    resolve_barrier_target,
)


def inputs(**changes):
    return replace(
        BarrierCheckInputs(
            20,20,False,0,
            25,25,25,25,
            0,0,False,
        ),
        **changes,
    )


class BarrierModelTests(unittest.TestCase):
    def test_option_codecs_converge(self):
        for codec in ("cp950","big5","utf-8"):
            self.assertEqual(
                parse_barrier_option(
                    "turn=3 成=50".encode(codec),
                    encoding=codec,
                ),
                BarrierOption(3,50),
            )

    def test_sequential_success_search_ignores_marker_before_turn(self):
        self.assertEqual(
            parse_barrier_option(
                "成=99 turn=4 成=25".encode("big5"),
                encoding="big5",
            ),
            BarrierOption(4,25),
        )

    def test_missing_or_malformed_turn_is_undefined(self):
        for raw in ("成=50","turn=x 成=50","turn"):
            with self.subTest(raw=raw):
                with self.assertRaises(BarrierUndefinedSourceDomain):
                    parse_barrier_option(raw.encode("big5"),encoding="big5")

    def test_missing_success_retains_initialized_zero(self):
        self.assertEqual(
            parse_barrier_option(b"turn=3",encoding="big5"),
            BarrierOption(3,0),
        )

    def test_probability_and_strict_hit_boundary(self):
        self.assertEqual(barrier_probability_value(inputs(),50),40)
        self.assertEqual(
            resolve_barrier_target(
                inputs(),BarrierOption(3,50),roll_1_100=39
            ).counter_written,
            4,
        )
        self.assertIsNone(
            resolve_barrier_target(
                inputs(),BarrierOption(3,50),roll_1_100=40
            ).counter_written
        )

    def test_existing_status_blocks_before_rng(self):
        blocked=resolve_barrier_target(
            inputs(any_existing_status=True),
            BarrierOption(3,50),
            roll_1_100=None,
        )
        self.assertFalse(blocked.rng_consumed)
        with self.assertRaises(ValueError):
            resolve_barrier_target(
                inputs(any_existing_status=True),
                BarrierOption(3,50),
                roll_1_100=1,
            )

    def test_general_mod_and_suit_resistance_are_explicit(self):
        self.assertEqual(
            barrier_probability_value(
                inputs(
                    defender_mod_barrier=3,
                    defender_suit_resist=4,
                ),
                50,
            ),
            33,
        )

    def test_self_freeze_is_preserved_not_normalized(self):
        frozen=resolve_barrier_self_tick(4)
        self.assertEqual(
            (
                frozen.decremented_local_counter,
                frozen.counter_after,
                frozen.expired,
                frozen.self_freeze_restored_storage,
            ),
            (3,4,False,True),
        )
        expired=resolve_barrier_self_tick(1)
        self.assertEqual(
            (
                expired.decremented_local_counter,
                expired.counter_after,
                expired.expired,
                expired.self_freeze_restored_storage,
            ),
            (0,0,True,False),
        )
        weaken_edge=resolve_barrier_self_tick(
            1,
            weaken_active_at_visit=True,
        )
        self.assertEqual(
            (
                weaken_edge.decremented_local_counter,
                weaken_edge.counter_after,
                weaken_edge.expired,
                weaken_edge.self_freeze_restored_storage,
            ),
            (0,1,True,True),
        )

    def test_positive_barrier_blocks_action(self):
        self.assertTrue(barrier_blocks_action(1))
        self.assertFalse(barrier_blocks_action(0))

    def test_multilist_single_retarget_and_rows(self):
        self.assertEqual(
            resolve_barrier_multilist(
                3,
                alive_slots=(1,4,11),
                retarget_draws_0_9=(9,8,1),
            ).slots,
            (4,),
        )
        self.assertEqual(
            resolve_barrier_multilist(
                20,
                alive_slots=(8,3,12),
            ).slots,
            (3,8),
        )

    def test_multilist_unsafe_target_all_fails_closed(self):
        with self.assertRaises(BarrierUndefinedSourceDomain):
            resolve_barrier_multilist(22,alive_slots=(0,10))


if __name__=="__main__":
    unittest.main()
