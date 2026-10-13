"""R27 bounded conditional API metadata; original custody checked separately."""
import argparse,json
from pathlib import Path
from tools.stoneage_tw10_savedata_native_io_r27 import *
from tools.stoneage_tw10_savedata_upstream_r22_guard import source_guard,FORBIDDEN

def check(ok,why):
    if not ok:raise ValueError('R27 '+why)

def validate(d):
    check(isinstance(d,dict) and d.get('schema')==SCHEMA and d.get('status')==STATUS,'schema')
    check(d.get('runtime_sha256')==RUNTIME_SHA256 and d.get('savedata_sha256')==SAVEDATA_SHA256,'hash')
    check(d.get('r26_exact_original_revalidated') is True and d.get('r26_exact_report_sha256')==PRIOR_SHA256
          and d.get('static_only') is True and d.get('savedata_literal_rva')==EXPECTED_STRING_RVA,'prior chain')
    check(all(d.get(k) is False for k in FLAGS),'promotion')
    inv=d.get('inventory',{});lo=inv.get('text_start_rva');size=inv.get('text_bytes')
    check(inv.get('scope')=='full_raw_text_linear_imported_call_candidates' and type(lo) is int and lo>=0
          and type(size) is int and 0<size<=1000000 and type(inv.get('decoded_instructions')) is int
          and 0<inv['decoded_instructions']<=size and type(inv.get('decode_gap_bytes')) is int
          and 0<=inv['decode_gap_bytes']<=size and inv.get('all_indirect_api_sites_or_runtime_paths_proven') is False,'inventory scope')
    apis=inv.get('apis');check(isinstance(apis,list) and len(apis)==3,'API count')
    by={}
    for row,api in zip(apis,APIS):
        count=row.get('count');samples=row.get('samples')
        check(row.get('name')==api and type(count) is int and 0<=count<=inv['decoded_instructions']
              and isinstance(samples,list) and len(samples)==min(count,MAX_API_SAMPLES)
              and row.get('samples_truncated') is (count>MAX_API_SAMPLES),'API inventory bounds')
        last=-1
        for sample in samples:
            at=sample.get('site_rva');slot=sample.get('iat_rva')
            check(type(at) is int and lo<=at<lo+size and at>last and type(slot) is int and slot>=0,'API sample')
            last=at
        by[api]=row
    rows=d.get('selected_api_details');check(isinstance(rows,list) and 1<=len(rows)<=MAX_DETAILS,'detail count')
    expected=[('CreateFileA',CREATE_SITE)]+[(api,s['site_rva']) for api in APIS[1:] for s in by[api]['samples'][:2]]
    check([(r.get('api'),r.get('site_rva')) for r in rows]==expected,'detail selection')
    for r in rows:
        api,at,anchor=r['api'],r['site_rva'],r.get('linear_anchor_rva')
        check(type(anchor) is int and lo<=anchor<=at and at-anchor<=96,'anchor bound')
        ident=r.get('identity',{});imp=ident.get('import_identity') or {};g=ident.get('memory_target') or {}
        check(ident.get('call_rva')==at and ident.get('kind')=='memory_indirect' and imp.get('name')==api
              and str(imp.get('dll','')).lower()=='kernel32.dll' and ident.get('import_slot_association_proven') is True
              and ident.get('runtime_target_or_effects_proven') is False and g.get('width_bytes')==4
              and all(g.get(k) is None for k in ('base_register','index_register','segment_register'))
              and g.get('displacement_region',{}).get('displacement_rva')==imp.get('iat_rva')
              and {'site_rva':at,'iat_rva':imp.get('iat_rva')} in by[api]['samples'],'import identity')
        check(all(r.get(k) is False for k in ('actual_entry_or_feasible_path_proven','original_file_handle_buffer_proven','related_to_savedata_literal_proven'))
              and r.get('external_return_eax_unknown') is True,'detail promotion')
        s=r.get('suffix',{});pushes=s.get('pushes');ps=r.get('push_candidates')
        check(s.get('conditional_pre_call_esp_only') is True and s.get('abi_roles_applied') is False
              and s.get('actual_stack_values_known') is False and type(s.get('linear_call_boundary_reached')) is bool
              and s.get('stop_reason') in ('candidate_anchor','control_transfer','stack_or_memory_barrier','push_cap','decode_or_boundary_gap','bound')
              and isinstance(pushes,list) and len(pushes)<=24 and (s['linear_call_boundary_reached'] or not pushes)
              and isinstance(ps,list) and len(ps)==len(pushes),'suffix scope')
        previous=at
        for n,(p,c) in enumerate(zip(pushes,ps)):
            check(type(p.get('site_rva')) is int and anchor<=p['site_rva']<previous
                  and p.get('conditional_pre_call_esp_offset')==4*n and p.get('input',{}).get('width_bytes')==4
                  and all(c.get(k)==v for k,v in p.items()) and c.get('api_parameter_role_proven') is False
                  and c.get('original_operand_value_proven') is False,'PUSH geometry/value')
            previous=p['site_rva'];source=c.get('register_source');shape=p['input']
            if shape.get('kind')=='register':
                source_guard(source);check(source.get('candidate_anchor_rva')==anchor,'PUSH source anchor')
            else:check(source is None,'nonregister source')
            check(c.get('savedata_literal_address_candidate') is savedata_literal_candidate(shape,source,0x400000),'literal candidate')
        regs=r.get('registers_before_call',{})
        check(set(regs)=={'eax','ecx','edx'},'register keys')
        for source in regs.values():
            source_guard(source);check(source.get('candidate_anchor_rva')==anchor,'register anchor')
    callers=d.get('nearby_direct_callers',{});windows=callers.get('windows')
    check(callers.get('scope')=='direct_call_targets_near_selected_api_windows'
          and windows==[{'api_site_rva':r['site_rva'],'start_rva':max(lo,r['site_rva']-512),'end_rva':r['site_rva']+64} for r in rows]
          and callers.get('all_callers_or_true_entries_proven') is False,'caller scope')
    count=callers.get('count');samples=callers.get('samples')
    check(type(count) is int and 0<=count<=inv['decoded_instructions'] and isinstance(samples,list)
          and len(samples)==min(count,MAX_CALLERS) and callers.get('samples_truncated') is (count>MAX_CALLERS),'caller bound')
    last=-1
    for r in samples:
        at=r.get('site_rva');target=r.get('target_rva')
        check(type(at) is int and lo<=at<lo+size and at>last and type(target) is int and r.get('kind')=='call'
              and any(w['start_rva']<=target<w['end_rva'] for w in windows)
              and r.get('executed_or_true_entry_proven') is False,'caller primitive')
        last=at
    def ban(o):
        if isinstance(o,dict):
            check(not set(o)&FORBIDDEN,'payload')
            for v in o.values():ban(v)
        elif isinstance(o,list):
            for v in o:ban(v)
    ban(d);return True

def main():
    p=argparse.ArgumentParser();p.add_argument('--report',type=Path,required=True)
    path=p.parse_args().report;check(path.stat().st_size<=70000,'size')
    validate(json.loads(path.read_text()));print('TW10_R27_STRICT_STATIC=PASS; NATIVE_SAVE=OPEN')
if __name__=='__main__':main()
