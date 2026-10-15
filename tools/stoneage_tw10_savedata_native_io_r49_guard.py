"""Strict R49 source/temporal-slot replay, without runtime promotion."""
import argparse
import json
from pathlib import Path
from tools.stoneage_tw10_savedata_native_io_r49 import *
from tools.stoneage_tw10_savedata_native_io_r45_guard import graph_nodes, branches_guard
from tools.stoneage_tw10_savedata_native_io_r42_guard import inputs_guard
from tools.stoneage_tw10_savedata_native_io_r40_guard import rows_guard
from tools.stoneage_tw10_savedata_native_io_r37_guard import direct_guard
from tools.stoneage_tw10_savedata_upstream_r22_guard import FORBIDDEN


def require(ok,why):
    if not ok:raise ValueError('R49 '+why)


def surface_guard(s,root,ats,initial):
    keys,cap=inputs_guard(s.get('input_sources',{}),root,ats);rows=s.get('source_definition_shapes')
    rows_guard(rows,MAX_DEFS,root,root+768,keys,cap,ats)
    sites=sorted({t['rva'] for q in s['input_sources']['queries'] for t in q['reaching_candidates'] if t['origin']=='definition'})
    pending=s.get('source_expansion_pending_definition_rvas')
    require(isinstance(pending,list) and pending==sorted(set(pending)) and set(pending)<=set(sites) and not(set(pending)&{r['site_rva'] for r in rows}),'pending definition scope')
    require(s.get('source_definition_count')==len(sites) and s.get('source_definitions_truncated') is (len(sites)>MAX_DEFS)
            and s.get('source_expansion_rounds')==SOURCE_ROUNDS
            and [r['site_rva'] for r in rows]==[a for a in sites[:MAX_DEFS] if a not in pending],'source bounds/agreement')
    rows_guard(initial,len(initial),root,root+768,keys,cap,ats)
    return keys,cap


def audit_guard(a,rows,inputs,root,ats,edges,read,reference):
    keys,cap=inputs_guard(inputs,root,ats);rows_guard(rows,MAX_AUDIT,root,root+768,keys,cap,ats)
    expected=memory_audit({r['site_rva']:r for r in rows},edges,root,read,reference)
    require(a==expected and [r['site_rva'] for r in rows]==a['visited_predecessor_rvas']
            and all(t['kind']!='missing_shape' for t in a['terminal_candidates']),'memory audit completeness/replay')


def validate(d):
    require(isinstance(d,dict) and d.get('schema')==SCHEMA and d.get('status')==STATUS,'schema/status')
    require(d.get('runtime_sha256')==RUNTIME_SHA256 and d.get('savedata_sha256')==SAVEDATA_SHA256 and d.get('static_only') is True
            and d.get('r48_exact_original_revalidated') is True and d.get('r48_exact_report_sha256')==PRIOR_SHA256
            and all(d.get(f) is False for f in FLAGS),'source/non-promotion')
    c=d.get('native_overwrite_context',{});require(c.get('root_candidate_rva')==READ_ROOT and c.get('actual_native_count_or_overwrite_execution_proven') is False,'native scope')
    ats=graph_nodes(c,READ_ROOT,True);r=c.get('overwrite_shape');require(r.get('site_rva')==OVERWRITE,'overwrite site')
    surface_guard(c.get('edi_source_surface',{}),READ_ROOT,ats,[r])
    require(c.get('conditional_overwrite_link')==overwrite_link(r,c['edi_source_surface']),'overwrite source replay')
    audit_guard(c.get('pre_overwrite_memory_audit'),c.get('pre_overwrite_memory_shapes'),c.get('pre_overwrite_input_sources'),READ_ROOT,ats,c['bounded_edges'],OVERWRITE,r['operands'][0])
    b=c.get('bypass_branch_context',{});branches_guard([b],1,False,READ_ROOT,ats,READ_ROOT+768)
    require(b.get('branch_site_rva')==BYPASS and b['direct_target_rva'] in ats and b['fallthrough_rva'] in ats
            and [BYPASS,b['direct_target_rva']] in c['bounded_edges'] and [BYPASS,b['fallthrough_rva']] in c['bounded_edges'],'bypass edge agreement')
    require(c.get('branch_target_to_return_avoiding_overwrite_candidate') is path_without(c['bounded_edges'],b['direct_target_rva'],RETURN_LOAD,OVERWRITE)
            and c.get('branch_fallthrough_to_overwrite_candidate') is path_without(c['bounded_edges'],b['fallthrough_rva'],OVERWRITE)
            and c.get('overwrite_to_return_load_candidate') is path_without(c['bounded_edges'],OVERWRITE,RETURN_LOAD),'overwrite path replay')
    w=d.get('wrapper_temporal_slot_context',{});require(w.get('root_candidate_rva')==WRAPPER and w.get('actual_product_slot_dividend_divisor_or_quotient_proven') is False,'wrapper scope')
    ats=graph_nodes(w,WRAPPER,True);direct_guard(w.get('native_call_identity',{}),NATIVE_CALL,READ_ROOT)
    frames,seeds,divs=w.get('frame_plus20_shapes'),w.get('product_remaining_numerator_shapes'),w.get('division_shapes')
    require(isinstance(frames,list) and isinstance(seeds,list) and isinstance(divs,list),'wrapper row surfaces')
    keys,cap=surface_guard(w.get('temporal_source_surface',{}),WRAPPER,ats,sorted({r['site_rva']:r for r in frames+seeds+divs}.values(),key=lambda r:r['site_rva']))
    rows_guard(frames,MAX_FRAME_ROWS,WRAPPER,WRAPPER+768,keys,cap,ats)
    rows_guard(seeds,len(SEEDS),WRAPPER,WRAPPER+768,keys,cap,ats);rows_guard(divs,2,WRAPPER,WRAPPER+768,keys,cap,ats)
    n=w.get('frame_plus20_instruction_count');require(type(n) is int and 0<=n<=256 and len(frames)==min(n,MAX_FRAME_ROWS)
            and w.get('frame_plus20_shapes_truncated') is (n>MAX_FRAME_ROWS) and all(slot_refs([r],20) for r in frames),'frame reference sample')
    require([r['site_rva'] for r in seeds]==list(SEEDS) and [r['site_rva'] for r in divs]==list(DIVS),'seed/division sites')
    require(w.get('frame_plus20_reference_candidates')==slot_refs(frames,20)
            and w.get('frame_plus20_write_source_links')==write_source_links(frames,w['temporal_source_surface']),'temporal slot source replay')
    audits=w.get('division_memory_boundary_audits');require(isinstance(audits,list) and len(audits)==2,'division audits')
    for a,div in zip(audits,divs):
        require(a.get('division_site_rva')==div['site_rva'],'division audit site')
        audit_guard(a.get('audit'),a.get('predecessor_shapes'),a.get('input_sources'),WRAPPER,ats,w['bounded_edges'],div['site_rva'],div['operands'][0])
    by={}
    for row in frames+seeds+divs+w['temporal_source_surface']['source_definition_shapes']:
        at=row['site_rva']
        if at in by:require(by[at]==row,'cross-surface instruction agreement')
        by[at]=row
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
    print('TW10_R49_STRICT_STATIC=PASS; ACTUAL_NATIVE_SAVE=OPEN')


if __name__=='__main__':main()
