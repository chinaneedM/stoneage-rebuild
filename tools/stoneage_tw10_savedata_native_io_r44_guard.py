"""Replay R44 literal ESP arithmetic, slots/prefixes and mutable source models."""
import argparse
import json
from pathlib import Path
from tools.stoneage_tw10_savedata_native_io_r44 import *
from tools.stoneage_tw10_savedata_native_io_r42_guard import inputs_guard
from tools.stoneage_tw10_savedata_native_io_r37_guard import direct_guard
from tools.stoneage_tw10_savedata_native_io_r40_guard import rows_guard
from tools.stoneage_tw10_savedata_native_io_r30_guard import graph_guard
from tools.stoneage_tw10_savedata_native_io_r29_guard import shape_guard
from tools.stoneage_tw10_savedata_upstream_r22_guard import FORBIDDEN


def require(ok,why):
    if not ok:raise ValueError('R44 '+why)


def topology_guard(g,effects,edges,root):
    graph_guard(g);require(isinstance(effects,list) and len(effects)==g['nodes'],'effect count')
    ats=[]
    for e in effects:
        at,k,delta,w=(e.get(key) for key in ('site_rva','syntax_class','esp_delta','operand_width_bytes'))
        require(type(at) is int and root<=at<root+768 and k in ('neutral','push','pop','opaque_call','unknown_esp_write')
                and e.get('conditional_32bit_stack_address_only') is True,'inherited effect scope')
        if k in ('push','pop'):require(type(w) is int and w in (2,4) and type(delta) is int and delta==(-w if k=='push' else w),'inherited delta')
        else:require(w is None and (type(delta) is int and delta==0 if k=='neutral' else delta is None),'inherited opacity')
        ats.append(at)
    require(ats==sorted(set(ats)) and root in ats,'node order')
    require(isinstance(edges,list) and len(edges)==g['edges'] and all(isinstance(e,list) and len(e)==2
            and all(type(at) is int and at in ats for at in e) for e in edges)
            and edges==[list(e) for e in sorted(set(tuple(e) for e in edges))],'edges')
    return ats


def validate(d):
    require(isinstance(d,dict) and d.get('schema')==SCHEMA and d.get('status')==STATUS,'schema')
    require(d.get('runtime_sha256')==RUNTIME_SHA256 and d.get('savedata_sha256')==SAVEDATA_SHA256
            and d.get('r43_exact_original_revalidated') is True and d.get('r43_exact_report_sha256')==PRIOR_SHA256
            and d.get('static_only') is True and all(d.get(k) is False for k in FLAGS),'source/non-promotion')
    cs=d.get('native_contexts');require(isinstance(cs,list) and len(cs)==2,'native count')
    for c,spec in zip(cs,WRAPPERS):
        label,wrapper,call,root,_=spec
        require(c.get('label')==label and c.get('wrapper_root_candidate_rva')==wrapper and c.get('native_root_candidate_rva')==root
                and c.get('actual_native_argument_value_descriptor_buffer_count_or_effect_proven') is False,'native context')
        direct_guard(c.get('caller_identity',{}),call,root)
        e=c.get('qualified_prefix_evidence',{});inherited=c.get('inherited_stack_effect_candidates')
        ats=topology_guard(c.get('graph',{}),inherited,e.get('bounded_edges'),root)
        keys,cap=inputs_guard(c.get('frame_input_sources',{}),root,ats)
        adjustments=c.get('literal_esp_adjustment_or_unknown_shapes');rows_guard(adjustments,256,root,root+768,keys,cap,ats)
        expected=[r['site_rva'] for r in inherited if r['syntax_class']=='unknown_esp_write']
        require([r['site_rva'] for r in adjustments]==expected,'adjustment shape coverage')
        shapes={r['site_rva']:r for r in adjustments}
        effects=[literal_effect(shapes[r['site_rva']],r) if r['site_rva'] in shapes else r for r in inherited]
        require(e.get('stack_effect_candidates')==effects,'literal arithmetic replay/no CALL restore')
        states,updates,limit=stack_states(effects,e['bounded_edges'],root)
        require(c.get('stack_model_updates')==updates and c.get('stack_model_update_limit_hit') is limit,'stack model replay')
        prolog=c.get('entry_prolog_shapes');rows_guard(prolog,24,root,root+24,keys,cap,ats)
        require(all(set(r['decoder_written_registers'])&{'esp','ebp'} for r in prolog),'prolog syntax')
        reads,count=c.get('early_frame_read_shapes'),c.get('early_frame_read_count')
        require(type(count) is int and 0<=count<=256 and isinstance(reads,list) and len(reads)==min(count,MAX_READS)
                and c.get('early_frame_reads_truncated') is (count>MAX_READS)
                and c.get('early_frame_read_scope')=='instruction_starts_first96bytes_whole_instructions_in_parent768','early read cap')
        rows_guard(reads,MAX_READS,root,root+96,keys,cap,ats)
        require(all(r['mnemonic']!='lea' and any(o.get('kind')=='memory' and o.get('decoder_read') and o.get('geometry',{}).get('base_register')=='ebp'
                for o in r['operands']) for r in reads),'frame read syntax')
        defs=e.get('frame_definition_shapes');rows_guard(defs,MAX_DEFS,root,root+768,keys,cap,ats)
        expected=sorted({t['rva'] for q in c['frame_input_sources']['queries'] if q['register']=='ebp'
                         for t in q['reaching_candidates'] if t['origin']=='definition'})
        require(c.get('frame_definition_count')==len(expected) and [r['site_rva'] for r in defs]==expected[:MAX_DEFS]
                and c.get('frame_definitions_truncated') is (len(expected)>MAX_DEFS),'frame definitions')
        summaries=[state_summary(states,r['site_rva'],limit) for r in defs]
        require(e.get('frame_definition_esp_summaries')==summaries,'frame summary')
        prefix=set().union(*[(closure(e['bounded_edges'],root)&closure(e['bounded_edges'],r['site_rva'],True))-{r['site_rva']} for r in reads]) if reads else set()
        writes=e.get('prefix_explicit_write_shapes');rows_guard(writes,256,root,root+768,keys,cap,ats)
        require(all(r['site_rva'] in prefix and any(o.get('kind')=='memory' and o.get('decoder_write') for o in r['operands']) for r in writes),'prefix explicit writes')
        unknown=e.get('prefix_unmodeled_effect_shapes');rows_guard(unknown,256,root,root+768,keys,cap,ats)
        require(all(r['site_rva'] in prefix and r['mnemonic'] not in PREFIX_KNOWN_SYNTAX for r in unknown),'prefix unknown effect')
        ps=c.get('prior_caller_push_candidates');require(isinstance(ps,list) and len(ps)<=24,'push bound')
        last=call
        for i,p in enumerate(ps):
            at=p.get('site_rva');op=p.get('input',{})
            require(type(at) is int and wrapper<=at<last and p.get('conditional_pre_call_esp_offset')==i*4 and op.get('width_bytes')==4,'caller push geometry')
            shape_guard({'site_rva':at,'class':'unmodeled','operands':[op]},at);last=at
        bridges=[frame_bridge(r,c['frame_input_sources'],defs,summaries,ps) for r in reads]
        require(c.get('conditional_native_slot_bridges')==bridges,'native slot replay')
        require(c.get('native_prefix_token_audits')==[prefix_audit(root,e,r,b,c['frame_input_sources']) for r,b in zip(reads,bridges)],'native prefix token replay')
    ms=d.get('mutable_wrapper_slots');require(isinstance(ms,list) and len(ms)==2,'mutable count')
    for c,spec,wrapper_spec in zip(ms,MUTABLE,WRAPPERS):
        root,store,load,reg=spec;call=wrapper_spec[2]
        require(c.get('root_candidate_rva')==root and c.get('prior_native_call_site_rva')==call
                and c.get('actual_later_slot_preservation_buffer_role_or_io_proven') is False,'mutable identity')
        graph_guard(c.get('graph',{}));ats=c.get('bounded_node_rvas');edges=c.get('bounded_edges')
        require(isinstance(ats,list) and len(ats)==c['graph']['nodes'] and ats==sorted(set(ats))
                and all(type(at) is int and root<=at<root+768 for at in ats),'mutable graph nodes')
        require(isinstance(edges,list) and len(edges)==c['graph']['edges'] and all(isinstance(e,list) and len(e)==2 and all(at in ats for at in e) for e in edges)
                and edges==[list(e) for e in sorted(set(tuple(e) for e in edges))],'mutable graph edges')
        keys,cap=inputs_guard(c.get('source_input_sources',{}),root,ats)
        rows=[c.get('initial_slot_read_shape'),c.get('slot_write_shape')];rows_guard(rows,2,root,root+768,keys,cap,ats)
        require([r['site_rva'] for r in rows]==[load,store] and c.get('source_expansion_rounds')==MAX_SOURCE_ROUNDS,'mutable shape identities')
        expected=sorted({t['rva'] for q in c['source_input_sources']['queries'] for t in q['reaching_candidates'] if t['origin']=='definition'})
        shapes=c.get('source_definition_shapes');rows_guard(shapes,MAX_DEFS,root,root+768,keys,cap,ats)
        pending=c.get('source_expansion_pending_definition_rvas')
        require(c.get('source_definition_count')==len(expected) and c.get('source_definitions_truncated') is (len(expected)>MAX_DEFS)
                and isinstance(pending,list) and pending==sorted(set(pending)) and set(pending)<=set(expected)
                and [r['site_rva'] for r in shapes]==[at for at in expected[:MAX_DEFS] if at not in pending],'source shape coverage')
        require(c.get('conditional_rewrite_source_link')==rewrite_link(rows[1],rows[0],shapes,c['source_input_sources'],reg),'slot rewrite source replay')
        require(c.get('structural_load_to_store_candidate') is (store in closure(edges,load))
                and c.get('structural_store_to_native_call_candidate') is (call in closure(edges,store)),'mutable route replay')
        pushes=c.get('prior_native_push_candidates');require(isinstance(pushes,list) and len(pushes)<=24,'mutable push bound')
        for i,p in enumerate(pushes):
            require(p.get('conditional_pre_call_esp_offset')==i*4 and p.get('site_rva') in ats,'mutable push geometry')
            shape_guard({'site_rva':p['site_rva'],'class':'unmodeled','operands':[p.get('input')]},p['site_rva'])
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
    validate(json.loads(path.read_text()));print('TW10_R44_STRICT_STATIC=PASS; ACTUAL_NATIVE_SAVE=OPEN')


if __name__=='__main__':main()
