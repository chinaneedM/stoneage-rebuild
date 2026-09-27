#!/usr/bin/env python3
"""Inspect non-personal asset topology of archived China.com article 63271.

No raw HTML or image body is committed. The probe:
- replays the earliest known archived article capture;
- extracts first-party asset paths from IMG/SCRIPT/LINK/BODY backgrounds;
- replays image assets transiently at the same timestamp;
- records only path, status, MIME, byte count, SHA-256 and image dimensions.

This is intended to discover an exact activity/test-disc artwork filename while
keeping historical participant identities and asset bodies out of the repo.
"""
from __future__ import annotations

import hashlib
import html
import re
import struct
import urllib.parse
import urllib.request
from html.parser import HTMLParser

UA="stoneage-rebuild-archaeology/1.0"
TS="20010309223137"
ORIGINAL="http://game.china.com:80/zh_cn/news/news1/444/20001220/63271.html"
MAX_HTML=512_000
MAX_ASSET=2_000_000
FIRST_PARTY={"game.china.com","www.china.com","china.com"}
IMAGE_EXTS=(".gif",".jpg",".jpeg",".png",".bmp",".webp")
GENERIC_HINTS=(
    "/images/", "/image/", "/img/", "logo", "banner", "menu", "nav",
    "arrow", "dot", "line", "button", "title", "top", "left", "right",
)


def clean(value,limit=2200):
    text=" ".join(str(value if value is not None else "").split())
    return "".join(ch for ch in text if ch>=" " and ch!="\x7f").replace("|","%7C")[:limit]


def replay_url(original,mode="id_"):
    return f"https://web.archive.org/web/{TS}{mode}/{original}"


def fetch(url,timeout=45,max_bytes=MAX_ASSET):
    req=urllib.request.Request(url,headers={
        "User-Agent":UA,
        "Accept":"*/*",
        "Accept-Encoding":"identity",
    })
    with urllib.request.urlopen(req,timeout=timeout) as r:
        body=r.read(max_bytes+1)
        if len(body)>max_bytes:
            raise ValueError(f"body exceeds limit: {len(body)}")
        return int(getattr(r,"status",r.getcode())),r.geturl(),r.headers,body


def canonical_first_party(raw):
    raw=html.unescape(str(raw or "")).strip()
    if not raw or raw.lower().startswith(("data:","javascript:","mailto:","tel:","#")):
        return None
    joined=urllib.parse.urljoin(ORIGINAL,raw)
    p=urllib.parse.urlsplit(joined)
    host=(p.hostname or "").lower()
    if host not in FIRST_PARTY:
        return None
    scheme=p.scheme if p.scheme in ("http","https") else "http"
    # Strip queries/fragments; only non-personal path topology is retained.
    return urllib.parse.urlunsplit((scheme,p.netloc,p.path or "/", "", ""))


class AssetParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.assets=[]

    def add(self,kind,value):
        url=canonical_first_party(value)
        if url and (kind,url) not in self.assets:
            self.assets.append((kind,url))

    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        low=tag.lower()
        if low=="img":
            self.add("img",a.get("src"))
        elif low=="script":
            self.add("script",a.get("src"))
        elif low=="link":
            self.add("link",a.get("href"))
        elif low in ("body","table","td","tr"):
            self.add("background",a.get("background"))


def decode_html(headers,body):
    encs=[]
    try:
        cs=headers.get_content_charset()
    except Exception:
        cs=None
    if cs:
        encs.append(cs)
    head=body[:8192].decode("latin1","ignore")
    for m in re.finditer(r'charset\s*=\s*["\']?\s*([a-zA-Z0-9._-]+)',head,re.I):
        encs.append(m.group(1))
    encs+=["gb18030","gbk","gb2312","utf-8","latin1"]
    best=None
    for enc in encs:
        try:
            text=body.decode(enc,errors="replace")
        except Exception:
            continue
        score=sum(1 for ch in text if "\u4e00"<=ch<="\u9fff")-text.count("\ufffd")*20
        if best is None or score>best[0]:
            best=(score,enc,text)
    return (best[1],best[2]) if best else ("unknown",body.decode("utf-8","replace"))


def image_dimensions(body,mime="",path=""):
    low=(path or "").lower()
    m=(mime or "").lower()
    try:
        if body.startswith(b"\x89PNG\r\n\x1a\n") and len(body)>=24:
            w,h=struct.unpack(">II",body[16:24])
            return w,h
        if body[:6] in (b"GIF87a",b"GIF89a") and len(body)>=10:
            w,h=struct.unpack("<HH",body[6:10])
            return w,h
        if body.startswith(b"BM") and len(body)>=26:
            w,h=struct.unpack("<ii",body[18:26])
            return abs(w),abs(h)
        if body.startswith(b"\xff\xd8"):
            i=2
            while i+9<len(body):
                if body[i]!=0xFF:
                    i+=1
                    continue
                marker=body[i+1]
                i+=2
                if marker in (0xD8,0xD9):
                    continue
                if i+2>len(body):
                    break
                seglen=struct.unpack(">H",body[i:i+2])[0]
                if marker in (0xC0,0xC1,0xC2,0xC3,0xC5,0xC6,0xC7,0xC9,0xCA,0xCB,0xCD,0xCE,0xCF) and i+7<len(body):
                    h,w=struct.unpack(">HH",body[i+3:i+7])
                    return w,h
                i+=max(2,seglen)
    except Exception:
        pass
    return 0,0


def is_image_url(url):
    return urllib.parse.urlsplit(url).path.lower().endswith(IMAGE_EXTS)


def specificity(path,w,h,size):
    low=path.lower()
    generic=sum(1 for hint in GENERIC_HINTS if hint in low)
    large=int(w>=300 and h>=180) + int(size>=40_000)
    return large-generic


def main():
    print("StoneAge China.com article 63271 asset-topology probe — R1")
    print("SCOPE|earliest archived article|first-party asset paths + transient image metadata only|no participant data|no asset bodies committed")
    errors=[]

    status,final,headers,body=fetch(replay_url(ORIGINAL),max_bytes=MAX_HTML)
    enc,text=decode_html(headers,body)
    parser=AssetParser()
    parser.feed(text)
    print(f"PAGE|timestamp={TS}|status={status}|bytes={len(body)}|sha256={hashlib.sha256(body).hexdigest()}|encoding={clean(enc)}|assets={len(parser.assets)}|final={clean(final)}")

    images=[]
    others=[]
    for kind,url in parser.assets:
        path=urllib.parse.urlsplit(url).path
        if kind in ("img","background") or is_image_url(url):
            images.append((kind,url,path))
        else:
            others.append((kind,url,path))

    print(f"COUNT|image_asset_paths|{len(images)}")
    print(f"COUNT|other_asset_paths|{len(others)}")
    for kind,url,path in others[:100]:
        print(f"ASSET_PATH|kind={kind}|path={clean(path)}")

    candidates=0
    replayed=0
    for kind,url,path in images:
        try:
            st,fin,hdrs,data=fetch(replay_url(url),max_bytes=MAX_ASSET)
            replayed+=1
            mime=(hdrs.get_content_type() if hasattr(hdrs,"get_content_type") else hdrs.get("Content-Type",""))
            w,h=image_dimensions(data,mime,path)
            score=specificity(path,w,h,len(data))
            if score>0:
                candidates+=1
            print(f"IMAGE_META|kind={kind}|path={clean(path)}|status={st}|mime={clean(mime)}|bytes={len(data)}|sha256={hashlib.sha256(data).hexdigest()}|width={w}|height={h}|specificity={score}|final={clean(fin)}")
        except Exception as exc:
            errors.append((kind,path,type(exc).__name__,str(exc)))
            print(f"IMAGE_PATH|kind={kind}|path={clean(path)}|replay=failed")

    for kind,path,ename,msg in errors:
        print(f"ERROR|kind={clean(kind)}|path={clean(path)}|error={clean(ename)}|message={clean(msg)}")

    print(f"COUNT|image_assets_replayed|{replayed}")
    print(f"COUNT|candidate_large_specific_assets|{candidates}")
    print(f"COUNT|errors|{len(errors)}")
    if candidates:
        print("RESOLUTION|PAGE_SPECIFIC_IMAGE_CANDIDATES_FOUND|inspect filenames/dimensions only and follow source-driven candidates")
    elif errors:
        print("RESOLUTION|PARTIAL_ASSET_TOPOLOGY|retry failed archived image paths only")
    else:
        print("RESOLUTION|63271_ASSET_ROUTE_BOUNDED|all replayable images appear generic/small under current heuristic")
    print("EVIDENCE_BOUNDARY|Asset metadata and dimensions do not prove depicted content. No image body or participant data is persisted.")

if __name__=="__main__":
    main()
