import unittest
from types import MappingProxyType

from tools.stoneage_battle_command_model import (
    ATTACK,
    CAPTURE,
    ESCAPE,
    GUARD,
    WAIT,
    apply_error_status_fallback,
    parse_player_battle_command,
    prepare_player_round_action,
)
from tools.stoneage_singleplayer_battle import BattleParticipant


def player():
    return BattleParticipant(
        participant_id="player",
        side="player",
        kind="player",
        level=10,
        hp=100,
        max_hp=100,
        attack=80,
        defense=70,
        quick=60,
        name="Hero",
        fixed_vital=40,
    )


class BattleCommandModelTests(unittest.TestCase):
    def test_attack_uses_hex_target_domain_zero_through_nineteen(self):
        command = parse_player_battle_command("H|0A")
        self.assertEqual(command.kind, ATTACK)
        self.assertEqual(command.target_slot, 10)

        self.assertEqual(
            parse_player_battle_command("H|13").target_slot,
            19,
        )

    def test_invalid_attack_target_is_preserved_as_minus_one_like_source(self):
        self.assertEqual(
            parse_player_battle_command("H|14").target_slot,
            -1,
        )
        self.assertEqual(
            parse_player_battle_command("H|garbage").target_slot,
            -1,
        )

    def test_guard_wait_escape_and_capture_core_commands(self):
        self.assertEqual(parse_player_battle_command("G").kind, GUARD)
        self.assertEqual(parse_player_battle_command("N").kind, WAIT)
        self.assertEqual(parse_player_battle_command("E").kind, ESCAPE)
        capture = parse_player_battle_command("T|0F")
        self.assertEqual(capture.kind, CAPTURE)
        self.assertEqual(capture.target_slot, 15)

    def test_fixed_dispatcher_prefix_behavior_is_retained(self):
        self.assertEqual(parse_player_battle_command("Gextra").kind, GUARD)
        self.assertEqual(parse_player_battle_command("Nanything").kind, WAIT)

    def test_later_or_unmodeled_commands_fail_explicitly(self):
        for wire in ("U", "S|1", "W|1|2", "I|1|2", "J|1|2", "P1|2"):
            with self.assertRaises(ValueError):
                parse_player_battle_command(wire)

    def test_error_status_falls_checked_commands_back_to_wait(self):
        for wire in ("H|01", "G", "E", "T|01"):
            parsed = parse_player_battle_command(wire)
            normalized = apply_error_status_fallback(
                parsed,
                error_status=True,
            )
            self.assertEqual(normalized.kind, WAIT)
            self.assertEqual(normalized.wire_command, "N")

        wait = parse_player_battle_command("N")
        self.assertEqual(
            apply_error_status_fallback(wait, error_status=True),
            wait,
        )

    def test_round_action_uses_explicit_recovered_initiative_roll(self):
        action = prepare_player_round_action(
            player(),
            parse_player_battle_command("H|01"),
            initiative_random_subtract=12,
        )
        self.assertEqual(action.actor_id, "player")
        self.assertEqual(action.command.kind, ATTACK)
        self.assertEqual(action.initiative, 68)
        self.assertTrue(action.ready)

    def test_initiative_roll_bounds_are_inherited_from_battle_core(self):
        with self.assertRaises(ValueError):
            prepare_player_round_action(
                player(),
                parse_player_battle_command("G"),
                initiative_random_subtract=25,
            )

    def test_non_player_actor_cannot_use_player_command_boundary(self):
        enemy = BattleParticipant(
            participant_id="enemy:1:0",
            side="enemy",
            kind="enemy",
            level=1,
            hp=10,
            max_hp=10,
            attack=5,
            defense=5,
            quick=5,
            name="Enemy",
        )
        with self.assertRaises(ValueError):
            prepare_player_round_action(
                enemy,
                parse_player_battle_command("N"),
                initiative_random_subtract=0,
            )


if __name__ == "__main__":
    unittest.main()
