"""Strict derived R6 metadata grammar; no original data retrieval."""
import argparse
import json
from pathlib import Path
from tools.stoneage_tw10_savedata_dataflow_r6 import (
    SCHEMA, STATUS, STOPS, MAX_PREFIX, MAX_DEPTH, MAX_NODES, MAX_EVENTS,
    RUNTIME_SHA256, SAVEDATA_SHA256, WORD_RVAS, FILE_APIS)
FLAGS={'filename_api_argument_proven','handle_buffer_size_link_proven',
       'native_io_executed','fixed_128_byte_schema_proven','original_bytes_published'}
TOP={'schema','status','runtime_sha256','savedata_sha256','sites'}|FLAGS
PREFIX={'stop','transfer_rva','direct_target_rva','import_api','filename_stack_slot','stack_tracking_precise','prefix_nodes'}
SURFACE={'visited_states','node_limit_hit','depth_limit_stops','unresolved_indirect_transfers','api_events'}
TEXT_LO=0x1000; TEXT_HI=TEXT_LO+331776

def integer(v,lo,hi):
    if type(v) is not int or not lo<=v<=hi: raise ValueError('bounded integer')
    return v

def fields(v,keys):
    if not isinstance(v,dict) or set(v)!=keys: raise ValueError('fields')

def text_rva(v): return integer(v,TEXT_LO,TEXT_HI-1)

def unique_object(pairs):
    d={}
    for k,v in pairs:
        if k in d: raise ValueError('duplicate JSON key')
        d[k]=v
    return d

def validate(text):
    if not isinstance(text,str) or len(text.encode())>24000: raise ValueError('size')
    root=json.loads(text,object_pairs_hook=unique_object); fields(root,TOP)
    if (root['schema']!=SCHEMA or root['status']!=STATUS or root['runtime_sha256']!=RUNTIME_SHA256
        or root['savedata_sha256']!=SAVEDATA_SHA256): raise ValueError('identity/status')
    if any(root[k] is not False for k in FLAGS): raise ValueError('native promotion')
    if not isinstance(root['sites'],list) or len(root['sites'])!=4: raise ValueError('sites')
    total=0
    for word,site in zip(WORD_RVAS,root['sites']):
        fields(site,{'word_rva','push_rva','first_transfer','cross_callee'})
        if integer(site['word_rva'],0,2**32-1)!=word or integer(site['push_rva'],0,2**32-1)!=word-1: raise ValueError('site identity')
        p=site['first_transfer']; fields(p,PREFIX)
        if p['stop'] not in STOPS: raise ValueError('stop')
        integer(p['prefix_nodes'],1,MAX_PREFIX)
        if type(p['stack_tracking_precise']) is not bool: raise ValueError('precision type')
        is_transfer=p['stop'] in ('call','branch')
        if is_transfer:
            text_rva(p['transfer_rva'])
            if not word-1+5<=p['transfer_rva']<=word-1+15*(MAX_PREFIX-1): raise ValueError('prefix transfer range')
        elif p['transfer_rva'] is not None: raise ValueError('nontransfer address')
        target=p['direct_target_rva']
        if target is not None:
            integer(target,0,2**32-1)
            if not is_transfer or p['import_api'] is not None: raise ValueError('transfer kind')
        if p['import_api'] is not None and (not is_transfer or p['import_api'] not in FILE_APIS): raise ValueError('API')
        slot=p['filename_stack_slot']
        if slot is not None:
            integer(slot,0,MAX_PREFIX-1)
            if p['stop']!='call' or not p['stack_tracking_precise'] or slot>p['prefix_nodes']-2: raise ValueError('slot inconsistency')
        elif p['stack_tracking_precise']: raise ValueError('precision without slot')
        surface=site['cross_callee']
        expected=target is not None and TEXT_LO<=target<TEXT_HI
        if (surface is not None)!=expected: raise ValueError('callee presence')
        if surface is None: continue
        fields(surface,SURFACE); n=integer(surface['visited_states'],0,MAX_NODES)
        if type(surface['node_limit_hit']) is not bool: raise ValueError('node flag')
        if surface['node_limit_hit'] and n!=MAX_NODES: raise ValueError('node limit')
        for key in ('depth_limit_stops','unresolved_indirect_transfers'): integer(surface[key],0,n)
        events=surface['api_events']
        if not isinstance(events,list) or len(events)>min(MAX_EVENTS,n): raise ValueError('events')
        seen=set()
        for e in events:
            fields(e,{'rva','api','min_call_depth'}); text_rva(e['rva']); integer(e['min_call_depth'],0,MAX_DEPTH)
            if e['api'] not in FILE_APIS: raise ValueError('file API')
            key=(e['rva'],e['api'])
            if key in seen: raise ValueError('duplicate API')
            seen.add(key)
        total+=len(events)
    return {'schema':'tw10-r6-strict-static-report-guard','sites':4,'api_events':total,
            'native_io_semantics_admitted':False,'original_payload_present':False}

def main():
    p=argparse.ArgumentParser(); p.add_argument('--report',type=Path,required=True); args=p.parse_args()
    print(json.dumps(validate(args.report.read_text()),sort_keys=True))
if __name__=='__main__': main()
