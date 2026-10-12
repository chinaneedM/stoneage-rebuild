"""Original static indirect-call identity and bounded reference candidates."""
import argparse,json,tempfile
from pathlib import Path
from capstone import CS_GRP_CALL
from capstone.x86 import X86_OP_REG,X86_OP_MEM,X86_OP_IMM
from tools.stoneage_tw10_savedata_inputs_r11 import inspect_verified as inspect_r11,input_queries,FLAGS as R11_FLAGS,ROOT,RUNTIME_SHA256,SAVEDATA_SHA256
from tools.stoneage_tw10_savedata_provenance_r10 import graph,memory_geometry
from tools.stoneage_tw10_savedata_helper_effects_r8 import summarize
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder,direct_target
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH,SAVEDATA_PATH
from tools.stoneage_tw10_technical_probe import find_rows,extract_row
SCHEMA='tw10-r12-original-indirect-and-global-reference-frontier'
STATUS='PINNED_ORIGINAL_STATIC_IMPORT_AND_REFERENCE_CANDIDATES_NOT_RUNTIME'
DELEGATE=0x49d93;CALL=0x491fb
QUERIES=((0x4b8f6,'edi'),(0x4b8f6,'eax'),(0x4b8c0,'edi'),(0x4b8cc,'eax'))
GLOBALS=(0x1721884,0x17228a0)
MAX_SAMPLES=32
FLAGS=R11_FLAGS|{'global_initialization_proven','indirect_call_effects_admitted'}

def call_identity(dec,site,imports,sections):
    ins=dec.at(site)
    if ins is None or not ins.group(CS_GRP_CALL) or ins.mnemonic!='call' or len(ins.operands)!=1:raise ValueError('near CALL site')
    op=ins.operands[0]
    row={'call_rva':site,'kind':'other','register_target':None,'memory_target':None,'direct_target_rva':None,'import_identity':None,'import_slot_association_proven':False,'runtime_target_or_effects_proven':False}
    if op.type==X86_OP_IMM:row.update(kind='direct',direct_target_rva=direct_target(ins,dec.base))
    elif op.type==X86_OP_REG:row.update(kind='register_indirect',register_target=ins.reg_name(op.reg))
    elif op.type==X86_OP_MEM:
        row.update(kind='memory_indirect',memory_target=memory_geometry(ins,op,sections,dec.base))
        m=op.mem
        # Exact absolute unsegmented four-byte near CALL through original IAT slot.
        if not m.base and not m.index and not m.segment and op.size==4:
            match=imports.get(int(m.disp)&0xffffffff)
            if match:
                row.update(import_identity={'dll':match[0],'name':match[1],'iat_rva':((int(m.disp)&0xffffffff)-dec.base)&0xffffffff},import_slot_association_proven=True)
    return row

def linear_references(dec,targets=GLOBALS):
    if len(set(targets))!=len(targets):raise ValueError('duplicate globals')
    rows={r:{'global_rva':r,'counts':{'read_candidate':0,'write_candidate':0,'address_candidate':0,'unknown_candidate':0},'samples':[],'samples_truncated':False,'runtime_initialization_proven':False} for r in targets}
    va_targets={dec.base+r:r for r in targets};pos=dec.lo;decoded=0;decode_gap_bytes=0
    while pos<dec.hi:
        ins=dec.at(pos)
        if ins is None:pos+=1;decode_gap_bytes+=1;continue
        decoded+=1
        hits=set()
        for op in ins.operands:
            kind=None;target=None
            if op.type==X86_OP_MEM and not op.mem.base and not op.mem.index and not op.mem.segment:
                target=va_targets.get(int(op.mem.disp)&0xffffffff)
                if target is not None:
                    # Access-bit bugs on unmodeled x87/stores cannot prove read-only.
                    if ins.mnemonic=='lea':kind='address_candidate'
                    elif ins.mnemonic in ('mov','movzx','movsx','cmp','test','push','add','sub','and','or','xor','inc','dec'):
                        kind='write_candidate' if op.access&2 else 'read_candidate' if op.access&1 else 'unknown_candidate'
                    else:kind='unknown_candidate'
            elif op.type==X86_OP_IMM:
                target=va_targets.get(int(op.imm)&0xffffffff)
                if target is not None:kind='address_candidate'
            if kind is not None:hits.add((target,kind))
        for target,kind in sorted(hits):
            row=rows[target];row['counts'][kind]+=1
            if len(row['samples'])<MAX_SAMPLES:row['samples'].append({'rva':pos,'kind':kind})
            else:row['samples_truncated']=True
        pos+=ins.size
    return {'scope':'linear_text_decode_candidates_not_reachable_execution','decoded_instructions':decoded,'decode_gap_bytes':decode_gap_bytes,'text_bytes':dec.hi-dec.lo,'globals':[rows[r] for r in targets],'all_indirect_references_covered':False}

def inspect_verified(runtime,savedata):
    r11=inspect_r11(runtime,savedata)
    gaps=r11['delegate_helper']['gap_sites']
    if not any(g['rva']==0x491db and g['direct_target_rva']==DELEGATE for g in gaps) or not any(g['rva']==CALL and g['direct_target_rva'] is None for g in gaps):raise ValueError('R11 frontier changed')
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'sa_3.exe';p.write_bytes(runtime);data,pe,base,sections,imports=image_layout(p)
    for s,raw_sec in zip(sections,pe.sections):s['characteristics']=int(raw_sec.Characteristics)
    t=next(s for s in sections if s['name']=='.text');dec=Decoder(data[t['raw']:t['raw']+t['raw_size']],t['rva'],base)
    nodes,edges=graph(dec,ROOT)
    if len(nodes)!=50 or len(edges)!=55:raise ValueError('parent graph identity')
    return {'schema':SCHEMA,'status':STATUS,'runtime_sha256':RUNTIME_SHA256,'savedata_sha256':SAVEDATA_SHA256,
            'parent_nodes':50,'parent_edges':55,'structural_call_return_assumptions':1,'input_queries':input_queries(dec,nodes,edges,sections,QUERIES),
            'call_identity':call_identity(dec,CALL,imports,sections),'global_references':linear_references(dec),'delegate_helper':summarize(dec,DELEGATE),**{k:False for k in FLAGS}}

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
