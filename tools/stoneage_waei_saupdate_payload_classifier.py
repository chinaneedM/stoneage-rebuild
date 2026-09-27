#!/usr/bin/env python3
"""Transient byte-level classifier for archived stoneage.waei.net sa_40.exe / sa_42.exe.

The two payloads were discovered by first-party CDX census. This tool fetches
only those exact archived executables into runner memory, emits hashes,
PE/container structure and bounded strings, then discards the bytes.
No executable payload is committed.
"""
from __future__ import annotations

import base64
import hashlib
import re
import struct
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
TARGETS=(
    ("sa40","20011031155747","http://stoneage.waei.net:80/saupdate/sa_40.exe","N2X37GUIMAQSSHG6C234TOXSEGJLVYZK"),
    ("sa42","20011206183120","http://stoneage.waei.net:80/saupdate/sa_42.exe","IWYPBI66JUCJMHGQUQ6D24BATU2QRFZE"),
)
MAX=8*1024*1024

KEYWORDS=(
    "stoneage","waei","saupdate","version","ver","patch","update",
    "data\\","data/","program files","石器","華義","华义",
    ".bin",".bmp",".spr",".txt",".dat",".ini",".exe",".dll",".cab",".zip",
    "http://","https://",
)

def clean(v,n=5000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(ts,orig):
    url=f"https://web.archive.org/web/{ts}id_/{orig}"
    req=urllib.request.Request(url,headers={
        "User-Agent":UA,
        "Accept":"application/octet-stream,*/*;q=0.1",
        "Accept-Encoding":"identity",
    })
    with urllib.request.urlopen(req,timeout=60) as r:
        body=r.read(MAX+1)
        if len(body)>MAX:
            raise ValueError(f"response-too-large:{len(body)}")
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),body

def sha1_b32(data):
    return base64.b32encode(hashlib.sha1(data).digest()).decode("ascii").rstrip("=")

def ascii_strings(data,minlen=5):
    pat=rb"[\x20-\x7e]{"+str(minlen).encode()+rb",}"
    return [m.group().decode("ascii","replace") for m in re.finditer(pat,data)]

def utf16le_strings(data,minlen=4):
    pat=(rb"(?:[\x20-\x7e]\x00){"+str(minlen).encode()+rb",}")
    return [m.group().decode("utf-16le","replace") for m in re.finditer(pat,data)]

def big5_runs(data,minlen=4):
    # Conservative printable ASCII + common Big5 lead/trail sequences.
    out=[]
    i=0
    while i<len(data):
        start=i; chars=[]; wide=0
        while i<len(data):
            b=data[i]
            if 0x20<=b<=0x7e:
                chars.append(bytes([b])); i+=1; continue
            if 0x81<=b<=0xfe and i+1<len(data):
                b2=data[i+1]
                if 0x40<=b2<=0x7e or 0xa1<=b2<=0xfe:
                    chars.append(data[i:i+2]); wide+=1; i+=2; continue
            break
        if i>start and len(chars)>=minlen and wide:
            raw=b"".join(chars)
            try:
                s=raw.decode("big5")
                if any("\u4e00"<=ch<="\u9fff" for ch in s):
                    out.append(s)
            except Exception:
                pass
        i=max(i+1,start+1)
    return out

def interesting(strings):
    seen=set(); out=[]
    for s in strings:
        low=s.lower()
        if any(k.lower() in low for k in KEYWORDS):
            v=clean(s,1200)
            if v and v not in seen:
                seen.add(v); out.append(v)
    return out[:120]

def pe_info(data):
    result={"is_mz":int(data[:2]==b"MZ")}
    if data[:2]!=b"MZ" or len(data)<0x40:
        return result
    peoff=struct.unpack_from("<I",data,0x3c)[0]
    result["pe_offset"]=peoff
    if peoff+24>len(data) or data[peoff:peoff+4]!=b"PE\0\0":
        result["is_pe"]=0
        return result
    result["is_pe"]=1
    machine,nsec,tstamp,ptrsym,nsym,opt_size,chars=struct.unpack_from("<HHIIIHH",data,peoff+4)
    result.update(machine=machine,sections=nsec,timestamp=tstamp,opt_size=opt_size,characteristics=chars)
    opt=peoff+24
    if opt+2<=len(data):
        magic=struct.unpack_from("<H",data,opt)[0]
        result["optional_magic"]=magic
        if magic==0x10b and opt+68<=len(data):
            result["image_base"]=struct.unpack_from("<I",data,opt+28)[0]
            result["entry_rva"]=struct.unpack_from("<I",data,opt+16)[0]
            result["section_alignment"]=struct.unpack_from("<I",data,opt+32)[0]
            result["file_alignment"]=struct.unpack_from("<I",data,opt+36)[0]
            result["subsystem"]=struct.unpack_from("<H",data,opt+68)[0] if opt+70<=len(data) else None
    secbase=opt+opt_size
    sections=[]
    maxraw=0
    for i in range(nsec):
        off=secbase+i*40
        if off+40>len(data): break
        name=data[off:off+8].split(b"\0",1)[0].decode("ascii","replace")
        vsize,vaddr,rsize,rptr=struct.unpack_from("<IIII",data,off+8)
        schar=struct.unpack_from("<I",data,off+36)[0]
        sections.append((name,vsize,vaddr,rsize,rptr,schar))
        maxraw=max(maxraw,rptr+rsize)
    result["section_rows"]=sections
    result["overlay_offset"]=maxraw
    result["overlay_size"]=max(0,len(data)-maxraw) if maxraw else 0
    return result

def sigs(data):
    checks=(
      ("zip-local",b"PK\x03\x04"),("zip-eocd",b"PK\x05\x06"),
      ("cab",b"MSCF"),("rar4",b"Rar!\x1a\x07\x00"),("rar5",b"Rar!\x1a\x07\x01\x00"),
      ("7z",b"7z\xbc\xaf\x27\x1c"),("gzip",b"\x1f\x8b"),
      ("upx0",b"UPX0"),("upx1",b"UPX1"),("upx!",b"UPX!"),
      ("nsis",b"Nullsoft"),("winrar-sfx",b"WinRAR"),
      ("installshield",b"InstallShield"),("wise",b"Wise Installation"),
    )
    return [(name,data.find(sig)) for name,sig in checks if data.find(sig)>=0]

def main():
    print("StoneAge Waei first-party sa_40/sa_42 transient classifier — R1")
    print("SCOPE|exact Wayback payload replay|hash+PE/container+bounded strings|no executable committed")
    blobs={}
    errors=[]
    for label,ts,orig,expected_b32 in TARGETS:
        try:
            st,final,h,b=fetch(ts,orig)
            blobs[label]=b
            s256=hashlib.sha256(b).hexdigest()
            s1=hashlib.sha1(b).hexdigest()
            md5=hashlib.md5(b).hexdigest()
            b32=sha1_b32(b)
            print(f"PAYLOAD|label={label}|status={st}|bytes={len(b)}|sha256={s256}|sha1={s1}|md5={md5}|sha1_b32={b32}|cdx_digest_match={int(b32==expected_b32)}|content_type={clean(h.get('Content-Type'))}|final={clean(final)}")
            info=pe_info(b)
            print("PE|label={}|is_mz={}|is_pe={}|pe_offset={}|machine={}|sections={}|timestamp={}|optional_magic={}|entry_rva={}|image_base={}|section_alignment={}|file_alignment={}|subsystem={}|overlay_offset={}|overlay_size={}".format(
                label,info.get("is_mz",0),info.get("is_pe",0),info.get("pe_offset",""),info.get("machine",""),
                info.get("sections",""),info.get("timestamp",""),info.get("optional_magic",""),info.get("entry_rva",""),
                info.get("image_base",""),info.get("section_alignment",""),info.get("file_alignment",""),
                info.get("subsystem",""),info.get("overlay_offset",""),info.get("overlay_size","")
            ))
            for name,vsize,vaddr,rsize,rptr,schar in info.get("section_rows",()):
                print(f"SECTION|label={label}|name={clean(name)}|virtual_size={vsize}|virtual_address={vaddr}|raw_size={rsize}|raw_ptr={rptr}|characteristics=0x{schar:08x}")
            for name,off in sigs(b):
                print(f"SIGNATURE|label={label}|kind={name}|offset={off}")
            all_strings=ascii_strings(b)+utf16le_strings(b)+big5_runs(b)
            ints=interesting(all_strings)
            print(f"STRING_COUNT|label={label}|interesting={len(ints)}")
            for s in ints:
                print(f"STRING|label={label}|text={clean(s,1400)}")
        except Exception as e:
            errors.append((label,type(e).__name__,str(e)))
            print(f"ERROR|label={label}|kind={type(e).__name__}|message={clean(e)}")

    if "sa40" in blobs and "sa42" in blobs:
        a=blobs["sa40"]; b=blobs["sa42"]
        prefix=0
        for x,y in zip(a,b):
            if x!=y: break
            prefix+=1
        suffix=0
        while suffix<min(len(a),len(b))-prefix and a[-1-suffix]==b[-1-suffix]:
            suffix+=1
        common=sum(1 for x,y in zip(a,b) if x==y)
        print(f"PAIR|left=sa40|right=sa42|left_bytes={len(a)}|right_bytes={len(b)}|same_offset_equal_bytes={common}|common_prefix={prefix}|common_suffix={suffix}")
    print(f"COUNT|errors|{len(errors)}")
    if not errors and len(blobs)==2:
        print("RESOLUTION|WAEI_FIRST_PARTY_UPDATE_BYTES_BOUND|classify embedded payload/file targets and historical version semantics next")
    elif blobs:
        print("RESOLUTION|PARTIAL_WAEI_UPDATE_BYTES|retry only failed exact payload")
    else:
        print("RESOLUTION|WAEI_UPDATE_REPLAY_FAILED|retain CDX metadata only")
    print("EVIDENCE_BOUNDARY|raw executable bytes are transient runner inputs only and are not written to the repository.")

if __name__=="__main__":
    main()
