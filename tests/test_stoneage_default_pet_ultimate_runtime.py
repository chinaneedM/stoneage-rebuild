"""Actual ordinary/continuation and immutable persistent exit witnesses."""
from dataclasses import replace
import unittest

from tests.test_stoneage_battle_state_model import participant, session, profile
from tools.stoneage_default_pet_exit_model import DefaultPetExitAuthority
from tools.stoneage_battle_round_model import (
    BattleCommand, OrdinaryAttackRolls, ContinuationAttackRolls,
    BATTLE_COM_ATTACK, BATTLE_COM_WAIT, BATTLE_COM_S_RENZOKU,
    pack_battle_command3, prepare_battle_round, resolve_ordinary_round,
    resolve_continuation_nonbow_baseline,
    PROFIT_BOUNDARY_ORDINARY_PER_HIT,
)
from tools.stoneage_battle_state_model import begin_persistent_battle, resolve_persistent_ordinary_round
from tools.stoneage_battle_status_model import BaseBattleStatusRuntime, BaseBattleStatusState
from tools.stoneage_battle_guardian_model import GuardianRegistration


def hit():
    return OrdinaryAttackRolls(dodge_roll_1_10000=10000,critical_roll_1_10000=10000,damage_roll=0)


class DefaultPetUltimateRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.player=participant("player","player","player",hp=30,max_hp=30,defense=20,quick=40,level=20)
        self.pet=participant("pet","player","pet",hp=100,quick=30,level=20,source_pet_slot=0)
        self.enemy=participant("enemy","enemy","enemy",hp=100,attack=200,quick=100,level=20)
        self.by_slot={0:self.player,5:self.pet,10:self.enemy}

    def authority(self, selected="pet", slots=None, owned=None):
        return {"player":DefaultPetExitAuthority("player",selected,
            ("pet",) if owned is None else owned,{"pet":5} if slots is None else slots)}

    def ordinary(self, authorities=None, by_slot=None, **kwargs):
        by_slot=self.by_slot if by_slot is None else by_slot
        commands={p.participant_id:BattleCommand(BATTLE_COM_WAIT) for p in by_slot.values()}
        commands["enemy"]=BattleCommand(BATTLE_COM_ATTACK,0)
        prepared=prepare_battle_round(tuple(by_slot.values()),commands,{pid:0 for pid in commands},tie_break_order=tuple(commands))
        return resolve_ordinary_round(prepared,slots={p.participant_id:s for s,p in by_slot.items()},
            profiles={pid:profile() for pid in commands},attack_rolls={"enemy":hit()},
            defense_profile="newpower_70pct",default_pet_exit_authorities=authorities,**kwargs)

    def state(self, *, selected=0, pets=None, pet_slots=None, **kwargs):
        pets=(self.pet,) if pets is None else pets
        pet_slots={"pet":5} if pet_slots is None else pet_slots
        return begin_persistent_battle(session(self.player,(self.enemy,),pets),
            slots={"player":0,"enemy":10}|pet_slots,default_pet_slot=selected,**kwargs)

    def state_round(self, state, commands=None, rolls=None, **kwargs):
        from tools.stoneage_battle_state_model import active_participants
        active=active_participants(state)
        commands=commands or {p.participant_id:BattleCommand(BATTLE_COM_WAIT) for p in active}
        if "enemy" in commands and commands["enemy"].command1==BATTLE_COM_WAIT:
            commands=dict(commands);commands["enemy"]=BattleCommand(BATTLE_COM_ATTACK,0)
        return resolve_persistent_ordinary_round(state,commands=commands,
            initiative_random_subtracts={pid:0 for pid in commands},profiles={pid:profile() for pid in commands},
            attack_rolls={"enemy":hit()} if rolls is None else rolls,defense_profile="newpower_70pct",tie_break_order=tuple(commands),**kwargs)

    def test_missing_authority_fails_closed_even_with_sole_pet(self):
        with self.assertRaisesRegex(ValueError,"explicit default-pet authority"):
            self.ordinary()

    def test_player_ultimate_boundary_is_captured_before_exit_mutates_occupancy(self):
        authority=self.authority()
        result=self.ordinary(authority)
        self.assertEqual(len(result.profit_boundaries),1)
        boundary=result.profit_boundaries[0]
        self.assertEqual(
            boundary.boundary_kind,
            PROFIT_BOUNDARY_ORDINARY_PER_HIT,
        )
        self.assertEqual(boundary.hp_by_slot[0],0)
        self.assertEqual(
            dict(boundary.occupied_participant_id_by_slot),
            {0:"player",5:"pet",10:"enemy"},
        )
        self.assertGreater(boundary.ultimate_kind_by_slot[0],0)
        self.assertEqual(boundary.prior_processed_death_ids,())
        self.assertEqual(
            boundary.default_pet_authorities_by_owner_id["player"].selected_pet_id,
            "pet",
        )
        self.assertEqual(result.ultimate_exited_participant_ids,("player","pet"))

    def test_next_profit_boundary_carries_prior_normal_death_as_processed(self):
        pet=replace(
            self.pet,
            hp=1,
            max_hp=1000,
            defense=0,
        )
        enemy2=replace(
            self.enemy,
            participant_id="enemy2",
            quick=90,
        )
        before=begin_persistent_battle(
            session(self.player,(self.enemy,enemy2),(pet,)),
            slots={"player":0,"pet":5,"enemy":10,"enemy2":11},
            default_pet_slot=0,
        )
        commands={
            "player":BattleCommand(BATTLE_COM_WAIT),
            "pet":BattleCommand(BATTLE_COM_WAIT),
            "enemy":BattleCommand(BATTLE_COM_ATTACK,5),
            "enemy2":BattleCommand(BATTLE_COM_ATTACK,0),
        }
        result=self.state_round(
            before,
            commands,
            {"enemy":hit(),"enemy2":hit()},
        )
        boundaries=[
            boundary for boundary in result.round.profit_boundaries
            if boundary.boundary_kind == PROFIT_BOUNDARY_ORDINARY_PER_HIT
        ]
        self.assertEqual(len(boundaries),2)
        first,second=boundaries
        self.assertEqual(first.hp_by_slot[5],0)
        self.assertNotIn(5,first.ultimate_kind_by_slot)
        self.assertNotIn("pet",first.prior_processed_death_ids)
        self.assertIn("pet",second.prior_processed_death_ids)
        self.assertEqual(second.hp_by_slot[5],0)

    def test_explicit_none_still_removes_paired_occupancy(self):
        result=self.ordinary(self.authority(None))
        self.assertEqual(result.ultimate_exited_participant_ids,("player","pet"))
        self.assertEqual(result.hp_by_participant_id["pet"],100)

    def test_unrelated_sole_pet_is_neither_selected_nor_cleaned(self):
        other=replace(self.pet,participant_id="other")
        result=self.ordinary(self.authority(None,{},()),{0:self.player,6:other,10:self.enemy},
            base_status_runtime_by_participant_id={"other":BaseBattleStatusRuntime(BaseBattleStatusState(paralysis=2))})
        self.assertEqual(result.ultimate_exited_participant_ids,("player",))
        self.assertGreater(result.base_status_runtime_by_participant_id["other"].status.paralysis,0)

    def test_selected_retained_absent_does_not_replace_paired_identity(self):
        result=self.ordinary(self.authority("retained",{"pet":5},("pet","retained")))
        self.assertEqual(result.ultimate_exited_participant_ids,("player","pet"))

    def test_selected_and_paired_same_identity_exits_once(self):
        result=self.ordinary(self.authority())
        self.assertEqual(result.ultimate_exited_participant_ids.count("pet"),1)

    def test_selected_and_paired_are_independent_exact_identities(self):
        selected=replace(self.pet,participant_id="selected")
        result=self.ordinary(self.authority("selected",{"selected":1,"pet":5},("selected","pet")),
            {0:self.player,1:selected,5:self.pet,10:self.enemy})
        self.assertEqual(result.ultimate_exited_participant_ids,("player","selected","pet"))

    def test_paired_entry_from_another_owner_rejects(self):
        with self.assertRaisesRegex(ValueError,"paired occupancy"):
            self.ordinary(self.authority(None,{},()))

    def test_occupancy_drift_rejects_before_action(self):
        with self.assertRaisesRegex(ValueError,"occupancy identity drift"):
            self.ordinary(self.authority("pet",{"pet":0}))

    def test_duplicate_ownership_authorities_reject(self):
        a=self.authority();a["another"]=DefaultPetExitAuthority("another",None,("pet",),{"pet":5})
        with self.assertRaisesRegex(ValueError,"multiple owners"):
            self.ordinary(a)

    def test_persistent_no_selection_has_no_selected_pet_loyalty_penalty(self):
        before=self.state(selected=None);result=self.state_round(before)
        self.assertEqual(result.after.pending_pet_variable_ai_by_participant_id["pet"],0)
        self.assertIsNone(result.after.default_pet_slot)
        self.assertEqual(result.after.session.allied_pets,before.session.allied_pets)
        self.assertEqual(before.hp_by_participant_id["player"],30)

    def test_processed_normal_pet_death_is_visible_at_next_round_profit_boundary(self):
        pet=replace(
            self.pet,
            hp=1,
            max_hp=1000,
            defense=0,
        )
        before=self.state(pets=(pet,))
        first=self.state_round(
            before,
            commands={
                "player":BattleCommand(BATTLE_COM_WAIT),
                "pet":BattleCommand(BATTLE_COM_WAIT),
                "enemy":BattleCommand(BATTLE_COM_ATTACK,5),
            },
            rolls={"enemy":hit()},
        )
        self.assertEqual(
            first.after.profit_processed_death_ids,
            ("pet",),
        )
        enemy=first.after.session.enemies[0]
        second=self.state_round(
            first.after,
            commands={
                "player":BattleCommand(BATTLE_COM_WAIT),
                "enemy":BattleCommand(BATTLE_COM_ATTACK,0),
            },
            rolls={"enemy":hit()},
        )
        boundary=next(
            boundary for boundary in second.round.profit_boundaries
            if boundary.boundary_kind == PROFIT_BOUNDARY_ORDINARY_PER_HIT
        )
        self.assertIn("pet",boundary.prior_processed_death_ids)
        self.assertIn("pet",second.before.profit_processed_death_ids)

    def test_player_ultimate_preserves_explicit_selection(self):
        result=self.state_round(self.state())
        self.assertEqual(result.after.default_pet_slot,0)
        self.assertEqual(result.after.pending_pet_variable_ai_by_participant_id["pet"],-1000)
        self.assertEqual(result.after.hp_by_participant_id["pet"],100)

    def test_retained_exited_selection_is_penalized_without_reentering(self):
        retained=replace(self.pet,participant_id="retained",source_pet_slot=1)
        before=replace(self.state(selected=1,pets=(self.pet,retained),pet_slots={"pet":5,"retained":6}),
                       battle_exited_participant_ids=("retained",))
        result=self.state_round(before)
        self.assertEqual(result.round.ultimate_exited_participant_ids,("player","pet"))
        self.assertEqual(result.after.pending_pet_variable_ai_by_participant_id["retained"],-1000)
        self.assertEqual(result.after.pending_pet_variable_ai_by_participant_id["pet"],0)
        self.assertEqual(result.after.default_pet_slot,1)

    def test_player_exit_recovers_dead_owned_pet_without_prepared_entry(self):
        dead=replace(self.pet,hp=0)
        before=self.state(pets=(dead,),base_status_runtime_by_participant_id={
            "player":BaseBattleStatusRuntime(),"pet":BaseBattleStatusRuntime(BaseBattleStatusState(poison=3)),
            "enemy":BaseBattleStatusRuntime()})
        result=self.state_round(before)
        self.assertIn("pet",result.after.ultimate_exited_participant_ids)
        self.assertEqual(result.after.hp_by_participant_id["pet"],1)
        self.assertEqual(result.after.base_status_runtime_by_participant_id["pet"].status.poison,0)
        self.assertEqual(before.hp_by_participant_id["pet"],0)

    def test_pet_ultimate_then_player_death_clears_selection_before_loyalty(self):
        pet=replace(self.pet,hp=30,max_hp=30,defense=0)
        enemy2=replace(self.enemy,participant_id="enemy2",quick=90)
        before=begin_persistent_battle(session(self.player,(self.enemy,enemy2),(pet,)),
            slots={"player":0,"pet":5,"enemy":10,"enemy2":11},default_pet_slot=0)
        commands={"player":BattleCommand(BATTLE_COM_WAIT),"pet":BattleCommand(BATTLE_COM_WAIT),
                  "enemy":BattleCommand(BATTLE_COM_ATTACK,5),"enemy2":BattleCommand(BATTLE_COM_ATTACK,0)}
        result=self.state_round(before,commands,{"enemy":hit(),"enemy2":hit()})
        self.assertIsNone(result.after.default_pet_slot)
        self.assertEqual(result.after.pending_pet_variable_ai_by_participant_id["pet"],-1000)
        self.assertEqual(result.after.pending_player_dead_pet_count_delta,1)
        self.assertEqual(result.after.hp_by_participant_id["pet"],1)
        marker=next(e for e in result.round.events if e.default_pet_selection_cleared_owner_id)
        self.assertEqual(marker.default_pet_selection_cleared_owner_id,"player")
        self.assertEqual(before.default_pet_slot,0)

    def test_nonselected_pet_ultimate_also_clears_owner_selection(self):
        other=replace(self.pet,participant_id="other",source_pet_slot=1,hp=30,max_hp=30,defense=0)
        before=self.state(pets=(self.pet,other),pet_slots={"pet":5,"other":6})
        commands={"player":BattleCommand(BATTLE_COM_WAIT),"pet":BattleCommand(BATTLE_COM_WAIT),
                  "other":BattleCommand(BATTLE_COM_WAIT),"enemy":BattleCommand(BATTLE_COM_ATTACK,6)}
        result=self.state_round(before,commands)
        self.assertIsNone(result.after.default_pet_slot)
        self.assertEqual(result.after.hp_by_participant_id["player"],30)
        self.assertEqual(result.after.pending_pet_variable_ai_by_participant_id["pet"],0)

    def test_guardian_actual_pet_victim_clears_selection_not_player_exit(self):
        pet=replace(self.pet,hp=30,max_hp=30,defense=0)
        before=self.state(pets=(pet,))
        result=self.state_round(before,guardian_registrations_by_defender_slot={
            0:GuardianRegistration(5,100)})
        self.assertIsNone(result.after.default_pet_slot)
        self.assertNotIn("player",result.after.ultimate_exited_participant_ids)
        self.assertTrue(next(e for e in result.round.events if e.guardian_redirected).guardian_redirected)

    def test_failed_round_leaves_original_state_and_selection_immutable(self):
        before=self.state()
        with self.assertRaises(ValueError):
            self.state_round(before,rolls={"enemy":OrdinaryAttackRolls(dodge_roll_1_10000=10000,critical_roll_1_10000=10000,damage_roll=99999)})
        self.assertEqual(before.default_pet_slot,0)
        self.assertEqual(before.hp_by_participant_id["player"],30)

    def test_continuation_none_removes_paired_and_does_not_retarget_it(self):
        command=BattleCommand(BATTLE_COM_S_RENZOKU,0,pack_battle_command3(low=2,high=0))
        result=resolve_continuation_nonbow_baseline(actor=self.enemy,actor_slot=10,command=command,
            action_value=100,by_slot=self.by_slot,hp_by_slot={0:30,5:100,10:100},
            profiles={p.participant_id:profile() for p in self.by_slot.values()},
            command_by_slot={0:BattleCommand(BATTLE_COM_WAIT),5:BattleCommand(BATTLE_COM_WAIT),10:command},
            rolls=ContinuationAttackRolls((hit(),hit())),defense_profile="newpower_70pct",
            default_pet_exit_authorities=self.authority(None))
        self.assertEqual(result.ultimate_exited_participant_ids,("player","pet"))
        self.assertEqual(len(result.events),1)
        self.assertEqual(result.hp_by_slot[5],100)

    def test_continuation_pet_then_player_death_propagates_selection_to_profit(self):
        before=self.state(pets=(replace(self.pet,hp=30,max_hp=30,defense=0),))
        command=BattleCommand(BATTLE_COM_S_RENZOKU,5,pack_battle_command3(low=2,high=0))
        result=self.state_round(before,commands={"player":BattleCommand(BATTLE_COM_WAIT),
            "pet":BattleCommand(BATTLE_COM_WAIT),"enemy":command},rolls={},
            continuation_rolls_by_attack_id={"enemy":ContinuationAttackRolls((
                hit(),replace(hit(),retarget_roll=0)))})
        self.assertEqual(result.round.ultimate_exited_participant_ids,("pet","player"))
        self.assertIsNone(result.after.default_pet_slot)
        self.assertEqual(result.after.pending_pet_variable_ai_by_participant_id["pet"],-1000)
        self.assertEqual(result.after.hp_by_participant_id["pet"],1)

    def test_continuation_player_exit_carries_dead_absent_pet_occupancy(self):
        before=self.state(pets=(replace(self.pet,hp=0),))
        command=BattleCommand(BATTLE_COM_S_RENZOKU,0,pack_battle_command3(low=1,high=0))
        result=self.state_round(before,commands={"player":BattleCommand(BATTLE_COM_WAIT),
            "enemy":command},rolls={},continuation_rolls_by_attack_id={
                "enemy":ContinuationAttackRolls((hit(),))})
        self.assertEqual(result.round.ultimate_exited_participant_ids,("player","pet"))
        self.assertEqual(result.after.hp_by_participant_id["pet"],1)

    def test_new_round_after_pet_ultimate_has_no_default_selection(self):
        before=self.state(pets=(replace(self.pet,hp=30,max_hp=30,defense=0),))
        first=self.state_round(before,commands={"player":BattleCommand(BATTLE_COM_WAIT),
            "pet":BattleCommand(BATTLE_COM_WAIT),"enemy":BattleCommand(BATTLE_COM_ATTACK,5)})
        self.assertIsNone(first.after.default_pet_slot)
        follow=self.state_round(first.after)
        self.assertIsNone(follow.after.default_pet_slot)
        self.assertEqual(follow.after.pending_pet_variable_ai_by_participant_id["pet"],-1000)

    def test_actual_terminal_return_preserves_roster_and_cleared_selection_without_profit(self):
        import tests.test_stoneage_group_battle_runtime as fixtures
        from tools.stoneage_singleplayer_domain import PetSlot
        fixture=fixtures.GroupEncounterBattleRuntimeTests();fixture.setUp()
        fixture.domain.persistent.pets[PetSlot(2)]=fixtures.allied_pet()
        fixture.domain.persistent.default_pet_slot=PetSlot(2)
        fixture.domain.move_player(floor_id=2000,x=10,y=10)
        pet=replace(self.pet,source_pet_slot=2,hp=30,max_hp=30,defense=0)
        enemy2=replace(self.enemy,participant_id="enemy2",quick=90)
        before=begin_persistent_battle(session(self.player,(self.enemy,enemy2),(pet,)),
            slots={"player":0,"pet":5,"enemy":10,"enemy2":11},default_pet_slot=2)
        result=self.state_round(before,commands={"player":BattleCommand(BATTLE_COM_WAIT),
            "pet":BattleCommand(BATTLE_COM_WAIT),"enemy":BattleCommand(BATTLE_COM_ATTACK,5),
            "enemy2":BattleCommand(BATTLE_COM_ATTACK,0)},rolls={"enemy":hit(),"enemy2":hit()})
        exp=fixture.domain.persistent.character.fields["exp"]
        fixture.runtime.finish_persistent_player_ultimate_exit(result.after,elder_return_position=None)
        self.assertIsNone(fixture.domain.persistent.default_pet_slot)
        self.assertIn(PetSlot(2),fixture.domain.persistent.pets)
        self.assertEqual(fixture.domain.persistent.pets[PetSlot(2)].state["hp"],1)
        self.assertEqual(fixture.domain.persistent.pets[PetSlot(2)].state["exp"],10)
        self.assertEqual(fixture.domain.persistent.character.fields["exp"],exp)


if __name__=="__main__":
    unittest.main()
