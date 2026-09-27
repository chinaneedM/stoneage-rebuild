#!/usr/bin/env python3
"""Map the Bahamut Mainland StoneAge 1.0 test-carrier lead to exact article images.

Source:
  https://forum.gamer.com.tw/C.php?bsn=1571&snA=81396

The collector first shows a rumored 1.0 package image, then states that the
Mainland 1.0 test item he obtained was actually a test manual carrying a disc,
distributed with a magazine, without a retail box.

This probe resolves the live article's text/image sequence and emits only:
- article hash/title/anchor positions;
- exact article-body image URLs and their text intervals;
- transient image hashes/dimensions where public image bodies are readable.

No image body, personal data, software payload, or OCR output is committed.
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

ANCHORS=(
    "據傳說還存在一個1.0的測試禮包",
    "給大家看看謠傳中的圖片",
    "大陸版1.0測試包其實是一個測試說明書夾帶光碟的隨雜誌附贈的東西",
    "本身不帶包裝盒子",
    "也是我機緣巧合下得到的",
    "有空再和大傢俱體聊了哈",
)

ATTR_RE=re.compile(r"""(?is)(?:src|data-src|data-original|href)\s*=\s*["']([^"']+)["']""")
CONTENT_HOSTS=("truth.bahamut.com.tw","cos.stoneage.cn","i2.bahamut.com.tw","i3.bahamut.com.tw")

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

def article_images(raw):
    out=[];seen=set()
    for m in ATTR_RE.finditer(raw):
        u=html.unescape(m.group(1).strip())
        if u.startswith("//"): u="https:"+u
        low=u.lower()
        if not low.startswith(("http://","https://")): continue
        if not any(h in low for h in CONTENT_HOSTS): continue
        if not re.search(r"(?i)\.(?:jpe?g|png|gif|webp)(?:\?|$)",u): continue
        if any(noise in low for noise in ("avatar","sticker","logo","icon","emoji","forum_menu","ani_")): continue
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
    print("StoneAge Mainland SA1.0 test-carrier Bahamut image-order probe — R1")
    print("SCOPE|single public collector article|text-to-image-order+transient-image-metadata|no-image-commit|no-OCR|no-payload")
    print(f"TARGET|{PAGE}")
    errors=[]
    st,final,h,b=fetch(PAGE,25,MAX_PAGE,3)
    enc,raw=decode(b,declared_charset(b))
    print(f"PAGE|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|encoding={clean(enc)}|title={clean(title(raw),1800)}|final={clean(final)}")

    for a in ANCHORS:
        p=raw.find(a)
        print(f"ANCHOR|found={int(p>=0)}|raw_pos={p}|text={clean(a)}")

    seq=article_images(raw)
    print(f"COUNT|article_image_urls|{len(seq)}")
    prev=0
    rows=[]
    for i,(pos,u) in enumerate(seq,1):
        before=interval_text(raw,prev,pos)
        next_pos=seq[i][0] if i<len(seq) else min(len(raw),pos+12000)
        after=interval_text(raw,pos,next_pos)
        print(f"IMAGE_URL|order={i}|raw_pos={pos}|url={clean(u)}")
        print(f"IMAGE_PRECEDING|order={i}|text={clean(before,8000)}")
        print(f"IMAGE_FOLLOWING|order={i}|text={clean(after,8000)}")
        rows.append((i,pos,u))
        prev=pos+len(u)

    for i,pos,u in rows:
        try:
            st2,final2,h2,ib=fetch(u,25,MAX_IMAGE,2,accept="image/*,*/*",referer=PAGE)
            w,hh,fmt=image_dimensions(ib)
            print(f"IMAGE_META|order={i}|status={st2}|bytes={len(ib)}|sha256={hashlib.sha256(ib).hexdigest()}|format={fmt}|size={clean(w)}x{clean(hh)}|final={clean(final2)}")
        except Exception as e:
            errors.append((f"image:{i}",type(e).__name__,str(e)))

    claim_pos=raw.find("大陸版1.0測試包其實是一個測試說明書夾帶光碟的隨雜誌附贈的東西")
    images_after=[(i,pos,u) for i,pos,u in rows if claim_pos>=0 and pos>claim_pos]
    rumor_pos=raw.find("給大家看看謠傳中的圖片")
    images_between=[(i,pos,u) for i,pos,u in rows if rumor_pos>=0 and claim_pos>=0 and pos>rumor_pos and pos<claim_pos]
    print(f"COUNT|images_between_rumor_and_actual_claim|{len(images_between)}")
    print(f"COUNT|images_after_actual_test_carrier_claim|{len(images_after)}")
    for i,pos,u in images_between[:20]:
        print(f"RUMOR_REGION_IMAGE|order={i}|url={clean(u)}")
    for i,pos,u in images_after[:20]:
        print(f"POST_CLAIM_IMAGE|order={i}|url={clean(u)}")

    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|errors|{len(errors)}")

    if claim_pos>=0 and images_after:
        print("RESOLUTION|POST_CLAIM_IMAGE_PRESENT|inspect exact post-claim image(s) as possible test-manual/disc evidence before classification")
    elif claim_pos>=0:
        print("RESOLUTION|CLAIM_TEXT_ONLY_NO_POST_CLAIM_IMAGE|collector claim is public text only on this article; no actual test-manual/disc image follows it")
    else:
        print("RESOLUTION|TEST_CARRIER_CLAIM_NOT_RESOLVED|do not infer article-image identity")
    print("EVIDENCE_BOUNDARY|Image order can bind pictures to nearby collector text, but collector attribution does not authenticate magazine identity, optical mastering, client bytes, or release date.")

if __name__=="__main__":
    main()
