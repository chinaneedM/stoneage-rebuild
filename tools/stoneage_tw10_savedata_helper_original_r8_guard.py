"""Strict derived helper metadata validation, no original data retrieval."""
import argparse,json
from pathlib import Path
from collections import Counter
from tools.stoneage_tw10_savedata_helper_original_r8 import SCHEMA,STATUS,ROOT,RUNTIME_SHA256,SAVEDATA_SHA256
from tools.stoneage_tw10_savedata_helper_effects_r8 import GAPS,MAX_RETURNS,MAX_STATES
FLAGS={'historical_helper_effect_summary_accepted','caller_resumption_admitted','filename_api_link_proven',
       'handle_buffer_size_link_proven','native_io_executed','fixed_128_byte_schema_proven','original_bytes_published'}
TOP={'schema','status','runtime_sha256','savedata_sha256','r7_caller_rva','r7_verified_trace_states','helper'}|FLAGS
HELPER={'schema','root_rva','visited_states','state_limit_hit','control_flow_cycle','gaps','gap_sites',
        'return_paths','common_preserved_registers','uniform_ret_cleanup_bytes','qualifies_modeled_return_effect_summary',
        'original_helper_accepted','native_io_executed'}
REG_ORDER=['eax','ebx','ecx','edx','esi','edi','ebp']

def unique(pairs):
    d={}
    for k,v in pairs:
        if k in d:raise ValueError('duplicate JSON key')
        d[k]=v
    return d

def obj(v,keys):
    if type(v) is not dict or set(v)!=keys:raise ValueError('fields')

def integer(v,lo,hi):
    if type(v) is not int or not lo<=v<=hi:raise ValueError('bounded integer')
    return v

def boolean(v):
    if type(v) is not bool:raise ValueError('boolean type')
    return v

def registers(v,ordered=False):
    if type(v) is not list or len(v)>7 or any(type(n) is not str or n not in REG_ORDER for n in v) or len(set(v))!=len(v):raise ValueError('registers')
    if ordered and v!=[r for r in REG_ORDER if r in v]:raise ValueError('register order')
    return set(v)

def validate(text):
    if type(text) is not str or len(text.encode())>24000:raise ValueError('size')
    d=json.loads(text,object_pairs_hook=unique);obj(d,TOP)
    if (d['schema']!=SCHEMA or d['status']!=STATUS or d['runtime_sha256']!=RUNTIME_SHA256
        or d['savedata_sha256']!=SAVEDATA_SHA256 or integer(d['r7_caller_rva'],0,2**32-1)!=0x4879a
        or integer(d['r7_verified_trace_states'],1,MAX_STATES)!=136):raise ValueError('source identity')
    if any(d[k] is not False for k in FLAGS):raise ValueError('native/history promotion')
    h=d['helper'];obj(h,HELPER)
    if h['schema']!='tw10-r8-bounded-helper-return-effects' or integer(h['root_rva'],0,2**32-1)!=ROOT:raise ValueError('helper identity')
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
    return {'schema':'tw10-r8-original-report-guard','states':n,'gap_sites':len(sites),
            'return_paths':len(paths),'qualifies_modeled_summary':qualified,
            'original_helper_resumption_admitted':False,'native_io_executed':False}

def main():
    p=argparse.ArgumentParser();p.add_argument('--report',type=Path,required=True);args=p.parse_args()
    print(json.dumps(validate(args.report.read_text()),sort_keys=True))
if __name__=='__main__':main()
