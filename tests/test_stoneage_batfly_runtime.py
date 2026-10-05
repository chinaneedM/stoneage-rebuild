import unittest

from tools.stoneage_batfly_reference_model import CALLBACK_NAME, resolve_batfly_setup
from tools.stoneage_enemy_ai_batfly_bridge import EnemyAiBatFlySubmission
from tools.stoneage_battle_round_model import (
    BATTLE_COM_ATTACK,
    BATTLE_COM_WAIT,
    BattleCombatProfile,
    BattleCommand,
)
from tools.stoneage_battle_state_model import (
    begin_persistent_battle,
    resolve_persistent_ordinary_round,
)
from tools.stoneage_singleplayer_battle import BattleParticipant, BattleSession
from tools.stoneage_singleplayer_domain import (
    EncounterRequest,
    EnemyVariantId,
    MapPosition,
    PetTemplateId,
)


def actor(pid,side,kind,*,hp=100,max_hp=None,attack=50,defense=10,quick=20,source_pet_slot=None):
    return BattleParticipant(
        participant_id=pid,
        side=side,
        kind=kind,
        level=20,
        hp=int(hp),
        max_hp=int(hp if max_hp is None else max_hp),
        attack=int(attack),
        defense=int(defense),
        quick=int(quick),
        name=pid,
        fixed_vital=40,
        source_pet_slot=source_pet_slot,
    )


def profile(*,dex=20):
    return BattleCombatProfile(
        fixed_dex=int(dex),
        fixed_luck=0,
        earth=0,
        water=0,
        fire=0,
        wind=0,
    )


def session(player,enemies,*,pets=(),ride_pet=None):
    encounter=EncounterRequest(
        position=MapPosition(2000,10,10),
        area_index=1,
        group_id=1,
        enemy_variant_id=EnemyVariantId(10),
        pet_template_id=PetTemplateId(20),
        level=5,
        max_enemy_count=max(1,len(enemies)),
    )
    return BattleSession(
        origin_position=encounter.position,
        encounter=encounter,
        player=player,
        allied_pets=tuple(pets),
        enemies=tuple(enemies),
        ride_pet=ride_pet,
    )


def submission(*,target_slot=0,participant_id="enemy",skill_slot=0):
    return EnemyAiBatFlySubmission(
        participant_id=participant_id,
        skill_slot=skill_slot,
        skill_id=633,
        callback=CALLBACK_NAME,
        source_target_slot=target_slot,
        setup=resolve_batfly_setup(
            target_slot=target_slot,
            skill_array=0,
            packed_com3_before=0,
        ),
    )


class BatFlyRuntimeTests(unittest.TestCase):
    def resolve(self,state,sub,*,retarget_roll=None):
        living=[
            participant
            for participant in (
                state.session.player,
                *state.session.allied_pets,
                *state.session.enemies,
            )
            if (
                participant.participant_id in state.hp_by_participant_id
                and state.hp_by_participant_id[participant.participant_id] > 0
                and participant.participant_id not in state.battle_exited_participant_ids
                and participant.participant_id not in state.ultimate_exited_participant_ids
            )
        ]
        commands={
            participant.participant_id:(
                BattleCommand(BATTLE_COM_ATTACK,command2=sub.source_target_slot)
                if participant.participant_id==sub.participant_id
                else BattleCommand(BATTLE_COM_WAIT)
            )
            for participant in living
        }
        initiatives={
            participant.participant_id:0 for participant in living
        }
        profiles={
            participant.participant_id:profile(dex=participant.quick)
            for participant in living
        }
        return resolve_persistent_ordinary_round(
            state,
            commands=commands,
            initiative_random_subtracts=initiatives,
            profiles=profiles,
            attack_rolls={},
            defense_profile="newpower_70pct",
            batfly_submissions_by_participant_id={sub.participant_id:sub},
            batfly_retarget_rolls_by_participant_id={
                sub.participant_id:retarget_roll
            },
            tie_break_order=(sub.participant_id,)+tuple(
                participant.participant_id
                for participant in living
                if participant.participant_id!=sub.participant_id
            ),
        )

    def test_whole_side_drain_mount_split_and_single_heal(self):
        player=actor("player","player","player",hp=100,max_hp=100)
        pet=actor("pet:0","player","pet",hp=100,max_hp=100,source_pet_slot=0)
        ride=actor("ride:1","player","pet",hp=100,max_hp=100,source_pet_slot=1)
        enemy=actor("enemy","enemy","enemy",hp=50,max_hp=100,quick=100)
        state=begin_persistent_battle(
            session(player,(enemy,),pets=(pet,),ride_pet=ride),
            slots={"player":0,"pet:0":5,"enemy":10},
        )
        result=self.resolve(state,submission(target_slot=0))
        self.assertEqual(result.after.hp_by_participant_id["player"],95)
        self.assertEqual(result.after.hp_by_participant_id["pet:0"],90)
        self.assertEqual(result.after.hp_by_participant_id["enemy"],70)
        self.assertEqual(result.after.ride_pet_runtime.hp,95)
        self.assertTrue(result.after.ride_pet_runtime.mounted)
        events=[event for event in result.round.events if event.batfly_skill_id==633]
        self.assertEqual([event.resolved_target_slot for event in events],[0,5])
        self.assertTrue(all(event.batfly_resolution.total_drain==20 for event in events))
        self.assertTrue(all(event.batfly_resolution.reported_heal==20 for event in events))
        self.assertTrue(all(event.batfly_execution_gate.rng_draws==0 for event in events))

    def test_dead_source_target_consumes_one_targetadjust_draw_then_hits_whole_side(self):
        player=actor("player","player","player",hp=100,max_hp=100)
        dead_pet=actor("pet:0","player","pet",hp=0,max_hp=100,source_pet_slot=0)
        enemy=actor("enemy","enemy","enemy",hp=50,max_hp=100,quick=100)
        state=begin_persistent_battle(
            session(player,(enemy,),pets=(dead_pet,)),
            slots={"player":0,"pet:0":5,"enemy":10},
        )
        result=self.resolve(
            state,
            submission(target_slot=5),
            retarget_roll=0,
        )
        events=[event for event in result.round.events if event.batfly_skill_id==633]
        self.assertEqual(len(events),1)
        self.assertEqual(events[0].resolved_target_slot,0)
        self.assertTrue(events[0].retargeted)
        self.assertEqual(events[0].batfly_execution_gate.adjusted_target_slot,0)
        self.assertEqual(events[0].batfly_execution_gate.rng_draws,1)
        self.assertEqual(result.after.hp_by_participant_id["player"],90)
        self.assertEqual(result.after.hp_by_participant_id["enemy"],60)

    def test_ride_pet_zero_sets_petfall_and_overflow_reports_zero_heal(self):
        player=actor("player","player","player",hp=1,max_hp=100)
        ride=actor("ride:1","player","pet",hp=1,max_hp=100,source_pet_slot=1)
        enemy=actor("enemy","enemy","enemy",hp=99,max_hp=100,quick=100)
        state=begin_persistent_battle(
            session(player,(enemy,),ride_pet=ride),
            slots={"player":0,"enemy":10},
        )
        result=self.resolve(state,submission(target_slot=0))
        event=next(event for event in result.round.events if event.batfly_skill_id==633)
        self.assertEqual(event.target_hp_after,0)
        self.assertTrue(event.batfly_target_resolution.ride_pet_fell)
        self.assertEqual(result.after.ride_pet_runtime.hp,0)
        self.assertFalse(result.after.ride_pet_runtime.mounted)
        self.assertTrue(result.after.ride_pet_runtime.petfall)
        self.assertEqual(result.after.hp_by_participant_id["enemy"],100)
        self.assertEqual(event.batfly_resolution.total_drain,2)
        self.assertEqual(event.batfly_resolution.applied_heal,1)
        self.assertEqual(event.batfly_resolution.reported_heal,0)
        self.assertEqual(result.after.phase,"finished")
        self.assertEqual(result.after.result,"defeat")


if __name__ == "__main__":
    unittest.main()
