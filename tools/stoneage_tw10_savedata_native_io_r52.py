"""Pinned R51 numeric metadata -> bounded architectural source graphs.

Never downloads or executes the original client, evaluates original bytes, or
rewrites decoder observations. CDQ architectural qualification is an overlay.
"""
import argparse,hashlib,json
from collections import deque
from pathlib import Path

SCHEMA='tw10-r52-pinned-metadata-cdq-qualified-signed-division-output-consumers'
SOURCE_SCHEMA='tw10-r51-original-complete-processor-caller-conditional-stack-consumers'
SOURCE_SHA256='15f54e5de8d1d20128fb7d948b54f13a0e3f6cf372eca203cbc7bb8adc473052'
ROOT=0x47160
REGS={'eax':{'eax','ax','al','ah'},'ebx':{'ebx','bx','bl','bh'},'ecx':{'ecx','cx','cl','ch'},'edx':{'edx','dx','dl','dh'},'esi':{'esi','si'},'edi':{'edi','di'},'ebp':{'ebp','bp'}}
MAX_FOCUS=192
FLAGS=('actual_original_values_arithmetic_or_division_results_proven','actual_processor_algorithm_payload_or_length_proven','actual_abi_stack_alias_tag_migration_schema_or_persistence_proven','native_io_executed','original_bytes_published')
INTEL_URL='https://www.intel.com/content/dam/support/us/en/documents/processors/pentium4/sb/25366521.pdf'

def family(reg):return next((r for r,names in REGS.items() if reg in names),None)
def cdq(row):
    return row['mnemonic']=='cdq' and row['operands']==[] and row['decoder_read_registers']==['eax'] and set(row['decoder_written_registers']) in ({'edx'},{'eax','edx'})
def writes(row,architecture=True):
    names=set(row['decoder_written_registers'])
    if architecture and cdq(row):names.discard('eax')
    return {family(r) for r in names}-{None}
def reads(row):
    names=set(row['decoder_read_registers'])
    for op in row['operands']:
        if op.get('kind')=='register' and op.get('decoder_read'):names.add(op['register'])
        if op.get('kind')=='memory':
            g=op['geometry'];names.update((g.get('base_register'),g.get('index_register')))
    # A partial-register definition has an unknown preserved parent slice.
    names.update(r for r in row['decoder_written_registers'] if family(r) and r!=family(r))
    return sorted({family(r) for r in names}-{None})

def reaches(rows,edges,root,reg,architecture=True):
    by={r['site_rva']:r for r in rows};adj={a:[] for a in by}
    if root not in by or reg not in REGS or len(by)!=len(rows) or len(rows)>256:raise ValueError('source graph scope')
    for a,b in edges:
        if a not in by or b not in by:raise ValueError('source edge membership')
        adj[a].append(b)
    incoming={root:{('entry',root)}};todo=deque([root]);pending={root};steps=0
    while todo and steps<65536:
        a=todo.popleft();pending.discard(a);r=by[a]
        out={('unknown_call',a)} if r['mnemonic'] in ('call','lcall') else {('definition',a)} if reg in writes(r,architecture) else incoming[a]
        for b in adj[a]:
            new=incoming.get(b,set())|out
            if new!=incoming.get(b,set()):
                incoming[b]=new
                if b not in pending:todo.append(b);pending.add(b)
        steps+=1
    if todo:raise ValueError('source update bound')
    return incoming

def focus(rows,maps,seeds,cap=MAX_FOCUS):
    if type(cap) is not int or not 1<=cap<=192:raise ValueError('focus cap')
    by={r['site_rva']:r for r in rows};todo=deque(sorted(set(seeds)));seen={};definitions=set()
    while todo and len(seen)<cap:
        a,reg=todo.popleft()
        if (a,reg) in seen:continue
        if a not in by or reg not in REGS:raise ValueError('focus seed')
        tokens=sorted(maps[reg].get(a,()),key=lambda x:(x[1],x[0]));deps=set()
        for origin,site in tokens:
            if origin=='definition':
                definitions.add(site);deps.update((site,r) for r in reads(by[site]))
        seen[(a,reg)]={'site_rva':a,'register':reg,'source_candidates':[{'origin':o,'site_rva':s} for o,s in tokens],
                       'dependency_queries':[{'site_rva':s,'register':r} for s,r in sorted(deps)],'actual_register_or_memory_value_known':False}
        todo.extend(sorted(deps-set(seen)))
    pending=sorted(set(todo)-set(seen))
    return {'query_cap':cap,'queries':[seen[k] for k in sorted(seen)],'query_limit_hit':bool(pending),
            'pending_queries':[{'site_rva':a,'register':r} for a,r in pending],
            'definition_shapes':[by[a] for a in sorted(definitions)],'definition_shapes_truncated':False,
            'graph_local_dependency_queries_closed':not pending,'actual_memory_closure_or_values_proven':False}

def flag_context(rows,edges,branch):
    by={r['site_rva']:r for r in rows};rev={a:[] for a in by}
    for a,b in edges:rev[b].append(a)
    todo=deque(rev[branch]);seen=set();sources=set();barriers=set();entry=False
    while todo and len(seen)<256:
        a=todo.popleft()
        if a in seen:continue
        seen.add(a);r=by[a]
        if r['mnemonic'] in ('call','lcall'):barriers.add(a)
        elif 'eflags' in r['decoder_written_registers']:sources.add(a)
        elif not rev[a]:entry=True
        else:todo.extend(rev[a])
    r=by[branch];target=r['operands'][0]['constant']-0x400000
    return {'branch_site_rva':branch,'mnemonic':r['mnemonic'],'direct_target_rva':target,
            'successor_rvas':sorted(b for a,b in edges if a==branch),'nearest_flag_source_shapes':[by[a] for a in sorted(sources)],
            'opaque_call_barrier_rvas':sorted(barriers),'entry_without_flag_source_candidate':entry,
            'predecessor_nodes_examined':len(seen),'predecessor_cap_hit':bool(todo),
            'actual_flags_path_feasibility_or_loop_iterations_proven':False}

def analyze(d):
    rows=d['processor_instruction_shapes'];p=d['r50_snapshot']['processing_entry_context'];edges=p['bounded_edges'];by={r['site_rva']:r for r in rows}
    if [r['site_rva'] for r in rows]!=p['bounded_node_rvas'] or len(rows)>256:raise ValueError('inventory scope')
    if p['graph']['node_limit_hit'] or p['graph']['frontier']:raise ValueError('unclosed processor graph')
    maps={r:reaches(rows,edges,ROOT,r) for r in REGS};raw={r:reaches(rows,edges,ROOT,r,False) for r in ('eax','edx')}
    divs=[r for r in rows if r['mnemonic']=='idiv'];result=[]
    for r in divs:
        a=r['site_rva'];s=focus(rows,maps,[(a,r) for r in reads(r)])
        low=maps['eax'][a];high=maps['edx'][a];sites=[t[1] for t in high if t[0]=='definition' and cdq(by[t[1]])]
        linked=len(high)==1 and len(sites)==1 and low==maps['eax'].get(sites[0],set())
        consumers={}
        for reg in ('eax','edx'):
            consumers[reg]=[x['site_rva'] for x in rows if reg in reads(x) and ('definition',a) in maps[reg].get(x['site_rva'],set())]
        result.append({'site_rva':a,'shape':r,'source_graph':s,
                       'decoder_eax_source_candidates':[{'origin':o,'site_rva':n} for o,n in sorted(raw['eax'][a])],
                       'qualified_eax_source_candidates':[{'origin':o,'site_rva':n} for o,n in sorted(low)],
                       'qualified_edx_source_candidates':[{'origin':o,'site_rva':n} for o,n in sorted(high)],
                       'unique_cdq_site_rva':sites[0] if len(high)==1 and len(sites)==1 else None,
                       'conditional_sign_extended_eax_dividend_syntax_qualified':linked,
                       'architecture_quotient_register':'eax','architecture_remainder_register':'edx',
                       'quotient_register_consumer_candidates':consumers['eax'],'remainder_register_consumer_candidates':consumers['edx'],
                       'actual_dividend_divisor_quotient_remainder_or_nonzero_divisor_proven':False})
    old=d['processor_division_source_surface'];legacy=sorted({t['rva'] for q in old['input_sources']['queries'] for t in q['reaching_candidates'] if t['origin']=='definition'})
    outputsites=(0x47160,0x4716a,0x47173,0x4717c)
    output=focus(rows,maps,[(0x4717c,'ecx'),(0x4717c,'esi')])
    refs=d['conditional_consumer_analysis']['processor_entry_stack_coordinates']['references']
    memwrites=[r for r in rows if any(o.get('kind')=='memory' and o.get('decoder_write') for o in r['operands'])]
    return {'cdq_architecture_overlays':[{'site_rva':r['site_rva'],'decoder_observation':r,'architectural_read_registers':['eax'],
              'architectural_written_registers':['edx'],'architecturally_preserved_registers':['eax'],
              'architectural_edx_expression':'all_bits_equal_to_sign_bit_31_of_input_EAX','actual_original_sign_bit_or_register_values_known':False} for r in rows if cdq(r)],
            'signed_division_contexts':result,
            'r51_legacy_definition_shapes_complete':[by[a] for a in legacy],
            'r51_legacy_definition_count':len(legacy),'r51_legacy_definitions_truncated':False,
            'r51_pending_definition_shapes':[by[a] for a in old['source_expansion_pending_definition_rvas']],
            'conditional_output_store_context':{'syntax_shapes':[by[a] for a in outputsites],'source_graph':output,
              'entry_coordinate_candidates':[r for r in refs if r['site_rva'] in (0x47160,0x47173)],
              'explicit_memory_write_alias_barrier_shapes':memwrites,'implicit_stack_write_barrier_rvas':[r['site_rva'] for r in rows if r['mnemonic']=='push'],
              'actual_read_count_minus_one_length_output_contents_or_alias_proven':False},
            'byte_transform_shapes':[r for r in rows if r['mnemonic'] in ('imul','sub','not') and any(o['width_bytes']==1 for o in r['operands'])],
            'processor_predicate_contexts':[flag_context(rows,edges,r['site_rva']) for r in rows if r['mnemonic'].startswith('j') and r['mnemonic']!='jmp'],
            'actual_savedata_algorithm_output_length_version_schema_or_persistence_proven':False}

def derive(raw,expected_sha=SOURCE_SHA256):
    if len(raw)>1000000 or hashlib.sha256(raw).hexdigest()!=expected_sha:raise ValueError('R52 source custody')
    d=json.loads(raw)
    if d.get('schema')!=SOURCE_SCHEMA or d.get('static_only') is not True:raise ValueError('R52 source schema')
    if any(v is not False for k,v in d.items() if k.startswith('actual_') or k in ('native_io_executed','original_bytes_published')):raise ValueError('R52 source promotion')
    return {'schema':SCHEMA,'status':'PINNED_METADATA_CONDITIONAL_ARCHITECTURE_SOURCES_SCHEMA_OPEN','source_r51_sha256':expected_sha,
            'source_r51_bytes':len(raw),'static_only':True,'metadata_only_no_original_redownload':True,
            'architecture_source':{'url':INTEL_URL,'volume':'Intel 64 and IA-32 SDM Volume1','sections':['7.3.1.6','7.3.2.5'],
                                   'idiv_reference_url':'https://cdrdv2-public.intel.com/789581/325383-sdm-vol-2abcd.pdf',
                                   'idiv_reference_location':'Volume2A IDIV, Table3-51, printed page3-498',
                                   'architectural_effects_only_not_original_values':True},'analysis':analyze(d),**{k:False for k in FLAGS}}

def validate(report,raw,expected_sha=SOURCE_SHA256):
    if json.dumps(report,sort_keys=True,separators=(',',':'))!=json.dumps(derive(raw,expected_sha),sort_keys=True,separators=(',',':')):raise ValueError('R52 exact replay differs')
    return True

def main():
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--verify',type=Path);a=p.parse_args()
    if a.source.stat().st_size>1000000:raise ValueError('source bound')
    raw=a.source.read_bytes()
    if a.verify:
        if a.verify.stat().st_size>2000000:raise ValueError('report bound')
        validate(json.loads(a.verify.read_text()),raw);print('TW10_R52_PINNED_METADATA_REPLAY=PASS; ACTUAL_SAVE_SCHEMA=OPEN')
    else:print(json.dumps(derive(raw),sort_keys=True,indent=2))
if __name__=='__main__':main()
