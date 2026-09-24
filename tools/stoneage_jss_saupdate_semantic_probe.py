#!/usr/bin/env python3
"""Recover semantic metadata from the archived first-party JSS SaUpdate launcher.

This is a derived-only probe. The executable is fetched transiently and never
retained in the repository.
"""

from __future__ import annotations

import hashlib
import struct

from tools.stoneage_jss_launcher_archive_probe import ORIGINAL, get_bounded, replay_url
from tools.stoneage_jss_launcher_deep_probe import (
    KNOWN_SHA256,
    TIMESTAMP,
    parse_pe_layout,
    resource_entries,
    resource_type,
)

VERSION_SIGNATURE=0xFEEF04BD
SCN_CNT_CODE=0x00000020
SCN_CNT_INITIALIZED_DATA=0x00000040
SCN_CNT_UNINITIALIZED_DATA=0x00000080
SCN_MEM_EXECUTE=0x20000000
SCN_MEM_READ=0x40000000
SCN_MEM_WRITE=0x80000000


def clean(v,limit=1800):
    s=" ".join(str(v if v is not None else "").split())
    return "".join(c for c in s if c>=" " and c!="\x7f").replace("|","%7C")[:limit]


def version_tuple(ms,ls):
    return ((ms>>16)&0xffff,ms&0xffff,(ls>>16)&0xffff,ls&0xffff)


def find_fixed_file_info(blob):
    sig=struct.pack("<I",VERSION_SIGNATURE)
    pos=blob.find(sig)
    if pos<0 or pos+52>len(blob):
        return None
    fields=struct.unpack_from("<13I",blob,pos)
    if fields[0]!=VERSION_SIGNATURE:
        return None
    return {
        "offset":pos,
        "struct_version":fields[1],
        "file_version_ms":fields[2],
        "file_version_ls":fields[3],
        "product_version_ms":fields[4],
        "product_version_ls":fields[5],
        "file_flags_mask":fields[6],
        "file_flags":fields[7],
        "file_os":fields[8],
        "file_type":fields[9],
        "file_subtype":fields[10],
        "file_date_ms":fields[11],
        "file_date_ls":fields[12],
    }


def allowed_text_char(ch):
    cp=ord(ch)
    return (
        0x20<=cp<=0x7e
        or 0x00a0<=cp<=0x00ff
        or 0x3000<=cp<=0x30ff
        or 0x3400<=cp<=0x4dbf
        or 0x4e00<=cp<=0x9fff
        or 0xff00<=cp<=0xffef
    )


def utf16_runs(blob,min_chars=2,limit=300):
    out=[]; seen=set(); current=[]
    # Version/dialog/string resources are WORD-aligned; inspect both parity
    # streams because a nested field can still begin on either file parity.
    for parity in (0,1):
        current=[]
        for off in range(parity,len(blob)-1,2):
            code=blob[off] | (blob[off+1]<<8)
            if code==0:
                if len(current)>=min_chars:
                    s="".join(current)
                    if s not in seen:
                        seen.add(s); out.append(s)
                        if len(out)>=limit: return tuple(out)
                current=[]
                continue
            ch=chr(code)
            if allowed_text_char(ch):
                current.append(ch)
            else:
                if len(current)>=min_chars:
                    s="".join(current)
                    if s not in seen:
                        seen.add(s); out.append(s)
                        if len(out)>=limit: return tuple(out)
                current=[]
        if len(current)>=min_chars:
            s="".join(current)
            if s not in seen:
                seen.add(s); out.append(s)
                if len(out)>=limit: return tuple(out)
    return tuple(out)


def string_table_values(blob,block_id):
    values=[]
    off=0
    base=(block_id-1)*16
    for index in range(16):
        if off+2>len(blob):
            break
        count=struct.unpack_from("<H",blob,off)[0]
        off+=2
        raw=blob[off:off+count*2]
        off+=count*2
        if not count:
            continue
        text=raw.decode("utf-16le","replace")
        values.append((base+index,text))
    return tuple(values)


def section_flags(chars):
    names=[]
    for bit,name in (
        (SCN_CNT_CODE,"CODE"),
        (SCN_CNT_INITIALIZED_DATA,"INIT_DATA"),
        (SCN_CNT_UNINITIALIZED_DATA,"UNINIT_DATA"),
        (SCN_MEM_EXECUTE,"EXECUTE"),
        (SCN_MEM_READ,"READ"),
        (SCN_MEM_WRITE,"WRITE"),
    ):
        if chars & bit:
            names.append(name)
    return tuple(names)


def main():
    print("StoneAge JSS SaUpdate semantic probe — R1")
    print("SCOPE|archived-first-party-executable|version+ui+section-semantics|derived-only|binary-not-committed")

    status,final,headers,data=get_bounded(
        replay_url({"timestamp":TIMESTAMP,"original":ORIGINAL}),
        timeout=20,
    )
    sha=hashlib.sha256(data).hexdigest()
    print(f"FETCH|status={status}|bytes={len(data)}|sha256={sha}|final={clean(final)}")
    if sha!=KNOWN_SHA256:
        print(f"RESOLUTION|HASH_MISMATCH|expected={KNOWN_SHA256}")
        return

    layout=parse_pe_layout(data)
    for sec in layout["sections"]:
        zero_fill=max(0,sec["vsize"]-sec["raw_size"])
        print(
            f"SECTION_ROLE|name={clean(sec['name'])}|chars=0x{sec['chars']:08x}|"
            f"flags={','.join(section_flags(sec['chars']))}|raw_size={sec['raw_size']}|"
            f"virtual_size={sec['vsize']}|zero_fill_tail={zero_fill}"
        )

    entries=resource_entries(data)
    version_entries=[e for e in entries if resource_type(e)=="VERSION"]
    dialog_entries=[e for e in entries if resource_type(e)=="DIALOG"]
    string_entries=[e for e in entries if resource_type(e)=="STRING"]

    for idx,e in enumerate(version_entries):
        ffi=find_fixed_file_info(e["blob"])
        print(f"VERSION_RESOURCE|index={idx}|size={e['size']}|fixed_info={int(ffi is not None)}")
        if ffi:
            fv=version_tuple(ffi["file_version_ms"],ffi["file_version_ls"])
            pv=version_tuple(ffi["product_version_ms"],ffi["product_version_ls"])
            print(
                f"FIXED_VERSION|file={'.'.join(map(str,fv))}|product={'.'.join(map(str,pv))}|"
                f"flags_mask=0x{ffi['file_flags_mask']:08x}|flags=0x{ffi['file_flags']:08x}|"
                f"os=0x{ffi['file_os']:08x}|type=0x{ffi['file_type']:08x}|"
                f"subtype=0x{ffi['file_subtype']:08x}"
            )
        for value in utf16_runs(e["blob"],2,250):
            print(f"VERSION_TEXT|index={idx}|text={clean(value)}")

    for idx,e in enumerate(dialog_entries):
        vals=utf16_runs(e["blob"],2,200)
        print(f"DIALOG_TEXT_COUNT|index={idx}|count={len(vals)}")
        for value in vals:
            print(f"DIALOG_TEXT|index={idx}|text={clean(value)}")

    for idx,e in enumerate(string_entries):
        try:
            block_id=int(e["path"][1])
        except Exception:
            block_id=0
        vals=string_table_values(e["blob"],block_id) if block_id else ()
        print(f"STRING_TABLE|index={idx}|block={block_id}|values={len(vals)}")
        for sid,value in vals:
            print(f"STRING_VALUE|id={sid}|text={clean(value)}")

    huge_zero_fill=[
        sec for sec in layout["sections"]
        if sec["name"]==".data" and sec["vsize"]>sec["raw_size"]*100
    ]
    known_packer_names=any(
        sec["name"].upper().startswith(("UPX","ASPACK","PEC","MPRESS","FSG"))
        for sec in layout["sections"]
    )
    print(
        "PACKING_BOUNDARY|"
        f"huge_data_zero_fill={int(bool(huge_zero_fill))}|known_packer_section_names={int(known_packer_names)}|"
        "interpretation=large-zero-fill-data-alone-is-not-packer-proof"
    )
    print("RESOLUTION|SAUPDATE_IDENTITY_REFINED|version-and-ui-metadata-derived|binary-not-committed")


if __name__=="__main__":
    main()
