"""Public replay of the 3400 scene, source custody and directed door joins."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'research/recovered/STONEAGE-INTEGRATION28-QIKAKA-VILLAGE-SCENE-SOURCE-R1.json'
BLOBS = {
    'i10': '4b91fd0f0115bc58fed182b2f36468d5e3b117b2',
    'i20': '53497d591604794b74180c3162e07204cdd0c9f8',
    'i27': '8b23611accca4f26b9322da55261a768b52d701e',
    'accept27': '62f4e0dd587552c0739875349fb6caff1d637a2f',
    'map04': '1ef8c004179128ea44ffa4fb4259748bc8c83911',
    'map09': '137580e7c25aadf3d679b6ebfb5080b79912cc4f',
    'map09_custody': '5d6b591c659563aef24d93a30d314dd1d13b8d2c',
}


def git_blob(raw):
    return hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest()


class Integration28Source(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = json.loads(REPORT.read_bytes())
        cls.pins = {k: (ROOT/v['path']).read_bytes() for k, v in cls.r['upstream'].items()}
        cls.sources = {k: json.loads(v) for k, v in cls.pins.items()}

    def test_remote_upstreams_and_historical_current(self):
        self.assertEqual({k: git_blob(v) for k,v in self.pins.items()}, BLOBS)
        self.assertEqual({k: v['git_blob'] for k,v in self.r['upstream'].items()}, BLOBS)
        current = (ROOT/'docs/CURRENT-STATE.md').read_bytes()
        self.assertEqual(self.r['historical_CURRENT'],
                         {'bytes':2709173,'git_blob':'c89e0e33537990aa2132b47c40fef49a985a935c'})
        self.assertEqual(git_blob(current[:2709173]), self.r['historical_CURRENT']['git_blob'])

    def test_3400_dat_already_archived_in_i10(self):
        old = next(row for row in self.sources['i10']['recovered_DAT'] if row['floor']==3400)
        other = self.sources['i27']['exterior_3400']
        self.assertEqual(self.r['exterior_DAT_sha256'], old['sha256'])
        self.assertEqual(self.r['exterior_DAT_sha256'], other['sha256'])
        self.assertEqual(self.r['whole_3400']['geometry'], [old['width'], old['height']])
        self.assertEqual(self.r['whole_3400']['geometry'], [120,120])

    def test_window_scope_and_exact_extra_alias(self):
        w = self.r['window']
        former = self.sources['accept27']['next_source_ready_work']
        self.assertEqual(w['source_window'], [48,44,59,54])
        self.assertEqual(w['geometry'], [12,11])
        self.assertEqual(w['draw_positions'], former['window_tile_placements'])
        self.assertEqual(len(w['alias_counts']), former['distinct_aliases'])
        self.assertEqual(sum(w['alias_counts'].values()),136)
        self.assertEqual(w['canvas_size'],[768,599])
        self.assertEqual(w['map09_identical_PNG_count'],40)
        pin=former['actual_map04_extra_private_candidate']
        self.assertEqual(w['map04_extra_window_alias'],pin['alias'])
        self.assertEqual(w['alias_counts'][str(pin['alias'])],1)
        self.assertEqual(self.r['matched_legacy_RD'][str(pin['alias'])],pin['original_RD_sha256'])
        self.assertEqual(set(w['rgba_sha256_by_mode']),{'plane0','plane1','combined'})

    def test_whole_floor_only_uses_qualified_original_blocks(self):
        w = self.r['whole_3400']
        legacy = self.r['matched_legacy_RD']
        new = self.r['new_mixed25_RD']
        map04 = {str(row[0]):row for row in self.sources['map04']['source_TW1_real_RD_rows']}
        self.assertEqual(w['draw_positions'],6461)
        self.assertEqual(sum(w['alias_counts'].values()),6461)
        self.assertEqual(len(w['alias_counts']),329)
        self.assertEqual(w['canvas_size'],[7649,5745])
        self.assertEqual(len(legacy),321)
        self.assertEqual(set(new),{str(n) for n in range(3109,3117)})
        self.assertFalse(new.keys() & map04.keys())
        self.assertEqual(set(w['alias_counts']),legacy.keys() | new.keys())
        self.assertEqual(legacy,{key:map04[key][5] for key in legacy})
        self.assertEqual(self.r['qualification']['MAP04_TW10_RD_blocks_exact_mixed25_match'],321)
        self.assertEqual(self.r['qualification']['whole_and_window_base_modes_replayed'],6)

    def test_eight_unique_adrn_and_rd_records(self):
        tiles = self.r['new_mixed25_RD']
        self.assertEqual(len({tile['rd_sha256'] for tile in tiles.values()}),8)
        for key,row in tiles.items():
            self.assertEqual(row['source'],'mixed25_original_ADRN_REAL')
            self.assertEqual(row['ordinal'], int(key)-1990)
            self.assertEqual(row['bitmap'],row['ordinal'])
            self.assertEqual((row['width'],row['height'],row['xoff'],row['yoff']),(64,47,-32,-24))
            for field in ('adrn_sha256','rd_sha256','indexed_sha256','png_sha256','rgba_sha256'):
                self.assertRegex(row[field],r'^[0-9a-f]{64}$')
        coords = {row['alias']:row['xy'] for row in self.r['whole_3400']['new_alias_placements']}
        self.assertEqual(coords, {3109:[25,54],3110:[25,55],3111:[25,56],3112:[26,54],
                                  3113:[26,55],3114:[26,56],3115:[26,57],3116:[27,54]})
        self.assertTrue(all(row['layer']=='tile' for row in self.r['whole_3400']['new_alias_placements']))
        self.assertTrue(self.r['qualification']['two_independent_RD_decoders'])

    def test_pet_shop_scene_and_four_source_links(self):
        old_room = self.sources['i20']['rooms']['3403']
        room = self.r['interior']
        self.assertEqual(room['combined_RGBA_sha256'],old_room['candidate_canvas']['full_RGBA_sha256']['combined'])
        self.assertEqual(room['canvas_size'],old_room['candidate_canvas']['size_px'])
        self.assertEqual(self.r['interior_DAT_sha256'],old_room['original_DAT']['sha256'])
        window = self.r['window']
        x0,y0,x1,y1=room['inspection_crop_xyxy']
        self.assertEqual(room['inspection_size'],[x1-x0,y1-y0])
        for current,old in zip(self.r['directed_links'],self.sources['i27']['exterior_3400']['edges'],strict=True):
            self.assertEqual({k:current[k] for k in old},old)
            floor,x,y=current['start']
            ox,oy=(window if floor==3400 else room)['origin']
            if floor==3400:
                x-=48
                y-=44
            px,py=ox+(x+y)*32,oy+(y-x)*24
            self.assertEqual(current['start_pixel'],[px,py])
            if floor==3403:
                self.assertTrue(x0+17<=px<=x1-17 and y0+17<=py<=y1-17)

    def test_all_direction_shapes_and_displaced_entry_exit(self):
        t=self.r['whole_3400_portal_topology']
        rows=t['directions']
        pairs={(tuple(row['start']),tuple(row['target'])) for row in rows}
        self.assertEqual(len(pairs),33)
        self.assertEqual([r['mapwarp_line'] for r in rows],list(range(603,613))+list(range(752,775)))
        for row in rows:
            source,target=tuple(row['start']),tuple(row['target'])
            self.assertEqual(row['exact_reverse'],(target,source) in pairs)
            self.assertIn(3400,(source[0],target[0]))
            for field in ('start_u16','target_u16'):
                self.assertEqual(len(row[field]),3)
                self.assertTrue(all(0<=v<=65535 for v in row[field]))
            for node in (source,target):
                w,h=t['original_DATs'][str(node[0])]['geometry']
                self.assertTrue(0<=node[1]<w and 0<=node[2]<h)
        self.assertEqual(sum(row['exact_reverse'] for row in rows),22)
        external=[r for r in rows if 200 in (r['start'][0],r['target'][0])]
        self.assertEqual(len(external),10)
        self.assertTrue(all(not row['exact_reverse'] for row in external))
        indoor=[r for r in rows if r not in external and not r['exact_reverse']]
        self.assertEqual([(r['start'],r['target']) for r in indoor],[([3406,10,16],[3400,54,62])])
        self.assertEqual(t['counts'],{'all_directions':33,'with_exact_reverse':22,
                                      'to_or_from_200_displaced':10,'indoor_without_exact_reverse':1})

    def test_direction_records_match_original_create_partitions(self):
        rows=self.r['whole_3400_portal_topology']['directions']
        self.assertEqual([r['create_ordinal'] for r in rows[:10]],list(range(60,70)))
        self.assertEqual([r['create_file'] for r in rows[:10]],['200warp.create']*10)
        self.assertEqual([r['create_ordinal'] for r in rows[10:]],list(range(139,162)))
        self.assertEqual([r['create_file'] for r in rows[10:]],['warp_y2.create']*23)
        self.assertEqual(len({r['create_sha256'] for r in rows}),33)
        existing={r['mapwarp_line']:r for r in self.sources['i27']['verified_original_configuration']['lines']}
        for row in rows[10:14]:
            old=existing[row['mapwarp_line']]
            for key in ('mapwarp_line_sha256','create_sha256','create_ordinal'):
                self.assertEqual(row[key],old[key if key.startswith('mapwarp') else 'warp_CREATE_'+key[7:]])

    def test_destination_map_provenance_and_original_room_names(self):
        t=self.r['whole_3400_portal_topology']
        i10={str(r['floor']):r for r in self.sources['i10']['recovered_DAT']}
        self.assertEqual(set(t['original_DATs']),{'200','3400','3403','3404','3405','3406','3409','3412'})
        for floor,row in t['original_DATs'].items():
            expected = i10[floor]['sha256'] if floor in ('200','3400') else self.sources['map09']['maps'][floor]['source_sha256']
            self.assertEqual(row['sha256'],expected)
            w,h = row['geometry']
            self.assertEqual(row['bytes'],8+6*w*h)
        self.assertEqual(set(t['original_indoor_LS2MAP_names']),set(t['original_DATs'])-{'200','3400'})
        self.assertEqual(t['original_indoor_LS2MAP_names']['3406']['name'],'奇喀喀的村長家')

    def test_preserves_observer_boundaries(self):
        self.assertTrue(self.r['qualification']['private_HTML_static_routes_and_images_checked'])
        self.assertFalse(self.r['qualification']['browser_runtime_checked'])
        self.assertEqual(self.r['private_zip']['members'],373)
        self.assertTrue(self.r['private_zip']['roundtrip_SHA256_and_CRC_verified'])
        self.assertEqual(self.r['bounds'],{'original_client_or_server_executed':False,
            'native_collision_palette_layering_or_warp_proven':False,'official_same_deployment_proven':False,
            'raw_proprietary_assets_published_in_Git':False,'stage_A':'7_PARTIAL_2_OPEN',
            'stage_B_wiki':'GATED','R79':'PAUSED_NON_BLOCKING','overall_percent':None})


if __name__=='__main__':
    unittest.main()
