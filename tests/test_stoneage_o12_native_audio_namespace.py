import copy, json, unittest
from tools.stoneage_o12_native_sound_namespace import SOURCE, verify, bounded_original_source_check

class OriginalNativeAudioO12(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.good=json.loads(SOURCE.read_text(encoding='utf-8'))
    def test_source_derived_report(self):
        self.assertEqual(verify(self.good)['native_verified_id_paths'],102)
    def reject(self,path,value):
        x=copy.deepcopy(self.good)
        cur=x
        for p in path[:-1]: cur=cur[p]
        cur[path[-1]]=value
        with self.assertRaises((ValueError,KeyError,TypeError)):
            verify(x)
    def test_wrong_original_executable(self):
        self.reject(['original_source','original_runtime_sha256'],'0'*64)
    def test_wrong_original_audio_table(self):
        self.reject(['original_source','original_sfx_address_table_sha256'],'0'*64)
    def test_invented_114_compiled_paths(self):
        self.reject(['compiled_static_names','sfx_unique'],114)
    def test_remove_awkward_unmatched_path(self):
        self.reject(['bounded_native_x86_machine_join','unmatched_static_names_due_to_alternate_codegen'],self.good['bounded_native_x86_machine_join']['unmatched_static_names_due_to_alternate_codegen'][:-1])
    def test_wrong_compiled_73(self):
        self.reject(['key_number_73','compiled_native_sound_number_filepath'],'data\\se\\sam_18.wav')
    def test_wrong_address_table_73(self):
        self.reject(['indexed_sfx','index73'],'sae_23.wav')
    def test_wrong_sak_98_negative(self):
        self.reject(['indexed_sfx','not_in_compiled_static_paths'],[])
    def test_fake_73_frame_event_selector(self):
        self.reject(['key_number_73','original_frame_word_to_audio_event_selector_found'],True)
    def test_fake_73_native_binding(self):
        self.reject(['key_number_73','frame_word_73_uses_this_compiled_namespace_verified'],True)
    def test_fake_native_audio_playback(self):
        self.reject(['negative_scope','historic_audio_playback_was_observed'],True)
    def test_fake_world_entry(self):
        self.reject(['negative_scope','original_game_world_entered'],True)
    def test_fake_pet_species_name(self):
        self.reject(['negative_scope','pet_species_or_name_was_identified'],True)
    def test_fake_10000_resolved(self):
        self.reject(['negative_scope','sound_word_10000_was_mapped_to_audio'],True)
    def test_fake_public_original_binary(self):
        self.reject(['negative_scope','proprietary_binaries_audio_or_images_in_public_git'],True)
    def test_falsified_machine_triple(self):
        x=copy.deepcopy(self.good);x['bounded_native_x86_machine_join']['verified_pairs'][0]['compiled_sound_number']=73
        with self.assertRaises(ValueError):verify(x)
    def test_falsified_machine_source_location(self):
        x=copy.deepcopy(self.good);x['bounded_native_x86_machine_join']['verified_pairs'][0]['load_instruction_file_offset']+=1
        with self.assertRaises(ValueError):verify(x)
    def test_fake_privileged_ci_original_source(self):
        self.reject(['evidence_notes','git_actions_will_verify_only_frozen_derived_source'],False)
    def test_fake_completion_percentage(self):
        self.reject(['overall_percent'],100)
    def test_wrong_cross_sample_24(self):
        self.reject(['prior_O11_source_control','verified_same_source_animation_segments'],23)
    def test_wrong_report_schema(self):
        self.reject(['schema'],'unknown')
    def test_bounded_source_rejects_missing_private_input(self):
        with self.assertRaises(ValueError):bounded_original_source_check(b'x',b'y')

if __name__=='__main__':unittest.main()
