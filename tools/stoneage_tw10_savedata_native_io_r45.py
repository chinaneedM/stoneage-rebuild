"""Optional count decrement paths, exact API inputs and delayed write barrier.

Original static metadata only. Graph connectivity is not branch feasibility;
shared frame syntax is not actual memory/ABI/descriptor/count binding.
"""
import argparse
import hashlib
import json
import tempfile
from pathlib import Path
from tools.stoneage_tw10_savedata_native_io_r44 import inspect_verified as inspect_r44, unique_definition, RUNTIME_SHA256, SAVEDATA_SHA256
from tools.stoneage_tw10_savedata_native_io_r44_guard import validate as validate_r44
from tools.stoneage_tw10_savedata_native_io_r42 import branch_context
from tools.stoneage_tw10_savedata_native_io_r28 import candidate_graph, input_surface
from tools.stoneage_tw10_savedata_native_io_r30 import graph_meta
from tools.stoneage_tw10_savedata_native_io_r37 import instruction_row, operand_registers
from tools.stoneage_tw10_savedata_native_io_r41 import queries_for
from tools.stoneage_tw10_savedata_native_io_r40 import geometry_key
from tools.stoneage_tw10_savedata_native_io_r36 import closure
from tools.stoneage_tw10_savedata_upstream_r23 import local_push_suffix
from tools.stoneage_tw10_savedata_frontier_r12 import call_identity
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH, SAVEDATA_PATH
from tools.stoneage_tw10_technical_probe import find_rows, extract_row

SCHEMA='tw10-r45-original-optional-count-paths-api-inputs-delayed-write-barrier'
STATUS='PINNED_ORIGINAL_CONDITIONAL_OPTIONAL_COUNT_API_SOURCES_NATIVE_SAVE_OPEN'
PRIOR_SHA256='52c158d5f28f3ea287432e4b8214d306c491f158820808d7c4dd212c0646f5e8'
READ_ROOT=0x4a8dc
WRITE_ROOT=0x4c5b4
DEC=0x4a93b
COUNT_PUSH=0x4a959
BARRIER=0x4c60d
BUFFER_READ=0x4c623
APIS=(('ReadFile',READ_ROOT,0x4a960,0x4a906,0x520d8),('WriteFile',WRITE_ROOT,0x4c68c,0x4c62c,0x520a4))
MAX_DEFS=24
MAX_BRANCHES=12
FLAGS=('actual_decrement_branch_or_execution_proven','actual_entry_count_or_api_transferred_bytes_proven',
       'actual_api_handle_buffer_argument_values_or_roles_proven','actual_write_frame_preservation_or_callee_effects_proven',
       'actual_savedata_format_schema_or_persistence_proven','native_io_executed','original_bytes_published')


def path_without(edges,start,goal,excluded=None):
    return goal in closure([(a,b) for a,b in edges if a!=excluded and b!=excluded],start) if start!=excluded and goal!=excluded else False


def count_relationship(root,edges,dec,push,inputs):
    a,b=dec['operands'],push['operands']
    da=unique_definition(inputs,dec['site_rva'],'ebp');db=unique_definition(inputs,push['site_rva'],'ebp')
    shape=bool(dec['mnemonic']=='dec' and push['mnemonic']=='push' and len(a)==len(b)==1
               and a[0].get('kind')==b[0].get('kind')=='memory' and a[0].get('width_bytes')==b[0].get('width_bytes')==4
               and a[0].get('decoder_read') is True and a[0].get('decoder_write') is True and b[0].get('decoder_read') is True
               and geometry_key(a[0])==geometry_key(b[0]))
    same=bool(shape and da is not None and da==db)
    reachable=path_without(edges,root,push['site_rva'])
    return {'same_four_byte_count_slot_spelling_candidate':shape,'shared_unique_ebp_definition_rva':da if same else None,
            'same_graph_local_frame_source_candidate':same,
            'root_to_push_structural_path_candidate':reachable,
            'decrement_to_push_structural_path_candidate':path_without(edges,dec['site_rva'],push['site_rva']),
            'root_to_push_path_avoiding_decrement_candidate':path_without(edges,root,push['site_rva'],dec['site_rva']),
            'decrement_on_all_bounded_root_to_push_paths_candidate':reachable and not path_without(edges,root,push['site_rva'],dec['site_rva']),
            'actual_same_address_contents_modified_count_or_taken_path_proven':False,
            'original_count_or_decrement_result_evaluated':False}


def api_context(dec,sections,imports,spec):
    name,root,site,anchor,slot=spec
    nodes,edges,front,cap=candidate_graph(dec,root)
    identity=call_identity(dec,site,imports,sections)
    if site not in nodes or identity.get('import_identity')!={'dll':'KERNEL32.dll','name':name,'iat_rva':slot}:raise ValueError('R45 exact API import identity')
    suffix=local_push_suffix(dec,sections,anchor,site)
    queries={(p['site_rva'],r) for p in suffix['pushes'] for r in operand_registers(p['input'])}
    queries.update((site,r) for r in ('eax','ebx','ecx','esi','edi','ebp'))
    inputs=input_surface(dec,sections,nodes,edges,root,queries)
    defs=sorted({t['rva'] for q in inputs['queries'] if (q['site_rva'],q['register']) in queries
                 for t in q['reaching_candidates'] if t['origin']=='definition'})
    rows=[instruction_row(dec,sections,nodes,at) for at in defs[:MAX_DEFS]]
    inputs=input_surface(dec,sections,nodes,edges,root,queries|queries_for(rows))
    return {'api':name,'root_candidate_rva':root,'site_rva':site,'linear_anchor_rva':anchor,'identity':identity,
            'graph':graph_meta(nodes,edges,front,cap),'bounded_node_rvas':sorted(nodes),
            'physical_push_suffix':suffix,'input_sources':inputs,'direct_definition_count':len(defs),
            'direct_definition_shapes':rows,'direct_definitions_truncated':len(defs)>MAX_DEFS,
            'actual_native_handle_buffer_count_return_or_io_proven':False}


def read_context(dec,sections,prior):
    nodes,edges,front,cap=candidate_graph(dec,READ_ROOT)
    old=next(c for c in prior['native_contexts'] if c['native_root_candidate_rva']==READ_ROOT)
    shapes=[instruction_row(dec,sections,nodes,at) for at in (DEC,COUNT_PUSH)]
    if shapes!=[next(r for r in old['early_frame_read_shapes'] if r['site_rva']==at) for at in (DEC,COUNT_PUSH)]:raise ValueError('R45 exact R44 decrement/push changed')
    inputs=input_surface(dec,sections,nodes,edges,READ_ROOT,queries_for(shapes))
    branches=[at for at,ins in sorted(nodes.items()) if at<APIS[0][2] and ins.mnemonic in ('je','jne','jz','jnz')]
    return {'root_candidate_rva':READ_ROOT,'graph':graph_meta(nodes,edges,front,cap),'bounded_node_rvas':sorted(nodes),
            'bounded_edges':[list(e) for e in sorted(edges)],'decrement_shape':shapes[0],'count_push_shape':shapes[1],
            'count_frame_input_sources':inputs,'conditional_count_relationship':count_relationship(READ_ROOT,edges,*shapes,inputs),
            'prior_count_push_overlapping_write_sites':next(a['overlapping_write_sites'] for a in old['native_prefix_token_audits'] if a['read_site_rva']==COUNT_PUSH),
            'zf_branch_scope':'JE_JNE_before_first_API_only_other_condition_flags_not_qualified',
            'zf_branch_count':len(branches),'zf_branches_truncated':len(branches)>MAX_BRANCHES,
            'zf_branch_contexts':[branch_context(dec,sections,nodes,edges,READ_ROOT,at) for at in branches[:MAX_BRANCHES]],
            'actual_count_transformation_branch_or_schema_proven':False}


def delayed_write_context(dec,sections,imports,prior):
    nodes,edges,front,cap=candidate_graph(dec,WRITE_ROOT)
    old=next(c for c in prior['native_contexts'] if c['native_root_candidate_rva']==WRITE_ROOT)
    read=instruction_row(dec,sections,nodes,BUFFER_READ)
    if read!=next(r for r in old['early_frame_read_shapes'] if r['site_rva']==BUFFER_READ):raise ValueError('R45 exact R44 delayed write read changed')
    identity=call_identity(dec,BARRIER,imports,sections)
    suffix=local_push_suffix(dec,sections,WRITE_ROOT,BARRIER)
    queries=queries_for([read])|{(BARRIER,r) for r in ('eax','ebp','esi')}
    queries.update((p['site_rva'],r) for p in suffix['pushes'] for r in operand_registers(p['input']))
    inputs=input_surface(dec,sections,nodes,edges,WRITE_ROOT,queries)
    return {'root_candidate_rva':WRITE_ROOT,'graph':graph_meta(nodes,edges,front,cap),'bounded_node_rvas':sorted(nodes),
            'bounded_edges':[list(e) for e in sorted(edges)],'barrier_identity':identity,'barrier_physical_push_suffix':suffix,
            'delayed_buffer_read_shape':read,'input_sources':inputs,
            'barrier_to_buffer_read_structural_path_candidate':path_without(edges,BARRIER,BUFFER_READ),
            'same_bound_frame_source_after_call_proven':False,'actual_helper_return_heap_owner_or_frame_preservation_proven':False}


def derive(dec,sections,imports,prior):
    if prior.get('schema')!='tw10-r44-original-native-frame-slots-wrapper-slot-rewrite-source-candidates':raise ValueError('R45 prerequisite schema')
    return {'schema':SCHEMA,'status':STATUS,'runtime_sha256':RUNTIME_SHA256,'savedata_sha256':SAVEDATA_SHA256,
            'r44_exact_original_revalidated':True,'r44_exact_report_sha256':PRIOR_SHA256,'static_only':True,
            'read_count_context':read_context(dec,sections,prior),
            'native_api_contexts':[api_context(dec,sections,imports,spec) for spec in APIS],
            'delayed_write_context':delayed_write_context(dec,sections,imports,prior),**{flag:False for flag in FLAGS}}


def inspect_verified(runtime,savedata):
    prior=inspect_r44(runtime,savedata);validate_r44(prior)
    if hashlib.sha256((json.dumps(prior,sort_keys=True)+'\n').encode()).hexdigest()!=PRIOR_SHA256:raise ValueError('R45 exact R44 derivative changed')
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'sa_3.exe';p.write_bytes(runtime);data,pe,base,sections,imports=image_layout(p)
    for s,raw in zip(sections,pe.sections):s['characteristics']=int(raw.Characteristics)
    t=next(s for s in sections if s['name']=='.text')
    return derive(Decoder(data[t['raw']:t['raw']+t['raw_size']],t['rva'],base),sections,imports,prior)


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
