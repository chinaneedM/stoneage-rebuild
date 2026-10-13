"""Original R27 file API inventory and conditional local argument surface.

Full raw .text linear decode is a candidate universe. Imported CALL identity,
pre-CALL PUSH geometry and nearby direct callers are separate evidence axes.
No Windows ABI roles, original filename/handle/buffer linkage, execution,
successful external return, CRT ownership or save schema is inferred.
"""
import argparse,hashlib,json,tempfile
from collections import deque
from pathlib import Path
from capstone import CS_GRP_CALL,CS_GRP_JUMP
from tools.stoneage_tw10_savedata_upstream_r26 import inspect_verified as inspect_r26,RUNTIME_SHA256,SAVEDATA_SHA256
from tools.stoneage_tw10_savedata_upstream_r26_guard import validate as validate_r26
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder,direct_target
from tools.stoneage_tw10_savedata_frontier_r12 import call_identity
from tools.stoneage_tw10_savedata_upstream_r23 import local_push_suffix
from tools.stoneage_tw10_savedata_write_shapes_r17 import candidate_sources
from tools.stoneage_tw10_savedata_instruction_probe import EXPECTED_STRING_RVA
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH,SAVEDATA_PATH
from tools.stoneage_tw10_technical_probe import find_rows,extract_row

SCHEMA='tw10-r27-original-native-file-api-conditional-arguments'
STATUS='PINNED_ORIGINAL_STATIC_API_CANDIDATES_FILENAME_HANDLE_BUFFER_OPEN'
PRIOR_SHA256='ff829f3aa6b1ebfaf2f2d251581293ca734ef4837f7276f54000f364085b2122'
APIS=('CreateFileA','ReadFile','WriteFile')
CREATE_SITE=0x4ed01
MAX_API_SAMPLES=32
MAX_CALLERS=48
MAX_DETAILS=5
FLAGS=('actual_api_calls_executed','true_function_entries_proven','all_indirect_api_sites_proven',
       'original_filename_api_link_proven','original_create_return_handle_proven','original_handle_read_write_link_proven',
       'original_buffer_length128_link_proven','windows_abi_roles_applied','crt_or_file_object_owner_proven',
       'caller_return_effects_admitted','native_save_schema_proven','native_io_executed','original_bytes_published')

def scan_apis(dec,sections,imports):
    pos=dec.lo;decoded=0;gaps=0;history=deque(maxlen=64);all_calls=[];transfers=[]
    counts={api:0 for api in APIS};samples={api:[] for api in APIS}
    while pos<dec.hi:
        ins=dec.at(pos)
        if ins is None:gaps+=1;history.clear();pos+=1;continue
        decoded+=1
        if ins.group(CS_GRP_CALL) and ins.mnemonic=='call' and len(ins.operands)==1:
            identity=call_identity(dec,pos,imports,sections)
            imported=identity['import_identity']
            if (imported and imported['dll'].lower()=='kernel32.dll' and imported['name'] in APIS):
                api=imported['name'];counts[api]+=1
                if len(samples[api])<MAX_API_SAMPLES:
                    samples[api].append({'site_rva':pos,'iat_rva':imported['iat_rva']})
                anchors=[x for x in history if pos-x<=96]
                all_calls.append({'api':api,'site_rva':pos,'anchor_rva':anchors[0] if anchors else pos})
        if ins.group(CS_GRP_CALL) or ins.group(CS_GRP_JUMP):
            target=direct_target(ins,dec.base)
            if target is not None:
                kind='call' if ins.group(CS_GRP_CALL) else ('jump' if ins.mnemonic in ('jmp','ljmp') else 'conditional_jump')
                transfers.append({'site_rva':pos,'target_rva':target,'kind':kind})
        history.append(pos);pos+=ins.size
    inventory={'scope':'full_raw_text_linear_imported_call_candidates','text_start_rva':dec.lo,'text_bytes':dec.hi-dec.lo,
               'decoded_instructions':decoded,'decode_gap_bytes':gaps,
               'apis':[{'name':api,'count':counts[api],'samples':samples[api],'samples_truncated':counts[api]>MAX_API_SAMPLES} for api in APIS],
               'all_indirect_api_sites_or_runtime_paths_proven':False}
    return inventory,all_calls,transfers

def choose_details(calls,create_site=CREATE_SITE):
    selected=[r for r in calls if r['api']=='CreateFileA' and r['site_rva']==create_site]
    if len(selected)!=1:raise ValueError('R27 pinned CreateFileA CALL not in original linear inventory')
    for api in ('ReadFile','WriteFile'):
        selected.extend([r for r in calls if r['api']==api][:2])
    if len(selected)>MAX_DETAILS:raise ValueError('R27 detail cap')
    return selected

def savedata_literal_candidate(shape,source,base):
    literal=base+EXPECTED_STRING_RVA
    if shape.get('kind')=='immediate':return shape.get('constant')==literal
    if shape.get('kind')!='register' or source is None:return False
    tokens=source.get('reaching_candidates',[])
    if len(tokens)!=1 or source.get('candidates_truncated') is not False:return False
    sem=tokens[0].get('semantic') or {}
    return tokens[0].get('origin')=='definition' and sem.get('kind')=='constant_assignment' and sem.get('constant')==literal and sem.get('width_bits')==32

def detail(dec,sections,imports,row):
    site,anchor=row['site_rva'],row['anchor_rva']
    ident=call_identity(dec,site,imports,sections)
    if not ident['import_identity'] or ident['import_identity']['name']!=row['api']:raise ValueError('R27 API identity changed')
    suffix=local_push_suffix(dec,sections,anchor,site)
    pushes=[]
    for p in suffix['pushes']:
        shape=p['input'];reg=shape.get('register') if shape.get('kind')=='register' else None
        source=candidate_sources(dec,p['site_rva'],reg,sections,anchor) if reg else None
        pushes.append({**p,'register_source':source,'savedata_literal_address_candidate':savedata_literal_candidate(shape,source,dec.base),
                       'api_parameter_role_proven':False,'original_operand_value_proven':False})
    return {'api':row['api'],'site_rva':site,'linear_anchor_rva':anchor,'identity':ident,
            'suffix':suffix,'push_candidates':pushes,'registers_before_call':{
                r:candidate_sources(dec,site,r,sections,anchor) for r in ('eax','ecx','edx')},
            'actual_entry_or_feasible_path_proven':False,'original_file_handle_buffer_proven':False,
            'external_return_eax_unknown':True,'related_to_savedata_literal_proven':False}

def caller_surface(transfers,selected,text_lo):
    windows=[{'api_site_rva':r['site_rva'],'start_rva':max(text_lo,r['site_rva']-512),'end_rva':r['site_rva']+64} for r in selected]
    rows=[{**r,'executed_or_true_entry_proven':False} for r in transfers if r['kind']=='call' and any(w['start_rva']<=r['target_rva']<w['end_rva'] for w in windows)]
    return {'scope':'direct_call_targets_near_selected_api_windows','windows':windows,'count':len(rows),
            'samples':rows[:MAX_CALLERS],'samples_truncated':len(rows)>MAX_CALLERS,'all_callers_or_true_entries_proven':False}

def inspect_verified(runtime,savedata):
    prior=inspect_r26(runtime,savedata);validate_r26(prior)
    digest=hashlib.sha256((json.dumps(prior,sort_keys=True)+'\n').encode()).hexdigest()
    if digest!=PRIOR_SHA256:raise ValueError('R26 exact original derivative changed')
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'sa_3.exe';p.write_bytes(runtime);data,pe,base,sections,imports=image_layout(p)
    for sec,raw in zip(sections,pe.sections):sec['characteristics']=int(raw.Characteristics)
    t=next(s for s in sections if s['name']=='.text');dec=Decoder(data[t['raw']:t['raw']+t['raw_size']],t['rva'],base)
    inventory,calls,transfers=scan_apis(dec,sections,imports);selected=choose_details(calls)
    return {'schema':SCHEMA,'status':STATUS,'runtime_sha256':RUNTIME_SHA256,'savedata_sha256':SAVEDATA_SHA256,
            'r26_exact_original_revalidated':True,'r26_exact_report_sha256':digest,'static_only':True,
            'savedata_literal_rva':EXPECTED_STRING_RVA,'inventory':inventory,
            'selected_api_details':[detail(dec,sections,imports,row) for row in selected],
            'nearby_direct_callers':caller_surface(transfers,selected,dec.lo),**{k:False for k in FLAGS}}

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
