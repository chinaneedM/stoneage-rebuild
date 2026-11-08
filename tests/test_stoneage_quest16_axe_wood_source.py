"""Public QUEST16 historical source contracts. No private original asset IO in CI."""
import json
import re
import struct
import unittest
from collections import Counter
from pathlib import Path
from tools.stoneage_quest16_axe_wood_source import (
    ROOT, SOURCE, CREATE, SCRIPTS, ITEM_IDS, SOURCE_MAPS, MAP09_PUBLIC_BLOB,
    QUEST01_PUBLIC_BLOB, parse_events, parse_creates, read_map_cell, git_blob, sha,
)

QUEST01=ROOT/'research/recovered/STONEAGE-QUEST-STORY-MODULE-01-ORIGINAL-EXCHANGEMAN-QUEST-SOURCE-BLOCK-CATALOG-R1.json'
ITEM01=ROOT/'research/recovered/item-module-01/STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-01-R1.json'
ITEM02=ROOT/'research/recovered/item-module-01/STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-02-R1.json'
MAP09=ROOT/'research/recovered/STONEAGE-MAP09-691-SOURCE-READY-SCENES-R1.json'

class Quest16SourceBoundaries(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads(SOURCE.read_text())
        cls.q=json.loads(QUEST01.read_text())
        cls.items={x[0]:x for f in (ITEM01,ITEM02) for x in json.loads(f.read_text())['rows']}
        cls.maps=json.loads(MAP09.read_text())

    def test_01_original_2205_inventory_and_legacy_catalog(self):
        r=self.r
        self.assertEqual(r['original_NPC_zip_member_count'],2205)
        self.assertEqual(r['original_source_QUEST01_public_blob'],QUEST01_PUBLIC_BLOB)
        self.assertEqual(git_blob(QUEST01.read_bytes()),QUEST01_PUBLIC_BLOB)
        self.assertEqual(r['original_RAR_sha256'], 'd71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5')
        self.assertEqual(r['source_event_total'],36)
        self.assertEqual(len(r['source_files']),7)
        sources={x['path']:x for x in r['source_files']}
        self.assertEqual(set(sources),{CREATE,*SCRIPTS,'jaruga/event/event.template'})
        for x in sources.values():
            self.assertRegex(x['sha256'],r'^[0-9a-f]{64}$')
            self.assertRegex(x['crc32'],r'^[0-9a-f]{8}$')

    def test_02_exact_five_create_source_references(self):
        x=self.r['source_creates']
        self.assertEqual(len(x),5)
        refs=sorted([v for v in self.q['source_creation_references'] if v['create_source_path']==CREATE],key=lambda x:x['create_brace_ordinal'])
        self.assertEqual(len(refs),5)
        for c,ref in zip(x,refs):
            self.assertEqual(c['ordinal'],ref['create_brace_ordinal'])
            self.assertEqual(c['floor'],ref['floorid'])
            self.assertEqual(c['graphic_alias'],ref['graphic_alias_numeric'])
            self.assertEqual(c['script_ref'],ref['original_script_path'])
            self.assertGreater(c['source_offset_end_exclusive'],c['source_offset_start'])
            self.assertTrue(len(c['name_original'])>0)
        self.assertEqual([(c['floor'],c['borncorner'][:2]) for c in x],
                         [(20508,[12,11]),(20507,[32,29]),(3300,[60,75]),(3300,[46,55]),(3000,[114,69])])
        self.assertEqual(len({c['script_ref'] for c in x}),5)

    def test_03_exact_36_prior_original_event_blocks(self):
        actual={(s['path'],e['ordinal']):e for s in self.r['source_event_blocks'] for e in s['events']}
        old={(v['script_path'],v['script_block_ordinal']):v for v in self.q['source_event_blocks'] if v['script_path'] in SCRIPTS}
        self.assertEqual(set(actual),set(old))
        for key,e in actual.items():
            o=old[key]
            self.assertEqual((e['event_no'],e['type'],e['predicate_sha256'],e['section_sha256']),
             (o['event_number'],o['raw_type'],o['condition_expression_decoded_cp950_UTF8_sha256'],
              o['source_section_decoded_cp950_normalized_UTF8_sha256']))
            self.assertTrue(e['literal_EventEnd_present'])
        self.assertEqual([len(s['events']) for s in self.r['source_event_blocks']],[10,2,6,1,17])
        self.assertEqual(Counter(e['type'] for e in actual.values()),Counter({'MESSAGE':10,'ACCEPT':19,'REQUEST':5,'CLEAN':2}))

    def test_04_original_water_can_and_axe_separate_source_paths(self):
        scripts={s['path']:s['events'] for s in self.r['source_event_blocks']}
        x=scripts['jaruga/event/20501ev1']
        self.assertEqual((x[1]['predicate'],x[1]['controls']),
           ('NOWEV=19&ITEM=2464&ITEM=2466',{'GetItem':['2465*1'],'DelItem':['2464,2466,2463'],'EndSetFlg':['19']}))
        self.assertEqual(x[2]['controls'],{'GetItem':['2463']})
        y=scripts['jaruga/event/20501ev2']
        self.assertEqual(y[1]['controls'],{'GetItem':['2464*1'],'DelItem':['2463*1']})
        self.assertEqual(x[5]['controls'],{'GetItem':['2485*1'],'DelItem':['2484*1']})
        self.assertEqual(x[8]['controls'],{'GetItem':['1838*1'],'DelItem':['1837*1']})

    def test_05_original_woodcutting_recommendation_and_flags(self):
        e={s['path']:s['events'] for s in self.r['source_event_blocks']}['jaruga/event/20501ev3']
        self.assertEqual(e[2]['controls'],{'GetItem':['2467,2484'],'DelItem':['2465*1'],'EndSetFlg':['18']})
        self.assertEqual(e[3]['controls'],e[2]['controls'])
        self.assertEqual(e[4]['predicate'],'NOWEV=18&ITEM!=2466')
        self.assertEqual(e[5]['predicate'],'LV>14')
        self.assertNotEqual(e[2]['event_no'],e[3]['event_no'])

    def test_06_fourteen_literal_merchant_branches_not_inferred_formula(self):
        tiers=self.r['original_getstone_wood_tiers']
        self.assertEqual([v['quantity_literal'] for v in tiers],list(range(1,15)))
        self.assertEqual([v['source_getstone_literal'] for v in tiers],
           ['400','1600','2400','3200','4000','4800','5600','6400','7200','8000','10000','12000','16000','20000'])
        for t in tiers:
            self.assertEqual(t['original_delitem_literals'],['2468,2478'] if t['quantity_literal']==12 else ['2468,2478,2467'])
        self.assertEqual(len({t['event_ordinal'] for t in tiers}),14)
        self.assertTrue(self.r['source_work_scope']['merchant_amounts_are_script_literals_not_proven_runtime_prices'])

    def test_07_branch_selection_and_bare_delitem_are_open(self):
        s=next(v for v in self.r['source_event_blocks'] if v['path'].endswith('20501ev5'))
        self.assertEqual(len(s['events']),17)
        self.assertEqual(s['events'][15]['predicate'],'ITEM=2478&ITEM!=2468')
        self.assertEqual(s['events'][15]['controls']['DelItem'],['2478'])
        self.assertIn('quantity_semantics_of_bare_DelItem',self.r['remaining_open'])
        self.assertIn('native_predicate_order_branch_selection',self.r['remaining_open'])

    def test_08_24_qualified_original_item_physical_rows(self):
        self.assertEqual(self.r['item_count'],12)
        self.assertEqual(self.r['source_item_rows'],24)
        self.assertEqual({x['item_id'] for x in self.r['items']},set(ITEM_IDS))
        for v in self.r['items']:
            orig=self.items[v['item_id']]
            self.assertEqual([x['sha256'] for x in v['source_rows']],orig[1:3])
            self.assertEqual([x['columns'] for x in v['source_rows']],[94,94])
            self.assertEqual([x['graphic_alias'] for x in v['source_rows']],[orig[3],orig[3]])
            self.assertEqual(v['graphic_alias'],orig[3])

    def test_09_eight_original_images_are_cross_carrier_only(self):
        ims=self.r['original_TW1_cross_carrier_images']
        self.assertEqual(self.r['original_TW1_cross_carrier_unique_image_count'],8)
        self.assertEqual(len(ims),8)
        self.assertEqual(len({x['alias'] for x in ims}),8)
        self.assertTrue(all(x['official_same_deployment_unproven'] for x in self.r['items']))
        self.assertTrue(all(v['graphic_alias'] in {x['alias'] for x in ims} for v in self.r['items']))
        for v in self.r['items']:
            self.assertEqual(v['cross_carrier_TW1_candidate_image_sha256'],
                next(i['sha256'] for i in ims if i['alias']==v['graphic_alias']))

    def test_10_MAP09_exact_source_floors_not_new_DAT_claim(self):
        r=self.r['source_map_qualification']
        self.assertEqual(r['map09_public_git_blob'],MAP09_PUBLIC_BLOB)
        self.assertEqual(git_blob(MAP09.read_bytes()),MAP09_PUBLIC_BLOB)
        self.assertEqual({x['floor'] for x in r['source_qualified_floors']},{20507,20508,3300})
        for x in r['source_qualified_floors']:
            old=self.maps['maps'][str(x['floor'])]
            self.assertEqual((x['source_dat_sha256'],x['geometry']),(old['source_sha256'],old['geometry']))
            self.assertTrue(x['original_DAT_bytes_not_read_this_work_unit'])
            self.assertTrue(old['independent_all_three_frames_equal'])
        self.assertNotIn('3000',self.maps['maps'])
        self.assertEqual(r['not_observed_floor'],3000)
        self.assertEqual(r['actual_three_plane_values_measured_this_work_unit'],0)

    def test_11_historical_unknowns_and_copyright_guard(self):
        s=SOURCE.read_text()
        self.assertNotIn('NomalWindowMsg:',s)
        self.assertNotIn('AcceptMsg:',s)
        self.assertEqual(self.r['stage_A'],{'PARTIAL':7,'OPEN':2})
        self.assertEqual((self.r['stage_B'],self.r['wiki'],self.r['R79'],self.r['overall_percent']),
                         ('GATED','GATED','PAUSED_NON_BLOCKING',None))
        self.assertFalse(self.r['source_work_scope']['original_game_started'])
        self.assertFalse(self.r['source_work_scope']['official_same_deployment_confirmed'])
        self.assertEqual(self.r['source_work_scope']['original_DAT_bytes_newly_recovered'],0)
        self.assertEqual(self.r['source_work_scope']['quest_origin'],'UNRESOLVED')

    def test_12_synthetic_CP950_event_newline_and_three_plane_parser(self):
        raw='EventNo:19\nTYPE:REQUEST\nEVENT:LV>14&ITEM=2463\nGetItem:2464*1\nEventEnd'.encode('cp950')
        self.assertEqual(parse_events(raw)[0]['controls'],{'GetItem':['2464*1']})
        self.assertEqual(parse_events(raw)[0]['event_no'],19)
        self.assertEqual(sha('LV>14&ITEM=2463'.encode()),parse_events(raw)[0]['predicate_sha256'])
        with self.assertRaises(ValueError):parse_events(b'EventNo:19\nTYPE:REQUEST\nEVENT:LV>14\n')
        d=struct.pack('<II',2,2)+struct.pack('<12H',1,2,3,4,10,11,12,13,100,101,102,103)
        self.assertEqual(read_map_cell(d,1,1),[4,13,103])
        with self.assertRaises(AssertionError):read_map_cell(d,2,0)
        with self.assertRaises(AssertionError):read_map_cell(d[:-1],0,0)

if __name__=='__main__':
    unittest.main()
