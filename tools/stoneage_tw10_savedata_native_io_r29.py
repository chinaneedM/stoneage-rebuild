"""Original file-IO scalar/address syntax; no actual values/handle/ABI promotion."""
import argparse,hashlib,json,tempfile
from pathlib import Path
from capstone.x86 import X86_OP_MEM,X86_OP_IMM
from tools.stoneage_tw10_savedata_native_io_r28 import inspect_verified as inspect_r28,candidate_graph,input_surface,ALIASES,RUNTIME_SHA256,SAVEDATA_SHA256
from tools.stoneage_tw10_savedata_native_io_r28_guard import validate as validate_r28
from tools.stoneage_tw10_savedata_write_shapes_r17 import operand_shape
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH,SAVEDATA_PATH
from tools.stoneage_tw10_technical_probe import find_rows,extract_row
SCHEMA='tw10-r29-original-native-io-conditional-scalar-address-shapes'
STATUS='PINNED_ORIGINAL_STATIC_SCALAR_ADDRESS_SYNTAX_HANDLE_OWNER_OPEN'
PRIOR_SHA256='296e5754a3eebafc6360cc45000ba73b6bcf1cc0a5d0ee439aa291eb45e0d645'
ROWS=(('ReadFile',0x4a8dc,((0x4a8f9,'eax'),(0x4a8fc,'esi')),0x4a8ff),
      ('WriteFile',0x4c5b4,((0x4c5d3,'eax'),(0x4c5e0,'esi'),(0x4c617,'eax')),0x4c5d9))
SHARED=0x1721760;MAX_REFS=32
CLASSES={'sar','shr','shl','sal','and','or','xor','add','sub','inc','dec','mov','lea'}
FLAGS=('actual_original_scalar_values_proven','actual_index_range_or_effective_address_proven',
       'shared_memory_contents_or_initialization_proven','same_runtime_table_handle_owner_proven',
       'actual_functions_frames_paths_proven','abi_roles_or_callee_effects_admitted',
       'native_filename_handle_buffer128_link_proven','native_save_schema_proven','native_io_executed','original_bytes_published')

def scalar_model(shape,register):
    ops=shape['operands'];kind=shape['class'];op=None;rhs=None
    if ops and ops[0].get('kind')=='register' and ops[0].get('register')==register and ops[0].get('width_bytes')==4 and ops[0].get('decoder_write') is True:
        if len(ops)==2:
            b=ops[1]
            if kind in ('sar','shr','shl','sal') and b.get('kind')=='immediate':
                op='shl' if kind=='sal' else kind;rhs={'kind':'shift_count','constant':b['constant']&31}
            elif kind in ('and','or','xor','add','sub'):
                if b.get('kind')=='immediate':op=kind;rhs={'kind':'constant','constant':b['constant']&0xffffffff}
                elif b.get('kind')=='register' and b.get('width_bytes')==4 and b.get('register') in ALIASES:
                    op=kind;rhs={'kind':'register','register':b['register']}
        elif len(ops)==1 and kind in ('inc','dec'):
            op='add' if kind=='inc' else 'sub';rhs={'kind':'constant','constant':1}
    return {'kind':'conditional_u32_scalar' if op else 'unqualified_scalar','operation':op,'lhs_register':register if op else None,
            'rhs':rhs,'width_bits':32 if op else None,'modulus':4294967296 if op else None,
            'sar_uses_signed_reinterpretation':op=='sar','flags_or_branch_effects_modeled':False,
            'original_input_values_known':False,'evaluated_original_result':None,'index_or_api_role_proven':False}

def eval_synthetic(model,values):
    """Invented numbers only; original inspection never invokes this evaluator."""
    if model['kind']!='conditional_u32_scalar':raise ValueError('unqualified scalar')
    x=values[model['lhs_register']]&0xffffffff;b=model['rhs'];y=(values[b['register']]&0xffffffff) if b['kind']=='register' else b['constant']
    op=model['operation']
    if op=='sar':out=(x if x<0x80000000 else x-4294967296)>>y
    elif op=='shr':out=x>>y
    elif op=='shl':out=x<<y
    elif op=='and':out=x&y
    elif op=='or':out=x|y
    elif op=='xor':out=x^y
    elif op=='add':out=x+y
    elif op=='sub':out=x-y
    else:raise ValueError('operation scope')
    return out&0xffffffff

def shape_at(dec,sections,nodes,at):
    ins=dec.at(at)
    if ins is None or at not in nodes:raise ValueError('R29 shape outside supported graph')
    return {'site_rva':at,'class':ins.mnemonic if ins.mnemonic in CLASSES else 'unmodeled',
            'operands':[operand_shape(ins,o,sections,dec.base) for o in ins.operands]}

def scalar_context(dec,sections,prior,api,root,sites,address):
    old=next(c for c in prior['contexts'] if c['api']==api and c['root_candidate_rva']==root)
    definitions={s['rva'] for q in old['inputs']['queries'] for s in q['reaching_candidates'] if s['origin']=='definition'}
    if not {at for at,_ in sites}<=definitions:raise ValueError('R29 definitions absent from exact R28')
    nodes,edges,front,hit=candidate_graph(dec,root);queries=set();rows=[]
    for at,reg in sites:
        shape=shape_at(dec,sections,nodes,at);ins=nodes[at]
        regs={ins.reg_name(r) for r in ins.regs_access()[0]}&set(ALIASES)
        regs.add(reg);queries.update((at,r) for r in regs)
        rows.append({'site_rva':at,'written_register_candidate':reg,'supported_by_r28_definition':True,
                     'shape':shape,'conditional_model':scalar_model(shape,reg),
                     'input_queries':[{'site_rva':at,'register':r} for r in sorted(regs)],'actual_value_or_effect_proven':False})
    lea=shape_at(dec,sections,nodes,address);queries.add((address,'eax'))
    return {'api':api,'root_candidate_rva':root,'supported_by_r28_call_root':True,
            'graph':{'nodes':len(nodes),'edges':len(edges),'span_bytes':768,'node_cap':256,
                     'frontier':[{'reason':why,'rva':at} for why,at in front],'node_limit_hit':hit,
                     'actual_entry_path_proven':False,'returning_call_assumption_only':True},
            'scalar_definitions':rows,'shared_address_shape':lea,'inputs':input_surface(dec,sections,nodes,edges,root,queries),
            'effective_address_or_table_owner_proven':False}

def shared_references(dec,sections):
    pos=dec.lo;count=0;decoded=0;gaps=0;samples=[]
    while pos<dec.hi:
        ins=dec.at(pos)
        if ins is None:gaps+=1;pos+=1;continue
        decoded+=1
        for n,op in enumerate(ins.operands):
            matched=(op.type==X86_OP_MEM and not op.mem.segment and (int(op.mem.disp)&0xffffffff)==dec.base+SHARED)
            matched=matched or (op.type==X86_OP_IMM and (int(op.imm)&0xffffffff)==dec.base+SHARED)
            if not matched:continue
            count+=1
            if len(samples)<MAX_REFS:
                samples.append({'site_rva':pos,'operand_index':n,'class':ins.mnemonic if ins.mnemonic in CLASSES else 'unmodeled',
                                'operand':operand_shape(ins,op,sections,dec.base),'actual_read_write_initialization_proven':False})
        pos+=ins.size
    return {'scope':'full_raw_text_exact_displacement_or_immediate_candidates','shared_displacement_rva':SHARED,
            'decoded_instructions':decoded,'decode_gap_bytes':gaps,'text_start_rva':dec.lo,'text_bytes':dec.hi-dec.lo,
            'count':count,'samples':samples,'samples_truncated':count>MAX_REFS,
            'indirect_alias_complete_or_actual_table_contents_proven':False}

def inspect_verified(runtime,savedata):
    prior=inspect_r28(runtime,savedata);validate_r28(prior)
    digest=hashlib.sha256((json.dumps(prior,sort_keys=True)+'\n').encode()).hexdigest()
    if digest!=PRIOR_SHA256:raise ValueError('R28 exact original derivative changed')
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'sa_3.exe';p.write_bytes(runtime);data,pe,base,sections,imports=image_layout(p)
    for sec,raw in zip(sections,pe.sections):sec['characteristics']=int(raw.Characteristics)
    t=next(s for s in sections if s['name']=='.text');dec=Decoder(data[t['raw']:t['raw']+t['raw_size']],t['rva'],base)
    return {'schema':SCHEMA,'status':STATUS,'runtime_sha256':RUNTIME_SHA256,'savedata_sha256':SAVEDATA_SHA256,
            'r28_exact_original_revalidated':True,'r28_exact_report_sha256':digest,'static_only':True,
            'contexts':[scalar_context(dec,sections,prior,*row) for row in ROWS],
            'shared_address_references':shared_references(dec,sections),**{k:False for k in FLAGS}}

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
