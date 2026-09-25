#!/usr/bin/env python3
"""Discover current public Ruten StoneAge 2.5 disc listings from search HTML.

Public GET only. No login, purchase or seller contact. The probe stores only
derived metadata (IDs, titles, URLs, response fingerprints), never image bodies.
"""
from __future__ import annotations
import hashlib, html, re, urllib.parse, urllib.request

UA="stoneage-rebuild-archaeology/1.0"
QUERIES=(
    "石器時代2.5版 精靈王傳說",
    "石器時代 2.5版 精靈王傳說",
    "石器時代2.5 精靈王傳說 光碟",
)
BASE="https://www.ruten.com.tw/find/"
ITEM_RE=re.compile(r'https?://www\.ruten\.com\.tw/item/(\d{12,16})/?',re.I)
ITEM_PATH_RE=re.compile(r'(?:"|\')/item/(\d{12,16})/?(?:"|\')',re.I)
TEXT_ITEM_RE=re.compile(r'(\d{12,16})')
TITLE_RE=re.compile(r'(?is)<title[^>]*>(.*?)</title>')
URL_RE=re.compile(r'''(?i)(?:https?:)?//[^"'<>\s]+|/[^"'<>\s]+''')
SCRIPT_RE=re.compile(r'''(?is)<script\b[^>]*?src=["']([^"']+)["']''')
TAG_RE=re.compile(r'(?is)<[^>]+>')

def clean(v,n=1800):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=35):
    req=urllib.request.Request(url,headers={
        "User-Agent":UA,
        "Accept":"text/html,application/xhtml+xml,*/*;q=0.8",
        "Accept-Language":"zh-TW,zh;q=0.9,en;q=0.5",
    })
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(4_000_001)
        if len(b)>4_000_000: raise ValueError("response-too-large")
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b

def visible(text):
    return " ".join(html.unescape(TAG_RE.sub(" ",text)).split())

def ids_from_html(text):
    out=[]; seen=set()
    for pat in (ITEM_RE,ITEM_PATH_RE):
        for m in pat.finditer(text):
            pid=m.group(1)
            if pid not in seen:
                seen.add(pid); out.append(pid)
    return tuple(out)

def discovery_urls(text,base):
    out=[]; seen=set()
    for raw in URL_RE.findall(text):
        u=html.unescape(raw).replace("\\/","/")
        if u.startswith("//"): u="https:"+u
        elif u.startswith("/"): u=urllib.parse.urljoin(base,u)
        low=u.lower()
        if not any(k in low for k in ("api","search","prod","item","query")):
            continue
        if u not in seen:
            seen.add(u); out.append(u)
    for raw in SCRIPT_RE.findall(text):
        u=html.unescape(raw)
        if u.startswith("//"): u="https:"+u
        else: u=urllib.parse.urljoin(base,u)
        if u not in seen:
            seen.add(u); out.append(u)
    return tuple(out)

def relevant_contexts(text,pids):
    out=[]
    for pid in pids:
        pos=text.find(pid)
        if pos<0: continue
        seg=text[max(0,pos-1400):min(len(text),pos+2400)]
        vis=visible(seg)
        if ("石器時代" in vis or "石器时代" in vis) and ("2.5" in vis or "精靈王" in vis or "精灵王" in vis):
            out.append((pid,vis))
    return tuple(out)

def main():
    print("StoneAge 2.5 Ruten public-search listing discovery — R2")
    print("SCOPE|public-search-html-only|ids+nearby-title-context|no-login|no-purchase|no-seller-contact|no-image-body")
    all_ids={}
    errors=[]
    for qi,q in enumerate(QUERIES,1):
        url=BASE+"?"+urllib.parse.urlencode({"q":q,"cateid":"0022"})
        try:
            st,final,h,b=fetch(url)
            text=b.decode("utf-8","replace")
            ids=ids_from_html(text)
            ctx=relevant_contexts(text,ids)
            du=discovery_urls(text,final)
            tm=TITLE_RE.search(text)
            title=visible(tm.group(1)) if tm else ""
            print(f"QUERY|index={qi}|q={clean(q)}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|title={clean(title)}|ids={len(ids)}|relevant={len(ctx)}|discovery_urls={len(du)}|final={clean(final,3000)}")
            for pid,vis in ctx:
                all_ids.setdefault(pid,[]).append((qi,vis))
                print(f"CANDIDATE|query={qi}|id={pid}|context={clean(vis,4000)}|url=https://www.ruten.com.tw/item/{pid}/")
            for n,u in enumerate(du[:250],1):
                print(f"DISCOVERY_URL|query={qi}|index={n}|url={clean(u,4000)}")
        except Exception as e:
            errors.append((qi,q,type(e).__name__,str(e)))
    for qi,q,kind,msg in errors:
        print(f"ERROR|query={qi}|q={clean(q)}|kind={kind}|message={clean(msg)}")
    print(f"COUNT|queries|{len(QUERIES)}")
    print(f"COUNT|unique_candidates|{len(all_ids)}")
    print(f"COUNT|errors|{len(errors)}")
    print("CANDIDATE_IDS|"+",".join(sorted(all_ids)))
    if all_ids:
        print("RESOLUTION|PUBLIC_RUTEN_SEARCH_IDS_DISCOVERED|feed unseen IDs into provenance/image probes and deduplicate before counting specimens")
    elif errors==len(QUERIES):
        print("RESOLUTION|RUTEN_SEARCH_TRANSPORT_BLOCKED|do not infer no listings")
    else:
        print("RESOLUTION|NO_IDS_EXPOSED_IN_TESTED_SEARCH_HTML|inspect DISCOVERY_URL rows for a public frontend search API; search-engine indexed variants may still exist")
    print("EVIDENCE_BOUNDARY|Search-result IDs and titles are discovery metadata only; they do not establish physical independence, disc contents, pressing/mastering or historical provenance.")

if __name__=="__main__":
    main()
