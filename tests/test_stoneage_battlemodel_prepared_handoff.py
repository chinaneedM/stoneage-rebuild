"""Current-work handoff and real ordinary continuation cancellation witnesses."""
from dataclasses import replace
import unittest
from unittest.mock import patch

from tests.test_stoneage_battlemodel_admission import fixture, spawned
from tools import stoneage_enemy_ai_battlemodel_bridge as bridge
from tools.stoneage_battlemodel_reference_model import PROFILE_BIG5, PROFILE_UTF8
from tools.stoneage_battlemodel_hit_loop import BattleModelEntry, BattleModelDraw
from tools.stoneage_battlemodel_physical_attackseq import (
    PHYSICAL_SCOPE_R1, BattleModelPhysicalProfile, BattleModelPhysicalContext,
)
from tools.stoneage_battlemodel_itemcrush_model import (
    BattleModelItemCrushContext, EmptyEquipmentParticipant,
)
from tools.stoneage_battlemodel_prepared_handoff import (
    PREPARED_HANDOFF_SCOPE_R1, execute_battlemodel_prepared_handoff,
    reset_battlemodel_round_flags,
)
from tools.stoneage_battle_round_model import (
    BATTLE_COM_ATTACK, BATTLE_COM_GUARD, BATTLE_COM_NONE, BATTLE_COM_WAIT,
    BATTLE_COM_COMBO, BattleCommand, BattleCombatProfile, prepare_battle_round,
    resolve_ordinary_round, OrdinaryAttackRolls,
)
from tools.stoneage_battle_status_model import BaseBattleStatusRuntime, BaseBattleStatusState
from tools.stoneage_battle_damage_react_model import BaseDamageReactState
from tools.stoneage_battle_guardian_model import GuardianRegistration
from tools.stoneage_singleplayer_battle import BattleParticipant


class PreparedHandoffTests(unittest.TestCase):
    def setUp(self):
        self.runtime, identities = fixture()
        pin = patch.object(bridge, "EXPECTED_ROW_IDENTITIES", identities)
        pin.start()
        self.addCleanup(pin.stop)
        self.entries = {0: BattleModelEntry("target", "player", 500, 500, 0),
                        10: BattleModelEntry("enemy", "enemy", 500, 500, 0)}
        self.profiles = {
            0: BattleModelPhysicalProfile("target", 10, 100, 0, 10, 40, (0, 0, 0, 0), no_dodge=True),
            10: BattleModelPhysicalProfile("enemy", 10, 100, 0, 80, 60, (0, 0, 0, 0)),
        }
        self.commands = {"target": BattleCommand(BATTLE_COM_ATTACK, 10, 73),
                         "enemy": BattleCommand(BATTLE_COM_NONE)}

    def prepared(self, order=("enemy", "target")):
        actors = tuple(BattleParticipant(e.participant_id, "player" if s < 10 else "enemy",
            e.kind, 10, e.hp, e.max_hp, 100, self.profiles[s].defense_power,
            self.profiles[s].quick, None) for s, e in self.entries.items())
        return prepare_battle_round(actors, self.commands, {e.participant_id: 0 for e in self.entries.values()},
            action_value_overrides_by_participant_id={pid: 100 - i for i, pid in enumerate(order)})

    def tape(self, *, guard=False, status=True, item=True):
        draws = []
        for i in range(4):
            if i:
                draws.append(BattleModelDraw(i, "target_selection", 0))
            draws += [BattleModelDraw(i, "attackseq_critical", 10000), BattleModelDraw(i, "attackseq_damage", 2)]
            if guard and (not status or i == 0):
                draws.append(BattleModelDraw(i, "attackseq_guard", 100))
            if item:
                draws.append(BattleModelDraw(i, "itemcrush_check", 400000))
            if status and i == 0:
                draws.append(BattleModelDraw(i, "status", 1))
        return tuple(draws)

    def execute(self, draws=None, **kwargs):
        charset = kwargs.pop("charset", PROFILE_BIG5)
        submission = bridge.resolve_enemy_ai_battlemodel_submission(spawned(), skill_slot=2,
            target_slot=5, petskill_runtime=self.runtime, profile=charset, source_profile="iris",
            powers_before=(100, 80, 60))
        context = BattleModelPhysicalContext(PHYSICAL_SCOPE_R1, "newpower_70pct",
            self.profiles, kwargs.pop("guardians", {}))
        item = BattleModelItemCrushContext("iris", "legacy", 400000, 2147483647,
            {s: EmptyEquipmentParticipant(e.participant_id, e.kind, 10, (-1,) * 5)
             for s, e in self.entries.items()})
        return execute_battlemodel_prepared_handoff(kwargs.pop("prepared", self.prepared()), submission,
            scope=kwargs.pop("scope", PREPARED_HANDOFF_SCOPE_R1),
            slots=kwargs.pop("slots", {e.participant_id: s for s, e in self.entries.items()}),
            entries=self.entries, completed_prefix=kwargs.pop("completed_prefix", ()),
            initial_living_slots=(0,), draws=self.tape() if draws is None else draws,
            physical_context=context, itemcrush_context=item,
            source_pet_guard_flags=kwargs.pop("flags", tuple(self.entries[s].ultimate_flag if s in self.entries else False for s in range(20))),
            **kwargs)

    def continue_ordinary(self, handoff, attack_rolls=None):
        return resolve_ordinary_round(handoff.ordinary_continuation(), slots=handoff.slots,
            profiles={pid: BattleCombatProfile(100, 0, 0, 0, 0, 0) for pid in handoff.slots},
            attack_rolls=attack_rolls or {}, defense_profile="newpower_70pct",
            base_status_runtime_by_participant_id=handoff.status_runtime_by_participant_id,
            base_damage_react_state_by_participant_id=handoff.reaction_by_participant_id,
            ultimate_overkill_by_participant_id=handoff.overkill_by_participant_id)

    def test_success_cancels_real_prepared_attack_after_paralysis_expires(self):
        handoff = self.execute()
        self.assertEqual(handoff.commands_by_participant_id["target"], BattleCommand(BATTLE_COM_NONE, 10, 73))
        self.assertEqual(handoff.completed_prefix, ("enemy",))
        self.assertEqual(handoff.entries[0].hp, 372)
        result = self.continue_ordinary(handoff)  # no attack RNG supplied
        self.assertEqual(result.hp_by_participant_id["enemy"], 500)
        self.assertEqual(result.base_status_runtime_by_participant_id["target"].status.paralysis, 0)
        self.assertFalse(any(e.participant_id == "target" and e.result == "normal" for e in result.events))
        self.assertEqual(sum(e.result == "status_tick" for e in result.events), 1)

    def test_prepared_guard_overrides_stale_physical_command_then_clears(self):
        self.commands["target"] = BattleCommand(BATTLE_COM_GUARD, 10, 73)
        before = self.prepared()
        handoff = self.execute(self.tape(guard=True), prepared=before)
        self.assertEqual([e.reported_damage for e in handoff.loop.events], [16, 32, 32, 32])
        self.assertEqual(handoff.guarding_slots, frozenset())
        self.assertEqual(self.profiles[0].command, "none")
        self.assertEqual(before.ordered_entries[1].command.command1, BATTLE_COM_GUARD)
        self.assertEqual(self.entries[0].hp, 500)

    def test_failed_application_preserves_prepared_attack_and_actual_continuation(self):
        draws = list(self.tape(status=False))
        for i in range(3, -1, -1):
            index = next(j for j, d in enumerate(draws) if d.ordinal == i and d.owner == "itemcrush_check")
            draws.insert(index + 1, BattleModelDraw(i, "status", 100))
        handoff = self.execute(tuple(draws))
        self.assertEqual(handoff.commands_by_participant_id["target"], self.commands["target"])
        result = self.continue_ordinary(handoff, {"target": OrdinaryAttackRolls(10000, 0, 10000)})
        self.assertLess(result.hp_by_participant_id["enemy"], 500)

    def test_already_executed_target_is_updated_but_never_replayed(self):
        prepared = self.prepared(("target", "enemy"))
        handoff = self.execute(prepared=prepared, completed_prefix=("target",))
        self.assertEqual(handoff.completed_prefix, ("target", "enemy"))
        continuation = handoff.ordinary_continuation()
        self.assertFalse(continuation.executable_entries)
        self.assertEqual(handoff.status_runtime_by_participant_id["target"].status.paralysis, 1)
        result = self.continue_ordinary(handoff)
        self.assertFalse(any(e.result == "status_tick" for e in result.events))

    def test_new_preparation_drops_only_round_flags_and_accepts_fresh_guard(self):
        handoff = self.execute()
        old = handoff.entries[0]
        old = replace(old, reaction=BaseDamageReactState(reflect=3), accumulated_overkill=17, ultimate_flag=True)
        reset = reset_battlemodel_round_flags({**handoff.entries, 0: old})
        self.assertEqual(reset[0], replace(old, command_cleared=False, ultimate_flag=False))
        self.entries = dict(reset)
        self.entries[0] = replace(self.entries[0], status_runtime=BaseBattleStatusRuntime())
        self.commands["target"] = BattleCommand(BATTLE_COM_GUARD)
        next_handoff = self.execute(self.tape(guard=True, status=False), charset=PROFILE_UTF8)
        self.assertEqual(next_handoff.guarding_slots, frozenset({0}))
        self.assertFalse(next_handoff.entries[0].command_cleared)

    def test_current_hp_not_initial_prepared_hp_drives_settlement_and_death(self):
        prepared = self.prepared()
        self.entries[0] = replace(self.entries[0], hp=1)
        draws = (BattleModelDraw(0, "attackseq_critical", 10000), BattleModelDraw(0, "attackseq_damage", 2),
                 *(BattleModelDraw(i, "target_selection", 0) for i in range(1, 4)))
        handoff = self.execute(draws, prepared=prepared)
        self.assertEqual(handoff.entries[0].hp, 0)
        self.assertEqual([e.outcome for e in handoff.loop.events][1:], ["skipped_target"] * 3)
        self.assertFalse(any(e.participant.participant_id == "target" for e in handoff.prepared.executable_entries))
        with self.assertRaisesRegex(ValueError, "death requires profit"):
            handoff.ordinary_continuation()

    def test_living_ultimate_flag_is_preserved_without_inventing_exit(self):
        self.entries[0] = replace(self.entries[0], ultimate_flag=True)
        handoff = self.execute()
        self.assertGreater(handoff.entries[0].hp, 0)
        self.assertTrue(handoff.source_pet_guard_flags[0])
        self.assertTrue(handoff.entries[0].target_check_allowed)
        with self.assertRaisesRegex(ValueError, "ultimate flags"):
            handoff.ordinary_continuation()

    def test_guardian_actual_recipient_updates_only_its_prepared_command(self):
        self.entries[5] = BattleModelEntry("guardian", "pet", 500, 500, 100)
        self.profiles[5] = replace(self.profiles[0], participant_id="guardian")
        self.commands["guardian"] = BattleCommand(BATTLE_COM_ATTACK, 10)
        prepared = self.prepared(("enemy", "target", "guardian"))
        # Guardian becomes paralyzed; original target has resisting failed rolls.
        self.entries[0] = replace(self.entries[0], paralysis_resistance=100)
        self.entries[5] = replace(self.entries[5], paralysis_resistance=0)
        draws = []
        for i in range(4):
            if i:
                draws.append(BattleModelDraw(i, "target_selection", 0))
            draws += [BattleModelDraw(i, "attackseq_critical", 10000), BattleModelDraw(i, "attackseq_damage", 2)]
            if i:
                draws.append(BattleModelDraw(i, "itemcrush_check", 400000))
            if i == 0:
                draws.append(BattleModelDraw(i, "status", 1))
            else:
                draws.append(BattleModelDraw(i, "status", 100))
        handoff = self.execute(tuple(draws), prepared=prepared, guardians={0: GuardianRegistration(5)})
        self.assertEqual([e.actual_defender_slot for e in handoff.loop.events], [5, 0, 0, 0])
        self.assertEqual(handoff.commands_by_participant_id["guardian"].command1, BATTLE_COM_NONE)
        self.assertEqual(handoff.commands_by_participant_id["target"].command1, BATTLE_COM_ATTACK)

    def test_reflection_reaction_and_damage_count_survive_handoff(self):
        self.entries[0] = replace(self.entries[0], reaction=BaseDamageReactState(reflect=4),
            status_runtime=BaseBattleStatusRuntime(status=BaseBattleStatusState(sleep=2)))
        handoff = self.execute()
        self.assertEqual(handoff.entries[0].hp, 500)
        self.assertEqual(handoff.reaction_by_participant_id["target"].reflect, 0)
        self.assertEqual(handoff.status_runtime_by_participant_id["target"].damage_count, 4)
        self.assertEqual(handoff.status_runtime_by_participant_id["target"].status.paralysis, 1)
        with self.assertRaises(TypeError):
            handoff.commands_by_participant_id["target"] = None

    def test_identity_prefix_scope_and_numeric_carrier_fail_closed(self):
        cases = [dict(scope="ordinary"), dict(completed_prefix=("target",)),
                 dict(completed_prefix=("enemy", "target")), dict(slots={"target": 1, "enemy": 10})]
        for case in cases:
            with self.subTest(case=case), self.assertRaises(ValueError):
                self.execute((), **case)
        self.commands["enemy"] = BattleCommand(BATTLE_COM_ATTACK, 0)
        with self.assertRaisesRegex(ValueError, "NONE carrier"):
            self.execute(())
        self.commands["enemy"] = BattleCommand(BATTLE_COM_NONE)
        self.commands["target"] = BattleCommand(BATTLE_COM_COMBO)
        with self.assertRaisesRegex(ValueError, "noncombo"):
            self.execute(())

    def test_status_or_cleared_or_incomplete_actor_requires_status_dispatch(self):
        for actor in (replace(self.entries[10], command_cleared=True),
                      replace(self.entries[10], hp=0),
                      replace(self.entries[10], status_runtime=BaseBattleStatusRuntime(status=BaseBattleStatusState(confusion=1)))):
            self.entries[10] = actor
            with self.assertRaisesRegex(ValueError, "not executable"):
                self.execute(())
        self.entries[10] = BattleModelEntry("enemy", "enemy", 500, 500, 0)
        self.commands["enemy"] = BattleCommand(BATTLE_COM_NONE, input_complete=False)
        with self.assertRaisesRegex(ValueError, "not executable"):
            self.execute(())

    def test_item_status_rng_order_still_fails_before_any_handoff_mutation(self):
        draws = list(self.tape())
        draws[2], draws[3] = draws[3], draws[2]
        with self.assertRaisesRegex(ValueError, "chronology/owner"):
            self.execute(tuple(draws))
        self.assertEqual(self.entries[0].hp, 500)
        self.assertEqual(self.commands["target"].command1, BATTLE_COM_ATTACK)


if __name__ == "__main__":
    unittest.main()
