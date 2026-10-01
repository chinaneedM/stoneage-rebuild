import unittest
from dataclasses import replace

from tools.stoneage_attack_magic_action_model import (
    AttackMagicTargetRolls,
    EnemyAttackMagicActionRolls,
)
from tools.stoneage_attack_magic_model import (
    BATTLE_COM_S_ATTACK_MAGIC,
    PROFILE_RECOVERED25,
    build_magic_direct_use_request,
    encode_attack_magic_command,
)
from tools.stoneage_attack_magic_state_model import (
    AttackMagicResistanceRuntime,
    AttackMagicRoundOverlay,
)
from tools.stoneage_battle_round_model import (
    BATTLE_COM_WAIT,
    BattleCombatProfile,
    BattleCommand,
    prepare_battle_round,
    resolve_ordinary_round,
)
from tools.stoneage_battle_state_model import (
    begin_persistent_battle,
    resolve_persistent_ordinary_round,
)
from tools.stoneage_battle_status_model import (
    BaseBattleStatusRuntime,
    BaseBattleStatusState,
)
from tools.stoneage_enemy_ai_attack_magic_bridge import (
    ATTACK_MAGIC_CALLBACK,
    EnemyAiAttackMagicSubmission,
)
from tools.stoneage_recovered25_attack_magic_runtime import (
    NONPLAYER_ITEM_ROLE,
    Recovered25AttackMagicEntry,
    Recovered25AttackMagicRuntime,
)
from tools.stoneage_singleplayer_battle import BattleParticipant, BattleSession
from tools.stoneage_singleplayer_domain import MapPosition


CENTER=(
    (0,0,0,0,0),
    (0,0,1,0,0),
    (0,0,0,0,0),
)
WHOLE=(
    (1,1,1,1,1),
    (1,1,1,1,1),
    (0,0,0,0,0),
)


def participant(pid,side,kind,level,quick,hp=1000):
    return BattleParticipant(
        participant_id=pid,
        side=side,
        kind=kind,
        level=level,
        hp=hp,
        max_hp=1000,
        attack=100,
        defense=100,
        quick=quick,
        name=pid,
        source_pet_slot=(1 if kind=="pet" else None),
    )


def profile(earth,water,luck=0):
    return BattleCombatProfile(
        fixed_dex=50,
        fixed_luck=luck,
        earth=earth,
        water=water,
        fire=0,
        wind=0,
    )


def runtime():
    entries={}
    for offset,magic_id in enumerate(range(301,326)):
        matrix=WHOLE if magic_id == 305 else CENTER
        entries[1001+offset]=Recovered25AttackMagicEntry(
            skill_id=1001+offset,
            magic_id=magic_id,
            item_config_id=19647+offset,
            item_magicusemp=5,
            magic_idx=2+offset,
            element=0,
            power=(3000 if magic_id == 301 else 100),
            magic_level=1,
            attacker_side1_matrix=matrix,
            attacker_side0_matrix=matrix,
        )
    return Recovered25AttackMagicRuntime(
        entries=entries,
        itemset_file="itemset.txt",
    )


def submission(magic_id=301,target=0):
    offset=magic_id-301
    command=encode_attack_magic_command(
        target,
        f"magic={magic_id} item={19647+offset}",
        profile=PROFILE_RECOVERED25,
    )
    return EnemyAiAttackMagicSubmission(
        participant_id="enemy",
        skill_slot=0,
        skill_id=1001+offset,
        callback=ATTACK_MAGIC_CALLBACK,
        command=command,
        direct_use_request=build_magic_direct_use_request(command),
        nonplayer_item_runtime_role=NONPLAYER_ITEM_ROLE,
    )


def overlay(include_pet=False):
    values={
        "player":AttackMagicResistanceRuntime(
            levels=(20,5,0,0),
            exps=(90,1,0,0),
        )
    }
    if include_pet:
        values["pet:1"]=AttackMagicResistanceRuntime(
            levels=(10,3,0,0),
            exps=(0,0,0,0),
        )
    return AttackMagicRoundOverlay(values)


def command_from_submission(value):
    return BattleCommand(
        value.command.command1,
        command2=value.command.command2,
        command3=value.command.command3,
    )


class AttackMagicRoundExecutionTests(unittest.TestCase):
    def test_command_2002_executes_in_action_order_and_skips_dead_later_actor(self):
        player=participant("player","player","player",50,50)
        enemy=participant("enemy","enemy","enemy",56,200)
        sub=submission()
        commands={
            "player":BattleCommand(BATTLE_COM_WAIT),
            "enemy":command_from_submission(sub),
        }
        prepared=prepare_battle_round(
            (player,enemy),
            commands,
            {"player":0,"enemy":0},
        )
        result=resolve_ordinary_round(
            prepared,
            slots={"player":0,"enemy":15},
            profiles={
                "player":profile(0,100),
                "enemy":profile(100,0),
            },
            attack_rolls={},
            defense_profile="preserved_old",
            base_status_runtime_by_participant_id={
                "player":BaseBattleStatusRuntime(
                    status=BaseBattleStatusState(sleep=3),
                    work_quick=50,
                ),
                "enemy":BaseBattleStatusRuntime(work_quick=200),
            },
            attack_magic_runtime=runtime(),
            attack_magic_submissions_by_participant_id={"enemy":sub},
            attack_magic_rolls_by_participant_id={
                "enemy":EnemyAttackMagicActionRolls(
                    0,{0:AttackMagicTargetRolls(100,0)}
                )
            },
            attack_magic_overlay=overlay(),
        )
        magic_events=[
            event for event in result.events
            if event.command1 == BATTLE_COM_S_ATTACK_MAGIC
        ]
        self.assertEqual(len(magic_events),1)
        self.assertEqual(magic_events[0].result,"attackmagic_hit")
        self.assertEqual(magic_events[0].resolved_target_slot,0)
        self.assertEqual(result.hp_by_participant_id["player"],0)
        self.assertEqual(
            result.base_status_runtime_by_participant_id[
                "player"
            ].status.sleep,
            0,
        )
        self.assertEqual(result.events[-1].result,"skipped_dead")
        trained=result.attack_magic_overlay.resistance_by_participant_id[
            "player"
        ]
        self.assertEqual(trained.levels[:2],(21,4))

    def test_persistent_round_reuses_existing_death_and_termination_seams(self):
        player=participant("player","player","player",50,50)
        enemy=participant("enemy","enemy","enemy",56,200)
        session=BattleSession(
            origin_position=MapPosition(0,0,0),
            encounter=object(),
            player=player,
            allied_pets=(),
            enemies=(enemy,),
        )
        state=begin_persistent_battle(
            session,
            slots={"player":0,"enemy":15},
        )
        statuses=dict(state.base_status_runtime_by_participant_id)
        statuses["player"]=BaseBattleStatusRuntime(
            status=BaseBattleStatusState(sleep=2),
            work_quick=50,
        )
        state=replace(
            state,
            base_status_runtime_by_participant_id=statuses,
        )
        sub=submission()
        result=resolve_persistent_ordinary_round(
            state,
            commands={
                "player":BattleCommand(BATTLE_COM_WAIT),
                "enemy":command_from_submission(sub),
            },
            initiative_random_subtracts={"player":0,"enemy":0},
            profiles={
                "player":profile(0,100),
                "enemy":profile(100,0),
            },
            attack_rolls={},
            defense_profile="preserved_old",
            attack_magic_runtime=runtime(),
            attack_magic_submissions_by_participant_id={"enemy":sub},
            attack_magic_rolls_by_participant_id={
                "enemy":EnemyAttackMagicActionRolls(
                    0,{0:AttackMagicTargetRolls(100,0)}
                )
            },
            attack_magic_overlay=overlay(),
        )
        self.assertEqual(result.after.turn,1)
        self.assertEqual(result.after.phase,"finished")
        self.assertEqual(result.after.result,"defeat")
        self.assertEqual(result.after.winning_side,1)
        self.assertEqual(result.after.hp_by_participant_id["player"],0)
        self.assertIsNotNone(result.attack_magic_overlay_after)
        self.assertEqual(
            result.attack_magic_overlay_after.resistance_by_participant_id[
                "player"
            ].levels[:2],
            (21,4),
        )
        self.assertLess(result.after.pending_player_charm_delta,0)

    def test_nonportable_multitarget_magic_fails_closed_inside_round(self):
        player=participant("player","player","player",50,50)
        pet=participant("pet:1","player","pet",40,40)
        enemy=participant("enemy","enemy","enemy",56,200)
        sub=submission(305,0)
        prepared=prepare_battle_round(
            (player,pet,enemy),
            {
                "player":BattleCommand(BATTLE_COM_WAIT),
                "pet:1":BattleCommand(BATTLE_COM_WAIT),
                "enemy":command_from_submission(sub),
            },
            {"player":0,"pet:1":0,"enemy":0},
        )
        with self.assertRaisesRegex(ValueError,"SortLoc/qsort"):
            resolve_ordinary_round(
                prepared,
                slots={"player":0,"pet:1":1,"enemy":15},
                profiles={
                    "player":profile(0,100),
                    "pet:1":profile(0,100),
                    "enemy":profile(100,0),
                },
                attack_rolls={},
                defense_profile="preserved_old",
                attack_magic_runtime=runtime(),
                attack_magic_submissions_by_participant_id={"enemy":sub},
                attack_magic_rolls_by_participant_id={
                    "enemy":EnemyAttackMagicActionRolls(
                        0,{
                            0:AttackMagicTargetRolls(100,0),
                            1:AttackMagicTargetRolls(100,0),
                        }
                    )
                },
                attack_magic_overlay=overlay(include_pet=True),
            )

    def test_dead_single_target_early_return_needs_no_magic_rng(self):
        player=participant(
            "player","player","player",50,50,hp=0
        )
        enemy=participant("enemy","enemy","enemy",56,200)
        sub=submission()
        prepared=prepare_battle_round(
            (player,enemy),
            {
                "player":BattleCommand(BATTLE_COM_WAIT),
                "enemy":command_from_submission(sub),
            },
            {"player":0,"enemy":0},
        )
        result=resolve_ordinary_round(
            prepared,
            slots={"player":0,"enemy":15},
            profiles={
                "player":profile(0,100),
                "enemy":profile(100,0),
            },
            attack_rolls={},
            defense_profile="preserved_old",
            attack_magic_runtime=runtime(),
            attack_magic_submissions_by_participant_id={"enemy":sub},
            attack_magic_overlay=overlay(),
        )
        magic=[e for e in result.events if e.command1==BATTLE_COM_S_ATTACK_MAGIC]
        self.assertEqual(len(magic),1)
        self.assertEqual(magic[0].result,"attackmagic_no_target")

    def test_status_blocked_magic_rejects_supplied_unused_magic_rng(self):
        player=participant("player","player","player",50,50)
        enemy=participant("enemy","enemy","enemy",56,200)
        sub=submission()
        prepared=prepare_battle_round(
            (player,enemy),
            {
                "player":BattleCommand(BATTLE_COM_WAIT),
                "enemy":command_from_submission(sub),
            },
            {"player":0,"enemy":0},
        )
        with self.assertRaisesRegex(ValueError,"unused AttackMagic action RNG"):
            resolve_ordinary_round(
                prepared,
                slots={"player":0,"enemy":15},
                profiles={
                    "player":profile(0,100),
                    "enemy":profile(100,0),
                },
                attack_rolls={},
                defense_profile="preserved_old",
                base_status_runtime_by_participant_id={
                    "player":BaseBattleStatusRuntime(work_quick=50),
                    "enemy":BaseBattleStatusRuntime(
                        status=BaseBattleStatusState(sleep=2),
                        work_quick=200,
                    ),
                },
                attack_magic_runtime=runtime(),
                attack_magic_submissions_by_participant_id={"enemy":sub},
                attack_magic_rolls_by_participant_id={
                    "enemy":EnemyAttackMagicActionRolls(
                        0,{0:AttackMagicTargetRolls(100,0)}
                    )
                },
                attack_magic_overlay=overlay(),
            )


if __name__=="__main__":
    unittest.main()
