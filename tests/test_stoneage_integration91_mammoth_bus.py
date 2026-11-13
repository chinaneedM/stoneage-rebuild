import json
import hashlib
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'research/recovered/STONEAGE-INTEGRATION91-MAMMOTH-BUS-ORIGINAL-2D-R1.json'
O86=ROOT/'research/recovered/STONEAGE-O86-MAMMOTH-BUS-SOURCE-R1.json'
CHAR=ROOT/'research/recovered/STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json'
PET=ROOT/'research/recovered/STONEAGE-PET-MODULE-11-TW10-CAPTURE-SPR-ORIGINAL-496-PIXEL-SOURCE-R1.json'

class OriginalBusSpriteSourceBridge(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=json.loads(OUT.read_text(encoding='utf-8'))
        cls.o=json.loads(O86.read_text(encoding='utf-8'))
        cls.c=json.loads(CHAR.read_text(encoding='utf-8'))
        cls.p=json.loads(PET.read_text(encoding='utf-8'))

    def test_original_CREATE_six_exact_source_windows(self):
        rows=self.d['original_mixed25_six_BUS_CREATE_route_numeric_source_rows']
        raw=[r for r in self.c['create_rows'] if r[0]=='chatroom/bus.create']
        self.assertEqual(len(rows),6)
        self.assertEqual(len(raw),6)
        for a,b in zip(raw,rows):
            self.assertEqual([a[1],a[2],a[3],a[4]],[b['index'],*b['exact_original_CREATE_byte_span'],b['exact_CREATE_byte_SHA256']])
            self.assertEqual([a[5],a[8][:2],a[8],a[6],a[10],a[11]],[b['original_floor'],b['original_xy'],b['borncenter'],b['original_graphic_literal'],b['original_direction_literal'],b['original_template_token']])
            self.assertEqual(a[15][0][0],'chatroom/'+b['original_ARG_path'].split('/')[-1])
            self.assertEqual(a[15][0][2],b['original_ARG_full_file_sha256'])

    def test_original_bus_file_hash_and_function_scope(self):
        d=self.d
        f=next(r for r in self.c['source_files'] if r[0]=='chatroom/bus.create')
        self.assertEqual([f[1],f[2],f[3]],[d['inherited_originals']['original_create_file_bytes'],d['inherited_originals']['original_create_file_SHA256'],d['inherited_originals']['original_create_file_CRC32']])
        self.assertEqual(d['inherited_originals']['original_functionset_literal'],self.o['bus_template']['source_functionset'])
        self.assertEqual(d['inherited_originals']['original_type_literal'],self.o['bus_template']['source_type_literal'])
        self.assertFalse(self.o['bus_template']['actual_native_handler_executed'])

    def test_original_35_file_manifest_source_bound(self):
        expected={x['member_path']:(x['bytes'],x['sha256'],x['rar_header_crc32']) for x in self.o['original_member_manifest']}
        got=self.d['original_bus_route_original_file_manifest_all_35']
        self.assertEqual(len(got),35)
        self.assertEqual(sum(x['bytes'] for x in got),14116)
        for item in got:
            self.assertEqual((item['bytes'],item['sha256'],item['crc32']),expected[item['path']])

    def test_six_routes_and_ordered_coordinate_summaries(self):
        o={x['source_file'].removeprefix('data/npc/'):x for x in self.o['six_original_routes']}
        d=self.d['original_mixed25_six_BUS_CREATE_route_numeric_source_rows']
        self.assertEqual(sum(x['source_waypoints'] for x in d),300)
        self.assertEqual([x['source_waypoints'] for x in d],[66,10,15,45,55,109])
        for x in d:
            r=o[x['original_ARG_path'].removeprefix('npc/')]
            self.assertEqual([x['original_floor'],x['original_xy'],x['source_waypoints'],x['source_first'],x['source_last'],x['needstone_original_literal'],x['waittime_original_literal']],[r['original_floor'],r['original_bus_NPC_xy'],r['route_point_count'],r['first_route_point'],r['last_route_point'],r['source_needstone_literal'],r['source_waittime_literal']])

    def test_raw_route_hashes_are_original_derived_witnesses_not_raw_coordinates(self):
        r=self.d['original_mixed25_six_BUS_CREATE_route_numeric_source_rows']
        hashes=['28221c566b110efe4729889f6215692d355e94d24701b01d3acc62c8f8c87840','863465d40c650e8df70c21d922afc3f616efa2c83609efe0366ef09e0a80dcaa','cf85e20b5a3adcc4c6dee54b7a8b3bf6bdc69d18f372ae64c77d3f2e13b78d16','5593736799eff476364d84815c37664008ae3d9e8df1d5155ae351d2e5a8817d','9dac11c04bff7fcd6d664a7fe4ef1fb1fc11bd2288d268f1653baf8ba370cac1','39f0657148667c347f032867790f43f44758c4cfe5f3295baf27fea7b8967d8c']
        self.assertEqual([x['original_route_line_raw_SHA256'] for x in r],hashes)
        self.assertTrue(all(re.fullmatch(r'[0-9a-f]{64}',v) for v in hashes))
        self.assertNotIn('routeto1',self.d)

    def test_original_bus_literal_discrepancies_survive(self):
        d=self.d
        r=d['original_mixed25_six_BUS_CREATE_route_numeric_source_rows']
        self.assertEqual([x['source_denied_item_second_id'] for x in r],[403,2403,2403,2403,2403,2403])
        self.assertFalse(r[3]['route_name_raw_line_roundtrip_CP950'])
        self.assertTrue(d['important_prior_O86_anomalies_preserved']['guide_station_text_disagreement_200_426_100'])
        self.assertTrue(d['important_prior_O86_anomalies_preserved']['floor3000_two_static_board_guide_without_bus_vehicle'])
        self.assertEqual(len([x for x in self.o['six_station_clusters']]),6)

    def test_tw1_source_group_is_pet11_exact_and_cross_version(self):
        g=next(x for x in self.p['actual_original_sprite_source']['groups'] if x['spr_no']==100355)
        n=self.d['original_TW1_retail_SPR_candidate']
        self.assertEqual((n['source_original_SPR_segment_SHA256'],n['original_spr_segment_bytes'],n['original_source_SPR_index_12byte_SHA256']),(g['original_source_segment_sha256'],g['original_source_segment_bytes'],g['source_index_record_sha256']))
        self.assertEqual((n['source_group_original_animations'],n['source_original_frame_occurrences'],n['source_unique_RD_bitmaps']),(56,640,248))
        self.assertEqual((n['source_private_prior_strict_RD_decoded'],n['source_private_prior_bounded_RD']),(248,0))

    def test_248_original_RD_and_ADRN_chain_proofs(self):
        g=next(x for x in self.p['actual_original_sprite_source']['groups'] if x['spr_no']==100355)
        n=self.d['original_TW1_retail_SPR_candidate']
        self.assertEqual([n['prior_source_248_ADRN_record_SHA256_concatenation_SHA256'],n['prior_source_248_RD_SHA256_concatenation_SHA256'],n['prior_source_248_canvas_indices_SHA256_concatenation_SHA256']],[g['original_adrn_record_sha256_sequence_sha256'],g['original_rd_sha256_sequence_sha256'],g['canvas_index_sha256_sequence_sha256']])
        self.assertEqual([n['private_this_unit_248_earlier_PNG_color_SHA256_verified_vs_original_PET11_manifest'],n['private_this_unit_248_earlier_PNG_gray_SHA256_verified_vs_original_PET11_manifest']],[248,248])
        self.assertEqual(n['private_this_unit_actual_NEW_RD_source_decoded'],0)

    def test_pet_flg_zero_and_capture_key_not_species(self):
        link=next(x for x in self.p['capture_candidate_links'] if x['original_source_graphic_no']==100355)
        n=self.d['original_TW1_retail_SPR_candidate']
        self.assertEqual([link['source_PETFLG'],link['compiled_char_int_key53']],[0,8])
        self.assertEqual([n['same_graphic_in_mixed25_later_template_source_PETFLG'],n['prior_compiled_capture_candidate_key53']],[0,8])
        self.assertFalse(n['original_native_sprite_palette_orientation_timing_sound_selection_proven'])

    def test_other_pet11_bad_RD_not_wrongly_applied_to_bus(self):
        p=self.p['actual_original_sprite_source']
        bad=p['one_strict_RD_failure_preserved']
        self.assertEqual(bad['bitmapno'],113576)
        n=self.d['original_TW1_retail_SPR_candidate']
        self.assertEqual(n['source_private_prior_bounded_RD'],0)
        self.assertEqual(n['source_private_prior_strict_RD_decoded'],248)

    def test_private_custody_and_real_browser_vs_native_game(self):
        p=self.d['private_source_2d_observer']
        self.assertEqual((p['archive_bytes'],p['archive_members']),(2530925,37))
        self.assertEqual(p['archive_sha256'],'a0bf3d9875a9aee50e35a21c7154c45f2c39fd0d9bf5eed8d4ce3af1b692d878')
        self.assertTrue(p['independent_Library_re_download_SHA256_exact_match'])
        self.assertEqual((p['chromium_real_six_route_selectors_passed'],p['chromium_direction_action_original_sequences_both_palette_modes_images_loaded'],p['chromium_actual_next_frame_transitions']),(6,112,56))
        self.assertEqual((p['chromium_JS_errors'],p['chromium_external_HTTP_requests']),(0,0))
        self.assertFalse(p['file_URL_navigation_success_claimed'])
        self.assertFalse(self.d['rights_and_historical_boundaries']['official_same_deployment_proven'])
        self.assertFalse(self.d['rights_and_historical_boundaries']['original_NPC_bus_handler_executed'])
        self.assertIsNone(self.d['stage']['overall_percent'])

    def test_rights_and_source_scope_negative(self):
        d=self.d
        self.assertTrue(d['rights_and_historical_boundaries']['no_original_binaries_images_scripts_or_raw_300_waypoint_table_in_public_Git'])
        self.assertTrue(d['rights_and_historical_boundaries']['original_100355_same_numeric_graphic_does_NOT_confirm_early_pet_species_or_capture'])
        self.assertTrue(d['original_TW1_retail_SPR_candidate']['original_native_sprite_palette_orientation_timing_sound_selection_proven'] is False)
        self.assertEqual(d['task_scope']['content'],'SOURCE_BOUND_MAMMOTH_BUS_ROUTE_NPC_TO_ORIGINAL_SPR_VISUAL_EVIDENCE')

if __name__=='__main__':
    unittest.main()
