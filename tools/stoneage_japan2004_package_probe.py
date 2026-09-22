#!/usr/bin/env python3
"""Probe the official Japanese StoneAge 2004 retail-package page.

The page path is contemporaneously linked by 4Gamer's 2004-05-20 release
report as the package/retailer page. Only archive metadata and bounded HTML are
read. The report emits derived identifiers, counts, hashes and relevant link
targets; archived page bodies and game payloads are never committed.
"""

from __future__ import annotations

import hashlib
import html
import json
import re
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0 (+https://github.com/chinaneedM/stoneage-rebuild)"
AVAIL="https://archive.org/wayback/available"
TARGET="http://stoneage.to/package.html"
KEY_DATES=("20040520","20040527","20040603","20040615","20040701")
MAX_BODY=256*1024

URL_REF=re.compile(r"""(?ix)(?:href|src)\s*=\s*["']?([^"'\s>]+)""")
JAN=re.compile(r"(?<!\d)(\d{13})(?!\d)")
PRICE=re.compile(r"(?<!\d)(\d{1,3}(?:,\d{3})*)\s*円")
MODEL_CODE=re.compile(
    r"(?<![A-Za-z0-9])([A-Z]{2,8}[-_][A-Z0-9_-]{2,20})(?![A-Za-z0-9])"
)


def clean(value,limit=1000):
    value=" ".join(str(value if value is not None else "").split())
    return "".join(ch for ch in value if ch >= " " and ch != "\x7f").replace("|","%7C")[:limit]


def get_json(url,timeout=8):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json"})
    with urllib.request.urlopen(req,timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8","replace"))


def availability(date):
    query=urllib.parse.urlencode({"url":TARGET,"timestamp":date})
    data=get_json(AVAIL+"?"+query)
    closest=data.get("archived_snapshots",{}).get("closest")
    if not isinstance(closest,dict) or not closest.get("available"):
        return None
    return {
        "timestamp":str(closest.get("timestamp","")),
        "status":str(closest.get("status","")),
        "url":str(closest.get("url","")),
    }


def bounded_replay(timestamp,timeout=12):
    replay=f"https://web.archive.org/web/{timestamp}id_/{TARGET}"
    req=urllib.request.Request(
        replay,
        headers={
            "User-Agent":UA,
            "Accept":"text/html,*/*",
            "Accept-Encoding":"identity",
            "Range":f"bytes=0-{MAX_BODY-1}",
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


def decode_html(data):
    for encoding in ("utf-8","cp932","shift_jis","euc-jp"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            pass
    return data.decode("latin-1","replace")


def derived_page_facts(body):
    decoded=decode_html(body)
    visible=html.unescape(re.sub(r"(?is)<[^>]+>"," ",decoded))
    visible=" ".join(visible.split())
    refs=[]
    for match in URL_REF.finditer(decoded):
        ref=html.unescape(match.group(1)).strip()
        if ref:
            refs.append(urllib.parse.urljoin(TARGET,ref))
    refs=tuple(sorted(set(refs)))
    jan=tuple(sorted(set(JAN.findall(visible))))
    prices=tuple(sorted(set(PRICE.findall(visible))))
    model_codes=tuple(sorted(set(MODEL_CODE.findall(visible))))
    lowered=visible.lower()
    return {
        "jan":jan,
        "prices":prices,
        "model_codes":model_codes,
        "cdrom_occurrences":lowered.count("cd-rom")+lowered.count("cdrom"),
        "upopo_occurrences":visible.count("ウポポ"),
        "day30_occurrences":visible.count("30日"),
        "refs":refs,
        "visible_text_chars":len(visible),
        "visible_text_sha256":hashlib.sha256(visible.encode("utf-8")).hexdigest(),
    }


def is_relevant_ref(ref):
    lower=ref.lower()
    return (
        any(token in lower for token in (
            "package","shop","store","buy","order","stoneage","image","img",
            ".jpg",".jpeg",".gif",".png",".exe",".zip",".cab",
        ))
        or "amazon" in lower
        or "rakuten" in lower
    )


def main():
    print("StoneAge Japan 2004 official retail-package page probe — R1")
    print("SCOPE|official-package-page|availability+bounded-html|derived-metadata-only")
    print("PROVENANCE|4Gamer-2004-05-20 retailer-link-target")
    print("TARGET|"+TARGET)
    print("KEY_DATES|"+",".join(KEY_DATES))

    captures={}
    errors=[]
    for date in KEY_DATES:
        try:
            cap=availability(date)
        except Exception as exc:
            errors.append((date,type(exc).__name__,str(exc)))
            continue
        if cap is None:
            print(f"AVAIL|requested={date}|available=0")
            continue
        print(
            f"AVAIL|requested={date}|available=1|timestamp={clean(cap['timestamp'])}|"
            f"status={clean(cap['status'])}|url={clean(cap['url'])}"
        )
        if cap["status"]=="200" and cap["timestamp"]:
            captures.setdefault(cap["timestamp"],cap)

    relevant_refs=set()
    for timestamp in sorted(captures):
        try:
            result=bounded_replay(timestamp)
        except Exception as exc:
            print(
                f"FETCH_ERROR|timestamp={timestamp}|kind={type(exc).__name__}|"
                f"message={clean(exc)}"
            )
            continue
        body=result["body"]
        facts=derived_page_facts(body)
        print(
            f"FETCH|timestamp={timestamp}|status={result['status']}|bytes={len(body)}|"
            f"truncated={int(result['truncated'])}|sha256={hashlib.sha256(body).hexdigest()}|"
            f"content_type={clean(result['content_type'])}|final={clean(result['final'])}"
        )
        print(
            f"PAGE_FACT|timestamp={timestamp}|jan={','.join(facts['jan'])}|"
            f"prices={','.join(facts['prices'])}|"
            f"model_codes={','.join(facts['model_codes'])}|"
            f"cdrom_occurrences={facts['cdrom_occurrences']}|"
            f"upopo_occurrences={facts['upopo_occurrences']}|"
            f"day30_occurrences={facts['day30_occurrences']}|"
            f"visible_text_chars={facts['visible_text_chars']}|"
            f"visible_text_sha256={facts['visible_text_sha256']}"
        )
        for ref in facts["refs"]:
            if is_relevant_ref(ref):
                relevant_refs.add((timestamp,ref))

    for date,kind,message in errors:
        print(f"ERROR|requested={date}|kind={clean(kind)}|message={clean(message)}")
    print(f"COUNT|availability_errors|{len(errors)}")
    print(f"COUNT|unique_200_captures|{len(captures)}")
    print(f"COUNT|relevant_refs|{len(relevant_refs)}")
    for timestamp,ref in sorted(relevant_refs):
        print(f"REF|timestamp={timestamp}|value={clean(ref)}")


if __name__=="__main__":
    main()
