"""Original-only R10 conditional register/flags definition provenance.

No unknown CALL preserves ESI/EFLAGS. Candidate syntax ignoring CALL clobbers
is reported separately and never becomes an effective-address proof.
"""
import argparse,json,tempfile
from collections import deque
from pathlib import Path
from capstone import CS_GRP_CALL,CS_GRP_JUMP,CS_GRP_RET
from capstone.x86 import X86_OP_REG,X86_OP_MEM,X86_OP_IMM,X86_REG_ESI,X86_REG_EFLAGS,X86_REG_INVALID
from tools.stoneage_tw10_savedata_helper_frontier_r9 import inspect_verified as inspect_r9,ROOT,STORE,region_for_va,RUNTIME_SHA256,SAVEDATA_SHA256
from tools.stoneage_tw10_savedata_helper_effects_r8 import summarize
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder,direct_target
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH,SAVEDATA_PATH
from tools.stoneage_tw10_technical_probe import find_rows,extract_row
DELEGATE=0x491a1
BRANCHES=(0x4b8c4,0x4b8ca,0x4b8d2)
SCHEMA='tw10-r10-original-esi-predicate-provenance'
STATUS='PINNED_ORIGINAL_CONDITIONAL_DEFINITIONS_NOT_RUNTIME_OWNERSHIP'
MAX_NODES=256

def graph(dec,root):
    q=deque([root]);nodes={};edges=set()
    while q and len(nodes)<MAX_NODES:
        rva=q.popleft()
        if rva in nodes:continue
        if not root<=rva<root+1024:raise ValueError('out-of-scope parent path')
        ins=dec.at(rva)
        if ins is None:raise ValueError('parent decode gap')
        nodes[rva]=ins
        if ins.group(CS_GRP_RET) or ins.mnemonic in ('int','int3','into','ud2','hlt','iret','iretd'):continue
        if ins.group(CS_GRP_JUMP):
            target=direct_target(ins,dec.base)
            if target is None:raise ValueError('parent indirect jump')
            succ=[target]
            if ins.mnemonic not in ('jmp','ljmp'):succ.append(rva+ins.size)
        else:succ=[rva+ins.size] # CALL continuation is structural RETURN assumption.
        for dst in set(succ):edges.add((rva,dst));q.append(dst)
    if any(v not in nodes for v in q):raise ValueError('parent graph cap')
    return nodes,edges

def reaches(nodes,edges,root,register,havoc_calls=True):
    if register not in (X86_REG_ESI,X86_REG_EFLAGS):raise ValueError('provenance register scope')
    incoming={root:{('entry',root)}};succ={}
    for a,b in edges:succ.setdefault(a,[]).append(b)
    q=deque([root]);pending={root}
    while q:
        rva=q.popleft();pending.discard(rva);ins=nodes[rva]
        writes=ins.regs_access()[1]
        if register==X86_REG_ESI:
            defines=any(ins.reg_name(r) in ('esi','si') for r in writes)
        else:defines=X86_REG_EFLAGS in writes
        if ins.group(CS_GRP_CALL) and havoc_calls:out={('unknown_call',rva)}
        elif defines:out={('definition',rva)}
        else:out=incoming[rva]
        for dst in succ.get(rva,()):
            before=incoming.setdefault(dst,set());size=len(before);before.update(out)
            if len(before)>size and dst not in pending:q.append(dst);pending.add(dst)
    return incoming

def memory_geometry(ins,op,sections,base):
    m=op.mem;mapped=region_for_va(sections,base,int(m.disp))
    return {'width_bytes':op.size,'base_register':ins.reg_name(m.base) if m.base else None,
            'index_register':ins.reg_name(m.index) if m.index else None,'index_scale':int(m.scale),
            'segment_register':ins.reg_name(m.segment) if m.segment else None,
            'relative_field_offset':int(m.disp) if (m.base or m.index) and -4096<=int(m.disp)<=4096 else None,
            'displacement_region':mapped}

def semantic_definition(ins,register,sections,base):
    result={'kind':'unmodeled_write','register_inputs':[],'memory_input':None,'constant':None,'width_bits':None}
    ops=ins.operands;name=ins.mnemonic
    if register==X86_REG_EFLAGS:
        if name=='test' and len(ops)==2 and all(o.type==X86_OP_REG for o in ops) and ops[0].reg==ops[1].reg:
            result.update(kind='register_zero_test',register_inputs=[ins.reg_name(ops[0].reg)],constant=0,width_bits=ops[0].size*8)
        elif name in ('cmp','test') and len(ops)==2:
            regs=[ins.reg_name(o.reg) for o in ops if o.type==X86_OP_REG]
            mem=next((o for o in ops if o.type==X86_OP_MEM),None)
            imm=next((o for o in ops if o.type==X86_OP_IMM),None)
            result.update(kind='comparison' if name=='cmp' else 'masked_test',register_inputs=regs,
                          memory_input=memory_geometry(ins,mem,sections,base) if mem else None,
                          constant=int(imm.imm) if imm else None,width_bits=ops[0].size*8)
    elif ops and ops[0].type==X86_OP_REG and ops[0].reg==register and ops[0].size==4:
        if name in ('mov','lea') and len(ops)==2:
            src=ops[1]
            result['width_bits']=32
            if src.type==X86_OP_REG:result.update(kind='register_copy',register_inputs=[ins.reg_name(src.reg)])
            elif src.type==X86_OP_MEM:result.update(kind='address_calculation' if name=='lea' else 'memory_load',memory_input=memory_geometry(ins,src,sections,base))
            elif src.type==X86_OP_IMM:result.update(kind='constant_assignment',constant=int(src.imm))
        elif name in ('add','sub') and len(ops)==2 and ops[1].type==X86_OP_IMM:
            result.update(kind='register_offset_adjustment',register_inputs=[ins.reg_name(register)],constant=int(ops[1].imm)*(1 if name=='add' else -1),width_bits=32)
        elif name=='pop':result.update(kind='stack_pop',width_bits=32)
    return result

def describe_sources(tokens,nodes,register,sections,base):
    return [{'origin':kind,'rva':rva,
             'semantic':semantic_definition(nodes[rva],register,sections,base) if kind=='definition' else None}
            for kind,rva in sorted(tokens,key=lambda x:(x[1],x[0]))]

def provenance(dec,nodes,edges,sections):
    if STORE not in nodes or any(r not in nodes for r in BRANCHES):raise ValueError('frontier site absent')
    esi=reaches(nodes,edges,ROOT,X86_REG_ESI)
    syntax=reaches(nodes,edges,ROOT,X86_REG_ESI,False)
    flags=reaches(nodes,edges,ROOT,X86_REG_EFLAGS)
    predicates=[]
    for rva in BRANCHES:
        tokens=flags[rva]
        predicates.append({'branch_rva':rva,'condition':nodes[rva].mnemonic,
                           'flag_sources':describe_sources(tokens,nodes,X86_REG_EFLAGS,sections,dec.base),
                           'unique_conditional_flag_definition':len(tokens)==1 and next(iter(tokens))[0]=='definition',
                           'runtime_branch_outcome_proven':False})
    return {'esi_at_store':{'store_rva':STORE,
                'conservative_sources':describe_sources(esi[STORE],nodes,X86_REG_ESI,sections,dec.base),
                'syntax_candidates_ignoring_call_clobbers':describe_sources(syntax[STORE],nodes,X86_REG_ESI,sections,dec.base),
                'effective_target_proven':False},
            'loop_predicates':predicates,'structural_call_return_assumptions':sum(i.group(CS_GRP_CALL) for i in nodes.values())}

def inspect_verified(runtime,savedata):
    r9=inspect_r9(runtime,savedata)
    if not any(g['rva']==0x49199 and g['direct_target_rva']==DELEGATE for g in r9['nested_helper']['gap_sites']):raise ValueError('accepted R9 delegate changed')
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'sa_3.exe';p.write_bytes(runtime);data,pe,base,sections,_=image_layout(p)
    for s,raw_sec in zip(sections,pe.sections):s['characteristics']=int(raw_sec.Characteristics)
    t=next(s for s in sections if s['name']=='.text');raw=data[t['raw']:t['raw']+t['raw_size']]
    dec=Decoder(raw,t['rva'],base);nodes,edges=graph(dec,ROOT)
    if len(nodes)!=50 or len(edges)!=55:raise ValueError('accepted R9 parent graph changed')
    return {'schema':SCHEMA,'status':STATUS,'runtime_sha256':RUNTIME_SHA256,'savedata_sha256':SAVEDATA_SHA256,
            'parent_nodes':50,'parent_edges':55,'provenance':provenance(dec,nodes,edges,sections),
            'delegate_helper':summarize(dec,DELEGATE),'delegate_effects_admitted':False,
            'loop_runtime_bound_proven':False,'caller_resumption_admitted':False,
            'filename_api_link_proven':False,'handle_buffer_size_link_proven':False,
            'native_io_executed':False,'fixed_128_byte_schema_proven':False,'original_bytes_published':False}

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
