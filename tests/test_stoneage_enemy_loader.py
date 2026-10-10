import json
import unittest
from tools.stoneage_enemy_loader_audit import (
    PIN_PATH, PROFILES, c_atoi, definition, fields, fixture, input_lines,
    loaded_oracle, eligible, birth_expectation,
)


class EnemyLoaderTests(unittest.TestCase):
    def setUp(self):self.receipt=json.loads(PIN_PATH.read_text())
    def identity(self,profile):return self.receipt['profiles'][profile]['identity']
    def load(self,profile,kind):return loaded_oracle(profile,self.identity(profile),*fixture(self.identity(profile),kind),32,32)

    def test_source_definition_supports_FILE_pointer_and_exact_names(self):
        text='FILE *open_realop_file_extra(int x){return 0;}\nFILE *open_realop_file(int x){return 1;}'
        self.assertEqual(definition(text,'open_realop_file'),'FILE *open_realop_file(int x){return 1;}')

    def test_atoi_prefix_is_not_float_or_strict_integer_parser(self):
        self.assertEqual([c_atoi(v) for v in (b'4.50',b' -2tail',b'',b'NULL',b'+17')],[4,-2,0,0,17])
        with self.assertRaises(ValueError):c_atoi(b'2147483648')

    def test_high_byte_delimiter_behavior_stays_profile_specific(self):
        raw=b'\x81,AB,0'
        self.assertEqual(fields('gavin',raw),[b'\x81,AB',b'0'])
        self.assertEqual(fields('bismarck',raw),[b'\x81',b'AB',b'0'])

    def test_legacy_chomp_leaves_CR_and_trimming_keeps_one_leading_space(self):
        self.assertEqual(list(input_lines('gavin',b'  name,1\r\n')),[b' name,1\r'])
        self.assertEqual(list(input_lines('bismarck',b'  name,1\r\r\n')),[b'  name,1'])
        with self.assertRaises(ValueError):list(input_lines('gavin',b'   \n'))

    def test_empty_file_has_no_loaded_records(self):
        for p in PROFILES:self.assertEqual(self.load(p,'empty'),([],[]))

    def test_linking_and_level_normalization_use_actual_master_identity(self):
        for p in PROFILES:
            ts,es=self.load(p,'valid');ev=self.identity(p)['accepted_creator_identity']['enum_values']
            self.assertEqual(len(ts),1);self.assertEqual(len(es),1);self.assertEqual(es[0][0],0)
            self.assertEqual([es[0][1][ev[n]] for n in ('ENEMY_LV_MIN','ENEMY_LV_MAX')],[2,4])

    def test_partial_template_write_is_retained_when_next_cell_is_empty(self):
        for p in PROFILES:
            ts,es=self.load(p,'partial');ev=self.identity(p)['accepted_creator_identity']['enum_values']
            self.assertEqual(ts[0][0][ev['E_T_BASEVITAL']],77)
            self.assertEqual(len(es),1)
            self.assertEqual([es[0][1][ev[n]] for n in ('ENEMY_LV_MIN','ENEMY_LV_MAX')],[7,7])

    def test_duplicate_tempno_preserves_both_and_maps_first(self):
        for p in PROFILES:
            ts,es=self.load(p,'duplicate');ev=self.identity(p)['accepted_creator_identity']['enum_values']
            self.assertEqual(len(ts),2);self.assertEqual(es[0][0],0)
            self.assertEqual([t[0][ev['E_T_BASEVITAL']] for t in ts],[25,35])

    def test_ordinary_birth_filter_excludes_special_ids_equipment_and_unsafe_packing(self):
        p='gavin';i=self.identity(p);ts,es=self.load(p,'valid');ev=i['accepted_creator_identity']['enum_values']
        self.assertEqual(eligible(i,ts,es,[]),[0])
        es[0][1][ev['ENEMY_ID']]=564;self.assertEqual(eligible(i,ts,es,[]),[])
        es[0][1][ev['ENEMY_ID']]=1;es[0][1][ev['ENEMY_ITEMPROB1']]=1
        self.assertEqual(eligible(i,ts,es,[]),[])
        es[0][1][ev['ENEMY_ITEMPROB1']]=0;ts[0][0][ev['E_T_BASEVITAL']]=128
        self.assertEqual(eligible(i,ts,es,[]),[])

    def test_loaded_birth_expectation_uses_master_stats_and_zero_object_ticket(self):
        p='gavin';i=self.identity(p);ts,es=self.load(p,'valid');ev=i['accepted_creator_identity']['enum_values']
        data=[0]*ev['CHAR_DATAINTNUM'];d,w=birth_expectation(i,data,[2]*200,ts[0],es[0],20,1)
        self.assertEqual(d['CHAR_VITAL'],290*25);self.assertEqual(d['CHAR_TOUGH'],290*35)
        self.assertEqual(d['CHAR_PETRANK'],0);self.assertEqual(d['CHAR_EXP'],52)
        self.assertEqual([w[n] for n in ('CHAR_WORKTICKETTIME','CHAR_WORKTICKETTIMESTART','CHAR_WORKOBJINDEX')],[0,0,0])

    def test_real_input_pin_and_cross_profile_boundary_are_explicit(self):
        s=self.receipt['preserved_specimen']
        self.assertEqual(set(s['files']),{'gmsv/data/enemybase1.txt','gmsv/data/enemy1.txt'})
        self.assertTrue(s['gavin_own_configured_specimen'])
        self.assertTrue(s['bismarck_cross_profile_bytes_not_own_historical_data'])
        self.assertEqual(self.identity('gavin')['accepted_creator_identity']['enum_values']['E_T_DATAINTNUM'],50)
        self.assertEqual(self.identity('bismarck')['accepted_creator_identity']['enum_values']['E_T_DATAINTNUM'],49)

    def test_original_pool_and_file_helpers_are_pinned_without_freeMemory_claim(self):
        for p in PROFILES:
            i=self.identity(p)
            for n in ('memInit','allocateMemory','memEnd','ENEMYTEMP_initEnemy','ENEMY_initEnemy'):
                self.assertIn(n,i['functions'])
            self.assertNotIn('freeMemory',i['functions'])
            self.assertEqual(i['controlled_pool_bytes'],16777216)
        for n in ('open_realop_file','get_file_line_num','get_file_lines','strncpysafe2'):
            self.assertIn(n,self.identity('bismarck')['functions'])

    def test_iris_conversion_and_object_callers_remain_static_only(self):
        for p,r in self.receipt['static_provenance'].items():
            self.assertTrue(r['static_only_not_transitive_ownership_proof'])
            self.assertEqual(r['battle_creation_direct_character_object_field_writes'],0)
            self.assertTrue(r['object_allocator_calls_MAP_addNewObj'])
        boundary=self.receipt['static_provenance']['iris']['unexecuted_windows_conversion']
        self.assertEqual(boundary['status'],'OPEN');self.assertFalse(boundary['conversion_adapter_supplied'])
        self.assertEqual(boundary['Windows_API_dependencies'],['MultiByteToWideChar','WideCharToMultiByte'])


if __name__=='__main__':unittest.main()
