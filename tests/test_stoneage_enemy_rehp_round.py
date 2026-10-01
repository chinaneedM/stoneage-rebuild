import unittest

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
from tools.stoneage_enemy_ai_rehp_bridge import EnemyAiReHpSubmission
from tools.stoneage_enemy_rehp_model import EnemyReHpRolls
from tools.stoneage_singleplayer_battle import BattleParticipant


def participant(pid,side,kind,hp,max_hp,quick):
    return BattleParticipant(
        participant_id=pid,
        side=side,
        kind=kind,
        level=80,
        hp=hp,
        max_hp=max_hp,
        attack=120,
        defense=20,
        quick=quick,
        name=None,
    )


def profile():
    return BattleCombatProfile(
        fixed_dex=100,
        fixed_luck=0,
        earth=0,
        water=0,
        fire=0,
        wind=0,
    )


def submission(target=0):
    return EnemyAiReHpSubmission(
        participant_id="enemy:caster",
        skill_slot=0,
        skill_id=501,
        callback="ENEMYSKILL_ReHP",
        source_target_slot=target,
    )


class EnemyReHpRoundTests(unittest.TestCase):
    def prepared(self, ally_hp=100, target=0):
        player=participant("player","player","player",1000,1000,10)
        caster=participant("enemy:caster","enemy","enemy",600,600,200)
        ally=participant("enemy:ally","enemy","enemy",ally_hp,600,20)
        prepared=prepare_battle_round(
            (player,caster,ally),
            {
                "player":BattleCommand(BATTLE_COM_WAIT),
                "enemy:caster":BattleCommand(BATTLE_COM_ATTACK,command2=target),
                "enemy:ally":BattleCommand(BATTLE_COM_GUARD),
            },
            {"player":0,"enemy:caster":0,"enemy:ally":0},
        )
        return prepared,{
            "player":profile(),
            "enemy:caster":profile(),
            "enemy:ally":profile(),
        }

    def test_success_heals_enemy_ally_without_ordinary_attack_rng(self):
        prepared,profiles=self.prepared(ally_hp=100)
        resolved=resolve_ordinary_round(
            prepared,
            slots={"player":0,"enemy:caster":10,"enemy:ally":11},
            profiles=profiles,
            attack_rolls={},
            defense_profile="newpower_70pct",
            enemy_rehp_submissions_by_participant_id={
                "enemy:caster":submission(),
            },
            enemy_rehp_rolls_by_participant_id={
                "enemy:caster":EnemyReHpRolls(0,100,100),
            },
            enemy_rehp_retarget_rolls_by_participant_id={
                "enemy:caster":None,
            },
        )
        event=next(
            e for e in resolved.events
            if e.participant_id=="enemy:caster" and e.result=="enemy_rehp"
        )
        self.assertEqual(event.command1,BATTLE_COM_ATTACK)
        self.assertEqual(event.resolved_target_slot,11)
        self.assertEqual(event.target_hp_before,100)
        self.assertEqual(event.target_hp_after,200)
        self.assertIsNotNone(event.enemy_rehp_resolution)
        self.assertEqual(resolved.hp_by_participant_id["player"],1000)
        self.assertEqual(resolved.hp_by_participant_id["enemy:ally"],200)

    def test_no_eligible_ally_falls_back_to_same_adjusted_physical_target(self):
        prepared,profiles=self.prepared(ally_hp=600)
        resolved=resolve_ordinary_round(
            prepared,
            slots={"player":0,"enemy:caster":10,"enemy:ally":11},
            profiles=profiles,
            attack_rolls={
                "enemy:caster":OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                    minimum_damage_roll_0_1=1,
                )
            },
            defense_profile="newpower_70pct",
            enemy_rehp_submissions_by_participant_id={
                "enemy:caster":submission(),
            },
            enemy_rehp_rolls_by_participant_id={
                "enemy:caster":EnemyReHpRolls(),
            },
            enemy_rehp_retarget_rolls_by_participant_id={
                "enemy:caster":None,
            },
        )
        events=[
            e for e in resolved.events
            if e.participant_id=="enemy:caster"
        ]
        self.assertEqual(events[0].result,"enemy_rehp_fallback")
        self.assertTrue(events[0].enemy_rehp_resolution.fallback_to_attack)
        self.assertIn(events[1].result,{"normal","critical","guard"})
        self.assertEqual(events[1].resolved_target_slot,0)
        self.assertLess(resolved.hp_by_participant_id["player"],1000)

    def test_dead_submitted_target_consumes_explicit_targetadjust_roll(self):
        prepared,profiles=self.prepared(ally_hp=100,target=9)
        resolved=resolve_ordinary_round(
            prepared,
            slots={"player":0,"enemy:caster":10,"enemy:ally":11},
            profiles=profiles,
            attack_rolls={},
            defense_profile="newpower_70pct",
            enemy_rehp_submissions_by_participant_id={
                "enemy:caster":submission(9),
            },
            enemy_rehp_rolls_by_participant_id={
                "enemy:caster":EnemyReHpRolls(0,100,100),
            },
            enemy_rehp_retarget_rolls_by_participant_id={
                "enemy:caster":0,
            },
        )
        event=next(e for e in resolved.events if e.result=="enemy_rehp")
        self.assertTrue(event.retargeted)
        self.assertEqual(
            event.enemy_rehp_resolution.adjusted_attack_target_slot,
            0,
        )

    def test_success_rejects_unused_fallback_attack_rng(self):
        prepared,profiles=self.prepared(ally_hp=100)
        with self.assertRaisesRegex(ValueError,"unused fallback attack RNG"):
            resolve_ordinary_round(
                prepared,
                slots={"player":0,"enemy:caster":10,"enemy:ally":11},
                profiles=profiles,
                attack_rolls={
                    "enemy:caster":OrdinaryAttackRolls(
                        critical_roll_1_10000=10000,
                        damage_roll=0,
                    )
                },
                defense_profile="newpower_70pct",
                enemy_rehp_submissions_by_participant_id={
                    "enemy:caster":submission(),
                },
                enemy_rehp_rolls_by_participant_id={
                    "enemy:caster":EnemyReHpRolls(0,100,100),
                },
                enemy_rehp_retarget_rolls_by_participant_id={
                    "enemy:caster":None,
                },
            )


if __name__ == "__main__":
    unittest.main()
