import copy
import json
import unittest
from tools import stoneage_audio_r22_evidence_guard as g

class AudioEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.s=json.loads((g.RECOVERED/'STONEAGE-PRIVATE-AUDIO-R22-SOURCE-R1.json').read_bytes())
        self.d=json.loads((g.RECOVERED/'STONEAGE-PRIVATE-AUDIO-R22-DELIVERY-R1.json').read_bytes())
    def test_actual_source_and_private_delivery(self):g.verify_source(self.s);g.verify_delivery(self.d,self.s)
    def test_changed_table_slot_cannot_name_another_sample(self):
        self.s['sample_table_index']=1
        with self.assertRaises(ValueError):g.verify_source(self.s)
    def test_container_suffix_cannot_replace_wav_and_pcm_hashes(self):
        for k in ('sha256','pcm_sha256'):
            r=copy.deepcopy(self.s);r['sample'][k]='0'*64
            with self.subTest(k=k),self.assertRaises(ValueError):g.verify_source(r)
    def test_forged_resampled_format_or_duration_rejected(self):
        for k,v in [('sample_rate',44100),('frames',1),('duration_seconds',2),('sample_width_bytes',2)]:
            r=copy.deepcopy(self.s);r['sample'][k]=v
            with self.subTest(k=k),self.assertRaises(ValueError):g.verify_source(r)
    def test_source_cannot_preclaim_private_storage_or_hearing(self):
        for k in ('private_persistent_storage_verified','assistant_listening_confirmed','user_playback_confirmed','original_game_audio_device_played'):
            r=copy.deepcopy(self.s);r[k]=True
            with self.subTest(k=k),self.assertRaises(ValueError):g.verify_source(r)
    def test_private_save_without_independent_readback_is_not_qualified(self):
        self.d['independent_complete_readback']=False
        with self.assertRaises(ValueError):g.verify_delivery(self.d,self.s)
    def test_decoder_success_is_not_playback_or_hearing(self):
        for k in ('assistant_listening_confirmed','user_playback_confirmed','original_game_audio_device_played','audio_player_render_verified'):
            r=copy.deepcopy(self.d);r[k]=True
            with self.subTest(k=k),self.assertRaises(ValueError):g.verify_delivery(r,self.s)
    def test_changed_private_readback_or_decoded_frames_rejected(self):
        for k,v in [('original_wav_sha256','0'*64),('decoded_s16_bytes',1),('decoded_all_samples_equal_unsigned8_to_signed16_scaling',False)]:
            r=copy.deepcopy(self.d);r[k]=v
            with self.subTest(k=k),self.assertRaises(ValueError):g.verify_delivery(r,self.s)
    def test_unknown_sound_cannot_be_named_or_official_build_promoted(self):
        self.s['named_scene_pet_or_battle_event']='invented pet attack'
        with self.assertRaises(ValueError):g.verify_source(self.s)
        self.d['original_event_name']='invented event'
        with self.assertRaises(ValueError):g.verify_delivery(self.d,self.s)

if __name__=='__main__':unittest.main()
