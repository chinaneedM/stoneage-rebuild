#!/usr/bin/env python3
"""Recover only derived byte metadata for Waei's archived spr_1.bin.

The archived payload is fetched transiently in the runner, hashed, classified,
then discarded. Raw bytes are never committed.
"""
from __future__ import annotations
import base64, hashlib, json, math, urllib.parse, urllib.request
from collections import Counter

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
ORIGINAL="http://www7.waei.net:80/download/file/%AD%D7%B8%C9%B5%7b%A6%A1/spr_1.bin"
MAX_BYTES=16*1024*1024
TW10_SIZE=2889630
TW10_SHA256="53d5b2d40453a30fd1569637ebf0db7b3010542b00970ec83af0295a3b3ae31a"

def fetch(url,timeout=60,max_bytes=MAX_BYTES):
    req=urllib.request.Request(url,headers={
        "User-Agent":UA,
        "Accept":"application/octet-stream,*/*;q=0.1",
        "Accept-Encoding":"identity",
    })
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        if len(b)>max_bytes:
            raise ValueError(f"response-too-large:{len(b)}")
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b

def cdx_url():
    params=[
        ("url",ORIGINAL),("matchType","exact"),("output","json"),
        ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
        ("from","2000"),("to","2002"),("filter","statuscode:200"),("limit","100"),
    ]
    return CDX+"?"+urllib.parse.urlencode(params)

def rows(body):
    obj=json.loads(body.decode("utf-8"))
    if not isinstance(obj,list) or len(obj)<2:return ()
    head=obj[0]
    return tuple(dict(zip(head,r)) for r in obj[1:] if isinstance(r,list))

def replay(ts,orig):
    return f"https://web.archive.org/web/{ts}id_/{orig}"

def sha1b32(data):
    return base64.b32encode(hashlib.sha1(data).digest()).decode("ascii").rstrip("=")

def entropy(data):
    if not data:return 0.0
    c=Counter(data);n=len(data)
    return -sum((v/n)*math.log2(v/n) for v in c.values())

def looks_html(data,headers):
    ct=str(headers.get("Content-Type") or headers.get("content-type") or "").lower()
    head=data[:512].lstrip().lower()
    return ("text/html" in ct) or head.startswith(b"<html") or b"<!doctype html" in head

def main():
    print("StoneAge Waei archived spr_1.bin byte-metadata probe — R2")
    print("SCOPE|transient archived payload<=16MiB|derived hashes/size only|raw bytes not committed")
    st,final,h,b=fetch(cdx_url(),max_bytes=2*1024*1024)
    rr=rows(b)
    print(f"CDX|status={st}|rows={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={final}")
    if not rr:
        print("RESOLUTION|NO_CDX_CAPTURE")
        return
    r=sorted(rr,key=lambda x:str(x.get("timestamp") or ""))[0]
    ts=str(r.get("timestamp") or "")
    orig=str(r.get("original") or ORIGINAL)
    print("CAPTURE|timestamp={}|cdx_length={}|cdx_digest={}|mime={}|original={}".format(
        ts,r.get("length",""),r.get("digest",""),r.get("mimetype",""),orig
    ))
    st,final,h,data=fetch(replay(ts,orig),timeout=90,max_bytes=MAX_BYTES)
    s256=hashlib.sha256(data).hexdigest()
    s1=hashlib.sha1(data).hexdigest()
    b32=sha1b32(data)
    md5=hashlib.md5(data).hexdigest()
    html=int(looks_html(data,h))
    print(
        "PAYLOAD|status={}|bytes={}|sha256={}|sha1={}|sha1_base32={}|md5={}|"
        "cdx_digest_match={}|entropy={:.6f}|looks_html={}|content_type={}|"
        "head32={}|tail32={}|final={}".format(
            st,len(data),s256,s1,b32,md5,
            int(bool(r.get("digest")) and b32==str(r.get("digest"))),
            entropy(data),html,str(h.get("Content-Type") or h.get("content-type") or ""),
            data[:32].hex(),data[-32:].hex(),final
        )
    )
    print(f"COMPARE_TW10|size_expected={TW10_SIZE}|size_match={int(len(data)==TW10_SIZE)}|sha256_expected={TW10_SHA256}|sha256_match={int(s256==TW10_SHA256)}")
    if html:
        print("RESOLUTION|REPLAY_NOT_BINARY|archive replay returned HTML; do not classify payload")
    elif s256==TW10_SHA256:
        print("RESOLUTION|BYTE_IDENTICAL_TO_TW10_SPR1|strong cross-regional resource identity")
    else:
        print("RESOLUTION|VALID_BINARY_DIFFERENT_FROM_TW10_SPR1|retain as independent archived Waei resource artifact pending title association")
    print("EVIDENCE_BOUNDARY|Even a valid binary at this URL requires independent title/download-page association before promotion to StoneAge-specific official patch provenance.")

if __name__=="__main__":
    main()
