"""Native entry slots and wrapper slot rewrite sources, conditional metadata.

A separately qualified ADD/SUB ESP literal model retains opaque CALL barriers.
No original values, memory, arithmetic products, ABI or file IO are executed.
"""
import argparse
import hashlib
import json
import tempfile
from pathlib import Path
from capstone.x86 import X86_OP_MEM, X86_OP_REG, X86_OP_IMM
from tools.stoneage_tw10_savedata_native_io_r43 import (
    inspect_verified as inspect_r43, prefix_audit, PREFIX_KNOWN_SYNTAX, RUNTIME_SHA256, SAVEDATA_SHA256)
from tools.stoneage_tw10_savedata_native_io_r43_guard import validate as validate_r43
from tools.stoneage_tw10_savedata_native_io_r42 import WRAPPERS
from tools.stoneage_tw10_savedata_native_io_r38 import stack_effect, stack_states, state_summary
from tools.stoneage_tw10_savedata_native_io_r40 import frame_bridge, geometry_key
from tools.stoneage_tw10_savedata_native_io_r37 import instruction_row, operand_registers
from tools.stoneage_tw10_savedata_native_io_r41 import queries_for
from tools.stoneage_tw10_savedata_native_io_r28 import candidate_graph, input_surface
from tools.stoneage_tw10_savedata_native_io_r30 import graph_meta
from tools.stoneage_tw10_savedata_native_io_r36 import closure
from tools.stoneage_tw10_savedata_frontier_r12 import call_identity
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH, SAVEDATA_PATH
from tools.stoneage_tw10_technical_probe import find_rows, extract_row

SCHEMA='tw10-r44-original-native-frame-slots-wrapper-slot-rewrite-source-candidates'
STATUS='PINNED_ORIGINAL_CONDITIONAL_NATIVE_SLOTS_MUTABLE_SOURCES_SAVE_OPEN'
PRIOR_SHA256='f5eeaac700c649f92e3fca5e7cbefa465879048f54d84b3896dcdb72115d7b42'
MUTABLE=((0x48bbc,0x48bd2,0x48bca,'eax'),(0x48660,0x48678,0x4866e,'ecx'))
MAX_READS=16
EARLY_SPAN=160
MAX_DEFS=16
MAX_SOURCE_ROUNDS=3
FLAGS=('actual_native_parameter_values_or_abi_roles_proven','actual_esp_stack_contents_or_frame_preservation_proven',
       'slot_rewrite_establishes_actual_buffer_or_count','original_size_product_or_api_byte_count_proven',
       'actual_descriptor_handle_or_owner_binding_proven','actual_savedata_schema_or_persistence_proven',
       'native_io_executed','original_bytes_published')


def literal_effect(row, inherited):
    e=dict(inherited);ops=row['operands']
    if (inherited['syntax_class']=='unknown_esp_write' and row['mnemonic'] in ('add','sub') and len(ops)==2
        and ops[0].get('kind')=='register' and ops[0].get('register')=='esp' and ops[0].get('width_bytes')==4
        and ops[1].get('kind')=='immediate' and ops[1].get('width_bytes')==4
        and type(ops[1].get('constant')) is int and abs(ops[1]['constant'])<=4096):
        e.update(syntax_class='literal_esp_adjustment',esp_delta=ops[1]['constant']*(1 if row['mnemonic']=='add' else -1),operand_width_bytes=4)
    return e


def unique_definition(inputs,site,register):
    q=next((q for q in inputs['queries'] if q['site_rva']==site and q['register']==register),{})
    ts=q.get('reaching_candidates',[])
    return (ts[0]['rva'] if q.get('site_in_candidate_graph') is True and q.get('candidates_truncated') is False
            and not inputs['query_limit_hit'] and len(ts)==1 and ts[0]['origin']=='definition' else None)


def rewrite_link(store,load,shapes,inputs,register):
    source=unique_definition(inputs,store['site_rva'],register)
    row=next((r for r in shapes if r['site_rva']==source),{})
    ops=row.get('operands',[]);copy=None
    if row.get('mnemonic')=='mov' and len(ops)==2 and all(o.get('kind')=='register' and o.get('width_bytes')==4 for o in ops):
        copy=unique_definition(inputs,row['site_rva'],ops[1].get('register'))
    copied=next((r for r in shapes if r['site_rva']==copy),{})
    dest=store['operands'][0];src=store['operands'][1]
    same=bool(source==load['site_rva'] and row.get('mnemonic')=='mov' and len(ops)==2 and ops[1].get('kind')=='memory'
              and geometry_key(dest)==geometry_key(ops[1]) and dest.get('width_bytes')==ops[1].get('width_bytes')==4)
    product=bool(copied.get('mnemonic')=='imul' and len(copied.get('operands',[]))==2
                 and copied['operands'][0].get('kind')=='register' and copied['operands'][0].get('width_bytes')==4)
    qualified=bool(store['mnemonic']=='mov' and dest.get('kind')=='memory' and dest.get('width_bytes')==4
                   and src.get('kind')=='register' and src.get('register')==register and src.get('width_bytes')==4)
    return {'store_site_rva':store['site_rva'],'source_definition_rva':source,'source_copy_input_definition_rva':copy,
            'qualified_four_byte_slot_rewrite_syntax':qualified,'unique_load_from_same_slot_then_rewrite_candidate':same,
            'unique_register_copy_from_imul_source_candidate':product,
            'source_definition_numerically_before_store':source is not None and source<store['site_rva'],
            'actual_same_runtime_address_contents_buffer_or_count_proven':False,'original_values_or_product_evaluated':False}


def mutable_context(dec,sections,prior,spec):
    root,store_site,load_site,reg=spec
    old=next(c for c in prior['contexts'] if c['root_candidate_rva']==root)
    nodes,edges,_,_=candidate_graph(dec,root)
    store=instruction_row(dec,sections,nodes,store_site);load=instruction_row(dec,sections,nodes,load_site)
    queries=queries_for([store,load]);rows={}
    for _ in range(MAX_SOURCE_ROUNDS):
        inputs=input_surface(dec,sections,nodes,edges,root,queries)
        sites=sorted({t['rva'] for q in inputs['queries'] for t in q['reaching_candidates'] if t['origin']=='definition'})
        for at in sites[:MAX_DEFS]:rows[at]=instruction_row(dec,sections,nodes,at)
        queries.update(queries_for(list(rows.values())))
    inputs=input_surface(dec,sections,nodes,edges,root,queries)
    sites=sorted({t['rva'] for q in inputs['queries'] for t in q['reaching_candidates'] if t['origin']=='definition'})
    sampled=[rows[at] for at in sites[:MAX_DEFS] if at in rows]
    pending=[at for at in sites if at not in rows]
    native=old['native_call_site_rva'];pushes=old['prior_native_physical_suffix']['pushes']
    return {'root_candidate_rva':root,'graph':old['prior_wrapper_evidence']['graph'],
            'bounded_edges':old['prior_wrapper_evidence']['bounded_edges'],
            'bounded_node_rvas':[e['site_rva'] for e in old['prior_wrapper_evidence']['stack_effect_candidates']],
            'initial_slot_read_shape':load,'slot_write_shape':store,'source_input_sources':inputs,
            'source_definition_count':len(sites),'source_definition_shapes':sampled,
            'source_definitions_truncated':len(sites)>MAX_DEFS,'source_expansion_rounds':MAX_SOURCE_ROUNDS,
            'source_expansion_pending_definition_rvas':pending,
            'conditional_rewrite_source_link':rewrite_link(store,load,sampled,inputs,reg),
            'structural_load_to_store_candidate':store_site in closure(edges,load_site),
            'structural_store_to_native_call_candidate':native in closure(edges,store_site),
            'prior_native_call_site_rva':native,'prior_native_push_candidates':pushes,
            'actual_later_slot_preservation_buffer_role_or_io_proven':False}


def native_context(dec,sections,imports,prior,spec):
    label,wrapper,call,root,_=spec
    old=next(c for c in prior['contexts'] if c['root_candidate_rva']==wrapper)
    ident=call_identity(dec,call,imports,sections)
    if ident!=old['prior_native_call_identity'] or ident['direct_target_rva']!=root:raise ValueError('R44 exact original native caller changed')
    nodes,edges,front,cap=candidate_graph(dec,root)
    inherited=[stack_effect(ins,dec.base) for _,ins in sorted(nodes.items())]
    adjustments=[instruction_row(dec,sections,nodes,e['site_rva']) for e in inherited if e['syntax_class']=='unknown_esp_write']
    bysite={r['site_rva']:r for r in adjustments}
    effects=[literal_effect(bysite[e['site_rva']],e) if e['site_rva'] in bysite else e for e in inherited]
    states,updates,limit=stack_states(effects,edges,root)
    early=[at for at,ins in sorted(nodes.items()) if at<root+EARLY_SPAN and ins.mnemonic!='lea'
           and any(o.type==X86_OP_MEM and o.access&1 and ins.reg_name(o.mem.base)=='ebp' for o in ins.operands)]
    reads=[instruction_row(dec,sections,nodes,at) for at in early[:MAX_READS]]
    prolog=[instruction_row(dec,sections,nodes,at) for at,ins in sorted(nodes.items()) if at<root+24
            and set(ins.reg_name(r) for r in ins.regs_access()[1])&{'esp','ebp'}]
    queries=queries_for(reads+prolog+adjustments)
    inputs=input_surface(dec,sections,nodes,edges,root,queries)
    sites=sorted({t['rva'] for q in inputs['queries'] if q['register']=='ebp' for t in q['reaching_candidates'] if t['origin']=='definition'})
    defs=[instruction_row(dec,sections,nodes,at) for at in sites[:MAX_DEFS]]
    summaries=[state_summary(states,at,limit) for at in sites[:MAX_DEFS]]
    prefix=set().union(*[(closure(edges,root)&closure(edges,r['site_rva'],True))-{r['site_rva']} for r in reads]) if reads else set()
    writes=[instruction_row(dec,sections,nodes,at) for at,ins in sorted(nodes.items()) if at in prefix
            and any(o.type==X86_OP_MEM and o.access&2 for o in ins.operands)]
    unknown=[instruction_row(dec,sections,nodes,at) for at in sorted(prefix) if nodes[at].mnemonic not in PREFIX_KNOWN_SYNTAX]
    inputs=input_surface(dec,sections,nodes,edges,root,queries|queries_for(defs+writes+unknown))
    evidence={'bounded_edges':[list(e) for e in sorted(edges)],'stack_effect_candidates':effects,
              'frame_definition_shapes':defs,'frame_definition_esp_summaries':summaries,
              'prefix_explicit_write_shapes':writes,'prefix_unmodeled_effect_shapes':unknown}
    ps=old['prior_native_physical_suffix']['pushes']
    bridges=[frame_bridge(r,inputs,defs,summaries,ps) for r in reads]
    return {'label':label,'wrapper_root_candidate_rva':wrapper,'native_root_candidate_rva':root,'caller_identity':ident,
            'prior_caller_push_candidates':ps,'graph':graph_meta(nodes,edges,front,cap),
            'inherited_stack_effect_candidates':inherited,'literal_esp_adjustment_or_unknown_shapes':adjustments,
            'qualified_prefix_evidence':evidence,'stack_model_updates':updates,'stack_model_update_limit_hit':limit,
            'entry_prolog_shapes':prolog,'early_frame_read_count':len(early),'early_frame_read_shapes':reads,
            'early_frame_reads_truncated':len(early)>MAX_READS,
            'early_frame_read_scope':'instruction_starts_first160bytes_whole_instructions_in_parent768',
            'frame_input_sources':inputs,'frame_definition_count':len(sites),'frame_definitions_truncated':len(sites)>MAX_DEFS,
            'conditional_native_slot_bridges':bridges,
            'native_prefix_token_audits':[prefix_audit(root,evidence,r,b,inputs) for r,b in zip(reads,bridges)],
            'actual_native_argument_value_descriptor_buffer_count_or_effect_proven':False}


def derive(dec,sections,imports,prior):
    if prior.get('schema')!='tw10-r43-original-wrapper-prefix-product-complete-native-source-candidates':raise ValueError('R44 prerequisite schema')
    return {'schema':SCHEMA,'status':STATUS,'runtime_sha256':RUNTIME_SHA256,'savedata_sha256':SAVEDATA_SHA256,
            'r43_exact_original_revalidated':True,'r43_exact_report_sha256':PRIOR_SHA256,'static_only':True,
            'native_contexts':[native_context(dec,sections,imports,prior,s) for s in WRAPPERS],
            'mutable_wrapper_slots':[mutable_context(dec,sections,prior,s) for s in MUTABLE],
            **{flag:False for flag in FLAGS}}


def inspect_verified(runtime,savedata):
    prior=inspect_r43(runtime,savedata);validate_r43(prior)
    if hashlib.sha256((json.dumps(prior,sort_keys=True)+'\n').encode()).hexdigest()!=PRIOR_SHA256:raise ValueError('R44 exact R43 derivative changed')
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'sa_3.exe';p.write_bytes(runtime);data,pe,base,sections,imports=image_layout(p)
    for s,raw in zip(sections,pe.sections):s['characteristics']=int(raw.Characteristics)
    t=next(s for s in sections if s['name']=='.text')
    return derive(Decoder(data[t['raw']:t['raw']+t['raw_size']],t['rva'],base),sections,imports,prior)


def main():
    p=argparse.ArgumentParser();p.add_argument('--bin',type=Path,required=True)
    image,rows,_,_=find_rows(p.parse_args().bin)
    try:
        files={r['path']:r for r in rows if not r['is_dir']}
        with tempfile.TemporaryDirectory() as td:
            exe,save=Path(td)/'sa_3.exe',Path(td)/'savedata.dat'
            extract_row(image,files[RUNTIME_PATH],exe);extract_row(image,files[SAVEDATA_PATH],save)
            d=inspect_verified(exe.read_bytes(),save.read_bytes())
    finally:image.close()
    print(json.dumps(d,sort_keys=True))


if __name__=='__main__':main()
