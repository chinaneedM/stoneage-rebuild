"""Bounded static palette-source windows from authenticated original TW1 bytes.

Derived x86 instruction metadata only. No original palette bytes, executable,
image or audio is emitted. This triage does not certify historical color.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct

EXE_SHA='cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a'
PAL_SHA='89709d906bbd9cd9f5c2b8e0bd993e2897a1c9136ada2e211109983bb3b06cbf'


def authenticate(raw, palette):
    if len(raw)!=425984 or hashlib.sha256(raw).hexdigest()!=EXE_SHA:
        raise ValueError('not accepted TW1 original sa_3.exe')
    if len(palette)!=708 or hashlib.sha256(palette).hexdigest()!=PAL_SHA:
        raise ValueError('not accepted TW1 Palet_0.sap')


def inspect(raw,palette):
    authenticate(raw,palette)
    import pefile
    from capstone import Cs,CS_ARCH_X86,CS_MODE_32
    from capstone.x86 import X86_OP_IMM,X86_OP_MEM
    pe=pefile.PE(data=raw);base=pe.OPTIONAL_HEADER.ImageBase
    md=Cs(CS_ARCH_X86,CS_MODE_32);md.detail=True;md.skipdata=True
    instructions=[]
    for sec in pe.sections:
        if sec.Characteristics & 0x20000000:
            instructions.extend(i for i in md.disasm(sec.get_data(),base+sec.VirtualAddress) if i.id)
    strings=[]
    for m in re.finditer(rb'[\x20-\x7e]{4,}',raw):
        if re.search(rb'(?i)(palet|\.sap)',m.group()):
            strings.append({'file_offset':m.start(),'rva':pe.get_rva_from_offset(m.start()),
                            'text':m.group().decode('ascii')})
    if not 1<=len(strings)<=32:raise ValueError('palette literal census outside finite scope')
    starts=sorted({i.operands[0].imm for i in instructions if i.mnemonic=='call' and i.operands and i.operands[0].type==X86_OP_IMM})
    rows={i.address:i for i in instructions}
    pointer_slots=[]
    for s in strings:
        address=base+s['rva']
        for offset in range(0,len(raw)-3,4):
            if struct.unpack_from('<I',raw,offset)[0]==address:
                pointer_slots.append({'slot_rva':pe.get_rva_from_offset(offset),'literal_rva':s['rva']})
    refs=[]
    for s in strings:
        address=base+s['rva']
        for i in instructions:
            if any((op.type==X86_OP_IMM and op.imm==address) or
                   (op.type==X86_OP_MEM and op.mem.base==0 and op.mem.index==0 and op.mem.disp==address)
                   for op in i.operands):
                refs.append({'literal_rva':s['rva'],'instruction_rva':i.address-base,
                             'kind':'LITERAL_ADDRESS_CANDIDATE_MAY_BE_BOUNDARY_CONSTANT'})
    for slot in pointer_slots:
        address=base+slot['slot_rva']
        for i in instructions:
            if any((op.type==X86_OP_IMM and op.imm==address) or
                   (op.type==X86_OP_MEM and op.mem.disp==address) for op in i.operands):
                refs.append({'literal_rva':slot['literal_rva'],'slot_rva':slot['slot_rva'],
                             'instruction_rva':i.address-base,'kind':'STATIC_PATH_POINTER_SLOT_REFERENCE'})
    if len(refs)>48:raise ValueError('palette xref scope exceeded')
    windows={}
    def window(start,end,reason):
        start=max(base,start);end=min(base+len(raw),end)
        key=str(start-base)+':'+str(end-base)
        if key in windows:return
        selected=[i for i in instructions if start<=i.address<end]
        if len(selected)>400:raise ValueError('palette instruction window scope exceeded')
        windows[key]={'start_rva':start-base,'end_rva_exclusive':end-base,'reason':reason,
                      'window_sha256':hashlib.sha256(pe.get_data(start-base,end-start)).hexdigest(),
                      'instructions':[{'rva':i.address-base,'mnemonic':i.mnemonic,'operands':i.op_str} for i in selected]}
    for r in refs:
        address=base+r['instruction_rva']
        preceding=[s for s in starts if base<=s<=address and address-s<=1536]
        start=max(preceding) if preceding else max(base,address-256)
        later=[s for s in starts if s>address]
        end=min(later[0] if later else start+1536,start+1536)
        window(start,end,'DIRECT_PALETTE_LITERAL_REFERENCE_NOT_CERTIFIED_FUNCTION_BOUNDARIES')
    initial=list(windows.values())
    for w in initial:
        for row in w['instructions']:
            i=rows[base+row['rva']]
            if i.mnemonic=='call' and i.operands and i.operands[0].type==X86_OP_IMM:
                target=i.operands[0].imm
                if base<=target<base+0x50000 and len(windows)<20:
                    later=[s for s in starts if s>target]
                    end=min(later[0] if later else target+1024,target+1024)
                    window(target,end,'ONE_LEVEL_DIRECT_CALLEE_WINDOW_NOT_EXECUTED')
    root_starts={base+w['start_rva'] for w in initial}
    callers=[i for i in instructions if i.mnemonic=='call' and i.operands and
             i.operands[0].type==X86_OP_IMM and i.operands[0].imm in root_starts]
    for i in callers[:8]:window(i.address-96,i.address+160,'DIRECT_CALLER_CONTEXT_FOR_ROOT_WINDOW')
    imports=[]
    for dll in pe.DIRECTORY_ENTRY_IMPORT:
        for symbol in dll.imports:
            if symbol.name and any(x in symbol.name.lower() for x in (b'palette',b'color',b'readfile',b'createfile')):
                imports.append({'dll':dll.dll.decode(),'name':symbol.name.decode(),'iat_rva':symbol.address-base})
    return {'schema':'stoneage.tw10.palette_source_triage.p2b_v1',
            'original_exe':{'bytes':len(raw),'sha256':EXE_SHA},
            'original_palette':{'path':'StoneAge/data/pal/Palet_0.sap','bytes':len(palette),'sha256':PAL_SHA,
                'first_672_sha256':hashlib.sha256(palette[:672]).hexdigest(),
                'last_36_sha256':hashlib.sha256(palette[672:]).hexdigest()},
            'image_base':base,'palette_literals':strings,'static_literal_pointer_slots':pointer_slots,
            'direct_literal_xrefs':refs,
            'windows':list(windows.values()),'selected_imports':imports,
            'original_client_executed':False,'historical_color_proven':False,
            'original_palette_bytes_published':False,'actual_scene_palette_selection_proven':False}


def main():
    p=argparse.ArgumentParser();p.add_argument('--exe',type=Path,required=True)
    p.add_argument('--palette',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();d=inspect(a.exe.read_bytes(),a.palette.read_bytes())
    data=json.dumps(d,ensure_ascii=False,indent=2)+'\n'
    if len(data.encode())>250000:raise ValueError('derived instruction report exceeded finite scope')
    a.output.write_text(data)
    print('TW1_PALETTE_STATIC_SOURCE_TRIAGE='+json.dumps(d,separators=(',',':')))


if __name__=='__main__':main()
