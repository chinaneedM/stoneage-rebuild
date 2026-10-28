"""Source-bound pet observation validation. It cannot certify official species."""
import copy,json,struct
from pathlib import Path
from tools.stoneage_private_scene_pet_r8 import (
    ROOT,PINS,PET_KEYS,EVIDENCE,LINK_KIND,R7_HTML_SHA,R7_SOURCE_SHA,qualified_links,need,sha)
REPORT=ROOT/'research/recovered/STONEAGE-SCENE08-PET-SOURCE-R8.json'

def validate(r):
    need(r['schema']=='stoneage.same_carrier_pet_observation.r8','pet schema')
    need(r['source_scope']=='PRESERVED_MIXED25_NOT_OFFICIAL_TW1','sample scope')
    need(r['source_files']=={k:{'bytes':v[0],'sha256':v[1]} for k,v in PINS.items()},'actual source identities')
    need(r['prior_R7_html_sha256']==R7_HTML_SHA and r['prior_R7_source_report_sha256']==R7_SOURCE_SHA and r['evidence_sha256']==EVIDENCE,'exact prior evidence pins')
    for key in ['same_deployed_build_proven','official_species_identity_authenticated','original_world_entered','original_client_launched_in_this_observation','live_palette_verified','native_actor_occlusion_verified','native_fps_verified','audio_events_played','automatic_action_fallback']:
        need(r[key] is False,'unproven promotion: '+key)
    need(r['source_duration_word_is_not_milliseconds'] is True and r['preview_frame_ms']==180,'source timing is not modern milliseconds')
    need(r['actor_placement']=='MODERN_MANUAL_OVERLAY_AFTER_ALL_MAP_PARTS','manual placement scope')
    need((r['stage_a'],r['stage_b'],r['r79'],r['overall_completion_percent'])==('7_PARTIAL_2_OPEN','GATED','PAUSED_NON_BLOCKING',None),'stage boundary')
    links,prior=qualified_links();need(r['template_links']==links,'all seven original template rows, including flag0')
    need([g['spr_no'] for g in r['groups']]==list(PET_KEYS),'fixed material family')
    refs=[];selected=0
    for g,old in zip(r['groups'],prior):
        need((g['source_group_index'],g['offset'],g['end_offset'],g['source_animation_count'],g['reserved_word'],g['whole_group_segment_sha256'])==
             (old['group_index'],old['offset'],old['end_offset'],old['anim_count'],old['reserved'],old['segment_sha256']),'whole original group witness')
        need(g['index_record_sha256']==sha(struct.pack('<IIHH',g['spr_no'],g['offset'],g['source_animation_count'],g['reserved_word'])),'source index record')
        ll=[v for v in links if v['server_graphic_column_37']==g['spr_no']]
        need(g['template_links']==ll and {v['server_name'] for v in ll}=={g['preserved_template_name']},'preserve source-original names and row occurrences')
        need(g['available_source_action_codes']==sorted({v['anim_no'] for v in old['animations']}) and g['absent_source_action_codes']==[6],'explicit missing human action')
        aa=[v for v in old['animations'] if v['anim_no']==2]
        need(len(g['animations'])==len(aa)==8,'all eight directions')
        for a,b in zip(g['animations'],aa):
            need((a['source_animation_index'],a['header_offset'],a['end_offset'],a['direction'],a['action'],a['duration_word'],a['frames'])==
                 (b['index'],b['header_offset'],b['end_offset'],b['direction'],b['anim_no'],b['duration'],b['frames']),'all original selected frame occurrences, including repeats')
            raw=struct.pack('<HHII',a['direction'],a['action'],a['duration_word'],len(a['frames']))+b''.join(struct.pack('<IhhH',*f) for f in a['frames'])
            need(sha(raw)==a['source_animation_span_sha256'] and a['end_offset']-a['header_offset']==len(raw),'selected original frame bytes')
            refs.extend(f[0] for f in a['frames']);selected+=1
    bitmaps={v['bitmapno']:v for v in r['bitmaps']}
    need(len(refs)==r['frame_occurrences']==256 and selected==r['selected_animation_count']==24,'original frame references not species counts')
    need(len(bitmaps)==len(r['bitmaps'])==r['distinct_source_bitmaps']==160 and set(refs)==set(bitmaps),'all actual pet image references')
    for b in bitmaps.values():
        need(16<=b['size']<=1000000 and 0<=b['offset']<=PINS['real_15.bin'][0]-b['size'],'bounded original REAL extent')
        need(0<b['width']<=1024 and 0<b['height']<=1024 and b['RD_flag'] in [0,1],'original image geometry')
        for key in ['record_sha256','RD_sha256','index_pixels_sha256','candidate_RGBA_sha256','PNG_sha256']:
            need(len(b[key])==64 and all(c in '0123456789abcdef' for c in b[key]),'exact source digest')
    raw=(ROOT/'research/recovered/STONEAGE-SCENE07-ACTOR-SOURCE-R7.json').read_bytes();need(sha(raw)==R7_SOURCE_SHA,'immutable R7 human source')
    prior=json.loads(raw);human=copy.deepcopy(prior['groups'][0]);human['animations']=[a for a in human['animations'] if a['action']==2]
    needed={f[0] for a in human['animations'] for f in a['frames']};bb=[v for v in prior['bitmaps'] if v['bitmapno'] in needed]
    need(r['human_reused']=={'group':human,'bitmaps':bb},'unchanged qualified human reference')
    return {'pet_groups':3,'selected_animations':selected,'frame_occurrences':len(refs),'pet_bitmaps':len(bitmaps),'official_species_identity_authenticated':False}

if __name__=='__main__':print(json.dumps(validate(json.loads(REPORT.read_text()))))
