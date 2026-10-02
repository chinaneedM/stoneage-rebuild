import unittest

from tools.stoneage_barrier_model import BarrierOption
from tools.stoneage_barrier_runtime_state import BarrierActionRolls
from tools.stoneage_battle_round_model import (
    BATTLE_COM_ATTACK,
    BATTLE_COM_WAIT,
    BattleCombatProfile,
    BattleCommand,
    prepare_battle_round,
    resolve_ordinary_round,
)
from tools.stoneage_enemy_ai_barrier_bridge import EnemyAiBarrierSubmission
from tools.stoneage_nocast_runtime_state import (
    NocastParticipantRuntime,
    NocastRoundOverlay,
)
from tools.stoneage_singleplayer_battle import BattleParticipant


def actor(pid,side,kind,*,quick,level=10,hp=300):
    return BattleParticipant(
        participant_id=pid,
        side=side,
        kind=kind,
        level=level,
        hp=hp,
        max_hp=hp,
        attack=100,
        defense=70,
        quick=quick,
        name=pid,
        fixed_vital=40,
    )


def profile(luck=0):
    return BattleCombatProfile(
        fixed_dex=100,
        fixed_luck=luck,
        earth=0,water=0,fire=0,wind=0,
    )


def overlay(*,player_counter=0):
    return NocastRoundOverlay({
        "player":NocastParticipantRuntime(
            25,25,25,25,
            counter=player_counter,
        ),
        "enemy":NocastParticipantRuntime(25,25,25,25),
    })


def submission(skill_id=594):
    options={
        579:BarrierOption(turn=1,success_offset=50),
        594:BarrierOption(turn=3,success_offset=50),
    }
    return EnemyAiBarrierSubmission(
        participant_id="enemy",
        skill_slot=0,
        skill_id=skill_id,
        callback="PETSKILL_Barrier",
        source_target_slot=0,
        option=options[skill_id],
    )


class BarrierRuntimeTests(unittest.TestCase):
    def _round(self,*,skill_id=594,player_counter=0,hit_rolls=None):
        player=actor("player","player","player",quick=10)
        enemy=actor("enemy","enemy","enemy",quick=200)
        prepared=prepare_battle_round(
            (player,enemy),
            {
                "player":BattleCommand(BATTLE_COM_ATTACK,command2=10),
                "enemy":BattleCommand(BATTLE_COM_ATTACK,command2=0),
            },
            {"player":0,"enemy":0},
        )
        return resolve_ordinary_round(
            prepared,
            slots={"player":0,"enemy":10},
            profiles={"player":profile(),"enemy":profile()},
            attack_rolls={},
            barrier_submissions_by_participant_id={
                "enemy":submission(skill_id)
            },
            barrier_rolls_by_participant_id={
                "enemy":BarrierActionRolls(
                    hit_rolls_by_slot=(
                        {} if hit_rolls is None else hit_rolls
                    )
                )
            },
            nocast_overlay=overlay(player_counter=player_counter),
            defense_profile="newpower_70pct",
        )

    def test_id594_applies_then_blocks_later_target_in_same_round(self):
        result=self._round(hit_rolls={0:1})
        applied=next(
            event for event in result.events
            if event.barrier_application is not None
        )
        self.assertEqual(applied.result,"barrier_applied")
        self.assertEqual(applied.barrier_application.counter_written,4)

        target_tick=next(
            event for event in result.events
            if event.participant_id=="player"
            and event.barrier_tick_resolution is not None
        )
        self.assertEqual(
            (
                target_tick.barrier_tick_resolution.counter_before,
                target_tick.barrier_tick_resolution.decremented_local_counter,
                target_tick.barrier_tick_resolution.counter_after,
            ),
            (4,3,4),
        )
        self.assertTrue(
            target_tick.barrier_tick_resolution.self_freeze_restored_storage
        )
        no_action=next(
            event for event in result.events
            if event.participant_id=="player"
            and event.result=="status_no_action"
        )
        self.assertEqual(no_action.command1,0)
        player_runtime=result.nocast_overlay.runtime_by_participant_id["player"]
        self.assertEqual(player_runtime.barrier_counter,4)
        self.assertEqual(result.hp_by_participant_id["enemy"],300)

    def test_id579_turn_one_still_self_freezes_after_application(self):
        result=self._round(skill_id=579,hit_rolls={0:1})
        applied=next(
            event for event in result.events
            if event.barrier_application is not None
        )
        self.assertEqual(applied.barrier_application.counter_written,2)
        player_runtime=result.nocast_overlay.runtime_by_participant_id["player"]
        # Fixed StatusSeq decrements local 2->1 then positive Barrier restores
        # storage to 2. Do not normalize this historical self-freeze away.
        self.assertEqual(player_runtime.barrier_counter,2)

    def test_existing_nocast_blocks_barrier_before_rng(self):
        result=self._round(player_counter=2,hit_rolls={})
        event=next(
            event for event in result.events
            if event.barrier_application is not None
        )
        self.assertEqual(event.result,"barrier_blocked_existing_status")
        self.assertFalse(event.barrier_application.rng_consumed)
        player_runtime=result.nocast_overlay.runtime_by_participant_id["player"]
        self.assertEqual(player_runtime.barrier_counter,0)
        # Player later visits Nocast slot 10 normally.
        self.assertEqual(player_runtime.counter,1)


if __name__=="__main__":
    unittest.main()
