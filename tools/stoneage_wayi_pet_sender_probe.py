"""Offline static PET sender/argument evidence for exact operator-linked sa.exe.

No program execution or networking. A limited symbolic stack walk emits call
arguments under explicit helper-return contracts; it is not a runtime witness.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import struct
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_OP_REG
from tools.stoneage_wayi_pe_static_inventory import inventory_pe
from tools.stoneage_jss_launcher_deep_probe import parse_pe_layout
from tools.stoneage_wayi_saupdate_route_probe import decode_window, raw_window

EXPECTED_SHA256 = '4193a7e1b20b996f7902424ae05092b455c5dbbe3f133d331a4897bbc7abfe63'
EXPECTED_BYTES = 921600
EMITTER = 0x93c50
INTEGER_APPEND = 0x907a0
SEND_HUB = 0x8fe70
CALLER_WINDOWS = ((0x52450,0x5246c),(0x52603,0x52620),(0x531e5,0x53208))


def add_expression(left, right):
    values = []
    for value in (left, right):
        values.extend(value['sum'] if isinstance(value,dict) and 'sum' in value else [value])
    return {'sum': values}


def trace_cdecl(instructions, image_base, initial_esp, helper_contracts):
    """Track only a straight-line cdecl call window; unknown effects fail closed.

    Contracts map exact callee VA to argument count and optional return-arg index.
    Expressions describe original stack arguments/globals, never load live memory.
    """
    esp = initial_esp
    registers = {}
    stack = {}
    calls = []

    def read(op, ins):
        if op.type == X86_OP_IMM:
            return op.imm & 0xffffffff
        if op.type == X86_OP_REG:
            name=ins.reg_name(op.reg)
            return registers.get(name, {'unknown_register':name})
        if op.type == X86_OP_MEM:
            mem=op.mem
            if ins.reg_name(mem.base)=='esp' and not mem.index:
                slot=esp+mem.disp
                if slot in stack:return stack[slot]
                if slot>=4 and slot%4==0:return {'original_argument':slot//4}
                return {'unknown_stack_offset':slot}
            if not mem.base and not mem.index:
                return {'global_rva':(mem.disp & 0xffffffff)-image_base,'width_bytes':op.size}
        return {'unresolved':True}

    for ins in instructions:
        if not ins.id:raise ValueError('Skipped data in argument window')
        ops=ins.operands;name=ins.mnemonic
        if name=='push':
            value=read(ops[0],ins);esp-=4;stack[esp]=value
        elif name=='pop':
            if ops[0].type!=X86_OP_REG:raise ValueError('Unsupported pop')
            registers[ins.reg_name(ops[0].reg)]=stack.get(esp,{'unknown_stack_offset':esp});esp+=4
        elif name=='mov':
            if ops[0].type==X86_OP_REG:
                registers[ins.reg_name(ops[0].reg)]=read(ops[1],ins)
            elif ops[0].type==X86_OP_MEM and ops[0].size==1:
                # This selected window only initializes its local byte buffer.
                mem=ops[0].mem
                if ins.reg_name(mem.base)!='esp' or mem.index or esp+mem.disp>=0:
                    raise ValueError('Unsupported memory write')
            else:raise ValueError('Unsupported mov destination')
        elif name=='lea':
            mem=ops[1].mem
            if ops[0].type!=X86_OP_REG or ins.reg_name(mem.base)!='esp' or mem.index:
                raise ValueError('Unsupported address expression')
            registers[ins.reg_name(ops[0].reg)]={'local_address':esp+mem.disp}
        elif name in ('add','sub'):
            dst=ins.reg_name(ops[0].reg) if ops[0].type==X86_OP_REG else None
            if dst=='esp' and ops[1].type==X86_OP_IMM:
                esp += ops[1].imm if name=='add' else -ops[1].imm
            elif dst and name=='add':
                registers[dst]=add_expression(read(ops[0],ins),read(ops[1],ins))
            else:raise ValueError('Unsupported arithmetic')
        elif name=='call':
            if ops[0].type!=X86_OP_IMM:raise ValueError('Indirect call not contracted')
            target=ops[0].imm & 0xffffffff
            if target not in helper_contracts:raise ValueError('Uncontracted callee')
            count,return_arg=helper_contracts[target]
            args=[stack.get(esp+4*i,{'unknown_stack_offset':esp+4*i}) for i in range(count)]
            calls.append({'call_rva':ins.address-image_base,'target_rva':target-image_base,'arguments':args})
            registers['eax']=args[return_arg] if return_arg is not None else {'unknown_call_return':target-image_base}
            registers['ecx']={'clobbered_by_call':target-image_base}
            registers['edx']={'clobbered_by_call':target-image_base}
        elif name=='nop':pass
        else:raise ValueError('Nonlinear or unsupported operation '+name)
    return {'calls':calls,'final_esp_offset':esp,'interpretation':'STATIC_WITH_EXPLICIT_HELPER_CONTRACTS'}


def raw_e8_refs(blob, section_rva, target_rva):
    return [section_rva+i for i in range(max(0,len(blob)-4))
            if blob[i]==0xe8 and section_rva+i+5+struct.unpack_from('<i',blob,i+1)[0]==target_rva]


def probe(payload):
    if len(payload)!=EXPECTED_BYTES or hashlib.sha256(payload).hexdigest()!=EXPECTED_SHA256:
        raise ValueError('Expected exact accepted decompressed game specimen')
    inventory_pe(payload);layout=parse_pe_layout(payload)
    base=struct.unpack_from('<I',payload,layout['pe_off']+52)[0]
    decoder=Cs(CS_ARCH_X86,CS_MODE_32);decoder.detail=True;decoder.skipdata=True
    coverage=[];refs={SEND_HUB:[],EMITTER:[]};raw_refs={SEND_HUB:[],EMITTER:[]}
    for sec in layout['sections']:
        if not sec['chars']&0x20000000:continue
        blob=payload[sec['raw_ptr']:sec['raw_ptr']+sec['raw_size']]
        instructions=list(decoder.disasm(blob,base+sec['vaddr']))
        gaps=[{'rva':x.address-base,'size':x.size} for x in instructions if not x.id]
        coverage.append({'section':sec['name'],'raw_bytes':len(blob),
                         'decoded_bytes':sum(x.size for x in instructions if x.id),
                         'skipped_bytes':sum(x.size for x in instructions if not x.id),'gaps':gaps})
        for target in refs:
            raw_refs[target]+=raw_e8_refs(blob,sec['vaddr'],target)
        for ins in instructions:
            if ins.id and ins.mnemonic=='call' and ins.operands[0].type==X86_OP_IMM:
                target=ins.operands[0].imm-base
                if target in refs:refs[target].append(ins.address-base)
    def window(start,end):return decode_window(raw_window(payload,layout,start,end),base+start)
    emitter_trace=trace_cdecl(window(EMITTER+10,0x93ce3),base,-0x4000,
                              {base+INTEGER_APPEND:(2,1),base+SEND_HUB:(3,None)})
    caller_traces=[{'start_rva':start,'end_rva_exclusive':end,
                   **trace_cdecl(window(start,end),base,0,{base+EMITTER:(6,None)})}
                   for start,end in CALLER_WINDOWS]
    hub_insns=window(SEND_HUB,0x8feca)
    bias_ins=next(x for x in hub_insns if x.address-base==0x8fe88)
    if bias_ins.mnemonic!='add' or bias_ins.operands[1].type!=X86_OP_IMM:
        raise ValueError('Missing exact observed message-ID adjustment')
    bias=bias_ins.operands[1].imm
    logical_id=emitter_trace['calls'][-1]['arguments'][1]
    helper_call_sites=[]
    for label,start,end in [('message-hub',SEND_HUB,0x8feca),('integer-append',INTEGER_APPEND,0x90855),
                            ('stack-allocation',0x96620,0x9664f)]:
        insns=window(start,end)
        helper_call_sites.append({'label':label,'start_rva':start,'end_rva_exclusive':end,
                                  'instruction_count':len(insns),
                                  'direct_calls':[{'rva':x.address-base,'target_rva':x.operands[0].imm-base}
                                  for x in insns if x.mnemonic=='call' and x.operands[0].type==X86_OP_IMM]})
    return {'schema':'STONEAGE-WAYI-COMPILED-PET-SENDER-PROBE-R1',
            'input_bytes':len(payload),'decompressed_input_sha256':EXPECTED_SHA256,
            'linear_decode_coverage_not_runtime':coverage,'decoded_direct_calls':refs,
            'raw_e8_candidates':raw_refs,'emitter_static_argument_trace':emitter_trace,
            'caller_static_argument_traces':caller_traces,'helper_windows':helper_call_sites,
            'helper_contract_basis':'integer append preserves second original argument in EAX; stack helper reserves EAX bytes, independently inspected exact helper windows',
            'logical_message_id':logical_id,'hub_message_id_bias':bias,'formatted_message_id':logical_id+bias,
            'formatted_message_id_is_raw_wire_observation':False,
            'frame_format_literal':payload[0xdb970:payload.index(b'\0',0xdb970)].decode('ascii'),
            'riding_guard_ui_text':payload[0xc5da8:payload.index(b'\0',0xc5da8)].decode('big5'),
            'file_executed':False,'native_pet_runtime_verified':False,
            'matching_server_verified':False,'publisher_original_hash_verified':False}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('local_decompressed_client',type=Path);args=parser.parse_args()
    with args.local_decompressed_client.open('rb') as f:payload=f.read(EXPECTED_BYTES+1)
    print(json.dumps(probe(payload),ensure_ascii=False,indent=2))

if __name__=='__main__':main()
