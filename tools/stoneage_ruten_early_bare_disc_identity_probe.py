#!/usr/bin/env python3
"""Recover public provenance-relevant metadata for the early StoneAge bare-disc carrier.

Target 22111215616086 has one public disc-face image and strong visual geometry
against tracked early StoneAge carrier controls. This probe reads only public
item detail/description surfaces and emits a strict allow-list of product
identity fields/snippets. Seller/account/contact fields are excluded.

No login, purchase, messaging, OCR, image-body persistence, or software payload.
"""
from __future__ import annotations

import hashlib
import html
import json
import re
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
TARGET="22111215616086"
DETAIL="https://rapi.ruten.com.tw/api/items/v2/list"
WORDS=(
    "石器","STONEAGE","StoneAge","Stone Age","華義","华义","北京華義","北京华义",
    "JSS","Japan System Supply","版本","版號","版号","V1.","V2.",
    "P-RPG","ISBN","條碼","条码","型號","型号","貨號","货号",
    "CD-ROM","CDROM","光碟","光盘","客戶端","客户端","PC版","中文版",
)
CODE_PATTERNS=(
    re.compile(r"(?i)\bP[-_. ]?RPG[-_. ]?[A-Z0-9]{3,16}\b"),
    re.compile(r"(?i)\bISBN\s*[-:：]?\s*[0-9Xx\-]{8,24}\b"),
    re.compile(r"(?i)(?:EAN|UPC|BARCODE|條碼|条码)\s*[-:：]?\s*[0-9\-]{8,24}"),
    re.compile(r"(?i)(?:型號|型号|貨號|货号|MODEL|CODE)\s*[-:：]?\s*[A-Z0-9][A-Z0-9._\-/]{3,40}"),
    re.compile(r"(?i)\bV(?:ER(?:SION)?)?\s*[0-9]+(?:\.[0-9]+){1,2}\b"),
    re.compile(r"(?<!\d)\d{12,14}(?!\d)"),
)
ALLOW_KEYS=re.compile(r"(name|title|description|desc|spec|attribute|brand|model|barcode|isbn|ean|upc|mpn|product|version|edition|publisher|maker|manufacturer|media|disc|cd|code)",re.I)
BLOCK_KEYS=re.compile(r"(seller|store|user|member|account|email|phone|mobile|address|contact|nickname|owner|login|token|cookie|chat|message)",re.I)

def clean(v,n=6000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=35,max_bytes=6*1024*1024):
    req=urllib.request.Request(url,headers={
        "User-Agent":UA,
        "Accept":"application/json,text/html,*/*;q=0.2",
        "Accept-Language":"zh-TW,zh;q=0.9,en;q=0.5",
        "Referer":"https://www.ruten.com.tw/",
        "Accept-Encoding":"identity",
    })
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        if len(b)>max_bytes: raise ValueError("response-too-large")
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b

def detail_url(level="detail"):
    return DETAIL+"?"+urllib.parse.urlencode({"gno":TARGET,"level":level})

def walk(v,path=""):
    if isinstance(v,dict):
        for k,x in v.items():
            if BLOCK_KEYS.search(str(k)):
                continue
            p=f"{path}.{k}" if path else str(k)
            yield from walk(x,p)
    elif isinstance(v,list):
        for i,x in enumerate(v):
            yield from walk(x,f"{path}[{i}]")
    else:
        leaf=path.rsplit(".",1)[-1]
        if ALLOW_KEYS.search(path) or ALLOW_KEYS.search(leaf):
            s=str(v if v is not None else "")
            if s: yield path,s

def find_description_url(v):
    if isinstance(v,dict):
        for k,x in v.items():
            if k=="description_url" and isinstance(x,str) and x.startswith(("http://","https://")):
                return x
            hit=find_description_url(x)
            if hit:return hit
    elif isinstance(v,list):
        for x in v:
            hit=find_description_url(x)
            if hit:return hit
    return ""

def decode(body):
    for enc in ("utf-8","big5","gb18030","latin1"):
        try:return enc,body.decode(enc)
        except UnicodeDecodeError:pass
    return "latin1",body.decode("latin1","replace")

def visible(raw):
    raw=re.sub(r"(?is)<script\b.*?</script>|<style\b.*?</style>"," ",raw)
    return re.sub(r"\s+"," ",html.unescape(re.sub(r"(?s)<[^>]+>"," ",raw))).strip()

def main():
    print("StoneAge early bare-disc public identity probe — R3")
    print(f"TARGET|ruten_id={TARGET}|role=early-bare-disc")
    print("PARENT|STONEAGE-RUTEN-EARLY-BARE-DISC-R1 + R2 identity probe|visual carrier-family candidate; R2 marketplace-ID false positive corrected")
    print("SCOPE|public product detail+description|strict identity fields only|no OCR|no contact data|no payload")
    errors=[];fields=[];tokens=set()
    excluded_tokens={TARGET}

    try:
        st,final,h,b=fetch(detail_url("detail"))
        obj=json.loads(b.decode("utf-8","replace"))
        durl=find_description_url(obj)
        print(f"DETAIL|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|description_url_present={int(bool(durl))}|final={clean(final)}")
        seen=set()
        for path,val in walk(obj):
            k=(path,val)
            if k in seen:continue
            seen.add(k);fields.append(k)
            print(f"FIELD|path={clean(path,1200)}|value={clean(val,10000)}")
            for pat in CODE_PATTERNS:
                for m in pat.finditer(val):
                    token=m.group(0)
                    if token not in excluded_tokens:
                        tokens.add(token)
    except Exception as e:
        durl=""
        errors.append(("detail",type(e).__name__,str(e)))

    snippets=[]
    if durl:
        try:
            st,final,h,b=fetch(durl)
            enc,raw=decode(b);plain=visible(raw);low=plain.lower()
            print(f"DESCRIPTION|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|encoding={enc}|visible_chars={len(plain)}|final_host={clean(urllib.parse.urlsplit(final).hostname)}")
            seen=set()
            for word in WORDS:
                start=0
                while True:
                    pos=low.find(word.lower(),start)
                    if pos<0:break
                    s=clean(plain[max(0,pos-220):pos+520],1200)
                    if s not in seen:
                        seen.add(s);snippets.append((word,s))
                        # Do not persist marketplace boilerplate/contact context.
                        low_s=s.lower()
                        if not any(x in low_s for x in ("電話", "电话", "匯款", "汇款", "面交", "詐騙", "诈骗", "賣場", "卖场")):
                            print(f"SNIPPET|needle={clean(word)}|text={s}")
                    start=pos+max(1,len(word))
            for pat in CODE_PATTERNS:
                for m in pat.finditer(plain):
                    token=m.group(0)
                    if token not in excluded_tokens:
                        tokens.add(token)
        except Exception as e:
            errors.append(("description",type(e).__name__,str(e)))

    for token in sorted(tokens):
        print(f"IDENTITY_TOKEN|value={clean(token)}")
    for scope,k,m in errors:
        print(f"ERROR|scope={scope}|kind={clean(k)}|message={clean(m)}")
    print(f"COUNT|identity_fields={len(fields)}")
    print(f"COUNT|identity_snippets={len(snippets)}")
    print(f"COUNT|identity_tokens={len(tokens)}")
    print(f"COUNT|errors={len(errors)}")
    if tokens:
        print("RESOLUTION|BARE_DISC_PUBLIC_IDENTITY_TOKEN_FOUND|verify exact token against first-party/archival media records next")
    elif fields or snippets:
        print("RESOLUTION|BARE_DISC_PUBLIC_CONTEXT_ONLY|no exact historical disc identifier; visual family binding remains candidate")
    elif errors:
        print("RESOLUTION|BARE_DISC_PUBLIC_IDENTITY_PARTIAL|retry failed public surface only")
    else:
        print("RESOLUTION|BARE_DISC_PUBLIC_IDENTITY_EMPTY")
    print("EVIDENCE_BOUNDARY|Marketplace metadata is secondary carrier evidence and cannot establish disc-byte identity, version, release date, or clean-client status.")

if __name__=="__main__":
    main()
