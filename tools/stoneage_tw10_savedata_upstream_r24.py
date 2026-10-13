"""Original-only R24 prefix barriers, scalar definition and conditional flags.

No executable runs, instruction bytes, whole disassembly or ABI role inference.
Alternative prefix anchors can decode differently: no candidate is promoted to
an original entry, complete incoming path, actual stack, heap owner or save IO.
"""
import argparse
import hashlib
import json
import tempfile
from pathlib import Path
from capstone import CS_GRP_CALL, CS_GRP_JUMP, CS_GRP_RET
from capstone.x86 import X86_OP_REG, X86_OP_MEM, X86_OP_IMM, X86_REG_EFLAGS
from tools.stoneage_tw10_savedata_upstream_r23 import (
    inspect_verified as inspect_r23, CALLS, STACK_NEUTRAL_CLASSES,
    local_push_suffix, RUNTIME_SHA256, SAVEDATA_SHA256)
from tools.stoneage_tw10_savedata_upstream_r23_guard import validate as validate_r23
from tools.stoneage_tw10_savedata_write_shapes_r17 import operand_shape, candidate_sources
from tools.stoneage_tw10_savedata_reachdefs_r14 import bounded_graph
from tools.stoneage_tw10_savedata_provenance_r10 import reaches as flag_reaches, semantic_definition
from tools.stoneage_tw10_savedata_inputs_r11 import ALIASES
from tools.stoneage_tw10_savedata_upstream_r22 import graph_path
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder, direct_target
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH, SAVEDATA_PATH
from tools.stoneage_tw10_technical_probe import find_rows, extract_row

SCHEMA='tw10-r24-original-prefix-barrier-scalar-flags'
STATUS='ORIGINAL_CONDITIONAL_STATIC_ONLY_ENTRIES_HEAP_NATIVE_IO_OPEN'
PRIOR_REPORT_SHA256='8d77cdd314def89e534c725d5db3ffa1e004f3fb64141fe73b66f4ebc19751bc'
PREFIXES=((0x499b0,0x499c0,0x499d0),(0x499e0,0x499f0,0x49a00),(0x4a090,0x4a0a0))
SCALAR_SITE=0x4a0b3
SCALAR_ROOT=0x4a0a0
FLAGS=('actual_function_entries_proven','all_incoming_paths_proven',
       'prefix_anchor_alignment_proven','original_stack_or_abi_roles_proven',
       'scalar_runtime_value_proven','branch_outcomes_proven','heap_owner_proven',
       'successful_call_return_admitted','caller_resumption_admitted',
       'native_save_schema_proven','native_io_executed','original_bytes_published')

def barrier_kind(ins):
    writes={ins.reg_name(r) for r in ins.regs_access()[1]}
    if ins.group(CS_GRP_CALL) or ins.group(CS_GRP_JUMP) or ins.group(CS_GRP_RET):
        return 'control_transfer'
    if ins.mnemonic=='push':
        return None if len(ins.operands)==1 and ins.operands[0].size==4 else 'partial_or_other_push'
    if writes & {'esp','sp','spl'}:return 'stack_register_write'
    if any(o.type==X86_OP_MEM and o.access & 2 for o in ins.operands):return 'memory_write'
    if ins.mnemonic not in STACK_NEUTRAL_CLASSES:return 'unmodeled_instruction'
    return None

def prefix_audit(dec,sections,anchor,call,alternatives=()):
    if not 0 <= call-anchor <= 192:raise ValueError('R24 prefix bound')
    cur=anchor;sequence=[];error=None
    while cur<call and len(sequence)<64:
        ins=dec.at(cur)
        if ins is None or cur+ins.size>call:
            error='decode_or_boundary_gap';break
        sequence.append(ins);cur+=ins.size
    boundary=cur==call
    barrier=None
    if boundary:
        for ins in reversed(sequence):
            kind=barrier_kind(ins)
            if kind:
                barrier={'site_rva':ins.address-dec.base,'class':ins.mnemonic,'kind':kind,
                         'operand_shapes':[operand_shape(ins,o,sections,dec.base) for o in ins.operands],
                         'written_registers':sorted({ins.reg_name(r) for r in ins.regs_access()[1]})}
                break
    overlaps=[]
    for ins in sequence:
        start=ins.address-dec.base
        for other in alternatives:
            if start<other<start+ins.size:
                overlaps.append({'alternative_anchor_rva':other,'containing_instruction_rva':start,
                                 'containing_instruction_end_rva':start+ins.size})
    if len(overlaps)>8:raise ValueError('R24 overlap cap')
    return {'anchor_rva':anchor,'call_rva':call,'linear_boundary_reached':boundary,
            'competing_anchor_overlaps':overlaps,
            'decoded_instruction_count':len(sequence),'decode_stop':error or ('call_boundary' if boundary else 'instruction_cap'),
            'last_suffix_barrier':barrier,'r23_suffix':local_push_suffix(dec,sections,anchor,call),
            'verified_entry_or_alignment':False,'actual_stack_values_known':False,
            'all_incoming_paths_proven':False}

def scalar_definition(dec,sections,site=SCALAR_SITE,root=SCALAR_ROOT):
    ins=dec.at(site)
    if ins is None or 'eax' not in {ins.reg_name(r) for r in ins.regs_access()[1]}:
        raise ValueError('R24 scalar site must define EAX')
    shapes=[operand_shape(ins,o,sections,dec.base) for o in ins.operands]
    reads=sorted({ins.reg_name(r) for r in ins.regs_access()[0]} & set(ALIASES))
    model={'kind':'unmodeled','width_bits':None,'shift_count_mask':None,'literal_shift_count':None,
           'output_modulus':None,'evaluated_runtime_result':None}
    ops=ins.operands
    if (ins.mnemonic in ('shl','sal') and len(ops)==2 and ops[0].type==X86_OP_REG
        and ins.reg_name(ops[0].reg)=='eax' and ops[0].size==4 and ops[1].type==X86_OP_IMM):
        model.update(kind='conditional_u32_left_shift',width_bits=32,shift_count_mask=31,
                     literal_shift_count=int(ops[1].imm)&31,output_modulus=4294967296)
    return {'site_rva':site,'anchor_rva':root,'class':ins.mnemonic,'operand_shapes':shapes,
            'register_inputs':reads,'input_sources':{reg:candidate_sources(dec,site,reg,sections,root) for reg in reads},
            'conditional_scalar_model':model,'actual_input_value_known':False,
            'allocation_size_or_role_proven':False,'original_path_executed_proven':False}

def branch_frontier(dec,sections,root=SCALAR_ROOT,call=CALLS[2][2]):
    nodes,edges,front,cap=bounded_graph(dec,root,max_span=192,max_nodes=128)
    flags=flag_reaches(nodes,edges,root,X86_REG_EFLAGS)
    rows=[]
    for at,ins in sorted(nodes.items()):
        if at>=call or not ins.group(CS_GRP_JUMP) or ins.mnemonic in ('jmp','ljmp'):continue
        tokens=sorted(flags.get(at,()),key=lambda t:(t[1],t[0]))
        rows.append({'site_rva':at,'condition':ins.mnemonic,
                     'direct_target_rva':direct_target(ins,dec.base),
                     'graph_path_to_call':graph_path(edges,at,call),
                     'flag_sources':[{'origin':kind,'rva':rva,'semantic':semantic_definition(nodes[rva],X86_REG_EFLAGS,sections,dec.base) if kind=='definition' else None} for kind,rva in tokens[:24]],
                     'flag_sources_truncated':len(tokens)>24,'branch_outcome_known':False})
    if len(rows)>24:raise ValueError('R24 branch cap')
    return {'anchor_rva':root,'call_rva':call,'nodes':len(nodes),'edges':len(edges),'node_cap':cap,
            'frontier':[{'reason':why,'rva':at} for why,at in front],'branches':rows,
            'opaque_calls_kill_flags':True,'actual_paths_or_complete_entries_proven':False}

def inspect_verified(runtime,savedata):
    prior=inspect_r23(runtime,savedata);validate_r23(prior)
    digest=hashlib.sha256((json.dumps(prior,sort_keys=True)+'\n').encode()).hexdigest()
    if digest!=PRIOR_REPORT_SHA256:raise ValueError('R23 exact original derivative changed')
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'sa_3.exe';p.write_bytes(runtime)
        data,pe,base,sections,_=image_layout(p)
    for sec,raw in zip(sections,pe.sections):sec['characteristics']=int(raw.Characteristics)
    t=next(s for s in sections if s['name']=='.text')
    dec=Decoder(data[t['raw']:t['raw']+t['raw_size']],t['rva'],base)
    audits=[]
    for old,anchors in zip(prior['heap_links'],PREFIXES):
        candidates=[prefix_audit(dec,sections,a,old['call_rva'],alternatives=anchors) for a in anchors]
        original=next(c for c in candidates if c['anchor_rva']==old['anchor_rva'])
        if original['r23_suffix']!=old['local_push_suffix']:raise ValueError('R23 exact suffix changed')
        audits.append({'name':old['name'],'call_rva':old['call_rva'],'candidate_prefixes':candidates,
                       'r23_suffix_revalidated':True,'selected_function_entry_proven':False})
    return {'schema':SCHEMA,'status':STATUS,'runtime_sha256':RUNTIME_SHA256,'savedata_sha256':SAVEDATA_SHA256,
            'r23_original_identity_revalidated':True,'r23_exact_report_sha256':digest,'static_only':True,
            'prefix_audits':audits,'realloc_eax_definition':scalar_definition(dec,sections),
            'realloc_branch_frontier':branch_frontier(dec,sections),**{k:False for k in FLAGS}}

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
