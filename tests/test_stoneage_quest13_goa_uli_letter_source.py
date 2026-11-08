"""QUEST13 public source-only contracts. No private assets required in CI."""
import hashlib
import json
import unittest
from tools.stoneage_quest13_goa_uli_letter_source import (
    ROOT, REPORT, CATALOG, SOURCE, ITEM_SHARDS, parse_events, git_blob,
)


class GoaUliLetterSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads(REPORT.read_text())
        cls.manifest=json.loads(SOURCE.read_text())
        cls.s=[x['events'] for x in cls.r['scripts']]
        cls.creates=cls.r['original_create_rows']

    def test_all_2205_original_inventory_and_selected_source_digests(self):
        self.assertEqual(self.r['verified_original_NPC_members'],2205)
        self.assertEqual(git_blob(SOURCE.read_bytes()),self.r['source_manifest_git_blob_sha1'])
        old={r[0]:r for r in self.manifest['source_files']}
        self.assertEqual(len(self.r['source_files']),11)
        for x in self.r['source_files']:
            self.assertEqual((x['original_bytes'],x['sha256'],x['crc32']),tuple(old[x['path']][1:4]))
        self.assertEqual(self.r['carrier'],'LATER_COMMUNITY_MIXED25_NOT_OFFICIAL_DEPLOYMENT')

    def test_original_ten_create_foreign_keys_and_separate_graphic_namespace(self):
        old={(r[0],r[1]):r for r in self.manifest['create_rows']}
        self.assertEqual(len(self.creates),10)
        self.assertEqual(sorted({x['source_script'] for x in self.creates}),sorted(x['path'] for x in self.r['scripts']))
        self.assertEqual([x['graphic_alias'] for x in self.creates],[100252,100252,100250,100250,100250,100252,100250,100252,100252,100250])
        for x in self.creates:
            raw=old[(x['path'],x['ordinal'])]
            self.assertEqual((x['start_byte'],x['end_byte'],x['original_block_sha256'],x['floor'],x['xy']),
                             (raw[2],raw[3],raw[4],raw[5],raw[7][:2]))
            self.assertEqual((x['template_token'],x['original_template_bindings']), (raw[11],raw[13]))
            self.assertEqual((x['source_script'],x['source_script_sha256']), (raw[15][0][0],raw[15][0][2]))

    def test_sixteen_original_type_blocks_against_prior_independent_quest01_catalog(self):
        self.assertEqual(git_blob(CATALOG.read_bytes()),self.r['prior_quest01_catalog_git_blob_sha1'])
        self.assertEqual([len(s) for s in self.s],[4,3,2,1,1,1,1,1,1,1])
        self.assertEqual(self.r['prior_QUEST01_TYPE_blocks_verified'],16)
        old=json.loads(CATALOG.read_text())['source_event_blocks']
        for s in self.r['scripts']:
            previous=[x for x in old if x['script_path']==s['path']]
            self.assertEqual(len(previous),len(s['events']))
            for e,p in zip(s['events'],previous):
                self.assertEqual((e['ordinal'],e['type'],e['event_number']),
                                 (p['script_block_ordinal'],p['raw_type'],p['event_number']))
                self.assertEqual(hashlib.sha256(e['raw_condition'].encode('utf-8')).hexdigest(),
                                 p['condition_expression_decoded_cp950_UTF8_sha256'])
                self.assertTrue(e['source_start_byte']<e['source_end_byte'])
                self.assertEqual(len(e['source_block_sha256']),64)

    def test_letter_exchange_order_is_literally_source_not_runtime_execution(self):
        a,b,c=self.s[:3]
        def ops(e):return [(x['key'],x['raw_operand']) for x in e['commands']]
        self.assertEqual((a[1]['event_number'],a[1]['type'],a[1]['raw_condition']),
                         (7,'REQUEST','LV>0&ITEM=2414'))
        self.assertEqual(ops(a[1]),[('GetItem','2425')])
        self.assertEqual((c[0]['event_number'],c[0]['raw_condition']),
                         (7,'NOWEV=7&ITEM=2414&ITEM=2425&ITEM!=2424'))
        self.assertEqual(ops(c[0]),[('GetItem','2424')])
        self.assertEqual((b[0]['event_number'],b[0]['raw_condition']),
                         (7,'NOWEV=7&ITEM=2414&ITEM=2424&ITEM=2425'))
        self.assertEqual(ops(b[0]),[('DelItem','2425,2424'),('EndSetFlg','7')])
        self.assertEqual(ops(b[1]),[('GetItem','2426')])
        self.assertEqual(ops(a[0]),[('GetItem','1206'),('DelItem','2426'),('EndSetFlg','8')])
        self.assertIsNone(a[0]['commands'][0]['operands'][0]['explicit_quantity'])
        self.assertIsNone(b[0]['commands'][0]['operands'][1]['explicit_quantity'])

    def test_original_condition_comma_remains_uninterpreted(self):
        self.assertEqual(self.s[2][1]['raw_condition'],'ENDEV=7,ENDEV=8&ITEM=2414')
        self.assertEqual(self.s[0][0]['raw_condition'],'NOWEV=8&ITEM=2414&ITEM=2426')
        self.assertEqual(self.s[9][0]['event_number'],7)
        self.assertTrue(self.r['source_stage']['source_only_not_a_verified_runtime_walkthrough'])
        self.assertFalse(self.r['provenance_negative_guards']['quest_branch_priority_or_condition_parser_verified'])

    def test_item_rows_match_public_source_shards_without_pretending_same_deployment(self):
        all_idx={}
        for shard in ITEM_SHARDS:
            for r in json.loads(shard.read_text())['rows']:
                all_idx[r[0]]=r
        items=self.r['item_source_evidence']
        self.assertEqual([i['item_id'] for i in items],[1206,2414,2424,2425,2426])
        self.assertEqual([len(i['original_rows']) for i in items],[2]*5)
        self.assertEqual([i['original_image_alias'] for i in items],[22068,24130,24173,24222,24222])
        self.assertTrue(all(i['tw1_original_RD_candidate_available'] for i in items))
        for item in items:
            id=item['item_id'];index=all_idx[id]
            for row in item['original_rows']:
                self.assertEqual(row['original_line_without_newline_sha256'],
                                 index[1 if row['source_table']=='itemset.txt' else 2])
        self.assertFalse(self.r['source_literal_crossfamily_item_2414']['official_same_deployment_identity_verified'])

    def test_source_six_map_dats_ten_exact_create_points_and_plane_values(self):
        m=self.r['original_map_source_observations']
        self.assertEqual([x['floor'] for x in m],[20401,20402,20403,20404,20405,20406])
        self.assertEqual(sum(len(x['source_points']) for x in m),10)
        qualified=json.loads((ROOT/'research/recovered/STONEAGE-MAP09-691-SOURCE-READY-SCENES-R1.json').read_text())
        for x in m:
            o=qualified['maps'][str(x['floor'])]
            self.assertEqual((x['source_DAT_SHA256'],x['original_DAT_bytes'],x['geometry']),
                             (o['source_sha256'],o['source_bytes'],o['geometry']))
            n=x['geometry'][0]*x['geometry'][1]
            self.assertEqual(x['original_DAT_bytes'],8+6*n)
            for point in x['source_points']:
                c=self.creates[point['create_ordinal']]
                self.assertEqual((x['floor'],point['xy']),(c['floor'],c['xy']))
                self.assertEqual(len(point['source_three_u16_values']),3)
        self.assertFalse(self.r['provenance_negative_guards']['source_map_collider_or_teleporter_verified'])

    def test_event_parser_fails_closed_and_does_not_assume_item_quantity(self):
        original=b'EventNo:7\nTYPE:ACCEPT\nEVENT:ITEM=2414&ITEM=2425\nDelItem:2425,2424\nEventEnd\n'
        parsed=parse_events(original)[0]
        self.assertEqual(parsed['source_block_sha256'],hashlib.sha256(original).hexdigest())
        self.assertEqual(parsed['commands'][0]['operands'],[
            {'item_id':2425,'explicit_quantity':None},{'item_id':2424,'explicit_quantity':None}])
        for bad in [original[:-9], b'TYPE:ACCEPT\nEVENT:ITEM=2414\nEventEnd\n',
                    original.replace(b'2425,2424',b'2425,2424?')]:
            with self.assertRaises(ValueError):parse_events(bad)

    def test_missing_official_identity_and_original_game_execution_remain_open(self):
        self.assertTrue(all(v is False for v in self.r['provenance_negative_guards'].values()))
        self.assertEqual(self.r['origin_class'],'ORIGIN_UNRESOLVED')
        self.assertEqual(self.r['status'],{'stage_A':'7_PARTIAL_2_OPEN','stage_B_wiki':'GATED',
                                           'R79':'PAUSED_NON_BLOCKING','overall_percent':None})


if __name__=='__main__':unittest.main()
