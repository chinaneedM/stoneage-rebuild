#!/usr/bin/env python3
"""Recover Waei StoneAge Dec-2000 / Jan-2001 news archive pages.

The preserved Feb-2001 first-party newsback page proves query form
newsback.asp?nyear=YYYY&nmonth=M. This probe uses that source-derived route for
2000-12 and 2001-01, extracts exact news anchors and contexts around the
Dec-1 free-test announcement and download/trial terms. HTML only; no payload.
"""
from __future__ import annotations
import hashlib, html, json, re, time, urllib.parse, urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
MAX=2*1024*1024
MONTHS=((2000,12),(2001,1))
HOSTS=("http://www7.waei.net/wgs/stoneage/newsback.asp",
       "http://www7.waei.net:80/wgs/stoneage/newsback.asp")

def clean(v,n=5000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=45,max_bytes=MAX,attempts=2):
    last=None
    for i in range(attempts):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/html,*/*;q=0.2","Accept-Encoding":"identity"})
            with urllib.request.urlopen(req,timeout=timeout) as r:
                b=r.read(max_bytes+1)
                if len(b)>max_bytes: raise ValueError("response-too-large")
                return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b,i+1
        except Exception as e:
            last=e
            if i+1<attempts: time.sleep(2)
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

def textify(t):
    p=re.sub(r"(?is)<script.*?</script>|<style.*?</style>"," ",t)
    return re.sub(r"\s+"," ",html.unescape(re.sub(r"(?s)<[^>]+>"," ",p)))

def anchors(t,base):
    out=[]
    for m in re.finditer(r'(?is)<a\b[^>]*href\s*=\s*["\']([^"\']+)["\'][^>]*>(.*?)</a>',t):
        u=urllib.parse.urljoin(base,html.unescape(m.group(1)).strip())
        a=clean(html.unescape(re.sub(r"(?s)<[^>]+>"," ",m.group(2))),1500)
        out.append((u,a,m.start(),m.end()))
    return out

def snippets(p):
    needles=("免費測試","免费测试","試玩","试玩","下載","下载","download","石器時代","石器时代","2000/12/1","274")
    low=p.lower();out=[]
    for n in needles:
        s=0;nl=n.lower()
        while True:
            i=low.find(nl,s)
            if i<0:break
            v=clean(p[max(0,i-420):min(len(p),i+900)],2200)
            if v not in out:out.append(v)
            s=i+max(1,len(n))
    return out[:40]

def relevant(u,a):
    s=(u+" "+a).lower()
    return any(k in s for k in ("免費測試","免费测试","試玩","试玩","download","down","news","detail","石器"))

def main():
    print("StoneAge Waei Dec-2000 / Jan-2001 newsback recovery — R1")
    print("SCOPE|source-derived first-party newsback month route|HTML only|no payload")
    captures={};errors=[]
    for y,m in MONTHS:
        for host in HOSTS:
            orig=host+"?"+urllib.parse.urlencode({"nyear":y,"nmonth":m})
            try:
                st,final,h,b,attempt=fetch(cdx(orig),max_bytes=1024*1024)
                rr=rows(b)
                print(f"CDX|year={y}|month={m}|port80={int(':80/' in host)}|status={st}|rows={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|attempt={attempt}")
                for r in rr:
                    key=(str(r.get("timestamp") or ""),str(r.get("original") or ""),str(r.get("digest") or ""))
                    captures[key]=r
            except Exception as e:
                errors.append((f"cdx:{y}-{m}:{host}",type(e).__name__,str(e)))
    for (ts,orig,dig),r in sorted(captures.items()):
        if str(r.get("statuscode") or "")!="200":
            print(f"ROW|timestamp={ts}|status={clean(r.get('statuscode'))}|mime={clean(r.get('mimetype'))}|length={clean(r.get('length'))}|digest={clean(dig)}|original={clean(orig)}")
            continue
        try:
            st,final,h,b,attempt=fetch(f"https://web.archive.org/web/{ts}id_/{orig}")
            enc,t=decode(b);p=textify(t);aa=anchors(t,orig)
            free=any(k in p for k in ("免費測試","免费测试"))
            trial=any(k in p for k in ("試玩","试玩"))
            down=any(k.lower() in p.lower() for k in ("下載","下载","download"))
            print(f"PAGE|timestamp={ts}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|encoding={enc}|free_test={int(free)}|trial={int(trial)}|download={int(down)}|anchors={len(aa)}|original={clean(orig)}")
            for u,a,start,end in aa:
                if relevant(u,a):
                    ctx=clean(p[max(0,p.find(a)-250) if a and p.find(a)>=0 else 0:min(len(p),(p.find(a)+len(a)+500) if a and p.find(a)>=0 else 900)],1600)
                    print(f"ANCHOR|timestamp={ts}|text={clean(a)}|url={clean(u)}|context={ctx}")
            for s in snippets(p):
                print(f"SNIPPET|timestamp={ts}|text={s}")
        except Exception as e:
            errors.append((f"replay:{ts}:{orig}",type(e).__name__,str(e)))
    for s,k,m in errors:
        print(f"ERROR|scope={clean(s)}|kind={k}|message={clean(m)}")
    print(f"COUNT|captures|{len(captures)}")
    print(f"COUNT|errors|{len(errors)}")
    if captures:
        print("RESOLUTION|EARLY_NEWSBACK_CAPTURE_FOUND|bind Dec-1 free-test article/detail route if exposed")
    elif errors:
        print("RESOLUTION|EARLY_NEWSBACK_PARTIAL|retry only failed exact month route")
    else:
        print("RESOLUTION|EARLY_NEWSBACK_EXACT_MONTH_UNPRESERVED|use homepage retained headlines as first-party chronology only")
    print("EVIDENCE_BOUNDARY|Retained headline/date text proves first-party publication chronology; only direct article/download routes can identify client distribution.")

if __name__=="__main__":main()
