#!/usr/bin/env python3
"""Recover provenance-relevant public description metadata for the Yegame-matched carrier.

R1 public-detail probe found no useful historical product identifier; its generic
EXACT_TOKEN classifier also admitted item-system tokens and must not be treated
as a provenance hit. The detail response does expose a public description_url.
This probe follows that URL, extracts visible product text and source image URLs,
and reports only StoneAge/version/publisher/model/barcode/ISBN-relevant snippets.

No login, seller contact, purchase, messaging, OCR, or image persistence.
"""
from __future__ import annotations

import hashlib
import html
import json
import re
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
TARGET="22636573895893"
DETAIL="https://rapi.ruten.com.tw/api/items/v2/list"
IDENTITY_WORDS=(
    "石器","StoneAge","Stone Age","北京华义","北京華義","华义","華義",
    "金海湾","金海灣","晶合","JSS","Japan System Supply",
    "ISBN","条码","條碼","型号","型號","货号","貨號","产品编号","產品編號",
    "版本","版號","版号","客户端","客戶端","光盘","光碟","CD-ROM","CDROM",
)
CODE_PATTERNS=(
    re.compile(r"(?i)ISBN\s*[-:：]?\s*[0-9Xx\-]{8,24}"),
    re.compile(r"(?i)(?:EAN|UPC|BARCODE|条码|條碼)\s*[-:：]?\s*[0-9\-]{8,24}"),
    re.compile(r"(?i)(?:型号|型號|货号|貨號|产品编号|產品編號|MODEL|CODE)\s*[-:：]?\s*[A-Z0-9][A-Z0-9._\-/]{3,40}"),
    re.compile(r"(?i)\b(?:SA|P-RPG|EN0ZGKJ)[-_]?[A-Z0-9.]{2,20}\b"),
    re.compile(r"(?<!\d)(?:1\.0|1\.82|2\.0|2\.5)(?!\d)"),
)
IMG_RE=re.compile(r"""(?is)<img\b[^>]*(?:src|data-src|data-original)\s*=\s*["']([^"']+)["']""")

def clean(v,n=6000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=35,max_bytes=4*1024*1024):
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

def detail_url():
    return DETAIL+"?"+urllib.parse.urlencode({"gno":TARGET,"level":"detail"})

def find_description_url(obj):
    if isinstance(obj,dict):
        for k,v in obj.items():
            if k=="description_url" and isinstance(v,str) and v.startswith(("http://","https://")):
                return v
            hit=find_description_url(v)
            if hit:return hit
    elif isinstance(obj,list):
        for v in obj:
            hit=find_description_url(v)
            if hit:return hit
    return ""

def decode_html(body):
    for enc in ("utf-8","big5","gb18030","latin1"):
        try:return enc,body.decode(enc)
        except UnicodeDecodeError:pass
    return "latin1",body.decode("latin1","replace")

def visible(text):
    text=re.sub(r"(?is)<script\b.*?</script>|<style\b.*?</style>"," ",text)
    text=html.unescape(re.sub(r"(?s)<[^>]+>"," ",text))
    return re.sub(r"\s+"," ",text).strip()

def snippets(text):
    low=text.lower(); out=[]; seen=set()
    for word in IDENTITY_WORDS:
        pos=low.find(word.lower())
        while pos>=0:
            s=clean(text[max(0,pos-220):pos+500],1200)
            if s not in seen:
                seen.add(s);out.append((word,s))
            pos=low.find(word.lower(),pos+len(word))
    return out[:50]

def main():
    print("StoneAge Yegame-matched Mainland carrier description probe — R2")
    print(f"TARGET|ruten_id={TARGET}|visual_anchor=EN0ZGKJ0002|role=mainland-retail-box")
    print("CORRECTION|R1 generic exact-token output contained marketplace/system tokens and is NOT provenance evidence")
    print("SCOPE|public item description only|identity snippets+codes+image URLs|no OCR|no image body|no contact extraction")
    errors=[]
    try:
        st,final,h,b=fetch(detail_url())
        obj=json.loads(b.decode("utf-8","replace"))
        durl=find_description_url(obj)
        print(f"DETAIL|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|description_url_present={int(bool(durl))}")
    except Exception as e:
        print(f"ERROR|scope=detail|kind={type(e).__name__}|message={clean(e)}")
        print("RESOLUTION|DESCRIPTION_ROUTE_UNAVAILABLE")
        return
    if not durl:
        print("RESOLUTION|NO_PUBLIC_DESCRIPTION_ROUTE")
        return

    try:
        st,final,h,b=fetch(durl,timeout=35,max_bytes=6*1024*1024)
        enc,raw=decode_html(b)
        plain=visible(raw)
        imgs=[]
        seen=set()
        for u in IMG_RE.findall(raw):
            u=urllib.parse.urljoin(final,html.unescape(u).strip())
            if u and u not in seen:
                seen.add(u);imgs.append(u)
        ss=snippets(plain)
        codes=set()
        for pat in CODE_PATTERNS:
            for m in pat.finditer(plain):
                codes.add(m.group(0))
        print(f"DESCRIPTION|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|encoding={enc}|visible_chars={len(plain)}|images={len(imgs)}|final_host={clean(urllib.parse.urlsplit(final).hostname)}")
        for word,s in ss:
            print(f"SNIPPET|needle={clean(word)}|text={s}")
        for code in sorted(codes):
            print(f"IDENTITY_TOKEN|value={clean(code)}")
        for i,u in enumerate(imgs[:40]):
            print(f"DESCRIPTION_IMAGE|index={i}|url={clean(u)}")
        print(f"COUNT|identity_snippets={len(ss)}")
        print(f"COUNT|identity_tokens={len(codes)}")
        print(f"COUNT|description_images={len(imgs)}")
        if codes:
            print("RESOLUTION|MATCHED_CARRIER_HISTORICAL_IDENTITY_TOKEN_FOUND|cross-search exact token against independent preservation indexes")
        elif ss:
            print("RESOLUTION|MATCHED_CARRIER_DESCRIPTION_CONTEXT_FOUND|classify version/publisher wording; seek disc-side identifier if absent")
        else:
            print("RESOLUTION|MATCHED_CARRIER_DESCRIPTION_NO_PROVENANCE_TEXT|visual match remains hypothesis only")
    except Exception as e:
        print(f"ERROR|scope=description|kind={type(e).__name__}|message={clean(e)}")
        print("RESOLUTION|DESCRIPTION_FETCH_PARTIAL|retry exact public description route only")

    print("EVIDENCE_BOUNDARY|Marketplace description is secondary carrier evidence; it cannot authenticate historical disc bytes or release date.")

if __name__=="__main__":
    main()
