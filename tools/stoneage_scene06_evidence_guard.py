"""Public metadata gate; it does not rerun the private commercial executable."""
from pathlib import Path
import json
from tools.stoneage_private_scene_order_r6 import EXE_SHA, HTML_SHA, SPANS, display_order, require, compare

REPORT=Path(__file__).resolve().parents[1]/'research/recovered/STONEAGE-SCENE06-NATIVE-ORDER-R6.json'

def validate(r):
    require(r['schema']=='stoneage.scene06.native_display_order.r6','schema')
    require(r['program_sha256']==EXE_SHA and r['program_bytes']==561152 and
            r['source_r5_html_sha256']==HTML_SHA,'private source identity')
    for k in ('original_client_launched','original_world_entered','directdraw_executed'):
        require(r[k] is False,'original execution promotion: '+k)
    for k in ('original_sorter_executed_in_unicorn','sorter_not_stubbed','native_map_sweep_executed',
              'runtime_alias_table_injected_from_unique_original_adrn','consumer_LoadBmp_stubbed_to_failure'):
        require(r[k] is True,'bounded execution conditions: '+k)
    require(r['native_scan_crop']==[13,13,17,17] and r['injected_viewport_translation']==[100,200], 'controlled crop')
    require(set(r['source_spans'])==set(SPANS),'source span coverage')
    for k,(a,b) in SPANS.items():
        v=r['source_spans'][k]
        require((v['va_start'],v['va_end_exclusive'])==(a,b) and
                len(v['sha256'])==64 and int(v['sha256'],16)>0,'source span identity')
    cases=[[a,p,b,q,compare((a,p),(b,q))] for p in (0,1,10,127,128,255)
           for q in (0,1,10,127,128,255) for a,b in ((0,1),(29,0),(32767,0),(0,32767),(3,3))]
    require(r['comparator_cases']==cases and r['comparator_case_count']==180,'native comparator cases')
    rows=r['controlled_queue']
    require(len(rows)==30 and [v['queue_no'] for v in rows]==list(range(30)),'30 queue identities')
    require(all(v['priority']==(0 if i<25 else 10) and v['layer']==('tile' if i<25 else 'parts')
                for i,v in enumerate(rows)),'native plane priorities')
    require(r['native_tile_priority']==0 and r['descendant_header_tile_priority']==1,'source version distinction')
    expected=[v['queue_no'] for v in display_order(rows)]
    require(r['original_sorted_queue_numbers']==expected,'actual source sort trace')
    require(r['native_consumer_requested_bitmap_order']==[rows[i]['bitmapno'] for i in expected], 'native consumer')
    require(r['independent_source_comparator']['compiled_cases_equal_native']==180 and
            r['independent_source_comparator']['same_build_source_authenticated'] is False,'independent source scope')
    require(set(r['unverified'])=={'native_map_and_alias_loader','live_original_palette','native_camera',
            'characters_parts_occlusion','same_deployed_official_build','playable_world_entry'},'unresolved dependencies')
    require(r['stage_a']=='7_PARTIAL_2_OPEN' and r['stage_b']=='GATED' and
            r['r79']=='PAUSED_NON_BLOCKING' and r['overall_completion_percent'] is None,'historical boundaries')
    require(r['pixel_impact']['changed_pixels']==3549 and r['pixel_impact']['actual_native_screenshot'] is False,'candidate pixel scope')
    require(not any(k in r for k in ('sprites','raw_exe','raw_map','original_pixels','library_file_id')),'private payload in public report')
    return True

if __name__=='__main__':
    validate(json.loads(REPORT.read_text()))
    print('SCENE06_PUBLIC_METADATA_ONLY=PASS; ORIGINAL_WORLD_ENTERED=FALSE')
