#!/usr/bin/env python3
"""Identify the historical download host serving the sa25up path from archived HTML.

Only small archived HTML pages are replayed. The report stores titles, branding snippets,
hostnames and hashes; no game/download payloads are fetched or committed.
"""
from __future__ import annotations

import hashlib
import html
import re
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
PAGES=(
    ("root-2001-12-27","20011227124446","http://202.104.32.168:80/"),
    ("list-113-2002-02-01","20020201180327","http://202.104.32.168:80/list.php?id=113"),
    ("list-1137-2002-02-01","20020201190512","http://202.104.32.168:80/list.php?id=1137"),
)
TITLE_RE=re.compile(r"(?is)<title[^>]*>(.*?)</title>")
META_RE=re.compile(r"""(?is)<meta\b[^>]*(?:name|http-equiv)\s*=\s*["']?([^"'\s>]+)["']?[^>]*content\s*=\s*["']([^"']*)["'][^>]*>""")
URL_RE=re.compile(r"""(?i)(?:https?|ftp)://[a-z0-9._:-]+(?:/[^s"'<>]*)?""")
CHARSET_RE=re.compile(br"(?i)charset\s*=\s*['\"]?([a-z0-9._-]+)")


def clean(v,limit=1400):
    return " ".join(str(v or "").split()).replace("|","%7C")[:limit]


def replay_url(ts,original):
    return f"https://web.archive.org/web/{ts}id_/{original}"


def fetch(url,timeout=35):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"text/html,*/*"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        body=r.read(2_000_001)
        if len(body)>2_000_000:
            raise ValueError("html-too-large")
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),body


def declared_charset(body):
    m=CHARSET_RE.search(body[:100_000])
    return m.group(1).decode("ascii","ignore").lower() if m else ""


def decode(body,declared=""):
    order=[]
    for enc in (declared,"gb18030","gbk","big5","cp950","utf-8","latin1"):
        if enc and enc not in order:
            order.append(enc)
    best=None
    for enc in order:
        try:
            text=body.decode(enc,errors="replace")
        except LookupError:
            continue
        # Prefer fewer replacements, then more CJK characters.
        repl=text.count("\ufffd")
        cjk=sum(1 for ch in text if "\u4e00"<=ch<="\u9fff")
        score=(repl,-cjk,order.index(enc))
        if best is None or score<best[0]:
            best=(score,enc,text)
    return ("binary","") if best is None else (best[1],best[2])


def visible(text):
    t=re.sub(r"(?is)<script\b.*?</script>"," ",text)
    t=re.sub(r"(?is)<style\b.*?</style>"," ",t)
    t=re.sub(r"(?is)<[^>]+>"," ",t)
    return " ".join(html.unescape(t).split())


def title(text):
    m=TITLE_RE.search(text)
    return visible(m.group(1)) if m else ""


def hostnames(text):
    out=[]
    seen=set()
    for url in URL_RE.findall(html.unescape(text)):
        try:
            h=urllib.parse.urlsplit(url).hostname or ""
        except Exception:
            h=""
        h=h.lower()
        if h and h not in seen:
            seen.add(h); out.append(h)
    return tuple(out)


def context(text,needles=("版权所有","下载","软件","网站","主页","首页","联系","copyright"),radius=220):
    v=visible(text)
    low=v.lower()
    for needle in needles:
        i=low.find(needle.lower())
        if i>=0:
            return v[max(0,i-radius):min(len(v),i+len(needle)+radius)]
    return v[:700]


def main():
    print("StoneAge 2.5 sa25up historical host identity probe — R1")
    print("SCOPE|small-archived-html-only|no-download-payload")
    errors=[]
    for label,ts,original in PAGES:
        try:
            st,final,headers,body=fetch(replay_url(ts,original))
            declared=declared_charset(body)
            enc,text=decode(body,declared)
            hosts=hostnames(text)
            print(
                f"PAGE|label={label}|timestamp={ts}|status={st}|bytes={len(body)}|"
                f"sha256={hashlib.sha256(body).hexdigest()}|declared_charset={clean(declared)}|"
                f"encoding={clean(enc)}|title={clean(title(text),700)}|hosts={len(hosts)}|final={clean(final)}"
            )
            print(f"CONTEXT|label={label}|value={clean(context(text),1800)}")
            for h in hosts[:100]:
                if h not in ("202.104.32.168","web.archive.org"):
                    print(f"HOSTNAME|label={label}|value={clean(h)}")
            for name,content in META_RE.findall(text):
                if name.lower() in ("description","keywords","author","generator"):
                    print(f"META|label={label}|name={clean(name)}|content={clean(content,1200)}")
        except Exception as e:
            errors.append((label,type(e).__name__,str(e)))
    for label,kind,msg in errors:
        print(f"ERROR|label={clean(label)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|pages|{len(PAGES)}")
    print(f"COUNT|errors|{len(errors)}")
    print("EVIDENCE_BOUNDARY|archived host branding can identify the historical download site, but does not prove StoneAge payload provenance or cleanliness.")


if __name__=="__main__":
    main()
