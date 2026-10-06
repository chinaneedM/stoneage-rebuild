"""Empty equipment still owns RNG: boundary and ordered physical witnesses."""
from dataclasses import replace
import unittest
from unittest.mock import patch

from tests.test_stoneage_battlemodel_admission import fixture, spawned
from tools import stoneage_enemy_ai_battlemodel_bridge as bridge
from tools.stoneage_battlemodel_reference_model import PROFILE_BIG5, PROFILE_UTF8
from tools.stoneage_battlemodel_hit_loop import (
    BattleModelEntry, BattleModelDraw, BattleModelAttackSeqResult, BattleModelAttackSeqRng,
    HIT_LOOP_SCOPE_R1, ITEMCRUSH_HIT_LOOP_SCOPE_R1, execute_battlemodel_post_attackseq_loop,
)
from tools.stoneage_battlemodel_itemcrush_model import (
    EmptyEquipmentParticipant, BattleModelItemCrushContext, resolve_empty_equipment_itemcrush,
)
from tools.stoneage_battlemodel_physical_attackseq import (
    PHYSICAL_SCOPE_R1, BattleModelPhysicalProfile, BattleModelPhysicalContext,
    execute_battlemodel_physical_loop,
)
from tools.stoneage_battle_guardian_model import GuardianRegistration
from tools.stoneage_battle_damage_react_model import BaseDamageReactState


class ItemCrushTests(unittest.TestCase):
    def setUp(self):
        runtime, identities = fixture()
        self.runtime = runtime
        pin = patch.object(bridge, "EXPECTED_ROW_IDENTITIES", identities)
        pin.start(); self.addCleanup(pin.stop)
        self.entries = {0: BattleModelEntry("target", "player", 500, 500, 0),
                        10: BattleModelEntry("enemy", "enemy", 500, 500, 0)}

    def submission(self, charset=PROFILE_UTF8, source="iris"):
        return bridge.resolve_enemy_ai_battlemodel_submission(spawned(), skill_slot=2,
            target_slot=5, petskill_runtime=self.runtime, profile=charset,
            source_profile=source, powers_before=(100, 80, 60))

    def context(self, variant="legacy", source="iris", **kwargs):
        return BattleModelItemCrushContext(source, variant, kwargs.pop("global_rate", 400000),
            kwargs.pop("raw_rand_max", 2**31-1), kwargs.pop("participants", {
                slot: EmptyEquipmentParticipant(e.participant_id, e.kind, 10,
                    (-1,) * (7 if e.kind == "pet" and "pet" in variant else 5))
                for slot, e in self.entries.items()}), **kwargs)

    def one(self, context=None, slot=0, draw=10):
        trace = []
        def take(owner, low, high):
            trace.append((owner, low, high, draw)); return draw
        result = resolve_empty_equipment_itemcrush(context or self.context(),
            actor_slot=10, defender_slot=slot, take=take)
        return result, trace

    def loop(self, draws, *, context=None, slots=(0,), charset=PROFILE_UTF8,
             source="iris", outcome="normal", damage=10, guardian=None, scope=ITEMCRUSH_HIT_LOOP_SCOPE_R1):
        return execute_battlemodel_post_attackseq_loop(self.submission(charset, source),
            actor_slot=10, execution_scope=scope, entries=self.entries,
            initial_living_slots=slots, draws=tuple(draws), itemcrush_context=context or self.context(source=source),
            source_pet_guard_flags=(False,) * 20,
            attack_sequence=lambda *a: BattleModelAttackSeqResult(outcome, damage, guardian))

    def test_legacy_strict_check_empty_scan_has_no_second_rng(self):
        for roll, passed, slots in ((9, True, tuple(range(5))), (10, False, ())):
            result, trace = self.one(draw=roll)
            self.assertEqual(result.legacy_check_passed, passed)
            self.assertEqual(result.defender_lookup_slots, slots)
            self.assertEqual(trace, [("itemcrush_check", 1, 400000, roll)])
            self.assertFalse(result.crushed)

    def test_legacy_nonplayer_owns_no_itemcrush_rng(self):
        for kind in ("pet", "enemy"):
            context = self.context(participants={0: EmptyEquipmentParticipant("target", kind, 10, (-1,)*5),
                                                 10: EmptyEquipmentParticipant("enemy", "enemy", 10, (-1,)*5)})
            result, trace = self.one(context)
            self.assertEqual(trace, [])
            self.assertEqual(result.defender_lookup_slots, ())

    def test_weighted_raw_draw_boundaries_and_attacker_lookup(self):
        context = self.context("take_itemdamage")
        for raw, start in ((0,1),(49,1),(50,0),(66,0),(67,3),(83,3),(84,4),(99,4),(150,0),(2**31-1,1)):
            result, trace = self.one(context, draw=raw)
            self.assertEqual(result.defender_lookup_slots[0], start)
            self.assertEqual(len(result.defender_lookup_slots), 5)
            self.assertEqual(trace, [("itemcrush_raw_rand", 0, 2**31-1, raw)])
            self.assertTrue(result.attacker_weapon_looked_up)
            self.assertFalse(result.crushed)

    def test_bismarck_pet_fix_keeps_literal_modulo_five_after_start(self):
        self.entries[5] = BattleModelEntry("pet", "pet", 500, 500, 0)
        context = self.context("take_itemdamage_pet_fix", "bismarck")
        result, trace = self.one(context, slot=5, draw=6)
        self.assertEqual(result.raw_rand_modulus, 7)
        self.assertEqual(result.defender_lookup_slots, (6,2,3,4,0,1,2))
        plain, _ = self.one(self.context("take_itemdamage_pet", "bismarck"), slot=5, draw=84)
        self.assertEqual(plain.defender_lookup_slots, (4,0,1,2,3,4,0))
        fixed, _ = self.one(self.context("take_itemdamage_fix", "bismarck"), draw=6)
        self.assertEqual(fixed.defender_lookup_slots, (1,2,3,4,0))

    def test_itemcrush_precedes_status_and_lazy_excess_selection(self):
        draws = []
        for i in range(4):
            if i: draws.append(BattleModelDraw(i, "target_selection", 0))
            draws.append(BattleModelDraw(i, "itemcrush_check", 10))
            if i == 0: draws.append(BattleModelDraw(i, "status", 1))
        result = self.loop(draws, charset=PROFILE_BIG5)
        self.assertEqual(result.draws_consumed, tuple(draws))
        self.assertEqual(result.entries[0].hp, 460)
        self.assertEqual(result.cleared_command_slots, frozenset({0}))
        phases = [t.phase for t in result.trace if t.ordinal == 0]
        self.assertLess(phases.index("itemcrush"), phases.index("command_clear"))
        self.assertTrue(all(e.itemcrush and not e.itemcrush.crushed for e in result.events))

    def test_surviving_dodge_miss_allguard_and_zero_damage_own_item_rng(self):
        for outcome in ("dodge", "miss", "allguard", "normal"):
            draws = []
            for i in range(4):
                if i: draws.append(BattleModelDraw(i, "target_selection", 0))
                draws.append(BattleModelDraw(i, "itemcrush_raw_rand", 84))
            result = self.loop(draws, context=self.context("take_itemdamage"), outcome=outcome, damage=0,
                               charset=PROFILE_BIG5)
            self.assertEqual(result.entries[0].hp, 500)
            self.assertEqual(result.draws_consumed, tuple(draws))
            self.assertTrue(all(e.itemcrush is not None and e.status_application is None for e in result.events))

    def test_dead_targets_and_pet_flag_skips_own_no_item_rng(self):
        draws = [BattleModelDraw(i, "target_selection", 0) for i in range(1,4)]
        self.entries[0] = replace(self.entries[0], hp=5)
        result = self.loop(draws, damage=10)
        self.assertTrue(all(e.itemcrush is None for e in result.events))
        self.entries = {5: BattleModelEntry("pet", "pet", 500, 500, 0),
                        10: replace(self.entries[10], ultimate_flag=True)}
        flags = (False,)*10 + (True,) + (False,)*9
        result = execute_battlemodel_post_attackseq_loop(self.submission(), actor_slot=10,
            execution_scope=ITEMCRUSH_HIT_LOOP_SCOPE_R1, entries=self.entries,
            initial_living_slots=(5,), draws=tuple(draws), source_pet_guard_flags=flags,
            itemcrush_context=self.context("take_itemdamage"),
            attack_sequence=lambda *a: self.fail("flag skip precedes physical/item work"))
        self.assertTrue(all(e.itemcrush is None for e in result.events))

    def test_actual_guardian_drives_legacy_kind_and_level(self):
        self.entries[5] = BattleModelEntry("pet", "pet", 500, 500, 0)
        draws = [BattleModelDraw(i, "target_selection", 0) for i in range(1,4)]
        result = self.loop(draws, guardian=5)
        self.assertTrue(all(e.itemcrush.actual_defender_slot == 5 for e in result.events))
        self.assertTrue(all(e.itemcrush.legacy_roll is None for e in result.events))
        self.assertEqual(result.entries[0].hp, 500)
        self.assertEqual(result.entries[5].hp, 460)

    def test_reflection_preserves_hp_but_item_rng_still_precedes_status(self):
        self.entries[0] = replace(self.entries[0], reaction=BaseDamageReactState(reflect=4))
        draws = []
        for i in range(4):
            if i: draws.append(BattleModelDraw(i, "target_selection", 0))
            draws.append(BattleModelDraw(i, "itemcrush_check", 9))
            if not i: draws.append(BattleModelDraw(i, "status", 1))
        result = self.loop(draws, charset=PROFILE_BIG5)
        self.assertEqual(result.entries[0].hp, 500)
        self.assertEqual(result.entries[0].reaction.reflect, 0)
        self.assertTrue(all(e.itemcrush.legacy_check_passed for e in result.events))

    def test_physical_guard_clear_and_item_rng_are_in_one_tape(self):
        profiles = {0: BattleModelPhysicalProfile("target", 10, 100, 0, 10, 40, (0,0,0,0), command="guard"),
                    10: BattleModelPhysicalProfile("enemy", 10, 100, 0, 80, 60, (0,0,0,0))}
        physical = BattleModelPhysicalContext(PHYSICAL_SCOPE_R1, "newpower_70pct", profiles, {})
        draws = [BattleModelDraw(0,"attackseq_critical",10000),BattleModelDraw(0,"attackseq_damage",2),
                 BattleModelDraw(0,"attackseq_guard",100),BattleModelDraw(0,"itemcrush_check",10),
                 BattleModelDraw(0,"status",1)]
        for i in range(1,4):
            draws += [BattleModelDraw(i,"target_selection",0),BattleModelDraw(i,"attackseq_critical",10000),
                      BattleModelDraw(i,"attackseq_damage",2),BattleModelDraw(i,"itemcrush_check",10)]
        result = execute_battlemodel_physical_loop(self.submission(PROFILE_BIG5), actor_slot=10,
            execution_scope=ITEMCRUSH_HIT_LOOP_SCOPE_R1, entries=self.entries,
            initial_living_slots=(0,), draws=tuple(draws), context=physical, itemcrush_context=self.context())
        self.assertEqual([e.reported_damage for e in result.events], [16,32,32,32])
        self.assertEqual(result.entries[0].hp, 388)
        self.assertEqual(result.draws_consumed, tuple(draws))
        wrong = self.context(participants={**self.context().participants,
            0: replace(self.context().participants[0], level=11)})
        with self.assertRaisesRegex(ValueError,"levels"):
            execute_battlemodel_physical_loop(self.submission(), actor_slot=10,
                execution_scope=ITEMCRUSH_HIT_LOOP_SCOPE_R1, entries=self.entries,
                initial_living_slots=(0,), draws=(), context=physical, itemcrush_context=wrong)

    def test_fail_closed_scope_identity_variants_equipment_and_rng(self):
        for kwargs in ({"source_profile":"unknown"},{"variant":"unknown"},{"variant":"take_itemdamage_fix"},
                       {"global_rate":0},{"raw_rand_max":True}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                BattleModelItemCrushContext(**{"source_profile":"iris","variant":"legacy","global_rate":400000,
                    "raw_rand_max":2**31-1,"participants":self.context().participants,**kwargs})
        with self.assertRaisesRegex(ValueError,"empty"):
            EmptyEquipmentParticipant("p","player",10,(-1,-1,1,-1,-1))
        with self.assertRaisesRegex(ValueError,"count"):
            self.context(participants={0:EmptyEquipmentParticipant("target","player",10,(-1,)*7)})
        with self.assertRaisesRegex(ValueError,"identity/kind"):
            self.loop([],context=self.context(participants={**self.context().participants,
                0:EmptyEquipmentParticipant("other","player",10,(-1,)*5)}))
        with self.assertRaisesRegex(ValueError,"exactly cover"):
            self.loop([],context=self.context(participants={10:self.context().participants[10]}))
        with self.assertRaisesRegex(ValueError,"source profile"):
            self.loop([],context=self.context(source="gavin"))
        with self.assertRaisesRegex(ValueError,"no-ItemCrush"):
            self.loop([],scope=HIT_LOOP_SCOPE_R1)
        with self.assertRaisesRegex(ValueError,"chronology/owner"):
            self.loop([BattleModelDraw(0,"status",1)])
        with self.assertRaisesRegex(ValueError,"draw"):
            self.loop([BattleModelDraw(0,"itemcrush_check",400001)])
        with self.assertRaisesRegex(ValueError,"cannot consume"):
            BattleModelAttackSeqRng(lambda *a:0).take("itemcrush_check",1,400000)
        with self.assertRaisesRegex(ValueError,"raw rand draw"):
            self.one(self.context("take_itemdamage",raw_rand_max=32767),draw=32768)
        with self.assertRaisesRegex(TypeError,"typed ItemCrush"):
            execute_battlemodel_post_attackseq_loop(self.submission(),actor_slot=10,
                execution_scope=ITEMCRUSH_HIT_LOOP_SCOPE_R1,entries=self.entries,
                initial_living_slots=(0,),draws=(),attack_sequence=lambda *a:None)

    def test_actual_physical_dodge_still_consumes_raw_item_draw_before_next_selection(self):
        profiles = {0:BattleModelPhysicalProfile("target",10,60,0,40,40,(0,0,0,0)),
                    10:BattleModelPhysicalProfile("enemy",10,100,0,80,60,(0,0,0,0))}
        draws=[]
        for i in range(4):
            if i:draws.append(BattleModelDraw(i,"target_selection",0))
            draws += [BattleModelDraw(i,"attackseq_dodge",1),BattleModelDraw(i,"itemcrush_raw_rand",6)]
        result=execute_battlemodel_physical_loop(self.submission(PROFILE_BIG5),actor_slot=10,
            execution_scope=ITEMCRUSH_HIT_LOOP_SCOPE_R1,entries=self.entries,
            initial_living_slots=(0,),draws=tuple(draws),
            context=BattleModelPhysicalContext(PHYSICAL_SCOPE_R1,"newpower_70pct",profiles,{}),
            itemcrush_context=self.context("take_itemdamage"))
        self.assertEqual([e.outcome for e in result.events],["dodge"]*4)
        self.assertEqual(result.entries[0].hp,500)
        self.assertEqual(result.draws_consumed,tuple(draws))

    def test_real_pet_critical_death_has_no_item_draw_before_selection(self):
        self.entries={5:BattleModelEntry("pet","pet",5,500,0),10:self.entries[10]}
        profiles={5:BattleModelPhysicalProfile("pet",10,10,0,40,40,(0,0,0,0),no_dodge=True),
                  10:BattleModelPhysicalProfile("enemy",10,100,0,80,60,(0,0,0,0))}
        draws=[BattleModelDraw(0,"attackseq_critical",500),BattleModelDraw(0,"attackseq_damage",0),
               BattleModelDraw(0,"critical_death",49),
               *(BattleModelDraw(i,"target_selection",0) for i in range(1,4))]
        result=execute_battlemodel_physical_loop(self.submission(),actor_slot=10,
            execution_scope=ITEMCRUSH_HIT_LOOP_SCOPE_R1,entries=self.entries,
            initial_living_slots=(5,),draws=tuple(draws),source_pet_guard_flags=(False,)*20,
            context=BattleModelPhysicalContext(PHYSICAL_SCOPE_R1,"newpower_70pct",profiles,{}),
            itemcrush_context=self.context("take_itemdamage"))
        self.assertEqual(result.events[0].outcome,"critical")
        self.assertEqual(result.events[0].ultimate_kind,1)
        self.assertTrue(all(e.itemcrush is None for e in result.events))
        self.assertEqual(result.draws_consumed,tuple(draws))


if __name__ == "__main__":
    unittest.main()
