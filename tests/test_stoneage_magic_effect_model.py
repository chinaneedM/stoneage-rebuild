import unittest

from tools.stoneage_battle_status_model import BaseBattleStatusState

from tools.stoneage_magic_effect_model import (
    att_reverse_cast_transition,
    att_reverse_precommand_refresh,
    att_reverse_transition,
    battle_recovery_gain,
    c_atoi,
    common_alive_target_list,
    common_cast_route,
    common_dead_target_list,
    common_magic_status_change_transition,
    field_recovery_gain,
    magic_def_transition,
    parse_after_marker,
    parse_field_attribute_option,
    parse_magic_def_option,
    parse_recovery_option,
    parse_resurrection_option,
    parse_status_change_option,
    recovery_rate,
    recovery_target_allowed,
    recovery_wrapper_target_allowed,
    res_and_def_transition,
    resurrection_gain,
    status_recovery_transition,
)


class StoneAgeMagicEffectModelTests(unittest.TestCase):
    def test_common_magic_status_change_uses_common_check_and_exact_turn(self):
        result=common_magic_status_change_transition(
            current_status=BaseBattleStatusState(),
            status_index=1,
            turn=3,
            success_offset=15,
            attacker_level=30,
            defender_level=10,
            pvp=False,
            attacker_fixed_luck=5,
            defender_vital=25,
            defender_str=25,
            defender_tough=25,
            defender_dex=25,
            defender_resistance=3,
            roll_1_100=26,
        )
        self.assertTrue(result["check"].success)
        self.assertEqual(result["check"].source_probability_value,27)
        self.assertEqual(result["status"].poison,3)
        self.assertFalse(result["command_cleared"])

    def test_common_magic_immobilizer_clears_command_on_success(self):
        result=common_magic_status_change_transition(
            current_status=BaseBattleStatusState(),
            status_index=2,
            turn=4,
            success_offset=99,
            attacker_level=1,
            defender_level=99,
            pvp=False,
            attacker_fixed_luck=99,
            defender_vital=100,
            defender_str=1,
            defender_tough=1,
            defender_dex=1,
            defender_resistance=0,
            roll_1_100=19,
        )
        self.assertTrue(result["check"].success)
        self.assertEqual(result["status"].paralysis,4)
        self.assertTrue(result["command_cleared"])

    def test_common_magic_status_change_does_not_replace_existing_status(self):
        current=BaseBattleStatusState(sleep=2)
        result=common_magic_status_change_transition(
            current_status=current,
            status_index=1,
            turn=3,
            success_offset=100,
            attacker_level=99,
            defender_level=1,
            pvp=False,
            attacker_fixed_luck=99,
            defender_vital=25,
            defender_str=25,
            defender_tough=25,
            defender_dex=25,
            defender_resistance=0,
            roll_1_100=None,
        )
        self.assertFalse(result["check"].rng_consumed)
        self.assertFalse(result["check"].success)
        self.assertEqual(result["status"],current)

    def test_c_atoi_matches_leading_integer_semantics(self):
        self.assertEqual(c_atoi("  -42abc"), -42)
        self.assertEqual(c_atoi("+17%"), 17)
        self.assertEqual(c_atoi("abc17"), 0)

    def test_recovery_rate_differs_for_player_and_nonplayer(self):
        self.assertAlmostEqual(recovery_rate(vital=2500, is_player=True), 1.25)
        self.assertAlmostEqual(recovery_rate(vital=2500, is_player=False), 1.125)

    def test_invalid_caster_does_not_spend_mp(self):
        r = common_cast_route(
            "status_change",
            caster_valid=False,
            battle_mode_init=False,
            current_mp=100,
            mp_cost=20,
            battling=True,
        )
        self.assertFalse(r["accepted"])
        self.assertEqual(r["remaining_mp"], 100)
        self.assertEqual(r["mp_spent"], 0)

    def test_battle_init_rejects_before_mp_spend(self):
        r = common_cast_route(
            "magic_def",
            caster_valid=True,
            battle_mode_init=True,
            current_mp=100,
            mp_cost=20,
            battling=True,
        )
        self.assertEqual(r["route"], "reject_battle_init")
        self.assertEqual(r["remaining_mp"], 100)

    def test_insufficient_mp_rejects_without_mutation(self):
        r = common_cast_route(
            "ressurect",
            caster_valid=True,
            battle_mode_init=False,
            current_mp=19,
            mp_cost=20,
            battling=True,
        )
        self.assertEqual(r["route"], "reject_insufficient_mp")
        self.assertEqual(r["remaining_mp"], 19)

    def test_battle_only_magic_spends_mp_before_not_battling_failure(self):
        r = common_cast_route(
            "field_att_change",
            caster_valid=True,
            battle_mode_init=False,
            current_mp=100,
            mp_cost=20,
            battling=False,
        )
        self.assertFalse(r["accepted"])
        self.assertEqual(r["route"], "reject_not_battling_after_mp")
        self.assertEqual(r["remaining_mp"], 80)
        self.assertEqual(r["mp_spent"], 20)

    def test_recovery_routes_to_field(self):
        r = common_cast_route(
            "recovery",
            caster_valid=True,
            battle_mode_init=False,
            current_mp=100,
            mp_cost=15,
            battling=False,
            target_valid=True,
        )
        self.assertTrue(r["accepted"])
        self.assertEqual(r["route"], "field")
        self.assertEqual(r["remaining_mp"], 85)

    def test_invalid_field_target_is_checked_after_mp_spend(self):
        r = common_cast_route(
            "other_recovery",
            caster_valid=True,
            battle_mode_init=False,
            current_mp=100,
            mp_cost=15,
            battling=False,
            target_valid=False,
        )
        self.assertFalse(r["accepted"])
        self.assertEqual(r["route"], "reject_invalid_field_target_after_mp")
        self.assertEqual(r["remaining_mp"], 85)

    def test_common_alive_target_expansion(self):
        alive = {0, 2, 9, 10, 15, 19}
        self.assertEqual(common_alive_target_list(2, alive), (2,))
        self.assertEqual(common_alive_target_list(3, alive), ())
        self.assertEqual(common_alive_target_list(20, alive), (0, 2, 9))
        self.assertEqual(common_alive_target_list(21, alive), (10, 15, 19))
        self.assertEqual(common_alive_target_list(22, alive), (0, 2, 9, 10, 15, 19))

    def test_common_dead_target_expansion(self):
        dead = {1, 4, 11, 18}
        self.assertEqual(common_dead_target_list(1, dead), (1,))
        self.assertEqual(common_dead_target_list(2, dead), ())
        self.assertEqual(common_dead_target_list(20, dead), (1, 4))
        self.assertEqual(common_dead_target_list(21, dead), (11, 18))
        self.assertEqual(common_dead_target_list(22, dead), (1, 4, 11, 18))

    def test_unknown_target_selector_falls_through_raw(self):
        self.assertEqual(common_alive_target_list(99, set()), (99,))
        self.assertEqual(common_dead_target_list(99, set()), (99,))

    def test_recovery_wrapper_rejects_battle_all_target_only_for_recovery(self):
        self.assertFalse(
            recovery_wrapper_target_allowed(
                "recovery", to_no=22, battling=True
            )
        )
        self.assertTrue(
            recovery_wrapper_target_allowed(
                "other_recovery", to_no=22, battling=True
            )
        )
        self.assertTrue(
            recovery_wrapper_target_allowed(
                "recovery", to_no=22, battling=False
            )
        )

    def test_recovery_target_guard_self_only(self):
        self.assertTrue(
            recovery_target_allowed(magic_target=0, caster_battle_no=12, to_no=12)
        )
        self.assertFalse(
            recovery_target_allowed(magic_target=0, caster_battle_no=12, to_no=11)
        )

    def test_recovery_target_guard_single_rejects_group_selectors(self):
        self.assertTrue(
            recovery_target_allowed(magic_target=1, caster_battle_no=0, to_no=19)
        )
        self.assertFalse(
            recovery_target_allowed(magic_target=1, caster_battle_no=0, to_no=20)
        )
        self.assertFalse(
            recovery_target_allowed(magic_target=1, caster_battle_no=0, to_no=22)
        )

    def test_recovery_other_target_modes_delegate(self):
        self.assertTrue(
            recovery_target_allowed(magic_target=2, caster_battle_no=0, to_no=22)
        )

    def test_recovery_option_detects_percent(self):
        self.assertEqual(parse_recovery_option("35%"), {"power": 35, "percent": True})
        self.assertEqual(parse_recovery_option("120"), {"power": 120, "percent": False})

    def test_battle_recovery_uses_percent_then_recovery_rate(self):
        # rolled power 20; 20 * 500 * .01 = 100; player rate 1.20 => 120
        self.assertEqual(
            battle_recovery_gain(
                power=20,
                percent=True,
                max_hp=500,
                rate=1.20,
                rolled_power=20,
            ),
            120,
        )

    def test_field_recovery_has_no_percent_branch(self):
        self.assertEqual(field_recovery_gain(rate=1.25, rolled_power=80), 100)

    def test_marker_parser_skips_exactly_one_separator(self):
        self.assertEqual(parse_after_marker("xturn=7", "turn", 3), 7)
        # No separator: the first digit is skipped, matching sizeof(marker) pointer advance.
        self.assertEqual(parse_after_marker("xturn7", "turn", 3), 3)
        self.assertEqual(parse_after_marker("x", "turn", 3), 3)

    def test_field_attribute_option_defaults_and_range_guard(self):
        tokens = ("NONE", "EARTH", "WATER", "FIRE", "WIND")
        self.assertEqual(
            parse_field_attribute_option("FIRE40turn=6", tokens),
            {"attribute": 3, "power": 40, "turn": 6},
        )
        self.assertEqual(
            parse_field_attribute_option("WIND999turn=4", tokens),
            {"attribute": 4, "power": 30, "turn": 4},
        )
        self.assertIsNone(parse_field_attribute_option("UNKNOWN", tokens))

    def test_status_change_defaults_turn_and_success(self):
        tokens = ("NONE", "POISON", "SLEEP")
        self.assertEqual(
            parse_status_change_option("POISON", tokens),
            {"status": 1, "turn": 3, "success": 15},
        )
        self.assertEqual(
            parse_status_change_option("SLEEPturn=5成=42", tokens),
            {"status": 2, "turn": 5, "success": 42},
        )

    def test_magic_def_option_parses_kind_and_turn(self):
        tokens = ("NONE", "LIGHT", "MIRROR")
        self.assertEqual(
            parse_magic_def_option("MIRRORturn=4", tokens),
            {"kind": 2, "turn": 4},
        )

    def test_resurrection_zero_power_means_full_max_hp(self):
        parsed = parse_resurrection_option("0")
        self.assertEqual(parsed, {"power": 0, "percent": False})
        self.assertEqual(
            resurrection_gain(
                power=parsed["power"],
                percent=parsed["percent"],
                max_hp=777,
            ),
            777,
        )

    def test_resurrection_percent_is_overwritten_for_nonzero_power(self):
        parsed = parse_resurrection_option("25%")
        # The old implementation computes the percentage and then overwrites it
        # with RAND(power*0.9, power*1.1). Supply the already-rolled result.
        self.assertEqual(
            resurrection_gain(
                power=parsed["power"],
                percent=parsed["percent"],
                max_hp=1000,
                rolled_power=24,
            ),
            24,
        )

    def test_resurrection_nonzero_gain_is_at_least_one(self):
        self.assertEqual(
            resurrection_gain(
                power=1,
                percent=False,
                max_hp=100,
                rolled_power=0,
            ),
            1,
        )

    def test_status_recovery_selects_highest_active_status(self):
        r = status_recovery_transition(
            {1, 3, 5},
            requested_status=0,
            confusion_index=5,
        )
        self.assertEqual(r["selected_status"], 5)
        self.assertTrue(r["cleared"])
        self.assertEqual(r["active_statuses"], (1, 3))

    def test_status_recovery_does_not_fall_back_to_lower_status(self):
        r = status_recovery_transition(
            {1, 6},
            requested_status=1,
            confusion_index=5,
        )
        self.assertEqual(r["selected_status"], 6)
        self.assertFalse(r["cleared"])
        self.assertEqual(r["active_statuses"], (1, 6))

    def test_magic_def_overwrites_turn_for_same_kind(self):
        self.assertEqual(
            magic_def_transition(current_turns={1: 2, 2: 5}, kind=1, turn=7),
            {1: 7, 2: 5},
        )

    def test_attribute_reverse_is_xor_toggle(self):
        bit = 0x20
        flags = 0x04
        enabled = att_reverse_transition(battle_flags=flags, reverse_bit=bit)
        self.assertEqual(enabled, 0x24)
        self.assertEqual(
            att_reverse_transition(battle_flags=enabled, reverse_bit=bit),
            flags,
        )

    def test_reverse_enable_immediately_swaps_fixed_attributes(self):
        r = att_reverse_cast_transition(
            battle_flags=0,
            reverse_bit=0x20,
            earth=10,
            water=20,
            fire=30,
            wind=40,
        )
        self.assertEqual(r["battle_flags"], 0x20)
        self.assertEqual(
            r["attributes"],
            {"earth": 30, "water": 40, "fire": 10, "wind": 20},
        )

    def test_reverse_disable_does_not_immediately_swap_back(self):
        r = att_reverse_cast_transition(
            battle_flags=0x20,
            reverse_bit=0x20,
            earth=30,
            water=40,
            fire=10,
            wind=20,
        )
        self.assertEqual(r["battle_flags"], 0)
        self.assertEqual(
            r["attributes"],
            {"earth": 30, "water": 40, "fire": 10, "wind": 20},
        )

    def test_precommand_refresh_restores_or_reapplies_reverse(self):
        base = {"earth": 10, "water": 20, "fire": 30, "wind": 40}
        self.assertEqual(
            att_reverse_precommand_refresh(
                battle_flags=0,
                reverse_bit=0x20,
                **base,
            ),
            base,
        )
        self.assertEqual(
            att_reverse_precommand_refresh(
                battle_flags=0x20,
                reverse_bit=0x20,
                **base,
            ),
            {"earth": 30, "water": 40, "fire": 10, "wind": 20},
        )

    def test_res_and_def_skips_living_target(self):
        r = res_and_def_transition(
            is_dead=False,
            is_pvp_player=False,
            current_hp=50,
            max_hp=500,
            power=100,
            percent=False,
            rolled_power=95,
            magic_def_turns={},
            magic_def_kind=1,
            turn=3,
        )
        self.assertFalse(r["changed"])
        self.assertEqual(r["hp"], 50)
        self.assertEqual(r["magic_def_turns"], {})

    def test_res_and_def_skips_pvp_player(self):
        r = res_and_def_transition(
            is_dead=True,
            is_pvp_player=True,
            current_hp=0,
            max_hp=500,
            power=100,
            percent=False,
            rolled_power=95,
            magic_def_turns={},
            magic_def_kind=1,
            turn=3,
        )
        self.assertFalse(r["changed"])
        self.assertTrue(r["is_dead"])

    def test_res_and_def_revives_and_sets_defense(self):
        r = res_and_def_transition(
            is_dead=True,
            is_pvp_player=False,
            current_hp=0,
            max_hp=500,
            power=100,
            percent=False,
            rolled_power=95,
            magic_def_turns={2: 1},
            magic_def_kind=1,
            turn=4,
        )
        self.assertTrue(r["changed"])
        self.assertFalse(r["is_dead"])
        self.assertEqual(r["hp"], 95)
        self.assertEqual(r["magic_def_turns"], {2: 1, 1: 4})


if __name__ == "__main__":
    unittest.main()
