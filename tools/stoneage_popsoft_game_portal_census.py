#!/usr/bin/env python3
"""Census the source-grounded game.popsoft.com.cn launch-window archive.

Jinghe/Yegame's archived business page directly links to
http://game.popsoft.com.cn/. This probe checks that exact historical game
portal across the Mainland StoneAge test/launch window for StoneAge/download
URL topology. CDX metadata only; no page or payload body is downloaded.
"""
from __future__ import annotations
import collections,hashlib,json,re,urllib.parse,urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
FROM="20001101"; TO="20010228"
FIELDS="timestamp,original,statuscode,mimetype,digest,length,redirect"
TARGETS=(
 ("host","http://game.popsoft.com.cn/","prefix"),
 ("host80","http://game.popsoft.com.cn:80/","prefix"),
)
BINARY=(".exe",".zip",".rar",".cab",".arj",".lzh",".7z",".iso",".bin",".cue")
HINTS=("stoneage","stone_age","stone-age","shiqi","石器","download","down","demo","trial","test","beta","client","setup","ftp")

def clean(v,n=7000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=75,max_bytes=32*1024*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,*/*;q=0.2","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        if len(b)>max_bytes:raise ValueError("response-too-large")
        return int(getattr(r,"status",r.getcode())),r.geturl(),b

def cdx_url(url,match):
    p=[("url",url),("matchType",match),("output","json"),("fl",FIELDS),
       ("from",FROM),("to",TO),("filter","statuscode:200"),("limit","50000"),("collapse","urlkey")]
    return CDX+"?"+urllib.parse.urlencode(p)

def parse(b):
    o=json.loads(b.decode("utf-8"))
    if not isinstance(o,list) or len(o)<2:return ()
    h=o[0];return tuple(dict(zip(h,r)) for r in o[1:] if isinstance(r,list))

def decoded_url(u):return urllib.parse.unquote_plus(str(u or "")).lower()
def is_binary(u):return urllib.parse.urlsplit(decoded_url(u)).path.endswith(BINARY)
def hint_score(u):
    s=decoded_url(u)
    return sum(1 for h in HINTS if h in s)
def ext(u):
    p=urllib.parse.urlsplit(decoded_url(u)).path
    m=re.search(r"(\.[a-z0-9]{1,8})$",p)
    return m.group(1) if m else ""

def main():
    print("StoneAge Popsoft game-portal launch-window CDX census — R1")
    print(f"SOURCE_CHAIN|archived Jinghe/Yegame business page -> http://game.popsoft.com.cn/")
    print(f"SCOPE|Wayback CDX unique HTTP-200 URL topology|{FROM}..{TO}|metadata-only|no HTML/payload")
    rows={};errors=[]
    for label,url,match in TARGETS:
        try:
            st,final,b=fetch(cdx_url(url,match));rr=parse(b)
            print(f"QUERY|label={label}|status={st}|rows={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
            for r in rr:
                k=(str(r.get("original") or ""),str(r.get("digest") or ""))
                rows[k]=r
        except Exception as e:
            errors.append((label,type(e).__name__,str(e)))
    ordered=sorted(rows.values(),key=lambda r:(str(r.get("timestamp") or ""),str(r.get("original") or "")))
    candidates=[];binary=[];exts=collections.Counter()
    for r in ordered:
        u=str(r.get("original") or "");score=hint_score(u);ib=is_binary(u);e=ext(u)
        if e:exts[e]+=1
        if ib:binary.append(r)
        if score or ib:candidates.append((score,ib,r))
        print("ROW|timestamp={}|score={}|binary={}|ext={}|mime={}|length={}|digest={}|original={}".format(
            clean(r.get("timestamp")),score,int(ib),clean(e),clean(r.get("mimetype")),clean(r.get("length")),clean(r.get("digest")),clean(u)
        ))
    for score,ib,r in sorted(candidates,key=lambda x:(-x[0],-int(x[1]),str(x[2].get("original") or ""))):
        print("CANDIDATE|score={}|binary={}|timestamp={}|mime={}|length={}|digest={}|original={}".format(
            score,int(ib),clean(r.get("timestamp")),clean(r.get("mimetype")),clean(r.get("length")),clean(r.get("digest")),clean(r.get("original"))
        ))
    for e,n in sorted(exts.items()): print(f"EXT_COUNT|ext={clean(e)}|rows={n}")
    for label,k,m in errors: print(f"ERROR|label={clean(label)}|kind={clean(k)}|message={clean(m)}")
    print(f"COUNT|unique_rows|{len(ordered)}")
    print(f"COUNT|candidate_rows|{len(candidates)}")
    print(f"COUNT|binary_rows|{len(binary)}")
    print(f"COUNT|errors|{len(errors)}")
    if any(s>=1 for s,_,_ in candidates):
        print("RESOLUTION|POPSOFT_PORTAL_TARGETS_FOUND|replay only exact high-value HTML/router candidates next")
    elif ordered:
        print("RESOLUTION|POPSOFT_PORTAL_ARCHIVED_NO_URL_HINT|replay bounded root/navigation captures for text-level StoneAge/download links")
    elif errors:
        print("RESOLUTION|PARTIAL_POPSOFT_PORTAL_CENSUS|retry only failed host surface")
    else:
        print("RESOLUTION|POPSOFT_PORTAL_WINDOW_NOT_INDEXED|return to other source-grounded recovery routes")
    print("EVIDENCE_BOUNDARY|URL index topology only; no client or page body is fetched.")

if __name__=="__main__":main()
