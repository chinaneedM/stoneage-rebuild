"""Ordered seam witnesses; AttackSeq remains an explicit controlled dependency."""
from dataclasses import replace
import unittest
from unittest.mock import patch

from tests.test_stoneage_battlemodel_admission import fixture, spawned
from tools import stoneage_enemy_ai_battlemodel_bridge as bridge
from tools.stoneage_battlemodel_reference_model import PROFILE_BIG5, PROFILE_UTF8
from tools.stoneage_battlemodel_hit_loop import (
    BattleModelEntry, BattleModelDraw, BattleModelAttackSeqResult,
    execute_battlemodel_post_attackseq_loop, resolve_battlemodel_marker_settlement,
    HIT_LOOP_SCOPE_R1,
)
from tools.stoneage_battle_damage_react_model import (
    BaseDamageReactState, resolve_base_damage_react,
)
from tools.stoneage_battle_status_model import BaseBattleStatusRuntime, BaseBattleStatusState


class BattleModelHitLoopTests(unittest.TestCase):
    def setUp(self):
        self.runtime, identities = fixture()
        pin = patch.object(bridge, "EXPECTED_ROW_IDENTITIES", identities)
        pin.start()
        self.addCleanup(pin.stop)

    def submission(self, profile=PROFILE_UTF8):
        return bridge.resolve_enemy_ai_battlemodel_submission(
            spawned(), skill_slot=2, target_slot=5, petskill_runtime=self.runtime,
            profile=profile, source_profile="iris", powers_before=(100, 80, 60),
        )

    def entries(self, slots=(0,), hp=100, max_hp=200):
        result = {s: BattleModelEntry(f"target:{s}", "player", hp, max_hp, 0, marker=123)
                  for s in slots}
        result[10] = BattleModelEntry("enemy", "enemy", 150, 200, 0)
        return result

    def run_loop(self, entries=None, slots=(0,), draws=(), callback=None, profile=PROFILE_UTF8, **kwargs):
        return execute_battlemodel_post_attackseq_loop(
            self.submission(profile), actor_slot=10, entries=entries or self.entries(slots),
            execution_scope=kwargs.pop("execution_scope", HIT_LOOP_SCOPE_R1),
            initial_living_slots=slots, draws=draws,
            attack_sequence=callback or (lambda a, e, r: BattleModelAttackSeqResult("normal", 0)),
            **kwargs,
        )

    def test_count_and_action_cycling_match_independent_reference_for_all_pool_sizes(self):
        for n in (1, 2, 4, 5, 10):
            slots = tuple(range(n))
            selections = tuple(i % n for i in range(max(0, 4 - n)))
            draws = tuple(BattleModelDraw(n + i, "target_selection", v) for i, v in enumerate(selections))
            result = self.run_loop(slots=slots, draws=draws)
            plan = self.submission().target_plan(living_opposing_slots=slots, excess_target_rolls=selections)
            with self.subTest(n=n):
                self.assertEqual(tuple(e.attack for e in result.events), plan.attacks)
                self.assertEqual([e.ordinal for e in result.events], list(range(max(4, n))))
                self.assertEqual(result.draws_consumed, draws)
                self.assertEqual(result.initial_living_slots, slots)

    def test_selection_draws_follow_prior_hit_and_status_draws(self):
        draws = (
            BattleModelDraw(0, "attackseq_damage", 10), BattleModelDraw(0, "status", 20),
            BattleModelDraw(1, "attackseq_damage", 10), BattleModelDraw(1, "status", 20),
            BattleModelDraw(2, "target_selection", 1),
            BattleModelDraw(2, "attackseq_damage", 10), BattleModelDraw(2, "status", 20),
            BattleModelDraw(3, "target_selection", 0),
            BattleModelDraw(3, "attackseq_damage", 10), BattleModelDraw(3, "status", 20),
        )
        result = self.run_loop(slots=(0, 1), draws=draws, profile=PROFILE_BIG5,
            callback=lambda a, e, r: BattleModelAttackSeqResult("normal", r.take("attackseq_damage", 0, 100)))
        self.assertEqual([e.attack.target_slot for e in result.events], [0, 1, 1, 0])
        self.assertEqual(result.draws_consumed, draws)
        phases = [(t.phase, t.ordinal) for t in result.trace]
        self.assertLess(phases.index(("marker_restore", 1)), phases.index(("rng", 2)))
        self.assertEqual(result.entries[0].hp, 80)
        self.assertEqual(result.entries[1].hp, 80)
        # Strict roll<20 fails at20, despite caller input30.
        self.assertFalse(result.cleared_command_slots)

    def test_dead_sampled_targets_are_not_retargeted_and_still_consume_selection(self):
        original = self.entries((0, 1), hp=5)
        calls = []
        def attack(a, entries, rng):
            calls.append(a.target_slot)
            return BattleModelAttackSeqResult("normal", rng.take("attackseq_damage", 0, 100))
        draws = (BattleModelDraw(0, "attackseq_damage", 10),
                 BattleModelDraw(1, "attackseq_damage", 10),
                 BattleModelDraw(2, "target_selection", 0), BattleModelDraw(3, "target_selection", 1))
        result = self.run_loop(entries=original, slots=(0, 1), draws=draws, callback=attack)
        self.assertEqual(calls, [0, 1])
        self.assertEqual([e.outcome for e in result.events], ["normal", "normal", "skipped_target", "skipped_target"])
        self.assertEqual(result.draws_consumed, draws)
        self.assertEqual(original[0].hp, 5)  # immutable caller state

    def test_recycled_object_index_keeps_distinct_rng_ordinal(self):
        draws = tuple(BattleModelDraw(i, "attackseq_damage", i) for i in range(5))
        result = self.run_loop(slots=(0, 1, 2, 3, 4), draws=draws,
            callback=lambda a, e, r: BattleModelAttackSeqResult("normal", r.take("attackseq_damage", 0, 100)))
        self.assertEqual([e.attack.object_index for e in result.events], [0, 1, 2, 3, 0])
        self.assertEqual([e.ordinal for e in result.events], [0, 1, 2, 3, 4])
        self.assertEqual([e.attack.action_number for e in result.events], [7, 8, 7, 8, 7])

    def test_reflection_preserves_hp_reports_damage_and_can_wake_then_paralyze(self):
        entries = self.entries((0,), hp=100)
        entries[0] = replace(entries[0], reaction=BaseDamageReactState(reflect=4),
            status_runtime=BaseBattleStatusRuntime(status=BaseBattleStatusState(sleep=3)))
        draws = (BattleModelDraw(0, "status", 1),
                 BattleModelDraw(1, "target_selection", 0),
                 BattleModelDraw(2, "target_selection", 0), BattleModelDraw(3, "target_selection", 0))
        snapshots = []
        def attack(a, current, rng):
            snapshots.append(current[0])
            return BattleModelAttackSeqResult("normal", 30)
        result = self.run_loop(entries=entries, draws=draws, callback=attack, profile=PROFILE_BIG5)
        self.assertEqual((result.entries[10].hp, result.entries[0].hp), (150, 100))
        self.assertEqual(result.entries[0].reaction.reflect, 0)
        self.assertEqual([e.reported_damage for e in result.events], [30] * 4)
        self.assertEqual([e.hp_loss for e in result.events], [0] * 4)
        self.assertEqual(result.entries[0].status_runtime.status, BaseBattleStatusState(paralysis=1))
        self.assertEqual(result.cleared_command_slots, frozenset({0}))
        self.assertTrue(snapshots[1].command_cleared)
        self.assertEqual(result.entries[0].marker, 123)
        phases = [t.phase for t in result.trace if t.ordinal == 0]
        self.assertLess(phases.index("wakeup"), phases.index("command_clear"))

    def test_absorb_and_vanish_suppress_wake_but_not_surviving_status(self):
        for reaction, expected_hp in ((BaseDamageReactState(absorb=4), 200),
                                      (BaseDamageReactState(vanish=4), 100)):
            entries = self.entries((0,))
            entries[0] = replace(entries[0], reaction=reaction)
            draws = (BattleModelDraw(0, "status", 1),
                     *(BattleModelDraw(i, "target_selection", 0) for i in range(1, 4)))
            result = self.run_loop(entries=entries, draws=draws, profile=PROFILE_BIG5,
                callback=lambda a, e, r: BattleModelAttackSeqResult("normal", 30))
            with self.subTest(reaction=reaction):
                self.assertEqual(result.entries[0].hp, expected_hp)
                self.assertEqual(result.entries[0].status_runtime.damage_count, 0)
                self.assertEqual(result.entries[0].status_runtime.status.paralysis, 1)
                self.assertTrue(result.events[0].status_application.check.success)
        entries[0] = replace(entries[0], status_runtime=BaseBattleStatusRuntime(status=BaseBattleStatusState(sleep=2)))
        result = self.run_loop(entries=entries,
            draws=tuple(BattleModelDraw(i, "target_selection", 0) for i in range(1, 4)), profile=PROFILE_BIG5,
            callback=lambda a, e, r: BattleModelAttackSeqResult("normal", 30))
        self.assertEqual(result.entries[0].status_runtime.status.sleep, 2)

    def test_guardian_receives_damage_and_status_dead_candidate_is_cleared(self):
        entries = self.entries((0, 5), hp=100)
        entries[5] = replace(entries[5], kind="pet", reaction=BaseDamageReactState(vanish=4))
        draws = (BattleModelDraw(0, "status", 1), BattleModelDraw(2, "target_selection", 0),
                 BattleModelDraw(3, "target_selection", 0))
        result = self.run_loop(entries=entries, slots=(0, 5), draws=draws, profile=PROFILE_BIG5,
            source_pet_guard_flags=(False,) * 20,
            callback=lambda a, e, r: BattleModelAttackSeqResult("normal", 10, 5))
        self.assertEqual([e.actual_defender_slot for e in result.events], [5] * 4)
        self.assertEqual(result.cleared_command_slots, frozenset({5}))
        self.assertEqual(result.entries[0].status_runtime.status.paralysis, 0)
        entries[5] = replace(entries[5], hp=0)
        result = self.run_loop(entries=entries, slots=(0,),
            draws=tuple(BattleModelDraw(i, "target_selection", 0) for i in range(1, 4)),
            callback=lambda a, e, r: BattleModelAttackSeqResult("normal", 1, 5))
        self.assertEqual([e.actual_defender_slot for e in result.events], [0] * 4)
        self.assertEqual(result.entries[0].hp, 96)

    def test_ultimate_without_hp_loss_sets_flag_but_does_not_invent_exit(self):
        entries = self.entries((0,), hp=100, max_hp=100)
        entries[0] = replace(entries[0], reaction=BaseDamageReactState(reflect=4))
        result = self.run_loop(entries=entries,
            draws=tuple(BattleModelDraw(i, "target_selection", 0) for i in range(1, 4)),
            callback=lambda a, e, r: BattleModelAttackSeqResult("normal", 140))
        self.assertEqual([e.ultimate_kind for e in result.events], [2] * 4)
        self.assertTrue(result.entries[0].ultimate_flag)
        self.assertEqual(result.entries[0].hp, 100)
        self.assertTrue(result.entries[0].live_target)

    def test_pet_guard_reads_target_plus_five_and_requires_explicit_state(self):
        entries = self.entries((5,))
        entries[5] = replace(entries[5], kind="pet")
        # target5+5 is opposing entry10, not owner player0.
        entries[10] = replace(entries[10], ultimate_flag=True)
        flags = [False] * 20
        flags[10] = True
        result = self.run_loop(entries=entries, slots=(5,), source_pet_guard_flags=tuple(flags),
            draws=tuple(BattleModelDraw(i, "target_selection", 0) for i in range(1, 4)),
            callback=lambda a, e, r: self.fail("flag guard must run before AttackSeq"))
        self.assertEqual([e.outcome for e in result.events], ["skipped_source_pet_flag"] * 4)
        with self.assertRaisesRegex(ValueError, "explicit twenty"):
            self.run_loop(entries=entries, slots=(5,))
        with self.assertRaisesRegex(ValueError, "disagree"):
            self.run_loop(entries=entries, slots=(5,), source_pet_guard_flags=(False,) * 20)

    def test_all_pet_slots_use_literal_guard_and_never_normalize_to_owner(self):
        for target in range(5, 10):
            for owner_flag in (False, True):
                for opposite_flag in (False, True):
                    entries = self.entries((target, target - 5))
                    entries[target] = replace(entries[target], kind="pet")
                    entries[target - 5] = replace(entries[target - 5], ultimate_flag=owner_flag)
                    flags = [False] * 20
                    flags[target - 5] = owner_flag
                    flags[target + 5] = opposite_flag
                    if target + 5 == 10:
                        entries[10] = replace(entries[10], ultimate_flag=opposite_flag)
                    result = self.run_loop(entries=entries, slots=(target,), source_pet_guard_flags=tuple(flags),
                        draws=tuple(BattleModelDraw(i, "target_selection", 0) for i in range(1, 4)))
                    with self.subTest(target=target, owner=owner_flag, opposite=opposite_flag):
                        self.assertEqual([e.outcome for e in result.events],
                            ["skipped_source_pet_flag" if opposite_flag else "normal"] * 4)

    def test_dodge_zero_and_miss_own_no_post_hit_status_rng(self):
        for outcome in ("dodge", "normal", "miss", "allguard"):
            entries = self.entries((0,))
            entries[0] = replace(entries[0], reaction=BaseDamageReactState(reflect=4))
            result = self.run_loop(entries=entries, profile=PROFILE_BIG5,
                draws=tuple(BattleModelDraw(i, "target_selection", 0) for i in range(1, 4)),
                callback=lambda a, e, r: BattleModelAttackSeqResult(outcome, 0))
            with self.subTest(outcome=outcome):
                self.assertEqual(result.entries[0].reaction.reflect, 4)
                self.assertEqual(result.entries[0].marker, 123)
                self.assertTrue(all(e.pet_presentation_damage == 0 and e.status_application is None for e in result.events))

    def test_resistance_strict_boundary_and_preexisting_status_rng_ownership(self):
        for resistance, roll, expected in ((0, 19, True), (0, 20, False),
                                           (5, 14, True), (5, 15, False), (20, 1, False)):
            entries = self.entries((0,))
            entries[0] = replace(entries[0], paralysis_resistance=resistance, reaction=BaseDamageReactState(vanish=4))
            draws = []
            for i in range(4):
                if i:
                    draws.append(BattleModelDraw(i, "target_selection", 0))
                if i == 0 or not expected:
                    draws.append(BattleModelDraw(i, "status", roll))
            result = self.run_loop(entries=entries, draws=tuple(draws), profile=PROFILE_BIG5,
                callback=lambda a, e, r: BattleModelAttackSeqResult("normal", 1))
            with self.subTest(resistance=resistance, roll=roll):
                self.assertEqual(result.events[0].status_application.check.success, expected)
                self.assertEqual(result.events[0].status_application.check.source_probability_value, 20 - resistance)

    def test_critical_nonplayer_death_draw_precedes_next_selection_abio_owns_none(self):
        for abio in (False, True):
            entries = self.entries((5,), hp=5)
            entries[5] = replace(entries[5], kind="pet", abio=abio)
            draws = ([] if abio else [BattleModelDraw(0, "critical_death", 49)])
            draws += [BattleModelDraw(i, "target_selection", 0) for i in range(1, 4)]
            result = self.run_loop(entries=entries, slots=(5,), draws=tuple(draws),
                source_pet_guard_flags=(False,) * 20,
                callback=lambda a, e, r: BattleModelAttackSeqResult("critical", 10))
            self.assertEqual(result.events[0].ultimate_kind, 1)
            self.assertEqual([e.outcome for e in result.events[1:]], ["skipped_target"] * 3)
        entries = self.entries((0,), hp=5)
        result = self.run_loop(entries=entries,
            draws=tuple(BattleModelDraw(i, "target_selection", 0) for i in range(1, 4)),
            callback=lambda a, e, r: BattleModelAttackSeqResult("critical", 10))
        self.assertEqual(result.events[0].ultimate_kind, 0)

    def test_rng_tape_rejects_missing_extra_wrong_owner_and_wrong_order(self):
        callback = lambda a, e, r: BattleModelAttackSeqResult("normal", r.take("attackseq_damage", 0, 100))
        selections = tuple(BattleModelDraw(i, "target_selection", 0) for i in range(1, 4))
        valid = (BattleModelDraw(0, "attackseq_damage", 200), *selections)
        for draws in ((), selections,
                      (BattleModelDraw(1, "attackseq_damage", 1), *selections),
                      (BattleModelDraw(0, "status", 1), *selections), valid):
            with self.subTest(draws=draws), self.assertRaises(ValueError):
                self.run_loop(draws=draws, callback=callback)
        with self.assertRaisesRegex(ValueError, "unused"):
            self.run_loop(draws=(*selections, BattleModelDraw(3, "status", 1)))
        with self.assertRaisesRegex(ValueError, "cannot consume"):
            self.run_loop(callback=lambda a, e, r: r.take("status", 1, 100))
        for args in ((True, "status", 1), (0, "status", True), (0, "counter", 1)):
            with self.assertRaises(ValueError):
                BattleModelDraw(*args)

    def test_input_identity_live_list_and_immutable_dependency_boundaries(self):
        with self.assertRaisesRegex(ValueError, "explicit reduced"):
            self.run_loop(execution_scope="production")
        for slots in ((), (0, 0), (10,), (True,)):
            with self.subTest(slots=slots), self.assertRaises(ValueError):
                self.run_loop(slots=slots, entries=self.entries())
        entries = self.entries()
        entries[10] = replace(entries[10], participant_id="different")
        with self.assertRaisesRegex(ValueError, "actor"):
            self.run_loop(entries=entries)
        entries = self.entries()
        entries[0] = replace(entries[0], target_check_allowed=False)
        with self.assertRaisesRegex(ValueError, "unavailable"):
            self.run_loop(entries=entries)
        def invalid_mutation(attack, current, rng):
            current[0] = replace(current[0], hp=0)
        with self.assertRaises(TypeError):
            self.run_loop(callback=invalid_mutation)
        with self.assertRaises(TypeError):
            self.run_loop(callback=lambda a, e, r: "untyped result")

    def test_marker_reflection_differs_from_ordinary_reflection_and_exhausts(self):
        inputs = dict(raw_damage=30, attacker_hp=150, attacker_max_hp=200, defender_hp=100, defender_max_hp=200)
        ordinary = resolve_base_damage_react(BaseDamageReactState(reflect=1), **inputs)
        modern = resolve_battlemodel_marker_settlement(BaseDamageReactState(reflect=1), **inputs)
        self.assertEqual(ordinary.attacker_hp_after, 120)
        self.assertEqual((modern.attacker_hp_after, modern.defender_hp_after), (150, 100))
        next_hit = resolve_battlemodel_marker_settlement(modern.state_after, **inputs)
        self.assertEqual(next_hit.defender_hp_after, 70)
        self.assertEqual(modern.raw_damage, 30)
        self.assertTrue(modern.charge_consumed)


if __name__ == "__main__":
    unittest.main()
