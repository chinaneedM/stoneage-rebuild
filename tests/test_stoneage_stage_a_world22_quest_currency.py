"""Published source joins and synthetic parser adversaries; no original runtime."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import unittest

from tools.stoneage_quest_currency_source import currency_blocks

R = Path(__file__).resolve().parents[1] / 'research/recovered'


def load(name):
    return json.loads((R / name).read_text(encoding='utf-8'))


class QuestCurrencySource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = load('STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-22-QUEST-CURRENCY-SOURCE-R1.json')
        cls.old = load('STONEAGE-QUEST-STORY-MODULE-01-ORIGINAL-EXCHANGEMAN-QUEST-SOURCE-BLOCK-CATALOG-R1.json')
        cls.manifest = load('STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json')
        cls.branches = [b for s in cls.report['source_scripts'] for b in s['branches']]

    def test_source_members_and_all_script_identity(self):
        z = self.report['private_source_zip']
        self.assertEqual((z['bytes'], z['members'], z['member_bytes']), (995176, 2205, 1930332))
        self.assertEqual(z['sha256'], 'c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f')
        files = {r[0]: r for r in self.manifest['source_files']}
        for s in self.report['source_scripts']:
            self.assertEqual([s['source_bytes'], s['source_sha256'], s['source_crc32']], files[s['path']][1:4])

    def test_all_99_previous_rewards_match_independent_catalog(self):
        old = {(b['script_path'], b['source_type_line']): b for b in self.old['source_event_blocks']}
        seen = set()
        for s in self.report['source_scripts']:
            for b in s['branches']:
                key = (s['path'], b['type_line'])
                if key not in old:
                    self.assertIn(s['path'], {'extra/event/osaisen', 'extra/event/osaisen2'})
                    self.assertEqual(s['exact_create_refs'], [])
                    continue
                prior = old[key]
                self.assertEqual(hashlib.sha256(b['event_predicate_literal'].encode()).hexdigest(), prior['condition_expression_decoded_cp950_UTF8_sha256'])
                if b['directive'] == 'GetStone':
                    self.assertEqual([int(b['literal'])], prior['item_numeric_refs']['GetStone'])
                    seen.add(key)
        expected = {k for k, b in old.items() if b['source_operations'].get('GetStone')}
        self.assertEqual(seen, expected)
        self.assertEqual(len(seen), 99)

    def test_sixteen_source_debits_are_additive_not_relabelled_old_rewards(self):
        debit = [b for b in self.branches if b['directive'] == 'DelStone']
        self.assertEqual(len(debit), 16)
        self.assertEqual(sum(b['previous_QUEST01_block_present'] for b in debit), 14)
        self.assertTrue(all(b['previous_QUEST01_currency_field_count'] == 0 for b in debit))
        self.assertEqual(Counter(b['literal'] for b in debit), {'LV*3': 5, '50': 3, '1200': 2, '3000': 2, '1000': 1, 'LV*40': 2, 'LV*20': 1})

    def test_currency_is_not_automatically_accept_reward(self):
        self.assertEqual(Counter(b['type_literal'] for b in self.branches), {'ACCEPT': 108, 'REQUEST': 7})
        self.assertTrue(all(b['directive'] == 'DelStone' for b in self.branches if b['type_literal'] == 'REQUEST'))
        self.assertTrue(all(b['source_EventEnd_found'] for b in self.branches))
        for b in self.branches:
            self.assertLess(b['type_line'], b['currency_line'])
            self.assertLessEqual(b['currency_line'], b['scope_last_line'])
            fields = b['ordered_control_fields']
            self.assertEqual([x['line'] for x in fields], sorted(x['line'] for x in fields))

    def test_item_joins_preserve_both_candidate_tables_and_missing_A(self):
        expected = {r[0]: r for p in (R / 'item-module-01').glob('*.json') for r in json.loads(p.read_text())['rows']}
        joins = self.report['item01_source_joins']
        self.assertEqual(len(joins), 124)
        for j in joins:
            self.assertEqual(j['item01_row'], expected[j['item_id']])
        self.assertIsNone(next(x['item01_row'] for x in joins if x['item_id'] == 2391)[1])
        self.assertEqual(self.report['counts']['item_ids_absent_from_itemset_A'], [2391])

    def test_create_joins_use_exact_path_and_source_hash(self):
        original = {(r[0], r[1]): r for r in self.manifest['create_rows']}
        n = 0
        for s in self.report['source_scripts']:
            for ref in s['exact_create_refs']:
                r = original[ref['create_path'], ref['block_ordinal']]
                self.assertIn([s['path'], 'EXACT_SAME_NPC_SUBTREE_PATH', s['source_sha256']], r[15])
                self.assertEqual([ref['floorid'], ref['graphic_literal'], ref['borncorner'], ref['borncenter']], r[5:9])
                n += 1
        self.assertEqual(n, 26)

    def test_level_expression_and_debit_direction_are_preserved(self):
        raw = b'EventNo:-1\r\nTYPE:ACCEPT\r\nEVENT:LV>49\r\nDelStone:LV*40\r\nGetItem:2756\r\nEventEnd\r\n'
        b, = currency_blocks(raw)
        self.assertEqual((b['directive'], b['literal']), ('DelStone', 'LV*40'))
        self.assertEqual(b['amount'], {'kind': 'UNEXECUTED_LEVEL_EXPRESSION', 'level_multiplier_literal': 40})
        self.assertEqual(b['source_line_sha256'], hashlib.sha256(b'DelStone:LV*40').hexdigest())
        self.assertNotIn('integer', b['amount'])

    def test_comments_and_event_boundaries_do_not_leak(self):
        raw = b'#GetStone:999\nEventNo:1\nTYPE:ACCEPT\nEVENT:ITEM=1\nGetStone:7\nEventEnd\nEventNo:2\nTYPE:REQUEST\nEVENT:LV>0\nDelStone:50\nEventEnd\n'
        a, b = currency_blocks(raw)
        self.assertEqual([a['literal'], b['literal']], ['7', '50'])
        self.assertEqual(a['event_predicate_literal'], 'ITEM=1')
        self.assertEqual(b['event_predicate_literal'], 'LV>0')
        self.assertNotIn('50', [f['value'] for f in a['ordered_control_fields']])
        with self.assertRaisesRegex(ValueError, 'outside TYPE'):
            currency_blocks(b'TYPE:ACCEPT\nEVENT:LV>0\nEventEnd\nGetStone:10\n')
        with self.assertRaisesRegex(ValueError, 'preceding TYPE'):
            currency_blocks(b'GetStone:10\n')

    def test_unknown_amount_and_duplicate_lines_are_not_coerced_or_deduplicated(self):
        raw = b'TYPE:ACCEPT\nEVENT:LV>0\nGetStone:SP*X\nGetStone:SP*X\nEventEnd\n'
        a, b = currency_blocks(raw)
        self.assertEqual(a['amount'], {'kind': 'UNRESOLVED_LITERAL'})
        self.assertEqual(a['source_line_sha256'], b['source_line_sha256'])
        self.assertNotEqual(a['currency_line'], b['currency_line'])

    def test_no_runtime_official_origin_or_percentage_promotion(self):
        self.assertTrue(all(v is False for k, v in self.report['limits'].items() if k != 'overall_restoration_percent'))
        self.assertIsNone(self.report['limits']['overall_restoration_percent'])
        self.assertFalse(self.report['original_parent_RAR_reread_this_work_unit'])
        self.assertTrue(all(b['origin_class'] == 'UNRESOLVED' for b in self.branches))


if __name__ == '__main__':
    unittest.main()
