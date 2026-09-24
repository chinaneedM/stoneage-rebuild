#!/usr/bin/env python3
"""Deep derived-only analysis of the archived first-party JSS StoneAge launcher.

The launcher bytes are fetched transiently from the already-proven Wayback replay,
analysed in memory / temporary storage, and never committed. The report records
only structural metadata, resource summaries and bounded printable strings.
"""

from __future__ import annotations

import hashlib
import math
import re
import struct
import urllib.parse

from tools.stoneage_jss_launcher_archive_probe import (
    ORIGINAL,
    get_bounded,
    replay_url,
)
from tools.stoneage_tw10_technical_probe import pe_sections

TIMESTAMP="20010503013834"
KNOWN_SHA256="6795d9349168f77aa025d7c4ea05d005c5bbfe33dd4b227eb7731802fa7eb82b"
MAX_BYTES=1024*1024

RESOURCE_TYPES={
    1:"CURSOR",2:"BITMAP",3:"ICON",4:"MENU",5:"DIALOG",6:"STRING",7:"FONTDIR",
    8:"FONT",9:"ACCELERATOR",10:"RCDATA",11:"MESSAGETABLE",12:"GROUP_CURSOR",
    14:"GROUP_ICON",16:"VERSION",24:"MANIFEST",
}
PACKER_MARKERS=(
    b"UPX!",b"UPX0",b"UPX1",b"ASPack",b".aspack",b"PECompact",b"PEC2",
    b"Petite",b"FSG!",b"MEW",b"MPRESS",b"WWPACK",b"NSPack",b"nsp0",
)
ASCII_RE=re.compile(rb"[\x20-\x7e]{4,}")
UTF16_ASCII_RE=re.compile(rb"(?:[\x20-\x7e]\x00){4,}")


def clean(v,limit=1600):
    s=" ".join(str(v if v is not None else "").split())
    return "".join(c for c in s if c>=" " and c!="\x7f").replace("|","%7C")[:limit]


def entropy(data):
    if not data:
        return 0.0
    counts=[0]*256
    for b in data:
        counts[b]+=1
    n=len(data)
    return -sum((c/n)*math.log2(c/n) for c in counts if c)


def parse_pe_layout(data):
    if len(data)<0x40 or data[:2]!=b"MZ":
        raise ValueError("not MZ")
    pe=struct.unpack_from("<I",data,0x3c)[0]
    if pe+24>len(data) or data[pe:pe+4]!=b"PE\0\0":
        raise ValueError("not PE")
    machine,nsec,stamp,_,_,opt_size,_=struct.unpack_from("<HHIIIHH",data,pe+4)
    opt=pe+24
    magic=struct.unpack_from("<H",data,opt)[0]
    if magic!=0x10b:
        raise ValueError(f"unsupported PE magic {magic:#x}")
    dirs_count=struct.unpack_from("<I",data,opt+92)[0] if opt_size>=96 else 0
    dirs=[]
    dir_base=opt+96
    for i in range(min(dirs_count,16)):
        rva,size=struct.unpack_from("<II",data,dir_base+i*8)
        dirs.append((rva,size))
    sec_off=opt+opt_size
    secs=[]
    for i in range(nsec):
        off=sec_off+i*40
        raw_name=data[off:off+8].split(b"\0",1)[0]
        name=raw_name.decode("ascii","replace")
        vsize,vaddr,raw_size,raw_ptr=struct.unpack_from("<IIII",data,off+8)
        chars=struct.unpack_from("<I",data,off+36)[0]
        secs.append({
            "name":name,"vsize":vsize,"vaddr":vaddr,
            "raw_size":raw_size,"raw_ptr":raw_ptr,"chars":chars,
        })
    return {
        "pe_off":pe,"machine":machine,"timestamp":stamp,"opt_size":opt_size,
        "directories":dirs,"sections":secs,
    }


def rva_to_offset(layout,rva):
    for sec in layout["sections"]:
        span=max(sec["vsize"],sec["raw_size"])
        if sec["vaddr"]<=rva<sec["vaddr"]+span:
            return sec["raw_ptr"]+(rva-sec["vaddr"])
    return None


def read_resource_name(data,base_off,value):
    if not (value & 0x80000000):
        return str(value & 0xffff)
    rel=value & 0x7fffffff
    off=base_off+rel
    if off+2>len(data):
        return "INVALID_NAME"
    count=struct.unpack_from("<H",data,off)[0]
    raw=data[off+2:off+2+count*2]
    try:
        return raw.decode("utf-16le","replace")
    except Exception:
        return "INVALID_NAME"


def resource_entries(data):
    layout=parse_pe_layout(data)
    if len(layout["directories"])<=2:
        return []
    rva,size=layout["directories"][2]
    if not rva or not size:
        return []
    base_off=rva_to_offset(layout,rva)
    if base_off is None:
        return []

    out=[]
    seen=set()

    def walk(dir_rel,path,depth):
        if depth>4:
            return
        dir_off=base_off+dir_rel
        if dir_off+16>len(data):
            return
        named,ids=struct.unpack_from("<HH",data,dir_off+12)
        count=named+ids
        for idx in range(count):
            ent=dir_off+16+idx*8
            if ent+8>len(data):
                break
            nameval,target=struct.unpack_from("<II",data,ent)
            name=read_resource_name(data,base_off,nameval)
            is_dir=bool(target & 0x80000000)
            rel=target & 0x7fffffff
            next_path=path+(name,)
            key=(rel,is_dir,next_path)
            if key in seen:
                continue
            seen.add(key)
            if is_dir:
                walk(rel,next_path,depth+1)
                continue
            de=base_off+rel
            if de+16>len(data):
                continue
            data_rva,data_size,codepage,_=struct.unpack_from("<IIII",data,de)
            file_off=rva_to_offset(layout,data_rva)
            if file_off is None or file_off+data_size>len(data):
                blob=b""
            else:
                blob=data[file_off:file_off+data_size]
            out.append({
                "path":next_path,"rva":data_rva,"size":data_size,
                "codepage":codepage,"file_off":file_off,"blob":blob,
            })
    walk(0,(),0)
    return out


def resource_type(entry):
    if not entry["path"]:
        return "UNKNOWN"
    first=entry["path"][0]
    try:
        return RESOURCE_TYPES.get(int(first),f"TYPE_{first}")
    except ValueError:
        return first


def bounded_strings(blob,encoding,limit=80):
    regex=ASCII_RE if encoding=="ascii" else UTF16_ASCII_RE
    seen=set(); out=[]
    for match in regex.finditer(blob):
        try:
            value=match.group().decode("ascii" if encoding=="ascii" else "utf-16le")
        except Exception:
            continue
        if value not in seen:
            seen.add(value); out.append(value)
        if len(out)>=limit:
            break
    return tuple(out)


def magic(blob):
    if blob.startswith(b"MZ"): return "MZ"
    if blob.startswith(b"PK\x03\x04"): return "ZIP"
    if blob.startswith(b"MSCF"): return "CAB"
    if blob.startswith(b"\x89PNG\r\n\x1a\n"): return "PNG"
    if blob.startswith(b"BM"): return "BMP"
    return blob[:8].hex()


def main():
    print("StoneAge JSS archived launcher deep-structure probe — R1")
    print("SCOPE|first-party-archived-launcher|transient-bytes|derived-structural-metadata-only")
    print(f"CAPTURE|timestamp={TIMESTAMP}|original={ORIGINAL}")
    row={"timestamp":TIMESTAMP,"original":ORIGINAL}
    status,final,headers,data=get_bounded(replay_url(row),timeout=20)
    sha=hashlib.sha256(data).hexdigest()
    print(f"FETCH|status={status}|bytes={len(data)}|sha256={sha}|final={clean(final)}")
    if sha!=KNOWN_SHA256:
        print(f"RESOLUTION|HASH_MISMATCH|expected={KNOWN_SHA256}")
        return

    layout=parse_pe_layout(data)
    pe=pe_sections(data)
    max_raw=max((s["raw_ptr"]+s["raw_size"] for s in layout["sections"]),default=0)
    overlay=max(0,len(data)-max_raw)
    print(
        f"PE_LAYOUT|pe_offset={layout['pe_off']}|machine={layout['machine']}|"
        f"sections={len(layout['sections'])}|directories={len(layout['directories'])}|"
        f"overlay_bytes={overlay}"
    )

    for sec in layout["sections"]:
        start=sec["raw_ptr"]; end=min(len(data),start+sec["raw_size"])
        blob=data[start:end] if start<len(data) else b""
        ratio=(sec["vsize"]/sec["raw_size"]) if sec["raw_size"] else 0.0
        print(
            f"SECTION|name={clean(sec['name'])}|vsize={sec['vsize']}|raw_size={sec['raw_size']}|"
            f"raw_ptr={sec['raw_ptr']}|virtual_raw_ratio={ratio:.3f}|entropy={entropy(blob):.5f}|"
            f"sha256={hashlib.sha256(blob).hexdigest()}"
        )

    markers=[m.decode("ascii","replace") for m in PACKER_MARKERS if m.lower() in data.lower()]
    print(f"PACKER_MARKERS|count={len(markers)}|values={','.join(markers)}")

    entries=resource_entries(data)
    by_type={}
    embedded=[]
    for e in entries:
        typ=resource_type(e)
        by_type.setdefault(typ,[]).append(e)
        if e["blob"].startswith((b"MZ",b"PK\x03\x04",b"MSCF")):
            embedded.append((typ,e))

    print(f"RESOURCE_COUNT|entries={len(entries)}|types={len(by_type)}|embedded_payloads={len(embedded)}")
    for typ in sorted(by_type):
        items=by_type[typ]
        total=sum(x["size"] for x in items)
        print(f"RESOURCE_TYPE|type={clean(typ)}|count={len(items)}|total_bytes={total}")
        for e in items[:20]:
            path="/".join(e["path"])
            blob=e["blob"]
            print(
                f"RESOURCE|type={clean(typ)}|path={clean(path)}|size={e['size']}|"
                f"codepage={e['codepage']}|file_off={e['file_off']}|magic={magic(blob)}|"
                f"entropy={entropy(blob):.5f}|sha256={hashlib.sha256(blob).hexdigest() if blob else ''}"
            )

    # Version and manifest resources: retain only bounded printable tokens.
    for typ in ("VERSION","MANIFEST","RCDATA"):
        for idx,e in enumerate(by_type.get(typ,[])[:20]):
            for enc in ("ascii","utf16"):
                vals=bounded_strings(e["blob"],"ascii" if enc=="ascii" else "utf16",120)
                for val in vals:
                    print(f"RESOURCE_STRING|type={typ}|index={idx}|encoding={enc}|text={clean(val)}")

    for typ,e in embedded:
        print(
            f"EMBEDDED|type={clean(typ)}|path={clean('/'.join(e['path']))}|"
            f"size={e['size']}|magic={magic(e['blob'])}|sha256={hashlib.sha256(e['blob']).hexdigest()}"
        )

    # Whole-file UTF-16 strings can expose VS_VERSION_INFO even when resource parsing is partial.
    whole_utf16=bounded_strings(data,"utf16",250)
    print(f"WHOLE_UTF16|count={len(whole_utf16)}")
    for val in whole_utf16:
        if re.search(r"(?i)(version|stone|jss|japan|company|product|copyright|file|update|game)",val):
            print(f"UTF16_RELEVANT|text={clean(val)}")

    suspicious = (
        any(sec["raw_size"] and sec["vsize"] >= sec["raw_size"]*20 for sec in layout["sections"])
        or any(entropy(data[s["raw_ptr"]:s["raw_ptr"]+s["raw_size"]])>=7.2 for s in layout["sections"] if s["raw_size"])
    )
    print(
        "RESOLUTION|DEEP_STRUCTURE_ANALYZED|"
        f"compression_or_unpacking_indicators={int(suspicious)}|"
        f"resource_entries={len(entries)}|embedded_payloads={len(embedded)}|binary-not-committed"
    )


if __name__=="__main__":
    main()
