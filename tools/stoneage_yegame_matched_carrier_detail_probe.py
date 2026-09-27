#!/usr/bin/env python3
"""Inspect public metadata for the Yegame-matched Mainland StoneAge physical carrier.

Target 22636573895893 is the only current early-carrier listing that passed the
Yegame EN0ZGKJ0002 visual-match threshold. This probe queries only public Ruten
item APIs/pages and emits non-personal product metadata useful for provenance:
title, category/product attributes, descriptions, model/barcode/ISBN/version
tokens and image filenames. Seller identity/contact/account fields are excluded.

No purchase, login, messaging, or image/payload persistence.
"""
from __future__ import annotations

import hashlib
import json
import re
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
TARGET="22636573895893"
API="https://rapi.ruten.com.tw/api/items/v2/list"
LEVELS=("simple","detail","normal","full")
ALLOW_RE=re.compile(
    r"(name|title|category|catalog|brand|model|barcode|isbn|ean|upc|mpn|product|item|"
    r"description|desc|spec|attribute|version|edition|publisher|maker|manufacturer|"
    r"media|disc|cd|package|serial|code|filename|image)",
    re.I,
)
BLOCK_RE=re.compile(
    r"(seller|store|user|member|account|email|phone|mobile|address|contact|nickname|"
    r"owner|login|token|cookie|chat|message)",
    re.I,
)
TOKEN_RE=re.compile(r"(EN0ZGKJ0002|[A-Z]{1,6}-?[A-Z0-9]{3,}|\b\d{8,14}\b|\bISBN[- :0-9Xx]+)",re.I)

def clean(v,n=5000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=30,max_bytes=4*1024*1024):
    req=urllib.request.Request(url,headers={
        "User-Agent":UA,
        "Accept":"application/json,text/html,*/*;q=0.2",
        "Accept-Language":"zh-TW,zh;q=0.9,en;q=0.5",
        "Referer":"https://www.ruten.com.tw/",
        "Accept-Encoding":"identity",
    })
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        if len(b)>max_bytes:
            raise ValueError("response-too-large")
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b

def api_url(level):
    return API+"?"+urllib.parse.urlencode({"gno":TARGET,"level":level})

def walk(value,path=""):
    """Yield scalar public product fields from nested JSON."""
    if isinstance(value,dict):
        for k,v in value.items():
            kp=f"{path}.{k}" if path else str(k)
            if BLOCK_RE.search(str(k)):
                continue
            yield from walk(v,kp)
    elif isinstance(value,list):
        for i,v in enumerate(value):
            yield from walk(v,f"{path}[{i}]")
    else:
        leaf=path.rsplit(".",1)[-1]
        if ALLOW_RE.search(path) or ALLOW_RE.search(leaf):
            text=str(value if value is not None else "")
            if text:
                yield path,text

def main():
    print("StoneAge Yegame-matched Mainland carrier public-detail probe — R1")
    print(f"TARGET|ruten_id={TARGET}|role=mainland-retail-box|visual_anchor=EN0ZGKJ0002")
    print("SCOPE|public product metadata only|seller/contact fields excluded|no login|no purchase|no image persistence")
    errors=[]
    seen_fields=set()
    tokens=set()
    successful=0

    for level in LEVELS:
        try:
            st,final,h,b=fetch(api_url(level),timeout=30)
            successful+=1
            print(f"API|level={level}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|content_type={clean(h.get('Content-Type'))}|final={clean(final)}")
            obj=json.loads(b.decode("utf-8","replace"))
            for path,val in walk(obj):
                key=(path,val)
                if key in seen_fields:
                    continue
                seen_fields.add(key)
                cv=clean(val,10000)
                print(f"FIELD|level={level}|path={clean(path,1000)}|value={cv}")
                for m in TOKEN_RE.finditer(val):
                    tokens.add(m.group(0))
        except Exception as e:
            errors.append((level,type(e).__name__,str(e)))

    for token in sorted(tokens):
        print(f"EXACT_TOKEN|value={clean(token)}")
    for level,kind,msg in errors:
        print(f"ERROR|level={level}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|levels_attempted={len(LEVELS)}")
    print(f"COUNT|levels_successful={successful}")
    print(f"COUNT|public_fields={len(seen_fields)}")
    print(f"COUNT|exact_tokens={len(tokens)}")
    print(f"COUNT|errors={len(errors)}")
    if tokens:
        print("RESOLUTION|MATCHED_CARRIER_EXACT_PRODUCT_TOKENS_FOUND|cross-search independent preservation indexes next")
    elif seen_fields:
        print("RESOLUTION|MATCHED_CARRIER_PUBLIC_METADATA_RECOVERED_NO_EXACT_CODE|retain visual carrier binding candidate; seek disc-side identifiers")
    elif errors:
        print("RESOLUTION|MATCHED_CARRIER_DETAIL_PARTIAL|retry successful public endpoint variants only")
    else:
        print("RESOLUTION|MATCHED_CARRIER_DETAIL_EMPTY")
    print("EVIDENCE_BOUNDARY|Current public listing metadata can support carrier attribution but cannot authenticate historical disc bytes or release date.")

if __name__=="__main__":
    main()
