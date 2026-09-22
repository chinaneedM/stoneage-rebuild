import unittest

from tools.stoneage_battle_status_model import BaseBattleStatusState

from tools.stoneage_petskill_core_model import (
    abduct_command,
    abduct_probability,
    abduct_transition,
    charge_attack_command,
    charge_execution_step,
    continuation_attack_command,
    continuation_execution,
    earth_round_attack_transition,
    earth_round_command,
    earth_round_hide_transition,
    guard_break_command,
    guard_break_gate,
    guardian_command,
    guardian_redirect_allowed,
    merge_transition,
    mighty_command,
    mighty_execution,
    no_guard_command,
    no_guard_execution,
    parse_status_skill,
    power_balance_command,
    skill_none,
    skill_normal_attack,
    skill_normal_guard,
    status_attack_application,
    status_attack_probability,
    status_attack_transition,
    status_change_command,
    steal_command,
    steal_transition,
)


STATUS = ("NONE", "POISON", "PARALYSIS", "SLEEP", "STONE", "DRUNK", "CONFUSION")


class StoneAgePetSkillCoreModelTests(unittest.TestCase):
    def test_none_attack_guard_commands(self):
        self.assertEqual(skill_none(3)["command"], "NONE")
        self.assertEqual(skill_normal_attack(12)["command"], "ATTACK")
        self.assertEqual(skill_normal_guard(5)["command"], "GUARD")
        self.assertEqual(skill_normal_attack(12)["mode"], "C_OK")

    def test_continuation_attack_count_range(self):
        self.assertEqual(continuation_attack_command(10, "3")["low"], 3)
        self.assertEqual(continuation_attack_command(10, "0")["low"], 1)
        self.assertEqual(continuation_attack_command(10, "11")["low"], 1)
        self.assertEqual(continuation_attack_command(10, "bad")["low"], 1)

    def test_continuation_execution_divides_by_attack_count(self):
        self.assertEqual(
            continuation_execution(count=4),
            {"attack_max": 4, "damage_divisor": 4, "attack_loop": True},
        )

    def test_continuation_preserves_prior_high_half(self):
        r = continuation_attack_command(10, "3", prior_high=77)
        self.assertEqual(r["low"], 3)
        self.assertEqual(r["high"], 77)

    def test_charge_parses_wait_count_and_attack_percent(self):
        r = charge_attack_command(11, "2 攻%35")
        self.assertEqual(r["command"], "S_CHARGE")
        self.assertEqual(r["low"], 2)
        self.assertEqual(r["high"], 35)

    def test_charge_invalid_wait_count_defaults_one(self):
        self.assertEqual(charge_attack_command(11, "99 攻%20")["low"], 1)

    def test_charge_wait_step_decrements_and_does_no_action(self):
        r = charge_execution_step(
            remaining=2,
            attack_percent=50,
            fixed_attack=1000,
            attack_modifier=100,
        )
        self.assertFalse(r["ready"])
        self.assertEqual(r["remaining"], 1)
        self.assertTrue(r["no_action"])
        self.assertIsNone(r["attack_power"])

    def test_charge_ready_step_rebuilds_attack_power(self):
        r = charge_execution_step(
            remaining=0,
            attack_percent=50,
            fixed_attack=1000,
            attack_modifier=100,
        )
        self.assertTrue(r["ready"])
        self.assertEqual(r["command"], "S_CHARGE_OK")
        self.assertEqual(r["attack_power"], 1600)

    def test_power_balance_applies_percent_to_fixed_values(self):
        r = power_balance_command(
            8,
            "攻%20 防%-10",
            fixed_attack=1000,
            fixed_defense=800,
        )
        self.assertEqual(r["attack_power"], 1200)
        self.assertEqual(r["defense_power"], 720)

    def test_power_balance_null_option_fails_after_command_setup(self):
        r = power_balance_command(
            8,
            None,
            fixed_attack=1000,
            fixed_defense=800,
        )
        self.assertFalse(r["accepted"])
        self.assertEqual(r["command"], "S_POWERBALANCE")
        self.assertEqual(r["mode"], "C_OK")

    def test_guardian_attack_mode_sets_flag_and_default_owner_slot(self):
        r = guardian_command(
            12,
            "攻%10 防%25",
            fixed_attack=1000,
            fixed_defense=800,
            battle_slot=15,
            battle_side=1,
        )
        self.assertEqual(r["command"], "S_GUARDIAN_ATTACK")
        self.assertTrue(r["guardian_flag"])
        self.assertEqual(r["guardian_for_slot"], 10)
        self.assertEqual(r["attack_power"], 1100)
        self.assertEqual(r["defense_power"], 1000)

    def test_guardian_defensive_mode_guards_selected_slot(self):
        r = guardian_command(
            13,
            "COM:防御",
            fixed_attack=1000,
            fixed_defense=800,
            battle_slot=15,
            battle_side=1,
        )
        self.assertEqual(r["command"], "GUARD")
        self.assertEqual(r["guardian_for_slot"], 13)

    def test_guardian_redirect_accepts_healthy_nonthrow_case(self):
        self.assertTrue(
            guardian_redirect_allowed(
                guardian_exists=True,
                guardian_slot=5,
                defender_slot=0,
                guardian_alive=True,
                guardian_flag=True,
            )
        )

    def test_guardian_redirect_rejects_bad_statuses(self):
        for field in (
            "guardian_sleep",
            "guardian_confusion",
            "guardian_paralysis",
            "guardian_stone",
            "guardian_barrier",
        ):
            args = dict(
                guardian_exists=True,
                guardian_slot=5,
                defender_slot=0,
                guardian_alive=True,
                guardian_flag=True,
            )
            args[field] = 1
            self.assertFalse(guardian_redirect_allowed(**args))

    def test_guardian_redirect_rejects_throw_weapon_and_self_attack(self):
        base = dict(
            guardian_exists=True,
            guardian_slot=5,
            defender_slot=0,
            guardian_alive=True,
            guardian_flag=True,
        )
        self.assertFalse(
            guardian_redirect_allowed(**base, attacker_uses_throw_weapon=True)
        )
        self.assertFalse(
            guardian_redirect_allowed(**base, guardian_is_attacker=True)
        )

    def test_mighty_parses_multiplier_and_dodge(self):
        r = mighty_command(10, "倍2.5 避20")
        self.assertEqual(r["low"], 250)
        self.assertEqual(r["high"], 20)
        self.assertEqual(
            mighty_execution(
                encoded_multiplier=r["low"],
                dodge_modifier=r["high"],
            ),
            {"damage_multiplier": 2.5, "dodge_modifier": 20},
        )

    def test_mighty_missing_multiplier_marker_preserves_zero_quirk(self):
        r = mighty_command(10, "避25")
        self.assertEqual(r["low"], 0)
        self.assertEqual(
            mighty_execution(encoded_multiplier=0, dodge_modifier=25)[
                "damage_multiplier"
            ],
            0.0,
        )

    def test_status_parser_defaults_turn_three(self):
        r = parse_status_skill("POISON", STATUS)
        self.assertEqual(r["status"], 1)
        self.assertEqual(r["turn"], 3)

    def test_status_parser_reads_turn_and_power_modifiers(self):
        r = parse_status_skill("SLEEP turn5 攻%20 防%-10", STATUS)
        self.assertEqual(r["status"], 3)
        self.assertEqual(r["turn"], 5)
        self.assertEqual(r["attack_percent"], 20.0)
        self.assertEqual(r["defense_percent"], -10.0)

    def test_missing_status_token_encodes_end_sentinel(self):
        r = parse_status_skill("UNKNOWN turn2", STATUS)
        self.assertFalse(r["matched"])
        self.assertEqual(r["status"], len(STATUS))
        self.assertEqual(r["turn"], 2)

    def test_status_command_encodes_status_and_turn(self):
        r = status_change_command(
            11,
            "STONE turn4 攻%25",
            STATUS,
            fixed_attack=1000,
            fixed_defense=800,
        )
        self.assertEqual(r["command"], "S_STATUSCHANGE")
        self.assertEqual(r["low"], 4)
        self.assertEqual(r["high"], 4)
        self.assertEqual(r["attack_power"], 1250)

    def test_paralysis_probability_is_fixed_twenty_minus_resist(self):
        self.assertEqual(
            status_attack_probability(
                status=2,
                defender_vital=20,
                defender_str=20,
                defender_tough=20,
                defender_dex=20,
                attacker_luck=99,
                attacker_level=100,
                defender_level=1,
                pvp=False,
                status_specific_resist=7,
            ),
            13,
        )

    def test_status_probability_uses_battle_attack_base_thirty(self):
        self.assertEqual(
            status_attack_probability(
                status=1,
                defender_vital=25,
                defender_str=25,
                defender_tough=25,
                defender_dex=25,
                attacker_luck=10,
                attacker_level=20,
                defender_level=10,
                pvp=False,
                status_specific_resist=5,
            ),
            45,
        )

    def test_status_probability_allows_explicit_per_offset_override(self):
        self.assertEqual(
            status_attack_probability(
                status=1,
                defender_vital=25,
                defender_str=25,
                defender_tough=25,
                defender_dex=25,
                attacker_luck=10,
                attacker_level=20,
                defender_level=10,
                pvp=False,
                status_specific_resist=5,
                per_offset=0,
            ),
            15,
        )

    def test_status_probability_caps_at_eighty(self):
        self.assertEqual(
            status_attack_probability(
                status=1,
                defender_vital=1,
                defender_str=99,
                defender_tough=99,
                defender_dex=99,
                attacker_luck=100,
                attacker_level=100,
                defender_level=1,
                pvp=False,
            ),
            80,
        )

    def test_status_application_uses_authoritative_physical_core(self):
        result=status_attack_application(
            current_status=BaseBattleStatusState(),
            damage=100,
            status=1,
            turn=3,
            defender_vital=25,
            defender_str=25,
            defender_tough=25,
            defender_dex=25,
            attacker_luck=10,
            attacker_level=20,
            defender_level=10,
            pvp=False,
            status_specific_resist=5,
            roll_1_to_100=44,
        )
        self.assertTrue(result["valid_status"])
        application=result["application"]
        self.assertEqual(application.check.source_probability_value,45)
        self.assertTrue(application.check.success)
        self.assertEqual(application.turn_written,4)
        self.assertEqual(application.status_after.poison,4)

    def test_status_application_preserves_damage_gate_and_invalid_sentinel(self):
        blocked=status_attack_application(
            current_status=BaseBattleStatusState(),
            damage=0,
            status=3,
            turn=3,
            defender_vital=25,
            defender_str=25,
            defender_tough=25,
            defender_dex=25,
            attacker_luck=99,
            attacker_level=20,
            defender_level=10,
            pvp=False,
            roll_1_to_100=None,
        )
        self.assertTrue(blocked["valid_status"])
        self.assertTrue(blocked["application"].check.blocked_by_damage_gate)
        self.assertFalse(blocked["application"].check.rng_consumed)

        invalid=status_attack_application(
            current_status=BaseBattleStatusState(),
            damage=100,
            status=len(STATUS),
            turn=3,
            defender_vital=25,
            defender_str=25,
            defender_tough=25,
            defender_dex=25,
            attacker_luck=99,
            attacker_level=20,
            defender_level=10,
            pvp=False,
            roll_1_to_100=None,
        )
        self.assertFalse(invalid["valid_status"])
        self.assertIsNone(invalid["application"])

    def test_status_application_carries_physical_drunk_post_write_halving(self):
        result=status_attack_application(
            current_status=BaseBattleStatusState(),
            damage=100,
            status=5,
            turn=3,
            defender_vital=25,
            defender_str=25,
            defender_tough=25,
            defender_dex=25,
            attacker_luck=100,
            attacker_level=20,
            defender_level=10,
            pvp=False,
            roll_1_to_100=1,
            per_offset=100,
        )
        application=result["application"]
        self.assertTrue(application.check.success)
        self.assertEqual(application.turn_written,2)
        self.assertEqual(application.status_after.drunk,2)

    def test_status_transition_requires_positive_damage(self):
        r = status_attack_transition(
            damage=0,
            status=1,
            turn=3,
            already_has_ordinary_status=False,
            probability=80,
            rolled_1_to_100=1,
        )
        self.assertFalse(r["applied"])

    def test_status_transition_rejects_existing_status(self):
        r = status_attack_transition(
            damage=100,
            status=1,
            turn=3,
            already_has_ordinary_status=True,
            probability=80,
            rolled_1_to_100=1,
        )
        self.assertFalse(r["applied"])

    def test_status_transition_writes_turn_plus_one(self):
        r = status_attack_transition(
            damage=100,
            status=3,
            turn=3,
            already_has_ordinary_status=False,
            probability=80,
            rolled_1_to_100=20,
        )
        self.assertTrue(r["applied"])
        self.assertEqual(r["timer"], 4)
        self.assertTrue(r["clear_command"])

    def test_physical_drunk_status_halves_written_timer(self):
        r=status_attack_transition(
            damage=100,
            status=5,
            turn=3,
            already_has_ordinary_status=False,
            probability=80,
            rolled_1_to_100=20,
        )
        self.assertTrue(r["applied"])
        self.assertEqual(r["timer"],2)
        self.assertFalse(r["clear_command"])

    def test_earth_round_is_two_phase(self):
        r = earth_round_command(12, "攻%35")
        self.assertEqual(r["command"], "S_EARTHROUND1")
        self.assertEqual(r["com3"], 35)
        hidden = earth_round_hide_transition()
        self.assertEqual(hidden["next_command"], "S_EARTHROUND0")
        self.assertFalse(hidden["is_attacked_flag"])
        attack = earth_round_attack_transition(attack_percent=35)
        self.assertAlmostEqual(attack["damage_multiplier"], 1.35)
        self.assertTrue(attack["reset_command_after_attack"])

    def test_earth_round_missing_marker_preserves_whole_prior_com3(self):
        r = earth_round_command(12, "NO_PERCENT", prior_com3=321)
        self.assertEqual(r["com3"], 321)
        self.assertAlmostEqual(
            earth_round_attack_transition(attack_percent=r["com3"])[
                "damage_multiplier"
            ],
            4.21,
        )

    def test_guard_break_attack_modifier(self):
        r = guard_break_command(12, "攻%30", fixed_attack=1000)
        self.assertEqual(r["attack_power"], 1300)

    def test_guard_break_only_damages_guarding_nonconfused_target(self):
        self.assertTrue(
            guard_break_gate(target_guarding=True, target_confused=False)
        )
        self.assertFalse(
            guard_break_gate(target_guarding=False, target_confused=False)
        )
        self.assertFalse(
            guard_break_gate(target_guarding=True, target_confused=True)
        )

    def test_abduct_command_carries_skill_array(self):
        r = abduct_command(12, skill_array=77)
        self.assertEqual(r["command"], "S_ABDUCT")
        self.assertEqual(r["low"], 77)

    def test_abduct_preserves_prior_high_half(self):
        r = abduct_command(12, skill_array=77, prior_high=9)
        self.assertEqual(r["low"], 77)
        self.assertEqual(r["high"], 9)

    def test_abduct_probability_has_minimum_fifty(self):
        self.assertEqual(
            abduct_probability(
                attacker_level=100,
                defender_level=1,
                defender_is_player=False,
                has_win_func=False,
            ),
            50,
        )

    def test_abduct_probability_can_exceed_fifty(self):
        self.assertEqual(
            abduct_probability(
                attacker_level=10,
                defender_level=110,
                defender_is_player=False,
                has_win_func=False,
            ),
            90,
        )

    def test_abduct_player_and_win_battle_are_zero_probability(self):
        self.assertEqual(
            abduct_probability(
                attacker_level=10,
                defender_level=20,
                defender_is_player=True,
                has_win_func=False,
            ),
            0,
        )
        self.assertEqual(
            abduct_probability(
                attacker_level=10,
                defender_level=20,
                defender_is_player=False,
                has_win_func=True,
            ),
            0,
        )

    def test_abduct_pet_exits_on_success_or_failure(self):
        success = abduct_transition(
            attacker_type="pet",
            defender_type="enemy",
            probability=50,
            rolled_1_to_100=1,
        )
        self.assertTrue(success["success"])
        self.assertTrue(success["attacker_exits"])
        self.assertTrue(success["defender_exits"])
        failure = abduct_transition(
            attacker_type="pet",
            defender_type="enemy",
            probability=50,
            rolled_1_to_100=99,
        )
        self.assertFalse(failure["success"])
        self.assertTrue(failure["attacker_exits"])
        self.assertFalse(failure["defender_exits"])

    def test_abduct_player_attacker_is_ineligible(self):
        r = abduct_transition(
            attacker_type="player",
            defender_type="enemy",
            probability=50,
            rolled_1_to_100=1,
        )
        self.assertFalse(r["attempted"])
        self.assertFalse(r["attacker_exits"])

    def test_steal_command(self):
        self.assertEqual(steal_command(12)["command"], "S_STEAL")

    def test_steal_nonplayer_target_always_fails(self):
        r = steal_transition(
            defender_type="enemy",
            success_roll_1_to_100=1,
        )
        self.assertFalse(r["success"])

    def test_steal_player_entry_probability_is_fifty(self):
        self.assertFalse(
            steal_transition(
                defender_type="player",
                success_roll_1_to_100=50,
            )["success"]
        )

    def test_steal_gold_mode_uses_eight_to_twelve_percent_roll(self):
        r = steal_transition(
            defender_type="player",
            success_roll_1_to_100=1,
            mode_roll_1_to_100=1,
            defender_gold=1000,
            gold_percent_roll=10,
        )
        self.assertTrue(r["success"])
        self.assertEqual(r["mode"], "gold")
        self.assertEqual(r["defender_gold_loss"], 100)
        self.assertEqual(r["attacker_gold_gain"], 0)
        self.assertTrue(r["attacker_exits"])

    def test_steal_zero_gold_converts_to_failure(self):
        r = steal_transition(
            defender_type="player",
            success_roll_1_to_100=1,
            mode_roll_1_to_100=1,
            defender_gold=0,
            gold_percent_roll=10,
        )
        self.assertFalse(r["success"])
        self.assertFalse(r["attacker_exits"])

    def test_steal_item_mode_selects_carried_slot(self):
        r = steal_transition(
            defender_type="player",
            success_roll_1_to_100=1,
            mode_roll_1_to_100=99,
            carried_item_slots=(9, 11, 15),
            chosen_item_ordinal=1,
        )
        self.assertTrue(r["success"])
        self.assertEqual(r["destroyed_item_slot"], 11)
        self.assertFalse(r["attacker_item_gain"])
        self.assertTrue(r["attacker_exits"])

    def test_merge_rejects_when_owner_in_battle(self):
        self.assertEqual(
            merge_transition(
                owner_battle_mode_none=False,
                merge_result=True,
            ),
            {"accepted": False, "result": False, "reason": "owner_in_battle"},
        )

    def test_merge_delegates_result_outside_battle(self):
        self.assertEqual(
            merge_transition(
                owner_battle_mode_none=True,
                merge_result=True,
            ),
            {"accepted": True, "result": True, "reason": "merge_called"},
        )

    def test_no_guard_packs_counter_critical_and_dodge(self):
        r = no_guard_command(12, "避%20 击%30 心%40")
        self.assertEqual(r["high"], 20)
        self.assertEqual(r["low"], (30 << 8) + 40)

    def test_no_guard_missing_dodge_marker_preserves_prior_high_half(self):
        r = no_guard_command(12, "击%30 心%40", prior_high=88)
        self.assertEqual(r["high"], 88)
        self.assertEqual(r["low"], (30 << 8) + 40)

    def test_no_guard_supports_traditional_counter_marker(self):
        r = no_guard_command(
            12,
            "避%20 擊%30 心%40",
            counter_marker="擊%",
        )
        self.assertEqual(r["high"], 20)
        self.assertEqual(r["low"], (30 << 8) + 40)

    def test_no_guard_execution_is_no_action_and_drops_parameters(self):
        self.assertEqual(
            no_guard_execution(),
            {"no_action": True, "parsed_parameters_consumed": False},
        )


if __name__ == "__main__":
    unittest.main()
