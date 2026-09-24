#!/usr/bin/env python3
"""Extract and fingerprint the StoneAge install-disc photo from a 2016 SMZDM collector post.

Public page/photo bodies are read transiently. Only URLs, hashes, dimensions and
derived visual metrics are emitted; no photograph or game payload is committed.
"""
from __future__ import annotations
import hashlib, html, re, urllib.parse, urllib.request
from tools.stoneage_sa25_physical_image_fingerprint_probe import load_image, match_features, ruten_full_images
from tools.stoneage_sa25_host_identity_probe import declared_charset, decode, visible

PAGE="https://post.smzdm.com/p/462347/"
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/153 Safari/537.36"
IMG_RE=re.compile(r"""(?is)<img\b[^>]*(?:src|data-src|data-original|data-lazy-src)\s*=\s*["']([^"']+)["'][^>]*>""")
URL_RE=re.compile(r"""https?://[^\s"'<>]+\.(?:jpg|jpeg|png|webp)(?:\?[^\s"'<>]*)?""",re.I)

def clean(v,n=8000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=25,max_bytes=4_000_000):
    req=urllib.request.Request(url,headers={
        "User-Agent":UA,"Accept":"text/html,image/*,*/*","Accept-Language":"zh-CN,zh;q=0.9,en;q=0.5"
    })
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        if len(b)>max_bytes: raise ValueError("response-too-large")
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b

def absolutize(raw,base=PAGE):
    u=html.unescape(raw.strip())
    if u.startswith("//"): return "https:"+u
    return urllib.parse.urljoin(base,u)

def section(text):
    anchors=("游戏安装光盘","遊戲安裝光碟")
    start=-1
    for a in anchors:
        start=text.find(a)
        if start>=0: break
    if start<0: return "",-1,-1
    ends=[x for x in (text.find("游戏说明书",start),text.find("遊戲說明書",start)) if x>=0]
    end=min(ends) if ends else min(len(text),start+30000)
    return text[start:end],start,end

def image_urls(seg):
    out=[]; seen=set()
    for raw in IMG_RE.findall(seg)+URL_RE.findall(seg):
        u=absolutize(raw)
        low=u.lower()
        if any(x in low for x in ("emotion","avatar","logo","icon","loading","blank")): continue
        if u not in seen:
            seen.add(u); out.append(u)
    return tuple(out)

def main():
    print("StoneAge 2.5 SMZDM surviving install-disc visual probe — R1")
    print("SCOPE|2016-public-collector-post+transient-images|derived-metadata-only|no-image-commit|no-game-payload")
    errors=[]
    st,final,h,b=fetch(PAGE)
    enc,text=decode(b,declared_charset(b))
    seg,start,end=section(text)
    urls=image_urls(seg)
    print(f"PAGE|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|encoding={clean(enc)}|section_start={start}|section_end={end}|images={len(urls)}|final={clean(final)}")
    print(f"SECTION_TEXT|value={clean(visible(seg),14000)}")
    for i,u in enumerate(urls,1):
        print(f"IMAGE_URL|order={i}|url={clean(u)}")

    collector=[]
    for i,u in enumerate(urls,1):
        try:
            f=load_image(f"smzdm:{i}",u,referer=PAGE,timeout=20,attempts=2)
            collector.append(f)
            print(f"IMAGE|order={i}|bytes={f['bytes']}|sha256={f['sha256']}|size={f['width']}x{f['height']}|dhash={f['dhash']}|keypoints={len(f['kp'])}|url={clean(f['url'])}")
        except Exception as e:
            errors.append((f"image:{i}",type(e).__name__,str(e)))

    controls=[]
    try:
        for row in ruten_full_images():
            if str(row.get("carrier")) not in {"21926883918096","22242541948520","22632305238624"}:
                continue
            try:
                f=load_image(row["label"],row["url"],referer="https://www.ruten.com.tw/",timeout=18,attempts=1)
                controls.append(f)
            except Exception as e:
                errors.append((str(row.get("label")),type(e).__name__,str(e)))
    except Exception as e:
        errors.append(("ruten-metadata",type(e).__name__,str(e)))

    matches=[]
    for a in collector:
        for c in controls:
            m=match_features(a,c)
            matches.append((m["inliers"],m["good"],a,c,m))
    matches.sort(key=lambda x:(x[0],x[1]),reverse=True)
    for _,_,a,c,m in matches[:80]:
        print(f"MATCH|smzdm={clean(a['label'])}|control={clean(c['label'])}|orb_matches={m['matches']}|good_le64={m['good']}|ransac_inliers={m['inliers']}|inlier_ratio={m['inlier_ratio']:.4f}|smzdm_url={clean(a.get('url'))}|control_url={clean(c.get('url'))}")

    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|section_images|{len(urls)}")
    print(f"COUNT|images_loaded|{len(collector)}")
    print(f"COUNT|controls_loaded|{len(controls)}")
    print(f"COUNT|match_pairs|{len(matches)}")
    print(f"COUNT|errors|{len(errors)}")
    if collector:
        print("RESOLUTION|INDEPENDENT_SURVIVING_DISC_PHOTO_RECOVERED|use as independent physical-survival and visual-family control")
    elif urls:
        print("RESOLUTION|DISC_PHOTO_URLS_RECOVERED_BODY_UNAVAILABLE|retain exact URLs for later cache/archive recovery")
    else:
        print("RESOLUTION|SMZDM_DISC_IMAGE_MAPPING_UNRESOLVED|retain text-only survival evidence")
    print("EVIDENCE_BOUNDARY|collector photos can corroborate survival and artwork family only; they cannot establish disc filesystem, mastering, installer build, or clean-client byte provenance.")

if __name__=="__main__":
    main()
