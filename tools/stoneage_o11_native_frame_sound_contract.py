"""O11 public source-only guard. No original client/PNG/WAV payload is in this repository.

The public report records a previously completed PRIVATE raw-byte replay; running
this check does NOT rerun the proprietary client, render original images or play WAV.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'research/recovered/STONEAGE-O11-NATIVE-FRAME-SOUND-SOURCE-R1.json'
PIXEL_AUDIT = ROOT / 'research/recovered/STONEAGE-O11-TW1-208RD-PIXEL-AUDIT-R1.json'
GROUPS = (100250, 100251, 100252)
TW1_SPR_SHA = '53d5b2d40453a30fd1569637ebf0db7b3010542b00970ec83af0295a3b3ae31a'
O10_ZIP_SHA = 'b3f04b571b4b64b654ee4f314a33d6ab1a85e2d8a8ddaf21b2c102fc5a45c197'
O11_ZIP_SHA = 'a972f91257bef896a07e436727072d8341940c570386b6e9282b4e8d2892f811'
STREAM_SHA = 'db7e4e243eb7fea1a38f5fa9bd82444428725f8e671142e69dc3606ce6be2086'
WAV = {'zero_based': (73,'sam_18.wav',18892,'dc15de085cada9a701e79b6490f72a6169ea0ae08f4d7c9c13806074e99f56b3'),
       'one_based': (72,'sam_17.wav',15020,'3426f6e73bd7842e9be6212a6cfb7401fefcbe64e5f45761338a5f64656a2274')}
EXPECTED_FLAGS = ('original_client_executed', 'official_species_name_proven',
 'original_sound_event_selector_proven', 'raw_word_73_is_proven_sound_number',
 'sound_row_index_base_proven', 'word_10000_maps_to_soundaddr',
 'candidate_audition_proves_original_sync', 'historical_duration_unit_proven',
 'same_actual_game_deployment_proven', 'private_original_assets_in_public_git')

def need(condition: bool, msg: str) -> None:
    if not condition:
        raise ValueError('O11 source boundary: '+msg)

def validate(x:dict) -> dict:
    need(x['schema']=='stoneage.o11.tw10.original_animation_sound_word_candidate.source_derived.r1','schema')
    need(x['remote_base_head']=='d87bd74e8e1ac16beef837f0276806433956a688','fresh remote parent')
    need(x['prior_current_state_git_blob']=='20050acf279a01555ab06a381dfcdc936bd381a6','entire prior CURRENT')
    p=x['source_pins']
    need(p['tw1_p3h_archive_sha256']=='3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24','original P3H source')
    need(p['tw1_spr_sha256']==TW1_SPR_SHA and len(p['tw1_spradrn_sha256'])==64,'authentic TW1 SPR source')
    need(p['mixed25_o10_archive_sha256']==O10_ZIP_SHA,'independent mixed25 parent')
    need(len(p['original_soundaddr_sha256'])==64 and len(p['original_sound_container_sha256'])==64,'original sound source pins')
    s=x['full_spr_inventory']
    need((s['groups'],s['animations'],s['frames'])==(464,39065,242085),'complete TW1 SPR conservation')
    need(s['distinct_frame_sound_words']==34 and s['zero_frames']==229810 and s['nonzero_frames']==12275,'full frame field distribution')
    v=s['unique_nonzero_values']
    need(len(v)==33 and v==sorted(set(v)) and 73 in v and 10000 in v and 1000 in v and 114 in v,'do not conflate raw field with 114 rows')
    b=x['bounded_original_sprite_sample']
    need(b['numeric_spr_groups']==list(GROUPS) and b['sequences']==24 and b['directions_per_group']==8,'24 source animations')
    need(b['independent_source_spans_sha_equal']==24 and b['ordered_frame_positions']==352 and b['original_distinct_png']==208,'actual same source source spans')
    need(b['numeric_frame_word_occurrences']=={'0':304,'73':24,'10000':24},'keep original raw word 10000')
    rows=b['all_24_source_animation_records']
    need(len(rows)==24 and {(q['spr_no'],q['direction']) for q in rows}=={(g,d) for g in GROUPS for d in range(8)},'all eight directions per source group')
    for q in rows:
        g=q['spr_no'];d=q['direction'];n=26 if g==100252 else 9
        need(q['original_animation_index']==d*7 and q['frame_count']==n,'fixed original source index and ordered count')
        need(len(q['source_animation_span_sha256'])==64 and all(c in '0123456789abcdef' for c in q['source_animation_span_sha256']),'source animation SHA')
        f=q['nonzero_frame_source_words']
        need(f==[{'frame_index':4 if g==100252 else 2,'source_word':73},{'frame_index':6 if g==100252 else 4,'source_word':10000}],'do not invent event ID or normalize raw word')
    raw=json.dumps(rows,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
    need(hashlib.sha256(raw).hexdigest()==STREAM_SHA and x['ordered_24_anims_canonical_sha256']==STREAM_SHA,'all exact original spans unchanged')
    im=x['original_client_source_pixel_confirmation']
    need((im['actual_TW1_ADRN_REAL_RD_decoded_images'],im['identical_RGBA_to_previous_mixed25_png'],im['delta_count'])==(208,208,0),'all 208 physically decoded and same candidate RGBA')
    need(len(im['private_208_RD_independent_report_sha256'])==64 and im['official_species_identity_known'] is False and im['color_palette_is_proven_historical_selector'] is False,'TW1 source image provenance but not official game color')
    a=x['audio_index_candidate']
    need(a['sound_total_rows']==114 and a['raw_frame_value']==73 and a['source_word_10000_class']=='OUT_OF_INDEXED_RANGE','audition is hypothetical')
    for mode,(ind,name,n,sha) in WAV.items():
        q=a[mode];need((q['table_index'],q['name'],q['length'],q['sha256'])==(ind,name,n,sha),'audio index side '+mode)
        need(q['format']['channels']==1 and q['format']['sample_bytes']==1 and q['format']['pcm_frames']>0,'source WAV PCM metadata')
    need(a['zero_based']['name']!=a['one_based']['name'],'ambiguous index surfaces do not collapse')
    obs=x['private_observation']
    need((obs['private_zip_members'],obs['private_zip_bytes'],obs['private_zip_sha256'])==(216,1145869,O11_ZIP_SHA),'private archive identity')
    need(obs['private_zip_crc_and_original_source_members_replayed'] is True and obs['private_library_upload_success'] is True and obs['private_library_roundtrip_full_SHA_equal'] is True,'actual private custody')
    need(obs['browser_positive_case_groups']==5 and obs['browser_js_error_count']==0 and obs['browser_http_request_count']==0,'actual modern browser tests')
    need(obs['file_url_navigation_blocked'] is True and obs['original_source_same_bytes_memory_browser'] is True and obs['local_user_double_click_verified'] is False,'preserve browser local failure')
    need(set(x['historical_unknowns'])==set(EXPECTED_FLAGS) and not any(x['historical_unknowns'].values()),'no invented event, name or runtime proof')
    stage=x['project_gates']
    need(stage=={'stage_A_partial':7,'stage_A_open':2,'stage_B_gated':True,'wiki_gated':True,'R79_paused_nonblocking':True,'overall_completion_percent':None,'new_modern_game_development_started':False},'project stage')
    return {'TW1_native_source_frames':242085,'cross_sample_exact_action0_animations':24,'TW1_physical_pixels':208,'sound_event_selector_proven':False}

def validate_pixel_audit(data: dict, actual_raw: bytes, audit: dict) -> dict:
    expected = data['original_client_source_pixel_confirmation']
    need(hashlib.sha256(actual_raw).hexdigest()==expected['private_208_RD_independent_report_sha256'],'whole independently-derived pixel audit hash')
    need(json.loads(actual_raw)==audit,'the parsed independent original 208 pixel audit must match its raw bytes')
    need(audit['full_original_TW1_208_actual_RD_bytes_verified']==208 and audit['pixel_matches']==208 and audit['diff_count']==0,'physical original 208 RD verification')
    need(audit['errors_sample']==[],'all original pixel comparisons exact')
    records=audit['records']
    need(len(records)==208 and len(set(x['bitmap'] for x in records))==208,'no lost or duplicated source images')
    need(all(x['matched'] is True and len(x['rd_sha256'])==64 and len(x['source_ad_record_sha256'])==64 for x in records),'original record and RD SHA exact and every image matched')
    need(all(0<=x['bitmap']<125996 for x in records),'TW1 source record bounded')
    return {'source_verified_tw1_original_rd_pixels':208}

def main():
    data=json.loads(REPORT.read_text(encoding='utf-8'))
    raw=PIXEL_AUDIT.read_bytes()
    print('STONEAGE_O11_SOURCE_ONLY=PASS',json.dumps({**validate(data),**validate_pixel_audit(data,raw,json.loads(raw))},ensure_ascii=False))
if __name__ == '__main__':main()
