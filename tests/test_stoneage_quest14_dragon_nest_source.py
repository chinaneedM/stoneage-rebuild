"""Public, offline QUEST14 derived-source checks; do not fetch proprietary assets."""
import json
import re
import unittest
from collections import Counter
from pathlib import Path

from tools.stoneage_quest14_dragon_nest_source import ROOT, SOURCE, git_blob, read_map_cell, parse_events, sha

NPC = ROOT/'research/recovered/STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json'
QUEST01 = ROOT/'research/recovered/STONEAGE-QUEST-STORY-MODULE-01-ORIGINAL-EXCHANGEMAN-QUEST-SOURCE-BLOCK-CATALOG-R1.json'
ITEM = ROOT/'research/recovered/item-module-01/STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-02-R1.json'


class Quest14OriginalBoundaries(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads(SOURCE.read_text())
        cls.npc=json.loads(NPC.read_text())
        cls.quest01=json.loads(QUEST01.read_text())
        cls.item=json.loads(ITEM.read_text())
        cls.scripts={x['path']:x for x in cls.r['scripts']}

    def test_source_identity_original_inventory_preserved(self):
        r=self.r
        self.assertEqual(r['source_parent_RAR_sha256'],self.npc['original_rar_sha256'])
        self.assertEqual(r['source_parent_RAR_original_bytes'],self.npc['original_rar_bytes'])
        self.assertEqual((r['source_original_NPC_members_checked'],r['source_original_NPC_member_bytes_checked']),(2205,1930332))
        self.assertEqual(git_blob(NPC.read_bytes()),r['public_source_NPC_inventory_git_blob'])
        self.assertEqual(git_blob(QUEST01.read_bytes()),r['public_SOURCE_QUEST01_index_git_blob'])
        self.assertEqual(len(r['original_source_files']),6)  # 1 CREATE + 4 scripts + 1 shared template
        public={x[0]:x for x in self.npc['source_files']}
        for x in r['original_source_files']:
            row=public[x['path']]
            self.assertEqual((x['bytes'],x['original_sha256'],x['source_crc32']),tuple(row[1:4]))

    def test_four_actual_create_blocks_exact_source_index(self):
        rows=[x for x in self.npc['create_rows'] if x[0]=='jaruga/event/event17.create']
        self.assertEqual(len(rows),4)
        for i,c in enumerate(self.r['original_create_rows']):
            row=rows[i]
            self.assertEqual((c['ordinal'],c['source_offset_start'],c['source_offset_end_exclusive'],c['original_sha256']),(i,row[2],row[3],row[4]))
            self.assertEqual((c['floor'],c['graphic_alias'],c['original_borncorner']),(row[5],row[6],row[7]))
            self.assertEqual((c['floor'],c['original_borncorner'][:2]),(20807,[7,8]) if i==0 else (20807,[23,6]) if i==1 else (20807,[41,14]) if i==2 else (20801,[13,63]))
            self.assertEqual(c['script_ref'],f'jaruga/event/event17_{i+1}')
            self.assertEqual(c['enemy_function'],'changeevent')

    def test_event10_same_as_existing_independent_quest01_index(self):
        src=[x for x in self.quest01['source_event_blocks'] if x['script_path'] in self.scripts]
        self.assertEqual(len(src),10)
        self.assertEqual(self.r['script_total_events'],10)
        for item in src:
            event=self.scripts[item['script_path']]['events'][item['script_block_ordinal']]
            self.assertEqual((event['section_sha256'],event['predicate_sha256'],event['event_no'],event['type']),
                             (item['source_section_decoded_cp950_normalized_UTF8_sha256'],item['condition_expression_decoded_cp950_UTF8_sha256'],item['event_number'],item['raw_type']))
        self.assertEqual([len(v['events']) for v in self.r['scripts']],[2,2,2,4])

    def test_three_dragon_shared_predicate_distinct_outcomes(self):
        expected={1:2462,2:2460,3:2461}
        for i,reward in expected.items():
            event=self.scripts[f'jaruga/event/event17_{i}']['events'][0]
            self.assertEqual((event['type'],event['event_no']),('ACCEPT',17))
            self.assertEqual(event['predicate'],'NOWEV=17&ITEM=2457&ITEM=2458&ITEM=2459&ITEM=2505')
            self.assertEqual(event['actions'],{'GetItem':[str(reward)], 'DelItem':['2457,2458,2459,2505'],'EndSetFlg':['17']})
            self.assertEqual((self.scripts[f'jaruga/event/event17_{i}']['events'][1]['event_no'],self.scripts[f'jaruga/event/event17_{i}']['events'][1]['type']),(-1,'MESSAGE'))
            self.assertEqual(event['has_eventend'],True)

    def test_guardian_four_distinct_control_branches_not_runtime(self):
        events=self.scripts['jaruga/event/event17_4']['events']
        self.assertEqual([(v['event_no'],v['type']) for v in events],[(17,'ACCEPT'),(17,'REQUEST'),(17,'MESSAGE'),(-1,'MESSAGE')])
        self.assertEqual([x['predicate'] for x in events],['NOWEV=17&ITEM!=2505','LV>0&ITEM!=2505','NOWEV=17&ITEM=2505','ENDEV=17'])
        self.assertEqual([x['actions']['GetItem'] for x in events],[['2505'],['2505'],[],[]])
        self.assertEqual([x['actions']['EndSetFlg'] for x in events],[[],[],[],[]])

    def test_original_item_row_hard_identity_and_cross_carrier_image(self):
        r=self.r
        self.assertEqual(r['source_item_physical_rows_verified'],14)
        self.assertEqual(r['seven_item_IDs'],[2457,2458,2459,2460,2461,2462,2505])
        src={x[0]:x for x in self.item['rows']}
        for item in r['original_item_94_column_rows']:
            x=src[item['item_id']]
            self.assertEqual(item['row_identity'],'IDENTICAL_RAW_LINE')
            self.assertEqual(len(item['two_source_original_lines']),2)
            self.assertEqual([a['source_sha256'] for a in item['two_source_original_lines']],x[1:3])
            self.assertEqual(item['two_source_original_lines'][0]['source_graphic_alias'],x[3])
            self.assertEqual(item['separate_TW1_carrying_source_graphic_alias'],x[3])
            self.assertEqual(x[8:10],['REAL_RD_DECODED_CROSS_CARRIER']*2)
            self.assertTrue(item['cross_carrier_not_proof_of_same_official_deployment'])

    def test_bounded_negative_jade_source_and_positive_hits(self):
        hits=self.r['literal_GetItem_occurrences_all_2205_NPC_files']
        self.assertEqual({x:len(hits[str(x)]) for x in [2457,2458,2459,2505,2460,2461,2462]},
                         {2457:0,2458:0,2459:0,2505:2,2460:1,2461:1,2462:1})
        for x in [2460,2461,2462]:
            self.assertTrue(all(s['file'].startswith('jaruga/event/event17_') for s in hits[str(x)]))
        for item in hits.values():
            for h in item:
                self.assertRegex(h['file_sha256'],r'^[0-9a-f]{64}$')
        self.assertEqual(self.r['unknowns']['dragon_jade_origin_in_this_original_NPC_inventory'],'NO_MATCHING_GetItem_LITERAL_FOUND')

    def test_source_dat_geometry_and_four_exact_cells(self):
        self.assertEqual(self.r['original_DAT_map_count'],2)
        by={m['floor']:m for m in self.r['two_original_dat_maps']}
        self.assertEqual((by[20801]['dimensions'],by[20801]['original_bytes']),([70,70],29408))
        self.assertEqual((by[20807]['dimensions'],by[20807]['original_bytes']),([50,50],15008))
        self.assertEqual(by[20801]['source_positions'],[{'create_ordinal':3,'at':[13,63],'actual_three_original_u16':[4001,0,49152]}])
        self.assertEqual(by[20807]['source_positions'],[
            {'create_ordinal':0,'at':[7,8],'actual_three_original_u16':[4004,0,49152]},
            {'create_ordinal':1,'at':[23,6],'actual_three_original_u16':[4001,0,49152]},
            {'create_ordinal':2,'at':[41,14],'actual_three_original_u16':[4008,0,49152]}])
        for m in by.values():
            self.assertRegex(m['original_sha256'],r'^[0-9a-f]{64}$')
            self.assertTrue(m['scene_thumbnail_is_modern_source_observer_not_original_client'])

    def test_public_source_contract_not_an_original_game_runtime(self):
        self.assertIn('NOT_CONFIRMED_OFFICIAL_EARLY_VERSION',self.r['source_scope'])
        self.assertEqual(self.r['stage_A'],{'PARTIAL':7,'OPEN':2})
        self.assertEqual((self.r['stage_B'],self.r['wiki'],self.r['R79'],self.r['overall_percent']),('GATED','GATED','PAUSED_NON_BLOCKING',None))
        self.assertTrue(all(v=='UNPROVEN' for k,v in self.r['unknowns'].items() if k!='dragon_jade_origin_in_this_original_NPC_inventory'))
        self.assertEqual(len([e for e in self.r['catalog_relationships'] if e['relation']=='dragon_source_condition_exchange_to_reward']),3)
        self.assertFalse(any('NomalMsg:' in SOURCE.read_text() for _ in [0]))

    def test_synthetic_three_plane_parser_and_cp950_event_parser(self):
        # Synthetic data: ensures public tooling decodes sequential planes, not interleaved u16.
        import struct
        mapbuf=struct.pack('<II',2,2)+struct.pack('<12H',1,2,3,4,10,11,12,13,100,101,102,103)
        self.assertEqual(read_map_cell(mapbuf,1,1),[4,13,103])
        text='EventNo:17\nTYPE:REQUEST\nEVENT:LV>0&ITEM!=2505\nGetItem:2505\nEventEnd\n'.encode('cp950')
        result=parse_events(text)
        self.assertEqual([(x['event_no'],x['type'],x['actions']['GetItem']) for x in result],[(17,'REQUEST',['2505'])])
        with self.assertRaises(AssertionError):read_map_cell(mapbuf,2,1)


if __name__=='__main__':unittest.main()
