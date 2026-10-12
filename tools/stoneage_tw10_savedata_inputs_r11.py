"""Bounded conditional parent-input definitions; no object or runtime promotion."""
import argparse,json,tempfile
from collections import deque
from pathlib import Path
from capstone import CS_GRP_CALL
from capstone.x86 import X86_OP_REG
from tools.stoneage_tw10_savedata_provenance_r10 import inspect_verified as inspect_r10,graph,semantic_definition as semantic_r10,ROOT,RUNTIME_SHA256,SAVEDATA_SHA256
from tools.stoneage_tw10_savedata_helper_effects_r8 import summarize
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH,SAVEDATA_PATH
from tools.stoneage_tw10_technical_probe import find_rows,extract_row
SCHEMA='tw10-r11-original-parent-input-definitions'
STATUS='PINNED_ORIGINAL_CONDITIONAL_INPUTS_NOT_EFFECTIVE_OBJECT_OR_RUNTIME'
DELEGATE=0x491cd
ALIASES={'eax':{'eax','ax','al','ah'},'ebx':{'ebx','bx','bl','bh'},'ecx':{'ecx','cx','cl','ch'},'edx':{'edx','dx','dl','dh'},'esi':{'esi','si'},'edi':{'edi','di'},'ebp':{'ebp','bp'}}
QUERIES=((0x4b8d6,'ebx'),(0x4b8d6,'eax'),(0x4b8fd,'edi'),(0x4b8c2,'ecx'),(0x4b8c2,'ebp'),(0x4b8c6,'ecx'),(0x4b8d0,'eax'),(0x4b8d0,'edx'))
FLAGS={'delegate_effects_admitted','parent_inputs_fully_known','effective_object_proven','loop_runtime_bound_proven','caller_resumption_admitted','filename_api_link_proven','handle_buffer_size_link_proven','native_io_executed','fixed_128_byte_schema_proven','original_bytes_published'}

def reaches(nodes,edges,root,register):
    if register not in ALIASES:raise ValueError('register scope')
    incoming={root:{('entry',root)}};succ={}
    for a,b in edges:succ.setdefault(a,[]).append(b)
    q=deque([root]);pending={root}
    while q:
        rva=q.popleft();pending.discard(rva);ins=nodes[rva]
        defines=any(ins.reg_name(r) in ALIASES[register] for r in ins.regs_access()[1])
        if ins.group(CS_GRP_CALL):out={('unknown_call',rva)}
        elif defines:out={('definition',rva)}
        else:out=incoming[rva]
        for dst in succ.get(rva,()):
            before=incoming.setdefault(dst,set());size=len(before);before.update(out)
            if len(before)>size and dst not in pending:q.append(dst);pending.add(dst)
    return incoming

def semantic(ins,register,sections,base):
    regid=next((r for r in ins.regs_access()[1] if ins.reg_name(r)==register),None)
    if regid is None:return {'kind':'unmodeled_write','register_inputs':[],'memory_input':None,'constant':None,'width_bits':None}
    result=semantic_r10(ins,regid,sections,base)
    ops=ins.operands
    if ops and ops[0].type==X86_OP_REG and ops[0].reg==regid and ops[0].size==4:
        if ins.mnemonic in ('inc','dec'):
            result.update(kind='register_offset_adjustment',register_inputs=[register],constant=1 if ins.mnemonic=='inc' else -1,width_bits=32)
        elif ins.mnemonic in ('xor','sub') and len(ops)==2 and ops[1].type==X86_OP_REG and ops[1].reg==regid:
            result.update(kind='constant_assignment',register_inputs=[],constant=0,width_bits=32)
    return result

def input_queries(dec,nodes,edges,sections,queries=QUERIES,root=ROOT):
    maps={reg:reaches(nodes,edges,root,reg) for reg in {reg for _,reg in queries}}
    rows=[]
    for site,reg in queries:
        if site not in nodes:raise ValueError('query site absent')
        sources=[]
        for origin,rva in sorted(maps[reg][site],key=lambda x:(x[1],x[0])):
            sources.append({'origin':origin,'rva':rva,'semantic':semantic(nodes[rva],reg,sections,dec.base) if origin=='definition' else None})
        rows.append({'site_rva':site,'register':reg,'reaching_sources':sources,'value_fully_known':False})
    return rows

def inspect_verified(runtime,savedata):
    r10=inspect_r10(runtime,savedata)
    if not any(g['rva']==0x491ac and g['direct_target_rva']==DELEGATE for g in r10['delegate_helper']['gap_sites']):raise ValueError('R10 delegate changed')
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'sa_3.exe';p.write_bytes(runtime);data,pe,base,sections,_=image_layout(p)
    for s,raw_sec in zip(sections,pe.sections):s['characteristics']=int(raw_sec.Characteristics)
    t=next(s for s in sections if s['name']=='.text');dec=Decoder(data[t['raw']:t['raw']+t['raw_size']],t['rva'],base)
    nodes,edges=graph(dec,ROOT)
    if len(nodes)!=50 or len(edges)!=55:raise ValueError('parent graph identity')
    return {'schema':SCHEMA,'status':STATUS,'runtime_sha256':RUNTIME_SHA256,'savedata_sha256':SAVEDATA_SHA256,
            'parent_nodes':50,'parent_edges':55,'structural_call_return_assumptions':sum(i.group(CS_GRP_CALL) for i in nodes.values()),
            'input_queries':input_queries(dec,nodes,edges,sections),'delegate_helper':summarize(dec,DELEGATE),**{k:False for k in FLAGS}}

def main():
    p=argparse.ArgumentParser();p.add_argument('--bin',type=Path,required=True);args=p.parse_args()
    img,rows,_,_=find_rows(args.bin)
    try:
        paths={r['path']:r for r in rows if not r['is_dir']}
        with tempfile.TemporaryDirectory() as td:
            exe=Path(td)/'sa_3.exe';save=Path(td)/'savedata.dat'
            extract_row(img,paths[RUNTIME_PATH],exe);extract_row(img,paths[SAVEDATA_PATH],save)
            report=inspect_verified(exe.read_bytes(),save.read_bytes())
    finally:img.close()
    print(json.dumps(report,sort_keys=True))
if __name__=='__main__':main()
