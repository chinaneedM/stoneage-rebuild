from dataclasses import replace
from types import SimpleNamespace
import unittest

from tests.test_stoneage_attack_crazed_runtime import actor, hit
from tools.stoneage_battle_core_model import physical_base_damage, critical_damage, guard_damage
from tools.stoneage_battle_round_model import (
    BATTLE_COM_ATTACK, BATTLE_COM_WAIT, BATTLE_COM_GUARD, BATTLE_COM_COMBO,
    BattleCommand, BattleCombatProfile, BattleCommandSetupEffects,
    prepare_battle_round, resolve_ordinary_round, apply_base_combo_rewrite,
)
from tools.stoneage_battle_guardian_model import GuardianRegistration
from tools.stoneage_battle_damage_react_model import BaseDamageReactState
from tools.stoneage_battle_ride_damage_model import RidePetRuntime
from tools.stoneage_battle_status_model import BaseBattleStatusRuntime, BaseBattleStatusState, BaseStatusTurnRolls
from tools.stoneage_enemy_ai_mdfyattack_bridge import EnemyAiMdfyAttackSubmission, resolve_enemy_ai_mdfyattack_submission
from tools.stoneage_enemy_ai_guard_break2_bridge import EnemyAiGuardBreak2Submission
from tools.stoneage_local_runtime_session_coordinator import EnemyAiCommonCommandBatch
from tools.stoneage_mdfyattack_model import mdfyattack_attribute_damage
from tools.stoneage_recovered25_petskill_runtime import Recovered25PetSkillEntry, Recovered25PetSkillRuntime


def submission(skill_id=548, target=0):
    return EnemyAiMdfyAttackSubmission('enemy', 0, skill_id, 'PETSKILL_Mdfyattack', target)


def skills():
    return Recovered25PetSkillRuntime(skills={548+i: Recovered25PetSkillEntry(
        548+i, 1, 6, 2, 2000, 'PETSKILL_Mdfyattack', code+b'|100')
        for i, code in enumerate((b'EA', b'WA', b'FI', b'WI'))}, source_file='synthetic')


class MdfyAttackRuntimeTests(unittest.TestCase):
    def resolve(self, *, skill_id=548, target=0, commands=None, players=None,
                enemy=None, elements=(0, 100, 0, 0), enemy_elements=(0, 0, 100, 0),
                rolls=None, extra=None):
        players=players or {0: actor('player', 'player', 'player', hp=5000)}
        enemy=enemy or actor('enemy', 'enemy', 'enemy', quick=200)
        participants=tuple(players.values())+(enemy,)
        cmd={p.participant_id: BattleCommand(BATTLE_COM_WAIT) for p in players.values()}
        cmd['enemy']=BattleCommand(BATTLE_COM_ATTACK, command2=target)
        cmd.update(commands or {})
        prepared=prepare_battle_round(participants, cmd, {p.participant_id:0 for p in participants},
                                     tie_break_order=tuple(p.participant_id for p in participants))
        profiles={p.participant_id:BattleCombatProfile(100,0,*elements) for p in players.values()}
        profiles['enemy']=BattleCombatProfile(100,0,*enemy_elements)
        args=dict(slots={p.participant_id:s for s,p in players.items()}|{'enemy':10},
                  profiles=profiles, attack_rolls={'enemy': rolls or hit()},
                  defense_profile='newpower_70pct',
                  mdfyattack_submissions_by_participant_id={'enemy':submission(skill_id,target)})
        args.update(extra or {})
        return resolve_ordinary_round(prepared, **args)

    def event(self, result):
        return next(e for e in result.events if e.participant_id=='enemy' and e.result!='status_tick')

    def test_all_four_ids_replace_original_attack_elements(self):
        base=physical_base_damage(100,0,0)
        for skill_id in range(548,552):
            with self.subTest(skill_id=skill_id):
                event=self.event(self.resolve(skill_id=skill_id))
                self.assertEqual(event.damage, mdfyattack_attribute_damage(base,submission(skill_id).option,(0,100,0,0)))
                self.assertEqual(event.mdfyattack_attack_vector, submission(skill_id).option.attack_vector)
                self.assertEqual(event.mdfyattack_skill_id, skill_id)
                self.assertTrue(event.mdfyattack_event_marked)

    def test_field_uses_replaced_elements_with_native_float_rounding(self):
        event=self.event(self.resolve(extra={'field_attr':'earth','field_power':73}))
        self.assertEqual(event.damage,mdfyattack_attribute_damage(physical_base_damage(100,0,0),
            submission().option,(0,100,0,0),field_attr='earth',field_power=73))

    def test_critical_bonus_follows_attribute_replacement(self):
        event=self.event(self.resolve(rolls=replace(hit(),critical_roll_1_10000=1),extra={
            'profiles':{'enemy':BattleCombatProfile(100,100,0,0,100,0),
                        'player':BattleCombatProfile(1,0,0,100,0,0)}}))
        self.assertTrue(event.critical)
        expected=mdfyattack_attribute_damage(physical_base_damage(100,0,0),submission().option,(0,100,0,0))
        self.assertEqual(event.damage,critical_damage(expected,0,10,10))

    def test_guard_scales_after_attribute_stage(self):
        event=self.event(self.resolve(commands={'player':BattleCommand(BATTLE_COM_GUARD)},rolls=hit(guard_roll_1_100=100)))
        expected=mdfyattack_attribute_damage(physical_base_damage(100,0,0),submission().option,(0,100,0,0))
        self.assertEqual(event.damage,guard_damage(expected,100))

    def test_guardian_calculates_but_original_target_settles(self):
        players={0:actor('player','player','player',hp=5000),1:actor('pet','player','pet',hp=5000,defense=70)}
        event_result=self.resolve(players=players,extra={'guardian_registrations_by_defender_slot':{0:GuardianRegistration(guardian_slot=1)}})
        event=self.event(event_result)
        expected=mdfyattack_attribute_damage(physical_base_damage(100,49,0),submission().option,(0,100,0,0))
        self.assertTrue(event.guardian_redirected)
        self.assertEqual((event.guardian_slot,event.resolved_target_slot),(1,0))
        self.assertEqual(event.damage,expected)
        self.assertEqual(event_result.hp_by_participant_id['pet'],5000)
        self.assertLess(event_result.hp_by_participant_id['player'],5000)

    def test_reflection_retains_override_but_cancels_special_mark(self):
        result=self.resolve(extra={'base_damage_react_state_by_participant_id':{'player':BaseDamageReactState(reflect=1)}})
        event=self.event(result)
        self.assertEqual(event.resolved_target_slot,10)
        self.assertEqual(event.damage,mdfyattack_attribute_damage(physical_base_damage(100,0,0),submission().option,(0,100,0,0)))
        self.assertFalse(event.mdfyattack_event_marked)
        self.assertEqual(result.hp_by_participant_id['player'],5000)
        self.assertEqual(result.base_damage_react_state_by_participant_id['player'].reflect,0)

    def test_absorption_and_vanish_cancel_special_mark(self):
        for state in (BaseDamageReactState(absorb=1),BaseDamageReactState(vanish=1)):
            event=self.event(self.resolve(extra={'base_damage_react_state_by_participant_id':{'player':state}}))
            self.assertFalse(event.mdfyattack_event_marked)

    def test_zero_final_damage_and_minimum_damage_rng(self):
        for minimum in (0,1):
            event=self.event(self.resolve(enemy=actor('enemy','enemy','enemy',attack=0,quick=200),
                         rolls=hit(minimum_damage_roll_0_1=minimum)))
            self.assertEqual(event.damage,minimum)
            self.assertEqual(event.mdfyattack_event_marked,minimum>0)

    def test_no_counter_chain_after_special_hit_or_dodge(self):
        for rolls in (hit(), replace(hit(),dodge_roll_1_10000=1)):
            result=self.resolve(rolls=rolls,commands={'player':BattleCommand(BATTLE_COM_ATTACK,command2=10)},
                    extra={'attack_rolls':{'enemy':rolls,'player':hit()},'counter_rolls_by_attack_id':{}})
            # Player's ordinary hit may attempt a counter; the enemy's
            # symbolic Mdfyattack command is ineligible before RNG lookup.
            counters=[e for e in result.events if e.is_counter]
            self.assertTrue(all(e.participant_id=='enemy' and e.result=='counter_ineligible_command' for e in counters))

    def test_counter_ineligibility_before_and_after_own_action(self):
        for quick in (5,200):
            result=self.resolve(enemy=actor('enemy','enemy','enemy',quick=quick),
                players={0:actor('player','player','player',hp=5000,quick=100)},
                commands={'player':BattleCommand(BATTLE_COM_ATTACK,command2=10)},
                extra={'attack_rolls':{'enemy':hit(),'player':hit()},'counter_rolls_by_attack_id':{}})
            counters=[e for e in result.events if e.is_counter]
            self.assertEqual([e.result for e in counters],['counter_ineligible_command'])

    def test_sleep_suppresses_before_physical_rng(self):
        result=self.resolve(extra={'attack_rolls':{},'base_status_runtime_by_participant_id':{
            'enemy':BaseBattleStatusRuntime(status=BaseBattleStatusState(sleep=2),work_quick=200)}})
        self.assertFalse(any(e.mdfyattack_skill_id is not None for e in result.events))

    def test_confusion_rewrites_to_ordinary_attributes(self):
        result=self.resolve(extra={'base_status_runtime_by_participant_id':{
            'enemy':BaseBattleStatusRuntime(status=BaseBattleStatusState(confusion=2),work_quick=200)},
            'base_status_rolls_by_participant_id':{'enemy':BaseStatusTurnRolls(1,0,0)}})
        event=self.event(result)
        self.assertIsNone(event.mdfyattack_skill_id)
        # Original fire against water is the losing multiplier.
        self.assertEqual(event.damage,int(physical_base_damage(100,0,0)*0.6))

    def test_retarget_rechecks_live_slots(self):
        result=self.resolve(target=1,players={0:actor('player','player','player',hp=5000)},rolls=hit(retarget_roll=0))
        event=self.event(result)
        self.assertTrue(event.retargeted)
        self.assertEqual((event.original_target_slot,event.resolved_target_slot),(1,0))

    def test_ride_split_settles_original_rider(self):
        result=self.resolve(extra={'ride_pet_runtime':RidePetRuntime('player','ride',1000,1000,100),
                                   'ride_pet_source_slot':0})
        event=self.event(result)
        self.assertIsNotNone(event.ride_damage_split)
        self.assertLess(result.ride_pet_runtime.hp,1000)
        self.assertLess(result.hp_by_participant_id['player'],5000)

    def test_bow_carrier_schema_and_overlap_fail_closed(self):
        for extra in ({'profiles':{'enemy':BattleCombatProfile(100,0,0,0,0,0,counter_weapon_type='bow'),
                                   'player':BattleCombatProfile(100,0,0,0,0,0)}},
                      {'mdfyattack_submissions_by_participant_id':{'enemy':object()}},
                      {'mdfyattack_submissions_by_participant_id':{'missing':submission()}},
                      {'mdfyattack_submissions_by_participant_id':{'enemy':submission(target=1)}}):
            with self.subTest(extra=extra),self.assertRaises((ValueError,TypeError)):
                self.resolve(extra=extra)

    def test_typed_bridge_checks_all_rows_and_authoritative_slot(self):
        spawned=SimpleNamespace(participant=actor('enemy','enemy','enemy'),
            template=SimpleNamespace(skill_slot_ids=(548,549,550,551,0,-1,0)))
        for slot in range(4):
            item=resolve_enemy_ai_mdfyattack_submission(spawned,skill_slot=slot,target_slot=0,petskill_runtime=skills())
            self.assertEqual(item.option.element_index,slot)
        for mutation in ('unselected_metadata','option','callback','missing'):
            runtime=skills(); changed=dict(runtime.skills)
            if mutation=='missing':del changed[551]
            else:changed[551]=replace(changed[551],**{'unselected_metadata':{'illegal':0},'option':{'option_bytes':b'WI|60'},'callback':{'function_name':'PETSKILL_Modifyattack'}}[mutation])
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):
                resolve_enemy_ai_mdfyattack_submission(spawned,skill_slot=0,target_slot=0,
                    petskill_runtime=Recovered25PetSkillRuntime(changed,'synthetic'))

    def test_batch_schema_and_no_persistent_command_number(self):
        batch=EnemyAiCommonCommandBatch(commands={'enemy':BattleCommand(BATTLE_COM_ATTACK,command2=0)},setup_effects={},
                                      mdfyattack_submissions={'enemy':submission()})
        self.assertEqual(batch.mdfyattack_submissions['enemy'].semantic_command_name,'BATTLE_COM_S_MDFYATTACK')
        with self.assertRaises(ValueError):
            EnemyAiCommonCommandBatch(commands={'enemy':BattleCommand(BATTLE_COM_GUARD)},setup_effects={},mdfyattack_submissions={'enemy':submission()})

    def test_carrier_cannot_start_or_join_combo(self):
        participants=(actor('player','player','player'),actor('enemy','enemy','enemy',quick=200),
                      actor('enemy2','enemy','enemy',quick=100))
        prepared=prepare_battle_round(participants,{'player':BattleCommand(BATTLE_COM_WAIT),
            'enemy':BattleCommand(BATTLE_COM_ATTACK,command2=0),
            'enemy2':BattleCommand(BATTLE_COM_ATTACK,command2=0)},
            {p.participant_id:0 for p in participants})
        profiles={p.participant_id:BattleCombatProfile(100,0,0,0,0,0) for p in participants}
        rewritten=apply_base_combo_rewrite(prepared,profiles,{'enemy2':1},semantic_nonattack_ids=('enemy',))
        self.assertFalse(any(e.command.command1==BATTLE_COM_COMBO for e in rewritten.ordered_entries))

    def test_specialized_overlap_and_typed_identity_rejected(self):
        guard=EnemyAiGuardBreak2Submission('enemy',0,543,'PETSKILL_GuardBreak2',0)
        with self.assertRaisesRegex(ValueError,'overlap'):
            self.resolve(extra={'guard_break2_submissions_by_participant_id':{'enemy':guard}})
        for kw in ({'skill_id':544},{'callback':'PETSKILL_Modifyattack'},
                   {'skill_slot':7},{'source_target_slot':10},{'semantic_command_name':'BATTLE_COM_ATTACK'}):
            with self.subTest(kw=kw),self.assertRaises(ValueError):
                replace(submission(),**kw)


if __name__=='__main__':
    unittest.main()
