import unittest

from tools.stoneage_battle_damage_react_model import (
    DAMAGE_REACT_REFLEC,
    DAMAGE_REACT_VANISH,
    BaseDamageReactState,
)
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
from tools.stoneage_battle_state_model import (
    ACTIVE,
    begin_persistent_battle,
    resolve_persistent_ordinary_round,
)
from tools.stoneage_enemy_ai_lighttakeed_bridge import (
    EnemyAiLighttakeedSubmission,
)
from tools.stoneage_lighttakeed_model import (
    PROFILE_BISMARCK_COPY_PLUS_ONE,
    PROFILE_GAVIN_IRIS_COPY,
)
from tools.stoneage_singleplayer_battle import BattleParticipant, BattleSession
from tools.stoneage_singleplayer_domain import (
    EncounterRequest,
    EnemyVariantId,
    MapPosition,
    PetTemplateId,
)


def actor(pid,side,kind,*,hp=500,attack=100,defense=0,quick=50):
    return BattleParticipant(
        participant_id=pid,
        side=side,
        kind=kind,
        level=20,
        hp=hp,
        max_hp=max(1,hp),
        attack=attack,
        defense=defense,
        quick=quick,
        name=pid,
        fixed_vital=40,
    )


def profile():
    return BattleCombatProfile(
        fixed_dex=100,
        fixed_luck=0,
        earth=0,
        water=0,
        fire=0,
        wind=0,
    )


def attack_rolls(*,dodge=10000):
    return OrdinaryAttackRolls(
        dodge_roll_1_10000=dodge,
        critical_roll_1_10000=10000,
        damage_roll=0,
        minimum_damage_roll_0_1=1,
    )


def submission(
    *,
    skill_id=611,
    marker=DAMAGE_REACT_VANISH,
    source_target=0,
    profile_name=PROFILE_GAVIN_IRIS_COPY,
    enemy=None,
):
    enemy=enemy or actor("enemy","enemy","enemy")
    return EnemyAiLighttakeedSubmission(
        participant_id="enemy",
        skill_slot=4 if skill_id==611 else 3,
        skill_id=skill_id,
        callback="PETSKILL_Lighttakeed",
        source_target_slot=source_target,
        marker_kind=marker,
        profile=profile_name,
        attack_power=int(enemy.attack*0.7),
        defense_power=int(enemy.defense*0.5),
    )


def setup_effects(sub):
    return {
        "enemy":BattleCommandSetupEffects(
            attack_power=int(sub.attack_power),
            defense_power=int(sub.defense_power),
        )
    }


def session(player,enemy):
    encounter=EncounterRequest(
        position=MapPosition(2000,10,10),
        area_index=1,
        group_id=1,
        enemy_variant_id=EnemyVariantId(10),
        pet_template_id=PetTemplateId(20),
        level=5,
        max_enemy_count=1,
    )
    return BattleSession(
        origin_position=encounter.position,
        encounter=encounter,
        player=player,
        allied_pets=(),
        enemies=(enemy,),
    )


class LighttakeedOrderedRuntimeTests(unittest.TestCase):
    def resolve(
        self,
        *,
        sub=None,
        player=None,
        enemy=None,
        react=None,
        dodge=10000,
        counter_rolls=None,
        setup=None,
    ):
        player=player or actor("player","player","player",quick=10)
        enemy=enemy or actor("enemy","enemy","enemy",quick=100)
        sub=sub or submission(enemy=enemy)
        prepared=prepare_battle_round(
            (player,enemy),
            {
                "player":BattleCommand(BATTLE_COM_WAIT),
                "enemy":BattleCommand(BATTLE_COM_ATTACK,command2=0),
            },
            {"player":0,"enemy":0},
            tie_break_order=("enemy","player"),
        )
        return resolve_ordinary_round(
            prepared,
            slots={"player":0,"enemy":10},
            profiles={"player":profile(),"enemy":profile()},
            attack_rolls={"enemy":attack_rolls(dodge=dodge)},
            defense_profile="newpower_70pct",
            command_setup_effects_by_participant_id=(
                setup if setup is not None else setup_effects(sub)
            ),
            base_damage_react_state_by_participant_id=react,
            lighttakeed_submissions_by_participant_id={"enemy":sub},
            counter_rolls_by_attack_id=counter_rolls,
        )

    @staticmethod
    def light_event(result):
        return next(
            event for event in result.events
            if event.lighttakeed_skill_id in {610,611}
        )

    def test_vanish_positive_hit_consumes_then_transfers_remaining_charge(self):
        result=self.resolve(
            react={
                "player":BaseDamageReactState(vanish=2),
                "enemy":BaseDamageReactState(),
            },
        )
        event=self.light_event(result)
        self.assertEqual(event.lighttakeed_skill_id,611)
        self.assertEqual(
            event.lighttakeed_profile,PROFILE_GAVIN_IRIS_COPY
        )
        self.assertTrue(event.lighttakeed_resolution.matched_reaction)
        self.assertEqual(event.lighttakeed_resolution.transferred_count,1)
        self.assertEqual(
            result.base_damage_react_state_by_participant_id["player"].vanish,
            1,
        )
        self.assertEqual(
            result.base_damage_react_state_by_participant_id["enemy"].vanish,
            1,
        )
        self.assertEqual(result.hp_by_participant_id["player"],500)

    def test_reflect_gavin_self_copy_and_bismarck_plus_one(self):
        player=actor("player","player","player",hp=500,quick=10)
        enemy=actor("enemy","enemy","enemy",hp=500,quick=100)
        common_react={
            "player":BaseDamageReactState(reflect=2),
            "enemy":BaseDamageReactState(reflect=7),
        }
        gavin=self.resolve(
            player=player,
            enemy=enemy,
            sub=submission(
                skill_id=610,
                marker=DAMAGE_REACT_REFLEC,
                profile_name=PROFILE_GAVIN_IRIS_COPY,
                enemy=enemy,
            ),
            react=common_react,
        )
        ge=self.light_event(gavin)
        self.assertTrue(ge.lighttakeed_resolution.matched_reaction)
        self.assertEqual(
            gavin.base_damage_react_state_by_participant_id["player"].reflect,
            1,
        )
        self.assertEqual(
            gavin.base_damage_react_state_by_participant_id["enemy"].reflect,
            7,
        )
        self.assertLess(gavin.hp_by_participant_id["enemy"],500)
        self.assertEqual(gavin.hp_by_participant_id["player"],500)

        bismarck=self.resolve(
            player=player,
            enemy=enemy,
            sub=submission(
                skill_id=610,
                marker=DAMAGE_REACT_REFLEC,
                profile_name=PROFILE_BISMARCK_COPY_PLUS_ONE,
                enemy=enemy,
            ),
            react=common_react,
        )
        be=self.light_event(bismarck)
        self.assertEqual(
            be.lighttakeed_profile,PROFILE_BISMARCK_COPY_PLUS_ONE
        )
        self.assertEqual(
            bismarck.base_damage_react_state_by_participant_id["player"].reflect,
            1,
        )
        self.assertEqual(
            bismarck.base_damage_react_state_by_participant_id["enemy"].reflect,
            8,
        )

    def test_active_marker_mismatch_demotes_to_ordinary_reaction(self):
        sub=submission(
            skill_id=610,
            marker=DAMAGE_REACT_REFLEC,
        )
        result=self.resolve(
            sub=sub,
            react={
                "player":BaseDamageReactState(vanish=2),
                "enemy":BaseDamageReactState(reflect=4),
            },
        )
        event=self.light_event(result)
        self.assertTrue(event.lighttakeed_resolution.demoted_to_ordinary)
        self.assertFalse(event.lighttakeed_resolution.matched_reaction)
        self.assertIsNone(event.lighttakeed_resolution.transferred_count)
        self.assertEqual(
            result.base_damage_react_state_by_participant_id["player"].vanish,
            1,
        )
        self.assertEqual(
            result.base_damage_react_state_by_participant_id["enemy"].reflect,
            4,
        )

    def test_dodge_is_zero_damage_and_does_not_transfer_or_consume(self):
        result=self.resolve(
            react={
                "player":BaseDamageReactState(vanish=2),
                "enemy":BaseDamageReactState(),
            },
            dodge=1,
        )
        event=self.light_event(result)
        self.assertEqual(event.result,"dodge")
        self.assertFalse(event.lighttakeed_resolution.lighttake_case_executed)
        self.assertIsNone(event.lighttakeed_resolution.transferred_count)
        self.assertEqual(
            result.base_damage_react_state_by_participant_id["player"].vanish,
            2,
        )
        self.assertEqual(
            result.base_damage_react_state_by_participant_id["enemy"].vanish,
            0,
        )

    def test_callback_power_setup_drift_is_rejected(self):
        sub=submission()
        with self.assertRaisesRegex(ValueError,"work-power"):
            self.resolve(
                sub=sub,
                setup={
                    "enemy":BattleCommandSetupEffects(
                        attack_power=int(sub.attack_power)+1,
                        defense_power=int(sub.defense_power),
                    )
                },
            )

    def test_attack_carrier_does_not_gain_native_counter_eligibility(self):
        # Player acts first and physically attacks the Lighttakeed caster.
        # The caster's ATTACK-shaped scheduling carrier must not make it an
        # ordinary BATTLE_Counter actor.
        player=actor(
            "player","player","player",
            hp=500,attack=50,defense=0,quick=200,
        )
        enemy=actor(
            "enemy","enemy","enemy",
            hp=500,attack=100,defense=0,quick=100,
        )
        sub=submission(enemy=enemy)
        prepared=prepare_battle_round(
            (player,enemy),
            {
                "player":BattleCommand(BATTLE_COM_ATTACK,command2=10),
                "enemy":BattleCommand(BATTLE_COM_ATTACK,command2=0),
            },
            {"player":0,"enemy":0},
            tie_break_order=("player","enemy"),
        )
        result=resolve_ordinary_round(
            prepared,
            slots={"player":0,"enemy":10},
            profiles={"player":profile(),"enemy":profile()},
            attack_rolls={
                "player":attack_rolls(),
                "enemy":attack_rolls(),
            },
            defense_profile="newpower_70pct",
            command_setup_effects_by_participant_id=setup_effects(sub),
            lighttakeed_submissions_by_participant_id={"enemy":sub},
            counter_rolls_by_attack_id={"player":(),"enemy":()},
            counter_abio_by_participant_id={"player":True},
        )
        counter=next(
            event for event in result.events
            if event.is_counter and event.participant_id=="enemy"
        )
        self.assertEqual(counter.participant_id,"enemy")
        self.assertEqual(counter.result,"counter_ineligible_command")
        self.assertTrue(any(
            event.participant_id=="enemy"
            and event.lighttakeed_skill_id==611
            for event in result.events
        ))

    def test_persistent_round_carries_transferred_counter_forward(self):
        player=actor("player","player","player",hp=500,quick=10)
        enemy=actor("enemy","enemy","enemy",hp=500,quick=100)
        state=begin_persistent_battle(
            session(player,enemy),
            slots={"player":0,"enemy":10},
            base_damage_react_state_by_participant_id={
                "player":BaseDamageReactState(vanish=2),
                "enemy":BaseDamageReactState(),
            },
        )
        sub=submission(enemy=enemy)
        result=resolve_persistent_ordinary_round(
            state,
            commands={
                "player":BattleCommand(BATTLE_COM_WAIT),
                "enemy":BattleCommand(BATTLE_COM_ATTACK,command2=0),
            },
            initiative_random_subtracts={"player":0,"enemy":0},
            profiles={"player":profile(),"enemy":profile()},
            attack_rolls={"enemy":attack_rolls()},
            defense_profile="newpower_70pct",
            lighttakeed_submissions_by_participant_id={"enemy":sub},
        )
        self.assertEqual(result.after.phase,ACTIVE)
        self.assertEqual(
            result.after.base_damage_react_state_by_participant_id[
                "player"
            ].vanish,
            1,
        )
        self.assertEqual(
            result.after.base_damage_react_state_by_participant_id[
                "enemy"
            ].vanish,
            1,
        )
        event=self.light_event(result.round)
        self.assertEqual(event.lighttakeed_resolution.transferred_count,1)


if __name__=="__main__":
    unittest.main()
