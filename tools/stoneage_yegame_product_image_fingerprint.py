#!/usr/bin/env python3
"""Transiently fingerprint the exact archived Yegame StoneAge product image.

The image body is fetched only in runner memory, hashed and structurally parsed,
then discarded. No image bytes are committed.
"""
from __future__ import annotations
import hashlib,struct,urllib.request

UA="stoneage-rebuild-archaeology/1.0"
TS="20010828031151"
ORIG="http://yegame.com:80/product_images/EN0ZGKJ0002.jpg"
URL=f"https://web.archive.org/web/{TS}id_/{ORIG}"
MAX=2*1024*1024

def jpeg_size(b):
    if len(b)<4 or b[:2]!=b"\xff\xd8": return None
    i=2
    sof={0xC0,0xC1,0xC2,0xC3,0xC5,0xC6,0xC7,0xC9,0xCA,0xCB,0xCD,0xCE,0xCF}
    while i+4<=len(b):
        if b[i]!=0xFF:
            i+=1; continue
        while i<len(b) and b[i]==0xFF:i+=1
        if i>=len(b):break
        marker=b[i]; i+=1
        if marker in (0xD8,0xD9) or 0xD0<=marker<=0xD7: continue
        if i+2>len(b):break
        seg=struct.unpack(">H",b[i:i+2])[0]
        if seg<2 or i+seg>len(b):break
        if marker in sof and seg>=7:
            h=struct.unpack(">H",b[i+3:i+5])[0]
            w=struct.unpack(">H",b[i+5:i+7])[0]
            comps=b[i+7] if i+7<len(b) else None
            return w,h,comps,marker
        i+=seg
    return None

def main():
    print("StoneAge Yegame EN0ZGKJ0002 archived product-image fingerprint — R1")
    print("SCOPE|single exact archived JPEG|transient fetch/hash/geometry only|image body not committed")
    req=urllib.request.Request(URL,headers={"User-Agent":UA,"Accept":"image/jpeg,*/*;q=0.1","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=60) as r:
        b=r.read(MAX+1)
        if len(b)>MAX: raise ValueError("response-too-large")
        ct=str(r.headers.get("Content-Type") or "")
        final=r.geturl()
        status=int(getattr(r,"status",r.getcode()))
    geom=jpeg_size(b)
    print(f"RESPONSE|status={status}|content_type={ct}|bytes={len(b)}|final={final}")
    print(f"HASH|sha256={hashlib.sha256(b).hexdigest()}|sha1={hashlib.sha1(b).hexdigest()}|md5={hashlib.md5(b).hexdigest()}")
    if geom:
        w,h,c,m=geom
        print(f"JPEG|valid=1|width={w}|height={h}|components={c}|sof_marker=0x{m:02x}")
    else:
        print("JPEG|valid=0")
    print(f"ARCHIVE_BINDING|timestamp={TS}|original={ORIG}")
    print("EVIDENCE_BOUNDARY|Only derived metadata is printed; raw historical image bytes are discarded and not committed.")

if __name__=="__main__":main()
