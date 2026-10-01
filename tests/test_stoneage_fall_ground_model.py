import unittest

from tools.stoneage_fall_ground_model import (
    fall_ground_attack_power,
    parse_fall_ground_option,
    resolve_fall_ground,
)


class FallGroundModelTests(unittest.TestCase):
    def test_attack_percent_is_additive_from_fixed_strength(self):
        opt=parse_fall_ground_option("攻%50")
        self.assertTrue(opt.marker_present)
        self.assertEqual(opt.attack_percent,50.0)
        self.assertEqual(fall_ground_attack_power(101,opt),151)

    def test_marker_without_float_preserves_source_default_001_percent(self):
        opt=parse_fall_ground_option("攻%oops")
        self.assertTrue(opt.marker_present)
        self.assertIsNone(opt.attack_percent)
        self.assertEqual(fall_ground_attack_power(10000,opt),10001)

    def test_absent_marker_does_not_define_new_attack_power(self):
        opt=parse_fall_ground_option("none")
        self.assertFalse(opt.marker_present)
        with self.assertRaisesRegex(ValueError,"prior WORKATTACKPOWER"):
            fall_ground_attack_power(100,opt)

    def test_roll_is_consumed_even_when_player_is_not_mounted(self):
        result=resolve_fall_ground(
            post_damage_player_damage=10,
            damage_react=0,
            same_side=False,
            target_kind="player",
            ride_pet_slot=None,
            fall_roll_0_100=100,
            equipment_fall_resistance=0,
            use_equipment_resistance=True,
            prevent_same_side=True,
        )
        self.assertTrue(result.rng_consumed)
        self.assertTrue(result.roll_passed)
        self.assertFalse(result.fell)

    def test_pinned_unfixed_slot_zero_bug_is_preserved(self):
        result=resolve_fall_ground(
            post_damage_player_damage=10,
            damage_react=0,
            same_side=False,
            target_kind="player",
            ride_pet_slot=0,
            fall_roll_0_100=100,
            use_equipment_resistance=False,
            prevent_same_side=False,
        )
        self.assertTrue(result.roll_passed)
        self.assertFalse(result.fell)
        fixed=resolve_fall_ground(
            post_damage_player_damage=10,
            damage_react=0,
            same_side=False,
            target_kind="player",
            ride_pet_slot=0,
            fall_roll_0_100=100,
            use_equipment_resistance=False,
            prevent_same_side=False,
            fix_petfall=True,
        )
        self.assertTrue(fixed.fell)

    def test_equipment_resistance_changes_strict_threshold(self):
        common=dict(
            post_damage_player_damage=10,
            damage_react=0,
            same_side=False,
            target_kind="player",
            ride_pet_slot=1,
            fall_roll_0_100=60,
            prevent_same_side=True,
        )
        self.assertTrue(resolve_fall_ground(
            **common,
            equipment_fall_resistance=0,
            use_equipment_resistance=True,
        ).fell)
        blocked=resolve_fall_ground(
            **common,
            equipment_fall_resistance=10,
            use_equipment_resistance=True,
        )
        self.assertFalse(blocked.roll_passed)

    def test_same_side_prevention_is_compile_profile_specific(self):
        kwargs=dict(
            post_damage_player_damage=10,
            damage_react=0,
            same_side=True,
            target_kind="player",
            ride_pet_slot=1,
            equipment_fall_resistance=0,
            use_equipment_resistance=False,
        )
        blocked=resolve_fall_ground(
            **kwargs,fall_roll_0_100=None,prevent_same_side=True
        )
        self.assertFalse(blocked.rng_consumed)
        allowed=resolve_fall_ground(
            **kwargs,fall_roll_0_100=100,prevent_same_side=False
        )
        self.assertTrue(allowed.fell)

    def test_damage_or_reaction_gate_rejects_rng(self):
        for damage,react in ((0,0),(10,1)):
            result=resolve_fall_ground(
                post_damage_player_damage=damage,
                damage_react=react,
                same_side=False,
                target_kind="player",
                ride_pet_slot=1,
                fall_roll_0_100=None,
                use_equipment_resistance=False,
                prevent_same_side=False,
            )
            self.assertFalse(result.rng_consumed)


if __name__=="__main__":
    unittest.main()
