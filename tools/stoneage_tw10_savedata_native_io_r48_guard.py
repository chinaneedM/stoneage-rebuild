"""Strict count/return/loop replay; opaque calls and alias boundaries preserved."""
import argparse
import json
from pathlib import Path
from tools.stoneage_tw10_savedata_native_io_r48 import *
from tools.stoneage_tw10_savedata_native_io_r45_guard import graph_nodes, branches_guard
from tools.stoneage_tw10_savedata_native_io_r42_guard import inputs_guard
from tools.stoneage_tw10_savedata_native_io_r40_guard import rows_guard
from tools.stoneage_tw10_savedata_native_io_r37_guard import direct_guard
from tools.stoneage_tw10_savedata_upstream_r22_guard import FORBIDDEN


def require(ok,why):
    if not ok:raise ValueError('R48 '+why)


def returns_guard(s,root,ats):
    require(s.get('actual_return_values_abi_or_return_effects_proven') is False,'return non-promotion')
    keys,cap=inputs_guard(s.get('input_sources',{}),root,ats);rs=s.get('return_shapes');n=s.get('return_count')
    rows_guard(rs,MAX_RETURN_ROWS,root,root+768,keys,cap,ats)
    require(type(n) is int and 0<=n<=256 and len(rs)==min(n,MAX_RETURN_ROWS) and s.get('returns_truncated') is (n>MAX_RETURN_ROWS)
            and all(r['mnemonic'] in ('ret','retf') for r in rs),'return sample')
    initial={(r['site_rva'],reg) for r in rs for reg in ('eax','ebp')}
    require(all(k in keys for k in initial) or cap,'return queries')
    defs=sorted({t['rva'] for q in s['input_sources']['queries'] if (q['site_rva'],q['register']) in initial for t in q['reaching_candidates'] if t['origin']=='definition'})
    rows=s.get('direct_return_definition_shapes');rows_guard(rows,MAX_DEFS,root,root+768,keys,cap,ats)
    require(s.get('direct_return_definition_count')==len(defs) and [r['site_rva'] for r in rows]==defs[:MAX_DEFS]
            and s.get('return_definitions_truncated') is (len(defs)>MAX_DEFS),'return definition replay')


def validate(d):
    require(isinstance(d,dict) and d.get('schema')==SCHEMA and d.get('status')==STATUS,'schema/status')
    require(d.get('runtime_sha256')==RUNTIME_SHA256 and d.get('savedata_sha256')==SAVEDATA_SHA256 and d.get('static_only') is True
            and d.get('r47_exact_original_revalidated') is True and d.get('r47_exact_report_sha256')==PRIOR_SHA256
            and all(d.get(f) is False for f in FLAGS),'source/non-promotion')
    c=d.get('native_count_return_context',{});require(c.get('root_candidate_rva')==READ_ROOT and c.get('actual_native_api_bytes_or_aggregate_return_proven') is False,'native scope')
    ats=graph_nodes(c,READ_ROOT,True);keys,cap=inputs_guard(c.get('input_sources',{}),READ_ROOT,ats)
    rows=c.get('count_shapes');rows_guard(rows,3,READ_ROOT,READ_ROOT+768,keys,cap,ats)
    require([r['site_rva'] for r in rows]==[COUNT_LOAD,ACCUM,RETURN_LOAD],'count sites')
    require(c.get('conditional_count_relation')==count_relation(rows,c['input_sources'],c['bounded_edges']),'count source/path replay')
    auditrows=c.get('return_memory_predecessor_shapes');rows_guard(auditrows,MAX_AUDIT,READ_ROOT,READ_ROOT+768,keys,cap,ats)
    audit=c.get('return_memory_boundary_audit',{});by={r['site_rva']:r for r in auditrows}
    expected=memory_audit(by,c['bounded_edges'],READ_ROOT,RETURN_LOAD,rows[-1]['operands'][1])
    require(audit==expected and [r['site_rva'] for r in auditrows]==audit['visited_predecessor_rvas']
            and all(x['kind']!='missing_shape' for x in audit['terminal_candidates']),'memory boundary replay/completeness')
    for r in rows:
        if r['site_rva'] in by:require(r==by[r['site_rva']],'count/audit row agreement')
    returns_guard(c.get('return_surface',{}),READ_ROOT,ats)
    w=d.get('wrapper_loop_division_context',{});require(w.get('root_candidate_rva')==WRAPPER
            and w.get('actual_wrapper_count_or_division_result_native_binding_proven') is False,'wrapper scope')
    ats=graph_nodes(w,WRAPPER,True);require(NATIVE_CALL in ats,'native call node')
    direct_guard(w.get('native_call_identity',{}),NATIVE_CALL,READ_ROOT)
    keys,cap=inputs_guard(w.get('input_sources',{}),WRAPPER,ats);rows=w.get('post_native_shapes')
    rows_guard(rows,MAX_WRAPPER_ROWS,NATIVE_CALL+5,WRAPPER+768,keys,cap,ats)
    expected=[a for a in ats if a>=NATIVE_CALL+5]
    require(w.get('post_native_shape_count')==len(expected) and [r['site_rva'] for r in rows]==expected[:MAX_WRAPPER_ROWS]
            and w.get('post_native_shapes_truncated') is (len(expected)>MAX_WRAPPER_ROWS) and set(CONSUMERS)<=set(r['site_rva'] for r in rows),'wrapper sample')
    require(w.get('conditional_consumer_relation')==consumer_relation(rows,w['input_sources'],w['bounded_edges']),'consumer loop/source replay')
    bs=w.get('native_result_test_branches');branches_guard(bs,2,False,WRAPPER,ats,WRAPPER+768)
    require([b['branch_site_rva'] for b in bs]==list(BRANCHES),'wrapper result branches')
    dkeys,dcap=inputs_guard(w.get('division_input_sources',{}),WRAPPER,ats);divs=w.get('division_shapes');n=w.get('division_count')
    rows_guard(divs,MAX_DIVISIONS,WRAPPER,WRAPPER+768,dkeys,dcap,ats)
    require(type(n) is int and 0<=n<=256 and len(divs)==min(n,MAX_DIVISIONS) and w.get('divisions_truncated') is (n>MAX_DIVISIONS)
            and all(r['mnemonic'] in ('div','idiv') and len(r['operands'])==1 for r in divs),'division syntax/sample')
    by={r['site_rva']:r for r in rows}
    for r in divs:
        if r['site_rva'] in by:require(r==by[r['site_rva']],'division/postcall agreement')
    returns_guard(w.get('return_surface',{}),WRAPPER,ats)
    def ban(o):
        if isinstance(o,dict):
            require(not(set(o)&FORBIDDEN),'original payload')
            for v in o.values():ban(v)
        elif isinstance(o,list):
            for v in o:ban(v)
    ban(d);return True


def main():
    p=argparse.ArgumentParser();p.add_argument('--report',type=Path,required=True);path=p.parse_args().report
    require(path.stat().st_size<=300000,'report bound');validate(json.loads(path.read_text()))
    print('TW10_R48_STRICT_STATIC=PASS; ACTUAL_NATIVE_SAVE=OPEN')


if __name__=='__main__':main()
