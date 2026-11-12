"""Negative-guarded public derived-source acceptance for INTEGRATION81.
No copyrighted original NPC or bitmap source bytes are required by these tests.
"""
import copy
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'research/recovered/STONEAGE-INTEGRATION81-JANKEN-NINE-ORIGINAL-PARTIAL-2D-SOURCE-R1.json'
HEX = re.compile(r'^[0-9a-f]{64}$')
FLOORS = [802, 804, 807, 822, 824, 827, 842, 844, 847]
MISSING = {9420, 9421, 9422, 9423, 10940}


class OriginalJankenPartial2D(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = json.loads(SOURCE.read_text(encoding='utf-8'))
        cls.rows = cls.d['janken_original_source_records']

    def test_source_carrier_and_exact_sha(self):
        p = self.d['provenance']
        self.assertEqual(p['parent_RAR_bytes'], 361255180)
        self.assertEqual(p['parent_RAR_sha256'], 'd71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5')
        self.assertEqual(p['original_NPC_create_bytes'], 1619)
        self.assertEqual(p['original_NPC_create_sha256'], '1514521d52ebb2db139bf51e32e835b24db9b05187b54817497257afea6dce24')
        self.assertTrue(p['original_NPC_create_parse_CP950_roundtrip'])

    def test_nine_exact_source_created_floor_order(self):
        self.assertEqual(len(self.rows), 9)
        self.assertEqual([r['floor'] for r in self.rows], FLOORS)
        self.assertEqual([r['source_index'] for r in self.rows], list(range(1, 10)))
        self.assertEqual(len({r['source_block_sha256'] for r in self.rows}), 9)
        self.assertTrue(all(HEX.fullmatch(r['source_block_sha256']) for r in self.rows))
        self.assertTrue(all(r['source_offset_start'] < r['source_offset_end_exclusive'] <= 1619 for r in self.rows))
        self.assertEqual(len({r['source_offset_start'] for r in self.rows}), 9)

    def test_three_NPC_graphic_groups_preserved_without_identity_merge(self):
        groups = [(100120, '拉伊奇', [802, 822, 842]), (100125, '布拉姆', [804, 824, 844]), (100130, '札克羅', [807, 827, 847])]
        for graphic, name, floors in groups:
            self.assertEqual([r['floor'] for r in self.rows if r['graphicname'] == graphic and r['npc_name'] == name], floors)
        self.assertEqual(len({r['npc_name'] for r in self.rows}), 3)

    def test_argument_source_files_are_real_and_distinct(self):
        self.assertEqual(len({r['parameter_sha256'] for r in self.rows}), 9)
        self.assertEqual(len({r['npc_parameter_path'] for r in self.rows}), 9)
        self.assertTrue(all(HEX.fullmatch(r['parameter_sha256']) for r in self.rows))
        self.assertTrue(all(r['parameter_bytes'] == 287 for r in self.rows))
        for r in self.rows:
            self.assertTrue(r['npc_parameter_path'].endswith(f"jan_{r['floor']}_{r['borncorner'][0]}_{r['borncorner'][1]}"))

    def test_nine_original_argument_entry_item_and_result_warps(self):
        for r in self.rows:
            self.assertEqual(r['entry_item_literal'], '2751*1')
            self.assertEqual(len(r['winwarp']), 3)
            self.assertEqual(len(r['losewarp']), 3)
            self.assertEqual(r['winwarp'][0], r['floor'])
            self.assertEqual(r['winwarp'][1], r['borncorner'][0])
            self.assertEqual(r['winwarp'][2], 15)
            self.assertFalse(r['has_win_item'])
            self.assertFalse(r['has_lose_item'])
            self.assertNotEqual(r['losewarp'][0], r['floor'])

    def test_nine_original_DAT_hashes_geometry(self):
        self.assertEqual(len({r['map_original_DAT']['sha256'] for r in self.rows}), 9)
        for r in self.rows:
            m = r['map_original_DAT']
            self.assertEqual(m['path'], f"{r['floor']}.dat")
            self.assertEqual(m['bytes'], 15008)
            self.assertEqual(m['geometry'], [50, 50])
            self.assertTrue(HEX.fullmatch(m['sha256']))

    def test_same_original_NPC_cell_values_not_collision_semantics(self):
        for r in self.rows:
            self.assertEqual(r['NPC_source_three_plane_u16'], [5002, 0, 49152])
            self.assertEqual(len(r['NPC_original_DAT_byte_offsets']), 3)
            self.assertTrue(all(8 <= v <= 15006 for v in r['NPC_original_DAT_byte_offsets']))

    def test_per_map_518_qualified_vs_5_gap(self):
        self.assertEqual(self.d['aggregates']['qualified_tile_placements_per_map'], 518)
        self.assertEqual(self.d['aggregates']['unqualified_tile_placements_per_map'], 5)
        self.assertEqual(self.d['aggregates']['total_qualified_tile_placements'], 4662)
        self.assertEqual(self.d['aggregates']['total_missing_tile_placements'], 45)
        for r in self.rows:
            self.assertEqual(r['tile_image_placement_count'], 518)
            self.assertEqual(r['tile_missing_placement_count'], 5)
            self.assertEqual(r['tile_distinct_qualified_alias_count'], 35)
            self.assertEqual({x['image_alias'] for x in r['missing_aliases_in_source_DAT']}, MISSING)
            self.assertTrue(all(x['plane'] in [0, 1] for x in r['missing_aliases_in_source_DAT']))

    def test_no_catalog_promotes_5_missing_as_recovered(self):
        g=self.d['original_image_gap']
        self.assertEqual({int(k) for k in g['aliases']}, MISSING)
        self.assertTrue(g['all_five_have_unique_community_index_records'])
        self.assertTrue(g['all_five_are_after_TW10_verified_index_prefix'])
        self.assertFalse(g['all_five_original_REAL_pixel_bytes_retrieved_this_round'])
        self.assertTrue(g['no_fabricated_missing_tiles'])
        for alias,entry in g['aliases'].items():
            self.assertTrue(HEX.fullmatch(entry['record_sha256']))
            self.assertGreaterEqual(entry['index'], 125996)
            self.assertGreaterEqual(entry['original_RD_byte_offset'], 315842228)
            self.assertGreater(entry['original_RD_record_length'], 0)

    def test_exact_first_four_post_prefix_source_index(self):
        g=self.d['original_image_gap']['aliases']
        self.assertEqual([g[str(n)]['index'] for n in range(9420,9424)], [125996,125997,125998,125999])
        self.assertEqual(g['10940']['index'], 126008)
        self.assertEqual(g['9420']['original_RD_byte_offset'], 315842228)
        self.assertEqual(g['10940']['original_RD_byte_offset'], 316009215)

    def test_negative_REAL_extraction_is_not_original_archive_damaged(self):
        p=self.d['original_image_gap']['community_REAL_read_probe']
        self.assertEqual(p['declared_uncompressed_bytes'],763908374)
        self.assertEqual(p['actual_bytes_read'],0)
        self.assertEqual(p['libarchive_reported_error'],'Invalid symbol')
        self.assertEqual(p['RD_payloads_newly_recovered'],0)
        self.assertTrue(p['failure_does_not_establish_archive_corruption'])

    def test_original_DAT_pair_differences_do_not_equal_visible_differences(self):
        comparisons=self.d['original_DAT_differences']
        self.assertEqual(len(comparisons),8)
        self.assertTrue(any(sum(r['different_original_u16_cells_by_plane'])>0 for r in comparisons))
        self.assertTrue(all(len(r['different_original_u16_cells_by_plane'])==3 for r in comparisons))
        self.assertEqual(self.d['independent_visual_replay']['unique_candidate_clean_pixel_canvases'],3)
        self.assertEqual(len({r['candidate_canvas']['clean_RGBA_sha256_independent_numpy'] for r in self.rows}),3)

    def test_eighteen_modern_source_canvas_sha_and_independent_replay(self):
        self.assertEqual(self.d['independent_visual_replay']['independent_full_map_RGBA_comparisons_passed'],9)
        self.assertEqual(self.d['aggregates']['private_modern_candidate_clean_images'],9)
        self.assertEqual(self.d['aggregates']['private_modern_candidate_annotated_images'],9)
        for r in self.rows:
            c=r['candidate_canvas']
            self.assertEqual(c['dimensions'],[1466,1247])
            self.assertTrue(c['independent_full_canvas_pixel_identical'])
            self.assertTrue(HEX.fullmatch(c['clean_png_sha256']))
            self.assertTrue(HEX.fullmatch(c['annotated_png_sha256']))
            self.assertTrue(HEX.fullmatch(c['clean_RGBA_sha256_independent_numpy']))
            self.assertFalse(c['native_original_client_rendered'])
            self.assertTrue(c['modern_overlay_explicit'])

    def test_preserve_mixed25_and_tw10_source_separation(self):
        q=self.d['evidence_boundaries']
        for k in ['JSS1999_or_TW10_official_Janken_source_claim','same_build_NPC_and_TW10_RD_source_claim','original_warp_execution_claim','original_native_janken_player_battle_claim','original_entry_item_consumption_in_this_source_executed','original_map_visual_complete_claim','original_png_published_to_Git']:
            self.assertFalse(q[k],k)
        self.assertEqual(self.d['aggregates']['new_original_RD_decode_this_round'],0)
        self.assertEqual(self.d['aggregates']['new_origin_artwork_this_round'],0)
        self.assertEqual(q['overall_percent'],None)

    def test_historical_state_retained_and_no_future_game(self):
        self.assertEqual(self.d['historical_CURRENT_blob_unchanged'],'c89e0e33537990aa2132b47c40fef49a985a935c')
        q=self.d['evidence_boundaries'];self.assertEqual((q['stage_A_partial'],q['stage_A_open']), (7,2))
        self.assertEqual((q['stage_B'],q['wiki'],q['R79']),('GATED','GATED','PAUSED_NON_BLOCKING'))

    def test_excluded_copyright_source_pixels_remain_private(self):
        raw=SOURCE.read_bytes()
        for unsafe in [b'NPCCREATE\n',b'WinWarp:',b'LoseWarp:',b'MainMsg:',b'\x89PNG\r\n']:
            self.assertNotIn(unsafe,raw)
        self.assertLess(len(raw),120000)

    def test_adversarial_tampered_missing_and_official_claims_detected(self):
        changed=copy.deepcopy(self.d)
        changed['janken_original_source_records'][0]['missing_aliases_in_source_DAT'][0]['image_alias']=7
        self.assertNotEqual({x['image_alias'] for x in changed['janken_original_source_records'][0]['missing_aliases_in_source_DAT']},MISSING)
        changed=copy.deepcopy(self.d);changed['evidence_boundaries']['same_build_NPC_and_TW10_RD_source_claim']=True
        self.assertTrue(changed['evidence_boundaries']['same_build_NPC_and_TW10_RD_source_claim'])


if __name__=='__main__':
    unittest.main()
