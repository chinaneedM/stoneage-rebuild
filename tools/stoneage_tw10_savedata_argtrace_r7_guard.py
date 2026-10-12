"""Strict R7 derived-only metadata guard; format acceptance is not native IO."""
import argparse,json
from pathlib import Path
from tools.stoneage_tw10_savedata_argtrace_r7 import (
    SCHEMA,STATUS,MAX_STATES,MAX_DEPTH,MAX_SLOTS,MAX_EVENTS,STOP_NAMES,
    RUNTIME_SHA256,SAVEDATA_SHA256)
FLAGS={'actual_path_feasibility_proven','complete_filename_api_link_proven',
       'handle_buffer_size_link_proven','native_io_executed',
       'fixed_128_byte_schema_proven','original_bytes_published'}
TOP={'schema','status','runtime_sha256','savedata_sha256','seed_callee_rva','seed','trace'}|FLAGS
TRACE={'visited_states','state_limit_hit','gaps','calls','api_candidates','CreateFileA_filename_slot0_candidate'}
SEED='FOUR_R6_PHYSICAL_STACK_SLOT0_DIRECT_CALLS_ENTER_WITH_FILENAME_AT_ESP_PLUS4'

def unique(pairs):
    d={}
    for k,v in pairs:
        if k in d: raise ValueError('duplicate JSON key')
        d[k]=v
    return d

def obj(v,keys):
    if type(v) is not dict or set(v)!=keys: raise ValueError('fields')

def integer(v,lo,hi):
    if type(v) is not int or not lo<=v<=hi: raise ValueError('integer bound')
    return v

def rva(v): return integer(v,0x1000,0x1000+331776-1)

def slots(v):
    if type(v) is not list or len(v)>MAX_SLOTS: raise ValueError('slots')
    for n in v: integer(n,0,MAX_SLOTS-1)
    if v!=sorted(set(v)): raise ValueError('slot order/duplicate')
    return tuple(v)

def validate(text):
    if type(text) is not str or len(text.encode())>24000: raise ValueError('report size')
    d=json.loads(text,object_pairs_hook=unique); obj(d,TOP)
    if (d['schema']!=SCHEMA or d['status']!=STATUS or d['runtime_sha256']!=RUNTIME_SHA256
        or d['savedata_sha256']!=SAVEDATA_SHA256 or d['seed']!=SEED
        or integer(d['seed_callee_rva'],0,2**32-1)!=0x487ba): raise ValueError('source identity')
    if any(d[k] is not False for k in FLAGS): raise ValueError('unjustified promotion')
    t=d['trace']; obj(t,TRACE); n=integer(t['visited_states'],1,MAX_STATES)
    if type(t['state_limit_hit']) is not bool or (t['state_limit_hit'] and n!=MAX_STATES): raise ValueError('state cap')
    g=t['gaps']
    if type(g) is not dict or set(g)-STOP_NAMES: raise ValueError('gaps')
    for v in g.values(): integer(v,1,2*MAX_STATES)
    if type(t['calls']) is not list or type(t['api_candidates']) is not list or len(t['calls'])+len(t['api_candidates'])>MAX_EVENTS:
        raise ValueError('events')
    seen=set(); candidate=False
    for e in t['calls']:
        obj(e,{'rva','target_rva','depth','filename_stack_slots'}); rva(e['rva']); integer(e['depth'],0,MAX_DEPTH)
        if e['target_rva'] is not None: integer(e['target_rva'],0,2**32-1)
        s=slots(e['filename_stack_slots']); key=(e['rva'],e['target_rva'],e['depth'],s)
        if key in seen: raise ValueError('duplicate call')
        seen.add(key)
    seen=set()
    for e in t['api_candidates']:
        obj(e,{'rva','api','depth','filename_stack_slots'}); rva(e['rva']); integer(e['depth'],0,MAX_DEPTH)
        if e['api'] not in ('CreateFileA','ReadFile','WriteFile'): raise ValueError('API')
        s=slots(e['filename_stack_slots']); key=(e['rva'],e['api'],e['depth'],s)
        if key in seen: raise ValueError('duplicate API')
        seen.add(key)
        if e['api']=='CreateFileA' and 0 in s: candidate=True
    if type(t['CreateFileA_filename_slot0_candidate']) is not bool or t['CreateFileA_filename_slot0_candidate']!=candidate:
        raise ValueError('candidate flag')
    return {'schema':'tw10-r7-strict-prefix-report-guard','visited_states':n,
            'calls':len(t['calls']),'api_candidates':len(t['api_candidates']),
            'conditional_CreateFileA_filename_candidate':candidate,
            'complete_filename_api_link_proven':False,'native_io_executed':False}

def main():
    p=argparse.ArgumentParser();p.add_argument('--report',type=Path,required=True);args=p.parse_args()
    print(json.dumps(validate(args.report.read_text()),sort_keys=True))
if __name__=='__main__':main()
