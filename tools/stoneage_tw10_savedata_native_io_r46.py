"""Conditional read adjustment bundles and helper ESP slot syntax; no original execution."""
import argparse
import hashlib
import json
import tempfile
from collections import deque
from pathlib import Path
from capstone.x86 import X86_OP_MEM
from tools.stoneage_tw10_savedata_native_io_r45 import (
    inspect_verified as inspect_r45, READ_ROOT, WRITE_ROOT, DEC, COUNT_PUSH, BARRIER,
    RUNTIME_SHA256, SAVEDATA_SHA256, unique_definition, path_without)
from tools.stoneage_tw10_savedata_native_io_r45_guard import validate as validate_r45
from tools.stoneage_tw10_savedata_native_io_r28 import candidate_graph, input_surface
from tools.stoneage_tw10_savedata_native_io_r30 import graph_meta
from tools.stoneage_tw10_savedata_native_io_r37 import instruction_row, operand_registers, memory_surface
from tools.stoneage_tw10_savedata_native_io_r41 import queries_for
from tools.stoneage_tw10_savedata_native_io_r38 import stack_effect, stack_states, state_summary, slot_bridge
from tools.stoneage_tw10_savedata_upstream_r23 import local_push_suffix
from tools.stoneage_tw10_savedata_frontier_r12 import call_identity
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH, SAVEDATA_PATH
from tools.stoneage_tw10_technical_probe import find_rows, extract_row

SCHEMA='tw10-r46-original-conditional-read-adjustment-bundle-helper-esp-slots'
STATUS='PINNED_ORIGINAL_CONDITIONAL_ADJUSTMENT_PAIRING_HELPER_SLOTS_SAVE_OPEN'
PRIOR_SHA256='77919ef7e23f6a25afc66c2bc54b7b0f7da02df1b618e4a50743cda7ad26c21e'
R37_SHA256='a16c858a46d502dec5c99fe43528601f0bc89449c671a717198725c95aa496d0'
COPY=0x4a926
STORE=0x4a93e
SHIFT=0x4a942
BUFFER_PUSH=0x4a95c
READ_API=0x4a960
BRANCHES=(0x4a932,0x4a939)
HELPER=0x4c761
SEEK_API=0x4c7b0
SEEK_IAT=0x520cc
MARKERS=(DEC,STORE,SHIFT)
MAX_PATH_STATES=4096
MAX_WINDOW_ROWS=32
MAX_HELPER_READS=16
FLAGS=('actual_branch_feasibility_or_read_count_buffer_values_proven',
       'actual_byte_prefix_text_mode_or_pending_byte_role_proven',
       'actual_helper_abi_seek_return_frame_or_owner_effects_proven',
       'actual_savedata_schema_or_persistence_proven','native_io_executed','original_bytes_published')


def signatures(edges,start,goal,markers=MARKERS,limit=MAX_PATH_STATES):
    """Finite graph x seen-marker powerset. Stop at first goal; do not evaluate predicates."""
    adj={}
    for a,b in edges:adj.setdefault(a,set()).add(b)
    bits={at:1<<n for n,at in enumerate(markers)}
    queue=deque([(start,0)]);seen=set();found=set()
    while queue and len(seen)<limit:
        at,mask=queue.popleft();mask|=bits.get(at,0)
        if (at,mask) in seen:continue
        seen.add((at,mask))
        if at==goal:found.add(mask);continue
        for b in sorted(adj.get(at,())):
            if (b,mask|bits.get(b,0)) not in seen:queue.append((b,mask))
    return {'start_rva':start,'stop_at_first_goal_rva':goal,'marker_rvas':list(markers),
            'reachable_seen_marker_masks':sorted(found),'states_examined':len(seen),
            'state_limit':limit,'state_limit_hit':bool(queue),
            'graph_paths_only_actual_feasibility_or_execution_proven':False}


def bundle_relation(rows,inputs,root_paths):
    by={r['site_rva']:r for r in rows};store=by[STORE];shift=by[SHIFT];copy=by[COPY]
    so,sh,co=store['operands'],shift['operands'],copy['operands']
    def reg(o,name,width=4):return o.get('kind')=='register' and o.get('register')==name and o.get('width_bytes')==width
    def mem(o,base,offset,width):
        g=o.get('geometry') or {}
        return (o.get('kind')=='memory' and o.get('width_bytes')==width and g.get('base_register')==base
                and g.get('relative_field_offset')==offset and g.get('index_register') is None and g.get('segment_register') is None)
    store_ok=bool(store['mnemonic']=='mov' and len(so)==2 and mem(so[0],'edi',0,1)
                  and so[0].get('decoder_write') is True and reg(so[1],'al',1))
    shift_ok=bool(shift['mnemonic']=='lea' and len(sh)==2 and reg(sh[0],'ecx') and mem(sh[1],'edi',1,4))
    copy_ok=bool(copy['mnemonic']=='mov' and len(co)==2 and reg(co[0],'ecx') and reg(co[1],'edi'))
    sa=unique_definition(inputs,STORE,'edi');sb=unique_definition(inputs,SHIFT,'edi');sc=unique_definition(inputs,COPY,'edi')
    query=next((q for q in inputs['queries'] if q['site_rva']==BUFFER_PUSH and q['register']=='ecx'),{})
    candidates=query.get('reaching_candidates',[])
    exact_sources=bool(not inputs['query_limit_hit'] and query.get('site_in_candidate_graph') is True
                       and query.get('candidates_truncated') is False and len(candidates)==2
                       and { (t['origin'],t['rva']) for t in candidates }=={('definition',COPY),('definition',SHIFT)})
    masks=root_paths['reachable_seen_marker_masks'];complete=not root_paths['state_limit_hit']
    return {'byte_store_edi_al_syntax_candidate':store_ok,'buffer_plus_one_lea_syntax_candidate':shift_ok,
            'buffer_copy_syntax_candidate':copy_ok,'shared_unique_edi_definition_rva':sa if sa is not None and sa==sb==sc else None,
            'first_api_buffer_push_has_exact_copy_or_plus_one_sources_candidate':exact_sources,
            'decrement_store_plus_one_cooccur_on_all_bounded_first_api_paths_candidate':bool(complete and masks and all(m in (0,7) for m in masks)),
            'both_adjusted_and_bypass_structural_paths_candidate':bool(complete and 0 in masks and 7 in masks),
            'actual_same_buffer_byte_count_text_role_or_execution_proven':False}


def read_context(dec,sections,prior):
    nodes,edges,front,cap=candidate_graph(dec,READ_ROOT)
    old=prior['read_count_context']
    if sorted(nodes)!=old['bounded_node_rvas'] or [list(e) for e in sorted(edges)]!=old['bounded_edges']:raise ValueError('R46 R45 read graph changed')
    sites=[at for at in sorted(nodes) if COPY<=at<READ_API]
    rows=[instruction_row(dec,sections,nodes,at) for at in sites[:MAX_WINDOW_ROWS]]
    inputs=input_surface(dec,sections,nodes,edges,READ_ROOT,queries_for(rows))
    paths=signatures(edges,READ_ROOT,READ_API)
    branches=[]
    for at in BRANCHES:
        b=next((b for b in old['zf_branch_contexts'] if b['branch_site_rva']==at),None)
        if b is None:raise ValueError('R46 bypass branch missing')
        branches.append({'prior_zf_context':b,
            'target_arm_paths':signatures(edges,b['direct_target_rva'],READ_API),
            'fallthrough_arm_paths':signatures(edges,b['fallthrough_rva'],READ_API)})
    return {'root_candidate_rva':READ_ROOT,'graph':graph_meta(nodes,edges,front,cap),
            'bounded_node_rvas':sorted(nodes),'bounded_edges':[list(e) for e in sorted(edges)],
            'window_start_rva':COPY,'window_stop_exclusive_rva':READ_API,'window_shape_count':len(sites),
            'window_shapes':rows,'window_shapes_truncated':len(sites)>MAX_WINDOW_ROWS,'input_sources':inputs,
            'root_first_api_paths':paths,'conditional_adjustment_relation':bundle_relation(rows,inputs,paths),
            'bypass_branch_arms':branches,'prior_count_relationship':old['conditional_count_relationship'],
            'first_read_api_identity':prior['native_api_contexts'][0]['identity'],
            'actual_read_execution_count_buffer_or_contents_proven':False}


def helper_context(dec,sections,imports,prior):
    old=prior['delayed_write_context'];ident=call_identity(dec,BARRIER,imports,sections)
    if ident!=old['barrier_identity'] or ident.get('direct_target_rva')!=HELPER:raise ValueError('R46 exact helper target')
    nodes,edges,front,cap=candidate_graph(dec,HELPER)
    effects=[stack_effect(ins,dec.base) for _,ins in sorted(nodes.items())]
    states,updates,limit=stack_states(effects,edges,HELPER)
    sites=[at for at,ins in sorted(nodes.items()) if at<SEEK_API and ins.mnemonic!='lea'
           and any(o.type==X86_OP_MEM and o.access&1 and ins.reg_name(o.mem.base)=='esp' for o in ins.operands)]
    rows=[instruction_row(dec,sections,nodes,at) for at in sites[:MAX_HELPER_READS]]
    summaries=[state_summary(states,r['site_rva'],limit) for r in rows]
    suffix=local_push_suffix(dec,sections,HELPER,SEEK_API)
    queries=queries_for(rows)|{(p['site_rva'],r) for p in suffix['pushes'] for r in operand_registers(p['input'])}
    queries.update((SEEK_API,r) for r in ('eax','ecx','esi','edi','ebp'))
    inputs=input_surface(dec,sections,nodes,edges,HELPER,queries)
    seek=call_identity(dec,SEEK_API,imports,sections)
    if seek.get('import_identity')!={'dll':'KERNEL32.dll','name':'SetFilePointer','iat_rva':SEEK_IAT}:raise ValueError('R46 exact seek import')
    return {'root_candidate_rva':HELPER,'caller_identity':ident,'prior_caller_suffix':old['barrier_physical_push_suffix'],
            'graph':graph_meta(nodes,edges,front,cap),'bounded_node_rvas':sorted(nodes),'bounded_edges':[list(e) for e in sorted(edges)],
            'stack_effect_candidates':effects,'stack_model_updates':updates,'stack_model_update_limit_hit':limit,
            'pre_seek_esp_read_count':len(sites),'pre_seek_esp_read_shapes':rows,'pre_seek_esp_reads_truncated':len(sites)>MAX_HELPER_READS,
            'stack_state_queries':summaries,'conditional_caller_slot_bridges':[slot_bridge(r,s,old['barrier_physical_push_suffix']['pushes']) for r,s in zip(rows,summaries)],
            'seek_api_identity':seek,'seek_physical_push_suffix':suffix,'input_sources':inputs,
            'r37_helper_surface_rederived':memory_surface(dec,sections,imports,HELPER),
            'root_to_seek_structural_path_candidate':path_without(edges,HELPER,SEEK_API),
            'actual_seek_parameter_values_return_or_caller_frame_preservation_proven':False}


def derive(dec,sections,imports,prior):
    if prior.get('schema')!='tw10-r45-original-optional-count-paths-api-inputs-delayed-write-barrier':raise ValueError('R46 prerequisite schema')
    return {'schema':SCHEMA,'status':STATUS,'runtime_sha256':RUNTIME_SHA256,'savedata_sha256':SAVEDATA_SHA256,
            'r45_exact_original_revalidated':True,'r45_exact_report_sha256':PRIOR_SHA256,
            'r37_exact_helper_surface_revalidated':True,'r37_exact_report_sha256':R37_SHA256,'static_only':True,
            'read_adjustment_context':read_context(dec,sections,prior),'write_helper_context':helper_context(dec,sections,imports,prior),
            **{f:False for f in FLAGS}}


def inspect_verified(runtime,savedata):
    prior=inspect_r45(runtime,savedata);validate_r45(prior)
    if hashlib.sha256((json.dumps(prior,sort_keys=True)+'\n').encode()).hexdigest()!=PRIOR_SHA256:raise ValueError('R46 exact R45 derivative changed')
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'sa_3.exe';p.write_bytes(runtime);data,pe,base,sections,imports=image_layout(p)
    for s,raw in zip(sections,pe.sections):s['characteristics']=int(raw.Characteristics)
    t=next(s for s in sections if s['name']=='.text')
    result=derive(Decoder(data[t['raw']:t['raw']+t['raw_size']],t['rva'],base),sections,imports,prior)
    r37=Path(__file__).resolve().parents[1]/'research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R37-ORIGINAL.json'
    raw=r37.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=R37_SHA256:raise ValueError('R46 R37 canonical custody')
    old=next(c['callee_context'] for c in json.loads(raw)['helper_candidates'] if c['callee_context']['root_candidate_rva']==HELPER)
    if result['write_helper_context']['r37_helper_surface_rederived']!=old:raise ValueError('R46 exact R37 helper surface changed')
    return result


def main():
    p=argparse.ArgumentParser();p.add_argument('--bin',type=Path,required=True)
    image,rows,_,_=find_rows(p.parse_args().bin)
    try:
        files={r['path']:r for r in rows if not r['is_dir']}
        with tempfile.TemporaryDirectory() as td:
            exe,save=Path(td)/'sa_3.exe',Path(td)/'savedata.dat'
            extract_row(image,files[RUNTIME_PATH],exe);extract_row(image,files[SAVEDATA_PATH],save)
            d=inspect_verified(exe.read_bytes(),save.read_bytes())
    finally:image.close()
    print(json.dumps(d,sort_keys=True))


if __name__=='__main__':main()
