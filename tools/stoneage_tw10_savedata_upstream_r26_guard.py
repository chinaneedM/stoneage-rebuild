"""R26 static expression validation; immutable source/exact JSON gate separate."""
import argparse,json
from pathlib import Path
from tools.stoneage_tw10_savedata_upstream_r26 import (
    SCHEMA,STATUS,PRIOR_SHA256,FLAGS,BINDINGS,CREATE_ROOT,SETE,PUSH,REALLOC_ROOT,
    LEA,SHIFT,QUERY,RUNTIME_SHA256,SAVEDATA_SHA256)
from tools.stoneage_tw10_savedata_upstream_r22_guard import source_guard,FORBIDDEN

def check(ok,why):
    if not ok:raise ValueError('R26 '+why)

def graph(g,root):
    check(g.get('root_rva')==root and type(g.get('nodes')) is int and 1<=g['nodes']<=128
          and type(g.get('edges')) is int and 0<=g['edges']<=350
          and g.get('entry_or_executed_path_proven') is False
          and g.get('structural_call_return_assumption_only') is True,'graph scope')

def validate(d):
    check(isinstance(d,dict) and d.get('schema')==SCHEMA and d.get('status')==STATUS,'schema')
    check(d.get('runtime_sha256')==RUNTIME_SHA256 and d.get('savedata_sha256')==SAVEDATA_SHA256,'hash')
    check(d.get('r25_exact_original_revalidated') is True and d.get('r25_exact_report_sha256')==PRIOR_SHA256
          and d.get('static_only') is True,'R25 exact chain')
    check(all(d.get(k) is False for k in FLAGS),'runtime promotion')
    bindings=d.get('caller_bindings');check(isinstance(bindings,list) and len(bindings)==2,'bindings')
    for row,(site,root) in zip(bindings,BINDINGS):
        identity=row.get('identity',{})
        check(row.get('call_rva')==site and row.get('target_candidate_rva')==root
              and row.get('supported_by_r25_original_scan') is True
              and row.get('runtime_entry_or_call_effect_admitted') is False
              and identity.get('call_rva')==site and identity.get('kind')=='direct'
              and identity.get('direct_target_rva')==root
              and identity.get('runtime_target_or_effects_proven') is False,'binding identity/effect')
    c=d.get('create_context',{});graph(c.get('graph',{}),CREATE_ROOT)
    op=c.get('destination',{})
    check(c.get('sete_rva')==SETE and c.get('push_rva')==PUSH and op.get('kind')=='register'
          and op.get('register')=='al' and op.get('width_bytes')==1 and op.get('decoder_write') is True
          and c.get('actual_flag_value_known') is False and c.get('call_argument_or_return_effect_admitted') is False,'SETE scope')
    before=c.get('eax_before_sete',{});after=c.get('eax_before_push',{})
    for source in (before,after):
        source_guard(source);check(source.get('candidate_anchor_rva')==CREATE_ROOT,'SETE source root')
    tokens=before.get('reaching_candidates',[])
    semantic=(tokens[0].get('semantic') or {}) if len(tokens)==1 else {}
    zero=(len(tokens)==1 and tokens[0].get('origin')=='definition' and semantic.get('kind')=='constant_assignment'
          and semantic.get('constant')==0 and semantic.get('width_bits')==32
          and before.get('query_site_in_candidate_graph') is True and before.get('candidates_truncated') is False)
    m=c.get('conditional_model',{})
    check(m.get('kind')=='conditional_eax_low_byte_sete' and m.get('preserved_mask')==4294967040
          and m.get('condition_flag')=='zf' and m.get('low_byte_choices')==[0,1]
          and m.get('pre_eax_unique_zero_candidate')==zero
          and m.get('conditional_possible_values')==([0,1] if zero else None)
          and m.get('whole_runtime_value_known') is False and m.get('abi_or_heap_flag_role_proven') is False,'conditional partial model')
    flags=c.get('flag_sources');check(isinstance(flags,list) and len(flags)<=24,'flag cap')
    for t in flags:
        check(t.get('origin') in ('definition','unknown_call','entry') and type(t.get('rva')) is int,'flag source')
        if t['origin']!='definition':check(t.get('semantic') is None,'opaque flag effect')
    r=d.get('realloc_context',{});graph(r.get('graph',{}),REALLOC_ROOT)
    check(r.get('actual_comparison_outcome_known') is False and r.get('caller_return_or_heap_effect_admitted') is False,'realloc outcome/effect')
    inputs=r.get('inputs');check(isinstance(inputs,list) and len(inputs)==len(QUERY),'input count')
    for item,(site,reg) in zip(inputs,QUERY):
        check((item.get('site_rva'),item.get('register'))==(site,reg) and item.get('actual_value_known') is False,'input identity/value')
        source_guard(item.get('candidate_source',{}));check(item['candidate_source'].get('candidate_anchor_rva')==REALLOC_ROOT,'input root')
    a,b=r.get('lea_shape',{}),r.get('shift_shape',{})
    check(a.get('site_rva')==LEA and b.get('site_rva')==SHIFT,'arithmetic identity')
    ao,bo=a.get('operands'),b.get('operands')
    check(isinstance(ao,list) and len(ao)<=8 and isinstance(bo,list) and len(bo)<=8,'operand caps')
    source=inputs[3]['candidate_source'];tokens=source.get('reaching_candidates',[])
    linked=(len(tokens)==1 and tokens[0].get('origin')=='definition' and tokens[0].get('rva')==LEA
            and source.get('query_site_in_candidate_graph') is True and source.get('candidates_truncated') is False)
    g=ao[1].get('geometry',{}) if len(ao)==2 else {}
    qualified=(linked and a.get('class')=='lea' and b.get('class') in ('shl','sal') and len(ao)==2 and len(bo)==2
               and ao[0].get('register')=='eax' and ao[0].get('width_bytes')==4 and ao[1].get('kind')=='memory'
               and g.get('base_register')=='ecx' and g.get('index_register')=='ecx'
               and g.get('segment_register') is None and g.get('displacement_region') is None
               and g.get('index_scale') in (1,2,4,8) and type(g.get('relative_field_offset')) is int
               and bo[0].get('register')=='eax' and bo[0].get('width_bytes')==4 and bo[1].get('kind')=='immediate')
    m=r.get('conditional_affine_model',{})
    check(m.get('unique_lea_to_shift_candidate')==linked and m.get('evaluated_original_result') is None
          and m.get('actual_ecx_value_known') is False and m.get('allocation_size_or_abi_role_proven') is False,'affine effect scope')
    if qualified:
        count=bo[1]['constant']&31
        check(m.get('kind')=='conditional_ecx_affine_u32' and m.get('shift_count')==count and m.get('modulus')==4294967296
              and m.get('multiplier')==((1+g['index_scale'])*(1<<count))&0xffffffff
              and m.get('bias')==(g['relative_field_offset']<<count)&0xffffffff,'affine coefficients')
    else:
        check(m.get('kind')=='unqualified_composition' and all(m.get(k) is None for k in ('shift_count','modulus','multiplier','bias')),'unqualified expression')
    def ban(o):
        if isinstance(o,dict):
            check(not set(o)&FORBIDDEN,'proprietary payload')
            for v in o.values():ban(v)
        elif isinstance(o,list):
            for v in o:ban(v)
    ban(d);return True

def main():
    p=argparse.ArgumentParser();p.add_argument('--report',type=Path,required=True)
    path=p.parse_args().report;check(path.stat().st_size<=70000,'size')
    validate(json.loads(path.read_text()));print('TW10_R26_STRICT_CONDITIONAL_STATIC=PASS; NATIVE_SAVE=OPEN')
if __name__=='__main__':main()
