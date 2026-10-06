"""Actual player Exit clears late work; preserved baselines rebuild views."""
from dataclasses import replace
import unittest

from tests import test_stoneage_default_pet_ultimate_runtime as fixtures
from tools.stoneage_battle_round_model import (
    BattleCommand, BATTLE_COM_WAIT, BATTLE_COM_ATTACK, BATTLE_COM_S_RENZOKU,
    ContinuationAttackRolls, pack_battle_command3,
)
from tools.stoneage_battle_state_model import (
    active_participants, participant_snapshot, resolve_persistent_ordinary_round,
)
from tools.stoneage_battle_status_model import BaseBattleStatusRuntime, BaseBattleStatusState
from tools.stoneage_nocast_runtime_state import NocastParticipantRuntime, NocastRoundOverlay, PreparedWeakenPowers
from tools.stoneage_setmagicpet_runtime_state import (
    SetMagicPetParticipantRuntime, SetMagicPetRoundOverlay, PreparedSetMagicPetPowers,
)
from tools.stoneage_setmagicpet_model import SetMagicPetTargetState


def late(**changes):
    return NocastParticipantRuntime(25,25,25,25, counter=4,barrier_counter=4,
        weaken_counter=4,nc_flag=1,weaken_active_at_visit=True,
        barrier_active_at_visit=True,**changes)


class PlayerExitStatusRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.f=fixtures.DefaultPetUltimateRuntimeTests()
        self.f.setUp()

    def overlay(self, pets=None, **overrides):
        pets=(self.f.pet,) if pets is None else pets
        ids=("player",)+tuple(p.participant_id for p in pets)
        records={pid:late() for pid in ids}
        records["enemy"]=NocastParticipantRuntime(25,25,25,25)
        records.update(overrides)
        return NocastRoundOverlay(records)

    def run_state(self,state,*,target=0,continuation=False):
        participants=active_participants(state)
        commands={p.participant_id:BattleCommand(BATTLE_COM_WAIT) for p in participants}
        commands["enemy"]=(BattleCommand(BATTLE_COM_S_RENZOKU,target,pack_battle_command3(low=1,high=0))
                           if continuation else BattleCommand(BATTLE_COM_ATTACK,target))
        baseline={p.participant_id:p for p in (state.session.player,)+state.session.allied_pets+state.session.enemies}
        kwargs=({"continuation_rolls_by_attack_id":{"enemy":ContinuationAttackRolls((fixtures.hit(),))}}
                if continuation else {})
        return resolve_persistent_ordinary_round(state,commands=commands,
            initiative_random_subtracts={pid:0 for pid in commands},
            profiles={pid:replace(fixtures.profile(),fixed_dex=baseline[pid].quick) for pid in commands},
            attack_rolls={} if continuation else {"enemy":fixtures.hit()},
            defense_profile="newpower_70pct",tie_break_order=tuple(commands),**kwargs)

    def assert_cleared(self,overlay,ids):
        for pid in ids:
            with self.subTest(pid=pid):
                runtime=overlay.runtime_by_participant_id[pid]
                self.assertEqual((runtime.counter,runtime.barrier_counter,runtime.weaken_counter),(0,0,0))
                self.assertFalse(runtime.weaken_active_at_visit)
                self.assertFalse(runtime.barrier_active_at_visit)
                self.assertIsNone(runtime.prepared_weaken_powers)
                self.assertEqual(runtime.nc_flag,1)

    def test_actual_ordinary_player_exit_clears_owner_and_owned_late_work(self):
        before=self.overlay()
        result=self.f.ordinary(self.f.authority(),nocast_overlay=before)
        self.assert_cleared(result.nocast_overlay,("player","pet"))
        self.assertEqual(before.runtime_by_participant_id["player"].counter,4)
        self.assertIs(result.nocast_overlay.runtime_by_participant_id["enemy"],before.runtime_by_participant_id["enemy"])

    def test_clear_is_visible_before_a_later_prepared_actor(self):
        # The engine-neutral test can represent an owned carried entry that
        # remains in the array. Its later visit must not freeze on old counters.
        carried=replace(self.f.pet,participant_id="carried",quick=20)
        by_slot={0:self.f.player,5:self.f.pet,6:carried,10:self.f.enemy}
        authority=self.f.authority(None,{"pet":5,"carried":6},("pet","carried"))
        before=self.overlay((self.f.pet,carried))
        result=self.f.ordinary(authority,by_slot,nocast_overlay=before)
        self.assert_cleared(result.nocast_overlay,("player","pet","carried"))
        visits=[e for e in result.events if e.participant_id=="carried"]
        self.assertTrue(visits)
        self.assertFalse(any(e.result in {"weaken_tick","barrier_tick","nocast_tick"} for e in visits))

    def test_unrelated_pet_overlay_is_preserved(self):
        unrelated=replace(self.f.pet,participant_id="unrelated",quick=20)
        by_slot={0:self.f.player,5:self.f.pet,6:unrelated,10:self.f.enemy}
        before=self.overlay((self.f.pet,unrelated))
        result=self.f.ordinary(self.f.authority(),by_slot,nocast_overlay=before)
        self.assert_cleared(result.nocast_overlay,("player","pet"))
        self.assertGreater(result.nocast_overlay.runtime_by_participant_id["unrelated"].weaken_counter,0)

    def test_persistent_exit_clears_cached_weaken_and_restores_baseline_views(self):
        before=self.f.state(nocast_overlay=self.overlay(
            player=late(prepared_weaken_powers=PreparedWeakenPowers(80,16,32)),
            pet=late(prepared_weaken_powers=PreparedWeakenPowers(80,56,24))))
        self.assertEqual(participant_snapshot(before,"player").quick,32)
        result=self.run_state(before)
        self.assert_cleared(result.after.nocast_overlay,("player","pet"))
        for p in (self.f.player,self.f.pet):
            after=participant_snapshot(result.after,p.participant_id)
            self.assertEqual((after.attack,after.defense,after.quick),(p.attack,p.defense,p.quick))
            self.assertEqual(result.after.base_status_runtime_by_participant_id[p.participant_id].work_quick,p.quick)
        self.assertEqual(before.nocast_overlay.runtime_by_participant_id["player"].prepared_weaken_powers.dexterity,32)

    def test_dead_pet_absent_from_prepared_round_is_healed_and_cleared(self):
        pet=replace(self.f.pet,hp=0)
        before=self.f.state(pets=(pet,),nocast_overlay=self.overlay((pet,),
            pet=late(prepared_weaken_powers=PreparedWeakenPowers(80,56,24))),
            base_status_runtime_by_participant_id={"player":BaseBattleStatusRuntime(),
                "pet":BaseBattleStatusRuntime(BaseBattleStatusState(poison=3)),"enemy":BaseBattleStatusRuntime()})
        result=self.run_state(before)
        self.assertNotIn("pet",result.round.action_order)
        self.assert_cleared(result.after.nocast_overlay,("player","pet"))
        self.assertEqual(result.after.hp_by_participant_id["pet"],1)
        self.assertEqual(result.after.base_status_runtime_by_participant_id["pet"].status.poison,0)
        self.assertEqual(participant_snapshot(result.after,"pet").quick,pet.quick)

    def test_retained_exited_selected_pet_is_in_full_cleanup_roster(self):
        retained=replace(self.f.pet,participant_id="retained",source_pet_slot=1)
        pets=(self.f.pet,retained)
        before=replace(self.f.state(selected=1,pets=pets,pet_slots={"pet":5,"retained":6},
            nocast_overlay=self.overlay(pets)),battle_exited_participant_ids=("retained",))
        result=self.run_state(before)
        self.assert_cleared(result.after.nocast_overlay,("player","pet","retained"))
        self.assertEqual(result.after.default_pet_slot,1)
        self.assertEqual(result.after.pending_pet_variable_ai_by_participant_id["retained"],-1000)

    def test_no_selection_still_clears_all_owned_work(self):
        result=self.run_state(self.f.state(selected=None,nocast_overlay=self.overlay()))
        self.assert_cleared(result.after.nocast_overlay,("player","pet"))
        self.assertEqual(result.after.pending_pet_variable_ai_by_participant_id["pet"],0)

    def test_continuation_exit_binds_outer_overlay_before_later_actor(self):
        before=self.f.state(nocast_overlay=self.overlay())
        result=self.run_state(before,continuation=True)
        self.assertIn("player",result.round.ultimate_exited_participant_ids)
        self.assert_cleared(result.round.nocast_overlay,("player","pet"))
        self.assert_cleared(result.after.nocast_overlay,("player","pet"))

    def test_continuation_with_inactive_dead_pet_restores_work(self):
        pet=replace(self.f.pet,hp=0)
        before=self.f.state(pets=(pet,),nocast_overlay=self.overlay((pet,),
            pet=late(prepared_weaken_powers=PreparedWeakenPowers(80,56,24))))
        result=self.run_state(before,continuation=True)
        self.assert_cleared(result.after.nocast_overlay,("player","pet"))
        self.assertEqual(participant_snapshot(result.after,"pet").quick,pet.quick)

    def test_pet_ultimate_without_owner_exit_does_not_clear_roster_status(self):
        pet=replace(self.f.pet,hp=30,max_hp=30,defense=0)
        before=self.f.state(pets=(pet,),nocast_overlay=self.overlay((pet,)))
        result=self.run_state(before,target=5)
        self.assertNotIn("player",result.round.ultimate_exited_participant_ids)
        self.assertGreater(result.after.nocast_overlay.runtime_by_participant_id["pet"].counter,0)
        self.assertGreater(result.after.nocast_overlay.runtime_by_participant_id["player"].weaken_counter,0)

    def test_normal_owner_death_does_not_clear_late_status(self):
        self.f.player=replace(self.f.player,hp=10)
        self.f.enemy=replace(self.f.enemy,attack=30)
        before=self.f.state(nocast_overlay=self.overlay())
        result=self.run_state(before)
        self.assertEqual(result.after.hp_by_participant_id["player"],0)
        self.assertNotIn("player",result.round.ultimate_exited_participant_ids)
        self.assertGreater(result.after.nocast_overlay.runtime_by_participant_id["player"].counter,0)

    def test_unknown_active_status_failure_leaves_input_state_unchanged(self):
        before=self.f.state(nocast_overlay=self.overlay(player=late(unmodeled_status_active=True)))
        with self.assertRaisesRegex(ValueError,"unmodeled"):
            self.run_state(before)
        self.assertEqual(before.hp_by_participant_id["player"],30)
        self.assertEqual(before.nocast_overlay.runtime_by_participant_id["player"].counter,4)

    def test_missing_retained_roster_status_rejects_in_actual_ordinary_exit(self):
        authority=self.f.authority("retained",{"pet":5},("pet","retained"))
        with self.assertRaisesRegex(ValueError,"complete owned roster"):
            self.f.ordinary(authority,nocast_overlay=self.overlay())

    def test_setmagicpet_prepared_powers_survive_weaken_cleanup(self):
        before=self.f.state(nocast_overlay=self.overlay(
            player=late(prepared_weaken_powers=PreparedWeakenPowers(80,24,32))),
            setmagicpet_overlay=SetMagicPetRoundOverlay({
                "player":SetMagicPetParticipantRuntime(SetMagicPetTargetState(tgh_turn=3,tgh_power=50),
                    prepared_powers=PreparedSetMagicPetPowers(100,30,40)),
                "pet":SetMagicPetParticipantRuntime(),"enemy":SetMagicPetParticipantRuntime()}))
        result=self.run_state(before)
        after=participant_snapshot(result.after,"player")
        self.assertEqual((after.attack,after.defense,after.quick),(100,30,40))
        self.assertEqual(result.after.base_status_runtime_by_participant_id["player"].work_quick,40)


if __name__=="__main__":
    unittest.main()
