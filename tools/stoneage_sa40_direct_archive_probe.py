#!/usr/bin/env python3
"""Probe independent archives for the evidence-synthesized StoneAge 4.0 direct URL.

Wayback proves that 202.106.185.223/updatex_1024/ was live before the target
publication date, but has no row for the target basename. This bounded probe
asks Arquivo.pt and a small set of early Common Crawl indexes for the exact
direct URL (including explicit :80 variant). Metadata/WARC headers only.
"""
from __future__ import annotations
import gzip, json, urllib.error, urllib.parse, urllib.request

UA="stoneage-rebuild-archaeology/1.0 (+https://github.com/chinaneedM/stoneage-rebuild)"
TARGETS=(
 "http://202.106.185.223/updatex_1024/shiqi4updatex_02_11_08.zip",
 "http://202.106.185.223:80/updatex_1024/shiqi4updatex_02_11_08.zip",
)
ARQ_CDX="https://arquivo.pt/wayback/cdx"
ARQ_TEXT="https://arquivo.pt/textsearch"
CC_COLL="https://index.commoncrawl.org/collinfo.json"
CC_DATA="https://data.commoncrawl.org/"
MAX_WARC=256*1024

def clean(v,n=5000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=35,headers=None,max_bytes=2*1024*1024):
    h={"User-Agent":UA,"Accept-Encoding":"identity"}
    if headers:h.update(headers)
    req=urllib.request.Request(url,headers=h)
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        if len(b)>max_bytes:raise ValueError(f"response-too-large:{len(b)}")
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b

def arq_cdx(u):
    return ARQ_CDX+"?"+urllib.parse.urlencode({"url":u,"output":"json","limit":"5000"})

def arq_version(u):
    return ARQ_TEXT+"?"+urllib.parse.urlencode({"versionHistory":u,"maxItems":"500"})

def parse_obj(b):
    try:return json.loads(b.decode("utf-8"))
    except Exception:return None

def count_arq(obj):
    if isinstance(obj,list):return max(0,len(obj)-1) if obj and isinstance(obj[0],list) else len(obj)
    if isinstance(obj,dict):
        for k in ("response_items","items","results","documents","captures"):
            if isinstance(obj.get(k),list):return len(obj[k])
    return 0

def cc_indexes():
    st,final,h,b=fetch(CC_COLL,timeout=30,max_bytes=2*1024*1024)
    obj=json.loads(b.decode("utf-8"))
    chosen=[]
    for x in obj:
        cid=str(x.get("id") or "")
        # Keep only earliest available index for each useful early year.
        if any(y in cid for y in ("2008","2009","2010","2011","2012","2013","2014")):
            chosen.append(cid)
    # Sort oldest first and cap to avoid broad modern crawl work.
    return tuple(sorted(set(chosen),reverse=False)[:16])

def cc_query(cid,u):
    ep=f"https://index.commoncrawl.org/{cid}-index?"+urllib.parse.urlencode({"url":u,"output":"json"})
    try:
        st,final,h,b=fetch(ep,timeout=18,max_bytes=512*1024)
    except urllib.error.HTTPError as e:
        if e.code in (400,404):return ep,()
        raise
    out=[]
    for line in b.decode("utf-8","replace").splitlines():
        try:
            o=json.loads(line)
            if isinstance(o,dict):out.append(o)
        except Exception:pass
    return ep,tuple(out)

def warc_head(row):
    fn=str(row.get("filename") or ""); off=int(row.get("offset") or 0); ln=int(row.get("length") or 0)
    if not fn or ln<=0 or ln>MAX_WARC:return ""
    st,final,h,b=fetch(CC_DATA+fn,timeout=35,headers={"Range":f"bytes={off}-{off+ln-1}"},max_bytes=MAX_WARC+1024)
    try:raw=gzip.decompress(b)
    except Exception:raw=b
    p=raw.find(b"HTTP/")
    if p<0:return ""
    e=raw.find(b"\r\n\r\n",p)
    if e<0:e=raw.find(b"\n\n",p)
    return raw[p:e if e>p else min(len(raw),p+8192)].decode("latin1","replace").splitlines()[0]

def main():
    print("StoneAge 4.0 synthesized direct-route independent-archive probe — R1")
    print("SCOPE|exact direct URL + :80 variant|Arquivo.pt + bounded early Common Crawl|metadata/header-only|no-payload")
    errors=[];arq_hits=0;cc_hits=0
    for i,u in enumerate(TARGETS,1):
        for kind,maker in (("cdx",arq_cdx),("version",arq_version)):
            try:
                st,final,h,b=fetch(maker(u),timeout=40,max_bytes=4*1024*1024)
                obj=parse_obj(b);n=count_arq(obj)
                arq_hits+=n
                print(f"ARQUIVO|target={i}|kind={kind}|status={st}|json={int(obj is not None)}|rows={n}|bytes={len(b)}|final={clean(final)}")
            except Exception as e:errors.append((f"arquivo:{i}:{kind}",type(e).__name__,str(e)))
    try:ids=cc_indexes()
    except Exception as e:
        errors.append(("cc:index-list",type(e).__name__,str(e)));ids=()
    print(f"COUNT|cc_indexes|{len(ids)}")
    rows=[]
    for cid in ids:
        for i,u in enumerate(TARGETS,1):
            try:
                ep,rr=cc_query(cid,u)
                if rr:print(f"CC_INDEX|id={cid}|target={i}|rows={len(rr)}|endpoint={clean(ep)}")
                for r in rr:
                    rows.append((cid,i,r));cc_hits+=1
                    print(f"CC_ROW|id={cid}|target={i}|timestamp={clean(r.get('timestamp'))}|url={clean(r.get('url'))}|status={clean(r.get('status'))}|mime={clean(r.get('mime'))}|digest={clean(r.get('digest'))}|length={clean(r.get('length'))}")
            except Exception as e:errors.append((f"cc:{cid}:{i}",type(e).__name__,str(e)))
    for cid,i,r in rows[:12]:
        try:
            head=warc_head(r)
            print(f"CC_WARC|id={cid}|target={i}|http={clean(head)}")
        except Exception as e:errors.append((f"warc:{cid}:{i}",type(e).__name__,str(e)))
    print(f"COUNT|arquivo_rows|{arq_hits}")
    print(f"COUNT|commoncrawl_rows|{cc_hits}")
    for s,k,m in errors[:100]:print(f"ERROR|scope={clean(s)}|kind={clean(k)}|message={clean(m)}")
    print(f"COUNT|errors|{len(errors)}")
    if arq_hits or cc_hits:
        print("RESOLUTION|INDEPENDENT_ARCHIVE_DIRECT_ROUTE_HIT|inspect exact capture provenance/bytes next")
    elif errors and not ids:
        print("RESOLUTION|INDEPENDENT_ARCHIVE_PROBE_INCOMPLETE|retry only failed direct URL surfaces")
    else:
        print("RESOLUTION|NO_INDEPENDENT_DIRECT_ROUTE_HIT|direct network-recovery route is bounded on tested archives")
    print("EVIDENCE_BOUNDARY|Zero archive-index rows mean no indexed capture on tested services; they do not prove the historical file never existed.")

if __name__=="__main__":
    main()
