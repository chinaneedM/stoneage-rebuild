"""Strict R34 provenance gate: candidate inputs do not prove native save."""
import argparse,json
from pathlib import Path
from tools.stoneage_tw10_savedata_native_io_r34 import *
from tools.stoneage_tw10_savedata_native_io_r30_guard import graph_guard
from tools.stoneage_tw10_savedata_native_io_r29_guard import input_guard
from tools.stoneage_tw10_savedata_upstream_r22_guard import FORBIDDEN

def require(ok,where):
    if not ok:raise ValueError('R34 '+where)

def validate(d):
    require(isinstance(d,dict) and d.get('schema')==SCHEMA and d.get('status')==STATUS,'schema')
    require(d.get('runtime_sha256')==RUNTIME_SHA256 and d.get('savedata_sha256')==SAVEDATA_SHA256,'original hashes')
    require(d.get('r33_exact_original_revalidated') is True and d.get('r33_exact_report_sha256')==PRIOR_SHA256
            and d.get('static_only') is True,'exact prior')
    require(d.get('actual_stack_frames_paths_values_or_returns_proven') is False
            and all(d.get(x) is False for x in FLAGS),'runtime promotion')
    graph_guard(d.get('parent_graph',{}))
    rows=d.get('predicate_operands')
    require(isinstance(rows,list) and len(rows)==2,'predicate count')
    for x,at,mnemonic,regs in zip(rows,(CMP,TEST),('cmp','test'),(('esi','edi'),('eax','eax'))):
        require(x.get('site_rva')==at and x.get('mnemonic')==mnemonic and
                x.get('actual_inputs_or_predicate_value_proven') is False,'predicate static shape')
        ops=x.get('operands')
        require(isinstance(ops,list) and len(ops)==2 and all(
                op.get('kind')=='register' and op.get('register')==r
                and op.get('width_bytes')==4 and op.get('decoder_read') is True
                for op,r in zip(ops,regs)),'original full width operands')
    identity=d.get('closehandle_identity',{})
    require(identity.get('call_rva')==CALL and identity.get('kind')=='memory_indirect'
            and identity.get('import_identity')=={'dll':'KERNEL32.dll','name':'CloseHandle','iat_rva':0x520a8}
            and identity.get('import_slot_association_proven') is True
            and identity.get('runtime_target_or_effects_proven') is False,'original CloseHandle identity')
    suffix=d.get('closehandle_pre_call_suffix',{})
    require(suffix.get('linear_call_boundary_reached') is True
            and suffix.get('conditional_pre_call_esp_only') is True
            and suffix.get('abi_roles_applied') is False
            and suffix.get('actual_stack_values_known') is False
            and suffix.get('stop_reason') in ('control_transfer','candidate_anchor',
                  'stack_or_memory_barrier','push_cap'),'caller suffix uncertainty')
    ps=suffix.get('pushes')
    rows=d.get('closehandle_push_candidates')
    require(isinstance(ps,list) and isinstance(rows,list) and len(rows)==len(ps)
            and len(rows)<=MAX_PUSHES,'bounded PUSH candidates')
    keys=input_guard(d.get('register_sources',{}),PARENT)
    require(all(k in keys for k in ((CMP,'esi'),(CMP,'edi'),(TEST,'eax'),(CALL,'esi'),(CALL,'eax'))),'input sites')
    previous=CALL
    for n,(p,old) in enumerate(zip(rows,ps)):
        at=p.get('site_rva')
        op=p.get('input',{})
        require(type(at) is int and ANCHOR<=at<previous
                and p.get('conditional_pre_call_esp_offset')==4*n
                and op.get('width_bytes')==4
                and all(p.get(k)==v for k,v in old.items())
                and p.get('actual_argument_role_or_value_proven') is False,'PUSH slot/value')
        regs=([op['register']] if op.get('kind')=='register' and op.get('register') in ALIASES else
              [r for r in (op.get('geometry',{}).get('base_register'),
                           op.get('geometry',{}).get('index_register')) if r in ALIASES])
        refs=[{'site_rva':at,'register':r} for r in sorted(set(regs))]
        require(p.get('source_queries')==refs and
                (all((at,r) in keys for r in regs) or d['register_sources']['query_limit_hit']),
                'PUSH source queries')
        previous=at
    def no_original(o):
        if isinstance(o,dict):
            require(not(set(o)&FORBIDDEN),'proprietary payload')
            for v in o.values():no_original(v)
        elif isinstance(o,list):
            for v in o:no_original(v)
    no_original(d)
    return True

def main():
    p=argparse.ArgumentParser();p.add_argument('--report',type=Path,required=True)
    args=p.parse_args()
    require(args.report.stat().st_size<=75000,'bounded report')
    validate(json.loads(args.report.read_text()))
    print('TW10_R34_STRICT_STATIC=PASS; NATIVE_SAVE=OPEN')

if __name__=='__main__':main()
