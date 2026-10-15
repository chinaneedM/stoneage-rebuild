"""Pinned write/close conditional return expressions and structural bypass witness."""
import argparse,hashlib,json
from collections import deque
from pathlib import Path
SHA='3e562ab02a80e0f6516f8a91c93b897eef05f606be62f1df5cb48686d64114e6'

def route(edges,start,end,excluded=()):
    excluded=set(excluded);adj={}
    for a,b in edges:
        if a not in excluded and b not in excluded:adj.setdefault(a,[]).append(b)
    q=deque([(start,[start])]);seen=set()
    while q and len(seen)<256:
        a,path=q.popleft()
        if a in seen or a in excluded:continue
        seen.add(a)
        if a==end:return path
        q.extend((b,path+[b]) for b in sorted(adj.get(a,[])))
    return None

def derive(raw):
    if len(raw)!=203899 or hashlib.sha256(raw).hexdigest()!=SHA:raise ValueError('R57 source custody')
    d=json.loads(raw);w,c=d['contexts'];wr={r['site_rva']:r for r in w['instruction_shapes']};cr={r['site_rva']:r for r in c['instruction_shapes']}
    if w['root_candidate_rva']!=0x48bbc or c['root_candidate_rva']!=0x4856c:raise ValueError('R57 context identities')
    path=route(w['bounded_edges'],0x48bbc,0x48c1a,(0x48c5e,));tail=route(w['bounded_edges'],0x48c1a,0x48caa,(0x48c5e,));ret=route(w['bounded_edges'],0x48caa,0x48cb1)
    if not path or not tail or not ret:raise ValueError('R57 buffer-copy structural witness')
    witness=path+tail[1:]+ret[1:]
    returns=[]
    for context in (w,c):
        for r in context['return_analysis']['return_contexts']:
            q=next(q for q in r['eax_source_graph']['queries'] if q['site_rva']==r['shape']['site_rva'] and q['register']=='eax')
            returns.append({'root_candidate_rva':context['root_candidate_rva'],'return_site_rva':r['shape']['site_rva'],'direct_eax_source_candidates':q['source_candidates'],'actual_return_value_proven':False})
    return {'schema':'tw10-r57-pinned-conditional-write-close-return-contract','source_sha256':SHA,
      'write_conditional_frame':{'entry_ebp_offset_after_push_ebp_and_mov_ebp_esp':-4,'requires_valid_preserved_ebp_stack_and_nonalias_memory':True,
        'initial_entry_slot_roles':[{'entry_esp_offset':4,'role':'buffer shaped'},{'entry_esp_offset':8,'role':'element size shaped'},{'entry_esp_offset':12,'role':'element count shaped'},{'entry_esp_offset':16,'role':'object shaped, later overwritten with block quantity'}]},
      'write_return_syntax':{'product_shape_sites':[0x48bc3,0x48bc6,0x48bcd],'zero_product_return_site':0x48bd9,'normal_completion_count_load_site':0x48caa,
        'partial_progress_sites':[0x48cb6,0x48cbb,0x48cbd,0x48cbf,0x48cc1],
        'partial_formula_candidates':'u32(EAX_snapshot - EBX_remaining) / entry_element_size -> EAX quotient, assuming valid preserved frame/values/nonzero divisor; snapshot may come from saved total or EDI',
        'normal_completion_expression':'return original count-shaped slot when the bounded remaining-count loop reaches zero, under valid nonaliased frame assumptions',
        'zero_product_expression':'return0 when low32(size*count)==0 under valid input/frame arithmetic assumptions',
        'native_context_return_minus_one_compare_site':0x48c66,'native_context_short_return_unsigned_compare_site':0x48c70,'native_error_or_short_status_or20_site':0x48cb2,
        'native_error_value_or_actual_transferred_bytes_proven':False},
      'buffer_copy_path_without_direct_native_context_call':{'path_rvas':witness,'buffer_copy_call_rva':0x48c1a,'buffer_copy_target_rva':0x4aae0,'avoided_native_context_call_rva':0x48c5e,'normal_count_load_rva':0x48caa,
        'all_adjacent_edges_in_bounded_graph':True,'returning_calls_assumed':True,'actual_path_feasibility_or_native_write_proven':False},
      'close_syntax':{'conditional_input_pointer_entry_offset':4,'object_flag_load_rva':0x48575,'flag40_test_rva':0x48578,'flag83_test_rva':0x48581,
        'literal_minus_one_eax_site':0x4857c,'initial_minus_one_edi_site':0x48572,'first_helper_return_to_edi_site':0x4858c,
        'first_helper_call_rva':0x48586,'shared_write_close_helper_target_rva':0x4a657,'intervening_opaque_call_rvas':[0x4858e,0x48596,0x485af],
        'last_helper_sign_test_rva':0x4859e,'negative_result_sets_edi_minus_one_rva':0x485a2,'object_plus28_optional_cleanup_call_rva':0x485af,
        'return_edi_to_eax_site':0x485b9,'object_flags_clear_site':0x485bb,'actual_flush_close_error_or_callee_preservation_proven':False},
      'direct_return_source_surfaces':returns,
      'caller_obligation':'R56 unsigned count test and literal1 overwrite do not establish native write/close/flush success',
      'actual_buffering_api_ownership_native_count_flush_close_or_persistence_proven':False}

def validate(d,raw):
    if json.dumps(d,sort_keys=True,separators=(',',':'))!=json.dumps(derive(raw),sort_keys=True,separators=(',',':')):raise ValueError('R57 contract mismatch')
    return True

def main():
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--verify',type=Path);a=p.parse_args();raw=a.source.read_bytes()
    if a.verify:validate(json.loads(a.verify.read_text()),raw);print('TW10_R57_RETURN_CONTRACT=PASS; ACTUAL_NATIVE_PERSISTENCE=OPEN')
    else:print(json.dumps(derive(raw),sort_keys=True))
if __name__=='__main__':main()
