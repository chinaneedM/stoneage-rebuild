"""Offline, hash-pinned StoneAge2 route evidence; no fetch or program execution.

Decode selected exact x86 windows and emit derived operand/control-flow metadata.
Registry/path decisions are documented interpretations, not runtime observations.
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
from tools.stoneage_jss_saupdate_xref_probe import parse_imports

EXPECTED_SHA256 = 'd0d9c33acc7eb47c2f625b827d5e30daccd29cb9782ff6c302b730e0a5406b2f'
EXPECTED_BYTES = 253952
SLOTS = {0x856c0: 'host-buffer', 0x85740: 'manifest-path-buffer', 0x85840: 'port-word'}
TOKENS = ('stoneage.wayi.com.tw', '/saupdate/newest6.txt', '/saupdate/sa70a/newest7x.txt',
          '%s/data/path.txt', 'Software\\Wayi\\石器時代\\5.00.000',
          'Software\\Waei\\石器時代\\5.00.000', 'saupdate', 'newest', 'GET %s\r\n')
WINDOWS = ((0x18a0, 0x19a0), (0x19a0, 0x1b5c), (0x3d4e, 0x3d7f), (0x3ffa, 0x4046),
           (0x6360, 0x6397), (0x19870, 0x19876), (0xf170, 0xf1f0))


def decode_window(blob: bytes, start_va: int):
    decoder = Cs(CS_ARCH_X86, CS_MODE_32)
    decoder.detail = True
    rows = list(decoder.disasm(blob, start_va))
    if sum(row.size for row in rows) != len(blob):
        raise ValueError('Window did not decode completely')
    return rows


def operand_metadata(ins, image_base: int) -> list[dict]:
    rows = []
    for op in ins.operands:
        row = {'width_bytes': op.size}
        if op.type == X86_OP_REG:
            row.update(kind='register', name=ins.reg_name(op.reg))
        elif op.type == X86_OP_IMM:
            row.update(kind='immediate', value=op.imm & 0xffffffff)
        elif op.type == X86_OP_MEM:
            row.update(kind='memory', base=ins.reg_name(op.mem.base),
                       index=ins.reg_name(op.mem.index), scale=op.mem.scale,
                       displacement=op.mem.disp)
            if not op.mem.base and not op.mem.index:
                row['absolute_rva'] = (op.mem.disp & 0xffffffff) - image_base
        else:
            row['kind'] = 'other'
        rows.append(row)
    return rows


def raw_window(payload, layout, start, end):
    if end <= start:
        raise ValueError('Expected nonempty forward window')
    for section in layout['sections']:
        relative = start-section['vaddr']
        if section['chars'] & 0x20000000 and 0 <= relative and end-start <= section['raw_size']-relative:
            offset = section['raw_ptr']+relative
            return payload[offset:offset+end-start]
    raise ValueError('Window outside executable raw section')


def probe(payload: bytes) -> dict:
    if len(payload) != EXPECTED_BYTES or hashlib.sha256(payload).hexdigest() != EXPECTED_SHA256:
        raise ValueError('Expected exact accepted decompressed updater specimen')
    inventory_pe(payload)
    layout = parse_pe_layout(payload)
    image_base = struct.unpack_from('<I', payload, layout['pe_off']+52)[0]
    tokens = []
    token_addresses = {}
    for text in TOKENS:
        encoded = text.encode('big5')+b'\0'
        start = 0
        while (offset := payload.find(encoded, start)) >= 0:
            start = offset+1
            for section in layout['sections']:
                if section['raw_ptr'] <= offset < section['raw_ptr']+section['raw_size']:
                    rva = section['vaddr']+offset-section['raw_ptr']
                    tokens.append({'text':text, 'file_offset':offset, 'rva':rva})
                    token_addresses[image_base+rva] = text
                    break
    imports = parse_imports(payload, layout, image_base)
    windows = []
    for start, end in WINDOWS:
        instructions = decode_window(raw_window(payload, layout, start, end), image_base+start)
        rows = []
        for ins in instructions:
            operands = operand_metadata(ins, image_base)
            labels = []
            for op in operands:
                address = op.get('value') if op['kind']=='immediate' else op.get('displacement') if 'absolute_rva' in op else None
                if address in token_addresses:
                    labels.append('literal:'+token_addresses[address])
                if address is not None and address-image_base in SLOTS:
                    labels.append('slot:'+SLOTS[address-image_base])
                if address in imports:
                    labels.append('import:'+':'.join(imports[address]))
            control = ins.mnemonic in ('call','jmp') or ins.mnemonic.startswith(('j','ret'))
            # Full operand shapes only for selected structural operations, not raw disassembly.
            if labels or control or ins.mnemonic in ('dec','rep movsd','rep movsb') or start in (0x6360,0x19870,0xf170):
                rows.append({'rva':ins.address-image_base,'operation':ins.mnemonic,
                             'operands':operands,'labels':labels})
        windows.append({'start_rva':start,'end_rva_exclusive':end,'instruction_count':len(instructions),'structural_rows':rows})
    return {'schema':'STONEAGE-WAYI-SAUPDATE-ROUTE-PROBE-R1',
            'decompressed_input_bytes':len(payload),'decompressed_input_sha256':EXPECTED_SHA256,
            'image_base':image_base,'literal_locations':tokens,'global_slot_rvas':SLOTS,
            'windows':windows,'file_executed':False,'live_server_contacted':False,
            'manifest_bytes_obtained':False,'publisher_original_hash_verified':False,
            'native_pet_runtime_verified':False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('local_decompressed_updater', type=Path)
    args = parser.parse_args()
    with args.local_decompressed_updater.open('rb') as stream:
        payload=stream.read(EXPECTED_BYTES+1)
    print(json.dumps(probe(payload),ensure_ascii=False,indent=2))

if __name__ == '__main__': main()
