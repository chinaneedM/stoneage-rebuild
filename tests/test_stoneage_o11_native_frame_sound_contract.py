import copy,json,unittest
from tools.stoneage_o11_native_frame_sound_contract import REPORT,PIXEL_AUDIT,validate,validate_pixel_audit
class TestO11(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.data=json.loads(REPORT.read_text(encoding='utf8'))
    def test_accepted_private_source_evidence(self):self.assertEqual(validate(self.data)['TW1_physical_pixels'],208)
    def test_second_independent_208_actual_RD_pixel_audit(self):
        raw=PIXEL_AUDIT.read_bytes()
        self.assertEqual(validate_pixel_audit(self.data,raw,json.loads(raw))["source_verified_tw1_original_rd_pixels"],208)
    def test_wrong_pixel_audit_original_record(self):
        raw=PIXEL_AUDIT.read_bytes();a=json.loads(raw)
        a["records"][0]["rd_sha256"]="0"*64
        with self.assertRaises(ValueError):validate_pixel_audit(self.data,raw,a)
    def test_missing_pixel_audit_record(self):
        raw=PIXEL_AUDIT.read_bytes();a=json.loads(raw)
        a["records"].pop()
        with self.assertRaises(ValueError):validate_pixel_audit(self.data,raw,a)
    def reject(self,path,value):
        d=copy.deepcopy(self.data);v=d
        for p in path[:-1]:v=v[p]
        v[path[-1]]=value
        with self.assertRaises(ValueError):validate(d)
    def test_old_unverified_source(self):self.reject(['source_pins','tw1_spr_sha256'],'0'*64)
    def test_wrong_original_container(self):self.reject(['source_pins','tw1_p3h_archive_sha256'],'0'*64)
    def test_wrong_full_frame_count(self):self.reject(['full_spr_inventory','frames'],242084)
    def test_drop_10000_value(self):self.reject(['full_spr_inventory','unique_nonzero_values'],[v for v in self.data['full_spr_inventory']['unique_nonzero_values'] if v!=10000])
    def test_wrong_actual_span_count(self):self.reject(['bounded_original_sprite_sample','independent_source_spans_sha_equal'],23)
    def test_wrong_73_occurrence(self):self.reject(['bounded_original_sprite_sample','numeric_frame_word_occurrences','73'],25)
    def test_promote_official_pets(self):self.reject(['original_client_source_pixel_confirmation','official_species_identity_known'],True)
    def test_fake_true_historical_palette(self):self.reject(['original_client_source_pixel_confirmation','color_palette_is_proven_historical_selector'],True)
    def test_wrong_original_pixels(self):self.reject(['original_client_source_pixel_confirmation','identical_RGBA_to_previous_mixed25_png'],207)
    def test_wrong_zero_base_candidate(self):self.reject(['audio_index_candidate','zero_based','name'],'sam_17.wav')
    def test_wrong_one_base_candidate(self):self.reject(['audio_index_candidate','one_based','table_index'],73)
    def test_fake_10000_in114(self):self.reject(['audio_index_candidate','source_word_10000_class'],'INDEX_10000')
    def test_fake_audio_event_selector(self):self.reject(['historical_unknowns','original_sound_event_selector_proven'],True)
    def test_fake_sound_word73_meaning(self):self.reject(['historical_unknowns','raw_word_73_is_proven_sound_number'],True)
    def test_fake_original_client_run(self):self.reject(['historical_unknowns','original_client_executed'],True)
    def test_fake_private_library(self):self.reject(['private_observation','private_library_roundtrip_full_SHA_equal'],False)
    def test_fake_local_open(self):self.reject(['private_observation','file_url_navigation_blocked'],False)
    def test_fake_100_percent(self):self.reject(['project_gates','overall_completion_percent'],100)
    def test_wrong_source_animation_span_sha(self):self.reject(['bounded_original_sprite_sample','all_24_source_animation_records',0,'source_animation_span_sha256'],'0'*64)
    def test_wrong_original_event_word_at_100252(self):
        d=copy.deepcopy(self.data)
        x=next(a for a in d['bounded_original_sprite_sample']['all_24_source_animation_records'] if a['spr_no']==100252)
        x['nonzero_frame_source_words'][1]['source_word']=73
        with self.assertRaises(ValueError):validate(d)
if __name__=='__main__':unittest.main()
