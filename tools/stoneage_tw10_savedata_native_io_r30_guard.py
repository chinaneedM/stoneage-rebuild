"""R30 bounded conditional composition/caller/store validation; custody separate."""
import argparse,json
from pathlib import Path
from tools.stoneage_tw10_savedata_native_io_r30 import *
from tools.stoneage_tw10_savedata_native_io_r29_guard import shape_guard,input_guard
from tools.stoneage_tw10_savedata_upstream_r22_guard import FORBIDDEN

def check(ok,why):
    if not ok:raise ValueError('R30 '+why)

def graph_guard(g):
    check(g.get('span_bytes')==768 and g.get('node_cap')==256 and type(g.get('nodes')) is int and 1<=g['nodes']<=256
          and type(g.get('edges')) is int and 0<=g['edges']<=512 and type(g.get('node_limit_hit')) is bool
          and isinstance(g.get('frontier'),list) and len(g['frontier'])<=512
          and g.get('actual_entry_path_proven') is False and g.get('returning_call_assumption_only') is True,'graph scope')
    for f in g['frontier']:check(f.get('reason') in ('out_of_window','decode_gap','instruction_span_limit','indirect_jump','node_cap') and type(f.get('rva')) is int,'frontier')

def validate(d):
    check(isinstance(d,dict) and d.get('schema')==SCHEMA and d.get('status')==STATUS,'schema')
    check(d.get('runtime_sha256')==RUNTIME_SHA256 and d.get('savedata_sha256')==SAVEDATA_SHA256,'hash')
    check(d.get('r29_exact_original_revalidated') is True and d.get('r29_exact_report_sha256')==PRIOR_SHA256 and d.get('static_only') is True,'prior')
    check(all(d.get(k) is False for k in FLAGS),'promotion')
    cs=d.get('mask_contexts');check(isinstance(cs,list) and len(cs)==2,'mask count')
    for c,(api,root,site,shift) in zip(cs,MASKS):
        check(c.get('api')==api and c.get('root_candidate_rva')==root and c.get('supported_by_r29_context_and_definition') is True
              and c.get('original_descriptor_value_or_owner_proven') is False,'mask context')
        graph_guard(c.get('graph',{}));shape_guard(c.get('mask_shape',{}),site);shape_guard(c.get('shift_shape',{}),shift)
        check(c.get('mask_model')==scalar_model(c['mask_shape'],'esi'),'mask symbolic model')
        keys=input_guard(c.get('inputs',{}),root);check((site,'esi') in keys and (shift,'esi') in keys,'mask queries')
        source=next(q for q in c['inputs']['queries'] if (q['site_rva'],q['register'])==(shift,'esi'))
        check(c.get('composition')==composition(c['mask_shape'],c['shift_shape'],source),'mask/shift composition')
    dis=d.get('writer_discovery',{});lo=dis.get('text_start_rva');size=dis.get('text_bytes');count=dis.get('caller_count');calls=dis.get('caller_samples');roots=dis.get('selected_root_candidates')
    check(dis.get('scope')=='full_raw_text_direct_CALL_targets_near_writer' and dis.get('writer_rva')==WRITER
          and type(lo) is int and lo>=0 and type(size) is int and 0<size<=1000000
          and dis.get('window_start_rva')==max(lo,WRITER-384) and dis.get('window_end_rva')==WRITER+16
          and type(dis.get('decoded_instructions')) is int and 0<dis['decoded_instructions']<=size
          and type(dis.get('decode_gap_bytes')) is int and 0<=dis['decode_gap_bytes']<=size
          and type(dis.get('writer_is_linear_boundary_candidate')) is bool and type(count) is int and 0<=count<=dis['decoded_instructions']
          and isinstance(calls,list) and len(calls)==min(count,MAX_CALLERS) and dis.get('caller_samples_truncated') is (count>MAX_CALLERS)
          and isinstance(roots,list) and len(roots)<=MAX_ROOTS
          and dis.get('root_selection')=='nearest_earlier_linear_boundary_direct_call_targets_max3'
          and dis.get('complete_indirect_callers_or_real_entries_proven') is False,'discovery bounds')
    last=-1
    for c in calls:
        at,target=c.get('site_rva'),c.get('target_rva')
        check(type(at) is int and lo<=at<lo+size and at>last and type(target) is int and dis['window_start_rva']<=target<dis['window_end_rva']
              and c.get('kind')=='call' and c.get('executed_or_true_entry_proven') is False,'caller primitive');last=at
    previous=WRITER+1
    for r in roots:
        root,caller=r.get('root_rva'),r.get('supporting_call_rva')
        check(type(root) is int and dis['window_start_rva']<=root<=WRITER and root<previous and type(caller) is int and lo<=caller<lo+size
              and r.get('full_linear_scan_boundary_candidate') is True and r.get('actual_entry_proven') is False,'root primitive')
        check(any(c['site_rva']==caller and c['target_rva']==root for c in calls) or dis['caller_samples_truncated'],'root caller support');previous=root
    w=d.get('writer_inputs',{});store=w.get('store_candidate',{});dst=store.get('destination',{});source=store.get('source_operand') or {}
    check(store.get('site_rva')==WRITER and store.get('mnemonic_class')=='mov' and store.get('expected_global_rva')==SHARED
          and store.get('previous_destination_value_required') is False and dst.get('write_width_bytes')==4
          and dst.get('absolute_effective_rva')==SHARED and dst.get('displacement_region',{}).get('displacement_rva')==SHARED
          and all(dst.get(k) is None for k in ('base_register','index_register'))
          and dst.get('table_or_object_ownership_proven') is False
          and all(store.get(k) is False for k in ('register_inputs_resolved','executed_write_proven','effective_object_proven','named_caller_effect_admitted')),'writer shape/effect')
    regs=w.get('source_query_registers');expected=[r for r in store.get('value_input_registers',[]) if r in ALIASES]
    check(isinstance(regs,list) and regs==expected and len(regs)<=7 and source.get('width_bytes')==4
          and w.get('qualified_actual_writer_execution_or_callee_return_proven') is False,'writer query scope')
    contexts=w.get('contexts');check(isinstance(contexts,list) and len(contexts)==len(roots),'writer root contexts')
    for c,r in zip(contexts,roots):
        root=r['root_rva'];identity=c.get('caller_identity',{})
        check(c.get('root_candidate_rva')==root and identity.get('call_rva')==r['supporting_call_rva'] and identity.get('kind')=='direct'
              and identity.get('direct_target_rva')==root and identity.get('runtime_target_or_effects_proven') is False
              and type(c.get('writer_site_in_candidate_graph')) is bool and c.get('actual_store_value_owner_or_initialization_proven') is False,'writer context identity')
        graph_guard(c.get('graph',{}));keys=input_guard(c.get('inputs',{}),root)
        check(all((WRITER,r) in keys for r in regs) or c['inputs']['query_limit_hit'],'missing writer query')
        if not c['writer_site_in_candidate_graph']:
            check(all(not q['site_in_candidate_graph'] and not q['reaching_candidates'] for q in c['inputs']['queries'] if q['site_rva']==WRITER),'unreachable source')
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
    validate(json.loads(path.read_text()));print('TW10_R30_STRICT_STATIC=PASS; NATIVE_SAVE=OPEN')
if __name__=='__main__':main()
