import unittest

from tools.stoneage_battle_round_model import (
    BATTLE_COM_ATTACK,
    BATTLE_COM_WAIT,
    BattleCombatProfile,
    BattleCommand,
    OrdinaryAttackRolls,
    prepare_battle_round,
    resolve_ordinary_round,
)
from tools.stoneage_enemy_ai_relife_bridge import EnemyAiReLifeSubmission
from tools.stoneage_enemy_relife_model import EnemyReLifeRolls
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
    return EnemyAiReLifeSubmission(
        participant_id="enemy:caster",
        skill_slot=4,
        skill_id=500,
        callback="ENEMYSKILL_ReLife",
        source_attack_target_slot=target,
    )


class EnemyReLifeOrderedRuntimeTests(unittest.TestCase):
    def setup_round(self,*,player_attack=False,target=0):
        player=participant("player","player","player",1000,1000,10)
        caster=participant("enemy:caster","enemy","enemy",600,600,200)
        dead=participant("enemy:dead","enemy","enemy",0,101,20)
        prepared=prepare_battle_round(
            (player,caster),
            {
                "player":BattleCommand(
                    BATTLE_COM_ATTACK if player_attack else BATTLE_COM_WAIT,
                    command2=11 if player_attack else 0,
                ),
                "enemy:caster":BattleCommand(
                    BATTLE_COM_ATTACK,
                    command2=target,
                ),
            },
            {"player":0,"enemy:caster":0},
        )
        return prepared,dead,{
            "player":profile(),
            "enemy:caster":profile(),
            "enemy:dead":profile(),
        }

    def test_cross_round_dead_entry_is_revived_without_becoming_initiative_actor(self):
        prepared,dead,profiles=self.setup_round()
        resolved=resolve_ordinary_round(
            prepared,
            slots={"player":0,"enemy:caster":10},
            passive_battle_entries_by_slot={11:dead},
            revivable_dead_participant_ids=("enemy:dead",),
            profiles=profiles,
            attack_rolls={},
            defense_profile="newpower_70pct",
            enemy_relife_submissions_by_participant_id={
                "enemy:caster":submission(),
            },
            enemy_relife_rolls_by_participant_id={
                "enemy:caster":EnemyReLifeRolls(
                    dead_target_index=0,
                    revive_amount_roll=55,
                ),
            },
            enemy_relife_retarget_rolls_by_participant_id={
                "enemy:caster":None,
            },
        )
        event=next(e for e in resolved.events if e.result=="enemy_relife")
        self.assertEqual(event.resolved_target_slot,11)
        self.assertEqual((event.target_hp_before,event.target_hp_after),(0,55))
        self.assertEqual(resolved.hp_by_participant_id["enemy:dead"],55)
        self.assertEqual(
            resolved.action_order,
            ("enemy:caster","player"),
        )
        self.assertFalse(any(
            e.participant_id=="enemy:dead" for e in resolved.events
        ))

    def test_revived_entry_is_targetable_by_later_same_round_action(self):
        prepared,dead,profiles=self.setup_round(player_attack=True)
        resolved=resolve_ordinary_round(
            prepared,
            slots={"player":0,"enemy:caster":10},
            passive_battle_entries_by_slot={11:dead},
            revivable_dead_participant_ids=("enemy:dead",),
            profiles=profiles,
            attack_rolls={
                "player":OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                    minimum_damage_roll_0_1=1,
                ),
            },
            defense_profile="newpower_70pct",
            enemy_relife_submissions_by_participant_id={
                "enemy:caster":submission(),
            },
            enemy_relife_rolls_by_participant_id={
                "enemy:caster":EnemyReLifeRolls(0,55),
            },
            enemy_relife_retarget_rolls_by_participant_id={
                "enemy:caster":None,
            },
        )
        revive_index=next(
            i for i,e in enumerate(resolved.events)
            if e.result=="enemy_relife"
        )
        attack_index=next(
            i for i,e in enumerate(resolved.events)
            if e.participant_id=="player"
            and e.result in {"normal","critical","guard","dodge"}
        )
        self.assertLess(revive_index,attack_index)
        self.assertEqual(resolved.events[attack_index].resolved_target_slot,11)

    def test_no_revivable_dead_entry_falls_back_to_same_adjusted_attack_target(self):
        prepared,dead,profiles=self.setup_round()
        resolved=resolve_ordinary_round(
            prepared,
            slots={"player":0,"enemy:caster":10},
            passive_battle_entries_by_slot={11:dead},
            revivable_dead_participant_ids=(),
            profiles=profiles,
            attack_rolls={
                "enemy:caster":OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                    minimum_damage_roll_0_1=1,
                ),
            },
            defense_profile="newpower_70pct",
            enemy_relife_submissions_by_participant_id={
                "enemy:caster":submission(),
            },
            enemy_relife_rolls_by_participant_id={
                "enemy:caster":EnemyReLifeRolls(),
            },
            enemy_relife_retarget_rolls_by_participant_id={
                "enemy:caster":None,
            },
        )
        events=[e for e in resolved.events if e.participant_id=="enemy:caster"]
        self.assertEqual(events[0].result,"enemy_relife_fallback")
        self.assertTrue(events[0].enemy_relife_resolution.fallback_to_attack)
        self.assertEqual(events[0].resolved_target_slot,0)
        self.assertIn(events[1].result,{"normal","critical","guard","dodge"})
        self.assertEqual(events[1].resolved_target_slot,0)
        self.assertLess(resolved.hp_by_participant_id["player"],1000)

    def test_targetadjust_no_target_blocks_relife_effect_even_with_dead_ally(self):
        caster=participant("enemy:caster","enemy","enemy",600,600,200)
        dead_player=participant("player","player","player",0,1000,10)
        dead_ally=participant("enemy:dead","enemy","enemy",0,100,20)
        prepared=prepare_battle_round(
            (caster,),
            {"enemy:caster":BattleCommand(BATTLE_COM_ATTACK,command2=0)},
            {"enemy:caster":0},
        )
        resolved=resolve_ordinary_round(
            prepared,
            slots={"enemy:caster":10},
            passive_battle_entries_by_slot={0:dead_player,11:dead_ally},
            revivable_dead_participant_ids=("enemy:dead",),
            profiles={
                "enemy:caster":profile(),
                "player":profile(),
                "enemy:dead":profile(),
            },
            attack_rolls={},
            defense_profile="newpower_70pct",
            enemy_relife_submissions_by_participant_id={
                "enemy:caster":submission(),
            },
            enemy_relife_rolls_by_participant_id={
                "enemy:caster":EnemyReLifeRolls(),
            },
            enemy_relife_retarget_rolls_by_participant_id={
                "enemy:caster":0,
            },
        )
        event=next(e for e in resolved.events if e.participant_id=="enemy:caster")
        self.assertEqual(event.result,"enemy_relife_no_target")
        self.assertEqual(resolved.hp_by_participant_id["enemy:dead"],0)


if __name__=="__main__":
    unittest.main()
