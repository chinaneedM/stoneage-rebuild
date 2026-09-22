import unittest

from tools.stoneage_battle_status_model import (
    BaseBattleStatusState,
    BaseStatusAttackInputs,
    BaseStatusTickInputs,
    STATUS_PARALYSIS,
    STATUS_POISON,
    apply_base_status_counter,
    base_status_name_from_index,
    base_poison_damage,
    base_status_can_move,
    base_stone_defense_multiplier,
    resolve_base_damage_wakeup,
    resolve_base_status_attack_check,
    resolve_base_status_tick,
)


class BattleStatusModelTests(unittest.TestCase):
    def test_status_index_mapping_is_common_base_only(self):
        self.assertEqual(base_status_name_from_index(1),STATUS_POISON)
        self.assertEqual(base_status_name_from_index(2),STATUS_PARALYSIS)
        with self.assertRaises(ValueError):
            base_status_name_from_index(7)

    def test_existing_status_blocks_new_status_without_rng(self):
        result=resolve_base_status_attack_check(
            BaseStatusAttackInputs(
                status=STATUS_POISON,
                attacker_level=10,
                defender_level=10,
                pvp=False,
                attacker_fixed_luck=0,
                defender_vital=25,
                defender_str=25,
                defender_tough=25,
                defender_dex=25,
                defender_resistance=0,
                per_offset=15,
                level_range=30,
                level_scale=1.0,
            ),
            BaseBattleStatusState(sleep=2),
            roll_1_100=None,
        )
        self.assertFalse(result.eligible)
        self.assertTrue(result.blocked_by_existing_status)
        self.assertFalse(result.rng_consumed)

    def test_paralysis_uses_fixed_twenty_minus_resistance_and_strict_less_than(self):
        inputs=BaseStatusAttackInputs(
            status=STATUS_PARALYSIS,
            attacker_level=99,
            defender_level=1,
            pvp=False,
            attacker_fixed_luck=50,
            defender_vital=90,
            defender_str=1,
            defender_tough=1,
            defender_dex=1,
            defender_resistance=3,
            per_offset=99,
            level_range=30,
            level_scale=1.0,
        )
        hit=resolve_base_status_attack_check(
            inputs,BaseBattleStatusState(),roll_1_100=16
        )
        boundary=resolve_base_status_attack_check(
            inputs,BaseBattleStatusState(),roll_1_100=17
        )
        self.assertEqual(hit.source_probability_value,17)
        self.assertTrue(hit.success)
        self.assertFalse(boundary.success)

    def test_general_status_formula_uses_vital_share_level_luck_and_resistance(self):
        inputs=BaseStatusAttackInputs(
            status=STATUS_POISON,
            attacker_level=30,
            defender_level=10,
            pvp=False,
            attacker_fixed_luck=5,
            defender_vital=25,
            defender_str=25,
            defender_tough=25,
            defender_dex=25,
            defender_resistance=3,
            per_offset=15,
            level_range=30,
            level_scale=1.0,
        )
        hit=resolve_base_status_attack_check(
            inputs,BaseBattleStatusState(),roll_1_100=26
        )
        boundary=resolve_base_status_attack_check(
            inputs,BaseBattleStatusState(),roll_1_100=27
        )
        self.assertEqual(hit.source_probability_value,27)
        self.assertTrue(hit.success)
        self.assertFalse(boundary.success)

    def test_general_status_caps_only_upper_end_and_pvp_removes_level_delta(self):
        capped=resolve_base_status_attack_check(
            BaseStatusAttackInputs(
                status=STATUS_POISON,
                attacker_level=100,
                defender_level=1,
                pvp=False,
                attacker_fixed_luck=100,
                defender_vital=1,
                defender_str=99,
                defender_tough=0,
                defender_dex=0,
                defender_resistance=0,
                per_offset=100,
                level_range=30,
                level_scale=2.0,
            ),
            BaseBattleStatusState(),
            roll_1_100=79,
        )
        self.assertEqual(capped.source_probability_value,80)
        self.assertTrue(capped.success)
        self.assertFalse(
            resolve_base_status_attack_check(
                BaseStatusAttackInputs(
                    status=STATUS_POISON,
                    attacker_level=1,
                    defender_level=100,
                    pvp=True,
                    attacker_fixed_luck=0,
                    defender_vital=100,
                    defender_str=0,
                    defender_tough=0,
                    defender_dex=0,
                    defender_resistance=50,
                    per_offset=15,
                    level_range=30,
                    level_scale=1.0,
                ),
                BaseBattleStatusState(),
                roll_1_100=1,
            ).success
        )

    def test_apply_base_status_counter_sets_exact_magic_turn(self):
        self.assertEqual(
            apply_base_status_counter(
                BaseBattleStatusState(),
                status=STATUS_POISON,
                turn=3,
            ).poison,
            3,
        )

    def test_can_move_common_base_blockers(self):
        self.assertFalse(
            base_status_can_move(BaseBattleStatusState(paralysis=1))
        )
        self.assertFalse(base_status_can_move(BaseBattleStatusState(sleep=1)))
        self.assertFalse(base_status_can_move(BaseBattleStatusState(stone=1)))
        self.assertTrue(
            base_status_can_move(
                BaseBattleStatusState(poison=2,confusion=2,drunk=2)
            )
        )

    def test_expiring_paralysis_still_consumes_current_action(self):
        result=resolve_base_status_tick(
            BaseStatusTickInputs(
                hp=100,
                status=BaseBattleStatusState(paralysis=1),
            )
        )
        self.assertFalse(result.can_move_before_decrement)
        self.assertTrue(result.can_move_after_tick)
        self.assertEqual(result.status_after.paralysis,0)
        self.assertEqual(result.command_override,"none")
        self.assertEqual(result.expired_statuses,("paralysis",))

    def test_poison_decrements_before_damage_and_never_kills(self):
        damage,hp_after=base_poison_damage(10,10000)
        self.assertEqual((damage,hp_after),(9,1))

        active=resolve_base_status_tick(
            BaseStatusTickInputs(
                hp=10,
                status=BaseBattleStatusState(poison=2),
                poison_stat_sum=10000,
            )
        )
        self.assertEqual(active.status_after.poison,1)
        self.assertEqual(active.poison_damage,9)
        self.assertEqual(active.hp_after,1)

        expiring=resolve_base_status_tick(
            BaseStatusTickInputs(
                hp=10,
                status=BaseBattleStatusState(poison=1),
            )
        )
        self.assertEqual(expiring.status_after.poison,0)
        self.assertEqual(expiring.poison_damage,0)
        self.assertEqual(expiring.hp_after,10)

    def test_confusion_boundary_and_increment_before_target_probe(self):
        rewritten=resolve_base_status_tick(
            BaseStatusTickInputs(
                hp=100,
                status=BaseBattleStatusState(confusion=2),
                actor_slot=0,
                valid_target_slots=(0,2,11),
                confusion_action_roll_1_100=80,
                confusion_side_roll_0_1=0,
                confusion_pos_roll_0_9=9,
            )
        )
        self.assertTrue(rewritten.confusion_rewrote_command)
        self.assertEqual(rewritten.command_override,"attack")
        self.assertEqual(rewritten.target_override,2)

        untouched=resolve_base_status_tick(
            BaseStatusTickInputs(
                hp=100,
                status=BaseBattleStatusState(confusion=2),
                actor_slot=0,
                valid_target_slots=(2,),
                confusion_action_roll_1_100=81,
            )
        )
        self.assertFalse(untouched.confusion_rewrote_command)
        self.assertIsNone(untouched.command_override)
        self.assertIsNone(untouched.target_override)

    def test_expiring_immobilizer_can_be_overridden_by_live_confusion(self):
        result=resolve_base_status_tick(
            BaseStatusTickInputs(
                hp=100,
                status=BaseBattleStatusState(
                    paralysis=1,
                    confusion=2,
                ),
                actor_slot=0,
                valid_target_slots=(10,),
                confusion_action_roll_1_100=1,
                confusion_side_roll_0_1=1,
                confusion_pos_roll_0_9=9,
            )
        )
        self.assertFalse(result.can_move_before_decrement)
        self.assertTrue(result.can_move_after_tick)
        self.assertEqual(result.command_override,"attack")
        self.assertEqual(result.target_override,10)

    def test_nonexpiring_immobilizer_suppresses_confusion_rewrite(self):
        result=resolve_base_status_tick(
            BaseStatusTickInputs(
                hp=100,
                status=BaseBattleStatusState(
                    paralysis=2,
                    confusion=2,
                ),
                actor_slot=0,
                valid_target_slots=(10,),
                confusion_action_roll_1_100=1,
                confusion_side_roll_0_1=1,
                confusion_pos_roll_0_9=9,
            )
        )
        self.assertTrue(result.confusion_rewrote_command)
        self.assertFalse(result.can_move_after_tick)
        self.assertEqual(result.command_override,"none")
        self.assertEqual(result.target_override,10)

    def test_drunk_expiration_restores_quick_by_source_branch(self):
        solo=resolve_base_status_tick(
            BaseStatusTickInputs(
                hp=100,
                status=BaseBattleStatusState(drunk=1),
                work_quick=40,
            )
        )
        self.assertEqual(solo.work_quick_after,80)

        riding=resolve_base_status_tick(
            BaseStatusTickInputs(
                hp=100,
                status=BaseBattleStatusState(drunk=1),
                work_quick=40,
                ride_work_quick=30,
            )
        )
        self.assertEqual(riding.work_quick_after,70)

    def test_positive_damage_wakes_sleep_and_increments_damage_count(self):
        status=BaseBattleStatusState(sleep=3)
        wake=resolve_base_damage_wakeup(
            status,
            damage_count_before=4,
            damage=1,
        )
        self.assertTrue(wake.wakeup_applied)
        self.assertTrue(wake.sleep_was_cleared)
        self.assertEqual(wake.status_after.sleep,0)
        self.assertEqual(wake.damage_count_after,5)

        blocked=resolve_base_damage_wakeup(
            status,
            damage_count_before=4,
            damage=10,
            absorb_or_vanish=True,
        )
        self.assertFalse(blocked.wakeup_applied)
        self.assertEqual(blocked.status_after.sleep,3)
        self.assertEqual(blocked.damage_count_after,4)

    def test_stone_defense_multiplier_is_binary(self):
        self.assertEqual(
            base_stone_defense_multiplier(BaseBattleStatusState()),
            1.0,
        )
        self.assertEqual(
            base_stone_defense_multiplier(BaseBattleStatusState(stone=1)),
            2.0,
        )


if __name__ == "__main__":
    unittest.main()
