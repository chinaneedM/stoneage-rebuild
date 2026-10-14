"""Byte-source slices, local result syntax and savedata-wrapper return boundary.

Static metadata only: partial register/address geometry never evaluates original
bytes, count arithmetic, memory aliasing, ABI or opaque API-return effects.
"""
import argparse
import hashlib
import json
import tempfile
from pathlib import Path
from tools.stoneage_tw10_savedata_native_io_r46 import inspect_verified as inspect_r46, READ_ROOT, READ_API, RUNTIME_SHA256, SAVEDATA_SHA256
from tools.stoneage_tw10_savedata_native_io_r46_guard import validate as validate_r46
from tools.stoneage_tw10_savedata_native_io_r44 import unique_definition
from tools.stoneage_tw10_savedata_native_io_r37 import instruction_row, partial_model
from tools.stoneage_tw10_savedata_native_io_r41 import queries_for
from tools.stoneage_tw10_savedata_native_io_r28 import candidate_graph, input_surface
from tools.stoneage_tw10_savedata_native_io_r30 import graph_meta
from tools.stoneage_tw10_savedata_native_io_r40 import geometry_key
from tools.stoneage_tw10_savedata_native_io_r42 import branch_context
from tools.stoneage_tw10_savedata_frontier_r12 import call_identity
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH, SAVEDATA_PATH
from tools.stoneage_tw10_technical_probe import find_rows, extract_row

SCHEMA='tw10-r47-original-byte-source-partial-geometry-local-results-wrapper-return'
STATUS='PINNED_ORIGINAL_CONDITIONAL_BYTE_LOCAL_RESULT_RETURN_SYNTAX_SAVE_OPEN'
PRIOR_SHA256='9aff27e1dadb33b1df5642e114488b238e83efcb97015a806c9e6527658c560e'
LOAD=0x4a934
STORE=0x4a93e
RELOAD=0x4a940
MARKER=0x4a945
RESET=0x4a94c
INIT=0x4a91b
BYTE_SITES=(INIT,LOAD,STORE,RELOAD,MARKER,RESET)
WRAPPER=0x48660
NATIVE_CALL=0x486f0
TAIL_SPAN=112
WRAPPER_SPAN=40
MAX_SOURCE_ROWS=24
SOURCE_ROUNDS=2
MAX_TAIL_ROWS=48
MAX_FRAME_ROWS=24
MAX_BRANCHES=12
FLAGS=('actual_source_byte_or_same_memory_alias_proven','actual_text_pending_byte_or_reset_role_proven',
       'actual_api_success_transferred_count_or_total_return_proven','actual_frame_abi_or_wrapper_return_binding_proven',
       'actual_savedata_schema_or_persistence_proven','native_io_executed','original_bytes_published')


def byte_relation(rows,sources,inputs):
    by={r['site_rva']:r for r in rows};load,store,reload,reset=[by[a] for a in (LOAD,STORE,RELOAD,RESET)]
    lo,so,ro,zo=[r['operands'] for r in (load,store,reload,reset)]
    def reg(o,n,w):return o.get('kind')=='register' and o.get('register')==n and o.get('width_bytes')==w
    def mem(o,n,off,w,index=None):
        g=o.get('geometry') or {}
        return (o.get('kind')=='memory' and o.get('width_bytes')==w and g.get('base_register')==n and g.get('index_register')==index
                and g.get('relative_field_offset')==off and g.get('segment_register') is None and g.get('index_scale')==1)
    load_ok=bool(load['mnemonic']=='mov' and len(lo)==2 and reg(lo[0],'al',1) and mem(lo[1],'eax',5,1) and lo[1].get('decoder_read') is True)
    store_ok=bool(store['mnemonic']=='mov' and len(so)==2 and mem(so[0],'edi',0,1) and so[0].get('decoder_write') is True and reg(so[1],'al',1))
    reload_ok=bool(reload['mnemonic']=='mov' and len(ro)==2 and reg(ro[0],'eax',4) and mem(ro[1],'ebx',0,4))
    reset_ok=bool(reset['mnemonic']=='mov' and len(zo)==2 and mem(zo[0],'eax',5,1,'esi') and zo[0].get('decoder_write') is True
                  and zo[1].get('kind')=='immediate' and zo[1].get('width_bytes')==1 and zo[1].get('constant')==10)
    before=unique_definition(inputs,LOAD,'eax');at_store=unique_definition(inputs,STORE,'eax');at_reset=unique_definition(inputs,RESET,'eax')
    defs={r['site_rva']:r for r in sources}
    return {'one_byte_eax_plus5_load_syntax_candidate':load_ok,'one_byte_edi_al_store_syntax_candidate':store_ok,
            'partial_register_slice_model':partial_model(load),'pre_load_eax_definition_rva':before,
            'pre_load_eax_definition_shape':defs.get(before),
            'store_al_unique_parent_definition_is_load_candidate':bool(load_ok and store_ok and at_store==LOAD),
            'separate_four_byte_eax_reload_from_ebx_candidate':reload_ok,
            'reset_byte_eax_esi_plus5_literal10_syntax_candidate':reset_ok,
            'reset_eax_unique_definition_is_reload_candidate':bool(reload_ok and reset_ok and at_reset==RELOAD),
            'load_eax_and_reset_eax_distinct_local_definition_candidates':before is not None and at_reset is not None and before!=at_reset,
            'same_displacement5_does_not_establish_alias':True,
            'actual_byte_value_same_address_reset_or_text_role_proven':False}


def source_surface(dec,sections,nodes,edges,rows):
    queries=queries_for(rows);shapes={}
    for _ in range(SOURCE_ROUNDS):
        inputs=input_surface(dec,sections,nodes,edges,READ_ROOT,queries)
        sites=sorted({t['rva'] for q in inputs['queries'] for t in q['reaching_candidates'] if t['origin']=='definition'})
        for at in sites[:MAX_SOURCE_ROWS]:shapes[at]=instruction_row(dec,sections,nodes,at)
        queries.update(queries_for(list(shapes.values())))
    inputs=input_surface(dec,sections,nodes,edges,READ_ROOT,queries)
    sites=sorted({t['rva'] for q in inputs['queries'] for t in q['reaching_candidates'] if t['origin']=='definition'})
    return {'input_sources':inputs,'source_definition_count':len(sites),'source_definition_shapes':[shapes[a] for a in sites[:MAX_SOURCE_ROWS] if a in shapes],
            'source_definition_shape_cap':MAX_SOURCE_ROWS,'source_definitions_truncated':len(sites)>MAX_SOURCE_ROWS,
            'source_expansion_rounds':SOURCE_ROUNDS,'source_expansion_pending_definition_rvas':[a for a in sites if a not in shapes]}


def frame_refs(rows):
    refs=[]
    for row in rows:
        for i,o in enumerate(row['operands']):
            g=o.get('geometry') or {}
            if (o.get('kind')=='memory' and g.get('base_register')=='ebp' and g.get('index_register') is None
                and g.get('segment_register') is None and g.get('relative_field_offset') in (-8,-12)):
                refs.append({'site_rva':row['site_rva'],'operand_index':i,'frame_offset':g['relative_field_offset'],
                             'width_bytes':o['width_bytes'],'address_only_lea_candidate':row['mnemonic']=='lea',
                             'decoder_read':o['decoder_read'],'decoder_write':o['decoder_write'],
                             'actual_same_frame_memory_api_result_or_value_proven':False})
    return refs


def frame_pairs(refs):
    return [{'write_site_rva':w['site_rva'],'read_or_address_site_rva':r['site_rva'],
             'same_frame_offset':w['frame_offset'],'same_width_bytes':w['width_bytes'],
             'write_numerically_before_read_candidate':w['site_rva']<r['site_rva'],
             'actual_frame_alias_contents_preservation_or_api_effect_proven':False}
            for w in refs if w['decoder_write'] and not w['address_only_lea_candidate']
            for r in refs if (r['decoder_read'] or r['address_only_lea_candidate']) and r['site_rva']!=w['site_rva']
            and w['frame_offset']==r['frame_offset'] and w['width_bytes']==r['width_bytes']]


def read_context(dec,sections,imports,prior):
    nodes,edges,front,cap=candidate_graph(dec,READ_ROOT);old=prior['read_adjustment_context']
    if sorted(nodes)!=old['bounded_node_rvas'] or [list(e) for e in sorted(edges)]!=old['bounded_edges']:raise ValueError('R47 exact R46 graph')
    rows=[instruction_row(dec,sections,nodes,at) for at in BYTE_SITES]
    for r in rows:
        if r['site_rva']!=INIT and r!=next(x for x in old['window_shapes'] if x['site_rva']==r['site_rva']):raise ValueError('R47 R46 byte window changed')
    surface=source_surface(dec,sections,nodes,edges,rows)
    tail_sites=[a for a in sorted(nodes) if READ_API+6<=a<READ_API+6+TAIL_SPAN]
    tail=[instruction_row(dec,sections,nodes,a) for a in tail_sites[:MAX_TAIL_ROWS]]
    all_rows=[instruction_row(dec,sections,nodes,a) for a in sorted(nodes)]
    fsites=sorted({r['site_rva'] for r in frame_refs(all_rows)})
    frames=[instruction_row(dec,sections,nodes,a) for a in fsites[:MAX_FRAME_ROWS]]
    frefs=frame_refs(frames)
    # Keep these queries separate from source expansion, so caps remain explicit.
    tail_inputs=input_surface(dec,sections,nodes,edges,READ_ROOT,queries_for(tail+frames))
    branch_sites=[a for a in tail_sites if nodes[a].mnemonic in ('je','jne','jz','jnz')]
    return {'root_candidate_rva':READ_ROOT,'graph':graph_meta(nodes,edges,front,cap),'bounded_node_rvas':sorted(nodes),
            'bounded_edges':[list(e) for e in sorted(edges)],'byte_shapes':rows,'byte_source_surface':surface,
            'conditional_byte_relation':byte_relation(rows,surface['source_definition_shapes'],surface['input_sources']),
            'first_read_api_identity':call_identity(dec,READ_API,imports,sections),
            'post_api_window_start_rva':READ_API+6,'post_api_window_bytes':TAIL_SPAN,'post_api_shape_count':len(tail_sites),
            'post_api_shapes':tail,'post_api_shapes_truncated':len(tail_sites)>MAX_TAIL_ROWS,
            'frame_reference_instruction_count':len(fsites),'frame_reference_shapes':frames,'frame_reference_shapes_truncated':len(fsites)>MAX_FRAME_ROWS,
            'frame_reference_candidates':frefs,'equal_frame_spelling_pairs':frame_pairs(frefs),
            'post_api_and_frame_input_sources':tail_inputs,'post_api_zf_branch_count':len(branch_sites),
            'post_api_zf_branches_truncated':len(branch_sites)>MAX_BRANCHES,
            'post_api_zf_branch_contexts':[branch_context(dec,sections,nodes,edges,READ_ROOT,a) for a in branch_sites[:MAX_BRANCHES]],
            'actual_prefix_marker_api_result_total_count_or_return_value_proven':False}


def wrapper_context(dec,sections,imports):
    nodes,edges,front,cap=candidate_graph(dec,WRAPPER)
    ident=call_identity(dec,NATIVE_CALL,imports,sections)
    if NATIVE_CALL not in nodes or ident.get('direct_target_rva')!=READ_ROOT:raise ValueError('R47 savedata native caller identity')
    sites=[a for a in sorted(nodes) if NATIVE_CALL+5<=a<NATIVE_CALL+5+WRAPPER_SPAN]
    rows=[instruction_row(dec,sections,nodes,a) for a in sites[:MAX_TAIL_ROWS]]
    return {'root_candidate_rva':WRAPPER,'graph':graph_meta(nodes,edges,front,cap),'bounded_node_rvas':sorted(nodes),
            'bounded_edges':[list(e) for e in sorted(edges)],'native_call_identity':ident,'post_call_shape_count':len(sites),
            'post_call_shapes':rows,'post_call_shapes_truncated':len(sites)>MAX_TAIL_ROWS,
            'input_sources':input_surface(dec,sections,nodes,edges,WRAPPER,queries_for(rows)),
            'actual_native_return_value_abi_frame_or_wrapper_count_binding_proven':False}


def derive(dec,sections,imports,prior):
    if prior.get('schema')!='tw10-r46-original-conditional-read-adjustment-bundle-helper-esp-slots':raise ValueError('R47 prerequisite schema')
    return {'schema':SCHEMA,'status':STATUS,'runtime_sha256':RUNTIME_SHA256,'savedata_sha256':SAVEDATA_SHA256,
            'r46_exact_original_revalidated':True,'r46_exact_report_sha256':PRIOR_SHA256,'static_only':True,
            'read_byte_result_context':read_context(dec,sections,imports,prior),
            'savedata_wrapper_return_context':wrapper_context(dec,sections,imports),**{f:False for f in FLAGS}}


def inspect_verified(runtime,savedata):
    prior=inspect_r46(runtime,savedata);validate_r46(prior)
    if hashlib.sha256((json.dumps(prior,sort_keys=True)+'\n').encode()).hexdigest()!=PRIOR_SHA256:raise ValueError('R47 exact R46 report changed')
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'sa_3.exe';p.write_bytes(runtime);data,pe,base,sections,imports=image_layout(p)
    for s,raw in zip(sections,pe.sections):s['characteristics']=int(raw.Characteristics)
    t=next(s for s in sections if s['name']=='.text')
    return derive(Decoder(data[t['raw']:t['raw']+t['raw_size']],t['rva'],base),sections,imports,prior)


def main():
    p=argparse.ArgumentParser();p.add_argument('--bin',type=Path,required=True);image,rows,_,_=find_rows(p.parse_args().bin)
    try:
        files={r['path']:r for r in rows if not r['is_dir']}
        with tempfile.TemporaryDirectory() as td:
            exe,save=Path(td)/'sa_3.exe',Path(td)/'savedata.dat'
            extract_row(image,files[RUNTIME_PATH],exe);extract_row(image,files[SAVEDATA_PATH],save)
            d=inspect_verified(exe.read_bytes(),save.read_bytes())
    finally:image.close()
    print(json.dumps(d,sort_keys=True))


if __name__=='__main__':main()
