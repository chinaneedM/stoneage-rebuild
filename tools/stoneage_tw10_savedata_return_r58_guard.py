"""R58 independent reverse-register return-source audit over pinned static metadata.

Input is derived nonexecuting instruction/graph records. Native result/persistence unknown.
"""
import argparse
import json
from pathlib import Path
from tools.stoneage_tw10_savedata_native_io_r58_guard import validate
from tools.stoneage_tw10_savedata_native_io_r52_guard import reverse_sources

def audit(report):
    validate(report)
    total = 0
    result = []
    for context in report['contexts']:
        if context['graph']['frontier'] or context['graph']['node_limit_hit'] or not context['bounded_graph_complete']:
            raise ValueError('R58 graph incomplete for independent admission')
        root = context['root_candidate_rva']
        count = 0
        for ret in context['return_analysis']['return_contexts']:
            for query in ret['eax_source_graph']['queries']:
                expected = reverse_sources(context['instruction_shapes'],
                                           context['bounded_edges'], root,
                                           query['site_rva'], query['register'], False)
                received = {(x['origin'], x['site_rva']) for x in query['source_candidates']}
                if expected != received:
                    raise ValueError('R58 independent return query mismatch')
                count += 1
        if not count:
            raise ValueError('R58 no return-source queries')
        total += count
        result.append({'root_candidate_rva': root,
                       'nodes': context['graph']['nodes'],
                       'edges': context['graph']['edges'],
                       'return_source_queries': count,
                       'predicates': len(context['return_analysis']['predicate_contexts']),
                       'memory_write_shapes': len(context['return_analysis']['explicit_memory_write_shapes']),
                       'actual_native_persistence_proven': False})
    return {'contexts': result, 'total_return_source_queries': total,
            'actual_native_persistence_proven': False}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    if args.report.stat().st_size > 2000000:
        raise ValueError('R58 size bound')
    summary = audit(json.loads(args.report.read_text()))
    print('TW10_R58_INDEPENDENT_REVERSE_RETURNS=PASS; QUERIES=' +
          str(summary['total_return_source_queries']) +
          '; ACTUAL_NATIVE_PERSISTENCE=OPEN')
    print(json.dumps(summary, sort_keys=True))

if __name__ == '__main__':
    main()
