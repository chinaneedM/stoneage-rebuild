"""R28 strict conditional input/caller constraints; immutable custody separate."""
import argparse,json
from pathlib import Path
from tools.stoneage_tw10_savedata_native_io_r28 import *
from tools.stoneage_tw10_savedata_upstream_r22_guard import FORBIDDEN

def check(ok,why):
    if not ok:raise ValueError('R28 '+why)

def validate(d):
    check(isinstance(d,dict) and d.get('schema')==SCHEMA and d.get('status')==STATUS,'schema')
    check(d.get('runtime_sha256')==RUNTIME_SHA256 and d.get('savedata_sha256')==SAVEDATA_SHA256,'hash')
    check(d.get('r27_exact_original_revalidated') is True and d.get('r27_exact_report_sha256')==PRIOR_SHA256
          and d.get('static_only') is True and d.get('third_writefile_and_early_createfile_detail_deferred') is True,'prior scope')
    check(all(d.get(k) is False for k in FLAGS),'runtime promotion')
    contexts=d.get('contexts');check(isinstance(contexts,list) and len(contexts)==3,'contexts')
    for c,(api,caller,root,sites) in zip(contexts,CONTEXTS):
        i=c.get('caller_identity',{})
        check((c.get('api'),c.get('caller_rva'),c.get('root_candidate_rva'))==(api,caller,root)
              and i.get('call_rva')==caller and i.get('kind')=='direct' and i.get('direct_target_rva')==root
              and i.get('runtime_target_or_effects_proven') is False and c.get('supported_by_exact_r27_direct_call') is True
              and c.get('entry_or_call_execution_proven') is False,'caller binding')
        g=c.get('graph',{});frontier=g.get('frontier')
        check(g.get('span_bytes')==MAX_SPAN and g.get('node_cap')==MAX_NODES
              and type(g.get('nodes')) is int and 1<=g['nodes']<=MAX_NODES and type(g.get('edges')) is int
              and 0<=g['edges']<=2*MAX_NODES and type(g.get('node_limit_hit')) is bool
              and isinstance(frontier,list) and len(frontier)<=2*MAX_NODES
              and g.get('call_fallthrough_structural_only') is True and g.get('all_incoming_paths_proven') is False,'graph limits')
        for f in frontier:check(f.get('reason') in ('out_of_window','decode_gap','indirect_jump','node_cap') and type(f.get('rva')) is int,'frontier')
        inp=c.get('inputs',{});queries=inp.get('queries')
        check(isinstance(queries,list) and len(queries)<=MAX_QUERIES and type(inp.get('query_limit_hit')) is bool
              and type(inp.get('pending_query_count')) is int and inp['pending_query_count']>=0
              and inp['query_limit_hit'] is (inp['pending_query_count']>0)
              and inp.get('dependency_depth_limit')==MAX_DEPTH and inp.get('dependency_closure_or_memory_values_proven') is False,'input scope')
        keys=[]
        for q in queries:
            at,reg=q.get('site_rva'),q.get('register');depth=q.get('dependency_depth');sources=q.get('reaching_candidates');deps=q.get('dependency_queries')
            check(type(at) is int and root<=at<root+MAX_SPAN and reg in ALIASES and type(depth) is int and 0<=depth<=MAX_DEPTH
                  and type(q.get('site_in_candidate_graph')) is bool and q.get('actual_register_value_known') is False
                  and isinstance(sources,list) and len(sources)<=24 and type(q.get('candidates_truncated')) is bool
                  and (q['site_in_candidate_graph'] or not sources) and isinstance(deps,list) and len(deps)<=168,'query bounds')
            keys.append((at,reg));expected=set()
            for s in sources:
                check(s.get('origin') in ('definition','unknown_call','entry') and type(s.get('rva')) is int
                      and root<=s['rva']<root+MAX_SPAN,'source identity')
                if s['origin']!='definition':check(s.get('semantic') is None,'opaque source')
                else:
                    check(isinstance(s.get('semantic'),dict),'definition primitive')
                    if depth<MAX_DEPTH:expected.update((s['rva'],r) for r in dependencies(s['semantic']))
            check([(r.get('site_rva'),r.get('register')) for r in deps]==sorted(expected),'dependency shape')
        check(keys==sorted(set(keys)),'unique sorted queries')
        rows=c.get('api_sites');check(isinstance(rows,list) and [r.get('site_rva') for r in rows]==list(sites),'API sites')
        for row in rows:
            at=row['site_rva'];i=row.get('identity',{});imp=i.get('import_identity') or {};geom=i.get('memory_target') or {}
            check(i.get('call_rva')==at and i.get('kind')=='memory_indirect' and imp.get('name')==api
                  and str(imp.get('dll','')).lower()=='kernel32.dll' and i.get('import_slot_association_proven') is True
                  and i.get('runtime_target_or_effects_proven') is False and geom.get('width_bytes')==4
                  and all(geom.get(k) is None for k in ('base_register','index_register','segment_register'))
                  and geom.get('displacement_region',{}).get('displacement_rva')==imp.get('iat_rva'),'API identity')
            anchor=row.get('prior_linear_anchor_rva');post=row.get('conditional_post_call_rva')
            check(type(anchor) is int and root<=anchor<=at and at-anchor<=96 and type(post) is int and at<post<=at+15
                  and type(row.get('site_in_candidate_graph')) is bool and type(row.get('prior_graph_site_reached')) is bool
                  and row.get('actual_external_return_proven') is False,'site scope')
            pushes=row.get('push_candidates');check(isinstance(pushes,list) and len(pushes)<=24,'push cap')
            previous=at
            for n,p in enumerate(pushes):
                shape=p.get('input',{});pa=p.get('site_rva');refs=p.get('source_queries')
                regs=([shape.get('register')] if shape.get('kind')=='register' else [r for r in (shape.get('geometry',{}).get('base_register'),shape.get('geometry',{}).get('index_register')) if r in ALIASES])
                check(type(pa) is int and anchor<=pa<previous and shape.get('width_bytes')==4
                      and p.get('conditional_pre_call_esp_offset')==4*n and p.get('actual_argument_value_or_role_proven') is False
                      and refs==[{'site_rva':pa,'register':r} for r in sorted(set(regs))],'push/query link')
                previous=pa
                check(all((r['site_rva'],r['register']) in keys for r in refs) or inp['query_limit_hit'],'missing push query')
            check(all((at,r) in keys for r in ('eax','ebx','esi','ebp','ecx','edi')) or inp['query_limit_hit'],'missing call queries')
            check((post,'eax') in keys or inp['query_limit_hit'],'missing opaque continuation query')
    def ban(o):
        if isinstance(o,dict):
            check(not set(o)&FORBIDDEN,'proprietary payload')
            for v in o.values():ban(v)
        elif isinstance(o,list):
            for v in o:ban(v)
    ban(d);return True

def main():
    p=argparse.ArgumentParser();p.add_argument('--report',type=Path,required=True)
    path=p.parse_args().report;check(path.stat().st_size<=70000,'size')
    validate(json.loads(path.read_text()));print('TW10_R28_STRICT_STATIC=PASS; NATIVE_SAVE=OPEN')
if __name__=='__main__':main()
