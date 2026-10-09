import json
import unittest
from tools.stoneage_enemy_creation_audit import (
    PIN_PATH, PINNED, base_stats, definition, oracle, rng_value, vectors,
)


class EnemyCreationTests(unittest.TestCase):
    def setUp(self):
        self.rows=json.loads(PIN_PATH.read_text())['profiles']

    def fixture(self,profile='gavin'):
        identity=self.rows[profile]['identity'];ev=identity['enum_values']
        data=[0]*ev['CHAR_DATAINTNUM'];data[ev['CHAR_CHARM']]=100
        return identity,data,[63,128],[2]*200,[]

    def row(self,case,profile='gavin',sequence=0):
        return oracle(profile,*self.fixture(profile),case,sequence)

    def test_exact_accessor_name_does_not_select_strict_prefix(self):
        text='int CHAR_getIntStrict(int x){return 8;} int CHAR_getInt(int x){return 9;}'
        self.assertEqual(definition(text,'CHAR_getInt'),'int CHAR_getInt(int x){return 9;}')
        with self.assertRaises(ValueError):definition(text,'CHAR_missing')

    def test_vectors_cover_allocator_rotations_ranks_rng_levels_and_guards(self):
        cases=vectors();self.assertEqual(len(cases),4640)
        self.assertEqual(len(set(cases)),4640)
        for guard in range(1,5):self.assertEqual(sum(c[0]==guard for c in cases),8)
        self.assertEqual({c[1] for c in cases},{*range(8)})
        self.assertEqual({c[4] for c in cases},{*range(6)})

    def test_rand_macro_endpoints_and_interior_are_retained(self):
        self.assertEqual([rng_value(m,0,4) for m in range(4)],[0,2,4,1])
        self.assertEqual([rng_value(m,0,3) for m in range(4)],[0,2,3,1])
        self.assertEqual([rng_value(m,2,4) for m in range(4)],[2,3,4,2])

    def test_invalid_record_guards_preserve_cursor_sequence_without_rng(self):
        for profile in PINNED:
            for guard in range(1,5):
                row,seq=self.row((guard,0,2,0,0,0,0),profile,7)
                self.assertEqual(row,[-1,0,0,0,0,6,1]);self.assertEqual(seq,7)

    def test_full_partition_still_consumes_creator_rng_without_lookup(self):
        for p in PINNED:
            row,seq=self.row((0,7,2,0,0,0,0),p,7)
            self.assertEqual(row,[-1,15,0,2 if p=='bismarck' else 1,0,6,1])
            self.assertEqual(seq,7)

    def test_cursor_wrap_selects_first_free_slot_and_advances_sequence(self):
        row,seq=self.row((0,4,2,20,0,0,0),sequence=7)
        self.assertEqual(row[0],4);self.assertEqual(row[4:7],[7,5,1]);self.assertEqual(seq,8)

    def test_allocpoint_packs_perturbed_stats_before_growth_and_rank_uses_master(self):
        row,_=self.row((0,0,0,20,5,0,0));ev=self.rows['gavin']['identity']['enum_values']
        first=[v-2 for v in base_stats(5)]
        self.assertEqual(row[7+ev['CHAR_ALLOCPOINT']],sum(v<<(24-8*i) for i,v in enumerate(first)))
        self.assertEqual(row[7+ev['CHAR_VITAL']],290*(first[0]+10))
        self.assertEqual(row[7+ev['CHAR_PETRANK']],5)

    def test_explicit_exp_and_table_rank_adjustment_are_distinct(self):
        ev=self.rows['gavin']['identity']['enum_values']
        a,_=self.row((0,0,0,20,0,0,0));b,_=self.row((0,0,0,20,0,0,1))
        self.assertEqual(a[7+ev['CHAR_EXP']],52);self.assertEqual(b[7+ev['CHAR_EXP']],37)
        self.assertEqual(a[1],14)

    def test_real_charm_input_and_zero_ticket_object_tail_survive_composition(self):
        for p in PINNED:
            row,_=self.row((0,0,0,20,0,0,0),p);ev=self.rows[p]['identity']['enum_values']
            offset=7+ev['CHAR_DATAINTNUM']
            self.assertEqual(row[offset+ev['CHAR_WORKFIXCHARM']],100)
            for n in ('CHAR_WORKTICKETTIME','CHAR_WORKTICKETTIMESTART','CHAR_WORKOBJINDEX'):
                self.assertEqual(row[offset+ev[n]],0)

    def test_original_helper_header_closure_and_abort_traps_are_pinned(self):
        for p,r in self.rows.items():
            i=r['identity'];self.assertEqual(i['source_sha'],PINNED[p])
            for n in ('ENEMY_createEnemy','CHAR_initCharOneArray','_CHAR_complianceParameter','ITEM_equipEffect','Other_DefcharWorkInt','getFunctionPointerFromName'):
                self.assertIn(n,i['functions'])
            for suffix in ('enemy.h','enemyexptbl.h','char_base.h','version.h'):
                self.assertTrue(any(path.endswith(suffix) for path in i['header_dependency_closure']))
            self.assertNotIn('CheckCharMaxItem',r['unreachable_traps'])
            self.assertIn('ITEM_makeItemAndRegist',r['unreachable_traps'])
            self.assertIn('hashpjw',r['unreachable_traps'])


if __name__=='__main__':unittest.main()
