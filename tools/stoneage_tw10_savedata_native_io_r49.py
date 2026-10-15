"""Native EDI overwrite and temporal wrapper division slots; static metadata only."""
import argparse
import hashlib
import json
import tempfile
from pathlib import Path
from tools.stoneage_tw10_savedata_native_io_r48 import (
    inspect_verified as inspect_r48, READ_ROOT, READ_API, WRAPPER, NATIVE_CALL, RETURN_LOAD,
    memory_audit, RUNTIME_SHA256, SAVEDATA_SHA256)
from tools.stoneage_tw10_savedata_native_io_r48_guard import validate as validate_r48
from tools.stoneage_tw10_savedata_native_io_r44 import unique_definition
from tools.stoneage_tw10_savedata_native_io_r37 import instruction_row
from tools.stoneage_tw10_savedata_native_io_r41 import queries_for
from tools.stoneage_tw10_savedata_native_io_r42 import branch_context
from tools.stoneage_tw10_savedata_native_io_r45 import path_without
from tools.stoneage_tw10_savedata_native_io_r28 import candidate_graph, input_surface
from tools.stoneage_tw10_savedata_native_io_r30 import graph_meta
from tools.stoneage_tw10_savedata_frontier_r12 import call_identity
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH, SAVEDATA_PATH
from tools.stoneage_tw10_technical_probe import find_rows, extract_row

SCHEMA='tw10-r49-original-native-edi-overwrite-temporal-wrapper-division-slots'
STATUS='PINNED_ORIGINAL_CONDITIONAL_OVERWRITE_DIVISION_SLOT_SOURCES_SAVE_OPEN'
PRIOR_SHA256='f92a652b446a5433fa1afaa5708112c91bd39c1ef2c4fff27e69a419f013ccfa'
OVERWRITE=0x4aab1
BYPASS=0x4a9b6
DIVS=(0x486e4,0x48743)
SEEDS=(0x48667,0x4866a,0x48671,0x48678,0x4871d,0x4873c,0x48740)
MAX_DEFS=24
SOURCE_ROUNDS=2
MAX_FRAME_ROWS=32
MAX_AUDIT=512
FLAGS=('actual_native_edi_or_local_overwrite_count_proven','actual_temporal_slot_contents_abi_or_memory_alias_proven',
       'actual_dividend_divisor_product_or_quotient_evaluated','actual_original_byte_text_or_crt_owner_role_proven',
       'actual_savedata_schema_or_persistence_proven','native_io_executed','original_bytes_published')


def sources(dec,sections,nodes,edges,root,rows):
    qs=queries_for(rows);shapes={}
    for _ in range(SOURCE_ROUNDS):
        inputs=input_surface(dec,sections,nodes,edges,root,qs)
        sites=sorted({t['rva'] for q in inputs['queries'] for t in q['reaching_candidates'] if t['origin']=='definition'})
        for a in sites[:MAX_DEFS]:shapes[a]=instruction_row(dec,sections,nodes,a)
        qs.update(queries_for(list(shapes.values())))
    inputs=input_surface(dec,sections,nodes,edges,root,qs)
    sites=sorted({t['rva'] for q in inputs['queries'] for t in q['reaching_candidates'] if t['origin']=='definition'})
    return {'input_sources':inputs,'source_definition_count':len(sites),'source_definition_shapes':[shapes[a] for a in sites[:MAX_DEFS] if a in shapes],
            'source_definitions_truncated':len(sites)>MAX_DEFS,'source_expansion_rounds':SOURCE_ROUNDS,
            'source_expansion_pending_definition_rvas':[a for a in sites if a not in shapes]}


def overwrite_link(row,surface):
    ops=row['operands'];at=unique_definition(surface['input_sources'],OVERWRITE,'edi')
    definition=next((r for r in surface['source_definition_shapes'] if r['site_rva']==at),None)
    shape=bool(row['mnemonic']=='mov' and len(ops)==2 and ops[0].get('kind')=='memory' and ops[0].get('width_bytes')==4
               and ops[0].get('geometry',{}).get('base_register')=='ebp' and ops[0]['geometry'].get('relative_field_offset')==-8 and ops[0]['geometry'].get('index_register') is None and ops[0]['geometry'].get('segment_register') is None
               and ops[1].get('kind')=='register' and ops[1].get('register')=='edi' and ops[1].get('width_bytes')==4)
    return {'qualified_four_byte_edi_to_local_slot_syntax_candidate':shape,'unique_edi_definition_rva':at,'unique_edi_definition_shape':definition,
            'actual_edi_byte_count_conversion_alias_or_overwrite_value_proven':False}


def slot_refs(rows,offset):
    result=[]
    for r in rows:
        for i,o in enumerate(r['operands']):
            g=o.get('geometry') or {}
            if o.get('kind')=='memory' and g.get('base_register')=='ebp' and g.get('index_register') is None and g.get('segment_register') is None and g.get('relative_field_offset')==offset:
                result.append({'site_rva':r['site_rva'],'operand_index':i,'mnemonic':r['mnemonic'],'frame_offset_spelling':offset,
                               'width_bytes':o['width_bytes'],'decoder_read':o['decoder_read'],'decoder_write':o['decoder_write'],
                               'actual_same_frame_contents_or_parameter_role_proven':False})
    return result


def write_source_links(rows,surface):
    result=[];defs={r['site_rva']:r for r in surface['source_definition_shapes']}
    for r in rows:
        ops=r['operands']
        if r['mnemonic']!='mov' or len(ops)!=2 or not any(x['operand_index']==0 and x['decoder_write'] for x in slot_refs([r],20)):continue
        reg=ops[1].get('register') if ops[1].get('kind')=='register' else None
        source=unique_definition(surface['input_sources'],r['site_rva'],reg) if reg else None
        sr=defs.get(source,{});so=sr.get('operands',[])
        field=bool(sr.get('mnemonic')=='mov' and len(so)==2 and so[1].get('kind')=='memory' and so[1].get('width_bytes')==4
                   and so[1].get('geometry',{}).get('base_register')=='esi' and so[1]['geometry'].get('relative_field_offset')==24
                   and so[1]['geometry'].get('index_register') is None)
        result.append({'write_site_rva':r['site_rva'],'source_register':reg,'unique_register_definition_rva':source,
                       'unique_definition_has_esi_plus24_load_spelling_candidate':field,
                       'actual_stream_buffer_capacity_owner_value_or_slot_binding_proven':False})
    return result


def native_context(dec,sections,prior):
    nodes,edges,front,cap=candidate_graph(dec,READ_ROOT);old=prior['native_count_return_context']
    if sorted(nodes)!=old['bounded_node_rvas'] or [list(e) for e in sorted(edges)]!=old['bounded_edges']:raise ValueError('R49 R48 native graph')
    row=instruction_row(dec,sections,nodes,OVERWRITE)
    if row!=next(r for r in old['return_memory_predecessor_shapes'] if r['site_rva']==OVERWRITE):raise ValueError('R49 R48 overwrite shape')
    surface=sources(dec,sections,nodes,edges,READ_ROOT,[row])
    audit=memory_audit({a:instruction_row(dec,sections,nodes,a) for a in nodes},edges,READ_ROOT,OVERWRITE,row['operands'][0])
    ar=[instruction_row(dec,sections,nodes,a) for a in audit['visited_predecessor_rvas']]
    audit_inputs=input_surface(dec,sections,nodes,edges,READ_ROOT,queries_for(ar+[row]))
    b=branch_context(dec,sections,nodes,edges,READ_ROOT,BYPASS)
    return {'root_candidate_rva':READ_ROOT,'graph':graph_meta(nodes,edges,front,cap),'bounded_node_rvas':sorted(nodes),'bounded_edges':[list(e) for e in sorted(edges)],
            'overwrite_shape':row,'edi_source_surface':surface,'conditional_overwrite_link':overwrite_link(row,surface),
            'pre_overwrite_memory_shapes':ar,'pre_overwrite_memory_audit':audit,'pre_overwrite_input_sources':audit_inputs,
            'bypass_branch_context':b,
            'branch_target_to_return_avoiding_overwrite_candidate':path_without(edges,b['direct_target_rva'],RETURN_LOAD,OVERWRITE),
            'branch_fallthrough_to_overwrite_candidate':path_without(edges,b['fallthrough_rva'],OVERWRITE),
            'overwrite_to_return_load_candidate':path_without(edges,OVERWRITE,RETURN_LOAD),
            'actual_native_count_or_overwrite_execution_proven':False}


def wrapper_context(dec,sections,imports,prior):
    nodes,edges,front,cap=candidate_graph(dec,WRAPPER);old=prior['wrapper_loop_division_context']
    identity=call_identity(dec,NATIVE_CALL,imports,sections)
    if sorted(nodes)!=old['bounded_node_rvas'] or [list(e) for e in sorted(edges)]!=old['bounded_edges'] or identity!=old['native_call_identity']:raise ValueError('R49 R48 wrapper graph/caller')
    allrows=[instruction_row(dec,sections,nodes,a) for a in sorted(nodes)]
    sites=sorted({r['site_rva'] for r in allrows if slot_refs([r],20)})
    frames=[instruction_row(dec,sections,nodes,a) for a in sites[:MAX_FRAME_ROWS]]
    seeds=[instruction_row(dec,sections,nodes,a) for a in SEEDS]
    divs=[instruction_row(dec,sections,nodes,a) for a in DIVS]
    if divs!=old['division_shapes']:raise ValueError('R49 R48 division shapes')
    surface=sources(dec,sections,nodes,edges,WRAPPER,frames+seeds+divs)
    audits=[]
    for d in divs:
        a=memory_audit({r['site_rva']:r for r in allrows},edges,WRAPPER,d['site_rva'],d['operands'][0])
        rs=[instruction_row(dec,sections,nodes,at) for at in a['visited_predecessor_rvas']]
        audits.append({'division_site_rva':d['site_rva'],'audit':a,'predecessor_shapes':rs,
                       'input_sources':input_surface(dec,sections,nodes,edges,WRAPPER,queries_for(rs+[d]))})
    return {'root_candidate_rva':WRAPPER,'graph':graph_meta(nodes,edges,front,cap),'bounded_node_rvas':sorted(nodes),'bounded_edges':[list(e) for e in sorted(edges)],
            'native_call_identity':identity,'frame_plus20_instruction_count':len(sites),'frame_plus20_shapes':frames,'frame_plus20_shapes_truncated':len(sites)>MAX_FRAME_ROWS,
            'frame_plus20_reference_candidates':slot_refs(frames,20),'product_remaining_numerator_shapes':seeds,'division_shapes':divs,
            'temporal_source_surface':surface,'frame_plus20_write_source_links':write_source_links(frames,surface),
            'division_memory_boundary_audits':audits,'actual_product_slot_dividend_divisor_or_quotient_proven':False}


def derive(dec,sections,imports,prior):
    if prior.get('schema')!='tw10-r48-original-native-count-return-barriers-wrapper-loop-division':raise ValueError('R49 prerequisite schema')
    return {'schema':SCHEMA,'status':STATUS,'runtime_sha256':RUNTIME_SHA256,'savedata_sha256':SAVEDATA_SHA256,
            'r48_exact_original_revalidated':True,'r48_exact_report_sha256':PRIOR_SHA256,'static_only':True,
            'native_overwrite_context':native_context(dec,sections,prior),'wrapper_temporal_slot_context':wrapper_context(dec,sections,imports,prior),**{f:False for f in FLAGS}}


def inspect_verified(runtime,savedata):
    prior=inspect_r48(runtime,savedata);validate_r48(prior)
    if hashlib.sha256((json.dumps(prior,sort_keys=True)+'\n').encode()).hexdigest()!=PRIOR_SHA256:raise ValueError('R49 exact R48 report changed')
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
