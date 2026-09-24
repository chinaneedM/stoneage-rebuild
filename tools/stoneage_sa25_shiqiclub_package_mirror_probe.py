#!/usr/bin/env python3
"""Trace the shiqi.club mirror of the StoneAge 2.5 client-package article.

The public archiver index maps the article to /shiqi2712.html. This probe checks
that exact mirror URL and its Wayback history, extracting text and image URLs only.
No image or game payload bodies are downloaded.
"""
from __future__ import annotations
import hashlib, html, json, re, time, urllib.parse, urllib.request
from tools.stoneage_sa25_host_identity_probe import declared_charset, decode, title, visible

UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/153 Safari/537.36"
CDX="https://web.archive.org/cdx/search/cdx"
TARGETS=(
    "https://www.shiqi.club/shiqi2712.html",
    "http://www.shiqi.club/shiqi2712.html",
    "https://shiqi.club/shiqi2712.html",
    "http://shiqi.club/shiqi2712.html",
)
TOKENS=("2.5精灵王传说","2.5精靈王傳說","客户端礼包","用戶端禮包","WGS","新手包","简装","簡裝","精灵王","精靈王")
ATTR_RE=re.compile(r"""(?is)(?:href|src|data-src|data-original)\s*=\s*["']([^"']+)["']""")

def clean(v,n=14000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=18,max_bytes=3_000_000,attempts=2):
    last=None
    for n in range(attempts):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"text/html,application/json,*/*","Accept-Language":"zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.5"})
            with urllib.request.urlopen(req,timeout=timeout) as r:
                b=r.read(max_bytes+1)
                if len(b)>max_bytes: raise ValueError("response-too-large")
                return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b
        except Exception as e:
            last=e
            if n+1<attempts: time.sleep(1.0)
    raise last

def cdx_url(url):
    return CDX+"?"+urllib.parse.urlencode([
        ("url",url),("matchType","exact"),("output","json"),
        ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
        ("from","2019"),("to","2026"),("limit","500"),
    ])

def parse_cdx(b):
    d=json.loads(b.decode("utf-8","replace"))
    if not isinstance(d,list) or not d or not isinstance(d[0],list): return ()
    h=d[0]
    return tuple(dict(zip(h,row)) for row in d[1:] if isinstance(row,list))

def hits(body,text):
    low=text.lower(); out=[]
    for t in TOKENS:
        yes=t.lower() in low
        if not yes and any(ord(c)>127 for c in t):
            for enc in ("utf-8","gb18030","big5","cp950"):
                try:
                    if t.encode(enc) in body: yes=True; break
                except Exception: pass
        if yes: out.append(t)
    return tuple(out)

def relevant_attrs(text):
    out=[]; seen=set()
    for raw in ATTR_RE.findall(text):
        u=html.unescape(raw.strip()); low=u.lower()
        if any(k in low for k in ("2712","stoneage","shiqi","upload","jpg","jpeg","png","gif","webp")):
            if u not in seen:
                seen.add(u); out.append(u)
    return tuple(out)

def emit(label,st,final,b):
    enc,text=decode(b,declared_charset(b)); hh=hits(b,text); aa=relevant_attrs(text)
    print(
        f"PAGE|label={clean(label)}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|"
        f"encoding={clean(enc)}|title={clean(title(text),1800)}|tokens={clean(','.join(hh))}|attrs={len(aa)}|final={clean(final)}"
    )
    print(f"TEXT|label={clean(label)}|value={clean(visible(text),22000)}")
    for i,u in enumerate(aa[:200],1):
        print(f"ATTR|label={clean(label)}|order={i}|value={clean(u,5000)}")
    return bool(hh)

def main():
    print("StoneAge 2.5 shiqi.club client-package mirror trace — R1")
    print("SCOPE|exact-mirror-url+wayback-html|text/image-url-only|no-image-body|no-game-payload")
    errors=[]; live=0; archived=0
    for i,u in enumerate(TARGETS):
        try:
            st,final,h,b=fetch(u,15,3_000_000,1)
            if emit(f"live:{i}",st,final,b): live+=1
        except Exception as e:
            errors.append((f"live:{i}",type(e).__name__,str(e)))
        try:
            st,final,h,b=fetch(cdx_url(u),18,2_000_000,2)
            rows=parse_cdx(b)
            print(f"CDX|target={clean(u)}|status={st}|rows={len(rows)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
            for r in rows:
                print(
                    f"CDX_ROW|timestamp={clean(r.get('timestamp'))}|original={clean(r.get('original'))}|"
                    f"status={clean(r.get('statuscode'))}|mime={clean(r.get('mimetype'))}|length={clean(r.get('length'))}|"
                    f"digest={clean(r.get('digest'))}|redirect={clean(r.get('redirect'))}"
                )
            seen=set()
            for r in rows:
                if str(r.get("statuscode") or "")!="200": continue
                dg=str(r.get("digest") or "")
                if dg and dg in seen: continue
                if dg: seen.add(dg)
                try:
                    ru=f"https://web.archive.org/web/{r['timestamp']}id_/{r['original']}"
                    st2,final2,h2,b2=fetch(ru,18,3_000_000,2)
                    if emit(f"archive:{r.get('timestamp')}",st2,final2,b2): archived+=1
                except Exception as e:
                    errors.append((f"archive:{r.get('timestamp')}",type(e).__name__,str(e)))
                if len(seen)>=3: break
        except Exception as e:
            errors.append((f"cdx:{i}",type(e).__name__,str(e)))
    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|live_token_pages|{live}")
    print(f"COUNT|archive_token_pages|{archived}")
    print(f"COUNT|errors|{len(errors)}")
    if live or archived:
        print("RESOLUTION|SHIQICLUB_SA25_PACKAGE_MIRROR_RECOVERED|extract independent image URLs and package wording")
    else:
        print("RESOLUTION|SHIQICLUB_SA25_PACKAGE_MIRROR_BOUNDED|exact mirror URL no longer yields article body on tested surfaces")
    print("EVIDENCE_BOUNDARY|modern repost/mirror content can corroborate packaging and image provenance only; it cannot establish original disc bytes or mastering identity.")

if __name__=="__main__":
    main()
