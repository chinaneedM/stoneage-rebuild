#!/usr/bin/env python3
"""Probe Wayback for five exact early-client-disc article image URLs.

The live collector article references five primary 2020-12 images on
shiqifabu.fszye.com that are currently connection-refused. Their exact leaf
filenames are now stable recovery tokens. This probe checks exact HTTP/HTTPS
CDX/availability and, only when an image replay exists, transiently hashes the
replayed image. No image bytes are committed.
"""
from __future__ import annotations
import hashlib,json,urllib.parse,urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
AVAIL="https://archive.org/wayback/available"
PATHS=(
 "/zb_users/upload/2020/12/20201218135732160827105240814.jpg",
 "/zb_users/upload/2020/12/20201218135732160827105231744.jpg",
 "/zb_users/upload/2020/12/20201218135733160827105385640.jpg",
 "/zb_users/upload/2020/12/20201218135734160827105460668.jpg",
 "/zb_users/upload/2020/12/20201218135734160827105464241.jpg",
)
HOST="shiqifabu.fszye.com"
SMZDM_SHA256="98ad75b6eb5fa5aca6fa7e37095bd207779321ea4991ccf0754117cfaf3884c3"

def clean(v,n=5000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=40,max_bytes=12*1024*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,image/*,*/*;q=0.3","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        if len(b)>max_bytes: raise ValueError(f"response-too-large:{len(b)}")
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b

def cdx_url(u):
    p=[("url",u),("matchType","exact"),("output","json"),
       ("fl","timestamp,original,statuscode,mimetype,digest,length"),
       ("from","2020"),("to","2026"),("limit","100")]
    return CDX+"?"+urllib.parse.urlencode(p)

def avail_url(u):
    return AVAIL+"?"+urllib.parse.urlencode({"url":u,"timestamp":"20201218"})

def cdx_rows(body):
    obj=json.loads(body.decode("utf-8"))
    if not isinstance(obj,list) or len(obj)<2:return ()
    h=obj[0]
    return tuple(dict(zip(h,r)) for r in obj[1:] if isinstance(r,list))

def main():
    print("StoneAge early collector primary-image archive probe — R1")
    print("SCOPE|five exact shiqifabu.fszye.com article-image URLs|Wayback exact CDX+availability+transient image hash|no-image-commit")
    errors=[];rows_total=0;replayed=0
    for idx,path in enumerate(PATHS,1):
        for scheme in ("http","https"):
            u=f"{scheme}://{HOST}{path}"
            try:
                st,final,h,b=fetch(cdx_url(u),max_bytes=2*1024*1024)
                rr=cdx_rows(b);rows_total+=len(rr)
                print(f"CDX|index={idx}|scheme={scheme}|status={st}|rows={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|url={clean(u)}")
                for r in rr:
                    print(f"CDX_ROW|index={idx}|scheme={scheme}|timestamp={clean(r.get('timestamp'))}|original={clean(r.get('original'))}|statuscode={clean(r.get('statuscode'))}|mimetype={clean(r.get('mimetype'))}|digest={clean(r.get('digest'))}|length={clean(r.get('length'))}")
            except Exception as e:
                errors.append((f"cdx:{idx}:{scheme}",type(e).__name__,str(e)))
            try:
                st,final,h,b=fetch(avail_url(u),max_bytes=512*1024)
                obj=json.loads(b.decode("utf-8"));snap=((obj.get("archived_snapshots") or {}).get("closest") or {})
                print(f"AVAIL|index={idx}|scheme={scheme}|status={st}|available={int(bool(snap.get('available')))}|timestamp={clean(snap.get('timestamp'))}|capture={clean(snap.get('url'))}|http_status={clean(snap.get('status'))}")
                cap=str(snap.get("url") or "")
                ts=str(snap.get("timestamp") or "")
                orig=str(snap.get("url") or "")
                if snap.get("available") and cap:
                    # Prefer raw replay using the original exact URL and capture timestamp.
                    replay=f"https://web.archive.org/web/{ts}id_/{u}" if ts else cap
                    try:
                        ist,ifinal,hh,bb=fetch(replay,max_bytes=12*1024*1024)
                        sha=hashlib.sha256(bb).hexdigest();replayed+=1
                        print(f"REPLAY|index={idx}|scheme={scheme}|status={ist}|bytes={len(bb)}|sha256={sha}|exact_smzdm_2.0={int(sha==SMZDM_SHA256)}|final={clean(ifinal)}")
                    except Exception as e:
                        errors.append((f"replay:{idx}:{scheme}",type(e).__name__,str(e)))
            except Exception as e:
                errors.append((f"avail:{idx}:{scheme}",type(e).__name__,str(e)))
    print(f"COUNT|target_images|{len(PATHS)}")
    print(f"COUNT|cdx_rows|{rows_total}")
    print(f"COUNT|images_replayed|{replayed}")
    for s,k,m in errors:
        print(f"ERROR|scope={clean(s)}|kind={clean(k)}|message={clean(m)}")
    print(f"COUNT|errors|{len(errors)}")
    if replayed:
        print("RESOLUTION|PRIMARY_COLLECTOR_IMAGES_RECOVERED_FROM_ARCHIVE|classify visible disc/version identifiers without treating photo bytes as client provenance")
    elif rows_total:
        print("RESOLUTION|PRIMARY_IMAGE_ARCHIVE_METADATA_ONLY|retain capture tokens; image body replay not recovered")
    elif errors:
        print("RESOLUTION|PRIMARY_IMAGE_ARCHIVE_SURFACE_INCOMPLETE|do not declare images unpreserved")
    else:
        print("RESOLUTION|NO_PRIMARY_IMAGE_ARCHIVE_ROW|tested exact Wayback surface exposes no capture for the five image URLs")
    print("EVIDENCE_BOUNDARY|archived photograph bytes establish only photographic evidence; they cannot establish disc filesystem, mastering, installer hash or historical client-byte identity.")

if __name__=="__main__":
    main()
