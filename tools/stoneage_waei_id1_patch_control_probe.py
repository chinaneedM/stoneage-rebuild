#!/usr/bin/env python3
"""Inspect the archived Waei ID=1 page around StoneAge patch entries.

Metadata/HTML only. No linked binary payload is fetched.
"""
from __future__ import annotations
import hashlib, html, re, urllib.request

UA="stoneage-rebuild-archaeology/1.0"
TS="20010619204044"
ORIG="http://www7.waei.net:80/download/dldetial.asp?ID=1&xPage=2"
URL=f"https://web.archive.org/web/{TS}id_/{ORIG}"
TARGETS=("石器時代聲控程式(2000版)","石器時代聲控程式(98版)","石器隱形人無所遁形修正檔")
TOKENS=("download","downloading","file/","spr_1.bin","adrn_1.bin","real_1.bin","spradrn_1.bin","onclick","window.open","location.href")

def clean(s,n=8000):
    return " ".join(str(s or "").split()).replace("|","%7C")[:n]

def fetch():
    req=urllib.request.Request(URL,headers={"User-Agent":UA,"Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=45) as r:
        b=r.read(1024*1024)
        return int(getattr(r,"status",r.getcode())),r.geturl(),b

def decode(b):
    for enc in ("big5","gb18030","gbk","utf-8","latin1"):
        try:return enc,b.decode(enc)
        except UnicodeDecodeError:pass
    return "latin1",b.decode("latin1","replace")

def main():
    print("StoneAge Waei ID1 StoneAge patch-control probe — R1")
    print("SCOPE|single archived HTML page|control/form/link extraction only|no binary payload")
    st,final,b=fetch()
    enc,t=decode(b)
    print(f"PAGE|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|encoding={enc}|final={clean(final)}")

    low=t.lower()
    for target in TARGETS:
        pos=t.find(target)
        if pos<0:
            print(f"TARGET|name={target}|found=0")
            continue
        a=max(0,pos-1800); z=min(len(t),pos+3200)
        raw=t[a:z]
        print(f"TARGET|name={target}|found=1|offset={pos}")
        # Emit compact raw HTML around the entry. This page is a public download
        # catalogue and contains no participant/customer records.
        print(f"HTML_CONTEXT|name={target}|html={clean(raw,7000)}")
        # Extract URLs and form-ish attributes from the local block.
        urls=[]
        for m in re.finditer(r'(?i)(?:href|src|action)\s*=\s*["\']([^"\']+)["\']',raw):
            u=html.unescape(m.group(1)).strip()
            if u not in urls:urls.append(u)
        for u in urls:
            print(f"LOCAL_URL|name={target}|url={clean(u,2000)}")
        inputs=[]
        for m in re.finditer(r'(?is)<input\b[^>]*>',raw):
            tag=clean(m.group(0),1800)
            if tag not in inputs:inputs.append(tag)
        for tag in inputs:
            print(f"LOCAL_INPUT|name={target}|tag={tag}")
        # Surface scripts/attributes containing route tokens.
        for tok in TOKENS:
            start=0
            while True:
                i=low.find(tok.lower(),max(a,start))
                if i<0 or i>=z:break
                s=clean(t[max(a,i-450):min(z,i+850)],1800)
                print(f"TOKEN_CONTEXT|name={target}|token={tok}|text={s}")
                start=i+len(tok)

    # Whole-page route inventory, deduplicated.
    routes=[]
    for m in re.finditer(r'(?i)(?:href|src|action)\s*=\s*["\']([^"\']+)["\']',t):
        u=html.unescape(m.group(1)).strip()
        l=u.lower()
        if any(k in l for k in ("download","file/","dldetial","spr_1","stoneage")) and u not in routes:
            routes.append(u)
    print(f"COUNT|route_candidates|{len(routes)}")
    for u in routes:
        print(f"ROUTE|{clean(u,3000)}")
    print("EVIDENCE_BOUNDARY|HTML controls can bind catalogue entries to routes; no linked binary is fetched or authenticated here.")

if __name__=="__main__":main()
