#!/usr/bin/env python3
"""Probe Waei's historical central download center for early StoneAge entries.

Evidence:
- the official StoneAge site lived under www7.waei.net/wgs/stoneage/;
- surviving later archive references show Waei used
  www7.waei.net/download/dldetial.asp?... and /download/file/ as a central
  download system;
- a 17173 diary reports a ~274 MB StoneAge trial download visible on Waei's
  homepage on 2001-01-04.

This probe searches archived download-center metadata/pages from Dec-2000
through Jun-2001. It does not download candidate game binaries.
"""
from __future__ import annotations

import hashlib, html, json, re, urllib.parse, urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
PREFIX="http://www7.waei.net/download/"
FROM="20001201"
TO="20010630"
MAX_ROWS=30000
MAX_PAGES=160
MAX_BODY=1024*1024

STONE=("stoneage","stone age","石器时代","石器時代","石器")
TRIAL=("trial","demo","test","试玩","試玩","测试","測試")
CLIENT=("client","客户端","客戶端","完整","安裝","安装","setup")
DOWNLOAD=("download","下載","下载","檔案","档案","file")
BINARY_EXTS=(".exe",".zip",".rar",".cab",".arj",".lzh",".7z")


def clean(v,n=5000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]


def fetch(url,timeout=45,max_bytes=MAX_BODY):
    req=urllib.request.Request(url,headers={
        "User-Agent":UA,
        "Accept":"application/json,text/html,text/plain,*/*;q=0.2",
        "Accept-Encoding":"identity",
    })
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        if len(b)>max_bytes:
            raise ValueError(f"response-too-large:{len(b)}")
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b


def cdx_url():
    params=[
        ("url",PREFIX),("matchType","prefix"),("output","json"),
        ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
        ("from",FROM),("to",TO),("limit",str(MAX_ROWS)),("collapse","urlkey"),
    ]
    return CDX+"?"+urllib.parse.urlencode(params)


def rows(body):
    obj=json.loads(body.decode("utf-8"))
    if not isinstance(obj,list) or len(obj)<2:return ()
    head=obj[0]
    return tuple(dict(zip(head,r)) for r in obj[1:] if isinstance(r,list))


def low(v):
    return urllib.parse.unquote_plus(str(v or "")).lower()


def is_binary(url):
    return urllib.parse.urlsplit(low(url)).path.endswith(BINARY_EXTS)


def html_candidate(r):
    url=str(r.get("original") or "")
    mt=str(r.get("mimetype") or "").lower()
    path=urllib.parse.urlsplit(url).path.lower()
    return "html" in mt or path.endswith((".asp",".htm",".html",".shtml",".php")) or path.endswith("/")


def page_score(r):
    url=low(r.get("original"))
    s=0
    if "dldetial" in url or "detail" in url: s+=10
    if "dllist" in url or "list" in url or url.rstrip("/").endswith("/download"): s+=8
    if any(t in url for t in STONE): s+=20
    if any(t in url for t in TRIAL+CLIENT): s+=10
    if is_binary(url): s+=15
    ts=str(r.get("timestamp") or "")
    if ts.startswith(("200012","200101")): s+=6
    return s


def replay_url(ts,orig):
    return f"https://web.archive.org/web/{ts}id_/{orig}"


def decode(body):
    for enc in ("big5","gb18030","gbk","gb2312","utf-8","latin1"):
        try:return enc,body.decode(enc)
        except UnicodeDecodeError:pass
    return "latin1",body.decode("latin1","replace")


def plain_text(text):
    p=html.unescape(re.sub(r"(?s)<script.*?</script>|<style.*?</style>"," ",text))
    p=html.unescape(re.sub(r"(?s)<[^>]+>"," ",p))
    return re.sub(r"\s+"," ",p)


def semantics(text):
    p=plain_text(text); l=p.lower()
    stone=[t for t in STONE if t.lower() in l]
    trial=[t for t in TRIAL if t.lower() in l]
    client=[t for t in CLIENT if t.lower() in l]
    down=[t for t in DOWNLOAD if t.lower() in l]
    s274=bool(re.search(r"274\s*(?:m|mb|兆)",l,re.I))
    return stone,trial,client,down,s274


def links(text,base):
    out=[]
    for m in re.finditer(r'(?is)<a\b[^>]*href\s*=\s*["\']([^"\']+)["\'][^>]*>(.*?)</a>',text):
        href=html.unescape(m.group(1)).strip()
        anchor=html.unescape(re.sub(r"\s+"," ",re.sub(r"(?s)<[^>]+>"," ",m.group(2)))).strip()
        if not href or href.lower().startswith(("javascript:","mailto:","#")):continue
        out.append((urllib.parse.urljoin(base,href),anchor))
    return tuple(out)


def target_link(href,anchor):
    l=low(href+" "+anchor)
    return is_binary(href) or any(t.lower() in l for t in STONE+TRIAL+CLIENT)


def main():
    print("StoneAge Waei central-download archive probe — R1")
    print(f"SCOPE|prefix={PREFIX}|window={FROM}..{TO}|archived metadata+HTML only|no-binary-payload")
    print("EVIDENCE_ANCHOR|17173-2001-01-04 trial~274MB + historical Waei central download-center topology")
    errors=[]
    try:
        st,final,h,b=fetch(cdx_url(),timeout=60,max_bytes=12*1024*1024)
        rr=rows(b)
        print(f"CDX|status={st}|rows={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
    except Exception as exc:
        errors.append(("cdx",type(exc).__name__,str(exc)));rr=()

    binaries=[r for r in rr if is_binary(str(r.get("original") or ""))]
    print(f"COUNT|rows|{len(rr)}")
    print(f"COUNT|binary_rows|{len(binaries)}")
    for r in binaries[:200]:
        print(f"BINARY_ROW|timestamp={clean(r.get('timestamp'))}|original={clean(r.get('original'))}|status={clean(r.get('statuscode'))}|mime={clean(r.get('mimetype'))}|length={clean(r.get('length'))}|digest={clean(r.get('digest'))}|redirect={clean(r.get('redirect'))}")

    cands=[r for r in rr if html_candidate(r)]
    cands.sort(key=lambda r:(page_score(r),str(r.get("timestamp") or "")),reverse=True)
    selected=[];seen=set()
    for r in cands:
        orig=str(r.get("original") or "")
        # Distinct URL only; preserve best-scored/newer capture for bounded replay.
        if orig in seen:continue
        seen.add(orig);selected.append(r)
        if len(selected)>=MAX_PAGES:break
    print(f"COUNT|html_candidates|{len(cands)}")
    print(f"COUNT|selected_pages|{len(selected)}")

    replayed=0;stone_pages=0;trial_pages=0;size274_pages=0;link_hits={}
    for i,r in enumerate(selected,1):
        ts=str(r.get("timestamp") or "");orig=str(r.get("original") or "")
        try:
            st,final,h,b=fetch(replay_url(ts,orig),timeout=40,max_bytes=MAX_BODY)
            replayed+=1
            enc,text=decode(b)
            stone,trial,client,down,s274=semantics(text)
            if stone:stone_pages+=1
            if stone and trial:trial_pages+=1
            if s274:size274_pages+=1
            ls=links(text,orig)
            hits=[(u,a) for u,a in ls if target_link(u,a)]
            interesting=bool(stone or trial or client or s274 or hits or page_score(r)>=10)
            if interesting:
                print(
                  f"PAGE|index={i}|score={page_score(r)}|timestamp={ts}|status={st}|bytes={len(b)}|"
                  f"sha256={hashlib.sha256(b).hexdigest()}|encoding={enc}|stone={clean(','.join(stone),500)}|"
                  f"trial={clean(','.join(trial),500)}|client={clean(','.join(client),500)}|download={clean(','.join(down),500)}|"
                  f"size274={int(s274)}|links={len(ls)}|target_links={len(hits)}|orig={clean(orig)}"
                )
            for u,a in hits:
                link_hits[(u,a)]=orig
                print(f"LINK|page={clean(orig)}|href={clean(u)}|anchor={clean(a,1000)}|binary={int(is_binary(u))}")
        except Exception as exc:
            errors.append((f"page:{i}:{orig}",type(exc).__name__,str(exc)))

    binary_links=[(u,a,p) for (u,a),p in link_hits.items() if is_binary(u)]
    print(f"COUNT|pages_replayed|{replayed}")
    print(f"COUNT|stone_pages|{stone_pages}")
    print(f"COUNT|stone_trial_pages|{trial_pages}")
    print(f"COUNT|size274_pages|{size274_pages}")
    print(f"COUNT|unique_target_links|{len(link_hits)}")
    print(f"COUNT|binary_link_hits|{len(binary_links)}")
    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|errors|{len(errors)}")

    if binary_links or binaries:
        print("RESOLUTION|WAEI_DOWNLOAD_CENTER_BINARY_ROUTE_FOUND|classify exact file identity and archive metadata next")
    elif trial_pages or size274_pages:
        print("RESOLUTION|WAEI_DOWNLOAD_CENTER_TRIAL_SIGNAL_FOUND|follow exact detail/list page topology next")
    elif stone_pages or link_hits:
        print("RESOLUTION|WAEI_DOWNLOAD_CENTER_STONEAGE_SIGNAL_FOUND|follow exact IDs/links next")
    elif errors and replayed==0:
        print("RESOLUTION|WAEI_DOWNLOAD_CENTER_REPLAY_INCOMPLETE|do not close route")
    else:
        print("RESOLUTION|WAEI_DOWNLOAD_CENTER_ROUTE_BOUNDED|current archived central-download pages expose no early StoneAge trial signal")
    print("EVIDENCE_BOUNDARY|HTML/archive metadata are routing evidence only. No game binary is fetched or authenticated.")

if __name__=="__main__":
    main()
