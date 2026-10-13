"""CreateFileA opaque-value capture and bounded helper stores, static only."""
import argparse,hashlib,json,tempfile
from pathlib import Path
from capstone.x86 import X86_OP_REG,X86_OP_MEM
from tools.stoneage_tw10_savedata_native_io_r30 import inspect_verified as inspect_r30,graph_meta,RUNTIME_SHA256,SAVEDATA_SHA256
from tools.stoneage_tw10_savedata_native_io_r30_guard import validate as validate_r30
from tools.stoneage_tw10_savedata_native_io_r28 import candidate_graph,input_surface,ALIASES
from tools.stoneage_tw10_savedata_write_shapes_r17 import operand_shape
from tools.stoneage_tw10_savedata_upstream_r23 import local_push_suffix
from tools.stoneage_tw10_savedata_frontier_r12 import call_identity
from tools.stoneage_tw10_savedata_mutations_r13 import write_candidate,WRITE_MNEMONICS
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH,SAVEDATA_PATH
from tools.stoneage_tw10_technical_probe import find_rows,extract_row
SCHEMA='tw10-r31-original-createfile-opaque-capture-helper-stores'
STATUS='PINNED_ORIGINAL_CONDITIONAL_CAPTURE_STORES_HANDLE_BINDING_OPEN'
PRIOR_SHA256='760730dc57c823a7279b22a0944ffaac588e77d4fb6b0d5f5024265345f0b45a'
PARENT=0x4eb55;PARENT_CALLER=0x4b873;API=0x4ed01;POST=0x4ed07;CALL=0x4ed26;HELPER=0x4c953
MAX_COPIES=8;MAX_STORES=12;MAX_STACK_REFS=16
FLAGS=('actual_api_return_handle_or_success_proven','actual_functions_frames_paths_proven',
       'caller_push_to_callee_parameter_binding_proven','actual_helper_store_value_address_or_owner_proven',
       'file_crt_heap_alias_owner_or_lifetime_proven','callee_effects_or_caller_resumption_admitted',
       'native_filename_handle_read_write_buffer128_link_proven','native_save_schema_proven','native_io_executed','original_bytes_published')

def opaque_api_source(q):
    tokens=q.get('reaching_candidates',[])
    return (q.get('site_in_candidate_graph') is True and q.get('candidates_truncated') is False
            and len(tokens)==1 and tokens[0].get('origin')=='unknown_call' and tokens[0].get('rva')==API
            and tokens[0].get('semantic') is None)

def caller_surface(dec,sections,imports):
    parent=call_identity(dec,PARENT_CALLER,imports,sections)
    if parent['kind']!='direct' or parent['direct_target_rva']!=PARENT:raise ValueError('R31 parent caller syntax')
    ident=call_identity(dec,CALL,imports,sections);api=call_identity(dec,API,imports,sections)
    if ident['kind']!='direct' or ident['direct_target_rva']!=HELPER:raise ValueError('R31 helper call syntax')
    if api['import_identity']!={'dll':'KERNEL32.dll','name':'CreateFileA','iat_rva':0x520a0}:raise ValueError('R31 original CreateFileA identity')
    nodes,edges,front,hit=candidate_graph(dec,PARENT)
    if not {API,POST,CALL}<=set(nodes):raise ValueError('R31 supported graph misses API/continuation/CALL')
    suffix=local_push_suffix(dec,sections,POST,CALL);queries={(POST,'eax')}|{(CALL,r) for r in ('eax','ebx','esi','edi','ecx')};copies=[]
    for at,ins in sorted(nodes.items()):
        if not POST<=at<CALL or ins.mnemonic!='mov' or len(ins.operands)!=2:continue
        a,b=ins.operands
        if a.type!=X86_OP_REG or b.type!=X86_OP_REG or a.size!=4 or b.size!=4:continue
        dst,src=ins.reg_name(a.reg),ins.reg_name(b.reg)
        if dst not in ALIASES or src not in ALIASES:continue
        if len(copies)<MAX_COPIES:
            copies.append({'site_rva':at,'destination':operand_shape(ins,a,sections,dec.base),'source':operand_shape(ins,b,sections,dec.base)})
            queries.add((at,src))
    copy_count=sum(POST<=at<CALL and ins.mnemonic=='mov' and len(ins.operands)==2 and all(o.type==X86_OP_REG and o.size==4 and ins.reg_name(o.reg) in ALIASES for o in ins.operands) for at,ins in nodes.items())
    pushes=[]
    for p in suffix['pushes']:
        op=p['input'];regs=([op['register']] if op['kind']=='register' and op['register'] in ALIASES else [r for r in (op.get('geometry',{}).get('base_register'),op.get('geometry',{}).get('index_register')) if r in ALIASES])
        refs=[{'site_rva':p['site_rva'],'register':r} for r in sorted(set(regs))]
        queries.update((q['site_rva'],q['register']) for q in refs)
        pushes.append({**p,'source_queries':refs,'actual_value_or_api_parameter_role_proven':False})
    inputs=input_surface(dec,sections,nodes,edges,PARENT,queries)
    for c in copies:
        q=next(q for q in inputs['queries'] if (q['site_rva'],q['register'])==(c['site_rva'],c['source']['register']))
        c.update(opaque_api_token_input_candidate=opaque_api_source(q),actual_api_return_or_handle_value_proven=False)
    return {'root_candidate_rva':PARENT,'supporting_parent_call':parent,'graph':graph_meta(nodes,edges,front,hit),
            'api_identity':api,'conditional_post_api_rva':POST,'helper_call_identity':ident,'local_push_suffix':suffix,
            'push_candidates':pushes,'copy_count':copy_count,'register_copy_candidates':copies,'copies_truncated':copy_count>MAX_COPIES,
            'inputs':inputs,'callee_entry_or_stack_binding_proven':False}

def helper_surface(dec,sections):
    nodes,edges,front,hit=candidate_graph(dec,HELPER);stores=[];stack=[];count=0;stack_count=0;queries=set()
    for at,ins in sorted(nodes.items()):
        if ins.mnemonic in WRITE_MNEMONICS and ins.operands and ins.operands[0].type==X86_OP_MEM and ins.operands[0].access&2 and not ins.operands[0].mem.segment:
            count+=1
            if len(stores)<MAX_STORES:
                w=write_candidate(dec,at,sections);regs=set(w['address_inputs']+w['value_input_registers'])&set(ALIASES)
                refs=[{'site_rva':at,'register':r} for r in sorted(regs)];queries.update((q['site_rva'],q['register']) for q in refs)
                stores.append({'write':w,'source_and_address_queries':refs,'caller_value_or_api_handle_binding_proven':False})
        for n,op in enumerate(ins.operands):
            if op.type!=X86_OP_MEM or ins.reg_name(op.mem.base) not in ('esp','ebp') or op.mem.segment:continue
            stack_count+=1
            if len(stack)<MAX_STACK_REFS:
                stack.append({'site_rva':at,'operand_index':n,'operand':operand_shape(ins,op,sections,dec.base),
                              'actual_frame_owner_or_parameter_binding_proven':False})
    return {'root_candidate_rva':HELPER,'graph':graph_meta(nodes,edges,front,hit),'store_count':count,'store_candidates':stores,
            'stores_truncated':count>MAX_STORES,'stack_reference_count':stack_count,'stack_reference_candidates':stack,
            'stack_references_truncated':stack_count>MAX_STACK_REFS,'inputs':input_surface(dec,sections,nodes,edges,HELPER,queries),
            'all_alias_writes_or_actual_call_effect_proven':False}

def inspect_verified(runtime,savedata):
    prior=inspect_r30(runtime,savedata);validate_r30(prior)
    digest=hashlib.sha256((json.dumps(prior,sort_keys=True)+'\n').encode()).hexdigest()
    if digest!=PRIOR_SHA256:raise ValueError('R30 exact original derivative changed')
    if not any(r['site_rva']==CALL and r['target_rva']==HELPER for r in prior['writer_discovery']['caller_samples']):raise ValueError('R30 original helper CALL missing')
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'sa_3.exe';p.write_bytes(runtime);data,pe,base,sections,imports=image_layout(p)
    for sec,raw in zip(sections,pe.sections):sec['characteristics']=int(raw.Characteristics)
    t=next(s for s in sections if s['name']=='.text');dec=Decoder(data[t['raw']:t['raw']+t['raw_size']],t['rva'],base)
    return {'schema':SCHEMA,'status':STATUS,'runtime_sha256':RUNTIME_SHA256,'savedata_sha256':SAVEDATA_SHA256,
            'r30_exact_original_revalidated':True,'r30_exact_report_sha256':digest,'static_only':True,
            'caller_capture':caller_surface(dec,sections,imports),'helper_memory':helper_surface(dec,sections),**{k:False for k in FLAGS}}

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
