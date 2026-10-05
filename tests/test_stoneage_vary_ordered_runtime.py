import unittest
from dataclasses import replace

from tools.stoneage_battle_round_model import (
    BATTLE_COM_ATTACK,
    BATTLE_COM_WAIT,
    BattleCombatProfile,
    BattleCommand,
    prepare_battle_round,
    resolve_ordinary_round,
)
from tools.stoneage_enemy_ai_vary_bridge import EnemyAiVarySubmission
from tools.stoneage_singleplayer_battle import BattleParticipant
from tools.stoneage_vary_runtime_state import (
    CALLBACK_NAME,
    PROFILE_BISMARCK_ATTACK_DEFENSE_QUICK,
    PROFILE_GAVIN_IRIS_ATTACK_QUICK,
    cast_vary,
    create_vary_participant_runtime,
)


def actor(pid, side, kind, *, quick, attack=100, defense=80):
    return BattleParticipant(
        participant_id=pid,
        side=side,
        kind=kind,
        level=10,
        hp=500,
        max_hp=500,
        attack=attack,
        defense=defense,
        quick=quick,
        name=pid,
        fixed_vital=100,
    )


def profile(dex):
    return BattleCombatProfile(
        fixed_dex=dex,
        fixed_luck=0,
        earth=0,
        water=0,
        fire=0,
        wind=0,
    )


def submission(profile_name):
    state=create_vary_participant_runtime(
        profile=profile_name,
        tempno=981,
        base_image=101427,
        fixed_attack=100,
        fixed_defense=80,
        fixed_quick=80,
    )
    state=cast_vary(state)
    return EnemyAiVarySubmission(
        participant_id="enemy",
        skill_slot=2,
        skill_id=600,
        callback=CALLBACK_NAME,
        source_target_carrier=0,
        runtime_after_callback=state,
    )


class VaryOrderedRuntimeTests(unittest.TestCase):
    def resolve(self, profile_name):
        player=actor("player","player","player",quick=100)
        enemy_base=actor("enemy","enemy","enemy",quick=80)
        sub=submission(profile_name)

        # PETSKILL_Vary mutates WORKQUICK before BATTLE_DexCalc.  The common
        # sorter must therefore see callback-updated quick on the cast round.
        enemy=replace(
            enemy_base,
            quick=sub.runtime_after_callback.quick,
            attack=sub.runtime_after_callback.attack_power,
            defense=sub.runtime_after_callback.defense_power,
        )
        prepared=prepare_battle_round(
            (player,enemy),
            {
                "player":BattleCommand(BATTLE_COM_WAIT),
                "enemy":BattleCommand(
                    BATTLE_COM_ATTACK,
                    command2=sub.source_target_carrier,
                ),
            },
            {"player":0,"enemy":0},
        )
        result=resolve_ordinary_round(
            prepared,
            slots={"player":0,"enemy":10},
            profiles={"player":profile(100),"enemy":profile(80)},
            attack_rolls={},
            defense_profile="newpower_70pct",
            vary_submissions_by_participant_id={"enemy":sub},
        )
        return result

    def test_cast_quick_changes_same_round_order_without_special_dexcalc(self):
        result=self.resolve(PROFILE_GAVIN_IRIS_ATTACK_QUICK)
        self.assertEqual(result.action_order,("enemy","player"))
        event=next(e for e in result.events if e.vary_skill_id is not None)
        self.assertEqual(event.result,"vary_applied")
        self.assertEqual(event.command1,BATTLE_COM_ATTACK)
        self.assertTrue(event.vary_visual_effect_enabled)
        self.assertEqual(result.hp_by_participant_id["player"],500)

    def test_bismarck_profile_is_same_semantic_no_damage_without_visual(self):
        result=self.resolve(PROFILE_BISMARCK_ATTACK_DEFENSE_QUICK)
        event=next(e for e in result.events if e.vary_skill_id is not None)
        self.assertEqual(event.vary_skill_id,600)
        self.assertFalse(event.vary_visual_effect_enabled)
        self.assertEqual(result.hp_by_participant_id["player"],500)

    def test_vary_carrier_cannot_fall_through_to_physical_attack(self):
        result=self.resolve(PROFILE_GAVIN_IRIS_ATTACK_QUICK)
        enemy_events=[e for e in result.events if e.participant_id=="enemy"]
        self.assertEqual(len(enemy_events),1)
        self.assertEqual(enemy_events[0].result,"vary_applied")
        self.assertEqual(enemy_events[0].damage,0)


if __name__=="__main__":
    unittest.main()
