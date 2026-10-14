"""Replay R42 conditional geometry/topology; custody/equality is independent."""
import argparse
import json
from pathlib import Path
from tools.stoneage_tw10_savedata_native_io_r42 import *
from tools.stoneage_tw10_savedata_native_io_r37_guard import row_guard, direct_guard
from tools.stoneage_tw10_savedata_native_io_r40_guard import rows_guard, suffix_guard
from tools.stoneage_tw10_savedata_native_io_r41_guard import identity_guard
from tools.stoneage_tw10_savedata_native_io_r29_guard import input_guard, shape_guard
from tools.stoneage_tw10_savedata_native_io_r30_guard import graph_guard
from tools.stoneage_tw10_savedata_upstream_r22_guard import FORBIDDEN


def require(ok, why):
    if not ok:raise ValueError('R42 ' + why)


def inputs_guard(s, root, ats):
    keys = input_guard(s, root)
    require(all(q['site_in_candidate_graph'] is (q['site_rva'] in ats)
                and all(t['rva'] in ats for t in q['reaching_candidates']) for q in s['queries']), 'source/node agreement')
    return keys, s['query_limit_hit']


def validate(d):
    require(isinstance(d, dict) and d.get('schema') == SCHEMA and d.get('status') == STATUS, 'schema')
    require(d.get('runtime_sha256') == RUNTIME_SHA256 and d.get('savedata_sha256') == SAVEDATA_SHA256
            and d.get('r41_exact_original_revalidated') is True and d.get('r41_exact_report_sha256') == PRIOR_SHA256
            and d.get('static_only') is True and all(d.get(k) is False for k in FLAGS), 'source/non-promotion')
    e = d.get('entrygraph_support', {})
    require(type(e.get('entrypoint_rva')) is int and type(e.get('visited_nodes')) is int and 1 <= e['visited_nodes'] <= 120000
            and type(e.get('edges')) is int and 0 <= e['edges'] <= 240000 and type(e.get('node_limit_hit')) is bool
            and e.get('direct_cfg_candidate_only') is True and e.get('complete_cfg_or_actual_execution_proven') is False, 'entry support')
    ws = d.get('wrappers');require(isinstance(ws, list) and len(ws) == 2, 'wrapper count')
    for w, spec in zip(ws, WRAPPERS):
        label, root, call, target, callers = spec
        require(w.get('label') == label and w.get('root_candidate_rva') == root
                and w.get('actual_function_entry_or_execution_proven') is False
                and w.get('actual_native_argument_buffer_count_or_savedata_io_proven') is False
                and w.get('structural_path_requires_opaque_calls_to_return') is True, 'wrapper context')
        require(all(type(w.get(k)) is bool for k in ('entrygraph_wrapper_boundary_seen', 'entrygraph_native_call_boundary_seen',
                'entrygraph_native_target_boundary_seen', 'entrygraph_native_call_target_edge_seen')), 'boundary syntax')
        graph_guard(w.get('graph', {}))
        effects, edges = w.get('stack_effect_candidates'), w.get('bounded_edges')
        require(isinstance(effects, list) and len(effects) == w['graph']['nodes'], 'effect count')
        ats = []
        for effect in effects:
            at, kind, delta, width = (effect.get(k) for k in ('site_rva', 'syntax_class', 'esp_delta', 'operand_width_bytes'))
            require(type(at) is int and root <= at < root + 768 and kind in ('neutral', 'push', 'pop', 'opaque_call', 'unknown_esp_write')
                    and effect.get('conditional_32bit_stack_address_only') is True, 'effect scope')
            if kind in ('push', 'pop'):
                require(type(width) is int and width in (2, 4) and type(delta) is int and delta == (-width if kind == 'push' else width), 'effect arithmetic')
            else:
                require(width is None and (type(delta) is int and delta == 0 if kind == 'neutral' else delta is None), 'opaque stack change')
            ats.append(at)
        require(ats == sorted(set(ats)) and root in ats and call in ats, 'effect topology')
        require(isinstance(edges, list) and len(edges) == w['graph']['edges']
                and all(isinstance(e, list) and len(e) == 2 and all(type(a) is int and a in ats for a in e) for e in edges)
                and edges == [list(e) for e in sorted(set(tuple(e) for e in edges))], 'graph edge order')
        states, updates, limit = stack_states(effects, edges, root)
        require(w.get('stack_model_updates') == updates and w.get('stack_model_update_limit_hit') is limit, 'stack replay')
        keys, cap = inputs_guard(w.get('frame_input_sources', {}), root, ats)
        rows, defs, prolog = (w.get(k) for k in ('early_stack_read_or_multiply_shapes', 'frame_definition_shapes', 'entry_prolog_shapes'))
        count = w.get('early_stack_read_or_multiply_count')
        require(type(count) is int and 0 <= count <= 256 and isinstance(rows, list) and len(rows) == min(count, MAX_EARLY)
                and w.get('early_shapes_truncated') is (count > MAX_EARLY)
                and w.get('early_shape_scope') == 'instruction_starts_first96bytes_whole_instructions_in_parent768', 'early sample bound')
        rows_guard(rows, MAX_EARLY, root, root + 96, keys, cap, ats)
        require(all(r['mnemonic'] in ('mul', 'imul') or (r['mnemonic'] != 'lea' and any(o.get('kind') == 'memory' and o.get('decoder_read')
                and o.get('geometry', {}).get('base_register') in ('esp', 'ebp') for o in r['operands'])) for r in rows), 'early syntax')
        rows_guard(prolog, 24, root, root + 24, keys, cap, ats)
        require(all(set(r['decoder_written_registers']) & {'esp', 'ebp'} for r in prolog), 'prolog writes')
        expected = sorted({s['rva'] for q in w['frame_input_sources']['queries'] if q['register'] == 'ebp'
                           for s in q['reaching_candidates'] if s['origin'] == 'definition'})
        rows_guard(defs, MAX_DEFS, root, root + 768, keys, cap, ats)
        require(w.get('frame_definition_count') == len(expected) and [r['site_rva'] for r in defs] == expected[:MAX_DEFS]
                and w.get('frame_definitions_truncated') is (len(expected) > MAX_DEFS), 'frame source agreement')
        summaries = [state_summary(states, r['site_rva'], limit) for r in defs]
        require(w.get('frame_definition_esp_summaries') == summaries, 'frame summary replay')
        bs = w.get('savedata_caller_bridges');require(isinstance(bs, list) and len(bs) == len(callers), 'caller count')
        for b, (parent, caller) in zip(bs, callers):
            require(b.get('parent_filename_push_rva') == parent and b.get('caller_site_rva') == caller
                    and b.get('actual_caller_wrapper_parameter_or_owner_binding_proven') is False
                    and type(b.get('entrygraph_caller_boundary_seen')) is bool and type(b.get('entrygraph_call_to_wrapper_edge_seen')) is bool, 'caller identity')
            direct_guard(b.get('caller_identity', {}), caller, root)
            pushes = b.get('prior_caller_push_candidates');require(isinstance(pushes, list) and len(pushes) <= 24, 'caller push bound')
            last = caller
            for i, p in enumerate(pushes):
                at = p.get('site_rva');op = p.get('input', {})
                require(type(at) is int and parent <= at < last and p.get('conditional_pre_call_esp_offset') == i * 4 and op.get('width_bytes') == 4, 'caller push geometry')
                shape_guard({'site_rva': at, 'class': 'unmodeled', 'operands': [op]}, at);last = at
            require(b.get('conditional_frame_slot_bridges') == [frame_bridge(r, w['frame_input_sources'], defs, summaries, pushes) for r in rows], 'slot bridge replay')
        branches, count = w.get('pre_native_zf_branches'), w.get('pre_native_zf_branch_count')
        require(type(count) is int and 0 <= count <= 256 and isinstance(branches, list) and len(branches) == min(count, MAX_BRANCHES)
                and w.get('pre_native_zf_branches_truncated') is (count > MAX_BRANCHES), 'branch cap')
        seen = []
        for b in branches:
            at, n, sources = b.get('branch_site_rva'), b.get('source_count'), b.get('source_candidates')
            require(type(at) is int and root <= at < call and at in ats and b.get('mnemonic') in ('je', 'jne', 'jz', 'jnz')
                    and type(b.get('direct_target_rva')) is int and type(b.get('fallthrough_rva')) is int and at < b['fallthrough_rva'] <= at + 15
                    and type(n) is int and 0 <= n <= 256 and isinstance(sources, list) and len(sources) == min(n, MAX_SOURCE_SAMPLES)
                    and b.get('sources_truncated') is (n > MAX_SOURCE_SAMPLES) and type(b.get('predecessor_nodes_examined')) is int
                    and 1 <= b['predecessor_nodes_examined'] <= 512 and type(b.get('predecessor_cap_hit')) is bool
                    and type(b.get('branch_disconnected_in_graph')) is bool
                    and b.get('actual_flag_value_feasibility_or_taken_path_proven') is False, 'branch scope/non-promotion')
            bk, bc = inputs_guard(b.get('input_sources', {}), root, ats);ss = []
            for source in sources:
                row = source.get('shape', {});a = row.get('site_rva');kind = source.get('kind')
                require(type(a) is int and a in ats and kind in ('zf_write', 'opaque_call'), 'ZF source scope')
                row_guard(row, a, bk, bc)
                if kind == 'opaque_call':require(row['mnemonic'] in ('call', 'lcall'), 'CALL flag barrier')
                ss.append((a, kind))
            require(ss == sorted(set(ss)), 'source order');seen.append(at)
        require(seen == sorted(set(seen)), 'branch order')
        calls, count = w.get('call_candidates'), w.get('call_candidate_count')
        require(type(count) is int and 1 <= count <= 256 and isinstance(calls, list) and len(calls) == min(count, MAX_CALLS)
                and w.get('call_candidates_truncated') is (count > MAX_CALLS), 'call sample bound')
        for c in calls:
            at = c.get('call_rva');require(type(at) is int and at in ats, 'CALL membership');identity_guard(c, at)
            require(next(e['syntax_class'] for e in effects if e['site_rva'] == at) == 'opaque_call', 'CALL opacity')
        require([c['call_rva'] for c in calls] == sorted(set(c['call_rva'] for c in calls)), 'call order')
        a = w.get('native_context_call', {});direct_guard(a.get('identity', {}), call, target)
        require(a.get('site_rva') == call and a.get('actual_return_argument_buffer_count_or_io_proven') is False, 'native no-promotion')
        ak, ac = inputs_guard(a.get('input_sources', {}), root, ats)
        suffix = a.get('conditional_linear_push_suffix', {});suffix_guard(suffix, root, call, ak, ac)
        initial = {(p['site_rva'], r) for p in suffix['pushes'] for r in operand_registers(p['input'])}
        initial.update((call, r) for r in ('eax', 'ebx', 'esi', 'edi', 'ebp'))
        expected = sorted({s['rva'] for q in a['input_sources']['queries'] if (q['site_rva'], q['register']) in initial
                           for s in q['reaching_candidates'] if s['origin'] == 'definition'})
        rows = a.get('direct_input_definition_shapes');rows_guard(rows, 12, root, root + 768, ak, ac, ats)
        require(a.get('direct_input_definition_count') == len(expected) and [r['site_rva'] for r in rows] == expected[:12]
                and a.get('direct_input_definitions_truncated') is (len(expected) > 12), 'native source agreement')
        require(w.get('structural_root_to_native_call_candidate') is graph_path(edges, root, call, cap=256), 'path replay')
    def ban(obj):
        if isinstance(obj, dict):
            require(not (set(obj) & FORBIDDEN), 'original payload')
            for v in obj.values():ban(v)
        elif isinstance(obj, list):
            for v in obj:ban(v)
    ban(d);return True


def main():
    p = argparse.ArgumentParser();p.add_argument('--report', type=Path, required=True)
    path = p.parse_args().report;require(path.stat().st_size <= 300000, 'report size')
    validate(json.loads(path.read_text()));print('TW10_R42_STRICT_STATIC=PASS; ACTUAL_SAVEDATA_PAYLOAD=OPEN')


if __name__ == '__main__':main()
