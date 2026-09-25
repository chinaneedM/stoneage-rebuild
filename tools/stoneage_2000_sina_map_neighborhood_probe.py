#!/usr/bin/env python3
"""Probe same-week Sina StoneAge map downloads as topology controls for aid=23223.

The target full-map CGI has no archived response.  Two 2000-12-28 StoneAge map
guide pages use the same Sina download backend.  This probe extracts their live
CGI tokens and checks Wayback/Arquivo metadata for redirects or file-server
paths.  No package body is downloaded.
"""
from __future__ import annotations
import hashlib,html,json,re,urllib.parse,urllib.request

UA="stoneage-rebuild-archaeology/1.0"
TARGET_PAGE="https://games.sina.com.cn/downgames/map/1220492.shtml"
NEIGHBOR_PAGES=(
 "https://games.sina.com.cn/downgames/map/1228507.shtml",
 "https://games.sina.com.cn/downgames/map/1228508.shtml",
)
TARGET_FILENAME="samap_1220.zip"
TARGET_AID="23223"
CDX="https://web.archive.org/cdx/search/cdx"
AVAIL="https://archive.org/wayback/available"
ARQ_TEXT="https://arquivo.pt/textsearch"
ARQ_CDX="https://arquivo.pt/wayback/cdx"

def clean(v,n=6000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=40,max_bytes=2*1024*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/html,text/plain,*/*;q=0.5","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),r.read(max_bytes)

def download_cgis(page,body):
    text=body.decode("gb18030","replace")
    raw=re.findall(r'(?is)href\s*=\s*["\']([^"\']+)["\']',text)
    out=[]
    for x in raw:
        u=urllib.parse.urljoin(page,html.unescape(x).replace("&amp;","&"))
        if "download.pl" in u and "aid=" in u:out.append(u)
    return tuple(dict.fromkeys(out))

def params(u):
    return dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(u).query,keep_blank_values=True))

def cdx_url(u):
    return CDX+"?"+urllib.parse.urlencode({
      "url":u,"matchType":"exact","output":"json",
      "fl":"timestamp,original,statuscode,mimetype,digest,length,redirect",
      "from":"2000","to":"2005","limit":"500"
    })

def parse_cdx(b):
    d=json.loads(b.decode("utf-8"))
    if not isinstance(d,list) or not d or not isinstance(d[0],list):return ()
    h=d[0];return tuple(dict(zip(h,row)) for row in d[1:] if isinstance(row,list))

def availability(u,date):
    ep=AVAIL+"?"+urllib.parse.urlencode({"url":u,"timestamp":date})
    st,final,h,b=fetch(ep,timeout=25)
    d=json.loads(b.decode("utf-8"));c=(d.get("archived_snapshots") or {}).get("closest") or {}
    return st,c if c.get("available") else None

def arq_version(u):
    return ARQ_TEXT+"?"+urllib.parse.urlencode({"versionHistory":u,"maxItems":"500"})

def arq_cdx(u):
    return ARQ_CDX+"?"+urllib.parse.urlencode({"url":u,"output":"json","limit":"5000"})

def arq_count(obj):
    if isinstance(obj,dict):
        for k in ("response_items","items","results","documents","captures"):
            if isinstance(obj.get(k),list):return len(obj[k])
    return len(obj) if isinstance(obj,list) else 0

def main():
    print("StoneAge 2000 Sina map neighborhood topology probe — R1")
    print("SCOPE|live same-week StoneAge map pages + Wayback/Arquivo CGI metadata|no-payload")
    errors=[];tokens=[]
    for role,page in (("target",TARGET_PAGE),("neighbor",NEIGHBOR_PAGES[0]),("neighbor",NEIGHBOR_PAGES[1])):
        try:
            st,final,h,b=fetch(page,timeout=30)
            cg=download_cgis(page,b)
            print(f"PAGE|role={role}|url={page}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|cgis={len(cg)}")
            for u in cg:
                p=params(u);tokens.append((role,page,u,p))
                print(f"CGI|role={role}|aid={clean(p.get('aid'))}|filename={clean(p.get('filename'))}|size={clean(p.get('size'))}|col={clean(p.get('col'))}|url={clean(u)}")
        except Exception as e:errors.append(("page:"+page,type(e).__name__,str(e)))
    topology=[]
    for role,page,u,p in tokens:
        aid=str(p.get("aid") or "");fn=str(p.get("filename") or "")
        for date in ("20001220","20001228","20010124","20011127","20020101"):
            try:
                st,c=availability(u,date)
                print(f"WAYBACK_AVAIL|role={role}|aid={clean(aid)}|date={date}|status={st}|hit={int(c is not None)}|timestamp={clean(c.get('timestamp') if c else '')}|capture={clean(c.get('url') if c else '')}")
            except Exception as e:errors.append((f"avail:{aid}:{date}",type(e).__name__,str(e)))
        try:
            st,final,h,b=fetch(cdx_url(u),timeout=45);rr=parse_cdx(b)
            print(f"WAYBACK_CDX|role={role}|aid={clean(aid)}|filename={clean(fn)}|status={st}|rows={len(rr)}|bytes={len(b)}")
            for x in rr:
                red=str(x.get("redirect") or "")
                print(f"WAYBACK_ROW|role={role}|aid={clean(aid)}|timestamp={clean(x.get('timestamp'))}|statuscode={clean(x.get('statuscode'))}|mimetype={clean(x.get('mimetype'))}|redirect={clean(red)}|digest={clean(x.get('digest'))}|length={clean(x.get('length'))}")
                if role=="neighbor" and red:topology.append((fn,red))
        except Exception as e:errors.append((f"cdx:{aid}",type(e).__name__,str(e)))
        for mode,builder in (("version",arq_version),("cdx",arq_cdx)):
            try:
                st,final,h,b=fetch(builder(u),timeout=45);obj=json.loads(b.decode("utf-8"));n=arq_count(obj)
                print(f"ARQUIVO|mode={mode}|role={role}|aid={clean(aid)}|status={st}|rows={n}|bytes={len(b)}")
            except Exception as e:errors.append((f"arquivo:{mode}:{aid}",type(e).__name__,str(e)))
    print(f"COUNT|tokens|{len(tokens)}")
    print(f"COUNT|neighbor_redirects|{len(topology)}")
    for fn,red in topology:print(f"TOPOLOGY|source_filename={clean(fn)}|redirect={clean(red)}")
    for s,k,m in errors[:200]:print(f"ERROR|scope={clean(s)}|kind={clean(k)}|message={clean(m)}")
    print(f"COUNT|errors|{len(errors)}")
    if topology:print("RESOLUTION|NEIGHBOR_DOWNLOAD_TOPOLOGY_FOUND|substitute target filename only as a hypothesis and probe exact archive metadata")
    else:print("RESOLUTION|NO_NEIGHBOR_REDIRECT_TOPOLOGY|same-week controls expose no archived redirect on tested indexes")
    print("EVIDENCE_BOUNDARY|neighbor packages are topology controls only; they do not prove target payload identity or direct-file location.")
if __name__=="__main__":main()
