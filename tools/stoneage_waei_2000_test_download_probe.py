#!/usr/bin/env python3
"""Probe archived Beijing-Waei domains for the Dec-2000/Jan-2001 StoneAge trial download.

Evidence anchor:
- A 2001-06-13 17173 player diary records that on 2001-01-04 the author
  visited Beijing Waei's homepage, saw a StoneAge "试玩版" available for
  download, and observed a download size of roughly 274 MB.
- The project independently confirms a physical official test CD and a
  Dec-15-2000..Jan-10-2001 public-test window.

This probe searches only archive routing/HTML metadata. It never downloads
candidate game binaries.
"""
from __future__ import annotations

import hashlib
import html
import json
import re
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
FROM="20001201"
TO="20010112"
DOMAINS=(
    ("waei","waei.com.cn"),
    ("wayi","wayi.com.cn"),
    ("wgs","wgs.com.cn"),
)
MAX_ROWS=20000
MAX_HTML_REPLAYS=50
MAX_HTML_BYTES=768*1024

STONE_TOKENS=(
    "stoneage","stone age","石器时代","石器時代","shiqi",
)
DOWNLOAD_TOKENS=(
    "download","down/","/down","下载","下載","client","客户端","客戶端",
    "setup","install","trial","试玩","試玩","test","测试","測試","demo",
)
BINARY_EXTS=(".exe",".zip",".rar",".cab",".arj",".lzh",".7z")
NOISE_TOKENS=("wallpaper","screen","screenshot","pic","image","forum","bbs","newsimg")


def clean(v,n=5000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]


def fetch(url,timeout=35,max_bytes=MAX_HTML_BYTES):
    req=urllib.request.Request(url,headers={
        "User-Agent":UA,
        "Accept":"application/json,text/html,text/plain,*/*;q=0.2",
        "Accept-Encoding":"identity",
    })
    with urllib.request.urlopen(req,timeout=timeout) as r:
        body=r.read(max_bytes+1)
        if len(body)>max_bytes:
            raise ValueError(f"response-too-large:{len(body)}")
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),body


def cdx_url(domain):
    params=[
        ("url",domain),
        ("matchType","domain"),
        ("output","json"),
        ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
        ("from",FROM),
        ("to",TO),
        ("limit",str(MAX_ROWS)),
        ("collapse","urlkey"),
    ]
    return CDX+"?"+urllib.parse.urlencode(params)


def rows(body):
    obj=json.loads(body.decode("utf-8"))
    if not isinstance(obj,list) or len(obj)<2:
        return ()
    head=obj[0]
    return tuple(dict(zip(head,r)) for r in obj[1:] if isinstance(r,list))


def decoded_url(url):
    return urllib.parse.unquote_plus(str(url or "")).lower()


def is_binary_url(url):
    path=urllib.parse.urlsplit(decoded_url(url)).path
    return path.endswith(BINARY_EXTS)


def is_noise(url):
    low=decoded_url(url)
    return any(t in low for t in NOISE_TOKENS)


def target_score(row):
    url=str(row.get("original") or "")
    low=decoded_url(url)
    path=urllib.parse.urlsplit(low).path
    score=0
    if any(t.lower() in low for t in STONE_TOKENS):
        score+=18
    if any(t.lower() in low for t in DOWNLOAD_TOKENS):
        score+=12
    if is_binary_url(url):
        score+=15
    if is_noise(url):
        score-=15
    mt=str(row.get("mimetype") or "").lower()
    if "html" in mt:
        score+=2
    if path.count("/")<=2:
        score+=2
    return score


def html_candidate(row):
    url=str(row.get("original") or "")
    mt=str(row.get("mimetype") or "").lower()
    path=urllib.parse.urlsplit(url).path.lower()
    looks_html=("html" in mt or path.endswith((".htm",".html",".asp",".shtml",".php")) or path.endswith("/"))
    if not looks_html or is_noise(url):
        return False
    low=decoded_url(url)
    return (
        any(t.lower() in low for t in STONE_TOKENS)
        or any(t.lower() in low for t in DOWNLOAD_TOKENS)
        or path in ("","/")
        or path.count("/")<=2
    )


def replay_url(ts,orig):
    return f"https://web.archive.org/web/{ts}id_/{orig}"


def decode_body(body):
    for enc in ("gb18030","gbk","gb2312","big5","utf-8","latin1"):
        try:
            return enc,body.decode(enc)
        except UnicodeDecodeError:
            continue
    return "latin1",body.decode("latin1","replace")


def extract_links(text,base):
    out=[]
    pat=re.compile(r'(?is)<a\b[^>]*href\s*=\s*["\']([^"\']+)["\'][^>]*>(.*?)</a>')
    for m in pat.finditer(text):
        href=html.unescape(m.group(1)).strip()
        anchor=re.sub(r"(?s)<[^>]+>"," ",m.group(2))
        anchor=html.unescape(re.sub(r"\s+"," ",anchor)).strip()
        if not href or href.lower().startswith(("javascript:","mailto:","#")):
            continue
        out.append((urllib.parse.urljoin(base,href),anchor))
    return tuple(out)


def page_semantics(text):
    plain=html.unescape(re.sub(r"(?s)<[^>]+>"," ",text))
    plain=re.sub(r"\s+"," ",plain)
    low=plain.lower()
    stones=[t for t in STONE_TOKENS if t.lower() in low]
    downs=[t for t in DOWNLOAD_TOKENS if t.lower() in low]
    return stones,downs,bool(stones and downs)


def link_target(href,anchor):
    low=decoded_url(href+" "+anchor)
    return (
        is_binary_url(href)
        or any(t.lower() in low for t in STONE_TOKENS)
        or any(t.lower() in low for t in DOWNLOAD_TOKENS)
    ) and not is_noise(href)


def main():
    print("StoneAge Beijing-Waei Dec-2000/Jan-2001 trial-download archive probe — R1")
    print(f"SCOPE|domains={','.join(d for _,d in DOMAINS)}|window={FROM}..{TO}|CDX+HTML-links|no-binary-payload")
    print("EVIDENCE_ANCHOR|17173 diary dated 2001-06-13 records Waei homepage trial download on 2001-01-04 at roughly 274 MB")
    errors=[]
    all_rows=[]
    completed=0

    for label,domain in DOMAINS:
        try:
            st,final,h,b=fetch(cdx_url(domain),timeout=55,max_bytes=8*1024*1024)
            rr=rows(b)
            completed+=1
            print(f"CDX|label={label}|domain={domain}|status={st}|rows={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
            for r in rr:
                all_rows.append((label,r))
        except Exception as exc:
            errors.append((f"cdx:{label}",type(exc).__name__,str(exc)))

    # Deduplicate equivalent archived URLs across domain queries.
    uniq={}
    for label,r in all_rows:
        key=(str(r.get("original") or ""),str(r.get("digest") or ""),str(r.get("timestamp") or ""))
        uniq[key]=(label,r)

    scored=[]
    binary_rows=[]
    for label,r in uniq.values():
        score=target_score(r)
        if score>0:
            scored.append((score,label,r))
        if is_binary_url(str(r.get("original") or "")) and not is_noise(str(r.get("original") or "")):
            binary_rows.append((label,r))
    scored.sort(key=lambda x:(x[0],str(x[2].get("timestamp") or "")),reverse=True)
    binary_rows.sort(key=lambda x:(x[0],str(x[1].get("original") or "")))

    print(f"COUNT|completed_domains|{completed}")
    print(f"COUNT|unique_rows|{len(uniq)}")
    print(f"COUNT|positive_scored_rows|{len(scored)}")
    print(f"COUNT|binary_extension_rows|{len(binary_rows)}")

    for score,label,r in scored[:160]:
        print(
            f"ROW_HIT|score={score}|label={label}|timestamp={clean(r.get('timestamp'))}|"
            f"original={clean(r.get('original'))}|status={clean(r.get('statuscode'))}|"
            f"mimetype={clean(r.get('mimetype'))}|length={clean(r.get('length'))}|"
            f"digest={clean(r.get('digest'))}|redirect={clean(r.get('redirect'))}"
        )

    selected=[]
    seen_urls=set()
    candidates=[(target_score(r),label,r) for label,r in uniq.values() if html_candidate(r)]
    candidates.sort(key=lambda x:(x[0],str(x[2].get("timestamp") or "")),reverse=True)
    for score,label,r in candidates:
        orig=str(r.get("original") or "")
        if orig in seen_urls:
            continue
        seen_urls.add(orig)
        selected.append((score,label,r))
        if len(selected)>=MAX_HTML_REPLAYS:
            break

    print(f"COUNT|html_candidates|{len(candidates)}")
    print(f"COUNT|selected_html_replays|{len(selected)}")
    replayed=0
    semantic_pages=0
    link_hits={}

    for idx,(score,label,r) in enumerate(selected,1):
        ts=str(r.get("timestamp") or "")
        orig=str(r.get("original") or "")
        try:
            st,final,h,b=fetch(replay_url(ts,orig),timeout=35,max_bytes=MAX_HTML_BYTES)
            replayed+=1
            enc,text=decode_body(b)
            stones,downs,sem=page_semantics(text)
            if sem:
                semantic_pages+=1
            links=extract_links(text,orig)
            hits=[(u,a) for u,a in links if link_target(u,a)]
            print(
                f"PAGE|index={idx}|score={score}|label={label}|timestamp={ts}|status={st}|"
                f"bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|encoding={enc}|"
                f"semantic={int(sem)}|stone={clean(','.join(stones),600)}|download={clean(','.join(downs),600)}|"
                f"links={len(links)}|target_links={len(hits)}|orig={clean(orig)}"
            )
            for u,a in hits:
                key=(u,a)
                link_hits[key]=orig
                print(f"LINK_HIT|page={clean(orig)}|href={clean(u)}|anchor={clean(a,1000)}|binary={int(is_binary_url(u))}")
        except Exception as exc:
            errors.append((f"page:{idx}:{orig}",type(exc).__name__,str(exc)))

    binary_links=[(u,a,p) for (u,a),p in link_hits.items() if is_binary_url(u)]
    print(f"COUNT|pages_replayed|{replayed}")
    print(f"COUNT|semantic_pages|{semantic_pages}")
    print(f"COUNT|unique_target_links|{len(link_hits)}")
    print(f"COUNT|binary_link_hits|{len(binary_links)}")
    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|errors|{len(errors)}")

    if binary_links:
        print("RESOLUTION|EARLY_WAEI_BINARY_LINK_FOUND|verify archive metadata/redirect identity next; do not fetch binary yet")
    elif semantic_pages or link_hits or scored:
        print("RESOLUTION|EARLY_WAEI_TOPOLOGY_SIGNAL_FOUND|classify source-derived rows/pages and expand exact paths only")
    elif errors and completed<len(DOMAINS):
        print("RESOLUTION|EARLY_WAEI_ARCHIVE_SURFACE_INCOMPLETE|retry failed domains only")
    else:
        print("RESOLUTION|EARLY_WAEI_DOMAIN_ROUTE_BOUNDED_AT_CURRENT_INDEX|no source-specific download token recovered from tested archive window")
    print("EVIDENCE_BOUNDARY|Archive URLs and HTML links prove routing/distribution only; no candidate client byte identity is inferred or downloaded.")

if __name__=="__main__":
    main()
