"""Offline guards for source-derived numeric actors, never game-world acceptance."""
import hashlib
import json
from pathlib import Path
import struct
from tools.stoneage_private_scene_actor_r7 import PINS,GROUPS,R6_SHA,need,sha
ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'research/recovered/STONEAGE-SCENE07-ACTOR-SOURCE-R7.json'

def validate(r):
    need(r['schema']=='stoneage.same_carrier_actor_observation.r7','source schema')
    need(r['source_scope']=='PRESERVED_MIXED25_NOT_OFFICIAL_TW1' and r['room_r6_sha256']==R6_SHA,'bounded source scope')
    need(r['source_files']=={k:{'bytes':v[0],'sha256':v[1]} for k,v in PINS.items()},'whole-file source identities')
    for key in ['original_world_entered','original_client_launched_in_this_observation','official_build_authenticated','entity_names_verified','live_palette_verified','native_actor_occlusion_verified','native_fps_verified','audio_events_played']:
        need(r[key] is False,'unproven promotion: '+key)
    need(r['actor_placement']=='MODERN_MANUAL_OVERLAY_AFTER_ALL_MAP_PARTS','manual overlay attribution')
    need(r['source_duration_word_is_not_milliseconds'] is True and r['preview_frame_ms']==180,'separate source duration and preview rate')
    need((r['stage_a'],r['stage_b'],r['r79'],r['overall_completion_percent'])==('7_PARTIAL_2_OPEN','GATED','PAUSED_NON_BLOCKING',None),'stage boundary')
    need([g['spr_no'] for g in r['groups']]==list(GROUPS),'fixed two groups')
    bitmaps={b['bitmapno']:b for b in r['bitmaps']}
    need(len(bitmaps)==len(r['bitmaps'])==r['distinct_source_bitmaps']==128,'bitmap uniqueness and conservation')
    frames=animations=0;needed=set()
    for g,gi,start,end in zip(r['groups'],[0,464],[0,2889630],[6128,2895758]):
        need((g['source_group_index'],g['offset'],g['end_offset'],g['source_animation_count'],g['reserved_word'])==(gi,start,end,104,2),'native source index fields')
        need(g['index_record_sha256']==sha(struct.pack('<IIHH',g['spr_no'],start,104,2)),'original index record SHA')
        need(len(g['animations'])==16,'all selected animations retained')
        need({(a['direction'],a['action']) for a in g['animations']}=={(d,a) for d in range(8) for a in [2,6]},'direction/action ambiguity')
        for a in g['animations']:
            count=6 if a['action']==2 else 7
            need(len(a['frames'])==count and a['duration_word']==(600 if a['action']==2 else 1000),'source frames/duration')
            need(a['source_animation_index']==13*a['direction']+(2 if a['action']==2 else 1),'original selector occurrence')
            b=struct.pack('<HHII',a['direction'],a['action'],a['duration_word'],count)+b''.join(struct.pack('<IhhH',*f) for f in a['frames'])
            need(start<=a['header_offset']<a['end_offset']<=end and a['end_offset']-a['header_offset']==len(b),'bounded selected source span')
            need(sha(b)==a['source_animation_span_sha256'],'selected original bytes digest')
            frames+=count;animations+=1;needed.update(f[0] for f in a['frames'])
    need(frames==r['frame_occurrences']==208 and animations==r['selected_animation_count']==32,'frame reference conservation')
    need(needed==set(bitmaps),'all selected references resolved exactly')
    for b in bitmaps.values():
        need(16<=b['size']<=1000000 and 0<=b['offset']<=PINS['real_15.bin'][0]-b['size'],'bounded actual RD extent')
        need(0<b['width']<=1024 and 0<b['height']<=1024 and b['RD_flag'] in [0,1],'actual legacy geometry')
        for key in ['record_sha256','RD_sha256','index_pixels_sha256','candidate_RGBA_sha256','PNG_sha256']:
            need(len(b[key])==64 and all(c in '0123456789abcdef' for c in b[key]),'source digest')
    return {'selected_animations':animations,'frame_occurrences':frames,'source_bitmaps':len(bitmaps),'original_world_entered':False}

def main():print(json.dumps(validate(json.loads(REPORT.read_text()))))
if __name__=='__main__':main()
