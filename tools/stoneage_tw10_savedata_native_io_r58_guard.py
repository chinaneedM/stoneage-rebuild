"""Fail-closed static R58 source inventory, bridge and return replay."""
import argparse
import json
from pathlib import Path
from tools.stoneage_tw10_savedata_native_io_r58 import (
    SCHEMA, R57_SHA256, TARGETS, FLAGS, find_bridges,
)
from tools.stoneage_tw10_savedata_native_io_r57 import RUNTIME_SHA256, SAVEDATA_SHA256
from tools.stoneage_tw10_savedata_return_r57 import analyze
from tools.stoneage_tw10_savedata_native_io_r41_guard import identity_guard
from tools.stoneage_tw10_savedata_native_io_r45_guard import graph_nodes
from tools.stoneage_tw10_savedata_native_io_r40_guard import rows_guard, suffix_guard
from tools.stoneage_tw10_savedata_native_io_r42_guard import inputs_guard
from tools.stoneage_tw10_savedata_application_r51 import same
from tools.stoneage_tw10_savedata_upstream_r22_guard import FORBIDDEN

def req(condition, reason):
    if not condition:
        raise ValueError('R58 ' + reason)

def validate(report):
    req(isinstance(report, dict) and report.get('schema') == SCHEMA
        and report.get('static_only') is True
        and report.get('runtime_sha256') == RUNTIME_SHA256
        and report.get('savedata_sha256') == SAVEDATA_SHA256
        and report.get('exact_r57_report_sha256') == R57_SHA256
        and report.get('exact_r57_requalified') is True
        and report.get('entrygraph_node_limit_hit') is False
        and all(report.get(k) is False for k in FLAGS), 'provenance/non-promotion')
    contexts = report.get('contexts')
    req(isinstance(contexts, list) and len(contexts) == len(TARGETS), 'context count')
    for c, (label, root, parents) in zip(contexts, TARGETS):
        req(c.get('label') == label and c.get('root_candidate_rva') == root
            and c.get('entrygraph_boundary_seen') is True
            and c.get('actual_path_or_callee_effects_proven') is False, 'root scope')
        bridges = c.get('r57_caller_bridges')
        seen = c.get('r57_wrapper_edges_seen_in_entrygraph')
        req(isinstance(bridges, list) and len(bridges) == len(parents)
            and seen == [True] * len(parents), 'edge custody')
        for bridge, (wrapper, call) in zip(bridges, parents):
            req(bridge.get('wrapper_root_rva') == wrapper
                and bridge.get('call_site_rva') == call
                and bridge.get('target_rva') == root, 'bridge geometry')
            identity_guard(bridge['r57_direct_identity'], call)
            req(bridge['r57_direct_identity']['direct_target_rva'] == root,
                'bridge target')
        ats = graph_nodes(c, root, True)
        rows = c['instruction_shapes']
        keys = {(r['site_rva'], reg) for r in rows for reg in r['input_query_registers']}
        rows_guard(rows, 256, root, root + 768, keys, False, ats)
        req([r['site_rva'] for r in rows] == ats
            and c.get('instruction_shapes_truncated') is False, 'complete rows')
        calls = c['call_contexts']
        req(len(calls) <= 16 and [call['site_rva'] for call in calls]
            == [row['site_rva'] for row in rows if row['mnemonic'] == 'call'],
            'call census')
        for call in calls:
            site = call['site_rva']
            identity_guard(call['identity'], site)
            inputs, cap = inputs_guard(call['input_sources'], root, ats)
            suffix_guard(call['physical_push_suffix'], root, site, set(inputs), cap)
            rows_guard(call['direct_input_definition_shapes'], 24,
                       root, root + 768, set(inputs), cap, ats)
            req(call.get('actual_argument_values_roles_return_or_callee_effects_proven')
                is False, 'call effects')
        req(same(c['return_analysis'], analyze(c)), 'independent return replay')
        graph = c['graph']
        complete = (not graph['node_limit_hit'] and not graph['frontier']
                    and bool(c['return_analysis']['return_contexts']))
        req(c.get('bounded_graph_complete') is complete, 'graph completeness')
    def prohibit(obj):
        if isinstance(obj, dict):
            req(not (set(obj) & FORBIDDEN), 'proprietary payload')
            for v in obj.values():
                prohibit(v)
        elif isinstance(obj, list):
            for v in obj:
                prohibit(v)
    prohibit(report)
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--report', type=Path, required=True)
    path = parser.parse_args().report
    req(path.stat().st_size <= 2000000, 'report bound')
    validate(json.loads(path.read_text()))
    print('TW10_R58_ROOTED_HELPER_STATIC=PASS; ACTUAL_NATIVE_PERSISTENCE=OPEN')

if __name__ == '__main__':
    main()
