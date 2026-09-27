#!/usr/bin/env python3
"""Resolve the Bahamut Mainland StoneAge 1.0 test-carrier claim against first-post images.

Source:
  https://forum.gamer.com.tw/C.php?bsn=1571&snA=81396

R1 correctly recovered the text/image sequence but over-counted site chrome,
"extended reading" thumbnails and editor-emotion GIFs as post-claim images.
R2 defines the first-post body structurally and classifies only full-size
truth.bahamut.com.tw images inside that body.

Evidence question:
- six full-size images follow the collector's "rumored 1.0 package" wording;
- does any first-post image follow the later statement that the actual Mainland
  1.0 test item was a magazine-insert test manual carrying a disc?

Only URLs, text ordering, hashes and dimensions are emitted. Image bodies are
read transiently and discarded. No OCR or game payload is used.
"""
from __future__ import annotations

import hashlib
import html
import re
import struct
import time
import urllib.request

from tools.stoneage_sa25_host_identity_probe import declared_charset, decode, title, visible

PAGE="https://forum.gamer.com.tw/C.php?bsn=1571&snA=81396"
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/153 Safari/537.36"
MAX_PAGE=3_000_000
MAX_IMAGE=12*1024*1024

POST_START_ANCHOR="首先慣例一張全家福"
POST_END_MARKERS=("延伸閱讀","未登入的勇者，要加入 2 樓的討論嗎？")
RUMOR_ANCHOR="給大家看看謠傳中的圖片"
CLAIM_ANCHOR="大陸版1.0測試包其實是一個測試說明書夾帶光碟的隨雜誌附贈的東西"

ANCHORS=(
    "據傳說還存在一個1.0的測試禮包",
    RUMOR_ANCHOR,
    CLAIM_ANCHOR,
    "本身不帶包裝盒子",
    "也是我機緣巧合下得到的",
    "有空再和大傢俱體聊了哈",
)

ATTR_RE=re.compile(r"""(?is)(?:src|data-src|data-original|href)\s*=\s*["']([^"']+)["']""")
FULLSIZE_HOST="truth.bahamut.com.tw"

def clean(v,n=10000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=25,max_bytes=MAX_PAGE,attempts=2,accept="text/html,*/*",referer=None):
    last=None
    for i in range(attempts):
        try:
            headers={"User-Agent":UA,"Accept":accept,"Accept-Language":"zh-TW,zh;q=0.9,en;q=0.5"}
            if referer: headers["Referer"]=referer
            req=urllib.request.Request(url,headers=headers)
            with urllib.request.urlopen(req,timeout=timeout) as r:
                b=r.read(max_bytes+1)
                if len(b)>max_bytes: raise ValueError("response-too-large")
                return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b
        except Exception as e:
            last=e
            if i+1<attempts: time.sleep(1.0)
    raise last

def first_post_bounds(raw):
    start=raw.find(POST_START_ANCHOR)
    if start<0:
        start=0
    ends=[raw.find(marker,start) for marker in POST_END_MARKERS]
    ends=[p for p in ends if p>=0]
    end=min(ends) if ends else len(raw)
    return start,end

def article_images(raw,start=None,end=None):
    if start is None or end is None:
        start,end=first_post_bounds(raw)
    out=[];seen=set()
    for m in ATTR_RE.finditer(raw,start,end):
        u=html.unescape(m.group(1).strip())
        if u.startswith("//"): u="https:"+u
        low=u.lower()
        if not low.startswith(("http://","https://")): continue
        if FULLSIZE_HOST not in low: continue
        if not re.search(r"(?i)\.(?:jpe?g|png|webp)(?:$)",u): continue
        if "?" in u: continue
        if u in seen: continue
        seen.add(u);out.append((m.start(),u))
    return tuple(out)

def interval_text(raw,start,end):
    return visible(raw[max(0,start):min(len(raw),end)])

def image_dimensions(body):
    if body.startswith(b"\x89PNG\r\n\x1a\n") and len(body)>=24:
        w,h=struct.unpack(">II",body[16:24]);return w,h,"png"
    if body.startswith((b"GIF87a",b"GIF89a")) and len(body)>=10:
        w,h=struct.unpack("<HH",body[6:10]);return w,h,"gif"
    if body.startswith(b"\xff\xd8"):
        i=2
        while i+9<len(body):
            if body[i]!=0xFF:
                i+=1;continue
            while i<len(body) and body[i]==0xFF:i+=1
            if i>=len(body):break
            marker=body[i];i+=1
            if marker in (0xD8,0xD9) or 0xD0<=marker<=0xD7:continue
            if i+2>len(body):break
            seg=int.from_bytes(body[i:i+2],"big")
            if seg<2 or i+seg>len(body):break
            if marker in {0xC0,0xC1,0xC2,0xC3,0xC5,0xC6,0xC7,0xC9,0xCA,0xCB,0xCD,0xCE,0xCF} and seg>=7:
                h=int.from_bytes(body[i+3:i+5],"big")
                w=int.from_bytes(body[i+5:i+7],"big")
                return w,h,"jpeg"
            i+=seg
    return None,None,"unknown"

def main():
    print("StoneAge Mainland SA1.0 test-carrier Bahamut classification — R2")
    print("SUPERSEDES|STONEAGE-MAINLAND-SA10-TEST-CARRIER-BAHAMUT-IMAGES-R1|R1 post-claim image count included recommendation/UI assets")
    print("SCOPE|single public collector first-post body|text-to-image-order+transient-image-metadata|no-image-commit|no-OCR|no-payload")
    print(f"TARGET|{PAGE}")
    errors=[]
    st,final,h,b=fetch(PAGE,25,MAX_PAGE,3)
    enc,raw=decode(b,declared_charset(b))
    start,end=first_post_bounds(raw)
    print(f"PAGE|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|encoding={clean(enc)}|title={clean(title(raw),1800)}|final={clean(final)}")
    print(f"FIRST_POST_BOUNDS|start={start}|end={end}|chars={max(0,end-start)}|start_anchor={clean(POST_START_ANCHOR)}")

    for a in ANCHORS:
        p=raw.find(a,start,end)
        print(f"ANCHOR|found={int(p>=0)}|raw_pos={p}|text={clean(a)}")

    seq=article_images(raw,start,end)
    print(f"COUNT|first_post_fullsize_images|{len(seq)}")
    prev=start
    rows=[]
    for i,(pos,u) in enumerate(seq,1):
        next_pos=seq[i][0] if i<len(seq) else end
        before=interval_text(raw,prev,pos)
        after=interval_text(raw,pos,next_pos)
        print(f"IMAGE_URL|order={i}|raw_pos={pos}|url={clean(u)}")
        print(f"IMAGE_PRECEDING|order={i}|text={clean(before,5000)}")
        print(f"IMAGE_FOLLOWING|order={i}|text={clean(after,5000)}")
        rows.append((i,pos,u))
        prev=pos+len(u)

    for i,pos,u in rows:
        try:
            st2,final2,h2,ib=fetch(u,25,MAX_IMAGE,2,accept="image/*,*/*",referer=PAGE)
            w,hh,fmt=image_dimensions(ib)
            print(f"IMAGE_META|order={i}|status={st2}|bytes={len(ib)}|sha256={hashlib.sha256(ib).hexdigest()}|format={fmt}|size={clean(w)}x{clean(hh)}|final={clean(final2)}")
        except Exception as e:
            errors.append((f"image:{i}",type(e).__name__,str(e)))

    rumor_pos=raw.find(RUMOR_ANCHOR,start,end)
    claim_pos=raw.find(CLAIM_ANCHOR,start,end)
    images_between=[(i,pos,u) for i,pos,u in rows if rumor_pos>=0 and claim_pos>=0 and rumor_pos<pos<claim_pos]
    images_after=[(i,pos,u) for i,pos,u in rows if claim_pos>=0 and claim_pos<pos<end]

    print(f"COUNT|images_between_rumor_and_actual_claim|{len(images_between)}")
    print(f"COUNT|first_post_images_after_actual_claim|{len(images_after)}")
    for i,pos,u in images_between:
        print(f"RUMOR_REGION_IMAGE|order={i}|url={clean(u)}")
    for i,pos,u in images_after:
        print(f"ACTUAL_CLAIM_REGION_IMAGE|order={i}|url={clean(u)}")

    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|errors|{len(errors)}")

    if claim_pos>=0 and not images_after:
        print("RESOLUTION|TEST_CARRIER_CLAIM_TEXT_ONLY_NO_PUBLIC_SPECIMEN_IMAGE|six preceding images belong to the rumored/unverified 1.0 package region; no first-post image follows the actual test-manual/disc claim")
    elif claim_pos>=0:
        print("RESOLUTION|ACTUAL_CLAIM_REGION_IMAGE_PRESENT|inspect only first-post image(s) after the claim before any carrier promotion")
    else:
        print("RESOLUTION|TEST_CARRIER_CLAIM_NOT_RESOLVED|do not infer article-image identity")
    print("EVIDENCE_BOUNDARY|The collector's actual Mainland 1.0 test-manual/disc statement is later first-person evidence. This page does not authenticate magazine identity, optical mastering, file tree, client bytes or release date.")

if __name__=="__main__":
    main()
