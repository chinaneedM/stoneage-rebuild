"""Source contracts for two-tribe branches, anomalies and cross-carrier evidence."""
import hashlib
import json
import unittest
from tools.stoneage_quest11_two_tribes_source import ROOT,REPORT,SOURCE,CATALOG,source_events


class TwoTribesSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=json.loads(REPORT.read_text());cls.s=[s['events'] for s in cls.d['source_event_scripts']]

    def test_original_population_and_source_create_identity(self):
        old=json.loads(SOURCE.read_text());manifest={r[0]:r for r in old['source_files']}
        self.assertEqual((self.d['verified_original_NPC_members'],len(self.d['source_files'])),(2205,10))
        for r in self.d['source_files']:self.assertEqual([r['bytes'],r['sha256'],r['crc32']],manifest[r['path']][1:4])
        original=[r for r in old['create_rows'] if r[0]=='giiru/event/garunaev1.create']
        self.assertEqual(len(original),8)
        for a,b in zip(self.d['source_creates'],original):
            self.assertEqual([a['file'],a['ordinal'],a['start_byte'],a['end_byte'],a['block_sha256'],a['floor'],a['graphic_alias'],a['borncorner_raw']],b[:8])
            self.assertEqual(a['parameter_references'],b[15]);self.assertEqual(a['template_bindings'],b[13])

    def test_all_TYPE_blocks_match_independent_prior_catalog(self):
        old=json.loads(CATALOG.read_text())['source_event_blocks']
        self.assertEqual([len(s) for s in self.s],[13,6,13,13,6,15,1,1])
        self.assertEqual(self.d['prior_QUEST01_TYPE_blocks_verified'],68)
        for script in self.d['source_event_scripts']:
            prior=[r for r in old if r['script_path']==script['path']]
            for e,p in zip(script['events'],prior):
                self.assertEqual((e['ordinal'],e['type_line'],e['type']),(p['script_block_ordinal'],p['source_type_line'],p['raw_type']))
                self.assertEqual(hashlib.sha256(e['event'].encode()).hexdigest(),p['condition_expression_decoded_cp950_UTF8_sha256'])

    def test_misspelled_header_remains_noncanonical(self):
        e=self.s[5][3]
        self.assertEqual((e['header_key'],e['header_numeric_literal'],e['event_number']),('EvebtNo',-1,None))
        self.assertEqual(e['message_keys'],['NomalWinodowMsg'])
        self.assertEqual(self.s[2][9]['event'],'NOEEV=24')
        self.assertEqual(self.s[5][2]['event'],'ENDEV=25&ITEM=1,ENDEV=26&ITEM=1')
        self.assertEqual(self.s[2][10]['event'],self.s[2][11]['event'])
        self.assertNotEqual(self.s[2][10]['block_sha256'],self.s[2][11]['block_sha256'])
        self.assertEqual(sum(e['event_number'] is not None for s in self.s for e in s),67)

    def test_parallel_letter_handoffs_and_ordered_ore_synthesis(self):
        def ops(e):return [(c['name'],[(o['item_id'],o['explicit_quantity']) for o in c['operands']]) for c in e['commands']]
        self.assertEqual(ops(self.s[0][3]),[('GetItem',[(2501,1)]),('DelItem',[(2500,None)])])
        self.assertEqual(ops(self.s[3][3]),[('GetItem',[(2502,1)]),('DelItem',[(2499,None)])])
        for s in [self.s[2],self.s[5]]:
            self.assertEqual(s[0]['event'],'ITEM=2503&ITEM=2504&ITEM=2414')
            self.assertEqual(ops(s[0]),[('DelItem',[(2503,1),(2504,1)]),('GetItem',[(2506,None)])])
        self.assertEqual(ops(self.s[0][11]),[('GetItem',[(2393,1)]),('DelItem',[(2391,1),(2395,1)])])
        self.assertEqual([self.s[n][k]['other_numeric_controls'] for n,k in [(2,4),(5,6),(0,6),(3,6)]],
                         [[{'name':'EndSetFlg','value':v}] for v in [23,24,25,26]])

    def test_ore_vendors_and_shell_replacements_are_distinct(self):
        for n,item in [(6,2504),(7,2503)]:
            e=self.s[n][0];self.assertEqual(e['event'],'ENDEV=25,ENDEV=26')
            self.assertEqual(e['commands'],[{'name':'GetItem','raw_operand':str(item),'operands':[{'item_id':item,'explicit_quantity':None}]}])
            self.assertEqual(e['other_numeric_controls'],[{'name':'DelStone','value':3000}])
        for n in [1,4]:self.assertEqual(self.s[n][0]['other_numeric_controls'],[{'name':'DelStone','value':1200}])
        self.assertEqual(self.s[1][3]['commands'][0]['raw_operand'],'2414*1')
        self.assertEqual(self.s[4][3]['commands'][0]['raw_operand'],'2414')
        self.assertEqual(self.s[5][4]['commands'][0]['raw_operand'],'2883')

    def test_original_item_rows_and_source_map_points(self):
        items={r['item_id']:r for r in self.d['source_item_evidence']}
        self.assertEqual(set(items),{1,2391,2393,2395,2414,2499,2500,2501,2502,2503,2504,2506,2883})
        self.assertEqual(sum(len(r['source_row_reconstructions']) for r in items.values()),25)
        self.assertIsNone(items[2391]['source_item01_numeric_row'][1]);self.assertFalse(items[2391]['qualified_icon_present'])
        self.assertEqual(sum(r['qualified_icon_present'] for r in items.values()),12)
        for r in items.values():
            for row in r['source_row_reconstructions']:
                self.assertEqual(row['sha256'],r['source_item01_numeric_row'][1 if row['table']=='itemset.txt' else 2])
        maps=self.d['source_map_observations'];self.assertEqual([m['floor'] for m in maps],[31002,31003,31102,31103,31205])
        prior=json.loads((ROOT/'research/recovered/STONEAGE-MAP09-691-SOURCE-READY-SCENES-R1.json').read_text())
        seen=[]
        for m in maps:
            self.assertEqual(m['source_DAT_sha256'],prior['maps'][str(m['floor'])]['source_sha256'])
            for p in m['source_points']:
                c=self.d['source_creates'][p['source_create_ordinal_or_target']];seen.append(c['ordinal'])
                self.assertEqual((m['floor'],p['xy']),(c['floor'],c['borncorner_raw'][:2]))
                self.assertEqual(len(p['original_three_u16_values']),3)
        self.assertEqual(sorted(seen),list(range(8)))

    def test_parser_never_repairs_or_swallows_malformed_blocks(self):
        raw=b'EvebtNo:-1\nTYPE:MESSAGE\nEVENT:NOEEV=24\nDelItem:1*1,2\nNomalWinodowMsg:x\nEventEnd\n'
        e=source_events(raw)[0]
        self.assertIsNone(e['event_number']);self.assertEqual(e['block_sha256'],hashlib.sha256(raw).hexdigest())
        self.assertEqual(e['commands'][0]['operands'],[{'item_id':1,'explicit_quantity':1},{'item_id':2,'explicit_quantity':None}])
        for bad in [b'TYPE:MESSAGE\nEVENT:ITEM=1\nEventEnd\n',raw[:-9],raw.replace(b'1*1,2',b'1*1,2?')]:
            with self.assertRaises(ValueError):source_events(bad)

    def test_dependencies_and_unpromoted_runtime_boundaries(self):
        for path,digest in self.d['derived_input_blobs'].items():
            raw=(ROOT/path).read_bytes();self.assertEqual(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),digest)
        self.assertTrue(all(v is False for v in self.d['boundaries'].values()))
        self.assertEqual(self.d['origin_class'],'ORIGIN_UNRESOLVED');self.assertIsNone(self.d['status']['overall_percent'])


if __name__=='__main__':unittest.main()
