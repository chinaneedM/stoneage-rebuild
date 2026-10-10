import json
import unittest
from tools.stoneage_battle_pool_audit import PIN_PATH, cases_for, verify_pool, actor_delta


class BattlePoolTests(unittest.TestCase):
    def setUp(self):self.pins=json.loads(PIN_PATH.read_text())
    def identity(self,p):return self.pins['profiles'][p]['identity']

    def test_bounded_composition_pins_original_bootstrap_rollback_and_Finish(self):
        for p in self.pins['profiles']:
            i=self.identity(p)
            for n in ('BATTLE_initBattleArray','BATTLE_SearchTask','BATTLE_CreateBattle','BATTLE_DeleteBattle',
                      'BATTLE_CreateVsEnemy','_BATTLE_ExitAll','BATTLE_GetExpGold','BATTLE_GetProfit','BATTLE_Finish'):
                self.assertIn(n,i['functions'])
            self.assertEqual(i['battle_capacity'],3);self.assertEqual(i['enemy_capacity'],3)

    def test_constructor_whole_structure_zeroing_remains_profile_specific(self):
        self.assertFalse(self.identity('gavin')['constructor_zeroes_whole_BATTLE'])
        self.assertTrue(self.identity('bismarck')['constructor_zeroes_whole_BATTLE'])

    def test_original_player_entry_and_profit_paths_remain_abort_traps(self):
        for p,row in self.pins['profiles'].items():
            for n in ('BATTLE_PartyNewEntry','BATTLE_GetExp','BATTLE_GetDuelPoint'):
                self.assertIn(n,row['unreachable_traps'])
            self.assertIn('OPEN',self.pins['iris_execution'])

    def test_all_input_records_and_RNG_modes_have_rollback_and_Finish(self):
        cases=cases_for([3,9])
        for index in (3,9):
            for mode in range(4):
                self.assertEqual(sum(c[:2]==(index,mode) and c[2]==0 for c in cases),1)
                self.assertEqual(sum(c[:2]==(index,mode) and c[2]==1 for c in cases),1)

    def test_invalid_array_prefixes_and_capacity_failure_are_separate(self):
        cases=cases_for([3,9]);self.assertEqual({c[3] for c in cases if c[2]==0},{0,1,2,3})
        self.assertEqual([c for c in cases if c[2]==2],[(3,m,2,3) for m in range(4)])
        self.assertEqual({c[3] for c in cases if c[2]==1},{1,2,3})

    def test_pool_oracle_accepts_exact_golden_observation(self):
        line='P 1 3 0 1 1 1 2 1 -1 3 0 0 0 0 6 8 0 1 1 1 1'
        for p in self.pins['profiles']:verify_pool(self.identity(p),line)

    def test_pool_oracle_rejects_total_constructor_and_world_corruption(self):
        line='P 1 3 0 1 1 1 2 1 -1 3 0 0 0 0 6 8 0 1 1 1 1'.split()
        for at in (1,4,10,17,18):
            altered=line.copy();altered[at]=str(int(altered[at])+1)
            with self.assertRaises(ValueError):verify_pool(self.identity('gavin'),' '.join(altered))
        with self.assertRaises(ValueError):verify_pool(self.identity('gavin'),' '.join(line)+' 0')

    def test_arena_reuse_tracks_real_battle_index_without_changing_ownership_ticket(self):
        for p in self.pins['profiles']:
            i=self.identity(p);ev=i['accepted_entry_identity']['enum_values']
            before={ev['CHAR_WORKOBJINDEX']:0,ev['CHAR_WORKTICKETTIME']:0,ev['CHAR_WORKTICKETTIMESTART']:0}
            delta=actor_delta(p,i,before,2,False)
            self.assertEqual(delta[ev['CHAR_WORKBATTLEINDEX']],2)
            for n in ('CHAR_WORKOBJINDEX','CHAR_WORKTICKETTIME','CHAR_WORKTICKETTIMESTART'):
                self.assertNotIn(ev[n],delta)

    def test_full_Exit_oracle_requires_FINAL6_and_minus_one_index(self):
        for p in self.pins['profiles']:
            i=self.identity(p);ev=i['accepted_entry_identity']['enum_values']
            delta=actor_delta(p,i,{},2,True)
            self.assertEqual(delta[ev['CHAR_WORKBATTLEMODE']],6)
            self.assertEqual(delta[ev['CHAR_WORKBATTLEINDEX']],-1)

    def test_adapters_and_actual_mode_enums_are_explicit(self):
        for p in self.pins['profiles']:
            i=self.identity(p)
            self.assertEqual(i['battle_mode_enum_values']['BATTLE_MODE_NONE'],0)
            self.assertIn('descriptor-1',i['adapters'])
            self.assertIn('encounter table/NULL selector',i['adapters'])
            self.assertIn('Doujyou_GetEnemy',i['unreachable_file_local_signature_sha256'])
            self.assertTrue(any(x.endswith('/battle.h') for x in i['header_dependency_closure']))


if __name__=='__main__':unittest.main()
