"""Strict derived-only R10 schema; custody remains an independent gate."""
import argparse,json
from pathlib import Path
from tools.stoneage_tw10_savedata_provenance_r10 import SCHEMA,STATUS,ROOT,STORE,DELEGATE,BRANCHES,RUNTIME_SHA256,SAVEDATA_SHA256
from tools.stoneage_tw10_savedata_helper_original_r8_guard import obj,integer,boolean,registers,unique,HELPER,MAX_STATES,MAX_RETURNS,GAPS,Counter
FLAGS={'delegate_effects_admitted','loop_runtime_bound_proven','caller_resumption_admitted','filename_api_link_proven','handle_buffer_size_link_proven','native_io_executed','fixed_128_byte_schema_proven','original_bytes_published'}
TOP={'schema','status','runtime_sha256','savedata_sha256','parent_nodes','parent_edges','provenance','delegate_helper'}|FLAGS
REGS={'eax','ebx','ecx','edx','esi','edi','ebp','esp','ax','bx','cx','dx','si','di','bp','sp','al','bl','cl','dl','ah','bh','ch','dh'}
KINDS={'unmodeled_write','register_zero_test','comparison','masked_test','register_copy','memory_load','address_calculation','constant_assignment','register_offset_adjustment','stack_pop'}
def geometry(g):
    obj(g,{'width_bytes','base_register','index_register','index_scale','segment_register','relative_field_offset','displacement_region'})
    if integer(g['width_bytes'],1,4) not in (1,2,4):raise ValueError('memory width')
    for k in ('base_register','index_register'):
        if g[k] is not None and g[k] not in REGS:raise ValueError('memory register')
    if integer(g['index_scale'],1,8) not in (1,2,4,8):raise ValueError('memory scale')
    if g['segment_register'] is not None and g['segment_register'] not in ('cs','ds','es','fs','gs','ss'):raise ValueError('segment')
    offset=g['relative_field_offset']
    if offset is not None:
        integer(offset,-4096,4096)
        if g['base_register'] is None and g['index_register'] is None:raise ValueError('relative offset')
    r=g['displacement_region']
    if r is not None:
        obj(r,{'section','displacement_rva','raw_backed','writable'})
        if r['section'] not in ('.text','.data','.bss','.rdata','.rsrc','.reloc','.idata','.edata','.tls'):raise ValueError('region')
        integer(r['displacement_rva'],0,2**32-1);boolean(r['raw_backed']);boolean(r['writable'])
def sources(rows,flags=False):
    if type(rows) is not list or not 1<=len(rows)<=256:raise ValueError('sources')
    seen=set()
    for r in rows:
        obj(r,{'origin','rva','semantic'});integer(r['rva'],ROOT,ROOT+1023)
        origin=r['origin']
        if origin not in ('entry','unknown_call','definition'):raise ValueError('origin')
        key=(origin,r['rva'])
        if key in seen:raise ValueError('duplicate source')
        seen.add(key)
        if origin=='entry' and r['rva']!=ROOT:raise ValueError('entry')
        s=r['semantic']
        if origin!='definition':
            if s is not None:raise ValueError('barrier semantic')
            continue
        obj(s,{'kind','register_inputs','memory_input','constant','width_bits'})
        kind=s['kind']
        if kind not in KINDS:raise ValueError('kind')
        if flags and kind not in ('unmodeled_write','register_zero_test','comparison','masked_test'):raise ValueError('flag kind')
        if not flags and kind in ('register_zero_test','comparison','masked_test'):raise ValueError('ESI kind')
        regs=s['register_inputs']
        if type(regs) is not list or len(regs)>2 or any(type(x) is not str or x not in REGS for x in regs):raise ValueError('inputs')
        width=s['width_bits']
        if width is not None and integer(width,8,32) not in (8,16,32):raise ValueError('width')
        c=s['constant']
        if c is not None:integer(c,-2**32,2**32-1)
        mem=s['memory_input']
        if mem is not None:geometry(mem)
        if kind=='unmodeled_write' and (regs or mem is not None or c is not None or width is not None):raise ValueError('unmodeled semantics')
        if kind=='register_zero_test' and (len(regs)!=1 or c!=0 or mem is not None or width is None):raise ValueError('zero test')
        if kind in ('memory_load','address_calculation') and (mem is None or regs or c is not None or width!=32):raise ValueError('memory definition')
        if kind=='constant_assignment' and (c is None or regs or mem is not None or width!=32):raise ValueError('constant definition')
        if kind=='register_copy' and (len(regs)!=1 or c is not None or mem is not None or width!=32):raise ValueError('copy')
        if kind=='register_offset_adjustment' and (regs!=['esi'] or c is None or mem is not None or width!=32):raise ValueError('adjustment')
        if kind=='stack_pop' and (regs or c is not None or mem is not None or width!=32):raise ValueError('pop')
        if kind in ('comparison','masked_test') and (width is None or not (regs or mem is not None)):raise ValueError('predicate')
    return len(rows)==1 and rows[0]['origin']=='definition'
def validate(text):
    if type(text) is not str or len(text.encode())>24000:raise ValueError('size')
    d=json.loads(text,object_pairs_hook=unique);obj(d,TOP)
    if d['schema']!=SCHEMA or d['status']!=STATUS or d['runtime_sha256']!=RUNTIME_SHA256 or d['savedata_sha256']!=SAVEDATA_SHA256:raise ValueError('identity')
    if integer(d['parent_nodes'],1,256)!=50 or integer(d['parent_edges'],1,512)!=55:raise ValueError('parent graph')
    if any(d[k] is not False for k in FLAGS):raise ValueError('promotion')
    h=d['delegate_helper'];obj(h,HELPER)
    if h['schema']!='tw10-r8-bounded-helper-return-effects' or integer(h['root_rva'],0,2**32-1)!=DELEGATE:raise ValueError('helper identity')
    n=integer(h['visited_states'],1,MAX_STATES)
    cap=boolean(h['state_limit_hit']);cycle=boolean(h['control_flow_cycle'])
    if cap and n!=MAX_STATES:raise ValueError('cap consistency')
    if h['original_helper_accepted'] is not False or h['native_io_executed'] is not False:raise ValueError('helper promotion')
    g=h['gaps']
    if type(g) is not dict or set(g)-GAPS:raise ValueError('gap names')
    for count in g.values():integer(count,1,2*MAX_STATES)
    sites=h['gap_sites']
    if type(sites) is not list or len(sites)>64:raise ValueError('gap sites')
    counts=Counter();seen=set()
    for e in sites:
        obj(e,{'rva','reason','direct_target_rva','occurrences'});integer(e['rva'],0,2**32-1)
        if e['reason'] not in GAPS:raise ValueError('site reason')
        target=e['direct_target_rva']
        if target is not None:integer(target,0,2**32-1)
        if target is not None and e['reason']!='unsummarized_call':raise ValueError('gap target')
        key=(e['rva'],e['reason'],target)
        if key in seen:raise ValueError('duplicate gap site')
        seen.add(key);counts[e['reason']]+=integer(e['occurrences'],1,2*MAX_STATES)
    if dict(counts)!=g:raise ValueError('gap counts')
    paths=h['return_paths']
    if type(paths) is not list or len(paths)>MAX_RETURNS:raise ValueError('return paths')
    kept=[];cleanups=set();seen=set();safe_returns=True
    for p in paths:
        obj(p,{'rva','pre_ret_stack_delta','ret_cleanup_bytes','return_word_preserved','preserved_registers'})
        integer(p['rva'],0x1000,0x1000+331776-1)
        sp=p['pre_ret_stack_delta']
        if sp is not None:integer(sp,-2**31*MAX_STATES,2**31*MAX_STATES)
        word=boolean(p['return_word_preserved'])
        if sp is None and word:raise ValueError('unknown return word')
        reg=registers(p['preserved_registers'],True);kept.append(reg)
        cleanup=integer(p['ret_cleanup_bytes'],0,65535);cleanups.add(cleanup)
        key=(p['rva'],sp,cleanup,word,tuple(p['preserved_registers']))
        if key in seen:raise ValueError('duplicate return')
        seen.add(key);safe_returns&=(sp==0 and word)
    common=sorted(set.intersection(*kept)) if kept else []
    registers(h['common_preserved_registers'])
    if h['common_preserved_registers']!=common:raise ValueError('register intersection')
    uniform=next(iter(cleanups)) if len(cleanups)==1 else None
    if h['uniform_ret_cleanup_bytes'] is not None:integer(h['uniform_ret_cleanup_bytes'],0,65535)
    if h['uniform_ret_cleanup_bytes']!=uniform:raise ValueError('cleanup consistency')
    qualified=bool(paths) and not g and not cap and not cycle and safe_returns and len(cleanups)==1
    if boolean(h['qualifies_modeled_return_effect_summary'])!=qualified:raise ValueError('qualification consistency')
    p=d['provenance'];obj(p,{'esi_at_store','loop_predicates','structural_call_return_assumptions'})
    if integer(p['structural_call_return_assumptions'],0,256)!=1:raise ValueError('call assumptions')
    e=p['esi_at_store'];obj(e,{'store_rva','conservative_sources','syntax_candidates_ignoring_call_clobbers','effective_target_proven'})
    if integer(e['store_rva'],0,2**32-1)!=STORE or e['effective_target_proven'] is not False:raise ValueError('store proof')
    sources(e['conservative_sources']);sources(e['syntax_candidates_ignoring_call_clobbers'])
    rows=p['loop_predicates']
    if type(rows) is not list or len(rows)!=3:raise ValueError('predicate count')
    for rva,cond,row in zip(BRANCHES,('je','je','jl'),rows):
        obj(row,{'branch_rva','condition','flag_sources','unique_conditional_flag_definition','runtime_branch_outcome_proven'})
        if integer(row['branch_rva'],0,2**32-1)!=rva or row['condition']!=cond:raise ValueError('branch identity')
        single=sources(row['flag_sources'],True)
        if boolean(row['unique_conditional_flag_definition'])!=single or row['runtime_branch_outcome_proven'] is not False:raise ValueError('predicate promotion')
    return {'schema':'tw10-r10-strict-provenance-report-guard','delegate_states':n,'delegate_qualifies_modeled_summary':qualified,'loop_predicates':len(rows),'effective_target_proven':False,'native_io_executed':False}
def main():
    p=argparse.ArgumentParser();p.add_argument('--report',type=Path,required=True);args=p.parse_args()
    print(json.dumps(validate(args.report.read_text()),sort_keys=True))
if __name__=='__main__':main()
