import unittest

from tools.stoneage_battle_core_model import guard_damage
from tools.stoneage_battle_guardian_model import GuardianRegistration
from tools.stoneage_battle_round_model import (
    BATTLE_COM_ATTACK,
    BATTLE_COM_GUARD,
    BATTLE_COM_WAIT,
    BattleCombatProfile,
    BattleCommand,
    OrdinaryAttackRolls,
    prepare_battle_round,
    resolve_ordinary_round,
)
from tools.stoneage_enemy_ai_guard_break2_bridge import (
    EnemyAiGuardBreak2Submission,
)
from tools.stoneage_singleplayer_battle import BattleParticipant


def actor(
    pid,
    side,
    kind,
    *,
    hp=500,
    attack=100,
    defense=70,
    quick=50,
    level=10,
):
    return BattleParticipant(
        participant_id=pid,
        side=side,
        kind=kind,
        level=level,
        hp=hp,
        max_hp=hp,
        attack=attack,
        defense=defense,
        quick=quick,
        name=pid,
        fixed_vital=40,
    )


def profile(dex=100,luck=0):
    return BattleCombatProfile(
        fixed_dex=dex,
        fixed_luck=luck,
        earth=0,
        water=0,
        fire=0,
        wind=0,
    )


def submission(target=0):
    return EnemyAiGuardBreak2Submission(
        participant_id="enemy",
        skill_slot=0,
        skill_id=543,
        callback="PETSKILL_GuardBreak2",
        source_target_slot=target,
    )


class GuardBreak2RuntimeTests(unittest.TestCase):
    def test_guard_branch_scales_130_then_runs_guard_adjust(self):
        player=actor("player","player","player",defense=0,quick=10)
        enemy=actor("enemy","enemy","enemy",attack=300,quick=100)
        prepared=prepare_battle_round(
            (player,enemy),
            {
                "player":BattleCommand(BATTLE_COM_GUARD),
                "enemy":BattleCommand(BATTLE_COM_ATTACK,command2=0),
            },
            {"player":0,"enemy":0},
        )
        result=resolve_ordinary_round(
            prepared,
            slots={"player":0,"enemy":10},
            profiles={"player":profile(),"enemy":profile()},
            attack_rolls={
                "enemy":OrdinaryAttackRolls(
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                    guard_roll_1_100=100,
                )
            },
            guard_break2_submissions_by_participant_id={
                "enemy":submission()
            },
            defense_profile="newpower_70pct",
        )
        event=next(
            event for event in result.events
            if event.participant_id=="enemy"
            and event.guard_break2_resolution is not None
        )
        resolution=event.guard_break2_resolution
        self.assertTrue(resolution.defender_command_is_guard)
        self.assertEqual(resolution.multiplier,1.3)
        self.assertTrue(resolution.guard_adjust_applies_after_multiplier)
        self.assertEqual(
            resolution.damage_after_multiplier,
            int(resolution.damage_before*1.3),
        )
        self.assertEqual(
            event.damage,
            guard_damage(resolution.damage_after_multiplier,100),
        )

    def test_non_guard_branch_scales_70_without_guard_rng(self):
        player=actor("player","player","player",defense=0,quick=10)
        enemy=actor("enemy","enemy","enemy",attack=300,quick=100)
        prepared=prepare_battle_round(
            (player,enemy),
            {
                "player":BattleCommand(BATTLE_COM_WAIT),
                "enemy":BattleCommand(BATTLE_COM_ATTACK,command2=0),
            },
            {"player":0,"enemy":0},
        )
        result=resolve_ordinary_round(
            prepared,
            slots={"player":0,"enemy":10},
            profiles={"player":profile(),"enemy":profile()},
            attack_rolls={
                "enemy":OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                )
            },
            guard_break2_submissions_by_participant_id={
                "enemy":submission()
            },
            defense_profile="newpower_70pct",
        )
        event=next(
            event for event in result.events
            if event.guard_break2_resolution is not None
        )
        resolution=event.guard_break2_resolution
        self.assertFalse(resolution.defender_command_is_guard)
        self.assertEqual(resolution.multiplier,0.7)
        self.assertFalse(resolution.guard_adjust_applies_after_multiplier)
        self.assertEqual(
            event.damage,
            resolution.damage_after_multiplier,
        )

    def test_guardian_controls_multiplier_but_damage_sub_uses_original_target(self):
        player=actor("player","player","player",hp=500,defense=0,quick=20)
        guardian=actor("guardian","player","pet",hp=500,defense=0,quick=10)
        enemy=actor("enemy","enemy","enemy",hp=500,attack=300,quick=100)
        prepared=prepare_battle_round(
            (player,guardian,enemy),
            {
                "player":BattleCommand(BATTLE_COM_WAIT),
                "guardian":BattleCommand(BATTLE_COM_GUARD),
                "enemy":BattleCommand(BATTLE_COM_ATTACK,command2=0),
            },
            {"player":0,"guardian":0,"enemy":0},
        )
        result=resolve_ordinary_round(
            prepared,
            slots={"player":0,"guardian":1,"enemy":10},
            profiles={
                "player":profile(),
                "guardian":profile(),
                "enemy":profile(),
            },
            attack_rolls={
                "enemy":OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                    guard_roll_1_100=100,
                )
            },
            guardian_registrations_by_defender_slot={
                0:GuardianRegistration(guardian_slot=1)
            },
            guard_break2_submissions_by_participant_id={
                "enemy":submission()
            },
            defense_profile="newpower_70pct",
        )
        event=next(
            event for event in result.events
            if event.guard_break2_resolution is not None
        )
        self.assertTrue(event.guardian_redirected)
        self.assertEqual(event.guardian_slot,1)
        self.assertTrue(
            event.guard_break2_resolution.defender_command_is_guard
        )
        self.assertEqual(
            result.hp_by_participant_id["guardian"],
            500,
        )
        self.assertLess(
            result.hp_by_participant_id["player"],
            500,
        )


if __name__=="__main__":
    unittest.main()
