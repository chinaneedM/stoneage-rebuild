"""R25 derivative semantic limits; original custody and exact JSON separate."""
import argparse,json
from pathlib import Path
from tools.stoneage_tw10_savedata_upstream_r25 import (
    SCHEMA,STATUS,PRIOR_SHA256,FLAGS,BOUNDARIES,RANGES,STARTS,SETE,PUSH,SETE_ANCHORS,
    MAX_SAMPLES,RUNTIME_SHA256,SAVEDATA_SHA256)
from tools.stoneage_tw10_savedata_upstream_r22_guard import source_guard,FORBIDDEN

def check(ok,why):
    if not ok:raise ValueError('R25 '+why)

def validate(d):
    check(isinstance(d,dict) and d.get('schema')==SCHEMA and d.get('status')==STATUS,'schema')
    check(d.get('runtime_sha256')==RUNTIME_SHA256 and d.get('savedata_sha256')==SAVEDATA_SHA256,'hash identity')
    check(d.get('r24_exact_original_revalidated') is True and d.get('r24_exact_report_sha256')==PRIOR_SHA256
          and d.get('static_only') is True,'exact R24 chain')
    check(all(d.get(k) is False for k in FLAGS),'runtime promotion')
    scan=d.get('linear_boundary_callers',{})
    check(scan.get('scope')=='full_raw_text_linear_candidates_not_executed_paths'
          and scan.get('all_incoming_callers_covered') is False
          and scan.get('complete_runtime_instruction_alignment_proven') is False,'linear scope')
    for k in ('text_start_rva','text_end_rva','text_bytes','decoded_instructions','decode_gap_bytes','direct_transfer_candidate_count','indirect_transfers_not_resolved'):
        check(type(scan.get(k)) is int and scan[k]>=0,'scan integer')
    check(0<scan['text_bytes']<=1000000 and scan['text_end_rva']-scan['text_start_rva']==scan['text_bytes']
          and scan['decoded_instructions']<=scan['text_bytes'] and scan['decode_gap_bytes']<=scan['text_bytes'],'scan bound')
    check(scan.get('target_ranges')==[{'start_rva':a,'end_rva':b} for a,b in RANGES],'target ranges')
    q=scan.get('boundary_queries');check(isinstance(q,list) and len(q)==len(BOUNDARIES),'boundary list')
    for row,site in zip(q,BOUNDARIES):
        check(row.get('query_rva')==site and type(row.get('is_linear_decode_boundary')) is bool,'query identity')
        a,b=row.get('instruction_start_rva'),row.get('instruction_end_rva')
        if a is None:check(b is None and row['is_linear_decode_boundary'] is False,'unmapped boundary')
        else:check(type(a) is int and type(b) is int and scan['text_start_rva']<=a<=site<b<=scan['text_end_rva']
                   and b-a<=15 and row['is_linear_decode_boundary']==(a==site),'boundary span')
    rows=scan.get('samples');count=scan['direct_transfer_candidate_count']
    check(isinstance(rows,list) and len(rows)==min(count,MAX_SAMPLES)
          and scan.get('samples_truncated')==(count>MAX_SAMPLES),'transfer cap/count')
    previous=-1
    for r in rows:
        check(type(r.get('site_rva')) is int and previous<r['site_rva']<scan['text_end_rva']
              and r['site_rva']>=scan['text_start_rva'] and type(r.get('target_rva')) is int
              and any(a<=r['target_rva']<b for a,b in RANGES)
              and r.get('kind') in ('call','jump','conditional_jump')
              and r.get('executed_or_true_entry_proven') is False,'transfer candidate')
        previous=r['site_rva']
    starts=d.get('new_start_candidates');check(isinstance(starts,list) and len(starts)==2,'start candidates')
    for s,(name,root,call) in zip(starts,STARTS):
        check((s.get('name'),s.get('root_rva'),s.get('call_rva'))==(name,root,call)
              and type(s.get('nodes')) is int and 1<=s['nodes']<=128
              and type(s.get('edges')) is int and 0<=s['edges']<=350
              and type(s.get('call_in_candidate_graph')) is bool
              and s.get('true_entry_or_actual_path_proven') is False
              and s.get('original_stack_values_proven') is False,'new start identity/scope')
        p=s.get('prefix',{});suf=p.get('r23_suffix',{})
        check(p.get('anchor_rva')==root and p.get('call_rva')==call
              and p.get('verified_entry_or_alignment') is False and p.get('actual_stack_values_known') is False
              and p.get('all_incoming_paths_proven') is False
              and suf.get('conditional_pre_call_esp_only') is True and suf.get('abi_roles_applied') is False
              and suf.get('actual_stack_values_known') is False,'prefix role')
        pushes=suf.get('pushes');check(isinstance(pushes,list) and len(pushes)<=24,'prefix push cap')
        prev=call
        for n,v in enumerate(pushes):
            check(root<=v.get('site_rva',-1)<prev and v.get('conditional_pre_call_esp_offset')==4*n
                  and v.get('input',{}).get('width_bytes')==4,'prefix push shape')
            prev=v['site_rva']
    partial=d.get('sete_partial_frontier',{});op=partial.get('one_byte_destination',{})
    check(partial.get('site_rva')==SETE and partial.get('push_rva')==PUSH
          and op.get('kind')=='register' and op.get('register')=='al' and op.get('width_bytes')==1
          and op.get('decoder_write') is True and partial.get('upper_24_bits_not_written_by_sete') is True
          and partial.get('whole_eax_return_or_argument_known') is False,'partial SETE shape/effect')
    rows=partial.get('candidate_contexts');check(isinstance(rows,list) and len(rows)==2,'SETE contexts')
    for row,root in zip(rows,SETE_ANCHORS):
        check(row.get('anchor_rva')==root and type(row.get('site_in_candidate_graph')) is bool
              and type(row.get('nodes')) is int and 1<=row['nodes']<=128
              and row.get('whole_eax_composed_value_proven') is False and row.get('actual_zf_known') is False,'SETE context scope')
        source_guard(row.get('eax_before_partial_write',{}));source_guard(row.get('eax_before_push',{}))
        tokens=row.get('flag_sources');check(isinstance(tokens,list) and len(tokens)<=24,'flag cap')
        for t in tokens:
            check(t.get('origin') in ('entry','unknown_call','definition') and type(t.get('rva')) is int,'flag identity')
            if t['origin']!='definition':check(t.get('semantic') is None,'opaque flag effect')
    inputs=d.get('realloc_new_anchor_inputs');expected=((0x4a0ab,'eax'),(0x4a0ab,'ecx'),(0x4a0af,'ecx'))
    check(isinstance(inputs,list) and len(inputs)==3,'realloc inputs')
    for q,(site,reg) in zip(inputs,expected):
        check((q.get('site_rva'),q.get('register'))==(site,reg) and q.get('runtime_input_value_proven') is False,'input identity/value')
        source_guard(q.get('candidate_source',{}))
        check(q['candidate_source'].get('candidate_anchor_rva')==STARTS[1][1],'input root')
    def ban(o):
        if isinstance(o,dict):
            check(not set(o)&FORBIDDEN,'proprietary payload')
            for v in o.values():ban(v)
        elif isinstance(o,list):
            for v in o:ban(v)
    ban(d);return True

def main():
    p=argparse.ArgumentParser();p.add_argument('--report',type=Path,required=True)
    path=p.parse_args().report;check(path.stat().st_size<=70000,'size')
    validate(json.loads(path.read_text()));print('TW10_R25_STRICT_STATIC=PASS; NATIVE_SAVE=OPEN')
if __name__=='__main__':main()
