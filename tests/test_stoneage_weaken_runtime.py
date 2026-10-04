"""Independent synthetic action/state witnesses; preservation bytes stay external."""
from dataclasses import replace
from hashlib import sha256
from types import SimpleNamespace
from unittest.mock import patch
import unittest

from tests.test_stoneage_attack_crazed_runtime import actor, hit
from tests.test_stoneage_battle_state_model import session
from tools.stoneage_battle_core_model import physical_base_damage
from tools.stoneage_battle_round_model import (
    BATTLE_COM_ATTACK, BATTLE_COM_WAIT, BATTLE_COM_GUARD, BATTLE_COM_S_EARTHROUND0, BATTLE_COM_S_EARTHROUND1,
    BattleCommand, BattleCombatProfile, BattleCommandSetupEffects,
    prepare_battle_round, resolve_ordinary_round,
)
from tools.stoneage_battle_state_model import begin_persistent_battle, resolve_persistent_ordinary_round, participant_snapshot
from tools.stoneage_battle_status_model import BaseBattleStatusRuntime, BaseBattleStatusState, BaseStatusTurnRolls
from tools.stoneage_enemy_ai_weaken_bridge import (
    EnemyAiWeakenSubmission, resolve_enemy_ai_weaken_submission, validate_recovered25_weaken_population,
)
from tools.stoneage_local_runtime_session_coordinator import EnemyAiCommonCommandBatch
from tools.stoneage_nocast_runtime_state import NocastParticipantRuntime, NocastRoundOverlay, PreparedWeakenPowers
from tools.stoneage_recovered25_petskill_runtime import Recovered25PetSkillEntry, Recovered25PetSkillRuntime
from tools.stoneage_weaken_runtime_state import WeakenActionRolls
from tools.stoneage_weaken_model import WeakenOption

SYNTHETIC_OPTION='虛 turn=3 成=50'.encode('cp950')
SYNTHETIC_HASH=sha256(SYNTHETIC_OPTION).hexdigest()


def skills():
    return Recovered25PetSkillRuntime({i:Recovered25PetSkillEntry(i,1,6 if i==575 else 3,2,
        3000 if i==575 else 0,'PETSKILL_Weaken',SYNTHETIC_OPTION) for i in (575,576)},'synthetic')


def submission(skill_id=575,target=0):
    return EnemyAiWeakenSubmission('enemy',0,skill_id,'PETSKILL_Weaken',target)


def overlay(participants, **overrides):
    return NocastRoundOverlay({p.participant_id:overrides.get(p.participant_id,
        NocastParticipantRuntime(25,25,25,25)) for p in participants})


def profiles(participants):
    return {p.participant_id:BattleCombatProfile(p.quick,0,0,0,0,0) for p in participants}


class WeakenRuntimeTests(unittest.TestCase):
    def resolve(self, *, target=0, skill_id=575, players=None, enemy=None, commands=None,
                hit_rolls=None, retarget=(), late=None, extra=None):
        players=players or {0:actor('player','player','player',defense=50)}
        enemy=enemy or actor('enemy','enemy','enemy',quick=200)
        participants=tuple(players.values())+(enemy,)
        commands={p.participant_id:BattleCommand(BATTLE_COM_WAIT) for p in players.values()} | {
            'enemy':BattleCommand(BATTLE_COM_ATTACK,command2=target)} | (commands or {})
        prepared=prepare_battle_round(participants,commands,{p.participant_id:0 for p in participants},tie_break_order=tuple(p.participant_id for p in participants))
        args=dict(slots={p.participant_id:s for s,p in players.items()}|{'enemy':10},
            profiles=profiles(participants),attack_rolls={},defense_profile='newpower_70pct',
            weaken_submissions_by_participant_id={'enemy':submission(skill_id,target)},
            weaken_rolls_by_participant_id={'enemy':WeakenActionRolls(retarget,hit_rolls or {})},
            nocast_overlay=late or overlay(participants))
        args.update(extra or {})
        return resolve_ordinary_round(prepared,**args)

    def application(self,r):
        return next(e for e in r.events if e.weaken_application is not None)

    def test_both_ids_apply_counter_without_canceling_target_attack(self):
        for skill_id in (575,576):
            r=self.resolve(skill_id=skill_id,hit_rolls={0:1},commands={'player':BattleCommand(BATTLE_COM_ATTACK,command2=10)},
                extra={'attack_rolls':{'player':hit()}})
            e=self.application(r)
            self.assertEqual((e.result,e.weaken_skill_id,e.weaken_application.counter_written),('weaken_applied',skill_id,4))
            self.assertFalse(e.weaken_application.source_return_value)
            target_attack=next(e for e in r.events if e.participant_id=='player' and e.result=='normal')
            self.assertEqual(target_attack.damage,physical_base_damage(100,0,0))
            self.assertIsNone(r.nocast_overlay.runtime_by_participant_id['player'].prepared_weaken_powers)

    def test_strict_probability_boundary_and_roll_consumption(self):
        per=self.application(self.resolve(hit_rolls={0:1})).weaken_application.probability_value
        self.assertEqual(self.application(self.resolve(hit_rolls={0:per-1})).result,'weaken_applied')
        self.assertEqual(self.application(self.resolve(hit_rolls={0:per})).result,'weaken_missed')
        for rolls in ({},{0:1,1:1}):
            with self.assertRaises(ValueError):self.resolve(hit_rolls=rolls)

    def test_pet_target_is_admitted(self):
        r=self.resolve(target=1,players={0:actor('player','player','player'),1:actor('pet','player','pet')},hit_rolls={1:1})
        self.assertEqual(self.application(r).resolved_target_slot,1)
        self.assertEqual(r.nocast_overlay.runtime_by_participant_id['pet'].weaken_counter,4)

    def test_existing_status_blocks_before_rng_for_every_late_status_kind(self):
        actors=(actor('player','player','player'),actor('enemy','enemy','enemy'))
        for kwargs in ({'counter':2},{'barrier_counter':2},{'weaken_counter':2},
                       {'unmodeled_status_active':True},{'weaken_active_at_visit':True},{'barrier_active_at_visit':True}):
            late=overlay(actors,player=NocastParticipantRuntime(25,25,25,25,**kwargs))
            r=self.resolve(late=late)
            self.assertEqual(self.application(r).result,'weaken_blocked_existing_status')
            with self.assertRaises(ValueError):self.resolve(late=late,hit_rolls={0:1})

    def test_base_status_blocks_before_weaken_rng(self):
        r=self.resolve(extra={'base_status_runtime_by_participant_id':{
            'player':BaseBattleStatusRuntime(status=BaseBattleStatusState(poison=2),poison_stat_sum=100)}})
        self.assertFalse(self.application(r).weaken_application.rng_consumed)

    def test_unoccupied_live_side_target_uses_multilist_draws(self):
        r=self.resolve(target=9,retarget=(0,),hit_rolls={0:1})
        self.assertTrue(self.application(r).retargeted)
        self.assertEqual(self.application(r).resolved_target_slot,0)
        with self.assertRaises(ValueError):self.resolve(target=9,retarget=(),hit_rolls={0:1})

    def test_symbolic_carrier_never_counters_before_its_action(self):
        r=self.resolve(enemy=actor('enemy','enemy','enemy',quick=1),hit_rolls={0:1},
            commands={'player':BattleCommand(BATTLE_COM_ATTACK,command2=10)},
            extra={'attack_rolls':{'player':hit()},'counter_rolls_by_attack_id':{}})
        self.assertTrue(all(e.result=='counter_ineligible_command' for e in r.events if e.is_counter))

    def test_suppressed_skill_rejects_unused_rng(self):
        actors=(actor('player','player','player'),actor('enemy','enemy','enemy'))
        late=overlay(actors,enemy=NocastParticipantRuntime(25,25,25,25,barrier_counter=2))
        self.assertFalse(any(e.weaken_application for e in self.resolve(late=late).events))
        with self.assertRaises(ValueError):self.resolve(late=late,hit_rolls={0:1})

    def test_sleep_suppresses_before_rng_and_confusion_discards_semantic_skill(self):
        r=self.resolve(extra={'base_status_runtime_by_participant_id':{
            'enemy':BaseBattleStatusRuntime(status=BaseBattleStatusState(sleep=2),work_quick=200)}})
        self.assertFalse(any(e.weaken_application for e in r.events))
        with self.assertRaises(ValueError):
            self.resolve(hit_rolls={0:1},extra={'base_status_runtime_by_participant_id':{
                'enemy':BaseBattleStatusRuntime(status=BaseBattleStatusState(sleep=2),work_quick=200)}})
        r=self.resolve(extra={'base_status_runtime_by_participant_id':{
            'enemy':BaseBattleStatusRuntime(status=BaseBattleStatusState(confusion=2),work_quick=200)},
            'base_status_rolls_by_participant_id':{'enemy':BaseStatusTurnRolls(1,0,0)},
            'attack_rolls':{'enemy':hit()}})
        self.assertFalse(any(e.weaken_application for e in r.events))
        self.assertTrue(any(e.result=='normal' and e.participant_id=='enemy' for e in r.events))
        self.assertEqual(r.nocast_overlay.runtime_by_participant_id['player'].weaken_counter,0)

    def test_early_base_and_late_tick_order_uses_current_weaken_storage(self):
        actors=(actor('player','player','player'),actor('enemy','enemy','enemy'))
        late=overlay(actors,player=NocastParticipantRuntime(25,25,25,25,weaken_counter=1,counter=1))
        r=self.resolve(late=late,extra={'base_status_runtime_by_participant_id':{
            'player':BaseBattleStatusRuntime(status=BaseBattleStatusState(poison=2),poison_stat_sum=100)}})
        visits=[e.result for e in r.events if e.participant_id=='player']
        self.assertLess(visits.index('status_tick'),visits.index('weaken_tick'))
        self.assertLess(visits.index('weaken_tick'),visits.index('nocast_tick'))
        self.assertEqual(r.base_status_runtime_by_participant_id['player'].status.poison,2)
        self.assertEqual(r.nocast_overlay.runtime_by_participant_id['player'].counter,0)

    def test_mutual_freeze_keeps_storage_but_emits_nocast_local_expiry(self):
        actors=(actor('player','player','player'),actor('enemy','enemy','enemy'))
        late=overlay(actors,player=NocastParticipantRuntime(25,25,25,25,weaken_counter=1,barrier_counter=1,counter=1))
        r=self.resolve(late=late)
        current=r.nocast_overlay.runtime_by_participant_id['player']
        self.assertEqual((current.weaken_counter,current.barrier_counter,current.counter,current.nc_flag),(1,1,1,0))
        self.assertEqual([e.result for e in r.events if e.participant_id=='player'][:3],['weaken_tick','barrier_tick','nocast_tick'])

    def test_batch_rejects_all_other_semantic_overlaps_and_bad_carriers(self):
        from tools.stoneage_enemy_ai_mdfyattack_bridge import EnemyAiMdfyAttackSubmission
        with self.assertRaises(ValueError):
            EnemyAiCommonCommandBatch({'enemy':BattleCommand(BATTLE_COM_ATTACK,command2=0)}, {},
                weaken_submissions={'enemy':submission()},mdfyattack_submissions={
                    'enemy':EnemyAiMdfyAttackSubmission('enemy',0,548,'PETSKILL_Mdfyattack',0)})
        with self.assertRaises(ValueError):
            EnemyAiCommonCommandBatch({'enemy':BattleCommand(BATTLE_COM_GUARD)}, {},weaken_submissions={'enemy':submission()})

    def test_invalid_typed_submission_and_rng_are_rejected(self):
        for changes in ({'skill_id':544},{'source_target_slot':10},{'option':WeakenOption(1,50)},
                        {'semantic_command_name':'2022'},{'skill_slot':7},{'callback':'wrong'}):
            with self.assertRaises(ValueError):replace(submission(),**changes)
        for rolls in (WeakenActionRolls(hit_rolls_by_slot={0:1}),):
            with self.assertRaises(ValueError):self.resolve(extra={'weaken_rolls_by_participant_id':{'wrong':rolls}})
        with self.assertRaises(TypeError):self.resolve(extra={'weaken_rolls_by_participant_id':{'enemy':object()}})
        with self.assertRaises(ValueError):self.resolve(extra={'nocast_overlay':None})

    def test_real_hash_gate_rejects_synthetic_semantic_equivalence(self):
        with self.assertRaisesRegex(ValueError,'hash drift'):validate_recovered25_weaken_population(skills())

    def test_full_population_metadata_hash_and_slot_identity_gate(self):
        # Synthetic positive grammar witness with its own explicit fixture hash.
        # Production hash acceptance is independently exercised on verified bundle data.
        spawned=SimpleNamespace(participant=actor('enemy','enemy','enemy'),
                                template=SimpleNamespace(skill_slot_ids=(575,576,0,-1,0,0,0)))
        with patch('tools.stoneage_enemy_ai_weaken_bridge.EXPECTED_OPTION_SHA256',SYNTHETIC_HASH):
            for slot in (0,1):
                s=resolve_enemy_ai_weaken_submission(spawned,skill_slot=slot,target_slot=0,petskill_runtime=skills())
                self.assertEqual(s.skill_id,575+slot)
            for key,value in (('field',2),('target',6),('illegal',3000),('option_bytes',b'bad')):
                runtime=skills(); entries=dict(runtime.skills);entries[576]=replace(entries[576],**{key:value})
                with self.assertRaises(ValueError):
                    resolve_enemy_ai_weaken_submission(spawned,skill_slot=0,target_slot=0,
                        petskill_runtime=replace(runtime,skills=entries))
            for slots in ((575,), (0,0,0,0,0,0,0)):
                with self.assertRaises(ValueError):
                    resolve_enemy_ai_weaken_submission(replace_namespace(spawned,template=SimpleNamespace(skill_slot_ids=slots)),
                        skill_slot=0,target_slot=0,petskill_runtime=skills())


class WeakenPersistentTests(unittest.TestCase):
    def initial(self,late=None):
        player=actor('player','player','player',attack=101,defense=53,quick=101,hp=10000)
        enemy=actor('enemy','enemy','enemy',attack=80,quick=100,hp=10000)
        actors=(player,enemy)
        return begin_persistent_battle(session(player,(enemy,)),slots={'player':0,'enemy':10},
                                      nocast_overlay=late or overlay(actors))

    def advance(self,state,apply=False,commands=None,extra=None):
        actors=(state.session.player,)+state.session.enemies
        cmds={'player':BattleCommand(BATTLE_COM_WAIT),'enemy':BattleCommand(BATTLE_COM_WAIT)}
        if apply:cmds['enemy']=BattleCommand(BATTLE_COM_ATTACK,command2=0)
        cmds.update(commands or {})
        args=dict(commands=cmds,initiative_random_subtracts={'player':0,'enemy':0},profiles=profiles(actors),
                  attack_rolls={},defense_profile='newpower_70pct')
        if apply:args.update(weaken_submissions_by_participant_id={'enemy':submission()},
                            weaken_rolls_by_participant_id={'enemy':WeakenActionRolls(hit_rolls_by_slot={0:1})})
        args.update(extra or {})
        return resolve_persistent_ordinary_round(state,**args)

    def test_application_preparation_expiry_and_recovery_are_separate(self):
        state=self.initial()
        r=self.advance(state,apply=True)
        self.assertEqual(r.round.nocast_overlay.runtime_by_participant_id['player'].weaken_counter,4)
        late=r.after.nocast_overlay.runtime_by_participant_id['player']
        self.assertEqual((late.weaken_counter,late.prepared_weaken_powers),(3,PreparedWeakenPowers(80,42,80)))
        self.assertEqual(r.after.session.player.attack,101)
        # No second preparation when the next call starts: 3 remains 3 during
        # the self-freezing StatusSeq, then one post-round preparation makes 2.
        expected=((2,80),(1,80),(0,101))
        state=r.after
        for count,attack in expected:
            r=self.advance(state)
            self.assertEqual(r.round.action_order[0],'enemy')
            self.assertEqual(r.after.nocast_overlay.runtime_by_participant_id['player'].weaken_counter,count)
            self.assertEqual(participant_snapshot(r.after,'player').attack,attack)
            state=r.after
        # Counter one expires in StatusSeq before preparation; this round's
        # prepared physical powers remain weakened until that preparation.
        self.assertEqual(r.round.nocast_overlay.runtime_by_participant_id['player'].weaken_counter,0)
        self.assertEqual(participant_snapshot(state,'player').quick,101)
        self.assertEqual(self.advance(state).round.action_order[0],'player')

    def test_prepared_attack_defense_and_dex_are_used_next_round(self):
        state=self.advance(self.initial(),apply=True).after
        r=self.advance(state,commands={'player':BattleCommand(BATTLE_COM_ATTACK,command2=10)},
                       extra={'attack_rolls':{'player':hit()}})
        attack=next(e for e in r.round.events if e.participant_id=='player' and e.result=='normal')
        self.assertEqual(attack.damage,physical_base_damage(80,0,0))
        r=self.advance(state,commands={'enemy':BattleCommand(BATTLE_COM_ATTACK,command2=0)},
                       extra={'attack_rolls':{'enemy':hit()}})
        attack=next(e for e in r.round.events if e.participant_id=='enemy' and e.result=='normal')
        self.assertEqual(attack.damage,physical_base_damage(80,42*.7,0))

    def test_counter_one_still_reduces_before_becoming_zero(self):
        state=self.initial();late=dict(state.nocast_overlay.runtime_by_participant_id)
        # Zero-HP valid enemy is not visited by StatusSeq, but is prepared.
        late['enemy']=replace(late['enemy'],weaken_counter=1)
        state=replace(state,hp_by_participant_id={'player':10000,'enemy':0},nocast_overlay=NocastRoundOverlay(late))
        # Need another living enemy to preserve an executable battle round.
        other=actor('other','enemy','enemy',hp=10000)
        state=begin_persistent_battle(session(state.session.player,(state.session.enemies[0],other)),
            slots={'player':0,'enemy':10,'other':11},nocast_overlay=NocastRoundOverlay(late|{'other':NocastParticipantRuntime(25,25,25,25)}))
        state=replace(state,hp_by_participant_id={'player':10000,'enemy':0,'other':10000})
        r=resolve_persistent_ordinary_round(state,commands={'player':BattleCommand(BATTLE_COM_WAIT),'other':BattleCommand(BATTLE_COM_WAIT)},
            initiative_random_subtracts={'player':0,'other':0},profiles=profiles((state.session.player,other)),attack_rolls={},defense_profile='newpower_70pct')
        late=r.after.nocast_overlay.runtime_by_participant_id['enemy']
        self.assertEqual(late.weaken_counter,0)
        self.assertEqual(late.prepared_weaken_powers,PreparedWeakenPowers(64,0,80))

    def test_counter_expiry_does_not_restore_prepared_damage_mid_round(self):
        state=self.advance(self.initial(),apply=True).after
        late=dict(state.nocast_overlay.runtime_by_participant_id)
        late['player']=replace(late['player'],weaken_counter=1)
        state=replace(state,nocast_overlay=NocastRoundOverlay(late))
        r=self.advance(state,commands={'player':BattleCommand(BATTLE_COM_ATTACK,command2=10)},
                       extra={'attack_rolls':{'player':hit()}})
        attack=next(e for e in r.round.events if e.participant_id=='player' and e.result=='normal')
        self.assertEqual(attack.damage,physical_base_damage(80,0,0))
        self.assertEqual(r.round.nocast_overlay.runtime_by_participant_id['player'].weaken_counter,0)
        self.assertEqual(participant_snapshot(r.after,'player').attack,101)

    def test_barrier_preparation_decrements_even_without_weaken(self):
        state=self.initial();late=dict(state.nocast_overlay.runtime_by_participant_id)
        late['player']=replace(late['player'],barrier_counter=3)
        r=self.advance(replace(state,nocast_overlay=NocastRoundOverlay(late)))
        self.assertEqual(r.round.nocast_overlay.runtime_by_participant_id['player'].barrier_counter,3)
        self.assertEqual(r.after.nocast_overlay.runtime_by_participant_id['player'].barrier_counter,2)

    def test_mutual_freeze_still_decrements_both_in_preparation(self):
        state=self.initial();late=dict(state.nocast_overlay.runtime_by_participant_id)
        late['player']=replace(late['player'],barrier_counter=1,weaken_counter=1,counter=1)
        r=self.advance(replace(state,nocast_overlay=NocastRoundOverlay(late)))
        late=r.after.nocast_overlay.runtime_by_participant_id['player']
        self.assertEqual((late.weaken_counter,late.barrier_counter,late.counter,late.nc_flag),(0,0,1,0))
        self.assertEqual(late.prepared_weaken_powers,PreparedWeakenPowers(80,42,80))

    def test_current_earthround0_skips_preparation(self):
        state=self.initial();late=dict(state.nocast_overlay.runtime_by_participant_id)
        late['player']=replace(late['player'],weaken_counter=3)
        state=replace(state,nocast_overlay=NocastRoundOverlay(late))
        r=self.advance(state,commands={'player':BattleCommand(BATTLE_COM_S_EARTHROUND1,command2=10)})
        self.assertEqual(r.after.nocast_overlay.runtime_by_participant_id['player'].weaken_counter,3)
        self.assertIsNone(r.after.nocast_overlay.runtime_by_participant_id['player'].prepared_weaken_powers)

    def test_weaken_carrier_is_excluded_from_combo_before_execution(self):
        state=self.initial();enemy2=actor('enemy2','enemy','enemy',quick=99,hp=10000)
        state=begin_persistent_battle(session(state.session.player,tuple(state.session.enemies)+(enemy2,)),
            slots={'player':0,'enemy':10,'enemy2':11},nocast_overlay=overlay((state.session.player,)+state.session.enemies+(enemy2,)))
        r=resolve_persistent_ordinary_round(state,
            commands={'player':BattleCommand(BATTLE_COM_WAIT),'enemy':BattleCommand(BATTLE_COM_ATTACK,command2=0),'enemy2':BattleCommand(BATTLE_COM_ATTACK,command2=0)},
            initiative_random_subtracts={'player':0,'enemy':0,'enemy2':0},profiles=profiles((state.session.player,)+state.session.enemies),
            attack_rolls={'enemy2':hit()},defense_profile='newpower_70pct',combo_start_rolls_1_100={'enemy2':1},
            weaken_submissions_by_participant_id={'enemy':submission()},weaken_rolls_by_participant_id={'enemy':WeakenActionRolls(hit_rolls_by_slot={0:1})})
        self.assertTrue(any(e.weaken_application for e in r.round.events))
        self.assertFalse(any(e.combo_id for e in r.round.events))

    def test_unverified_modifier_overlap_fails_closed(self):
        state=self.advance(self.initial(),apply=True).after
        with self.assertRaisesRegex(ValueError,'callback power setup'):
            self.advance(state,extra={'command_setup_effects_by_participant_id':{'player':BattleCommandSetupEffects(attack_power=999)}})
        badprofiles=profiles((state.session.player,)+state.session.enemies);badprofiles['player']=replace(badprofiles['player'],fixed_dex=999)
        with self.assertRaisesRegex(ValueError,'DEX/QUICK'):self.advance(state,extra={'profiles':badprofiles})


def replace_namespace(obj,**kwargs):
    return SimpleNamespace(**(vars(obj)|kwargs))


if __name__=='__main__':unittest.main()
