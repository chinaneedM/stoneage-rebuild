"""Check the public evidence for the Qikaka chief house and event20 sources."""
from hashlib import sha1
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'research/recovered/STONEAGE-INTEGRATION29-QIKAKA-CHIEF-HOUSE-EVENT20-SOURCE-R1.json'
PINS={
    'i27':'8b23611accca4f26b9322da55261a768b52d701e',
    'i28':'4b5b44c7be55b5b68b8b3ded57b73ceb2c014891',
    'accept28':'4e1642b9401c40e75520c287e0665058592b6c66',
    'map09':'137580e7c25aadf3d679b6ebfb5080b79912cc4f',
    'quest15':'e18743c702ee979cc96f009bed4d4f62a27f5bbc',
    'world11':'f79d7355a4e82c2bd8c0a771b898690cc4a3e680',
    'r40':'5b49d54d7cff2d79d3610db7ca4a37108f1f9e03',
}


def blob(raw):
    return sha1(f'blob {len(raw)}\0'.encode()+raw).hexdigest()


class Integration29(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads(REPORT.read_bytes())
        cls.pinned={k:(ROOT/v['path']).read_bytes() for k,v in cls.r['upstream'].items()}
        cls.source={k:json.loads(v) for k,v in cls.pinned.items()}

    def test_upstream_git_objects_and_preserved_current(self):
        self.assertEqual({k:blob(v) for k,v in self.pinned.items()},PINS)
        self.assertEqual({k:v['git_blob'] for k,v in self.r['upstream'].items()},PINS)
        current=self.r['historical_CURRENT']
        self.assertEqual(current,{'bytes':2709173,'git_blob':'c89e0e33537990aa2132b47c40fef49a985a935c'})
        self.assertEqual(blob((ROOT/'docs/CURRENT-STATE.md').read_bytes()[:current['bytes']]),current['git_blob'])

    def test_real_dat_and_base_room_replayed(self):
        ref=self.source['map09']['maps']['3406']
        old=self.source['i28']['whole_3400_portal_topology']
        self.assertEqual(self.r['archived_DAT_sha256'],
                         {f:old['original_DATs'][f]['sha256'] for f in ('3400','3406')})
        self.assertEqual(self.r['archived_DAT_sha256']['3406'],ref['source_sha256'])
        self.assertEqual(self.r['original_ls2map_sha256'],old['original_indoor_LS2MAP_names']['3406']['sha256'])
        room=self.r['room']
        self.assertEqual(room['base_RGBA_by_mode'],ref['frame_RGBA_sha256'])
        self.assertEqual(room['canvas_size'],ref['canvas_size'])
        self.assertEqual(room['origin'],ref['origin'])
        self.assertEqual(len(room['alias_counts']),62)
        self.assertEqual(sum(room['alias_counts'].values()),ref['draw_positions'])
        pre=self.source['accept28']['next_source_ready_work']['preflight']
        self.assertEqual(room['combined_RGBA_sha256'],pre['combined_candidate_RGBA_sha256'])
        self.assertNotEqual(room['combined_RGBA_sha256'],room['base_RGBA_by_mode']['combined'])

    def test_three_unchanged_directions(self):
        old=self.source['i28']
        expected=[r for r in old['whole_3400_portal_topology']['directions']
                  if 3406 in (r['start'][0],r['target'][0])]
        self.assertEqual(self.r['routes'],expected)
        self.assertEqual([r['mapwarp_line'] for r in expected],[768,769,770])
        self.assertEqual([r['exact_reverse'] for r in expected],[True,True,False])
        self.assertEqual(expected[2]['start'],[3406,10,16])
        self.assertNotIn(([3400,54,62],[3406,10,16]),[(r['start'],r['target']) for r in expected])
        self.assertEqual(self.r['original_mapwarp_sha256'],old['mapwarp_sha256'])
        self.assertEqual(self.r['original_warp_create_sha256'],
                         old['whole_3400_portal_topology']['member_files']['warp_y2.create']['sha256'])

    def test_original_creates_and_all_14_script_sections(self):
        q=self.source['quest15']
        rows=self.r['npcs']
        self.assertEqual([r['name'] for r in rows],['吉德的朋友','吉德','吉德的兒子'])
        self.assertEqual([r['event_count'] for r in rows],[5,6,3])
        self.assertEqual([r['alias'] for r in rows],[16030,16017,16046])
        for r,c in zip(rows,q['original_creates'][:3],strict=True):
            self.assertEqual((r['ordinal'],r['floor'],r['xy'],r['alias'],r['direction'],r['script_ref']),
                (c['ordinal'],c['source_floor'],c['source_borncorner'][:2],c['graphic_alias_not_image_identity'],
                 c['direction'],c['script_ref']))
            self.assertEqual(r['create_block_sha256'],c['source_block_sha256'])
            script=next(s for s in q['original_scripts'] if s['path']==r['script_ref'])
            self.assertEqual(r['script_sha256'],script['source_sha256'])
            self.assertEqual(r['events'],script['events'])

    def test_two_indoor_pixel_candidates_and_projection(self):
        rows=self.r['npcs'][1:]
        pre=self.source['accept28']['next_source_ready_work']['preflight']['rows']
        for row,old in zip(rows,pre,strict=True):
            self.assertEqual(row['source_u16'],old['original_DAT_u16'])
            pin=next(p for p in self.source['world11']['decoded_static_graphics'] if p['graphic']==row['alias'])
            v=row['static_candidate']
            self.assertEqual(v['top_left'],old['candidate_top_left_px'])
            self.assertEqual(v['signed_offset'],pin['signed_adrn_offset'])
            self.assertEqual(v['size'],pin['dimensions'])
            for field in ('png_sha256','rd_sha256','rgba_sha256'):
                self.assertEqual(v[field],pin[field])

    def test_outside_sprite_is_direct_adrn_rd_and_base_is_pinned(self):
        old=self.source['i28']['whole_3400']
        outside=self.r['outdoor']
        self.assertEqual(outside['source_full_RGBA_sha256'],old['rgba_sha256_by_mode']['combined'])
        self.assertEqual(outside['origin'],old['origin'])
        self.assertNotEqual(outside['inspection_RGBA_sha256'],outside['base_inspection_RGBA_sha256'])
        exterior=self.r['npcs'][0]
        art=self.r['event20_original_graphic_namespaces']['16030']
        self.assertEqual((art['adrn_match_count'],art['spradrn_match_count']),(1,0))
        actual=exterior['static_candidate']
        self.assertEqual({k:actual[k] for k in art['static_candidate']},art['static_candidate'])
        self.assertEqual((actual['adrn_ordinal'],actual['bitmap'],actual['rd_bytes']),(5876,5876,2113))
        self.assertEqual(actual['rd_sha256'],'ae3ceca2f3e0d8412588e9cb900dcac1e31f80014651a900deae1f21d2374de4')
        x,y=exterior['xy']
        ox,oy=outside['origin']
        dx,dy=actual['signed_offset']
        self.assertEqual(actual['top_left'],[ox+(x+y)*32+dx,oy+(y-x)*24+dy])
        self.assertEqual(self.r['checked_original_graphics'],self.source['i27']['extraction']['complete_graphic_source_members'])

    def test_dungeon_namespaces_and_bounded_source_frame(self):
        art=self.r['event20_original_graphic_namespaces']
        self.assertEqual(set(art),{'16029','16030','16032','100431'})
        self.assertEqual(art['100431'],{'adrn_match_count':0,'spradrn_match_count':1,'static_candidate':None})
        nxt=self.r['next_source_ready_work']
        group=nxt['spr_100431']
        matches=[r for r in self.source['r40']['material']['all_index_rows'] if r[1]==100431]
        self.assertEqual(matches,[[group[k] for k in ('group_index','spr_no','offset','anim_count','reserved')]])
        self.assertEqual((group['end_offset'],group['frame_count'],group['sentinel_frames']),(2630856,592,0))
        self.assertEqual(nxt['explicit_frame_candidate_only']['bitmap'],87803)
        self.assertFalse(nxt['native_frame_selection_verified'])
        for n,c in zip(nxt['source_rows'],self.source['quest15']['original_creates'][3:],strict=True):
            self.assertEqual((n['floor'],n['xy'],n['alias'],n['script_ref']),
                             (c['source_floor'],c['source_borncorner'][:2],c['graphic_alias_not_image_identity'],c['script_ref']))
            self.assertEqual(n['source_DAT_sha256'],self.source['map09']['maps'][str(n['floor'])]['source_sha256'])

    def test_original_runtime_boundary_and_private_roundtrip(self):
        self.assertEqual(self.r['html'],{'script_sections':14,'svg_door_links':3,'svg_npc_links':3,
                                         'source_text_hashes_match':True})
        self.assertTrue(self.r['verification']['desktop_chromium_file_policy_blocked'])
        self.assertFalse(self.r['verification']['actual_browser_interaction_verified'])
        self.assertEqual(self.r['private_zip']['members'],30)
        self.assertTrue(self.r['private_zip']['roundtrip_SHA256_and_CRC_verified'])
        self.assertEqual(self.r['bounds'],{'native_client_or_server_executed':False,
            'original_event_or_warp_trigger_verified':False,'official_same_deployment_verified':False,
            'raw_proprietary_assets_published_in_Git':False,'stage_A':'7_PARTIAL_2_OPEN',
            'stage_B_wiki':'GATED','R79':'PAUSED_NON_BLOCKING','overall_percent':None})


if __name__=='__main__':
    unittest.main()
