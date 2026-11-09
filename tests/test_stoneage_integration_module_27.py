"""Replay public joins for the four tutors and the 3400 exterior door cells."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'research/recovered/STONEAGE-INTEGRATION27-PET-TUTORS-AND-3400-DAT-SOURCE-R1.json'
UPSTREAM = {
    'i17': 'e716f01bbf7d08be2e13654909282a198f5334dd',
    'r4': '0f1ac43bd3abb11b360a040e842dcac11d159e9a',
    'i20': '53497d591604794b74180c3162e07204cdd0c9f8',
    'i21': '56fd04d1bc47b20ed6c5ca26c91e7bbb6f892ad7',
    'map09': '137580e7c25aadf3d679b6ebfb5080b79912cc4f',
    'map09_custody': '5d6b591c659563aef24d93a30d314dd1d13b8d2c',
    'world11': 'f79d7355a4e82c2bd8c0a771b898690cc4a3e680',
}


def git_blob(raw):
    return hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest()


class Integration27Source(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads(REPORT.read_bytes())
        cls.sources = {
            key: (row, (ROOT / row['path']).read_bytes())
            for key, row in cls.report['upstream'].items()
        }
        cls.inputs = {key: json.loads(raw) for key, (_, raw) in cls.sources.items()}

    def test_exact_upstream_git_blobs(self):
        self.assertEqual(set(self.sources), set(UPSTREAM))
        for key, (row, raw) in self.sources.items():
            self.assertEqual(git_blob(raw), UPSTREAM[key], key)
            self.assertEqual(row['git_blob'], UPSTREAM[key], key)

    def test_current_history_prefix_preserved(self):
        raw = (ROOT / 'docs/CURRENT-STATE.md').read_bytes()
        history = self.report['historical_CURRENT']
        self.assertEqual(history, {'bytes': 2709173, 'git_blob': 'c89e0e33537990aa2132b47c40fef49a985a935c'})
        self.assertEqual(git_blob(raw[:history['bytes']]), history['git_blob'])

    def test_full_source_members_and_two_exact_sprites(self):
        report = self.report
        self.assertEqual(report['parent_rar'], self.inputs['i17']['parent_rar'])
        self.assertEqual(report['extraction']['complete_graphic_source_members'],
                         self.inputs['world11']['original_files'])
        self.assertEqual(report['extraction']['verified_adrn_records'], 234564)
        self.assertEqual(report['extraction']['verified_spradrn_records'], 847)
        self.assertEqual(report['extraction']['selected_spr_matches'], 0)
        self.assertEqual(report['graphics'], self.inputs['i17']['tutor_source_preflight']['graphics'])
        self.assertEqual([row['graphic'] for row in report['graphics']], [16122, 16127])
        self.assertEqual([row['bitmap'] for row in report['graphics']], [232699, 232704])
        self.assertEqual(report['verification']['separate_rd_decoders'], 2)
        self.assertEqual(report['verification']['exact_indexed_pngs_match_i17'], 2)

    def test_four_distinct_source_create_placements(self):
        report = self.report
        rooms = report['rooms']
        self.assertEqual([r['floor'] for r in rooms], [1003, 2003, 3003, 4003])
        self.assertEqual([r['alias'] for r in rooms], [16122, 16127, 16122, 16122])
        self.assertEqual(len({r['create_sha256'] for r in rooms}), 4)
        graphics = {r['graphic']: r for r in report['graphics']}
        for current, old in zip(rooms, self.inputs['r4']['four_rooms'], strict=True):
            create = old['original_create']
            source = self.inputs['map09']['maps'][str(current['floor'])]
            self.assertEqual((current['floor'], current['create_ordinal'], current['create_sha256'],
                              current['xy'], current['alias']),
                             (old['floor'], create['ordinal'], create['block_sha256'],
                              create['borncenter'], create['graphic_alias']))
            graphic = graphics[current['alias']]
            x, y = current['xy']
            ox, oy = source['origin']
            sx, sy = graphic['signed_adrn_offset']
            self.assertEqual(current['placement_xy'], [ox+(x+y)*32+sx, oy+(y-x)*24+sy])
            self.assertEqual(current['placement_xy'], old['candidate_pixel_geometry']['modern_sprite_top_left_xy'])
            self.assertEqual(current['sprite_dimensions'], graphic['dimensions'])
            self.assertEqual(current['canvas_size'], source['canvas_size'])

    def test_base_canvases_and_overlay_deltas(self):
        for room in self.report['rooms']:
            source = self.inputs['map09']['maps'][str(room['floor'])]
            self.assertEqual(room['source_DAT_sha256'], source['source_sha256'])
            self.assertEqual(room['verified_base_states'], source['frame_RGBA_sha256'])
            self.assertEqual(room['base_RGBA_sha256'], source['frame_RGBA_sha256']['combined'])
            self.assertEqual(room['tile_placements'], source['draw_positions'])
            self.assertNotEqual(room['overlay_RGBA_sha256'], room['base_RGBA_sha256'])
            self.assertNotEqual(room['overlay_PNG_sha256'], room['base_PNG_sha256'])
            width, height = room['sprite_dimensions']
            self.assertGreater(room['changed_canvas_pixels'], 0)
            self.assertLessEqual(room["changed_canvas_pixels"], room["opaque_sprite_pixels"])
            self.assertLessEqual(room['opaque_sprite_pixels'], width * height)
            for field in ('base_PNG_sha256','overlay_PNG_sha256','overlay_RGBA_sha256'):
                self.assertRegex(room[field], r'^[0-9a-f]{64}$')
        self.assertEqual(self.report['verification']['complete_base_rgba_replays'], 12)
        self.assertEqual(self.report['verification']['independent_composite_rgba_replays'], 4)

    def test_3400_three_plane_member_keeps_old_map_distinct(self):
        exterior = self.report['exterior_3400']
        old = self.inputs['i20']['original_3400_source_boundary']
        aux = self.inputs['i21']['independent_3400_single_plane_auxiliary_observation']
        w, h = exterior['geometry']
        self.assertEqual((w, h), (120, 120))
        self.assertEqual(exterior['bytes'], 8+6*w*h)
        self.assertEqual(exterior['bytes'], old['named_RAR_member_size'])
        self.assertEqual(exterior['crc32'], old['named_RAR_member_header_crc32'])
        self.assertEqual(exterior['sha256'], 'a3c6918ba21c909e6312329c936615aa6b6d8800d7967ed85a2146d55ca263c4')
        self.assertNotEqual(exterior['sha256'], aux['source_sha256'])
        self.assertFalse(old['successful_full_3400_DAT_extraction_this_work'])
        self.assertFalse(aux['actual_same_source_three_plane_3400_DAT_qualified'])

    def test_four_directions_and_two_distinct_exterior_cells(self):
        exterior = self.report['exterior_3400']
        prior = self.inputs['i20']['rooms']['3403']
        self.assertEqual(exterior['original_3403_DAT_sha256'], prior['original_DAT']['sha256'])
        self.assertEqual(len(exterior['edges']), 4)
        expected = {(53, 49): [375, 0, 49155], (54, 49): [391, 0, 49155]}
        width, height = exterior['geometry']
        directions = set()
        for new, old in zip(exterior['edges'], prior['original_directed_edges'], strict=True):
            self.assertEqual({k: new[k] for k in old}, old)
            outside, inside = sorted((new['start'],new['target']))
            self.assertEqual([outside[0], inside[0]], [3400, 3403])
            x,y = new['exterior_xy']
            self.assertEqual([x,y], outside[1:])
            self.assertEqual(new['exterior_DAT_u16'], expected[(x,y)])
            self.assertEqual(new['exterior_DAT_u16_offsets'],
                             [8+2*(p*width*height+y*width+x) for p in range(3)])
            directions.add((tuple(new['start']),tuple(new['target'])))
        self.assertEqual(len(directions), 4)
        self.assertEqual(directions, {(target,start) for start,target in directions})

    def test_original_config_and_dialogue_custody(self):
        report = self.report
        original = report['verified_original_configuration']
        self.assertEqual(original['members']['mapwarp.txt']['sha256'],
                         self.inputs['i17']['original_mapwarp_sha256'])
        self.assertEqual(original['members']['newbie.create']['sha256'], report['original_create_file_sha256'])
        self.assertEqual(original['members']['petmaster']['sha256'], report['original_script_sha256'])
        script = self.inputs['r4']['shared_private_original_script']
        self.assertEqual(report['original_script_sha256'], script['sha256'])
        self.assertEqual(report['dialogue_entries'],
                         script['dialogue_original_main_count']+script['dialogue_original_window_count'])
        for config,edge in zip(original['lines'], report['exterior_3400']['edges'], strict=True):
            self.assertEqual(config['warp_CREATE_file'], 'genout/warp_y2.create')
            for key in ('mapwarp_line','warp_CREATE_ordinal','warp_CREATE_sha256'):
                self.assertEqual(config[key], edge[key])
            self.assertRegex(config['mapwarp_line_sha256'], r'^[0-9a-f]{64}$')

    def test_observation_does_not_claim_native_or_official_runtime(self):
        report = self.report
        self.assertTrue(report['private_HTML_static_references_verified'])
        self.assertFalse(report['browser_render_verified'])
        self.assertTrue(report['verification']['private_zip_roundtrip_whole_sha256_and_crc_verified'])
        self.assertEqual(report['bounds'], {
            'native_client_or_server_executed': False,
            'native_palette_layer_order_or_collision_verified': False,
            'native_dialogue_or_warp_executed': False,
            'official_same_deployment_verified': False,
            'proprietary_originals_in_public_git': False,
            'stage_A': '7_PARTIAL_2_OPEN',
            'stage_B_wiki': 'GATED',
            'R79': 'PAUSED_NON_BLOCKING',
            'overall_percent': None,
        })


if __name__ == '__main__':
    unittest.main()
