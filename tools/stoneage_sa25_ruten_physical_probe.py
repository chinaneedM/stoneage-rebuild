#!/usr/bin/env python3
"""Probe public Ruten metadata for surviving StoneAge 2.5 physical-media listings.

This probe only reads Ruten's public JSON endpoints and image HEAD metadata.
It never buys, messages a seller, logs in, or commits image/payload bytes.
"""
from __future__ import annotations

import hashlib
import json
import time
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
IDS=(
    "22632305238624",  # boxed 2.5 newbie package
    "21926883918096",  # 2.5 disc listing
    "22242541948520",  # 2.5 disc listing
    "22615474551866",  # 2.5 game disc + box listing
)
PROD="https://rtapi.ruten.com.tw/api/prod/v2/index.php/prod"
DETAIL="https://rapi.ruten.com.tw/api/items/v2/list"

def clean(v,n=3000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=35,attempts=3):
    last=None
    for i in range(attempts):
        try:
            req=urllib.request.Request(url,headers={
                "User-Agent":UA,
                "Accept":"application/json,*/*",
                "Referer":"https://www.ruten.com.tw/",
            })
            with urllib.request.urlopen(req,timeout=timeout) as r:
                b=r.read()
                return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b
        except Exception as e:
            last=e
            if i+1<attempts:
                time.sleep(2*(i+1))
    raise last

def json_fetch(url):
    st,final,h,b=fetch(url)
    return st,final,h,b,json.loads(b.decode("utf-8","replace"))

def image_urls(row):
    out=[]
    if not isinstance(row,dict):
        return out
    images=row.get("images")
    if isinstance(images,dict):
        for key in ("url","m_url"):
            vals=images.get(key)
            if isinstance(vals,list):
                out.extend(str(x) for x in vals if x)
            elif vals:
                out.append(str(vals))
    for key in ("image_urls","images_url","Image","image"):
        vals=row.get(key)
        if isinstance(vals,list):
            out.extend(str(x) for x in vals if x)
        elif isinstance(vals,str) and vals:
            out.append(vals)
    fixed=[]
    seen=set()
    for u in out:
        if u.startswith("//"):
            u="https:"+u
        elif u.startswith("/"):
            u="https://a.rimg.com.tw"+u
        if u not in seen:
            seen.add(u); fixed.append(u)
    return fixed

def detail_rows(data):
    if isinstance(data,dict):
        d=data.get("data")
        if isinstance(d,list):
            return [x for x in d if isinstance(x,dict)]
        if isinstance(d,dict):
            return [d]
    if isinstance(data,list):
        return [x for x in data if isinstance(x,dict)]
    return []

def main():
    print("StoneAge 2.5 Ruten physical-media public metadata probe — R1")
    print("SCOPE|public-Ruten-JSON+image-HEAD-metadata|no-login|no-purchase|no-image-body")
    print("TARGETS|" + ",".join(IDS))
    errors=[]

    # Legacy/batch endpoint: useful control and title/image-summary fields.
    q=urllib.parse.urlencode({"id":",".join(IDS)})
    u=PROD+"?"+q
    try:
        st,final,h,b,data=json_fetch(u)
        print(f"PROD_QUERY|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
        rows=detail_rows(data)
        if not rows and isinstance(data,list):
            rows=[x for x in data if isinstance(x,dict)]
        for row in rows:
            pid=str(row.get("ProdId") or row.get("id") or "")
            print(
                "PROD_ROW|"
                f"id={clean(pid)}|name={clean(row.get('ProdName') or row.get('name'))}|"
                f"image={clean(row.get('Image') or row.get('image'))}|"
                f"stock={clean(row.get('StockQty') or row.get('num'))}|"
                f"sold={clean(row.get('SoldQty') or row.get('sold_num'))}|"
                f"seller={clean(row.get('SellerId') or row.get('user'))}"
            )
    except Exception as e:
        errors.append(("prod-batch",type(e).__name__,str(e)))

    all_images=[]
    for pid in IDS:
        q=urllib.parse.urlencode({"gno":pid,"level":"simple"})
        u=DETAIL+"?"+q
        try:
            st,final,h,b,data=json_fetch(u)
            print(f"DETAIL_QUERY|id={pid}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
            rows=detail_rows(data)
            print(f"DETAIL_COUNT|id={pid}|rows={len(rows)}")
            for row in rows:
                rid=str(row.get("id") or row.get("ProdId") or pid)
                imgs=image_urls(row)
                print(
                    "DETAIL_ROW|"
                    f"id={clean(rid)}|name={clean(row.get('name') or row.get('ProdName'))}|"
                    f"user={clean(row.get('user') or row.get('SellerId'))}|num={clean(row.get('num') or row.get('StockQty'))}|"
                    f"goods_no={clean(row.get('goods_no'))}|post_time={clean(row.get('post_time') or row.get('PostTime'))}|"
                    f"image_count={len(imgs)}"
                )
                for idx,img in enumerate(imgs):
                    all_images.append((pid,idx,img))
                    print(f"IMAGE_URL|id={pid}|index={idx}|url={clean(img,5000)}")
        except Exception as e:
            errors.append((f"detail:{pid}",type(e).__name__,str(e)))

    # HEAD only: record whether each public image still resolves. Never read image body.
    for pid,idx,img in all_images:
        try:
            req=urllib.request.Request(img,method="HEAD",headers={"User-Agent":UA,"Referer":"https://www.ruten.com.tw/"})
            with urllib.request.urlopen(req,timeout=25) as r:
                hh=dict(r.headers.items())
                print(
                    f"IMAGE_HEAD|id={pid}|index={idx}|status={int(getattr(r,'status',r.getcode()))}|"
                    f"content_type={clean(hh.get('Content-Type'))}|content_length={clean(hh.get('Content-Length'))}|"
                    f"etag={clean(hh.get('ETag'))}|last_modified={clean(hh.get('Last-Modified'))}|final={clean(r.geturl(),5000)}"
                )
        except Exception as e:
            print(f"IMAGE_HEAD_ERROR|id={pid}|index={idx}|kind={type(e).__name__}|message={clean(e)}")

    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={kind}|message={clean(msg)}")
    print(f"COUNT|targets|{len(IDS)}")
    print(f"COUNT|image_urls|{len(all_images)}")
    print(f"COUNT|errors|{len(errors)}")
    if all_images and not errors:
        print("RESOLUTION|PUBLIC_IMAGE_SET_RESOLVED|inspect image faces for exact carrier identifiers")
    elif all_images:
        print("RESOLUTION|PARTIAL_IMAGE_SET_RESOLVED|inspect resolved images and retry failed metadata only")
    elif errors:
        print("RESOLUTION|PUBLIC_API_PARTIAL_FAILURE|do not infer absence")
    else:
        print("RESOLUTION|NO_IMAGE_URLS_ON_TESTED_PUBLIC_ENDPOINTS")
    print("EVIDENCE_BOUNDARY|seller listing metadata and photographs are survival/recovery leads only; they do not establish disc byte provenance or clean-client identity.")

if __name__=="__main__":
    main()
