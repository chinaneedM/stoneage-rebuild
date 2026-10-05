"""End-state and chronological witnesses for the equipment-free adapter."""
from dataclasses import replace
import unittest
from unittest.mock import patch

from tests.test_stoneage_battlemodel_admission import fixture, spawned
from tools import stoneage_enemy_ai_battlemodel_bridge as bridge
from tools.stoneage_battlemodel_reference_model import (
    PROFILE_BIG5, PROFILE_UTF8, BattleModelAttackObject,
)
from tools.stoneage_battlemodel_hit_loop import (
    BattleModelEntry, BattleModelDraw, BattleModelAttackSeqRng, HIT_LOOP_SCOPE_R1,
)
from tools.stoneage_battlemodel_physical_attackseq import (
    PHYSICAL_SCOPE_R1, BattleModelPhysicalProfile, BattleModelPhysicalContext,
    resolve_battlemodel_physical_attackseq, execute_battlemodel_physical_loop,
)
from tools.stoneage_battle_guardian_model import GuardianRegistration
from tools.stoneage_battle_damage_react_model import BaseDamageReactState
from tools.stoneage_battle_status_model import BaseBattleStatusRuntime, BaseBattleStatusState


class BattleModelPhysicalTests(unittest.TestCase):
    def setUp(self):
        self.runtime, identities = fixture()
        pin = patch.object(bridge, "EXPECTED_ROW_IDENTITIES", identities)
        pin.start()
        self.addCleanup(pin.stop)
        self.entries = {0: BattleModelEntry("target", "player", 500, 500, 0),
                        10: BattleModelEntry("enemy", "enemy", 500, 500, 0)}
        self.profiles = {
            0: BattleModelPhysicalProfile("target", 10, 100, 0, 40, 40, (0, 0, 0, 0), fixed_vital=40),
            10: BattleModelPhysicalProfile("enemy", 10, 100, 999, 80, 60, (0, 0, 0, 0), fixed_vital=80),
        }

    def submission(self, charset=PROFILE_UTF8):
        return bridge.resolve_enemy_ai_battlemodel_submission(
            spawned(), skill_slot=2, target_slot=5, petskill_runtime=self.runtime,
            profile=charset, source_profile="iris", powers_before=(100, 80, 60))

    def context(self, **kwargs):
        return BattleModelPhysicalContext(PHYSICAL_SCOPE_R1,
            kwargs.pop("defense_profile", "newpower_70pct"),
            kwargs.pop("profiles", self.profiles), kwargs.pop("guardians", {}), **kwargs)

    def one(self, draws, context=None, charset=PROFILE_UTF8):
        remaining = list(draws)
        def take(owner, low, high):
            self.assertTrue(remaining, owner)
            actual_owner, value = remaining.pop(0)
            self.assertEqual(actual_owner, owner)
            self.assertLessEqual(low, value)
            self.assertLessEqual(value, high)
            return value
        result = resolve_battlemodel_physical_attackseq(
            self.submission(charset), actor_slot=10, attack=BattleModelAttackObject(0, 0, 7),
            entries=self.entries, context=context or self.context(), rng=BattleModelAttackSeqRng(take))
        self.assertFalse(remaining)
        return result

    def loop(self, draws, slots=(0,), context=None, charset=PROFILE_UTF8):
        return execute_battlemodel_physical_loop(
            self.submission(charset), actor_slot=10, execution_scope=HIT_LOOP_SCOPE_R1,
            entries=self.entries, initial_living_slots=slots, draws=tuple(draws),
            context=context or self.context(), source_pet_guard_flags=(False,) * 20)

    def test_four_real_hits_change_hp_without_injected_outcomes(self):
        for slot in range(1, 4):
            self.entries[slot] = replace(self.entries[0], participant_id=f"t{slot}")
            self.profiles[slot] = replace(self.profiles[0], participant_id=f"t{slot}")
        draws = [BattleModelDraw(i, owner, value) for i in range(4)
                 for owner, value in (("attackseq_dodge", 10000), ("attackseq_critical", 10000),
                                      ("attackseq_damage", 0))]
        result = self.loop(draws, slots=(0, 1, 2, 3))
        self.assertEqual([e.reported_damage for e in result.events], [137] * 4)
        self.assertEqual([result.entries[i].hp for i in range(4)], [363] * 4)
        self.assertEqual(result.draws_consumed, tuple(draws))
        self.assertEqual(self.entries[0].hp, 500)

    def test_big5_work_attack_and_paralysis_remove_guard_on_later_hits(self):
        self.profiles[0] = replace(self.profiles[0], defense_power=10, command="guard")
        draws = [BattleModelDraw(0, "attackseq_critical", 10000),
                 BattleModelDraw(0, "attackseq_damage", 2),
                 BattleModelDraw(0, "attackseq_guard", 100), BattleModelDraw(0, "status", 1)]
        for i in range(1, 4):
            draws += [BattleModelDraw(i, "target_selection", 0),
                      BattleModelDraw(i, "attackseq_critical", 10000),
                      BattleModelDraw(i, "attackseq_damage", 2)]
        result = self.loop(draws, charset=PROFILE_BIG5)
        self.assertEqual([e.reported_damage for e in result.events], [16, 32, 32, 32])
        self.assertEqual(result.entries[0].hp, 388)
        self.assertEqual(result.entries[0].status_runtime.status.paralysis, 1)
        self.assertEqual(result.cleared_command_slots, frozenset({0}))
        self.assertEqual(result.draws_consumed, tuple(draws))

    def test_reflect_preserves_hp_wakes_and_paralyzes_with_real_damage(self):
        self.profiles[0] = replace(self.profiles[0], defense_power=10)
        self.entries[0] = replace(self.entries[0], reaction=BaseDamageReactState(reflect=4),
            status_runtime=BaseBattleStatusRuntime(status=BaseBattleStatusState(sleep=2)))
        draws = []
        for i in range(4):
            if i:
                draws.append(BattleModelDraw(i, "target_selection", 0))
            draws += [BattleModelDraw(i, "attackseq_critical", 10000), BattleModelDraw(i, "attackseq_damage", 2)]
            if not i:
                draws.append(BattleModelDraw(i, "status", 1))
        result = self.loop(draws, charset=PROFILE_BIG5)
        self.assertEqual(result.entries[0].hp, 500)
        self.assertEqual(result.entries[10].hp, 500)
        self.assertEqual(result.entries[0].reaction.reflect, 0)
        self.assertEqual(result.entries[0].status_runtime.status, BaseBattleStatusState(paralysis=1))
        self.assertEqual([e.reported_damage for e in result.events], [32] * 4)
        self.assertEqual([e.hp_loss for e in result.events], [0] * 4)

    def test_dodge_inclusive_boundary_critical_strict_boundary_and_enemy_luck_ignored(self):
        self.profiles[0] = replace(self.profiles[0], fixed_dex=60)
        self.assertEqual(self.one([("attackseq_dodge", 1)]).outcome, "dodge")
        for roll, outcome, damage in ((399, "critical", 157), (400, "normal", 137)):
            with self.subTest(roll=roll):
                result = self.one([("attackseq_dodge", 2), ("attackseq_critical", roll), ("attackseq_damage", 0)])
                self.assertEqual((result.outcome, result.raw_damage), (outcome, damage))

    def test_dodge_gates_consume_no_dodge_or_drunk_rng(self):
        self.entries[10] = replace(self.entries[10],
            status_runtime=BaseBattleStatusRuntime(status=BaseBattleStatusState(drunk=1)))
        original, profile = self.entries[0], self.profiles[0]
        variants = [replace(original, reaction=BaseDamageReactState(vanish=1)),
                    replace(original, abio=True)]
        variants += [replace(original, status_runtime=BaseBattleStatusRuntime(
            status=BaseBattleStatusState(**{name: 1}))) for name in ("sleep", "paralysis", "stone")]
        for entry in variants:
            self.entries[0] = entry
            result = self.one([("attackseq_critical", 10000), ("attackseq_damage", 0)])
            self.assertEqual(result.outcome, "normal")
        self.entries[0] = original
        self.profiles[0] = replace(profile, no_dodge=True)
        self.one([("attackseq_critical", 10000), ("attackseq_damage", 0)])
        self.profiles[0] = replace(profile, command="guard")
        self.entries[0] = replace(original, status_runtime=BaseBattleStatusRuntime(status=BaseBattleStatusState(confusion=1)))
        self.one([("attackseq_critical", 10000), ("attackseq_damage", 0)])

    def test_drunk_draw_precedes_dodge_and_is_range_checked(self):
        self.profiles[0] = replace(self.profiles[0], fixed_dex=60)
        self.entries[10] = replace(self.entries[10],
            status_runtime=BaseBattleStatusRuntime(status=BaseBattleStatusState(drunk=1)))
        result = self.one([("attackseq_drunk_dodge", 20), ("attackseq_dodge", 2000)])
        self.assertEqual(result.outcome, "dodge")
        with self.assertRaisesRegex(ValueError, "attackseq_drunk_dodge draw"):
            self.loop([BattleModelDraw(0, "attackseq_drunk_dodge", 19)])
        with self.assertRaisesRegex(ValueError, "chronology/owner"):
            self.loop([BattleModelDraw(0, "attackseq_dodge", 2000)])

    def test_piecewise_damage_and_stone_and_old_defense_profiles(self):
        for defense, roll, damage in ((200, 1, 1), (130, 3, 3), (40, 0, 137)):
            self.profiles[0] = replace(self.profiles[0], defense_power=defense, no_dodge=True)
            with self.subTest(defense=defense):
                self.assertEqual(self.one([("attackseq_critical", 10000), ("attackseq_damage", roll)]).raw_damage, damage)
        self.entries[0] = replace(self.entries[0], status_runtime=BaseBattleStatusRuntime(status=BaseBattleStatusState(stone=1)))
        self.assertEqual(self.one([("attackseq_critical", 10000), ("attackseq_damage", 0)]).raw_damage, 81)
        self.entries[0] = replace(self.entries[0], status_runtime=BaseBattleStatusRuntime())
        self.assertEqual(self.one([("attackseq_critical", 10000), ("attackseq_damage", 0)],
            context=self.context(defense_profile="preserved_old_mixed")).raw_damage, 133)

    def test_elements_and_field_adjust_real_damage(self):
        self.profiles[10] = replace(self.profiles[10], elements=(100, 0, 0, 0))
        self.profiles[0] = replace(self.profiles[0], elements=(0, 100, 0, 0), no_dodge=True)
        tape = [("attackseq_critical", 10000), ("attackseq_damage", 0)]
        self.assertEqual(self.one(tape).raw_damage, 205)
        self.assertEqual(self.one(tape, context=self.context(field_attr="earth", field_power=100)).raw_damage, 410)

    def test_guard_floor_and_miss_classification(self):
        self.profiles[0] = replace(self.profiles[0], command="guard")
        for floor, outcome in ((0, "allguard"), (1, "normal")):
            result = self.one([("attackseq_critical", 10000), ("attackseq_damage", 0),
                               ("attackseq_guard", 25), ("attackseq_minimum", floor)])
            self.assertEqual((result.outcome, result.raw_damage), (outcome, floor))
        self.profiles[0] = replace(self.profiles[0], command="none", no_dodge=True, defense_power=200)
        self.assertEqual(self.one([("attackseq_critical", 10000), ("attackseq_damage", 0),
                                  ("attackseq_minimum", 0)]).outcome, "miss")

    def guardian(self):
        self.entries[5] = BattleModelEntry("guardian", "pet", 500, 500, 0)
        self.profiles[5] = BattleModelPhysicalProfile("guardian", 20, 10, 999, 100, 40,
                                                      (0, 0, 0, 0), fixed_vital=100)
        return {0: GuardianRegistration(5)}

    def test_original_dodge_precedes_guardian_actual_critical_and_defense(self):
        guardians = self.guardian()
        self.profiles[0] = replace(self.profiles[0], fixed_dex=60)
        context = self.context(guardians=guardians)
        dodge = self.one([("attackseq_dodge", 1)], context=context)
        self.assertIsNone(dodge.guardian_slot)
        # Actual pet critical probability900; original player probability400.
        result = self.one([("attackseq_dodge", 2), ("attackseq_critical", 500),
                           ("attackseq_damage", 0)], context=context)
        self.assertEqual((result.outcome, result.raw_damage, result.guardian_slot), ("critical", 78, 5))

    def test_guardian_floor_forces_one_and_uses_actual_guard(self):
        guardians = self.guardian()
        self.profiles[0] = replace(self.profiles[0], no_dodge=True)
        self.profiles[5] = replace(self.profiles[5], command="guard")
        result = self.one([("attackseq_critical", 10000), ("attackseq_damage", 0),
                           ("attackseq_guard", 1), ("attackseq_minimum", 0)],
                          context=self.context(guardians=guardians))
        self.assertEqual((result.outcome, result.raw_damage, result.guardian_slot), ("normal", 1, 5))

    def test_paralyzed_guardian_stops_intercepting_later_hits(self):
        guardians = self.guardian()
        self.profiles[0] = replace(self.profiles[0], no_dodge=True, defense_power=10)
        self.profiles[5] = replace(self.profiles[5], defense_power=10)
        draws = []
        for i in range(4):
            if i:
                draws.append(BattleModelDraw(i, "target_selection", 0))
            draws += [BattleModelDraw(i, "attackseq_critical", 10000), BattleModelDraw(i, "attackseq_damage", 2)]
            if i < 2:
                draws.append(BattleModelDraw(i, "status", 1))
        result = self.loop(draws, context=self.context(guardians=guardians), charset=PROFILE_BIG5)
        self.assertEqual([e.actual_defender_slot for e in result.events], [5, 0, 0, 0])
        self.assertEqual((result.entries[5].hp, result.entries[0].hp), (468, 404))
        self.assertEqual(result.cleared_command_slots, frozenset({0, 5}))

    def test_guardian_gates_do_not_own_rng(self):
        guardians = self.guardian()
        self.profiles[0] = replace(self.profiles[0], no_dodge=True)
        original = self.entries[5]
        for name in ("sleep", "confusion", "paralysis", "stone"):
            self.entries[5] = replace(original, status_runtime=BaseBattleStatusRuntime(
                status=BaseBattleStatusState(**{name: 1})))
            self.assertIsNone(self.one([("attackseq_critical", 10000), ("attackseq_damage", 0)],
                                      context=self.context(guardians=guardians)).guardian_slot)
        self.entries[5] = replace(original, hp=0)
        self.assertIsNone(self.one([("attackseq_critical", 10000), ("attackseq_damage", 0)],
                                  context=self.context(guardians=guardians)).guardian_slot)
        self.entries[5] = original
        for registration in (GuardianRegistration(5, guardian_flag=False),
                             GuardianRegistration(5, guardian_barrier=1), GuardianRegistration(0)):
            self.assertIsNone(self.one([("attackseq_critical", 10000), ("attackseq_damage", 0)],
                context=self.context(guardians={0: registration})).guardian_slot)

    def test_real_kill_skips_later_sampled_target_preserving_selection_rng(self):
        self.entries[0] = replace(self.entries[0], hp=5)
        draws = [BattleModelDraw(0, "attackseq_dodge", 10000), BattleModelDraw(0, "attackseq_critical", 10000),
                 BattleModelDraw(0, "attackseq_damage", 0)]
        draws += [BattleModelDraw(i, "target_selection", 0) for i in range(1, 4)]
        result = self.loop(draws)
        self.assertEqual([e.outcome for e in result.events], ["normal"] + ["skipped_target"] * 3)
        self.assertEqual(result.entries[0].hp, 0)
        self.assertEqual(result.draws_consumed, tuple(draws))

    def test_context_binding_and_scope_reject_ambiguous_or_inconsistent_inputs(self):
        for profiles in ({0: self.profiles[0]},
                         {**self.profiles, 0: replace(self.profiles[0], participant_id="other")},
                         {**self.profiles, 10: replace(self.profiles[10], quick=61)}):
            with self.subTest(profiles=profiles), self.assertRaises(ValueError):
                self.loop([], context=self.context(profiles=profiles))
        for kwargs in ({"scope": "ordinary"}, {"defense_profile": "unknown"},
                       {"field_attr": "none", "field_power": 1}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                BattleModelPhysicalContext(**{"scope": PHYSICAL_SCOPE_R1, "defense_profile": "newpower_70pct",
                    "profiles": self.profiles, "guardians": {}, **kwargs})
        with self.assertRaisesRegex(ValueError, "fixed vital"):
            self.context(defense_profile="preserved_old_mixed",
                profiles={**self.profiles, 0: replace(self.profiles[0], fixed_vital=None)})
        with self.assertRaisesRegex(ValueError, "neutral/guard"):
            replace(self.profiles[0], command="noguard")
        with self.assertRaisesRegex(ValueError, "integer"):
            replace(self.profiles[0], level=True)
        with self.assertRaises(TypeError):
            self.context(profiles={0: object()})
        with self.assertRaisesRegex(ValueError, "cannot consume"):
            BattleModelAttackSeqRng(lambda *a: 0).take("status", 1, 100)

    def test_actual_pet_critical_death_draw_precedes_selection_and_abio_bypasses_draw(self):
        original = self.entries.pop(0)
        profile = self.profiles.pop(0)
        self.profiles[5] = replace(profile, fixed_dex=10, no_dodge=True)
        for abio in (False, True):
            self.entries[5] = replace(original, hp=5, kind="pet", abio=abio)
            draws = [BattleModelDraw(0, "attackseq_critical", 500), BattleModelDraw(0, "attackseq_damage", 0)]
            if not abio:
                draws.append(BattleModelDraw(0, "critical_death", 49))
            draws += [BattleModelDraw(i, "target_selection", 0) for i in range(1, 4)]
            result = self.loop(draws, slots=(5,))
            self.assertEqual(result.events[0].outcome, "critical")
            self.assertEqual(result.events[0].reported_damage, 157)
            self.assertEqual(result.events[0].ultimate_kind, 1)
            self.assertEqual(result.entries[5].hp, 0)
            self.assertEqual(result.draws_consumed, tuple(draws))
            self.assertEqual([e.outcome for e in result.events[1:]], ["skipped_target"] * 3)

    def test_context_copies_mutable_maps_and_loop_rejects_unused_rng(self):
        context = self.context()
        self.profiles.clear()
        self.assertEqual(len(context.profiles), 2)
        with self.assertRaises(TypeError):
            context.profiles[0] = None
        with self.assertRaisesRegex(ValueError, "unused"):
            draws = [BattleModelDraw(0, "attackseq_dodge", 1)]
            for i in range(1, 4):
                draws += [BattleModelDraw(i, "target_selection", 0), BattleModelDraw(i, "attackseq_dodge", 1)]
            self.loop(draws + [BattleModelDraw(3, "attackseq_critical", 1)], context=context)


if __name__ == "__main__":
    unittest.main()
