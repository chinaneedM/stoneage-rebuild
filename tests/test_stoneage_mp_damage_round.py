import unittest

from tools.stoneage_battle_damage_react_model import BaseDamageReactState
from tools.stoneage_battle_round_model import (
    BATTLE_COM_ATTACK,
    BATTLE_COM_WAIT,
    BattleCombatProfile,
    BattleCommand,
    OrdinaryAttackRolls,
    prepare_battle_round,
    resolve_ordinary_round,
)
from tools.stoneage_enemy_ai_mp_damage_bridge import EnemyAiMpDamageSubmission
from tools.stoneage_mp_damage_model import parse_mp_damage_option
from tools.stoneage_singleplayer_battle import BattleParticipant


def actor(pid,side,kind,hp,max_hp,attack,defense,quick):
    return BattleParticipant(
        participant_id=pid,side=side,kind=kind,level=80,
        hp=hp,max_hp=max_hp,attack=attack,defense=defense,quick=quick,
        name=None,
    )


def profile(dex):
    return BattleCombatProfile(
        fixed_dex=dex,fixed_luck=0,
        earth=0,water=0,fire=0,wind=0,
    )


def submission(pid,skill_id,target=0):
    option={506:"50|50",507:"50|75",508:"50|100"}[skill_id]
    return EnemyAiMpDamageSubmission(
        participant_id=pid,
        skill_slot=0,
        skill_id=skill_id,
        callback="PETSKILL_MpDamage",
        source_target_slot=target,
        option=parse_mp_damage_option(option),
    )


def hit_roll():
    return OrdinaryAttackRolls(
        dodge_roll_1_10000=10000,
        critical_roll_1_10000=10000,
        damage_roll=0,
        minimum_damage_roll_0_1=1,
    )


class MpDamageRoundTests(unittest.TestCase):
    def test_positive_hit_removes_percent_of_current_player_mp(self):
        player=actor("player","player","player",1000,1000,0,0,10)
        enemy=actor("enemy:mp","enemy","enemy",500,500,300,0,200)
        prepared=prepare_battle_round(
            (player,enemy),
            {
                "player":BattleCommand(BATTLE_COM_WAIT),
                "enemy:mp":BattleCommand(BATTLE_COM_ATTACK,command2=0),
            },
            {"player":0,"enemy:mp":0},
        )
        result=resolve_ordinary_round(
            prepared,
            slots={"player":0,"enemy:mp":10},
            profiles={"player":profile(10),"enemy:mp":profile(200)},
            attack_rolls={"enemy:mp":hit_roll()},
            defense_profile="newpower_70pct",
            mp_damage_submissions_by_participant_id={
                "enemy:mp":submission("enemy:mp",506),
            },
            mp_by_participant_id={"player":40},
        )
        event=next(e for e in result.events if e.mp_damage_resolution)
        self.assertEqual(event.mp_damage_resolution.mp_before,40)
        self.assertEqual(event.mp_damage_resolution.mp_damage,20)
        self.assertEqual(event.mp_damage_resolution.mp_after,20)
        self.assertEqual(result.mp_by_participant_id["player"],20)

    def test_two_attackers_consume_updated_mp_in_action_order(self):
        player=actor("player","player","player",5000,5000,0,0,10)
        first=actor("enemy:first","enemy","enemy",500,500,150,0,300)
        second=actor("enemy:second","enemy","enemy",500,500,150,0,200)
        prepared=prepare_battle_round(
            (player,first,second),
            {
                "player":BattleCommand(BATTLE_COM_WAIT),
                "enemy:first":BattleCommand(BATTLE_COM_ATTACK,command2=0),
                "enemy:second":BattleCommand(BATTLE_COM_ATTACK,command2=0),
            },
            {"player":0,"enemy:first":0,"enemy:second":0},
        )
        result=resolve_ordinary_round(
            prepared,
            slots={"player":0,"enemy:first":10,"enemy:second":11},
            profiles={
                "player":profile(10),
                "enemy:first":profile(200),
                "enemy:second":profile(200),
            },
            attack_rolls={
                "enemy:first":hit_roll(),
                "enemy:second":hit_roll(),
            },
            defense_profile="newpower_70pct",
            mp_damage_submissions_by_participant_id={
                "enemy:first":submission("enemy:first",506),
                "enemy:second":submission("enemy:second",507),
            },
            mp_by_participant_id={"player":40},
        )
        effects=[e.mp_damage_resolution for e in result.events
                 if e.mp_damage_resolution is not None]
        self.assertEqual([(x.mp_before,x.mp_after) for x in effects],
                         [(40,20),(20,5)])
        self.assertEqual(result.mp_by_participant_id["player"],5)

    def test_pet_target_is_excluded_without_pet_mp_state(self):
        pet=actor("pet","player","pet",1000,1000,0,0,10)
        enemy=actor("enemy:mp","enemy","enemy",500,500,300,0,200)
        prepared=prepare_battle_round(
            (pet,enemy),
            {
                "pet":BattleCommand(BATTLE_COM_WAIT),
                "enemy:mp":BattleCommand(BATTLE_COM_ATTACK,command2=5),
            },
            {"pet":5,"enemy:mp":10},
        )
        result=resolve_ordinary_round(
            prepared,
            slots={"pet":5,"enemy:mp":10},
            profiles={"pet":profile(10),"enemy:mp":profile(200)},
            attack_rolls={"enemy:mp":hit_roll()},
            defense_profile="newpower_70pct",
            mp_damage_submissions_by_participant_id={
                "enemy:mp":submission("enemy:mp",506,target=5),
            },
            mp_by_participant_id={},
        )
        effect=next(e.mp_damage_resolution for e in result.events
                    if e.mp_damage_resolution is not None)
        self.assertFalse(effect.attempted)
        self.assertEqual(dict(result.mp_by_participant_id),{})

    def test_damage_react_blocks_mp_effect(self):
        player=actor("player","player","player",1000,1000,0,0,10)
        enemy=actor("enemy:mp","enemy","enemy",500,500,300,0,200)
        prepared=prepare_battle_round(
            (player,enemy),
            {
                "player":BattleCommand(BATTLE_COM_WAIT),
                "enemy:mp":BattleCommand(BATTLE_COM_ATTACK,command2=0),
            },
            {"player":0,"enemy:mp":0},
        )
        result=resolve_ordinary_round(
            prepared,
            slots={"player":0,"enemy:mp":10},
            profiles={"player":profile(10),"enemy:mp":profile(200)},
            attack_rolls={"enemy:mp":hit_roll()},
            defense_profile="newpower_70pct",
            base_damage_react_state_by_participant_id={
                "player":BaseDamageReactState(vanish=1),
                "enemy:mp":BaseDamageReactState(),
            },
            mp_damage_submissions_by_participant_id={
                "enemy:mp":submission("enemy:mp",506),
            },
            mp_by_participant_id={"player":40},
        )
        self.assertFalse(any(e.mp_damage_resolution for e in result.events))
        self.assertEqual(result.mp_by_participant_id["player"],40)


if __name__=="__main__":
    unittest.main()
