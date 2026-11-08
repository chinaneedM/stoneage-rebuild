"""Public source evidence checks; commercial scripts and pixels remain private."""
import hashlib
import json
from pathlib import Path
import unittest

from tools.stoneage_quest23_poru_source import OUTPUT, CREATE, FLOORS, QUEST01, CHAR01, WORLD21, MAP09, catalog_sections, load


class PoruOriginalEvidence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads(OUTPUT.read_text());cls.q=load(QUEST01);cls.c=load(CHAR01);cls.m=load(MAP09);cls.w=load(WORLD21)
        cls.events={(s['path'],e['ordinal']):e for s in cls.r['source_scripts'] for e in s['events']}

    def test_01_original_files_and_102_catalog_sections(self):
        files={r[0]:r for r in self.c['source_files']}
        self.assertEqual(len(self.r['source_manifest']),23)
        for s in self.r['source_manifest']:
            self.assertEqual((s['bytes'],s['sha256'],s['crc32']),tuple(files[s['path']][1:4]))
        old={(b['script_path'],b['script_block_ordinal']):b for b in self.q['source_event_blocks']}
        self.assertEqual(len(self.events),102)
        for key,e in self.events.items():
            b=old[key]
            self.assertEqual((e['type_line'],e['event_no'],e['type'],e['condition_sha256'],e['section_sha256'],e['exact_EventEnd_found']),
                             (b['source_type_line'],b['event_number'],b['raw_type'],b['condition_expression_decoded_cp950_UTF8_sha256'],b['source_section_decoded_cp950_normalized_UTF8_sha256'],b['source_End_found']))
        self.assertEqual(self.r['new_original_script_discoveries'],0)

    def test_02_distinct_catalog_ordinals_do_not_shift_after_comment(self):
        old={r['original_script_path']:r for r in self.q['source_creation_references'] if r['create_source_path']==CREATE}
        raw={r[1]:r for r in self.c['create_rows'] if r[0]==CREATE}
        self.assertEqual(len(self.r['source_creates']),20)
        for c in self.r['source_creates']:
            b=raw[c['ordinal']];q=old[c['script_ref']]
            self.assertEqual((c['source_byte_start'],c['source_byte_end'],c['source_block_sha256'],c['floor'],c['graphic_alias'],c['borncenter']),
                             (b[2],b[3],b[4],b[5],b[6],b[8]))
            self.assertEqual(c['raw_brace_match_ordinal'],q['create_brace_ordinal'])
            self.assertEqual(c['raw_brace_match_ordinal'],c['ordinal']+(c['ordinal']>=14))
            self.assertIsNone(c['borncorner'])
        comment=self.r['source_comment_only_block']
        self.assertEqual(comment['raw_brace_match_ordinal'],14)
        self.assertIsNone(comment['catalog_active_field_ordinal'])
        self.assertTrue(comment['all_configuration_fields_prefixed_by_comment'])
        self.assertTrue(comment['closing_brace_also_comment_prefixed'])
        self.assertFalse(comment['actual_shop_or_runtime_loader_effect_verified'])
        self.assertEqual(comment['original_referenced_file_header'],'LIMITSHOP')
        self.assertEqual(comment['source_LimitItemNo'],[12174,12175,12176])

    def test_03_malformed_titan_end_stays_missing(self):
        failures=[(k,e) for k,e in self.events.items() if not e['exact_EventEnd_found']]
        self.assertEqual([k for k,e in failures],[('poru/titan',7)])
        e=failures[0][1]
        self.assertEqual((e['event_no'],e['type'],e['condition_literal']),(65,'REQUEST','NOWEV=64'))
        self.assertEqual(e['malformed_EventEnd_prefix_lines'][0]['line'],73)
        self.assertFalse(self.r['source_malformed_end']['original_text_fixed'])

    def test_04_synthetic_glued_end_cannot_be_repaired_silently(self):
        source=b'EventNo:65\nTYPE:REQUEST\nEVENT:NOWEV=64\nEventEndX\n\n'
        old=dict(source_eventno_line=1,source_type_line=2,source_End_found=False,event_number=65,raw_type='REQUEST',
                 condition_expression_decoded_cp950_UTF8_sha256=hashlib.sha256(b'NOWEV=64').hexdigest(),
                 source_section_decoded_cp950_normalized_UTF8_sha256=hashlib.sha256(source).hexdigest())
        parsed=catalog_sections(source,[old])[0]
        self.assertFalse(parsed['exact_EventEnd_found'])
        self.assertEqual(parsed['malformed_EventEnd_prefix_lines'][0]['line'],4)
        with self.assertRaises(AssertionError):catalog_sections(source.replace(b'EventEndX',b'EventEnd'),[old])
        with self.assertRaises(AssertionError):catalog_sections(source[:-1],[old])

    def test_05_four_stones_finale_and_explicit_quantity_survive(self):
        e=self.events[('poru/mary01',0)]
        self.assertEqual(e['condition_literal'],'NOWEV=64&ITEM=18556&ITEM=18557&ITEM=18558&ITEM=18559')
        self.assertEqual(e['commands'],{'DelItem':['18556,18557,18558*1,18559'],'GetPet':['310'],'EndSetFlg':['64']})
        self.assertEqual(self.r['four_stones_finale']['original_DelItem_literal'],'18556,18557,18558*1,18559')
        self.assertFalse(self.r['four_stones_finale']['actual_reward_delivered'])

    def test_06_five_GetPet_references_are_old_instance_namespace_records(self):
        rows=self.r['existing_WORLD21_GetPet_links'];old={r['getpet_integer']:r for r in self.w['original_enemy_instance_to_template_lookups']}
        self.assertEqual(sorted(int(r['source_GetPet_literal']) for r in rows),[310,333,1481,1482,1483])
        for r in rows:
            self.assertEqual(r['existing_WORLD21_lookup'],old[int(r['source_GetPet_literal'])])
            self.assertFalse(r['new_pet_discovery'])
            self.assertIn(r['source_GetPet_literal'],self.events[(r['script'],r['event_ordinal'])]['commands']['GetPet'])
        self.assertEqual(old[310]['template_id_via_enemy_field4'],194)
        self.assertEqual([(old[i]['template_id_via_enemy_field4']) for i in (1483,1481,1482)],[720,719,721])
        self.assertEqual(sorted(v for e in self.events.values() for v in e['commands'].get('DelPet',[])),
                         ['PET=30-719*1','PET=30-720*1','PET=33-721*1'])

    def test_07_seventeen_items_and_34_rows_exclude_currency_and_comments(self):
        rows=self.r['source_items'];ids=[r['item_ID'] for r in rows]
        self.assertEqual(ids,[2432,2474,2477,2478,18544,*range(18551,18563)])
        for i in [50,80,100,12174,12175,12176]:self.assertNotIn(i,ids)
        old={r[0]:r for n in range(1,8) for r in load(f'item-module-01/STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-{n:02d}-R1.json')['rows']}
        for r in rows:self.assertEqual([s['sha256'] for s in r['source_rows']],old[r['item_ID']][1:3])
        self.assertEqual(self.r['distinct_cross_carrier_item_candidate_images'],12)
        alias={r['item_ID']:r['cross_carrier_candidate_alias'] for r in rows}
        self.assertEqual((alias[18561],alias[18562]),(24112,24112))
        self.assertNotEqual(old[18561][1],old[18562][1])

    def test_08_two_original_NpcWarp_fields_preserve_order_and_missing_map(self):
        rows=self.r['source_NpcWarp_fields'];self.assertEqual(len(rows),2)
        for r in rows:
            self.assertEqual(r['script'],'poru/mary02')
            self.assertEqual(len(r['target_occurrences']),7)
            literal=','.join('.'.join(map(str,p)) for p in r['target_occurrences'])
            self.assertEqual(literal,r['source_literal'])
            self.assertFalse(r['original_NPC_relocation_executed'])
        self.assertEqual(set(map(tuple,rows[0]['target_occurrences'])),set(map(tuple,rows[1]['target_occurrences'])))
        self.assertNotEqual(rows[0]['target_occurrences'],rows[1]['target_occurrences'])
        self.assertFalse(self.r['original_floor500']['matching_DAT_in_955'])

    def test_09_nine_maps_and_17_centers_preserve_borncenter(self):
        scenes=self.r['original_scene_observations'];self.assertEqual(tuple(s['floor'] for s in scenes),FLOORS)
        creates={c['ordinal']:c for c in self.r['source_creates']}
        self.assertEqual(sum(len(s['source_points']) for s in scenes),17)
        for s in scenes:
            old=self.m['maps'][str(s['floor'])]
            self.assertEqual((s['original_DAT_sha256'],s['geometry'],s['three_candidate_RGBA_sha256']),
                             (old['source_sha256'],old['geometry'],old['frame_RGBA_sha256']))
            self.assertTrue(s['independent_Pillow_and_NumPy_all_three_equal'])
            for p in s['source_points']:
                c=creates[p['create_ordinal']]
                self.assertEqual(p['source_coordinate_field'],'borncenter')
                self.assertEqual(p['source_coordinate_literal'],c['borncenter'])
                self.assertEqual(p['xy'],c['borncenter'][:2])
                self.assertFalse(p['actual_spawn_cell_verified'])
        self.assertEqual(self.r['distinct_replayed_candidate_tile_PNGs'],913)

    def test_10_stage_and_original_execution_limits(self):
        r=self.r;self.assertTrue(all(v is False for v in r['boundaries'].values() if isinstance(v,bool)))
        self.assertEqual(r['boundaries']['task_origin'],'UNRESOLVED')
        self.assertEqual(r['source_center_observation']['independent_candidate_full_frames'],27)
        self.assertEqual(r['stage_A'],{'PARTIAL':7,'OPEN':2})
        self.assertEqual((r['stage_B'],r['wiki'],r['R79']),('GATED','GATED','PAUSED_NON_BLOCKING'))
        self.assertIsNone(r['overall_percent'])


if __name__=='__main__':unittest.main()
