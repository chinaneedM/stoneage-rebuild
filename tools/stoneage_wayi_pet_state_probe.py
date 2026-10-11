"""Offline static S/B PET display-state layout for one exact archived client."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import struct
from capstone.x86 import X86_OP_IMM, X86_OP_REG, X86_OP_MEM
from tools.stoneage_jss_launcher_deep_probe import parse_pe_layout
from tools.stoneage_wayi_pet_sender_probe import EXPECTED_BYTES, EXPECTED_SHA256
from tools.stoneage_wayi_pet_transport_probe import summarize_window
from tools.stoneage_wayi_saupdate_route_probe import decode_window, raw_window, operand_metadata


def read_rva(payload, layout, rva, size):
    if size<=0:raise ValueError('Positive bounded size required')
    for section in layout['sections']:
        relative=rva-section['vaddr']
        if 0<=relative and relative+size<=section['raw_size']:
            offset=section['raw_ptr']+relative
            if offset+size>len(payload):raise ValueError('Truncated section')
            return payload[offset:offset+size]
    raise ValueError('RVA not contained in raw section')


def resolve_indexed_switch(payload, layout, lower, count, index_rva, target_rva, target_count, image_base):
    if not 0<count<=256 or not 0<target_count<=256 or not 0<=lower<=255 or lower+count>256:
        raise ValueError('Unbounded switch or non-byte input range')
    indices=read_rva(payload,layout,index_rva,count)
    targets=read_rva(payload,layout,target_rva,target_count*4)
    result=[]
    for i,index in enumerate(indices):
        if index>=target_count:raise ValueError('Index exceeds jump table')
        address=struct.unpack_from('<I',targets,index*4)[0]
        rva=address-image_base
        if not any(s['chars']&0x20000000 and 0<=rva-s['vaddr']<s['raw_size'] for s in layout['sections']):
            raise ValueError('Switch target outside executable raw section')
        result.append({'input_byte':lower+i,'table_index':index,'target_rva':rva})
    return result


def affine_address(instructions, initial_registers, stack_symbols):
    """Limited signed affine metadata walk; no live memory or native execution."""
    regs={k:dict(v) for k,v in initial_registers.items()}
    def plus(a,b,scale=1):
        out=dict(a)
        for key,value in b.items():out[key]=out.get(key,0)+scale*value
        return {k:v for k,v in out.items() if v}
    def get(name):
        if name not in regs:raise ValueError('Unknown address register '+name)
        return regs[name]
    for ins in instructions:
        ops=ins.operands
        if not ins.id or not ops or ops[0].type!=X86_OP_REG:raise ValueError('Unsupported address operation')
        dst=ins.reg_name(ops[0].reg)
        if ops[0].size!=4:raise ValueError('Partial address register')
        if ins.mnemonic=='lea':
            mem=ops[1].mem;value={'constant':mem.disp} if mem.disp else {}
            if mem.base:value=plus(value,get(ins.reg_name(mem.base)))
            if mem.index:value=plus(value,get(ins.reg_name(mem.index)),mem.scale)
            regs[dst]=value
        elif ins.mnemonic=='shl' and ops[1].type==X86_OP_IMM and 0<=ops[1].imm<=31:
            regs[dst]={k:v*(1<<ops[1].imm) for k,v in get(dst).items()}
        elif ins.mnemonic=='sub' and ops[1].type==X86_OP_REG:
            regs[dst]=plus(get(dst),get(ins.reg_name(ops[1].reg)),-1)
        elif ins.mnemonic=='mov' and ops[1].type==X86_OP_REG:
            regs[dst]=dict(get(ins.reg_name(ops[1].reg)))
        elif ins.mnemonic=='mov' and ops[1].type==X86_OP_MEM:
            mem=ops[1].mem
            if ins.reg_name(mem.base)!='esp' or mem.index or mem.disp not in stack_symbols:
                raise ValueError('Uncontracted stack address input')
            regs[dst]={stack_symbols[mem.disp]:1}
        else:raise ValueError('Unsupported address instruction '+ins.mnemonic)
    return regs


def loop_values(start, stride, limit):
    if stride<=0 or limit<=start or limit-start>4096:raise ValueError('Unbounded/inconsistent loop')
    return list(range(start,limit,stride))


def probe(payload):
    if len(payload)!=EXPECTED_BYTES or hashlib.sha256(payload).hexdigest()!=EXPECTED_SHA256:
        raise ValueError('Expected exact accepted decompressed game specimen')
    layout=parse_pe_layout(payload);base=struct.unpack_from('<I',payload,layout['pe_off']+52)[0]
    def window(a,b):return decode_window(raw_window(payload,layout,a,b),base+a)
    switch=resolve_indexed_switch(payload,layout,0x42,23,0x620d0,0x62094,15,base)
    branch=next(x for x in switch if x['input_byte']==ord('B'))
    if branch['target_rva']!=0x61d0b:raise ValueError('Changed B route')
    body=window(0x61d0b,0x62086);by_rva={i.address-base:i for i in body}
    def imm(rva,operation,index=1):
        ins=by_rva[rva]
        if ins.mnemonic!=operation or ins.operands[index].type!=X86_OP_IMM:raise ValueError('Changed loop structure')
        return ins.operands[index].imm
    start=imm(0x61d12,'mov');stride=imm(0x6206c,'add');limit=imm(0x62075,'cmp')
    slot_stride=imm(0x6206f,'add');clear_dwords=imm(0x61d6a,'mov')
    backedge=by_rva[0x62080]
    if backedge.mnemonic!='jl' or backedge.operands[0].imm-base!=0x61d2a:
        raise ValueError('Changed exclusive signed loop backedge')
    registers=affine_address(window(0x61d88,0x61d9a),{'ecx':{'pet_index':1}},{0x14:'slot_byte_offset'})
    origin_rva=by_rva[0x61e46].operands[0].mem.disp-base
    # Field labels are pinned descendant-source comparisons; offsets/widths are binary observations.
    fields=[]
    sites=[(3,'color',0x61e46),(5,'graNo',0x61ec8),(6,'field',0x61ed7),
           (7,'target',0x61ef1),(8,'level',0x61f2c),(9,'sendFlag',0x61f4f),
           (11,'pile',0x61fc1),(13,'type',0x6201e)]
    for token,label,rva in sites:
        ins=by_rva[rva];op=ins.operands[0]
        fields.append({'token_within_slot':token,'semantic_label_from_source':label,
                       'write_rva':rva,'offset_in_record':op.mem.disp-base-origin_rva,'width_bytes':op.size})
    strings=[]
    for token,label,rva in [(1,'name',0x61dbf),(2,'name2',0x61e1b),(4,'memo',0x61e9d),
                            (10,'damage',0x61f88),(12,'alch',0x61fdf),(14,'jigsaw',0x62048)]:
        ins=by_rva[rva];op=ins.operands[1]
        strings.append({'token_within_slot':token,'semantic_label_from_source':label,
                        'destination_lea_rva':rva,'offset_in_record':op.mem.disp-base-origin_rva})
    windows=[]
    for label,a,b in [('S46-dispatch',0x912c8,0x91329),('category-prefix',0x600a9,0x600ce),
                      ('B-PET-state',0x61d0b,0x62086),('UI-use-flag-address',0x523b4,0x523c9),
                      ('string-token-helper',0x8dcd0,0x8dd40),
                      ('integer-token-helper',0x8ddb0,0x8ddfd),('pre-callback-noop',0x65480,0x65481)]:
        windows.append({'label':label,'start_rva':a,'end_rva_exclusive':b,**summarize_window(window(a,b),base,{})})
    dispatch=window(0x912c8,0x91329)
    logical_id=dispatch[0].operands[1].imm
    callback=next(i for i in dispatch if i.address-base==0x9130d).operands[0].imm-base
    return {'schema':'STONEAGE-WAYI-PET-STATE-PROBE-R1','input_bytes':len(payload),
            'decompressed_input_sha256':EXPECTED_SHA256,'status_logical_message_id':logical_id,
            'status_callback_rva':callback,'indexed_category_switch':switch,
            'pet_category_byte':ord('B'),'pet_category_branch_rva':branch['target_rva'],
            'slot_token_loop':{'start':start,'step':stride,'exclusive_limit':limit,'values':loop_values(start,stride,limit)},
            'slots_per_pet':len(loop_values(start,stride,limit)),
            'record_stride_bytes':slot_stride,'empty_record_clear_bytes':clear_dwords*4,
            'record_origin_rva':origin_rva,'address_expression':registers['ebp'],
            'numeric_field_writes':fields,'string_destinations':strings,
            'use_flag_offset':by_rva[0x61da4].operands[0].mem.disp-base-origin_rva,
            'use_flag_width_bytes':by_rva[0x61da4].operands[0].size,
            'windows':windows,'field_names_are_source_comparison':True,
            'file_executed':False,'packets_captured':False,'matching_server_verified':False,
            'native_pet_owner_save_unique_code_verified':False}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('local_decompressed_client',type=Path);args=parser.parse_args()
    with args.local_decompressed_client.open('rb') as f:payload=f.read(EXPECTED_BYTES+1)
    print(json.dumps(probe(payload),ensure_ascii=False,indent=2))

if __name__=='__main__':main()
