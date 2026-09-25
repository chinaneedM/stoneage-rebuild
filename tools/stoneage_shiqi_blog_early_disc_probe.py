#!/usr/bin/env python3
"""Inventory a public collector article about early StoneAge client discs.

The current blog index exposes an article titled 石器时代游戏周边收藏客户端光盘1.82-2.2.
This probe discovers the article URL from the category page, records bounded
text evidence and transiently hashes article images. It never commits images or
game payloads. Exact image SHA comparison is used only to detect byte-identical
reuse of the already locked SMZDM 2.0 newbie-disc photograph.
"""
from __future__ import annotations
import hashlib,html,re,urllib.parse,urllib.request

UA="stoneage-rebuild-archaeology/1.0"
INDEX="https://blog.shiqi.so/sqcy4.htm"
TITLE="石器时代游戏周边收藏客户端光盘1.82-2.2"
SMZDM_SHA256="98ad75b6eb5fa5aca6fa7e37095bd207779321ea4991ccf0754117cfaf3884c3"
TEXT_TOKENS=("1.82","2.0","大陆","台版","台湾","客户端","新手","杂志","攻略","光盘","北京华义","WAEI")

def clean(v,n=5000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=40,max_bytes=8*1024*1024,accept="text/html,*/*;q=0.5"):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":accept,"Accept-Encoding":"identity","Referer":INDEX})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        if len(b)>max_bytes: raise ValueError(f"response-too-large:{len(b)}")
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b

def decode(b):
    for enc in ("utf-8","gb18030","big5","latin1"):
        try:return b.decode(enc)
        except UnicodeDecodeError:pass
    return b.decode("utf-8","replace")

def strip_tags(s):
    s=re.sub(r"(?is)<script.*?</script>|<style.*?</style>"," ",s)
    s=re.sub(r"(?s)<[^>]+>"," ",s)
    return html.unescape(re.sub(r"\s+"," ",s)).strip()

def discover_article(index_html,base=INDEX):
    candidates=[]
    for m in re.finditer(r'(?is)<a\b[^>]*href\s*=\s*["\']([^"\']+)["\'][^>]*>(.*?)</a>',index_html):
        href=html.unescape(m.group(1)).strip()
        text=strip_tags(m.group(2))
        if TITLE in text or ("客户端光盘" in text and "1.82" in text and "2.2" in text):
            candidates.append(urllib.parse.urljoin(base,href))
    return tuple(dict.fromkeys(candidates))

def image_urls(article_html,base):
    out=[]
    for m in re.finditer(r'(?is)<img\b[^>]*\bsrc\s*=\s*["\']([^"\']+)["\']',article_html):
        raw=html.unescape(m.group(1)).strip()
        if raw and not raw.startswith(("data:","javascript:")):
            out.append(urllib.parse.urljoin(base,raw))
    return tuple(dict.fromkeys(out))

def relevant_text(article_html):
    txt=strip_tags(article_html)
    parts=re.split(r"(?<=[。！？!?])|\s{2,}",txt)
    rows=[]
    for p in parts:
        p=" ".join(p.split())
        if p and any(t.lower() in p.lower() for t in TEXT_TOKENS):
            rows.append(p)
    return tuple(dict.fromkeys(rows))

def main():
    print("StoneAge early-client-disc collector article probe — R1")
    print("SCOPE|blog.shiqi.so collector article discovery+text+transient image hashes|no-image-commit|no-payload")
    errors=[]
    try:
        st,final,h,b=fetch(INDEX)
        ih=decode(b)
        articles=discover_article(ih,final)
        print(f"INDEX|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}|article_candidates={len(articles)}")
    except Exception as e:
        errors.append(("index",type(e).__name__,str(e)));articles=()
    print(f"COUNT|article_candidates|{len(articles)}")
    images_total=0; exact_smzdm=0
    for i,u in enumerate(articles,1):
        try:
            st,final,h,b=fetch(u)
            ah=decode(b)
            texts=relevant_text(ah)
            imgs=image_urls(ah,final)
            print(f"ARTICLE|index={i}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|url={clean(final)}|text_hits={len(texts)}|images={len(imgs)}")
            for j,t in enumerate(texts[:80],1):
                print(f"TEXT_HIT|article={i}|index={j}|text={clean(t,1800)}")
            for j,img in enumerate(imgs,1):
                try:
                    ist,ifinal,hh,bb=fetch(img,max_bytes=12*1024*1024,accept="image/*,*/*;q=0.2")
                    sha=hashlib.sha256(bb).hexdigest()
                    same=int(sha==SMZDM_SHA256)
                    images_total+=1;exact_smzdm+=same
                    print(f"IMAGE|article={i}|index={j}|status={ist}|bytes={len(bb)}|sha256={sha}|exact_smzdm_2.0={same}|url={clean(ifinal)}")
                except Exception as e:
                    errors.append((f"image:{i}:{j}:{img}",type(e).__name__,str(e)))
        except Exception as e:
            errors.append((f"article:{i}:{u}",type(e).__name__,str(e)))
    print(f"COUNT|images_hashed|{images_total}")
    print(f"COUNT|exact_smzdm_image_reuse|{exact_smzdm}")
    for s,k,m in errors:
        print(f"ERROR|scope={clean(s)}|kind={clean(k)}|message={clean(m)}")
    print(f"COUNT|errors|{len(errors)}")
    if articles and images_total:
        print("RESOLUTION|COLLECTOR_ARTICLE_INVENTORIED|classify visible disc/version identifiers; exact SHA only closes byte-identical reposting")
    elif articles:
        print("RESOLUTION|ARTICLE_FOUND_IMAGES_UNAVAILABLE|retain text/source identity and reopen image path only if needed")
    elif errors:
        print("RESOLUTION|COLLECTOR_SOURCE_INCOMPLETE|do not promote physical-disc claims")
    else:
        print("RESOLUTION|ARTICLE_NOT_DISCOVERED|current index surface does not expose the expected article href")
    print("EVIDENCE_BOUNDARY|collector pages/photos prove only current physical-survival/label evidence; they do not establish optical filesystem, pressing, installer identity or historical byte provenance.")

if __name__=="__main__":
    main()
