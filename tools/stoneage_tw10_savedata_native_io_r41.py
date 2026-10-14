"""Savedata-specific caller continuation discovery, without return/ABI binding.

Metadata only. Each filename PUSH is an independent conditional graph root;
CALL fallthrough assumes structural return, killing every register provenance.
"""
import argparse
import hashlib
import json
import tempfile
from pathlib import Path
from capstone import CS_GRP_CALL
from capstone.x86 import X86_OP_MEM
from tools.stoneage_tw10_savedata_argtrace_r7 import inspect_verified as inspect_r7
from tools.stoneage_tw10_savedata_argtrace_r7_guard import validate as validate_r7
from tools.stoneage_tw10_savedata_native_io_r28 import candidate_graph, input_surface
from tools.stoneage_tw10_savedata_native_io_r37 import instruction_row, operand_registers
from tools.stoneage_tw10_savedata_upstream_r23 import local_push_suffix
from tools.stoneage_tw10_savedata_frontier_r12 import call_identity
from tools.stoneage_tw10_savedata_entrygraph_r4 import explore
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
from tools.stoneage_tw10_savedata_instruction_probe import RUNTIME_SHA256, SAVEDATA_SHA256, EXPECTED_STRING_RVA
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH, SAVEDATA_PATH
from tools.stoneage_tw10_technical_probe import find_rows, extract_row

SCHEMA = 'tw10-r41-original-savedata-specific-caller-continuation-candidates'
STATUS = 'PINNED_ORIGINAL_CONDITIONAL_FILENAME_CALLERS_PAYLOAD_IO_OPEN'
PRIOR_SHA256 = '73b965887f0ff391f40abba4649482aa2d832151df5fbb602c4274d356bc71d8'
SITES = ((0x40064, 0x40069), (0x400e4, 0x400e9), (0x40115, 0x4011a), (0x402a0, 0x402a5))
OPEN_ROOT = 0x487ba
SPAN = 192
NODE_CAP = 128
CONTINUATION_BYTES = 128
MAX_CALLS = 8
MAX_SHAPES = 24
MAX_DEFS = 12
FLAGS = ('actual_function_entry_or_path_proven', 'actual_filename_open_return_handle_proven',
         'actual_caller_frame_or_register_preservation_proven', 'actual_api_argument_roles_or_values_proven',
         'savedata_buffer_length128_or_schema_proven', 'actual_payload_io_or_persistence_proven',
         'native_io_executed', 'original_bytes_published')


def queries_for(rows):
    return {(r['site_rva'], reg) for r in rows for reg in r['input_query_registers']}


def call_context(dec, sections, imports, root, nodes, edges, at):
    suffix = local_push_suffix(dec, sections, root, at)
    queries = {(p['site_rva'], r) for p in suffix['pushes'] for r in operand_registers(p['input'])}
    queries.update((at, r) for r in ('eax', 'ebx', 'esi', 'edi', 'ebp'))
    sources = input_surface(dec, sections, nodes, edges, root, queries)
    defs = sorted({s['rva'] for q in sources['queries']
                   if (q['site_rva'], q['register']) in queries
                   for s in q['reaching_candidates'] if s['origin'] == 'definition'})
    rows = [instruction_row(dec, sections, nodes, site) for site in defs[:MAX_DEFS]]
    # Re-run from the same root; explicitly requested definition inputs have depth0.
    sources = input_surface(dec, sections, nodes, edges, root, queries | queries_for(rows))
    return {'site_rva': at, 'identity': call_identity(dec, at, imports, sections),
            'conditional_linear_push_suffix': suffix, 'input_sources': sources,
            'direct_input_definition_count': len(defs), 'direct_input_definition_shapes': rows,
            'direct_input_definitions_truncated': len(defs) > MAX_DEFS,
            'actual_return_argument_buffer_count_or_io_proven': False}


def caller_context(dec, sections, imports, root, call, entrygraph):
    nodes, edges, front, hit = candidate_graph(dec, root, span=SPAN, cap=NODE_CAP)
    if root not in nodes or call not in nodes or nodes[root].mnemonic != 'push':
        raise ValueError('R41 filename prefix boundary')
    prefix = [instruction_row(dec, sections, nodes, root), instruction_row(dec, sections, nodes, call)]
    op = prefix[0]['operands']
    if len(op) != 1 or op[0].get('kind') != 'immediate' or op[0].get('constant') != dec.base + EXPECTED_STRING_RVA:
        raise ValueError('R41 exact savedata filename immediate')
    identity = call_identity(dec, call, imports, sections)
    if identity['kind'] != 'direct' or identity['direct_target_rva'] != OPEN_ROOT or root + nodes[root].size != call:
        raise ValueError('R41 savedata open CALL identity')
    lo, hi = call + nodes[call].size, call + nodes[call].size + CONTINUATION_BYTES
    continuation = [(at, ins) for at, ins in sorted(nodes.items()) if lo <= at < hi]
    calls = [at for at, ins in continuation if ins.group(CS_GRP_CALL)]
    # Candidate memory/address, immediate PUSH and comparison syntax for payload discovery.
    selected = [at for at, ins in continuation if ins.mnemonic in ('lea', 'cmp', 'test', 'push')
                or any(o.type == X86_OP_MEM for o in ins.operands)]
    rows = [instruction_row(dec, sections, nodes, at) for at in selected[:MAX_SHAPES]]
    return {'filename_push_rva': root, 'open_call_rva': call, 'filename_displacement_rva': EXPECTED_STRING_RVA,
            'entrygraph_push_boundary_seen': root in entrygraph['visited'],
            'entrygraph_call_boundary_seen': call in entrygraph['visited'],
            'entrygraph_push_to_call_edge_seen': (root, call) in entrygraph['edges'],
            'actual_entry_or_execution_proven': False, 'filename_prefix_shapes': prefix,
            'filename_call_identity': identity,
            'prefix_input_sources': input_surface(dec, sections, nodes, edges, root, queries_for(prefix)),
            'filename_physical_push_suffix': local_push_suffix(dec, sections, root, call),
            'graph': {'span_bytes': SPAN, 'node_cap': NODE_CAP, 'nodes': len(nodes), 'edges': len(edges),
                      'frontier': [{'reason': why, 'rva': at} for why, at in front], 'node_limit_hit': hit,
                      'returning_call_assumption_only': True, 'actual_entry_path_proven': False},
            'bounded_node_rvas': sorted(nodes), 'bounded_edges': [list(e) for e in sorted(edges)],
            'continuation_start_rva': lo, 'continuation_end_rva': hi,
            'selection_scope': 'instruction_starts_first128bytes_whole_instructions_in_parent192',
            'continuation_call_count': len(calls), 'continuation_calls_truncated': len(calls) > MAX_CALLS,
            'continuation_calls': [call_context(dec, sections, imports, root, nodes, edges, at) for at in calls[:MAX_CALLS]],
            'continuation_shape_count': len(selected), 'continuation_shapes_truncated': len(selected) > MAX_SHAPES,
            'continuation_shapes': rows,
            'continuation_input_sources': input_surface(dec, sections, nodes, edges, root, queries_for(rows)),
            'actual_open_return_handle_or_payload_binding_proven': False}


def derive(dec, sections, imports, entrygraph, entry_rva):
    return {'schema': SCHEMA, 'status': STATUS, 'runtime_sha256': RUNTIME_SHA256,
            'savedata_sha256': SAVEDATA_SHA256, 'r7_exact_original_revalidated': True,
            'r7_exact_report_sha256': PRIOR_SHA256, 'static_only': True, 'image_base': dec.base,
            'entrygraph_support': {'entrypoint_rva': entry_rva, 'visited_nodes': len(entrygraph['visited']),
                                   'edges': len(entrygraph['edges']), 'node_limit_hit': entrygraph['limit_hit'],
                                   'direct_cfg_candidate_only': True, 'complete_cfg_or_actual_execution_proven': False},
            'caller_contexts': [caller_context(dec, sections, imports, root, call, entrygraph) for root, call in SITES],
            **{flag: False for flag in FLAGS}}


def inspect_verified(runtime, savedata):
    prior = inspect_r7(runtime, savedata)
    validate_r7(json.dumps(prior, sort_keys=True))
    if hashlib.sha256((json.dumps(prior, sort_keys=True) + '\n').encode()).hexdigest() != PRIOR_SHA256:
        raise ValueError('R41 exact R7 hardened derivative changed')
    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / 'sa_3.exe'
        path.write_bytes(runtime)
        data, pe, base, sections, imports = image_layout(path)
    for section, raw in zip(sections, pe.sections):
        section['characteristics'] = int(raw.Characteristics)
    text = next(s for s in sections if s['name'] == '.text')
    raw = data[text['raw']:text['raw'] + text['raw_size']]
    entry = int(pe.OPTIONAL_HEADER.AddressOfEntryPoint)
    graph = explore(raw, text['rva'], base, entry)
    return derive(Decoder(raw, text['rva'], base), sections, imports, graph, entry)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bin', type=Path, required=True)
    image, rows, _, _ = find_rows(parser.parse_args().bin)
    try:
        files = {r['path']: r for r in rows if not r['is_dir']}
        with tempfile.TemporaryDirectory() as td:
            exe, save = Path(td) / 'sa_3.exe', Path(td) / 'savedata.dat'
            extract_row(image, files[RUNTIME_PATH], exe)
            extract_row(image, files[SAVEDATA_PATH], save)
            report = inspect_verified(exe.read_bytes(), save.read_bytes())
    finally:
        image.close()
    print(json.dumps(report, sort_keys=True))


if __name__ == '__main__':
    main()
