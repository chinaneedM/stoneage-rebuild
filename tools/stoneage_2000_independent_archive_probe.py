#!/usr/bin/env python3
"""Independent archive metadata probe for Sina's 2000-12-20 StoneAge full-map token.

Queries Arquivo.pt and Common Crawl for the exact filename, source page and
surviving Sina CGI URL. No historical binary payload is downloaded.
"""
from __future__ import annotations
import hashlib,json,urllib.error,urllib.parse,urllib.request

UA="stoneage-rebuild-archaeology/1.0 (+https://github.com/chinaneedM/stoneage-rebuild)"
FILENAME="samap_1220.zip"
SOURCE="http://games.sina.com.cn/downgames/map/1220492.shtml"
CGI="http://games1.sina.com.cn/cgi-bin/games/downgames/download.pl?col=map&aid=23223&title=%CA%AF%C6%F7%CA%B1%B4%FA%A1%AA%C8%AB%B5%D8%CD%BC&author=%D3%CE%C3%F1%B2%BF%C2%E4&filename=samap_1220.zip&size=1410"
DIRECT="http://202.106.184.193/downfiles/map_1212/samap_1220.zip"
ARQ_TEXT="https://arquivo.pt/textsearch"
ARQ_CDX="https://arquivo.pt/wayback/cdx"
CC_COLL="https://index.commoncrawl.org/collinfo.json"

def clean(v,n=5000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=40,max_bytes=8*1024*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/plain,*/*;q=0.5","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b

def parse_json(b):
    try:return json.loads(b.decode("utf-8"))
    except Exception:return None

def arq_items(obj):
    if isinstance(obj,dict):
        for k in ("response_items","items","results","documents","captures"):
            if isinstance(obj.get(k),list):return obj[k]
    return obj if isinstance(obj,list) else []

def arq_text_url(q):
    return ARQ_TEXT+"?"+urllib.parse.urlencode({"q":q,"maxItems":"500","from":"20000101000000","to":"20151231235959"})

def arq_version_url(u):
    return ARQ_TEXT+"?"+urllib.parse.urlencode({"versionHistory":u,"maxItems":"500"})

def arq_cdx_url(u):
    return ARQ_CDX+"?"+urllib.parse.urlencode({"url":u,"output":"json","limit":"5000"})

def cc_indexes():
    st,final,h,b=fetch(CC_COLL,timeout=30,max_bytes=2*1024*1024)
    d=json.loads(b.decode("utf-8"));by_year={}
    for x in d:
        cid=str(x.get("id") or "")
        import re
        m=re.search(r"CC-MAIN-(\d{4})",cid)
        if not m:continue
        y=int(m.group(1))
        if 2008<=y<=2018:by_year.setdefault(y,[]).append(cid)
    out=[]
    for y in sorted(by_year):
        vals=sorted(set(by_year[y]))
        out.append(vals[0])
        if vals[-1]!=vals[0]:out.append(vals[-1])
    return tuple(out)

def cc_query(cid,u):
    ep=f"https://index.commoncrawl.org/{cid}-index?"+urllib.parse.urlencode({"url":u,"output":"json"})
    try: st,final,h,b=fetch(ep,timeout=20,max_bytes=2*1024*1024)
    except urllib.error.HTTPError as e:
        if e.code in (400,404):return ep,()
        raise
    rows=[]
    for line in b.decode("utf-8","replace").splitlines():
        try:
            x=json.loads(line)
            if isinstance(x,dict):rows.append(x)
        except Exception:pass
    return ep,tuple(rows)

def emit_arq(label,obj):
    rr=arq_items(obj)
    print(f"ARQUIVO_COUNT|label={clean(label)}|rows={len(rr)}")
    for i,x in enumerate(rr[:500],1):
        if not isinstance(x,dict):continue
        low={str(k).lower():v for k,v in x.items()}
        def f(*names):
            for n in names:
                if n.lower() in low:return low[n.lower()]
            return ""
        print(f"ARQUIVO_ROW|label={clean(label)}|index={i}|url={clean(f('originalURL','url','original','uri'))}|title={clean(f('title'))}|timestamp={clean(f('tstamp','timestamp','date'))}|status={clean(f('statusCode','status','statuscode'))}|mime={clean(f('mimeType','mime','mimetype'))}|digest={clean(f('digest'))}|length={clean(f('contentLength','length'))}")
    return len(rr)

def main():
    print("StoneAge 2000 independent archive probe — R1")
    print("SCOPE|Arquivo.pt full-text/version/CDX + Common Crawl exact URL indexes|metadata-only|no-payload")
    print(f"TARGET|filename={FILENAME}|aid=23223|source={SOURCE}|direct={DIRECT}")
    errors=[];arq_rows=0;cc_rows=0
    for q in (FILENAME,"samap_1220",'"石器时代" "全地图"','"StoneAge" "samap"'):
        try:
            u=arq_text_url(q);st,final,h,b=fetch(u);obj=parse_json(b)
            print(f"ARQUIVO_TEXT|q={clean(q)}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|json={int(obj is not None)}")
            if obj is not None:arq_rows+=emit_arq("text:"+q,obj)
        except Exception as e:errors.append(("arquivo-text:"+q,type(e).__name__,str(e)))
    for label,u0 in (("source",SOURCE),("cgi",CGI),("direct",DIRECT)):
        for mode,builder in (("version",arq_version_url),("cdx",arq_cdx_url)):
            try:
                u=builder(u0);st,final,h,b=fetch(u);obj=parse_json(b)
                print(f"ARQUIVO_{mode.upper()}|label={label}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|json={int(obj is not None)}")
                if obj is not None:arq_rows+=emit_arq(mode+":"+label,obj)
            except Exception as e:errors.append((f"arquivo-{mode}:{label}",type(e).__name__,str(e)))
    try: ids=cc_indexes()
    except Exception as e:
        ids=();errors.append(("cc-index-list",type(e).__name__,str(e)))
    print(f"COMMONCRAWL_INDEX_COUNT|count={len(ids)}")
    for cid in ids:
        for label,u0 in (("filename","*"+FILENAME+"*"),("source",SOURCE),("cgi",CGI),("direct",DIRECT)):
            try:
                ep,rr=cc_query(cid,u0)
                if rr:print(f"COMMONCRAWL_HIT|index={clean(cid)}|label={label}|rows={len(rr)}|endpoint={clean(ep)}")
                for x in rr[:200]:
                    cc_rows+=1
                    print(f"COMMONCRAWL_ROW|index={clean(cid)}|label={label}|timestamp={clean(x.get('timestamp'))}|url={clean(x.get('url'))}|status={clean(x.get('status'))}|mime={clean(x.get('mime'))}|digest={clean(x.get('digest'))}|length={clean(x.get('length'))}")
            except Exception as e:errors.append((f"cc:{cid}:{label}",type(e).__name__,str(e)))
    for s,k,m in errors[:300]:print(f"ERROR|scope={clean(s)}|kind={clean(k)}|message={clean(m)}")
    print(f"COUNT|arquivo_rows|{arq_rows}")
    print(f"COUNT|commoncrawl_rows|{cc_rows}")
    print(f"COUNT|errors|{len(errors)}")
    if arq_rows or cc_rows:print("RESOLUTION|INDEPENDENT_ARCHIVE_ROWS_FOUND|inspect exact URL/filename matches before any payload recovery")
    else:print("RESOLUTION|NO_INDEPENDENT_ARCHIVE_ROW|tested independent public archive indexes expose no indexed target row")
    print("EVIDENCE_BOUNDARY|archive index/search rows are discovery metadata only; no returned historical binary body is downloaded.")
if __name__=="__main__":main()
