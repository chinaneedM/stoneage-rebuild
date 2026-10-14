"""Wrapper prefix token, multiply-source and complete native definition audit.

Every token is a bounded operand symbol. No original arithmetic, memory,
parameter values, IO effects or owner identities are evaluated/admitted.
"""
import argparse
import hashlib
import json
import tempfile
from pathlib import Path
from capstone.x86 import X86_OP_MEM
from tools.stoneage_tw10_savedata_native_io_r42 import inspect_verified as inspect_r42, WRAPPERS, RUNTIME_SHA256, SAVEDATA_SHA256
from tools.stoneage_tw10_savedata_native_io_r42_guard import validate as validate_r42
from tools.stoneage_tw10_savedata_native_io_r28 import candidate_graph, input_surface
from tools.stoneage_tw10_savedata_native_io_r37 import instruction_row, operand_registers
from tools.stoneage_tw10_savedata_native_io_r41 import queries_for
from tools.stoneage_tw10_savedata_native_io_r38 import stack_states, state_summary
from tools.stoneage_tw10_savedata_native_io_r40 import frame_bridge
from tools.stoneage_tw10_savedata_native_io_r36 import closure
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH, SAVEDATA_PATH
from tools.stoneage_tw10_technical_probe import find_rows, extract_row

SCHEMA = 'tw10-r43-original-wrapper-prefix-product-complete-native-source-candidates'
STATUS = 'PINNED_ORIGINAL_CONDITIONAL_PREFIX_PRODUCT_CYCLE_SOURCES_NATIVE_SAVE_OPEN'
PRIOR_SHA256 = '545901acc97a027fb38a3937e00549b15f45b379c7c059e98ece6133c9541732'
PRODUCTS = ((0x48bc3, 0x48bc6), (0x48667, 0x4866a))
OMITTED = 0x48c93
MAX_NATIVE_DEFS = 32
MAX_CYCLES = 96
PREFIX_KNOWN_SYNTAX = {'push','pop','mov','lea','movzx','movsx','xor','add','sub','and','or','inc','dec','cmp','test','nop','imul','mul','shl','shr','sar','sal','cdq','call','je','jne','jz','jnz','jmp','ja','jbe','jb','jae','jg','jge','jl','jle'}
FLAGS = ('actual_original_stack_contents_or_parameter_values_proven', 'actual_size_product_or_api_count_proven',
         'symbolic_prefix_establishes_actual_handle_or_owner', 'loop_connectivity_establishes_feasible_execution',
         'actual_descriptor_buffer_or_native_callee_binding_proven', 'native_save_schema_or_persistence_proven',
         'native_io_executed', 'original_bytes_published')


def frame_source_offset(row, operand, inputs, definitions, summaries):
    geo = operand.get('geometry') or {}
    query = next((q for q in inputs['queries'] if q['site_rva'] == row['site_rva'] and q['register'] == 'ebp'), {})
    tokens = query.get('reaching_candidates', [])
    at = tokens[0]['rva'] if len(tokens) == 1 and tokens[0]['origin'] == 'definition' else None
    definition = next((r for r in definitions if r['site_rva'] == at), {})
    ops = definition.get('operands', [])
    delta = next((s['unique_conditional_esp_delta'] for s in summaries if s['site_rva'] == at), None)
    good = (geo.get('base_register') == 'ebp' and geo.get('index_register') is None and geo.get('segment_register') is None
            and type(geo.get('relative_field_offset')) is int and definition.get('mnemonic') == 'mov'
            and len(ops) == 2 and all(o.get('kind') == 'register' and o.get('width_bytes') == 4 for o in ops)
            and [o.get('register') for o in ops] == ['ebp', 'esp'] and delta is not None
            and query.get('site_in_candidate_graph') is True and query.get('candidates_truncated') is False
            and inputs['query_limit_hit'] is False)
    return delta + geo['relative_field_offset'] if good else None


def prefix_audit(root, evidence, read, bridge, inputs):
    edges, effects = evidence['bounded_edges'], evidence['stack_effect_candidates']
    states, _, limit = stack_states(effects, edges, root)
    site = read['site_rva'];prefix = (closure(edges, root) & closure(edges, site, True)) - {site}
    mems = [op for op in read['operands'] if op.get('kind') == 'memory']
    width = mems[0]['width_bytes'] if len(mems) == 1 else None
    target = bridge['callee_entry_esp_relative_offset']
    writes, unknown = [], []
    for e in effects:
        at = e['site_rva']
        if at not in prefix:continue
        delta = state_summary(states, at, limit)['unique_conditional_esp_delta']
        if e['syntax_class'] in ('opaque_call', 'unknown_esp_write'):
            unknown.append({'site_rva': at, 'kind': e['syntax_class']})
        if e['syntax_class'] == 'push':
            start = delta - e['operand_width_bytes'] if delta is not None else None
            writes.append({'site_rva': at, 'kind': 'implicit_push_write', 'entry_relative_start': start,
                           'width_bytes': e['operand_width_bytes'], 'possible_alias_or_unknown_offset': start is None})
    for w in evidence['prefix_explicit_write_shapes']:
        at = w['site_rva']
        if at not in prefix:continue
        for op in w['operands']:
            if op.get('kind') != 'memory' or not op.get('decoder_write'):continue
            geo = op.get('geometry') or {};start = None
            if geo.get('base_register') == 'ebp':
                start = frame_source_offset(w, op, inputs, evidence['frame_definition_shapes'], evidence['frame_definition_esp_summaries'])
            elif geo.get('base_register') == 'esp' and geo.get('index_register') is None and geo.get('segment_register') is None:
                delta = state_summary(states, at, limit)['unique_conditional_esp_delta']
                if delta is not None and type(geo.get('relative_field_offset')) is int:start = delta + geo['relative_field_offset']
            writes.append({'site_rva': at, 'kind': 'explicit_memory_write', 'entry_relative_start': start,
                           'width_bytes': op['width_bytes'], 'possible_alias_or_unknown_offset': start is None})
    for row in evidence['prefix_unmodeled_effect_shapes']:
        if row['site_rva'] in prefix:unknown.append({'site_rva':row['site_rva'],'kind':'unmodeled_prefix_instruction'})
    unknown.sort(key=lambda r:(r['site_rva'],r['kind']))
    writes.sort(key=lambda r:(r['site_rva'],r['kind']))
    overlaps = sorted({w['site_rva'] for w in writes if w['entry_relative_start'] is not None and type(target) is int
                       and type(width) is int and w['entry_relative_start'] < target + width
                       and target < w['entry_relative_start'] + w['width_bytes']})
    clear = bool(bridge['conditional_whole_slot_geometry_candidate'] and not limit and not unknown and not overlaps
                 and not any(w['possible_alias_or_unknown_offset'] for w in writes))
    push = bridge['matching_push_operand_shape'] or {};ops = read['operands'];dst = ops[0] if ops else {}
    token = bool(clear and read['mnemonic'] == 'mov' and dst.get('kind') == 'register' and dst.get('width_bytes') == width == 4
                 and push.get('kind') in ('register','immediate'))
    return {'read_site_rva': site, 'prefix_node_rvas': sorted(prefix), 'target_entry_relative_start': target,
            'target_width_bytes': width, 'modeled_prefix_write_candidates': writes, 'overlapping_write_sites': overlaps,
            'unknown_prefix_effect_candidates': unknown, 'no_bounded_prefix_overwrite_candidate': clear,
            'conditional_caller_operand_to_register_symbol_candidate': token,
            'source_push_rva': bridge['matching_push_rva'] if token else None,
            'source_push_operand_symbol': push if token else None,
            'destination_register_symbol': dst.get('register') if token else None,
            'requires_prior32bit_stack_near_call_and_frame_conditions': True,
            'only_explicit_decoder_writes_and_modeled_pushes_covered': True,
            'actual_original_contents_argument_value_alias_owner_proven': False}


def product_link(load, multiply, inputs):
    ops = load['operands'];ms = multiply['operands']
    reg = ms[0].get('register') if ms else None
    q = next((q for q in inputs['queries'] if q['site_rva'] == multiply['site_rva'] and q['register'] == reg), {})
    tokens = q.get('reaching_candidates', [])
    unique = bool(q.get('site_in_candidate_graph') is True and q.get('candidates_truncated') is False
                  and not inputs['query_limit_hit'] and len(tokens) == 1
                  and tokens[0]['origin'] == 'definition' and tokens[0]['rva'] == load['site_rva'])
    qualified = bool(unique and load['mnemonic'] == 'mov' and multiply['mnemonic'] == 'imul' and len(ops) == len(ms) == 2
                     and ops[0].get('kind') == ms[0].get('kind') == 'register' and ops[0].get('register') == reg
                     and ops[0].get('width_bytes') == ms[0].get('width_bytes') == 4
                     and ops[1].get('kind') == ms[1].get('kind') == 'memory' and ops[1].get('width_bytes') == ms[1].get('width_bytes') == 4)
    return {'load_site_rva': load['site_rva'], 'multiply_site_rva': multiply['site_rva'],
            'unique_local_load_definition_to_imul_candidate': unique,
            'conditional_two_memory_operands_multiply_shape': qualified,
            'register_symbol': reg if qualified else None, 'original_inputs_or_product_evaluated': False,
            'actual_size_count_overflow_or_api_role_proven': False}


def cycle_sources(inputs, query_sites, edges):
    rows = []
    for q in inputs['queries']:
        if q['site_rva'] not in query_sites:continue
        a = q['site_rva']
        for token in q['reaching_candidates']:
            b = token['rva'];ab = b in closure(edges,a);ba = a in closure(edges,b)
            rows.append({'query_site_rva': a, 'register': q['register'], 'source_origin': token['origin'], 'source_rva': b,
                         'source_numerically_after_or_equal_query': b >= a,
                         'query_to_source_graph_path_candidate': ab, 'source_to_query_graph_path_candidate': ba,
                         'same_structural_cycle_region_candidate': ab and ba,
                         'actual_iteration_value_callee_effect_or_feasible_path_proven': False})
    return rows


def context(dec, sections, prior, spec, product):
    _,root,call,_,_ = spec
    old = next(w for w in prior['wrappers'] if w['root_candidate_rva'] == root)
    nodes,edges,_,_ = candidate_graph(dec,root)
    reads = old['early_stack_read_or_multiply_shapes'][:4]
    prefix = set().union(*[(closure(edges,root)&closure(edges,r['site_rva'],True))-{r['site_rva']} for r in reads])
    writes = [instruction_row(dec,sections,nodes,at) for at,ins in sorted(nodes.items()) if at in prefix
              and any(o.type == X86_OP_MEM and o.access&2 for o in ins.operands)]
    evidence = {k:old[k] for k in ('graph','bounded_edges','stack_effect_candidates','frame_definition_shapes','frame_definition_esp_summaries')}
    evidence['prefix_explicit_write_shapes'] = writes
    evidence['prefix_unmodeled_effect_shapes'] = [instruction_row(dec,sections,nodes,at) for at in sorted(prefix) if nodes[at].mnemonic not in PREFIX_KNOWN_SYNTAX]
    inputs = input_surface(dec,sections,nodes,edges,root,queries_for(reads+writes+evidence['prefix_unmodeled_effect_shapes']+old['frame_definition_shapes']))
    callers = []
    for b in old['savedata_caller_bridges']:
        bridges = [frame_bridge(r,inputs,old['frame_definition_shapes'],old['frame_definition_esp_summaries'],b['prior_caller_push_candidates']) for r in reads]
        callers.append({k:b[k] for k in ('caller_site_rva','parent_filename_push_rva','caller_identity','prior_caller_push_candidates')}
                       | {'conditional_slot_bridges':bridges,'prefix_token_audits':[prefix_audit(root,evidence,r,bridge,inputs) for r,bridge in zip(reads,bridges)]})
    load,multiply = [instruction_row(dec,sections,nodes,at) for at in product]
    native = old['native_context_call'];suffix = native['conditional_linear_push_suffix'];query_sites={call}|{p['site_rva'] for p in suffix['pushes']}
    queries = {(p['site_rva'],r) for p in suffix['pushes'] for r in operand_registers(p['input'])}
    queries.update((call,r) for r in ('eax','ebx','esi','edi','ebp'))
    ni = input_surface(dec,sections,nodes,edges,root,queries)
    defs = sorted({t['rva'] for q in ni['queries'] if (q['site_rva'],q['register']) in queries for t in q['reaching_candidates'] if t['origin']=='definition'})
    shapes = [instruction_row(dec,sections,nodes,at) for at in defs[:MAX_NATIVE_DEFS]]
    ni = input_surface(dec,sections,nodes,edges,root,queries|queries_for(shapes))
    cycles = cycle_sources(ni,query_sites,edges)
    return {'root_candidate_rva':root,'prior_wrapper_evidence':evidence,'early_parameter_read_shapes':reads,
            'prefix_input_sources':inputs,'savedata_caller_token_contexts':callers,
            'multiply_load_shape':load,'multiply_shape':multiply,'conditional_multiply_source_link':product_link(load,multiply,inputs),
            'native_call_site_rva':call,'prior_native_call_identity':native['identity'],'prior_native_physical_suffix':suffix,
            'native_input_sources':ni,'native_direct_definition_count':len(defs),'native_direct_definition_shapes':shapes,
            'native_direct_definitions_truncated':len(defs)>MAX_NATIVE_DEFS,
            'prior_native_direct_definition_count':native['direct_input_definition_count'],
            'prior_native_direct_shape_count':len(native['direct_input_definition_shapes']),
            'prior_native_direct_shape_rvas':[r['site_rva'] for r in native['direct_input_definition_shapes']],
            'prior_sampler_omitted_definition_rvas':sorted(set(defs)-{r['site_rva'] for r in native['direct_input_definition_shapes']}),
            'cycle_source_count':len(cycles),'cycle_source_candidates':cycles[:MAX_CYCLES],'cycle_sources_truncated':len(cycles)>MAX_CYCLES,
            'actual_descriptor_buffer_count_or_native_parameter_binding_proven':False}


def derive(dec,sections,prior):
    if prior.get('schema')!='tw10-r42-original-savedata-wrapper-native-io-correspondence-candidates':raise ValueError('R43 prerequisite schema')
    return {'schema':SCHEMA,'status':STATUS,'runtime_sha256':RUNTIME_SHA256,'savedata_sha256':SAVEDATA_SHA256,
            'r42_exact_original_revalidated':True,'r42_exact_report_sha256':PRIOR_SHA256,'static_only':True,
            'contexts':[context(dec,sections,prior,spec,product) for spec,product in zip(WRAPPERS,PRODUCTS)],
            **{flag:False for flag in FLAGS}}


def inspect_verified(runtime,savedata):
    prior=inspect_r42(runtime,savedata);validate_r42(prior)
    if hashlib.sha256((json.dumps(prior,sort_keys=True)+'\n').encode()).hexdigest()!=PRIOR_SHA256:raise ValueError('R43 exact R42 derivative changed')
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'sa_3.exe';p.write_bytes(runtime);data,pe,base,sections,_=image_layout(p)
    for s,raw in zip(sections,pe.sections):s['characteristics']=int(raw.Characteristics)
    t=next(s for s in sections if s['name']=='.text')
    return derive(Decoder(data[t['raw']:t['raw']+t['raw_size']],t['rva'],base),sections,prior)


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
