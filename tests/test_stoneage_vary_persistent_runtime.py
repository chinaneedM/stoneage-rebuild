import unittest

from tools.stoneage_battle_round_model import (
    BATTLE_COM_ATTACK,
    BATTLE_COM_WAIT,
    BattleCombatProfile,
    BattleCommand,
)
from tools.stoneage_battle_state_model import (
    begin_persistent_battle,
    participant_snapshot,
    resolve_persistent_ordinary_round,
)
from tools.stoneage_enemy_ai_vary_bridge import EnemyAiVarySubmission
from tools.stoneage_singleplayer_battle import BattleParticipant, BattleSession
from tools.stoneage_singleplayer_domain import (
    EncounterRequest,
    EnemyVariantId,
    MapPosition,
    PetTemplateId,
)
from tools.stoneage_vary_runtime_state import (
    CALLBACK_NAME,
    PROFILE_BISMARCK_ATTACK_DEFENSE_QUICK,
    PROFILE_GAVIN_IRIS_ATTACK_QUICK,
    cast_vary,
    create_vary_participant_runtime,
)


def actor(pid,side,kind,*,quick,attack=100,defense=80):
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


def session():
    player=actor("player","player","player",quick=100)
    enemy=actor("enemy","enemy","enemy",quick=80)
    encounter=EncounterRequest(
        position=MapPosition(2000,10,10),
        area_index=1,
        group_id=1,
        enemy_variant_id=EnemyVariantId(10),
        pet_template_id=PetTemplateId(981),
        level=10,
        max_enemy_count=1,
    )
    return BattleSession(
        origin_position=encounter.position,
        encounter=encounter,
        player=player,
        allied_pets=(),
        enemies=(enemy,),
    )


def submission(profile_name=PROFILE_GAVIN_IRIS_ATTACK_QUICK):
    runtime=create_vary_participant_runtime(
        profile=profile_name,
        tempno=981,
        base_image=101427,
        fixed_attack=100,
        fixed_defense=80,
        fixed_quick=80,
    )
    return EnemyAiVarySubmission(
        participant_id="enemy",
        skill_slot=2,
        skill_id=600,
        callback=CALLBACK_NAME,
        source_target_carrier=0,
        runtime_after_callback=cast_vary(runtime),
    )


class VaryPersistentRuntimeTests(unittest.TestCase):
    def begin(self):
        return begin_persistent_battle(
            session(),
            slots={"player":0,"enemy":10},
        )

    def run_round(self,state,*,sub=None):
        enemy_command=(
            BattleCommand(BATTLE_COM_ATTACK,command2=0)
            if sub is not None
            else BattleCommand(BATTLE_COM_WAIT)
        )
        return resolve_persistent_ordinary_round(
            state,
            commands={
                "player":BattleCommand(BATTLE_COM_WAIT),
                "enemy":enemy_command,
            },
            initiative_random_subtracts={"player":0,"enemy":0},
            profiles={"player":profile(100),"enemy":profile(80)},
            attack_rolls={},
            defense_profile="newpower_70pct",
            vary_submissions_by_participant_id=(
                {} if sub is None else {"enemy":sub}
            ),
        )

    def test_cast_persists_six_actor_actions_then_restores_baseline(self):
        first=self.run_round(self.begin(),sub=submission())
        self.assertEqual(first.round.action_order,("enemy","player"))
        self.assertIsNotNone(first.after.vary_overlay)
        vary=first.after.vary_overlay.runtime_by_participant_id["enemy"]
        self.assertEqual(vary.work_turn,1)
        transformed=participant_snapshot(first.after,"enemy")
        self.assertEqual(
            (transformed.attack,transformed.defense,transformed.quick),
            (130,80,104),
        )

        state=first.after
        for expected in (2,3,4,5):
            result=self.run_round(state)
            state=result.after
            vary=state.vary_overlay.runtime_by_participant_id["enemy"]
            self.assertEqual(vary.work_turn,expected)
            self.assertEqual(result.round.action_order,("enemy","player"))

        sixth=self.run_round(state)
        state=sixth.after
        self.assertIsNotNone(state.vary_overlay)
        self.assertEqual(state.vary_overlay.runtime_by_participant_id,{})
        restored=participant_snapshot(state,"enemy")
        self.assertEqual(
            (restored.attack,restored.defense,restored.quick),
            (100,80,80),
        )
        self.assertEqual(sixth.round.action_order,("enemy","player"))

        seventh=self.run_round(state)
        self.assertEqual(seventh.round.action_order,("player","enemy"))

    def test_recast_is_rejected_while_persistent_wolf_is_active(self):
        first=self.run_round(self.begin(),sub=submission())
        with self.assertRaisesRegex(ValueError,"recast"):
            self.run_round(first.after,sub=submission())

    def test_bismarck_defense_profile_persists_until_expiry(self):
        first=self.run_round(
            self.begin(),
            sub=submission(PROFILE_BISMARCK_ATTACK_DEFENSE_QUICK),
        )
        transformed=participant_snapshot(first.after,"enemy")
        self.assertEqual(
            (transformed.attack,transformed.defense,transformed.quick),
            (130,40,104),
        )


if __name__=="__main__":
    unittest.main()
