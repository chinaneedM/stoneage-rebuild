#!/usr/bin/env python3
"""Resolve the inferred Bahamut StoneAge collector 'disc article part II'.

The surrounding series is publicly indexed at snA=81430 (part I), 81428
(part III), and 81427 (part IV), while those pages link to part II. This probe
tests the intervening snA=81429 as a discovery hypothesis and checks Wayback.
Text/HTML metadata only; image bodies and game payloads are not downloaded.
"""
from __future__ import annotations
import hashlib, html, json, re, time, urllib.parse, urllib.request
from tools.stoneage_sa25_host_identity_probe import declared_charset, decode, title, visible

UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/153 Safari/537.36"
CDX="https://web.archive.org/cdx/search/cdx"
TARGETS=(
    "https://forum.gamer.com.tw/C.php?bsn=1571&snA=81429",
    "https://forum.gamer.com.tw/C.php?bsn=01571&snA=81429",
    "https://forum.gamer.com.tw/C.php?page=1&bsn=1571&snA=81429",
)
TOKENS=("石器時代","石器时代","光碟篇","光盘篇","2.5","精靈王","精灵王","stoneage2017","寂寞如風")
ATTR_RE=re.compile(r"""(?is)(?:href|src|data-src|data-original)\s*=\s*["']([^"']+)["']""")

def clean(v,n=6000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=20,max_bytes=3_000_000,attempts=2):
    last=None
    for n in range(attempts):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"text/html,application/json,*/*","Accept-Language":"zh-TW,zh;q=0.9,en;q=0.5"})
            with urllib.request.urlopen(req,timeout=timeout) as r:
                b=r.read(max_bytes+1)
                if len(b)>max_bytes: raise ValueError("response-too-large")
                return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b
        except Exception as e:
            last=e
            if n+1<attempts: time.sleep(1.2)
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

def attrs(text):
    out=[]; seen=set()
    for raw in ATTR_RE.findall(text):
        u=html.unescape(raw.strip())
        low=u.lower()
        if any(k in low for k in ("bahamut","gamer.com.tw","stoneage","shiqi","upload","jpg","jpeg","png","webp")):
            if u not in seen:
                seen.add(u); out.append(u)
    return tuple(out)

def hits(body,text):
    out=[]
    low=text.lower()
    for t in TOKENS:
        yes=t.lower() in low
        if not yes and any(ord(c)>127 for c in t):
            for enc in ("utf-8","big5","cp950","gb18030"):
                try:
                    if t.encode(enc) in body: yes=True; break
                except Exception: pass
        if yes: out.append(t)
    return tuple(out)

def emit_page(label,st,final,h,b):
    enc,text=decode(b,declared_charset(b)); hh=hits(b,text); aa=attrs(text)
    print(f"PAGE|label={label}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|encoding={clean(enc)}|title={clean(title(text),1500)}|tokens={clean(','.join(hh))}|attrs={len(aa)}|final={clean(final)}")
    print(f"TEXT|label={label}|value={clean(visible(text),12000)}")
    for i,u in enumerate(aa[:200],1):
        print(f"ATTR|label={label}|order={i}|value={clean(u,4000)}")
    return hh

def main():
    print("StoneAge Bahamut collector disc article part-II resolution — R1")
    print("SCOPE|public-page+wayback-metadata/html|resolve-snA-81429|no-image-body|no-game-payload")
    errors=[]; live_hits=0; archive_hits=0
    for i,u in enumerate(TARGETS):
        try:
            st,final,h,b=fetch(u,18,3_000_000,2)
            hh=emit_page(f"live:{i}",st,final,h,b)
            if hh: live_hits+=1
        except Exception as e:
            errors.append((f"live:{i}",type(e).__name__,str(e)))
        try:
            st,final,h,b=fetch(cdx_url(u),20,2_000_000,2)
            rows=parse_cdx(b)
            print(f"CDX|target={clean(u)}|status={st}|rows={len(rows)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
            for r in rows:
                print(f"CDX_ROW|timestamp={clean(r.get('timestamp'))}|original={clean(r.get('original'))}|status={clean(r.get('statuscode'))}|mime={clean(r.get('mimetype'))}|length={clean(r.get('length'))}|digest={clean(r.get('digest'))}|redirect={clean(r.get('redirect'))}")
            seen=set()
            for r in rows:
                if str(r.get("statuscode") or "")!="200": continue
                dg=str(r.get("digest") or "")
                if dg and dg in seen: continue
                if dg: seen.add(dg)
                try:
                    ru=f"https://web.archive.org/web/{r['timestamp']}id_/{r['original']}"
                    st2,final2,h2,b2=fetch(ru,18,3_000_000,2)
                    hh=emit_page(f"archive:{r.get('timestamp')}",st2,final2,h2,b2)
                    if hh: archive_hits+=1
                except Exception as e:
                    errors.append((f"archive:{r.get('timestamp')}",type(e).__name__,str(e)))
                if len(seen)>=3: break
        except Exception as e:
            errors.append((f"cdx:{i}",type(e).__name__,str(e)))
    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|live_token_pages|{live_hits}")
    print(f"COUNT|archive_token_pages|{archive_hits}")
    print(f"COUNT|errors|{len(errors)}")
    if live_hits or archive_hits:
        print("RESOLUTION|SNA_81429_RESPONDED_WITH_STONEAGE_COLLECTOR_CONTEXT|classify exact part/version and extract image URLs")
    else:
        print("RESOLUTION|SNA_81429_UNRESOLVED|retain as sequence-derived hypothesis only")
    print("EVIDENCE_BOUNDARY|sequence adjacency is a discovery heuristic until page body/title confirms part II; collector text/images do not prove disc bytes.")

if __name__=="__main__":
    main()
