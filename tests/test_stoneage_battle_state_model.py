import unittest
from dataclasses import replace

from tools.stoneage_battle_core_model import (
    BattleCaptureInputs,
    BattleDropItem,
    DropAllocationRoll,
)

from tools.stoneage_battle_round_model import (
    BATTLE_COM_ATTACK,
    BATTLE_COM_CAPTURE,
    BATTLE_COM_ESCAPE,
    BATTLE_COM_WAIT,
    BattleCombatProfile,
    BattleCommand,
    CounterAttemptRolls,
    OrdinaryAttackRolls,
    OrdinaryCaptureContext,
    OrdinaryCaptureRolls,
    OrdinaryEscapeContext,
    OrdinaryEscapeRolls,
)
from tools.stoneage_battle_state_model import (
    ACTIVE,
    ENEMY_WIN,
    FINISHED,
    PLAYER_ESCAPE,
    PLAYER_WIN,
    begin_persistent_battle,
    living_non_pet_count,
    resolve_persistent_capture_transition,
    resolve_persistent_ordinary_round,
    termination_result,
)
from tools.stoneage_singleplayer_battle import (
    BattleParticipant,
    BattleSession,
)
from tools.stoneage_singleplayer_domain import (
    EncounterRequest,
    EnemyVariantId,
    MapPosition,
    PetTemplateId,
)


def participant(
    pid,
    side,
    kind,
    *,
    hp=100,
    attack=100,
    defense=70,
    quick=50,
    level=10,
    reward_exp=None,
    source_pet_slot=None,
    reward_items=(),
    max_hp=None,
    capturable=None,
    capture_default=None,
    source_variant_id=None,
    source_template_id=None,
):
    return BattleParticipant(
        participant_id=pid,
        side=side,
        kind=kind,
        level=level,
        hp=hp,
        max_hp=hp if max_hp is None else max_hp,
        attack=attack,
        defense=defense,
        quick=quick,
        name=pid,
        fixed_vital=40,
        reward_exp=reward_exp,
        source_pet_slot=source_pet_slot,
        reward_items=tuple(reward_items),
        capturable=capturable,
        capture_default=capture_default,
        source_variant_id=source_variant_id,
        source_template_id=source_template_id,
    )


def session(player, enemies, pets=(), ride_pet=None):
    encounter = EncounterRequest(
        position=MapPosition(2000, 10, 10),
        area_index=1,
        group_id=1,
        enemy_variant_id=EnemyVariantId(10),
        pet_template_id=PetTemplateId(20),
        level=5,
        max_enemy_count=max(1, len(enemies)),
    )
    return BattleSession(
        origin_position=encounter.position,
        encounter=encounter,
        player=player,
        allied_pets=tuple(pets),
        enemies=tuple(enemies),
        ride_pet=ride_pet,
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


class PersistentBattleStateTests(unittest.TestCase):
    def test_two_rounds_preserve_hp_and_increment_turn(self):
        player = participant("player", "player", "player", attack=60, quick=100)
        enemy = participant("enemy", "enemy", "enemy", hp=200, defense=70, quick=40)
        state = begin_persistent_battle(
            session(player, (enemy,)),
            slots={"player": 0, "enemy": 10},
        )
        self.assertEqual(state.phase, ACTIVE)
        self.assertEqual(state.turn, 0)

        first = resolve_persistent_ordinary_round(
            state,
            commands={
                "player": BattleCommand(BATTLE_COM_ATTACK, command2=10),
                "enemy": BattleCommand(BATTLE_COM_WAIT),
            },
            initiative_random_subtracts={"player": 0, "enemy": 0},
            profiles={"player": profile(), "enemy": profile()},
            attack_rolls={
                "player": OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=1,
                )
            },
            defense_profile="newpower_70pct",
        )
        self.assertEqual(first.after.turn, 1)
        self.assertEqual(first.after.phase, ACTIVE)
        first_hp = first.after.hp_by_participant_id["enemy"]
        self.assertLess(first_hp, 200)

        second = resolve_persistent_ordinary_round(
            first.after,
            commands={
                "player": BattleCommand(BATTLE_COM_ATTACK, command2=10),
                "enemy": BattleCommand(BATTLE_COM_WAIT),
            },
            initiative_random_subtracts={"player": 0, "enemy": 0},
            profiles={"player": profile(), "enemy": profile()},
            attack_rolls={
                "player": OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=1,
                )
            },
            defense_profile="newpower_70pct",
        )
        self.assertEqual(second.after.turn, 2)
        self.assertLess(second.after.hp_by_participant_id["enemy"], first_hp)

    def test_player_death_finishes_even_if_allied_pet_is_alive(self):
        player = participant("player", "player", "player", hp=30, quick=40)
        pet = participant("pet:0", "player", "pet", hp=100, quick=30)
        enemy = participant(
            "enemy", "enemy", "enemy",
            hp=100, attack=200, defense=20, quick=100,
        )
        state = begin_persistent_battle(
            session(player, (enemy,), pets=(pet,)),
            slots={"player": 0, "pet:0": 1, "enemy": 10},
        )
        result = resolve_persistent_ordinary_round(
            state,
            commands={
                "player": BattleCommand(BATTLE_COM_WAIT),
                "pet:0": BattleCommand(BATTLE_COM_WAIT),
                "enemy": BattleCommand(BATTLE_COM_ATTACK, command2=0),
            },
            initiative_random_subtracts={"player": 0, "pet:0": 0, "enemy": 0},
            profiles={
                "player": profile(),
                "pet:0": profile(),
                "enemy": profile(),
            },
            attack_rolls={
                "enemy": OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                )
            },
            defense_profile="newpower_70pct",
        )
        self.assertEqual(result.after.hp_by_participant_id["player"], 0)
        self.assertEqual(result.after.hp_by_participant_id["pet:0"], 100)
        self.assertEqual(living_non_pet_count(result.after, 0), 0)
        self.assertEqual(result.after.phase, FINISHED)
        self.assertEqual(result.after.result, ENEMY_WIN)
        self.assertEqual(result.after.winning_side, 1)

    def test_last_enemy_death_finishes_with_player_victory(self):
        player = participant(
            "player", "player", "player",
            attack=200, quick=100,
        )
        enemy = participant(
            "enemy", "enemy", "enemy",
            hp=30, defense=20, quick=40, reward_exp=1500,
        )
        state = begin_persistent_battle(
            session(player, (enemy,)),
            slots={"player": 0, "enemy": 10},
        )
        result = resolve_persistent_ordinary_round(
            state,
            commands={
                "player": BattleCommand(BATTLE_COM_ATTACK, command2=10),
                "enemy": BattleCommand(BATTLE_COM_WAIT),
            },
            initiative_random_subtracts={"player": 0, "enemy": 0},
            profiles={"player": profile(), "enemy": profile()},
            attack_rolls={
                "player": OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                )
            },
            defense_profile="newpower_70pct",
        )
        self.assertEqual(result.after.hp_by_participant_id["enemy"], 0)
        self.assertEqual(living_non_pet_count(result.after, 1), 0)
        self.assertEqual(result.after.phase, FINISHED)
        self.assertEqual(result.after.result, PLAYER_WIN)
        self.assertEqual(result.after.winning_side, 0)
        self.assertEqual(
            dict(result.after.pending_exp_by_participant_id),
            {"player": 1500},
        )

        with self.assertRaisesRegex(ValueError, "after battle termination"):
            resolve_persistent_ordinary_round(
                result.after,
                commands={},
                initiative_random_subtracts={},
                profiles={},
                attack_rolls={},
                defense_profile="newpower_70pct",
            )

    def test_player_kill_also_awards_exp_to_nonparticipant_ride_pet(self):
        player = participant(
            "player", "player", "player",
            attack=200, quick=100, level=10,
        )
        ride = participant(
            "pet:0", "player", "pet",
            quick=20, level=16, source_pet_slot=0,
        )
        enemy = participant(
            "enemy", "enemy", "enemy",
            hp=30, defense=20, quick=20, level=10, reward_exp=1500,
        )
        state = begin_persistent_battle(
            session(player, (enemy,), ride_pet=ride),
            slots={"player": 0, "enemy": 10},
        )
        self.assertEqual(
            dict(state.pending_exp_by_participant_id),
            {"player": 0, "pet:0": 0},
        )
        self.assertNotIn("pet:0", state.hp_by_participant_id)

        result = resolve_persistent_ordinary_round(
            state,
            commands={
                "player": BattleCommand(BATTLE_COM_ATTACK, command2=10),
                "enemy": BattleCommand(BATTLE_COM_WAIT),
            },
            initiative_random_subtracts={"player": 0, "enemy": 0},
            profiles={"player": profile(), "enemy": profile()},
            attack_rolls={
                "player": OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                )
            },
            defense_profile="newpower_70pct",
        )
        self.assertEqual(
            dict(result.after.pending_exp_by_participant_id),
            {"player": 1500, "pet:0": 840},
        )
        self.assertEqual(
            dict(result.after.pending_pet_variable_ai_by_participant_id),
            {},
        )

    def test_enemy_death_awards_only_the_player_side_actor_that_caused_it(self):
        player = participant("player", "player", "player", quick=40)
        pet = participant(
            "pet:0", "player", "pet",
            attack=200, quick=100, level=16,
        )
        enemy = participant(
            "enemy", "enemy", "enemy",
            hp=30, defense=20, quick=20, level=10, reward_exp=1500,
        )
        state = begin_persistent_battle(
            session(player, (enemy,), pets=(pet,)),
            slots={"player": 0, "pet:0": 1, "enemy": 10},
        )
        result = resolve_persistent_ordinary_round(
            state,
            commands={
                "player": BattleCommand(BATTLE_COM_WAIT),
                "pet:0": BattleCommand(BATTLE_COM_ATTACK, command2=10),
                "enemy": BattleCommand(BATTLE_COM_WAIT),
            },
            initiative_random_subtracts={
                "player": 0,
                "pet:0": 0,
                "enemy": 0,
            },
            profiles={
                "player": profile(),
                "pet:0": profile(),
                "enemy": profile(),
            },
            attack_rolls={
                "pet:0": OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                )
            },
            defense_profile="newpower_70pct",
        )
        self.assertEqual(result.after.phase, FINISHED)
        self.assertEqual(
            dict(result.after.pending_exp_by_participant_id),
            {"player": 0, "pet:0": 1400},
        )
        self.assertEqual(
            dict(result.after.pending_pet_variable_ai_by_participant_id),
            {"pet:0": 1},
        )

    def test_player_counter_kill_uses_counter_actor_for_pending_exp(self):
        player=participant(
            "player","player","player",
            hp=100,attack=200,defense=70,quick=40,level=10,
        )
        enemy=participant(
            "enemy","enemy","enemy",
            hp=30,attack=20,defense=20,quick=100,level=10,reward_exp=1500,
        )
        state=begin_persistent_battle(
            session(player,(enemy,)),
            slots={"player":0,"enemy":10},
        )
        result=resolve_persistent_ordinary_round(
            state,
            commands={
                "player":BattleCommand(BATTLE_COM_ATTACK,command2=10),
                "enemy":BattleCommand(BATTLE_COM_ATTACK,command2=0),
            },
            initiative_random_subtracts={"player":0,"enemy":0},
            profiles={
                "player":BattleCombatProfile(
                    fixed_dex=200,fixed_luck=0,
                    earth=0,water=0,fire=0,wind=0,
                ),
                "enemy":BattleCombatProfile(
                    fixed_dex=100,fixed_luck=0,
                    earth=0,water=0,fire=0,wind=0,
                ),
            },
            attack_rolls={
                "enemy":OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=1,
                ),
                "player":OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                ),
            },
            counter_rolls_by_attack_id={
                "enemy":(
                    CounterAttemptRolls(
                        counter_check_roll_1_10000=1,
                        attack_rolls=OrdinaryAttackRolls(
                            dodge_roll_1_10000=10000,
                            critical_roll_1_10000=10000,
                            damage_roll=0,
                        ),
                    ),
                ),
            },
            defense_profile="newpower_70pct",
        )
        counter=[
            event for event in result.round.events
            if event.is_counter and event.participant_id=="player"
        ][0]
        self.assertEqual(counter.result,"counter_normal")
        self.assertEqual(counter.target_hp_after,0)
        self.assertEqual(result.after.phase,FINISHED)
        self.assertEqual(result.after.result,PLAYER_WIN)
        self.assertEqual(
            dict(result.after.pending_exp_by_participant_id),
            {"player":1500},
        )

        def test_source_side_check_order_preserves_enemy_win_if_both_are_zero(self):
        player = participant("player", "player", "player", hp=1)
        enemy = participant("enemy", "enemy", "enemy", hp=1)
        state = begin_persistent_battle(
            session(player, (enemy,)),
            slots={"player": 0, "enemy": 10},
        )
        zero = replace(
            state,
            hp_by_participant_id={"player": 0, "enemy": 0},
        )
        self.assertEqual(living_non_pet_count(zero, 0), 0)
        self.assertEqual(living_non_pet_count(zero, 1), 0)
        self.assertEqual(termination_result(zero), (ENEMY_WIN, 1))


    def test_enemy_drop_items_flow_into_player_pending_buffer_on_ordinary_kill(self):
        player=participant("player","player","player",attack=200,quick=100)
        items=(
            BattleDropItem("drop:a",501,{"name":"A"}),
            BattleDropItem("drop:b",502,{"name":"B"}),
        )
        enemy=participant(
            "enemy","enemy","enemy",
            hp=30,defense=20,quick=20,reward_exp=100,
            reward_items=items,
        )
        state=begin_persistent_battle(
            session(player,(enemy,)),
            slots={"player":0,"enemy":10},
        )
        result=resolve_persistent_ordinary_round(
            state,
            commands={
                "player":BattleCommand(BATTLE_COM_ATTACK,command2=10),
                "enemy":BattleCommand(BATTLE_COM_WAIT),
            },
            initiative_random_subtracts={"player":0,"enemy":0},
            profiles={"player":profile(),"enemy":profile()},
            attack_rolls={
                "player":OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                )
            },
            drop_rolls_by_enemy_id={
                "enemy":(DropAllocationRoll(0),DropAllocationRoll(0)),
            },
            defense_profile="newpower_70pct",
        )
        self.assertEqual(result.after.phase,FINISHED)
        self.assertEqual(
            result.after.pending_drop_items_by_player_entry_id["player"],
            items,
        )
        self.assertEqual(result.after.destroyed_drop_items,())



    def test_successful_capture_exits_enemy_without_kill_profit(self):
        player=participant("player","player","player",level=10)
        enemy=participant(
            "enemy","enemy","enemy",
            hp=10,max_hp=100,level=10,reward_exp=1500,
            reward_items=(BattleDropItem("held",501),),
            capturable=True,capture_default=11,
            source_variant_id=700,source_template_id=88,
        )
        state=begin_persistent_battle(
            session(player,(enemy,)),
            slots={"player":0,"enemy":10},
        )
        result=resolve_persistent_capture_transition(
            state,
            attacker_id="player",
            target_id="enemy",
            inputs=BattleCaptureInputs(
                10,50,30,3,10,10,100,15,11,
                occupied_pet_slots=(0,2),
            ),
            roll_1_100=1,
        )
        self.assertTrue(result.resolution.success)
        self.assertEqual(result.resolution.assigned_pet_slot,1)
        self.assertEqual(result.captured_target.hp,10)
        self.assertEqual(result.after.session.enemies,())
        self.assertNotIn("enemy",result.after.hp_by_participant_id)
        self.assertNotIn("enemy",result.after.slots)
        self.assertEqual(result.after.phase,FINISHED)
        self.assertEqual(result.after.result,PLAYER_WIN)
        self.assertEqual(dict(result.after.pending_exp_by_participant_id),{"player":0})
        self.assertEqual(
            result.after.pending_drop_items_by_player_entry_id["player"],
            (),
        )
        self.assertEqual(result.after.destroyed_drop_items,())

    def test_failed_capture_leaves_battle_state_unchanged(self):
        player=participant("player","player","player",level=10)
        enemy=participant(
            "enemy","enemy","enemy",
            hp=10,max_hp=100,level=10,
            capturable=True,capture_default=11,
        )
        state=begin_persistent_battle(
            session(player,(enemy,)),
            slots={"player":0,"enemy":10},
        )
        result=resolve_persistent_capture_transition(
            state,
            attacker_id="player",
            target_id="enemy",
            inputs=BattleCaptureInputs(
                10,50,30,3,10,10,100,15,11,
            ),
            roll_1_100=24,
        )
        self.assertFalse(result.resolution.success)
        self.assertIs(result.after,state)
        self.assertEqual(result.after.phase,ACTIVE)


    def test_capture_command_round_removes_target_without_exp_or_drop_profit(self):
        player=participant("player","player","player",quick=100,level=10)
        enemy=participant(
            "enemy","enemy","enemy",
            hp=10,max_hp=100,quick=20,level=10,reward_exp=1500,
            reward_items=(BattleDropItem("held:round",501),),
            capturable=True,capture_default=11,
        )
        state=begin_persistent_battle(
            session(player,(enemy,)),
            slots={"player":0,"enemy":10},
        )
        result=resolve_persistent_ordinary_round(
            state,
            commands={
                "player":BattleCommand(BATTLE_COM_CAPTURE,command2=10),
                "enemy":BattleCommand(BATTLE_COM_WAIT),
            },
            initiative_random_subtracts={"player":0,"enemy":0},
            profiles={
                "player":BattleCombatProfile(
                    fixed_dex=30,fixed_luck=3,
                    earth=0,water=0,fire=0,wind=0,
                ),
                "enemy":BattleCombatProfile(
                    fixed_dex=15,fixed_luck=0,
                    earth=0,water=0,fire=0,wind=0,
                ),
            },
            attack_rolls={},
            defense_profile="newpower_70pct",
            capture_contexts={
                "player":OrdinaryCaptureContext(
                    attacker_charm=50,
                    occupied_pet_slots=(0,2),
                ),
            },
            capture_rolls={
                "player":OrdinaryCaptureRolls(1),
            },
        )
        self.assertEqual(result.round.exited_participant_ids,("enemy",))
        self.assertEqual(result.after.session.enemies,())
        self.assertEqual(result.after.phase,FINISHED)
        self.assertEqual(result.after.result,PLAYER_WIN)
        self.assertEqual(dict(result.after.pending_exp_by_participant_id),{"player":0})
        self.assertEqual(
            result.after.pending_drop_items_by_player_entry_id["player"],()
        )


    def test_persistent_escape_counter_increments_on_failure_then_drives_next_attempt(self):
        player=participant("player","player","player",quick=100,level=10)
        enemy=participant("enemy","enemy","enemy",quick=20,level=30)
        state=begin_persistent_battle(
            session(player,(enemy,)),
            slots={"player":0,"enemy":10},
        )
        self.assertEqual(
            dict(state.escape_count_by_participant_id),
            {"player":0,"enemy":0},
        )
        first=resolve_persistent_ordinary_round(
            state,
            commands={
                "player":BattleCommand(BATTLE_COM_ESCAPE),
                "enemy":BattleCommand(BATTLE_COM_WAIT),
            },
            initiative_random_subtracts={"player":0,"enemy":0},
            profiles={
                "player":BattleCombatProfile(
                    fixed_dex=0,fixed_luck=2,
                    earth=0,water=0,fire=0,wind=0,
                ),
                "enemy":profile(),
            },
            attack_rolls={},
            defense_profile="newpower_70pct",
            escape_contexts={
                "player":OrdinaryEscapeContext(
                    stored_escape_count_before=0,
                ),
            },
            escape_rolls={
                "player":OrdinaryEscapeRolls(40),
            },
        )
        self.assertEqual(first.after.phase,ACTIVE)
        self.assertEqual(first.after.escape_count_by_participant_id["player"],1)
        self.assertEqual(first.round.events[0].result,"escape_failed")

        second=resolve_persistent_ordinary_round(
            first.after,
            commands={
                "player":BattleCommand(BATTLE_COM_ESCAPE),
                "enemy":BattleCommand(BATTLE_COM_WAIT),
            },
            initiative_random_subtracts={"player":0,"enemy":0},
            profiles={
                "player":BattleCombatProfile(
                    fixed_dex=0,fixed_luck=2,
                    earth=0,water=0,fire=0,wind=0,
                ),
                "enemy":profile(),
            },
            attack_rolls={},
            defense_profile="newpower_70pct",
            escape_contexts={
                "player":OrdinaryEscapeContext(
                    stored_escape_count_before=1,
                ),
            },
            escape_rolls={
                "player":OrdinaryEscapeRolls(79),
            },
        )
        self.assertEqual(second.round.events[0].escape_resolution.probability,80)
        self.assertEqual(second.after.phase,FINISHED)
        self.assertEqual(second.after.result,PLAYER_ESCAPE)
        self.assertIsNone(second.after.winning_side)
        self.assertEqual(second.after.escape_count_by_participant_id["player"],2)
        self.assertEqual(
            dict(second.after.pending_exp_by_participant_id),
            {"player":0},
        )

    def test_persistent_escape_rejects_caller_counter_drift(self):
        player=participant("player","player","player",level=10)
        enemy=participant("enemy","enemy","enemy",level=10)
        state=begin_persistent_battle(
            session(player,(enemy,)),
            slots={"player":0,"enemy":10},
        )
        with self.assertRaisesRegex(ValueError,"escape counter drift"):
            resolve_persistent_ordinary_round(
                state,
                commands={
                    "player":BattleCommand(BATTLE_COM_ESCAPE),
                    "enemy":BattleCommand(BATTLE_COM_WAIT),
                },
                initiative_random_subtracts={"player":0,"enemy":0},
                profiles={"player":profile(),"enemy":profile()},
                attack_rolls={},
                defense_profile="newpower_70pct",
                escape_contexts={
                    "player":OrdinaryEscapeContext(
                        stored_escape_count_before=1,
                    ),
                },
                escape_rolls={"player":OrdinaryEscapeRolls(1)},
            )



    def test_player_death_accumulates_charm_and_active_pet_loyalty_penalty(self):
        player=participant(
            "player","player","player",
            hp=20,defense=0,quick=20,level=11,
        )
        pet=participant(
            "pet:0","player","pet",
            hp=100,quick=10,level=20,source_pet_slot=0,
        )
        enemy=participant(
            "enemy","enemy","enemy",
            hp=100,attack=200,quick=100,level=20,
        )
        state=begin_persistent_battle(
            session(player,(enemy,),pets=(pet,)),
            slots={"player":0,"pet:0":1,"enemy":10},
        )
        result=resolve_persistent_ordinary_round(
            state,
            commands={
                "player":BattleCommand(BATTLE_COM_WAIT),
                "pet:0":BattleCommand(BATTLE_COM_WAIT),
                "enemy":BattleCommand(BATTLE_COM_ATTACK,command2=0),
            },
            initiative_random_subtracts={
                "player":0,"pet:0":0,"enemy":0,
            },
            profiles={
                "player":profile(),"pet:0":profile(),"enemy":profile(),
            },
            attack_rolls={
                "enemy":OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                )
            },
            defense_profile="newpower_70pct",
        )
        self.assertEqual(result.after.phase,FINISHED)
        self.assertEqual(result.after.result,ENEMY_WIN)
        self.assertEqual(result.after.pending_player_charm_delta,-2)
        self.assertEqual(
            dict(result.after.pending_pet_variable_ai_by_participant_id),
            {"pet:0":-100},
        )
        self.assertEqual(result.after.pending_player_dead_pet_count_delta,0)

    def test_pet_death_accumulates_signed_loyalty_and_dead_pet_count_once(self):
        player=participant(
            "player","player","player",
            hp=100,quick=20,level=11,
        )
        pet=participant(
            "pet:0","player","pet",
            hp=20,defense=0,quick=10,level=20,source_pet_slot=0,
        )
        enemy=participant(
            "enemy","enemy","enemy",
            hp=100,attack=200,quick=100,level=20,
        )
        state=begin_persistent_battle(
            session(player,(enemy,),pets=(pet,)),
            slots={"player":0,"pet:0":1,"enemy":10},
        )
        first=resolve_persistent_ordinary_round(
            state,
            commands={
                "player":BattleCommand(BATTLE_COM_WAIT),
                "pet:0":BattleCommand(BATTLE_COM_WAIT),
                "enemy":BattleCommand(BATTLE_COM_ATTACK,command2=1),
            },
            initiative_random_subtracts={
                "player":0,"pet:0":0,"enemy":0,
            },
            profiles={
                "player":profile(),"pet:0":profile(),"enemy":profile(),
            },
            attack_rolls={
                "enemy":OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                )
            },
            defense_profile="newpower_70pct",
        )
        self.assertEqual(first.after.phase,ACTIVE)
        self.assertEqual(
            first.after.pending_pet_variable_ai_by_participant_id["pet:0"],
            -500,
        )
        self.assertEqual(first.after.pending_player_dead_pet_count_delta,1)

        second=resolve_persistent_ordinary_round(
            first.after,
            commands={
                "player":BattleCommand(BATTLE_COM_WAIT),
                "enemy":BattleCommand(BATTLE_COM_WAIT),
            },
            initiative_random_subtracts={"player":0,"enemy":0},
            profiles={"player":profile(),"enemy":profile()},
            attack_rolls={},
            defense_profile="newpower_70pct",
        )
        self.assertEqual(
            second.after.pending_pet_variable_ai_by_participant_id["pet:0"],
            -500,
        )
        self.assertEqual(second.after.pending_player_dead_pet_count_delta,1)

    def test_no_risk_round_suppresses_normal_death_penalties(self):
        player=participant(
            "player","player","player",
            hp=20,defense=0,quick=20,level=11,
        )
        pet=participant(
            "pet:0","player","pet",
            hp=100,quick=10,level=20,source_pet_slot=0,
        )
        enemy=participant(
            "enemy","enemy","enemy",
            hp=100,attack=200,quick=100,level=20,
        )
        state=begin_persistent_battle(
            session(player,(enemy,),pets=(pet,)),
            slots={"player":0,"pet:0":1,"enemy":10},
        )
        result=resolve_persistent_ordinary_round(
            state,
            commands={
                "player":BattleCommand(BATTLE_COM_WAIT),
                "pet:0":BattleCommand(BATTLE_COM_WAIT),
                "enemy":BattleCommand(BATTLE_COM_ATTACK,command2=0),
            },
            initiative_random_subtracts={
                "player":0,"pet:0":0,"enemy":0,
            },
            profiles={
                "player":profile(),"pet:0":profile(),"enemy":profile(),
            },
            attack_rolls={
                "enemy":OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                )
            },
            defense_profile="newpower_70pct",
            no_risk=True,
        )
        self.assertEqual(result.after.pending_player_charm_delta,0)
        self.assertEqual(
            result.after.pending_pet_variable_ai_by_participant_id["pet:0"],
            0,
        )



    def test_no_risk_does_not_erase_ordinary_pet_kill_loyalty(self):
        player=participant("player","player","player",quick=20,level=20)
        pet=participant(
            "pet:0","player","pet",
            attack=200,quick=100,level=20,source_pet_slot=0,
        )
        enemy=participant(
            "enemy","enemy","enemy",
            hp=20,defense=0,quick=10,level=10,reward_exp=100,
        )
        state=begin_persistent_battle(
            session(player,(enemy,),pets=(pet,)),
            slots={"player":0,"pet:0":1,"enemy":10},
        )
        result=resolve_persistent_ordinary_round(
            state,
            commands={
                "player":BattleCommand(BATTLE_COM_WAIT),
                "pet:0":BattleCommand(BATTLE_COM_ATTACK,command2=10),
                "enemy":BattleCommand(BATTLE_COM_WAIT),
            },
            initiative_random_subtracts={"player":0,"pet:0":0,"enemy":0},
            profiles={"player":profile(),"pet:0":profile(),"enemy":profile()},
            attack_rolls={
                "pet:0":OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                )
            },
            defense_profile="newpower_70pct",
            no_risk=True,
        )
        self.assertEqual(
            result.after.pending_pet_variable_ai_by_participant_id["pet:0"],
            1,
        )
        self.assertEqual(result.after.pending_player_charm_delta,0)
        self.assertEqual(result.after.pending_player_dead_pet_count_delta,0)



if __name__ == "__main__":
    unittest.main()
