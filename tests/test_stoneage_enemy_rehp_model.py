import unittest

from tools.stoneage_enemy_rehp_model import (
    PROFILE_BISMARCK,
    PROFILE_GAVIN_IRIS,
    EnemyReHpAllyState,
    EnemyReHpRolls,
    enemy_rehp_command_code,
    resolve_enemy_rehp_effect,
)


def ally(slot, hp, max_hp=900):
    return EnemyReHpAllyState(f"enemy:{slot}", slot, hp, max_hp)


class EnemyReHpModelTests(unittest.TestCase):
    def test_guarded_command_numbers_are_profile_specific(self):
        self.assertEqual(enemy_rehp_command_code(PROFILE_GAVIN_IRIS), 2014)
        self.assertEqual(enemy_rehp_command_code(PROFILE_BISMARCK), 2013)
        with self.assertRaisesRegex(ValueError, "evidenced descendant profile"):
            enemy_rehp_command_code("recovered25-unknown")

    def test_wounded_threshold_is_strict_two_thirds_integer_boundary(self):
        self.assertTrue(ally(10, 599).eligible)
        self.assertFalse(ally(10, 600).eligible)
        self.assertFalse(ally(10, 0).eligible)
        # C integer threshold for 901 max HP is floor(1802/3)=600.
        self.assertTrue(ally(10, 599, 901).eligible)
        self.assertFalse(ally(10, 600, 901).eligible)

    def test_success_consumes_target_power_and_multirecovery_rolls_in_order(self):
        resolved = resolve_enemy_rehp_effect(
            adjusted_attack_target_slot=2,
            allies_by_slot={
                10: ally(10, 700),
                12: ally(12, 200),
                15: ally(15, 300),
            },
            rolls=EnemyReHpRolls(
                target_index=1,
                base_power=500,
                heal_variance=550,
            ),
        )
        self.assertEqual(resolved.eligible_slots, (12, 15))
        self.assertEqual(resolved.healed_slot, 15)
        self.assertEqual(resolved.base_power, 500)
        self.assertEqual(resolved.reported_heal, 550)
        self.assertEqual(resolved.effective_heal, 550)
        self.assertEqual(resolved.hp_before, 300)
        self.assertEqual(resolved.hp_after, 850)
        self.assertEqual(resolved.allies_after[15].hp, 850)
        self.assertFalse(resolved.fallback_to_attack)

    def test_heal_caps_hp_but_preserves_reported_up_point(self):
        resolved = resolve_enemy_rehp_effect(
            adjusted_attack_target_slot=0,
            allies_by_slot={10: ally(10, 100, 300)},
            rolls=EnemyReHpRolls(0, 300, 330),
        )
        self.assertEqual(resolved.reported_heal, 330)
        self.assertEqual(resolved.effective_heal, 200)
        self.assertEqual(resolved.hp_after, 300)

    def test_no_eligible_ally_falls_back_without_effect_rng(self):
        resolved = resolve_enemy_rehp_effect(
            adjusted_attack_target_slot=4,
            allies_by_slot={10: ally(10, 600), 11: ally(11, 0)},
            rolls=EnemyReHpRolls(),
        )
        self.assertFalse(resolved.success)
        self.assertTrue(resolved.fallback_to_attack)
        self.assertEqual(resolved.adjusted_attack_target_slot, 4)
        with self.assertRaisesRegex(ValueError, "must not consume effect RNG"):
            resolve_enemy_rehp_effect(
                adjusted_attack_target_slot=4,
                allies_by_slot={10: ally(10, 600)},
                rolls=EnemyReHpRolls(target_index=0),
            )

    def test_inactive_caster_falls_back_before_rehp_rng(self):
        resolved = resolve_enemy_rehp_effect(
            adjusted_attack_target_slot=1,
            allies_by_slot={10: ally(10, 100)},
            rolls=EnemyReHpRolls(),
            caster_mode_ready=False,
        )
        self.assertFalse(resolved.success)
        self.assertTrue(resolved.fallback_to_attack)

    def test_rng_bounds_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "target-selection"):
            resolve_enemy_rehp_effect(
                adjusted_attack_target_slot=0,
                allies_by_slot={10: ally(10, 100)},
                rolls=EnemyReHpRolls(1, 100, 90),
            )
        with self.assertRaisesRegex(ValueError, "base-power"):
            resolve_enemy_rehp_effect(
                adjusted_attack_target_slot=0,
                allies_by_slot={10: ally(10, 100)},
                rolls=EnemyReHpRolls(0, 99, 90),
            )
        with self.assertRaisesRegex(ValueError, "MultiRecovery"):
            resolve_enemy_rehp_effect(
                adjusted_attack_target_slot=0,
                allies_by_slot={10: ally(10, 100)},
                rolls=EnemyReHpRolls(0, 500, 551),
            )

    def test_reversed_rand_range_is_not_invented(self):
        with self.assertRaisesRegex(ValueError, "reversed range"):
            resolve_enemy_rehp_effect(
                adjusted_attack_target_slot=0,
                allies_by_slot={10: ally(10, 10, 90)},
                rolls=EnemyReHpRolls(0, 100, 90),
            )


if __name__ == "__main__":
    unittest.main()
