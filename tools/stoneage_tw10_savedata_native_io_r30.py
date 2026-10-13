"""Original mask/shift composition and CALL-supported shared writer candidates."""
import argparse,hashlib,json,tempfile
from pathlib import Path
from capstone import CS_GRP_CALL
from tools.stoneage_tw10_savedata_native_io_r29 import inspect_verified as inspect_r29,shape_at,scalar_model,SHARED,RUNTIME_SHA256,SAVEDATA_SHA256
from tools.stoneage_tw10_savedata_native_io_r29_guard import validate as validate_r29
from tools.stoneage_tw10_savedata_native_io_r28 import candidate_graph,input_surface,ALIASES
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder,direct_target
from tools.stoneage_tw10_savedata_frontier_r12 import call_identity
from tools.stoneage_tw10_savedata_mutations_r13 import write_candidate
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH,SAVEDATA_PATH
from tools.stoneage_tw10_technical_probe import find_rows,extract_row
SCHEMA='tw10-r30-original-mask-composition-shared-writer-candidates'
STATUS='PINNED_ORIGINAL_CONDITIONAL_MASK_WRITER_SOURCE_NATIVE_LINKAGE_OPEN'
PRIOR_SHA256='151b846b843165c0cf5002792f4a43904d7f2b6a3683e1d951ea3d6cf5dbe415'
MASKS=(('ReadFile',0x4a8dc,0x4a8f6,0x4a8fc),('WriteFile',0x4c5b4,0x4c5d6,0x4c5e0))
WRITER=0x4c9da;MAX_CALLERS=32;MAX_ROOTS=3
FLAGS=('actual_original_values_or_index_ranges_proven','actual_descriptor_or_handle_table_owner_proven',
       'global_actual_value_or_initialization_proven','complete_alias_writers_or_lifetime_proven',
       'actual_functions_frames_paths_proven','returning_call_or_api_effects_admitted',
       'native_filename_returned_handle_buffer128_link_proven','native_save_schema_proven','native_io_executed','original_bytes_published')

def composition(mask,shift,source):
    tokens=source.get('reaching_candidates',[])
    linked=(source.get('site_in_candidate_graph') is True and source.get('candidates_truncated') is False
            and len(tokens)==1 and tokens[0].get('origin')=='definition' and tokens[0].get('rva')==mask['site_rva'])
    a,b=scalar_model(mask,'esi'),scalar_model(shift,'esi')
    qualified=(linked and a['operation']=='and' and a['rhs']['kind']=='constant' and b['operation']=='shl')
    return {'kind':'conditional_esi_mask_then_left_shift_u32' if qualified else 'unqualified_composition',
            'unique_mask_to_shift_candidate':linked,'mask':a['rhs']['constant'] if qualified else None,
            'left_shift_count':b['rhs']['constant'] if qualified else None,'modulus':4294967296 if qualified else None,
            'original_input_or_result_known':False,'evaluated_original_result':None,'actual_index_range_or_handle_role_proven':False}

def mask_context(dec,sections,prior,api,root,site,shift_site):
    old=next(c for c in prior['contexts'] if c['api']==api and c['root_candidate_rva']==root)
    if not any(s['origin']=='definition' and s['rva']==site for q in old['inputs']['queries'] if q['site_rva']==shift_site and q['register']=='esi' for s in q['reaching_candidates']):raise ValueError('R30 mask absent from exact R29')
    nodes,edges,front,hit=candidate_graph(dec,root);mask=shape_at(dec,sections,nodes,site)
    shift=shape_at(dec,sections,nodes,shift_site)
    oldshape=next(r['shape'] for r in old['scalar_definitions'] if r['site_rva']==shift_site)
    if shift!=oldshape:raise ValueError('R29 exact shift shape changed')
    inputs=input_surface(dec,sections,nodes,edges,root,{(site,'esi'),(shift_site,'esi')})
    source=next(q for q in inputs['queries'] if q['site_rva']==shift_site and q['register']=='esi')
    return {'api':api,'root_candidate_rva':root,'supported_by_r29_context_and_definition':True,
            'mask_shape':mask,'shift_shape':shift,'mask_model':scalar_model(mask,'esi'),
            'inputs':inputs,'composition':composition(mask,shift,source),
            'graph':graph_meta(nodes,edges,front,hit),'original_descriptor_value_or_owner_proven':False}

def graph_meta(nodes,edges,front,hit):
    return {'nodes':len(nodes),'edges':len(edges),'span_bytes':768,'node_cap':256,
            'frontier':[{'reason':why,'rva':at} for why,at in front],'node_limit_hit':hit,
            'actual_entry_path_proven':False,'returning_call_assumption_only':True}

def discover_writer(dec,site=WRITER):
    lo=max(dec.lo,site-384);hi=site+16;pos=dec.lo;boundaries=set();calls=[];decoded=0;gaps=0
    while pos<dec.hi:
        ins=dec.at(pos)
        if ins is None:gaps+=1;pos+=1;continue
        decoded+=1;boundaries.add(pos)
        if ins.group(CS_GRP_CALL) and ins.mnemonic=='call' and len(ins.operands)==1:
            target=direct_target(ins,dec.base)
            if target is not None and lo<=target<hi:calls.append({'site_rva':pos,'target_rva':target,'kind':'call','executed_or_true_entry_proven':False})
        pos+=ins.size
    roots=sorted({r['target_rva'] for r in calls if r['target_rva']<=site and r['target_rva'] in boundaries},reverse=True)[:MAX_ROOTS]
    selected=[{'root_rva':r,'full_linear_scan_boundary_candidate':True,
               'supporting_call_rva':next(x['site_rva'] for x in calls if x['target_rva']==r),'actual_entry_proven':False} for r in roots]
    return {'scope':'full_raw_text_direct_CALL_targets_near_writer','writer_rva':site,'window_start_rva':lo,'window_end_rva':hi,
            'text_start_rva':dec.lo,'text_bytes':dec.hi-dec.lo,'decoded_instructions':decoded,'decode_gap_bytes':gaps,
            'writer_is_linear_boundary_candidate':site in boundaries,'caller_count':len(calls),'caller_samples':calls[:MAX_CALLERS],
            'caller_samples_truncated':len(calls)>MAX_CALLERS,'selected_root_candidates':selected,
            'root_selection':'nearest_earlier_linear_boundary_direct_call_targets_max3',
            'complete_indirect_callers_or_real_entries_proven':False}

def writer_context(dec,sections,imports,discovery,site=WRITER):
    store=write_candidate(dec,site,sections,expected_global=SHARED)
    regs=[r for r in store['value_input_registers'] if r in ALIASES];contexts=[]
    for row in discovery['selected_root_candidates']:
        root=row['root_rva'];ident=call_identity(dec,row['supporting_call_rva'],imports,sections)
        if ident['kind']!='direct' or ident['direct_target_rva']!=root:raise ValueError('R30 direct caller changed')
        nodes,edges,front,hit=candidate_graph(dec,root)
        contexts.append({'root_candidate_rva':root,'caller_identity':ident,'graph':graph_meta(nodes,edges,front,hit),
                         'writer_site_in_candidate_graph':site in nodes,
                         'inputs':input_surface(dec,sections,nodes,edges,root,{(site,r) for r in regs}),
                         'actual_store_value_owner_or_initialization_proven':False})
    return {'store_candidate':store,'source_query_registers':regs,'contexts':contexts,
            'qualified_actual_writer_execution_or_callee_return_proven':False}

def inspect_verified(runtime,savedata):
    prior=inspect_r29(runtime,savedata);validate_r29(prior)
    digest=hashlib.sha256((json.dumps(prior,sort_keys=True)+'\n').encode()).hexdigest()
    if digest!=PRIOR_SHA256:raise ValueError('R29 exact original derivative changed')
    if not any(r['site_rva']==WRITER and r['operand_index']==0 and r['operand'].get('decoder_write') is True for r in prior['shared_address_references']['samples']):raise ValueError('R29 original writer candidate missing')
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'sa_3.exe';p.write_bytes(runtime);data,pe,base,sections,imports=image_layout(p)
    for sec,raw in zip(sections,pe.sections):sec['characteristics']=int(raw.Characteristics)
    t=next(s for s in sections if s['name']=='.text');dec=Decoder(data[t['raw']:t['raw']+t['raw_size']],t['rva'],base)
    discovery=discover_writer(dec)
    return {'schema':SCHEMA,'status':STATUS,'runtime_sha256':RUNTIME_SHA256,'savedata_sha256':SAVEDATA_SHA256,
            'r29_exact_original_revalidated':True,'r29_exact_report_sha256':digest,'static_only':True,
            'mask_contexts':[mask_context(dec,sections,prior,*row) for row in MASKS],
            'writer_discovery':discovery,'writer_inputs':writer_context(dec,sections,imports,discovery),**{k:False for k in FLAGS}}

def main():
    p=argparse.ArgumentParser();p.add_argument('--bin',type=Path,required=True)
    image,rows,_,_=find_rows(p.parse_args().bin)
    try:
        files={r['path']:r for r in rows if not r['is_dir']}
        with tempfile.TemporaryDirectory() as td:
            exe,saved=Path(td)/'sa_3.exe',Path(td)/'savedata.dat'
            extract_row(image,files[RUNTIME_PATH],exe);extract_row(image,files[SAVEDATA_PATH],saved)
            report=inspect_verified(exe.read_bytes(),saved.read_bytes())
    finally:image.close()
    print(json.dumps(report,sort_keys=True))
if __name__=='__main__':main()
