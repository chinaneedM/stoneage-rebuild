import unittest

from tools.stoneage_attack_magic_damage_model import (
    ElementAttrs,
    MagicExpState,
    apply_attack_magic_hp,
    apply_true_magic_penalty,
    attack_magic_effect_value,
    attack_magic_hit_clears_sleep,
    attack_magic_ride_ratio,
    attack_magic_training,
    attacker_magic_proficiency,
    attacker_training_applies,
    defense_magic_training,
    effective_magic_resistance,
    field_attribute_power,
    fixed_magic_base_power,
    magic_attribute_adjust,
    magic_dodge_threshold,
    resolve_fixed_magic_hit_damage,
    true_magic_success,
)


class StoneAgeAttackMagicDamageModelTests(unittest.TestCase):
    def test_enemy_and_pet_proficiency_sources_stay_distinct(self):
        self.assertEqual(
            attacker_magic_proficiency(
                actor_kind="enemy",
                level=99,
                stored_proficiency=7,
            ),
            (89, False),
        )
        self.assertEqual(
            attacker_magic_proficiency(
                actor_kind="pet",
                level=99,
                stored_proficiency=7,
            ),
            (7, True),
        )

    def test_resistance_includes_active_fixed_source_modifiers(self):
        self.assertEqual(
            effective_magic_resistance(
                actor_kind="player",
                level=1,
                stored_resistance=40,
                equipment_resistance=10,
                magic_defense_percent=20,
            ),
            60,
        )
        self.assertEqual(
            effective_magic_resistance(
                actor_kind="enemy",
                level=99,
                stored_resistance=0,
            ),
            49,
        )

    def test_true_magic_check_is_zero_based_and_inclusive(self):
        self.assertTrue(
            true_magic_success(
                proficiency=0,
                roll_0_99=0,
            )
        )
        self.assertFalse(
            true_magic_success(
                proficiency=0,
                roll_0_99=1,
            )
        )

    def test_magic_dodge_uses_player_and_nonplayer_branches(self):
        self.assertEqual(
            magic_dodge_threshold(
                actor_kind="player",
                level=1,
                luck=10,
                base_resistance=20,
                equipment_quimagic=10,
            ),
            42,
        )
        self.assertEqual(
            magic_dodge_threshold(
                actor_kind="enemy",
                level=200,
            ),
            30,
        )

    def test_fixed_base_power_reconstructs_kmagic_formula(self):
        self.assertEqual(
            fixed_magic_base_power(
                power=100,
                magic_level=1,
                attacker_proficiency=50,
                defender_resistance=20,
                random_0_19=0,
            ),
            110,
        )

    def test_field_adjust_bottom_and_full_matching_field(self):
        self.assertAlmostEqual(
            field_attribute_power(
                field_element=None,
                field_power=100,
                attrs=ElementAttrs(100, 0, 0, 0, 0),
            ),
            0.5,
        )
        self.assertAlmostEqual(
            field_attribute_power(
                field_element=0,
                field_power=100,
                attrs=ElementAttrs(100, 0, 0, 0, 0),
            ),
            1.0,
        )

    def test_magic_attribute_adjust_preserves_integer_traction(self):
        value = magic_attribute_adjust(
            damage=100,
            magic_level=1,
            element=0,
            attacker_attrs=ElementAttrs(100, 0, 0, 0, 0),
            defender_attrs=ElementAttrs(0, 100, 0, 0, 0),
            field_element=None,
            field_power=0,
        )
        self.assertEqual(value, 45)

    def test_failed_true_magic_cast_applies_int_point_seven(self):
        self.assertEqual(
            apply_true_magic_penalty(
                101,
                success=False,
            ),
            70,
        )

    def test_non_dodged_hit_resolution_order_is_stable(self):
        result = resolve_fixed_magic_hit_damage(
            power=100,
            magic_level=1,
            element=0,
            attacker_proficiency=50,
            defender_resistance=20,
            attacker_attrs=ElementAttrs(100, 0, 0, 0),
            defender_attrs=ElementAttrs(0, 100, 0, 0),
            field_element=None,
            field_power=0,
            damage_random_0_19=0,
            true_magic=False,
        )
        self.assertEqual(
            (
                result.base_power,
                result.attribute_adjusted,
                result.final_damage,
            ),
            (110, 49, 34),
        )

    def test_attack_magic_ride_ratio_uses_pure_attribute_contrast(self):
        self.assertEqual(
            attack_magic_effect_value(
                positive_attr=100,
                negative_attr=0,
            ),
            10,
        )
        self.assertEqual(
            attack_magic_ride_ratio(
                element=0,
                rider_attrs=ElementAttrs(0, 100, 0, 0),
                pet_attrs=ElementAttrs(100, 0, 0, 0),
            ),
            7,
        )

    def test_rider_overkill_source_quirk_can_inflate_pet_damage(self):
        result = apply_attack_magic_hp(
            damage=100,
            rider_hp=10,
            ride_pet_hp=100,
            ride_ratio=8,
        )
        self.assertEqual(result.reported_rider_damage, 80)
        self.assertEqual(result.rider_hp, 0)
        self.assertEqual(result.pet_damage, 170)
        self.assertEqual(result.pet_hp, 0)
        self.assertTrue(result.unmounted)

    def test_exact_zero_ride_pet_does_not_unmount_in_this_branch(self):
        result = apply_attack_magic_hp(
            damage=100,
            rider_hp=100,
            ride_pet_hp=20,
            ride_ratio=8,
        )
        self.assertEqual(result.rider_hp, 20)
        self.assertEqual(result.pet_hp, 0)
        self.assertEqual(result.pet_damage, 20)
        self.assertFalse(result.unmounted)

    def test_attack_and_defense_training_transitions(self):
        attack = attack_magic_training(
            MagicExpState(10, 95, 5, 1),
            magic_level=2,
            target_count=1,
        )
        self.assertEqual(
            attack,
            MagicExpState(11, 0, 4, 0),
        )

        defense = defense_magic_training(
            MagicExpState(10, 90, 5, 1),
            magic_level=2,
            damage=200,
        )
        self.assertEqual(
            defense,
            MagicExpState(11, 0, 4, 90),
        )

    def test_training_and_sleep_gates_match_execution_order(self):
        self.assertTrue(
            attacker_training_applies(
                training_actor=True,
                true_magic=False,
            )
        )
        self.assertFalse(
            attacker_training_applies(
                training_actor=False,
                true_magic=False,
            )
        )
        self.assertTrue(
            attack_magic_hit_clears_sleep(
                dodged=False,
            )
        )
        self.assertFalse(
            attack_magic_hit_clears_sleep(
                dodged=True,
            )
        )


if __name__ == "__main__":
    unittest.main()
