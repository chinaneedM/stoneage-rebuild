#!/usr/bin/env python3
"""Recover the exact photo labelled as the StoneAge 2.5-era disc.

The collector's creator page is preferred because article-body images are
positioned between narrative paragraphs there. The forum page is retained only
as a fallback. Public article/photo bodies are read transiently; only source
URLs, hashes, dimensions and derived visual metrics are emitted.
"""
from __future__ import annotations
import hashlib, html, re, urllib.parse, urllib.request
from tools.stoneage_sa25_host_identity_probe import declared_charset, decode, visible
from tools.stoneage_sa25_physical_image_fingerprint_probe import load_image, match_features, ruten_full_images

FORUM="https://forum.gamer.com.tw/C.php?bsn=1571&snA=81388"
HOME="https://home.gamer.com.tw/artwork.php?sn=4902119"
PAGES=(("home",HOME),("forum",FORUM))
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/153 Safari/537.36"
TARGET_PHRASES=("2.5時期的光碟","2.5时期的光碟","2.5時期的光盘","2.5时期的光盘")
NEXT_PHRASES=("2.5版本的說明書","2.5版本的说明书")
IMG_TAG_RE=re.compile(r"(?is)<img\b[^>]*>")
ATTR_RE=re.compile(r"""(?is)\b(?:data-src|data-original|data-lazy-src|src)\s*=\s*["']([^"']+)["']""")
RAW_IMAGE_RE=re.compile(r"""(?i)https?://[^\s"'<>]+?\.(?:jpe?g|png|webp)(?:\?[^\s"'<>]*)?""")
SMZDM_25="https://am.zdmimg.com/201606/16/5762764a03643.jpg_e1080.jpg"

def clean(v,n=9000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch_html(url):
    req=urllib.request.Request(url,headers={
        "User-Agent":UA,"Accept":"text/html,*/*","Accept-Language":"zh-TW,zh;q=0.9,en;q=0.5"
    })
    with urllib.request.urlopen(req,timeout=25) as r:
        b=r.read(3_000_001)
        if len(b)>3_000_000: raise ValueError("page-too-large")
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b

def target_window(text):
    starts=[text.find(p) for p in TARGET_PHRASES if text.find(p)>=0]
    if not starts:
        return "",-1,-1
    start=min(starts)
    ends=[text.find(p,start+1) for p in NEXT_PHRASES if text.find(p,start+1)>=0]
    end=min(ends) if ends else min(len(text),start+5000)
    return text[start:end],start,end

def _usable_image_url(raw,base):
    u=html.unescape(raw.strip())
    if u.startswith("//"): u="https:"+u
    u=urllib.parse.urljoin(base,u)
    low=u.lower()
    if any(x in low for x in ("avatar","emotion","emoji","logo","icon","loading","blank","noface")):
        return None
    if not any(x in low for x in (".jpg",".jpeg",".png",".webp")):
        return None
    return u

def target_urls(text,base):
    seg,start,end=target_window(text)
    if start<0:
        return tuple(),seg,start,end
    out=[]; seen=set()
    for tag in IMG_TAG_RE.findall(seg):
        for raw in ATTR_RE.findall(tag):
            u=_usable_image_url(raw,base)
            if u and u not in seen:
                seen.add(u); out.append(u)
                break
    if not out:
        for raw in RAW_IMAGE_RE.findall(seg):
            u=_usable_image_url(raw,base)
            if u and u not in seen:
                seen.add(u); out.append(u)
    return tuple(out),seg,start,end

# Compatibility helper retained so the first transition commit still passes the
# original unit test while the stricter extraction test is rolled in.
def target_rows(rows):
    out=[]
    for i,(u,pre,ctx) in enumerate(rows,1):
        hay=(pre+" "+ctx)
        if any(p in hay for p in TARGET_PHRASES):
            out.append((i,u,pre,ctx))
    return tuple(out)

def main():
    print("StoneAge 2.5 Yan-Nian surviving-disc exact-photo probe — R2")
    print("SCOPE|Bahamut-creator-body-window+forum-fallback|exact-disc-photo+derived-metrics-only|no-image-commit|no-game-payload")
    errors=[]; targets=[]; selected=None
    for label,url in PAGES:
        try:
            st,final,h,b=fetch_html(url)
            enc,text=decode(b,declared_charset(b))
            urls,seg,start,end=target_urls(text,final)
            print(f"PAGE|label={label}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|encoding={clean(enc)}|target_window_start={start}|target_window_end={end}|target_urls={len(urls)}|final={clean(final)}")
            print(f"TARGET_WINDOW|label={label}|value={clean(visible(seg),3000)}")
            for i,u in enumerate(urls,1):
                print(f"TARGET_IMAGE_URL|page={label}|order={i}|url={clean(u)}")
            if urls and not targets:
                targets=list(urls); selected=(label,final)
        except Exception as e:
            errors.append((f"page:{label}",type(e).__name__,str(e)))
    target_images=[]
    referer=selected[1] if selected else HOME
    for i,u in enumerate(targets,1):
        try:
            f=load_image(f"yannian:{i}",u,referer=referer,timeout=20,attempts=2)
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
                controls.append(load_image(row["label"],row["url"],referer="https://www.ruten.com.tw/",timeout=18,attempts=1))
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
    print(f"COUNT|target_urls|{len(targets)}")
    print(f"COUNT|target_images_loaded|{len(target_images)}")
    print(f"COUNT|controls_loaded|{len(controls)}")
    print(f"COUNT|errors|{len(errors)}")
    if len(target_images)==1:
        print("RESOLUTION|EXACT_YANNIAN_25_DISC_PHOTO_RECOVERED|source-body-window association; use as physical carrier control only")
    elif len(targets)==1:
        print("RESOLUTION|EXACT_YANNIAN_25_DISC_PHOTO_URL_RECOVERED|body unavailable; retain URL and body-window association")
    elif len(targets)>1:
        print("RESOLUTION|YANNIAN_25_DISC_PHOTO_WINDOW_AMBIGUOUS|multiple image URLs occur between disc and manual labels; do not select one")
    else:
        print("RESOLUTION|YANNIAN_25_DISC_PHOTO_URL_UNRESOLVED|do not reuse extension-reading thumbnails as article evidence")
    print("EVIDENCE_BOUNDARY|source-labelled photograph can establish physical-carrier identification only; it cannot establish disc filesystem, mastering, installer build, ISO/hash or clean-client provenance.")

if __name__=="__main__":
    main()
