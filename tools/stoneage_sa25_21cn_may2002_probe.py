#!/usr/bin/env python3
"""Focused 21CN May-2002 scan around the archived sa25up.jpg capture.

The 21CN-hosted image /file/game/maoxian/sa25up.jpg has an HTTP-200 archive record
at 2002-05-17. This probe scans only nearby archived 21CN detail pages and derives
HTML/image metadata. No linked StoneAge ZIP/client payload is downloaded.
"""
from __future__ import annotations

import hashlib
import html
import json
import re
import struct
import time
import urllib.parse
import urllib.request

from tools.stoneage_sa25_host_identity_probe import declared_charset, decode, title, visible

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
FROM="20020514"
TO="20020520"
PREFIXES=(
    ("ip","http://202.104.32.168/list.php?id="),
    ("hostname","http://download.21cn.com/list.php?id="),
)
IMAGE_TS="20020517235842"
IMAGE_URL="http://download.21cn.com:80/file/game/maoxian/sa25up.jpg"
TOKENS=("sa25up.jpg","sa25up.zip","石器时代","石器時代","精灵王","精靈王","stoneage","stone age")
ATTR_RE=re.compile(r"""(?is)(?:href|src)\s*=\s*["']?([^"'\s>]+)""")


def clean(v,limit=2200):
    return " ".join(str(v or "").split()).replace("|","%7C")[:limit]


def fetch(url,timeout=25,max_bytes=2_000_000,attempts=3):
    last=None
    for n in range(attempts):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/html,image/jpeg,*/*"})
            with urllib.request.urlopen(req,timeout=timeout) as r:
                body=r.read(max_bytes+1)
                if len(body)>max_bytes:
                    raise ValueError("response-too-large")
                return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),body
        except Exception as e:
            last=e
            if n+1<attempts:
                time.sleep(0.8*(n+1))
    raise last


def cdx_url(prefix):
    p=[
        ("url",prefix),("matchType","prefix"),("output","json"),
        ("fl","timestamp,original,statuscode,mimetype,digest,length"),
        ("from",FROM),("to",TO),("filter","statuscode:200"),
        ("filter","mimetype:text/html"),("collapse","urlkey"),("limit","1000"),
    ]
    return CDX+"?"+urllib.parse.urlencode(p)


def parse_cdx(body):
    data=json.loads(body.decode("utf-8","replace"))
    if not isinstance(data,list) or not data or not isinstance(data[0],list):
        return ()
    h=data[0]; out=[]; seen=set()
    for row in data[1:]:
        if not isinstance(row,list): continue
        d=dict(zip(h,row))
        original=str(d.get("original") or "")
        p=urllib.parse.urlsplit(original)
        if p.path.lower()!="/list.php": continue
        q=urllib.parse.parse_qs(p.query)
        if not (q.get("id") and str(q["id"][0]).isdigit()): continue
        key=(str(d.get("timestamp") or ""),original)
        if key not in seen:
            seen.add(key); out.append(d)
    return tuple(out)


def replay_url(ts,original):
    return f"https://web.archive.org/web/{ts}id_/{original}"


def page_id(url):
    try:
        return str((urllib.parse.parse_qs(urllib.parse.urlsplit(url).query).get("id") or [""])[0])
    except Exception:
        return ""


def token_hits(body,text):
    hits=[]
    low=text.lower()
    for token in TOKENS:
        found=token.lower() in low
        if not found and any(ord(ch)>127 for ch in token):
            for enc in ("gb2312","gbk","gb18030","big5","cp950"):
                try:
                    if token.encode(enc) in body:
                        found=True; break
                except Exception:
                    pass
        if found: hits.append(token)
    return tuple(dict.fromkeys(hits))


def relevant_attrs(text):
    out=[]; seen=set()
    for raw in ATTR_RE.findall(text):
        v=html.unescape(raw.strip())
        low=v.lower()
        if "sa25" in low or "stoneage" in low or "/file/game/maoxian/" in low or "downit.php" in low:
            if v not in seen:
                seen.add(v); out.append(v)
    return tuple(out)


def context(text,tokens,radius=600):
    v=visible(text); low=v.lower()
    pos=[]
    for t in tokens:
        i=low.find(t.lower())
        if i>=0: pos.append(i)
    if not pos: return ""
    i=min(pos)
    return v[max(0,i-radius):min(len(v),i+radius*2)]


def jpeg_size(body):
    if len(body)<4 or body[:2]!=b"\xff\xd8":
        return None
    i=2
    while i+4<=len(body):
        if body[i]!=0xff:
            i+=1; continue
        marker=body[i+1]; i+=2
        if marker in (0xd8,0xd9): continue
        if i+2>len(body): break
        seglen=struct.unpack(">H",body[i:i+2])[0]
        if seglen<2 or i+seglen>len(body): break
        if marker in tuple(range(0xc0,0xc4))+tuple(range(0xc5,0xc8))+tuple(range(0xc9,0xcc))+tuple(range(0xcd,0xd0)):
            if seglen>=7:
                h=struct.unpack(">H",body[i+3:i+5])[0]
                w=struct.unpack(">H",body[i+5:i+7])[0]
                return w,h,marker
        i+=seglen
    return None


def main():
    print("StoneAge 2.5 21CN May-2002 focused record probe — R1")
    print("SCOPE|2002-05-14..20-detail-html+sa25up-jpeg-metadata|no-zip-or-client-payload")
    errors=[]; rows_by_key={}
    for label,prefix in PREFIXES:
        try:
            st,final,hdr,body=fetch(cdx_url(prefix),30,2_000_000,2)
            rows=parse_cdx(body)
            print(f"CDX|label={label}|status={st}|bytes={len(body)}|sha256={hashlib.sha256(body).hexdigest()}|rows={len(rows)}|final={clean(final)}")
            for row in rows:
                rows_by_key[(str(row.get("timestamp") or ""),str(row.get("original") or ""))]=row
        except Exception as e:
            errors.append((f"cdx:{label}",type(e).__name__,str(e)))

    rows=tuple(sorted(rows_by_key.values(),key=lambda r:(str(r.get("timestamp") or ""),page_id(str(r.get("original") or "")))))
    print(f"COUNT|unique_detail_rows|{len(rows)}")
    matches=0; completed=0
    for row in rows:
        original=str(row.get("original") or ""); ts=str(row.get("timestamp") or "")
        try:
            st,final,hdr,body=fetch(replay_url(ts,original),18,1_500_000,3)
            enc,text=decode(body,declared_charset(body))
            hits=token_hits(body,text)
            attrs=relevant_attrs(text)
            completed+=1
            # Emit every page in the narrow window so ID/date progression survives,
            # but include body hash/title only; body is not stored.
            print(
                f"PAGE|id={clean(page_id(original))}|timestamp={clean(ts)}|status={st}|bytes={len(body)}|"
                f"sha256={hashlib.sha256(body).hexdigest()}|encoding={clean(enc)}|"
                f"title={clean(title(text),1200)}|tokens={clean(','.join(hits))}|attrs={len(attrs)}|original={clean(original)}"
            )
            if hits or attrs:
                matches+=1
                if hits:
                    print(f"CONTEXT|id={clean(page_id(original))}|value={clean(context(text,hits),3000)}")
                for n,a in enumerate(attrs[:80],1):
                    print(f"ATTR|id={clean(page_id(original))}|order={n}|value={clean(a,2200)}")
        except Exception as e:
            errors.append((f"page:{page_id(original)}:{ts}",type(e).__name__,str(e)))

    # Transiently verify the known archived JPEG itself, storing only metadata/hash.
    try:
        st,final,hdr,body=fetch(replay_url(IMAGE_TS,IMAGE_URL),25,500_000,3)
        dims=jpeg_size(body)
        print(
            f"JPEG|timestamp={IMAGE_TS}|url={clean(IMAGE_URL)}|status={st}|bytes={len(body)}|"
            f"sha256={hashlib.sha256(body).hexdigest()}|content_type={clean(hdr.get('Content-Type'))}|"
            f"width={dims[0] if dims else ''}|height={dims[1] if dims else ''}|sof={hex(dims[2]) if dims else ''}|final={clean(final)}"
        )
    except Exception as e:
        errors.append(("jpeg",type(e).__name__,str(e)))

    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|completed_detail_pages|{completed}")
    print(f"COUNT|signal_pages|{matches}")
    print(f"COUNT|errors|{len(errors)}")
    if matches:
        print("RESOLUTION|MAY2002_21CN_DETAIL_SIGNAL_FOUND|classify exact sa25 image/zip relation and native record before promotion")
    elif errors:
        print("RESOLUTION|PARTIAL_MAY2002_SCAN|retry only failed narrow-window records")
    else:
        print("RESOLUTION|NO_MAY2002_DETAIL_SIGNAL|bounded narrow date window has no StoneAge token")
    print("EVIDENCE_BOUNDARY|dated detail/image metadata can identify a 21CN catalogue record and artwork asset; it cannot authenticate the unavailable ZIP bytes.")


if __name__=="__main__":
    main()
