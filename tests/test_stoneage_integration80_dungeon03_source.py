"""INTEGRATION80 original static dungeon03 NPC warp / DAT derived evidence guard.
No commercial NPC, DAT, or sprite payload is required to validate these public facts.
"""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / 'research/recovered/STONEAGE-INTEGRATION80-DUNGEON03-NPC-WARP-DAT-SOURCE-R1.json'


class SourceBoundDungeon03(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = json.loads(RECEIPT.read_text(encoding='utf-8'))
        cls.rows = cls.d['static_warp_creates']
        cls.maps = cls.d['original_DATs']
        cls.count = cls.d['bounded_counts']

    def test_source_sha_bytes(self):
        s=self.d['original_create_source']
        self.assertEqual((s['bytes'], s['sha256']), (1621,'baf71a27eb74958c37e85ea362e16e0cf515bf31f1a3c5c08ee3ed0c55e267e8'))
        self.assertEqual(s['original_RAR_header_CRC32_recorded_int'],4284489019)

    def test_parent_exact_custody(self):
        r=self.d['original_parent_archive']
        self.assertEqual(r['size_bytes'],361255180)
        self.assertEqual(r['sha256'],'d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5')
        self.assertIn('community',r['source_qualification'])

    def test_all_thirteen_from_distinct_contiguous_blocks(self):
        self.assertEqual([r['create_order'] for r in self.rows], list(range(1,14)))
        self.assertEqual(self.count['create_count'],13)
        intervals=[r['original_create_block_byte_interval_halfopen'] for r in self.rows]
        self.assertEqual(intervals[0],[121,230]);self.assertEqual(intervals[-1],[1518,1620])
        self.assertTrue(all(0<=a<b<=1621 for a,b in intervals))
        self.assertTrue(all(intervals[i][1]<intervals[i+1][0] for i in range(12)))
        self.assertEqual(len({r['original_create_block_sha256'] for r in self.rows}),13)

    def test_exact_map_ids_five_sources(self):
        self.assertEqual(set(self.maps),{'40','31301','31302','31401','31501'})
        self.assertEqual(self.count['qualified_verified_original_DAT_floor_count'],5)
        self.assertEqual(self.maps['40']['geometry_width_height'],[20,20])
        self.assertEqual(self.maps['31301']['geometry_width_height'],[40,120])
        self.assertEqual(self.maps['31302']['geometry_width_height'],[60,60])
        self.assertEqual(self.maps['31401']['geometry_width_height'],[120,40])
        self.assertEqual(self.maps['31501']['geometry_width_height'],[40,120])

    def test_map_lengths_and_digest_pins(self):
        expected={'40':'3c62e11cba026ab27b212d7450ebdc9b73859bb7f3037657b2a6b70a8d3ec874',
          '31301':'e8cd18b7abb1e8c11ef2790acf802a3362842bb3ae1387f8070b834740694731',
          '31302':'2d553684d1af4054330ab881d19559c5a8e323b8984f0f023f165fa2dde76dec',
          '31401':'01dac6cbef282ac90635361eeacf3a2745e1500294c4b15fcb728b0f03bcc6c8',
          '31501':'226e709f03a80b940a660a73e33ef8177e0561fc6cf3550fb114311c54d9ba41'}
        for key,m in self.maps.items():
            with self.subTest(floor=key):
                w,h=m['geometry_width_height']
                self.assertEqual(m['original_DAT_bytes'],8+6*w*h)
                self.assertEqual(m['original_DAT_sha256'],expected[key])
                self.assertTrue(m['source_map09_DAT_bytes_verified'])

    def test_pixel_candidate_counts_not_discoveries(self):
        self.assertEqual(sum(x['source_qualified_TW10_original_RD_scene_candidate'] for x in self.maps.values()),4)
        self.assertIsNone(self.maps['40']['MAP09_prior_scene_combined_RGBA_sha256'])
        self.assertEqual(self.count['new_original_RD_pixel_decode_count'],0)
        for m in self.maps.values():self.assertEqual(m['new_original_pixel_RLE_decodes_this_turn'],0)

    def test_exact_source_destination_values(self):
        pairs=[(r['source_floorid'],*r['source_xy'],r['target_floorid'],*r['target_xy']) for r in self.rows]
        self.assertEqual(pairs[9],(31301,9,51,31302,52,11))
        self.assertEqual(pairs[10],(31302,52,11,31301,9,51))
        self.assertEqual(pairs[11],(40,6,3,6000,32,68))
        self.assertTrue(all(r['original_enemy_kind']=='npcgen_warp' for r in self.rows))
        self.assertEqual(self.count['distinct_source_floorids'],9)

    def test_five_textual_reverse_pairs_only(self):
        reverse=[]
        for r in self.rows:
            expected=[t['create_order'] for t in self.rows if t['source_floorid']==r['target_floorid'] and t['source_xy']==r['target_xy'] and t['target_floorid']==r['source_floorid'] and t['target_xy']==r['source_xy']]
            self.assertEqual(r['reverse_create_orders'],expected)
            reverse.extend([(r['create_order'],i) for i in expected if r['create_order']<i])
        self.assertEqual(reverse,[(1,2),(4,5),(7,8),(10,11),(12,13)])
        self.assertEqual(len([r for r in self.rows if not r['reverse_create_orders']]),3)

    def test_candidate_geometry_and_missing_data_are_separate(self):
        for side in ('source','target'):
            for r in self.rows:
                floor=r[f'{side}_floorid'];xy=r[f'{side}_xy'];anchor=r[f'{side}_anchor']
                if str(floor) in self.maps:
                    w,h=self.maps[str(floor)]['geometry_width_height']
                    self.assertTrue(0<=xy[0]<w and 0<=xy[1]<h)
                    self.assertEqual(anchor['in_bounds'],True)
                    self.assertEqual(len(anchor['original_DAT_three_plane_values_at_xy']),3)
                else:
                    self.assertIsNone(anchor['in_bounds'])
                    self.assertIsNone(anchor['original_DAT_three_plane_values_at_xy'])

    def test_qualified_source_target_total(self):
        self.assertEqual(sum(r['source_anchor']['map_source_in_verified_five_DAT'] for r in self.rows),9)
        self.assertEqual(sum(r['target_anchor']['map_source_in_verified_five_DAT'] for r in self.rows),9)
        self.assertEqual(sum(r['source_anchor']['map_source_in_verified_five_DAT'] and r['target_anchor']['map_source_in_verified_five_DAT'] for r in self.rows),5)
        self.assertEqual(self.count['both_ends_in_qualified_DAT_count'],5)

    def test_numeric_three_plane_original_not_collisions(self):
        self.assertEqual(self.rows[9]['source_anchor']['original_DAT_three_plane_values_at_xy'],[4007,0,49155])
        self.assertEqual(self.rows[9]['target_anchor']['original_DAT_three_plane_values_at_xy'],[4005,0,49155])
        self.assertFalse(self.d['negative_evidence_boundary']['original_collision_semantics_of_third_DAT_plane_proven'])

    def test_no_false_original_executed_or_official_merge(self):
        n=self.d['negative_evidence_boundary']
        for key in ('original_NPC_runtime_spawn_observed','original_warp_execution_observed','actual_map_traversal_reachability_proven','TW10_official_client_same_deployment_as_mixed25_server_proven','original_official_version_attribution_proven','public_original_raw_DAT_or_NPC_bytes'):
            self.assertIs(n[key],False,key)
        self.assertTrue(n['source_missing_from_current_five_DAT_does_not_imply_historic_absence'])

    def test_historical_state_untouched(self):
        h=self.d['historical_CURRENT_unchanged']
        self.assertEqual(h['git_blob_sha'],'c89e0e33537990aa2132b47c40fef49a985a935c')
        self.assertEqual(h['size_bytes'],2709173)
        n=self.d['negative_evidence_boundary']
        self.assertEqual((n['stage_A_partial'],n['stage_A_open'],n['stage_B'],n['wiki'],n['overall_percent']), (7,2,'GATED','GATED',None))
        self.assertEqual(n['R79'],'PAUSED_NON_BLOCKING')

    def test_raw_source_not_embedded(self):
        self.assertFalse(self.d['original_create_source']['source_contains_original_commercial_text_in_public'])
        text=RECEIPT.read_text(encoding='utf-8')
        self.assertNotIn('NPCCREATE\n',text)
        self.assertNotIn('borncorner=',text)
        self.assertNotIn('enemy=npcgen_warp|',text)


if __name__ == '__main__':unittest.main()