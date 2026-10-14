"""R39 strict scalar/prefix/native-call bounds; original custody separate."""
import argparse
import json
from pathlib import Path
from tools.stoneage_tw10_savedata_native_io_r39 import *
from tools.stoneage_tw10_savedata_native_io_r37_guard import row_guard, direct_guard
from tools.stoneage_tw10_savedata_native_io_r29_guard import input_guard, shape_guard
from tools.stoneage_tw10_savedata_upstream_r22_guard import FORBIDDEN

def require(ok,why):
    if not ok:raise ValueError('R39 '+why)

def validate(d):
    require(isinstance(d,dict) and d.get('schema')==SCHEMA and d.get('status')==STATUS,'schema')
    require(d.get('runtime_sha256')==RUNTIME_SHA256 and d.get('savedata_sha256')==SAVEDATA_SHA256
            and d.get('r38_exact_original_revalidated') is True and d.get('r38_exact_report_sha256')==PRIOR_SHA256
            and d.get('static_only') is True and all(d.get(k) is False for k in FLAGS),'prior/non-promotion')
    h=d.get('helper_mask_and_tokens',{})
    require(h.get('root_candidate_rva')==ROOT and h.get('actual_helper_value_index_table_or_handle_owner_proven') is False,'helper scope')
    from tools.stoneage_tw10_savedata_native_io_r30_guard import graph_guard
    graph_guard(h.get('graph',{}))
    keys=input_guard(h.get('input_sources',{}),ROOT);cap=h['input_sources']['query_limit_hit']
    mask,shift=h.get('mask_shape',{}),h.get('shift_shape',{})
    row_guard(mask,MASK,keys,cap);row_guard(shift,SCALARS[1],keys,cap)
    require(mask.get('conditional_full_width_model')==full_width_model(mask),'mask model')
    require((SCALARS[1],'esi') in keys,'shift source query')
    source=next(q for q in h['input_sources']['queries'] if (q['site_rva'],q['register'])==(SCALARS[1],'esi'))
    expected=composition({'site_rva':MASK,'class':mask['mnemonic'],'operands':mask['operands']},
                         {'site_rva':SCALARS[1],'class':shift['mnemonic'],'operands':shift['operands']},source)
    require(h.get('conditional_composition')==expected,'mask/shift composition')
    evidence=h.get('prior_stack_evidence',{});effects=evidence.get('effects');edges=evidence.get('edges')
    require(isinstance(effects,list) and len(effects)==h['graph']['nodes'] and isinstance(edges,list)
            and len(edges)==h['graph']['edges'],'stack evidence counts')
    ats=[]
    for e in effects:
        at,kind,delta,width=e.get('site_rva'),e.get('syntax_class'),e.get('esp_delta'),e.get('operand_width_bytes')
        require(type(at) is int and ROOT<=at<ROOT+768 and e.get('conditional_32bit_stack_address_only') is True
                and kind in ('neutral','push','pop','opaque_call','unknown_esp_write'),'effect scope')
        if kind in ('push','pop'):require(width in (2,4) and type(width) is int and delta==(-width if kind=='push' else width),'effect delta')
        else:require(width is None and (delta==0 if kind=='neutral' else delta is None),'effect opacity')
        ats.append(at)
    require(ats==sorted(set(ats)) and ROOT in ats and all(isinstance(e,list) and len(e)==2 and all(x in ats for x in e) for e in edges)
            and edges==[list(e) for e in sorted(set(tuple(e) for e in edges))],'stack topology')
    writes=h.get('explicit_write_shapes');require(isinstance(writes,list) and len(writes)<=256,'write bounds')
    writekeys=[]
    for w in writes:
        at,n,op=w.get('site_rva'),w.get('operand_index'),w.get('operand',{})
        shape_guard({'site_rva':at,'class':'unmodeled','operands':[op]},at)
        require(at in ats and type(n) is int and 0<=n<8 and op.get('kind')=='memory' and op.get('decoder_write') is True,'write primitive')
        writekeys.append((at,n))
    require(writekeys==sorted(set(writekeys)),'write order')
    reads,bridges,audits=h.get('prior_stack_read_shapes'),h.get('prior_slot_bridges'),h.get('prefix_token_audits')
    require(isinstance(reads,list) and len(reads)==2 and isinstance(bridges,list) and len(bridges)==2
            and isinstance(audits,list) and len(audits)==2,'prefix surfaces')
    for row,bridge,at in zip(reads,bridges,READS):
        shape_guard({'site_rva':at,'class':'unmodeled','operands':row.get('operands')},at)
        require(row.get('site_rva')==at and row.get('actual_instruction_effect_or_value_known') is False
                and bridge.get('callee_read_site_rva')==at
                and bridge.get('conditional_32bit_stack_address_required') is True
                and bridge.get('conditional_32bit_near_call_return_address_required') is True
                and bridge.get('actual_argument_value_abi_owner_or_stack_alias_binding_proven') is False,'prior geometry not runtime binding')
    require(audits==[prefix_audit(evidence,row,bridge,writes) for row,bridge in zip(reads,bridges)],'prefix overwrite/token replay')
    caller=input_guard(d.get('helper_caller_push_sources',{}),PARENT)
    require((0x4ed47,'esi') in caller and (0x4ed48,'ebx') in caller,'caller symbols')
    r=d.get('native_read_caller',{})
    require(r.get('root_candidate_rva')==PARENT and r.get('read_context_candidate_rva')==READ_ROOT
            and r.get('actual_callee_abi_buffer_payload_length_or_return_proven') is False,'read context')
    graph_guard(r.get('graph',{}));direct_guard(r.get('read_context_call_identity',{}),READ_CALL,READ_ROOT)
    keys=input_guard(r.get('input_sources',{}),PARENT);cap=r['input_sources']['query_limit_hit']
    require(all((READ_CALL,reg) in keys for reg in ('eax','ebx','ecx','esi','edi','ebp')) or cap,'read inputs')
    suffix=r.get('pre_call_suffix',{});pushes=r.get('push_candidates');old=suffix.get('pushes')
    require(type(suffix.get('linear_call_boundary_reached')) is bool and suffix.get('conditional_pre_call_esp_only') is True
            and suffix.get('abi_roles_applied') is False and suffix.get('actual_stack_values_known') is False
            and isinstance(pushes,list) and isinstance(old,list) and len(pushes)==len(old)<=24
            and (suffix['linear_call_boundary_reached'] or not pushes),'read suffix')
    last=READ_CALL
    for idx,(p,o) in enumerate(zip(pushes,old)):
        at=p.get('site_rva');regs=operand_registers(p.get('input',{}))
        require(type(at) is int and 0x4ed33<=at<last and p.get('conditional_pre_call_esp_offset')==idx*4
                and p.get('input',{}).get('width_bytes')==4 and all(p.get(k)==v for k,v in o.items())
                and p.get('actual_abi_role_value_or_buffer_length_proven') is False
                and p.get('input_query_registers')==regs and (all((at,x) in keys for x in regs) or cap),'read push geometry')
        last=at
    defs=r.get('push_definition_shapes');count=r.get('push_definition_count')
    require(type(count) is int and 0<=count<=256 and isinstance(defs,list) and len(defs)==min(count,MAX_DEFS)
            and r.get('push_definitions_truncated') is (count>MAX_DEFS),'definition bounds')
    seen=[]
    for row in defs:
        at=row.get('site_rva');require(type(at) is int and PARENT<=at<PARENT+768,'definition scope')
        row_guard(row,at,keys,cap);seen.append(at)
    require(seen==sorted(set(seen)),'definition order')
    comparisons=r.get('postcall_compare_shapes');count=r.get('postcall_compare_count')
    require(type(count) is int and 0<=count<=256 and isinstance(comparisons,list) and len(comparisons)==min(count,MAX_COMPARE)
            and r.get('postcall_compares_truncated') is (count>MAX_COMPARE),'compare bounds')
    seen=[]
    for row in comparisons:
        at=row.get('site_rva');require(type(at) is int and READ_CALL+5<=at<READ_CALL+48 and row.get('mnemonic') in ('cmp','test'),'postcall compare scope')
        row_guard(row,at,keys,cap);seen.append(at)
    require(seen==sorted(set(seen)),'compare order')
    def ban(obj):
        if isinstance(obj,dict):
            require(not(set(obj)&FORBIDDEN),'original payload')
            for v in obj.values():ban(v)
        elif isinstance(obj,list):
            for v in obj:ban(v)
    ban(d);return True

def main():
    p=argparse.ArgumentParser();p.add_argument('--report',type=Path,required=True)
    path=p.parse_args().report;require(path.stat().st_size<=100000,'report bound')
    validate(json.loads(path.read_text()));print('TW10_R39_STRICT_STATIC=PASS; NATIVE_PAYLOAD_SAVE=OPEN')

if __name__=='__main__':main()
