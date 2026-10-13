"""R24 strict static scope and report limits; immutable original custody separate."""
import argparse
import json
from pathlib import Path
from tools.stoneage_tw10_savedata_upstream_r24 import (
    SCHEMA,STATUS,FLAGS,PREFIXES,CALLS,SCALAR_SITE,SCALAR_ROOT,
    PRIOR_REPORT_SHA256,RUNTIME_SHA256,SAVEDATA_SHA256)
from tools.stoneage_tw10_savedata_upstream_r23_guard import require
from tools.stoneage_tw10_savedata_upstream_r22_guard import source_guard,FORBIDDEN

def check(ok,why):
    if not ok:raise ValueError('R24 '+why)

def validate(d):
    check(isinstance(d,dict) and d.get('schema')==SCHEMA and d.get('status')==STATUS,'schema')
    check(d.get('runtime_sha256')==RUNTIME_SHA256 and d.get('savedata_sha256')==SAVEDATA_SHA256,'original hash')
    check(d.get('r23_original_identity_revalidated') is True and d.get('static_only') is True
          and d.get('r23_exact_report_sha256')==PRIOR_REPORT_SHA256,'R23 original chain')
    check(all(d.get(k) is False for k in FLAGS),'runtime promotion')
    audits=d.get('prefix_audits')
    check(isinstance(audits,list) and len(audits)==3,'three calls')
    for row,callrow,anchors in zip(audits,CALLS,PREFIXES):
        check(row.get('name')==callrow[0] and row.get('call_rva')==callrow[2]
              and row.get('r23_suffix_revalidated') is True
              and row.get('selected_function_entry_proven') is False,'prefix identity')
        candidates=row.get('candidate_prefixes')
        check(isinstance(candidates,list) and len(candidates)==len(anchors),'prefix count')
        for p,anchor in zip(candidates,anchors):
            check(p.get('anchor_rva')==anchor and p.get('call_rva')==callrow[2]
                  and type(p.get('linear_boundary_reached')) is bool
                  and type(p.get('decoded_instruction_count')) is int
                  and 0<=p['decoded_instruction_count']<=64,'prefix bounds')
            check(all(p.get(k) is False for k in ('verified_entry_or_alignment','actual_stack_values_known','all_incoming_paths_proven')),'entry/stack promotion')
            s=p.get('r23_suffix',{})
            check(s.get('conditional_pre_call_esp_only') is True and s.get('abi_roles_applied') is False
                  and s.get('actual_stack_values_known') is False
                  and s.get('linear_call_boundary_reached')==p['linear_boundary_reached'],'suffix scope')
            pushes=s.get('pushes');check(isinstance(pushes,list) and len(pushes)<=24,'PUSH cap')
            check(p['linear_boundary_reached'] or not pushes,'unreached suffix')
            prev=callrow[2]
            for n,push in enumerate(pushes):
                check(anchor<=push.get('site_rva',-1)<prev
                      and push.get('conditional_pre_call_esp_offset')==n*4
                      and push.get('input',{}).get('width_bytes')==4,'PUSH order/width')
                prev=push['site_rva']
            b=p.get('last_suffix_barrier')
            if b is not None:
                check(p['linear_boundary_reached'] and anchor<=b.get('site_rva',-1)<callrow[2]
                      and b.get('kind') in ('control_transfer','partial_or_other_push','stack_register_write','memory_write','unmodeled_instruction')
                      and isinstance(b.get('operand_shapes'),list) and len(b['operand_shapes'])<=8,'barrier scope')
    s=d.get('realloc_eax_definition',{})
    check(s.get('site_rva')==SCALAR_SITE and s.get('anchor_rva')==SCALAR_ROOT
          and all(s.get(k) is False for k in ('actual_input_value_known','allocation_size_or_role_proven','original_path_executed_proven')),'scalar scope')
    ops=s.get('operand_shapes');check(isinstance(ops,list) and 1<=len(ops)<=8,'scalar operands')
    check(ops[0].get('kind')=='register' and ops[0].get('register')=='eax'
          and ops[0].get('decoder_write') is True,'EAX definition')
    inputs=s.get('register_inputs');sources=s.get('input_sources')
    check(isinstance(inputs,list) and len(inputs)<=7 and isinstance(sources,dict)
          and set(sources)==set(inputs),'scalar sources')
    for val in sources.values():source_guard(val)
    model=s.get('conditional_scalar_model',{})
    check(model.get('evaluated_runtime_result') is None,'scalar result promotion')
    check(model.get('kind') in ('unmodeled','conditional_u32_left_shift'),'scalar model')
    if model['kind']=='conditional_u32_left_shift':
        check(s.get('class') in ('shl','sal') and len(ops)==2 and ops[0].get('width_bytes')==4
              and ops[1].get('kind')=='immediate' and model.get('width_bits')==32
              and model.get('shift_count_mask')==31 and model.get('output_modulus')==4294967296
              and model.get('literal_shift_count')==(ops[1]['constant']&31),'shift semantics')
    else:
        check(all(model.get(k) is None for k in ('width_bits','shift_count_mask','literal_shift_count','output_modulus')),'unmodeled scalar')
    f=d.get('realloc_branch_frontier',{})
    check(f.get('anchor_rva')==SCALAR_ROOT and f.get('call_rva')==CALLS[2][2]
          and type(f.get('nodes')) is int and 1<=f['nodes']<=128
          and type(f.get('edges')) is int and 0<=f['edges']<=350
          and f.get('opaque_calls_kill_flags') is True
          and f.get('actual_paths_or_complete_entries_proven') is False,'flags scope')
    rows=f.get('branches');check(isinstance(rows,list) and len(rows)<=24,'branch cap')
    for b in rows:
        check(SCALAR_ROOT<=b.get('site_rva',-1)<CALLS[2][2] and b.get('branch_outcome_known') is False
              and type(b.get('graph_path_to_call')) is bool and isinstance(b.get('condition'),str)
              and b['condition'].startswith('j') and b['condition'] not in ('jmp','ljmp'),'branch identity')
        tokens=b.get('flag_sources');check(isinstance(tokens,list) and len(tokens)<=24,'flag cap')
        for token in tokens:
            check(token.get('origin') in ('entry','unknown_call','definition')
                  and type(token.get('rva')) is int,'flag source')
            if token['origin']!='definition':check(token.get('semantic') is None,'opaque flag effect')
    def ban(o):
        if isinstance(o,dict):
            check(not set(o)&FORBIDDEN,'proprietary payload')
            for v in o.values():ban(v)
        elif isinstance(o,list):
            for v in o:ban(v)
    ban(d);return True

def main():
    p=argparse.ArgumentParser();p.add_argument('--report',type=Path,required=True)
    path=p.parse_args().report;check(path.stat().st_size<=70000,'report size')
    validate(json.loads(path.read_text()));print('TW10_R24_STRICT_STATIC=PASS; HEAP_NATIVE_SAVE=OPEN')
if __name__=='__main__':main()
