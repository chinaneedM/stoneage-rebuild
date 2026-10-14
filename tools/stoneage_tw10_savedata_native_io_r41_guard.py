"""Bound R41 savedata metadata; independent immutable artifact custody separate."""
import argparse
import json
from pathlib import Path
from tools.stoneage_tw10_savedata_native_io_r41 import *
from tools.stoneage_tw10_savedata_native_io_r37_guard import row_guard, direct_guard
from tools.stoneage_tw10_savedata_native_io_r40_guard import suffix_guard
from tools.stoneage_tw10_savedata_native_io_r29_guard import input_guard
from tools.stoneage_tw10_savedata_upstream_r22_guard import FORBIDDEN


def require(ok, why):
    if not ok:
        raise ValueError('R41 ' + why)


def scoped_inputs(s, root, nodes):
    keys = input_guard(s, root)
    for q in s['queries']:
        require(root <= q['site_rva'] < root + SPAN and q['site_in_candidate_graph'] is (q['site_rva'] in nodes), 'query membership')
        require(all(t['rva'] in nodes for t in q['reaching_candidates']), 'source membership')
    return keys, s['query_limit_hit']


def ordered_rows(rows, limit, lo, hi, nodes, keys, cap):
    require(isinstance(rows, list) and len(rows) <= limit, 'row bound')
    seen = []
    for r in rows:
        at = r.get('site_rva')
        require(type(at) is int and lo <= at < hi and at in nodes, 'row graph/scope')
        row_guard(r, at, keys, cap)
        seen.append(at)
    require(seen == sorted(set(seen)), 'row order')


def identity_guard(ident, at):
    require(ident.get('call_rva') == at and ident.get('kind') in ('direct', 'register_indirect', 'memory_indirect', 'other')
            and ident.get('runtime_target_or_effects_proven') is False, 'call identity/no promotion')
    imp = ident.get('import_identity')
    if ident['kind'] == 'direct':
        require(type(ident.get('direct_target_rva')) is int and imp is None
                and ident.get('import_slot_association_proven') is False, 'direct target')
    elif imp:
        require(ident['kind'] == 'memory_indirect' and ident.get('import_slot_association_proven') is True
                and isinstance(imp.get('dll'), str) and isinstance(imp.get('name'), str) and type(imp.get('iat_rva')) is int, 'import association')
    else:
        require(ident.get('import_slot_association_proven') is False, 'unassociated import')


def validate(d):
    require(isinstance(d, dict) and d.get('schema') == SCHEMA and d.get('status') == STATUS, 'schema/status')
    require(d.get('runtime_sha256') == RUNTIME_SHA256 and d.get('savedata_sha256') == SAVEDATA_SHA256
            and d.get('r7_exact_original_revalidated') is True and d.get('r7_exact_report_sha256') == PRIOR_SHA256
            and d.get('static_only') is True and all(d.get(f) is False for f in FLAGS), 'source/non-promotion')
    base = d.get('image_base')
    require(type(base) is int and 0 <= base <= 0xffffffff, 'image base')
    e = d.get('entrygraph_support', {})
    require(type(e.get('entrypoint_rva')) is int and type(e.get('visited_nodes')) is int and 1 <= e['visited_nodes'] <= 120000
            and type(e.get('edges')) is int and 0 <= e['edges'] <= 240000 and type(e.get('node_limit_hit')) is bool
            and e.get('direct_cfg_candidate_only') is True and e.get('complete_cfg_or_actual_execution_proven') is False, 'entry evidence bounds')
    cs = d.get('caller_contexts')
    require(isinstance(cs, list) and len(cs) == len(SITES), 'caller count')
    for c, (root, call) in zip(cs, SITES):
        require(c.get('filename_push_rva') == root and c.get('open_call_rva') == call
                and c.get('filename_displacement_rva') == EXPECTED_STRING_RVA
                and c.get('actual_entry_or_execution_proven') is False
                and c.get('actual_open_return_handle_or_payload_binding_proven') is False, 'savedata caller/boundary')
        require(all(type(c.get(k)) is bool for k in ('entrygraph_push_boundary_seen', 'entrygraph_call_boundary_seen', 'entrygraph_push_to_call_edge_seen')),
                'entry boundary candidates')
        g = c.get('graph', {})
        ns, edges = c.get('bounded_node_rvas'), c.get('bounded_edges')
        require(g.get('span_bytes') == SPAN and g.get('node_cap') == NODE_CAP
                and type(g.get('nodes')) is int and 1 <= g['nodes'] <= NODE_CAP
                and type(g.get('edges')) is int and 0 <= g['edges'] <= 2 * NODE_CAP
                and type(g.get('node_limit_hit')) is bool and g.get('returning_call_assumption_only') is True
                and g.get('actual_entry_path_proven') is False, 'graph bounds/assumption')
        require(isinstance(ns, list) and len(ns) == g['nodes'] and ns == sorted(set(ns))
                and all(type(at) is int and root <= at < root + SPAN for at in ns) and root in ns and call in ns, 'graph nodes')
        require(isinstance(edges, list) and len(edges) == g['edges']
                and all(isinstance(edge, list) and len(edge) == 2 and all(type(at) is int and at in ns for at in edge) for edge in edges)
                and edges == [list(edge) for edge in sorted(set(tuple(edge) for edge in edges))] and [root, call] in edges, 'graph edges')
        front = g.get('frontier')
        require(isinstance(front, list) and len(front) <= 2 * NODE_CAP
                and all(f.get('reason') in ('out_of_window', 'decode_gap', 'instruction_span_limit', 'indirect_jump', 'node_cap')
                        and type(f.get('rva')) is int for f in front), 'frontier bounds')
        keys, cap = scoped_inputs(c.get('prefix_input_sources', {}), root, ns)
        prefix = c.get('filename_prefix_shapes')
        ordered_rows(prefix, 2, root, call + 5, ns, keys, cap)
        require([r['site_rva'] for r in prefix] == [root, call] and prefix[0]['mnemonic'] == 'push'
                and prefix[1]['mnemonic'] == 'call' and len(prefix[0]['operands']) == len(prefix[1]['operands']) == 1, 'prefix exact sites')
        op = prefix[0]['operands'][0]
        require(op.get('kind') == 'immediate' and op.get('width_bytes') == 4 and op.get('constant') == base + EXPECTED_STRING_RVA, 'exact filename immediate')
        require(prefix[1]['operands'][0].get('kind') == 'immediate'
                and prefix[1]['operands'][0].get('constant') == base + OPEN_ROOT, 'prefix target spelling')
        direct_guard(c.get('filename_call_identity', {}), call, OPEN_ROOT)
        suffix_guard(c.get('filename_physical_push_suffix', {}), root, call, keys, cap)
        require(c['filename_physical_push_suffix']['linear_call_boundary_reached'] is True
                and c['filename_physical_push_suffix']['pushes'] == [{'site_rva': root, 'conditional_pre_call_esp_offset': 0, 'input': op}], 'filename slot agreement')
        lo, hi = call + 5, call + 5 + CONTINUATION_BYTES
        require(c.get('continuation_start_rva') == lo and c.get('continuation_end_rva') == hi
                and c.get('selection_scope') == 'instruction_starts_first128bytes_whole_instructions_in_parent192', 'continuation scope')
        calls, count = c.get('continuation_calls'), c.get('continuation_call_count')
        require(type(count) is int and 0 <= count <= NODE_CAP and isinstance(calls, list) and len(calls) == min(count, MAX_CALLS)
                and c.get('continuation_calls_truncated') is (count > MAX_CALLS), 'call cap')
        seen = []
        for a in calls:
            at = a.get('site_rva')
            require(type(at) is int and lo <= at < hi and at in ns
                    and a.get('actual_return_argument_buffer_count_or_io_proven') is False, 'continuation call scope')
            identity_guard(a.get('identity', {}), at)
            keys, cap = scoped_inputs(a.get('input_sources', {}), root, ns)
            suffix = a.get('conditional_linear_push_suffix', {})
            suffix_guard(suffix, root, at, keys, cap)
            initial = {(p['site_rva'], r) for p in suffix['pushes'] for r in operand_registers(p['input'])}
            initial.update((at, r) for r in ('eax', 'ebx', 'esi', 'edi', 'ebp'))
            expected = sorted({t['rva'] for q in a['input_sources']['queries'] if (q['site_rva'], q['register']) in initial
                               for t in q['reaching_candidates'] if t['origin'] == 'definition'})
            rows = a.get('direct_input_definition_shapes')
            ordered_rows(rows, MAX_DEFS, root, root + SPAN, ns, keys, cap)
            require(a.get('direct_input_definition_count') == len(expected) and [r['site_rva'] for r in rows] == expected[:MAX_DEFS]
                    and a.get('direct_input_definitions_truncated') is (len(expected) > MAX_DEFS), 'definition-source agreement')
            seen.append(at)
        require(seen == sorted(set(seen)), 'call order')
        keys, cap = scoped_inputs(c.get('continuation_input_sources', {}), root, ns)
        rows, count = c.get('continuation_shapes'), c.get('continuation_shape_count')
        require(type(count) is int and 0 <= count <= NODE_CAP and isinstance(rows, list) and len(rows) == min(count, MAX_SHAPES)
                and c.get('continuation_shapes_truncated') is (count > MAX_SHAPES), 'shape cap')
        ordered_rows(rows, MAX_SHAPES, lo, hi, ns, keys, cap)
        require(all(r['mnemonic'] in ('lea', 'cmp', 'test', 'push') or any(o.get('kind') == 'memory' for o in r['operands']) for r in rows), 'selected syntax')
    def ban(obj):
        if isinstance(obj, dict):
            require(not (set(obj) & FORBIDDEN), 'original payload')
            for v in obj.values():
                ban(v)
        elif isinstance(obj, list):
            for v in obj:
                ban(v)
    ban(d)
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--report', type=Path, required=True)
    p = parser.parse_args().report
    require(p.stat().st_size <= 300000, 'report size')
    validate(json.loads(p.read_text()))
    print('TW10_R41_STRICT_STATIC=PASS; SAVEDATA_PAYLOAD=OPEN')


if __name__ == '__main__':
    main()
