#!/usr/bin/env python3
"""Replay a small set of high-value Beijing Waei StoneAge2 pages from Feb 2002.

The official StoneAge2 CDX index exposed a handful of top-level news/bulletin
pages captured exactly during the 2.5 rollout window. This probe retries those
specific captures through multiple Wayback replay modifiers, extracts 2.5
text evidence and download-like hrefs, and records hashes only. No binary
payload is fetched.
"""

from __future__ import annotations

import hashlib
import html
import re
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"

SEEDS=(
    ("root","20020201205818","http://www.waei.com.cn:80/ZHUANQU/stoneage2/"),
    ("index","20020201194955","http://www.waei.com.cn:80/ZHUANQU/stoneage2/index.asp"),
    ("bulletin-311","20020203155130","http://www.waei.com.cn:80/zhuanqu/stoneage2/stbulletin/st_bulletin_nr.asp?id=311"),
    ("bulletin-315","20020203155513","http://www.waei.com.cn:80/zhuanqu/stoneage2/stbulletin/st_bulletin_nr.asp?id=315"),
    ("news-31","20020201173036","http://www.waei.com.cn:80/ZHUANQU/stoneage2/stnews/st_news_nr.asp?id=31"),
)

TERMS=(
    "石器时代2.5","石器2.5","精灵王传说","完整升级版","升级程序",
    "575兆","580兆","8.25兆","575mb","580mb","8.25mb",
    "下载","客户端",
)
PAYLOAD_EXTS=(".exe",".zip",".rar",".cab",".001",".002",".vcd",".iso",".msi")

def clean(value,limit=2600):
    text=" ".join(str(value if value is not None else "").split())
    return "".join(ch for ch in text if ch>=" " and ch!="\x7f").replace("|","%7C")[:limit]

def fetch_bytes(url,timeout=30):
    req=urllib.request.Request(
        url,
        headers={"User-Agent":UA,"Accept":"text/html,text/plain;q=0.9,*/*;q=0.8"},
    )
    with urllib.request.urlopen(req,timeout=timeout) as response:
        body=response.read()
        return int(getattr(response,"status",response.getcode())),response.geturl(),body

def replay_urls(timestamp,original):
    quoted=original
    return (
        ("id",f"https://web.archive.org/web/{timestamp}id_/{quoted}"),
        ("if",f"https://web.archive.org/web/{timestamp}if_/{quoted}"),
        ("plain",f"https://web.archive.org/web/{timestamp}/{quoted}"),
    )

def decode(body):
    for enc in ("gb18030","utf-8","big5","latin1"):
        try:
            return body.decode(enc)
        except Exception:
            pass
    return body.decode("utf-8","replace")

def strip_text(text):
    text=re.sub(r"(?is)<script\b.*?</script>"," ",text)
    text=re.sub(r"(?is)<style\b.*?</style>"," ",text)
    text=re.sub(r"(?is)<[^>]+>"," ",text)
    text=html.unescape(text)
    return " ".join(text.split())

def extract(body,base):
    raw=decode(body)
    plain=strip_text(raw)
    low=plain.lower()
    terms=tuple(term for term in TERMS if term.lower() in low)
    hrefs=[]
    for raw_href in re.findall(r'(?is)href\s*=\s*["\']([^"\']+)["\']',raw):
        href=html.unescape(raw_href).strip()
        decoded=urllib.parse.unquote_plus(href).lower()
        if (
            any(ext in decoded for ext in PAYLOAD_EXTS)
            or any(token in decoded for token in ("download","down","update","upgrade","patch","setup","client","2.5","sa25"))
        ):
            hrefs.append((href,urllib.parse.urljoin(base,href)))
    excerpts=[]
    for term in terms:
        idx=low.find(term.lower())
        if idx>=0:
            excerpts.append(plain[max(0,idx-180):idx+420])
    return terms,tuple(dict.fromkeys(hrefs)),tuple(dict.fromkeys(excerpts))

def main():
    print("StoneAge Beijing-Waei 2.5 key-page replay probe — R1")
    print("SCOPE|five-official-Feb-2002-pages|multi-replay-mode|text+href-evidence|no-binary-payload")
    print(f"TARGET|seeds={len(SEEDS)}")

    errors=[]
    successes=[]
    hrefs={}
    for label,ts,original in SEEDS:
        got=None
        for mode,url in replay_urls(ts,original):
            try:
                status,final,body=fetch_bytes(url)
                terms,candidates,excerpts=extract(body,original)
                print(
                    f"REPLAY|label={label}|mode={mode}|timestamp={ts}|status={status}|bytes={len(body)}|"
                    f"sha256={hashlib.sha256(body).hexdigest()}|terms={clean(','.join(terms))}|"
                    f"candidate_hrefs={len(candidates)}|final={clean(final)}"
                )
                for excerpt in excerpts[:12]:
                    print(f"EXCERPT|label={label}|mode={mode}|text={clean(excerpt)}")
                for href,absolute in candidates:
                    hrefs[absolute]=(label,ts,original,href)
                    print(
                        f"HREF|label={label}|mode={mode}|timestamp={ts}|source={clean(original)}|"
                        f"href={clean(href)}|absolute={clean(absolute)}"
                    )
                got=(mode,status,final,body,terms,candidates)
                successes.append((label,got))
                break
            except Exception as exc:
                errors.append((f"{label}:{mode}",type(exc).__name__,str(exc)))

        if got is None:
            print(f"SEED_UNRESOLVED|label={label}|timestamp={ts}|original={clean(original)}")

    for scope,kind,message in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(message)}")

    strong=[]
    for absolute,(label,ts,source,href) in hrefs.items():
        low=urllib.parse.unquote_plus(absolute).lower()
        if any(ext in low for ext in PAYLOAD_EXTS) or any(x in low for x in ("2.5","sa25","setup","update","upgrade","client")):
            strong.append((absolute,label,ts,source,href))
    for absolute,label,ts,source,href in strong:
        print(
            f"STRONG_HREF|label={label}|timestamp={ts}|source={clean(source)}|"
            f"href={clean(href)}|absolute={clean(absolute)}"
        )

    print(f"COUNT|seeds|{len(SEEDS)}")
    print(f"COUNT|successful_seeds|{len(successes)}")
    print(f"COUNT|unique_candidate_hrefs|{len(hrefs)}")
    print(f"COUNT|strong_hrefs|{len(strong)}")
    print(f"COUNT|errors|{len(errors)}")
    if strong:
        print("RESOLUTION|OFFICIAL_25_STRONG_HREFS_FOUND|classify exact target identity and archive availability next")
    elif successes:
        print("RESOLUTION|KEY_PAGES_RECOVERED_NO_STRONG_HREF|official pages replayed but no strong client target extracted")
    else:
        print("RESOLUTION|KEY_PAGES_UNRECOVERED|all replay modes failed for the bounded seed set")

if __name__=="__main__":
    main()
