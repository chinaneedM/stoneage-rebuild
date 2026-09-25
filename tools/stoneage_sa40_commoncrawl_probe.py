#!/usr/bin/env python3
"""Probe Common Crawl URL indexes/WARC headers for Sina StoneAge 4.0 download CGI.

Looks for exact target CGI plus the adjacent aid=61619 CGI recovered from the
surviving neighbor page. If a small archived response exists, inspect only the
WARC/HTTP headers for historical Location. No patch payload is downloaded.
"""
from __future__ import annotations
import gzip,hashlib,json,re,urllib.error,urllib.parse,urllib.request

UA="stoneage-rebuild-archaeology/1.0 (+https://github.com/chinaneedM/stoneage-rebuild)"
COLL="https://index.commoncrawl.org/collinfo.json"
DATA="https://data.commoncrawl.org/"
SOURCE_TARGET="https://games.sina.com.cn/downgames/updatex/11084599.shtml"
SOURCE_NEIGHBOR="https://games.sina.com.cn/downgames/updatex/11084598.shtml"
MAX_WARC=256*1024

def clean(v,n=5000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=40,headers=None,max_bytes=4*1024*1024):
    hh={"User-Agent":UA,"Accept-Encoding":"identity"}
    if headers:hh.update(headers)
    req=urllib.request.Request(url,headers=hh)
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b

def source_cgi(page,aid):
    st,final,h,b=fetch(page,timeout=30,max_bytes=2*1024*1024)
    text=b.decode("gb18030","replace")
    hrefs=re.findall(r'(?is)href\s*=\s*["\']([^"\']+)["\']',text)
    for x in hrefs:
        x=x.replace("&amp;","&")
        u=urllib.parse.urljoin(page,x)
        q=dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(u).query,keep_blank_values=True))
        if q.get("aid")==str(aid) and "download.pl" in u:
            return u
    return ""

def indexes():
    st,final,h,b=fetch(COLL,timeout=30,max_bytes=2*1024*1024)
    obj=json.loads(b.decode("utf-8"));out=[]
    for x in obj:
        cid=str(x.get("id") or "")
        m=re.search(r"CC-MAIN-(\d{4})",cid)
        if m and int(m.group(1))<=2018:
            out.append(cid)
    return tuple(out)

def index_query(cid,u):
    ep=f"https://index.commoncrawl.org/{cid}-index?"+urllib.parse.urlencode({"url":u,"output":"json"})
    try:
        st,final,h,b=fetch(ep,timeout=20,max_bytes=1024*1024)
    except urllib.error.HTTPError as e:
        if e.code in (404,400):return ep,()
        raise
    rows=[]
    for line in b.decode("utf-8","replace").splitlines():
        try:
            o=json.loads(line)
            if isinstance(o,dict):rows.append(o)
        except Exception:pass
    return ep,tuple(rows)

def hget(headers,name):
    want=name.lower()
    for line in headers.splitlines():
        if ":" not in line:continue
        k,v=line.split(":",1)
        if k.strip().lower()==want:return v.strip()
    return ""

def warc_headers(row):
    length=int(row.get("length") or 0);offset=int(row.get("offset") or 0);fn=str(row.get("filename") or "")
    if not fn or not length or length>MAX_WARC:return None
    url=DATA+fn
    st,final,h,b=fetch(url,timeout=45,headers={"Range":f"bytes={offset}-{offset+length-1}"},max_bytes=MAX_WARC+1024)
    try:raw=gzip.decompress(b)
    except Exception:raw=b
    # WARC header then embedded HTTP response header.
    p=raw.find(b"HTTP/")
    if p<0:return {"status":st,"bytes":len(b),"raw_bytes":len(raw),"location":"","http":""}
    e=raw.find(b"\r\n\r\n",p)
    if e<0:e=raw.find(b"\n\n",p)
    head=raw[p:e if e>p else min(len(raw),p+16384)].decode("latin1","replace")
    first=head.splitlines()[0] if head else ""
    return {"status":st,"bytes":len(b),"raw_bytes":len(raw),"location":hget(head,"Location"),"http":first}

def main():
    print("StoneAge 4.0 Common Crawl CGI redirect probe — R1")
    print("SCOPE|exact-Sina-CGI+neighbor-CGI+historical-CC-indexes+small-WARC-header-only|no-payload")
    errors=[]
    target=source_cgi(SOURCE_TARGET,61620)
    neighbor=source_cgi(SOURCE_NEIGHBOR,61619)
    print(f"CGI|aid=61620|url={clean(target)}")
    print(f"CGI|aid=61619|url={clean(neighbor)}")
    ids=indexes()
    print(f"COUNT|historical_indexes|{len(ids)}")
    rows=[]
    for cid in ids:
        for label,u in (("target",target),("neighbor",neighbor),("source",SOURCE_TARGET)):
            if not u:continue
            try:
                ep,rr=index_query(cid,u)
                if rr:
                    print(f"INDEX|id={cid}|label={label}|rows={len(rr)}|endpoint={clean(ep)}")
                for r in rr:
                    rows.append((cid,label,u,r))
                    print(
                      f"ROW|id={cid}|label={label}|timestamp={clean(r.get('timestamp'))}|url={clean(r.get('url'))}|"
                      f"status={clean(r.get('status'))}|mime={clean(r.get('mime'))}|digest={clean(r.get('digest'))}|"
                      f"length={clean(r.get('length'))}|filename={clean(r.get('filename'))}|offset={clean(r.get('offset'))}"
                    )
            except Exception as exc:errors.append((cid+":"+label,type(exc).__name__,str(exc)))
    locs=[]
    seen=set()
    for cid,label,u,r in rows:
        k=(r.get("filename"),r.get("offset"),r.get("length"))
        if k in seen:continue
        seen.add(k)
        try:
            z=warc_headers(r)
            if z:
                print(f"WARC|id={cid}|label={label}|status={z['status']}|bytes={z['bytes']}|raw_bytes={z['raw_bytes']}|http={clean(z['http'])}|location={clean(z['location'])}")
                if z["location"]:locs.append((label,z["location"]))
        except Exception as exc:errors.append(("warc:"+cid+":"+label,type(exc).__name__,str(exc)))
    for s,k,m in errors[:200]:print(f"ERROR|scope={clean(s)}|kind={clean(k)}|message={clean(m)}")
    print(f"COUNT|index_rows|{len(rows)}");print(f"COUNT|historical_locations|{len(locs)}");print(f"COUNT|errors|{len(errors)}")
    for label,loc in locs:print(f"HISTORICAL_LOCATION|label={label}|url={clean(loc)}")
    print("RESOLUTION|"+("COMMONCRAWL_REDIRECT_RECOVERED|probe target server/path next" if locs else ("COMMONCRAWL_ROWS_NO_LOCATION|retain independent captures as topology controls" if rows else "NO_COMMONCRAWL_EXACT_CGI_ROW|tested historical indexes expose no exact CGI capture")))
    print("EVIDENCE_BOUNDARY|only exact URL index rows and bounded WARC response headers are inspected; large response records and payload bodies are not fetched.")
if __name__=="__main__":main()
