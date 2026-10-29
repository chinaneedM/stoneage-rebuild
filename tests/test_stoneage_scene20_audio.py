import copy
import json
import unittest
from pathlib import Path

from tools.stoneage_scene20_tw10_audio import REPORT, FALSE, loose_inventory, validate, validate_replay, validate_browser_qa, inspect
from tools.stoneage_scene20_audio_fixture import fixtures


class Scene20OriginalAudio(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=json.loads(REPORT.read_bytes())

    def reject(self, mutate):
        r=copy.deepcopy(self.report);mutate(r)
        with self.assertRaises((ValueError,KeyError)):
            validate(r)

    def test_all_127_original_loose_sources(self):
        self.assertEqual(validate(self.report)['loose_files'],127)

    def test_container_and_index_are_not_loose_WAVs(self):
        self.assertEqual(len(loose_inventory()),127)
        self.assertTrue(all(n.endswith('.wav') for n in loose_inventory()))

    def test_existing_duplicate_bytes_keep_both_source_paths(self):
        self.assertEqual(len({r['WAV_sha256'] for r in self.report['files']}),126)
        self.assertEqual(len({r['original_path'] for r in self.report['files']}),127)

    def test_drop_duplicate_not_allowed(self):
        self.reject(lambda r:r['files'].pop())

    def test_container_cannot_enter_list(self):
        self.reject(lambda r:r['files'][0].update(original_path='StoneAge/data/sound_1.bin'))

    def test_one_changed_original_WAV_rejected(self):
        self.reject(lambda r:r['files'][0].update(WAV_sha256='0'*64))

    def test_bad_original_bytes_rejected_before_decode(self):
        path=next(iter(loose_inventory()))
        with self.assertRaisesRegex(ValueError,'original full WAV'):
            inspect(b'not original',path,loose_inventory())

    def test_historical_and_audible_claims_not_promoted(self):
        for k in FALSE:
            with self.subTest(field=k):self.reject(lambda r:r.update({k:True}))

    def test_no_fabricated_source_CI(self):
        self.reject(lambda r:r.update(source_CI_run_id=1))

    def test_source_package_not_substituted(self):
        self.reject(lambda r:r.update(source_private_package_sha256='0'*64))

    def test_no_game_event_naming(self):
        self.reject(lambda r:r['files'][0].update(in_game_event='village music'))

    def test_modern_loop_not_historical_loop(self):
        self.reject(lambda r:r['files'][0].update(original_loop_points_applied=True))

    def test_wrong_PCM_hash_rejected(self):
        self.reject(lambda r:r['files'][0].update(PCM_sha256='0'*64))

    def test_sample_rate_not_normalized(self):
        def change(r):
            v=r['files'][0];v['sample_rate']=44100;v['duration_seconds']=v['frames']/44100
        self.reject(change)

    def test_wrong_duration_rejected(self):
        self.reject(lambda r:r['files'][0].update(duration_seconds=1))

    def test_conserved_audio_bytes(self):
        self.reject(lambda r:r.update(original_WAV_bytes=0))

    def test_synthetic_browser_audio_is_distinct_from_original(self):
        fake=fixtures();self.assertEqual(len(fake),127)
        self.assertTrue(all(r['original_path'].startswith('SYNTHETIC_NOT_ORIGINAL/') for r in fake))
        originals={r['WAV_sha256'] for r in self.report['files']}
        self.assertFalse(any(r['WAV_sha256'] in originals for r in fake))
        self.assertEqual({(r['channels'],r['sample_width_bytes']) for r in fake},{(1,1),(1,2),(2,1),(2,2)})

    def test_public_template_has_no_embedded_originals(self):
        text=Path(__file__).resolve().parents[1].joinpath('tools/stoneage_scene20_audio_observer.html').read_text()
        self.assertEqual(text.count('__PRIVATE_AUDIO_JSON__'),1)
        self.assertNotIn('data:audio/wav;base64,',text)

    def test_actual_FFmpeg_replay_preserved(self):
        a=json.loads((REPORT.parent/'STONEAGE-SCENE20-LOCAL-FFMPEG-ACCEPTANCE-R1.json').read_bytes())
        self.assertEqual(validate_replay(a,self.report)['actual_original_WAVs_independently_decoded'],127)

    def test_FFmpeg_does_not_certify_browser_or_hearing(self):
        for field in ['actual_browser_original_audio_verified','assistant_heard_audio','original_world_entered']:
            a=json.loads((REPORT.parent/'STONEAGE-SCENE20-LOCAL-FFMPEG-ACCEPTANCE-R1.json').read_bytes());a[field]=True
            with self.subTest(field=field),self.assertRaises(ValueError):validate_replay(a,self.report)

    def test_one_changed_float_channel_refused(self):
        a=json.loads((REPORT.parent/'STONEAGE-SCENE20-LOCAL-FFMPEG-ACCEPTANCE-R1.json').read_bytes());a['files'][0]['float32_channel_sha256'][0]='0'*64
        with self.assertRaises(ValueError):validate_replay(a,self.report)

    def test_real_browser_synthetic_report_replayed(self):
        a=json.loads((REPORT.parent/'STONEAGE-SCENE20-SYNTHETIC-BROWSER-REPORT-R1.json').read_bytes())
        self.assertEqual(validate_browser_qa(a)['synthetic_browser_decoded_files'],127)

    def test_browser_synthetic_cannot_promote_originals(self):
        a=json.loads((REPORT.parent/'STONEAGE-SCENE20-SYNTHETIC-BROWSER-REPORT-R1.json').read_bytes());a['original_audio_verified']=True
        with self.assertRaises(ValueError):validate_browser_qa(a)

    def test_browser_wrong_recovered_PCM_rejected(self):
        a=json.loads((REPORT.parent/'STONEAGE-SCENE20-SYNTHETIC-BROWSER-REPORT-R1.json').read_bytes());a['decoded'][0]['recovered_original_PCM_sha256']='0'*64
        with self.assertRaises(ValueError):validate_browser_qa(a)


if __name__=='__main__':unittest.main()
