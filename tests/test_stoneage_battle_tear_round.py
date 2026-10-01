import unittest
from tools.stoneage_battle_damage_react_model import BaseDamageReactState
from tools.stoneage_battle_ride_damage_model import RidePetRuntime
from tools.stoneage_battle_round_model import (
    BATTLE_COM_ATTACK,BATTLE_COM_WAIT,BattleCombatProfile,BattleCommand,
    BattleCommandSetupEffects,OrdinaryAttackRolls,prepare_battle_round,
    resolve_ordinary_round,
)
from tools.stoneage_enemy_ai_battle_tear_bridge import EnemyAiBattleTearSubmission
from tools.stoneage_singleplayer_battle import BattleParticipant
def actor(pid,side,kind,hp,max_hp,attack,defense,quick):
    return BattleParticipant(participant_id=pid,side=side,kind=kind,level=80,
        hp=hp,max_hp=max_hp,attack=attack,defense=defense,quick=quick,name=None)
def prof(dex):
    return BattleCombatProfile(fixed_dex=dex,fixed_luck=0,earth=0,water=0,fire=0,wind=0)
def submission(skill=615):
    return EnemyAiBattleTearSubmission(
        participant_id="enemy:tear",skill_slot=0,skill_id=skill,
        callback="PETSKILL_BattleTearDamage",source_target_slot=0,
        wound_percent={615:20,616:50}[skill],
    )
def hitroll():
    return OrdinaryAttackRolls(dodge_roll_1_10000=10000,
        critical_roll_1_10000=10000,damage_roll=0,minimum_damage_roll_0_1=1)
class BattleTearRoundTests(unittest.TestCase):
    def resolve(self,player_hp=500,skill=615,ride=None,react=None):
        p=actor("player","player","player",player_hp,1000,0,0,10)
        e=actor("enemy:tear","enemy","enemy",500,500,200,100,200)
        prepared=prepare_battle_round((p,e),{
            "player":BattleCommand(BATTLE_COM_WAIT),
            "enemy:tear":BattleCommand(BATTLE_COM_ATTACK,command2=0),
        },{"player":0,"enemy:tear":0})
        kw={}
        if react is not None:
            kw["base_damage_react_state_by_participant_id"]={
                "player":react,"enemy:tear":BaseDamageReactState(),
            }
        return resolve_ordinary_round(
            prepared,slots={"player":0,"enemy:tear":10},
            profiles={"player":prof(10),"enemy:tear":prof(200)},
            attack_rolls={"enemy:tear":hitroll()},defense_profile="newpower_70pct",
            command_setup_effects_by_participant_id={
                "enemy:tear":BattleCommandSetupEffects(attack_power=180,defense_power=80)
            },
            ride_pet_runtime=ride,
            battle_tear_submissions_by_participant_id={"enemy:tear":submission(skill)},
            **kw,
        )
    def test_twenty_percent_wound_is_added(self):
        r=self.resolve(500,615)
        a=next(e.battle_tear_augmentation for e in r.events if e.battle_tear_augmentation)
        self.assertEqual((a.option_percent,a.wound_basis,a.wound_damage),(20,500,100))
        self.assertGreater(a.damage_after,a.damage_before)
    def test_full_hp_zeroes_physical_damage(self):
        r=self.resolve(1000,616)
        e=next(e for e in r.events if e.battle_tear_augmentation)
        self.assertTrue(e.battle_tear_augmentation.zeroed_physical_damage)
        self.assertEqual(e.battle_tear_augmentation.damage_after,0)
        self.assertEqual(r.hp_by_participant_id["player"],1000)
    def test_ride_missing_hp_is_in_wound_basis(self):
        ride=RidePetRuntime(rider_id="player",pet_id="pet:1",hp=500,max_hp=1000,defense_power=100)
        r=self.resolve(800,616,ride=ride)
        a=next(e.battle_tear_augmentation for e in r.events if e.battle_tear_augmentation)
        self.assertEqual((a.wound_basis,a.wound_damage),(700,350))
    def test_damage_react_skips_wound_mutation(self):
        r=self.resolve(500,615,react=BaseDamageReactState(vanish=1))
        a=next(e.battle_tear_augmentation for e in r.events if e.battle_tear_augmentation)
        self.assertFalse(a.applied)
        self.assertEqual(a.damage_after,a.damage_before)
    def test_setup_must_match_callback(self):
        p=actor("player","player","player",500,1000,0,0,10)
        e=actor("enemy:tear","enemy","enemy",500,500,200,100,200)
        prepared=prepare_battle_round((p,e),{
            "player":BattleCommand(BATTLE_COM_WAIT),
            "enemy:tear":BattleCommand(BATTLE_COM_ATTACK,command2=0),
        },{"player":0,"enemy:tear":0})
        with self.assertRaisesRegex(ValueError,"attack/defense setup effect drift"):
            resolve_ordinary_round(
                prepared,slots={"player":0,"enemy:tear":10},
                profiles={"player":prof(10),"enemy:tear":prof(200)},
                attack_rolls={"enemy:tear":hitroll()},defense_profile="newpower_70pct",
                command_setup_effects_by_participant_id={
                    "enemy:tear":BattleCommandSetupEffects(attack_power=200,defense_power=100)
                },
                battle_tear_submissions_by_participant_id={"enemy:tear":submission()},
            )
if __name__=="__main__": unittest.main()
