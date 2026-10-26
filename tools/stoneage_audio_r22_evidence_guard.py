"""Bounded original WAV custody; decoder/file delivery never implies hearing or game playback."""
import hashlib
import json
from pathlib import Path
from tools.stoneage_private_audio_r22 import ROOT,SCHEMA,need
from tools.stoneage_audio_sample_r22 import PREVIOUS,PREVIOUS_SHA

RECOVERED=ROOT/'research/recovered'

def fingerprint(b):
    return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}

def verify_source(r):
    oldraw=(ROOT/PREVIOUS).read_bytes();need(hashlib.sha256(oldraw).hexdigest()==PREVIOUS_SHA,'old original report pin')
    old=json.loads(oldraw);row=old['table_records'][0];w=row['wave'];sample=r['sample']
    need(r['schema']=='stoneage.private_original_audio_sample_r22.v1','source schema')
    need(r['source']==old['source'] and r['members']==old['members'] and r['prior_report_path']==PREVIOUS and
        r['prior_report_sha256']==PREVIOUS_SHA and r['full_original_report_replayed'] is True,'complete original source qualification')
    need(r['sample_table_index']==0 and r['sample_table_name']==row['table_name'] and r['sample_offset']==0,'one original table entry')
    need(sample['bytes']==row['bytes'] and sample['sha256']==row['sha256'] and sample['pcm_sha256']==w['data_sha256'],'WAV/PCM provenance')
    need(sample['channels']==w['channels']==1 and sample['sample_width_bytes']==1 and sample['sample_rate']==22050 and
        sample['frames']==sample['pcm_bytes']==w['data_size'] and sample['duration_seconds']==sample['frames']/sample['sample_rate'],'frame format and exact duration')
    need(0<=sample['sample_unsigned_minimum']<=sample['sample_unsigned_maximum']<=255 and
        0<sample['non_midpoint_samples']<=sample['frames'],'sample statistics only')
    e=r['encrypted_transport'];public=(RECOVERED/'STONEAGE-R22-AUDIO-RECIPIENT-PUBLIC.pem').read_bytes()
    need(e['schema']==SCHEMA and e['media_type']=='audio/wav' and e['recipient_key_sha256']==hashlib.sha256(public).hexdigest() and
        e['plaintext_bytes']==sample['bytes'] and e['plaintext_sha256']==sample['sha256'],'private envelope identity')
    for k in ('original_client_executed','original_game_audio_device_played','assistant_listening_confirmed',
        'same_deployed_build_proven','waveform_or_private_key_in_git','public_artifact_plaintext_audio','private_persistent_storage_verified','user_playback_confirmed'):
        need(r[k] is False,'source-only runtime/delivery overclaim: '+k)
    need(r['named_scene_pet_or_battle_event'] is None,'unknown original event')

def verify_delivery(r,source):
    need(r['schema']=='stoneage.private_original_audio_delivery_r22.v1','delivery schema')
    need(r['status']=='PRIVATE_ORIGINAL_WAV_AVAILABLE_ASSISTANT_AUDIO_INPUT_UNSUPPORTED','bounded delivery result')
    need(r['private_file_saved'] is True and r['independent_complete_readback'] is True,'actual private storage and full reread')
    need(r['original_wav_bytes']==source['sample']['bytes'] and r['original_wav_sha256']==source['sample']['sha256'] and
        r['pcm_sha256']==source['sample']['pcm_sha256'],'private bytes equal actual source')
    need(r['ffmpeg_decode_returncode']==0 and r['decoded_s16_bytes']==source['sample']['frames']*2 and
        r['decoded_all_samples_equal_unsigned8_to_signed16_scaling'] is True and r['resampling_or_normalization_performed'] is False,'independent PCM decoder comparison')
    need(r['model_audio_input_result']=='AUDIO_CONTENT_OMITTED_MODEL_DOES_NOT_SUPPORT_AUDIO_INPUT','actual audio-input limitation')
    for k in ('assistant_listening_confirmed','user_playback_confirmed','original_game_audio_device_played','audio_player_render_verified','named_audio_event_authenticated'):
        need(r[k] is False,'file/decoder is not listening or original playback: '+k)
    need(r['original_event_name'] is None and r['overall_restoration_percent'] is None,'no invented content/completion')

def check():
    c=json.loads((RECOVERED/'STONEAGE-PRIVATE-AUDIO-R22-CUSTODY-R1.json').read_bytes())
    for f in c['derived_files']:
        b=(ROOT/f['path']).read_bytes();need(fingerprint(b)=={k:f[k] for k in ('bytes','sha256','git_blob')},'raw derived file custody')
    source=json.loads((RECOVERED/'STONEAGE-PRIVATE-AUDIO-R22-SOURCE-R1.json').read_bytes());verify_source(source)
    delivery=json.loads((RECOVERED/'STONEAGE-PRIVATE-AUDIO-R22-DELIVERY-R1.json').read_bytes());verify_delivery(delivery,source)
    need(c['source_run']['status']=='completed' and c['source_run']['conclusion']=='success' and
        all(j['conclusion']=='success' for j in c['source_jobs']),'actual source jobs')
    need(c['public_artifact_plaintext_audio'] is False and c['private_key_in_git'] is False and c['overall_restoration_percent'] is None,'global limits')
    for p,f in c['full_startup_files'].items():need(fingerprint((ROOT/p).read_bytes()[:f['bytes']])==f,'historical full prefix lost')
    print('R22_PRIVATE_WAV_SOURCE_READBACK_PCM_CUSTODY=PASS; ASSISTANT_HEARING_AND_GAME_PLAYBACK_NOT_PROMOTED')

if __name__=='__main__':check()
