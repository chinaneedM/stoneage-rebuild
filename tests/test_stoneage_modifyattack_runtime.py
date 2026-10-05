"""Ordered Modifyattack witnesses: exact admission and helper RNG ownership."""
from dataclasses import replace
from types import SimpleNamespace
import unittest

from tests.test_stoneage_attack_crazed_runtime import actor, hit
from tools.stoneage_battle_core_model import physical_base_damage, attribute_adjusted_damage, critical_damage, guard_damage
from tools.stoneage_battle_round_model import (
    BATTLE_COM_ATTACK, BATTLE_COM_WAIT, BATTLE_COM_GUARD,
    BattleCommand, BattleCombatProfile, BattleCommandSetupEffects,
    prepare_battle_round, resolve_ordinary_round,
)
from tools.stoneage_battle_guardian_model import GuardianRegistration
from tools.stoneage_battle_damage_react_model import BaseDamageReactState
from tools.stoneage_battle_status_model import BaseBattleStatusRuntime, BaseBattleStatusState, BaseStatusTurnRolls
from tools.stoneage_enemy_ai_modifyattack_bridge import (
    EnemyAiModifyAttackSubmission, resolve_enemy_ai_modifyattack_submission,
    EXPECTED_POSITIVE_TEMPLATE_SLOTS,
)
from tools.stoneage_enemy_ai_mdfyattack_bridge import EnemyAiMdfyAttackSubmission
from tools.stoneage_local_runtime_session_coordinator import EnemyAiCommonCommandBatch
from tools.stoneage_modifyattack_reference_model import modifyattack_helper_damage
from tools.stoneage_recovered25_petskill_runtime import Recovered25PetSkillEntry, Recovered25PetSkillRuntime


def submission(tempno=20, target=0):
    graphic, slot, skill = EXPECTED_POSITIVE_TEMPLATE_SLOTS[tempno]
    return EnemyAiModifyAttackSubmission('enemy', slot, skill, 'PETSKILL_Modifyattack', target, tempno, graphic)


def skills():
    return Recovered25PetSkillRuntime(skills={544+i: Recovered25PetSkillEntry(
        544+i, 1, 6, 2, 2000, 'PETSKILL_Modifyattack', code+b'|20')
        for i, code in enumerate((b'EA', b'WA', b'FI', b'WI'))}, source_file='synthetic')


class ModifyAttackRuntimeTests(unittest.TestCase):
    def resolve(self, *, tempno=20, target=0, rand=0, commands=None, players=None,
                enemy=None, elements=(100, 0, 0, 0), enemy_elements=(0, 0, 0, 0),
                rolls=None, extra=None):
        players=players if players is not None else {0:actor('player','player','player',hp=5000)}
        enemy=enemy or actor('enemy','enemy','enemy',quick=200)
        participants=tuple(players.values())+(enemy,)
        cmd={p.participant_id:BattleCommand(BATTLE_COM_WAIT) for p in players.values()}
        cmd['enemy']=BattleCommand(BATTLE_COM_ATTACK,command2=target)
        cmd.update(commands or {})
        prepared=prepare_battle_round(participants,cmd,{p.participant_id:0 for p in participants},
                                     tie_break_order=tuple(p.participant_id for p in participants))
        profiles={p.participant_id:BattleCombatProfile(100,0,*elements) for p in players.values()}
        profiles['enemy']=BattleCombatProfile(100,0,*enemy_elements)
        args=dict(slots={p.participant_id:s for s,p in players.items()}|{'enemy':10},
                  profiles=profiles,attack_rolls={'enemy':rolls or hit()},defense_profile='newpower_70pct',
                  modifyattack_submissions_by_participant_id={'enemy':submission(tempno,target)},
                  modifyattack_rand_by_participant_id={'enemy':rand})
        args.update(extra or {})
        return resolve_ordinary_round(prepared,**args)

    def event(self,result):
        return next(e for e in result.events if e.participant_id=='enemy' and e.result!='status_tick')

    def test_three_positive_ids_augment_once_after_ordinary_damage(self):
        base=physical_base_damage(100,0,0)
        for tempno in (18,19,20):
            item=submission(tempno)
            elements=tuple(100 if i==item.option.element_index else 0 for i in range(4))
            result=self.resolve(tempno=tempno,elements=elements,rand=99)
            events=[e for e in result.events if e.modifyattack_skill_id is not None]
            self.assertEqual(len(events),1)
            event=events[0]
            ordinary=attribute_adjusted_damage(base,(0,0,0,0),elements)
            self.assertEqual(event.modifyattack_damage_before,ordinary)
            self.assertEqual(event.damage,modifyattack_helper_damage(ordinary,item.option,elements,raw_rand=99)[0])
            self.assertEqual((event.modifyattack_skill_id,event.modifyattack_helper_draws),(item.skill_id,1))
            self.assertTrue(event.modifyattack_event_marked)
            self.assertIsNone(event.mdfyattack_skill_id)

    def test_raw_rand_integer_division_boundary_and_m95_draw(self):
        for matched,rand in ((95,99),(96,99),(96,100),(100,104),(100,105)):
            elements=(matched,0,0,0)
            event=self.event(self.resolve(elements=elements,rand=rand))
            expected,draws=modifyattack_helper_damage(event.modifyattack_damage_before,submission().option,elements,raw_rand=rand)
            self.assertEqual((event.damage,event.modifyattack_helper_draws),(expected,draws))
        self.assertGreater(self.event(self.resolve(elements=(96,0,0,0),rand=100)).damage,
                           self.event(self.resolve(elements=(96,0,0,0),rand=99)).damage)

    def test_ordinary_attributes_critical_and_guard_precede_helper(self):
        elements=(100,0,0,0)
        profiles={'player':BattleCombatProfile(1,0,*elements),
                  'enemy':BattleCombatProfile(100,100,0,100,0,0)}
        event=self.event(self.resolve(commands={'player':BattleCommand(BATTLE_COM_GUARD)},
            rolls=replace(hit(guard_roll_1_100=100),critical_roll_1_10000=1),extra={'profiles':profiles}))
        ordinary=int(physical_base_damage(100,0,0)*0.6)
        ordinary=guard_damage(critical_damage(ordinary,0,10,10),100)
        self.assertTrue(event.critical)
        self.assertEqual(event.modifyattack_damage_before,ordinary)
        self.assertEqual(event.damage,modifyattack_helper_damage(ordinary,submission().option,elements,raw_rand=0)[0])

    def test_guardian_calculates_but_original_defender_owns_helper_and_damage(self):
        players={0:actor('player','player','player',hp=5000),1:actor('pet','player','pet',hp=5000,defense=70)}
        result=self.resolve(players=players,extra={
            'profiles':{'player':BattleCombatProfile(100,0,100,0,0,0),'pet':BattleCombatProfile(100,0,0,100,0,0),
                        'enemy':BattleCombatProfile(100,0,0,0,0,0)},
            'guardian_registrations_by_defender_slot':{0:GuardianRegistration(guardian_slot=1)}})
        event=self.event(result)
        self.assertEqual((event.guardian_slot,event.resolved_target_slot),(1,0))
        self.assertEqual(event.modifyattack_damage_before,attribute_adjusted_damage(physical_base_damage(100,49,0),(0,0,0,0),(0,100,0,0)))
        self.assertEqual(event.modifyattack_helper_draws,1)
        self.assertEqual(result.hp_by_participant_id['pet'],5000)
        self.assertEqual(result.hp_by_participant_id['player'],5000-event.damage)

    def test_reactions_cancel_helper_and_marker_before_attackseq(self):
        for state in (BaseDamageReactState(reflect=1),BaseDamageReactState(absorb=1),BaseDamageReactState(vanish=1)):
            extra={'base_damage_react_state_by_participant_id':{'player':state}}
            result=self.resolve(rand=None,extra=extra)
            event=self.event(result)
            self.assertEqual(event.modifyattack_helper_draws,0)
            self.assertIsNone(event.modifyattack_damage_before)
            self.assertFalse(event.modifyattack_event_marked)
            with self.assertRaisesRegex(ValueError,'unowned'):
                self.resolve(rand=0,extra=extra)

    def test_zero_matching_attribute_has_no_draw_but_keeps_positive_marker(self):
        event=self.event(self.resolve(elements=(0,100,0,0),rand=None))
        self.assertEqual(event.damage,event.modifyattack_damage_before)
        self.assertEqual(event.modifyattack_helper_draws,0)
        self.assertTrue(event.modifyattack_event_marked)
        with self.assertRaisesRegex(ValueError,'unowned'):
            self.resolve(elements=(0,100,0,0),rand=0)

    def test_zero_damage_and_dodge_own_no_helper_rand(self):
        zero=dict(enemy=actor('enemy','enemy','enemy',attack=0,quick=200),rolls=hit(minimum_damage_roll_0_1=0))
        dodge=dict(rolls=replace(hit(),dodge_roll_1_10000=1))
        for args in (zero,dodge):
            event=self.event(self.resolve(rand=None,**args))
            self.assertEqual(event.modifyattack_helper_draws,0)
            self.assertFalse(event.modifyattack_event_marked)
            with self.assertRaisesRegex(ValueError,'unowned'):
                self.resolve(rand=0,**args)
        event=self.event(self.resolve(enemy=zero['enemy'],rolls=hit(minimum_damage_roll_0_1=1)))
        self.assertEqual((event.modifyattack_damage_before,event.modifyattack_helper_draws),(1,1))

    def test_sleep_confusion_and_missing_target_own_no_helper_rand(self):
        cases=(
            {'extra':{'attack_rolls':{},'base_status_runtime_by_participant_id':{'enemy':BaseBattleStatusRuntime(
                status=BaseBattleStatusState(sleep=2),work_quick=200)}}},
            {'extra':{'base_status_runtime_by_participant_id':{'enemy':BaseBattleStatusRuntime(
                status=BaseBattleStatusState(confusion=2),work_quick=200)},
                'base_status_rolls_by_participant_id':{'enemy':BaseStatusTurnRolls(1,0,0)}}},
            {'players':{}},
        )
        for args in cases:
            result=self.resolve(rand=None,**args)
            self.assertTrue(all(e.modifyattack_skill_id is None for e in result.events))
            with self.assertRaisesRegex(ValueError,'unowned'):
                self.resolve(rand=0,**args)

    def test_retarget_uses_live_adjusted_target(self):
        event=self.event(self.resolve(target=1,rolls=hit(retarget_roll=0)))
        self.assertTrue(event.retargeted)
        self.assertEqual((event.original_target_slot,event.resolved_target_slot,event.modifyattack_helper_draws),(1,0,1))

    def test_counter_ineligible_before_and_after_own_action_and_on_dodge(self):
        for quick in (5,200):
            for rolls in (hit(),replace(hit(),dodge_roll_1_10000=1)):
                result=self.resolve(enemy=actor('enemy','enemy','enemy',quick=quick),rand=None if rolls.dodge_roll_1_10000==1 else 0,
                    commands={'player':BattleCommand(BATTLE_COM_ATTACK,command2=10)},
                    extra={'attack_rolls':{'enemy':rolls,'player':hit()},'counter_rolls_by_attack_id':{}})
                self.assertEqual([e.result for e in result.events if e.is_counter],['counter_ineligible_command'])

    def test_raw_rng_requires_exact_actor_set_and_signed_int(self):
        for rng in ({},{'enemy':None},{'enemy':True},{'enemy':1.0},{'enemy':-1},{'enemy':2**31},{'enemy':0,'other':0}):
            with self.subTest(rng=rng),self.assertRaises(ValueError):
                self.resolve(extra={'modifyattack_rand_by_participant_id':rng})

    def test_exact_positive_template_slot_admission_and_population(self):
        for tempno,(graphic,slot,skill) in EXPECTED_POSITIVE_TEMPLATE_SLOTS.items():
            slots=[0]*7; slots[slot]=skill
            spawned=SimpleNamespace(participant=actor('enemy','enemy','enemy'),
                template=SimpleNamespace(tempno=tempno,graphic_id=graphic,skill_slot_ids=tuple(slots)))
            self.assertEqual(resolve_enemy_ai_modifyattack_submission(spawned,skill_slot=slot,target_slot=0,petskill_runtime=skills()),submission(tempno))
            for changes in ({'tempno':21},{'graphic_id':graphic+1},{'skill_slot_ids':tuple([skill]*7)}):
                if 'skill_slot_ids' in changes: changes['skill_slot_ids']=tuple([0]*7)
                template=SimpleNamespace(**(vars(spawned.template)|changes))
                with self.assertRaises(ValueError):
                    resolve_enemy_ai_modifyattack_submission(SimpleNamespace(participant=spawned.participant,template=template),
                        skill_slot=slot,target_slot=0,petskill_runtime=skills())
        spawned=SimpleNamespace(participant=actor('enemy','enemy','enemy'),
            template=SimpleNamespace(tempno=20,graphic_id=101532,skill_slot_ids=(0,0,0,544,0,0,0)))
        for mutation in ('option','callback','metadata','missing','extra'):
            changed=dict(skills().skills)
            if mutation=='missing':del changed[547]
            elif mutation=='extra':changed[700]=replace(changed[547],skill_id=700)
            else:changed[547]=replace(changed[547],**{'option':{'option_bytes':b'WI|21'},'callback':{'function_name':'other'},'metadata':{'cost':3}}[mutation])
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):
                resolve_enemy_ai_modifyattack_submission(spawned,skill_slot=3,target_slot=0,
                    petskill_runtime=Recovered25PetSkillRuntime(changed,'synthetic'))

    def test_typed_identity_carrier_weapon_setup_and_overlap_fail_closed(self):
        for changes in ({'skill_id':547},{'skill_slot':0},{'template_tempno':21},{'template_graphic':0},
                        {'source_target_slot':10},{'semantic_command_name':'BATTLE_COM_ATTACK'},{'skill_id':True}):
            with self.subTest(changes=changes),self.assertRaises(ValueError):replace(submission(),**changes)
        extras=(
            {'modifyattack_submissions_by_participant_id':{'enemy':object()}},
            {'modifyattack_submissions_by_participant_id':{'other':submission()}},
            {'profiles':{'player':BattleCombatProfile(100,0,100,0,0,0),
                         'enemy':BattleCombatProfile(100,0,0,0,0,0,counter_weapon_type='bow')}},
            {'command_setup_effects_by_participant_id':{'enemy':BattleCommandSetupEffects(attack_power=80)}},
            {'mdfyattack_submissions_by_participant_id':{'enemy':EnemyAiMdfyAttackSubmission('enemy',0,548,'PETSKILL_Mdfyattack',0)}},
        )
        for extra in extras:
            with self.assertRaises((ValueError,TypeError)):self.resolve(extra=extra)
        batch=EnemyAiCommonCommandBatch(commands={'enemy':BattleCommand(BATTLE_COM_ATTACK,command2=0)},
            setup_effects={},modifyattack_submissions={'enemy':submission()})
        self.assertEqual(batch.modifyattack_submissions['enemy'].semantic_command_name,'BATTLE_COM_S_MODIFYATT')
        with self.assertRaises(ValueError):
            EnemyAiCommonCommandBatch(commands={'enemy':BattleCommand(BATTLE_COM_GUARD)},
                setup_effects={},modifyattack_submissions={'enemy':submission()})


if __name__=='__main__':
    unittest.main()
