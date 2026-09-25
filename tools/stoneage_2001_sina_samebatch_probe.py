#!/usr/bin/env python3
"""Recover same-batch Sina map download records around the 2001-11-27 StoneAge page.

The target source page is /downgames/map/11271899.shtml. This probe scans a
small bounded numeric neighborhood on the still-live Sina HTML surface, extracts
only download.pl links, and records map-column siblings. It does not download
binary payloads.
"""
from __future__ import annotations
import hashlib, html, re, urllib.parse, urllib.request

UA="stoneage-rebuild-archaeology/1.0"
BASE="https://games.sina.com.cn/downgames/map/"
TARGET_PAGE=11271899
RADIUS=36
TARGET_AID="43172"
TARGET_FILENAME="Estoneage2.0map_1127.exe"

def clean(v,n=7000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=18,max_bytes=256*1024):
    req=urllib.request.Request(url,headers={
        "User-Agent":UA,
        "Accept":"text/html,text/plain,*/*;q=0.5",
        "Accept-Encoding":"identity",
    })
    with urllib.request.urlopen(req,timeout=timeout) as r:
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),r.read(max_bytes)

def decode(body):
    for enc in ("gb18030","utf-8","big5","latin1"):
        try:return body.decode(enc)
        except UnicodeDecodeError:pass
    return body.decode("latin1","replace")

def download_links(body,base):
    text=decode(body)
    vals=re.findall(r'(?is)href\s*=\s*["\']([^"\']+)["\']',text)
    out=[]
    for raw in vals:
        u=urllib.parse.urljoin(base,html.unescape(raw))
        low=urllib.parse.unquote_plus(u).lower()
        if "/cgi-bin/games/downgames/download.pl?" not in low:
            continue
        p=dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(u).query,keep_blank_values=True))
        if str(p.get("col","")).lower()!="map":
            continue
        out.append((u,p))
    seen={}
    for u,p in out:
        key=(str(p.get("aid","")),str(p.get("filename","")),str(p.get("size","")),u)
        seen[key]=(u,p)
    return tuple(seen.values())

def targetish(params):
    return str(params.get("aid",""))==TARGET_AID or str(params.get("filename","")).lower()==TARGET_FILENAME.lower()

def page_ids():
    return range(TARGET_PAGE-RADIUS,TARGET_PAGE+RADIUS+1)

def main():
    print("StoneAge 2001 Sina same-batch map-page probe — R1")
    print("SCOPE|bounded live Sina HTML neighborhood + map download-token extraction|no-payload")
    print(f"TARGET|page={TARGET_PAGE}|aid={TARGET_AID}|filename={TARGET_FILENAME}|radius={RADIUS}")
    errors=[];records=[]
    for pid in page_ids():
        url=f"{BASE}{pid}.shtml"
        try:
            st,final,h,b=fetch(url)
            links=download_links(b,url)
            if not links:
                continue
            print(f"PAGE|id={pid}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|links={len(links)}")
            for dl,p in links:
                rec=(pid,str(p.get("aid","")),str(p.get("filename","")),str(p.get("size","")),str(p.get("author","")),dl)
                records.append(rec)
                print(
                    f"RECORD|page={pid}|target={int(targetish(p))}|aid={clean(p.get('aid'))}|"
                    f"filename={clean(p.get('filename'))}|size={clean(p.get('size'))}|"
                    f"author={clean(p.get('author'))}|url={clean(dl)}"
                )
        except Exception as e:
            errors.append((pid,type(e).__name__,str(e)))
    uniq={}
    for r in records:
        uniq[(r[1],r[2],r[3],r[5])]=r
    ordered=sorted(uniq.values(),key=lambda r:(abs(r[0]-TARGET_PAGE),r[0],r[1],r[2].lower()))
    print(f"COUNT|pages_scanned|{len(tuple(page_ids()))}")
    print(f"COUNT|map_records|{len(ordered)}")
    for rank,r in enumerate(ordered,1):
        pid,aid,fn,size,author,dl=r
        print(f"NEIGHBOR|rank={rank}|page={pid}|distance={abs(pid-TARGET_PAGE)}|aid={clean(aid)}|filename={clean(fn)}|size={clean(size)}|author={clean(author)}|url={clean(dl)}")
    for pid,kind,msg in errors[:100]:
        print(f"ERROR|page={pid}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|errors|{len(errors)}")
    if len(ordered)>1:
        print("RESOLUTION|SAME_BATCH_MAP_RECORDS_FOUND|use nearest sibling CGI tokens for archived direct-server recovery")
    elif ordered:
        print("RESOLUTION|TARGET_ONLY|bounded sibling pages expose no additional map token")
    else:
        print("RESOLUTION|NO_MAP_RECORDS|live numeric neighborhood does not expose usable map pages")
    print("EVIDENCE_BOUNDARY|numeric page proximity is discovery evidence only; sibling records do not prove a shared binary host/directory.")

if __name__=="__main__":
    main()
