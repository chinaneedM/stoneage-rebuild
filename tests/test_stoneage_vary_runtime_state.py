import unittest
from dataclasses import replace

from tools.stoneage_vary_runtime_state import (
    PROFILE_BISMARCK_ATTACK_DEFENSE_QUICK,
    PROFILE_GAVIN_IRIS_ATTACK_QUICK,
    VARY_WOLF_IMAGE,
    advance_vary_after_actor_action,
    cast_vary,
    create_vary_participant_runtime,
    teardown_vary,
)


def runtime(profile=PROFILE_GAVIN_IRIS_ATTACK_QUICK, tempno=981):
    return create_vary_participant_runtime(
        profile=profile,
        tempno=tempno,
        base_image=101427,
        fixed_attack=101,
        fixed_defense=81,
        fixed_quick=91,
    )


class VaryRuntimeStateTests(unittest.TestCase):
    def test_profile_divergence_is_explicit_and_c_truncation_is_preserved(self):
        gi = cast_vary(runtime())
        self.assertEqual(gi.base_image, VARY_WOLF_IMAGE)
        self.assertEqual(gi.work_turn, 0)
        self.assertEqual(gi.attack_power, 131)
        self.assertEqual(gi.defense_power, 81)
        self.assertEqual(gi.quick, 118)
        self.assertTrue(gi.visual_effect_enabled)

        bi = cast_vary(runtime(PROFILE_BISMARCK_ATTACK_DEFENSE_QUICK))
        self.assertEqual(bi.attack_power, 131)
        self.assertEqual(bi.defense_power, 41)
        self.assertEqual(bi.quick, 118)
        self.assertFalse(bi.visual_effect_enabled)

    def test_only_four_source_gated_wolves_are_admitted(self):
        for tempno in (981, 982, 983, 984):
            self.assertEqual(runtime(tempno=tempno).tempno, tempno)
        with self.assertRaisesRegex(ValueError, "981..984"):
            runtime(tempno=985)

    def test_recast_is_blocked_while_default_wolf_image_is_active(self):
        state = cast_vary(runtime())
        self.assertTrue(state.blocks_recast)
        with self.assertRaisesRegex(ValueError, "recast"):
            cast_vary(state)

    def test_six_actor_actions_include_initial_vary_action(self):
        state = cast_vary(runtime())
        for expected_turn in range(1, 6):
            state, tick = advance_vary_after_actor_action(state)
            self.assertFalse(tick.expired)
            self.assertEqual(state.work_turn, expected_turn)
            self.assertTrue(state.active)
        state, tick = advance_vary_after_actor_action(state)
        self.assertTrue(tick.expired)
        self.assertFalse(state.active)
        self.assertEqual(state.base_image, 101427)
        self.assertEqual(state.work_turn, 0)
        self.assertEqual(
            (state.attack_power, state.defense_power, state.quick),
            (101, 81, 91),
        )

    def test_gavin_iris_expiry_does_not_claim_defense_restoration(self):
        state = cast_vary(runtime())
        state = replace(state, work_turn=5, defense_power=73)
        state, tick = advance_vary_after_actor_action(state)
        self.assertTrue(tick.expired)
        self.assertEqual(state.defense_power, 73)
        self.assertEqual((state.attack_power, state.quick), (101, 91))

    def test_bismarck_expiry_restores_defense_too(self):
        state = cast_vary(runtime(PROFILE_BISMARCK_ATTACK_DEFENSE_QUICK))
        state = replace(state, work_turn=5, defense_power=17)
        state, tick = advance_vary_after_actor_action(state)
        self.assertTrue(tick.expired)
        self.assertEqual(state.defense_power, 81)

    def test_teardown_restores_nonwolf_image_and_profile_owned_stats(self):
        state = cast_vary(runtime())
        state = teardown_vary(state)
        self.assertFalse(state.active)
        self.assertEqual(state.base_image, 101427)
        self.assertEqual((state.attack_power, state.quick), (101, 91))

    def test_inactive_actor_action_has_no_vary_tick(self):
        state, tick = advance_vary_after_actor_action(runtime())
        self.assertIsNone(tick)
        self.assertEqual(state.work_turn, 0)


if __name__ == "__main__":
    unittest.main()
