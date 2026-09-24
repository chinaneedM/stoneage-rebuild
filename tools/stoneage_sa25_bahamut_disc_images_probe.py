#!/usr/bin/env python3
"""Map Bahamut collector disc-part-II image order and compare with current Ruten discs.

Public article/product images are read transiently. Only source URLs, hashes,
dimensions, contextual text, and derived visual-match metrics are emitted.
No image body or game payload is committed.
"""
from __future__ import annotations
import hashlib, html, re, urllib.request

from tools.stoneage_sa25_host_identity_probe import declared_charset, decode, visible
from tools.stoneage_sa25_physical_image_fingerprint_probe import (
    load_image, match_features, ruten_full_images,
)

PAGE="https://forum.gamer.com.tw/C.php?bsn=1571&snA=81429"
UA="stoneage-rebuild-archaeology/1.0"
CONTENT_RE=re.compile(r'https://cos\.stoneage\.cn/uploads/article/minisnsimg/20201222/[A-Za-z0-9_.-]+',re.I)

def clean(v,n=8000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch_html(url=PAGE):
    req=urllib.request.Request(url,headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/153 Safari/537.36",
        "Accept":"text/html,*/*","Accept-Language":"zh-TW,zh;q=0.9,en;q=0.5"
    })
    with urllib.request.urlopen(req,timeout=25) as r:
        b=r.read(3_000_001)
        if len(b)>3_000_000: raise ValueError("page-too-large")
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b

def image_sequence(text):
    out=[]; seen=set()
    for m in CONTENT_RE.finditer(text):
        u=html.unescape(m.group(0))
        if u not in seen:
            seen.add(u); out.append((m.start(),u))
    return tuple(out)

def local_context(text,pos,radius=1800):
    return visible(text[max(0,pos-radius):min(len(text),pos+radius)])

def main():
    print("StoneAge 2.5 Bahamut disc-image mapping and Ruten comparison — R1")
    print("SCOPE|live-Bahamut-images+public-Ruten-images-transient|context+hash+visual-metrics-only|no-image-commit|no-game-payload")
    errors=[]
    st,final,h,b=fetch_html()
    enc,text=decode(b,declared_charset(b))
    seq=image_sequence(text)
    print(f"PAGE|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|encoding={clean(enc)}|images={len(seq)}|final={clean(final)}")
    for i,(pos,u) in enumerate(seq,1):
        print(f"ARTICLE_IMAGE_URL|order={i}|url={clean(u)}")
        print(f"ARTICLE_IMAGE_CONTEXT|order={i}|value={clean(local_context(text,pos),10000)}")

    article=[]
    for i,(_,u) in enumerate(seq,1):
        try:
            f=load_image(f"bahamut:{i}",u,referer=PAGE,timeout=20,attempts=2)
            article.append(f)
            print(
                f"ARTICLE_IMAGE|order={i}|bytes={f['bytes']}|sha256={f['sha256']}|"
                f"size={f['width']}x{f['height']}|dhash={f['dhash']}|keypoints={len(f['kp'])}|url={clean(f['url'])}"
            )
        except Exception as e:
            errors.append((f"article:{i}",type(e).__name__,str(e)))

    ruten=[]
    try:
        for row in ruten_full_images():
            if str(row.get("carrier")) not in {"22632305238624","21926883918096","22242541948520"}:
                continue
            try:
                f=load_image(row["label"],row["url"],referer="https://www.ruten.com.tw/",timeout=18,attempts=2)
                ruten.append(f)
                print(
                    f"RUTEN_IMAGE|label={clean(f['label'])}|bytes={f['bytes']}|sha256={f['sha256']}|"
                    f"size={f['width']}x{f['height']}|dhash={f['dhash']}|keypoints={len(f['kp'])}|url={clean(f['url'])}"
                )
            except Exception as e:
                errors.append((str(row.get("label")),type(e).__name__,str(e)))
    except Exception as e:
        errors.append(("ruten-metadata",type(e).__name__,str(e)))

    matches=[]
    for a in article:
        for r in ruten:
            m=match_features(a,r)
            matches.append((m["inliers"],m["good"],a,r,m))
    matches.sort(key=lambda x:(x[0],x[1]),reverse=True)
    for _,_,a,r,m in matches[:120]:
        print(
            f"MATCH|article={clean(a['label'])}|ruten={clean(r['label'])}|"
            f"orb_matches={m['matches']}|good_le64={m['good']}|ransac_inliers={m['inliers']}|"
            f"inlier_ratio={m['inlier_ratio']:.4f}|article_url={clean(a.get('url'))}|ruten_url={clean(r.get('url'))}"
        )

    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|article_image_urls|{len(seq)}")
    print(f"COUNT|article_images_loaded|{len(article)}")
    print(f"COUNT|ruten_images_loaded|{len(ruten)}")
    print(f"COUNT|match_pairs|{len(matches)}")
    print(f"COUNT|errors|{len(errors)}")
    if article and ruten:
        print("RESOLUTION|ARTICLE_IMAGE_ORDER_AND_VISUAL_METRICS_AVAILABLE|classify 2.5 mainland/Taiwan carrier relation from page context plus strong local matches")
    elif seq:
        print("RESOLUTION|ARTICLE_IMAGE_ORDER_AVAILABLE_BUT_VISUAL_FETCH_INCOMPLETE|use text/image order only and retry exact image bodies only if needed")
    else:
        print("RESOLUTION|ARTICLE_IMAGE_ORDER_UNRESOLVED|do not infer 2.5 image identity")
    print("EVIDENCE_BOUNDARY|collector page context and visual homography can corroborate carrier/artwork identity only; neither proves disc filesystem, mastering, clean-client bytes, or operator-distributed binary integrity.")

if __name__=="__main__":
    main()
