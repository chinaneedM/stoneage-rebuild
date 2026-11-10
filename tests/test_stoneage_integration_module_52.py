"""Rights-safe original source relations; NEVER interprets private pixel composites as native gameplay."""
import json
import re
from collections import Counter
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]/'research'/'recovered'
I52=ROOT/'STONEAGE-INTEGRATION52-1021-DOJO-ORIGINAL-MAP09-300-CELL-PIXEL-SOURCE-R1.json'
I51=ROOT/'STONEAGE-INTEGRATION51-TWO-ORIGINAL-100-DOJOS-SOURCE-BRIDGE-R1.json'
MAP09=ROOT/'STONEAGE-MAP09-691-SOURCE-READY-SCENES-R1.json'
HEX=re.compile(r'^[a-f0-9]{64}$')

class TestActualOriginalDojoDATToNPCStageSpatialEvidence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s=json.loads(I52.read_text(encoding='utf-8'))
        cls.old=json.loads(I51.read_text(encoding='utf-8'))
        cls.map=json.loads(MAP09.read_text(encoding='utf-8'))
        cls.rows=cls.s['original_dojo_stage_map_source_cells']

    def test_reopened_original_DATs_match_existing_MAP09_custody_and_i51_original_manifest(self):
        oldmaps={(r['floor'],r['format']):r for r in self.old['map_floor_original_MAP01_manifest_rows']}
        for k,r in self.s['actual_original_DATs_reopened'].items():
            map09=self.map['maps'][k];i51=oldmaps[(int(k),'DAT')]
            self.assertEqual(r['bytes'],map09['source_bytes'])
            self.assertEqual(r['sha256'],map09['source_sha256'])
            self.assertEqual(r['sha256'],i51['original_sha256'])
            self.assertEqual(r['geometry'],map09['geometry'])
            self.assertEqual(r['bytes'],8+6*r['geometry'][0]*r['geometry'][1])
        self.assertEqual(set(self.s['actual_original_DATs_reopened']),{'1021','1022','1008'})

    def test_original_archive_identity_is_prior_verified_archive_no_new_file_count(self):
        p=self.s['private_archive_replayed_now']
        self.assertEqual(p['bytes'],46844444)
        self.assertEqual(p['sha256'],'d84d0800dd600798769dfb7251a1d7816588ac061ccc27812ac64a37922d4a8a')
        self.assertEqual(p['nested_original_DAT_zip_sha256'],self.map['original_DAT_archive']['sha256'])
        self.assertEqual(p['all_ZIP_member_CRC_passed'],4195)
        self.assertEqual(p['nested_original_DAT_member_CRC_passed'],955)
        self.assertTrue(p['selected_source_pixel_png_sha256_and_RGBA_sha256_checked'])
        self.assertEqual(self.s['nonclaims']['new_original_map_DAT_acquired_this_unit'],0)
        self.assertEqual(self.s['nonclaims']['new_original_tile_RD_decodes_this_unit'],0)

    def test_all_one_hundred_original_NPC_source_rows_match_previous_source_by_ordinal(self):
        self.assertEqual(len(self.rows),100)
        self.assertEqual([r['stage'] for r in self.rows],list(range(1,101)))
        for got,old in zip(self.rows,self.old['samdou_100_original_arg_stage_manifest']):
            self.assertEqual(got['source_NPC_arg_sha256'],old['original_arg_sha256'])
            self.assertEqual(got['opponent_xy'],old['original_create_coordinate_xy'])
            self.assertEqual(got['warp_0_xy'],old['two_original_create_warp_xy'][0])
            self.assertEqual(got['warp_1_xy'],old['two_original_create_warp_xy'][1])
            self.assertEqual(got['source_NPC_arg_target_floor_xy'],old['arg_warp_target_floor_xy'])

    def test_three_hundred_original_cells_all_have_spatial_presence_and_distinct_coordinates(self):
        locations=[]
        for row in self.rows:
            for suffix in ('opponent','warp_0','warp_1'):
                x,y=row[f'{suffix}_xy']
                locations.append((x,y))
                self.assertTrue(0<=x<407 and 0<=y<144)
                cell=row[f'original_map_DAT_three_planes_at_{suffix}']
                self.assertEqual(len(cell),3)
                self.assertGreater(cell[0],99)
                self.assertEqual(cell[1],0)
                self.assertTrue(0<=cell[2]<=65535)
        self.assertEqual(len(locations),300)
        self.assertEqual(len(set(locations)),300)
        self.assertEqual(self.s['coordinate_and_alias_replay']['unique_source_xy_points'],300)

    def test_ground_plane_0_matches_exact_source_cell_aggregation(self):
        value_by_kind={}
        for suffix,kind in [('opponent','opponent'),('warp_0','warp_0'),('warp_1','warp_1')]:
            ground=Counter(r[f'original_map_DAT_three_planes_at_{suffix}'][0] for r in self.rows)
            value_by_kind[kind]={str(k):v for k,v in sorted(ground.items())}
            self.assertEqual(value_by_kind[kind],self.s['coordinate_and_alias_replay']['tile_source_values_by_role'][kind]['ground_plane0'])
            self.assertEqual(sum(ground.values()),100)
        self.assertEqual(value_by_kind['opponent'],{'4008':55,'5062':21,'5087':24})
        self.assertEqual(value_by_kind['warp_0'],{'4000':23,'4007':24,'4008':53})
        self.assertEqual(value_by_kind['warp_1'],{'4003':23,'4008':77})

    def test_opaque_plane2_not_silently_converted_to_collision_or_activation_flags(self):
        for kind in ('opponent','warp_0','warp_1'):
            distinct=len({r[f'original_map_DAT_three_planes_at_{kind}'][2] for r in self.rows})
            self.assertEqual(distinct,self.s['coordinate_and_alias_replay']['tile_source_values_by_role'][kind]['opaque_plane2_distinct_codes'])
        self.assertTrue(self.s['coordinate_and_alias_replay']['all_300_source_points_original_plane2_uninterpreted'])
        self.assertFalse(self.s['nonclaims']['native_collision_movement_or_opaque_plane2_event_meaning_verified'])

    def test_endpoints_reopen_exact_original_dat_location(self):
        self.assertEqual(self.s['actual_target_floor_probe'],{'1022_(1,7)':[4085,0,49152],'1008_(20,20)':[5046,0,49152]})
        self.assertEqual(self.s['original_source_literal_floor_targets']['entry_warp'],[1022,1,7])
        self.assertEqual(self.s['original_source_literal_floor_targets']['last_enemy_death_source_parameter'],[1008,20,20])
        self.assertEqual(self.rows[-1]['source_NPC_arg_target_floor_xy'],[1008,20,20])
        self.assertEqual(self.rows[0]['source_NPC_arg_target_floor_xy'],[1021,400,114])

    def test_private_six_crop_original_pixel_observations_have_real_source_draws(self):
        views=self.s['private_original_pixel_observation']['candidate_visual_crops']
        self.assertEqual(len(views),6)
        self.assertEqual([v['original_floor'] for v in views],[1021]*4+[1022,1008])
        self.assertEqual([v['source_cell_xy'] for v in views[:4]],[self.rows[k-1]['opponent_xy'] for k in (1,10,51,100)])
        self.assertEqual([v['source_cell_xy'] for v in views[4:]],[[1,7],[20,20]])
        for v in views:
            self.assertGreater(v['candidate_cropped_original_tile_draw_occurrences'],0)
            self.assertGreater(v['candidate_cropped_original_tile_distinct_aliases'],0)
            self.assertLessEqual(v['candidate_cropped_original_tile_distinct_aliases'],v['candidate_cropped_original_tile_draw_occurrences'])
            for name in ('candidate_crop_before_marker_RGBA_sha256','modern_annotated_image_sha256'):
                self.assertRegex(v[name],HEX)
            self.assertEqual(v['original_DAT_cell_three_planes'][1],0)
        self.assertEqual(self.s['private_original_pixel_observation']['source_floor_1021_selected_stages'],[1,10,51,100])

    def test_pixel_projection_anchors_follow_MAP09_actual_origin_and_coords(self):
        views=self.s['private_original_pixel_observation']['candidate_visual_crops']
        for v in views:
            floor=str(v['original_floor']);m=self.map['maps'][floor];x,y=v['source_cell_xy']
            self.assertEqual(v['candidate_isometric_anchor_xy'],[m['origin'][0]+(x+y)*32,m['origin'][1]+(y-x)*24])
            rect=v['candidate_crop_source_rectangle_xywh']
            self.assertEqual(rect[2:],[720,520])
            self.assertEqual(v['candidate_isometric_anchor_xy'],[rect[0]+360,rect[1]+260])

    def test_comparative_3021_DAT_read_failure_preserved(self):
        self.assertEqual(self.old['existing_MAP01_original_metadata']['MAP01_previous_original_3021_DAT_extraction_error_preserved']['error_tag'],'File CRC error')
        self.assertNotIn('3021',self.s['actual_original_DATs_reopened'])
        self.assertFalse(self.s['nonclaims']['unrestored_3021_DAT_fixed'])

    def test_source_versions_cannot_imply_original_official_same_deployment_or_native_run(self):
        self.assertEqual(self.s['source_versions']['map_DAT'],'LATER_COMMUNITY_MIXED25_PRESERVED_DAT')
        self.assertFalse(self.s['source_versions']['authentic_original_commercial_same_deployment'])
        self.assertFalse(self.s['nonclaims']['100_NPCs_or_200_warps_native_loaded_or_executed'])
        self.assertFalse(self.s['nonclaims']['MAP09_candidate_pixel_composition_is_original_client_renderer'])
        self.assertFalse(self.s['nonclaims']['original_source_NPC_text_or_images_published'])
        self.assertFalse(self.s['private_original_pixel_observation']['original_or_derived_pixel_assets_in_public_Git'])

    def test_stage_A_not_upgraded_and_history_blob_unchanged(self):
        self.assertEqual(self.s['stage_A'],'7 PARTIAL + 2 OPEN')
        self.assertEqual(self.s['stage_B'],'GATED')
        self.assertIsNone(self.s['overall_percent'])
        self.assertEqual(self.s['preserved_CURRENT_original_git_blob_sha'],'c89e0e33537990aa2132b47c40fef49a985a935c')

if __name__=='__main__': unittest.main()
