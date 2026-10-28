"""Public numeric guards: controlled fragment order is not live-game occlusion."""
import json
from pathlib import Path
from tools.stoneage_private_scene_actor_order_r9 import EXE_SHA,R8_SHA,SPANS,reference_list,require
ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'research/recovered/STONEAGE-SCENE09-NATIVE-ORDER-R9.json'

def validate(r):
    require(r['schema']=='stoneage.controlled_actor_parts_order.r9','schema')
    require(r['program_sha256']==EXE_SHA and r['original_R8_html_sha256']==R8_SHA,'original inputs')
    require(r['original_ADRN_sha256']=='92d0137590d35a7a1f4fb11af3ad13bbc585813a4b0e1e3f933c397007fbff74' and r['original_map_sha256']=='62dbef1614ede0ba032ca9c69cbfdc3d43938e45baba78701885790937b86b90','actual original resources')
    for k in ['native_actor_caller_fragment_executed','native_linked_insert_getters_and_sorter_executed','source_ADRN_array_injected','actor_structures_and_coordinates_injected','actor_then_parts_phase_order_injected','original_map_sweep_executed','all_30_native_map_requests_match_R8','all_208_source_actor_ADRN_records_match_R8','selected_source_frame_displacements_zero']:
        require(r[k] is True,'bounded execution or injected conditions: '+k)
    for k in ['complete_original_frame_phase_order_proven','native_GPU_blit_executed','original_client_launched','original_world_entered','official_species_identity_authenticated','same_deployed_build_proven']:
        require(r[k] is False,'unproven promotion: '+k)
    require(r['native_functions_stubbed']==[],'no metadata/caller/sort stubs')
    require(r['source_coordinate_field_order']=='XY' and r['map_world_scale']['float_value']==64,'actual source coordinate field layout')
    require(r['scope']=='CONTROLLED_TWO_ACTORS_FIVE_PARTS_1X1_MODE0_NOT_LIVE_GAME','finite scope')
    require(set(r['source_spans'])==set(SPANS),'all source code spans')
    for key,(a,b) in SPANS.items():
        v=r['source_spans'][key];require([v['start_va'],v['end_va_exclusive']]==[a,b] and len(v['sha256'])==64,'original code fingerprint')
    parts=r['original_parts'];require(len(parts)==5 and [p['token'] for p in parts]==list(range(25,30)),'all source part occurrences')
    prior=json.loads((ROOT/'research/recovered/STONEAGE-SCENE06-NATIVE-ORDER-R6.json').read_text())['controlled_queue'][25:]
    for p,q in zip(parts,prior):
        require(p['kind']=='parts' and p['bitmapno']==q['bitmapno'] and p['source_grid']==[q['x'],q['y']] and
                p['world']==[q['x']*64,q['y']*64] and p['footprint']==[1,1] and p['raw_attribute_word']==0,'same bounded source room metadata')
    configs=[([x,y],100250,0) for y in range(13,18) for x in range(13,18)]+[([15,15],p,d) for p in [100250,100251,100252] for d in range(8) if (p,d)!=(100250,0)]
    require(r['case_count']==len(r['cases'])==len(configs)==48,'all source movement and bitmap binding cases')
    for c,(anchor,pet,d) in zip(r['cases'],configs):
        require((c['anchor'],c['pet_spr'],c['direction'])==(anchor,pet,d),'source case identity')
        x,y=anchor;require(len(c['actors'])==2,'two injected actors')
        for i,a in enumerate(c['actors']):
            require(a['token']==['human','pet'][i] and a['kind']=='actor' and a['world']==[x*64,(y+i)*64] and
                    [a['screen_x'],a['screen_y']]==[(x+y-26)*32+i*32+100,(y-x)*24+i*24+200], 'explicit lab coordinates')
        linked=reference_list(c['actors'],parts);require(c['native_linked_tokens']==linked,'original insertion order')
        require(c['native_draw_tokens']==list(reversed(range(25)))+list(reversed(linked)),'native priority10 reverse consumption')
        entries=c['queue_entries'];require(len(entries)==32 and [e['queue_no'] for e in entries]==list(range(32)),'all native display queue references')
        require([e['token'] for e in entries]==list(range(25))+linked and [e['priority'] for e in entries]==[0]*25+[10]*7,'source priorities and occurrences')
        require(c['native_sorted_queue_numbers']==list(reversed(range(25)))+list(reversed(range(25,32))),'original final stable scope ordering')
    require((r['stage_a'],r['stage_b'],r['r79'],r['overall_completion_percent'])==('7_PARTIAL_2_OPEN','GATED','PAUSED_NON_BLOCKING',None),'stage boundaries')
    require(not any(k in r for k in ['sprites','raw_exe','original_pixels','library_file_id']),'no private payload')
    return {'cases':48,'native_map_parts':5,'complete_original_frame_phase_order_proven':False}

if __name__=='__main__':print(json.dumps(validate(json.loads(REPORT.read_text()))))
