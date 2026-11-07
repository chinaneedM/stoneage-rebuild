"""Source-bound dream cave: preserve branch order, duplicate warps and version gaps."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import unittest
from tools.stoneage_quest09_dream_cave_source import REPORT, SOURCE, ROOT, event_controls, create_controls


class DreamCaveSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads(REPORT.read_text())
        cls.source=json.loads(SOURCE.read_text())

    def test_original_members_and_all_117_create_slices(self):
        d=self.data;manifest={r[0]:r for r in self.source['source_files']}
        self.assertEqual(d['private_source_zip']['verified_members'],2205)
        self.assertEqual(d['private_source_zip']['verified_member_bytes'],1930332)
        self.assertEqual(len(d['source_files']),15)
        for row in d['source_files']:
            self.assertEqual([row['bytes'],row['sha256'],row['crc32']],manifest[row['path']][1:4])
        expected=[r for r in self.source['create_rows'] if r[0] in
                  ['seimu/event/event01.create','400/sb_mugen.create','genout/mugendungeon.create','genout/mugendungeon2.create']]
        self.assertEqual(len(d['source_creates']),117)
        for old,new in zip(expected,d['source_creates']):
            self.assertEqual([new['file'],new['ordinal'],new['start_byte'],new['end_byte'],new['block_sha256'],
                              new['floor'],new['graphic_alias'],new['borncorner_raw'],new['borncenter_raw']],old[:9])
            self.assertEqual(new['parameter_references'],old[15])

    def test_event_sequence_and_reward_operands(self):
        elder,sage=self.data['source_event_scripts']
        self.assertEqual([e['event_number'] for e in elder['events']],[34,33,32,-1,-1,-1])
        self.assertEqual([e['event_number'] for e in sage['events']],[173,34,33,32,-1,-1])
        self.assertEqual(elder['events'][0]['event'],'ENDEV=4&ENDEV=33&ENDEV=32')
        self.assertEqual(elder['events'][4]['event'],'LV>34,ENDEV=4&ENDEV=33&ENDEV=32&ENDEV=34')
        self.assertEqual(sage['events'][0]['event'],'ENDEV=4&ENDEV=34&ENDEV=33&ENDEV=32&ENDEV=105&NOWEV=172&ITEM=19550')
        self.assertFalse(sage['events'][0]['commands'])
        for event,item,flag in zip(sage['events'][1:4],[2604,2605,2606],[34,33,32]):
            self.assertEqual([(r['name'],r['item_id'],r['explicit_quantity']) for r in event['commands']],
                             [('DelItem',2603,None),('GetItem',item,None)])
            self.assertEqual(event['extra_controls'],[{'name':'EndSetFlg','values_in_source_order':[flag]}])
        pool=sage['events'][4]['extra_controls']
        self.assertEqual(pool,[{'name':'GetRandItem','values_in_source_order':
            [450,451,449,549,552,543,653,646,12623,12648,11895,11926,11936,12052,11803,11814,11824,11833,11843,11853]}])
        self.assertEqual(sage['events'][5]['event'],'LV>0,ENDEV=4&ITEM!=2603&ITEM!=19550')

    def test_warp_tokens_duplicates_and_day_night_are_not_normalized(self):
        warps=[r for r in self.data['source_creates'] if 'target_floor_x_y' in r]
        self.assertEqual(len(warps),106)
        self.assertEqual(Counter(r['trailing_token'] for r in warps),{None:101,'A':1,'M':3,'N':1})
        self.assertEqual(Counter(r['time_raw'] for r in self.data['source_creates']),{0:113,60000:4})
        self.assertTrue(all(r['time_raw']==60000 for r in self.data['source_creates'] if r['file']=='400/sb_mugen.create'))
        self.assertEqual(sorted(x['occurrences'] for x in self.data['repeated_original_warp_blocks']),[2,2])
        entrances=[r for r in warps if r['floor']==400]
        self.assertEqual([(r['borncorner_raw'][:2],r['target_floor_x_y'],r['trailing_token']) for r in entrances],
            [([97,119],[41,11,8],'A'),([98,119],[41,11,8],'M'),([97,120],[41,11,8],'M'),
             ([96,119],[41,11,8],'M'),([87,101],[42,11,8],'N')])
        self.assertEqual([(r['time_raw'],r['change_graphic_alias_raw']) for r in self.data['source_time_parameters']],
                         [('AFTER',16204),('AFTER',16204),('AFTER',16200),('AFTER',16200)])

    def test_guard_night_floor_retains_41_target_and_repeated_enemy_ids(self):
        guards=[r for r in self.data['source_creates'] if r['file']=='400/sb_mugen.create']
        self.assertEqual([r['floor'] for r in guards],[41,41,42,42])
        self.assertEqual([r['borncenter_raw'] for r in guards],[[34,41,1,1],[33,41,1,1]]*2)
        args=self.data['source_guard_arguments']
        self.assertEqual([r['warp_floor_x_y'] for r in args],[[41,34,39],[41,33,39]])
        self.assertTrue(all(r['enemy_instance_ids_in_source_order']==[1095,1095,1095,1087,1086,1096,1096,1096,1096,1096] for r in args))
        self.assertEqual([r[0] for r in self.data['prior_char09_enemy_numeric_rows']],[1086,1087,1095,1096])

    def test_guide_position_differences_and_bounds(self):
        p=self.data['prior_R68_documentary_positions']
        self.assertEqual(p['elder'],[73,55]);self.assertEqual(p['entrances'],{'day':[96,120],'night':[87,102]})
        elder=next(r for r in self.data['source_creates'] if r['file']=='seimu/event/event01.create' and r['floor']==6000)
        self.assertEqual(elder['borncorner_raw'],[73,54,73,54])
        self.assertFalse(p['exact_same_deployment_verified'])
        self.assertEqual(self.data['origin_class'],'ORIGIN_UNRESOLVED')
        self.assertTrue(all(v is False for v in self.data['boundaries'].values()))
        self.assertIsNone(self.data['status']['overall_percent'])

    def test_dependency_blobs_and_complete_item_ids(self):
        for path,expected in self.data['derived_input_blobs'].items():
            raw=(ROOT/path).read_bytes()
            self.assertEqual(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),expected)
        items={r[0]:r for r in self.data['prior_item01_numeric_rows']}
        self.assertEqual(len(items),25)
        for path in (ROOT/'research/recovered/item-module-01').glob('*DERIVED-INDEX-*-R1.json'):
            for row in json.loads(path.read_text())['rows']:
                if row[0] in items:self.assertEqual(items[row[0]],row)

    def test_parser_order_quantities_and_malformed_warp(self):
        raw=b'EventNo:32\r\nTYPE:ACCEPT\r\nEVENT:ITEM=1\r\nDelItem:1\r\nGetRandItem:9,8,9\r\nEndSetFlg:32\r\nEventEnd\r\n'
        e=event_controls(raw)[0]
        self.assertIsNone(e['commands'][0]['explicit_quantity'])
        self.assertEqual(e['extra_controls'],[{'name':'GetRandItem','values_in_source_order':[9,8,9]},
                                               {'name':'EndSetFlg','values_in_source_order':[32]}])
        self.assertEqual(create_controls(b'time=0\nenemy=npcgen_warp|42|11|8|N\n')['target_floor_x_y'],[42,11,8])
        with self.assertRaises(ValueError):create_controls(b'time=0\nenemy=npcgen_warp|42|11\n')

    def test_actual_private_map_observation_matches_qualified_prior_frames(self):
        p=ROOT/'research/recovered/STONEAGE-QUEST09-TWO-ORIGINAL-CAVE-MAPS-OBSERVATION-R1.json'
        visual=json.loads(p.read_text())
        prior=json.loads((ROOT/'research/recovered/STONEAGE-MAP09-691-SOURCE-READY-SCENES-R1.json').read_text())
        self.assertEqual(set(visual['maps']),{'41','42'})
        for floor,row in visual['maps'].items():
            old=prior['maps'][floor]
            self.assertEqual(row['source_DAT_sha256'],old['source_sha256'])
            self.assertEqual(row['three_full_frame_RGBA_sha256'],old['frame_RGBA_sha256'])
            self.assertEqual(row['geometry'],[70,70])
            self.assertEqual(row['canvas_size'],[4449,3345])
            self.assertEqual(row['source_candidate_PNGs_reread'],112)
            self.assertEqual(row['source_draw_positions'],3027 if floor=='41' else 3028)
            self.assertEqual([p['xy'] for p in row['source_points']],[[34,25],[34,41],[33,41],[11,8]])
            for point in row['source_points']:
                x,y=point['xy'];self.assertEqual(point['modern_anchor'],[16+(x+y)*32,1672+(y-x)*24])
                self.assertEqual(len(point['original_three_u16_values']),3)
        self.assertEqual(visual['source_MAP09_zip_sha256'],'d84d0800dd600798769dfb7251a1d7816588ac061ccc27812ac64a37922d4a8a')
        self.assertIs(visual['boundaries']['original_NPC_sprite_drawn'],False)
        self.assertIs(visual['boundaries']['native_walkability_verified'],False)
        self.assertEqual(visual['boundaries']['new_RD_decodes'],0)


if __name__=='__main__':unittest.main()
