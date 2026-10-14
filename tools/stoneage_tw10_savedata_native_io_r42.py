"""Savedata caller-supported wrappers and conditional native IO correspondence.

Nonexecuting metadata only. Stack/frame slots and structural paths never admit
actual parameters, returned handles, byte counts or original persisted contents.
"""
import argparse
import hashlib
import json
import tempfile
from pathlib import Path
from capstone import CS_GRP_CALL, CS_GRP_JUMP
from capstone.x86 import X86_OP_MEM
from tools.stoneage_tw10_savedata_native_io_r41 import (
    inspect_verified as inspect_r41, call_context, queries_for, RUNTIME_SHA256, SAVEDATA_SHA256)
from tools.stoneage_tw10_savedata_native_io_r41_guard import validate as validate_r41
from tools.stoneage_tw10_savedata_native_io_r28 import candidate_graph, input_surface
from tools.stoneage_tw10_savedata_native_io_r30 import graph_meta
from tools.stoneage_tw10_savedata_native_io_r37 import instruction_row, operand_registers
from tools.stoneage_tw10_savedata_native_io_r38 import stack_effect, stack_states, state_summary
from tools.stoneage_tw10_savedata_native_io_r40 import frame_bridge
from tools.stoneage_tw10_savedata_native_io_r33 import bounded_flag_sources, MAX_SOURCE_SAMPLES
from tools.stoneage_tw10_savedata_upstream_r22 import graph_path
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder, direct_target
from tools.stoneage_tw10_savedata_entrygraph_r4 import explore
from tools.stoneage_tw10_savedata_frontier_r12 import call_identity
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH, SAVEDATA_PATH
from tools.stoneage_tw10_technical_probe import find_rows, extract_row

SCHEMA = 'tw10-r42-original-savedata-wrapper-native-io-correspondence-candidates'
STATUS = 'PINNED_ORIGINAL_CONDITIONAL_WRAPPER_NATIVE_IO_PATHS_PAYLOAD_OPEN'
PRIOR_SHA256 = '8c8474f75eb6adec5aa3939054f0fce26997152fb8e1f1424e74f18485c2471c'
WRAPPERS = (('WriteFile_context_candidate', 0x48bbc, 0x48c5e, 0x4c5b4, ((0x40064, 0x40090), (0x402a0, 0x402c9))),
            ('ReadFile_context_candidate', 0x48660, 0x486f0, 0x4a8dc, ((0x40115, 0x40145),)))
MAX_EARLY = 16
MAX_DEFS = 12
MAX_BRANCHES = 8
MAX_CALLS = 12
FLAGS = ('actual_wrapper_function_or_executed_path_proven', 'actual_four_parameter_abi_value_binding_proven',
         'actual_size_product_count_or_buffer_capacity_proven', 'actual_open_handle_or_file_object_owner_proven',
         'actual_native_io_return_effects_or_persistence_proven', 'literal4000_establishes_actual_api_length',
         'fixed128_byte_savedata_schema_proven', 'native_io_executed', 'original_bytes_published')


def branch_context(dec, sections, nodes, edges, root, at):
    ins = nodes[at]
    sources, examined, cap, disconnected = bounded_flag_sources(nodes, edges, at)
    rows = [{'kind': kind, 'shape': instruction_row(dec, sections, nodes, site)}
            for site, kind in sources[:MAX_SOURCE_SAMPLES]]
    return {'branch_site_rva': at, 'mnemonic': ins.mnemonic,
            'direct_target_rva': direct_target(ins, dec.base), 'fallthrough_rva': at + ins.size,
            'source_count': len(sources), 'source_candidates': rows,
            'sources_truncated': len(sources) > MAX_SOURCE_SAMPLES,
            'predecessor_nodes_examined': examined, 'predecessor_cap_hit': cap,
            'branch_disconnected_in_graph': disconnected,
            'input_sources': input_surface(dec, sections, nodes, edges, root, queries_for([r['shape'] for r in rows])),
            'actual_flag_value_feasibility_or_taken_path_proven': False}


def wrapper_context(dec, sections, imports, prior, entrygraph, spec):
    label, root, native_call, native_root, callers = spec
    nodes, edges, front, hit = candidate_graph(dec, root)
    if native_call not in nodes:
        raise ValueError('R42 exact native context CALL absent from wrapper graph')
    native_identity = call_identity(dec, native_call, imports, sections)
    if native_identity['kind'] != 'direct' or native_identity['direct_target_rva'] != native_root:
        raise ValueError('R42 native context target mismatch')
    effects = [stack_effect(ins, dec.base) for _, ins in sorted(nodes.items())]
    states, updates, limit = stack_states(effects, edges, root)
    prolog = [instruction_row(dec, sections, nodes, at) for at, ins in sorted(nodes.items())
              if at < root + 24 and set(ins.reg_name(r) for r in ins.regs_access()[1]) & {'esp', 'ebp'}]
    early = [at for at, ins in sorted(nodes.items()) if at < root + 96 and ins.mnemonic != 'lea'
             and (ins.mnemonic in ('mul', 'imul') or any(o.type == X86_OP_MEM and o.access & 1
                  and ins.reg_name(o.mem.base) in ('esp', 'ebp') for o in ins.operands))]
    rows = [instruction_row(dec, sections, nodes, at) for at in early[:MAX_EARLY]]
    queries = queries_for(prolog + rows)
    inputs = input_surface(dec, sections, nodes, edges, root, queries)
    defs = sorted({s['rva'] for q in inputs['queries'] if q['register'] == 'ebp'
                   for s in q['reaching_candidates'] if s['origin'] == 'definition'})
    definitions = [instruction_row(dec, sections, nodes, at) for at in defs[:MAX_DEFS]]
    summaries = [state_summary(states, at, limit) for at in defs[:MAX_DEFS]]
    inputs = input_surface(dec, sections, nodes, edges, root, queries | queries_for(definitions))
    bridges = []
    for parent, call in callers:
        c = next(c for c in prior['caller_contexts'] if c['filename_push_rva'] == parent)
        a = next(a for a in c['continuation_calls'] if a['site_rva'] == call)
        actual = call_identity(dec, call, imports, sections)
        if actual != a['identity'] or actual['direct_target_rva'] != root:
            raise ValueError('R42 exact prior savedata caller changed')
        pushes = a['conditional_linear_push_suffix']['pushes']
        bridges.append({'parent_filename_push_rva': parent, 'caller_site_rva': call, 'caller_identity': actual,
                        'entrygraph_caller_boundary_seen': call in entrygraph['visited'],
                        'entrygraph_call_to_wrapper_edge_seen': (call, root) in entrygraph['edges'],
                        'prior_caller_push_candidates': pushes,
                        'conditional_frame_slot_bridges': [frame_bridge(r, inputs, definitions, summaries, pushes) for r in rows],
                        'actual_caller_wrapper_parameter_or_owner_binding_proven': False})
    branches = [at for at, ins in sorted(nodes.items()) if at < native_call and ins.mnemonic in ('je', 'jne', 'jz', 'jnz')]
    calls = [call_identity(dec, at, imports, sections) for at, ins in sorted(nodes.items()) if ins.group(CS_GRP_CALL)]
    return {'label': label, 'root_candidate_rva': root,
            'entrygraph_wrapper_boundary_seen': root in entrygraph['visited'],
            'entrygraph_native_call_boundary_seen': native_call in entrygraph['visited'],
            'entrygraph_native_target_boundary_seen': native_root in entrygraph['visited'],
            'entrygraph_native_call_target_edge_seen': (native_call, native_root) in entrygraph['edges'],
            'actual_function_entry_or_execution_proven': False,
            'graph': graph_meta(nodes, edges, front, hit), 'bounded_edges': [list(e) for e in sorted(edges)],
            'stack_effect_candidates': effects, 'stack_model_updates': updates, 'stack_model_update_limit_hit': limit,
            'entry_prolog_shapes': prolog, 'early_stack_read_or_multiply_count': len(early),
            'early_stack_read_or_multiply_shapes': rows, 'early_shapes_truncated': len(early) > MAX_EARLY,
            'early_shape_scope': 'instruction_starts_first96bytes_whole_instructions_in_parent768',
            'frame_definition_count': len(defs), 'frame_definition_shapes': definitions,
            'frame_definitions_truncated': len(defs) > MAX_DEFS, 'frame_definition_esp_summaries': summaries,
            'frame_input_sources': inputs, 'savedata_caller_bridges': bridges,
            'pre_native_zf_branch_count': len(branches), 'pre_native_zf_branches_truncated': len(branches) > MAX_BRANCHES,
            'pre_native_zf_branches': [branch_context(dec, sections, nodes, edges, root, at) for at in branches[:MAX_BRANCHES]],
            'call_candidate_count': len(calls), 'call_candidates': calls[:MAX_CALLS], 'call_candidates_truncated': len(calls) > MAX_CALLS,
            'native_context_call': call_context(dec, sections, imports, root, nodes, edges, native_call),
            'structural_root_to_native_call_candidate': graph_path(edges, root, native_call, cap=256),
            'structural_path_requires_opaque_calls_to_return': True,
            'actual_native_argument_buffer_count_or_savedata_io_proven': False}


def derive(dec, sections, imports, prior, entrygraph):
    if prior.get('schema') != 'tw10-r41-original-savedata-specific-caller-continuation-candidates':
        raise ValueError('R42 prerequisite schema')
    return {'schema': SCHEMA, 'status': STATUS, 'runtime_sha256': RUNTIME_SHA256, 'savedata_sha256': SAVEDATA_SHA256,
            'r41_exact_original_revalidated': True, 'r41_exact_report_sha256': PRIOR_SHA256, 'static_only': True,
            'entrygraph_support': prior['entrygraph_support'],
            'wrappers': [wrapper_context(dec, sections, imports, prior, entrygraph, spec) for spec in WRAPPERS],
            **{flag: False for flag in FLAGS}}


def inspect_verified(runtime, savedata):
    prior = inspect_r41(runtime, savedata)
    validate_r41(prior)
    if hashlib.sha256((json.dumps(prior, sort_keys=True) + '\n').encode()).hexdigest() != PRIOR_SHA256:
        raise ValueError('R42 exact R41 derivative changed')
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / 'sa_3.exe';p.write_bytes(runtime)
        data, pe, base, sections, imports = image_layout(p)
    for section, raw in zip(sections, pe.sections):
        section['characteristics'] = int(raw.Characteristics)
    t = next(s for s in sections if s['name'] == '.text')
    raw = data[t['raw']:t['raw'] + t['raw_size']]
    graph = explore(raw, t['rva'], base, int(pe.OPTIONAL_HEADER.AddressOfEntryPoint))
    return derive(Decoder(raw, t['rva'], base), sections, imports, prior, graph)


def main():
    p = argparse.ArgumentParser();p.add_argument('--bin', type=Path, required=True)
    image, rows, _, _ = find_rows(p.parse_args().bin)
    try:
        files = {r['path']: r for r in rows if not r['is_dir']}
        with tempfile.TemporaryDirectory() as td:
            exe, save = Path(td) / 'sa_3.exe', Path(td) / 'savedata.dat'
            extract_row(image, files[RUNTIME_PATH], exe);extract_row(image, files[SAVEDATA_PATH], save)
            d = inspect_verified(exe.read_bytes(), save.read_bytes())
    finally:
        image.close()
    print(json.dumps(d, sort_keys=True))


if __name__ == '__main__':
    main()
