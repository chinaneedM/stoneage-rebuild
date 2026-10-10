import json
import unittest
from tools.stoneage_enemy_entry_exit_audit import (
    PIN_PATH, RowReader, cases_for, entry_changes, seed_targets,
)
from tools.stoneage_enemy_creation_audit import definition


class EnemyEntryExitTests(unittest.TestCase):
    def setUp(self):self.pins=json.loads(PIN_PATH.read_text())
    def identity(self,p):return self.pins['profiles'][p]['identity']

    def test_real_headers_resolve_INIT_and_FINAL_without_symbolic_substitution(self):
        for p in self.pins['profiles']:
            ev=self.identity(p)['enum_values']
            self.assertEqual(ev['BATTLE_CHARMODE_INIT'],1)
            self.assertEqual(ev['BATTLE_CHARMODE_FINAL'],6)
            self.assertEqual(ev['BATTLE_ERR_CHARAINDEX'],6)

    def test_status_table_lengths_and_character_field_names_remain_profile_specific(self):
        g=self.identity('gavin');b=self.identity('bismarck')
        self.assertEqual(g['limits']['status_end'],44);self.assertEqual(b['limits']['status_end'],12)
        self.assertEqual(g['battle_entry_field'],'charaindex');self.assertEqual(b['battle_entry_field'],'char_index')
        for i in (g,b):
            self.assertEqual(i['table_work_indexes']['StatusTbl'][0],-1)
            self.assertEqual(len(i['table_work_indexes']['MagicTbl']),i['limits']['magic_end'])

    def test_entry_does_not_establish_object_ownership_or_ticket_state(self):
        for p in self.pins['profiles']:
            i=self.identity(p);ev=i['enum_values'];changes=entry_changes(p,i,{},1)
            for n in ('CHAR_WORKOBJINDEX','CHAR_WORKTICKETTIME','CHAR_WORKTICKETTIMESTART'):
                self.assertNotIn(ev[n],changes)
            self.assertEqual(changes[ev['CHAR_WORKBATTLESIDE']],1)
            self.assertEqual(changes[ev['CHAR_WORKBATTLECOM1']],-1)

    def test_Exit_delta_retains_entry_state_but_changes_mode_and_index(self):
        for p in self.pins['profiles']:
            i=self.identity(p);ev=i['enum_values'];before={ev['CHAR_WORKBATTLEMODE']:777}
            changed=entry_changes(p,i,before,1,True)
            self.assertEqual(changed[ev['CHAR_WORKBATTLEMODE']],6)
            self.assertEqual(changed[ev['CHAR_WORKBATTLEINDEX']],-1)
            self.assertEqual(changed[ev['CHAR_WORKBATTLESIDE']],1)

    def test_positive_status_seed_excludes_object_ticket_and_stat_fields(self):
        for p in self.pins['profiles']:
            i=self.identity(p);ev=i['enum_values'];seed=seed_targets(p,i)
            self.assertIn(ev['CHAR_WORKPOISON'],seed)
            self.assertIn(ev['CHAR_WORKBATTLEFLG'],seed)
            for n in ('CHAR_WORKOBJINDEX','CHAR_WORKTICKETTIME','CHAR_WORKTICKETTIMESTART','CHAR_WORKMAXHP'):
                self.assertNotIn(ev[n],seed)
            self.assertTrue(all(0<=v<ev['CHAR_WORKDATAINTNUM'] for v in seed))

    def test_complete_delta_preserves_unrelated_work_and_clears_seeded_status(self):
        for p in self.pins['profiles']:
            i=self.identity(p);ev=i['enum_values']
            before={ev['CHAR_WORKPOISON']:777,ev['CHAR_WORKOBJINDEX']:1,ev['CHAR_WORKMAXHP']:123}
            changed=entry_changes(p,i,before,0)
            self.assertEqual(changed[ev['CHAR_WORKPOISON']],0)
            self.assertNotIn(ev['CHAR_WORKOBJINDEX'],changed);self.assertNotIn(ev['CHAR_WORKMAXHP'],changed)

    def test_natural_case_selection_covers_both_sides_and_all_ten_positions(self):
        cases=cases_for(list(range(30)));natural=cases[:-20]
        self.assertEqual(len(natural),30*2*4)
        self.assertEqual({c[3:5] for c in natural},{(s,p) for s in (0,1) for p in range(10)})
        self.assertTrue(all(c[-1]==0 for c in natural))

    def test_dirty_cases_are_separate_from_unchanged_preserved_birth_scope(self):
        cases=cases_for([4]);dirty=cases[-20:]
        self.assertTrue(all(c[:3]==(4,20,1) and c[-1]==1 for c in dirty))
        self.assertEqual({c[3:5] for c in dirty},{(s,p) for s in (0,1) for p in range(10)})

    def test_sparse_parser_preserves_zero_changes_and_checks_index_domain(self):
        r=RowReader('C 2 1 0 3 -1');self.assertEqual(r.sparse(4),{1:0,3:-1});r.done()
        for row in ('C 2 1 0 1 8','C 1 -1 0','C 1 4 0','C -1','C 5'):
            with self.assertRaises(ValueError):RowReader(row).sparse(4)

    def test_sparse_parser_rejects_truncation_extra_values_and_wrong_tag(self):
        with self.assertRaises(ValueError):RowReader('C 1 0').sparse(4)
        r=RowReader('C 0 9');self.assertEqual(r.sparse(4),{})
        with self.assertRaises(ValueError):r.done()
        with self.assertRaises(ValueError):RowReader('B 0')

    def test_function_extraction_does_not_treat_macro_call_as_definition(self):
        text='int caller(int x){if(BATTLE_CHECKINDEX(x)==0){return 0;}return 1;}'
        with self.assertRaises(ValueError):definition(text,'BATTLE_CHECKINDEX')
        self.assertTrue(definition('inline int target(int x){return x;}','target').startswith('int target'))

    def test_complete_original_functions_and_unreachable_traps_are_pinned(self):
        for p,row in self.pins['profiles'].items():
            i=row['identity']
            for name in ('BATTLE_NewEntry','_BATTLE_Exit','EntryInit','BATTLE_BadStatusAllClr','CHAR_PartyUpdate','_CHAR_setFlg'):
                self.assertIn(name,i['functions'])
            self.assertIn('_CHAR_warpToSpecificPoint',row['unreachable_traps'])
            self.assertIn('BATTLE_Index2No',row['unreachable_traps'])
            self.assertIn('CHAR_send_N_StatusString',row['unreachable_traps'])
            self.assertTrue(any(path.endswith('/battle.h') for path in i['header_dependency_closure']))
        self.assertIn('OPEN',self.pins['iris_execution'])


if __name__=='__main__':unittest.main()
