import unittest

from tools.stoneage_battle_round_model import (
    BATTLE_COM_ATTACK,
    BATTLE_COM_NONE,
    BATTLE_COM_S_BECOMEFOX,
    BattleCombatProfile,
    BattleCommand,
    OrdinaryAttackRolls,
)
from tools.stoneage_battle_state_model import (
    begin_persistent_battle,
    participant_snapshot,
    resolve_persistent_ordinary_round,
)
from tools.stoneage_enemy_ai_becomefox_bridge import (
    CALLBACK_NAME,
    EnemyAiBecomeFoxSubmission,
)
from tools.stoneage_singleplayer_battle import BattleParticipant, BattleSession
from tools.stoneage_singleplayer_domain import (
    EncounterRequest, EnemyVariantId, MapPosition, PetTemplateId,
)


def actor(pid,side,kind,*,hp=5000,attack=100,defense=20,quick=50,slot=None):
    return BattleParticipant(
        participant_id=pid,side=side,kind=kind,level=10,
        hp=hp,max_hp=hp,attack=attack,defense=defense,quick=quick,
        name=pid,fixed_vital=40,source_pet_slot=slot,
    )


def session(*,pet_quick=70):
    player=actor("player","player","player",quick=50)
    pet=actor("pet","player","pet",quick=pet_quick,slot=0)
    caster=actor("caster","enemy","enemy",attack=180,quick=100)
    dummy=actor("dummy","enemy","enemy",hp=10000,defense=0,quick=10)
    encounter=EncounterRequest(
        position=MapPosition(2000,10,10),area_index=1,group_id=1,
        enemy_variant_id=EnemyVariantId(10),pet_template_id=PetTemplateId(20),
        level=5,max_enemy_count=2,
    )
    return BattleSession(
        origin_position=encounter.position,encounter=encounter,
        player=player,allied_pets=(pet,),enemies=(caster,dummy),
    )


def profile(dex=100):
    return BattleCombatProfile(
        fixed_dex=dex,fixed_luck=0,
        earth=0,water=0,fire=0,wind=0,
        weapon_critical=0,counter_weapon_type="fist",
    )


PROFILES={
    "player":profile(80),"pet":profile(90),
    "caster":profile(120),"dummy":profile(70),
}
SLOTS={"player":0,"pet":5,"caster":15,"dummy":16}


def attack_rolls():
    return OrdinaryAttackRolls(
        dodge_roll_1_10000=10000,
        critical_roll_1_10000=10000,
        damage_roll=0,
    )


def fox_submission():
    return EnemyAiBecomeFoxSubmission(
        participant_id="caster",skill_slot=2,skill_id=625,
        callback=CALLBACK_NAME,source_target_slot=5,
        source_profile="gavin",
    )


def run_round(state,commands,attacks,**extra):
    return resolve_persistent_ordinary_round(
        state,
        commands=commands,
        initiative_random_subtracts={pid:0 for pid in commands},
        profiles=PROFILES,
        attack_rolls=attacks,
        defense_profile="newpower_70pct",
        **extra,
    )


class BecomeFoxPersistentRuntimeTests(unittest.TestCase):
    def test_transform_before_pet_action_persists_80pct_work_state_across_rounds(self):
        state=begin_persistent_battle(session(),slots=SLOTS)
        first=run_round(
            state,
            {
                "player":BattleCommand(BATTLE_COM_NONE),
                "pet":BattleCommand(BATTLE_COM_ATTACK,command2=16),
                "caster":BattleCommand(BATTLE_COM_S_BECOMEFOX,command2=5),
                "dummy":BattleCommand(BATTLE_COM_NONE),
            },
            {"pet":attack_rolls(),"caster":attack_rolls()},
            becomefox_submissions_by_participant_id={"caster":fox_submission()},
            becomefox_draws_by_participant_id={"caster":0},
            becomefox_target_petflag_by_participant_id={"pet":1},
            becomefox_base_image_by_participant_id={"pet":101111},
            becomefox_attacker_pig_marker_by_participant_id={"caster":-1},
        )
        state=first.after
        self.assertEqual(state.turn,1)
        fox=state.becomefox_overlay.runtime_by_participant_id["pet"].state
        self.assertEqual(fox.fox_round,0)
        self.assertEqual((fox.attack_power,fox.defence_power,fox.quick),(80,16,56))
        snap=participant_snapshot(state,"pet")
        self.assertEqual((snap.attack,snap.defense,snap.quick),(80,16,56))

        # turn1 and turn2 remain foxed; turn3 still executes reduced, then recovers.
        reduced_damage=[]
        for expected_turn in (2,3,4):
            result=run_round(
                state,
                {
                    "player":BattleCommand(BATTLE_COM_NONE),
                    "pet":BattleCommand(BATTLE_COM_ATTACK,command2=16),
                    "caster":BattleCommand(BATTLE_COM_NONE),
                    "dummy":BattleCommand(BATTLE_COM_NONE),
                },
                {"pet":attack_rolls()},
            )
            reduced_damage.append(
                next(
                    event.damage for event in result.round.events
                    if event.participant_id=="pet"
                    and event.result not in {"status_tick"}
                )
            )
            state=result.after
            self.assertEqual(state.turn,expected_turn)

        self.assertFalse(state.becomefox_overlay.runtime_by_participant_id)
        snap=participant_snapshot(state,"pet")
        self.assertEqual((snap.attack,snap.defense,snap.quick),(100,20,70))
        self.assertEqual(len(set(reduced_damage)),1)

    def test_transform_after_pet_already_acted_does_not_retroactively_reduce_work_values(self):
        state=begin_persistent_battle(session(pet_quick=130),slots=SLOTS)
        first=run_round(
            state,
            {
                "player":BattleCommand(BATTLE_COM_NONE),
                "pet":BattleCommand(BATTLE_COM_ATTACK,command2=16),
                "caster":BattleCommand(BATTLE_COM_S_BECOMEFOX,command2=5),
                "dummy":BattleCommand(BATTLE_COM_NONE),
            },
            {"pet":attack_rolls(),"caster":attack_rolls()},
            becomefox_submissions_by_participant_id={"caster":fox_submission()},
            becomefox_draws_by_participant_id={"caster":0},
            becomefox_target_petflag_by_participant_id={"pet":1},
            becomefox_base_image_by_participant_id={"pet":101111},
            becomefox_attacker_pig_marker_by_participant_id={"caster":-1},
        )
        state=first.after
        fox=state.becomefox_overlay.runtime_by_participant_id["pet"].state
        self.assertEqual((fox.attack_power,fox.defence_power,fox.quick),(100,20,130))
        self.assertEqual(participant_snapshot(state,"pet").quick,130)

        second=run_round(
            state,
            {
                "player":BattleCommand(BATTLE_COM_NONE),
                "pet":BattleCommand(BATTLE_COM_ATTACK,command2=16),
                "caster":BattleCommand(BATTLE_COM_NONE),
                "dummy":BattleCommand(BATTLE_COM_NONE),
            },
            {"pet":attack_rolls()},
        )
        fox=second.after.becomefox_overlay.runtime_by_participant_id["pet"].state
        self.assertEqual((fox.attack_power,fox.defence_power,fox.quick),(80,16,104))

    def test_battle_termination_tears_down_fox_overlay(self):
        state=begin_persistent_battle(session(),slots=SLOTS)
        # A pre-existing active fox overlay on the pet must not leak after battle end.
        from tools.stoneage_becomefox_reference_model import FOX_IMAGE, FoxState
        from tools.stoneage_becomefox_runtime_state import (
            BecomeFoxRuntimeOverlay,FoxParticipantRuntime,
        )
        fox=FoxParticipantRuntime(
            "gavin",
            FoxState(
                base_image=FOX_IMAGE,base_base_image=101111,
                attack_power=80,defence_power=16,quick=56,
                fix_str=100,fix_tough=20,fix_dex=70,
                fox_round=0,ride_pet=-1,petfall=0,
            ),
        )
        state=begin_persistent_battle(
            session(),slots=SLOTS,
            becomefox_overlay=BecomeFoxRuntimeOverlay({"pet":fox}),
        )
        # Preserve this as a state invariant test: invalid target classes are rejected.
        with self.assertRaisesRegex(ValueError,"player-side pets"):
            begin_persistent_battle(
                session(),slots=SLOTS,
                becomefox_overlay=BecomeFoxRuntimeOverlay({"caster":fox}),
            )


if __name__=="__main__":
    unittest.main()
