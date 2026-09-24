#!/usr/bin/env python3
"""Derive the JSS SaUpdate HTTP/update call topology without retaining disassembly.

The MFC42 ordinal names below are a deliberately small derived subset of the
Visual C++ 6.0 MFC42.DEF export table, pinned to the public preservation blob
sha 3fb0685b8c2fe98932d3442d4fa0f9da8d69ccec. The full DEF is not vendored.
"""

from __future__ import annotations

import hashlib
import struct

from tools.stoneage_jss_launcher_archive_probe import ORIGINAL, get_bounded, replay_url
from tools.stoneage_jss_launcher_deep_probe import KNOWN_SHA256, TIMESTAMP, parse_pe_layout
from tools.stoneage_jss_saupdate_xref_probe import (
    TARGET_STRINGS,
    find_string_locations,
    find_va_refs,
    parse_imports,
    section_blob,
)
from tools.stoneage_tw10_technical_probe import pe_sections

VC6_MFC42_DEF_BLOB_SHA="3fb0685b8c2fe98932d3442d4fa0f9da8d69ccec"
VC6_MFC42_DEF_SOURCE="isledecomp/MSVC600-8168:VC98/MFC/SRC/PLATFORM/MFC42.DEF"
MFC_NETWORK_ORDINALS={
    389:"CInternetSession::CInternetSession",
    690:"CInternetSession::~CInternetSession",
    1247:"AfxSocketInit",
    1988:"CInternetSession::Close",
    3229:"CInternetSession::GetHttpConnection",
    5204:"CHttpConnection::OpenRequest",
    5356:"CHttpFile::QueryInfoStatusCode",
    5808:"CHttpFile::SendRequest",
}


def clean(v,limit=1200):
    s=" ".join(str(v if v is not None else "").split())
    return "".join(c for c in s if c>=" " and c!="\x7f").replace("|","%7C")[:limit]


def executable_sections(layout):
    return [sec for sec in layout["sections"] if sec["chars"] & 0x20000000]


def import_thunks(data,layout,iat_map):
    """Map x86 FF 25 absolute-IAT jump thunk RVA -> import tuple."""
    out={}
    for sec in executable_sections(layout):
        blob=section_blob(data,sec)
        for pos in range(max(0,len(blob)-6)):
            if blob[pos:pos+2]!=b"\xff\x25":
                continue
            addr=struct.unpack_from("<I",blob,pos+2)[0]
            target=iat_map.get(addr)
            if target:
                out[sec["vaddr"]+pos]=target
    return out


def import_call_sites(data,layout,iat_map,thunks):
    """Return (call_rva,dll,name,mode) for direct FF15 and E8-to-thunk calls."""
    out=[]
    seen=set()
    for sec in executable_sections(layout):
        blob=section_blob(data,sec)
        base=sec["vaddr"]
        for pos in range(len(blob)):
            # call dword ptr [absolute IAT]
            if pos+6<=len(blob) and blob[pos:pos+2]==b"\xff\x15":
                addr=struct.unpack_from("<I",blob,pos+2)[0]
                target=iat_map.get(addr)
                if target:
                    rec=(base+pos,target[0],target[1],"ff15")
                    if rec not in seen:
                        seen.add(rec); out.append(rec)
            # direct near call to linker import thunk
            if pos+5<=len(blob) and blob[pos]==0xe8:
                rel=struct.unpack_from("<i",blob,pos+1)[0]
                target_rva=base+pos+5+rel
                target=thunks.get(target_rva)
                if target:
                    rec=(base+pos,target[0],target[1],"e8-thunk")
                    if rec not in seen:
                        seen.add(rec); out.append(rec)
    return tuple(sorted(out))


def local_call_sites(data,layout):
    """Return direct E8 calls whose targets remain inside executable sections."""
    ranges=[
        (sec["vaddr"],sec["vaddr"]+max(sec["vsize"],sec["raw_size"]))
        for sec in executable_sections(layout)
    ]
    out=[]
    for sec in executable_sections(layout):
        blob=section_blob(data,sec)
        base=sec["vaddr"]
        for pos in range(max(0,len(blob)-5)):
            if blob[pos]!=0xe8:
                continue
            rel=struct.unpack_from("<i",blob,pos+1)[0]
            target=base+pos+5+rel
            if any(lo<=target<hi for lo,hi in ranges):
                out.append((base+pos,target))
    return tuple(sorted(set(out)))


def mapped_name(dll,name):
    if dll.lower()=="mfc42.dll" and name.startswith("ordinal:"):
        try:
            ordinal=int(name.split(":",1)[1])
        except ValueError:
            return name
        return MFC_NETWORK_ORDINALS.get(ordinal,name)
    return name


def network_call(call):
    _,dll,name,_=call
    if dll.lower()!="mfc42.dll":
        return False
    try:
        ordinal=int(name.split(":",1)[1])
    except Exception:
        return False
    return ordinal in MFC_NETWORK_ORDINALS


def main():
    print("StoneAge JSS SaUpdate HTTP-flow probe — R1")
    print("SCOPE|string-xrefs+IAT-thunks+selected-VC6-MFC42-ordinal-map|derived-only|no-disassembly-retained")
    print(f"MFC42_DEF|source={VC6_MFC42_DEF_SOURCE}|blob_sha={VC6_MFC42_DEF_BLOB_SHA}|vendored=0")

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
    iat=parse_imports(data,layout,pe["image_base"])
    thunks=import_thunks(data,layout,iat)
    calls=import_call_sites(data,layout,iat,thunks)
    network=[call for call in calls if network_call(call)]

    print(f"COUNT|iat_entries|{len(iat)}")
    print(f"COUNT|import_thunks|{len(thunks)}")
    print(f"COUNT|import_call_sites|{len(calls)}")
    print(f"COUNT|mapped_mfc_network_calls|{len(network)}")
    local_calls=local_call_sites(data,layout)
    print(f"COUNT|local_call_sites|{len(local_calls)}")

    # Summarize imported network methods and exact call RVAs.
    grouped={}
    for rva,dll,name,mode in network:
        try:
            ordinal=int(name.split(":",1)[1])
        except Exception:
            continue
        key=(ordinal,MFC_NETWORK_ORDINALS[ordinal])
        grouped.setdefault(key,[]).append((rva,mode))
    for (ordinal,symbol),sites in sorted(grouped.items()):
        encoded=",".join(f"0x{rva:x}:{mode}" for rva,mode in sites)
        print(f"NETWORK_IMPORT|ordinal={ordinal}|symbol={clean(symbol)}|calls={len(sites)}|sites={encoded}")

    string_refs=[]
    for token in TARGET_STRINGS:
        label=token.decode("ascii","replace")
        for _,string_rva in find_string_locations(data,layout,token):
            for xref in find_va_refs(data,layout,pe["image_base"],string_rva):
                string_refs.append((label,xref))

    # Associate every selected string xref with imported calls within +/- 0x800 RVA.
    for label,xref in sorted(string_refs,key=lambda x:x[1]):
        nearby=[]
        for rva,dll,name,mode in calls:
            delta=rva-xref
            if abs(delta)<=0x800:
                nearby.append((abs(delta),delta,rva,dll,mapped_name(dll,name),mode,name))
        nearby.sort()
        # emit at most 24 closest calls to bound the report
        print(f"FLOW_ANCHOR|string={clean(label)}|xref=0x{xref:x}|nearby_calls={len(nearby)}")
        for _,delta,rva,dll,symbol,mode,raw_name in nearby[:24]:
            print(
                f"FLOW_CALL|string={clean(label)}|xref=0x{xref:x}|call=0x{rva:x}|delta={delta}|"
                f"dll={clean(dll)}|symbol={clean(symbol)}|raw={clean(raw_name)}|mode={mode}"
            )

    # Local-call topology: expose only RVA edges, never instruction text.
    network_lo=(min((rva for rva,_,_,_ in network),default=0)-0x300)
    network_hi=(max((rva for rva,_,_,_ in network),default=0)+0x300)
    if network:
        for site,target in local_calls:
            if network_lo<=target<=network_hi:
                print(f"NETWORK_REGION_CALLER|site=0x{site:x}|target=0x{target:x}")
    for label,xref in sorted(string_refs,key=lambda x:x[1]):
        edges=[
            (site,target) for site,target in local_calls
            if abs(site-xref)<=0x300
        ]
        print(f"LOCAL_FLOW_ANCHOR|string={clean(label)}|xref=0x{xref:x}|local_calls={len(edges)}")
        for site,target in edges[:40]:
            relation="network-region" if network and network_lo<=target<=network_hi else "local"
            print(
                f"LOCAL_FLOW_CALL|string={clean(label)}|xref=0x{xref:x}|site=0x{site:x}|"
                f"target=0x{target:x}|relation={relation}"
            )

    # Strong topology facts that do not require exact function-boundary recovery.
    manifest_refs=[rva for label,rva in string_refs if label=="/~stoneage/newest.txt"]
    payload_refs=[rva for label,rva in string_refs if label=="/~stoneage/%s"]
    print(
        "RESOLUTION|HTTP_TOPOLOGY_DERIVED|"
        f"manifest_xrefs={len(manifest_refs)}|payload_xrefs={len(payload_refs)}|"
        f"mapped_network_methods={len(grouped)}|binary-not-committed"
    )


if __name__=="__main__":
    main()
