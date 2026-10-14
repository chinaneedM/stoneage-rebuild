"""Bounded native return/count syntax and wrapper loop, with memory barriers.

Nonexecuting metadata. Matching frame spellings never prove addresses/contents;
unknown CALL returns and alias/frame effects remain explicit.
"""
import argparse
import hashlib
import json
import tempfile
from collections import deque
from pathlib import Path
from tools.stoneage_tw10_savedata_native_io_r47 import inspect_verified as inspect_r47, READ_ROOT, READ_API, WRAPPER, NATIVE_CALL, RUNTIME_SHA256, SAVEDATA_SHA256
from tools.stoneage_tw10_savedata_native_io_r47_guard import validate as validate_r47
from tools.stoneage_tw10_savedata_native_io_r44 import unique_definition
from tools.stoneage_tw10_savedata_native_io_r37 import instruction_row
from tools.stoneage_tw10_savedata_native_io_r41 import queries_for
from tools.stoneage_tw10_savedata_native_io_r40 import geometry_key
from tools.stoneage_tw10_savedata_native_io_r42 import branch_context
from tools.stoneage_tw10_savedata_native_io_r45 import path_without
from tools.stoneage_tw10_savedata_native_io_r28 import candidate_graph, input_surface
from tools.stoneage_tw10_savedata_native_io_r30 import graph_meta
from tools.stoneage_tw10_savedata_frontier_r12 import call_identity
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH, SAVEDATA_PATH
from tools.stoneage_tw10_technical_probe import find_rows, extract_row

SCHEMA='tw10-r48-original-native-count-return-barriers-wrapper-loop-division'
STATUS='PINNED_ORIGINAL_CONDITIONAL_COUNT_RETURN_LOOP_SYNTAX_SAVE_OPEN'
PRIOR_SHA256='939d7080b61c2e8b3dc873cf0adec45ffc6b2c6154877aee787af6ab03dcf781'
COUNT_LOAD=0x4a9a6
ACCUM=0x4a9a9
RETURN_LOAD=0x4aab4
CONSUMERS=(0x486f8,0x486fc,0x48701,0x48704)
BRANCHES=(0x486fa,0x486ff)
MAX_AUDIT=512
MAX_RETURN_ROWS=8
MAX_DEFS=24
MAX_WRAPPER_ROWS=64
MAX_DIVISIONS=8
SAFE_NEUTRAL={'mov','movzx','movsx','lea','add','sub','and','or','xor','cmp','test','inc','dec','neg','not','imul','mul','div','idiv','shl','shr','sar','sal','cdq','cwd','nop','jmp','je','jne','jz','jnz','ja','jae','jb','jbe','jg','jge','jl','jle','jns','js','jo','jno','jp','jnp','ret','retf','pop'}
FLAGS=('actual_native_api_result_count_or_total_return_proven','actual_frame_alias_contents_or_preservation_proven',
       'actual_wrapper_read_loop_or_element_division_result_proven','actual_byte_text_eof_crt_or_owner_role_proven',
       'actual_savedata_schema_or_persistence_proven','native_io_executed','original_bytes_published')


def memory_boundary(row,reference):
    """Conservative predecessor stop classification, syntax only."""
    if row['mnemonic'] in ('call','lcall'):return 'opaque_call'
    if set(row['decoder_written_registers'])&{'ebp','bp','bpl'}:return 'frame_register_write'
    if row['mnemonic']=='push':return 'implicit_stack_write_alias_unknown'
    for op in row['operands']:
        if op.get('kind')!='memory' or not op.get('decoder_write'):continue
        if geometry_key(op)==geometry_key(reference):
            return 'same_frame_spelling_write' if op['width_bytes']==reference['width_bytes'] else 'overlapping_frame_spelling_write'
        # Even a different frame offset is not disjoint after unknown frame effects.
        return 'explicit_memory_write_alias_unknown'
    if row['mnemonic'] not in SAFE_NEUTRAL:return 'unmodeled_instruction_effect'
    return None


def memory_audit(rows,edges,root,read_site,reference,limit=MAX_AUDIT):
    pred={}
    for a,b in edges:pred.setdefault(b,set()).add(a)
    queue=deque(sorted(pred.get(read_site,())));seen=set();ends=set()
    while queue and len(seen)<limit:
        at=queue.popleft()
        if at in seen:continue
        seen.add(at);row=rows.get(at)
        kind=memory_boundary(row,reference) if row else 'missing_shape'
        if kind:ends.add((at,kind));continue
        ps=pred.get(at,set())
        if at==root or not ps:ends.add((at,'entry_or_disconnected'));continue
        for a in sorted(ps-seen):queue.append(a)
    return {'read_site_rva':read_site,'visited_predecessor_rvas':sorted(seen),'predecessor_limit':limit,'predecessor_limit_hit':bool(queue),
            'terminal_candidates':[{'site_rva':a,'kind':k} for a,k in sorted(ends)],
            'same_frame_spelling_write_candidate_sites':[a for a,k in sorted(ends) if k=='same_frame_spelling_write'],
            'actual_same_address_contents_alias_or_return_count_proven':False}


def count_relation(rows,inputs,edges):
    by={r['site_rva']:r for r in rows};a,b,c=[by[s] for s in (COUNT_LOAD,ACCUM,RETURN_LOAD)];ao,bo,co=[r['operands'] for r in (a,b,c)]
    def reg(o,n):return o.get('kind')=='register' and o.get('register')==n and o.get('width_bytes')==4
    def frame(o,off):
        g=o.get('geometry') or {}
        return o.get('kind')=='memory' and o.get('width_bytes')==4 and g.get('base_register')=='ebp' and g.get('relative_field_offset')==off and g.get('index_register') is None and g.get('segment_register') is None
    shape=bool(a['mnemonic']=='mov' and len(ao)==2 and reg(ao[0],'edx') and frame(ao[1],-12)
               and b['mnemonic']=='add' and len(bo)==2 and frame(bo[0],-8) and reg(bo[1],'edx')
               and c['mnemonic']=='mov' and len(co)==2 and reg(co[0],'eax') and frame(co[1],-8))
    first=unique_definition(inputs,ACCUM,'edx');fa=unique_definition(inputs,ACCUM,'ebp');fb=unique_definition(inputs,RETURN_LOAD,'ebp')
    return {'load_add_return_frame_spelling_syntax_candidate':shape,'add_edx_unique_source_is_count_load_candidate':first==COUNT_LOAD,
            'same_unique_graph_local_ebp_source_candidate':fa is not None and fa==fb,
            'accumulation_to_return_load_structural_path_candidate':path_without(edges,ACCUM,RETURN_LOAD),
            'root_to_return_load_bypassing_accumulation_candidate':path_without(edges,READ_ROOT,RETURN_LOAD,ACCUM),
            'actual_transferred_prefix_total_or_return_count_evaluated':False}


def return_surface(dec,sections,nodes,edges,root):
    sites=[at for at,ins in sorted(nodes.items()) if ins.mnemonic in ('ret','retf')]
    returns=[instruction_row(dec,sections,nodes,at) for at in sites[:MAX_RETURN_ROWS]]
    queries={(at,r) for at in sites[:MAX_RETURN_ROWS] for r in ('eax','ebp')}
    inputs=input_surface(dec,sections,nodes,edges,root,queries)
    defs=sorted({t['rva'] for q in inputs['queries'] for t in q['reaching_candidates'] if t['origin']=='definition'})
    rows=[instruction_row(dec,sections,nodes,at) for at in defs[:MAX_DEFS]]
    inputs=input_surface(dec,sections,nodes,edges,root,queries|queries_for(rows+returns))
    return {'return_count':len(sites),'return_shapes':returns,'returns_truncated':len(sites)>MAX_RETURN_ROWS,
            'direct_return_definition_count':len(defs),'direct_return_definition_shapes':rows,'return_definitions_truncated':len(defs)>MAX_DEFS,
            'input_sources':inputs,'actual_return_values_abi_or_return_effects_proven':False}


def native_context(dec,sections,prior):
    nodes,edges,front,cap=candidate_graph(dec,READ_ROOT);old=prior['read_byte_result_context']
    if sorted(nodes)!=old['bounded_node_rvas'] or [list(e) for e in sorted(edges)]!=old['bounded_edges']:raise ValueError('R48 R47 read graph changed')
    rows=[instruction_row(dec,sections,nodes,s) for s in (COUNT_LOAD,ACCUM,RETURN_LOAD)]
    if rows!=[next(r for r in old['frame_reference_shapes'] if r['site_rva']==s) for s in (COUNT_LOAD,ACCUM,RETURN_LOAD)]:raise ValueError('R48 R47 frame result shapes changed')
    allrows={a:instruction_row(dec,sections,nodes,a) for a in nodes}
    audit=memory_audit(allrows,edges,READ_ROOT,RETURN_LOAD,rows[-1]['operands'][1])
    audit_rows=[allrows[a] for a in audit['visited_predecessor_rvas']]
    inputs=input_surface(dec,sections,nodes,edges,READ_ROOT,queries_for(rows+audit_rows))
    return {'root_candidate_rva':READ_ROOT,'graph':graph_meta(nodes,edges,front,cap),'bounded_node_rvas':sorted(nodes),'bounded_edges':[list(e) for e in sorted(edges)],
            'count_shapes':rows,'return_memory_predecessor_shapes':audit_rows,'return_memory_boundary_audit':audit,'input_sources':inputs,
            'conditional_count_relation':count_relation(rows,inputs,edges),'return_surface':return_surface(dec,sections,nodes,edges,READ_ROOT),
            'actual_native_api_bytes_or_aggregate_return_proven':False}


def consumer_relation(rows,inputs,edges):
    by={r['site_rva']:r for r in rows};sub,add=by[CONSUMERS[2]],by[CONSUMERS[3]];so,ao=sub['operands'],add['operands']
    shape=bool(sub['mnemonic']=='sub' and len(so)==2 and so[0].get('kind')=='memory' and so[0].get('width_bytes')==4
               and so[0].get('geometry',{}).get('base_register')=='ebp' and so[0]['geometry'].get('relative_field_offset')==8
               and so[1].get('register')=='eax' and so[1].get('width_bytes')==4
               and add['mnemonic']=='add' and len(ao)==2 and ao[0].get('register')=='ebx' and ao[1].get('register')=='eax'
               and ao[0].get('width_bytes')==ao[1].get('width_bytes')==4)
    origins=[]
    for site in CONSUMERS:
        q=next((q for q in inputs['queries'] if q['site_rva']==site and q['register']=='eax'),{})
        ts=q.get('reaching_candidates',[])
        origins.append(bool(not inputs['query_limit_hit'] and q.get('site_in_candidate_graph') is True and q.get('candidates_truncated') is False
                            and len(ts)==1 and ts[0]['origin']=='unknown_call' and ts[0]['rva']==NATIVE_CALL))
    return {'remaining_slot_subtract_and_buffer_advance_syntax_candidate':shape,
            'four_consumers_have_only_opaque_native_call_eax_origin_candidate':all(origins),
            'subtract_to_native_call_structural_loop_candidate':path_without(edges,CONSUMERS[2],NATIVE_CALL),
            'buffer_advance_to_native_call_structural_loop_candidate':path_without(edges,CONSUMERS[3],NATIVE_CALL),
            'actual_native_return_bytes_element_count_or_iteration_proven':False}



def division_links(rows,definitions,inputs):
    by={r['site_rva']:r for r in definitions};result=[]
    for r in rows:
        op=r['operands'][0] if len(r['operands'])==1 else {};g=op.get('geometry') or {}
        eax=unique_definition(inputs,r['site_rva'],'eax');edx=unique_definition(inputs,r['site_rva'],'edx')
        z=by.get(edx,{});zo=z.get('operands',[])
        zero=bool(z.get('mnemonic')=='xor' and len(zo)==2 and all(o.get('kind')=='register' and o.get('register')=='edx' and o.get('width_bytes')==4 for o in zo))
        qualified=bool(r['mnemonic'] in ('div','idiv') and op.get('width_bytes')==4)
        frame=bool(op.get('kind')=='memory' and g.get('base_register')=='ebp' and g.get('index_register') is None and g.get('segment_register') is None)
        result.append({'site_rva':r['site_rva'],'qualified_32bit_divisor_64bit_edx_eax_dividend_syntax_candidate':qualified,
                       'signed_division_syntax':r['mnemonic']=='idiv','divisor_frame_offset_spelling':g.get('relative_field_offset') if frame else None,
                       'unique_eax_input_definition_rva':eax,'unique_edx_input_definition_rva':edx,
                       'edx_input_is_four_byte_self_xor_syntax_candidate':zero,
                       'actual_dividend_divisor_quotient_remainder_or_element_count_proven':False})
    return result


def wrapper_context(dec,sections,imports,prior):
    nodes,edges,front,cap=candidate_graph(dec,WRAPPER);old=prior['savedata_wrapper_return_context'];ident=call_identity(dec,NATIVE_CALL,imports,sections)
    if ident!=old['native_call_identity'] or sorted(nodes)!=old['bounded_node_rvas'] or [list(e) for e in sorted(edges)]!=old['bounded_edges']:raise ValueError('R48 exact savedata wrapper graph/caller')
    sites=[a for a in sorted(nodes) if a>=NATIVE_CALL+5];rows=[instruction_row(dec,sections,nodes,a) for a in sites[:MAX_WRAPPER_ROWS]]
    inputs=input_surface(dec,sections,nodes,edges,WRAPPER,queries_for(rows))
    divisions=[a for a,ins in sorted(nodes.items()) if ins.mnemonic in ('div','idiv')]
    divrows=[instruction_row(dec,sections,nodes,a) for a in divisions[:MAX_DIVISIONS]]
    division_queries=queries_for(divrows)
    division_inputs=input_surface(dec,sections,nodes,edges,WRAPPER,division_queries)
    division_defs=sorted({t['rva'] for q in division_inputs['queries'] if (q['site_rva'],q['register']) in division_queries for t in q['reaching_candidates'] if t['origin']=='definition'})
    definition_rows=[instruction_row(dec,sections,nodes,a) for a in division_defs[:MAX_DEFS]]
    division_inputs=input_surface(dec,sections,nodes,edges,WRAPPER,division_queries|queries_for(definition_rows))
    return {'root_candidate_rva':WRAPPER,'graph':graph_meta(nodes,edges,front,cap),'bounded_node_rvas':sorted(nodes),'bounded_edges':[list(e) for e in sorted(edges)],
            'native_call_identity':ident,'post_native_shape_count':len(sites),'post_native_shapes':rows,'post_native_shapes_truncated':len(sites)>MAX_WRAPPER_ROWS,
            'input_sources':inputs,'conditional_consumer_relation':consumer_relation(rows,inputs,edges),
            'native_result_test_branches':[branch_context(dec,sections,nodes,edges,WRAPPER,a) for a in BRANCHES],
            'division_count':len(divisions),'division_shapes':divrows,'divisions_truncated':len(divisions)>MAX_DIVISIONS,'division_input_sources':division_inputs,
            'division_direct_input_definition_count':len(division_defs),'division_direct_input_definition_shapes':definition_rows,
            'division_input_definitions_truncated':len(division_defs)>MAX_DEFS,'conditional_division_input_links':division_links(divrows,definition_rows,division_inputs),
            'return_surface':return_surface(dec,sections,nodes,edges,WRAPPER),
            'actual_wrapper_count_or_division_result_native_binding_proven':False}


def derive(dec,sections,imports,prior):
    if prior.get('schema')!='tw10-r47-original-byte-source-partial-geometry-local-results-wrapper-return':raise ValueError('R48 prerequisite schema')
    return {'schema':SCHEMA,'status':STATUS,'runtime_sha256':RUNTIME_SHA256,'savedata_sha256':SAVEDATA_SHA256,
            'r47_exact_original_revalidated':True,'r47_exact_report_sha256':PRIOR_SHA256,'static_only':True,
            'native_count_return_context':native_context(dec,sections,prior),'wrapper_loop_division_context':wrapper_context(dec,sections,imports,prior),**{f:False for f in FLAGS}}


def inspect_verified(runtime,savedata):
    prior=inspect_r47(runtime,savedata);validate_r47(prior)
    if hashlib.sha256((json.dumps(prior,sort_keys=True)+'\n').encode()).hexdigest()!=PRIOR_SHA256:raise ValueError('R48 exact R47 report changed')
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
