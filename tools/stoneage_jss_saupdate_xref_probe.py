#!/usr/bin/env python3
"""Derived cross-reference analysis for the archived JSS SaUpdate executable.

No disassembly text or executable bytes are retained. The probe maps selected
first-party strings and import-address-table entries to code-reference addresses,
then emits only structural/API summaries.
"""

from __future__ import annotations

import hashlib
import struct

from tools.stoneage_jss_launcher_archive_probe import ORIGINAL, get_bounded, replay_url
from tools.stoneage_jss_launcher_deep_probe import KNOWN_SHA256, TIMESTAMP, parse_pe_layout
from tools.stoneage_tw10_technical_probe import pe_sections

DIR_NAMES=(
    "EXPORT","IMPORT","RESOURCE","EXCEPTION","SECURITY","BASERELOC","DEBUG","ARCHITECTURE",
    "GLOBALPTR","TLS","LOAD_CONFIG","BOUND_IMPORT","IAT","DELAY_IMPORT","CLR","RESERVED",
)
TARGET_STRINGS=(
    b"update.gamersdream.ne.jp",
    b"/~stoneage/newest.txt",
    b"/~stoneage/%s",
    b"data\\download\\%s",
    b"(cksum:%u : File : %s)",
    b"sa_%d.exe",
    b"updated",
    b"MFC42.DLL",
)
DYNAMIC_API_TOKENS=(
    b"WSAStartup",b"WSACleanup",b"socket",b"connect",b"recv",b"send",
    b"gethostbyname",b"inet_addr",b"LoadLibrary",b"GetProcAddress",
)


def clean(v,limit=1200):
    s=" ".join(str(v if v is not None else "").split())
    return "".join(c for c in s if c>=" " and c!="\x7f").replace("|","%7C")[:limit]


def rva_to_offset(layout,rva):
    for sec in layout["sections"]:
        span=max(sec["vsize"],sec["raw_size"])
        if sec["vaddr"]<=rva<sec["vaddr"]+span:
            return sec["raw_ptr"]+(rva-sec["vaddr"])
    return None


def offset_to_rva(layout,off):
    for sec in layout["sections"]:
        if sec["raw_ptr"]<=off<sec["raw_ptr"]+sec["raw_size"]:
            return sec["vaddr"]+(off-sec["raw_ptr"])
    return None


def read_cstring(data,off,limit=512):
    if off is None or off<0 or off>=len(data):
        return ""
    end=data.find(b"\0",off,min(len(data),off+limit))
    if end<0:
        end=min(len(data),off+limit)
    return data[off:end].decode("ascii","replace")


def parse_imports(data,layout,image_base):
    dirs=layout["directories"]
    if len(dirs)<=1 or not dirs[1][0]:
        return {}
    imp_rva,_=dirs[1]
    off=rva_to_offset(layout,imp_rva)
    if off is None:
        return {}
    out={}
    for _ in range(256):
        if off+20>len(data):
            break
        oft,stamp,chain,name_rva,ft=struct.unpack_from("<IIIII",data,off)
        off+=20
        if not any((oft,stamp,chain,name_rva,ft)):
            break
        dll=read_cstring(data,rva_to_offset(layout,name_rva))
        thunk_rva=oft or ft
        thunk_off=rva_to_offset(layout,thunk_rva)
        if thunk_off is None:
            continue
        for idx in range(4096):
            p=thunk_off+idx*4
            if p+4>len(data):
                break
            value=struct.unpack_from("<I",data,p)[0]
            if value==0:
                break
            if value & 0x80000000:
                name=f"ordinal:{value&0xffff}"
            else:
                ibn=rva_to_offset(layout,value)
                if ibn is None or ibn+2>len(data):
                    name="invalid"
                else:
                    name=read_cstring(data,ibn+2)
            iat_va=image_base+ft+idx*4
            out[iat_va]=(dll,name)
    return out


def directory_summary(layout):
    rows=[]
    for idx,(rva,size) in enumerate(layout["directories"]):
        if rva or size:
            rows.append((idx,DIR_NAMES[idx] if idx<len(DIR_NAMES) else str(idx),rva,size))
    return tuple(rows)


def section_blob(data,sec):
    start=sec["raw_ptr"]; end=min(len(data),start+sec["raw_size"])
    return data[start:end]


def find_string_locations(data,layout,token):
    out=[]
    start=0
    while True:
        off=data.find(token,start)
        if off<0:
            break
        rva=offset_to_rva(layout,off)
        out.append((off,rva))
        start=off+1
    return tuple(out)


def find_va_refs(data,layout,image_base,target_rva):
    if target_rva is None:
        return ()
    needle=struct.pack("<I",image_base+target_rva)
    out=[]
    for sec in layout["sections"]:
        if not (sec["chars"] & 0x20000000):  # executable
            continue
        blob=section_blob(data,sec)
        start=0
        while True:
            pos=blob.find(needle,start)
            if pos<0:
                break
            out.append(sec["vaddr"]+pos)
            start=pos+1
    return tuple(out)


def import_calls_near(data,layout,image_base,iat_map,center_rva,radius=320):
    calls=set()
    for sec in layout["sections"]:
        if not (sec["vaddr"]<=center_rva<sec["vaddr"]+max(sec["vsize"],sec["raw_size"])):
            continue
        rel=center_rva-sec["vaddr"]
        blob=section_blob(data,sec)
        lo=max(0,rel-radius); hi=min(len(blob),rel+radius)
        window=blob[lo:hi]
        # FF 15 [absolute IAT address] = CALL dword ptr [addr] on x86.
        for pos in range(0,max(0,len(window)-6)):
            if window[pos:pos+2]!=b"\xff\x15":
                continue
            addr=struct.unpack_from("<I",window,pos+2)[0]
            if addr in iat_map:
                calls.add(iat_map[addr])
    return tuple(sorted(calls))


def dynamic_token_hits(data):
    out=[]
    lower=data.lower()
    for token in DYNAMIC_API_TOKENS:
        pos=lower.find(token.lower())
        if pos>=0:
            out.append((token.decode("ascii"),pos))
    return tuple(out)


def main():
    print("StoneAge JSS SaUpdate xref/import probe — R1")
    print("SCOPE|selected-string-xrefs+import-directories+nearby-IAT-calls|derived-only|no-disassembly-retained")

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
    for idx,name,rva,size in directory_summary(layout):
        print(f"DIRECTORY|index={idx}|name={name}|rva=0x{rva:x}|size={size}")

    iat=parse_imports(data,layout,image_base)
    dlls=sorted({dll for dll,_ in iat.values()})
    print(f"IMPORT_MAP|entries={len(iat)}|dlls={len(dlls)}|values={','.join(dlls)}")
    for dll in dlls:
        funcs=sorted(name for d,name in iat.values() if d==dll)
        print(f"IMPORT_DLL|dll={clean(dll)}|count={len(funcs)}|functions={','.join(clean(x) for x in funcs)}")

    dyn=dynamic_token_hits(data)
    print(f"DYNAMIC_API_STRING_HITS|count={len(dyn)}")
    for name,off in dyn:
        print(f"DYNAMIC_API_STRING|name={name}|file_off={off}")

    total_refs=0
    for token in TARGET_STRINGS:
        label=token.decode("ascii","replace")
        locs=find_string_locations(data,layout,token)
        print(f"STRING_TARGET|text={clean(label)}|locations={len(locs)}")
        for file_off,rva in locs:
            refs=find_va_refs(data,layout,image_base,rva)
            total_refs+=len(refs)
            print(
                f"STRING_LOCATION|text={clean(label)}|file_off={file_off}|"
                f"rva={'' if rva is None else f'0x{rva:x}'}|xref_count={len(refs)}"
            )
            for ref in refs:
                nearby=import_calls_near(data,layout,image_base,iat,ref)
                apis=";".join(f"{dll}!{name}" for dll,name in nearby)
                print(f"XREF|text={clean(label)}|code_rva=0x{ref:x}|nearby_direct_imports={clean(apis)}")

    delay_present=any(idx==13 for idx,_,_,_ in directory_summary(layout))
    print(
        "RESOLUTION|XREF_MAP_DERIVED|"
        f"selected_string_refs={total_refs}|delay_import_directory={int(delay_present)}|"
        f"dynamic_api_name_strings={len(dyn)}|binary-not-committed"
    )


if __name__=="__main__":
    main()
