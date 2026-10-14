"""Replay byte slices and local-frame spellings; reject runtime/alias promotion."""
import argparse
import json
from pathlib import Path
from tools.stoneage_tw10_savedata_native_io_r47 import *
from tools.stoneage_tw10_savedata_native_io_r45_guard import graph_nodes, branches_guard
from tools.stoneage_tw10_savedata_native_io_r42_guard import inputs_guard
from tools.stoneage_tw10_savedata_native_io_r41_guard import identity_guard
from tools.stoneage_tw10_savedata_native_io_r40_guard import rows_guard
from tools.stoneage_tw10_savedata_native_io_r37_guard import direct_guard
from tools.stoneage_tw10_savedata_upstream_r22_guard import FORBIDDEN


def require(ok,why):
    if not ok:raise ValueError('R47 '+why)


def validate(d):
    require(isinstance(d,dict) and d.get('schema')==SCHEMA and d.get('status')==STATUS,'schema/status')
    require(d.get('runtime_sha256')==RUNTIME_SHA256 and d.get('savedata_sha256')==SAVEDATA_SHA256 and d.get('static_only') is True
            and d.get('r46_exact_original_revalidated') is True and d.get('r46_exact_report_sha256')==PRIOR_SHA256
            and all(d.get(f) is False for f in FLAGS),'source/non-promotion')
    c=d.get('read_byte_result_context',{});require(c.get('root_candidate_rva')==READ_ROOT and c.get('actual_prefix_marker_api_result_total_count_or_return_value_proven') is False,'read scope')
    ats=graph_nodes(c,READ_ROOT,True);surface=c.get('byte_source_surface',{})
    keys,cap=inputs_guard(surface.get('input_sources',{}),READ_ROOT,ats)
    rows=c.get('byte_shapes');rows_guard(rows,6,READ_ROOT,READ_API,keys,cap,ats)
    require([r['site_rva'] for r in rows]==list(BYTE_SITES),'byte site order')
    defs=surface.get('source_definition_shapes');rows_guard(defs,MAX_SOURCE_ROWS,READ_ROOT,READ_ROOT+768,keys,cap,ats)
    expected=sorted({t['rva'] for q in surface['input_sources']['queries'] for t in q['reaching_candidates'] if t['origin']=='definition'})
    pending=surface.get('source_expansion_pending_definition_rvas')
    require(isinstance(pending,list) and pending==sorted(set(pending)) and set(pending)<=set(expected)
            and not(set(pending)&{r['site_rva'] for r in defs}),'source pending scope')
    require(surface.get('source_definition_count')==len(expected) and surface.get('source_definition_shape_cap')==MAX_SOURCE_ROWS
            and surface.get('source_expansion_rounds')==SOURCE_ROUNDS and surface.get('source_definitions_truncated') is (len(expected)>MAX_SOURCE_ROWS)
            and [r['site_rva'] for r in defs]==[a for a in expected[:MAX_SOURCE_ROWS] if a not in pending],'source bounds/agreement')
    require(c.get('conditional_byte_relation')==byte_relation(rows,defs,surface['input_sources']),'partial byte/source replay')
    identity_guard(c.get('first_read_api_identity',{}),READ_API)
    require(c['first_read_api_identity'].get('import_identity')=={'dll':'KERNEL32.dll','name':'ReadFile','iat_rva':0x520d8},'first API identity')
    require(c.get('post_api_window_start_rva')==READ_API+6 and c.get('post_api_window_bytes')==TAIL_SPAN,'tail window')
    tkeys,tcap=inputs_guard(c.get('post_api_and_frame_input_sources',{}),READ_ROOT,ats)
    tail=c.get('post_api_shapes');rows_guard(tail,MAX_TAIL_ROWS,READ_API+6,READ_API+6+TAIL_SPAN,tkeys,tcap,ats)
    expected=[a for a in ats if READ_API+6<=a<READ_API+6+TAIL_SPAN]
    require(c.get('post_api_shape_count')==len(expected) and [r['site_rva'] for r in tail]==expected[:MAX_TAIL_ROWS]
            and c.get('post_api_shapes_truncated') is (len(expected)>MAX_TAIL_ROWS),'tail count/sample')
    frames=c.get('frame_reference_shapes');n=c.get('frame_reference_instruction_count')
    rows_guard(frames,MAX_FRAME_ROWS,READ_ROOT,READ_ROOT+768,tkeys,tcap,ats)
    require(type(n) is int and 0<=n<=256 and len(frames)==min(n,MAX_FRAME_ROWS)
            and c.get('frame_reference_shapes_truncated') is (n>MAX_FRAME_ROWS)
            and all(frame_refs([r]) for r in frames),'frame reference sample')
    refs=frame_refs(frames);require(c.get('frame_reference_candidates')==refs and c.get('equal_frame_spelling_pairs')==frame_pairs(refs),'frame spelling replay')
    # Identical original instructions shared by evidence surfaces must stay identical.
    by={r['site_rva']:r for r in rows+defs}
    for r in tail+frames:
        if r['site_rva'] in by:require(r==by[r['site_rva']],'cross-surface shape disagreement')
        by[r['site_rva']]=r
    bs=c.get('post_api_zf_branch_contexts');branches_guard(bs,c.get('post_api_zf_branch_count'),c.get('post_api_zf_branches_truncated'),READ_ROOT,ats,READ_API+6+TAIL_SPAN)
    require(all(b['branch_site_rva']>=READ_API+6 for b in bs),'post-API branch lower bound')
    w=d.get('savedata_wrapper_return_context',{});require(w.get('root_candidate_rva')==WRAPPER
            and w.get('actual_native_return_value_abi_frame_or_wrapper_count_binding_proven') is False,'wrapper non-promotion')
    ats=graph_nodes(w,WRAPPER,True);require(NATIVE_CALL in ats,'native caller graph support')
    direct_guard(w.get('native_call_identity',{}),NATIVE_CALL,READ_ROOT)
    keys,cap=inputs_guard(w.get('input_sources',{}),WRAPPER,ats);rows=w.get('post_call_shapes')
    rows_guard(rows,MAX_TAIL_ROWS,NATIVE_CALL+5,NATIVE_CALL+5+WRAPPER_SPAN,keys,cap,ats)
    expected=[a for a in ats if NATIVE_CALL+5<=a<NATIVE_CALL+5+WRAPPER_SPAN]
    require(w.get('post_call_shape_count')==len(expected) and [r['site_rva'] for r in rows]==expected[:MAX_TAIL_ROWS]
            and w.get('post_call_shapes_truncated') is (len(expected)>MAX_TAIL_ROWS),'wrapper return sample')
    def ban(o):
        if isinstance(o,dict):
            require(not(set(o)&FORBIDDEN),'original payload')
            for v in o.values():ban(v)
        elif isinstance(o,list):
            for v in o:ban(v)
    ban(d);return True


def main():
    p=argparse.ArgumentParser();p.add_argument('--report',type=Path,required=True);path=p.parse_args().report
    require(path.stat().st_size<=300000,'report bound');validate(json.loads(path.read_text()))
    print('TW10_R47_STRICT_STATIC=PASS; ACTUAL_NATIVE_SAVE=OPEN')


if __name__=='__main__':main()
