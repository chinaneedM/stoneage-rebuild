#!/usr/bin/env python3
"""Replay dated Wayback captures of the source page attributed behind the sa25up link.

Only a hash/metadata/token-context report is emitted. The archived page body is fetched
transiently and is not committed. No StoneAge payload URL is downloaded.
"""
from __future__ import annotations

import hashlib
import html
import re
import urllib.error
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
TARGETS=(
    ("2003-06-05","20030605104851","http://pcpc.idv.tw:80/soft/soft.htm"),
    ("2003-12-03","20031203042412","http://pcpc.idv.tw:80/soft/soft.htm"),
    ("2005-01-01","20050101012107","http://pcpc.idv.tw:80/soft/soft.htm"),
)
TOKENS=(
    "sa25up.zip",
    "202.104.32.168",
    "石器時代2.5",
    "石器时代2.5",
    "精靈王傳說",
    "精灵王传说",
)
HREF_RE=re.compile(r"""(?is)href\s*=\s*["']?([^"'\s>]+)""")


def replay_url(timestamp,original,modifier="id_"):
    return f"https://web.archive.org/web/{timestamp}{modifier}/{original}"


def clean(v,limit=900):
    return " ".join(str(v or "").split()).replace("|","%7C")[:limit]


def fetch(url,timeout=35):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"text/html,*/*"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        body=r.read(8_000_001)
        if len(body)>8_000_000:
            raise ValueError("source-page-too-large")
        return (
            int(getattr(r,"status",r.getcode())),
            r.geturl(),
            dict(r.headers.items()),
            body,
        )


RAW_TEXT_TOKENS=(
    "下載",
    "石器時代2.5",
    "精靈王傳說",
)


def decode_body(body):
    # Replacement-count alone is unsafe: GB18030 can decode Big5 bytes into
    # mojibake without errors. Prefer encodings reproducing known neighboring
    # labels at the raw-byte level, then minimize replacement characters.
    candidates=[]
    order=("big5","cp950","utf-8","gb18030","latin1")
    for enc in order:
        try:
            byte_hits=sum(1 for token in RAW_TEXT_TOKENS if token.encode(enc) in body)
        except Exception:
            byte_hits=0
        text=body.decode(enc,errors="replace")
        candidates.append((-byte_hits,text.count("\ufffd"),order.index(enc),enc,text))
    _,_,_,enc,text=min(candidates)
    return enc,text


def normalized_visible(text):
    # Preserve href/text tokens but collapse markup for concise context.
    text=re.sub(r"(?is)<script\b.*?</script>"," ",text)
    text=re.sub(r"(?is)<style\b.*?</style>"," ",text)
    text=re.sub(r"(?is)<[^>]+>"," ",text)
    return " ".join(html.unescape(text).split())


def token_context(text,token,radius=260):
    low=text.lower()
    needle=token.lower()
    i=low.find(needle)
    if i<0:
        return ""
    return text[max(0,i-radius):min(len(text),i+len(token)+radius)]


def interesting_hrefs(text):
    out=[]
    seen=set()
    for raw in HREF_RE.findall(text):
        href=html.unescape(raw.strip())
        low=href.lower()
        if (
            "sa25" in low
            or "stoneage" in low
            or "202.104.32.168" in low
            or "/file/game/maoxian/" in low
        ):
            if href not in seen:
                seen.add(href)
                out.append(href)
    return tuple(out)


def main():
    print("StoneAge 2.5 pcpc.idv.tw source-page replay probe — R1")
    print("SCOPE|dated-wayback-page-body|derived-token-context-only|no-historical-game-payload")
    errors=[]
    positive=0

    for label,timestamp,original in TARGETS:
        url=replay_url(timestamp,original)
        try:
            st,final,headers,body=fetch(url)
            enc,text=decode_body(body)
            visible=normalized_visible(text)
            ascii_body=body.decode("latin1","ignore")
            hrefs=interesting_hrefs(text)
            token_hits=[]
            for token in TOKENS:
                hit=(token.lower() in text.lower()) or (token.lower() in ascii_body.lower())
                if hit:
                    token_hits.append(token)
            exact="sa25up.zip" in ascii_body.lower() or "sa25up.zip" in text.lower()
            if exact:
                positive+=1
            print(
                f"CAPTURE|label={label}|timestamp={timestamp}|status={st}|bytes={len(body)}|"
                f"sha256={hashlib.sha256(body).hexdigest()}|encoding={clean(enc)}|"
                f"content_type={clean(headers.get('Content-Type'))}|final={clean(final)}|"
                f"sa25up={1 if exact else 0}|interesting_hrefs={len(hrefs)}"
            )
            print(f"TOKENS|label={label}|values={clean(','.join(token_hits))}")
            for probe_enc in ("big5","cp950","utf-8","gb18030"):
                raw_hits=[]
                for raw_token in RAW_TEXT_TOKENS:
                    try:
                        if raw_token.encode(probe_enc) in body:
                            raw_hits.append(raw_token)
                    except Exception:
                        pass
                print(f"BYTE_TEXT|label={label}|encoding={probe_enc}|hits={clean(','.join(raw_hits))}")
            for n,href in enumerate(hrefs[:50],1):
                print(f"HREF|label={label}|order={n}|value={clean(href,1800)}")
            for token in ("sa25up.zip","202.104.32.168"):
                context=token_context(visible,token)
                if not context:
                    context=token_context(text,token)
                if context:
                    print(f"CONTEXT|label={label}|token={clean(token)}|value={clean(context,1600)}")
        except Exception as exc:
            errors.append((label,type(exc).__name__,str(exc)))

    for label,kind,msg in errors:
        print(f"ERROR|label={clean(label)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|captures|{len(TARGETS)}")
    print(f"COUNT|positive_sa25up_captures|{positive}")
    print(f"COUNT|errors|{len(errors)}")
    if positive:
        print("RESOLUTION|DATED_SOURCE_PAGE_CONTAINS_SA25UP|use earliest positive capture as a terminus-ante-quem for link-list presence only")
    elif errors:
        print("RESOLUTION|PARTIAL_SOURCE_REPLAY_FAILURE|retry only failed dated captures")
    else:
        print("RESOLUTION|DATED_SOURCE_PAGES_NO_SA25UP|surviving attributed source captures do not contain the token")
    print(
        "EVIDENCE_BOUNDARY|a dated archived source page can prove the link text/url existed on that page by that capture date; "
        "it cannot prove the linked payload was live, official, clean, or byte-identical to any known StoneAge client."
    )


if __name__=="__main__":
    main()
