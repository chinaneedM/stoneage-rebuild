"""R29 scalar/address no-promotion gate; original/exact custody separate."""
import argparse,json
from pathlib import Path
from tools.stoneage_tw10_savedata_native_io_r29 import *
from tools.stoneage_tw10_savedata_upstream_r22_guard import FORBIDDEN

def check(ok,why):
    if not ok:raise ValueError('R29 '+why)

def shape_guard(s,at):
    check(s.get('site_rva')==at and s.get('class') in CLASSES|{'unmodeled'}
          and isinstance(s.get('operands'),list) and len(s['operands'])<=8,'shape scope')
    for op in s['operands']:
        check(op.get('kind') in ('register','immediate','memory','unmodeled') and type(op.get('width_bytes')) is int
              and 1<=op['width_bytes']<=16 and type(op.get('decoder_read')) is bool and type(op.get('decoder_write')) is bool,'operand width/access')

def input_guard(s,root):
    qs=s.get('queries');check(isinstance(qs,list) and len(qs)<=64 and type(s.get('query_limit_hit')) is bool
         and type(s.get('pending_query_count')) is int and s['pending_query_count']>=0
         and s['query_limit_hit'] is (s['pending_query_count']>0) and s.get('dependency_depth_limit')==2
         and s.get('dependency_closure_or_memory_values_proven') is False,'input scope')
    keys=[]
    for q in qs:
        at,reg=q.get('site_rva'),q.get('register');sources=q.get('reaching_candidates');deps=q.get('dependency_queries');depth=q.get('dependency_depth')
        check(type(at) is int and root<=at<root+768 and reg in ALIASES and type(depth) is int and 0<=depth<=2
              and type(q.get('site_in_candidate_graph')) is bool and q.get('actual_register_value_known') is False
              and isinstance(sources,list) and len(sources)<=24 and type(q.get('candidates_truncated')) is bool
              and (q['site_in_candidate_graph'] or not sources) and isinstance(deps,list) and len(deps)<=168,'input query')
        expected=set()
        for token in sources:
            check(token.get('origin') in ('entry','definition','unknown_call') and type(token.get('rva')) is int
                  and root<=token['rva']<root+768,'source primitive')
            if token['origin']!='definition':check(token.get('semantic') is None,'opaque CALL/entry')
            else:
                check(isinstance(token.get('semantic'),dict),'definition semantic')
                if depth<2:
                    from tools.stoneage_tw10_savedata_native_io_r28 import dependencies
                    expected.update((token['rva'],r) for r in dependencies(token['semantic']))
        check([(r.get('site_rva'),r.get('register')) for r in deps]==sorted(expected),'dependency shape')
        keys.append((at,reg))
    check(keys==sorted(set(keys)),'query order/uniqueness')
    if not s['query_limit_hit']:
        check(all((r['site_rva'],r['register']) in keys for q in qs for r in q['dependency_queries']),'missing dependency')
    return keys

def validate(d):
    check(isinstance(d,dict) and d.get('schema')==SCHEMA and d.get('status')==STATUS,'schema')
    check(d.get('runtime_sha256')==RUNTIME_SHA256 and d.get('savedata_sha256')==SAVEDATA_SHA256,'hash')
    check(d.get('r28_exact_original_revalidated') is True and d.get('r28_exact_report_sha256')==PRIOR_SHA256
          and d.get('static_only') is True,'prior chain')
    check(all(d.get(k) is False for k in FLAGS),'promotion')
    cs=d.get('contexts');check(isinstance(cs,list) and len(cs)==2,'context count')
    for c,(api,root,sites,address) in zip(cs,ROWS):
        check(c.get('api')==api and c.get('root_candidate_rva')==root and c.get('supported_by_r28_call_root') is True
              and c.get('effective_address_or_table_owner_proven') is False,'root/owner')
        g=c.get('graph',{});front=g.get('frontier')
        check(g.get('span_bytes')==768 and g.get('node_cap')==256 and type(g.get('nodes')) is int and 1<=g['nodes']<=256
              and type(g.get('edges')) is int and 0<=g['edges']<=512 and type(g.get('node_limit_hit')) is bool
              and isinstance(front,list) and len(front)<=512 and g.get('actual_entry_path_proven') is False
              and g.get('returning_call_assumption_only') is True,'graph bounds')
        for f in front:check(f.get('reason') in ('out_of_window','decode_gap','instruction_span_limit','indirect_jump','node_cap') and type(f.get('rva')) is int,'frontier')
        keys=input_guard(c.get('inputs',{}),root)
        rows=c.get('scalar_definitions');check(isinstance(rows,list) and len(rows)==len(sites),'scalar count')
        for r,(at,reg) in zip(rows,sites):
            check((r.get('site_rva'),r.get('written_register_candidate'))==(at,reg) and r.get('supported_by_r28_definition') is True
                  and r.get('actual_value_or_effect_proven') is False,'definition identity')
            shape=r.get('shape',{});shape_guard(shape,at)
            check(r.get('conditional_model')==scalar_model(shape,reg),'conditional expression tamper')
            qs=r.get('input_queries');check(isinstance(qs,list) and 1<=len(qs)<=7
                and {'site_rva':at,'register':reg} in qs and all(q.get('site_rva')==at and q.get('register') in ALIASES for q in qs),'scalar input refs')
            check(all((q['site_rva'],q['register']) in keys for q in qs) or c['inputs']['query_limit_hit'],'missing input')
        s=c.get('shared_address_shape',{});shape_guard(s,address);ops=s['operands'];geom=ops[1].get('geometry',{}) if len(ops)==2 else {}
        check(s['class']=='lea' and len(ops)==2 and ops[0].get('register')=='ebx' and ops[0].get('width_bytes')==4
              and ops[1].get('kind')=='memory' and geom.get('width_bytes')==4 and geom.get('base_register') is None
              and geom.get('index_register')=='eax' and geom.get('index_scale')==4 and geom.get('segment_register') is None
              and geom.get('displacement_region',{}).get('displacement_rva')==SHARED,'shared address shape')
        check((address,'eax') in keys or c['inputs']['query_limit_hit'],'missing index input')
    refs=d.get('shared_address_references',{});lo=refs.get('text_start_rva');size=refs.get('text_bytes');count=refs.get('count');samples=refs.get('samples')
    check(refs.get('scope')=='full_raw_text_exact_displacement_or_immediate_candidates' and refs.get('shared_displacement_rva')==SHARED
          and type(lo) is int and lo>=0 and type(size) is int and 0<size<=1000000 and type(refs.get('decoded_instructions')) is int
          and 0<refs['decoded_instructions']<=size and type(refs.get('decode_gap_bytes')) is int and 0<=refs['decode_gap_bytes']<=size
          and type(count) is int and 0<=count<=8*refs['decoded_instructions'] and isinstance(samples,list) and len(samples)==min(count,MAX_REFS)
          and refs.get('samples_truncated') is (count>MAX_REFS) and refs.get('indirect_alias_complete_or_actual_table_contents_proven') is False,'reference bounds')
    keys=[]
    for r in samples:
        at,n=r.get('site_rva'),r.get('operand_index');op=r.get('operand',{});shape_guard({'site_rva':at,'class':r.get('class'),'operands':[op]},at)
        check(type(at) is int and lo<=at<lo+size and type(n) is int and 0<=n<8 and r.get('actual_read_write_initialization_proven') is False,'reference sample')
        if op.get('kind')=='memory':check(op.get('geometry',{}).get('displacement_region',{}).get('displacement_rva')==SHARED and op['geometry'].get('segment_register') is None,'reference displacement')
        else:check(op.get('kind')=='immediate' and type(op.get('constant')) is int and op['constant']&0xffffffff==0x400000+SHARED,'reference address')
        keys.append((at,n))
    check(keys==sorted(set(keys)),'reference order')
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
    validate(json.loads(path.read_text()));print('TW10_R29_STRICT_STATIC=PASS; NATIVE_SAVE=OPEN')
if __name__=='__main__':main()
