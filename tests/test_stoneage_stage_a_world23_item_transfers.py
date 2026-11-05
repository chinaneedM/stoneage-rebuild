"""Cross-source acceptance and adversarial item quantity/punctuation cases."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import unittest

from tools.stoneage_npc_item_transfers import item_slots, script_operations

R = Path(__file__).resolve().parents[1] / 'research/recovered'


def load(name):
    return json.loads((R / name).read_text(encoding='utf-8'))


class ItemTransfers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = load('STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-23-NPC-ITEM-TRANSFERS-R1.json')
        cls.files = {f[0]: f for f in cls.d['files']}
        cls.ops = [o for f in cls.d['files'] for o in f[6]]
        cls.old = load('STONEAGE-QUEST-STORY-MODULE-01-ORIGINAL-EXCHANGEMAN-QUEST-SOURCE-BLOCK-CATALOG-R1.json')
        cls.manifest = load('STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json')

    def test_entire_batch_and_original_file_identity(self):
        self.assertEqual((len(self.files), len(self.ops)), (410, 1246))
        self.assertEqual(Counter(o[1] for o in self.ops), {'GetItem': 532, 'DelItem': 659, 'GetRandItem': 55})
        self.assertEqual(self.d['private_source_zip']['sha256'], 'c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f')
        old = {r[0]: r for r in self.manifest['source_files']}
        for p, f in self.files.items():
            self.assertEqual(f[:4], old[p][:4])

    def test_exact_function_joins_keep_service_namespaces(self):
        templates = {(r[0], r[1]): r[4] for r in self.manifest['template_rows']}
        creates = {(r[0], r[1]): r for r in self.manifest['create_rows']}
        counts = Counter()
        for p, f in self.files.items():
            for ref in f[4]:
                old = creates[ref[0], ref[1]]
                self.assertIn([p, 'EXACT_SAME_NPC_SUBTREE_PATH', f[2]], old[15])
                self.assertEqual(ref[2:8], [old[4], old[5], old[6], old[7], old[8], old[13]])
                self.assertEqual(ref[8], sorted({templates.get(tuple(x), 'UNRESOLVED') for x in old[13]}))
            fam = ','.join(sorted({x for ref in f[4] for x in ref[8]})) or 'NO_EXACT_CREATE_REFERENCE'
            for op in f[6]:
                counts[op[1] + ' / ' + fam] += 1
        self.assertEqual(dict(counts), self.d['counts']['operations_by_source_function_candidates'])
        self.assertEqual(counts['GetItem / SavePoint'], 21)
        self.assertEqual(counts['GetItem / Quiz'], 4)
        self.assertEqual(counts['GetItem / Raceman'], 1)
        self.assertEqual(counts['DelItem / WarpMan'], 111)

    def test_all_prior_QUEST01_operations_reconcile_by_source_type_and_ID_set(self):
        old = {(b['script_path'], b['source_type_line']): b for b in self.old['source_event_blocks']}
        compared = Counter()
        for p, f in self.files.items():
            for op in f[6]:
                if op[4] is None:
                    continue
                ctx = f[5][op[4]]
                prev = old.get((p, ctx['type_line']))
                if prev is None or not prev['source_operations'].get(op[1]):
                    continue
                self.assertEqual(prev['source_file_sha'], f[2])
                conditions = [r[2] for r in ctx['ordered_other_control_fields'] if r[1] == 'EVENT']
                self.assertEqual(len(conditions), 1)
                self.assertEqual(hashlib.sha256(conditions[0].encode()).hexdigest(), prev['condition_expression_decoded_cp950_UTF8_sha256'])
                ids = {c[3] for s in op[5] for c in s[2] if c[3] is not None}
                self.assertEqual(ids, set(prev['item_numeric_refs'].get(op[1], [])))
                compared[op[1]] += 1
        self.assertEqual(compared, {'GetItem': 420, 'DelItem': 442, 'GetRandItem': 50})

    def test_879_numeric_joins_keep_missing_and_table_B_only(self):
        old = {r[0]: r for p in (R / 'item-module-01').glob('*.json') for r in json.loads(p.read_text())['rows']}
        ids = {c[3] for o in self.ops for s in o[5] for c in s[2] if c[3] is not None}
        self.assertEqual(len(ids), 879)
        self.assertEqual({i for i, row in self.d['item01_joins']}, ids)
        for i, row in self.d['item01_joins']:
            self.assertEqual(row, old.get(i))
        self.assertEqual(sorted(ids - old.keys()), [2744, 2745])
        self.assertEqual(self.d['counts']['present_only_in_candidate_table_B'], [1732,1733,1734,1735,1736,1737,2391,20570,20571,20572,20760])

    def test_known_fishing_quantity_correction_survives_global_batch(self):
        f, = [f for p, f in self.files.items() if p.endswith('/nevent01_1')]
        op, = [o for o in f[6] if o[1] == 'GetItem' and '11872*2' in o[2]]
        self.assertEqual(op[2], '2437,11872*2,11863')
        self.assertEqual([s[2][0][3] for s in op[5]], [2437,11872,11863])
        self.assertEqual([s[2][0][4] for s in op[5]], [None,2,None])

    def test_savepoint_comma_and_ampersand_positions_are_not_flattened(self):
        op, = self.files['genout/sp_100_183_346'][6]
        self.assertIsNone(op[4])
        self.assertEqual(len(op[5]), 8)
        self.assertEqual([s[1] for s in op[5]].count('1642*1&2214*1'), 2)
        self.assertEqual([[c[3] for c in s[2]] for s in op[5]][2], [1642,2214])
        self.assertEqual([s[0] for s in op[5]], list(range(1,9)))

    def test_incomplete_quantity_is_not_filled_and_EVDEL_is_not_item_zero(self):
        comps = [c for o in self.ops for s in o[5] for c in s[2]]
        malformed = [c for c in comps if c[2] == 'INCOMPLETE_QUANTITY']
        self.assertEqual(malformed, [[1,'1991*','INCOMPLETE_QUANTITY',1991,None]])
        symbolic = [c for c in comps if c[2] == 'SYMBOLIC_OR_UNRESOLVED']
        self.assertEqual(len(symbolic), 6)
        self.assertTrue(all(c[1] == 'EVDEL' and c[3:] == [None,None] for c in symbolic))
        self.assertEqual(sum(c[2] == 'EMPTY_COMPONENT' for c in comps), 10)

    def test_bare_explicit_zero_and_empty_slots_differ(self):
        x = item_slots('7,7*1,7*0,7*,EVDEL,')
        self.assertEqual([s[2][0][4] for s in x], [None,1,0,None,None,None])
        self.assertEqual([s[2][0][2] for s in x], ['BARE_ITEM_INTEGER','EXPLICIT_QUANTITY','EXPLICIT_QUANTITY','INCOMPLETE_QUANTITY','SYMBOLIC_OR_UNRESOLVED','EMPTY_COMPONENT'])
        self.assertEqual([s[1] for s in x], ['7','7*1','7*0','7*','EVDEL',''])

    def test_no_TYPE_service_field_remains_outside_event_scope(self):
        contexts, ops = script_operations(b'ID:21\nGetItem:7*1&8*2,7*1&8*2\n')
        self.assertEqual(contexts, [])
        self.assertIsNone(ops[0][4])
        self.assertEqual(len(ops[0][5]), 2)
        self.assertEqual(Counter(o[1] for o in self.ops if o[4] is None), {'DelItem':150,'GetItem':26})

    def test_comments_after_end_and_next_event_do_not_leak(self):
        raw = b'#GetItem:99\r\nEventNo:1\r\nTYPE:ACCEPT\r\nEVENT:ITEM=1\r\nGetItem:7*2\r\nEventEnd\r\nDelItem:42\r\nEventNo:2\r\nTYPE:REQUEST\r\nEVENT:LV>0\r\nGetItem:8\r\nEventEnd\r\n'
        contexts, ops = script_operations(raw)
        self.assertEqual(len(ops), 3)
        self.assertEqual([o[4] for o in ops], [0,None,1])
        self.assertEqual(ops[0][3], hashlib.sha256(b'GetItem:7*2').hexdigest())
        self.assertEqual([r[2] for r in contexts[1]['ordered_other_control_fields'] if r[1]=='EVENT'], ['LV>0'])

    def test_named_backups_and_runtime_unknowns_are_preserved(self):
        self.assertTrue(self.d['named_backup_files_preserved'])
        self.assertTrue(all(p in self.files for p in self.d['named_backup_files_preserved']))
        self.assertTrue(all(v is False for k,v in self.d['limits'].items() if k!='overall_completion_percent'))
        self.assertIsNone(self.d['limits']['overall_completion_percent'])

    def test_WORLD09_frozen_unique_projection_does_not_replace_actual_positions(self):
        old = load('STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-09-GETRANDITEM-SOURCE-SLOTS-R1.json')
        lookup = {(f[0], f[5][o[4]]['type_line']): (f,o) for f in self.files.values()
                  for o in f[6] if o[1]=='GetRandItem' and o[4] is not None}
        raw_slots = raw_numbers = extra = dup_fields = order_changed = identical = 0
        for b in old['original_getranditem_blocks']:
            f,o = lookup[b['script_path'],b['type_line']]
            self.assertEqual(f[2], b['source_file_sha256'])
            nums = [c[3] for s in o[5] for c in s[2] if c[3] is not None]
            self.assertEqual(set(nums),set(b['original_item_candidates_ordered']))
            raw_slots += len(o[5]);raw_numbers += len(nums)
            extra += len(nums)-len(set(nums));dup_fields += len(nums)!=len(set(nums))
            order_changed += list(dict.fromkeys(nums))!=b['original_item_candidates_ordered']
            identical += nums==b['original_item_candidates_ordered']
        self.assertEqual((raw_slots,raw_numbers,extra,dup_fields,order_changed,identical),(960,959,241,26,26,10))
        self.assertEqual(old['counts']['candidate_positions'],718)  # Frozen historical projection.
        c = self.d['WORLD09_additive_correction']
        self.assertEqual(c['actual_source_integer_positions'],959)
        self.assertEqual(c['actual_source_empty_positions'],1)
        self.assertFalse(c['actual_random_probability_proven'])
        self.assertFalse(c['old_WORLD09_JSON_and_QUEST01_JSON_rewritten'])


if __name__ == '__main__':
    unittest.main()
