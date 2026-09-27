#!/usr/bin/env python3
"""Recover the unc collapsed Waei www9 game-trial download timeline.

Prior broad censuses used collapse=urlkey, which intentionally retained only one
capture per URL. That is unsuitable for the Jan-2001 StoneAge trial-download
question because the same Dcat_ID=2 listing could have changed after Dec-2000.

This probe:
- requests *all* archived captures of the trial category and root download page
  from 2000-12-01 through 2001-01-12 without urlkey collapse;
- replays bounded HTML only and extracts StoneAge / trial / size signals plus
  downloading.php?ID=N links;
- enumerates archived downloading.php?ID= routes as CDX metadata only.

No candidate game binary is downloaded.
"""
from __future__ import annotations

import hashlib
import html
import json
import re
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
FROM="20001201"
TO="20010112"
MAX_BODY=1024*1024

TARGETS=(
    ("trial-cat","http://www9.waei.net/download.php?Dcat_ID=2"),
    ("trial-cat-port80","http://www9.waei.net:80/download.php?Dcat_ID=2"),
    ("root","http://www9.waei.net/download.php"),
    ("root-port80","http://www9.waei.net:80/download.php"),
)
ID_PREFIXES=(
    ("id-prefix","http://www9.waei.net/download/downloading.php?ID="),
    ("id-prefix-port80","http://www9.waei.net:80/download/downloading.php?ID="),
)

STONE=("stoneage","stone age","石器時代","石器时代","石器")
TRIAL=("試玩","试玩","測試","测试","trial","demo")
SIZE_RE=re.compile(r"(?<!\d)(27[0-9](?:\.\d+)?)\s*(?:m|mb|兆)",re.I)
ID_RE=re.compile(r"(?:[?&]ID=)(\d+)",re.I)

def clean(v,n=5000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=45,max_bytes=MAX_BODY):
    req=urllib.request.Request(url,headers={
        "User-Agent":UA,
        "Accept":"application/json,text/html,text/plain,*/*;q=0.2",
        "Accept-Encoding":"identity",
    })
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        if len(b)>max_bytes:
            raise ValueError(f"response-too-large:{len(b)}")
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b

def cdx_url(original,match_type="exact",limit=20000):
    params=[
        ("url",original),("matchType",match_type),("output","json"),
        ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
        ("from",FROM),("to",TO),("limit",str(limit)),
    ]
    # Intentionally NO collapse=urlkey.
    return CDX+"?"+urllib.parse.urlencode(params)

def rows(body):
    obj=json.loads(body.decode("utf-8"))
    if not isinstance(obj,list) or len(obj)<2:
        return ()
    h=obj[0]
    return tuple(dict(zip(h,r)) for r in obj[1:] if isinstance(r,list))

def replay_url(ts,orig):
    return f"https://web.archive.org/web/{ts}id_/{orig}"

def decode(body):
    for enc in ("big5","gb18030","gbk","utf-8","latin1"):
        try:
            return enc,body.decode(enc)
        except UnicodeDecodeError:
            pass
    return "latin1",body.decode("latin1","replace")

def plain_text(text):
    p=re.sub(r"(?is)<script.*?</script>|<style.*?</style>"," ",text)
    p=html.unescape(re.sub(r"(?s)<[^>]+>"," ",p))
    return re.sub(r"\s+"," ",p)

def title(text):
    m=re.search(r"(?is)<title[^>]*>(.*?)</title>",text)
    return clean(html.unescape(re.sub(r"(?s)<[^>]+>"," ",m.group(1))) if m else "",500)

def links(text,base):
    out=[]
    for m in re.finditer(r'(?is)<a\b[^>]*href\s*=\s*["\']([^"\']+)["\'][^>]*>(.*?)</a>',text):
        href=html.unescape(m.group(1)).strip()
        anchor=clean(html.unescape(re.sub(r"(?s)<[^>]+>"," ",m.group(2))),1000)
        if not href or href.lower().startswith(("javascript:","mailto:","#")):
            continue
        out.append((urllib.parse.urljoin(base,href),anchor))
    return tuple(out)

def stone_hits(text):
    l=plain_text(text).lower()
    return tuple(t for t in STONE if t.lower() in l)

def trial_hits(text):
    l=plain_text(text).lower()
    return tuple(t for t in TRIAL if t.lower() in l)

def size_hits(text):
    return tuple(dict.fromkeys(m.group(0) for m in SIZE_RE.finditer(plain_text(text))))

def downloading_id(url):
    m=ID_RE.search(str(url or ""))
    return m.group(1) if m else ""

def snippets(text,needles=("石器時代","石器时代","stoneage","stone age","274")):
    p=plain_text(text)
    low=p.lower()
    spans=[]
    for n in needles:
        start=0
        nl=n.lower()
        while True:
            i=low.find(nl,start)
            if i<0:break
            a=max(0,i-220);b=min(len(p),i+420)
            spans.append(clean(p[a:b],1200))
            start=i+max(1,len(n))
    seen=[]
    for s in spans:
        if s not in seen:seen.append(s)
    return tuple(seen[:12])

def main():
    print("StoneAge Waei www9 unc-ollapsed trial-download timeline — R1")
    print(f"SCOPE|all captures|window={FROM}..{TO}|trial category + root HTML|downloading-ID CDX|no binary payload")
    errors=[]
    all_caps=[]
    seen_caps=set()

    for label,url in TARGETS:
        try:
            st,final,h,b=fetch(cdx_url(url),timeout=60,max_bytes=8*1024*1024)
            rr=rows(b)
            print(f"CDX|label={label}|status={st}|rows={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
            for r in rr:
                key=(r.get("timestamp"),r.get("original"),r.get("digest"))
                if key in seen_caps:continue
                seen_caps.add(key);all_caps.append((label,r))
                print("CAPTURE|label={}|timestamp={}|status={}|mime={}|length={}|digest={}|redirect={}|original={}".format(
                    label,clean(r.get("timestamp")),clean(r.get("statuscode")),clean(r.get("mimetype")),
                    clean(r.get("length")),clean(r.get("digest")),clean(r.get("redirect")),clean(r.get("original"))
                ))
        except Exception as exc:
            errors.append((f"cdx:{label}",type(exc).__name__,str(exc)))

    # Replay unique HTML captures in chronological order. Bound by distinct timestamp+digest.
    all_caps.sort(key=lambda x:str(x[1].get("timestamp") or ""))
    replayed=0;stone_pages=0;size_pages=0
    timeline_ids={}
    for idx,(label,r) in enumerate(all_caps,1):
        if str(r.get("statuscode") or "") not in ("","200"):continue
        ts=str(r.get("timestamp") or "");orig=str(r.get("original") or "")
        try:
            st,final,h,b=fetch(replay_url(ts,orig),timeout=40,max_bytes=MAX_BODY)
            enc,text=decode(b);replayed+=1
            sh=stone_hits(text);th=trial_hits(text);zh=size_hits(text)
            if sh:stone_pages+=1
            if zh:size_pages+=1
            ls=links(text,orig)
            ids=[]
            for href,anchor in ls:
                did=downloading_id(href)
                if did:
                    ids.append((did,href,anchor))
            timeline_ids.setdefault(ts,set()).update(d for d,_,_ in ids)
            print(f"PAGE|index={idx}|label={label}|timestamp={ts}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|encoding={enc}|title={title(text)}|stone={clean(','.join(sh),500)}|trial={clean(','.join(th),500)}|size_tokens={clean(','.join(zh),500)}|download_ids={','.join(sorted({d for d,_,_ in ids},key=int))}|links={len(ls)}|original={clean(orig)}")
            for d,href,anchor in ids:
                print(f"ID_LINK|timestamp={ts}|id={d}|anchor={clean(anchor,1000)}|href={clean(href)}")
            if sh or zh:
                for s in snippets(text):
                    print(f"SNIPPET|timestamp={ts}|text={s}")
        except Exception as exc:
            errors.append((f"replay:{label}:{ts}:{orig}",type(exc).__name__,str(exc)))

    # Enumerate archived ID-router URLs without replaying payloads.
    id_rows={}
    for label,prefix in ID_PREFIXES:
        try:
            st,final,h,b=fetch(cdx_url(prefix,"prefix",50000),timeout=60,max_bytes=12*1024*1024)
            rr=rows(b)
            print(f"ID_CDX|label={label}|status={st}|rows={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
            for r in rr:
                did=downloading_id(r.get("original"))
                if not did:continue
                key=(did,str(r.get("timestamp") or ""),str(r.get("original") or ""),str(r.get("digest") or ""))
                id_rows[key]=r
        except Exception as exc:
            errors.append((f"id-cdx:{label}",type(exc).__name__,str(exc)))

    for (did,ts,orig,digest),r in sorted(id_rows.items(),key=lambda x:(int(x[0][0]),x[0][1])):
        print("ID_CAPTURE|id={}|timestamp={}|status={}|mime={}|length={}|digest={}|redirect={}|original={}".format(
            did,clean(ts),clean(r.get("statuscode")),clean(r.get("mimetype")),clean(r.get("length")),
            clean(digest),clean(r.get("redirect")),clean(orig)
        ))

    # Emit ID-set deltas between chronological listing snapshots.
    prev=set()
    for ts in sorted(timeline_ids):
        cur=set(timeline_ids[ts])
        added=sorted(cur-prev,key=int)
        removed=sorted(prev-cur,key=int)
        print(f"ID_SET|timestamp={ts}|count={len(cur)}|ids={','.join(sorted(cur,key=int))}|added={','.join(added)}|removed={','.join(removed)}")
        prev=cur

    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|unique_listing_captures|{len(all_caps)}")
    print(f"COUNT|pages_replayed|{replayed}")
    print(f"COUNT|stone_pages|{stone_pages}")
    print(f"COUNT|size274_pages|{size_pages}")
    print(f"COUNT|archived_router_rows|{len(id_rows)}")
    print(f"COUNT|archived_router_ids|{len({k[0] for k in id_rows})}")
    print(f"COUNT|errors|{len(errors)}")

    if stone_pages and size_pages:
        print("RESOLUTION|STONEAGE_274_TIMELINE_SIGNAL_FOUND|bind listing entry to exact downloading ID then recover redirect metadata")
    elif stone_pages:
        print("RESOLUTION|STONEAGE_LISTING_SIGNAL_FOUND|bind exact ID/title/size next")
    elif len(all_caps)>2:
        print("RESOLUTION|TIMELINE_RECOVERED_NO_STONEAGE_SIGNAL|inspect ID deltas and adjacent captures")
    elif errors:
        print("RESOLUTION|PARTIAL_TIMELINE|retry only failed archive surfaces")
    else:
        print("RESOLUTION|NO_ADDITIONAL_TIMELINE_CAPTURES|current archive lacks later trial-category snapshots")
    print("EVIDENCE_BOUNDARY|Listing HTML and CDX router metadata establish catalogue/routing only; no candidate game payload is downloaded or authenticated.")

if __name__=="__main__":
    main()
