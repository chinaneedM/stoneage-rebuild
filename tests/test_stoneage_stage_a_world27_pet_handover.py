"""Batch source content, exact old joins and malformed-source preservation."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import unittest

from tools.stoneage_quest_currency_source import source_command_blocks
from tools.stoneage_quest_pet_handover_source import selector_lexeme, condition_flags

R = Path(__file__).resolve().parents[1] / 'research/recovered'


def load(n):
    return json.loads((R / n).read_text(encoding='utf-8'))


class HandoverSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = load('STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-27-PET-HANDOVER-QUEST-BRANCHES-R1.json')
        cls.scripts = cls.d['source_scripts']
        cls.branches = [b for s in cls.scripts for b in s['branches']]

    def test_all_source_files_match_original_manifest(self):
        files = {r[0]: r for r in load('STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json')['source_files']}
        self.assertEqual(len(self.scripts), 17)
        self.assertEqual(len(self.branches), 97)
        self.assertEqual(self.d['private_source_zip']['members'], 2205)
        self.assertTrue(self.d['private_source_zip']['all_member_SHA_size_CRC_verified'])
        for s in self.scripts:
            self.assertEqual([s['source_bytes'], s['source_sha256'], s['source_crc32']], files[s['path']][1:4])

    def test_exact_create_references_do_not_make_unreferenced_files_reachable(self):
        rows = {(r[0], r[1]): r for r in load('STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json')['create_rows']}
        missing = set()
        n = 0
        for s in self.scripts:
            if not s['exact_create_refs']:
                missing.add(s['path'])
            for ref in s['exact_create_refs']:
                r = rows[ref['create_path'], ref['ordinal']]
                self.assertEqual(r[4], ref['block_sha256'])
                self.assertIn([s['path'], 'EXACT_SAME_NPC_SUBTREE_PATH', s['source_sha256']], r[15])
                n += 1
        self.assertEqual(n, 15)
        self.assertEqual(missing, {'jaruga/event/bait_03a', 'jaruga/event/bait_03b', 'jaruga/event/bait_03c'})
        self.assertEqual(sum(len(s['branches']) for s in self.scripts if not s['exact_create_refs']), 42)

    def test_old_55_command_summaries_and_conditions_remain_consistent(self):
        old = {(r['script_path'], r['source_type_line']): r for r in load('STONEAGE-QUEST-STORY-MODULE-01-ORIGINAL-EXCHANGEMAN-QUEST-SOURCE-BLOCK-CATALOG-R1.json')['source_event_blocks']}
        matched = 0
        for s in self.scripts:
            for b in s['branches']:
                r = old.get((s['path'], b['type_line']))
                if r is None:
                    self.assertEqual(b['previous_QUEST01_DelPet_field_count'], 0)
                    continue
                self.assertEqual(r['source_file_sha'], s['source_sha256'])
                self.assertEqual(r['condition_expression_decoded_cp950_UTF8_sha256'], hashlib.sha256(b['event_predicate_literal'].encode()).hexdigest())
                self.assertEqual(r['source_operations']['DelPet'], b['previous_QUEST01_DelPet_field_count'])
                self.assertEqual(r['origin_class'], 'UNRESOLVED')
                matched += 1
        self.assertEqual(matched, 55)

    def test_literal_selector_namespace_and_implicit_quantity_stay_unassigned(self):
        kinds = Counter(x['kind'] for b in self.branches for x in b['DelPet_comma_lexemes'])
        self.assertEqual(kinds, {'SOURCE_PET_SELECTOR_LEXEME': 140, 'UNEXPANDED_EVDEL_MARKER': 7})
        missing_quantity = [x for b in self.branches for x in b['DelPet_comma_lexemes'] if x['kind'] == 'SOURCE_PET_SELECTOR_LEXEME' and x['explicit_quantity_literal'] is None]
        self.assertEqual([x['raw'] for x in missing_quantity], ['PET>14-524', 'PET>14-524'])
        x = selector_lexeme('PET=33-721*1')
        self.assertEqual((x['first_integer_literal'], x['second_integer_literal'], x['explicit_quantity_literal']), (33, 721, 1))
        self.assertNotIn('enemy_instance_id', x)
        self.assertNotIn('template_id', x)
        self.assertEqual(selector_lexeme('EVDEL'), {'raw': 'EVDEL', 'kind': 'UNEXPANDED_EVDEL_MARKER'})
        self.assertEqual(selector_lexeme('PET>0-95*'), {'raw': 'PET>0-95*', 'kind': 'UNQUALIFIED_LITERAL'})

    def test_original_scope_and_comment_boundary_on_synthetic_source(self):
        raw = b'#DelPet:PET>0-7\nEventNo:1\nTYPE:ACCEPT\nEVENT:PET>0-7\nDelPet:PET>0-7\nGetItem:8\nEventEnd\nEventNo:2\nTYPE:MESSAGE\nEVENT:LV>0\nGetItem:9\nEventEnd\n'
        b, = source_command_blocks(raw, {'DelPet'})
        self.assertEqual((b['scope_first_line'], b['scope_last_line']), (2, 7))
        self.assertEqual([f['key'] for f in b['ordered_control_fields']], ['EventNo', 'TYPE', 'EVENT', 'DelPet', 'GetItem'])
        for bad in [b'DelPet:EVDEL\n', b'TYPE:ACCEPT\nEVENT:LV>0\nEventEnd\nDelPet:EVDEL\n']:
            with self.assertRaises(ValueError):
                source_command_blocks(bad, {'DelPet'})

    def test_source_condition_anomaly_is_not_silently_repaired(self):
        rows = [(s, b) for s in self.scripts for b in s['branches'] if b['condition_lexical_flags']]
        (s, b), = rows
        self.assertEqual(s['path'], 'sainasu/event/genou_2')
        self.assertEqual(b['event_predicate_literal'], 'LV>0&ENDEV=42&ENDEV=4&PET>60-95,&ITEM=2758LV>0&PET>59-95&ITEM=2758')
        self.assertEqual(b['condition_lexical_flags'], ['EMPTY_COMMA_OR_AMPERSAND_COMPONENT', 'ADJACENT_SCALAR_AND_CONDITION_KEY'])
        self.assertEqual(condition_flags('LV>0&PET>59-95&ITEM=2758'), [])

    def test_raw_item_reward_order_and_duplicates_match_WORLD23(self):
        old = {(f[0], o[0]): o for f in load('STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-23-NPC-ITEM-TRANSFERS-R1.json')['files'] for o in f[6]}
        for s in self.scripts:
            for b in s['branches']:
                for f in b['ordered_control_fields']:
                    if f['key'] in {'GetItem', 'DelItem', 'GetRandItem'}:
                        self.assertEqual(old[s['path'], f['line']][:4], [f['line'], f['key'], f['value'], f['source_line_sha256']])
        s = next(s for s in self.scripts if s['path'] == 'sainasu/event/genou_2')
        candidates = [x[4] for x in s['branches'][1]['explicit_item_field_positions'] if x[1] == 'GetRandItem']
        self.assertEqual(candidates, [67, 167, 271, 473, 676, 872, 1175, 2691, 167, 271, 676, 872, 1175])
        self.assertEqual((len(candidates), len(set(candidates))), (13, 8))

    def test_duplicate_conditions_remain_two_separate_reward_branches(self):
        s = next(s for s in self.scripts if s['path'] == 'jaruga/event/kikukuev')
        a, b = s['branches']
        self.assertEqual(a['event_predicate_literal'], b['event_predicate_literal'])
        self.assertNotEqual(a['command']['line'], b['command']['line'])
        self.assertIn('GetRandItem', [f['key'] for f in a['ordered_control_fields']])
        self.assertIn('GetItem', [f['key'] for f in b['ordered_control_fields']])

    def test_only_GetPet_reward_instances_inherit_WORLD21_master_qualification(self):
        old = {r['getpet_integer']: r for r in load('STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-21-GETPET-QUEST-BRANCHES-R1.json')['original_enemy_instance_to_template_lookups']}
        joins = [r for b in self.branches for r in b['reward_GetPet_source_joins']]
        self.assertEqual(sorted(i for r in joins for i in r['ordered_instance_integers']), [93, 95, 333, 341])
        for r in joins:
            self.assertEqual(r['WORLD21_master_row_evidence'], [old[i] for i in r['ordered_instance_integers']])
        s = next(s for s in self.scripts if s['path'] == 'poru/team03')
        b, = s['branches']
        self.assertEqual(b['command']['value'], 'PET=33-721*1')
        self.assertEqual(b['reward_GetPet_source_joins'][0]['ordered_instance_integers'], [333])

    def test_all_90_item_rows_match_and_no_origin_or_runtime_is_promoted(self):
        old = {r[0]: r for p in (R / 'item-module-01').glob('*.json') for r in json.loads(p.read_text())['rows']}
        self.assertEqual(len(self.d['item01_source_joins']), 90)
        for r in self.d['item01_source_joins']:
            self.assertEqual(r['item01_row'], old[r['item_id']])
            self.assertIsNotNone(r['item01_row'][1])
        self.assertEqual(Counter(b['origin_class'] for b in self.branches), {'ORIGIN_UNRESOLVED': 97})
        self.assertEqual(Counter(b['type_literal'] for b in self.branches), {'ACCEPT': 97})
        for b in self.branches:
            self.assertTrue(b['source_EventEnd_found'])
            self.assertLess(b['type_line'], b['command']['line'])
            self.assertLess(b['command']['line'], b['scope_last_line'])
        self.assertTrue(all(v is False for k, v in self.d['limits'].items() if k != 'overall_percent'))
        self.assertIsNone(self.d['limits']['overall_percent'])


if __name__ == '__main__':
    unittest.main()
