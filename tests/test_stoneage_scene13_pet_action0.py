import copy,json,unittest
from tools.stoneage_scene13_pet_action0 import REPORT,validate,validate_acceptance,FALSE_FLAGS

class SourceAction0Boundaries(unittest.TestCase):
    def setUp(self):self.r=json.loads(REPORT.read_bytes())
    def reject(self,mutate):
        r=copy.deepcopy(self.r);mutate(r)
        with self.assertRaises(ValueError):validate(r)
    def test_archived_exact_source_sequences(self):
        r=validate(self.r);self.assertEqual((r['animations'],r['frame_occurrences'],r['distinct_bitmaps'],r['repeated_positions']),(24,352,208,144))
    def test_repeated_occurrence_cannot_be_removed(self):self.reject(lambda r:r['groups'][2]['animations'][0]['frames'].pop(0))
    def test_direction_cannot_be_reused(self):self.reject(lambda r:r['groups'][0]['animations'][1].update(direction=0))
    def test_frame_offsets_are_not_discardable(self):self.reject(lambda r:r['groups'][0]['animations'][0]['frames'][0].__setitem__(1,123))
    def test_sound_word_is_not_normalized(self):self.reject(lambda r:r['groups'][0]['animations'][0]['frames'][0].__setitem__(3,65535))
    def test_original_duration_not_preview_ms(self):self.reject(lambda r:r['groups'][0]['animations'][0].update(duration_word=180))
    def test_all_original_bitmaps_required(self):self.reject(lambda r:r['bitmaps'].pop())
    def test_duplicate_bitmap_is_not_extra_source(self):self.reject(lambda r:r['bitmaps'].append(r['bitmaps'][0]))
    def test_invalid_digest_rejected(self):self.reject(lambda r:r['bitmaps'][0].update(RD_sha256='x'*64))
    def test_valid_looking_pixel_hash_change_rejected(self):self.reject(lambda r:r['bitmaps'][0].update(candidate_RGBA_sha256='0'*64))
    def test_rd_cannot_leave_original_carrier(self):self.reject(lambda r:r['bitmaps'][0].update(offset=9999999999))
    def test_no_action2_order_promotion(self):self.reject(lambda r:r.update(draw_order='CONTROLLED_CASE_R9'))
    def test_no_invented_action_name_or_fps(self):self.reject(lambda r:r.update(timing='1000ms_IDLE'))
    def test_source_identity_cannot_change(self):self.reject(lambda r:r['source_files']['Palet_1.sap'].update(sha256='0'*64))
    def test_historical_claims_remain_false(self):
        for key in FALSE_FLAGS:
            with self.subTest(key=key):self.reject(lambda r:r.update({key:True}))
    def test_no_restoration_percentage(self):self.reject(lambda r:r.update(overall_completion_percent=90))
    def test_original_source_span_required(self):self.reject(lambda r:r['groups'][0]['animations'][0].update(source_animation_span_sha256='0'*64))
    def test_original_header_location_required(self):self.reject(lambda r:r['groups'][0]['animations'][0].update(header_offset=0))
    def test_archived_full_browser_acceptance(self):
        a=json.loads(REPORT.with_name('STONEAGE-SCENE13-PIXEL-ACCEPTANCE-R1.json').read_bytes())
        self.assertEqual(validate_acceptance(a,self.r)['browser_canvas_states'],352)
    def test_browser_acceptance_missing_frame_rejected(self):
        a=json.loads(REPORT.with_name('STONEAGE-SCENE13-PIXEL-ACCEPTANCE-R1.json').read_bytes());a['frame_hashes'].pop()
        with self.assertRaises(ValueError):validate_acceptance(a,self.r)
    def test_local_pixels_cannot_be_described_as_source_CI(self):
        a=json.loads(REPORT.with_name('STONEAGE-SCENE13-PIXEL-ACCEPTANCE-R1.json').read_bytes());a['public_CI_reads_private_pixels']=True
        with self.assertRaises(ValueError):validate_acceptance(a,self.r)
    def test_viewer_keeps_human_action_independent(self):
        from pathlib import Path
        s=Path('tools/scene-room-action0-viewer-r13.html').read_text()
        self.assertIn('group.spr_no===100000?2:state.action',s)
        self.assertNotIn('actor_order_evidence',s)
        self.assertIn("connect-src 'none'",s)
if __name__=='__main__':unittest.main()
