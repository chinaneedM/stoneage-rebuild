#!/usr/bin/env python3
"""Map article-body image URLs to nearby text in StoneAge 2.5 collector mirrors.

Reads only public HTML and emits derived text/image-URL context. No image body,
login, purchase or proprietary game payload is retained.
"""
from __future__ import annotations

import hashlib
import html
import re
import ssl
import time
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
PAGES=(
    ("disc-collector","https://blog.shiqi.so/shiqi273.htm"),
    ("package-collector","https://www.soshiqi.com/pt-214.htm"),
)
INSECURE_TLS_HOSTS={"blog.shiqi.so","www.soshiqi.com","soshiqi.com"}
IMG_RE=re.compile(r"(?is)<img\b[^>]*>")
ATTR_RE=re.compile(r'''(?is)\b(src|data-src|data-original|data-lazy-src|alt|title)\s*=\s*["']([^"']*)["']''')
SCRIPT_RE=re.compile(r"(?is)<(script|style|noscript)\b[^>]*>.*?</\1>")
TAG_RE=re.compile(r"(?is)<[^>]+>")
SPACE_RE=re.compile(r"\s+")

def clean(v,n=6000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def visible(raw):
    raw=SCRIPT_RE.sub(" ",raw)
    raw=TAG_RE.sub(" ",raw)
    return SPACE_RE.sub(" ",html.unescape(raw)).strip()

def fetch(url,timeout=25,attempts=2):
    last=None
    for i in range(attempts):
        try:
            req=urllib.request.Request(url,headers={
                "User-Agent":UA,
                "Accept":"text/html,*/*",
                "Accept-Language":"zh-CN,zh-TW;q=0.9,en;q=0.5",
            })
            host=urllib.parse.urlsplit(url).hostname
            ctx=ssl._create_unverified_context() if host in INSECURE_TLS_HOSTS else None
            with urllib.request.urlopen(req,timeout=timeout,context=ctx) as r:
                b=r.read(3_000_001)
                if len(b)>3_000_000: raise ValueError("page-too-large")
                return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b
        except Exception as e:
            last=e
            if i+1<attempts: time.sleep(2)
    raise last

def rows(text,base):
    out=[]
    for idx,m in enumerate(IMG_RE.finditer(text)):
        attrs={}
        for k,v in ATTR_RE.findall(m.group(0)):
            attrs.setdefault(k.lower(),html.unescape(v))
        u=""
        for k in ("data-src","data-original","data-lazy-src","src"):
            if attrs.get(k):
                u=urllib.parse.urljoin(base,attrs[k]); break
        if not u: continue
        pre=visible(text[max(0,m.start()-2200):m.start()])
        post=visible(text[m.end():min(len(text),m.end()+2200)])
        out.append({
            "index":idx,
            "url":u,
            "alt":attrs.get("alt",""),
            "title":attrs.get("title",""),
            "pre":pre,
            "post":post,
        })
    return tuple(out)

def main():
    print("StoneAge 2.5 collector-mirror image-context probe — R1")
    print("SCOPE|public-html-only|image-url+nearby-text|no-image-body|no-login|no-purchase")
    errors=[]
    total=0
    for label,url in PAGES:
        try:
            st,final,h,b=fetch(url)
            text=b.decode("utf-8","replace")
            rr=rows(text,final)
            total += len(rr)
            print(f"PAGE|label={label}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|images={len(rr)}|final={clean(final)}")
            print(f"PAGE_TEXT|label={label}|value={clean(visible(text),9000)}")
            for n,row in enumerate(rr):
                print(f"IMAGE|page={label}|order={n}|source_index={row['index']}|url={clean(row['url'],5000)}|alt={clean(row['alt'],1500)}|title={clean(row['title'],1500)}")
                print(f"IMAGE_PRE|page={label}|order={n}|value={clean(row['pre'],5000)}")
                print(f"IMAGE_POST|page={label}|order={n}|value={clean(row['post'],5000)}")
        except Exception as e:
            errors.append((label,type(e).__name__,str(e)))
    for label,kind,msg in errors:
        print(f"ERROR|page={clean(label)}|kind={clean(kind)}|message={clean(msg,1800)}")
    print(f"COUNT|pages|{len(PAGES)}")
    print(f"COUNT|images|{total}")
    print(f"COUNT|errors|{len(errors)}")
    if total:
        print("RESOLUTION|COLLECTOR_IMAGE_CONTEXT_MAPPED|use only literal nearby-text associations")
    else:
        print("RESOLUTION|COLLECTOR_IMAGE_CONTEXT_UNRESOLVED|do not assign regional/artwork labels")
    print("EVIDENCE_BOUNDARY|nearby article text can label collector photographs but cannot establish pressing/mastering, disc bytes, package-to-disc chain or clean-client provenance.")

if __name__=="__main__":
    main()
