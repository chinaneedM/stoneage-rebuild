"""Replay R43 prefix/multiply/cycle evidence without runtime/value promotion."""
import argparse
import json
from pathlib import Path
from tools.stoneage_tw10_savedata_native_io_r43 import *
from tools.stoneage_tw10_savedata_native_io_r42_guard import inputs_guard
from tools.stoneage_tw10_savedata_native_io_r37_guard import direct_guard
from tools.stoneage_tw10_savedata_native_io_r40_guard import rows_guard, suffix_guard
from tools.stoneage_tw10_savedata_native_io_r30_guard import graph_guard
from tools.stoneage_tw10_savedata_upstream_r22_guard import FORBIDDEN
from tools.stoneage_tw10_savedata_native_io_r29_guard import shape_guard


def require(ok,why):
    if not ok:raise ValueError('R43 '+why)


def validate(d):
    require(isinstance(d,dict) and d.get('schema')==SCHEMA and d.get('status')==STATUS,'schema')
    require(d.get('runtime_sha256')==RUNTIME_SHA256 and d.get('savedata_sha256')==SAVEDATA_SHA256
            and d.get('r42_exact_original_revalidated') is True and d.get('r42_exact_report_sha256')==PRIOR_SHA256
            and d.get('static_only') is True and all(d.get(k) is False for k in FLAGS),'source/non-promotion')
    cs=d.get('contexts');require(isinstance(cs,list) and len(cs)==2,'context count')
    for c,spec,product in zip(cs,WRAPPERS,PRODUCTS):
        _,root,call,target,callers=spec
        require(c.get('root_candidate_rva')==root and c.get('native_call_site_rva')==call
                and c.get('actual_descriptor_buffer_count_or_native_parameter_binding_proven') is False,'context identity')
        e=c.get('prior_wrapper_evidence',{});graph_guard(e.get('graph',{}))
        effects,edges=e.get('stack_effect_candidates'),e.get('bounded_edges')
        require(isinstance(effects,list) and len(effects)==e['graph']['nodes'],'effect count')
        ats=[]
        for r in effects:
            at,k,delta,width=(r.get(key) for key in ('site_rva','syntax_class','esp_delta','operand_width_bytes'))
            require(type(at) is int and root<=at<root+768 and k in ('neutral','push','pop','opaque_call','unknown_esp_write')
                    and r.get('conditional_32bit_stack_address_only') is True,'effect scope')
            if k in ('push','pop'):require(type(width) is int and width in (2,4) and type(delta) is int and delta==(-width if k=='push' else width),'push/pop arithmetic')
            else:require(width is None and (type(delta) is int and delta==0 if k=='neutral' else delta is None),'effect opacity')
            ats.append(at)
        require(ats==sorted(set(ats)) and root in ats and call in ats,'node scope/order')
        require(isinstance(edges,list) and len(edges)==e['graph']['edges'] and all(isinstance(r,list) and len(r)==2
                and all(type(at) is int and at in ats for at in r) for r in edges)
                and edges==[list(r) for r in sorted(set(tuple(r) for r in edges))],'edge scope/order')
        keys,cap=inputs_guard(c.get('prefix_input_sources',{}),root,ats)
        reads=c.get('early_parameter_read_shapes');require(isinstance(reads,list) and len(reads)==4,'early reads')
        rows_guard(reads,4,root,root+96,keys,cap,ats)
        defs=e.get('frame_definition_shapes');rows_guard(defs,12,root,root+768,keys,cap,ats)
        states,_,limit=stack_states(effects,edges,root)
        summaries=[state_summary(states,r['site_rva'],limit) for r in defs]
        require(e.get('frame_definition_esp_summaries')==summaries,'frame summary replay')
        prefix=set().union(*[(closure(edges,root)&closure(edges,r['site_rva'],True))-{r['site_rva']} for r in reads])
        writes=e.get('prefix_explicit_write_shapes');rows_guard(writes,256,root,root+768,keys,cap,ats)
        require(all(r['site_rva'] in prefix and any(o.get('kind')=='memory' and o.get('decoder_write') for o in r['operands']) for r in writes),'prefix write syntax')
        unknown=e.get('prefix_unmodeled_effect_shapes');rows_guard(unknown,256,root,root+768,keys,cap,ats)
        require(all(r['site_rva'] in prefix and r['mnemonic'] not in PREFIX_KNOWN_SYNTAX for r in unknown),'unmodeled prefix syntax')
        bs=c.get('savedata_caller_token_contexts');require(isinstance(bs,list) and len(bs)==len(callers),'caller count')
        for b,(parent,caller) in zip(bs,callers):
            require(b.get('caller_site_rva')==caller and b.get('parent_filename_push_rva')==parent,'caller identity')
            direct_guard(b.get('caller_identity',{}),caller,root)
            ps=b.get('prior_caller_push_candidates');require(isinstance(ps,list) and len(ps)<=24,'caller push bound')
            last=caller
            for i,p in enumerate(ps):
                at=p.get('site_rva');op=p.get('input',{})
                require(type(at) is int and parent<=at<last and p.get('conditional_pre_call_esp_offset')==i*4 and op.get('width_bytes')==4,'caller push arithmetic')
                shape_guard({'site_rva':at,'class':'unmodeled','operands':[op]},at);last=at
            bridges=[frame_bridge(r,c['prefix_input_sources'],defs,summaries,ps) for r in reads]
            require(b.get('conditional_slot_bridges')==bridges,'slot geometry replay')
            require(b.get('prefix_token_audits')==[prefix_audit(root,e,r,bridge,c['prefix_input_sources']) for r,bridge in zip(reads,bridges)],'prefix overwrite/symbol replay')
        load,multiply=c.get('multiply_load_shape'),c.get('multiply_shape')
        rows_guard([load,multiply],2,root,root+96,keys,cap,ats)
        require([load['site_rva'],multiply['site_rva']]==list(product)
                and c.get('conditional_multiply_source_link')==product_link(load,multiply,c['prefix_input_sources']),'multiply source replay')
        direct_guard(c.get('prior_native_call_identity',{}),call,target)
        ni=c.get('native_input_sources',{});nk,nc=inputs_guard(ni,root,ats)
        suffix=c.get('prior_native_physical_suffix',{});suffix_guard(suffix,root,call,nk,nc)
        initial={(p['site_rva'],r) for p in suffix['pushes'] for r in operand_registers(p['input'])}
        initial.update((call,r) for r in ('eax','ebx','esi','edi','ebp'))
        expected=sorted({s['rva'] for q in ni['queries'] if (q['site_rva'],q['register']) in initial
                         for s in q['reaching_candidates'] if s['origin']=='definition'})
        shapes=c.get('native_direct_definition_shapes');rows_guard(shapes,MAX_NATIVE_DEFS,root,root+768,nk,nc,ats)
        require(c.get('native_direct_definition_count')==len(expected) and [r['site_rva'] for r in shapes]==expected[:MAX_NATIVE_DEFS]
                and c.get('native_direct_definitions_truncated') is (len(expected)>MAX_NATIVE_DEFS),'complete definition sample')
        oldcount,oldsites=c.get('prior_native_direct_definition_count'),c.get('prior_native_direct_shape_rvas')
        require(type(oldcount) is int and oldcount==len(expected) and isinstance(oldsites,list) and oldsites==expected[:12]
                and c.get('prior_native_direct_shape_count')==len(oldsites)
                and c.get('prior_sampler_omitted_definition_rvas')==sorted(set(expected)-set(oldsites)),'prior sample gap')
        sites={call}|{p['site_rva'] for p in suffix['pushes']};cycles=cycle_sources(ni,sites,edges)
        require(c.get('cycle_source_count')==len(cycles) and c.get('cycle_source_candidates')==cycles[:MAX_CYCLES]
                and c.get('cycle_sources_truncated') is (len(cycles)>MAX_CYCLES),'cycle/source replay/non-promotion')
    def ban(obj):
        if isinstance(obj,dict):
            require(not(set(obj)&FORBIDDEN),'original payload')
            for v in obj.values():ban(v)
        elif isinstance(obj,list):
            for v in obj:ban(v)
    ban(d);return True


def main():
    p=argparse.ArgumentParser();p.add_argument('--report',type=Path,required=True)
    path=p.parse_args().report;require(path.stat().st_size<=300000,'report bound')
    validate(json.loads(path.read_text()));print('TW10_R43_STRICT_STATIC=PASS; ACTUAL_NATIVE_SAVE=OPEN')


if __name__=='__main__':main()
