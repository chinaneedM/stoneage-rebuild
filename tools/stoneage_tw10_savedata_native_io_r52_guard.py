"""Independent reverse-predecessor audit of R52 architectural source queries."""
import argparse,json
from collections import deque
from pathlib import Path
from tools.stoneage_tw10_savedata_native_io_r52 import validate as exact_validate,ROOT,REGS,cdq

def reverse_sources(rows,edges,root,site,reg,architecture=True):
    by={r['site_rva']:r for r in rows};rev={a:[] for a in by};adj={a:[] for a in by}
    for a,b in edges:rev[b].append(a);adj[a].append(b)
    if reg not in REGS or root not in by or site not in by:raise ValueError('reverse scope')
    reachable=set();todo=[root]
    while todo:
        a=todo.pop()
        if a not in reachable:reachable.add(a);todo.extend(adj[a])
    if site not in reachable:return set()
    result={('entry',root)} if site==root else set();todo=deque(rev[site]);seen=set()
    while todo:
        a=todo.popleft()
        if a in seen or a not in reachable:continue
        seen.add(a);r=by[a];names=set(r['decoder_written_registers'])
        # Independent family membership, while retaining the exact qualification predicate.
        defines=bool(names&REGS[reg]) and not(architecture and reg=='eax' and cdq(r))
        if r['mnemonic'] in ('call','lcall'):result.add(('unknown_call',a))
        elif defines:result.add(('definition',a))
        else:
            if a==root:result.add(('entry',root))
            todo.extend(rev[a])
    return result

def validate(report,raw):
    exact_validate(report,raw);d=json.loads(raw);rows=d['processor_instruction_shapes'];edges=d['r50_snapshot']['processing_entry_context']['bounded_edges']
    contexts=report['analysis']['signed_division_contexts'];surfaces=[c['source_graph'] for c in contexts]+[c['source_graph'] for c in report['analysis']['r51_pending_definition_source_contexts']]+[report['analysis']['conditional_output_store_context']['source_graph']]
    checked=set()
    for s in surfaces:
        for q in s['queries']:
            expected=reverse_sources(rows,edges,ROOT,q['site_rva'],q['register'])
            actual={(x['origin'],x['site_rva']) for x in q['source_candidates']}
            if expected!=actual:raise ValueError('R52 reverse source mismatch')
            checked.add((q['site_rva'],q['register']))
    for c in contexts:
        for name,reg,arch in [('decoder_eax_source_candidates','eax',False),('qualified_eax_source_candidates','eax',True),('qualified_edx_source_candidates','edx',True)]:
            actual={(x['origin'],x['site_rva']) for x in c[name]}
            if actual!=reverse_sources(rows,edges,ROOT,c['site_rva'],reg,arch):raise ValueError('R52 division source mismatch')
    return len(checked)

def main():
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--report',type=Path,required=True);a=p.parse_args()
    if a.source.stat().st_size>1000000 or a.report.stat().st_size>2000000:raise ValueError('report bound')
    n=validate(json.loads(a.report.read_text()),a.source.read_bytes());print('TW10_R52_REVERSE_SOURCE_AUDIT=PASS; QUERIES='+str(n)+'; ACTUAL_SAVE_SCHEMA=OPEN')
if __name__=='__main__':main()
