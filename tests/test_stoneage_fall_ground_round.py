import unittest

from tools.stoneage_battle_damage_react_model import BaseDamageReactState
from tools.stoneage_battle_ride_damage_model import RidePetRuntime
from tools.stoneage_battle_round_model import (
    BATTLE_COM_ATTACK,
    BATTLE_COM_WAIT,
    BattleCombatProfile,
    BattleCommand,
    BattleCommandSetupEffects,
    OrdinaryAttackRolls,
    prepare_battle_round,
    resolve_ordinary_round,
)
from tools.stoneage_enemy_ai_fall_ground_bridge import (
    EnemyAiFallGroundSubmission,
)
from tools.stoneage_fall_ground_model import parse_fall_ground_option
from tools.stoneage_singleplayer_battle import BattleParticipant


def actor(pid,side,kind,hp,max_hp,attack,defense,quick):
    return BattleParticipant(
        participant_id=pid,side=side,kind=kind,level=80,
        hp=hp,max_hp=max_hp,attack=attack,defense=defense,quick=quick,
        name=None,
    )


def prof(dex):
    return BattleCombatProfile(
        fixed_dex=dex,fixed_luck=0,
        earth=0,water=0,fire=0,wind=0,
    )


def submission(target=0):
    return EnemyAiFallGroundSubmission(
        participant_id="enemy:fall",
        skill_slot=0,
        skill_id=210,
        callback="PETSKILL_FallGround",
        source_target_slot=target,
        option=parse_fall_ground_option("攻%-30"),
    )


def attack_roll(**overrides):
    values=dict(
        dodge_roll_1_10000=10000,
        critical_roll_1_10000=10000,
        damage_roll=0,
        minimum_damage_roll_0_1=1,
    )
    values.update(overrides)
    return OrdinaryAttackRolls(**values)


class FallGroundRoundTests(unittest.TestCase):
    def base(self,*,ride_slot=1,ride=True):
        player=actor("player","player","player",1000,1000,0,0,10)
        enemy=actor("enemy:fall","enemy","enemy",500,500,200,0,200)
        prepared=prepare_battle_round(
            (player,enemy),
            {
                "player":BattleCommand(BATTLE_COM_WAIT),
                "enemy:fall":BattleCommand(BATTLE_COM_ATTACK,command2=0),
            },
            {"player":0,"enemy:fall":0},
        )
        runtime=(
            RidePetRuntime(
                rider_id="player",pet_id=f"pet:{ride_slot}",
                hp=1000,max_hp=1000,defense_power=100,
            )
            if ride else None
        )
        return prepared,player,enemy,runtime

    def resolve(self,*,ride_slot=1,ride=True,fall_roll=100,react=None):
        prepared,player,enemy,runtime=self.base(
            ride_slot=ride_slot,ride=ride
        )
        kwargs={}
        if react is not None:
            kwargs["base_damage_react_state_by_participant_id"]={
                "player":react,
                "enemy:fall":BaseDamageReactState(),
            }
        return resolve_ordinary_round(
            prepared,
            slots={"player":0,"enemy:fall":10},
            profiles={"player":prof(10),"enemy:fall":prof(200)},
            attack_rolls={"enemy:fall":attack_roll()},
            defense_profile="newpower_70pct",
            command_setup_effects_by_participant_id={
                "enemy:fall":BattleCommandSetupEffects(attack_power=140),
            },
            ride_pet_runtime=runtime,
            ride_pet_source_slot=(ride_slot if ride else None),
            fall_ground_submissions_by_participant_id={
                "enemy:fall":submission(),
            },
            fall_ground_rolls_by_participant_id={
                "enemy:fall":fall_roll,
            },
            fall_ground_equipment_resistance_by_participant_id={
                "player":0,
            },
            **kwargs,
        )

    def test_successful_roll_unmounts_nonzero_source_pet_slot(self):
        result=self.resolve(ride_slot=1,fall_roll=100)
        event=next(
            e for e in result.events
            if e.participant_id=="enemy:fall"
            and e.fall_ground_resolution is not None
        )
        self.assertEqual(event.fall_ground_resolution.threshold,50)
        self.assertTrue(event.fall_ground_resolution.fell)
        self.assertFalse(result.ride_pet_runtime.mounted)
        self.assertTrue(result.ride_pet_runtime.petfall)

    def test_historical_slot_zero_bug_remains_mounted(self):
        result=self.resolve(ride_slot=0,fall_roll=100)
        event=next(
            e for e in result.events
            if e.participant_id=="enemy:fall"
            and e.fall_ground_resolution is not None
        )
        self.assertTrue(event.fall_ground_resolution.roll_passed)
        self.assertFalse(event.fall_ground_resolution.fell)
        self.assertTrue(result.ride_pet_runtime.mounted)

    def test_strict_roll_50_does_not_fall(self):
        result=self.resolve(ride_slot=1,fall_roll=50)
        event=next(
            e for e in result.events
            if e.participant_id=="enemy:fall"
            and e.fall_ground_resolution is not None
        )
        self.assertFalse(event.fall_ground_resolution.roll_passed)
        self.assertTrue(result.ride_pet_runtime.mounted)

    def test_damage_react_blocks_fall_and_requires_no_rng(self):
        result=self.resolve(
            ride_slot=1,
            fall_roll=None,
            react=BaseDamageReactState(vanish=1),
        )
        event=next(
            e for e in result.events
            if e.participant_id=="enemy:fall"
            and e.fall_ground_resolution is not None
        )
        self.assertFalse(event.fall_ground_resolution.rng_consumed)
        self.assertTrue(result.ride_pet_runtime.mounted)

    def test_nonzero_equipment_resistance_fails_closed(self):
        prepared,player,enemy,runtime=self.base()
        with self.assertRaisesRegex(ValueError,"cross-descendant"):
            resolve_ordinary_round(
                prepared,
                slots={"player":0,"enemy:fall":10},
                profiles={"player":prof(10),"enemy:fall":prof(200)},
                attack_rolls={"enemy:fall":attack_roll()},
                defense_profile="newpower_70pct",
                command_setup_effects_by_participant_id={
                    "enemy:fall":BattleCommandSetupEffects(attack_power=140),
                },
                ride_pet_runtime=runtime,
                ride_pet_source_slot=1,
                fall_ground_submissions_by_participant_id={
                    "enemy:fall":submission(),
                },
                fall_ground_rolls_by_participant_id={"enemy:fall":100},
                fall_ground_equipment_resistance_by_participant_id={
                    "player":10,
                },
            )

    def test_callback_attack_power_setup_must_be_exact_70_percent(self):
        prepared,player,enemy,runtime=self.base()
        with self.assertRaisesRegex(ValueError,"attack-power setup effect drift"):
            resolve_ordinary_round(
                prepared,
                slots={"player":0,"enemy:fall":10},
                profiles={"player":prof(10),"enemy:fall":prof(200)},
                attack_rolls={"enemy:fall":attack_roll()},
                defense_profile="newpower_70pct",
                command_setup_effects_by_participant_id={
                    "enemy:fall":BattleCommandSetupEffects(attack_power=200),
                },
                ride_pet_runtime=runtime,
                ride_pet_source_slot=1,
                fall_ground_submissions_by_participant_id={
                    "enemy:fall":submission(),
                },
                fall_ground_rolls_by_participant_id={"enemy:fall":100},
                fall_ground_equipment_resistance_by_participant_id={
                    "player":0,
                },
            )


if __name__=="__main__":
    unittest.main()
