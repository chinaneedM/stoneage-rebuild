#!/usr/bin/env python3
"""Replay the exact archived Sina CGI hit for samap_1220.zip.

Fetches one small Wayback HTML response only. No ZIP or other binary payload is
downloaded. Output is derived routing evidence: headers, hashes, links, forms,
script URLs and lines mentioning the target/download route.
"""
from __future__ import annotations
import hashlib,html,re,urllib.parse,urllib.request

UA="stoneage-rebuild-archaeology/1.0"
TS="20010126074600"
ORIGINAL="http://games.sina.com.cn:80/cgi-bin/games/downgames/download.pl?col=map&aid=23223&title=%CA%AF%C6%F7%CA%B1%B4%FA%A1%AA%C8%AB%B5%D8%CD%BC&author=%D3%CE%C3%F1%B2%BF%C2%E4&filename=samap_1220.zip&size=1410"
TARGET="samap_1220.zip"

def clean(v,n=6000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def replay_url():
    return f"https://web.archive.org/web/{TS}id_/{ORIGINAL}"

def fetch(url,timeout=45,max_bytes=256*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"text/html,text/plain,*/*;q=0.5","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),r.read(max_bytes)

def decode(body):
    for enc in ("gb18030","utf-8","latin1"):
        try:return body.decode(enc)
        except UnicodeDecodeError:pass
    return body.decode("latin1","replace")

def candidates(body):
    text=decode(body)
    vals=[]
    pats=(
      r'(?is)href\s*=\s*["\']([^"\']+)["\']',
      r'(?is)src\s*=\s*["\']([^"\']+)["\']',
      r'(?is)action\s*=\s*["\']([^"\']+)["\']',
      r'(?is)value\s*=\s*["\']([^"\']+)["\']',
      r'(?is)(?:window\.location|location\.href|document\.location)\s*=\s*["\']([^"\']+)["\']',
      r'(?i)(?:https?|ftp)://[^\s"\'<>]+',
    )
    for pat in pats: vals.extend(re.findall(pat,text))
    out=[]
    for raw in vals:
        raw=html.unescape(str(raw)).strip()
        if not raw:continue
        u=urllib.parse.urljoin(ORIGINAL,raw)
        low=urllib.parse.unquote_plus(u).lower()
        if TARGET.lower() in low or any(ext in low for ext in (".zip",".exe",".rar",".cab")) or any(k in low for k in ("download","ftp","down/","map")):
            out.append(u)
    return tuple(dict.fromkeys(out))

def relevant_lines(body):
    text=decode(body)
    out=[]
    for line in re.split(r'[\r\n]+',text):
        s=" ".join(line.split())
        low=urllib.parse.unquote_plus(s).lower()
        if TARGET.lower() in low or any(k in low for k in ("download","ftp","href","action","location","window.","document.","map")):
            out.append(s[:1800])
    return tuple(dict.fromkeys(out))[:80]

def main():
    print("StoneAge 2000 Sina exact CGI replay — R1")
    print("SCOPE|one archived CGI HTML response|small-response-only|no-payload")
    print(f"TARGET|timestamp={TS}|filename={TARGET}|original={clean(ORIGINAL)}")
    errors=[]
    try:
        st,final,h,b=fetch(replay_url())
        print(f"REPLAY|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
        for k,v in sorted(h.items(),key=lambda kv:kv[0].lower()):
            if k.lower() in ("content-type","content-length","location","x-archive-orig-location","x-archive-orig-content-type","x-archive-orig-content-length","x-archive-orig-last-modified"):
                print(f"HEADER|key={clean(k)}|value={clean(v)}")
        cs=candidates(b);ls=relevant_lines(b)
        print(f"COUNT|route_candidates|{len(cs)}")
        for i,u in enumerate(cs,1):print(f"ROUTE|index={i}|url={clean(u)}")
        print(f"COUNT|relevant_lines|{len(ls)}")
        for i,line in enumerate(ls,1):print(f"BODY_LINE|index={i}|text={clean(line,1800)}")
        if cs:
            print("RESOLUTION|CGI_ROUTE_VALUES_RECOVERED|classify each route before any binary request")
        else:
            print("RESOLUTION|CGI_HTML_NO_ROUTE_VALUE|archived response exists but exposes no parseable direct route")
    except Exception as e:
        errors.append((type(e).__name__,str(e)))
        print(f"ERROR|kind={type(e).__name__}|message={clean(e)}")
        print("RESOLUTION|REPLAY_FAILED|retain exact CDX row and retry only through another archive replay surface")
    print(f"COUNT|errors|{len(errors)}")
    print("EVIDENCE_BOUNDARY|this probe recovers routing HTML only; no route is treated as the target ZIP until exact bytes are separately recovered and verified.")

if __name__=="__main__":
    main()
