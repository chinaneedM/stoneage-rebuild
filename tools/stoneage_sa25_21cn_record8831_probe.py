#!/usr/bin/env python3
"""Trace 21CN list.php?id=8831, the nearest archived detail page before sa25up.jpg.

HTML/archive metadata only. No linked software payload is fetched.
"""
from __future__ import annotations
import hashlib, html, json, re, time, urllib.parse, urllib.request
from tools.stoneage_sa25_host_identity_probe import declared_charset, decode, title, visible

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
ID="8831"
HOSTS=("202.104.32.168","download.21cn.com")
TOKENS=("sa25up.jpg","sa25up.zip","石器时代","石器時代","精灵王","精靈王","stoneage","stone age")
ATTR_RE=re.compile(r"""(?is)(?:href|src)\s*=\s*["']?([^"'\s>]+)""")

def clean(v,limit=2400):
    return " ".join(str(v or "").split()).replace("|","%7C")[:limit]

def fetch(url,timeout=30,max_bytes=2_000_000,attempts=1):
    last=None
    for attempt in range(attempts):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/html,*/*"})
            with urllib.request.urlopen(req,timeout=timeout) as r:
                b=r.read(max_bytes+1)
                if len(b)>max_bytes: raise ValueError("response-too-large")
                return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b
        except Exception as exc:
            last=exc
            if attempt+1<attempts:
                time.sleep(1.5*(attempt+1))
    raise last

def cdx_url(url,match="exact",limit=300):
    p=[("url",url),("matchType",match),("output","json"),
       ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
       ("from","2001"),("to","2004"),("limit",str(limit))]
    return CDX+"?"+urllib.parse.urlencode(p)

def parse(body):
    d=json.loads(body.decode("utf-8","replace"))
    if not isinstance(d,list) or not d or not isinstance(d[0],list): return ()
    h=d[0]
    return tuple(dict(zip(h,row)) for row in d[1:] if isinstance(row,list))

def replay(row):
    return f"https://web.archive.org/web/{row['timestamp']}id_/{row['original']}"

def token_hits(body,text):
    hits=[]; low=text.lower()
    for t in TOKENS:
        found=t.lower() in low
        if not found and any(ord(ch)>127 for ch in t):
            for enc in ("gb2312","gbk","gb18030","big5","cp950"):
                try:
                    if t.encode(enc) in body: found=True; break
                except Exception: pass
        if found: hits.append(t)
    return tuple(dict.fromkeys(hits))

def attrs(text):
    out=[]; seen=set()
    for raw in ATTR_RE.findall(text):
        v=html.unescape(raw.strip()); low=v.lower()
        if "sa25" in low or "stoneage" in low or "/file/game/" in low or "downit.php" in low or ID in low:
            if v not in seen: seen.add(v); out.append(v)
    return tuple(out)

def context(text,hits,radius=900):
    v=visible(text); low=v.lower()
    pos=[low.find(t.lower()) for t in hits]
    pos=[x for x in pos if x>=0]
    if not pos: return v[:2400]
    i=min(pos); return v[max(0,i-radius):min(len(v),i+radius*2)]

def main():
    print("StoneAge 2.5 21CN record 8831 trace — R1")
    print("SCOPE|nearest-crawl-detail-page|html+cdx-only|no-linked-software-payload")
    errors=[]; rows=[]
    for host in HOSTS:
        url=f"http://{host}/list.php?id={ID}"
        try:
            st,final,hdr,b=fetch(cdx_url(url),30,2_000_000,2)
            rr=parse(b)
            print(f"CDX|host={host}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|rows={len(rr)}|final={clean(final)}")
            for r in rr:
                rows.append(r)
                print(f"CDX_ROW|timestamp={clean(r.get('timestamp'))}|original={clean(r.get('original'))}|status={clean(r.get('statuscode'))}|mime={clean(r.get('mimetype'))}|length={clean(r.get('length'))}|digest={clean(r.get('digest'))}|redirect={clean(r.get('redirect'))}")
        except Exception as e:
            errors.append((f"cdx:{host}",type(e).__name__,str(e)))

    seen=set()
    for r in sorted(rows,key=lambda x:(str(x.get("timestamp") or ""),str(x.get("original") or ""))):
        key=(str(r.get("timestamp") or ""),str(r.get("original") or ""))
        if key in seen: continue
        seen.add(key)
        try:
            st,final,hdr,b=fetch(replay(r),30,1_500_000,4)
            enc,text=decode(b,declared_charset(b)); hits=token_hits(b,text); aa=attrs(text)
            print(f"PAGE|timestamp={clean(r.get('timestamp'))}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|encoding={clean(enc)}|title={clean(title(text),1400)}|tokens={clean(','.join(hits))}|attrs={len(aa)}|final={clean(final)}")
            print(f"CONTEXT|timestamp={clean(r.get('timestamp'))}|value={clean(context(text,hits),3600)}")
            for n,a in enumerate(aa[:100],1):
                print(f"ATTR|order={n}|value={clean(a)}")
        except Exception as e:
            errors.append((f"replay:{key[0]}",type(e).__name__,str(e)))

    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|archive_rows|{len(rows)}")
    print(f"COUNT|errors|{len(errors)}")
    print("RESOLUTION|RECORD_8831_TRACED|accept relation to sa25up only if page/path evidence explicitly connects them")
    print("EVIDENCE_BOUNDARY|crawl proximity alone is not parent-child evidence.")

if __name__=="__main__":
    main()
