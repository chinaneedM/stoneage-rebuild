"""R40 nonexecuting read-frame geometry and postcall predicate candidates.

Slot arithmetic is conditional architecture geometry, not ABI/value binding.
Calls kill frame/register knowledge; matching address syntax is not preservation.
"""
import argparse
import hashlib
import json
import tempfile
from pathlib import Path
from capstone.x86 import X86_OP_MEM
from tools.stoneage_tw10_savedata_native_io_r39 import (
    inspect_verified as inspect_r39, derive as derive_r39, READ_ROOT, READ_CALL,
    PARENT, RUNTIME_SHA256, SAVEDATA_SHA256, FLAGS as R39_FLAGS,
)
from tools.stoneage_tw10_savedata_native_io_r39_guard import validate as validate_r39
from tools.stoneage_tw10_savedata_native_io_r38 import stack_effect, stack_states, state_summary
from tools.stoneage_tw10_savedata_native_io_r37 import instruction_row, operand_registers
from tools.stoneage_tw10_savedata_native_io_r33 import bounded_flag_sources, MAX_SOURCE_SAMPLES
from tools.stoneage_tw10_savedata_native_io_r30 import graph_meta
from tools.stoneage_tw10_savedata_native_io_r28 import candidate_graph, input_surface
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder, direct_target
from tools.stoneage_tw10_savedata_frontier_r12 import call_identity
from tools.stoneage_tw10_savedata_upstream_r23 import local_push_suffix
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH, SAVEDATA_PATH
from tools.stoneage_tw10_technical_probe import find_rows, extract_row

SCHEMA='tw10-r40-original-read-frame-slots-postcall-predicate-candidates'
STATUS='PINNED_ORIGINAL_CONDITIONAL_READ_FRAME_ENDCHECK_ROLE_SAVE_OPEN'
PRIOR_SHA256='9e7648bd716b65a3695c1a1b04461d5863474210f083e5a11df6595e8cdbbd44'
APIS=((0x4a960,0x4a906),(0x4aa31,0x4a9d3))
MAX_READS=16
MAX_FRAME_DEFS=16
MAX_BRANCHES=12
FLAGS=tuple(R39_FLAGS)+(
    'read_frame_geometry_establishes_actual_parameter_values',
    'matching_buffer_address_syntax_establishes_preserved_frame_or_memory',
    'endcheck_text_eof_crt_or_savedata_payload_role_proven',
)

def frame_bridge(row, inputs, definitions, summaries, pushes):
    refs=[o for o in row['operands'] if o.get('kind')=='memory' and o.get('decoder_read')]
    ref=refs[0] if len(refs)==1 else {};geo=ref.get('geometry') or {}
    base=geo.get('base_register')
    query=next((q for q in inputs['queries'] if q['site_rva']==row['site_rva'] and q['register']==base),None)
    tokens=query['reaching_candidates'] if query else []
    at=tokens[0]['rva'] if len(tokens)==1 and tokens[0]['origin']=='definition' else None
    definition=next((r for r in definitions if r['site_rva']==at),None)
    ops=definition['operands'] if definition else []
    copy=(base=='ebp' and len(ops)==2 and definition['mnemonic']=='mov'
          and all(o.get('kind')=='register' and o.get('width_bytes')==4 for o in ops)
          and ops[0].get('register')=='ebp' and ops[1].get('register')=='esp')
    summary=next((s for s in summaries if s['site_rva']==at),{})
    delta=summary.get('unique_conditional_esp_delta')
    qualified=(copy and delta is not None and query['site_in_candidate_graph']
               and not query['candidates_truncated'] and not inputs['query_limit_hit']
               and geo.get('index_register') is None and geo.get('segment_register') is None
               and type(geo.get('relative_field_offset')) is int)
    entry=delta+geo['relative_field_offset'] if qualified else None
    caller=entry-4 if entry is not None else None
    # Match a whole four-byte physical slot, not a partial/overrunning access.
    push=next((p for p in pushes if p['conditional_pre_call_esp_offset']==caller
               and p['input'].get('width_bytes')==ref.get('width_bytes')==4),None)
    return {'read_site_rva':row['site_rva'],'frame_definition_candidate_rva':at,
            'unique_mov_ebp_esp_source_candidate':bool(copy),
            'unique_frame_geometry_qualified':bool(qualified),
            'callee_entry_esp_relative_offset':entry,'caller_pre_call_esp_relative_offset':caller,
            'matching_push_rva':push['site_rva'] if push else None,
            'matching_push_operand_shape':push['input'] if push else None,
            'conditional_whole_slot_geometry_candidate':bool(push),
            'requires_32bit_stack_address_and_near_call_geometry':True,
            'actual_argument_contents_abi_alias_or_owner_binding_proven':False}

def geometry_key(op):
    g=op.get('geometry') or {}
    return tuple(g.get(k) for k in ('base_register','index_register','index_scale',
                                  'relative_field_offset','segment_register','displacement_region'))

def address_pairs(definitions,comparisons):
    rows=[]
    for definition in definitions:
        ops=definition['operands']
        if definition['mnemonic']!='lea' or len(ops)!=2 or ops[1].get('kind')!='memory':continue
        for compare in comparisons:
            for idx,op in enumerate(compare['operands']):
                if op.get('kind')=='memory':
                    rows.append({'lea_site_rva':definition['site_rva'],'compare_site_rva':compare['site_rva'],
                                 'compare_operand_index':idx,
                                 'same_address_spelling_candidate':geometry_key(ops[1])==geometry_key(op),
                                 'lea_operand_width_bytes':ops[1]['width_bytes'],
                                 'compare_memory_width_bytes':op['width_bytes'],
                                 'actual_same_effective_address_frame_memory_or_buffer_proven':False})
    return rows

def callee_context(dec,sections,imports,prior):
    nodes,edges,front,hit=candidate_graph(dec,READ_ROOT)
    effects=[stack_effect(ins,dec.base) for _,ins in sorted(nodes.items())]
    states,updates,limit=stack_states(effects,edges,READ_ROOT)
    reads=[instruction_row(dec,sections,nodes,at) for at,ins in sorted(nodes.items())
           if READ_ROOT<=at<READ_ROOT+96 and ins.mnemonic!='lea'
           and any(o.type==X86_OP_MEM and o.access&1 and ins.reg_name(o.mem.base)=='ebp' for o in ins.operands)]
    reads=reads[:MAX_READS]
    prolog=[instruction_row(dec,sections,nodes,at) for at,ins in sorted(nodes.items())
            if at<READ_ROOT+24 and (set(ins.reg_name(r) for r in ins.regs_access()[1])&{'esp','ebp'})]
    queries={(r['site_rva'],reg) for r in reads+prolog for reg in r['input_query_registers']}
    inputs=input_surface(dec,sections,nodes,edges,READ_ROOT,queries)
    defs=sorted({s['rva'] for q in inputs['queries'] if q['register']=='ebp'
                 for s in q['reaching_candidates'] if s['origin']=='definition'})
    definitions=[instruction_row(dec,sections,nodes,at) for at in defs[:MAX_FRAME_DEFS]]
    summaries=[state_summary(states,at,limit) for at in defs[:MAX_FRAME_DEFS]]
    queries.update((r['site_rva'],reg) for r in definitions for reg in r['input_query_registers'])
    inputs=input_surface(dec,sections,nodes,edges,READ_ROOT,queries)
    apis=[]
    for site,anchor in APIS:
        identity=call_identity(dec,site,imports,sections)
        if site not in nodes or (identity.get('import_identity') or {}).get('name')!='ReadFile':
            raise ValueError('R40 exact ReadFile import context')
        suffix=local_push_suffix(dec,sections,anchor,site)
        aq={(p['site_rva'],reg) for p in suffix['pushes'] for reg in operand_registers(p['input'])}
        aq.update((site,reg) for reg in ('eax','ebx','ecx','esi','edi','ebp'))
        apis.append({'site_rva':site,'linear_anchor_rva':anchor,'identity':identity,'physical_push_suffix':suffix,
                     'input_sources':input_surface(dec,sections,nodes,edges,READ_ROOT,aq),
                     'actual_api_parameter_handle_buffer_length_or_effect_proven':False})
    return {'root_candidate_rva':READ_ROOT,'graph':graph_meta(nodes,edges,front,hit),
            'bounded_edges':[list(e) for e in sorted(edges)],'stack_effect_candidates':effects,
            'stack_model_updates':updates,'stack_model_update_limit_hit':limit,
            'entry_prolog_shapes':prolog,'early_frame_read_shapes':reads,
            'early_frame_read_scope':'instruction_starts_first96bytes_whole_instructions_in_parent768',
            'early_frame_reads_truncated':sum(READ_ROOT<=at<READ_ROOT+96 and ins.mnemonic!='lea'
                and any(o.type==X86_OP_MEM and o.access&1 and ins.reg_name(o.mem.base)=='ebp' for o in ins.operands)
                for at,ins in nodes.items())>MAX_READS,
            'frame_input_sources':inputs,'frame_definition_count':len(defs),
            'frame_definition_shapes':definitions,'frame_definitions_truncated':len(defs)>MAX_FRAME_DEFS,
            'frame_definition_esp_summaries':summaries,
            'prior_caller_pushes':prior['native_read_caller']['push_candidates'],
            'conditional_frame_slot_bridges':[frame_bridge(row,inputs,definitions,summaries,
                prior['native_read_caller']['push_candidates']) for row in reads],
            'read_api_contexts':apis,'actual_frame_parameter_or_payload_role_proven':False}

def caller_context(dec,sections,prior):
    nodes,edges,front,hit=candidate_graph(dec,PARENT)
    branches=[(at,ins) for at,ins in sorted(nodes.items()) if READ_CALL+5<=at<READ_CALL+80
              and ins.mnemonic in ('je','jne','jz','jnz')]
    contexts=[];queries=set()
    for at,ins in branches[:MAX_BRANCHES]:
        sources,examined,cap,disconnected=bounded_flag_sources(nodes,edges,at)
        sample=[]
        for source,kind in sources[:MAX_SOURCE_SAMPLES]:
            row=instruction_row(dec,sections,nodes,source)
            queries.update((source,r) for r in row['input_query_registers'])
            sample.append({'kind':kind,'shape':row})
        contexts.append({'branch_site_rva':at,'mnemonic':ins.mnemonic,
                         'direct_target_rva':direct_target(ins,dec.base),'fallthrough_rva':at+ins.size,
                         'source_count':len(sources),'source_candidates':sample,
                         'sources_truncated':len(sources)>MAX_SOURCE_SAMPLES,
                         'predecessor_nodes_examined':examined,'predecessor_cap_hit':cap,
                         'branch_disconnected_in_graph':disconnected,
                         'actual_zf_value_feasible_or_taken_path_proven':False})
    old=prior['native_read_caller']
    defs,compares=old['push_definition_shapes'],old['postcall_compare_shapes']
    for row in defs+compares:queries.update((row['site_rva'],r) for r in row['input_query_registers'])
    return {'root_candidate_rva':PARENT,'graph':graph_meta(nodes,edges,front,hit),
            'prior_push_definition_shapes':defs,'prior_postcall_compare_shapes':compares,
            'buffer_address_spelling_pairs':address_pairs(defs,compares),
            'postcall_branch_count':len(branches),'postcall_branch_contexts':contexts,
            'postcall_branches_truncated':len(branches)>MAX_BRANCHES,
            'input_sources':input_surface(dec,sections,nodes,edges,PARENT,queries),
            'actual_endcheck_text_eof_or_savedata_payload_role_proven':False}

def derive(dec,sections,imports,prior):
    if prior.get('schema')!='tw10-r39-original-mask-symbolic-slots-native-read-caller':
        raise ValueError('R40 prerequisite schema')
    return {'schema':SCHEMA,'status':STATUS,'runtime_sha256':RUNTIME_SHA256,'savedata_sha256':SAVEDATA_SHA256,
            'r39_exact_original_revalidated':True,'r39_exact_report_sha256':PRIOR_SHA256,'static_only':True,
            'caller_identity':prior['native_read_caller']['read_context_call_identity'],
            'native_read_context':callee_context(dec,sections,imports,prior),
            'postcall_context':caller_context(dec,sections,prior),**{flag:False for flag in FLAGS}}

def inspect_verified(runtime,savedata):
    prior=inspect_r39(runtime,savedata);validate_r39(prior)
    if hashlib.sha256((json.dumps(prior,sort_keys=True)+'\n').encode()).hexdigest()!=PRIOR_SHA256:
        raise ValueError('R40 exact R39 derivative changed')
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'sa_3.exe';p.write_bytes(runtime);data,pe,base,sections,imports=image_layout(p)
    for sec,raw in zip(sections,pe.sections):sec['characteristics']=int(raw.Characteristics)
    text=next(s for s in sections if s['name']=='.text')
    return derive(Decoder(data[text['raw']:text['raw']+text['raw_size']],text['rva'],base),sections,imports,prior)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--bin',type=Path,required=True)
    image,rows,_,_=find_rows(parser.parse_args().bin)
    try:
        files={r['path']:r for r in rows if not r['is_dir']}
        with tempfile.TemporaryDirectory() as td:
            exe,save=Path(td)/'sa_3.exe',Path(td)/'savedata.dat'
            extract_row(image,files[RUNTIME_PATH],exe);extract_row(image,files[SAVEDATA_PATH],save)
            result=inspect_verified(exe.read_bytes(),save.read_bytes())
    finally:image.close()
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__':main()
