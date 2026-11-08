"""Checks only public bounded evidence; cannot prove original runtime gameplay."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
REC=ROOT/'research/recovered'
REPORT=REC/'STONEAGE-QUEST31-FOUR-VILLAGE-EVENT09-12-SOURCE-R1.json'
QUEST01=REC/'STONEAGE-QUEST-STORY-MODULE-01-ORIGINAL-EXCHANGEMAN-QUEST-SOURCE-BLOCK-CATALOG-R1.json'
CHAR01=REC/'STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json'


def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()

class Quest31SourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads(REPORT.read_text('utf8'))
        cls.q=json.loads(QUEST01.read_text('utf8'))
        cls.ch=json.loads(CHAR01.read_text('utf8'))
        cls.scripts=cls.r['source_scripts']
        cls.events=[(s['path'],e) for s in cls.scripts for e in s['events']]

    def test_01_indices_pinned_by_actual_git_blob(self):
        for path,expected in ((QUEST01,'52db8b4b6cd43cd2afa4a8d2e8460f214933f5e2'),
                              (CHAR01,'a088b61a3212f7049e7793f587123ffb29bebad7')):
            self.assertEqual(blob(path.read_bytes()),expected)
        self.assertEqual(self.r['initial_remote']['preserved_CURRENT_git_blob'],'c89e0e33537990aa2132b47c40fef49a985a935c')

    def test_02_global_catalog_count_is_census_not_new_content(self):
        self.assertEqual(len(self.q['source_scripts']),295)
        self.assertEqual(len(self.q['source_event_blocks']),1349)
        c=self.r['source_module_census']
        self.assertEqual(sum(c['prior_QUEST01_directories'].values()),295)
        self.assertEqual(len(c['prior_QUEST01_directories']),14)
        self.assertEqual([c['selected_original_scripts_already_in_QUEST01'],c['selected_original_TYPE_already_in_QUEST01']],[4,18])
        self.assertEqual([c['newly_discovered_original_scripts'],c['newly_discovered_original_TYPE']],[0,0])

    def test_03_every_script_exact_old_sha_and_crc(self):
        index={s['path']:s for s in self.q['source_scripts']}
        self.assertEqual([s['path'] for s in self.scripts],
          [f'sainasu/event/event{n:02}' for n in range(9,13)])
        self.assertEqual([len(s['events']) for s in self.scripts],[3,5,5,5])
        for s in self.scripts:
            old=index[s['path']]
            self.assertEqual((s['bytes'],s['sha256'],s['crc32']),
               (old['original_size'],old['original_sha256'],old['original_crc32']))

    def test_04_every_event_section_and_condition_sha_and_line(self):
        old={(x['script_path'],x['script_block_ordinal']):x for x in self.q['source_event_blocks']}
        self.assertEqual(len(self.events),18)
        for p,e in self.events:
            o=old[(p,e['ordinal'])]
            self.assertEqual((e['type'],e['event_no'],e['source_type_line'],e['section_sha256']),
                (o['raw_type'],o['event_number'],o['source_type_line'],o['source_section_decoded_cp950_normalized_UTF8_sha256']))
            self.assertEqual(e['condition_sha256'],o['condition_expression_decoded_cp950_UTF8_sha256'])
            self.assertEqual(hashlib.sha256(e['condition_literal'].encode()).hexdigest(),e['condition_sha256'])

    def test_05_four_original_create_positions_not_one_map(self):
        creates=self.r['source_create_records']
        self.assertEqual([r['floor'] for r in creates],[1200,1300,1400,11107])
        self.assertEqual([r['graphic_alias'] for r in creates],[16205,16206,16203,16057])
        old={(r[0],r[1]):r for r in self.ch['create_rows']}
        for c in creates:
            r=old[(c['create_path'],c['ordinal'])]
            self.assertEqual((c['source_block_sha256'],c['floor'],c['borncorner_original_four_numbers'],c['graphic_alias'],c['script_path']),
                (r[4],r[5],r[7],r[6],r[15][0][0]))
            self.assertFalse(c['actual_original_map_or_NPC_runtime_entered'])

    def test_06_map1300_missing_is_not_nonexistent_claim(self):
        creates=self.r['source_create_records']
        self.assertEqual([c['map_source_status'] for c in creates],
            ['MAP09_GT99_RD_SOURCE_READY_CANDIDATE','NO_MATCHING_DAT_IN_955',
             'MAP09_GT99_RD_SOURCE_READY_CANDIDATE','MAP09_GT99_RD_SOURCE_READY_CANDIDATE'])
        self.assertIsNone(creates[1]['prior_original_DAT_sha256'])
        self.assertFalse(self.r['unresolved_map_1300']['original_map_proven_absent'])

    def test_07_control_types_and_reward_literals_not_runtime(self):
        self.assertEqual(self.r['source_event_type_totals'],{'ACCEPT':8,'REQUEST':5,'MESSAGE':5})
        x=self.r['source_story_control_literals']
        self.assertEqual(x['event12_issue_tokens'],'2419,2420')
        self.assertEqual(x['event09_final_requirement'],'ENDEV=12&ENDEV=10&ENDEV=11')
        self.assertEqual(x['event09_reward'],'1357')
        self.assertFalse(x['actual_order_or_multiple_flags_execution_proven'])

    def test_08_original_multi_flag_branch_alternatives_conserved(self):
        x=self.r['source_story_control_literals']
        self.assertEqual(x['event10_alternative_flag_literals'],['10,12','10'])
        self.assertEqual(x['event11_alternative_flag_literals'],['11,12','11'])
        self.assertFalse(self.r['source_constraints']['native_EndSetFlg_multi_value_execution_proven'])
        s={r['path']:r for r in self.scripts}
        self.assertEqual(s['sainasu/event/event11']['events'][0]['commands']['Charm'],['1'])

    def test_09_event41_and42_are_literal_not_proven_progression(self):
        x=self.r['source_story_control_literals']['event41_42_coupled_conditions']
        self.assertEqual(len(x),3)
        self.assertEqual(x[0],'ENDEV=12&ITEM=2736,ENDEV=42&ITEM=2736,ENDEV=41&ITEM=2736')
        self.assertEqual(x[1],'ENDEV=41&ITEM!=2736&ENDEV=4&NOWEV=42')
        self.assertEqual(x[2],'LV>0&NOWEV=41&ENDEV=4&NOWEV=42')
        self.assertFalse(self.r['source_constraints']['native_EVENT_conditional_priority_or_comma_semantics_proven'])

    def test_10_six_items_two_rows_each_and_separate_ids(self):
        items=self.r['source_items']
        self.assertEqual([i['item_ID'] for i in items],[1052,1357,2419,2420,2421,2736])
        self.assertEqual([len(x['source_two_rows']) for x in items],[2]*6)
        self.assertEqual(self.r['source_item_rows'],12)
        shards={}
        for n in range(1,8):
            f=REC/'item-module-01'/f'STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-{n:02d}-R1.json'
            for row in json.loads(f.read_text('utf8'))['rows']:
                shards[row[0]]=row
        for i in items:
            a,b=i['source_two_rows']
            self.assertEqual(a['source_row_sha256'],b['source_row_sha256'])
            self.assertEqual([a['source_row_sha256'],b['source_row_sha256']],shards[i['item_ID']][1:3])
            self.assertFalse(i['same_official_build_or_original_quest_display_proven'])

    def test_11_candidate_icons_are_cross_carrier_not_official_quest(self):
        self.assertEqual({x['original_source_itemset_image_alias'] for x in self.r['source_items']},
                         {21025,22024,24057,24058,24071,24213})
        self.assertEqual(self.r['distinct_cross_carrier_image_aliases'],6)
        self.assertFalse(self.r['source_constraints']['cross_carrier_TW1_art_is_original_mixed25_quest_UI'])

    def test_12_legacy_integer_index_misses_compound_flag12(self):
        c=self.r['source_module_census']
        self.assertEqual(c['legacy_QUEST01_integer_EndSetFlg_flag12_matches'],0)
        self.assertFalse(any(12 in x['end_set_flags'] for x in self.q['source_event_blocks']))
        self.assertEqual([(x['script'],x['event_ordinal'],x['exact_line']) for x in c['source_compound_EndSetFlg_with_flag12']],
            [('sainasu/event/event10',0,'10,12'),('sainasu/event/event11',0,'11,12')])
        self.assertTrue(c['legacy_flag12_absence_not_source_absence'])

    def test_13_evidence_boundaries_and_next_module_stop(self):
        b=self.r['source_constraints']
        for k in ('original_client_or_server_running','early_official_same_deployment_proven',
                  'native_NPC_or_scene_rendered','geographic_island_or_village_hierarchy_authenticated'):
            self.assertFalse(b[k])
        self.assertFalse(b['original_script_text_or_dialogue_in_public_repo'])
        self.assertEqual(self.r['stage_A'],{'PARTIAL':7,'OPEN':2})
        self.assertEqual(self.r['stage_B'],'GATED')
        self.assertIsNone(self.r['overall_percent'])
        self.assertTrue(self.r['next'].startswith('QUEST32_MODULE_STOP'))

if __name__=='__main__':unittest.main()
