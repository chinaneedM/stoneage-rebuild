"""Mining source evidence: preserve implicit quantities and cross-source limits."""
import hashlib
import json
from pathlib import Path
import unittest
from tools.stoneage_quest08_mining_source import events, numeric_item

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'research/recovered/STONEAGE-QUEST08-MINING-APPRAISAL-AND-LIMITSHOP-SOURCE-R1.json'


class MiningSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(REPORT.read_text())

    def test_original_file_and_create_identities(self):
        d = self.data
        original = json.loads((ROOT / 'research/recovered/STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json').read_text())
        manifest = {r[0]: r[1:4] for r in original['source_files']}
        self.assertEqual(len(d['selected_original_files']), 18)
        for r in d['selected_original_files']:
            self.assertEqual([r['bytes'], r['sha256'], r['crc32']], manifest[r['path']])
        known = {(r[0], r[1]): r for r in original['create_rows']}
        self.assertEqual(len(d['source_creates']), 9)
        for r in d['source_creates']:
            old = known[r['source_file'], r['source_block_ordinal']]
            self.assertEqual([r['source_start_byte'], r['source_end_byte'], r['source_block_sha256'],
                              r['floor'], r['graphic_alias'], r['borncorner'], r['borncenter']], old[2:9])
            self.assertEqual(r['parameter_sha256'], manifest[r['parameter_file']][1])
        self.assertEqual(sorted(r['floor'] for r in d['source_creates']), [1212]*4 + [10603] + [10605]*4)

    def test_appraisal_literal_table_keeps_bare_deletions(self):
        for script_no, script in enumerate(self.data['source_scripts'][:3]):
            ore = 2469 + script_no
            certificate = 2472 + script_no
            self.assertEqual([r['type'] for r in script['events']], ['ACCEPT']*4 + ['MESSAGE'])
            quantities = [14, 11, None, None] if ore != 2471 else [14, 11, 8, 5]
            conditions = [[14], [11,12,13], [9,8,10], [7,6,5], [4,3,2,1]]
            for ordinal, event in enumerate(script['events']):
                self.assertEqual(event['event'], ','.join(f'ITEM={ore}*{n}' for n in conditions[ordinal]))
                if ordinal < 4:
                    self.assertEqual([(r['name'], r['item_id'], r['explicit_quantity']) for r in event['commands']],
                                     [('DelItem', ore, quantities[ordinal]), ('GetItem', certificate, 4-ordinal)])
                else:
                    self.assertEqual(event['commands'], [])

    def test_rescue_and_management_are_distinct(self):
        scripts = self.data['source_scripts']
        self.assertEqual([len(r['events']) for r in scripts], [5,5,5,2,3,1])
        rescue = scripts[3]['events']
        self.assertEqual([r['event'] for r in rescue], ['LV>0&ITEM!=2471', 'LV>0&ITEM=2471'])
        self.assertEqual([(r['name'], r['item_id'], r['explicit_quantity']) for r in rescue[0]['commands']],
                         [('GetItem',2471,1)])
        self.assertEqual(rescue[1]['commands'], [])
        self.assertTrue(all(not r['commands'] for s in scripts[4:] for r in s['events']))

    def test_source_shop_rates_are_not_payouts(self):
        expected = [('2469-2471','0.3','2471','0.4'), ('2472-2474','1.0','2474','1.1'),
                    ('2469-2471','1.0','2471','1.1')]
        for row, values in zip(self.data['source_limitshops'], expected):
            self.assertEqual(tuple(row['raw_numeric_controls'][k] for k in
                                   ['LimitItemNo','sell_rate','special_item','special_rate']), values)
            self.assertNotIn('actual_cash', row)
        self.assertEqual(self.data['origin_class'], 'ORIGIN_UNRESOLVED')
        self.assertTrue(all(value is False for value in self.data['boundaries'].values()))

    def test_upstream_license_and_entry_preserve_source_disagreement(self):
        upstream = self.data['source_upstream_parameters']
        self.assertEqual(len(upstream), 5)
        self.assertEqual(upstream[0]['raw_numeric_controls'],
                         {'buy_rate':'1.0','sell_rate':'0.5','ItemList':'2475-2477','LimitItemNo':'2475-2477'})
        self.assertEqual(upstream[2]['raw_numeric_controls'],
                         {'WARP':'10601,28,49','FREE':'LV>0','MONEY':'-1'})
        creates = self.data['source_upstream_creates']
        self.assertEqual(len(creates), 5)
        seller = next(r for r in creates if r['parameter_file'].endswith('ss_100_412_337'))
        self.assertEqual((seller['floor'],seller['borncorner']), (100,[412,337,412,337]))
        self.assertNotEqual(seller['floor'],10605)
        old = json.loads((ROOT/'research/recovered/STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json').read_text())
        for r in creates:
            match = next(x for x in old['create_rows'] if x[0]==r['source_file'] and x[1]==r['source_block_ordinal'])
            self.assertEqual([r['source_block_sha256'],r['floor'],r['graphic_alias'],r['borncorner']],match[4:8])
        items = json.loads((ROOT/'research/recovered/item-module-01/STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-02-R1.json').read_text())
        self.assertEqual(self.data['prior_item01_license_numeric_rows_2475_to_2477'],
                         [r for r in items['rows'] if 2475<=r[0]<=2477])

    def test_independent_item_and_map_joins(self):
        items = json.loads((ROOT / 'research/recovered/item-module-01/STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-02-R1.json').read_text())
        self.assertEqual(self.data['prior_item01_numeric_rows_2469_to_2474'],
                         [r for r in items['rows'] if 2469 <= r[0] <= 2474])
        maps = json.loads((ROOT / 'research/recovered/STONEAGE-QUEST05-598-ORIGINAL-CREATE-FLOOR-MAP-AND-WARP-CROSSWALK-R1.json').read_text())
        self.assertEqual(self.data['prior_quest05_map_qualification'],
                         [r for r in maps['floors'] if r['source_floor_id'] in {1212,10603,10605}])
        for path, expected in self.data['derived_input_blobs'].items():
            raw = (ROOT/path).read_bytes()
            self.assertEqual(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(), expected)

    def test_parser_byte_offsets_and_implicit_quantity(self):
        prefix = '# 中文說明\r\n'.encode('cp950')
        raw = prefix + b'EventNo:-1\r\nTYPE:ACCEPT\r\nEVENT:ITEM=2469*8\r\nDelItem:2469\r\nGetItem:2472*2\r\nEventEnd\r\n'
        row = events(raw)[0]
        self.assertEqual(row['start_byte'], len(prefix))
        self.assertEqual(row['end_byte'], len(raw))
        self.assertEqual(row['start_line'], 2)
        self.assertEqual(row['block_sha256'], hashlib.sha256(raw[len(prefix):]).hexdigest())
        self.assertIsNone(row['commands'][0]['explicit_quantity'])
        self.assertEqual(numeric_item('2469*1')['explicit_quantity'], 1)
        with self.assertRaises(ValueError):
            numeric_item('2469*1,2470')
        with self.assertRaises(ValueError):
            events(b'EventNo:-1\nTYPE:MESSAGE\n')


if __name__ == '__main__':
    unittest.main()
