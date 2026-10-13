"""R31 strict opaque capture/store scope; original exact custody separate."""
import argparse,json
from pathlib import Path
from tools.stoneage_tw10_savedata_native_io_r31 import *
from tools.stoneage_tw10_savedata_native_io_r30_guard import graph_guard
from tools.stoneage_tw10_savedata_native_io_r29_guard import input_guard
from tools.stoneage_tw10_savedata_upstream_r22_guard import FORBIDDEN

def check(ok,why):
    if not ok:raise ValueError('R31 '+why)

def direct(i,at,target):
    check(i.get('call_rva')==at and i.get('kind')=='direct' and i.get('direct_target_rva')==target
          and i.get('runtime_target_or_effects_proven') is False,'direct CALL')

def validate(d):
    check(isinstance(d,dict) and d.get('schema')==SCHEMA and d.get('status')==STATUS,'schema')
    check(d.get('runtime_sha256')==RUNTIME_SHA256 and d.get('savedata_sha256')==SAVEDATA_SHA256,'hash')
    check(d.get('r30_exact_original_revalidated') is True and d.get('r30_exact_report_sha256')==PRIOR_SHA256
          and d.get('static_only') is True,'prior')
    check(all(d.get(k) is False for k in FLAGS),'runtime promotion')
    c=d.get('caller_capture',{});check(c.get('root_candidate_rva')==PARENT and c.get('conditional_post_api_rva')==POST
          and c.get('callee_entry_or_stack_binding_proven') is False,'caller scope')
    direct(c.get('supporting_parent_call',{}),PARENT_CALLER,PARENT);direct(c.get('helper_call_identity',{}),CALL,HELPER)
    api=c.get('api_identity',{});g=api.get('memory_target') or {}
    check(api.get('call_rva')==API and api.get('kind')=='memory_indirect'
          and api.get('import_identity')=={'dll':'KERNEL32.dll','name':'CreateFileA','iat_rva':0x520a0}
          and api.get('import_slot_association_proven') is True and api.get('runtime_target_or_effects_proven') is False
          and g.get('width_bytes')==4 and all(g.get(k) is None for k in ('base_register','index_register','segment_register'))
          and g.get('displacement_region',{}).get('displacement_rva')==0x520a0,'API identity')
    graph_guard(c.get('graph',{}));keys=input_guard(c.get('inputs',{}),PARENT)
    check((POST,'eax') in keys and all((CALL,r) in keys for r in ('eax','ebx','esi','edi','ecx')),'caller queries')
    suffix=c.get('local_push_suffix',{});ps=suffix.get('pushes');copies=c.get('register_copy_candidates');count=c.get('copy_count')
    check(suffix.get('conditional_pre_call_esp_only') is True and suffix.get('abi_roles_applied') is False
          and suffix.get('actual_stack_values_known') is False and type(suffix.get('linear_call_boundary_reached')) is bool
          and suffix.get('stop_reason') in ('candidate_anchor','control_transfer','stack_or_memory_barrier','push_cap','decode_or_boundary_gap','bound')
          and isinstance(ps,list) and len(ps)<=24 and (suffix['linear_call_boundary_reached'] or not ps),'suffix uncertainty')
    pushes=c.get('push_candidates');check(isinstance(pushes,list) and len(pushes)==len(ps),'push count');previous=CALL
    for n,(p,old) in enumerate(zip(pushes,ps)):
        at=p.get('site_rva');op=p.get('input',{})
        check(type(at) is int and POST<=at<previous and p.get('conditional_pre_call_esp_offset')==4*n and op.get('width_bytes')==4
              and all(p.get(k)==v for k,v in old.items()) and p.get('actual_value_or_api_parameter_role_proven') is False,'push geometry/value')
        regs=([op['register']] if op.get('kind')=='register' and op.get('register') in ALIASES else [r for r in (op.get('geometry',{}).get('base_register'),op.get('geometry',{}).get('index_register')) if r in ALIASES])
        refs=[{'site_rva':at,'register':r} for r in sorted(set(regs))]
        check(p.get('source_queries')==refs and (all((r['site_rva'],r['register']) in keys for r in refs) or c['inputs']['query_limit_hit']),'push refs');previous=at
    check(type(count) is int and 0<=count<=256 and isinstance(copies,list) and len(copies)==min(count,MAX_COPIES)
          and c.get('copies_truncated') is (count>MAX_COPIES),'copy bounds');previous=POST-1
    for row in copies:
        at=row.get('site_rva');a,b=row.get('destination',{}),row.get('source',{})
        check(type(at) is int and POST<=at<CALL and at>previous and a.get('kind')==b.get('kind')=='register'
              and a.get('register') in ALIASES and b.get('register') in ALIASES and a.get('width_bytes')==b.get('width_bytes')==4
              and a.get('decoder_write') is True and b.get('decoder_read') is True
              and row.get('actual_api_return_or_handle_value_proven') is False and (at,b['register']) in keys,'copy shape')
        q=next(q for q in c['inputs']['queries'] if (q['site_rva'],q['register'])==(at,b['register']))
        check(row.get('opaque_api_token_input_candidate') is opaque_api_source(q),'opaque API capture');previous=at
    h=d.get('helper_memory',{});check(h.get('root_candidate_rva')==HELPER and h.get('all_alias_writes_or_actual_call_effect_proven') is False,'helper scope')
    graph_guard(h.get('graph',{}));keys=input_guard(h.get('inputs',{}),HELPER)
    stores=h.get('store_candidates');count=h.get('store_count')
    check(type(count) is int and 0<=count<=256 and isinstance(stores,list) and len(stores)==min(count,MAX_STORES)
          and h.get('stores_truncated') is (count>MAX_STORES),'store cap');previous=HELPER-1
    for row in stores:
        w=row.get('write',{});at=w.get('site_rva');dst=w.get('destination',{});rhs=w.get('source_operand') or {}
        check(type(at) is int and HELPER<=at<HELPER+768 and at>previous and w.get('mnemonic_class') in WRITE_MNEMONICS
              and dst.get('store_rva')==at and type(dst.get('write_width_bytes')) is int and 1<=dst['write_width_bytes']<=4
              and dst.get('table_or_object_ownership_proven') is False and w.get('expected_global_rva') is None
              and w.get('previous_destination_value_required') is (w['mnemonic_class']!='mov')
              and all(w.get(k) is False for k in ('register_inputs_resolved','executed_write_proven','effective_object_proven','named_caller_effect_admitted'))
              and row.get('caller_value_or_api_handle_binding_proven') is False,'store primitive/effects')
        regs=sorted(set(w.get('address_inputs',[])+w.get('value_input_registers',[]))&set(ALIASES));refs=[{'site_rva':at,'register':r} for r in regs]
        check(row.get('source_and_address_queries')==refs and (all((at,r) in keys for r in regs) or h['inputs']['query_limit_hit']),'store query links');previous=at
    refs=h.get('stack_reference_candidates');count=h.get('stack_reference_count')
    check(type(count) is int and 0<=count<=8*256 and isinstance(refs,list) and len(refs)==min(count,MAX_STACK_REFS)
          and h.get('stack_references_truncated') is (count>MAX_STACK_REFS),'stack ref cap');seen=[]
    for r in refs:
        at,n=r.get('site_rva'),r.get('operand_index');op=r.get('operand',{});geo=op.get('geometry',{})
        check(type(at) is int and HELPER<=at<HELPER+768 and type(n) is int and 0<=n<8 and op.get('kind')=='memory'
              and geo.get('base_register') in ('esp','ebp') and geo.get('segment_register') is None
              and r.get('actual_frame_owner_or_parameter_binding_proven') is False,'stack geometry/owner');seen.append((at,n))
    check(seen==sorted(set(seen)),'stack order')
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
    validate(json.loads(path.read_text()));print('TW10_R31_STRICT_STATIC=PASS; NATIVE_SAVE=OPEN')
if __name__=='__main__':main()
