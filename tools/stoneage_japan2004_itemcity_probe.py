#!/usr/bin/env python3
"""Probe the period Item City retail listing linked by StoneAge package.html.

The exact retailer URL was recovered from the archived first-party StoneAge
package page. Only Wayback metadata and bounded HTML are read. Output is
derived identifiers/hashes/link targets; archived retailer prose is not stored.
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
TARGET=(
    "http://www.item-city.com/shopping/SO_shopping.cgi?"
    "ten_id=itemcity&product_id=423"
)
KEY_DATES=("20040520","20040604","20040615","20040701","20040901","20041201")
MAX_BODY=256*1024

URL_REF=re.compile(r"""(?ix)(?:href|src)\s*=\s*["']?([^"'\s>]+)""")
JAN=re.compile(r"(?<!\d)(\d{13})(?!\d)")
PRICE=re.compile(r"(?<!\d)(\d{1,3}(?:,\d{3})*)\s*円")
MODEL_CODE=re.compile(
    r"(?<![A-Za-z0-9])([A-Z]{2,8}[-_][A-Z0-9_-]{2,20})(?![A-Za-z0-9])"
)


def clean(value,limit=1000):
    text=" ".join(str(value if value is not None else "").split())
    return "".join(ch for ch in text if ch >= " " and ch!="\x7f").replace("|","%7C")[:limit]


def get_json(url,timeout=8):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json"})
    with urllib.request.urlopen(req,timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8","replace"))


def availability(date):
    q=urllib.parse.urlencode({"url":TARGET,"timestamp":date})
    data=get_json(AVAIL+"?"+q)
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


def derived_facts(body):
    decoded=decode_html(body)
    visible=html.unescape(re.sub(r"(?is)<[^>]+>"," ",decoded))
    visible=" ".join(visible.split())
    refs={
        urllib.parse.urljoin(TARGET,html.unescape(m.group(1)).strip())
        for m in URL_REF.finditer(decoded)
        if m.group(1).strip()
    }
    lower=visible.lower()
    return {
        "jan":tuple(sorted(set(JAN.findall(visible)))),
        "prices":tuple(sorted(set(PRICE.findall(visible)))),
        "model_codes":tuple(sorted(set(MODEL_CODE.findall(visible)))),
        "stoneage_occurrences":lower.count("stoneage")+visible.count("ストーンエイジ"),
        "wr04156_occurrences":visible.count("WR-04156"),
        "refs":tuple(sorted(refs)),
        "visible_text_chars":len(visible),
        "visible_text_sha256":hashlib.sha256(visible.encode("utf-8")).hexdigest(),
    }


def relevant_ref(ref):
    lower=ref.lower()
    return any(
        token in lower
        for token in (
            "product","item","stone","423","image","img",
            ".jpg",".jpeg",".gif",".png","shopping",
        )
    )


def main():
    print("StoneAge Japan 2004 Item City product probe — R1")
    print("SCOPE|package-page-linked-retailer|availability+bounded-html|derived-only")
    print("PROVENANCE|official-stoneage-package-page-retailer-link")
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

    refs=set()
    for timestamp in sorted(captures):
        try:
            result=bounded_replay(timestamp)
        except Exception as exc:
            print(
                f"FETCH_ERROR|timestamp={timestamp}|kind={type(exc).__name__}|"
                f"message={clean(exc)}"
            )
            continue
        facts=derived_facts(result["body"])
        print(
            f"FETCH|timestamp={timestamp}|status={result['status']}|"
            f"bytes={len(result['body'])}|truncated={int(result['truncated'])}|"
            f"sha256={hashlib.sha256(result['body']).hexdigest()}|"
            f"content_type={clean(result['content_type'])}|final={clean(result['final'])}"
        )
        print(
            f"PRODUCT_FACT|timestamp={timestamp}|jan={','.join(facts['jan'])}|"
            f"prices={','.join(facts['prices'])}|"
            f"model_codes={','.join(facts['model_codes'])}|"
            f"stoneage_occurrences={facts['stoneage_occurrences']}|"
            f"wr04156_occurrences={facts['wr04156_occurrences']}|"
            f"visible_text_chars={facts['visible_text_chars']}|"
            f"visible_text_sha256={facts['visible_text_sha256']}"
        )
        refs.update(
            (timestamp,ref)
            for ref in facts["refs"]
            if relevant_ref(ref)
        )

    for date,kind,message in errors:
        print(f"ERROR|requested={date}|kind={clean(kind)}|message={clean(message)}")
    print(f"COUNT|availability_errors|{len(errors)}")
    print(f"COUNT|unique_200_captures|{len(captures)}")
    print(f"COUNT|relevant_refs|{len(refs)}")
    for timestamp,ref in sorted(refs):
        print(f"REF|timestamp={timestamp}|value={clean(ref)}")


if __name__=="__main__":
    main()
