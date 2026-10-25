"""Finite authentic metadata replay and synthetic original-file export guards."""
import copy
import hashlib
import json
from pathlib import Path
import struct
import tempfile
import unittest

from tools import stoneage_original_animation_lab as lab
from tools.stoneage_original_observation_lab import ROOT


class AnimationObservationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = lab.sample_report()

    def test_full_archived_report_exact(self):
        self.assertEqual(self.report,json.loads(lab.REPORT.read_text()))
        cases=self.report['cases']
        self.assertEqual([len(t['frames']) for t in cases],[12,7,6])
        self.assertEqual([t['frames'][0]['hold_ticks'] for t in cases],[5,8,6])
        self.assertEqual([t['cycle_ticks'] for t in cases],[60,56,36])
        self.assertEqual([f['bmp_no'] for f in cases[1]['frames']],
                         [10185,10186,10185,10185,10185,10185,10186])
        self.assertEqual(len(cases[0]['frames']),12)  # repeated bitmaps retain frame positions
        for t in cases:
            self.assertIsNone(t['source_tick_rate_hz'])
            for key in ['original_colors_reproduced','original_client_executed',
                        'transparency_verified','row_orientation_verified','sound_events_played']:
                self.assertIs(t[key],False)

    def test_missing_group_and_invalid_selector(self):
        for args in [(42,0,0),(100000,-1,0),(100000,0,65536),(True,0,0)]:
            with self.assertRaises(ValueError):lab.timeline(*args)

    def test_metadata_corruption_stops_before_decompression(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);(p/'SPR-GROUP-R1.tsv.gz').write_bytes(b'wrong')
            with self.assertRaisesRegex(ValueError,'SHA mismatch'):
                lab.timeline(100000,0,0,p)

    def fixture(self,p):
        group={'index':0,'spr_no':100000,'offset':0,'anim_count':1,'reserved':2,
               'end_offset':32,'next_offset':32}
        animation={'group_index':0,'spr_no':100000,'anim_index':0,'offset':0,
                   'direction':0,'anim_no':6,'duration':64,'frame_count':2,'end_offset':32}
        frame={'group_index':0,'spr_no':100000,'anim_index':0,'frame_index':0,
               'offset':12,'bmp_no':17,'pos_x':-3,'pos_y':4,'sound_no':123,'sentinel':0}
        ff=[frame,dict(frame,frame_index=1,offset=22)]
        spr=struct.pack('<HHII',0,6,64,2)+struct.pack('<IhhH',17,-3,4,123)*2
        group['segment_sha256']=lab.digest(spr)
        real=b'RD'+bytes([0,0])+struct.pack('<III',2,2,20)+bytes([10,20,30,40])
        adrn=struct.pack('<IIIiiii',17,0,20,-2,-5,2,2)+bytes(52)
        raw={'spr_1.bin':spr,'spradrn_1.bin':struct.pack('<IIHH',100000,0,1,2),
             'adrn_1.bin':adrn,'real_1.bin':real}
        paths={n:p/n for n in raw}
        for n,b in raw.items():paths[n].write_bytes(b)
        expected={n:(len(b),lab.digest(b)) for n,b in raw.items()}
        bitmap={'index':0,'bitmapno':17,'adder':0,'size':20,'xoff':-2,'yoff':-5,
                'width':2,'height':2,'rd_block_sha256':lab.digest(real)}
        t=dict(self.report['cases'][0],group=group,animation=animation,cycle_ticks=4,
               frames=[dict(f,bitmap=bitmap,composed_x=-5,composed_y=-1,
                            start_tick=i*2,hold_ticks=2) for i,f in enumerate(ff)],distinct_bitmaps=1)
        return group,animation,ff,t,paths,expected

    def test_reencode_semantics_detect_changes_without_whole_file_pin(self):
        with tempfile.TemporaryDirectory() as d:
            g,a,ff,*_=self.fixture(Path(d))
            lab.reconstruct_group(g,[a],{0:ff})
            for scope,key,value in [('frame','bmp_no',18),('frame','pos_x',-4),
                                    ('frame','sound_no',124),('frame','offset',13),
                                    ('animation','duration',65),('animation','end_offset',31),
                                    ('group','next_offset',33)]:
                gg,aa,f=copy.deepcopy((g,a,ff))
                {'frame':f[0],'animation':aa,'group':gg}[scope][key]=value
                with self.subTest(scope=scope,key=key),self.assertRaises(ValueError):
                    lab.reconstruct_group(gg,[aa],{0:f})

    def test_actual_synthetic_pixels_private_bundle_and_no_event_playback(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);_,_,_,t,paths,expected=self.fixture(p)
            html,c=lab.preview(t,paths,expected)
            self.assertEqual(len(c['bitmap_witnesses']),1)
            self.assertEqual(c['bitmap_witnesses'][0]['palette_index_sha256'],
                             hashlib.sha256(bytes([10,20,30,40])).hexdigest())
            self.assertNotIn('__PACK_JSON__',html)
            self.assertIn('data:image/png;base64,',html)
            self.assertFalse(c['timeline']['sound_events_played'])
            out=p/'private.html';lab.write_private(out,html,c)
            self.assertTrue(out.is_file());self.assertTrue(out.with_suffix('.json').is_file())
            with self.assertRaises(ValueError):lab.write_private(out,html,c)

    def test_source_mutations_and_wrong_geometry_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            _,_,_,t,paths,expected=self.fixture(Path(d))
            for n in paths:
                original=paths[n].read_bytes()
                paths[n].write_bytes(original[:-1]+bytes([original[-1]^1]))
                with self.subTest(name=n),self.assertRaises(ValueError):lab.preview(t,paths,expected)
                paths[n].write_bytes(original)
            wrong=copy.deepcopy(t);wrong['frames'][0]['bitmap']['xoff']=100
            with self.assertRaisesRegex(ValueError,'geometry mismatch'):lab.preview(wrong,paths,expected)

    def test_no_public_asset_or_sidecar_overwrite(self):
        with self.assertRaises(ValueError):lab.write_private(ROOT/'research/forbidden.html','html',{})
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)/'existing.html';out.with_suffix('.json').write_text('preserve')
            with self.assertRaises(ValueError):lab.write_private(out,'html',{})
            self.assertEqual(out.with_suffix('.json').read_text(),'preserve')
            self.assertFalse(out.exists())

    def test_missing_pair_retains_native_first_fallback(self):
        # Exercise native rule on the accepted group; never invent an action name.
        t=lab.timeline(100000,65535,65535)
        self.assertTrue(t['fallback_to_first']);self.assertEqual(t['animation']['anim_index'],0)
        self.assertEqual(t['requested']['direction'],65535)
        self.assertIsNone(t['action_name'])


if __name__ == '__main__':unittest.main()
