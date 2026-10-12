"""Strict R9 derived frontier schema. Source custody is an independent gate."""
import argparse,json
from pathlib import Path
from tools.stoneage_tw10_savedata_helper_frontier_r9 import SCHEMA,STATUS,ROOT,NESTED,STORE,RUNTIME_SHA256,SAVEDATA_SHA256
from tools.stoneage_tw10_savedata_helper_original_r8_guard import obj,integer,boolean,registers,unique,HELPER,MAX_STATES,MAX_RETURNS,GAPS,Counter
FLAGS={'nested_helper_effects_admitted','caller_resumption_admitted','filename_api_link_proven',
       'handle_buffer_size_link_proven','native_io_executed','fixed_128_byte_schema_proven','original_bytes_published'}
TOP={'schema','status','runtime_sha256','savedata_sha256','r8_verified_helper_states','nested_helper','store','structural_parent'}|FLAGS
REGS={'eax','ebx','ecx','edx','esi','edi','ebp','esp'}
CONDS={'ja','jae','jb','jbe','jcxz','jecxz','je','jg','jge','jl','jle','jne','jno','jnp','jns','jo','jp','js','loop','loope','loopne'}

def validate(text):
    if type(text) is not str or len(text.encode())>24000:raise ValueError('size')
    d=json.loads(text,object_pairs_hook=unique);obj(d,TOP)
    if (d['schema']!=SCHEMA or d['status']!=STATUS or d['runtime_sha256']!=RUNTIME_SHA256
        or d['savedata_sha256']!=SAVEDATA_SHA256 or integer(d['r8_verified_helper_states'],1,MAX_STATES)!=44):raise ValueError('identity')
    if any(d[k] is not False for k in FLAGS):raise ValueError('native/history promotion')
    h=d['nested_helper'];obj(h,HELPER)
    if h['schema']!='tw10-r8-bounded-helper-return-effects' or integer(h['root_rva'],0,2**32-1)!=NESTED:raise ValueError('helper identity')
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
    helper_n=n
    s=d['store'];obj(s,{'store_rva','write_width_bytes','base_register','index_register','index_scale',
        'displacement_region','absolute_effective_rva','effective_address_fully_known','table_or_object_ownership_proven'})
    if integer(s['store_rva'],0,2**32-1)!=STORE or integer(s['write_width_bytes'],1,4) not in (1,2,4):raise ValueError('store identity/width')
    for key in ('base_register','index_register'):
        if s[key] is not None and (type(s[key]) is not str or s[key] not in REGS):raise ValueError('address register')
    if integer(s['index_scale'],1,8) not in (1,2,4,8):raise ValueError('scale')
    region=s['displacement_region']
    if region is not None:
        obj(region,{'section','displacement_rva','raw_backed','writable'})
        if type(region['section']) is not str or region['section'] not in {'.text','.data','.bss','.rdata','.rsrc','.reloc','.idata','.edata','.tls'}:raise ValueError('section')
        integer(region['displacement_rva'],0,2**32-1);boolean(region['raw_backed']);boolean(region['writable'])
    absolute=s['base_register'] is None and s['index_register'] is None and region is not None
    if boolean(s['effective_address_fully_known'])!=absolute:raise ValueError('absolute address flag')
    expected=region['displacement_rva'] if absolute else None
    if s['absolute_effective_rva'] is not None:integer(s['absolute_effective_rva'],0,2**32-1)
    if s['absolute_effective_rva']!=expected or s['table_or_object_ownership_proven'] is not False:raise ValueError('ownership/address promotion')
    p=d['structural_parent'];obj(p,{'root_rva','nodes','edges','limit_hit','outside_or_decode_gap_count','indirect_jump_count','call_return_assumptions','loops','runtime_loop_conditions_proven','caller_resumption_admitted'})
    if integer(p['root_rva'],0,2**32-1)!=ROOT:raise ValueError('parent identity')
    nodes=integer(p['nodes'],1,256);integer(p['edges'],0,2*nodes)
    if boolean(p['limit_hit']) and nodes!=256:raise ValueError('parent cap')
    integer(p['outside_or_decode_gap_count'],0,2*nodes);integer(p['indirect_jump_count'],0,nodes);integer(p['call_return_assumptions'],0,nodes)
    if p['runtime_loop_conditions_proven'] is not False or p['caller_resumption_admitted'] is not False:raise ValueError('topology promotion')
    loops=p['loops']
    if type(loops) is not list or len(loops)>nodes:raise ValueError('loops')
    seen=set();total_nodes=0
    for loop in loops:
        obj(loop,{'node_count','min_rva','max_rva','conditional_branches','call_return_assumptions'})
        count=integer(loop['node_count'],1,nodes);total_nodes+=count
        lo=integer(loop['min_rva'],ROOT,ROOT+1024-1);hi=integer(loop['max_rva'],lo,ROOT+1024-1)
        key=(lo,hi,count)
        if key in seen:raise ValueError('duplicate SCC')
        seen.add(key);integer(loop['call_return_assumptions'],0,min(count,p['call_return_assumptions']))
        rows=loop['conditional_branches']
        if type(rows) is not list or len(rows)>count:raise ValueError('branches')
        row_seen=set()
        for row in rows:
            obj(row,{'rva','condition','target_rva','fallthrough_rva'});pos=integer(row['rva'],lo,hi)
            if pos in row_seen or type(row['condition']) is not str or row['condition'] not in CONDS:raise ValueError('branch condition')
            row_seen.add(pos)
            if row['target_rva'] is not None:integer(row['target_rva'],0,2**32-1)
            integer(row['fallthrough_rva'],pos+1,pos+15)
    if total_nodes>nodes:raise ValueError('SCC node total')
    return {'schema':'tw10-r9-strict-frontier-report-guard','nested_states':helper_n,
            'nested_qualifies_modeled_summary':qualified,'structural_loops':len(loops),
            'store_absolute_address_known':absolute,'ownership_proven':False,'native_io_executed':False}

def main():
    p=argparse.ArgumentParser();p.add_argument('--report',type=Path,required=True);args=p.parse_args()
    print(json.dumps(validate(args.report.read_text()),sort_keys=True))
if __name__=='__main__':main()
