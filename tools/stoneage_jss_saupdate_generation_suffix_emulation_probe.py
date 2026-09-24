#!/usr/bin/env python3
"""Bounded emulation of the JSS SaUpdate generation-suffix helper at RVA 0x2060.

The hash-pinned archived executable is fetched transiently. MSVCRT!atoi is
replaced by a tiny emulation stub whose input and return value are recorded.
Only synthetic input/output behavior is retained.
"""

from __future__ import annotations

import hashlib
import struct

from unicorn import Uc, UC_ARCH_X86, UC_MODE_32, UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_EIP, UC_X86_REG_ESP

from tools.stoneage_jss_launcher_archive_probe import ORIGINAL, get_bounded, replay_url
from tools.stoneage_jss_launcher_deep_probe import KNOWN_SHA256, TIMESTAMP, parse_pe_layout
from tools.stoneage_jss_saupdate_token_emulation_probe import map_image
from tools.stoneage_tw10_technical_probe import pe_sections

FUNC_RVA=0x2060
ATOI_IAT_RVA=0x5264
MAX_INSNS=2000
STACK_BASE=0x12000000
STACK_SIZE=0x10000
SCRATCH_BASE=0x22000000
SCRATCH_SIZE=0x10000
STUB_BASE=0x32000000
SENTINEL=0x33000000

CASES=(
    ("generation-before-extension","real_12.bin",12),
    ("leading-zero","spr_0017.bin",17),
    ("trailing-text","battle_42extra.dat",42),
    ("negative","sound_-3.bin",-3),
    ("underscore-after-dot","real.bin_12",0),
    ("dot-no-underscore","real.bin",0),
    ("no-dot","real_12",0),
    ("nondigit-suffix","real_beta.bin",0),
    ("last-underscore-before-dot","real_beta_9.bin",9),
    ("nested-extension","foo_27.bar.baz",27),
)


def clean(value,limit=700):
    text=str(value if value is not None else "")
    text=text.replace("\r","\\r").replace("\n","\\n").replace("\t","\\t")
    return "".join(ch for ch in text if ch>=" " and ch!="\x7f").replace("|","%7C")[:limit]


def c_atoi(text):
    i=0
    while i<len(text) and text[i].isspace():
        i+=1
    sign=1
    if i<len(text) and text[i] in "+-":
        if text[i]=="-":
            sign=-1
        i+=1
    start=i
    value=0
    while i<len(text) and text[i].isdigit():
        value=value*10+ord(text[i])-48
        i+=1
    if i==start:
        return 0
    return sign*value


def read_c_string(uc,address,limit=256):
    raw=bytes(uc.mem_read(address,limit))
    return raw.split(b"\0",1)[0].decode("ascii","replace")


def emulate_case(data,layout,image_base,text):
    uc=Uc(UC_ARCH_X86,UC_MODE_32)
    map_image(uc,data,layout,image_base)
    uc.mem_map(STACK_BASE,STACK_SIZE)
    uc.mem_map(SCRATCH_BASE,SCRATCH_SIZE)
    uc.mem_map(STUB_BASE,0x1000)
    uc.mem_map(SENTINEL,0x1000)
    uc.mem_write(STUB_BASE,b"\xC3")
    uc.mem_write(image_base+ATOI_IAT_RVA,struct.pack("<I",STUB_BASE))

    src=SCRATCH_BASE+0x100
    uc.mem_write(src,text.encode("ascii")+b"\0")
    esp=STACK_BASE+STACK_SIZE-0x100
    uc.mem_write(esp,struct.pack("<II",SENTINEL,src))
    uc.reg_write(UC_X86_REG_ESP,esp)

    state={"insns":0,"atoi_calls":0,"atoi_input":""}
    def hook_code(emu,address,size,user_data):
        state["insns"]+=1
        if state["insns"]>MAX_INSNS:
            emu.emu_stop()
            raise RuntimeError("instruction bound exceeded")
        if address==STUB_BASE:
            stub_esp=emu.reg_read(UC_X86_REG_ESP)&0xffffffff
            arg_ptr=struct.unpack("<I",bytes(emu.mem_read(stub_esp+4,4)))[0]
            value_text=read_c_string(emu,arg_ptr)
            state["atoi_calls"]+=1
            state["atoi_input"]=value_text
            emu.reg_write(UC_X86_REG_EAX,c_atoi(value_text)&0xffffffff)
    uc.hook_add(UC_HOOK_CODE,hook_code)

    uc.emu_start(image_base+FUNC_RVA,SENTINEL,count=MAX_INSNS)
    eip=uc.reg_read(UC_X86_REG_EIP)&0xffffffff
    eax=uc.reg_read(UC_X86_REG_EAX)&0xffffffff
    signed=eax if eax<0x80000000 else eax-0x100000000
    return {
        "eax":eax,"signed":signed,"eip":eip,"returned":eip==SENTINEL,
        "instructions":state["insns"],"atoi_calls":state["atoi_calls"],
        "atoi_input":state["atoi_input"],
    }


def main():
    print("StoneAge JSS SaUpdate generation-suffix helper emulation — R1")
    print("SCOPE|rva-0x2060|synthetic-filenames|atoi-stub|bounded-x86-emulation|derived-output-only")
    status,final,headers,data=get_bounded(
        replay_url({"timestamp":TIMESTAMP,"original":ORIGINAL}),timeout=20
    )
    sha=hashlib.sha256(data).hexdigest()
    print(f"FETCH|status={status}|bytes={len(data)}|sha256={sha}|final={clean(final)}")
    if sha!=KNOWN_SHA256:
        print(f"RESOLUTION|HASH_MISMATCH|expected={KNOWN_SHA256}")
        return

    layout=parse_pe_layout(data)
    image_base=pe_sections(data)["image_base"]
    print(
        f"FUNCTION|rva=0x{FUNC_RVA:x}|image_base=0x{image_base:x}|"
        f"atoi_iat_rva=0x{ATOI_IAT_RVA:x}"
    )
    successes=0
    failures=0
    for label,text,expected in CASES:
        try:
            result=emulate_case(data,layout,image_base,text)
        except Exception as exc:
            failures+=1
            print(
                f"CASE_ERROR|label={label}|input={clean(text)}|"
                f"kind={type(exc).__name__}|message={clean(exc)}"
            )
            continue
        match=result["returned"] and result["signed"]==expected
        successes+=int(match)
        failures+=int(not match)
        print(
            f"CASE|label={label}|input={clean(text)}|expected={expected}|"
            f"value={result['signed']}|eax=0x{result['eax']:x}|"
            f"atoi_calls={result['atoi_calls']}|atoi_input={clean(result['atoi_input'])}|"
            f"instructions={result['instructions']}|returned={int(result['returned'])}|"
            f"match={int(match)}"
        )

    print(
        f"RESOLUTION|GENERATION_SUFFIX_HELPER_EMULATED|successes={successes}|"
        f"failures={failures}|binary-not-committed"
    )


if __name__=="__main__":
    main()
