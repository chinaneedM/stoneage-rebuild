#!/usr/bin/env python3
"""Targeted probe for Waei's archived June-2001 spr_1.bin patch and detail pages.

This probe is intentionally narrow:
- CDX exact metadata for StoneAge-family resource filenames under the historical
  Big5 "修補程式" directory;
- replay of the small archived spr_1.bin only to compute hashes/structural
  metadata (raw payload is never committed);
- replay of a bounded set of June-2001 dldetial.asp pages to associate the file
  with a visible download item/title if possible.

No large client binary is downloaded.
"""
from __future__ import annotations

import base64
import hashlib
import html
import json
import math
import re
import urllib.parse
import urllib.request
from collections import Counter

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
PATCH_DIR="%AD%D7%B8%C9%B5%7b%A6%A1"  # Big5: 修補程式
BASE="http://www7.waei.net:80/download/file/"+PATCH_DIR+"/"
CANDIDATES=("spr_1.bin","spradrn_1.bin","adrn_1.bin","real_1.bin")
DETAIL_PREFIX="http://www7.waei.net/download/dldetial.asp"
MAX_DETAIL_PAGES=16

def clean(v,n=5000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=35,max_bytes=4*1024*1024):
    req=urllib.request.Request(url,headers={
        "User-Agent":UA,
        "Accept":"application/json,text/html,application/octet-stream,*/*;q=0.2",
        "Accept-Encoding":"identity",
    })
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        if len(b)>max_bytes:
            raise ValueError(f"response-too-large:{len(b)}")
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b

def cdx_url(url,match="exact",from_="20001201",to="20010630"):
    params=[
        ("url",url),("matchType",match),("output","json"),
        ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
        ("from",from_),("to",to),("filter","statuscode:200"),
        ("limit","5000"),("collapse","digest"),
    ]
    return CDX+"?"+urllib.parse.urlencode(params)

def parse_rows(body):
    obj=json.loads(body.decode("utf-8"))
    if not isinstance(obj,list) or len(obj)<2:return ()
    head=obj[0]
    return tuple(dict(zip(head,row)) for row in obj[1:] if isinstance(row,list))

def replay_url(ts,orig):
    # Preserve the historical percent-encoded Big5 path exactly.
    return f"https://web.archive.org/web/{ts}id_/{orig}"

def decode_text(body):
    for enc in ("big5","cp950","gb18030","utf-8","latin1"):
        try:return enc,body.decode(enc)
        except UnicodeDecodeError:pass
    return "latin1",body.decode("latin1","replace")

def plain(s):
    s=re.sub(r"(?is)<script.*?</script>|<style.*?</style>"," ",s)
    s=re.sub(r"(?is)<[^>]+>"," ",s)
    return re.sub(r"\s+"," ",html.unescape(s))

def links(text,base):
    out=[]
    for m in re.finditer(r'(?is)<a\b[^>]*href\s*=\s*["\']([^"\']+)["\'][^>]*>(.*?)</a>',text):
        href=html.unescape(m.group(1)).strip()
        anchor=plain(m.group(2)).strip()
        if not href or href.lower().startswith(("javascript:","mailto:","#")): continue
        out.append((urllib.parse.urljoin(base,href),anchor))
    return tuple(out)

def detail_id(url):
    q=urllib.parse.parse_qs(urllib.parse.urlsplit(str(url or "")).query)
    vals=q.get("ID") or q.get("id") or ()
    return str(vals[0]) if vals else ""

def xpage(url):
    q=urllib.parse.parse_qs(urllib.parse.urlsplit(str(url or "")).query)
    vals=q.get("xPage") or q.get("xpage") or ()
    return str(vals[0]) if vals else ""

def entropy(data):
    if not data:return 0.0
    c=Counter(data);n=len(data)
    return -sum((v/n)*math.log2(v/n) for v in c.values())

def sha1_base32(data):
    return base64.b32encode(hashlib.sha1(data).digest()).decode("ascii").rstrip("=")

def main():
    print("StoneAge Waei spr_1.bin patch provenance probe — R1")
    print("SCOPE|exact companion CDX + small spr_1 replay + bounded June detail-page replay|no large client payload")

    errors=[]
    exact={}
    for name in CANDIDATES:
        original=BASE+name
        try:
            st,final,h,b=fetch(cdx_url(original,"exact"))
            rows=parse_rows(b)
            exact[name]=rows
            print(f"CDX_EXACT|name={name}|status={st}|rows={len(rows)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
            for r in rows:
                print("FILE_CAPTURE|name={}|timestamp={}|status={}|mime={}|length={}|digest={}|original={}".format(
                    name,clean(r.get("timestamp")),clean(r.get("statuscode")),clean(r.get("mimetype")),
                    clean(r.get("length")),clean(r.get("digest")),clean(r.get("original"))
                ))
        except Exception as exc:
            errors.append((f"cdx:{name}",type(exc).__name__,str(exc)))

    spr_rows=exact.get("spr_1.bin") or ()
    if spr_rows:
        # Earliest successful digest-collapsed capture is enough for byte metadata.
        r=sorted(spr_rows,key=lambda x:str(x.get("timestamp") or ""))[0]
        ts=str(r.get("timestamp") or "")
        orig=str(r.get("original") or BASE+"spr_1.bin")
        try:
            st,final,h,b=fetch(replay_url(ts,orig),timeout=45,max_bytes=2*1024*1024)
            cdx_digest=str(r.get("digest") or "")
            print(
                "SPR_BYTES|timestamp={}|status={}|bytes={}|sha256={}|sha1={}|md5={}|"
                "sha1_base32={}|cdx_digest={}|digest_match={}|entropy={:.6f}|head16={}|tail16={}|final={}".format(
                    clean(ts),st,len(b),hashlib.sha256(b).hexdigest(),hashlib.sha1(b).hexdigest(),
                    hashlib.md5(b).hexdigest(),sha1_base32(b),clean(cdx_digest),
                    int(bool(cdx_digest) and sha1_base32(b)==cdx_digest),entropy(b),
                    b[:16].hex(),b[-16:].hex(),clean(final)
                )
            )
        except Exception as exc:
            errors.append(("spr-replay",type(exc).__name__,str(exc)))

    # June detail-page topology only: latest capture per (ID,xPage,order) URL.
    try:
        st,final,h,b=fetch(cdx_url(DETAIL_PREFIX,"prefix","20010601","20010630"),timeout=60,max_bytes=4*1024*1024)
        rows=parse_rows(b)
        print(f"DETAIL_CDX|status={st}|rows={len(rows)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
    except Exception as exc:
        errors.append(("detail-cdx",type(exc).__name__,str(exc)));rows=()

    by_url={}
    for r in rows:
        orig=str(r.get("original") or "")
        old=by_url.get(orig)
        if old is None or str(r.get("timestamp") or "")>str(old.get("timestamp") or ""):
            by_url[orig]=r
    selected=sorted(by_url.values(),key=lambda r:(int(detail_id(r.get("original")) or 9999),xpage(r.get("original")),str(r.get("original"))))[:MAX_DETAIL_PAGES]
    print(f"COUNT|detail_unique_urls|{len(by_url)}")
    print(f"COUNT|detail_selected|{len(selected)}")

    association_hits=0
    for i,r in enumerate(selected,1):
        ts=str(r.get("timestamp") or "");orig=str(r.get("original") or "")
        try:
            st,final,h,b=fetch(replay_url(ts,orig),timeout=25,max_bytes=1024*1024)
            enc,text=decode_text(b);vis=plain(text)
            ls=links(text,orig)
            target=[]
            for href,anchor in ls:
                lo=urllib.parse.unquote_plus(href).lower()
                if any(x in lo for x in ("spr_1.bin","spradrn_1.bin","adrn_1.bin","real_1.bin","stoneage")) or "石器" in anchor:
                    target.append((href,anchor))
            if target: association_hits+=1
            # Print only compact semantic markers, not full page text.
            stone=int("石器" in vis or "stoneage" in vis.lower() or "stone age" in vis.lower())
            print(f"DETAIL_PAGE|index={i}|id={clean(detail_id(orig))}|xpage={clean(xpage(orig))}|timestamp={ts}|status={st}|bytes={len(b)}|encoding={enc}|stone={stone}|links={len(ls)}|target_links={len(target)}|sha256={hashlib.sha256(b).hexdigest()}|original={clean(orig)}")
            for href,anchor in target[:30]:
                print(f"ASSOCIATION|id={clean(detail_id(orig))}|xpage={clean(xpage(orig))}|href={clean(href)}|anchor={clean(anchor,1000)}")
        except Exception as exc:
            errors.append((f"detail:{i}:{orig}",type(exc).__name__,str(exc)))

    print(f"COUNT|association_pages|{association_hits}")
    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|errors|{len(errors)}")

    if association_hits:
        print("RESOLUTION|SPR_PATCH_ASSOCIATION_FOUND|promote source classification and compare exact bytes next")
    elif spr_rows:
        print("RESOLUTION|SPR_PATCH_BYTES_FOUND_NO_DETAIL_ASSOCIATION|retain as strong filename/path lead and pursue adjacent captures")
    elif errors:
        print("RESOLUTION|PARTIAL_TARGETED_PROBE|retry failed surfaces only")
    else:
        print("RESOLUTION|NO_EXACT_SPR_PATCH_CAPTURE|do not infer payload identity")
    print("EVIDENCE_BOUNDARY|A matching filename/path is not sufficient by itself to prove StoneAge provenance; detail-page association or structural cross-check is required.")

if __name__=="__main__":
    main()
