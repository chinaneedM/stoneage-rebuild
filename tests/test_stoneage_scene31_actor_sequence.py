"""Historical evidence boundaries and destructive sequence mutations."""
import copy
import json
import unittest
from tools import stoneage_scene31_actor_sequence as m

class OriginalActorSequenceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.good=json.loads(m.REPORT.read_text())
        m.validate(cls.good)

    def rejects(self, mutate, reason):
        r=copy.deepcopy(self.good);mutate(r)
        with self.assertRaisesRegex(ValueError,reason):m.validate(r)

    def test_actual_source_receipt_and_full_sequences(self):
        self.assertEqual(m.validate(self.good)['frame_positions'],48)
        self.assertEqual([len(a['frames'])for a in self.good['sequences']],[6]*8)

    def test_first_frame_only_is_not_complete_animation(self):
        self.rejects(lambda r:r['sequences'][0].update(frames=r['sequences'][0]['frames'][:1]),'complete ordered')

    def test_swapped_frame_order_is_not_equivalent(self):
        self.rejects(lambda r:r['sequences'][0]['frames'].reverse(),'complete ordered')

    def test_duplicate_replacement_preserves_count_but_not_original(self):
        def change(r):r['sequences'][0]['frames'][1]=r['sequences'][0]['frames'][0]
        self.rejects(change,'complete ordered')

    def test_missing_or_duplicate_direction_is_not_eight_way_coverage(self):
        self.rejects(lambda r:r['sequences'].__setitem__(7,copy.deepcopy(r['sequences'][0])),'complete ordered')

    def test_source_duration_cannot_be_changed_to_preview_ms(self):
        self.rejects(lambda r:r['sequences'][0].update(duration_word=180),'complete ordered')

    def test_foreign_physical_bitmap_is_rejected(self):
        self.rejects(lambda r:r['sequences'][0]['frames'][0].__setitem__(0,20033),'complete ordered')

    def test_source_payload_or_pixel_claim_mutation_is_rejected(self):
        self.rejects(lambda r:r['bitmaps'][0].update(indices_sha256='0'*64),'pixel receipt')
        self.rejects(lambda r:r['bitmaps'].pop(),'complete source pixel')

    def test_original_namespace_and_source_pins(self):
        self.rejects(lambda r:r.update(source_scope='MIXED25_OFFICIAL_TW1'),'source scope')
        self.rejects(lambda r:r.update(source_parent_zip_sha256='0'*64),'parent package')
        self.rejects(lambda r:r['source_files']['real_1.bin'].update(sha256='0'*64),'same-build source pins')

    def test_false_native_interpretations_are_not_promoted(self):
        for k in m.FALSE:
            with self.subTest(k=k):self.rejects(lambda r,k=k:r.update({k:True}),'boundary')

    def test_no_invented_source_ci_or_overall_percent(self):
        self.rejects(lambda r:r.update(source_action_run_id=123),'invented run')
        self.rejects(lambda r:r.update(overall_percent=100),'invented run')

    def test_evidence_delta_does_not_recount_first_frames_as_new(self):
        self.rejects(lambda r:r.update(further_frame_positions_observed=48),'evidence delta')

    def test_source_bitmap_occurrences_are_not_silently_deduplicated(self):
        self.rejects(lambda r:r.update(frame_occurrences=40),'conservation')

    def test_native_timing_is_not_implied_by_modern_preview(self):
        self.rejects(lambda r:r.update(source_duration_is_not_milliseconds=False),'preview timing')

if __name__=='__main__':unittest.main()
