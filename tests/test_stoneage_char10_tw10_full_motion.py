import json
import re
import unittest
from tools import stoneage_char10_tw10_full_motion as char10
from tools import stoneage_pet15_tw10_full_motion as motion

class CharacterFullMotion(unittest.TestCase):
    def test_source_selectors_and_frames_preserve_previous_char02_scope(self):
        groups=char10.selected()
        self.assertEqual(len(groups),12)
        self.assertEqual(sum(len(g['sequences']) for g in groups),1248)
        self.assertEqual(sum(len(motion.frames_of(g)) for g in groups),6920)
        self.assertEqual(len({n for g in groups for n in motion.frames_of(g)}),4152)
        for g in groups:
            self.assertEqual({(a['direction'],a['action']) for a in g['sequences']},
                             {(direction,action) for direction in range(8) for action in range(13)})
        prior={f[0] for g in groups for s in g['sequences'] if s['action']==2 for f in s['frames']}
        self.assertEqual(len(prior),576)
    def test_pet15_default_scope_remains_byte_semantically_unchanged(self):
        prior=motion.archived(motion.REPORT)
        groups=motion.selected_motion()
        self.assertEqual(motion.motion_summary(groups,{}),prior['groups'])
        self.assertEqual(sum(len(motion.frames_of(g)) for g in groups),prior['frame_positions'])
    def test_private_observer_preserves_all_numeric_frame_fields(self):
        groups=char10.selected()
        page=char10.observer(groups,{})
        embedded=re.search(r'<script id="source" type="application/json">(.*?)</script>',page,re.S).group(1)
        self.assertEqual(json.loads(embedded)['groups'],groups)
        self.assertNotRegex(page,r'(?:src|href)=["\']https?://')
    def test_accepted_pixel_report_keeps_bounded_failure_and_native_unknowns(self):
        report=json.loads(char10.REPORT.read_text())
        self.assertEqual(report['source_bitmap_statuses'],{'strict':4151,'terminal_zero_outside_canvas':1})
        self.assertEqual(report['bounded_bitmaps'],[34699])
        self.assertEqual(report['additional_bitmap_scope_beyond_char02'],3576)
        self.assertTrue(all(v is False for v in report['boundaries'].values()))
        self.assertEqual(report['groups'],motion.motion_summary(char10.selected(),{}))

if __name__=='__main__':unittest.main()
