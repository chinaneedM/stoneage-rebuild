"""R50 custody-independent shape/path/stack validation; actual schema stays open."""
import argparse
import json
from pathlib import Path
from tools.stoneage_tw10_savedata_native_io_r50 import *
from tools.stoneage_tw10_savedata_native_io_r45_guard import graph_nodes, branches_guard
from tools.stoneage_tw10_savedata_native_io_r42_guard import inputs_guard
from tools.stoneage_tw10_savedata_native_io_r41_guard import identity_guard
from tools.stoneage_tw10_savedata_native_io_r40_guard import rows_guard, suffix_guard
from tools.stoneage_tw10_savedata_native_io_r37_guard import direct_guard
from tools.stoneage_tw10_savedata_upstream_r22_guard import FORBIDDEN


def require(ok,why):
    if not ok:raise ValueError('R50 '+why)


def call_guard(c,root,site,target,ats):
    require(c.get('site_rva')==site and c.get('actual_argument_values_roles_return_or_callee_effects_proven') is False,'call scope')
    direct_guard(c.get('identity',{}),site,target);keys,cap=inputs_guard(c.get('input_sources',{}),root,ats)
    suffix=c.get('physical_push_suffix',{});suffix_guard(suffix,root,site,keys,cap)
    initial={(p['site_rva'],r) for p in suffix['pushes'] for r in operand_registers(p['input'])}
    initial.update((site,r) for r in ('eax','ecx','edx','esi','edi','ebp'))
    require(all(k in keys for k in initial) or cap,'call source queries')
    defs=sorted({t['rva'] for q in c['input_sources']['queries'] if (q['site_rva'],q['register']) in initial for t in q['reaching_candidates'] if t['origin']=='definition'})
    rows=c.get('direct_input_definition_shapes');rows_guard(rows,MAX_DEFS,root,root+768,keys,cap,ats)
    require(c.get('direct_input_definition_count')==len(defs) and [r['site_rva'] for r in rows]==defs[:MAX_DEFS]
            and c.get('direct_input_definitions_truncated') is (len(defs)>MAX_DEFS),'call definition replay')


def slice_guard(rows,count,capped,limit,lo,hi,root,ats,inputs):
    keys,cap=inputs_guard(inputs,root,ats);rows_guard(rows,limit,lo,hi,keys,cap,ats)
    require(type(count) is int and 0<=count<=256 and len(rows)==min(count,limit) and capped is (count>limit),'shape sample bound')


def validate(d):
    require(isinstance(d,dict) and d.get('schema')==SCHEMA and d.get('status')==STATUS,'schema/status')
    require(d.get('runtime_sha256')==RUNTIME_SHA256 and d.get('savedata_sha256')==SAVEDATA_SHA256 and d.get('static_only') is True
            and d.get('r49_exact_original_revalidated') is True and d.get('r49_exact_report_sha256')==PRIOR_SHA256
            and d.get('r41_exact_original_caller_revalidated') is True and d.get('r41_exact_report_sha256')==R41_SHA256
            and all(d.get(f) is False for f in FLAGS),'source/non-promotion')
    c=d.get('caller_context',{});require(c.get('root_candidate_rva')==ROOT and c.get('actual_read_buffer_return_processor_output_or_schema_binding_proven') is False,'caller scope')
    ats=graph_nodes(c,ROOT,True);g=c.get('prior_narrow_graph',{});ns=c.get('prior_narrow_node_rvas');es=c.get('prior_narrow_edges')
    require(g.get('span_bytes')==192 and g.get('node_cap')==128 and isinstance(ns,list) and ns==sorted(set(ns)) and len(ns)==g.get('nodes') and set(ns)<=set(ats)
            and all(ROOT<=a<ROOT+192 for a in ns) and isinstance(es,list) and len(es)==g.get('edges') and all(e in c['bounded_edges'] for e in es),'prior narrow graph relation')
    e=c.get('entrygraph_support',{});require(e.get('actual_entry_or_execution_proven') is False
            and all(type(e.get(k)) is bool for k in ('root_boundary_seen','open_boundary_seen','read_boundary_seen','wrapper_boundary_seen','read_to_wrapper_edge_seen','processing_call_boundary_seen','entrygraph_node_limit_hit')),'entry support/non-promotion')
    call_guard(c.get('read_call_context',{}),ROOT,READ_CALL,READ_TARGET,ats);call_guard(c.get('processing_call_context',{}),ROOT,PROCESS,PROCESS_ROOT,ats)
    slice_guard(c.get('post_read_shapes'),c.get('post_read_shape_count'),c.get('post_read_shapes_truncated'),MAX_CALLER_ROWS,READ_CALL+5,PROCESS,ROOT,ats,c.get('post_read_input_sources'))
    slice_guard(c.get('first_output_shapes'),c.get('first_output_shape_count'),c.get('first_output_shapes_truncated'),MAX_CALLER_ROWS,PROCESS+5,PROCESS+69,ROOT,ats,c.get('first_output_input_sources'))
    slice_guard(c.get('post_processing_memory_shapes'),c.get('post_processing_memory_count'),c.get('post_processing_memory_shapes_truncated'),MAX_MEMORY_ROWS,PROCESS+5,ROOT+768,ROOT,ats,c.get('post_processing_memory_input_sources'))
    keys,cap=inputs_guard(c.get('address_input_sources',{}),ROOT,ats);address=c.get('address_shapes');rows_guard(address,3,ROOT,ROOT+768,keys,cap,ats)
    require([r['site_rva'] for r in address]==list(ADDRESS_SITES),'buffer address sites')
    inventory=c.get('literal_effect_input_shapes');require(isinstance(inventory,list) and [r['site_rva'] for r in inventory]==ats,'full effect shape inventory')
    synthetic_keys={(r['site_rva'],reg) for r in inventory for reg in r['input_query_registers']}
    rows_guard(inventory,256,ROOT,ROOT+768,synthetic_keys,False,ats)
    expected=[inventory_effect(r) for r in inventory];require(c.get('stack_effect_candidates')==expected,'literal ESP effect replay')
    states,updates,limit=stack_states(expected,c['bounded_edges'],ROOT)
    require(c.get('stack_model_updates')==updates and c.get('stack_model_update_limit_hit') is limit
            and c.get('address_stack_state_queries')==[state_summary(states,a,limit) for a in ADDRESS_SITES],'stack/address barrier replay')
    calls=c.get('post_read_call_identities');n=c.get('post_read_call_count');require(type(n) is int and 0<=n<=256 and isinstance(calls,list) and len(calls)==min(n,MAX_CALLS) and c.get('post_read_calls_truncated') is (n>MAX_CALLS),'call sample')
    for ident in calls:require(ident.get('call_rva') in ats and ident['call_rva']>=READ_CALL+5,'call node');identity_guard(ident,ident['call_rva'])
    branches_guard(c.get('post_read_zf_branch_contexts'),c.get('post_read_zf_branch_count'),c.get('post_read_zf_branches_truncated'),ROOT,ats,ROOT+768)
    require(all(b['branch_site_rva']>=READ_CALL+5 for b in c['post_read_zf_branch_contexts']),'post-read branch scope')
    transfers=c.get('post_processing_transfers');n=c.get('post_processing_transfer_count');require(type(n) is int and 0<=n<=256 and isinstance(transfers,list) and len(transfers)==min(n,32) and c.get('post_processing_transfers_truncated') is (n>32),'transfer sample')
    by={r['site_rva']:r for r in inventory}
    for t in transfers:
        r=t.get('shape',{});a=r.get('site_rva');require(a in by and by[a]==r and a>=PROCESS+5 and (t.get('direct_target_rva') is None or type(t['direct_target_rva']) is int)
                and type(t.get('fallthrough_rva')) is int and a<t['fallthrough_rva']<=a+15 and t.get('actual_flags_taken_path_or_loop_count_proven') is False,'transfer/no execution')
    for rows in [c['post_read_shapes'],c['first_output_shapes'],c['post_processing_memory_shapes'],address]:
        for r in rows:require(by[r['site_rva']]==r,'caller cross-surface row agreement')
    p=d.get('processing_entry_context',{});require(p.get('root_candidate_rva')==PROCESS_ROOT and p.get('actual_function_abi_decoding_compression_encryption_or_output_proven') is False
            and type(p.get('entrygraph_target_boundary_seen')) is bool and type(p.get('entrygraph_caller_to_target_edge_seen')) is bool,'processing entry scope')
    ats=graph_nodes(p,PROCESS_ROOT,True)
    slice_guard(p.get('early_frame_shapes'),p.get('early_frame_shape_count'),p.get('early_frame_shapes_truncated'),16,PROCESS_ROOT,PROCESS_ROOT+96,PROCESS_ROOT,ats,p.get('early_frame_input_sources'))
    slice_guard(p.get('memory_control_shapes'),p.get('memory_control_shape_count'),p.get('memory_control_shapes_truncated'),MAX_PROCESS_ROWS,PROCESS_ROOT,PROCESS_ROOT+768,PROCESS_ROOT,ats,p.get('memory_control_input_sources'))
    n=p.get('call_count');calls=p.get('call_identities');require(type(n) is int and 0<=n<=256 and isinstance(calls,list) and len(calls)==min(n,MAX_CALLS) and p.get('calls_truncated') is (n>MAX_CALLS),'processing call sample')
    for ident in calls:require(ident.get('call_rva') in ats,'processing call node');identity_guard(ident,ident['call_rva'])
    def ban(o):
        if isinstance(o,dict):
            require(not(set(o)&FORBIDDEN),'original payload')
            for v in o.values():ban(v)
        elif isinstance(o,list):
            for v in o:ban(v)
    ban(d);return True


def main():
    p=argparse.ArgumentParser();p.add_argument('--report',type=Path,required=True);path=p.parse_args().report
    require(path.stat().st_size<=500000,'report bound');validate(json.loads(path.read_text()))
    print('TW10_R50_STRICT_STATIC=PASS; ACTUAL_NATIVE_SAVE_SCHEMA=OPEN')


if __name__=='__main__':main()
