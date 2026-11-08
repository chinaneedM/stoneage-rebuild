"""Public replay of source-qualified metadata; original files are private."""
import hashlib
import json
from pathlib import Path
import unittest

from tools.stoneage_quest22_hekisei_source import (
    OUTPUT, CREATE, SCRIPTS, FILES, ITEM_IDS, QUEST01, CHAR01, MAP09, WORLD23, load,
)


class HekiseiOriginalEvidence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads(OUTPUT.read_text())
        cls.q=load(QUEST01);cls.ch=load(CHAR01);cls.m=load(MAP09);cls.w=load(WORLD23)

    def test_01_source_manifest_is_existing_original_bytes(self):
        rows={r[0]:r for r in self.ch['source_files']}
        self.assertEqual([r['path'] for r in self.r['source_manifest']],FILES)
        for r in self.r['source_manifest']:
            self.assertEqual((r['bytes'],r['sha256'],r['crc32']),tuple(rows[r['path']][1:4]))
        for pin in self.r['old_evidence_inputs']:
            raw=(OUTPUT.parents[2]/pin['path']).read_bytes()
            self.assertEqual((len(raw),hashlib.sha256(raw).hexdigest()),(pin['bytes'],pin['sha256']))
        self.assertEqual(self.r['private_verified_carriers']['NPC_all_member_CRC_and_SHA'],2205)

    def test_02_seven_creates_and_23_events_are_not_new_discoveries(self):
        old=[r for r in self.q['source_creation_references'] if r['create_source_path']==CREATE]
        self.assertEqual(len(old),7)
        for c in self.r['source_creates']:
            r=next(x for x in old if x['create_brace_ordinal']==c['ordinal'])
            self.assertEqual((c['floor'],c['graphic_alias'],c['script_ref']),
                             (r['floorid'],r['graphic_alias_numeric'],r['original_script_path']))
        blocks={(r['script_path'],r['script_block_ordinal']):r for r in self.q['source_event_blocks']}
        total=0
        for script in self.r['source_scripts']:
            for e in script['events']:
                r=blocks[(script['path'],e['ordinal'])]
                self.assertEqual((e['event_no'],e['type'],e['condition_sha256'],e['section_sha256']),
                                 (r['event_number'],r['raw_type'],r['condition_expression_decoded_cp950_UTF8_sha256'],r['source_section_decoded_cp950_normalized_UTF8_sha256']))
                total+=1
        self.assertEqual(total,23)
        self.assertEqual(self.r['original_events_already_in_QUEST01'],23)
        self.assertEqual(self.r['newly_discovered_original_scripts'],0)

    def test_03_prerequisites_are_three_requests_and_keep_all_six_flag_sources(self):
        r=self.r['prerequisites']
        self.assertEqual(r['original_three_request_conditions'],[
            'LV>64&ENDEV=4&ENDEV=39','LV>64&ENDEV=4&ENDEV=40','LV>64&ENDEV=4&ENDEV=42'])
        for flag in (39,40,42):
            old=[(b['script_path'],b['script_block_ordinal'],b['source_section_decoded_cp950_normalized_UTF8_sha256'])
                 for b in self.q['source_event_blocks'] if flag in b['end_set_flags']]
            observed=[(b['script'],b['ordinal'],b['section_sha256']) for b in r['all_existing_catalog_flag_setter_occurrences'][str(flag)]]
            self.assertEqual(observed,old)
            self.assertEqual(len(observed),2)
        self.assertFalse(r['flags_are_exclusive_quest_IDs_verified'])
        self.assertFalse(r['original_three_requests_collapsed_into_AND'])

    def test_04_crafting_original_alternative_and_bare_quantities_survive(self):
        row=self.r['source_scripts'][3]['events'][1]
        self.assertEqual(row['condition_literal'],'LV>64&NOWEV=46&ITEM=2767&ITEM=2768,LV>64&NOWEV=46&ITEM!=2769')
        self.assertEqual(row['commands'],{'GetItem':['2769'],'DelItem':['2767,2768']})
        # Neither deletion count nor boolean precedence is filled in by the exporter.
        self.assertNotIn('*',row['commands']['DelItem'][0])
        self.assertFalse(self.r['preserved_crafting_condition']['native_boolean_evaluation_priority_or_bug_verified'])
        self.assertEqual(self.r['source_scripts'][1]['events'][0]['commands'],
                         {'GetItem':['2770'],'DelItem':['2769'],'EndSetFlg':['46'],'Charm':['1']})
        self.assertEqual(self.r['full_2205_NPC_GetItem_literal_occurrences']['2766'],[])
        self.assertEqual(self.r['full_2205_NPC_GetItem_literal_occurrences']['2767'],[])

    def test_05_box_labels_preserve_reverse_filename_order_and_old_pools(self):
        by_ordinal={c['ordinal']:c for c in self.r['source_creates']}
        self.assertEqual((by_ordinal[5]['box_size_source_label'],by_ordinal[5]['script_ref'],by_ordinal[5]['graphic_alias']),
                         ('大箱子','jaruga/event/hekisei06',24308))
        self.assertEqual((by_ordinal[6]['box_size_source_label'],by_ordinal[6]['script_ref'],by_ordinal[6]['graphic_alias']),
                         ('小箱子','jaruga/event/hekisei05',24311))
        pools=self.r['old_WORLD09_and_WORLD23_pools']
        old=[r for r in self.w['WORLD09_additive_correction']['source_comparison_rows'] if r[0] in SCRIPTS[5:]]
        self.assertEqual(pools['old_comparison_rows'],old)
        self.assertEqual(pools['new_random_pool_discoveries'],0)
        for ids,script in zip(pools['ordered_source_positions'],self.r['source_scripts'][5:],strict=True):
            self.assertEqual((len(ids),len(set(ids))),(36,24))
            self.assertEqual(list(map(int,script['events'][0]['commands']['GetRandItem'][0].split(','))),ids)
            self.assertEqual(script['events'][0]['commands']['DelItem'],['2766'])
            self.assertEqual(script['events'][0]['bare_Break_lines'],1)
        self.assertFalse(pools['original_probability_distribution_verified'])

    def test_06_three_actual_maps_replay_nine_existing_full_frame_hashes(self):
        scenes=self.r['three_actual_DAT_scene_observations']
        self.assertEqual([s['floor'] for s in scenes],[21215,21308,31302])
        self.assertEqual([s['geometry'] for s in scenes],[[50,100],[40,40],[60,60]])
        self.assertEqual([s['source_draw_positions'] for s in scenes],[4227,1418,2283])
        for s in scenes:
            old=self.m['maps'][str(s['floor'])]
            self.assertEqual((s['original_DAT_bytes'],s['original_DAT_sha256']),
                             (old['source_bytes'],old['source_sha256']))
            self.assertEqual(s['three_candidate_RGBA_sha256'],old['frame_RGBA_sha256'])
            self.assertEqual((s['canvas_size'],s['origin']),(old['canvas_size'],old['origin']))
            self.assertTrue(s['independent_Pillow_and_NumPy_all_three_equal'])
        self.assertEqual(self.r['distinct_replayed_original_scene_candidate_PNGs'],156)

    def test_07_six_measured_source_cells_and_missing_3400_remain_distinct(self):
        scenes=self.r['three_actual_DAT_scene_observations']
        points=[(s,p) for s in scenes for p in s['source_points']]
        self.assertEqual(len(points),6)
        expected={0:[4005,0,49152],2:[4007,0,49152],5:[4064,0,49152],6:[4008,0,49152],3:[4408,12827,49152],4:[4004,0,49152]}
        creates={c['ordinal']:c for c in self.r['source_creates']}
        for s,p in points:
            c=creates[p['create_ordinal']];x,y=p['xy'];ox,oy=s['origin']
            self.assertEqual((s['floor'],p['xy']),(c['floor'],c['borncorner'][:2]))
            self.assertEqual(p['raw_three_u16'],expected[p['create_ordinal']])
            self.assertEqual(p['modern_projected_center'],[ox+(x+y)*32,oy+(y-x)*24])
            self.assertFalse(p['original_NPC_sprite_drawn'])
        self.assertEqual(self.r['map_3400']['xy'],[63,72])
        self.assertNotIn('3400',self.m['maps'])
        self.assertFalse(self.r['map_3400']['matching_original_DAT_in_955_batch'])

    def test_08_five_items_link_ten_existing_original_rows_without_same_build_claim(self):
        old={r[0]:r for n in range(1,8) for r in load(f'item-module-01/STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-{n:02d}-R1.json')['rows']}
        self.assertEqual([x['item_ID'] for x in self.r['core_items']],ITEM_IDS)
        self.assertEqual([x['cross_carrier_candidate_alias'] for x in self.r['core_items']],[24133,24198,23012,14648,22124])
        for x in self.r['core_items']:
            self.assertEqual([r['sha256'] for r in x['source_rows']],old[x['item_ID']][1:3])
            self.assertEqual(len(x['original_RD_sha256']),64)
            self.assertEqual(len(x['candidate_PNG_sha256']),64)

    def test_09_original_execution_and_stage_limits(self):
        r=self.r;obs=r['private_new_observation']
        self.assertEqual((obs['original_DAT_files_reread'],obs['source_NPC_positions_measured'],obs['complete_candidate_frames_independently_replayed']),(3,6,9))
        self.assertEqual(obs['new_original_RD_decodes'],0)
        self.assertTrue(all(v is False for v in r['boundaries'].values() if isinstance(v,bool)))
        self.assertFalse(obs['original_assets_browser_executed'])
        self.assertFalse(obs['original_game_executed'])
        self.assertEqual(r['boundaries']['task_permanent_or_event_origin'],'UNRESOLVED')
        self.assertEqual(r['stage_A'],{'PARTIAL':7,'OPEN':2})
        self.assertEqual((r['stage_B'],r['wiki'],r['R79']),('GATED','GATED','PAUSED_NON_BLOCKING'))
        self.assertIsNone(r['overall_percent'])


if __name__=='__main__':unittest.main()
