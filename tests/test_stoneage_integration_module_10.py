"""Public derived metadata gates; CI never reads the private original maps/art."""
import hashlib
import json
import struct
import unittest

from tools.stoneage_integration10_dat_recovery import (
    FLOORS, RAR_SHA, REC, REPORT, checkpoints, dat_planes, sources,
)


class SourceRecovery(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = json.loads(REPORT.read_bytes())
        cls.s = sources()

    def test_original_carrier_and_historical_prefix_preserved(self):
        self.assertEqual(self.r['original_RAR_sha256'], RAR_SHA)
        self.assertEqual(self.r['preserved_CURRENT_blob'], 'c89e0e33537990aa2132b47c40fef49a985a935c')
        raw = (REC.parents[1]/'docs/CURRENT-STATE.md').read_bytes()
        self.assertEqual(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(), self.r['preserved_CURRENT_blob'])

    def test_exact_twelve_previously_failed_members(self):
        rows = self.r['recovered_DAT']
        self.assertEqual([r['floor'] for r in rows], list(FLOORS))
        old = {r['floor_id']: r for r in self.s['i07']['floors']}
        for row in rows:
            self.assertEqual(row['old_read_error'], old[row['floor']]['source_DAT_original_read_errors'][0])
            self.assertEqual(old[row['floor']]['source_DAT_status'], 'INDEXED_DAT_READ_ERROR')
            self.assertEqual(row['bytes'], 8+6*row['width']*row['height'])
            self.assertEqual(row['unar_exit'], 0)

    def test_recovered_size_and_player_content_impact(self):
        rows = self.r['recovered_DAT']
        self.assertEqual(sum(r['bytes'] for r in rows), 16497180)
        self.assertEqual(sum(r['width']*r['height'] for r in rows), 2749514)
        chosen = [r for r in self.s['i07']['floors'] if r['floor_id'] in FLOORS]
        self.assertEqual(sum(r['quest05_source_CREATE_count'] for r in chosen), 67)
        self.assertEqual(self.r['material_impact']['QUEST05_source_CREATE_refs_newly_joinable'], 67)
        self.assertEqual(self.r['material_impact']['still_no_selected_DAT_floor'], 830)

    def test_original_case_and_non_square_geometry_retained(self):
        by = {r['floor']: r for r in self.r['recovered_DAT']}
        self.assertTrue(by[200]['original_path'].endswith('/200.dat'))
        self.assertTrue(by[3000]['original_path'].endswith('/3000.dat'))
        self.assertEqual((by[400]['width'], by[400]['height']), (150,149))
        self.assertEqual((by[200]['width'], by[200]['height']), (800,1200))

    def test_original_header_and_packed_stream_provenance(self):
        for row in self.r['recovered_DAT']:
            self.assertLess(row['header_offset'], row['packed_offset'])
            self.assertLessEqual(row['packed_offset']+row['packed_bytes'], 361255180)
            self.assertEqual(row['original_flags'] & (1|2|4|16), 0)
            for key in ('sha256', 'packed_sha256', 'original_header_sha256'):
                self.assertRegex(row[key], r'^[0-9a-f]{64}$')
            self.assertEqual(len(row['planes']), 3)

    def test_seven_source_checkpoint_positions_are_exact(self):
        expected = checkpoints(self.s['q25'])
        actual = self.r['source_windows']
        self.assertEqual([(r['route'],r['checkpoint']) for r in actual], [('C',2),('C',9),('D',1),('D',2),('D',5),('D',7),('D',12)])
        for row, (route, number, source) in zip(actual, expected):
            self.assertEqual((row['route'],row['checkpoint'],row['floor']), (route,number,source['floor']))
            self.assertEqual(row['xy'], source['borncorner'][:2])
            self.assertEqual(row['source_block_sha256'], source['block_sha256'])
            x,y = row['xy']
            self.assertEqual(row['window'], [x-5,y-5,x+5,y+5])
            self.assertEqual(row['missing_MAP04_pixel_aliases'], [])

    def test_pixel_reuse_and_complete_candidate_frames(self):
        resources = self.r['source_pixel_resources']
        prior = json.loads((REC/'STONEAGE-MAP-SCENE-MODULE-04-955-ORIGINAL-DAT-4166-RD-PIXEL-INDEX-R1.json').read_bytes())
        pins = {r[0]: r for r in prior['source_TW1_real_RD_rows']}
        self.assertEqual(len(resources), 279)
        for key, row in resources.items():
            self.assertEqual(row['source_RD_sha256'], pins[int(key)][5])
            self.assertEqual(row['source_index_pixels_sha256'], pins[int(key)][6])
        self.assertEqual(sum(r['draw_positions'] for r in self.r['source_windows']), 819)
        for row in self.r['source_windows']:
            self.assertEqual(set(row['frames']), {'plane0','plane1','combined'})
            self.assertTrue(all(0 <= v <= 65535 for v in row['checkpoint_three_u16']))

    def test_truncated_oversized_and_bad_plane_extents_rejected(self):
        for raw in (b'', b'1234567', struct.pack('<II',0,1), struct.pack('<II',1,1),
                    struct.pack('<II',2**32-1,1), struct.pack('<II',1,1)+b'\0'*7):
            with self.assertRaises(ValueError):
                dat_planes(raw)
        self.assertEqual(dat_planes(struct.pack('<IIHHH',1,1,0,99,65535)), (1,1,[(0,),(99,),(65535,)]))

    def test_source_qualification_does_not_promote_native_or_official_claims(self):
        self.assertTrue(all(v is False for v in self.r['boundaries'].values()))
        self.assertIsNone(self.r['source_ci_run_id'])
        self.assertIsNone(self.r['overall_percent'])
        self.assertEqual(self.r['stage_A'], '7_PARTIAL_2_OPEN')
        self.assertEqual(self.r['stage_B'], 'GATED')
        self.assertEqual(self.r['wiki'], 'GATED')
        self.assertEqual(self.r['R79'], 'PAUSED_NON_BLOCKING')


if __name__ == '__main__':
    unittest.main()
