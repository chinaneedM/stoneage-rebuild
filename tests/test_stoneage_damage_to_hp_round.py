import unittest

from tools.stoneage_battle_damage_react_model import BaseDamageReactState
from tools.stoneage_battle_ride_damage_model import RidePetRuntime
from tools.stoneage_battle_round_model import (
    BATTLE_COM_ATTACK,
    BATTLE_COM_WAIT,
    BattleCombatProfile,
    BattleCommand,
    OrdinaryAttackRolls,
    prepare_battle_round,
    resolve_ordinary_round,
)
from tools.stoneage_damage_to_hp_model import parse_damage_to_hp_option
from tools.stoneage_enemy_ai_damage_to_hp_bridge import (
    EnemyAiDamageToHpSubmission,
)
from tools.stoneage_singleplayer_battle import BattleParticipant


def actor(pid,side,kind,hp,max_hp,attack,defense,quick):
    return BattleParticipant(
        participant_id=pid,
        side=side,
        kind=kind,
        level=80,
        hp=hp,
        max_hp=max_hp,
        attack=attack,
        defense=defense,
        quick=quick,
        name=None,
    )


def prof(dex=100):
    return BattleCombatProfile(
        fixed_dex=dex,fixed_luck=0,
        earth=0,water=0,fire=0,wind=0,
    )


def submission(skill_id=503,target=0):
    option={503:"30|50",504:"20|70",505:"10|100"}[skill_id]
    return EnemyAiDamageToHpSubmission(
        participant_id="enemy:drain",
        skill_slot=0,
        skill_id=skill_id,
        callback="PETSKILL_DamageToHp",
        source_target_slot=target,
        option=parse_damage_to_hp_option(option),
    )


class DamageToHpRoundTests(unittest.TestCase):
    def base(self,*,player_hp=1000,enemy_hp=100):
        player=actor("player","player","player",player_hp,1000,0,0,10)
        enemy=actor("enemy:drain","enemy","enemy",enemy_hp,600,300,0,200)
        prepared=prepare_battle_round(
            (player,enemy),
            {
                "player":BattleCommand(BATTLE_COM_WAIT),
                "enemy:drain":BattleCommand(BATTLE_COM_ATTACK,command2=0),
            },
            {"player":0,"enemy:drain":0},
        )
        return prepared,{"player":prof(10),"enemy:drain":prof(200)}

    def attack_roll(self):
        return OrdinaryAttackRolls(
            dodge_roll_1_10000=10000,
            critical_roll_1_10000=10000,
            damage_roll=0,
            minimum_damage_roll_0_1=1,
        )

    def test_successful_physical_hit_recovers_selected_percent(self):
        prepared,profiles=self.base()
        resolved=resolve_ordinary_round(
            prepared,
            slots={"player":0,"enemy:drain":10},
            profiles=profiles,
            attack_rolls={"enemy:drain":self.attack_roll()},
            defense_profile="newpower_70pct",
            damage_to_hp_submissions_by_participant_id={
                "enemy:drain":submission(503),
            },
        )
        event=next(
            e for e in resolved.events
            if e.participant_id=="enemy:drain" and e.damage_to_hp_recovery
        )
        recovery=event.damage_to_hp_recovery
        self.assertEqual(recovery.recovery_percent,50)
        self.assertEqual(
            recovery.reported_recovery,
            min(500,int(recovery.damage_basis*0.5)),
        )
        self.assertGreater(
            resolved.hp_by_participant_id["enemy:drain"],100
        )

    def test_target_damage_react_demotes_special_heal(self):
        prepared,profiles=self.base()
        resolved=resolve_ordinary_round(
            prepared,
            slots={"player":0,"enemy:drain":10},
            profiles=profiles,
            attack_rolls={"enemy:drain":self.attack_roll()},
            defense_profile="newpower_70pct",
            base_damage_react_state_by_participant_id={
                "player":BaseDamageReactState(vanish=1),
                "enemy:drain":BaseDamageReactState(),
            },
            damage_to_hp_submissions_by_participant_id={
                "enemy:drain":submission(503),
            },
        )
        attack_event=next(
            e for e in resolved.events
            if e.participant_id=="enemy:drain"
        )
        self.assertIsNone(attack_event.damage_to_hp_recovery)
        self.assertEqual(
            resolved.hp_by_participant_id["enemy:drain"],100
        )

    def test_mounted_target_recovery_basis_is_rider_plus_pet_damage(self):
        prepared,profiles=self.base()
        ride=RidePetRuntime(
            rider_id="player",
            pet_id="ride:1",
            hp=500,max_hp=500,
            defense_power=100,
        )
        resolved=resolve_ordinary_round(
            prepared,
            slots={"player":0,"enemy:drain":10},
            profiles=profiles,
            attack_rolls={"enemy:drain":self.attack_roll()},
            defense_profile="newpower_70pct",
            ride_pet_runtime=ride,
            damage_to_hp_submissions_by_participant_id={
                "enemy:drain":submission(503),
            },
        )
        event=next(
            e for e in resolved.events
            if e.participant_id=="enemy:drain" and e.damage_to_hp_recovery
        )
        self.assertIsNotNone(event.ride_damage_split)
        split=event.ride_damage_split
        self.assertEqual(
            event.damage_to_hp_recovery.damage_basis,
            split.rider_amount+split.pet_amount,
        )

    def test_retarget_uses_ordinary_targetadjust_once(self):
        player=actor("player","player","player",1000,1000,0,0,10)
        enemy=actor("enemy:drain","enemy","enemy",100,600,300,0,200)
        prepared=prepare_battle_round(
            (player,enemy),
            {
                "player":BattleCommand(BATTLE_COM_WAIT),
                "enemy:drain":BattleCommand(BATTLE_COM_ATTACK,command2=9),
            },
            {"player":0,"enemy:drain":0},
        )
        resolved=resolve_ordinary_round(
            prepared,
            slots={"player":0,"enemy:drain":10},
            profiles={"player":prof(10),"enemy:drain":prof(200)},
            attack_rolls={
                "enemy:drain":OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                    minimum_damage_roll_0_1=1,
                    retarget_roll=0,
                )
            },
            defense_profile="newpower_70pct",
            damage_to_hp_submissions_by_participant_id={
                "enemy:drain":submission(503,target=9),
            },
        )
        event=next(
            e for e in resolved.events
            if e.participant_id=="enemy:drain" and e.damage_to_hp_recovery
        )
        self.assertTrue(event.retargeted)
        self.assertEqual(event.resolved_target_slot,0)


if __name__ == "__main__":
    unittest.main()
