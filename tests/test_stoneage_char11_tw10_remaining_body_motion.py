import json
import re
import unittest
from tools import stoneage_char11_tw10_remaining_body_motion as c
from tools import stoneage_char10_tw10_full_motion as old
from tools import stoneage_pet15_tw10_full_motion as motion

class RemainingBodyMotion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.groups=c.selected();cls.report=json.loads(c.REPORT.read_text())
    def test_original_interval_partitions_char10_without_identity_guess(self):
        before={g['graphic'] for g in old.selected()};now={g['graphic'] for g in self.groups}
        self.assertFalse(before&now);self.assertEqual(before|now,set(range(100000,100240)))
        self.assertEqual(len(now),228)
        self.assertEqual(sum(len(g['sequences']) for g in self.groups),23712)
    def test_all_original_positions_preserved_including_four_sentinels(self):
        self.assertEqual(sum(len(motion.frames_of(g)) for g in self.groups),130592)
        sentinel=c.sentinels(self.groups)
        self.assertEqual([(r['graphic'],r['source_animation_index'],r['source_frame_index']) for r in sentinel],
                         [(100102,82,0),(100102,83,0),(100102,83,1),(100102,84,1)])
        self.assertEqual(sentinel,self.report['source_sentinel_positions'])
        self.assertEqual(len({n for g in self.groups for n in motion.frames_of(g)}-{c.SENTINEL}),69620)
    def test_default_pet_selector_remains_strict_about_sentinels(self):
        with self.assertRaisesRegex(ValueError,'unsupported sentinel'):motion.selected_motion(c.GROUP_KEYS)
    def test_source_model_has_no_invented_sentinel_image_or_action_name(self):
        model_page=c.observer(self.groups,{})
        raw=re.search(r'<script id="source" type="application/json">(.*?)</script>',model_page,re.S).group(1)
        model=json.loads(raw)
        self.assertEqual(model['groups'],self.groups);self.assertNotIn(str(c.SENTINEL),model['bitmaps'])
        self.assertIn("unresolved_source_sentinel_no_bitmap",model_page)
        self.assertNotRegex(model_page,r'(?:src|href)=["\']https?://')
    def test_actual_pixel_receipt_keeps_strict_failures_and_unknowns(self):
        r=self.report
        self.assertEqual(r['source_bitmap_statuses'],{'strict':69592,'terminal_zero_outside_canvas':28})
        self.assertEqual(len(r['bounded_bitmaps']),28);self.assertEqual(r['unrendered_source_sequences'],3)
        self.assertEqual(r['source_bitmap_reference_positions'],130588)
        self.assertTrue(all(value is False for value in r['boundaries'].values()))
        self.assertEqual(r['source_archive_sha256'],motion.ZIP_SHA)
    def test_public_browser_fixture_explicitly_excludes_original_art(self):
        page=c.synthetic_fixture()
        self.assertIn('metadata-and-test-pixels-only',page)
        raw=re.search(r'<script id="source" type="application/json">(.*?)</script>',page,re.S).group(1)
        model=json.loads(raw)
        self.assertTrue(all(x['status']=='SYNTHETIC_BROWSER_FIXTURE' for x in model['bitmaps'].values()))
        self.assertEqual(len(model['bitmaps']),69620)

if __name__=='__main__':unittest.main()
