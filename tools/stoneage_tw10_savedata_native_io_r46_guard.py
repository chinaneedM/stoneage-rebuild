"""Strict R46 replay with conditional syntax and custody separate from runtime proof."""
import argparse
import json
from pathlib import Path
from tools.stoneage_tw10_savedata_native_io_r46 import *
from tools.stoneage_tw10_savedata_native_io_r45_guard import graph_nodes, branches_guard
from tools.stoneage_tw10_savedata_native_io_r42_guard import inputs_guard
from tools.stoneage_tw10_savedata_native_io_r41_guard import identity_guard
from tools.stoneage_tw10_savedata_native_io_r40_guard import rows_guard, suffix_guard
from tools.stoneage_tw10_savedata_native_io_r37_guard import row_guard, direct_guard
from tools.stoneage_tw10_savedata_native_io_r29_guard import shape_guard, input_guard
from tools.stoneage_tw10_savedata_native_io_r30_guard import graph_guard
from tools.stoneage_tw10_savedata_upstream_r22_guard import FORBIDDEN


def require(ok,why):
    if not ok:raise ValueError('R46 '+why)


def surface_guard(c,root):
    require(c.get('root_candidate_rva')==root and c.get('actual_function_entry_call_effect_or_complete_aliases_proven') is False,'helper surface scope')
    graph_guard(c.get('graph',{}));keys=input_guard(c.get('input_sources',{}),root);cap=c['input_sources']['query_limit_hit']
    refs=c.get('memory_references');n=c.get('memory_reference_count')
    require(type(n) is int and 0<=n<=1024 and isinstance(refs,list) and len(refs)==min(n,48) and c.get('memory_references_truncated') is (n>48),'helper surface memory bound')
    for r in refs:
        at=r.get('site_rva');require(type(at) is int and root<=at<root+768 and r.get('actual_effective_address_value_owner_or_parameter_proven') is False,'helper surface memory scope')
        shape_guard({'site_rva':at,'class':'unmodeled','operands':[r.get('operand')]},at)
        require(type(r.get('operand_index')) is int and 0<=r['operand_index']<8 and isinstance(r.get('mnemonic'),str)
                and isinstance(r.get('input_query_registers'),list) and (all((at,v) in keys for v in r['input_query_registers']) or cap)
                and type(r.get('stack_or_frame_spelling_candidate')) is bool and type(r.get('shared_displacement_reference_candidate')) is bool,'helper surface references')
    calls=c.get('call_candidates');n=c.get('call_count')
    require(type(n) is int and 0<=n<=256 and isinstance(calls,list) and len(calls)==min(n,24) and c.get('calls_truncated') is (n>24),'helper surface call bound')
    for ident in calls:
        at=ident.get('call_rva');require(type(at) is int and root<=at<root+768,'surface call scope');identity_guard(ident,at)


def validate(d):
    require(isinstance(d,dict) and d.get('schema')==SCHEMA and d.get('status')==STATUS,'schema/status')
    require(d.get('runtime_sha256')==RUNTIME_SHA256 and d.get('savedata_sha256')==SAVEDATA_SHA256 and d.get('static_only') is True
            and d.get('r45_exact_original_revalidated') is True and d.get('r45_exact_report_sha256')==PRIOR_SHA256
            and d.get('r37_exact_helper_surface_revalidated') is True and d.get('r37_exact_report_sha256')==R37_SHA256
            and all(d.get(f) is False for f in FLAGS),'source/non-promotion')
    c=d.get('read_adjustment_context',{});require(c.get('root_candidate_rva')==READ_ROOT and c.get('actual_read_execution_count_buffer_or_contents_proven') is False,'read scope')
    ats=graph_nodes(c,READ_ROOT,True);keys,cap=inputs_guard(c.get('input_sources',{}),READ_ROOT,ats)
    require(c.get('window_start_rva')==COPY and c.get('window_stop_exclusive_rva')==READ_API,'window scope')
    expected=[a for a in ats if COPY<=a<READ_API];rows=c.get('window_shapes')
    rows_guard(rows,MAX_WINDOW_ROWS,COPY,READ_API,keys,cap,ats)
    require(c.get('window_shape_count')==len(expected) and [r['site_rva'] for r in rows]==expected[:MAX_WINDOW_ROWS]
            and c.get('window_shapes_truncated') is (len(expected)>MAX_WINDOW_ROWS)
            and set((COPY,DEC,STORE,SHIFT,COUNT_PUSH,BUFFER_PUSH)).issubset({r['site_rva'] for r in rows}),'complete pairing shapes')
    paths=signatures(c['bounded_edges'],READ_ROOT,READ_API)
    require(c.get('root_first_api_paths')==paths and c.get('conditional_adjustment_relation')==bundle_relation(rows,c['input_sources'],paths),'path/bundle replay')
    branches=c.get('bypass_branch_arms');require(isinstance(branches,list) and len(branches)==2,'branch arms')
    for b,at in zip(branches,BRANCHES):
        z=b.get('prior_zf_context',{});require(z.get('branch_site_rva')==at,'branch identity')
        branches_guard([z],1,False,READ_ROOT,ats,READ_API)
        require(z['direct_target_rva'] in ats and z['fallthrough_rva'] in ats
                and [at,z['direct_target_rva']] in c['bounded_edges'] and [at,z['fallthrough_rva']] in c['bounded_edges'],'branch edge agreement')
        require(b.get('target_arm_paths')==signatures(c['bounded_edges'],z['direct_target_rva'],READ_API)
                and b.get('fallthrough_arm_paths')==signatures(c['bounded_edges'],z['fallthrough_rva'],READ_API),'branch arm path replay')
    identity_guard(c.get('first_read_api_identity',{}),READ_API)
    require(c['first_read_api_identity'].get('import_identity')=={'dll':'KERNEL32.dll','name':'ReadFile','iat_rva':0x520d8},'read import')
    # R45 count relationship is retained as evidence, never reinterpreted as runtime truth.
    old=c.get('prior_count_relationship',{})
    require(old.get('actual_same_address_contents_modified_count_or_taken_path_proven') is False
            and old.get('original_count_or_decrement_result_evaluated') is False,'prior count non-promotion')
    w=d.get('write_helper_context',{});require(w.get('root_candidate_rva')==HELPER
            and w.get('actual_seek_parameter_values_return_or_caller_frame_preservation_proven') is False,'helper scope')
    ats=graph_nodes(w,HELPER,True);keys,cap=inputs_guard(w.get('input_sources',{}),HELPER,ats)
    direct_guard(w.get('caller_identity',{}),BARRIER,HELPER)
    suffix=w.get('prior_caller_suffix',{});suffix_guard(suffix,WRITE_ROOT,BARRIER,set(),True)
    effects=w.get('stack_effect_candidates');require(isinstance(effects,list) and [e.get('site_rva') for e in effects]==ats,'stack effect scope/order')
    for e in effects:
        kind=e.get('syntax_class');delta=e.get('esp_delta');width=e.get('operand_width_bytes')
        require(e.get('conditional_32bit_stack_address_only') is True,'stack conditional scope')
        require((kind=='neutral' and delta==0 and width is None)
                or (kind in ('opaque_call','unknown_esp_write') and delta is None and width is None)
                or (kind in ('push','pop') and width in (2,4) and delta==width*(-1 if kind=='push' else 1)),'stack effect syntax')
    states,updates,limit=stack_states(effects,w['bounded_edges'],HELPER)
    require(w.get('stack_model_updates')==updates and w.get('stack_model_update_limit_hit') is limit,'stack replay')
    rows=w.get('pre_seek_esp_read_shapes');n=w.get('pre_seek_esp_read_count')
    rows_guard(rows,MAX_HELPER_READS,HELPER,SEEK_API,keys,cap,ats)
    require(type(n) is int and 0<=n<=256 and len(rows)==min(n,MAX_HELPER_READS) and w.get('pre_seek_esp_reads_truncated') is (n>MAX_HELPER_READS),'helper read bound')
    for r in rows:
        require(r['mnemonic']!='lea' and any(o.get('kind')=='memory' and o.get('decoder_read') is True and o.get('geometry',{}).get('base_register')=='esp' for o in r['operands']),'helper ESP read syntax')
    summaries=[state_summary(states,r['site_rva'],limit) for r in rows]
    require(w.get('stack_state_queries')==summaries and w.get('conditional_caller_slot_bridges')==[slot_bridge(r,s,suffix['pushes']) for r,s in zip(rows,summaries)],'ESP bridge replay')
    ident=w.get('seek_api_identity',{});identity_guard(ident,SEEK_API)
    require(SEEK_API in ats and ident.get('import_identity')=={'dll':'KERNEL32.dll','name':'SetFilePointer','iat_rva':SEEK_IAT},'seek import')
    suffix_guard(w.get('seek_physical_push_suffix',{}),HELPER,SEEK_API,keys,cap)
    surface_guard(w.get('r37_helper_surface_rederived',{}),HELPER)
    require(w['r37_helper_surface_rederived']['graph']==w['graph'] and ident in w['r37_helper_surface_rederived']['call_candidates'],'R37 helper/seek identity correspondence')
    require(w.get('root_to_seek_structural_path_candidate') is path_without(w['bounded_edges'],HELPER,SEEK_API),'helper structural path')
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
    print('TW10_R46_STRICT_STATIC=PASS; ACTUAL_NATIVE_SAVE=OPEN')


if __name__=='__main__':main()
