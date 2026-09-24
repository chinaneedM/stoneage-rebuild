#!/usr/bin/env python3
"""Trace native 21CN StoneAge 2.5 catalogue record id=20165.

HTML/CDX metadata only. The probe does not follow or download historical game payloads.
"""
from __future__ import annotations
import concurrent.futures, hashlib, html, json, re, time, urllib.parse, urllib.request
from tools.stoneage_sa25_host_identity_probe import declared_charset, decode, title, visible

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
ID="20165"
HOSTS=("202.104.32.168","download.21cn.com")
TOKENS=("石器时代2.5","石器時代2.5","精灵王","精靈王","sa25up","stoneage")
ATTR_RE=re.compile(r"""(?is)(?:href|src)\s*=\s*["']?([^"'\s>]+)""")

def clean(v,limit=3600):
    return " ".join(str(v or "").split()).replace("|","%7C")[:limit]

def fetch(url,timeout=30,max_bytes=3_000_000,attempts=3):
    last=None
    for n in range(attempts):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/html,*/*"})
            with urllib.request.urlopen(req,timeout=timeout) as r:
                b=r.read(max_bytes+1)
                if len(b)>max_bytes: raise ValueError("response-too-large")
                return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b
        except Exception as e:
            last=e
            if n+1<attempts: time.sleep(1.2*(n+1))
    raise last

def cdx_url(url,match="exact",limit=1000):
    p=[("url",url),("matchType",match),("output","json"),
       ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
       ("from","2001"),("to","2005"),("limit",str(limit))]
    return CDX+"?"+urllib.parse.urlencode(p)

def parse(body):
    d=json.loads(body.decode("utf-8","replace"))
    if not isinstance(d,list) or not d or not isinstance(d[0],list): return ()
    h=d[0]; return tuple(dict(zip(h,row)) for row in d[1:] if isinstance(row,list))

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

def relevant_attrs(text):
    out=[]; seen=set()
    for raw in ATTR_RE.findall(text):
        v=html.unescape(raw.strip()); low=v.lower()
        if (
            "downit.php" in low or "sa25up" in low or "stoneage" in low
            or "/file/game/" in low or ID in low
        ):
            if v not in seen: seen.add(v); out.append(v)
    return tuple(out)

def context(text,hits,radius=1300):
    v=visible(text); low=v.lower()
    pos=[]
    for t in hits:
        i=low.find(t.lower())
        if i>=0: pos.append(i)
    if not pos:
        # The page title/metadata is still valuable.
        return v[:5000]
    i=min(pos); return v[max(0,i-radius):min(len(v),i+radius*3)]

def emit_rows(label,rows):
    print(f"CDX_COUNT|label={label}|rows={len(rows)}")
    for r in rows:
        print(
            f"CDX_ROW|label={label}|timestamp={clean(r.get('timestamp'))}|original={clean(r.get('original'))}|"
            f"status={clean(r.get('statuscode'))}|mime={clean(r.get('mimetype'))}|length={clean(r.get('length'))}|"
            f"digest={clean(r.get('digest'))}|redirect={clean(r.get('redirect'))}"
        )

def main():
    print("StoneAge 2.5 exact 21CN catalogue record 20165 — R1")
    print("SCOPE|native-list-record+downit+file-neighborhood|html/cdx-only|no-game-payload")
    errors=[]; listrows=[]
    for host in HOSTS:
        label=f"list-{host}"
        url=f"http://{host}/list.php?id={ID}"
        try:
            st,final,hdr,b=fetch(cdx_url(url),35,3_000_000,2)
            rr=parse(b); emit_rows(label,rr)
            print(f"CDX_QUERY|label={label}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
            listrows.extend(rr)
        except Exception as e:
            errors.append((label,type(e).__name__,str(e)))

    # Prefer earliest captures and replay them concurrently with strict bounds.
    seen=set(); selected=[]
    for r in sorted(listrows,key=lambda x:(str(x.get("timestamp") or ""),str(x.get("original") or ""))):
        key=(str(r.get("timestamp") or ""),str(r.get("original") or ""))
        if key in seen: continue
        seen.add(key); selected.append(r)
        if len(selected)>=10: break

    def inspect(r):
        key=(str(r.get("timestamp") or ""),str(r.get("original") or ""))
        try:
            st,final,hdr,b=fetch(replay(r),18,2_000_000,2)
            enc,text=decode(b,declared_charset(b)); hits=token_hits(b,text); aa=relevant_attrs(text)
            return r,st,final,b,enc,text,hits,aa,None
        except Exception as e:
            return r,None,None,None,None,None,(),(),(type(e).__name__,str(e))

    replayed=0
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
        for r,st,final,b,enc,text,hits,aa,error in ex.map(inspect,selected):
            ts=str(r.get("timestamp") or "")
            if error:
                errors.append((f"replay:{ts}",error[0],error[1])); continue
            replayed+=1
            print(
                f"PAGE|timestamp={clean(ts)}|original={clean(r.get('original'))}|status={st}|"
                f"bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|encoding={clean(enc)}|"
                f"title={clean(title(text),1800)}|tokens={clean(','.join(hits))}|attrs={len(aa)}|final={clean(final)}"
            )
            print(f"CONTEXT|timestamp={clean(ts)}|value={clean(context(text,hits),7000)}")
            for n,a in enumerate(aa[:100],1):
                print(f"ATTR|timestamp={clean(ts)}|order={n}|value={clean(a,2400)}")

    # CDX-only metadata queries; run concurrently and never replay downit.
    targets=[
        (f"downit-{host}",f"http://{host}/downit.php?id={ID}","prefix")
        for host in HOSTS
    ] + [
        ("host-sa25up-jpg","http://download.21cn.com/file/game/maoxian/sa25up.jpg","exact"),
        ("host-sa25up-zip","http://download.21cn.com/file/game/maoxian/sa25up.zip","exact"),
        ("ip-sa25up-jpg","http://202.104.32.168/file/game/maoxian/sa25up.jpg","exact"),
        ("ip-sa25up-zip","http://202.104.32.168/file/game/maoxian/sa25up.zip","exact"),
        ("host-id-dir",f"http://download.21cn.com/file/game/maoxian/{ID}/","prefix"),
        ("ip-id-dir",f"http://202.104.32.168/file/game/maoxian/{ID}/","prefix"),
    ]

    def query_target(entry):
        label,url,match=entry
        try:
            st,final,hdr,b=fetch(cdx_url(url,match,1000),18,3_000_000,2)
            return label,st,final,b,parse(b),None
        except Exception as e:
            return label,None,None,None,(),(type(e).__name__,str(e))

    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
        for label,st,final,b,rr,error in ex.map(query_target,targets):
            if error:
                errors.append((label,error[0],error[1])); continue
            emit_rows(label,rr)
            print(f"CDX_QUERY|label={label}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")

    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|list_rows|{len(listrows)}")
    print(f"COUNT|replayed_pages|{replayed}")
    print(f"COUNT|errors|{len(errors)}")
    if replayed:
        print("RESOLUTION|NATIVE_21CN_STONEAGE25_RECORD_TRACED|classify page fields and explicit file/downit relation")
    else:
        print("RESOLUTION|NATIVE_21CN_STONEAGE25_RECORD_INDEXED_BUT_REPLAY_FAILED|retry exact captures only")
    print("EVIDENCE_BOUNDARY|native catalogue metadata establishes what 21CN described/distributed; payload integrity still requires bytes or an operator chain.")

if __name__=="__main__":
    main()
