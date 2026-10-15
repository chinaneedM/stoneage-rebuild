"""Savedata read caller, first application consumers and opaque processing entry.

Authenticated static metadata only. Read returns, stack-buffer identity, argument
roles, decoding behavior and savedata schema remain conditional/unknown.
"""
import argparse
import hashlib
import json
import tempfile
from pathlib import Path
from capstone import CS_GRP_CALL, CS_GRP_JUMP
from tools.stoneage_tw10_savedata_native_io_r49 import inspect_verified as inspect_r49, RUNTIME_SHA256, SAVEDATA_SHA256
from tools.stoneage_tw10_savedata_native_io_r49_guard import validate as validate_r49
from tools.stoneage_tw10_savedata_native_io_r41 import queries_for
from tools.stoneage_tw10_savedata_native_io_r42 import branch_context, PRIOR_SHA256 as R41_SHA256
from tools.stoneage_tw10_savedata_native_io_r28 import candidate_graph, input_surface
from tools.stoneage_tw10_savedata_native_io_r30 import graph_meta
from tools.stoneage_tw10_savedata_native_io_r37 import instruction_row, operand_registers
from tools.stoneage_tw10_savedata_native_io_r38 import stack_effect, stack_states, state_summary
from tools.stoneage_tw10_savedata_native_io_r44 import literal_effect
from tools.stoneage_tw10_savedata_upstream_r23 import local_push_suffix
from tools.stoneage_tw10_savedata_frontier_r12 import call_identity
from tools.stoneage_tw10_savedata_entrygraph_r4 import explore
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder, direct_target
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH, SAVEDATA_PATH
from tools.stoneage_tw10_technical_probe import find_rows, extract_row

SCHEMA='tw10-r50-original-savedata-read-caller-application-consumers-processing-entry'
STATUS='PINNED_ORIGINAL_CONDITIONAL_SAVEDATA_CALLER_PROCESSING_CONTEXT_SCHEMA_OPEN'
PRIOR_SHA256='fbb25583fa019e496fd0f4d06ef1b441731547e559dcb818d5244321cc3f0ab6'
ROOT=0x40115
OPEN_CALL=0x4011a
READ_CALL=0x40145
READ_TARGET=0x48660
PROCESS=0x40189
PROCESS_ROOT=0x47160
ADDRESS_SITES=(0x4013e,0x40177,0x4017b)
MAX_CALLER_ROWS=128
MAX_MEMORY_ROWS=64
MAX_DEFS=24
MAX_CALLS=24
MAX_BRANCHES=12
MAX_PROCESS_ROWS=32
FLAGS=('actual_savedata_read_return_bytes_or_input_product_proven','actual_caller_stack_buffer_alias_or_register_preservation_proven',
       'actual_processor_argument_roles_decoding_or_output_length_proven','actual_savedata_record_field_framing_schema_or_checksum_proven',
       'actual_native_persistence_or_cross_version_equivalence_proven','native_io_executed','original_bytes_published')



def inventory_effect(row):
    e={'site_rva':row['site_rva'],'syntax_class':'neutral','esp_delta':0,'operand_width_bytes':None,'conditional_32bit_stack_address_only':True}
    m=row['mnemonic'];ops=row['operands']
    if m in ('call','lcall'):e.update(syntax_class='opaque_call',esp_delta=None)
    elif m in ('push','pop') and len(ops)==1:
        o=ops[0];w=o.get('width_bytes');bad=m=='pop' and o.get('kind')=='register' and o.get('register') in ('esp','sp')
        if w in (2,4) and not bad:e.update(syntax_class=m,esp_delta=w*(-1 if m=='push' else 1),operand_width_bytes=w)
        else:e.update(syntax_class='unknown_esp_write',esp_delta=None)
    elif set(row['decoder_written_registers'])&{'esp','sp','spl'} or m in ('enter','leave'):e.update(syntax_class='unknown_esp_write',esp_delta=None)
    return literal_effect(row,e)


def call_surface(dec,sections,imports,nodes,edges,root,site):
    suffix=local_push_suffix(dec,sections,root,site)
    initial={(p['site_rva'],r) for p in suffix['pushes'] for r in operand_registers(p['input'])}
    initial.update((site,r) for r in ('eax','ecx','edx','esi','edi','ebp'))
    inputs=input_surface(dec,sections,nodes,edges,root,initial)
    defs=sorted({t['rva'] for q in inputs['queries'] if (q['site_rva'],q['register']) in initial for t in q['reaching_candidates'] if t['origin']=='definition'})
    rows=[instruction_row(dec,sections,nodes,a) for a in defs[:MAX_DEFS]]
    inputs=input_surface(dec,sections,nodes,edges,root,initial|queries_for(rows))
    return {'site_rva':site,'identity':call_identity(dec,site,imports,sections),'physical_push_suffix':suffix,'input_sources':inputs,
            'direct_input_definition_count':len(defs),'direct_input_definition_shapes':rows,'direct_input_definitions_truncated':len(defs)>MAX_DEFS,
            'actual_argument_values_roles_return_or_callee_effects_proven':False}


def graph_record(nodes,edges,front,cap):
    return {'graph':graph_meta(nodes,edges,front,cap),'bounded_node_rvas':sorted(nodes),'bounded_edges':[list(e) for e in sorted(edges)]}


def processor_context(dec,sections,imports,entrygraph):
    nodes,edges,front,cap=candidate_graph(dec,PROCESS_ROOT)
    allrows=[instruction_row(dec,sections,nodes,a) for a in sorted(nodes)]
    early=[r for r in allrows if r['site_rva']<PROCESS_ROOT+96 and any(o.get('kind')=='memory' and o.get('geometry',{}).get('base_register') in ('esp','ebp') for o in r['operands'])]
    selected=[r for r in allrows if r['mnemonic'] in ('cmp','test') or any(o.get('kind')=='memory' for o in r['operands'])]
    calls=[call_identity(dec,a,imports,sections) for a,ins in sorted(nodes.items()) if ins.group(CS_GRP_CALL)]
    return {'root_candidate_rva':PROCESS_ROOT,**graph_record(nodes,edges,front,cap),
            'entrygraph_target_boundary_seen':PROCESS_ROOT in entrygraph['visited'],
            'entrygraph_caller_to_target_edge_seen':(PROCESS,PROCESS_ROOT) in entrygraph['edges'],
            'early_frame_shape_count':len(early),'early_frame_shapes':early[:16],'early_frame_shapes_truncated':len(early)>16,
            'early_frame_input_sources':input_surface(dec,sections,nodes,edges,PROCESS_ROOT,queries_for(early[:16])),
            'memory_control_shape_count':len(selected),'memory_control_shapes':selected[:MAX_PROCESS_ROWS],'memory_control_shapes_truncated':len(selected)>MAX_PROCESS_ROWS,
            'memory_control_input_sources':input_surface(dec,sections,nodes,edges,PROCESS_ROOT,queries_for(selected[:MAX_PROCESS_ROWS])),
            'call_count':len(calls),'call_identities':calls[:MAX_CALLS],'calls_truncated':len(calls)>MAX_CALLS,
            'actual_function_abi_decoding_compression_encryption_or_output_proven':False}


def derive(dec,sections,imports,prior49,prior41,entrygraph):
    if prior49.get('schema')!='tw10-r49-original-native-edi-overwrite-temporal-wrapper-division-slots':raise ValueError('R50 R49 prerequisite schema')
    old=next(c for c in prior41['caller_contexts'] if c['filename_push_rva']==ROOT)
    narrow,ne,nf,nc=candidate_graph(dec,ROOT,span=192,cap=128)
    if sorted(narrow)!=old['bounded_node_rvas'] or [list(e) for e in sorted(ne)]!=old['bounded_edges']:raise ValueError('R50 exact R41 narrow graph')
    nodes,edges,front,cap=candidate_graph(dec,ROOT)
    read=call_surface(dec,sections,imports,nodes,edges,ROOT,READ_CALL)
    oldread=next(a for a in old['continuation_calls'] if a['site_rva']==READ_CALL)
    if read['identity']!=oldread['identity'] or read['physical_push_suffix']!=oldread['conditional_linear_push_suffix']:raise ValueError('R50 exact savedata read prefix')
    if read['identity'].get('direct_target_rva')!=READ_TARGET:raise ValueError('R50 savedata read target')
    process=call_surface(dec,sections,imports,nodes,edges,ROOT,PROCESS)
    if process['identity'].get('direct_target_rva')!=PROCESS_ROOT:raise ValueError('R50 processing target')
    allrows=[instruction_row(dec,sections,nodes,a) for a in sorted(nodes)]
    post=[r for r in allrows if READ_CALL+5<=r['site_rva']<PROCESS]
    outputs=[r for r in allrows if PROCESS+5<=r['site_rva']<PROCESS+5+64]
    mem=[r for r in allrows if r['site_rva']>=PROCESS+5 and any(o.get('kind')=='memory' for o in r['operands'])]
    addresses=[instruction_row(dec,sections,nodes,a) for a in ADDRESS_SITES]
    effect_rows=[instruction_row(dec,sections,nodes,a) for a in sorted(nodes)]
    effects=[literal_effect(r,stack_effect(nodes[r['site_rva']],dec.base)) for r in effect_rows]
    states,updates,limit=stack_states(effects,edges,ROOT)
    branches=[a for a,ins in sorted(nodes.items()) if a>=READ_CALL+5 and ins.mnemonic in ('je','jne','jz','jnz')]
    transfers=[{'shape':instruction_row(dec,sections,nodes,a),'direct_target_rva':direct_target(ins,dec.base),'fallthrough_rva':a+ins.size,
                'actual_flags_taken_path_or_loop_count_proven':False} for a,ins in sorted(nodes.items()) if a>=PROCESS+5 and ins.group(CS_GRP_JUMP)]
    calls=[call_identity(dec,a,imports,sections) for a,ins in sorted(nodes.items()) if a>=READ_CALL+5 and ins.group(CS_GRP_CALL)]
    return {'schema':SCHEMA,'status':STATUS,'runtime_sha256':RUNTIME_SHA256,'savedata_sha256':SAVEDATA_SHA256,'static_only':True,
            'r49_exact_original_revalidated':True,'r49_exact_report_sha256':PRIOR_SHA256,'r41_exact_original_caller_revalidated':True,'r41_exact_report_sha256':R41_SHA256,
            'caller_context':{'root_candidate_rva':ROOT,**graph_record(nodes,edges,front,cap),
                'prior_narrow_graph':old['graph'],'prior_narrow_node_rvas':old['bounded_node_rvas'],'prior_narrow_edges':old['bounded_edges'],
                'entrygraph_support':{'root_boundary_seen':ROOT in entrygraph['visited'],'open_boundary_seen':OPEN_CALL in entrygraph['visited'],
                    'read_boundary_seen':READ_CALL in entrygraph['visited'],'wrapper_boundary_seen':READ_TARGET in entrygraph['visited'],
                    'read_to_wrapper_edge_seen':(READ_CALL,READ_TARGET) in entrygraph['edges'],'processing_call_boundary_seen':PROCESS in entrygraph['visited'],
                    'entrygraph_node_limit_hit':entrygraph['limit_hit'],'actual_entry_or_execution_proven':False},
                'read_call_context':read,'post_read_shape_count':len(post),'post_read_shapes':post[:MAX_CALLER_ROWS],'post_read_shapes_truncated':len(post)>MAX_CALLER_ROWS,
                'post_read_input_sources':input_surface(dec,sections,nodes,edges,ROOT,queries_for(post[:MAX_CALLER_ROWS])),
                'processing_call_context':process,'first_output_shape_count':len(outputs),'first_output_shapes':outputs[:MAX_CALLER_ROWS],'first_output_shapes_truncated':len(outputs)>MAX_CALLER_ROWS,
                'first_output_input_sources':input_surface(dec,sections,nodes,edges,ROOT,queries_for(outputs[:MAX_CALLER_ROWS])),
                'post_processing_memory_count':len(mem),'post_processing_memory_shapes':mem[:MAX_MEMORY_ROWS],'post_processing_memory_shapes_truncated':len(mem)>MAX_MEMORY_ROWS,
                'post_processing_memory_input_sources':input_surface(dec,sections,nodes,edges,ROOT,queries_for(mem[:MAX_MEMORY_ROWS])),
                'address_shapes':addresses,'address_input_sources':input_surface(dec,sections,nodes,edges,ROOT,queries_for(addresses)),
                'stack_effect_candidates':effects,'literal_effect_input_shapes':effect_rows,'stack_model_updates':updates,'stack_model_update_limit_hit':limit,
                'address_stack_state_queries':[state_summary(states,a,limit) for a in ADDRESS_SITES],
                'post_read_call_count':len(calls),'post_read_call_identities':calls[:MAX_CALLS],'post_read_calls_truncated':len(calls)>MAX_CALLS,
                'post_read_zf_branch_count':len(branches),'post_read_zf_branch_contexts':[branch_context(dec,sections,nodes,edges,ROOT,a) for a in branches[:MAX_BRANCHES]],'post_read_zf_branches_truncated':len(branches)>MAX_BRANCHES,
                'post_processing_transfer_count':len(transfers),'post_processing_transfers':transfers[:32],'post_processing_transfers_truncated':len(transfers)>32,
                'actual_read_buffer_return_processor_output_or_schema_binding_proven':False},
            'processing_entry_context':processor_context(dec,sections,imports,entrygraph),**{f:False for f in FLAGS}}


def inspect_verified(runtime,savedata):
    prior=inspect_r49(runtime,savedata);validate_r49(prior)
    if hashlib.sha256((json.dumps(prior,sort_keys=True)+'\n').encode()).hexdigest()!=PRIOR_SHA256:raise ValueError('R50 exact R49 derivative changed')
    p41=Path(__file__).resolve().parents[1]/'research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R41-ORIGINAL.json'
    r41=json.loads(p41.read_text())
    if hashlib.sha256((json.dumps(r41,sort_keys=True)+'\n').encode()).hexdigest()!=R41_SHA256:raise ValueError('R50 exact R41 canonical')
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'sa_3.exe';p.write_bytes(runtime);data,pe,base,sections,imports=image_layout(p)
    for s,raw in zip(sections,pe.sections):s['characteristics']=int(raw.Characteristics)
    t=next(s for s in sections if s['name']=='.text');code=data[t['raw']:t['raw']+t['raw_size']]
    graph=explore(code,t['rva'],base,int(pe.OPTIONAL_HEADER.AddressOfEntryPoint))
    return derive(Decoder(code,t['rva'],base),sections,imports,prior,r41,graph)


def main():
    p=argparse.ArgumentParser();p.add_argument('--bin',type=Path,required=True);image,rows,_,_=find_rows(p.parse_args().bin)
    try:
        files={r['path']:r for r in rows if not r['is_dir']}
        with tempfile.TemporaryDirectory() as td:
            exe,save=Path(td)/'sa_3.exe',Path(td)/'savedata.dat'
            extract_row(image,files[RUNTIME_PATH],exe);extract_row(image,files[SAVEDATA_PATH],save)
            r=inspect_verified(exe.read_bytes(),save.read_bytes())
    finally:image.close()
    print(json.dumps(r,sort_keys=True))


if __name__=='__main__':main()
