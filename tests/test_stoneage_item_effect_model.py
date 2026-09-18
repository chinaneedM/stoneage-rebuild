import unittest

from tools.stoneage_item_effect_model import (
    apply_field_recovery,
    apply_param_modifier,
    battle_effect_consumption,
    battle_item_recovery_gain,
    capture_up_transition,
    dead_targets,
    field_change_consumption,
    item_use_route,
    living_targets,
    param_modifier_delta,
    parse_battle_recovery_option,
    parse_capture_up_option,
    parse_field_change_option,
    parse_field_recovery_option,
    parse_magic_def_option,
    parse_param_change_option,
    parse_resurrection_option,
    parse_status_change_option,
    parse_status_recovery_option,
    recover_statuses,
    resurrection_target_transition,
    reverse_target_transition,
    set_magic_defense,
)


STATUS = ("NONE", "POISON", "SLEEP", "STONE", "CONFUSION")
DEFENSE = ("NONE", "LIGHT", "MIRROR")
PARAM = ("NONE", "ATTACK", "DEFENSE", "QUICK", "CHARM", "CAPTURE")
ATTR = ("NONE", "EARTH", "WATER", "FIRE", "WIND")


class StoneAgeItemEffectModelTests(unittest.TestCase):
    def test_recovery_routes_field_or_battle(self):
        self.assertEqual(
            item_use_route(
                "recovery",
                caster_valid=True,
                battle_mode_init=False,
                battling=False,
            )["route"],
            "field",
        )
        self.assertEqual(
            item_use_route(
                "recovery",
                caster_valid=True,
                battle_mode_init=False,
                battling=True,
            )["route"],
            "battle",
        )

    def test_battle_only_item_does_nothing_outside_battle(self):
        r = item_use_route(
            "status_change",
            caster_valid=True,
            battle_mode_init=False,
            battling=False,
        )
        self.assertFalse(r["accepted"])
        self.assertEqual(r["route"], "reject_not_battling")

    def test_battle_init_suppresses_item_wrapper(self):
        r = item_use_route(
            "recovery",
            caster_valid=True,
            battle_mode_init=True,
            battling=True,
        )
        self.assertFalse(r["accepted"])
        self.assertEqual(r["route"], "reject_battle_init")

    def test_invalid_caster_rejects_before_routing(self):
        r = item_use_route(
            "recovery",
            caster_valid=False,
            battle_mode_init=False,
            battling=True,
        )
        self.assertEqual(r["route"], "reject_invalid_caster")

    def test_battle_recovery_hp_is_checked_before_mp(self):
        r = parse_battle_recovery_option(
            "HP=100 MP=50",
            hp_token="HP",
            mp_token="MP",
        )
        self.assertEqual(r, {"kind": "hp", "power": 100, "percent": False})

    def test_battle_recovery_mp_parse(self):
        r = parse_battle_recovery_option(
            "MP=60",
            hp_token="HP",
            mp_token="MP",
        )
        self.assertEqual(r, {"kind": "mp", "power": 60, "percent": False})

    def test_battle_recovery_bad_number_defaults_zero(self):
        r = parse_battle_recovery_option(
            "HP=x",
            hp_token="HP",
            mp_token="MP",
        )
        self.assertEqual(r["power"], 0)

    def test_unrecognized_battle_recovery_argument_does_not_parse(self):
        self.assertIsNone(
            parse_battle_recovery_option(
                "UNKNOWN",
                hp_token="HP",
                mp_token="MP",
            )
        )

    def test_battle_hp_recovery_uses_vital_rate(self):
        self.assertEqual(
            battle_item_recovery_gain(
                kind="hp",
                rolled_power=100,
                vital=2000,
                is_player=True,
            ),
            120,
        )

    def test_battle_mp_recovery_does_not_use_vital_rate(self):
        self.assertEqual(
            battle_item_recovery_gain(
                kind="mp",
                rolled_power=100,
                vital=9000,
                is_player=True,
            ),
            100,
        )

    def test_item_status_defaults_differ_from_magic(self):
        r = parse_status_change_option("POISON", STATUS)
        self.assertEqual(r, {"status": 1, "turn": 0, "success": 15})

    def test_item_status_explicit_turn_and_success(self):
        r = parse_status_change_option("SLEEP turn=4 成=35", STATUS)
        self.assertEqual(r, {"status": 2, "turn": 4, "success": 35})

    def test_status_recovery_parser_accepts_none_status(self):
        self.assertEqual(
            parse_status_recovery_option("NONE", STATUS),
            {"status": 0},
        )

    def test_item_magic_def_default_turn_is_zero(self):
        self.assertEqual(
            parse_magic_def_option("MIRROR", DEFENSE),
            {"kind": 2, "turn": 0},
        )

    def test_item_magic_def_explicit_turn(self):
        self.assertEqual(
            parse_magic_def_option("LIGHT turn=6", DEFENSE),
            {"kind": 1, "turn": 6},
        )

    def test_param_change_default_power(self):
        r = parse_param_change_option("ATTACK=x", PARAM)
        self.assertEqual(
            r,
            {"kind": 1, "power": 30, "percent": False},
        )

    def test_param_change_detects_percent(self):
        r = parse_param_change_option("DEFENSE=25%", PARAM)
        self.assertEqual(
            r,
            {"kind": 2, "power": 25, "percent": True},
        )

    def test_attack_flat_modifier_uses_x100_storage(self):
        self.assertEqual(
            param_modifier_delta(
                1,
                power=12,
                percent=False,
                fixed_attack=999,
            ),
            1200,
        )

    def test_attack_percent_modifier_multiplies_fixed_storage_directly(self):
        self.assertEqual(
            param_modifier_delta(
                1,
                power=10,
                percent=True,
                fixed_attack=3500,
            ),
            35000,
        )

    def test_charm_percent_uses_one_percent_factor(self):
        self.assertEqual(
            param_modifier_delta(
                4,
                power=20,
                percent=True,
                fixed_charm=75,
            ),
            15,
        )

    def test_capture_param_kind_ignores_percent_mode(self):
        self.assertEqual(
            param_modifier_delta(
                5,
                power=7,
                percent=True,
            ),
            7,
        )

    def test_modifier_is_additive(self):
        self.assertEqual(apply_param_modifier(1000, -250), 750)

    def test_field_change_delegates_common_parser(self):
        self.assertEqual(
            parse_field_change_option("FIRE40turn=5", ATTR),
            {"attribute": 3, "power": 40, "turn": 5},
        )

    def test_item_resurrection_parser(self):
        self.assertEqual(
            parse_resurrection_option("25%"),
            {"power": 25, "percent": True},
        )

    def test_item_resurrection_inherits_nonzero_percent_overwrite(self):
        r = resurrection_target_transition(
            is_dead=True,
            is_pvp_player=False,
            current_hp=0,
            max_hp=1000,
            power=25,
            percent=True,
            rolled_power=24,
        )
        self.assertEqual(r["hp"], 24)
        self.assertFalse(r["is_dead"])

    def test_item_resurrection_skips_pvp_player(self):
        r = resurrection_target_transition(
            is_dead=True,
            is_pvp_player=True,
            current_hp=0,
            max_hp=1000,
            power=0,
            percent=False,
        )
        self.assertFalse(r["changed"])
        self.assertTrue(r["is_dead"])

    def test_capture_power_defaults_five(self):
        self.assertEqual(parse_capture_up_option("x"), 5)

    def test_capture_up_changes_only_live_player(self):
        self.assertEqual(
            capture_up_transition(
                is_player=True,
                is_dead=False,
                current_capture_modifier=10,
                rolled_power=6,
            ),
            {"changed": True, "capture_modifier": 16},
        )
        self.assertFalse(
            capture_up_transition(
                is_player=False,
                is_dead=False,
                current_capture_modifier=10,
                rolled_power=6,
            )["changed"]
        )
        self.assertFalse(
            capture_up_transition(
                is_player=True,
                is_dead=True,
                current_capture_modifier=10,
                rolled_power=6,
            )["changed"]
        )

    def test_field_recovery_all_player_sets_hp_and_mp_requests(self):
        r = parse_field_recovery_option(
            "ALL",
            target_type="player",
            all_token="ALL",
            hp_token="HP",
            mp_token="MP",
            charm_token="CHARM",
            loyalty_token="LOYALTY",
        )
        self.assertIn("hp", r)
        self.assertIn("mp", r)
        self.assertEqual(r["hp"]["base"], 10_000_000)
        self.assertEqual(r["mp"]["base"], 100)

    def test_field_recovery_all_pet_has_no_mp_request(self):
        r = parse_field_recovery_option(
            "ALL",
            target_type="pet",
            all_token="ALL",
            hp_token="HP",
            mp_token="MP",
            charm_token="CHARM",
            loyalty_token="LOYALTY",
        )
        self.assertIn("hp", r)
        self.assertNotIn("mp", r)

    def test_explicit_mp_and_charm_are_player_only(self):
        player = parse_field_recovery_option(
            "MP=20 CHARM=5",
            target_type="player",
            all_token="ALL",
            hp_token="HP",
            mp_token="MP",
            charm_token="CHARM",
            loyalty_token="LOYALTY",
        )
        pet = parse_field_recovery_option(
            "MP=20 CHARM=5",
            target_type="pet",
            all_token="ALL",
            hp_token="HP",
            mp_token="MP",
            charm_token="CHARM",
            loyalty_token="LOYALTY",
        )
        self.assertEqual(set(player), {"mp", "charm"})
        self.assertEqual(pet, {})

    def test_loyalty_is_pet_only(self):
        r = parse_field_recovery_option(
            "LOYALTY=3",
            target_type="pet",
            all_token="ALL",
            hp_token="HP",
            mp_token="MP",
            charm_token="CHARM",
            loyalty_token="LOYALTY",
        )
        self.assertEqual(set(r), {"loyalty"})

    def test_field_hp_roll_uses_recovery_rate_and_caps(self):
        req = parse_field_recovery_option(
            "HP=100",
            target_type="player",
            all_token="ALL",
            hp_token="HP",
            mp_token="MP",
            charm_token="CHARM",
            loyalty_token="LOYALTY",
        )
        r = apply_field_recovery(
            req,
            target_type="player",
            current_hp=450,
            max_hp=500,
            current_mp=20,
            max_mp=100,
            vital=2000,
            rolls={"hp": 100},
        )
        self.assertEqual(r["hp"], 500)
        self.assertTrue(r["consume"])

    def test_field_negative_hp_cannot_drop_below_one(self):
        req = parse_field_recovery_option(
            "HP=-100",
            target_type="player",
            all_token="ALL",
            hp_token="HP",
            mp_token="MP",
            charm_token="CHARM",
            loyalty_token="LOYALTY",
        )
        r = apply_field_recovery(
            req,
            target_type="player",
            current_hp=20,
            max_hp=500,
            vital=0,
            rolls={"hp": -100},
        )
        self.assertEqual(r["hp"], 1)

    def test_field_charm_clamps_zero_to_hundred(self):
        req = parse_field_recovery_option(
            "CHARM=50",
            target_type="player",
            all_token="ALL",
            hp_token="HP",
            mp_token="MP",
            charm_token="CHARM",
            loyalty_token="LOYALTY",
        )
        r = apply_field_recovery(
            req,
            target_type="player",
            current_hp=100,
            max_hp=100,
            current_charm=90,
            rolls={"charm": 50},
        )
        self.assertEqual(r["charm"], 100)

    def test_field_loyalty_is_stored_x100_and_clamped(self):
        req = parse_field_recovery_option(
            "LOYALTY=30",
            target_type="pet",
            all_token="ALL",
            hp_token="HP",
            mp_token="MP",
            charm_token="CHARM",
            loyalty_token="LOYALTY",
        )
        r = apply_field_recovery(
            req,
            target_type="pet",
            current_hp=100,
            max_hp=100,
            current_loyalty=9000,
            rolls={"loyalty": 30},
        )
        self.assertEqual(r["loyalty"], 10000)

    def test_no_applicable_field_recovery_does_not_consume(self):
        r = apply_field_recovery(
            {},
            target_type="pet",
            current_hp=100,
            max_hp=100,
        )
        self.assertFalse(r["changed"])
        self.assertFalse(r["consume"])

    def test_successful_battle_parser_leads_to_consumption(self):
        self.assertTrue(
            battle_effect_consumption(
                item_valid=True,
                argument_valid=True,
                parser_succeeded=True,
            )
        )
        self.assertFalse(
            battle_effect_consumption(
                item_valid=True,
                argument_valid=True,
                parser_succeeded=False,
            )
        )

    def test_field_change_consumes_even_if_shared_parser_later_fails(self):
        self.assertTrue(
            field_change_consumption(
                item_valid=True,
                argument_valid=True,
            )
        )

    def test_living_and_dead_target_helpers_share_battle_topology(self):
        self.assertEqual(living_targets(20, {0, 3, 10}), (0, 3))
        self.assertEqual(dead_targets(21, {2, 11, 18}), (11, 18))

    def test_status_recovery_inherits_highest_active_candidate(self):
        r = recover_statuses(
            {1, 3, 4},
            requested_status=0,
            confusion_index=4,
        )
        self.assertEqual(r["selected_status"], 4)
        self.assertEqual(r["active_statuses"], (1, 3))

    def test_magic_defense_transition_overwrites_kind(self):
        self.assertEqual(
            set_magic_defense({1: 4}, kind=1, turn=0),
            {1: 0},
        )

    def test_reverse_item_uses_same_xor_transition(self):
        r = reverse_target_transition(
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


if __name__ == "__main__":
    unittest.main()
