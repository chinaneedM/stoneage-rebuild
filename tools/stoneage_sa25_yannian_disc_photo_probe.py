#!/usr/bin/env python3
"""Recover the exact photo labelled as the StoneAge 2.5-era disc in Bahamut snA=81388.

Public article/photo bodies are read transiently. Only source URLs, hashes,
dimensions and derived visual metrics are emitted. No image body or game payload
is committed.
"""
from __future__ import annotations
import hashlib, html, re, urllib.request
from tools.stoneage_sa25_host_identity_probe import declared_charset, decode, visible
from tools.stoneage_sa25_physical_image_fingerprint_probe import load_image, match_features, ruten_full_images

PAGE="https://forum.gamer.com.tw/C.php?bsn=1571&snA=81388"
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/153 Safari/537.36"
CONTENT_RE=re.compile(r'https://cos\.stoneage\.cn/uploads/article/minisnsimg/[0-9]{8}/[A-Za-z0-9_.-]+',re.I)
TARGET_PHRASES=("2.5時期的光碟","2.5时期的光碟","2.5時期的光盘","2.5时期的光盘")
SMZDM_25="https://am.zdmimg.com/201606/16/5762764a03643.jpg_e1080.jpg"

def clean(v,n=9000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch_html():
    req=urllib.request.Request(PAGE,headers={
        "User-Agent":UA,"Accept":"text/html,*/*","Accept-Language":"zh-TW,zh;q=0.9,en;q=0.5"
    })
    with urllib.request.urlopen(req,timeout=25) as r:
        b=r.read(3_000_001)
        if len(b)>3_000_000: raise ValueError("page-too-large")
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b

def sequence(text):
    out=[]; seen=set()
    for m in CONTENT_RE.finditer(text):
        u=html.unescape(m.group(0))
        if u not in seen:
            seen.add(u); out.append((m.start(),u))
    return tuple(out)

def segments(text,seq):
    out=[]; prev=0
    for pos,u in seq:
        out.append((u,visible(text[prev:pos]),visible(text[max(0,pos-1800):pos+1800])))
        prev=pos+len(u)
    return tuple(out)

def target_rows(rows):
    out=[]
    for i,(u,pre,ctx) in enumerate(rows,1):
        hay=(pre+" "+ctx)
        if any(p in hay for p in TARGET_PHRASES):
            out.append((i,u,pre,ctx))
    return tuple(out)

def main():
    print("StoneAge 2.5 Yan-Nian surviving-disc exact-photo probe — R1")
    print("SCOPE|Bahamut-snA81388+public-photo-transient|exact-disc-photo+derived-metrics-only|no-image-commit|no-game-payload")
    errors=[]
    st,final,h,b=fetch_html()
    enc,text=decode(b,declared_charset(b))
    seq=sequence(text); rows=segments(text,seq); targets=target_rows(rows)
    print(f"PAGE|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|encoding={clean(enc)}|images={len(seq)}|targets={len(targets)}|final={clean(final)}")
    for i,(u,pre,ctx) in enumerate(rows,1):
        print(f"ARTICLE_IMAGE_URL|order={i}|url={clean(u)}")
        print(f"ARTICLE_IMAGE_PRECEDING|order={i}|value={clean(pre,9000)}")
    for i,u,pre,ctx in targets:
        print(f"TARGET_IMAGE_URL|order={i}|url={clean(u)}|preceding={clean(pre,9000)}")

    target_images=[]
    for i,u,pre,ctx in targets:
        try:
            f=load_image(f"yannian:{i}",u,referer=PAGE,timeout=20,attempts=2)
            target_images.append(f)
            print(f"TARGET_IMAGE|order={i}|bytes={f['bytes']}|sha256={f['sha256']}|size={f['width']}x{f['height']}|dhash={f['dhash']}|keypoints={len(f['kp'])}|url={clean(f['url'])}")
        except Exception as e:
            errors.append((f"target:{i}",type(e).__name__,str(e)))

    controls=[]
    try:
        f=load_image("smzdm:2.5-sequence",SMZDM_25,referer="https://post.smzdm.com/p/462347/",timeout=20,attempts=2)
        controls.append(f)
        print(f"CONTROL_IMAGE|label={clean(f['label'])}|bytes={f['bytes']}|sha256={f['sha256']}|size={f['width']}x{f['height']}|url={clean(f['url'])}")
    except Exception as e:
        errors.append(("smzdm-control",type(e).__name__,str(e)))
    try:
        for row in ruten_full_images():
            if str(row.get("carrier")) not in {"21926883918096","22242541948520","22632305238624"}: continue
            try:
                f=load_image(row["label"],row["url"],referer="https://www.ruten.com.tw/",timeout=18,attempts=1)
                controls.append(f)
            except Exception as e:
                errors.append((str(row.get("label")),type(e).__name__,str(e)))
    except Exception as e:
        errors.append(("ruten-metadata",type(e).__name__,str(e)))

    matches=[]
    for a in target_images:
        for c in controls:
            m=match_features(a,c)
            matches.append((m["inliers"],m["good"],a,c,m))
    matches.sort(key=lambda x:(x[0],x[1]),reverse=True)
    for _,_,a,c,m in matches[:80]:
        print(f"MATCH|target={clean(a['label'])}|control={clean(c['label'])}|orb_matches={m['matches']}|good_le64={m['good']}|ransac_inliers={m['inliers']}|inlier_ratio={m['inlier_ratio']:.4f}|target_url={clean(a.get('url'))}|control_url={clean(c.get('url'))}")

    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|article_images|{len(seq)}")
    print(f"COUNT|target_rows|{len(targets)}")
    print(f"COUNT|target_images_loaded|{len(target_images)}")
    print(f"COUNT|controls_loaded|{len(controls)}")
    print(f"COUNT|errors|{len(errors)}")
    if target_images:
        print("RESOLUTION|EXACT_YANNIAN_25_DISC_PHOTO_RECOVERED|use as source-labelled physical carrier control only")
    elif targets:
        print("RESOLUTION|EXACT_YANNIAN_25_DISC_PHOTO_URL_RECOVERED|body unavailable; retain URL/context")
    else:
        print("RESOLUTION|YANNIAN_25_DISC_PHOTO_ORDER_UNRESOLVED|do not infer image identity")
    print("EVIDENCE_BOUNDARY|source-labelled photograph can establish the collector's physical-carrier identification only; it cannot establish disc filesystem, mastering, installer build, ISO/hash or clean-client provenance.")

if __name__=="__main__":
    main()
