"""CALL-supported bounded file API input candidates; no execution/ABI/owner claims."""
import argparse,hashlib,json,tempfile
from collections import deque
from pathlib import Path
from capstone import CS_GRP_CALL,CS_GRP_JUMP,CS_GRP_RET
from tools.stoneage_tw10_savedata_native_io_r27 import inspect_verified as inspect_r27,RUNTIME_SHA256,SAVEDATA_SHA256
from tools.stoneage_tw10_savedata_native_io_r27_guard import validate as validate_r27
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder,direct_target
from tools.stoneage_tw10_savedata_inputs_r11 import reaches,semantic,ALIASES
from tools.stoneage_tw10_savedata_frontier_r12 import call_identity
from tools.stoneage_tw10_savedata_write_shapes_r17 import operand_shape
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH,SAVEDATA_PATH
from tools.stoneage_tw10_technical_probe import find_rows,extract_row
SCHEMA='tw10-r28-original-call-supported-native-api-input-candidates'
STATUS='PINNED_ORIGINAL_CONDITIONAL_GRAPH_INPUTS_NATIVE_LINKAGE_OPEN'
PRIOR_SHA256='1c77b3c327a216729c1a66693d8dcb3be1c82205676365198fc5028239a12548'
CONTEXTS=(('CreateFileA',0x4b873,0x4eb55,(0x4ed01,)),
          ('ReadFile',0x486f0,0x4a8dc,(0x4a960,0x4aa31)),
          ('WriteFile',0x48c5e,0x4c5b4,(0x4c68c,0x4c6f1)))
MAX_SPAN=768;MAX_NODES=256;MAX_QUERIES=64;MAX_DEPTH=2
FLAGS=('actual_function_entries_proven','actual_paths_frames_or_argument_values_proven',
       'original_filename_api_link_proven','create_return_handle_link_proven','read_write_handle_buffer128_link_proven',
       'windows_abi_roles_applied','file_crt_heap_alias_ownership_proven','caller_return_effects_admitted',
       'native_save_schema_proven','native_io_executed','original_bytes_published')

def candidate_graph(dec,root,span=MAX_SPAN,cap=MAX_NODES):
    if not 1<=span<=MAX_SPAN or not 1<=cap<=MAX_NODES:raise ValueError('R28 graph bounds')
    q=deque([root]);nodes={};edges=set();frontier=set()
    while q and len(nodes)<cap:
        at=q.popleft()
        if at in nodes:continue
        if not root<=at<root+span:frontier.add(('out_of_window',at));continue
        ins=dec.at(at)
        if ins is None:frontier.add(('decode_gap',at));continue
        if at+ins.size>root+span:frontier.add(('instruction_span_limit',at));continue
        nodes[at]=ins
        if ins.group(CS_GRP_RET) or ins.mnemonic in ('int','int3','into','ud2','hlt','iret','iretd','sysenter','sysexit','syscall','sysret'):continue
        if ins.group(CS_GRP_JUMP):
            dst=direct_target(ins,dec.base)
            if dst is None:frontier.add(('indirect_jump',at));continue
            succ=[dst]+([] if ins.mnemonic in ('jmp','ljmp') else [at+ins.size])
        else:succ=[at+ins.size] # CALL continuation is an explicit structural-return assumption.
        for dst in sorted(set(succ)):
            edges.add((at,dst))
            if dst not in nodes:q.append(dst)
    hit=any(root<=at<root+span and at not in nodes for at in q)
    if hit:frontier.add(('node_cap',cap))
    return nodes,{(a,b) for a,b in edges if a in nodes and b in nodes},sorted(frontier),hit

def dependencies(sem):
    if not sem:return []
    regs=set(sem.get('register_inputs',[]));g=sem.get('memory_input') or {}
    regs.update(g.get(k) for k in ('base_register','index_register'))
    return sorted(r for r in regs if r in ALIASES)

def input_surface(dec,sections,nodes,edges,root,queries):
    todo=deque((at,reg,0) for at,reg in sorted(set(queries)));seen={};maps={}
    while todo and len(seen)<MAX_QUERIES:
        at,reg,depth=todo.popleft()
        if (at,reg) in seen:continue
        if reg not in ALIASES:raise ValueError('R28 register scope')
        if reg not in maps:maps[reg]=reaches(nodes,edges,root,reg)
        tokens=sorted(maps[reg].get(at,()),key=lambda x:(x[1],x[0])) if at in nodes else []
        sources=[{'origin':kind,'rva':site,'semantic':semantic(nodes[site],reg,sections,dec.base) if kind=='definition' else None} for kind,site in tokens[:24]]
        deps=[]
        if depth<MAX_DEPTH:
            for token in sources:
                for r in dependencies(token['semantic']):
                    deps.append({'site_rva':token['rva'],'register':r})
                    todo.append((token['rva'],r,depth+1))
        deps=sorted({(r['site_rva'],r['register']) for r in deps})
        seen[(at,reg)]={'site_rva':at,'register':reg,'dependency_depth':depth,'site_in_candidate_graph':at in nodes,
                        'reaching_candidates':sources,'candidates_truncated':len(tokens)>24,
                        'dependency_queries':[{'site_rva':a,'register':r} for a,r in deps],
                        'actual_register_value_known':False}
    pending=sorted({(at,reg) for at,reg,_ in todo if (at,reg) not in seen})
    return {'queries':[seen[k] for k in sorted(seen)],'query_limit_hit':bool(pending),
            'pending_query_count':len(pending),'dependency_depth_limit':MAX_DEPTH,
            'dependency_closure_or_memory_values_proven':False}

def context(dec,sections,imports,prior,name,caller,root,sites):
    identity=call_identity(dec,caller,imports,sections)
    if identity['kind']!='direct' or identity['direct_target_rva']!=root:raise ValueError('R28 caller syntax')
    if not any(r['site_rva']==caller and r['target_rva']==root for r in prior['nearby_direct_callers']['samples']):raise ValueError('R28 caller absent from original R27')
    nodes,edges,frontier,hit=candidate_graph(dec,root);apis=[];queries=set()
    for site in sites:
        old=next(r for r in prior['selected_api_details'] if r['site_rva']==site and r['api']==name)
        pushes=old['suffix']['pushes'];links=[]
        for p in pushes:
            shape=p['input'];regs=([shape['register']] if shape['kind']=='register' else
                  [r for r in (shape.get('geometry',{}).get('base_register'),shape.get('geometry',{}).get('index_register')) if r in ALIASES])
            refs=[{'site_rva':p['site_rva'],'register':r} for r in sorted(set(regs))]
            queries.update((r['site_rva'],r['register']) for r in refs)
            links.append({**p,'source_queries':refs,'actual_argument_value_or_role_proven':False})
        queries.update((site,r) for r in ('eax','ebx','esi','ebp','ecx','edi'))
        # Conditional continuation EAX is deliberately killed by opaque API CALL.
        post=site+dec.at(site).size;queries.add((post,'eax'))
        apis.append({'site_rva':site,'identity':call_identity(dec,site,imports,sections),
                     'site_in_candidate_graph':site in nodes,'prior_linear_anchor_rva':old['linear_anchor_rva'],
                     'prior_graph_site_reached':old['registers_before_call']['eax']['query_site_in_candidate_graph'],
                     'push_candidates':links,'conditional_post_call_rva':post,'actual_external_return_proven':False})
    return {'api':name,'caller_rva':caller,'root_candidate_rva':root,'caller_identity':identity,
            'supported_by_exact_r27_direct_call':True,'entry_or_call_execution_proven':False,
            'graph':{'span_bytes':MAX_SPAN,'node_cap':MAX_NODES,'nodes':len(nodes),'edges':len(edges),
                     'frontier':[{'reason':why,'rva':at} for why,at in frontier],'node_limit_hit':hit,
                     'call_fallthrough_structural_only':True,'all_incoming_paths_proven':False},
            'api_sites':apis,'inputs':input_surface(dec,sections,nodes,edges,root,queries)}

def inspect_verified(runtime,savedata):
    prior=inspect_r27(runtime,savedata);validate_r27(prior)
    digest=hashlib.sha256((json.dumps(prior,sort_keys=True)+'\n').encode()).hexdigest()
    if digest!=PRIOR_SHA256:raise ValueError('R27 exact original derivative changed')
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'sa_3.exe';p.write_bytes(runtime);data,pe,base,sections,imports=image_layout(p)
    for sec,raw in zip(sections,pe.sections):sec['characteristics']=int(raw.Characteristics)
    t=next(s for s in sections if s['name']=='.text');dec=Decoder(data[t['raw']:t['raw']+t['raw_size']],t['rva'],base)
    return {'schema':SCHEMA,'status':STATUS,'runtime_sha256':RUNTIME_SHA256,'savedata_sha256':SAVEDATA_SHA256,
            'r27_exact_original_revalidated':True,'r27_exact_report_sha256':digest,'static_only':True,
            'contexts':[context(dec,sections,imports,prior,*row) for row in CONTEXTS],
            'third_writefile_and_early_createfile_detail_deferred':True,**{k:False for k in FLAGS}}

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
