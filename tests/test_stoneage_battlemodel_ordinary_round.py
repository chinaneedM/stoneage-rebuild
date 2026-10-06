"""Actual ordinary-loop status clocks, semantic dispatch and subsequent actors."""
from dataclasses import replace
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from tests.test_stoneage_battlemodel_admission import fixture, spawned
from tools import stoneage_enemy_ai_battlemodel_bridge as bridge
from tools.stoneage_battlemodel_reference_model import PROFILE_BIG5, PROFILE_UTF8
from tools.stoneage_battlemodel_hit_loop import BattleModelDraw
from tools.stoneage_battlemodel_physical_attackseq import (
    PHYSICAL_SCOPE_R1, BattleModelPhysicalContext, BattleModelPhysicalProfile,
)
from tools.stoneage_battlemodel_itemcrush_model import BattleModelItemCrushContext, EmptyEquipmentParticipant
from tools.stoneage_battlemodel_round_action import (
    BATTLEMODEL_LETHAL_PROFIT_SCOPE_R1,
    BATTLEMODEL_ORDINARY_SCOPE_R1,
    BATTLEMODEL_ULTIMATE_EXIT_SCOPE_R1,
    BattleModelRoundAction,
)
from tools.stoneage_battle_round_model import (
    BATTLE_COM_NONE, BATTLE_COM_ATTACK, BATTLE_COM_GUARD, BATTLE_COM_WAIT,
    BattleCommand, BattleCommandSetupEffects, BattleCombatProfile,
    OrdinaryAttackRolls, prepare_battle_round, resolve_ordinary_round,
    PROFIT_BOUNDARY_BATTLEMODEL_COMMAND_TAIL,
)
from tools.stoneage_battle_status_model import BaseBattleStatusRuntime, BaseBattleStatusState, BaseStatusTurnRolls
from tools.stoneage_battle_damage_react_model import BaseDamageReactState
from tools.stoneage_battle_guardian_model import GuardianRegistration
from tools.stoneage_singleplayer_battle import BattleParticipant
from tools.stoneage_battle_state_model import begin_persistent_battle, resolve_persistent_ordinary_round
from tests.test_stoneage_battle_state_model import session
from tools.stoneage_local_runtime_session_coordinator import LocalRuntimeSessionCoordinator, LocalRuntimeBattleContext


class OrdinaryBattleModelTests(unittest.TestCase):
    def setUp(self):
        self.runtime, identities = fixture()
        pin = patch.object(bridge, "EXPECTED_ROW_IDENTITIES", identities)
        pin.start()
        self.addCleanup(pin.stop)
        self.actors = {
            0: BattleParticipant("target", "player", "player", 10, 500, 500, 100, 10, 40, None),
            10: BattleParticipant("enemy", "enemy", "enemy", 10, 500, 500, 100, 80, 60, None),
        }
        self.commands = {"target": BattleCommand(BATTLE_COM_ATTACK, 10), "enemy": BattleCommand(BATTLE_COM_NONE, 5)}
        self.status = {p.participant_id: BaseBattleStatusRuntime(work_quick=p.quick) for p in self.actors.values()}
        self.resistances = {s: 0 for s in self.actors}
        self.guardians = {}
        self.reactions = {}

    def tape(self, *, guard=False, status=True, failed=False, drunk=False, blocked_target=False):
        draws = []
        for i in range(4):
            if i:
                draws.append(BattleModelDraw(i, "target_selection", 0))
            if not blocked_target and not (guard and (not status or i == 0 or failed)) and (not status or i == 0 or failed):
                if drunk:
                    draws.append(BattleModelDraw(i, "attackseq_drunk_dodge", 20))
                draws.append(BattleModelDraw(i, "attackseq_dodge", 10000))
            draws += [BattleModelDraw(i, "attackseq_critical", 10000), BattleModelDraw(i, "attackseq_damage", 2)]
            if guard and (not status or i == 0 or failed):
                draws.append(BattleModelDraw(i, "attackseq_guard", 100))
            draws.append(BattleModelDraw(i, "itemcrush_check", 400000))
            if status and (i == 0 or failed):
                draws.append(BattleModelDraw(i, "status", 100 if failed else 1))
        return tuple(draws)

    def action(self, draws=None, charset=PROFILE_BIG5, actor_slot=10,
               scope=BATTLEMODEL_ORDINARY_SCOPE_R1):
        enemy = self.actors[actor_slot]
        source = spawned()
        source.participant.participant_id = enemy.participant_id
        submission = bridge.resolve_enemy_ai_battlemodel_submission(source, skill_slot=2,
            target_slot=5, petskill_runtime=self.runtime, profile=charset, source_profile="iris",
            powers_before=(enemy.attack, enemy.defense, enemy.quick))
        profiles = {s: BattleModelPhysicalProfile(p.participant_id, p.level, 100, 0, p.defense,
            self.status[p.participant_id].work_quick, (0, 0, 0, 0), fixed_vital=p.fixed_vital)
            for s, p in self.actors.items()}
        item = BattleModelItemCrushContext("iris", "legacy", 400000, 2147483647,
            {s: EmptyEquipmentParticipant(p.participant_id, p.kind, p.level, (-1,) * 5) for s, p in self.actors.items()})
        return BattleModelRoundAction(scope, submission,
            BattleModelPhysicalContext(PHYSICAL_SCOPE_R1, "newpower_70pct", profiles, self.guardians),
            item, tuple(s for s in self.actors if s < 10), self.resistances,
            self.tape() if draws is None else draws)

    def run_round(self, *, action=None, actions=None, order=None, draws=None, attack_rolls=None, status_rolls=None, **kwargs):
        action = action or self.action(draws)
        order = order or ("enemy", "target")
        prepared = prepare_battle_round(tuple(self.actors.values()), self.commands,
            {p.participant_id: 0 for p in self.actors.values()},
            action_value_overrides_by_participant_id={pid: 100-i for i, pid in enumerate(order)})
        actions = actions or {"enemy": action}
        return resolve_ordinary_round(prepared,
            slots={p.participant_id: s for s, p in self.actors.items()},
            profiles={p.participant_id: BattleCombatProfile(100, 0, 0, 0, 0, 0) for p in self.actors.values()},
            attack_rolls=attack_rolls or {}, defense_profile="newpower_70pct",
            base_status_runtime_by_participant_id=self.status,
            base_status_rolls_by_participant_id=status_rolls,
            base_damage_react_state_by_participant_id=self.reactions,
            guardian_registrations_by_defender_slot=self.guardians,
            command_setup_effects_by_participant_id={pid: BattleCommandSetupEffects(attack_power=a.submission.setup.powers[0]) for pid, a in actions.items()},
            battlemodel_actions_by_participant_id=actions, **kwargs)

    def loop(self, result):
        return next(e.battlemodel_loop_resolution for e in result.events if e.result == "battlemodel_action")

    def state_round(self, state, action):
        return resolve_persistent_ordinary_round(state,commands=self.commands,
            initiative_random_subtracts={p.participant_id:0 for p in self.actors.values()},
            profiles={p.participant_id:BattleCombatProfile(100,0,0,0,0,0) for p in self.actors.values()},
            attack_rolls={},defense_profile="newpower_70pct",
            command_setup_effects_by_participant_id={"enemy":BattleCommandSetupEffects(attack_power=action.submission.setup.powers[0])},
            battlemodel_actions_by_participant_id={"enemy":action})

    def persistent(self):
        return begin_persistent_battle(session(self.actors[0],(self.actors[10],)),
            slots={"target":0,"enemy":10},base_status_runtime_by_participant_id=self.status,
            base_damage_react_state_by_participant_id={p.participant_id:self.reactions.get(p.participant_id,BaseDamageReactState()) for p in self.actors.values()})

    def coordinator_round(self, context, action, runtime=None):
        coordinator=LocalRuntimeSessionCoordinator(SimpleNamespace(petskill_runtime=self.runtime if runtime is None else runtime),None)
        return coordinator.resolve_persistent_attack_wait_round(context,
            commands=self.commands,
            initiative_random_subtracts={
                p.participant_id:0 for p in self.actors.values()
            },
            profiles={
                p.participant_id:BattleCombatProfile(100,0,0,0,0,0)
                for p in self.actors.values()
            },
            attack_rolls={},defense_profile="newpower_70pct",
            tie_break_order=tuple(
                p.participant_id for p in self.actors.values()
            ),
            battlemodel_actions_by_participant_id={"enemy":action})

    def context(self):
        state=self.persistent()
        return LocalRuntimeBattleContext("control-contract","control-world",1,
            state.session.origin_position,frozenset(),"control-payload",state.session,
            (spawned(),),state)

    def test_battlemodel_records_one_command_tail_profit_boundary_after_all_hits(self):
        result=self.run_round()
        boundaries=[
            boundary for boundary in result.profit_boundaries
            if boundary.boundary_kind == PROFIT_BOUNDARY_BATTLEMODEL_COMMAND_TAIL
        ]
        self.assertEqual(len(boundaries),1)
        boundary=boundaries[0]
        self.assertEqual(boundary.hp_by_slot[0],372)
        self.assertEqual(
            dict(boundary.occupied_participant_id_by_slot),
            {0:"target",10:"enemy"},
        )
        self.assertEqual(dict(boundary.ultimate_kind_by_slot),{})
        self.assertEqual(boundary.prior_processed_death_ids,())
        trigger=[result.events[index] for index in boundary.trigger_event_indexes]
        self.assertEqual(trigger[-1].result,"battlemodel_action")
        self.assertTrue(all(event.battlemodel_skill_id==638 for event in trigger))
        self.assertEqual(
            len([event for event in trigger if event.result.startswith("battlemodel_")]),
            5,
        )

    def test_coordinator_readmits_and_returns_new_context_without_modifying_before(self):
        context=self.context()
        after,result=self.coordinator_round(context,self.action())
        self.assertIs(after.persistent_battle_state,result.after)
        self.assertEqual(after.persistent_battle_state.hp_by_participant_id["target"],372)
        self.assertEqual(context.persistent_battle_state.hp_by_participant_id["target"],500)
        self.assertEqual(after.persistent_state_payload,context.persistent_state_payload)
        self.assertEqual(after.spawned_enemies,context.spawned_enemies)

    def test_coordinator_template_or_loaded_skill_drift_rejects_before_commit(self):
        context=self.context()
        source=spawned(1179)
        wrong=replace(context,spawned_enemies=(source,))
        with self.assertRaisesRegex(ValueError,"template/work drift"):
            self.coordinator_round(wrong,self.action())
        rows=dict(self.runtime.skills)
        rows[638]=replace(rows[638],cost=4)
        with self.assertRaisesRegex(ValueError,"identity drift"):
            self.coordinator_round(context,self.action(),runtime=replace(self.runtime,skills=rows))
        self.assertEqual(context.persistent_battle_state.turn,0)

    def test_coordinator_cancellation_does_not_survive_fresh_second_round_guard(self):
        context,_=self.coordinator_round(self.context(),self.action())
        self.actors={s:replace(p,hp=context.persistent_battle_state.hp_by_participant_id[p.participant_id]) for s,p in self.actors.items()}
        self.status=dict(context.persistent_battle_state.base_status_runtime_by_participant_id)
        self.commands["target"]=BattleCommand(BATTLE_COM_GUARD)
        after,result=self.coordinator_round(context,self.action(self.tape(guard=True,status=False),charset=PROFILE_UTF8))
        self.assertEqual(after.persistent_battle_state.turn,2)
        self.assertTrue(any(e.result=="guard" for e in result.round.events))

    def test_coordinator_death_boundary_keeps_existing_context_and_payload(self):
        self.actors[0]=replace(self.actors[0],hp=1)
        context=self.context()
        draws=(BattleModelDraw(0,"attackseq_dodge",10000),BattleModelDraw(0,"attackseq_critical",10000),
               BattleModelDraw(0,"attackseq_damage",2),*(BattleModelDraw(i,"target_selection",0) for i in range(1,4)))
        with self.assertRaisesRegex(ValueError,"death requires"):
            self.coordinator_round(context,self.action(draws))
        self.assertEqual(context.persistent_battle_state.turn,0)
        self.assertEqual(context.persistent_battle_state.hp_by_participant_id["target"],1)
        self.assertEqual(context.persistent_state_payload,"control-payload")

    def test_persistent_transaction_commits_hp_status_and_reflection_charges(self):
        self.reactions["target"] = BaseDamageReactState(reflect=4)
        state = self.persistent()
        action = self.action(self.tape(blocked_target=True))
        result = self.state_round(state,action)
        self.assertEqual(result.after.turn,1)
        self.assertEqual(result.after.hp_by_participant_id["target"],500)
        self.assertEqual(result.after.base_damage_react_state_by_participant_id["target"].reflect,0)
        self.assertEqual(result.after.base_status_runtime_by_participant_id["target"].damage_count,4)
        self.assertEqual(result.after.pending_exp_by_participant_id,state.pending_exp_by_participant_id)
        self.assertIsNotNone(result.profit_scan_settlement)
        self.assertEqual(len(result.profit_scan_settlement.steps),1)
        self.assertEqual(
            result.profit_scan_settlement.steps[0].result.processed_death_ids,
            (),
        )
        self.assertEqual(state.base_damage_react_state_by_participant_id["target"].reflect,4)

    def test_persistent_next_preparation_takes_fresh_command_without_saved_cancellation(self):
        state = self.persistent()
        result = self.state_round(state,self.action())
        self.assertEqual(result.after.hp_by_participant_id["target"],372)
        self.assertEqual(result.after.base_status_runtime_by_participant_id["target"].status.paralysis,0)
        self.assertFalse(result.after.carried_commands_by_participant_id)
        self.actors = {s:replace(p,hp=result.after.hp_by_participant_id[p.participant_id]) for s,p in self.actors.items()}
        self.status = dict(result.after.base_status_runtime_by_participant_id)
        self.commands["target"] = BattleCommand(BATTLE_COM_GUARD)
        next_result = self.state_round(result.after,self.action(self.tape(guard=True,status=False),charset=PROFILE_UTF8))
        self.assertEqual(next_result.after.turn,2)
        self.assertTrue(any(e.result=="guard" for e in next_result.round.events))

    def test_persistent_death_rejection_preserves_entire_before_state(self):
        self.actors[0] = replace(self.actors[0],hp=1)
        state = self.persistent()
        draws = (BattleModelDraw(0,"attackseq_dodge",10000),BattleModelDraw(0,"attackseq_critical",10000),
                 BattleModelDraw(0,"attackseq_damage",2),*(BattleModelDraw(i,"target_selection",0) for i in range(1,4)))
        with self.assertRaisesRegex(ValueError,"death requires"):
            self.state_round(state,self.action(draws))
        self.assertEqual(state.turn,0)
        self.assertEqual(state.hp_by_participant_id["target"],1)
        self.assertEqual(state.pending_exp_by_participant_id["target"],0)

    def test_lethal638_persistent_normal_death_commits_command_tail_whole_scan(self):
        self.actors[0] = replace(self.actors[0],hp=1)
        state = self.persistent()
        draws = (
            BattleModelDraw(0,"attackseq_dodge",10000),
            BattleModelDraw(0,"attackseq_critical",10000),
            BattleModelDraw(0,"attackseq_damage",2),
            *(BattleModelDraw(i,"target_selection",0) for i in range(1,4)),
        )
        action=self.action(
            draws,
            scope=BATTLEMODEL_LETHAL_PROFIT_SCOPE_R1,
        )
        result=self.state_round(state,action)
        self.assertEqual(state.turn,0)
        self.assertEqual(state.hp_by_participant_id["target"],1)
        self.assertEqual(result.after.turn,1)
        self.assertEqual(result.after.hp_by_participant_id["target"],0)
        self.assertIsNotNone(result.profit_scan_settlement)
        self.assertEqual(len(result.profit_scan_settlement.steps),1)
        step=result.profit_scan_settlement.steps[0]
        self.assertEqual(step.result.processed_death_ids,("target",))
        self.assertEqual(
            result.after.profit_processed_death_ids,
            ("target",),
        )
        boundaries=[
            boundary for boundary in result.round.profit_boundaries
            if boundary.boundary_kind == PROFIT_BOUNDARY_BATTLEMODEL_COMMAND_TAIL
        ]
        self.assertEqual(len(boundaries),1)
        self.assertEqual(boundaries[0].hp_by_slot[0],0)
        trigger=[
            result.round.events[index]
            for index in boundaries[0].trigger_event_indexes
        ]
        self.assertEqual(trigger[-1].result,"battlemodel_action")
        self.assertTrue(all(event.battlemodel_skill_id==638 for event in trigger))

    def test_lethal638_coordinator_readmits_and_commits_without_mutating_before(self):
        self.actors[0]=replace(self.actors[0],hp=1)
        context=self.context()
        draws=(
            BattleModelDraw(0,"attackseq_dodge",10000),
            BattleModelDraw(0,"attackseq_critical",10000),
            BattleModelDraw(0,"attackseq_damage",2),
            *(BattleModelDraw(i,"target_selection",0) for i in range(1,4)),
        )
        action=self.action(
            draws,
            scope=BATTLEMODEL_LETHAL_PROFIT_SCOPE_R1,
        )
        after,result=self.coordinator_round(context,action)
        self.assertEqual(context.persistent_battle_state.turn,0)
        self.assertEqual(context.persistent_battle_state.hp_by_participant_id["target"],1)
        self.assertEqual(after.persistent_state_payload,context.persistent_state_payload)
        self.assertIs(after.persistent_battle_state,result.after)
        self.assertEqual(after.persistent_battle_state.hp_by_participant_id["target"],0)
        self.assertEqual(
            result.profit_scan_settlement.steps[0].result.processed_death_ids,
            ("target",),
        )

    def test_lethal638_persistent_player_ultimate_exits_at_command_tail(self):
        self.actors[0]=replace(self.actors[0],hp=10,max_hp=10)
        state=self.persistent()
        lethal_draws=(
            BattleModelDraw(0,"attackseq_dodge",10000),
            BattleModelDraw(0,"attackseq_critical",10000),
            BattleModelDraw(0,"attackseq_damage",2),
            *(BattleModelDraw(i,"target_selection",0) for i in range(1,4)),
        )
        action=self.action(lethal_draws,scope=BATTLEMODEL_ULTIMATE_EXIT_SCOPE_R1)
        result=self.state_round(state,action)
        self.assertEqual(state.hp_by_participant_id["target"],10)
        self.assertEqual(result.after.hp_by_participant_id["target"],1)
        self.assertEqual(
            result.round.ultimate_exited_participant_ids,
            ("target",),
        )
        self.assertNotIn(
            "target",
            result.after.profit_processed_death_ids,
        )
        boundaries=[
            boundary for boundary in result.round.profit_boundaries
            if boundary.boundary_kind == PROFIT_BOUNDARY_BATTLEMODEL_COMMAND_TAIL
        ]
        self.assertEqual(len(boundaries),1)
        self.assertEqual(boundaries[0].hp_by_slot[0],0)
        self.assertEqual(dict(boundaries[0].ultimate_kind_by_slot),{0:2})
        self.assertIsNotNone(result.profit_scan_settlement)
        self.assertEqual(len(result.profit_scan_settlement.steps),1)

    def test_lethal638_coordinator_player_ultimate_replays_current_identity(self):
        self.actors[0]=replace(self.actors[0],hp=10,max_hp=10)
        context=self.context()
        lethal_draws=(
            BattleModelDraw(0,"attackseq_dodge",10000),
            BattleModelDraw(0,"attackseq_critical",10000),
            BattleModelDraw(0,"attackseq_damage",2),
            *(BattleModelDraw(i,"target_selection",0) for i in range(1,4)),
        )
        action=self.action(lethal_draws,scope=BATTLEMODEL_ULTIMATE_EXIT_SCOPE_R1)
        after,result=self.coordinator_round(context,action)
        self.assertEqual(context.persistent_battle_state.hp_by_participant_id["target"],10)
        self.assertEqual(after.persistent_battle_state.hp_by_participant_id["target"],1)
        self.assertEqual(
            result.round.ultimate_exited_participant_ids,
            ("target",),
        )
        boundary=next(
            boundary for boundary in result.round.profit_boundaries
            if boundary.boundary_kind == PROFIT_BOUNDARY_BATTLEMODEL_COMMAND_TAIL
        )
        self.assertEqual(dict(boundary.ultimate_kind_by_slot),{0:2})
        self.assertEqual(after.persistent_state_payload,context.persistent_state_payload)

    def test_lethal638_guardian_pet_hit_first_but_owner_exit_scans_first(self):
        self.actors[0]=replace(self.actors[0],hp=10,max_hp=10)
        self.actors[5]=replace(
            self.actors[0],
            participant_id="guardian",
            kind="pet",
            source_pet_slot=0,
        )
        self.commands["guardian"]=BattleCommand(BATTLE_COM_WAIT)
        self.status["guardian"]=BaseBattleStatusRuntime(work_quick=40)
        self.resistances[5]=0
        self.guardians={0:GuardianRegistration(5)}
        state=begin_persistent_battle(
            session(self.actors[0],(self.actors[10],),(self.actors[5],)),
            slots={"target":0,"guardian":5,"enemy":10},
            default_pet_slot=0,
            base_status_runtime_by_participant_id=self.status,
        )
        draws=(
            BattleModelDraw(0,"attackseq_dodge",10000),
            BattleModelDraw(0,"attackseq_critical",10000),
            BattleModelDraw(0,"attackseq_damage",2),
            BattleModelDraw(2,"target_selection",0),
            BattleModelDraw(2,"attackseq_dodge",10000),
            BattleModelDraw(2,"attackseq_critical",10000),
            BattleModelDraw(2,"attackseq_damage",2),
            BattleModelDraw(3,"target_selection",0),
        )
        action=replace(
            self.action(draws,scope=BATTLEMODEL_ULTIMATE_EXIT_SCOPE_R1),
            opposing_slot_order=(0,5),
        )
        result=resolve_persistent_ordinary_round(
            state,
            commands=self.commands,
            initiative_random_subtracts={
                p.participant_id:0 for p in self.actors.values()
            },
            profiles={
                p.participant_id:BattleCombatProfile(100,0,0,0,0,0)
                for p in self.actors.values()
            },
            attack_rolls={},
            defense_profile="newpower_70pct",
            command_setup_effects_by_participant_id={
                "enemy":BattleCommandSetupEffects(
                    attack_power=action.submission.setup.powers[0]
                )
            },
            guardian_registrations_by_defender_slot=self.guardians,
            tie_break_order=tuple(
                p.participant_id for p in self.actors.values()
            ),
            battlemodel_actions_by_participant_id={"enemy":action},
        )
        loop=self.loop(result.round)
        damaged=[
            event for event in loop.events
            if event.actual_defender_slot is not None and event.hp_loss > 0
        ]
        self.assertEqual(
            [event.actual_defender_slot for event in damaged],
            [5,0],
        )
        boundary=next(
            boundary for boundary in result.round.profit_boundaries
            if boundary.boundary_kind == PROFIT_BOUNDARY_BATTLEMODEL_COMMAND_TAIL
        )
        self.assertEqual(boundary.hp_by_slot[0],0)
        self.assertEqual(boundary.hp_by_slot[5],0)
        self.assertEqual(dict(boundary.ultimate_kind_by_slot),{0:2,5:2})
        # Damage occurred pet5 -> owner0, but source AddProfit scans slot0 first.
        # Player Exit therefore owns the pet cleanup before slot5 can perform a
        # separate pet-ultimate selection clear.
        self.assertEqual(
            result.round.ultimate_exited_participant_ids,
            ("target","guardian"),
        )
        self.assertEqual(result.after.default_pet_slot,0)
        self.assertEqual(result.after.hp_by_participant_id["target"],1)
        self.assertEqual(result.after.hp_by_participant_id["guardian"],1)
        self.assertNotIn("target",result.after.profit_processed_death_ids)
        self.assertNotIn("guardian",result.after.profit_processed_death_ids)

    def test_lethal638_guardian_owner_first_exit_replays_through_coordinator(self):
        self.actors[0]=replace(self.actors[0],hp=10,max_hp=10)
        self.actors[5]=replace(
            self.actors[0],
            participant_id="guardian",
            kind="pet",
            source_pet_slot=0,
        )
        self.commands["guardian"]=BattleCommand(BATTLE_COM_WAIT)
        self.status["guardian"]=BaseBattleStatusRuntime(work_quick=40)
        self.resistances[5]=0
        self.guardians={0:GuardianRegistration(5)}
        state=begin_persistent_battle(
            session(self.actors[0],(self.actors[10],),(self.actors[5],)),
            slots={"target":0,"guardian":5,"enemy":10},
            default_pet_slot=0,
            base_status_runtime_by_participant_id=self.status,
        )
        context=LocalRuntimeBattleContext(
            "control-contract","control-world",1,
            state.session.origin_position,frozenset(),
            "control-payload",state.session,(spawned(),),state,
        )
        draws=(
            BattleModelDraw(0,"attackseq_dodge",10000),
            BattleModelDraw(0,"attackseq_critical",10000),
            BattleModelDraw(0,"attackseq_damage",2),
            BattleModelDraw(2,"target_selection",0),
            BattleModelDraw(2,"attackseq_dodge",10000),
            BattleModelDraw(2,"attackseq_critical",10000),
            BattleModelDraw(2,"attackseq_damage",2),
            BattleModelDraw(3,"target_selection",0),
        )
        action=replace(
            self.action(draws,scope=BATTLEMODEL_ULTIMATE_EXIT_SCOPE_R1),
            opposing_slot_order=(0,5),
        )
        after,result=self.coordinator_round(context,action)
        self.assertEqual(
            result.round.ultimate_exited_participant_ids,
            ("target","guardian"),
        )
        self.assertEqual(after.persistent_battle_state.default_pet_slot,0)
        self.assertEqual(after.persistent_battle_state.hp_by_participant_id["target"],1)
        self.assertEqual(after.persistent_battle_state.hp_by_participant_id["guardian"],1)
        self.assertEqual(context.persistent_battle_state.hp_by_participant_id["target"],10)
        self.assertEqual(context.persistent_battle_state.hp_by_participant_id["guardian"],10)

    def test_success_cancels_later_prepared_attack_in_actual_same_round(self):
        result = self.run_round()
        self.assertEqual(result.action_order, ("enemy", "target"))
        self.assertEqual(result.hp_by_participant_id, {"target": 372, "enemy": 500})
        self.assertEqual(result.battlemodel_cleared_command_ids, ("target",))
        self.assertEqual(result.base_status_runtime_by_participant_id["target"].status.paralysis, 0)
        self.assertEqual([e.result for e in result.events].count("status_tick"), 1)
        self.assertTrue(any(e.participant_id == "target" and e.result == "status_no_action" for e in result.events))
        self.assertEqual(self.loop(result).draws_consumed, self.tape())

    def test_prepared_guard_clears_after_first_hit_before_later_hits(self):
        self.commands["target"] = BattleCommand(BATTLE_COM_GUARD)
        result = self.run_round(draws=self.tape(guard=True))
        self.assertEqual([e.reported_damage for e in self.loop(result).events], [16, 32, 32, 32])
        self.assertFalse(any(e.result == "guard" for e in result.events))

    def test_actor_paralysis_one_expires_but_prepared_semantic_action_stays_cancelled(self):
        self.commands["target"] = BattleCommand(BATTLE_COM_WAIT)
        self.status["enemy"] = replace(self.status["enemy"], status=BaseBattleStatusState(paralysis=1))
        result = self.run_round(draws=())
        self.assertEqual(result.base_status_runtime_by_participant_id["enemy"].status.paralysis, 0)
        self.assertFalse(any(e.battlemodel_skill_id is not None for e in result.events))
        self.assertEqual(result.hp_by_participant_id["target"], 500)

    def test_suppressed_actor_with_action_draws_fails_unused_rng(self):
        self.commands["target"] = BattleCommand(BATTLE_COM_WAIT)
        self.status["enemy"] = replace(self.status["enemy"], status=BaseBattleStatusState(sleep=2))
        with self.assertRaisesRegex(ValueError, "unused BattleModel RNG"):
            self.run_round()
        self.assertEqual(self.status["enemy"].status.sleep, 2)

    def test_confusion_rewrites_to_real_ordinary_attack_and_owns_no_skill_draws(self):
        self.commands["target"] = BattleCommand(BATTLE_COM_WAIT)
        self.status["enemy"] = replace(self.status["enemy"], status=BaseBattleStatusState(confusion=2))
        result = self.run_round(draws=(), status_rolls={"enemy": BaseStatusTurnRolls(1, 0, 9)},
            attack_rolls={"enemy": OrdinaryAttackRolls(10000, 0, 10000)})
        self.assertEqual(sum(e.result == "normal" for e in result.events), 1)
        self.assertFalse(any(e.battlemodel_skill_id is not None for e in result.events))
        self.assertLess(result.hp_by_participant_id["target"], 500)

    def test_confusion_without_rewrite_preserves_skill_and_ticks_once(self):
        self.status["enemy"] = replace(self.status["enemy"], status=BaseBattleStatusState(confusion=2))
        result = self.run_round(status_rolls={"enemy": BaseStatusTurnRolls(100)})
        self.assertEqual(result.base_status_runtime_by_participant_id["enemy"].status.confusion, 1)
        self.assertEqual(sum(e.participant_id == "enemy" and e.result == "status_tick" for e in result.events), 1)
        self.assertEqual(len(self.loop(result).events), 4)

    def test_drunk_expiry_uses_current_work_quick_without_reordering_prepared_actions(self):
        self.actors[10] = replace(self.actors[10], quick=30)
        self.status["enemy"] = BaseBattleStatusRuntime(status=BaseBattleStatusState(drunk=1), work_quick=30)
        result = self.run_round()
        self.assertEqual(result.action_order, ("enemy", "target"))
        self.assertEqual(result.base_status_runtime_by_participant_id["enemy"].work_quick, 60)
        self.assertEqual(self.loop(result).entries[10].status_runtime.status.drunk, 0)
        self.assertFalse(any(d.owner == "attackseq_drunk_dodge" for d in self.loop(result).draws_consumed))

    def test_drunk_surviving_tick_draw_precedes_dodge(self):
        self.status["enemy"] = replace(self.status["enemy"], status=BaseBattleStatusState(drunk=2))
        result = self.run_round(draws=self.tape(drunk=True))
        consumed = self.loop(result).draws_consumed
        self.assertEqual([d.owner for d in consumed[:2]], ["attackseq_drunk_dodge", "attackseq_dodge"])
        self.assertEqual(self.loop(result).entries[10].status_runtime.status.drunk, 1)

    def test_poison_tick_hp_reaches_skill_snapshot_once(self):
        self.status["enemy"] = replace(self.status["enemy"], status=BaseBattleStatusState(poison=2), poison_stat_sum=2800)
        result = self.run_round()
        self.assertEqual(result.hp_by_participant_id["enemy"], 498)
        self.assertEqual(self.loop(result).entries[10].hp, 498)
        self.assertEqual(result.base_status_runtime_by_participant_id["enemy"].status.poison, 1)

    def test_preceding_actor_damage_reaches_dynamic_skill_actor_hp(self):
        result = self.run_round(order=("target", "enemy"),
            attack_rolls={"target": OrdinaryAttackRolls(10000, 0, 10000)})
        self.assertLess(self.loop(result).entries[10].hp, 500)
        self.assertEqual(sum(e.participant_id == "target" and e.result == "normal" for e in result.events), 1)
        # Target already acted: new one-turn paralysis is not decremented again.
        self.assertEqual(result.base_status_runtime_by_participant_id["target"].status.paralysis, 1)

    def test_failed_status_allows_later_real_attack(self):
        result = self.run_round(draws=self.tape(failed=True),
            attack_rolls={"target": OrdinaryAttackRolls(10000, 0, 10000)})
        self.assertFalse(result.battlemodel_cleared_command_ids)
        self.assertLess(result.hp_by_participant_id["enemy"], 500)

    def test_reflection_wakeup_status_and_charges_propagate(self):
        self.status["target"] = replace(self.status["target"], status=BaseBattleStatusState(sleep=2))
        self.reactions["target"] = BaseDamageReactState(reflect=4)
        result = self.run_round(draws=self.tape(blocked_target=True))
        self.assertEqual(result.hp_by_participant_id["target"], 500)
        self.assertEqual(result.base_damage_react_state_by_participant_id["target"].reflect, 0)
        self.assertEqual(result.base_status_runtime_by_participant_id["target"].damage_count, 4)

    def test_utf8_unknown_status_profile_does_not_cancel_prepared_action(self):
        self.actors[0] = replace(self.actors[0], hp=1000, max_hp=1000)
        action = self.action(self.tape(status=False), charset=PROFILE_UTF8)
        result = self.run_round(action=action, attack_rolls={"target": OrdinaryAttackRolls(10000, 0, 10000)})
        self.assertFalse(result.battlemodel_cleared_command_ids)
        self.assertIsNone(self.loop(result).events[0].status_application)

    def test_fresh_next_round_command_not_permanently_cancelled(self):
        result = self.run_round()
        self.actors = {s: replace(p, hp=result.hp_by_participant_id[p.participant_id]) for s, p in self.actors.items()}
        self.status = dict(result.base_status_runtime_by_participant_id)
        self.commands["target"] = BattleCommand(BATTLE_COM_GUARD)
        next_result = self.run_round(action=self.action(self.tape(guard=True, status=False), charset=PROFILE_UTF8))
        self.assertTrue(any(e.result == "guard" for e in next_result.events))
        self.assertFalse(next_result.battlemodel_cleared_command_ids)

    def test_two_semantic_actors_read_status_after_intervening_target_tick(self):
        self.actors[0] = replace(self.actors[0], hp=1000, max_hp=1000)
        self.actors[11] = replace(self.actors[10], participant_id="enemy2")
        self.commands["enemy2"] = BattleCommand(BATTLE_COM_NONE, 5)
        self.status["enemy2"] = BaseBattleStatusRuntime(work_quick=60)
        self.resistances[11] = 0
        actions = {"enemy": self.action(), "enemy2": self.action(actor_slot=11)}
        result = self.run_round(actions=actions, order=("enemy", "target", "enemy2"))
        loops = [e.battlemodel_loop_resolution for e in result.events if e.result == "battlemodel_action"]
        self.assertEqual(len(loops), 2)
        self.assertEqual(result.hp_by_participant_id["target"], 744)
        self.assertEqual(result.base_status_runtime_by_participant_id["target"].status.paralysis, 1)
        self.assertEqual(result.battlemodel_cleared_command_ids, ("target",))
        self.assertEqual(loops[1].draws_consumed[0].owner, "attackseq_dodge")

    def test_incomplete_actor_ticks_nothing_and_accepts_empty_action_rng(self):
        self.commands["enemy"] = BattleCommand(BATTLE_COM_NONE, 5, input_complete=False)
        self.commands["target"] = BattleCommand(BATTLE_COM_WAIT)
        self.status["enemy"] = replace(self.status["enemy"], status=BaseBattleStatusState(poison=2))
        result = self.run_round(draws=())
        self.assertEqual(result.base_status_runtime_by_participant_id["enemy"].status.poison, 2)
        self.assertTrue(any(e.result == "skipped_incomplete" for e in result.events))

    def test_no_living_opposition_emits_no_target_without_rng(self):
        self.actors[0] = replace(self.actors[0], hp=0)
        result = self.run_round(draws=())
        self.assertTrue(any(e.result == "battlemodel_no_target" for e in result.events))
        with self.assertRaisesRegex(ValueError, "no-target"):
            self.run_round()

    def test_guardian_changes_actual_recipient_and_later_command(self):
        self.actors[5] = replace(self.actors[0], participant_id="guardian", kind="pet")
        self.commands["guardian"] = BattleCommand(BATTLE_COM_ATTACK, 10)
        self.status["guardian"] = BaseBattleStatusRuntime(work_quick=40)
        self.resistances[5] = 0
        self.resistances[0] = 100
        self.guardians = {0: GuardianRegistration(5)}
        draws = []
        for i in range(4):
            if i >= 2:
                draws.append(BattleModelDraw(i, "target_selection", 0))
            if i == 0 or i >= 2:
                draws.append(BattleModelDraw(i, "attackseq_dodge", 10000))
            draws += [BattleModelDraw(i, "attackseq_critical", 10000), BattleModelDraw(i, "attackseq_damage", 2)]
            if i == 0:
                draws.append(BattleModelDraw(i, "status", 1))
            if i >= 2:
                draws += [BattleModelDraw(i, "itemcrush_check", 400000), BattleModelDraw(i, "status", 100)]
        result = self.run_round(draws=tuple(draws), order=("enemy", "target", "guardian"),
            attack_rolls={"target": OrdinaryAttackRolls(10000, 0, 10000)})
        self.assertEqual(result.battlemodel_cleared_command_ids, ("guardian",))
        self.assertEqual([e.actual_defender_slot for e in self.loop(result).events], [5, 5, 0, 0])
        self.assertFalse(any(e.participant_id == "guardian" and e.result == "normal" for e in result.events))

    def test_death_and_ultimate_leave_input_uncommitted(self):
        self.actors[0] = replace(self.actors[0], hp=1)
        draws = (BattleModelDraw(0, "attackseq_dodge", 10000), BattleModelDraw(0, "attackseq_critical", 10000),
                 BattleModelDraw(0, "attackseq_damage", 2), *(BattleModelDraw(i, "target_selection", 0) for i in range(1, 4)))
        with self.assertRaisesRegex(ValueError, "death requires"):
            self.run_round(draws=draws)
        self.assertEqual(self.actors[0].hp, 1)
        self.assertEqual(self.status["target"].status.paralysis, 0)

    def test_later_ordinary_death_stays_outside_both_battlemodel_scopes(self):
        # Kill the 500-HP enemy through the later ordinary attack without
        # crossing the source maxHP*1.2+20 ultimate threshold. With the fixed
        # no-element/newpower profile and damage_roll=0, attack=320 settles
        # above 500 but below the direct-ultimate boundary.
        self.actors[0] = replace(self.actors[0], attack=320)
        for scope in (
            BATTLEMODEL_ORDINARY_SCOPE_R1,
            BATTLEMODEL_LETHAL_PROFIT_SCOPE_R1,
        ):
            with self.subTest(scope=scope), self.assertRaisesRegex(
                ValueError, "excludes death outside"
            ):
                self.run_round(
                    action=self.action(self.tape(failed=True),scope=scope),
                    attack_rolls={
                        "target": OrdinaryAttackRolls(10000,0,10000)
                    },
                )
        self.assertEqual(self.actors[10].hp,500)

    def test_reflected_living_ultimate_flag_is_rejected_in_all_scopes(self):
        self.actors[0] = replace(self.actors[0], hp=10, max_hp=10)
        self.reactions["target"] = BaseDamageReactState(reflect=4)
        for scope in (
            BATTLEMODEL_ORDINARY_SCOPE_R1,
            BATTLEMODEL_LETHAL_PROFIT_SCOPE_R1,
        ):
            with self.subTest(scope=scope), self.assertRaisesRegex(
                ValueError, "ultimate flags"
            ):
                self.run_round(
                    action=self.action(
                        self.tape(blocked_target=True),
                        scope=scope,
                    )
                )
        with self.assertRaisesRegex(ValueError, "newly lethal ultimate flag"):
            self.run_round(
                action=self.action(
                    self.tape(blocked_target=True),
                    scope=BATTLEMODEL_ULTIMATE_EXIT_SCOPE_R1,
                )
            )
        self.assertEqual(self.actors[0].hp,10)

    def test_nonempty_counter_opt_in_is_rejected_for_bounded_composition(self):
        with self.assertRaisesRegex(ValueError, "counter"):
            self.run_round(counter_rolls_by_attack_id={})

    def test_draw_tuple_resistances_and_scope_are_strict_and_immutable(self):
        action = self.action()
        with self.assertRaises(ValueError):
            replace(action, scope="ordinary")
        with self.assertRaises(ValueError):
            replace(action, paralysis_resistance_by_slot={0: True})
        with self.assertRaises(TypeError):
            replace(action, draws=list(action.draws))
        self.resistances.clear()
        self.assertEqual(action.paralysis_resistance_by_slot[0], 0)
        with self.assertRaises(TypeError):
            action.paralysis_resistance_by_slot[0] = 1

    def test_binding_coverage_carrier_profiles_and_rng_order_fail_closed(self):
        action = self.action()
        cases = [replace(action, opposing_slot_order=()),
                 replace(action, paralysis_resistance_by_slot={0: 0}),
                 replace(action, physical_context=replace(action.physical_context,
                    profiles={**action.physical_context.profiles, 0: replace(action.physical_context.profiles[0], level=11)}))]
        for case in cases:
            with self.subTest(case=case), self.assertRaises(ValueError):
                self.run_round(action=case)
        draws = list(action.draws)
        draws[3], draws[4] = draws[4], draws[3]
        with self.assertRaisesRegex(ValueError, "chronology/owner"):
            self.run_round(action=replace(action, draws=tuple(draws)))
        self.commands["enemy"] = BattleCommand(BATTLE_COM_ATTACK, 5)
        with self.assertRaisesRegex(ValueError, "carrier"):
            self.run_round(action=action)


if __name__ == "__main__":
    unittest.main()
