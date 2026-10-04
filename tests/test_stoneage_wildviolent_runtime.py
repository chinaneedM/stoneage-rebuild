import unittest
from dataclasses import replace
from hashlib import sha256
from types import SimpleNamespace
from unittest.mock import patch

from tools.stoneage_enemy_ai_wildviolent_bridge import (
    CONDITIONAL_EXECUTION_CHARSET,
    EnemyAiWildViolentSubmission,
    validate_recovered25_wildviolent_population,
    resolve_enemy_ai_wildviolent_submission,
)
from tools.stoneage_recovered25_petskill_runtime import (
    Recovered25PetSkillEntry,
    Recovered25PetSkillRuntime,
)
from tools.stoneage_wildviolent_model import (
    CALLBACK_NAME,
    resolve_wildviolent_setup,
)
from tools.stoneage_battle_round_model import (
    BATTLE_COM_ATTACK,
    BATTLE_COM_WAIT,
    BattleCombatProfile,
    BattleCommand,
    BattleCommandSetupEffects,
    CounterAttemptRolls,
    OrdinaryAttackRolls,
    WildViolentRolls,
    _resolve_nonbow_multihit_baseline,
    apply_base_combo_rewrite,
    prepare_battle_round,
    resolve_ordinary_round,
)
from tools.stoneage_battle_status_model import (
    BaseBattleStatusRuntime,
    BaseBattleStatusState,
    BaseStatusTurnRolls,
)
from tools.stoneage_singleplayer_battle import BattleParticipant
from tools.stoneage_battle_guardian_model import GuardianRegistration
from tools.stoneage_battle_damage_react_model import BaseDamageReactState
from tools.stoneage_battle_ride_damage_model import RidePetRuntime
from tools.stoneage_battle_core_model import physical_base_damage
from tools.stoneage_wildviolent_model import wildviolent_divided_damage


# Independently invented fixtures: patch only their hashes, retaining production
# population, metadata, parsing, seven-slot and callback setup validation.
SYNTHETIC_OPTIONS = {
    541: "攻%95防%-35避30".encode("cp950").ljust(20, b" "),
    652: "攻%60防%-50避50".encode("cp950").ljust(20, b" "),
}
SYNTHETIC_HASHES = {key: sha256(raw).hexdigest() for key, raw in SYNTHETIC_OPTIONS.items()}


def synthetic_population():
    return Recovered25PetSkillRuntime({
        key: Recovered25PetSkillEntry(key, 1, 6, 2, 1000, CALLBACK_NAME, raw)
        for key, raw in SYNTHETIC_OPTIONS.items()
    }, "independent-synthetic-fixtures")


def synthetic_setup(target=0, packed=0x1234):
    return resolve_wildviolent_setup(
        option="攻%95防%-35避30".encode("cp950"),
        execution_charset="cp950",
        profile="gavin",
        target_slot=target,
        fixed_strength=100,
        fixed_toughness=100,
        attack_power_before=80,
        defense_power_before=90,
        packed_com3_before=packed,
    )


class WildViolentTypedAdmissionTests(unittest.TestCase):
    def test_typed_submission_keeps_symbolic_identity_and_conditional_charset(self):
        setup=synthetic_setup(target=0,packed=0x2345)
        submission=EnemyAiWildViolentSubmission(
            participant_id="enemy",
            skill_slot=0,
            skill_id=541,
            callback=CALLBACK_NAME,
            source_target_slot=0,
            setup=setup,
        )
        self.assertEqual(submission.conditional_execution_charset,CONDITIONAL_EXECUTION_CHARSET)
        self.assertEqual(submission.semantic_command_name,"BATTLE_COM_S_WILDVIOLENTATTACK")
        self.assertEqual(submission.setup.packed_com3 & 0xffff,0x2345)
        self.assertEqual(submission.setup.option.additive_dodge_percent_points,30)

    def test_unreferenced_652_cannot_be_selected_submission(self):
        with self.assertRaisesRegex(ValueError,"selected ID"):
            EnemyAiWildViolentSubmission(
                participant_id="enemy",
                skill_slot=0,
                skill_id=652,
                callback=CALLBACK_NAME,
                source_target_slot=0,
                setup=synthetic_setup(),
            )

    def test_population_validator_rejects_nonexact_synthetic_rows(self):
        bad=Recovered25PetSkillRuntime(
            skills={
                541:Recovered25PetSkillEntry(
                    541,1,6,2,1000,CALLBACK_NAME,
                    "攻%95防%-35避30".encode("cp950"),
                ),
                652:Recovered25PetSkillEntry(
                    652,1,6,2,1000,CALLBACK_NAME,
                    "攻%60防%-50避50".encode("cp950"),
                ),
            },
            source_file="petskill.txt",
        )
        with self.assertRaisesRegex(ValueError,"metadata/OPTION hash drift"):
            validate_recovered25_wildviolent_population(bad)
    def test_nonbow_runtime_repeats_original_target_and_divides_each_hit(self):
        actor=BattleParticipant("enemy","enemy","enemy",20,500,500,100,100,100,"enemy")
        defender=BattleParticipant("player","player","player",20,1000,1000,10,0,50,"player")
        setup=synthetic_setup(target=0,packed=0x2345)
        submission=EnemyAiWildViolentSubmission(
            participant_id="enemy",skill_slot=0,skill_id=541,
            callback=CALLBACK_NAME,source_target_slot=0,setup=setup,
        )
        command=BattleCommand(BATTLE_COM_ATTACK,command2=0,command3=setup.packed_com3)
        hit=OrdinaryAttackRolls(
            critical_roll_1_10000=10000,
            damage_roll=0,
            dodge_roll_1_10000=10000,
        )
        result=_resolve_nonbow_multihit_baseline(
            actor=actor,actor_slot=10,command=command,action_value=100,
            by_slot={0:defender,10:actor},hp_by_slot={0:1000,10:500},
            profiles={
                "player":BattleCombatProfile(fixed_dex=50,fixed_luck=0,earth=0,water=0,fire=0,wind=0),
                "enemy":BattleCombatProfile(fixed_dex=100,fixed_luck=0,earth=0,water=0,fire=0,wind=0),
            },
            command_by_slot={0:BattleCommand(0),10:command},
            rolls=WildViolentRolls(3,(hit,hit,hit)),
            defense_profile="newpower_70pct",
            setup_effects_by_participant_id={
                "enemy":BattleCommandSetupEffects(
                    attack_power=setup.attack_power,
                    defense_power=setup.defense_power,
                )
            },
            wildviolent_submission=submission,
        )
        self.assertEqual(len(result.events),3)
        self.assertEqual([event.wildviolent_hit_index for event in result.events],[0,1,2])
        self.assertTrue(all(event.original_target_slot==0 for event in result.events))
        self.assertTrue(all(event.wildviolent_attack_count==3 for event in result.events))
        self.assertTrue(all(event.wildviolent_dodge_percent_points==30 for event in result.events))
        self.assertLess(result.hp_by_slot[0],1000)


    def test_action_roll_bundle_closes_three_and_ten_boundaries(self):
        hit=OrdinaryAttackRolls(
            critical_roll_1_10000=10000,
            damage_roll=0,
            dodge_roll_1_10000=10000,
        )
        self.assertEqual(len(WildViolentRolls(3,(hit,)*3).hit_rolls),3)
        self.assertEqual(len(WildViolentRolls(10,(hit,)*10).hit_rolls),10)
        with self.assertRaisesRegex(ValueError,"3..10"):
            WildViolentRolls(2,(hit,)*2)
        with self.assertRaisesRegex(ValueError,"3..10"):
            WildViolentRolls(11,(hit,)*11)
        with self.assertRaisesRegex(ValueError,"exactly count-roll"):
            WildViolentRolls(3,(hit,)*2)

    def test_dead_original_retargets_each_later_wildviolent_hit(self):
        actor=BattleParticipant(
            "enemy","enemy","enemy",20,500,500,100,100,100,"enemy"
        )
        original=BattleParticipant(
            "original","player","pet",20,1,1,10,0,50,"original"
        )
        p1=BattleParticipant("p1","player","pet",20,1000,1000,10,0,50,"p1")
        p2=BattleParticipant("p2","player","pet",20,1000,1000,10,0,50,"p2")
        setup=synthetic_setup(target=0,packed=0x2345)
        submission=EnemyAiWildViolentSubmission(
            participant_id="enemy",skill_slot=0,skill_id=541,
            callback=CALLBACK_NAME,source_target_slot=0,setup=setup,
        )
        command=BattleCommand(
            BATTLE_COM_ATTACK,command2=0,command3=setup.packed_com3
        )
        hits=(
            OrdinaryAttackRolls(
                critical_roll_1_10000=10000,damage_roll=0,
                dodge_roll_1_10000=10000,
            ),
            OrdinaryAttackRolls(
                critical_roll_1_10000=10000,damage_roll=0,
                dodge_roll_1_10000=10000,retarget_roll=0,
            ),
            OrdinaryAttackRolls(
                critical_roll_1_10000=10000,damage_roll=0,
                dodge_roll_1_10000=10000,retarget_roll=1,
            ),
        )
        result=_resolve_nonbow_multihit_baseline(
            actor=actor,actor_slot=10,command=command,action_value=100,
            by_slot={0:original,1:p1,2:p2,10:actor},
            hp_by_slot={0:1,1:1000,2:1000,10:500},
            profiles={
                "original":BattleCombatProfile(
                    fixed_dex=50,fixed_luck=0,earth=0,water=0,fire=0,wind=0
                ),
                "p1":BattleCombatProfile(
                    fixed_dex=50,fixed_luck=0,earth=0,water=0,fire=0,wind=0
                ),
                "p2":BattleCombatProfile(
                    fixed_dex=50,fixed_luck=0,earth=0,water=0,fire=0,wind=0
                ),
                "enemy":BattleCombatProfile(
                    fixed_dex=100,fixed_luck=0,earth=0,water=0,fire=0,wind=0
                ),
            },
            command_by_slot={
                0:BattleCommand(BATTLE_COM_WAIT),
                1:BattleCommand(BATTLE_COM_WAIT),
                2:BattleCommand(BATTLE_COM_WAIT),
                10:command,
            },
            rolls=WildViolentRolls(3,hits),
            defense_profile="newpower_70pct",
            setup_effects_by_participant_id={
                "enemy":BattleCommandSetupEffects(
                    attack_power=setup.attack_power,
                    defense_power=setup.defense_power,
                )
            },
            wildviolent_submission=submission,
        )
        self.assertEqual(
            tuple(event.resolved_target_slot for event in result.events),
            (0,1,2),
        )
        self.assertEqual(result.hp_by_slot[0],0)
        self.assertTrue(result.events[1].retargeted)
        self.assertTrue(result.events[2].retargeted)

    def _status_suppression_case(self, status, status_rolls=None, attack_rolls=None):
        actor=BattleParticipant(
            "enemy","enemy","enemy",20,500,500,100,100,100,"enemy"
        )
        defender=BattleParticipant(
            "player","player","player",20,1000,1000,10,0,50,"player"
        )
        setup=synthetic_setup(target=0,packed=0x2345)
        submission=EnemyAiWildViolentSubmission(
            participant_id="enemy",skill_slot=0,skill_id=541,
            callback=CALLBACK_NAME,source_target_slot=0,setup=setup,
        )
        command=BattleCommand(
            BATTLE_COM_ATTACK,command2=0,command3=setup.packed_com3
        )
        prepared=prepare_battle_round(
            (defender,actor),
            {
                "player":BattleCommand(BATTLE_COM_WAIT),
                "enemy":command,
            },
            {"player":0,"enemy":0},
        )
        kwargs=dict(
            slots={"player":0,"enemy":10},
            profiles={
                "player":BattleCombatProfile(
                    fixed_dex=50,fixed_luck=0,earth=0,water=0,fire=0,wind=0
                ),
                "enemy":BattleCombatProfile(
                    fixed_dex=100,fixed_luck=0,earth=0,water=0,fire=0,wind=0
                ),
            },
            attack_rolls=dict(attack_rolls or {}),
            wildviolent_submissions_by_participant_id={"enemy":submission},
            command_setup_effects_by_participant_id={
                "enemy":BattleCommandSetupEffects(
                    attack_power=setup.attack_power,
                    defense_power=setup.defense_power,
                )
            },
            base_status_runtime_by_participant_id={
                "player":BaseBattleStatusRuntime(work_quick=50),
                "enemy":BaseBattleStatusRuntime(
                    status=status,work_quick=100
                ),
            },
            base_status_rolls_by_participant_id=(
                {} if status_rolls is None else {"enemy":status_rolls}
            ),
            defense_profile="newpower_70pct",
        )
        return prepared,kwargs

    def test_sleep_suppresses_action_time_rng_and_rejects_preconsumption(self):
        prepared,kwargs=self._status_suppression_case(
            BaseBattleStatusState(sleep=2)
        )
        result=resolve_ordinary_round(prepared,**kwargs)
        self.assertFalse(
            any(event.wildviolent_skill_id is not None for event in result.events)
        )
        hit=OrdinaryAttackRolls(
            critical_roll_1_10000=10000,damage_roll=0,
            dodge_roll_1_10000=10000,
        )
        with self.assertRaisesRegex(ValueError,"unused WildViolentAttack"):
            resolve_ordinary_round(
                prepared,
                **kwargs,
                wildviolent_rolls_by_attack_id={
                    "enemy":WildViolentRolls(3,(hit,hit,hit))
                },
            )

    def test_confusion_rewrite_suppresses_wildviolent_semantic_action(self):
        ordinary=OrdinaryAttackRolls(
            critical_roll_1_10000=10000,damage_roll=0,
            dodge_roll_1_10000=10000,
        )
        prepared,kwargs=self._status_suppression_case(
            BaseBattleStatusState(confusion=2),
            BaseStatusTurnRolls(
                confusion_action_roll_1_100=1,
                confusion_side_roll_0_1=0,
                confusion_pos_roll_0_9=0,
            ),
            {"enemy":ordinary},
        )
        result=resolve_ordinary_round(prepared,**kwargs)
        ticks=[
            event for event in result.events
            if event.participant_id=="enemy"
            and event.status_tick_resolution is not None
        ]
        self.assertEqual(len(ticks),1)
        self.assertTrue(ticks[0].status_tick_resolution.confusion_rewrote_command)
        self.assertFalse(
            any(event.wildviolent_skill_id is not None for event in result.events)
        )
        with self.assertRaisesRegex(ValueError,"unused WildViolentAttack"):
            resolve_ordinary_round(
                prepared,
                **kwargs,
                wildviolent_rolls_by_attack_id={
                    "enemy":WildViolentRolls(3,(ordinary,ordinary,ordinary))
                },
            )



    def test_no_remaining_opposite_target_terminates_after_kill(self):
        actor=BattleParticipant(
            "enemy","enemy","enemy",20,500,500,100,100,100,"enemy"
        )
        original=BattleParticipant(
            "original","player","pet",20,1,1,10,0,50,"original"
        )
        setup=synthetic_setup(target=0,packed=0x2345)
        submission=EnemyAiWildViolentSubmission(
            participant_id="enemy",skill_slot=0,skill_id=541,
            callback=CALLBACK_NAME,source_target_slot=0,setup=setup,
        )
        command=BattleCommand(
            BATTLE_COM_ATTACK,command2=0,command3=setup.packed_com3
        )
        hit=OrdinaryAttackRolls(
            critical_roll_1_10000=10000,
            damage_roll=0,
            dodge_roll_1_10000=10000,
        )
        result=_resolve_nonbow_multihit_baseline(
            actor=actor,actor_slot=10,command=command,action_value=100,
            by_slot={0:original,10:actor},
            hp_by_slot={0:1,10:500},
            profiles={
                "original":BattleCombatProfile(
                    fixed_dex=50,fixed_luck=0,earth=0,water=0,fire=0,wind=0
                ),
                "enemy":BattleCombatProfile(
                    fixed_dex=100,fixed_luck=0,earth=0,water=0,fire=0,wind=0
                ),
            },
            command_by_slot={
                0:BattleCommand(BATTLE_COM_WAIT),
                10:command,
            },
            rolls=WildViolentRolls(3,(hit,OrdinaryAttackRolls(None,None),OrdinaryAttackRolls(None,None))),
            defense_profile="newpower_70pct",
            setup_effects_by_participant_id={
                "enemy":BattleCommandSetupEffects(
                    attack_power=setup.attack_power,
                    defense_power=setup.defense_power,
                )
            },
            wildviolent_submission=submission,
        )
        self.assertEqual(len(result.events),1)
        self.assertEqual(result.hp_by_slot[0],0)
        self.assertFalse(result.counter_continuation_allowed)

    def test_semantic_carrier_is_excluded_from_base_combo_rewrite(self):
        player=BattleParticipant(
            "player","player","player",20,1000,1000,10,0,50,"player"
        )
        e1=BattleParticipant(
            "e1","enemy","enemy",20,500,500,100,100,100,"e1"
        )
        e2=BattleParticipant(
            "e2","enemy","enemy",20,500,500,90,100,100,"e2"
        )
        prepared=prepare_battle_round(
            (player,e1,e2),
            {
                "player":BattleCommand(BATTLE_COM_WAIT),
                "e1":BattleCommand(BATTLE_COM_ATTACK,command2=0),
                "e2":BattleCommand(BATTLE_COM_ATTACK,command2=0),
            },
            {"player":0,"e1":0,"e2":0},
            tie_break_order=("e1", "e2", "player"),
        )
        rewritten=apply_base_combo_rewrite(
            prepared,
            {
                "player":BattleCombatProfile(
                    fixed_dex=50,fixed_luck=0,earth=0,water=0,fire=0,wind=0
                ),
                "e1":BattleCombatProfile(
                    fixed_dex=100,fixed_luck=0,earth=0,water=0,fire=0,wind=0
                ),
                "e2":BattleCombatProfile(
                    fixed_dex=90,fixed_luck=0,earth=0,water=0,fire=0,wind=0
                ),
            },
            {"e1":1,"e2":1},
            semantic_nonattack_ids=("e1",),
        )
        e1_entry=next(
            entry for entry in rewritten.ordered_entries
            if entry.participant.participant_id=="e1"
        )
        self.assertEqual(e1_entry.command.command1,BATTLE_COM_ATTACK)
        self.assertEqual(e1_entry.combo_id,0)

    def test_wildviolent_finishes_before_shared_final_counter_probe(self):
        player=BattleParticipant(
            "player","player","player",20,1000,1000,80,70,200,"player"
        )
        enemy=BattleParticipant(
            "enemy","enemy","enemy",20,1000,1000,100,70,100,"enemy"
        )
        setup=synthetic_setup(target=0,packed=0x2345)
        submission=EnemyAiWildViolentSubmission(
            participant_id="enemy",skill_slot=0,skill_id=541,
            callback=CALLBACK_NAME,source_target_slot=0,setup=setup,
        )
        command=BattleCommand(
            BATTLE_COM_ATTACK,command2=0,command3=setup.packed_com3
        )
        prepared=prepare_battle_round(
            (player,enemy),
            {
                "player":BattleCommand(BATTLE_COM_ATTACK,command2=10),
                "enemy":command,
            },
            {"player":0,"enemy":0},
        )
        hit=OrdinaryAttackRolls(
            critical_roll_1_10000=10000,
            damage_roll=0,
            dodge_roll_1_10000=10000,
        )
        result=resolve_ordinary_round(
            prepared,
            slots={"player":0,"enemy":10},
            profiles={
                "player":BattleCombatProfile(
                    fixed_dex=200,fixed_luck=0,earth=0,water=0,fire=0,wind=0
                ),
                "enemy":BattleCombatProfile(
                    fixed_dex=100,fixed_luck=0,earth=0,water=0,fire=0,wind=0
                ),
            },
            attack_rolls={
                "player":OrdinaryAttackRolls(
                    critical_roll_1_10000=1,
                    damage_roll=0,
                    dodge_roll_1_10000=10000,
                )
            },
            wildviolent_submissions_by_participant_id={"enemy":submission},
            wildviolent_rolls_by_attack_id={
                "enemy":WildViolentRolls(3,(hit,hit,hit))
            },
            command_setup_effects_by_participant_id={
                "enemy":BattleCommandSetupEffects(
                    attack_power=setup.attack_power,
                    defense_power=setup.defense_power,
                )
            },
            counter_rolls_by_attack_id={
                "enemy":(
                    CounterAttemptRolls(
                        counter_check_roll_1_10000=10000
                    ),
                )
            },
            defense_profile="newpower_70pct",
        )
        wild=[
            event for event in result.events
            if event.wildviolent_skill_id is not None
        ]
        counters=[event for event in result.events if event.is_counter]
        self.assertEqual(len(wild),3)
        self.assertEqual([event.wildviolent_hit_index for event in wild],[0,1,2])
        self.assertEqual(len(counters),1)
        self.assertEqual(counters[0].participant_id,"player")
        self.assertEqual(counters[0].resolved_target_slot,10)
        self.assertGreater(
            result.events.index(counters[0]),
            result.events.index(wild[-1]),
        )

class WildViolentInteractionTests(unittest.TestCase):
    def resolve(self, *, count=3, hits=None, players=None, enemy=None, target=0,
                commands=None, extra=None):
        from tests.test_stoneage_attack_crazed_runtime import actor, hit
        players = players if players is not None else {0: actor("player", "player", "player")}
        enemy = enemy or actor("enemy", "enemy", "enemy", defense=100, quick=200)
        participants = (*players.values(), enemy)
        setup = resolve_wildviolent_setup(
            option=SYNTHETIC_OPTIONS[541], execution_charset="cp950", profile="gavin",
            target_slot=target, fixed_strength=enemy.attack, fixed_toughness=enemy.defense,
            attack_power_before=enemy.attack, defense_power_before=enemy.defense,
            packed_com3_before=0x2345,
        )
        submission = EnemyAiWildViolentSubmission("enemy", 0, 541, CALLBACK_NAME, target, setup)
        cmds = {p.participant_id: BattleCommand(BATTLE_COM_WAIT) for p in players.values()}
        cmds["enemy"] = BattleCommand(BATTLE_COM_ATTACK, target, setup.packed_com3)
        cmds.update(commands or {})
        prepared = prepare_battle_round(
            participants, cmds, {p.participant_id: 0 for p in participants},
            tie_break_order=tuple(p.participant_id for p in participants),
        )
        args = dict(
            slots={p.participant_id: slot for slot, p in players.items()} | {"enemy": 10},
            profiles={p.participant_id: BattleCombatProfile(p.quick, 0, 0, 0, 0, 0) for p in participants},
            attack_rolls={}, defense_profile="newpower_70pct",
            wildviolent_submissions_by_participant_id={"enemy": submission},
            wildviolent_rolls_by_attack_id={"enemy": WildViolentRolls(count, hits or (hit(),) * count)},
            command_setup_effects_by_participant_id={"enemy": BattleCommandSetupEffects(
                attack_power=setup.attack_power, defense_power=setup.defense_power)},
        )
        args.update(extra or {})
        return resolve_ordinary_round(prepared, **args)

    def wild_events(self, result):
        return tuple(e for e in result.events if e.wildviolent_skill_id is not None)

    def test_three_and_ten_hits_have_exact_float_division(self):
        for count in (3, 10):
            with self.subTest(count=count):
                events = self.wild_events(self.resolve(count=count))
                self.assertEqual(len(events), count)
                self.assertEqual([e.damage for e in events],
                                 [wildviolent_divided_damage(physical_base_damage(195, 0, 0), count)] * count)

    def test_dodge_uses_additive_modifier_and_does_not_consume_damage_rng(self):
        # Enemy DEX 250 becomes 200 against PET DEX 200, with zero base dodge. The
        # callback adds 3000 (inclusive source boundary).
        from tests.test_stoneage_attack_crazed_runtime import actor
        players = {0: actor("player", "player", "pet", quick=200)}
        dodge = OrdinaryAttackRolls(None, None, dodge_roll_1_10000=3000)
        hits = (dodge, OrdinaryAttackRolls(10000, 0, dodge_roll_1_10000=3001), dodge)
        enemy = actor("enemy", "enemy", "enemy", quick=250)
        events = self.wild_events(self.resolve(players=players, enemy=enemy, hits=hits))
        self.assertEqual([e.result for e in events], ["wildviolent_dodge", "wildviolent_normal", "wildviolent_dodge"])

    def test_guardian_redirect_then_division_and_later_hits_continue(self):
        from tests.test_stoneage_attack_crazed_runtime import actor
        players = {0: actor("player", "player", "player"), 1: actor("pet", "player", "pet")}
        events = self.wild_events(self.resolve(players=players, extra={
            "guardian_registrations_by_defender_slot": {0: GuardianRegistration(1)},
        }))
        self.assertEqual([e.resolved_target_slot for e in events], [1, 1, 1])
        self.assertTrue(all(e.guardian_redirected and e.guarded_target_slot == 0 for e in events))
        self.assertTrue(all(e.damage == wildviolent_divided_damage(physical_base_damage(195, 0, 0), 3) for e in events))

    def test_reflection_false_continuation_does_not_stop_later_hits(self):
        result = self.resolve(extra={"base_damage_react_state_by_participant_id": {
            "player": BaseDamageReactState(reflect=1)}})
        events = self.wild_events(result)
        self.assertEqual(len(events), 3)
        self.assertEqual([e.resolved_target_slot for e in events], [10, 0, 0])
        self.assertEqual(events[0].damage_react_resolution.state_after.reflect, 0)

    def test_reflected_actor_death_stops_later_hits(self):
        from tests.test_stoneage_attack_crazed_runtime import actor, hit
        result = self.resolve(enemy=actor("enemy", "enemy", "enemy", hp=1, quick=200),
                              hits=(hit(), OrdinaryAttackRolls(None, None), OrdinaryAttackRolls(None, None)), extra={
            "base_damage_react_state_by_participant_id": {"player": BaseDamageReactState(reflect=1)}})
        self.assertEqual(len(self.wild_events(result)), 1)
        self.assertEqual(result.hp_by_participant_id["enemy"], 0)

    def test_ride_pet_falls_after_divided_first_hit(self):
        result = self.resolve(extra={"ride_pet_runtime": RidePetRuntime("player", "ride", 1, 1, 0)})
        events = self.wild_events(result)
        self.assertEqual(len(events), 3)
        self.assertIsNotNone(events[0].ride_damage_split)
        self.assertEqual(events[0].ride_damage_split.raw_damage,
                         wildviolent_divided_damage(physical_base_damage(195, 0, 0), 3))
        self.assertEqual(events[0].ride_pet_fell_rider_id, "player")
        self.assertIsNone(events[1].ride_damage_split)
        self.assertFalse(result.ride_pet_runtime.mounted)

    def test_callback_defense_is_visible_before_actor_dispatch(self):
        from tests.test_stoneage_attack_crazed_runtime import actor, hit
        players = {0: actor("player", "player", "player", quick=300)}
        result = self.resolve(players=players, commands={"player": BattleCommand(BATTLE_COM_ATTACK, 10)},
                              extra={"attack_rolls": {"player": hit()}})
        attack = next(e for e in result.events if e.participant_id == "player" and e.damage > 0)
        self.assertEqual(attack.damage, physical_base_damage(100, 45.5, 0))
        self.assertLess(result.events.index(attack), result.events.index(self.wild_events(result)[0]))

    def test_production_bridge_population_metadata_and_slot_gates(self):
        from tests.test_stoneage_attack_crazed_runtime import actor
        spawned = SimpleNamespace(participant=actor("enemy", "enemy", "enemy"),
                                  template=SimpleNamespace(skill_slot_ids=(541, 0, 0, 0, 0, 0, 0)))
        runtime = synthetic_population()
        kwargs = dict(skill_slot=0, target_slot=0, petskill_runtime=runtime,
                      fixed_strength=100, fixed_toughness=100, attack_power_before=80,
                      defense_power_before=90, packed_com3_before=0x2345)
        with patch("tools.stoneage_enemy_ai_wildviolent_bridge.EXPECTED_OPTION_SHA256", SYNTHETIC_HASHES):
            rows = validate_recovered25_wildviolent_population(runtime)
            self.assertEqual([row.skill_id for row in rows], [541, 652])
            selected = resolve_enemy_ai_wildviolent_submission(spawned, **kwargs)
            self.assertEqual((selected.setup.attack_power, selected.setup.defense_power), (195, 65))
            self.assertEqual(selected.setup.packed_com3 & 0xffff, 0x2345)
            for changes in ({"field": 2}, {"target": 1}, {"cost": 3}, {"illegal": 0},
                            {"option_bytes": SYNTHETIC_OPTIONS[541][:-1]}, {"function_name": "PETSKILL_AttackCrazed"}):
                with self.subTest(changes=changes), self.assertRaises(ValueError):
                    bad = replace(runtime, skills=runtime.skills | {541: replace(runtime.skills[541], **changes)})
                    resolve_enemy_ai_wildviolent_submission(spawned, **(kwargs | {"petskill_runtime": bad}))
            with self.assertRaises(ValueError):
                resolve_enemy_ai_wildviolent_submission(spawned, **(kwargs | {"skill_slot": 1}))
            with self.assertRaises(ValueError):
                validate_recovered25_wildviolent_population(replace(runtime, skills={541: runtime.skills[541]}))

    def test_no_target_consumes_count_but_no_hit_rng(self):
        # The count draw exists even with an empty opponent side. Neither
        # critical/damage/dodge nor retarget RNG is needed on this empty path.
        result = self.resolve(players={}, hits=(OrdinaryAttackRolls(None, None),) * 3)
        self.assertEqual(self.wild_events(result), ())

    def test_unused_hit_rng_is_rejected_on_live_dodge_and_terminated_paths(self):
        from tests.test_stoneage_attack_crazed_runtime import actor, hit
        for unused in ({"retarget_roll": 0}, {"guard_roll_1_100": 50},
                       {"minimum_damage_roll_0_1": 0}, {"ultimate_roll_1_100": 50}):
            with self.subTest(unused=unused), self.assertRaisesRegex(ValueError, "unused|unused death|when no"):
                self.resolve(hits=(replace(hit(), **unused), hit(), hit()))
        with self.assertRaisesRegex(ValueError, "unused WildViolentAttack hit RNG"):
            self.resolve(hits=(replace(hit(), dodge_roll_1_10000=1), hit(), hit()))
        with self.assertRaisesRegex(ValueError, "unused WildViolentAttack hit RNG"):
            self.resolve(enemy=actor("enemy", "enemy", "enemy", hp=1, quick=200), extra={
                "base_damage_react_state_by_participant_id": {"player": BaseDamageReactState(reflect=1)}})
        with self.assertRaisesRegex(ValueError, "unused WildViolentAttack hit RNG"):
            self.resolve(players={})

    def test_missing_actual_action_count_draw_is_rejected(self):
        with self.assertRaisesRegex(KeyError, "action-time rolls"):
            self.resolve(extra={"wildviolent_rolls_by_attack_id": {}})

    def test_verified_probe_checks_each_authoritative_slot(self):
        from tools.stoneage_recovered25_wildviolent_probe import verify_typed_slot_admission
        pets = synthetic_population()
        enemies = SimpleNamespace(templates={i: SimpleNamespace(skill_slot_ids=(0, 541, 0, 0, 0, 0, 0)) for i in range(7)})
        with patch("tools.stoneage_enemy_ai_wildviolent_bridge.EXPECTED_OPTION_SHA256", SYNTHETIC_HASHES):
            self.assertEqual(verify_typed_slot_admission(pets, enemies), 7)
            enemies.templates[0].skill_slot_ids = (541, 541, 0, 0, 0, 0, 0)
            with self.assertRaisesRegex(ValueError, "population drift"):
                verify_typed_slot_admission(pets, enemies)
            enemies.templates[0].skill_slot_ids = (0, 652, 0, 0, 0, 0, 0)
            with self.assertRaisesRegex(ValueError, "positive seven-slot"):
                verify_typed_slot_admission(pets, enemies)

    def test_prepared_weaken_and_callback_powers_restore_next_round(self):
        from tests.test_stoneage_attack_crazed_runtime import actor, hit
        from tests.test_stoneage_battle_state_model import session
        from tools.stoneage_battle_state_model import begin_persistent_battle, resolve_persistent_ordinary_round, participant_snapshot
        from tools.stoneage_nocast_runtime_state import NocastRoundOverlay, NocastParticipantRuntime, PreparedWeakenPowers
        player = actor("player", "player", "player", hp=10000, quick=100)
        enemy = actor("enemy", "enemy", "enemy", hp=10000, defense=100, quick=200)
        late = NocastRoundOverlay({
            "player": NocastParticipantRuntime(25, 25, 25, 25),
            "enemy": NocastParticipantRuntime(25, 25, 25, 25, weaken_counter=1,
                                             prepared_weaken_powers=PreparedWeakenPowers(80, 80, 160)),
        })
        state = begin_persistent_battle(session(player, (enemy,)), slots={"player": 0, "enemy": 10}, nocast_overlay=late)
        setup = synthetic_setup()
        submission = EnemyAiWildViolentSubmission("enemy", 0, 541, CALLBACK_NAME, 0, setup)
        common = dict(initiative_random_subtracts={"player": 0, "enemy": 0},
                      profiles={"player": BattleCombatProfile(100, 0, 0, 0, 0, 0), "enemy": BattleCombatProfile(200, 0, 0, 0, 0, 0)},
                      attack_rolls={}, defense_profile="newpower_70pct")
        result = resolve_persistent_ordinary_round(state,
            commands={"player": BattleCommand(BATTLE_COM_WAIT), "enemy": BattleCommand(BATTLE_COM_ATTACK, 0, setup.packed_com3)},
            wildviolent_submissions_by_participant_id={"enemy": submission},
            wildviolent_rolls_by_attack_id={"enemy": WildViolentRolls(3, (hit(),) * 3)},
            command_setup_effects_by_participant_id={"enemy": BattleCommandSetupEffects(attack_power=195, defense_power=65)}, **common)
        self.assertEqual(len(self.wild_events(result.round)), 3)
        after = result.after.nocast_overlay.runtime_by_participant_id["enemy"]
        self.assertEqual(after.weaken_counter, 0)
        self.assertIsNone(after.prepared_weaken_powers)
        snapshot = participant_snapshot(result.after, "enemy")
        self.assertEqual((snapshot.attack, snapshot.defense, snapshot.quick), (100, 100, 200))
        following = resolve_persistent_ordinary_round(result.after,
            commands={"player": BattleCommand(BATTLE_COM_WAIT), "enemy": BattleCommand(BATTLE_COM_WAIT)}, **common)
        self.assertEqual(self.wild_events(following.round), ())
        self.assertEqual(following.after.session.enemies[0].attack, 100)


if __name__=="__main__":
    unittest.main()
