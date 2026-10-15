"""Independent R58 reverse-register-source and provenance audit on derived-only JSON.

No original executable, save contents, Windows I/O or imported APIs are run.
The independent predecessor traversal comes from the R52 source-audit framework.
"""
import argparse
import hashlib
import json
from pathlib import Path

from tools.stoneage_tw10_savedata_native_io_r58_guard import validate as validate_r58
from tools.stoneage_tw10_savedata_native_io_r52_guard import reverse_sources
from tools.stoneage_tw10_savedata_return_r57 import analyze

SCHEMA = 'tw10-r58-independent-derived-return-source-contract'
R57_SHA = '3e562ab02a80e0f6516f8a91c93b897eef05f606be62f1df5cb48686d64114e6'


def same(a, b):
    return json.dumps(a, sort_keys=True, separators=(',', ':')) == json.dumps(b, sort_keys=True, separators=(',', ':'))


def reverse_queries(c):
    rows, edges, root = c['instruction_shapes'], c['bounded_edges'], c['root_candidate_rva']
    queries = set()
    for ret in c['return_analysis']['return_contexts']:
        for q in ret['eax_source_graph']['queries']:
            key = (q['site_rva'], q['register'])
            expected = reverse_sources(rows, edges, root, *key, False)
            actual = {(r['origin'], r['site_rva']) for r in q['source_candidates']}
            if expected != actual:
                raise ValueError('R58 independent reverse-source mismatch at ' + str(key))
            queries.add(key)
    return sorted(queries)


def inspect(raw):
    if not isinstance(raw, bytes) or len(raw) > 2000000:
        raise ValueError('R58 bounded raw artifact required')
    report = json.loads(raw)
    validate_r58(report)
    if report.get('exact_r57_report_sha256') != R57_SHA:
        raise ValueError('R58 original R57 custody mismatch')
    result = []
    query_count = 0
    for c in report['contexts']:
        if not same(c['return_analysis'], analyze(c)):
            raise ValueError('R58 independent full return replay')
        qs = reverse_queries(c)
        query_count += len(qs)
        returns = []
        for x in c['return_analysis']['return_contexts']:
            ret_site = x['shape']['site_rva']
            candidates = next(q['source_candidates'] for q in x['eax_source_graph']['queries']
                              if q['site_rva'] == ret_site and q['register'] == 'eax')
            returns.append({
                'return_site_rva': ret_site,
                'direct_eax_source_candidates': candidates,
                'original_return_value_or_error_convention_proven': False,
            })
        contexts = {
            'label': c['label'],
            'root_candidate_rva': c['root_candidate_rva'],
            'r57_wrapper_bridge_sites': [x['call_site_rva'] for x in c['r57_caller_bridges']],
            'rooted_graph_nodes': c['graph']['nodes'],
            'rooted_graph_edges': c['graph']['edges'],
            'bounded_graph_complete': c['bounded_graph_complete'],
            'return_syntax_candidates': returns,
            'predicate_sites': [x['branch_site_rva'] for x in c['return_analysis']['predicate_contexts']],
            'opaque_call_sites': c['return_analysis']['opaque_call_sites'],
            'explicit_memory_write_sites': [r['site_rva'] for r in c['return_analysis']['explicit_memory_write_shapes']],
            'reverse_query_count': len(qs),
            'actual_file_descriptor_ownership_flush_close_written_bytes_or_persistence_proven': False,
        }
        result.append(contexts)
    return {
        'schema': SCHEMA,
        'source_sha256': hashlib.sha256(raw).hexdigest(),
        'source_static_original_custody_verified': True,
        'independent_reverse_queries': query_count,
        'contexts': result,
        'actual_runtime_path_memory_values_error_semantics_or_native_persistence_proven': False,
    }


def verify(contract, raw):
    if not same(contract, inspect(raw)):
        raise ValueError('R58 independent contract mismatch')
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--report', type=Path, required=True)
    ap.add_argument('--verify', type=Path)
    args = ap.parse_args()
    raw = args.report.read_bytes()
    if args.verify:
        verify(json.loads(args.verify.read_text()), raw)
        print('TW10_R58_INDEPENDENT_REVERSE=PASS; ACTUAL_NATIVE_PERSISTENCE=OPEN')
    else:
        print(json.dumps(inspect(raw), sort_keys=True))


if __name__ == '__main__':
    main()
