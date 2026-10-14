"""Replay R45 topology/count syntax and API sources; custody checked separately."""
import argparse
import json
from pathlib import Path
from tools.stoneage_tw10_savedata_native_io_r45 import *
from tools.stoneage_tw10_savedata_native_io_r42_guard import inputs_guard
from tools.stoneage_tw10_savedata_native_io_r41_guard import identity_guard
from tools.stoneage_tw10_savedata_native_io_r40_guard import rows_guard, suffix_guard
from tools.stoneage_tw10_savedata_native_io_r37_guard import row_guard
from tools.stoneage_tw10_savedata_native_io_r30_guard import graph_guard
from tools.stoneage_tw10_savedata_upstream_r22_guard import FORBIDDEN


def require(ok,why):
    if not ok:raise ValueError('R45 '+why)


def graph_nodes(c,root,edges=False):
    graph_guard(c.get('graph',{}));ats=c.get('bounded_node_rvas')
    require(isinstance(ats,list) and len(ats)==c['graph']['nodes'] and ats==sorted(set(ats)) and root in ats
            and all(type(at) is int and root<=at<root+768 for at in ats),'graph node scope')
    if edges:
        es=c.get('bounded_edges');require(isinstance(es,list) and len(es)==c['graph']['edges']
            and all(isinstance(e,list) and len(e)==2 and all(type(at) is int and at in ats for at in e) for e in es)
            and es==[list(e) for e in sorted(set(tuple(e) for e in es))],'edge scope/order')
    return ats


def branches_guard(bs,count,capped,root,ats,upper):
    require(type(count) is int and 0<=count<=256 and isinstance(bs,list) and len(bs)==min(count,MAX_BRANCHES)
            and capped is (count>MAX_BRANCHES),'branch sample bound')
    seen=[]
    for b in bs:
        at,n,ss=b.get('branch_site_rva'),b.get('source_count'),b.get('source_candidates')
        require(type(at) is int and root<=at<upper and at in ats and b.get('mnemonic') in ('je','jne','jz','jnz')
                and type(b.get('direct_target_rva')) is int and type(b.get('fallthrough_rva')) is int and at<b['fallthrough_rva']<=at+15
                and type(n) is int and 0<=n<=256 and isinstance(ss,list) and len(ss)==min(n,24)
                and b.get('sources_truncated') is (n>24) and type(b.get('predecessor_nodes_examined')) is int
                and 1<=b['predecessor_nodes_examined']<=512 and type(b.get('predecessor_cap_hit')) is bool
                and type(b.get('branch_disconnected_in_graph')) is bool
                and b.get('actual_flag_value_feasibility_or_taken_path_proven') is False,'branch non-promotion/scope')
        keys,cap=inputs_guard(b.get('input_sources',{}),root,ats);samples=[]
        for s in ss:
            r=s.get('shape',{});a=r.get('site_rva');kind=s.get('kind')
            require(type(a) is int and a in ats and kind in ('zf_write','opaque_call'),'branch source')
            row_guard(r,a,keys,cap)
            if kind=='opaque_call':require(r['mnemonic'] in ('call','lcall'),'flag CALL opacity')
            samples.append((a,kind))
        require(samples==sorted(set(samples)),'source order');seen.append(at)
    require(seen==sorted(set(seen)),'branch order')


def validate(d):
    require(isinstance(d,dict) and d.get('schema')==SCHEMA and d.get('status')==STATUS,'schema')
    require(d.get('runtime_sha256')==RUNTIME_SHA256 and d.get('savedata_sha256')==SAVEDATA_SHA256
            and d.get('r44_exact_original_revalidated') is True and d.get('r44_exact_report_sha256')==PRIOR_SHA256
            and d.get('static_only') is True and all(d.get(k) is False for k in FLAGS),'source/non-promotion')
    c=d.get('read_count_context',{});require(c.get('root_candidate_rva')==READ_ROOT and c.get('actual_count_transformation_branch_or_schema_proven') is False,'read context')
    ats=graph_nodes(c,READ_ROOT,True);keys,cap=inputs_guard(c.get('count_frame_input_sources',{}),READ_ROOT,ats)
    dec,push=c.get('decrement_shape'),c.get('count_push_shape');rows_guard([dec,push],2,READ_ROOT,READ_ROOT+768,keys,cap,ats)
    require([dec['site_rva'],push['site_rva']]==[DEC,COUNT_PUSH]
            and c.get('conditional_count_relationship')==count_relationship(READ_ROOT,c['bounded_edges'],dec,push,c['count_frame_input_sources']),'count source/path replay')
    require(c.get('prior_count_push_overlapping_write_sites')==[DEC]
            and c.get('zf_branch_scope')=='JE_JNE_before_first_API_only_other_condition_flags_not_qualified','prior overlap/flag scope')
    branches_guard(c.get('zf_branch_contexts'),c.get('zf_branch_count'),c.get('zf_branches_truncated'),READ_ROOT,ats,APIS[0][2])
    apis=d.get('native_api_contexts');require(isinstance(apis,list) and len(apis)==2,'API count')
    for a,spec in zip(apis,APIS):
        name,root,site,anchor,slot=spec
        require(a.get('api')==name and a.get('root_candidate_rva')==root and a.get('site_rva')==site and a.get('linear_anchor_rva')==anchor
                and a.get('actual_native_handle_buffer_count_return_or_io_proven') is False,'API context')
        ats=graph_nodes(a,root);require(site in ats,'API node')
        ident=a.get('identity',{});identity_guard(ident,site)
        require(ident.get('kind')=='memory_indirect' and ident.get('import_slot_association_proven') is True
                and ident.get('import_identity')=={'dll':'KERNEL32.dll','name':name,'iat_rva':slot},'exact import/IAT')
        keys,cap=inputs_guard(a.get('input_sources',{}),root,ats);suffix=a.get('physical_push_suffix',{})
        suffix_guard(suffix,anchor,site,keys,cap)
        initial={(p['site_rva'],r) for p in suffix['pushes'] for r in operand_registers(p['input'])}
        initial.update((site,r) for r in ('eax','ebx','ecx','esi','edi','ebp'))
        require(all(q in keys for q in initial) or cap,'API input refs')
        expected=sorted({t['rva'] for q in a['input_sources']['queries'] if (q['site_rva'],q['register']) in initial
                         for t in q['reaching_candidates'] if t['origin']=='definition'})
        rows=a.get('direct_definition_shapes');rows_guard(rows,MAX_DEFS,root,root+768,keys,cap,ats)
        require(a.get('direct_definition_count')==len(expected) and [r['site_rva'] for r in rows]==expected[:MAX_DEFS]
                and a.get('direct_definitions_truncated') is (len(expected)>MAX_DEFS),'API definition agreement')
    w=d.get('delayed_write_context',{});require(w.get('root_candidate_rva')==WRITE_ROOT
                and w.get('same_bound_frame_source_after_call_proven') is False
                and w.get('actual_helper_return_heap_owner_or_frame_preservation_proven') is False,'write unknown effects')
    ats=graph_nodes(w,WRITE_ROOT,True);require(BARRIER in ats and BUFFER_READ in ats,'write barrier nodes')
    keys,cap=inputs_guard(w.get('input_sources',{}),WRITE_ROOT,ats);r=w.get('delayed_buffer_read_shape',{})
    row_guard(r,BUFFER_READ,keys,cap);identity_guard(w.get('barrier_identity',{}),BARRIER)
    suffix_guard(w.get('barrier_physical_push_suffix',{}),WRITE_ROOT,BARRIER,keys,cap)
    require(w.get('barrier_to_buffer_read_structural_path_candidate') is path_without(w['bounded_edges'],BARRIER,BUFFER_READ),'write path replay')
    def ban(o):
        if isinstance(o,dict):
            require(not(set(o)&FORBIDDEN),'original payload')
            for v in o.values():ban(v)
        elif isinstance(o,list):
            for v in o:ban(v)
    ban(d);return True


def main():
    p=argparse.ArgumentParser();p.add_argument('--report',type=Path,required=True)
    path=p.parse_args().report;require(path.stat().st_size<=300000,'report bound')
    validate(json.loads(path.read_text()));print('TW10_R45_STRICT_STATIC=PASS; ACTUAL_NATIVE_SAVE=OPEN')


if __name__=='__main__':main()
