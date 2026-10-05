import unittest

from tools.stoneage_battle_round_model import (
    BATTLE_COM_ATTACK, BATTLE_COM_WAIT,
    BattleCombatProfile, BattleCommand,
    prepare_battle_round, resolve_ordinary_round,
)
from tools.stoneage_battle_status_model import (
    BaseBattleStatusRuntime, BaseStatusCombatProfile,
)
from tools.stoneage_combined_direct_magic_model import RuntimeItemZeroWitness
from tools.stoneage_combined_initiative_model import PROFILE_GAVIN_IRIS_30PCT
from tools.stoneage_combined_model import resolve_combined_selection
from tools.stoneage_combined_runtime_state import (
    CombinedActionRolls, CombinedRuntimeOverlay,
    STATUS_MAGIC_PROFILE_IRIS_CP950,
)
from tools.stoneage_enemy_ai_combined_bridge import (
    CombinedMagicCrosslink, EnemyAiCombinedSubmission,
)
from tools.stoneage_nocast_runtime_state import (
    NocastParticipantRuntime, NocastRoundOverlay,
)
from tools.stoneage_singleplayer_battle import BattleParticipant


def actor(pid,side,kind,*,level=10,hp=500,max_hp=1000,quick=50):
    return BattleParticipant(
        participant_id=pid,side=side,kind=kind,level=level,
        hp=hp,max_hp=max_hp,attack=100,defense=50,quick=quick,name=pid,
        fixed_vital=100,
    )


def profile(*,dex=100,earth=10,water=20,fire=30,wind=40,luck=100):
    return BattleCombatProfile(dex,luck,earth,water,fire,wind)


def late(*,counter=0,nc_flag=0):
    return NocastParticipantRuntime(
        vital=100,strength=100,toughness=100,dexterity=100,
        counter=counter,nc_flag=nc_flag,
    )


def submission(*,skill_id,magic_id,function,target=0):
    selection=resolve_combined_selection(
        target_slot=target,declared_count=1,magic_ids=(magic_id,),draw_index=0,
    )
    magic=CombinedMagicCrosslink(
        magic_id=magic_id,function_name=function,field=1,target=1,
        target_deadflg=0,idx=None,direct_item_index=0,
    )
    return EnemyAiCombinedSubmission(
        "enemy",0,skill_id,"PETSKILL_Combined",target,selection,magic,
    )


class CombinedOrderedRuntimeTests(unittest.TestCase):
    def resolve(
        self,*,sub,rolls,player=None,enemy=None,
        player_command=None,player_late=None,enemy_late=None,
        player_base=None,status_profile=None,item_mp=5,enemy_mp=20,
    ):
        player=player or actor("player","player","player",level=1,quick=10)
        enemy=enemy or actor("enemy","enemy","enemy",level=100,quick=200)
        participants=(player,enemy)
        commands={
            "player":player_command or BattleCommand(BATTLE_COM_WAIT),
            "enemy":BattleCommand(BATTLE_COM_ATTACK,command2=sub.source_target_slot),
        }
        prepared=prepare_battle_round(
            participants,commands,{"player":0,"enemy":0},
            tie_break_order=("enemy","player"),
        )
        nocast=NocastRoundOverlay({
            "player":player_late or late(),
            "enemy":enemy_late or late(),
        })
        combined=CombinedRuntimeOverlay(
            PROFILE_GAVIN_IRIS_30PCT,STATUS_MAGIC_PROFILE_IRIS_CP950,
            RuntimeItemZeroWitness(True,item_mp),
            {"enemy":enemy_mp},{"player":False,"enemy":False},
        )
        return resolve_ordinary_round(
            prepared,slots={"player":0,"enemy":10},
            profiles={"player":profile(),"enemy":profile()},
            attack_rolls={},defense_profile="newpower_70pct",
            base_status_runtime_by_participant_id={
                "player":player_base or BaseBattleStatusRuntime(),
                "enemy":BaseBattleStatusRuntime(),
            },
            base_status_combat_profiles_by_participant_id=(
                {} if status_profile is None else {"player":status_profile}
            ),
            combined_submissions_by_participant_id={"enemy":sub},
            combined_rolls_by_participant_id={"enemy":rolls},
            combined_overlay=combined,nocast_overlay=nocast,
        )

    def combined_event(self,result):
        return next(e for e in result.events if e.combined_magic_id is not None)

    def test_recovery21_updates_hp_mp_and_owns_one_effect_draw(self):
        result=self.resolve(
            sub=submission(skill_id=627,magic_id=21,function="MAGIC_Recovery"),
            rolls=CombinedActionRolls(recovery_roll_90_110=100),
            player=actor("player","player","player",level=1,hp=500,max_hp=1000,quick=10),
        )
        event=self.combined_event(result)
        self.assertEqual(event.result,"combined_recovery")
        self.assertEqual(event.target_hp_before,500)
        self.assertGreater(event.target_hp_after,500)
        self.assertEqual(result.combined_overlay.mp_by_participant_id["enemy"],15)
        self.assertEqual(event.combined_recovery_effect.effect_rng_draws_consumed,1)

    def test_nocast_rejects_before_item_mp_target_and_effect_rng(self):
        result=self.resolve(
            sub=submission(skill_id=627,magic_id=21,function="MAGIC_Recovery"),
            rolls=CombinedActionRolls(),enemy_late=late(counter=2,nc_flag=1),
        )
        event=self.combined_event(result)
        self.assertEqual(event.result,"combined_direct_rejected_nocast")
        self.assertEqual(event.combined_direct_route.item_reads,0)
        self.assertEqual(result.combined_overlay.mp_by_participant_id["enemy"],20)
        with self.assertRaisesRegex(ValueError,"cannot consume action RNG"):
            self.resolve(
                sub=submission(skill_id=627,magic_id=21,function="MAGIC_Recovery"),
                rolls=CombinedActionRolls(recovery_roll_90_110=100),
                enemy_late=late(counter=2,nc_flag=1),
            )

    def test_statuschange_sleep_cancels_later_command_and_ticks_same_round(self):
        player=actor("player","player","player",level=1,quick=10)
        result=self.resolve(
            sub=submission(skill_id=627,magic_id=189,function="MAGIC_StatusChange"),
            rolls=CombinedActionRolls(status_roll_1_100=1),
            player=player,
            player_command=BattleCommand(BATTLE_COM_ATTACK,command2=10),
            status_profile=BaseStatusCombatProfile(
                vital=1,strength=1,tough=1,dex=1,
            ),
        )
        event=self.combined_event(result)
        self.assertEqual(event.combined_status_change_effect.status_after.sleep,5)
        self.assertTrue(event.combined_status_change_effect.command_cleared)
        self.assertEqual(result.base_status_runtime_by_participant_id["player"].status.sleep,4)
        self.assertTrue(any(
            e.participant_id=="player" and e.result=="status_no_action"
            for e in result.events
        ))

    def test_statusrecovery61_clears_persistent_nocast_without_effect_rng(self):
        result=self.resolve(
            sub=submission(skill_id=637,magic_id=61,function="MAGIC_StatusRecovery"),
            rolls=CombinedActionRolls(),
            player_late=late(counter=3,nc_flag=1),
        )
        event=self.combined_event(result)
        self.assertEqual(event.combined_status_recovery_effect.cleared_status,10)
        self.assertEqual(result.nocast_overlay.runtime_by_participant_id["player"].counter,0)
        self.assertEqual(result.nocast_overlay.runtime_by_participant_id["player"].nc_flag,0)

    def test_attreverse240_toggles_overlay_and_reports_same_round_attributes(self):
        result=self.resolve(
            sub=submission(skill_id=632,magic_id=240,function="MAGIC_AttReverse"),
            rolls=CombinedActionRolls(),
        )
        event=self.combined_event(result)
        self.assertTrue(result.combined_overlay.att_reverse_by_participant_id["player"])
        effect=event.combined_att_reverse_effect
        self.assertEqual((effect.earth,effect.water,effect.fire,effect.wind),(30,40,10,20))

    def test_prepare_round_accepts_explicit_combined_action_value_override(self):
        player=actor("player","player","player",quick=200)
        enemy=actor("enemy","enemy","enemy",quick=10)
        prepared=prepare_battle_round(
            (player,enemy),
            {"player":BattleCommand(BATTLE_COM_WAIT),"enemy":BattleCommand(BATTLE_COM_ATTACK,command2=0)},
            {"player":0,"enemy":0},
            action_value_overrides_by_participant_id={"enemy":500},
        )
        self.assertEqual(prepared.ordered_entries[0].participant.participant_id,"enemy")
        self.assertEqual(prepared.ordered_entries[0].action_value,500)


if __name__=="__main__":
    unittest.main()
