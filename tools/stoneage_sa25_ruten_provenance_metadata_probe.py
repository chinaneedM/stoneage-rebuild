#!/usr/bin/env python3
"""Extract provenance-relevant public metadata from known StoneAge 2.5 Ruten listings.

Reads public Ruten item JSON and public item pages only. Emits:
- raw-response hashes and sizes;
- JSON key paths (names only);
- product-related scalar values selected by an allowlist;
- short public page snippets around StoneAge/product-provenance keywords.

Seller contact/address/private-like fields are intentionally excluded.
No login, messaging, purchase, image-body persistence, or payload download.
"""
from __future__ import annotations

import hashlib
import html
import json
import re
import time
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
IDS=(
    "22632305238624",
    "21926883918096",
    "22242541948520",
    "22615474551866",
    "22445165101247",
    "22637629794063",
    "22625938678558",
)
DETAIL="https://rapi.ruten.com.tw/api/items/v2/list"
ITEM="https://www.ruten.com.tw/item/show?{}"

ALLOW_KEYS=(
    "id","name","title","desc","description","content","remark","note","spec",
    "goods","item","condition","status","post_time","category","brand","mode",
    "price","num","stock","sold","images","image","shipping","location",
)
DENY_KEYS=(
    "user","seller","member","email","phone","mobile","tel","address","contact",
    "account","bank","realname","name_real","recipient","receiver",
)
VALUE_KEYWORDS=(
    "石器","StoneAge","stoneage","2.5","精靈王","精灵王","光碟","光盘","用戶端",
    "客户端","原版","原包裝","原包装","保存","說明書","说明书","華義","华义",
    "WAEI","WGS","台版","臺版","大陸","大陆","北京","版本","新手報到包","新手包",
)
PAGE_KEYWORDS=(
    "石器時代","石器时代","精靈王傳說","精灵王传说","遊戲光碟","游戏光盘",
    "原包裝","原包装","原版","用戶端","客户端","保存","說明書","说明书",
    "華義","华义","WAEI","WGS","新手報到包","新手包",
)

TAG_RE=re.compile(r"(?is)<[^>]+>")
SCRIPT_RE=re.compile(r"(?is)<(script|style|noscript)\b[^>]*>.*?</\1>")
SPACE_RE=re.compile(r"\s+")


def clean(v,n=2200):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]


def fetch(url, *, accept="*/*", timeout=30, attempts=3):
    last=None
    for i in range(attempts):
        try:
            req=urllib.request.Request(url,headers={
                "User-Agent":UA,
                "Accept":accept,
                "Accept-Language":"zh-TW,zh;q=0.9,en;q=0.5",
                "Referer":"https://www.ruten.com.tw/",
            })
            with urllib.request.urlopen(req,timeout=timeout) as r:
                b=r.read(8_000_001)
                if len(b)>8_000_000:
                    raise ValueError("response-too-large")
                return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b
        except Exception as e:
            last=e
            if i+1<attempts:
                time.sleep(i+1)
    raise last


def flatten(obj,path=""):
    if isinstance(obj,dict):
        for k,v in obj.items():
            p=f"{path}.{k}" if path else str(k)
            yield from flatten(v,p)
    elif isinstance(obj,list):
        for idx,v in enumerate(obj):
            p=f"{path}[]" if path else "[]"
            yield from flatten(v,p)
            if idx>=49:
                break
    else:
        yield path,obj


def key_allowed(path,value):
    low=path.lower()
    if any(x in low for x in DENY_KEYS):
        return False
    last=low.rsplit(".",1)[-1].replace("[]","")
    if any(x in last for x in ALLOW_KEYS):
        return True
    text=str(value)
    return any(k.lower() in text.lower() for k in VALUE_KEYWORDS)


def key_paths(obj):
    out=set()
    def walk(v,path=""):
        if isinstance(v,dict):
            for k,x in v.items():
                p=f"{path}.{k}" if path else str(k)
                low=p.lower()
                if not any(d in low for d in DENY_KEYS):
                    out.add(p)
                walk(x,p)
        elif isinstance(v,list):
            p=f"{path}[]" if path else "[]"
            out.add(p)
            for x in v[:5]:
                walk(x,p)
    walk(obj)
    return tuple(sorted(out))


def visible_text(raw):
    s=raw.decode("utf-8","replace")
    s=SCRIPT_RE.sub(" ",s)
    s=TAG_RE.sub(" ",s)
    return SPACE_RE.sub(" ",html.unescape(s)).strip()


def keyword_snippets(text, radius=360):
    low=text.lower()
    spans=[]
    for kw in PAGE_KEYWORDS:
        start=0
        needle=kw.lower()
        while True:
            p=low.find(needle,start)
            if p<0:
                break
            spans.append((max(0,p-radius),min(len(text),p+len(kw)+radius)))
            start=p+len(needle)
    spans.sort()
    merged=[]
    for a,b in spans:
        if not merged or a>merged[-1][1]+80:
            merged.append([a,b])
        else:
            merged[-1][1]=max(merged[-1][1],b)
    return tuple(text[a:b] for a,b in merged[:12])


def main():
    print("StoneAge 2.5 Ruten provenance-metadata probe — R1")
    print("SCOPE|public-item-json+public-item-html|product-metadata-only|no-login|no-purchase|no-contact-data")
    print("TARGETS|"+",".join(IDS))
    errors=[]
    for pid in IDS:
        q=urllib.parse.urlencode({"gno":pid,"level":"simple"})
        api=DETAIL+"?"+q
        try:
            st,final,h,b=fetch(api,accept="application/json,*/*")
            data=json.loads(b.decode("utf-8","replace"))
            print(f"API|id={pid}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
            paths=key_paths(data)
            print(f"API_KEY_COUNT|id={pid}|count={len(paths)}")
            for p in paths:
                print(f"API_KEY|id={pid}|path={clean(p,1000)}")
            seen=set()
            for p,v in flatten(data):
                if v is None or isinstance(v,(dict,list)):
                    continue
                if not key_allowed(p,v):
                    continue
                pair=(p,str(v))
                if pair in seen:
                    continue
                seen.add(pair)
                print(f"API_VALUE|id={pid}|path={clean(p,1000)}|value={clean(v,3500)}")
        except Exception as e:
            errors.append((pid,"api",type(e).__name__,str(e)))

        page=ITEM.format(pid)
        try:
            st,final,h,b=fetch(page,accept="text/html,*/*")
            text=visible_text(b)
            print(f"PAGE|id={pid}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|text_chars={len(text)}|final={clean(final)}")
            snippets=keyword_snippets(text)
            print(f"PAGE_SNIPPET_COUNT|id={pid}|count={len(snippets)}")
            for n,snip in enumerate(snippets,1):
                print(f"PAGE_SNIPPET|id={pid}|index={n}|value={clean(snip,2600)}")
            raw=b.decode("utf-8","replace")
            # Public metadata tags often carry the complete product title/description.
            for patt,label in (
                (r'(?is)<meta[^>]+(?:name|property)=["\'](?:description|og:description)["\'][^>]+content=["\']([^"\']*)', "description"),
                (r'(?is)<meta[^>]+(?:name|property)=["\'](?:og:title|twitter:title)["\'][^>]+content=["\']([^"\']*)', "title"),
                (r'(?is)<title[^>]*>(.*?)</title>', "html-title"),
            ):
                for m in re.finditer(patt,raw):
                    val=html.unescape(TAG_RE.sub(" ",m.group(1)))
                    if val:
                        print(f"PAGE_META|id={pid}|kind={label}|value={clean(val,3500)}")
        except Exception as e:
            errors.append((pid,"page",type(e).__name__,str(e)))

    for pid,scope,kind,msg in errors:
        print(f"ERROR|id={pid}|scope={scope}|kind={kind}|message={clean(msg,1800)}")
    print(f"COUNT|targets|{len(IDS)}")
    print(f"COUNT|errors|{len(errors)}")
    print("RESOLUTION|PUBLIC_RUTEN_PROVENANCE_METADATA_MAPPED|interpret only literal seller/platform product claims")
    print("EVIDENCE_BOUNDARY|marketplace text can identify surviving carrier claims and search tokens; it cannot establish disc filesystem, byte identity, pressing/mastering or clean-client provenance.")


if __name__=="__main__":
    main()
