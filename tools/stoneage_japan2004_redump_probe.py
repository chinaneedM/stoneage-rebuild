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
LEGACY_BASE="https://redump.org"
MODERN_BASE="https://redump.info/discs"
MODERN_DISC_URL=MODERN_BASE+"?region=jp"
LEGACY_TARGETS=(
    ("title-latin","/discs/quicksearch/StoneAge/"),
    ("model","/discs/quicksearch/WR-04156/"),
    ("barcode","/discs/barcode/4988609011565/"),
)
MODERN_TARGETS=(
    ("q-latin", {"region":"jp","system":"PC","q":"StoneAge"}),
    ("q-japanese", {"region":"jp","system":"PC","q":"ストーンエイジ"}),
    ("title-latin", {"region":"jp","system":"PC","title":"StoneAge"}),
    ("title-space", {"region":"jp","system":"PC","title":"Stone Age"}),
    ("title-japanese", {"region":"jp","system":"PC","title":"ストーンエイジ"}),
    ("serial-model", {"region":"jp","system":"PC","serial":"WR-04156","serial_exact":"1"}),
    ("barcode-jan", {"region":"jp","system":"PC","barcode":"4988609011565","barcode_exact":"1"}),
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
    m=re.search(r"([0-9][0-9,]*)\s+discs?\s+found",vis,re.I)
    if m:return int(m.group(1).replace(",",""))
    if re.search(r"No\s+(?:results|discs)",vis,re.I):return 0
    return None


def form_fields(body):
    text=body.decode("utf-8","replace")
    names=set()
    for tag in re.findall(r"(?is)<(?:input|select|textarea)\b[^>]*>",text):
        m=re.search(r"""(?is)\bname\s*=\s*["']?([^"'\s>]+)""",tag)
        if m:names.add(html.unescape(m.group(1)))
    forms=[]
    for tag in re.findall(r"(?is)<form\b[^>]*>",text):
        action=re.search(r"""(?is)\baction\s*=\s*["']?([^"'\s>]+)""",tag)
        method=re.search(r"""(?is)\bmethod\s*=\s*["']?([^"'\s>]+)""",tag)
        forms.append((html.unescape(action.group(1)) if action else "", (method.group(1) if method else "").upper()))
    return tuple(sorted(names)),tuple(forms)


def modern_url(params):
    return MODERN_BASE+"?"+urllib.parse.urlencode(params)


def main():
    print("StoneAge Japan 2004 Redump index probe — R3")
    print("SCOPE|public-disc-index-html-only|modern-title+serial+barcode|no-disc-download")
    print("ANCHOR|model=WR-04156|jan=4988609011565|package=two-game-CD-ROMs")
    print("QUERY_SCHEMA|source=superg/vgindex@main|fields=q,title,title_foreign,serial,barcode|exact=*_exact")

    discovery_error=0
    try:
        modern=fetch(MODERN_DISC_URL)
        fields,forms=form_fields(modern["body"])
        vis=visible_text(modern["body"])
        print(
            f"MODERN_DISCOVERY|status={modern['status']}|bytes={len(modern['body'])}|"
            f"sha256={hashlib.sha256(modern['body']).hexdigest()}|"
            f"fields={','.join(clean(x,100) for x in fields)}|forms={len(forms)}|"
            f"disc_database_marker={int('Disc Database' in vis)}|"
            f"final={clean(modern['final'])}"
        )
    except Exception as exc:
        discovery_error=1
        print(f"ERROR|surface=modern-discovery|kind={type(exc).__name__}|message={clean(exc)}")

    legacy_errors=0
    for label,path in LEGACY_TARGETS:
        try:
            result=fetch(LEGACY_BASE+path)
            print(
                f"LEGACY_QUERY|label={label}|status={result['status']}|"
                f"bytes={len(result['body'])}|final={clean(result['final'])}"
            )
        except Exception as exc:
            legacy_errors+=1
            print(f"LEGACY_ERROR|label={label}|kind={type(exc).__name__}|message={clean(exc)}")

    modern_errors=0
    modern_completed=0
    hits=0
    conclusive=0
    for label,params in MODERN_TARGETS:
        url=modern_url(params)
        try:
            result=fetch(url)
        except Exception as exc:
            modern_errors+=1
            print(f"ERROR|surface=modern|query={label}|kind={type(exc).__name__}|message={clean(exc)}")
            continue
        modern_completed+=1
        body=result["body"]
        vis=visible_text(body)
        rows=matching_rows(body)
        count=result_count(vis)
        database_marker="Disc Database" in vis
        if count is not None and database_marker:
            conclusive+=1
        hits+=len(rows)
        print(
            f"MODERN_QUERY|label={label}|status={result['status']}|bytes={len(body)}|"
            f"truncated={int(result['truncated'])}|sha256={hashlib.sha256(body).hexdigest()}|"
            f"disc_database_marker={int(database_marker)}|"
            f"result_count={'' if count is None else count}|matching_rows={len(rows)}|"
            f"final={clean(result['final'])}"
        )
        for row in rows:
            print(f"MATCH|query={label}|row={clean(row,1800)}")

    print(f"COUNT|modern_completed|{modern_completed}")
    print(f"COUNT|modern_errors|{modern_errors}")
    print(f"COUNT|modern_conclusive_queries|{conclusive}")
    print(f"COUNT|matching_rows|{hits}")
    print(f"COUNT|legacy_errors|{legacy_errors}")
    if hits:
        print("RESOLUTION|REDUMP_CANDIDATE_ROWS_FOUND|inspect disc records before any identity claim")
    elif conclusive==len(MODERN_TARGETS) and modern_errors==0 and discovery_error==0:
        print("RESOLUTION|REDUMP_NO_IDENTIFIER_HIT|modern Redump returned no StoneAge row for pinned Japan-PC title/model/barcode searches")
    else:
        print("RESOLUTION|INCONCLUSIVE|modern Redump query surface incomplete")



if __name__=="__main__":
    main()
