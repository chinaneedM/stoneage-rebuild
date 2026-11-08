"""QUEST15 public-source contracts: no private commercial payload needed in CI."""
from __future__ import annotations

import hashlib
import json
import struct
import unittest
from collections import Counter
from pathlib import Path

from tools.stoneage_quest15_bandit_source import (
    ROOT, SOURCE, SCRIPTS, ITEM_IDS, LATER_BRANCH_IDS, parse_creates,
    parse_events, sha,
)

NPC_INDEX = ROOT/'research/recovered/STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json'
QUEST01 = ROOT/'research/recovered/STONEAGE-QUEST-STORY-MODULE-01-ORIGINAL-EXCHANGEMAN-QUEST-SOURCE-BLOCK-CATALOG-R1.json'
ITEM_INDEX = ROOT/'research/recovered/item-module-01/STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-02-R1.json'


class Quest15OriginalSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads(SOURCE.read_text(encoding='utf-8'))
        cls.npc=json.loads(NPC_INDEX.read_text(encoding='utf-8'))
        cls.old=json.loads(QUEST01.read_text(encoding='utf-8'))
        cls.items=json.loads(ITEM_INDEX.read_text(encoding='utf-8'))
        cls.scripts={x['path']:x for x in cls.r['original_scripts']}

    def test_parent_archive_source_qualification_and_no_early_official_promotion(self):
        r=self.r
        self.assertEqual(r['original_carrier_NPC_zip_sha256'], 'c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f')
        self.assertEqual(r['original_carrier_ITEM01_zip_sha256'], 'cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa')
        self.assertEqual(r['original_NPC_members_source_verified'],2205)
        self.assertIn('NOT_CONFIRMED_OFFICIAL_EARLY',r['source_scope'])
        self.assertEqual(len(r['original_files']),8)
        src={x[0]:x for x in self.npc['source_files']}
        for f in r['original_files']:
            self.assertEqual((f['bytes'],f['sha256'],f['crc32']), tuple(src[f['path']][1:4]))

    def test_six_original_creates_exact_old_inventory_and_positions(self):
        rows=[x for x in self.npc['create_rows'] if x[0]=='jaruga/event/event20.create']
        self.assertEqual(len(rows),6)
        expected=[(3400,[59,66],16030),(3406,[27,14],16017),(3406,[28,17],16046),
                  (20607,[68,5],100431),(20607,[71,7],16032),(20608,[9,3],16029)]
        self.assertEqual(len(self.r['original_creates']),6)
        for i,(c,row,exp) in enumerate(zip(self.r['original_creates'], rows, expected)):
            self.assertEqual((c['ordinal'],c['source_offset_start'],c['source_offset_end_exclusive'],c['source_block_sha256']),
                             (i,row[2],row[3],row[4]))
            self.assertEqual((c['source_floor'],c['source_borncorner'][:2],c['graphic_alias_not_image_identity']),exp)
            self.assertEqual(c['script_ref'],SCRIPTS[i])
            self.assertEqual(c['function'],'changeevent')

    def test_twenty_eight_original_sections_match_old_quest01_immutable_index(self):
        prior=[x for x in self.old['source_event_blocks'] if x['script_path'] in SCRIPTS]
        self.assertEqual(len(prior),28)
        self.assertEqual(self.r['old_QUEST01_blocks_sha_and_condition_independently_matched'],28)
        self.assertEqual([x['event_count'] for x in self.r['original_scripts']],[5,6,3,6,3,5])
        self.assertEqual(self.r['original_event_total'],28)
        for old in prior:
            ev=self.scripts[old['script_path']]['events'][old['script_block_ordinal']]
            self.assertEqual((ev['event_no'],ev['type'],ev['section_sha256'],ev['predicate_sha256']),
                             (old['event_number'],old['raw_type'],old['source_section_decoded_cp950_normalized_UTF8_sha256'],old['condition_expression_decoded_cp950_UTF8_sha256']))
            self.assertTrue(ev['explicit_end_present'])

    def test_distinct_event_numbers_not_one_linear_quest(self):
        ev=[e for s in self.r['original_scripts'] for e in s['events']]
        self.assertEqual(Counter(x['type'] for x in ev),{'ACCEPT':13,'MESSAGE':13,'REQUEST':2})
        self.assertEqual({x['event_no'] for x in ev},{-1,20,21,22})
        self.assertEqual([x['source_floor'] for x in self.r['original_creates']],[3400,3406,3406,20607,20607,20608])

    def test_original_letter_consumption_exchange_and_flag_are_literal_only(self):
        e=self.scripts['jaruga/event/event20_2']['events'][0]
        self.assertEqual((e['event_no'],e['type'],e['predicate']),(21,'ACCEPT','ENDEV=20&NOWEV=21&ITEM=2488'))
        self.assertEqual(e['actions'],{'GetItem':['2489'],'DelItem':['2488'],'EndSetFlg':['21']})
        # Separately, Sara's source branch grants 2488; static references do not prove an executed handoff.
        sara=self.scripts['jaruga/event/event20_6']['events'][0]
        self.assertEqual(sara['actions']['GetItem'],['2488'])
        self.assertEqual(sara['predicate'],'NOWEV=21&ENDEV=22&ITEM!=2488')

    def test_five_way_random_pool_and_event22_are_separate(self):
        a=self.scripts['jaruga/event/event20_4']['events'][1]
        self.assertEqual((a['event_no'],a['type']), (22,'ACCEPT'))
        self.assertEqual(a['predicate'],'ENDEV=20&NOWEV=21')
        self.assertEqual(a['actions'], {'GetRandItem':['2490,2491,2492,2493,2494'],'EndSetFlg':['22']})
        # This is a random-item instruction, NOT five unconditional GetItem calls.
        for id in (2490,2491,2492,2493,2494):
            self.assertEqual(self.r['literal_GetItem_occurrences_in_exact_2205_NPC_file_scope'][str(id)],[])

    def test_high_level_161_conditional_branch_and_two_missing_catalog_items(self):
        ev=self.scripts['jaruga/event/event20_2']['events'][4]
        self.assertEqual((ev['event_no'],ev['type']),(-1,'ACCEPT'))
        self.assertEqual(ev['predicate'],'LV>79&ENDEV=20&ENDEV=21&NOWEV=161&ITEM=2744')
        self.assertEqual(ev['actions'],{'GetItem':['2745*1'],'DelItem':['2744']})
        self.assertEqual(self.r['item_2744_2745_scope']['not_found_in_private_ITEM01_13915_id_catalog'],[2744,2745])
        self.assertTrue(self.r['item_2744_2745_scope']['not_found_is_not_global_nonexistence'])

    def test_nine_original_item_rows_equal_and_cross_carrier_png_not_same_official(self):
        public={int(x[0]):x for x in self.items['rows']}
        got=self.r['original_items_with_two_original_rows_and_source_RD_candidates']
        self.assertEqual([x['item_id'] for x in got],ITEM_IDS)
        for item in got:
            iid=item['item_id']
            rows=item['two_original_94_column_rows']
            self.assertEqual([x['table'] for x in rows],['itemset.txt','itemset0710.txt'])
            self.assertTrue(all(x['original_columns']==94 for x in rows))
            self.assertEqual([x['sha256'] for x in rows],public[iid][1:3])
            self.assertEqual(item['source_itemset_image_alias'],public[iid][3])
            self.assertEqual(len(item['cross_carrier_TW1_verified_RD_candidate_png_sha256']),64)
            self.assertTrue(item['cross_carrier_not_official_same_deployment'])

    def test_getitem_literal_bound_and_absence_not_other_sources(self):
        hits=self.r['literal_GetItem_occurrences_in_exact_2205_NPC_file_scope']
        self.assertEqual({int(k):len(v) for k,v in hits.items()},
                         {2486:1,2487:1,2488:1,2489:1,2490:0,2491:0,2492:0,2493:0,2494:0,2744:0,2745:1})
        self.assertEqual(set(map(int,hits)),set(ITEM_IDS+LATER_BRANCH_IDS))
        for h in hits.values():
            for x in h:self.assertEqual(len(x['source_sha256']),64)

    def test_maps_stay_unreplayed_without_actual_same_source_dat(self):
        r=self.r['source_map_observation']
        self.assertEqual(r['source_floor_ids'],[3400,3406,20607,20608])
        self.assertEqual((r['source_DAT_raw_cells_reverified_this_unit'],r['source_map_graphics_observed_this_unit']),(0,0))
        self.assertEqual(r['status'],'EXISTING_MAP09_METADATA_JOIN_ONLY_NO_NEW_ORIGINAL_DAT_REPLAY')
        from tools.stoneage_quest15_bandit_source import PRIOR_MAP09
        map09=json.loads((ROOT/'research/recovered/STONEAGE-MAP09-691-SOURCE-READY-SCENES-R1.json').read_text())
        map10=json.loads((ROOT/'research/recovered/STONEAGE-MAP10-PUBLIC-ORIGINAL-SOURCE-CUSTODY-R1.json').read_text())
        self.assertNotIn('3400',map09['maps'])
        self.assertNotIn('3400',map10['maps'])
        self.assertEqual(len(r['previously_qualified_MAP09_sources']),3)
        for e in r['previously_qualified_MAP09_sources']:
            m=map09['maps'][str(e['floor'])]
            self.assertEqual((e['source_DAT_sha256_in_existing_MAP09'],e['original_grid_in_existing_MAP09']),
                             (m['source_sha256'],m['geometry']))
            self.assertFalse(e['this_unit_raw_DAT_sha_rechecked'])
            self.assertEqual((m['source_sha256'],m['geometry']), PRIOR_MAP09[e['floor']])
        self.assertIn('NOT_IN_PRIOR_MAP09',r['source_floor_3400'])

    def test_stage_and_unresolved_native_outcomes(self):
        r=self.r
        self.assertEqual(r['stage_A'],{'PARTIAL':7,'OPEN':2})
        self.assertEqual((r['stage_B'],r['wiki'],r['R79'],r['overall_percent']),('GATED','GATED','PAUSED_NON_BLOCKING',None))
        self.assertTrue(all(x=='UNPROVEN' for x in r['unknowns'].values()))
        self.assertEqual(len(r['catalog_relationships']),6)
        self.assertNotIn('NomalMsg:',SOURCE.read_text())

    def test_synthetic_event_parser_and_create_bounds(self):
        txt=('EventNo:22\nTYPE:ACCEPT\nEVENT:NOWEV=21\nGetRandItem:2490,2491,2492,2493,2494\nEventEnd\n').encode('cp950')
        e=parse_events(txt)
        self.assertEqual((e[0]['event_no'],e[0]['actions']), (22,{'GetRandItem':['2490,2491,2492,2493,2494']}))
        self.assertEqual(e[0]['predicate_sha256'],sha(b'NOWEV=21'))
        with self.assertRaises(ValueError):parse_events(b'EventNo:20\nTYPE:ACCEPT\nEVENT:ITEM=2488\n')
        src=b'{\nfloorid=3400\nborncorner=1,2,1,2\ngraphicname=100\ndir=1\nenemy=changeevent|file:jaruga/event/event20_1\n}'
        with self.assertRaises(AssertionError):parse_creates(src)  # all six required, no silent partial set

if __name__=='__main__': unittest.main()