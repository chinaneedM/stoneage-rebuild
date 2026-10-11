"""Hash-pinned offline PET transport/control-edge inventory; never executes client."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import struct
from capstone.x86 import X86_OP_IMM, X86_OP_MEM
from tools.stoneage_jss_launcher_deep_probe import parse_pe_layout
from tools.stoneage_jss_saupdate_xref_probe import parse_imports
from tools.stoneage_wayi_pet_sender_probe import EXPECTED_SHA256, EXPECTED_BYTES, trace_cdecl
from tools.stoneage_wayi_saupdate_route_probe import decode_window, raw_window, operand_metadata

# Only instruction-aligned, bounded windows independently inspected on this hash.
WINDOWS = {
    'drag-guard': (0x523ea, 0x52471),
    'double-click-guard': (0x525c3, 0x52623),
    'drag-out-guard': (0x531a9, 0x5320d),
    'send-message-hub': (0x8fe70, 0x8feca),
    'encoder': (0x8fc10, 0x8fccb),
    'decoder': (0x8fcd0, 0x8fd91),
    'receive-id-and-end': (0x8fda0, 0x8fe62),
    'receive-dispatch-prefix': (0x90990, 0x909e5),
    'send-handoff': (0x3e300, 0x3e363),
    'callback-setter-prefix': (0x3d9a0, 0x3d9b7),
    'callback-binding': (0x5ec32, 0x5ec48),
    'send-queue': (0x5ed20, 0x5edb1),
    'queue-flush': (0x5ea8a, 0x5eb01),
    'line-intake': (0x5ee80, 0x5ef10),
    'receive-mode-selection': (0x5eb44, 0x5eb6b),
    'send-import-thunk': (0x94e7c, 0x94e82),
}


def summarize_window(instructions, image_base, imports):
    """Emit control edges, tests and selected constants, without assembly text."""
    calls, branches, comparisons, writes, constants = [], [], [], [], []
    previous = None
    for ins in instructions:
        if not ins.id:
            raise ValueError('Undecoded bytes cannot be evidence')
        operands = operand_metadata(ins, image_base)
        rva = ins.address-image_base
        if ins.mnemonic == 'call':
            target = operands[0]
            row = {'call_rva':rva, 'target':target}
            if target['kind']=='immediate': row['direct_target_rva']=target['value']-image_base
            if target.get('absolute_rva') is not None:
                address=image_base+target['absolute_rva']
                if address in imports:row['import']=list(imports[address])
            calls.append(row)
        elif ins.mnemonic.startswith('j'):
            if ins.operands[0].type==X86_OP_IMM:
                row={'branch_rva':rva,'condition':ins.mnemonic,
                     'target_rva':ins.operands[0].imm-image_base,
                     'fallthrough_rva':rva+ins.size}
                if previous and previous.mnemonic in ('cmp','test'):
                    row['adjacent_comparison_rva']=previous.address-image_base
                branches.append(row)
            else:
                row={'branch_rva':rva,'condition':ins.mnemonic,'indirect_target':operands[0]}
                address=operands[0].get('absolute_rva',-image_base)+image_base
                if address in imports:row['import']=list(imports[address])
                branches.append(row)
        if ins.mnemonic in ('cmp','test'):
            comparisons.append({'rva':rva,'operation':ins.mnemonic,'operands':operands})
        if ins.mnemonic=='mov' and ins.operands[0].type==X86_OP_MEM and not ins.operands[0].mem.base and not ins.operands[0].mem.index:
            writes.append({'rva':rva,'destination':operands[0],'source':operands[1]})
        if ins.mnemonic in ('push','add','sub','mov','not','idiv') and any(o['kind']=='immediate' for o in operands):
            constants.append({'rva':rva,'operation':ins.mnemonic,'operands':operands})
        previous=ins
    return {'instruction_count':len(instructions),'calls':calls,'branches':branches,
            'comparisons':comparisons,'absolute_writes':writes,'selected_constants':constants}


def comparison_branch_taken(condition, left, right, width_bytes):
    """Interpret one CMP/Jcc pair for hypothetical values, not native execution."""
    if width_bytes not in (1,2,4):raise ValueError('Unsupported operand width')
    bits=width_bytes*8;mask=(1<<bits)-1;left&=mask;right&=mask
    sign=1<<(bits-1)
    signed_left=left-(1<<bits) if left&sign else left
    signed_right=right-(1<<bits) if right&sign else right
    tests={'je':left==right,'jne':left!=right,'jl':signed_left<signed_right,
           'jle':signed_left<=signed_right,'jg':signed_left>signed_right,
           'jge':signed_left>=signed_right,'jb':left<right,'jae':left>=right}
    if condition not in tests:raise ValueError('Unsupported branch condition')
    return tests[condition]


def probe(payload):
    if len(payload)!=EXPECTED_BYTES or hashlib.sha256(payload).hexdigest()!=EXPECTED_SHA256:
        raise ValueError('Expected exact accepted decompressed game specimen')
    layout=parse_pe_layout(payload)
    base=struct.unpack_from('<I',payload,layout['pe_off']+52)[0]
    imports=parse_imports(payload,layout,base)
    decoded={label:decode_window(raw_window(payload,layout,*bounds),base+bounds[0]) for label,bounds in WINDOWS.items()}
    windows=[{'label':label,'start_rva':WINDOWS[label][0],
              'end_rva_exclusive':WINDOWS[label][1],
              **summarize_window(insns,base,imports)} for label,insns in decoded.items()]
    # Derive each directional bias from the exact arithmetic instruction.
    def immediate_at(label,rva,operation):
        ins=next(i for i in decoded[label] if i.address-base==rva)
        if ins.mnemonic!=operation or ins.operands[1].type!=X86_OP_IMM:
            raise ValueError('Unexpected directional adjustment')
        return ins.operands[1].imm
    received_subtract=immediate_at('receive-id-and-end',0x8fde8,'sub')
    sent_add=immediate_at('send-message-hub',0x8fe88,'add')
    callback_binding=trace_cdecl(decoded['callback-binding'],base,0,{base+0x3d9a0:(3,None)})
    flush=decode_window(raw_window(payload,layout,0x5eaac,0x5eac0),base+0x5eaac)
    queue_length_load=next(i for i in decoded['queue-flush'] if i.address-base==0x5ea9f)
    flush_args=trace_cdecl([queue_length_load]+flush,base,0,{base+0x94e7c:(4,None)})
    flush_args['path_assumption']='queue-length branch0x5eaa6 does not bypass send'
    flush_args['skipped_control_interval']=[0x5eaa4,0x5eaac]
    return {'schema':'STONEAGE-WAYI-PET-TRANSPORT-PROBE-R1',
            'input_bytes':len(payload),'decompressed_input_sha256':EXPECTED_SHA256,
            'windows':windows,'callback_binding_static_arguments':callback_binding,
            'queue_flush_static_arguments':flush_args,
            'receive_formatted_id_subtract':received_subtract,
            'send_formatted_id_add':sent_add,
            'directional_biases_are_inverse':sent_add==received_subtract,
            'send_ordinal_import':list(imports[base+0xa02b8]),
            'queue_memory_protection_import':list(imports[base+0xa00d0]),
            'encoder_seed_order_literal':payload[0xdb95c:0xdb960].decode('ascii'),
            'decoder_seed_order_literal':payload[0xdb964:0xdb968].decode('ascii'),
            'encoding_alphabet':payload[0xdb918:0xdb958].decode('ascii'),
            'file_executed':False,'packets_captured':False,'matching_server_verified':False,
            'native_pet_runtime_verified':False}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('local_decompressed_client',type=Path);args=parser.parse_args()
    with args.local_decompressed_client.open('rb') as f:payload=f.read(EXPECTED_BYTES+1)
    print(json.dumps(probe(payload),ensure_ascii=False,indent=2))

if __name__=='__main__':main()
