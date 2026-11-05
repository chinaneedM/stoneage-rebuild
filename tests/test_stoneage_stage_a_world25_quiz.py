"""Compiled Quiz role/provenance joins; no original quiz or inventory execution."""
from collections import Counter
import json
from pathlib import Path
import unittest

from tools.stoneage_quiz_item_source import parse_quiz_reward_field, compiled_quiz

R=Path(__file__).resolve().parents[1]/'research/recovered'
def load(n):return json.loads((R/n).read_text(encoding='utf-8'))


class QuizItemSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=load('STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-25-QUIZ-ITEM-ROLE-R1.json')
        cls.w23=load('STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-23-NPC-ITEM-TRANSFERS-R1.json')
        cls.w24=load('STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-24-SAVEPOINT-ITEM-ROLE-R1.json')
        cls.rows=cls.d['source_Quiz_GetItem_rows']

    def test_same_compiled_source_has_own_reader_capacity(self):
        b=self.d['compiled_server'];old=self.w24['compiled_server']
        self.assertEqual((b['bytes'],b['sha256']),(old['bytes'],old['sha256']))
        self.assertEqual(b['immediates']['GetItem_field_capacity']['value'],256)
        self.assertEqual(old['immediates']['GetItem_reader_capacity']['value'],128)
        self.assertEqual(b['immediates']['threshold_token_capacity']['value'],32)
        self.assertEqual(b['immediates']['candidate_item_token_capacity']['value'],16)

    def test_four_original_files_and_physical_fields_match_WORLD23(self):
        old={f[0]:f for f in self.w23['files']}
        self.assertEqual(len(self.rows),4)
        for r in self.rows:
            f=old[r['path']];op,=[o for o in f[6]if o[1]=='GetItem']
            self.assertEqual((r['source_bytes'],r['source_sha256'],r['source_crc32']),tuple(f[1:4]))
            self.assertEqual(r['exact_original_CREATE_refs'],f[4])
            self.assertEqual((r['GetItem_line'],r['GetItem_line_sha256'],r['GetItem_raw_literal']),(op[0],op[3],op[2]))
            self.assertTrue(all('Quiz'in ref[8]for ref in f[4]))
        self.assertEqual(sorted(ref[3]for r in self.rows for ref in r['exact_original_CREATE_refs']),[800,812,820,840])

    def test_thresholds_are_not_reward_IDs(self):
        thresholds=[p['comparison_threshold']for r in self.rows for p in r['GetItem_source_pairs']]
        rewards=[i for r in self.rows for p in r['GetItem_source_pairs']for i in p['ordered_dot_candidate_item_ids']]
        self.assertEqual(Counter(thresholds),{1:3,100:1})
        self.assertEqual(Counter(rewards),{2754:3,2759:1})
        self.assertFalse({1,100}&set(rewards))
        for r in self.rows:
            p,=r['GetItem_source_pairs']
            self.assertEqual((p['threshold_comma_position'],p['payload_comma_position']),(1,2))

    def test_native_threshold_comparison_and_dot_candidate_namespace(self):
        b=self.d['compiled_server'];s=b['manual_objdump_semantics']
        self.assertEqual(s['threshold_scan'],'FIRST_MATCHING_ODD_COMMA_POSITION_IN_SOURCE_ORDER')
        self.assertEqual(s['comparison'],'SIGNED_SCORE_VALUE_GREATER_OR_EQUAL_THRESHOLD')
        self.assertEqual((s['threshold_position_step'],s['payload_position_relative_to_threshold']),(2,1))
        self.assertEqual([x['literal']for x in b['literals']],['GetItem','EntryItem',',','.'])
        self.assertEqual(b['signed_threshold_branch']['target'],0x4baef1)
        self.assertEqual(s['single_candidate_position'],1)

    def test_reward_attempt_reaches_make_add_and_failure_cleanup(self):
        b=self.d['compiled_server'];calls={r['purpose']:r['target_va']for r in b['call_witnesses']};symbols=b['COFF_symbols']
        self.assertEqual(calls['reward_payload_to_QuizAddItem'],symbols['_NPC_QuizAddItem'])
        self.assertEqual(calls['attempt_make_reward_item'],symbols['_ITEM_makeItemAndRegist'])
        self.assertEqual(calls['attempt_add_reward_to_inventory'],symbols['_CHAR_addItemSpecificItemIndex'])
        self.assertEqual(calls['cleanup_after_bad_inventory_slot'],symbols['__ITEM_endExistItemsOne'])
        self.assertFalse(b['manual_objdump_semantics']['guaranteed_original_reward_delivery'])

    def test_separate_entry_items_and_exact_candidate_item_rows(self):
        entry=[r['original_numeric_and_entry_fields']['EntryItem']['literal']for r in self.rows]
        self.assertEqual(Counter(entry),{'2752*1':3,'2753*1':1})
        old={r[0]:r for p in (R/'item-module-01').glob('*.json')for r in json.loads(p.read_text())['rows']}
        self.assertEqual({i for i,r in self.d['item01_source_joins']},{2752,2753,2754,2759})
        for i,r in self.d['item01_source_joins']:self.assertEqual(r,old[i])
        b=self.d['compiled_server'];calls={r['purpose']:r['target_va']for r in b['call_witnesses']}
        self.assertEqual(calls['entry_item_deletion'],b['COFF_symbols']['_NPC_EntryItemDel'])
        self.assertEqual(calls['starred_entry_item_inventory_delete'],b['COFF_symbols']['__CHAR_DelItem'])

    def test_source_pairs_preserve_order_duplicates_and_separate_candidate_delimiter(self):
        a,b=parse_quiz_reward_field('100,2759.2759.2754,1,2754')
        self.assertEqual(a['comparison_threshold'],100)
        self.assertEqual(a['ordered_dot_candidate_item_ids'],[2759,2759,2754])
        self.assertEqual(b['comparison_threshold'],1)
        self.assertEqual((b['threshold_comma_position'],b['payload_comma_position']),(3,4))
        self.assertEqual(a['payload_literal'],'2759.2759.2754')

    def test_unqualified_syntax_is_not_coerced_to_invented_item_or_quantity(self):
        for s in ['1,2754,100','score,2754','1,2754*2','1,2754&2759','1,2754.','1,']:
            with self.subTest(s=s):
                with self.assertRaises(ValueError):parse_quiz_reward_field(s)

    def test_role_overrides_preserve_raw_index_and_do_not_claim_global_item_population(self):
        for r in self.rows:
            override=r['WORLD23_role_override']
            self.assertEqual(override['odd_comma_positions'],'COMPARISON_THRESHOLD_NOT_ITEM_ID')
            self.assertTrue(override['old_raw_token_record_preserved'])
        self.assertFalse(self.d['limits']['WORLD23_raw_token_index_rewritten'])
        self.assertFalse(self.d['limits']['whole_game_unique_item_count_established'])

    def test_no_wrong_binary_runtime_or_official_claims(self):
        with self.assertRaisesRegex(ValueError,'complete original'):compiled_quiz(b'MZ')
        self.assertTrue(all(v is False for k,v in self.d['limits'].items()if k!='overall_percent'))
        self.assertIsNone(self.d['limits']['overall_percent'])
        self.assertFalse(self.d['compiled_server']['manual_objdump_semantics']['original_program_executed'])
        self.assertFalse(self.d['compiled_server']['manual_objdump_semantics']['actual_score_computation_reaudited'])


if __name__=='__main__':unittest.main()
