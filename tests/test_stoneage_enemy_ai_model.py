import unittest

from tools.stoneage_enemy_ai_model import (
    ATTACK,
    ESCAPE,
    GUARD,
    SKILL,
    EnemyAiDecision,
    EnemyAiTarget,
    parse_normal_enemy_ai_options,
    resolve_common_normal_enemy_ai,
)


def target(slot, kind, hp, *, alive=True, rescue=False):
    return EnemyAiTarget(
        slot=slot,
        participant_id=f"{kind}:{slot}",
        kind=kind,
        hp=hp,
        alive=alive,
        rescue_mode=rescue,
    )


class EnemyAiModelTests(unittest.TestCase):
    def test_parser_preserves_common_weights_and_tolerates_short_wa(self):
        options = parse_normal_enemy_ai_options(
            "at:10;2;3|gu:2|es:1|wa:5;bogus"
        )
        self.assertEqual(options.attack_weight, 10)
        self.assertEqual(options.target_scope, 2)
        self.assertEqual(options.target_selection, 3)
        self.assertEqual(options.guard_weight, 2)
        self.assertEqual(options.magic_weight, 0)
        self.assertEqual(options.escape_weight, 1)
        self.assertEqual(options.skill_weights, (5, 0, 0, 0, 0, 0, 0))

    def test_missing_required_attack_suboption_fails_closed(self):
        with self.assertRaises(ValueError):
            parse_normal_enemy_ai_options("at:10;1|gu:1")

    def test_weighted_mode_order_matches_source(self):
        text = "at:2;1;1|gu:1|ma:1|es:1|wa:1;0;2"
        targets = (target(0, "player", 100),)
        self.assertEqual(
            resolve_common_normal_enemy_ai(
                text, targets, mode_roll=0, target_roll=0
            ),
            EnemyAiDecision(ATTACK, target_slot=0),
        )
        self.assertEqual(
            resolve_common_normal_enemy_ai(
                text, targets, mode_roll=1, target_roll=0
            ),
            EnemyAiDecision(ATTACK, target_slot=0),
        )
        self.assertEqual(
            resolve_common_normal_enemy_ai(text, targets, mode_roll=2),
            EnemyAiDecision(GUARD),
        )
        self.assertIsNone(
            resolve_common_normal_enemy_ai(text, targets, mode_roll=3)
        )
        self.assertEqual(
            resolve_common_normal_enemy_ai(text, targets, mode_roll=4),
            EnemyAiDecision(ESCAPE),
        )
        self.assertEqual(
            resolve_common_normal_enemy_ai(
                text, targets, mode_roll=5, target_roll=0
            ),
            EnemyAiDecision(SKILL, target_slot=0, skill_slot=0),
        )
        self.assertEqual(
            resolve_common_normal_enemy_ai(
                text, targets, mode_roll=6, target_roll=0
            ),
            EnemyAiDecision(SKILL, target_slot=0, skill_slot=2),
        )
        self.assertEqual(
            resolve_common_normal_enemy_ai(
                text, targets, mode_roll=7, target_roll=0
            ),
            EnemyAiDecision(SKILL, target_slot=0, skill_slot=2),
        )

    def test_random_target_uses_explicit_roll_and_filters_dead_rescue(self):
        targets = (
            target(0, "player", 100),
            target(1, "pet", 90, alive=False),
            target(2, "pet", 80, rescue=True),
            target(3, "pet", 70),
        )
        text = "at:1;1;1"
        self.assertEqual(
            resolve_common_normal_enemy_ai(
                text, targets, mode_roll=0, target_roll=1
            ),
            EnemyAiDecision(ATTACK, target_slot=3),
        )
        with self.assertRaises(ValueError):
            resolve_common_normal_enemy_ai(
                text, targets, mode_roll=0, target_roll=2
            )

    def test_player_pet_scope_falls_back_to_all_only_when_empty(self):
        players = (
            target(0, "player", 100),
            target(1, "player", 80),
        )
        self.assertEqual(
            resolve_common_normal_enemy_ai(
                "at:1;3;1",
                players,
                mode_roll=0,
                target_roll=1,
            ),
            EnemyAiDecision(ATTACK, target_slot=1),
        )

        mixed = (
            target(0, "player", 100),
            target(1, "pet", 80),
        )
        self.assertEqual(
            resolve_common_normal_enemy_ai(
                "at:1;3;1",
                mixed,
                mode_roll=0,
                target_roll=0,
            ),
            EnemyAiDecision(ATTACK, target_slot=1),
        )

    def test_hp_max_min_keep_first_slot_on_tie(self):
        targets = (
            target(0, "player", 100),
            target(1, "pet", 100),
            target(2, "pet", 20),
            target(3, "pet", 20),
        )
        self.assertEqual(
            resolve_common_normal_enemy_ai(
                "at:1;1;2",
                targets,
                mode_roll=0,
            ),
            EnemyAiDecision(ATTACK, target_slot=0),
        )
        self.assertEqual(
            resolve_common_normal_enemy_ai(
                "at:1;1;3",
                targets,
                mode_roll=0,
            ),
            EnemyAiDecision(ATTACK, target_slot=2),
        )

    def test_invalid_target_selector_and_empty_targets_return_no_decision(self):
        self.assertIsNone(
            resolve_common_normal_enemy_ai(
                "at:1;1;0",
                (target(0, "player", 100),),
                mode_roll=0,
            )
        )
        self.assertIsNone(
            resolve_common_normal_enemy_ai(
                "at:1;1;1",
                (),
                mode_roll=0,
                target_roll=0,
            )
        )

    def test_compile_gated_rn_profile_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "_ENEMY_ATTACK_AI"):
            resolve_common_normal_enemy_ai(
                "at:1;1;2|rn:1",
                (target(0, "player", 100),),
                mode_roll=0,
            )

    def test_no_positive_action_returns_no_decision(self):
        self.assertIsNone(
            resolve_common_normal_enemy_ai(
                "at:0;1;1|gu:0|es:0|wa:0",
                (target(0, "player", 100),),
                mode_roll=0,
            )
        )


if __name__ == "__main__":
    unittest.main()
