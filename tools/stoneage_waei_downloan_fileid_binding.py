#!/usr/bin/env python3
"""Bind StoneAge down_loan.htm screen-saver controls to fileid 36/37.

Replays one known archived first-party HTML page and extracts each anchor's text
and surrounding DOM/text context. Separately checks exact CDX status rows for
fileids 35,36,37. No linked payload body is fetched.
"""
from __future__ import annotations
import hashlib, html, json, re, urllib.parse, urllib.request

UA="stoneage-rebuild-archaeology/1.0"
TS="20010226191900"
PAGE="http://www7.waei.net:80/wgs/stoneage/content/down_loan.htm"
CDX="https://web.archive.org/cdx/search/cdx"
IDS=(35,36,37)
FROM="20001201";TO="20010630"
MAX=1024*1024

def clean(v,n=4000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=45,max_bytes=MAX):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/html,*/*;q=0.2","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        if len(b)>max_bytes:raise ValueError("response-too-large")
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b

def decode(b):
    for enc in ("big5","gb18030","gbk","utf-8","latin1"):
        try:return enc,b.decode(enc)
        except UnicodeDecodeError:pass
    return "latin1",b.decode("latin1","replace")

def strip(t):
    return clean(html.unescape(re.sub(r"(?s)<[^>]+>"," ",t)),1200)

def anchors(t):
    out=[]
    pat=re.compile(r'(?is)<a\b([^>]*)href\s*=\s*["\']([^"\']+)["\']([^>]*)>(.*?)</a>')
    for i,m in enumerate(pat.finditer(t),1):
        u=urllib.parse.urljoin(PAGE,html.unescape(m.group(2)).strip())
        a=strip(m.group(4))
        out.append((i,m.start(),m.end(),u,a))
    return out

def cdx_url(fid):
    orig=f"http://www7.waei.net/download/download.asp?fileid={fid}"
    q=[("url",orig),("matchType","exact"),("output","json"),
       ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
       ("from",FROM),("to",TO),("limit","100")]
    return CDX+"?"+urllib.parse.urlencode(q)

def rows(b):
    o=json.loads(b.decode("utf-8"))
    if not isinstance(o,list) or len(o)<2:return ()
    h=o[0]
    return tuple(dict(zip(h,r)) for r in o[1:] if isinstance(r,list))

def main():
    print("StoneAge Waei down_loan fileid 35/36/37 binding — R1")
    print("SCOPE|known first-party 2001-02-26 HTML + exact CDX status|no linked payload")
    errors=[]
    try:
        st,final,h,b=fetch(f"https://web.archive.org/web/{TS}id_/{PAGE}")
        enc,t=decode(b)
        aa=anchors(t)
        print(f"PAGE|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|encoding={enc}|anchors={len(aa)}|final={clean(final)}")
        for i,start,end,u,a in aa:
            m=re.search(r"[?&]fileid=(\d+)",u,re.I)
            if not m or int(m.group(1)) not in IDS:continue
            fid=int(m.group(1))
            ctx=strip(t[max(0,start-500):min(len(t),end+500)])
            print(f"ANCHOR|order={i}|fileid={fid}|text={clean(a)}|url={clean(u)}|context={clean(ctx,1800)}")
    except Exception as e:
        errors.append(("page",type(e).__name__,str(e)))
    status_map={}
    for fid in IDS:
        try:
            st,final,h,b=fetch(cdx_url(fid),max_bytes=512*1024)
            rr=rows(b)
            vals=[]
            for r in rr:
                vals.append(str(r.get("statuscode") or ""))
                print(f"ROW|fileid={fid}|timestamp={clean(r.get('timestamp'))}|status={clean(r.get('statuscode'))}|mime={clean(r.get('mimetype'))}|length={clean(r.get('length'))}|digest={clean(r.get('digest'))}|original={clean(r.get('original'))}")
            status_map[fid]=tuple(vals)
        except Exception as e:
            errors.append((f"cdx:{fid}",type(e).__name__,str(e)))
    for s,k,m in errors:
        print(f"ERROR|scope={clean(s)}|kind={k}|message={clean(m)}")
    only500=bool(status_map.get(35)) and set(status_map[35])=={"500"}
    red36=any(x.startswith("30") and x!="300" for x in status_map.get(36,()))
    red37=any(x.startswith("30") and x!="300" for x in status_map.get(37,()))
    print(f"CLASS|fileid35_only_http500={int(only500)}|fileid36_has_redirect_status={int(red36)}|fileid37_has_redirect_status={int(red37)}")
    print(f"COUNT|errors|{len(errors)}")
    if only500 and red36 and red37:
        print("RESOLUTION|FILEID35_EXCLUDED_36_37_SCREEN_SAVER_CONTROLS|remove 35 adjacency heuristic from full-client recovery queue")
    else:
        print("RESOLUTION|FILEID35_37_BINDING_PARTIAL|retain only directly proven page associations")
    print("EVIDENCE_BOUNDARY|Page DOM can bind controls to visible labels; it does not identify unarchived target bytes. HTTP 500 rows are not download-payload evidence.")

if __name__=="__main__":main()
