#!/usr/bin/env python3
"""Replay exact Waei StoneAge early news articles 416 and 469.

Article IDs are directly bound by retained first-party homepage HTML:
416 = 2000/12/1 free-test StoneAge announcement.
469 = 2001/1/4 StoneAge mainland-situation article.
This probe recovers archived HTML, visible text, and download/client-related
links only. No linked binary payload is fetched.
"""
from __future__ import annotations
import hashlib, html, json, re, time, urllib.parse, urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
MAX=2*1024*1024
ARTICLES=(
 (416,"2000-12-01 free-test headline"),
 (469,"2001-01-04 mainland headline"),
)
HOSTS=("http://www7.waei.net/news/shownews.asp?id={}",
       "http://www7.waei.net:80/news/shownews.asp?id={}")

def clean(v,n=7000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=45,max_bytes=MAX,attempts=2):
    last=None
    for i in range(attempts):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/html,*/*;q=0.2","Accept-Encoding":"identity"})
            with urllib.request.urlopen(req,timeout=timeout) as r:
                b=r.read(max_bytes+1)
                if len(b)>max_bytes:raise ValueError("response-too-large")
                return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b,i+1
        except Exception as e:
            last=e
            if i+1<attempts:time.sleep(2)
    raise last

def cdx(orig):
    q=[("url",orig),("matchType","exact"),("output","json"),
       ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
       ("from","20001201"),("to","20011231"),("limit","5000")]
    return CDX+"?"+urllib.parse.urlencode(q)

def rows(b):
    o=json.loads(b.decode("utf-8"))
    if not isinstance(o,list) or len(o)<2:return ()
    h=o[0]
    return tuple(dict(zip(h,r)) for r in o[1:] if isinstance(r,list))

def decode(b):
    for enc in ("big5","gb18030","gbk","utf-8","latin1"):
        try:return enc,b.decode(enc)
        except UnicodeDecodeError:pass
    return "latin1",b.decode("latin1","replace")

def visible(t):
    x=re.sub(r"(?is)<script.*?</script>|<style.*?</style>"," ",t)
    return re.sub(r"\s+"," ",html.unescape(re.sub(r"(?s)<[^>]+>"," ",x)))

def anchors(t,base):
    out=[]
    for m in re.finditer(r'(?is)<a\b[^>]*href\s*=\s*["\']([^"\']+)["\'][^>]*>(.*?)</a>',t):
        u=urllib.parse.urljoin(base,html.unescape(m.group(1)).strip())
        a=clean(html.unescape(re.sub(r"(?s)<[^>]+>"," ",m.group(2))),1800)
        out.append((u,a))
    return out

def relevant(u,a):
    s=(u+" "+a).lower()
    return any(k in s for k in (
      "download","downloan","downloading","fileid","試玩","试玩","測試","测试",
      "client","setup",".exe",".zip",".rar",".cab","stoneage","石器"
    ))

def snippets(p):
    needles=("免費測試","免费测试","試玩","试玩","測試","测试","下載","下载",
             "download","客戶端","客户端","274","石器時代","石器时代","大陸","大陆")
    low=p.lower();out=[]
    for n in needles:
        st=0;nl=n.lower()
        while True:
            i=low.find(nl,st)
            if i<0:break
            v=clean(p[max(0,i-450):min(len(p),i+1200)],2600)
            if v not in out:out.append(v)
            st=i+max(1,len(n))
    return out[:45]

def main():
    print("StoneAge Waei exact early-news article replay — R1")
    print("SCOPE|first-party article ids directly bound from retained StoneAge homepage|HTML only|no linked payload")
    captures={};errors=[]
    for aid,label in ARTICLES:
        for fmt in HOSTS:
            orig=fmt.format(aid)
            try:
                st,final,h,b,attempt=fetch(cdx(orig),max_bytes=1024*1024)
                rr=rows(b)
                print(f"CDX|id={aid}|label={label}|port80={int(':80/' in orig)}|status={st}|rows={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|attempt={attempt}")
                for r in rr:
                    captures[(aid,str(r.get("timestamp") or ""),str(r.get("original") or ""),str(r.get("digest") or ""))]=r
            except Exception as e:
                errors.append((f"cdx:{aid}:{orig}",type(e).__name__,str(e)))
    replayed=set()
    for (aid,ts,orig,dig),r in sorted(captures.items()):
        print(f"ROW|id={aid}|timestamp={ts}|status={clean(r.get('statuscode'))}|mime={clean(r.get('mimetype'))}|length={clean(r.get('length'))}|digest={clean(dig)}|original={clean(orig)}")
        if str(r.get("statuscode") or "")!="200":continue
        dedup=(aid,dig)
        if dedup in replayed:continue
        replayed.add(dedup)
        try:
            st,final,h,b,attempt=fetch(f"https://web.archive.org/web/{ts}id_/{orig}")
            enc,t=decode(b);p=visible(t);aa=anchors(t,orig)
            rel=[x for x in aa if relevant(*x)]
            print(f"PAGE|id={aid}|timestamp={ts}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|encoding={enc}|anchors={len(aa)}|relevant_links={len(rel)}|final={clean(final)}")
            print(f"VISIBLE|id={aid}|timestamp={ts}|text={clean(p,18000)}")
            for u,a in rel:
                print(f"LINK|id={aid}|timestamp={ts}|text={clean(a)}|url={clean(u)}")
            for s in snippets(p):
                print(f"SNIPPET|id={aid}|timestamp={ts}|text={s}")
        except Exception as e:
            errors.append((f"replay:{aid}:{ts}",type(e).__name__,str(e)))
    for s,k,m in errors:
        print(f"ERROR|scope={clean(s)}|kind={k}|message={clean(m)}")
    ids=sorted({k[0] for k in captures})
    print(f"COUNT|article_ids_with_captures|{len(ids)}")
    print(f"IDS_WITH_CAPTURES|{','.join(map(str,ids))}")
    print(f"COUNT|unique_replayed_bodies|{len(replayed)}")
    print(f"COUNT|errors|{len(errors)}")
    if 416 in ids:
        print("RESOLUTION|FREE_TEST_ARTICLE_ARCHIVE_ROW_FOUND|interpret direct body/links before relating it to Jan-4 274MB trial")
    elif errors:
        print("RESOLUTION|EARLY_ARTICLE_REPLAY_PARTIAL|retry failed exact article only")
    else:
        print("RESOLUTION|EARLY_ARTICLE_IDS_UNPRESERVED|retain homepage route binding as chronology evidence")
    print("EVIDENCE_BOUNDARY|Article 416 is Taiwan/Waei first-party unless its body explicitly establishes another region. Do not equate it with Mainland Jan-2001 trial bytes without direct linkage.")

if __name__=="__main__":main()
