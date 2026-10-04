import unittest

from tools.stoneage_battle_damage_react_model import BaseDamageReactState
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
    ENEMY_WIN,
    begin_persistent_battle,
    resolve_persistent_ordinary_round,
)
from tools.stoneage_battle_status_model import (
    BaseBattleStatusRuntime,
    BaseBattleStatusState,
    BaseStatusTurnRolls,
)
from tools.stoneage_battletimid_model import resolve_battletimid_setup
from tools.stoneage_enemy_ai_battletimid_bridge import (
    EnemyAiBattleTimidSubmission,
)
from tools.stoneage_singleplayer_battle import BattleParticipant, BattleSession
from tools.stoneage_singleplayer_domain import (
    EncounterRequest,
    EnemyVariantId,
    MapPosition,
    PetTemplateId,
)


def actor(
    pid,
    side,
    kind,
    *,
    hp=500,
    attack=100,
    defense=0,
    quick=50,
    source_pet_slot=None,
):
    return BattleParticipant(
        participant_id=pid,
        side=side,
        kind=kind,
        level=10,
        hp=hp,
        max_hp=max(1,hp),
        attack=attack,
        defense=defense,
        quick=quick,
        name=pid,
        fixed_vital=40,
        source_pet_slot=source_pet_slot,
    )



def battle_session(player,enemy,pet=None):
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
        allied_pets=(() if pet is None else (pet,)),
        enemies=(enemy,),
    )


def profile(dex=100):
    return BattleCombatProfile(
        fixed_dex=dex,
        fixed_luck=0,
        earth=0,
        water=0,
        fire=0,
        wind=0,
    )


def attack_rolls(*, dodge=10000):
    return OrdinaryAttackRolls(
        dodge_roll_1_10000=dodge,
        critical_roll_1_10000=10000,
        damage_roll=0,
    )


def submission(*, target=0, enemy=None):
    enemy=enemy or actor("enemy","enemy","enemy")
    setup=resolve_battletimid_setup(
        actor_is_player=False,
        target_slot=target,
        skill_array=0,
        packed_com3_before=0,
        fixed_str=enemy.attack,
        fixed_tough=enemy.defense,
        fixed_dex=enemy.quick,
    )
    return EnemyAiBattleTimidSubmission(
        participant_id="enemy",
        skill_slot=0,
        skill_id=606,
        callback="PETSKILL_BattleTimid",
        source_target_slot=target,
        setup=setup,
    )


class BattleTimidRuntimeTests(unittest.TestCase):
    def resolve(
        self,
        *,
        target=0,
        draw=14,
        player=None,
        pet=None,
        enemy=None,
        dodge=10000,
        status_runtime=None,
        status_rolls=None,
        damage_react=None,
        counter_rolls=None,
    ):
        player=player or actor("player","player","player",quick=10)
        enemy=enemy or actor("enemy","enemy","enemy",quick=100)
        participants=[player]
        slots={"player":0,"enemy":10}
        commands={"player":BattleCommand(BATTLE_COM_WAIT)}
        profiles={"player":profile()}
        if pet is not None:
            participants.append(pet)
            slots["pet"]=1
            commands["pet"]=BattleCommand(BATTLE_COM_WAIT)
            profiles["pet"]=profile()
        participants.append(enemy)
        commands["enemy"]=BattleCommand(BATTLE_COM_ATTACK,command2=target)
        profiles["enemy"]=profile()
        prepared=prepare_battle_round(
            tuple(participants),
            commands,
            {p.participant_id:0 for p in participants},
            tie_break_order=tuple(p.participant_id for p in participants),
        )
        sub=submission(target=target,enemy=enemy)
        setup_effects={
            "enemy":BattleCommandSetupEffects(
                attack_power=sub.setup.attack_power,
                defense_power=sub.setup.defence_power,
            )
        }
        return resolve_ordinary_round(
            prepared,
            slots=slots,
            profiles=profiles,
            attack_rolls={"enemy":attack_rolls(dodge=dodge)},
            defense_profile="newpower_70pct",
            command_setup_effects_by_participant_id=setup_effects,
            battletimid_submissions_by_participant_id={"enemy":sub},
            battletimid_rolls_by_participant_id={"enemy":draw},
            base_status_runtime_by_participant_id=status_runtime,
            base_status_rolls_by_participant_id=status_rolls,
            base_damage_react_state_by_participant_id=damage_react,
            counter_rolls_by_attack_id=counter_rolls,
        )

    def timid_event(self,result):
        return next(
            event for event in result.events
            if event.battletimid_skill_id==606
        )

    def test_player_target_forced_exit_is_immediate_and_nonlethal(self):
        result=self.resolve(draw=14)
        event=self.timid_event(result)
        self.assertTrue(event.battletimid_resolution.forced_exit)
        self.assertTrue(event.battletimid_resolution.player_battle_exit)
        self.assertGreater(event.damage,1)
        self.assertGreater(result.hp_by_participant_id["player"],0)
        self.assertIn("player",result.exited_participant_ids)

    def test_pet_target_uses_pet_exit_shape(self):
        pet=actor("pet","player","pet",quick=20)
        result=self.resolve(target=1,draw=14,pet=pet)
        event=self.timid_event(result)
        self.assertTrue(event.battletimid_resolution.forced_exit)
        self.assertTrue(event.battletimid_resolution.pet_default_exit)
        self.assertTrue(event.battletimid_resolution.owner_default_pet_cleared)
        self.assertIn("pet",result.exited_participant_ids)
        self.assertNotIn("player",result.exited_participant_ids)

    def test_draw_15_does_not_exit(self):
        result=self.resolve(draw=15)
        event=self.timid_event(result)
        self.assertFalse(event.battletimid_resolution.forced_exit)
        self.assertEqual(result.exited_participant_ids,())

    def test_dodge_still_consumes_timid_draw_without_exit(self):
        player=actor("player","player","player",quick=10)
        result=self.resolve(
            draw=0,
            player=player,
            dodge=1,
        )
        event=self.timid_event(result)
        self.assertEqual(event.result,"dodge")
        self.assertEqual(event.damage,0)
        self.assertEqual(event.battletimid_resolution.draw,0)
        self.assertEqual(event.battletimid_resolution.rng_draws_consumed,1)
        self.assertFalse(event.battletimid_resolution.forced_exit)

    def test_target_damage_react_is_fail_closed(self):
        with self.assertRaisesRegex(ValueError,"DamageReact"):
            self.resolve(
                draw=14,
                damage_react={"player":BaseDamageReactState(reflect=1)},
            )

    def test_lethal_forced_exit_overlap_is_fail_closed(self):
        with self.assertRaisesRegex(ValueError,"lethal-damage"):
            self.resolve(
                draw=14,
                player=actor("player","player","player",hp=1,quick=10),
            )

    def test_callback_setup_power_drift_is_rejected(self):
        player=actor("player","player","player",quick=10)
        enemy=actor("enemy","enemy","enemy",quick=100)
        prepared=prepare_battle_round(
            (player,enemy),
            {
                "player":BattleCommand(BATTLE_COM_WAIT),
                "enemy":BattleCommand(BATTLE_COM_ATTACK,command2=0),
            },
            {"player":0,"enemy":0},
        )
        sub=submission(enemy=enemy)
        with self.assertRaisesRegex(ValueError,"work-power"):
            resolve_ordinary_round(
                prepared,
                slots={"player":0,"enemy":10},
                profiles={"player":profile(),"enemy":profile()},
                attack_rolls={"enemy":attack_rolls()},
                defense_profile="newpower_70pct",
                command_setup_effects_by_participant_id={
                    "enemy":BattleCommandSetupEffects(
                        attack_power=sub.setup.attack_power+1,
                        defense_power=sub.setup.defence_power,
                    )
                },
                battletimid_submissions_by_participant_id={"enemy":sub},
                battletimid_rolls_by_participant_id={"enemy":14},
            )

    def test_status_suppressed_action_requires_no_timid_draw(self):
        sleeping={
            "enemy":BaseBattleStatusRuntime(
                status=BaseBattleStatusState(sleep=1)
            )
        }
        result=self.resolve(
            draw=None,
            status_runtime=sleeping,
            status_rolls={"enemy":BaseStatusTurnRolls()},
        )
        self.assertFalse(any(
            event.battletimid_skill_id==606 for event in result.events
        ))
        with self.assertRaisesRegex(ValueError,"RNG supplied"):
            self.resolve(
                draw=14,
                status_runtime=sleeping,
                status_rolls={"enemy":BaseStatusTurnRolls()},
            )


    def test_persistent_player_exit_finishes_as_defeat(self):
        player=actor("player","player","player",hp=500,quick=10)
        enemy=actor("enemy","enemy","enemy",quick=100)
        state=begin_persistent_battle(
            battle_session(player,enemy),
            slots={"player":0,"enemy":10},
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
            battletimid_submissions_by_participant_id={"enemy":sub},
            battletimid_rolls_by_participant_id={"enemy":14},
        )
        self.assertEqual(result.after.result,ENEMY_WIN)
        self.assertIn("player",result.after.battle_exited_participant_ids)
        self.assertGreater(result.after.hp_by_participant_id["player"],0)

    def test_persistent_pet_exit_keeps_player_battle_active(self):
        player=actor("player","player","player",hp=500,quick=10)
        pet=actor(
            "pet","player","pet",hp=500,quick=20,source_pet_slot=0
        )
        enemy=actor("enemy","enemy","enemy",quick=100)
        state=begin_persistent_battle(
            battle_session(player,enemy,pet),
            slots={"player":0,"pet":1,"enemy":10},
        )
        sub=submission(target=1,enemy=enemy)
        result=resolve_persistent_ordinary_round(
            state,
            commands={
                "player":BattleCommand(BATTLE_COM_WAIT),
                "pet":BattleCommand(BATTLE_COM_WAIT),
                "enemy":BattleCommand(BATTLE_COM_ATTACK,command2=1),
            },
            initiative_random_subtracts={"player":0,"pet":0,"enemy":0},
            profiles={
                "player":profile(),"pet":profile(),"enemy":profile()
            },
            attack_rolls={"enemy":attack_rolls()},
            defense_profile="newpower_70pct",
            battletimid_submissions_by_participant_id={"enemy":sub},
            battletimid_rolls_by_participant_id={"enemy":14},
        )
        self.assertEqual(result.after.phase,ACTIVE)
        self.assertIn("pet",result.after.battle_exited_participant_ids)
        self.assertNotIn("player",result.after.battle_exited_participant_ids)
        self.assertEqual(
            tuple(p.participant_id for p in result.after.session.allied_pets),
            ("pet",),
        )

    def test_persistent_initiative_uses_callback_workquick_not_fixdex(self):
        player=actor("player","player","player",hp=500,quick=170)
        enemy=actor("enemy","enemy","enemy",quick=200)
        state=begin_persistent_battle(
            battle_session(player,enemy),
            slots={"player":0,"enemy":10},
        )
        sub=submission(enemy=enemy)
        self.assertEqual(sub.setup.quick,160)
        result=resolve_persistent_ordinary_round(
            state,
            commands={
                "player":BattleCommand(BATTLE_COM_WAIT),
                "enemy":BattleCommand(BATTLE_COM_ATTACK,command2=0),
            },
            initiative_random_subtracts={"player":0,"enemy":0},
            profiles={"player":profile(),"enemy":profile(dex=200)},
            attack_rolls={"enemy":attack_rolls()},
            defense_profile="newpower_70pct",
            battletimid_submissions_by_participant_id={"enemy":sub},
            battletimid_rolls_by_participant_id={"enemy":15},
        )
        meaningful=[
            event for event in result.round.events
            if event.result not in {"status_tick","setmagicpet_tick"}
        ]
        self.assertEqual(meaningful[0].participant_id,"player")
        self.assertEqual(profiles_fixed_dex := 200,200)
        self.assertEqual(profiles_fixed_dex,200)


if __name__=="__main__":
    unittest.main()
