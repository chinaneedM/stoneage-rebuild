#!/usr/bin/env python3
"""Probe Redump's public disc index for the Japanese 2004 StoneAge package.

Metadata/index HTML only. No disc image or downloadable payload is requested.
The report retains status, hashes, result counts and rows containing pinned
StoneAge identifiers.
"""

from __future__ import annotations

import hashlib
import html
import re
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0 (+https://github.com/chinaneedM/stoneage-rebuild)"
BASES=("https://redump.org","https://redump.info")
MODERN_DISC_URL="https://redump.info/discs?region=jp"
TARGETS=(
    ("title-latin","/discs/quicksearch/StoneAge/"),
    ("title-space","/discs/quicksearch/Stone%20Age/"),
    ("title-japanese","/discs/quicksearch/%E3%82%B9%E3%83%88%E3%83%BC%E3%83%B3%E3%82%A8%E3%82%A4%E3%82%B8/"),
    ("model","/discs/quicksearch/WR-04156/"),
    ("barcode","/discs/barcode/4988609011565/"),
)
PINNED=("stoneage","stone age","ストーンエイジ","wr-04156","4988609011565")
MAX_BODY=2*1024*1024


def clean(value,limit=1400):
    value=" ".join(str(value if value is not None else "").split())
    return "".join(ch for ch in value if ch>=" " and ch!="\x7f").replace("|","%7C")[:limit]


def fetch(url,timeout=20):
    req=urllib.request.Request(
        url,
        headers={
            "User-Agent":UA,
            "Accept":"text/html,application/xhtml+xml,*/*",
            "Accept-Encoding":"identity",
        },
    )
    with urllib.request.urlopen(req,timeout=timeout) as response:
        body=response.read(MAX_BODY+1)
        return {
            "status":int(getattr(response,"status",200)),
            "final":response.geturl(),
            "content_type":response.headers.get("Content-Type",""),
            "body":body[:MAX_BODY],
            "truncated":len(body)>MAX_BODY,
        }


def visible_text(body):
    text=body.decode("utf-8","replace")
    text=re.sub(r"(?is)<script\b.*?</script>|<style\b.*?</style>"," ",text)
    text=html.unescape(re.sub(r"(?is)<[^>]+>"," ",text))
    return " ".join(text.split())


def matching_rows(body):
    text=body.decode("utf-8","replace")
    rows=[]
    for raw in re.findall(r"(?is)<tr\b[^>]*>(.*?)</tr>",text):
        vis=html.unescape(re.sub(r"(?is)<[^>]+>"," ",raw))
        vis=" ".join(vis.split())
        low=vis.lower()
        if any(token in low for token in ("stoneage","stone age","wr-04156","4988609011565")) or "ストーンエイジ" in vis:
            rows.append(vis)
    return tuple(dict.fromkeys(rows))


def result_count(vis):
    m=re.search(r"Displaying\s+results\s+\d+\s*-\s*\d+\s+of\s+(\d+)",vis,re.I)
    if m:return int(m.group(1))
    if re.search(r"Displaying\s+results\s+0",vis,re.I):return 0
    if re.search(r"No\s+(?:results|discs)",vis,re.I):return 0
    return None


def form_fields(body):
    text=body.decode("utf-8","replace")
    names=set()
    for tag in re.findall(r"(?is)<(?:input|select|textarea)\\b[^>]*>",text):
        m=re.search(r"""(?is)\\bname\\s*=\\s*["']?([^"'\\s>]+)""",tag)
        if m:names.add(html.unescape(m.group(1)))
    forms=[]
    for tag in re.findall(r"(?is)<form\\b[^>]*>",text):
        action=re.search(r"""(?is)\\baction\\s*=\\s*["']?([^"'\\s>]+)""",tag)
        method=re.search(r"""(?is)\\bmethod\\s*=\\s*["']?([^"'\\s>]+)""",tag)
        forms.append((html.unescape(action.group(1)) if action else "", (method.group(1) if method else "").upper()))
    return tuple(sorted(names)),tuple(forms)


def main():
    print("StoneAge Japan 2004 Redump index probe — R2")
    print("SCOPE|public-disc-index-html-only|title+model+barcode|no-disc-download")
    print("ANCHOR|model=WR-04156|jan=4988609011565|package=two-game-CD-ROMs")
    errors=0
    hits=0
    completed=0

    try:
        modern=fetch(MODERN_DISC_URL)
        fields,forms=form_fields(modern["body"])
        print(
            f"MODERN_DISCOVERY|status={modern['status']}|bytes={len(modern['body'])}|"
            f"sha256={hashlib.sha256(modern['body']).hexdigest()}|"
            f"fields={','.join(clean(x,100) for x in fields)}|forms={len(forms)}|"
            f"final={clean(modern['final'])}"
        )
        for action,method in forms:
            print(f"FORM|method={clean(method)}|action={clean(action)}")
    except Exception as exc:
        errors+=1
        print(f"ERROR|base=https://redump.info|query=modern-discovery|kind={type(exc).__name__}|message={clean(exc)}")

    for base in BASES:
        for label,path in TARGETS:
            url=base+path
            try:
                result=fetch(url)
            except Exception as exc:
                errors+=1
                print(f"ERROR|base={clean(base)}|query={label}|kind={type(exc).__name__}|message={clean(exc)}")
                continue
            completed+=1
            body=result["body"]
            vis=visible_text(body)
            rows=matching_rows(body)
            count=result_count(vis)
            hits+=len(rows)
            print(
                f"QUERY|base={clean(base)}|label={label}|status={result['status']}|"
                f"bytes={len(body)}|truncated={int(result['truncated'])}|"
                f"sha256={hashlib.sha256(body).hexdigest()}|"
                f"result_count={'' if count is None else count}|matching_rows={len(rows)}|"
                f"final={clean(result['final'])}"
            )
            for row in rows:
                print(f"MATCH|base={clean(base)}|label={label}|row={clean(row,1800)}")
    print(f"COUNT|completed_queries|{completed}")
    print(f"COUNT|errors|{errors}")
    print(f"COUNT|matching_rows|{hits}")
    if hits:
        print("RESOLUTION|REDUMP_CANDIDATE_ROWS_FOUND|inspect disc records before any identity claim")
    elif completed==len(BASES)*len(TARGETS) and errors==0:
        print("RESOLUTION|REDUMP_NO_IDENTIFIER_HIT|no indexed row matched pinned title/model/barcode searches")
    else:
        print("RESOLUTION|INCONCLUSIVE|Redump query surface incomplete")


if __name__=="__main__":
    main()
