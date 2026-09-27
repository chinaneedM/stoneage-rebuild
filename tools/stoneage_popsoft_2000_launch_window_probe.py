#!/usr/bin/env python3
"""Probe Popsoft magazine OCR around the Dec-2000 Mainland StoneAge launch window.

This is a candidate-elimination probe, not a carrier-authentication probe.

Why Popsoft is tested:
- China.com's surviving Dec-2000 activity page sent Beijing users to Jinghe stores
  for the official StoneAge test CD.
- surviving Jinghe corporate material documents its institutional relationship
  with Popsoft / 大众软件.
- a later physical-media collector separately recalls a Mainland 1.0 test
  manual+disc distributed with a magazine.

Those facts make Popsoft a rational candidate surface, but DO NOT establish that
Popsoft was the collector's magazine or the China.com/Jinghe test-CD carrier.

Scope:
- Internet Archive item metadata for the preserved Popsoft magazine scan family;
- transient reads of DjVu OCR text derivatives for 2000-11, 2000-12, 2001-01;
- token counts and co-occurrence offsets only;
- no PDF/image body and no optical/game payload.
"""
from __future__ import annotations

import hashlib
import json
import re
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
IDENTIFIER="popsoft-magazine_202403"
IA_META="https://archive.org/metadata/"
IA_DOWNLOAD="https://archive.org/download/"
MAX_OCR_BYTES=2_000_000

WINDOW_MARKERS=(
    "2000年11月",
    "2000年12月",
    "2001年01月",
    "2001年1月",
)

TOKENS=(
    "石器时代",
    "石器時代",
    "StoneAge",
    "Stone Age",
    "测试光盘",
    "測試光碟",
    "测试版",
    "測試版",
    "试玩版",
    "試玩版",
    "测试",
    "測試",
    "试玩",
    "試玩",
    "光盘",
    "光碟",
    "晶合",
    "华义",
    "華義",
    "北京华义",
    "北京華義",
    "赠送",
    "贈送",
    "JSS",
    "Japan System Supply",
)

CARRIER_CONTEXT=(
    "测试",
    "測試",
    "试玩",
    "試玩",
    "光盘",
    "光碟",
    "晶合",
    "华义",
    "華義",
    "赠送",
    "贈送",
    "免费",
    "免費",
    "领取",
    "領取",
    "安装",
    "安裝",
    "客户端",
    "客戶端",
    "12月15",
    "12月31",
    "1月10",
    "1月12",
)

STONEAGE_ANCHORS=("石器时代","石器時代","StoneAge","Stone Age")


def clean(value,limit=2500):
    text=" ".join(str(value if value is not None else "").split())
    return "".join(ch for ch in text if ch >= " " and ch != "\x7f").replace("|","%7C")[:limit]


def fetch_bytes(url,timeout=60,max_bytes=MAX_OCR_BYTES):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as response:
        body=response.read(max_bytes+1)
        if len(body)>max_bytes:
            raise ValueError(f"body exceeds limit: {len(body)}")
        return int(getattr(response,"status",response.getcode())),response.geturl(),body


def fetch_json(url,timeout=60):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as response:
        body=response.read()
        return int(getattr(response,"status",response.getcode())),response.geturl(),body,json.loads(body.decode("utf-8"))


def metadata_url(identifier=IDENTIFIER):
    return IA_META+urllib.parse.quote(identifier,safe="")


def download_url(identifier,name):
    return IA_DOWNLOAD+urllib.parse.quote(identifier,safe="")+"/"+urllib.parse.quote(name,safe="/")


def file_name(row):
    return str(row.get("name") or "")


def launch_window_ocr_file(row):
    name=file_name(row)
    low=name.lower()
    if not low.endswith("_djvu.txt"):
        return False
    if not (low.startswith("2000/") or low.startswith("2001/")):
        return False
    return any(marker in name for marker in WINDOW_MARKERS)


def month_key(name):
    for marker in WINDOW_MARKERS:
        if marker in name:
            return marker
    return ""


def token_offsets(text,token,limit=16):
    out=[]
    start=0
    while len(out)<limit:
        pos=text.find(token,start)
        if pos<0:
            break
        out.append(pos)
        start=pos+max(1,len(token))
    return out


def stoneage_context_hits(text,limit=80,radius=700):
    hits=[]
    seen=set()
    for anchor in STONEAGE_ANCHORS:
        start=0
        while len(hits)<limit:
            pos=text.find(anchor,start)
            if pos<0:
                break
            lo=max(0,pos-radius)
            hi=min(len(text),pos+radius)
            window=text[lo:hi]
            flags=tuple(token for token in CARRIER_CONTEXT if token in window)
            key=(pos,flags)
            if key not in seen:
                seen.add(key)
                hits.append((pos,anchor,flags))
            start=pos+max(1,len(anchor))
    return sorted(hits,key=lambda x:x[0])[:limit]


def strong_hits(context_hits):
    return [row for row in context_hits if row[2]]


def main():
    print("StoneAge Popsoft 2000/2001 launch-window candidate probe — R1")
    print("SCOPE|Popsoft preserved scans|IA metadata + transient OCR only|2000-11,2000-12,2001-01|no PDF|no optical payload")
    print("HYPOTHESIS_BOUNDARY|Jinghe-Popsoft relationship makes this a candidate surface only; no source currently proves Popsoft carried the official Dec-2000 test CD.")

    errors=[]
    status,final,body,data=fetch_json(metadata_url())
    files=[row for row in data.get("files",[]) if isinstance(row,dict)]
    selected=[row for row in files if launch_window_ocr_file(row)]
    selected.sort(key=lambda r:file_name(r))
    optical=[row for row in files if file_name(row).lower().endswith((".iso",".bin",".cue",".img",".mdf",".mds",".nrg"))]
    print(f"IA_META|identifier={IDENTIFIER}|status={status}|bytes={len(body)}|sha256={hashlib.sha256(body).hexdigest()}|files={len(files)}|launch_window_ocr={len(selected)}|optical_files={len(optical)}|final={clean(final)}")

    total_anchor_mentions=0
    total_strong=0
    issues_with_anchor=0
    issues_with_strong=0

    for row in selected:
        name=file_name(row)
        try:
            st,fin,ocr=fetch_bytes(download_url(IDENTIFIER,name))
            text=ocr.decode("utf-8","replace")
            print(f"OCR_FETCH|month={clean(month_key(name))}|name={clean(name)}|status={st}|bytes={len(ocr)}|sha256={hashlib.sha256(ocr).hexdigest()}|final={clean(fin)}")
            any_token=False
            for token in TOKENS:
                count=text.count(token)
                if count:
                    any_token=True
                    print(f"TOKEN|name={clean(name)}|token={clean(token)}|count={count}|first_offsets={','.join(str(x) for x in token_offsets(text,token))}")
            contexts=stoneage_context_hits(text)
            strong=strong_hits(contexts)
            if contexts:
                issues_with_anchor+=1
            if strong:
                issues_with_strong+=1
            total_anchor_mentions+=len(contexts)
            total_strong+=len(strong)
            for pos,anchor,flags in contexts[:40]:
                print(f"CONTEXT|name={clean(name)}|offset={pos}|anchor={clean(anchor)}|carrier_flags={clean(','.join(flags))}|strong={int(bool(flags))}")
            if not any_token:
                print(f"NO_TARGET_TOKEN|name={clean(name)}")
        except Exception as exc:
            errors.append((name,type(exc).__name__,str(exc)))

    for name,kind,message in errors:
        print(f"ERROR|name={clean(name)}|kind={clean(kind)}|message={clean(message)}")

    print(f"COUNT|ocr_files_selected|{len(selected)}")
    print(f"COUNT|issues_with_stoneage_anchor|{issues_with_anchor}")
    print(f"COUNT|stoneage_context_mentions|{total_anchor_mentions}")
    print(f"COUNT|issues_with_carrier_context|{issues_with_strong}")
    print(f"COUNT|strong_carrier_context_hits|{total_strong}")
    print(f"COUNT|errors|{len(errors)}")

    if errors:
        print("RESOLUTION|PARTIAL_POPSOFT_LAUNCH_WINDOW_PROBE|retry failed OCR derivatives only")
    elif total_strong:
        print("RESOLUTION|POPSOFT_LAUNCH_WINDOW_CARRIER_CONTEXT_SIGNAL|inspect exact issue/page provenance; still not proof of test-CD inclusion")
    elif total_anchor_mentions:
        print("RESOLUTION|POPSOFT_LAUNCH_WINDOW_EDITORIAL_ONLY|StoneAge appears but tested OCR exposes no nearby carrier/test context")
    else:
        print("RESOLUTION|POPSOFT_LAUNCH_WINDOW_NO_STONEAGE_SIGNAL|tested Nov-2000 through Jan-2001 OCR does not support this candidate route")

    print("EVIDENCE_BOUNDARY|OCR token proximity is discovery evidence only. It cannot authenticate a magazine-insert disc, official pressing, or byte identity.")


if __name__=="__main__":
    main()
