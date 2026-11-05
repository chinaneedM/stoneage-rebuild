"""Compiled SavePoint provenance and conditional ASCII reader projection."""
import hashlib
import json
from pathlib import Path
import unittest

from tools.stoneage_savepoint_item_source import ascii_copy_projection, compiled_evidence

R=Path(__file__).resolve().parents[1]/'research/recovered'


def load(n):return json.loads((R/n).read_text(encoding='utf-8'))


class SavePointSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=load('STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-24-SAVEPOINT-ITEM-ROLE-R1.json')
        cls.w23=load('STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-23-NPC-ITEM-TRANSFERS-R1.json')
        cls.g5=load('STONEAGE-GAMEPLAY05-ORIGINAL-PETSHOP-SAVEPOINT-HEAL-SOURCE-R1.json')
        cls.rows={r['path']:r for r in cls.d['source_SavePoint_rows']}

    def test_complete_compiled_identity_matches_independent_WORLD18(self):
        old=load('STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-18-BATTLE-ENTRY-BGM-SOURCE-R1.json')['mixed25_server']
        b=self.d['compiled_server']
        self.assertEqual((b['bytes'],b['sha256']),(old['exe_bytes'],old['exe_sha256']))
        self.assertEqual(b['base'],0x400000)
        self.assertEqual(b['COFF_symbols']['_NPC_UsedCheck'],0x499440)
        self.assertEqual(b['COFF_symbols']['_NPC_SavePointItemDelete'],0x498fd0)

    def test_all_22_original_parameter_members_and_CREATE_refs(self):
        old={r['source_parameter_path']:r for r in self.g5['original_CREATE_refs_and_derived_numeric_fields'] if r.get('source_function')=='npcgen_savepoint'}
        self.assertEqual(set(old),set(self.rows));self.assertEqual(len(old),22)
        for p,r in self.rows.items():
            self.assertEqual(r['source_sha256'],old[p]['source_parameter_sha256'])
            self.assertEqual(r['source_CREATE']['create_block_sha256'],old[p]['create_block_sha256'])
            self.assertEqual(r['source_Born'],old[p]['source_fields']['source_Born_triplet'])
            self.assertEqual(r['source_ID'],old[p]['source_fields']['source_save_ID_number'])

    def test_GetItem_original_order_and_line_SHA_matches_WORLD23(self):
        old={f[0]:f for f in self.w23['files']}
        n=0
        for p,r in self.rows.items():
            g=r['GetItem']
            if g is None:continue
            op,=[o for o in old[p][6] if o[1]=='GetItem']
            self.assertEqual((g['physical_line'],g['raw_literal'],g['line_sha256']),(op[0],op[2],op[3]))
            self.assertEqual(g['raw_comma_slots'],len(op[5]));n+=1
        self.assertEqual(n,21)

    def test_consumption_has_compiled_delete_target_and_distinct_modes(self):
        b=self.d['compiled_server'];calls={c['purpose']:c for c in b['call_witnesses']}
        self.assertEqual(calls['inventory_item_deletion']['target_va'],b['COFF_symbols']['__CHAR_DelItem'])
        self.assertEqual(calls['successful_condition_enters_delete_path']['target_va'],b['COFF_symbols']['_NPC_AndReduceDelete'])
        self.assertEqual(calls['talk_checks_without_consumption']['target_va'],b['COFF_symbols']['_NPC_UsedCheck'])
        self.assertEqual(calls['window_reply_requests_consumption']['target_va'],b['COFF_symbols']['_NPC_UsedCheck'])
        facts=b['manual_objdump_dataflow']
        self.assertEqual((facts['talk_UsedCheck_mode'],facts['confirmation_mode']),(0,1))
        self.assertEqual(facts['check_and_delete_inventory_slot_domain'],[5,19])
        self.assertEqual((facts['confirmation_sequence_literal'],facts['confirmation_selection_literal']),(230,4))
        self.assertEqual(facts['GetItem_role'],'ACTIVATION_REQUIREMENT_AND_CONDITIONAL_CONSUMPTION_NOT_REWARD')

    def test_compiled_copy_chain_and_key_literal(self):
        b=self.d['compiled_server'];calls={c['purpose']:c for c in b['call_witnesses']}
        self.assertEqual(calls['reader_calls_bounded_copy']['target_va'],b['COFF_symbols']['_strcpysafe'])
        self.assertEqual(b['immediates']['GetItem_reader_capacity']['value'],128)
        self.assertEqual(b['manual_objdump_dataflow']['ASCII_max_copied_bytes'],127)
        self.assertEqual([r['literal']for r in b['literals']],['GetItem',',','&','*','NOITEM'])

    def test_seven_original_fields_exceed_reader_capacity_and_keep_cut_tail(self):
        expected={'genout/sp_100_344_466':(209,7,'2'),'genout/sp_1300_29_23':(223,13,'2'),
                  'genout/sp_1400_76_104':(251,13,'1'),'genout/sp_200_406_371':(251,13,'1'),
                  'genout/sp_200_449_982':(250,13,'19'),'genout/sp_3300_71_51':(251,13,'1'),
                  'genout/sp_3400_65_48':(237,13,'2')}
        actual={p:r['GetItem'] for p,r in self.rows.items() if r['GetItem'] and r['GetItem']['copy_truncates']}
        self.assertEqual(set(actual),set(expected))
        for p,g in actual.items():
            self.assertEqual((g['raw_ASCII_bytes'],g['projected_comma_positions_not_validated_choices'],g['cut_tail_fragment']),expected[p])
            self.assertEqual(g['copied_ASCII_bytes'],127)
            self.assertEqual(g['conditional_ASCII_copy'].encode(),g['raw_literal'].encode()[:127])
        self.assertEqual(self.d['counts']['raw_comma_slots'],209)
        self.assertEqual(self.d['counts']['conditional_copied_comma_positions'],161)

    def test_short_original_fields_are_not_truncated_or_reordered(self):
        unchanged=[r['GetItem'] for r in self.rows.values() if r['GetItem'] and not r['GetItem']['copy_truncates']]
        self.assertEqual(len(unchanged),14)
        self.assertTrue(all(g['raw_literal']==g['conditional_ASCII_copy'] for g in unchanged))
        self.assertTrue(all(g['cut_tail_fragment'] is None for g in unchanged))
        self.assertIn('1642*1&2214*1',self.rows['genout/sp_100_183_346']['GetItem']['raw_literal'])

    def test_missing_field_is_conditional_success_not_fabricated_NOITEM(self):
        missing=[r for r in self.rows.values() if r['GetItem'] is None]
        self.assertEqual([r['path']for r in missing],['genout/sp_30691_87_60'])
        self.assertFalse(any(r['NOITEM_literal_in_source_file']for r in self.rows.values()))
        f=self.d['compiled_server']['manual_objdump_dataflow']
        self.assertEqual((f['GetArgStr_failure_returns'],f['missing_GetItem_after_successful_GetArgStr_returns']),(0,1))

    def test_projection_rejects_unqualified_unicode_and_preserves_exact_capacity(self):
        self.assertEqual(ascii_copy_projection('A'*127),'A'*127)
        self.assertEqual(ascii_copy_projection('A'*128),'A'*127)
        self.assertEqual(ascii_copy_projection('1*2,1*2',5),'1*2,')
        with self.assertRaises(UnicodeEncodeError):ascii_copy_projection('原物品')
        with self.assertRaises(ValueError):ascii_copy_projection('12',0)
        with self.assertRaises(ValueError):ascii_copy_projection('1\0x')

    def test_no_wrong_binary_runtime_or_official_promotion(self):
        with self.assertRaisesRegex(ValueError,'complete original'):compiled_evidence(b'MZ'+bytes(64))
        self.assertFalse(self.d['source_original_parent_RAR_reread'])
        self.assertTrue(all(v is False for k,v in self.d['limits'].items() if k!='overall_percent'))
        self.assertIsNone(self.d['limits']['overall_percent'])
        self.assertFalse(self.d['compiled_server']['manual_objdump_dataflow']['original_program_executed'])


if __name__=='__main__':unittest.main()
