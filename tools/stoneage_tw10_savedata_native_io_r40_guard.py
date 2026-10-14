"""Replay R40 frame/slot arithmetic and bound syntax; custody checked separately."""
import argparse
import json
from pathlib import Path
from tools.stoneage_tw10_savedata_native_io_r40 import *
from tools.stoneage_tw10_savedata_native_io_r37_guard import row_guard, direct_guard
from tools.stoneage_tw10_savedata_native_io_r30_guard import graph_guard
from tools.stoneage_tw10_savedata_native_io_r29_guard import shape_guard, input_guard
from tools.stoneage_tw10_savedata_upstream_r22_guard import FORBIDDEN

def require(ok,why):
    if not ok:raise ValueError('R40 '+why)

def rows_guard(rows,limit,lo,hi,keys,cap,ats=None):
    require(isinstance(rows,list) and len(rows)<=limit,'row bound')
    sites=[]
    for row in rows:
        at=row.get('site_rva');require(type(at) is int and lo<=at<hi and (ats is None or at in ats),'row scope')
        row_guard(row,at,keys,cap);sites.append(at)
    require(sites==sorted(set(sites)),'row order')

def suffix_guard(suffix,lo,call,keys,cap,flags=False):
    require(type(suffix.get('linear_call_boundary_reached')) is bool
            and suffix.get('conditional_pre_call_esp_only') is True
            and suffix.get('abi_roles_applied') is False and suffix.get('actual_stack_values_known') is False
            and suffix.get('stop_reason') in ('candidate_anchor','control_transfer','stack_or_memory_barrier',
                                             'push_cap','decode_or_boundary_gap','bound'),'suffix assumption')
    ps=suffix.get('pushes');require(isinstance(ps,list) and len(ps)<=24
                                  and (suffix['linear_call_boundary_reached'] or not ps),'push bound')
    last=call
    for idx,p in enumerate(ps):
        at=p.get('site_rva');op=p.get('input',{})
        require(type(at) is int and lo<=at<last and p.get('conditional_pre_call_esp_offset')==idx*4
                and op.get('width_bytes')==4,'physical push')
        shape_guard({'site_rva':at,'class':'unmodeled','operands':[op]},at)
        require(all((at,r) in keys for r in operand_registers(op)) or cap,'push queries')
        if flags:require(p.get('actual_abi_role_value_or_buffer_length_proven') is False,'push non-promotion')
        last=at

def validate(d):
    require(isinstance(d,dict) and d.get('schema')==SCHEMA and d.get('status')==STATUS,'schema')
    require(d.get('runtime_sha256')==RUNTIME_SHA256 and d.get('savedata_sha256')==SAVEDATA_SHA256
            and d.get('r39_exact_original_revalidated') is True and d.get('r39_exact_report_sha256')==PRIOR_SHA256
            and d.get('static_only') is True and all(d.get(k) is False for k in FLAGS),'prior/non-promotion')
    direct_guard(d.get('caller_identity',{}),READ_CALL,READ_ROOT)
    c=d.get('native_read_context',{})
    require(c.get('root_candidate_rva')==READ_ROOT and c.get('actual_frame_parameter_or_payload_role_proven') is False,'callee')
    graph_guard(c.get('graph',{}));effects=c.get('stack_effect_candidates');edges=c.get('bounded_edges')
    require(isinstance(effects,list) and len(effects)==c['graph']['nodes'],'effect count')
    ats=[]
    for e in effects:
        at,k,delta,w=e.get('site_rva'),e.get('syntax_class'),e.get('esp_delta'),e.get('operand_width_bytes')
        require(type(at) is int and READ_ROOT<=at<READ_ROOT+768
                and e.get('conditional_32bit_stack_address_only') is True
                and k in ('push','pop','neutral','opaque_call','unknown_esp_write'),'effect scope')
        if k in ('push','pop'):require(type(w) is int and w in (2,4) and type(delta) is int and delta==(-w if k=='push' else w),'effect delta')
        else:require(w is None and (type(delta) is int and delta==0 if k=='neutral' else delta is None),'effect opacity')
        ats.append(at)
    require(ats==sorted(set(ats)) and READ_ROOT in ats and isinstance(edges,list) and len(edges)==c['graph']['edges']
            and all(isinstance(e,list) and len(e)==2 and all(type(x) is int and x in ats for x in e) for e in edges)
            and edges==[list(e) for e in sorted(set(tuple(e) for e in edges))],'topology')
    states,updates,limit=stack_states(effects,edges,READ_ROOT)
    require(c.get('stack_model_updates')==updates and c.get('stack_model_update_limit_hit') is limit,'stack replay')
    keys=input_guard(c.get('frame_input_sources',{}),READ_ROOT);cap=c['frame_input_sources']['query_limit_hit']
    reads,defs,prolog=c.get('early_frame_read_shapes'),c.get('frame_definition_shapes'),c.get('entry_prolog_shapes')
    rows_guard(reads,MAX_READS,READ_ROOT,READ_ROOT+96,keys,cap,ats)
    rows_guard(defs,MAX_FRAME_DEFS,READ_ROOT,READ_ROOT+768,keys,cap,ats)
    rows_guard(prolog,24,READ_ROOT,READ_ROOT+24,keys,cap,ats)
    require(c.get('early_frame_read_scope')=='instruction_starts_first96bytes_whole_instructions_in_parent768'
            and type(c.get('early_frame_reads_truncated')) is bool,'read scope')
    for row in reads:
        require(row['mnemonic']!='lea' and any(o.get('kind')=='memory' and o.get('decoder_read')
                and o.get('geometry',{}).get('base_register')=='ebp' for o in row['operands']),'read spelling')
    for row in prolog:require(bool(set(row['decoder_written_registers'])&{'esp','ebp'}),'prolog write')
    count=c.get('frame_definition_count')
    expected=sorted({s['rva'] for q in c['frame_input_sources']['queries'] if q['register']=='ebp'
                     for s in q['reaching_candidates'] if s['origin']=='definition'})
    require(type(count) is int and count==len(expected) and [r['site_rva'] for r in defs]==expected[:MAX_FRAME_DEFS]
            and c.get('frame_definitions_truncated') is (count>MAX_FRAME_DEFS),'definition source agreement')
    summaries=[state_summary(states,r['site_rva'],limit) for r in defs]
    require(c.get('frame_definition_esp_summaries')==summaries,'summary replay')
    pushes=c.get('prior_caller_pushes')
    require(isinstance(pushes,list) and len(pushes)<=24,'prior pushes')
    last=READ_CALL
    for i,p in enumerate(pushes):
        at=p.get('site_rva');op=p.get('input',{})
        require(type(at) is int and 0x4ed33<=at<last and p.get('conditional_pre_call_esp_offset')==i*4
                and op.get('width_bytes')==4 and p.get('actual_abi_role_value_or_buffer_length_proven') is False,'caller push')
        shape_guard({'site_rva':at,'class':'unmodeled','operands':[op]},at);last=at
    require(c.get('conditional_frame_slot_bridges')==[frame_bridge(r,c['frame_input_sources'],defs,summaries,pushes) for r in reads],
            'frame bridge replay/non-promotion')
    apis=c.get('read_api_contexts');require(isinstance(apis,list) and len(apis)==2,'api count')
    for a,(site,anchor) in zip(apis,APIS):
        ident=a.get('identity',{});imp=ident.get('import_identity') or {}
        require(a.get('site_rva')==site and a.get('linear_anchor_rva')==anchor and site in ats
                and ident.get('call_rva')==site and ident.get('kind')=='memory_indirect'
                and ident.get('runtime_target_or_effects_proven') is False
                and ident.get('import_slot_association_proven') is True
                and imp.get('name')=='ReadFile' and imp.get('iat_rva')==0x520d8
                and a.get('actual_api_parameter_handle_buffer_length_or_effect_proven') is False,'api identity')
        require(next(e['syntax_class'] for e in effects if e['site_rva']==site)=='opaque_call','api opacity')
        ak=input_guard(a.get('input_sources',{}),READ_ROOT);ac=a['input_sources']['query_limit_hit']
        suffix_guard(a.get('physical_push_suffix',{}),anchor,site,ak,ac)
    p=d.get('postcall_context',{})
    require(p.get('root_candidate_rva')==PARENT and p.get('actual_endcheck_text_eof_or_savedata_payload_role_proven') is False,'postcall')
    graph_guard(p.get('graph',{}));keys=input_guard(p.get('input_sources',{}),PARENT);cap=p['input_sources']['query_limit_hit']
    pd,pc=p.get('prior_push_definition_shapes'),p.get('prior_postcall_compare_shapes')
    rows_guard(pd,16,PARENT,PARENT+768,keys,cap);rows_guard(pc,8,READ_CALL+5,READ_CALL+48,keys,cap)
    require(all(r['mnemonic'] in ('cmp','test') for r in pc) and p.get('buffer_address_spelling_pairs')==address_pairs(pd,pc),'address replay')
    bs=p.get('postcall_branch_contexts');count=p.get('postcall_branch_count')
    require(type(count) is int and 0<=count<=256 and isinstance(bs,list) and len(bs)==min(count,MAX_BRANCHES)
            and p.get('postcall_branches_truncated') is (count>MAX_BRANCHES),'branch bounds')
    seen=[]
    for b in bs:
        at=b.get('branch_site_rva');n=b.get('source_count');ss=b.get('source_candidates')
        require(type(at) is int and READ_CALL+5<=at<READ_CALL+80 and b.get('mnemonic') in ('je','jne','jz','jnz')
                and type(b.get('direct_target_rva')) is int and type(b.get('fallthrough_rva')) is int
                and at<b['fallthrough_rva']<=at+15 and type(n) is int and 0<=n<=256
                and isinstance(ss,list) and len(ss)==min(n,MAX_SOURCE_SAMPLES)
                and b.get('sources_truncated') is (n>MAX_SOURCE_SAMPLES)
                and type(b.get('predecessor_nodes_examined')) is int and 1<=b['predecessor_nodes_examined']<=512
                and type(b.get('predecessor_cap_hit')) is bool and type(b.get('branch_disconnected_in_graph')) is bool
                and b.get('actual_zf_value_feasible_or_taken_path_proven') is False,'branch scope/non-promotion')
        sk=[]
        for source in ss:
            r=source.get('shape',{});a=r.get('site_rva');kind=source.get('kind')
            require(type(a) is int and PARENT<=a<PARENT+768 and kind in ('zf_write','opaque_call')
                    and (kind!='opaque_call' or r.get('mnemonic') in ('call','lcall')),'flag primitive')
            row_guard(r,a,keys,cap);sk.append((a,kind))
        require(sk==sorted(set(sk)),'flag order');seen.append(at)
    require(seen==sorted(set(seen)),'branch order')
    def ban(o):
        if isinstance(o,dict):
            require(not(set(o)&FORBIDDEN),'original payload')
            for v in o.values():ban(v)
        elif isinstance(o,list):
            for v in o:ban(v)
    ban(d);return True

def main():
    p=argparse.ArgumentParser();p.add_argument('--report',type=Path,required=True)
    path=p.parse_args().report;require(path.stat().st_size<=150000,'report bound')
    validate(json.loads(path.read_text()));print('TW10_R40_STRICT_STATIC=PASS; ENDCHECK_ROLE_NATIVE_SAVE=OPEN')

if __name__=='__main__':main()
