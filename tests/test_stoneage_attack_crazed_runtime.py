import unittest
from dataclasses import replace
from types import SimpleNamespace

from tools.stoneage_enemy_ai_attack_crazed_bridge import EnemyAiAttackCrazedSubmission, resolve_enemy_ai_attack_crazed_submission
from tools.stoneage_recovered25_petskill_runtime import Recovered25PetSkillEntry, Recovered25PetSkillRuntime
from tools.stoneage_battle_round_model import (
    AttackCrazedRolls, CounterAttemptRolls, BattleCombatProfile, BattleCommand, OrdinaryAttackRolls,
    BATTLE_COM_ATTACK, BATTLE_COM_WAIT, BATTLE_COM_GUARD, BATTLE_COM_COMBO,
    prepare_battle_round, resolve_ordinary_round, apply_base_combo_rewrite,
)
from tools.stoneage_battle_round_model import BattleCommandSetupEffects
from tools.stoneage_battle_guardian_model import GuardianRegistration
from tools.stoneage_battle_ride_damage_model import RidePetRuntime
from tools.stoneage_battle_status_model import BaseBattleStatusRuntime, BaseBattleStatusState, BaseStatusTurnRolls
from tools.stoneage_battle_damage_react_model import BaseDamageReactState
from tools.stoneage_singleplayer_battle import BattleParticipant
from tools.stoneage_battle_core_model import physical_base_damage


def actor(pid, side, kind, hp=2000, attack=100, defense=0, quick=10):
    return BattleParticipant(participant_id=pid,side=side,kind=kind,level=10,hp=hp,max_hp=hp,
                             attack=attack,defense=defense,quick=quick,name=pid,fixed_vital=40)


def submission(target=0):
    return EnemyAiAttackCrazedSubmission('enemy',0,613,'PETSKILL_AttackCrazed',target)


def hit(**kw):
    return OrdinaryAttackRolls(critical_roll_1_10000=10000,damage_roll=0,dodge_roll_1_10000=10000,**kw)


class AttackCrazedRuntimeTests(unittest.TestCase):
    def resolve(self, *, target=0, draws=(0,0,0), hits=None, players=None, enemy=None,
                commands=None, extra=None):
        players=players if players is not None else {0:actor('player','player','player'),1:actor('pet','player','pet'),9:actor('last','player','pet')}
        enemy=enemy or actor('enemy','enemy','enemy',quick=200)
        participants=tuple(players.values())+(enemy,)
        cmd={p.participant_id:BattleCommand(BATTLE_COM_WAIT) for p in players.values()}
        cmd['enemy']=BattleCommand(BATTLE_COM_ATTACK,command2=target)
        cmd.update(commands or {})
        prepared=prepare_battle_round(participants,cmd,{p.participant_id:0 for p in participants},tie_break_order=tuple(p.participant_id for p in participants))
        setup=submission(target).callback_setup(fixed_strength=enemy.attack,fixed_toughness=enemy.defense)
        args=dict(slots={p.participant_id:s for s,p in players.items()}|{'enemy':10},
                  profiles={p.participant_id:BattleCombatProfile(100,0,0,0,0,0) for p in participants},
                  attack_rolls={},defense_profile='newpower_70pct',
                  attack_crazed_submissions_by_participant_id={'enemy':submission(target)},
                  attack_crazed_rolls_by_attack_id={'enemy':AttackCrazedRolls(draws,hits or (hit(),hit(),hit()))},
                  command_setup_effects_by_participant_id={'enemy':BattleCommandSetupEffects(attack_power=setup.attack_power,defense_power=setup.defense_power)})
        args.update(extra or {})
        return resolve_ordinary_round(prepared,**args)

    def attack_events(self,result):
        return tuple(e for e in result.events if e.attack_crazed_skill_id is not None)

    def test_original_first_then_list_one_two_and_no_damage_division(self):
        r=self.resolve(target=9,draws=(0,1,0))
        events=self.attack_events(r)
        self.assertEqual([e.resolved_target_slot for e in events],[9,1,0])
        self.assertEqual([e.original_target_slot for e in events],[9,1,0])
        self.assertEqual([e.attack_crazed_hit_index for e in events],[0,1,2])
        self.assertTrue(all(e.attack_crazed_target_list==(0,1,0) for e in events))
        self.assertTrue(all(e.attack_crazed_selection_draws==3 for e in events))
        self.assertTrue(all(e.damage==physical_base_damage(80,0,0) for e in events))
        self.assertTrue(all(e.command1==BATTLE_COM_ATTACK for e in events))

    def test_preselected_dead_target_retargets_per_hit_after_mutation(self):
        players={0:actor('player','player','player'),1:actor('pet','player','pet',hp=1),9:actor('last','player','pet')}
        r=self.resolve(target=1,draws=(1,1,1),players=players,hits=(hit(),hit(retarget_roll=0),hit(retarget_roll=1)))
        events=self.attack_events(r)
        self.assertEqual([e.resolved_target_slot for e in events],[1,0,9])
        self.assertEqual([e.retargeted for e in events],[False,True,True])
        self.assertEqual(r.hp_by_participant_id['pet'],0)

    def test_only_last_slot_alive_uses_initial_list_without_pool_rng(self):
        r=self.resolve(target=9,draws=(),players={9:actor('player','player','player')})
        events=self.attack_events(r)
        self.assertEqual([e.resolved_target_slot for e in events],[9,9,9])
        self.assertTrue(all(e.attack_crazed_target_list==(9,9,9) and e.attack_crazed_selection_draws==0 for e in events))

    def test_pool_rng_domain_validated_against_action_time_candidates(self):
        with self.assertRaisesRegex(ValueError,'selection RNG'):
            self.resolve(draws=(0,2,0))
        with self.assertRaisesRegex(ValueError,'unused AttackCrazed'):
            self.resolve(target=9,players={9:actor('player','player','player')})
        with self.assertRaisesRegex(ValueError,'missing AttackCrazed'):
            self.resolve(draws=())

    def test_guardian_settlement_uses_guardian_on_each_hit(self):
        r=self.resolve(extra={'guardian_registrations_by_defender_slot':{0:GuardianRegistration(guardian_slot=1)}})
        events=self.attack_events(r)
        self.assertEqual([e.resolved_target_slot for e in events],[1,1,1])
        self.assertTrue(all(e.guardian_redirected for e in events))
        self.assertEqual(r.hp_by_participant_id['player'],2000)
        self.assertLess(r.hp_by_participant_id['pet'],2000)

    def test_reflection_kills_actor_and_stops_later_hits(self):
        r=self.resolve(enemy=actor('enemy','enemy','enemy',hp=1,quick=200),extra={
            'base_damage_react_state_by_participant_id':{'player':BaseDamageReactState(reflect=1)}})
        self.assertEqual(len(self.attack_events(r)),1)
        self.assertEqual(r.hp_by_participant_id['enemy'],0)
        self.assertEqual(r.base_damage_react_state_by_participant_id['player'].reflect,0)

    def test_guarded_targets_consume_per_hit_guard_rng(self):
        r=self.resolve(commands={'player':BattleCommand(BATTLE_COM_GUARD)},hits=(hit(guard_roll_1_100=100),)*3)
        self.assertEqual(len(self.attack_events(r)),3)
        self.assertTrue(all(e.damage<physical_base_damage(80,0,0) for e in self.attack_events(r)))

    def test_dodge_still_advances_to_next_preselected_target(self):
        r=self.resolve(draws=(0,1,0),hits=(replace(hit(),dodge_roll_1_10000=1),hit(),hit()))
        events=self.attack_events(r)
        self.assertEqual(events[0].result,'attack_crazed_dodge')
        self.assertEqual([e.resolved_target_slot for e in events],[0,1,0])
        self.assertEqual(events[0].damage,0)

    def test_setup_drift_missing_rng_and_bow_fail_closed(self):
        for extra in ({'command_setup_effects_by_participant_id':{}},
                      {'attack_crazed_rolls_by_attack_id':{}},
                      {'profiles':{k:BattleCombatProfile(100,0,0,0,0,0,counter_weapon_type='bow') for k in ('enemy','player','pet','last')}}):
            with self.subTest(extra=extra),self.assertRaises(ValueError):self.resolve(extra=extra)

    def test_counter_check_occurs_once_after_final_target_hit(self):
        r=self.resolve(target=9,draws=(0,1,0),extra={
            'counter_rolls_by_attack_id':{'enemy':(CounterAttemptRolls(10000),)},
        })
        indices=[i for i,e in enumerate(r.events) if e.attack_crazed_skill_id is not None]
        counter=[(i,e) for i,e in enumerate(r.events) if e.is_counter]
        self.assertEqual(len(counter),1)
        self.assertGreater(counter[0][0],indices[-1])
        self.assertEqual(counter[0][1].participant_id,'player')

    def test_sleeping_actor_does_not_consume_selection_or_per_hit_rng(self):
        r=self.resolve(draws=(),extra={
            'base_status_runtime_by_participant_id':{'enemy':BaseBattleStatusRuntime(status=BaseBattleStatusState(sleep=1))},
        })
        self.assertEqual(self.attack_events(r),())
        self.assertEqual(r.hp_by_participant_id['player'],2000)

    def test_ride_pet_falls_on_first_hit_and_later_hits_settle_unmounted(self):
        r=self.resolve(extra={'ride_pet_runtime':RidePetRuntime('player','ride',1,1,1)})
        events=self.attack_events(r)
        self.assertTrue(events[0].ride_damage_split.shared)
        self.assertTrue(events[0].ride_hp_resolution.unmounted)
        self.assertFalse(events[1].ride_damage_split.shared if events[1].ride_damage_split else False)
        self.assertFalse(r.ride_pet_runtime.mounted)
        self.assertEqual(r.ride_pet_runtime.hp,0)

    def test_callback_defense_write_precedes_faster_ordinary_attack(self):
        players={0:actor('player','player','player',quick=300)}
        r=self.resolve(players=players,enemy=actor('enemy','enemy','enemy',defense=100,quick=1),
                       commands={'player':BattleCommand(BATTLE_COM_ATTACK,command2=10)},
                       extra={'attack_rolls':{'player':hit()}})
        event=next(e for e in r.events if e.participant_id=='player' and e.damage>0)
        self.assertEqual(event.damage,physical_base_damage(100,49,0))
        self.assertLess(r.events.index(event),next(i for i,e in enumerate(r.events) if e.attack_crazed_skill_id is not None))

    def test_confusion_rewrite_executes_ordinary_attack_without_pool_rng(self):
        r=self.resolve(draws=(),extra={
            'attack_rolls':{'enemy':hit()},
            'base_status_runtime_by_participant_id':{'enemy':BaseBattleStatusRuntime(status=BaseBattleStatusState(confusion=2))},
            'base_status_rolls_by_participant_id':{'enemy':BaseStatusTurnRolls(1,0,9)},
        })
        self.assertEqual(self.attack_events(r),())
        self.assertEqual(len([e for e in r.events if e.participant_id=='enemy' and e.damage>0]),1)

    def test_internal_attack_carrier_neither_starts_nor_joins_combo(self):
        player=actor('player','player','player')
        first=actor('enemy','enemy','enemy',quick=200)
        second=actor('enemy2','enemy','enemy',quick=100)
        prepared=prepare_battle_round((player,first,second),{
            'player':BattleCommand(BATTLE_COM_WAIT),
            'enemy':BattleCommand(BATTLE_COM_ATTACK,command2=0),
            'enemy2':BattleCommand(BATTLE_COM_ATTACK,command2=0),
        },{'player':0,'enemy':0,'enemy2':0})
        profiles={p.participant_id:BattleCombatProfile(100,0,0,0,0,0) for p in (player,first,second)}
        result=apply_base_combo_rewrite(prepared,profiles,{'enemy2':1},semantic_nonattack_ids=('enemy',))
        self.assertTrue(all(e.command.command1!=BATTLE_COM_COMBO for e in result.ordered_entries))
        self.assertEqual([e.combo_id for e in result.ordered_entries],[0,0,0])

    def test_typed_submission_rejects_target_count_and_identity_drift(self):
        s=submission()
        for kw in ({'source_target_slot':10},{'attack_count':4},{'skill_id':608},{'skill_slot':7},{'callback':'PETSKILL_NormalAttack'}):
            with self.subTest(kw=kw),self.assertRaises(ValueError):replace(s,**kw)

    def test_recovered_bridge_checks_full_metadata_and_slot_identity(self):
        spawned=SimpleNamespace(participant=SimpleNamespace(participant_id='enemy'),template=SimpleNamespace(skill_slot_ids=(613,0,0,0,0,0,0)))
        entry=Recovered25PetSkillEntry(613,1,1,2,0,'PETSKILL_AttackCrazed',b'3')
        runtime=SimpleNamespace(skills={613:entry})
        self.assertEqual(resolve_enemy_ai_attack_crazed_submission(spawned,skill_slot=0,target_slot=0,petskill_runtime=runtime),submission())
        for kw in ({'target':6},{'field':2},{'cost':3},{'illegal':1},{'option_bytes':b'03'}):
            runtime=SimpleNamespace(skills={613:replace(entry,**kw)})
            with self.subTest(kw=kw),self.assertRaises(ValueError):resolve_enemy_ai_attack_crazed_submission(spawned,skill_slot=0,target_slot=0,petskill_runtime=runtime)
        with self.assertRaises(ValueError):resolve_enemy_ai_attack_crazed_submission(spawned,skill_slot=1,target_slot=0,petskill_runtime=SimpleNamespace(skills={613:entry}))

if __name__=='__main__':unittest.main()
