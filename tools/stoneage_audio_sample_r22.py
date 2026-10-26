"""Select exactly one pinned original sound3 WAV; publish metadata and ciphertext only."""
import argparse
import hashlib
import json
from pathlib import Path
from tools.stoneage_private_audio_r22 import ROOT,need,seal,wave_metadata,outside_new
from tools.stoneage_sound3_original_content import produce

PREVIOUS='research/recovered/STONEAGE-SOUND3-ORIGINAL-CONTENT-R1.json'
PREVIOUS_SHA='ed5d9387a6f8e70da5ad269fc9fa46f8ad5d0b6e0aaf25e3b6d969fe2e1934d0'

def extract(directory,cab,public):
    oldraw=(ROOT/PREVIOUS).read_bytes();need(hashlib.sha256(oldraw).hexdigest()==PREVIOUS_SHA,'prior full original report identity')
    old=json.loads(oldraw);fresh=produce(directory,cab);need(fresh==old,'full bounded original report differs')
    row=old['table_records'][0];need(row['table_name']=='saam_01.wav' and row['offset']==0 and row['bytes']==27180,'finite original sample selection')
    container=(directory/'sound_3.bin').read_bytes();raw=container[row['offset']:row['offset']+row['bytes']]
    meta=wave_metadata(raw);need(meta['sha256']==row['sha256'] and meta['pcm_sha256']==row['wave']['data_sha256'],'original WAV and PCM identities')
    envelope=seal(raw,public)
    result={'schema':'stoneage.private_original_audio_sample_r22.v1','source':old['source'],'members':old['members'],
        'prior_report_path':PREVIOUS,'prior_report_sha256':PREVIOUS_SHA,'full_original_report_replayed':True,
        'sample_table_index':0,'sample_table_name':row['table_name'],'sample_offset':row['offset'],
        'sample':meta,'encrypted_transport':{k:envelope[k] for k in ('schema','plaintext_bytes','plaintext_sha256','recipient_key_sha256','media_type')},
        'original_client_executed':False,'original_game_audio_device_played':False,'assistant_listening_confirmed':False,
        'named_scene_pet_or_battle_event':None,'same_deployed_build_proven':False,'waveform_or_private_key_in_git':False,
        'public_artifact_plaintext_audio':False,'private_persistent_storage_verified':False,'user_playback_confirmed':False}
    return result,envelope

def main():
    p=argparse.ArgumentParser();p.add_argument('--directory',type=Path,required=True);p.add_argument('--cab',type=Path,required=True)
    p.add_argument('--public-key',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--sealed',type=Path,required=True);a=p.parse_args()
    result,envelope=extract(a.directory,a.cab,a.public_key.read_bytes());dest=outside_new(a.sealed,'.json')
    b=(json.dumps(envelope,sort_keys=True,indent=2)+'\n').encode();dest.write_bytes(b)
    result['encrypted_transport'].update(envelope_bytes=len(b),envelope_sha256=hashlib.sha256(b).hexdigest())
    a.output.write_bytes((json.dumps(result,sort_keys=True,indent=2)+'\n').encode())
    print('R22_ONE_ORIGINAL_WAV_AUTHENTICATED_AND_ENCRYPTED; NO_PLAYBACK_CLAIM')

if __name__=='__main__':main()
