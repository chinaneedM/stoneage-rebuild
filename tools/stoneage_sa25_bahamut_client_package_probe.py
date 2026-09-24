#!/usr/bin/env python3
"""Resolve Bahamut StoneAge 2.5 client-package collector article snA=81400.

Text/HTML and archive metadata only. Image bodies and game payloads are not
downloaded. The goal is to map package variants and exact image ordering.
"""
from __future__ import annotations
import hashlib, html, json, re, time, urllib.parse, urllib.request
from tools.stoneage_sa25_host_identity_probe import declared_charset, decode, title, visible

UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/153 Safari/537.36"
CDX="https://web.archive.org/cdx/search/cdx"
TARGETS=(
    "https://forum.gamer.com.tw/C.php?bsn=1571&snA=81400",
    "https://forum.gamer.com.tw/C.php?bsn=01571&snA=81400",
    "https://forum.gamer.com.tw/Co.php?bsn=1571&sn=295378",
)
TOKENS=("石器時代","2.5","精靈王傳說","精灵王传说","用戶端","客户端","WGS","新手","簡裝","简装","stoneage2017","寂寞如風")
CONTENT_RE=re.compile(r'https://cos\.stoneage\.cn/uploads/article/minisnsimg/[0-9]{8}/[A-Za-z0-9_.-]+',re.I)
ATTR_RE=re.compile(r"""(?is)(?:href|src|data-src|data-original)\s*=\s*["']([^"']+)["']""")

def clean(v,n=12000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=20,max_bytes=3_000_000,attempts=2):
    last=None
    for n in range(attempts):
        try:
            req=urllib.request.Request(url,headers={
                "User-Agent":UA,"Accept":"text/html,application/json,*/*",
                "Accept-Language":"zh-TW,zh;q=0.9,en;q=0.5"
            })
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
        ("from","2020"),("to","2026"),("limit","200"),
    ])

def parse_cdx(b):
    d=json.loads(b.decode("utf-8","replace"))
    if not isinstance(d,list) or not d or not isinstance(d[0],list): return ()
    h=d[0]
    return tuple(dict(zip(h,row)) for row in d[1:] if isinstance(row,list))

def token_hits(body,text):
    low=text.lower(); out=[]
    for t in TOKENS:
        yes=t.lower() in low
        if not yes and any(ord(c)>127 for c in t):
            for enc in ("utf-8","big5","cp950","gb18030"):
                try:
                    if t.encode(enc) in body: yes=True; break
                except Exception: pass
        if yes: out.append(t)
    return tuple(out)

def image_sequence(text):
    out=[]; seen=set()
    for m in CONTENT_RE.finditer(text):
        u=html.unescape(m.group(0))
        if u not in seen:
            seen.add(u); out.append((m.start(),u))
    return tuple(out)

def preceding_segments(text,seq):
    start=0; out=[]
    for pos,u in seq:
        out.append((u,visible(text[start:pos])))
        start=pos+len(u)
    return tuple(out)

def related_attrs(text):
    out=[]; seen=set()
    for raw in ATTR_RE.findall(text):
        u=html.unescape(raw.strip()); low=u.lower()
        if any(k in low for k in ("81400","81429","stoneage","shiqi","minisnsimg","gamer.com.tw")):
            if u not in seen:
                seen.add(u); out.append(u)
    return tuple(out)

def emit_page(label,st,final,b):
    enc,text=decode(b,declared_charset(b)); hh=token_hits(b,text)
    seq=image_sequence(text); seg=preceding_segments(text,seq); aa=related_attrs(text)
    print(
        f"PAGE|label={clean(label)}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|"
        f"encoding={clean(enc)}|title={clean(title(text),1800)}|tokens={clean(','.join(hh))}|"
        f"images={len(seq)}|attrs={len(aa)}|final={clean(final)}"
    )
    print(f"TEXT|label={clean(label)}|value={clean(visible(text),18000)}")
    for i,(pos,u) in enumerate(seq,1):
        print(f"IMAGE_URL|label={clean(label)}|order={i}|url={clean(u)}")
        print(f"IMAGE_PRECEDING|label={clean(label)}|order={i}|value={clean(seg[i-1][1],12000)}")
    for i,u in enumerate(aa[:120],1):
        print(f"ATTR|label={clean(label)}|order={i}|value={clean(u,5000)}")
    return bool(hh), len(seq)

def main():
    print("StoneAge 2.5 Bahamut client-package article resolution — R1")
    print("SCOPE|public-page+wayback-html-metadata|snA-81400|no-image-body|no-game-payload")
    errors=[]; live_hits=0; archive_hits=0; image_urls=0
    for i,u in enumerate(TARGETS):
        try:
            st,final,h,b=fetch(u,20,3_000_000,2)
            hit,n=emit_page(f"live:{i}",st,final,b); image_urls=max(image_urls,n)
            if hit: live_hits+=1
        except Exception as e:
            errors.append((f"live:{i}",type(e).__name__,str(e)))
        try:
            st,final,h,b=fetch(cdx_url(u),20,2_000_000,2)
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
                    st2,final2,h2,b2=fetch(ru,20,3_000_000,2)
                    hit,n=emit_page(f"archive:{r.get('timestamp')}",st2,final2,b2); image_urls=max(image_urls,n)
                    if hit: archive_hits+=1
                except Exception as e:
                    errors.append((f"archive:{r.get('timestamp')}",type(e).__name__,str(e)))
                if len(seen)>=2: break
        except Exception as e:
            errors.append((f"cdx:{i}",type(e).__name__,str(e)))
    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|live_token_pages|{live_hits}")
    print(f"COUNT|archive_token_pages|{archive_hits}")
    print(f"COUNT|max_image_urls|{image_urls}")
    print(f"COUNT|errors|{len(errors)}")
    if live_hits or archive_hits:
        print("RESOLUTION|SA25_CLIENT_PACKAGE_ARTICLE_RESOLVED|classify package variants and exact image order")
    else:
        print("RESOLUTION|SA25_CLIENT_PACKAGE_ARTICLE_UNRESOLVED|retain public-search text as discovery lead only")
    print("EVIDENCE_BOUNDARY|collector article text/image order can identify package/carrier classes; it does not prove filesystem, mastering, or clean-client byte provenance.")

if __name__=="__main__":
    main()
