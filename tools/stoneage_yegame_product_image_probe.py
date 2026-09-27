#!/usr/bin/env python3
"""Bounded Wayback metadata probe for the exact Jinghe/Yegame StoneAge product image.

The product-detail HTML directly references /product_images/EN0ZGKJ0002.jpg.
Catalog pages also use /product_images2/ for many products, so that sibling
path is checked as a source-grounded variant. Metadata only: no image body.
"""
from __future__ import annotations
import hashlib,json,urllib.parse,urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
FROM="20010101"; TO="20021231"
FIELDS="timestamp,original,statuscode,mimetype,digest,length,redirect"
CODE="EN0ZGKJ0002"
URLS=tuple(
 f"http://{host}:80/{folder}/{CODE}.{ext}"
 for host in ("yegame.com","www.yegame.com")
 for folder in ("product_images","product_images2")
 for ext in ("jpg","gif")
)

def clean(v,n=5000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=60,max_bytes=4*1024*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,*/*;q=0.2","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        if len(b)>max_bytes: raise ValueError("response-too-large")
        return int(getattr(r,"status",r.getcode())),r.geturl(),b

def cdx_url(url):
    p=[("url",url),("matchType","exact"),("output","json"),("fl",FIELDS),
       ("from",FROM),("to",TO),("limit","1000")]
    return CDX+"?"+urllib.parse.urlencode(p)

def parse(b):
    o=json.loads(b.decode("utf-8"))
    if not isinstance(o,list) or len(o)<2:return ()
    h=o[0]
    return tuple(dict(zip(h,row)) for row in o[1:] if isinstance(row,list))

def main():
    print("StoneAge Yegame EN0ZGKJ0002 product-image archive probe — R1")
    print(f"SCOPE|exact source-grounded image paths|{FROM}..{TO}|CDX metadata only|no image body")
    rows={}; errors=[]
    for u in URLS:
        try:
            st,final,b=fetch(cdx_url(u)); rr=parse(b)
            print(f"QUERY|status={st}|rows={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|url={clean(u)}|final={clean(final)}")
            for r in rr:
                k=(str(r.get("timestamp") or ""),str(r.get("original") or ""),str(r.get("digest") or ""),str(r.get("statuscode") or ""))
                rows[k]=r
        except Exception as e:
            errors.append((u,type(e).__name__,str(e)))
    good=0
    for r in sorted(rows.values(),key=lambda x:(str(x.get("timestamp") or ""),str(x.get("original") or ""))):
        status=str(r.get("statuscode") or "")
        mime=str(r.get("mimetype") or "")
        if status=="200" and mime.lower().startswith("image/"): good+=1
        print("ROW|timestamp={}|status={}|mime={}|length={}|digest={}|redirect={}|original={}".format(
            clean(r.get("timestamp")),clean(status),clean(mime),clean(r.get("length")),clean(r.get("digest")),
            clean(r.get("redirect")),clean(r.get("original"))
        ))
    for u,k,m in errors: print(f"ERROR|url={clean(u)}|kind={clean(k)}|message={clean(m)}")
    print(f"COUNT|unique_rows|{len(rows)}")
    print(f"COUNT|http200_image_rows|{good}")
    print(f"COUNT|errors|{len(errors)}")
    if good:
        print("RESOLUTION|PRODUCT_IMAGE_CAPTURE_FOUND|transiently fingerprint exact archived image next; do not commit image body")
    elif errors:
        print("RESOLUTION|PARTIAL_PRODUCT_IMAGE_PROBE|retry only failed exact paths once")
    else:
        print("RESOLUTION|PRODUCT_IMAGE_ARCHIVE_ROUTE_BOUNDED|retain exact path as search token and return to full-client recovery")
    print("EVIDENCE_BOUNDARY|CDX image metadata only; product-image bytes are not fetched or stored.")

if __name__=="__main__": main()
