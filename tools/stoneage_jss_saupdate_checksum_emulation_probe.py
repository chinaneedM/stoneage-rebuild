#!/usr/bin/env python3
"""Emulate the archived JSS SaUpdate file-checksum helper at RVA 0x3f20.

The helper's CRT file calls are replaced with deterministic in-memory stubs.
Only input labels, returned values, and candidate-algorithm comparisons are
retained. No executable bytes, file payloads, or disassembly are committed.
"""

from __future__ import annotations

import hashlib
import struct
import zlib

from unicorn import Uc, UC_ARCH_X86, UC_MODE_32, UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_ESP, UC_X86_REG_EAX, UC_X86_REG_EIP

from tools.stoneage_jss_launcher_archive_probe import ORIGINAL, get_bounded, replay_url
from tools.stoneage_jss_launcher_deep_probe import KNOWN_SHA256, TIMESTAMP, parse_pe_layout
from tools.stoneage_jss_saupdate_xref_probe import parse_imports
from tools.stoneage_tw10_technical_probe import pe_sections

FUNC_RVA=0x3F20
STACK_BASE=0x10000000
STACK_SIZE=0x10000
SCRATCH_BASE=0x20000000
SCRATCH_SIZE=0x10000
STUB_BASE=0x30000000
SENTINEL=0x31000000
MAX_INSNS=20000

CASES=(
    ("empty", b""),
    ("zero", b"\x00"),
    ("one", b"\x01"),
    ("ff", b"\xff"),
    ("abc", b"abc"),
    ("010203", b"\x01\x02\x03"),
    ("range16", bytes(range(16))),
    ("stoneage", b"StoneAge"),
)


def clean(value,limit=700):
    text=" ".join(str(value if value is not None else "").split())
    return "".join(ch for ch in text if ch>=" " and ch!="\x7f").replace("|","%7C")[:limit]


def map_image(uc,data,layout,image_base):
    high=0x1000
    for sec in layout["sections"]:
        high=max(high,sec["vaddr"]+max(sec["vsize"],sec["raw_size"]))
    size=(high+0xFFF)&~0xFFF
    uc.mem_map(image_base,size)
    for sec in layout["sections"]:
        raw_start=sec["raw_ptr"]
        raw_end=min(len(data),raw_start+sec["raw_size"])
        if raw_end>raw_start:
            uc.mem_write(image_base+sec["vaddr"],data[raw_start:raw_end])
    return size


def import_iat(iat_map,dll,name):
    hits=[
        va for va,(d,n) in iat_map.items()
        if d.lower()==dll.lower() and n==name
    ]
    if len(hits)!=1:
        raise ValueError(f"expected one IAT for {dll}!{name}, got {len(hits)}")
    return hits[0]


def candidate_values(payload):
    xor8=0
    for b in payload:
        xor8 ^= b
    return {
        "sum32":sum(payload)&0xffffffff,
        "xor8":xor8,
        "crc32":zlib.crc32(payload)&0xffffffff,
        "adler32":zlib.adler32(payload)&0xffffffff,
        "len":len(payload)&0xffffffff,
    }


def emulate_checksum(data,layout,image_base,iat_map,payload):
    uc=Uc(UC_ARCH_X86,UC_MODE_32)
    map_image(uc,data,layout,image_base)
    uc.mem_map(STACK_BASE,STACK_SIZE)
    uc.mem_map(SCRATCH_BASE,SCRATCH_SIZE)
    uc.mem_map(STUB_BASE,0x1000)
    uc.mem_map(SENTINEL,0x1000)

    stubs={
        "fopen":STUB_BASE+0x10,
        "fgetc":STUB_BASE+0x20,
        "fclose":STUB_BASE+0x30,
    }
    for name,addr in stubs.items():
        iat=import_iat(iat_map,"MSVCRT.dll",name)
        uc.mem_write(iat,struct.pack("<I",addr))

    filename=SCRATCH_BASE+0x100
    uc.mem_write(filename,b"synthetic.bin\0")
    esp=STACK_BASE+STACK_SIZE-0x100
    uc.mem_write(esp,struct.pack("<II",SENTINEL,filename))
    uc.reg_write(UC_X86_REG_ESP,esp)

    state={"pos":0,"insns":0,"fopen":0,"fgetc":0,"fclose":0}

    def ret_from_stub(emu,eax):
        cur_esp=emu.reg_read(UC_X86_REG_ESP)
        retaddr=struct.unpack("<I",bytes(emu.mem_read(cur_esp,4)))[0]
        emu.reg_write(UC_X86_REG_EAX,eax&0xffffffff)
        emu.reg_write(UC_X86_REG_ESP,cur_esp+4)
        emu.reg_write(UC_X86_REG_EIP,retaddr)

    def hook(emu,address,size,user):
        state["insns"]+=1
        if state["insns"]>MAX_INSNS:
            emu.emu_stop()
            return
        if address==stubs["fopen"]:
            state["fopen"]+=1
            ret_from_stub(emu,0x22222222)
        elif address==stubs["fgetc"]:
            state["fgetc"]+=1
            if state["pos"]<len(payload):
                value=payload[state["pos"]]
                state["pos"]+=1
            else:
                value=0xffffffff
            ret_from_stub(emu,value)
        elif address==stubs["fclose"]:
            state["fclose"]+=1
            ret_from_stub(emu,0)
    uc.hook_add(UC_HOOK_CODE,hook)

    uc.emu_start(image_base+FUNC_RVA,SENTINEL,count=MAX_INSNS)
    eip=uc.reg_read(UC_X86_REG_EIP)&0xffffffff
    eax=uc.reg_read(UC_X86_REG_EAX)&0xffffffff
    return {
        "returned":eip==SENTINEL,
        "eip":eip,
        "eax":eax,
        **state,
    }


def main():
    print("StoneAge JSS SaUpdate checksum-helper emulation probe — R1")
    print("SCOPE|exact-file-helper|stubbed-CRT-I/O|synthetic-bytes|derived-output-only")

    status,final,headers,data=get_bounded(
        replay_url({"timestamp":TIMESTAMP,"original":ORIGINAL}),timeout=20
    )
    sha=hashlib.sha256(data).hexdigest()
    print(f"FETCH|status={status}|bytes={len(data)}|sha256={sha}|final={clean(final)}")
    if sha!=KNOWN_SHA256:
        print(f"RESOLUTION|HASH_MISMATCH|expected={KNOWN_SHA256}")
        return

    layout=parse_pe_layout(data)
    pe=pe_sections(data)
    image_base=pe["image_base"]
    iat_map=parse_imports(data,layout,image_base)

    print(f"FUNCTION|rva=0x{FUNC_RVA:x}|role=file-byte-checksum-candidate")
    exact_matches={}
    successes=0
    failures=0
    for label,payload in CASES:
        try:
            result=emulate_checksum(data,layout,image_base,iat_map,payload)
        except Exception as exc:
            failures+=1
            print(f"CASE_ERROR|label={label}|kind={type(exc).__name__}|message={clean(exc)}")
            continue
        if not result["returned"]:
            failures+=1
            print(
                f"CASE_BOUNDED|label={label}|bytes={len(payload)}|eip=0x{result['eip']:x}|"
                f"eax=0x{result['eax']:x}|instructions={result['insns']}"
            )
            continue
        successes+=1
        candidates=candidate_values(payload)
        matches=sorted(k for k,v in candidates.items() if v==result["eax"])
        for name in matches:
            exact_matches[name]=exact_matches.get(name,0)+1
        print(
            f"CASE|label={label}|bytes={len(payload)}|return={result['eax']}|"
            f"return_hex=0x{result['eax']:08x}|fopen={result['fopen']}|"
            f"fgetc={result['fgetc']}|fclose={result['fclose']}|"
            f"candidate_matches={','.join(matches)}"
        )

    for name,count in sorted(exact_matches.items()):
        print(f"CANDIDATE_MATCH_COUNT|name={name}|cases={count}")

    full=[
        name for name,count in exact_matches.items()
        if count==successes and successes>0
    ]
    print(
        f"RESOLUTION|CHECKSUM_HELPER_EMULATED|successes={successes}|failures={failures}|"
        f"full_candidate_matches={','.join(sorted(full))}|binary-not-committed"
    )


if __name__=="__main__":
    main()
