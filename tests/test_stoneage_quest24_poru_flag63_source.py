"""Derived evidence acceptance; original game files and assets are private."""
from collections import Counter
import json
import unittest

from tools.stoneage_quest24_poru_flag63_source import OUTPUT, CREATE, BOSS, FLOORS, ITEM_IDS, QUEST01, CHAR01, MAP09, WORLD21, Q23, load


class PoruFlag63OriginalEvidence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads(OUTPUT.read_text());cls.q=load(QUEST01);cls.c=load(CHAR01);cls.m=load(MAP09);cls.w=load(WORLD21);cls.previous=load(Q23)
        cls.events={(s['path'],e['ordinal']):e for s in cls.r['source_scripts'] for e in s['events']}

    def test_01_all_36_source_files_and_33_blocks_match_old_catalogue(self):
        old={r[0]:r for r in self.c['source_files']}
        self.assertEqual(len(self.r['source_manifest']),36)
        for s in self.r['source_manifest']:self.assertEqual((s['bytes'],s['sha256'],s['crc32']),tuple(old[s['path']][1:4]))
        blocks={(r[0],r[1]):r for r in self.c['create_rows']}
        self.assertEqual(len(self.r['source_creates']),33)
        for c in self.r['source_creates']:
            b=blocks[(c['source_create_path'],c['source_create_ordinal'])]
            self.assertEqual((c['original_block_sha256'],c['floor'],c['graphic_alias'],c['borncorner'],c['borncenter']),
                             (b[4],b[5],b[6],b[7],b[8]))
        self.assertEqual(self.r['source_creates'][-1]['source_create_path'],BOSS)
        self.assertEqual(self.r['source_creates'][-1]['source_create_ordinal'],0)

    def test_02_function_bindings_preserve_real_roles_and_double_coordinate_fields(self):
        rows=[c for c in self.r['source_creates'] if c['source_create_path']==CREATE]
        self.assertEqual(Counter(c['source_template_token'] for c in rows),
                         {'npcgen_man':15,'changeevent':11,'npcgen_shop':3,'npcgen_warpman':2,'npcgen_winhealer':1})
        templates={(t[0],t[1]):t for t in self.c['template_rows']}
        for c in self.r['source_creates']:
            for b in c['source_bindings']:
                t=templates[(b['template_path'],b['template_ordinal'])]
                self.assertEqual((b['source_template_name'],b['source_functionset']),(t[3],t[4]))
            self.assertFalse(c['original_borncenter_borncorner_precedence_verified'])
        self.assertEqual([c['source_create_ordinal'] for c in rows if c['borncorner'] is not None],[17,18,21,30,31])

    def test_03_39_existing_sections_are_not_new_quests(self):
        old={(b['script_path'],b['script_block_ordinal']):b for b in self.q['source_event_blocks']}
        self.assertEqual(len(self.events),39)
        for key,e in self.events.items():
            b=old[key]
            self.assertEqual((e['event_no'],e['type'],e['condition_sha256'],e['section_sha256']),
                             (b['event_number'],b['raw_type'],b['condition_expression_decoded_cp950_UTF8_sha256'],b['source_section_decoded_cp950_normalized_UTF8_sha256']))
        self.assertEqual(self.r['new_original_script_discoveries'],0)

    def test_04_flag63_provider_is_separate_boss_file_and_old_GetPet_namespace(self):
        b=self.r['flag63_bridge'];self.assertEqual((b['provider_CREATE'],b['provider_CREATE_ordinal']),(BOSS,0))
        self.assertEqual(b['original_provider_condition'],'NOWEV=63')
        self.assertEqual(b['original_provider_commands'],{'GetPet':['352'],'EndSetFlg':['63']})
        self.assertEqual(b['next_source_QUEST23_request_conditions'],['ENDEV=63'])
        old=next(x for x in self.w['original_enemy_instance_to_template_lookups'] if x['getpet_integer']==352)
        self.assertEqual(b['original_GetPet_352_existing_WORLD21_lookup'],old)
        self.assertEqual(old['template_id_via_enemy_field4'],303)
        self.assertEqual(old['original_template_graphic_id'],self.r['source_creates'][-1]['graphic_alias'])
        self.assertTrue(b['existing_pet_not_new_discovery']);self.assertFalse(b['original_flag_saved_or_reward_delivered'])

    def test_05_wpm_filename_does_not_override_original_function_and_gate_source(self):
        d=self.r['wpm_named_dialogue'];self.assertEqual((d['source_functionset'],d['actual_type']),('ExChangeMan','MESSAGE'))
        self.assertFalse(d['has_original_WARP_field']);self.assertFalse(d['classified_as_warp_from_filename'])
        self.assertEqual(self.events[('poru/wpm_5510_16_50',0)]['type'],'MESSAGE')
        gates=self.r['actual_source_warpman_parameters'];self.assertEqual(len(gates),2)
        self.assertEqual([g['source_values'] for g in gates],[
            {'WARP':'1000,71,49','FREE':'ITEM=2414','MONEY':'-1'},
            {'WARP':'5510,16,49','FREE':'ITEM=2414','MONEY':'-1'}])
        row=next(c for c in self.r['source_creates'] if c['source_create_path']==CREATE and c['source_create_ordinal']==21)
        self.assertEqual(row['borncenter'],[37,35,1,1])
        self.assertEqual(row['argument_paths'],['poru/wpm_5509_35_35'])

    def test_06_meat_list_and_bare_deletion_keep_original_punctuation(self):
        row=self.r['meat_shell_source']
        self.assertEqual(row['condition'],'ITEM=2248,ITEM=2249,ITEM=2250,ITEM=2251,ITEM=2252,ITEM=2253')
        self.assertEqual(row['commands'],{'GetItem':['2414'],'DelItem':['2248,2249,2250,2251,2252,2253']})
        self.assertFalse(row['original_boolean_or_deletion_semantics_verified'])
        self.assertNotIn('*',row['commands']['DelItem'][0])

    def test_07_old_message_18544_is_not_rewritten_as_finale_18558(self):
        d=self.r['source_four_object_message_difference']
        self.assertEqual(d['original_message_condition'],'ITEM=18556&ITEM=18557&ITEM=18559&ITEM=18544')
        self.assertEqual(d['later_QUEST23_finale_condition'],self.previous['four_stones_finale']['original_condition'])
        self.assertIn('ITEM=18558',d['later_QUEST23_finale_condition']);self.assertFalse(d['original_18544_replaced_with_18558'])

    def test_08_twelve_items_have_24_verified_rows_and_eleven_candidate_icons(self):
        items=self.r['core_items'];self.assertEqual([x['item_ID'] for x in items],ITEM_IDS)
        old={r[0]:r for n in range(1,8) for r in load(f'item-module-01/STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-{n:02d}-R1.json')['rows']}
        for i in items:self.assertEqual([r['sha256'] for r in i['source_rows']],old[i['item_ID']][1:3])
        self.assertEqual(len({i['cross_carrier_candidate_alias'] for i in items}),11)

    def test_09_four_maps_twelve_frames_and_27_literal_centers(self):
        scenes=self.r['original_scene_observations'];self.assertEqual(tuple(s['floor'] for s in scenes),FLOORS)
        self.assertEqual(sum(len(s['source_points']) for s in scenes),27)
        creates={c['marker_id']:c for c in self.r['source_creates']}
        for s in scenes:
            old=self.m['maps'][str(s['floor'])]
            self.assertEqual((s['original_DAT_sha256'],s['three_candidate_RGBA_sha256']),(old['source_sha256'],old['frame_RGBA_sha256']))
            for p in s['source_points']:
                c=creates[p['modern_marker_id']]
                self.assertEqual((p['source_create_path'],p['source_create_ordinal']),(c['source_create_path'],c['source_create_ordinal']))
                self.assertEqual(p['xy'],c['borncenter'][:2]);self.assertEqual(p['source_coordinate_literal'],c['borncenter'])
                self.assertFalse(p['actual_spawn_cell_verified'])
        self.assertEqual(self.r['distinct_candidate_tile_PNGs'],490)
        self.assertFalse(self.r['source_floor500']['matching_original_DAT_in_955'])

    def test_10_evidence_limits_and_stage_do_not_advance(self):
        r=self.r;self.assertTrue(all(v is False for v in r['boundaries'].values() if isinstance(v,bool)))
        self.assertEqual(r['boundaries']['task_origin'],'UNRESOLVED')
        self.assertEqual(r['source_center_observation']['complete_independent_candidate_frames'],12)
        self.assertEqual(r['stage_A'],{'PARTIAL':7,'OPEN':2});self.assertEqual((r['stage_B'],r['wiki'],r['R79']),('GATED','GATED','PAUSED_NON_BLOCKING'))
        self.assertIsNone(r['overall_percent'])


if __name__=='__main__':unittest.main()
