"""Strict bounded R12 static frontier guard; runtime remains unadmitted."""
import argparse,json,re
from collections import Counter
from pathlib import Path
from tools.stoneage_tw10_savedata_frontier_r12 import SCHEMA,STATUS,ROOT,DELEGATE,CALL,QUERIES,GLOBALS,FLAGS,MAX_SAMPLES,RUNTIME_SHA256,SAVEDATA_SHA256
from tools.stoneage_tw10_savedata_inputs_r11_guard import sources
from tools.stoneage_tw10_savedata_provenance_r10_guard import geometry,REGS
from tools.stoneage_tw10_savedata_helper_original_r8_guard import obj,integer,boolean,registers,unique,HELPER,MAX_STATES,MAX_RETURNS,GAPS
TOP={'schema','status','runtime_sha256','savedata_sha256','parent_nodes','parent_edges','structural_call_return_assumptions','input_queries','call_identity','global_references','delegate_helper'}|FLAGS
KINDS={'read_candidate','write_candidate','address_candidate','unknown_candidate'}
def validate(text):
    if type(text) is not str or len(text.encode())>24000:raise ValueError('size')
    d=json.loads(text,object_pairs_hook=unique);obj(d,TOP)
    if d['schema']!=SCHEMA or d['status']!=STATUS or d['runtime_sha256']!=RUNTIME_SHA256 or d['savedata_sha256']!=SAVEDATA_SHA256:raise ValueError('identity')
    if integer(d['parent_nodes'],1,256)!=50 or integer(d['parent_edges'],1,512)!=55 or integer(d['structural_call_return_assumptions'],0,256)!=1:raise ValueError('parent graph')
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
    rows=d['input_queries']
    if type(rows) is not list or len(rows)!=len(QUERIES):raise ValueError('queries')
    for row,(site,reg) in zip(rows,QUERIES):
        obj(row,{'site_rva','register','reaching_sources','value_fully_known'})
        if integer(row['site_rva'],0,2**32-1)!=site or row['register']!=reg or row['value_fully_known'] is not False:raise ValueError('query promotion')
        sources(row['reaching_sources'],reg)
    c=d['call_identity'];obj(c,{'call_rva','kind','register_target','memory_target','direct_target_rva','import_identity','import_slot_association_proven','runtime_target_or_effects_proven'})
    if integer(c['call_rva'],0,2**32-1)!=CALL or c['runtime_target_or_effects_proven'] is not False:raise ValueError('CALL identity/promotion')
    kind=c['kind'];mem=c['memory_target'];reg=c['register_target'];direct=c['direct_target_rva'];imp=c['import_identity']
    if type(kind) is not str or kind not in ('direct','register_indirect','memory_indirect','other'):raise ValueError('CALL kind')
    if kind=='memory_indirect':geometry(mem)
    elif mem is not None:raise ValueError('nonmemory target')
    if kind=='register_indirect':
        if type(reg) is not str or reg not in REGS:raise ValueError('CALL register')
    elif reg is not None:raise ValueError('nonregister target')
    if kind=='direct':integer(direct,0,2**32-1)
    elif direct is not None:raise ValueError('nondirect target')
    association=boolean(c['import_slot_association_proven'])
    if association!=(imp is not None):raise ValueError('import association')
    if imp is not None:
        obj(imp,{'dll','name','iat_rva'});iat=integer(imp['iat_rva'],0,2**32-1)
        if type(imp['dll']) is not str or not re.fullmatch(r'[A-Za-z0-9_.-]{1,128}',imp['dll']):raise ValueError('DLL')
        if type(imp['name']) is not str or not re.fullmatch(r'[A-Za-z0-9_?.@$#-]{1,128}',imp['name']):raise ValueError('import name')
        if kind!='memory_indirect' or mem['base_register'] is not None or mem['index_register'] is not None or mem['segment_register'] is not None or mem['width_bytes']!=4:raise ValueError('false IAT shape')
        region=mem['displacement_region']
        if region is None or region['displacement_rva']!=iat or not region['raw_backed']:raise ValueError('IAT region')
    g=d['global_references'];obj(g,{'scope','decoded_instructions','decode_gap_bytes','text_bytes','globals','all_indirect_references_covered'})
    if g['scope']!='linear_text_decode_candidates_not_reachable_execution' or g['all_indirect_references_covered'] is not False:raise ValueError('reference scope promotion')
    text_n=integer(g['text_bytes'],1,331776)
    if text_n!=331776:raise ValueError('text identity')
    decoded=integer(g['decoded_instructions'],1,text_n);gap=integer(g['decode_gap_bytes'],0,text_n)
    if decoded+gap>text_n or 15*decoded+gap<text_n:raise ValueError('scan size consistency')
    globals_=g['globals']
    if type(globals_) is not list or len(globals_)!=2:raise ValueError('globals')
    for row,target in zip(globals_,GLOBALS):
        obj(row,{'global_rva','counts','samples','samples_truncated','runtime_initialization_proven'})
        if integer(row['global_rva'],0,2**32-1)!=target or row['runtime_initialization_proven'] is not False:raise ValueError('global identity/promotion')
        counts=row['counts'];obj(counts,KINDS)
        total=sum(integer(v,0,3*decoded) for v in counts.values())
        if total>3*decoded:raise ValueError('reference count')
        samples=row['samples']
        if type(samples) is not list or len(samples)!=min(total,MAX_SAMPLES) or boolean(row['samples_truncated'])!=(total>MAX_SAMPLES):raise ValueError('sample truncation')
        seen=set();sample_counts=Counter();prev=0
        for sample in samples:
            obj(sample,{'rva','kind'});rva=integer(sample['rva'],0x1000,0x1000+text_n-1)
            kind=sample['kind']
            if type(kind) is not str or kind not in KINDS or rva<prev or (rva,kind) in seen:raise ValueError('sample identity/order')
            prev=rva;seen.add((rva,kind));sample_counts[kind]+=1
        if any(sample_counts[k]>counts[k] for k in KINDS):raise ValueError('sample counts')
    return {'schema':'tw10-r12-strict-frontier-report-guard','delegate_states':n,'delegate_qualifies_modeled_summary':qualified,'import_slot_association_proven':association,'input_queries':len(rows),'native_io_executed':False,'global_initialization_proven':False}
def main():
    p=argparse.ArgumentParser();p.add_argument('--report',type=Path,required=True);args=p.parse_args()
    print(json.dumps(validate(args.report.read_text()),sort_keys=True))
if __name__=='__main__':main()
