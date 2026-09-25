#!/usr/bin/env python3
"""Probe the public landing surface for a StoneAge 2.5 Baidu share.

No extraction code is supplied or guessed. No login/cookies are used. The probe
records only public landing status, safe file metadata explicitly embedded in
the anonymous response, and public archive-index metadata.
"""
from __future__ import annotations

import hashlib
import html
import json
import re
import urllib.error
import urllib.parse
import urllib.request

UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/153 Safari/537.36"
SOURCE="https://www.cangbaowan.vip/thread-9642-1-1.html"
SHARE_ID="1a2cOmPxo5GjFPFfU5Mj2Ug"
SHARE=f"https://pan.baidu.com/s/{SHARE_ID}"
CDX="https://web.archive.org/cdx/search/cdx"
IA="https://archive.org/advancedsearch.php"

TITLE_RE=re.compile(r"(?is)<title[^>]*>(.*?)</title>")
META_RE=re.compile(r"""(?is)<meta[^>]+(?:name|property)=["'](?:description|og:description|og:title)["'][^>]+content=["']([^"']*)""")
TAG_RE=re.compile(r"(?is)<[^>]+>")

SAFE_PATTERNS=(
    ("server_filename", re.compile(r'''["']server_filename["']\s*:\s*["']([^"']{1,500})["']''',re.I)),
    ("filename", re.compile(r'''["'](?:filename|file_name)["']\s*:\s*["']([^"']{1,500})["']''',re.I)),
    ("size", re.compile(r'''["']size["']\s*:\s*([0-9]{1,20})''',re.I)),
    ("ctime", re.compile(r'''["']ctime["']\s*:\s*([0-9]{8,20})''',re.I)),
    ("mtime", re.compile(r'''["']mtime["']\s*:\s*([0-9]{8,20})''',re.I)),
    ("fs_id", re.compile(r'''["']fs_id["']\s*:\s*([0-9]{4,30})''',re.I)),
)
STATE_PHRASES=(
    "请输入提取码","请输入密码","提取码","分享的文件已经被取消","分享的文件已被取消",
    "分享已过期","链接不存在","页面不存在","文件不存在","分享的文件不存在","失效",
)


def clean(v,n=2200):
    return " ".join(html.unescape(str(v if v is not None else "")).split()).replace("|","%7C")[:n]


def fetch(url, *, timeout=30, max_bytes=8_000_000):
    req=urllib.request.Request(url,headers={
        "User-Agent":UA,
        "Accept":"text/html,application/json,text/plain,*/*",
        "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.5",
    })
    try:
        with urllib.request.urlopen(req,timeout=timeout) as r:
            b=r.read(max_bytes+1)
            if len(b)>max_bytes:
                raise ValueError("response-too-large")
            return {
                "ok":True,
                "status":int(getattr(r,"status",r.getcode())),
                "final":r.geturl(),
                "headers":dict(r.headers.items()),
                "body":b,
            }
    except urllib.error.HTTPError as e:
        try:
            b=e.read(min(max_bytes,1_000_000))
        except Exception:
            b=b""
        return {
            "ok":False,"status":e.code,"final":url,
            "headers":dict(e.headers.items()) if e.headers else {},
            "body":b,"error":"HTTPError",
        }
    except Exception as e:
        return {
            "ok":False,"status":"","final":url,"headers":{},"body":b"",
            "error":type(e).__name__+": "+str(e),
        }


def cdx(target,match_type="exact"):
    params=[
        ("url",target),("output","json"),
        ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
        ("from","2025"),("to","2026"),("limit","500"),
    ]
    if match_type!="exact":
        params.append(("matchType",match_type))
    u=CDX+"?"+urllib.parse.urlencode(params)
    r=fetch(u,timeout=35)
    rows=[]
    if r.get("ok"):
        try:
            obj=json.loads(r["body"].decode("utf-8","replace"))
            if isinstance(obj,list) and obj:
                if isinstance(obj[0],list):
                    hdr=obj[0]
                    rows=[dict(zip(hdr,x)) for x in obj[1:] if isinstance(x,list)]
                else:
                    rows=[x for x in obj if isinstance(x,dict)]
        except Exception:
            pass
    return r,rows


def ia_search():
    params=[
        ("q",f'"{SHARE_ID}"'),
        ("fl[]","identifier"),("fl[]","title"),("fl[]","description"),
        ("rows","100"),("output","json"),
    ]
    r=fetch(IA+"?"+urllib.parse.urlencode(params),timeout=30)
    docs=[]
    if r.get("ok"):
        try:
            obj=json.loads(r["body"].decode("utf-8","replace"))
            docs=obj.get("response",{}).get("docs",[])
        except Exception:
            pass
    return r,docs


def main():
    print("StoneAge 2.5 CangBaoWan Baidu public-share probe — R1")
    print("SCOPE|anonymous-public-landing+public-archive-index|no-code-guess|no-login|no-bypass|no-payload")
    print(f"SOURCE|{SOURCE}")
    print(f"SHARE|id={SHARE_ID}|url={SHARE}")

    src=fetch(SOURCE)
    stxt=src.get("body",b"").decode("utf-8","replace")
    print(
        f"SOURCE_PAGE|ok={int(src.get('ok',False))}|status={src.get('status','')}|"
        f"bytes={len(src.get('body',b''))}|sha256={hashlib.sha256(src.get('body',b'')).hexdigest() if src.get('body') else ''}|"
        f"share_id_count={stxt.count(SHARE_ID)}|final={clean(src.get('final',''))}|error={clean(src.get('error',''))}"
    )

    r=fetch(SHARE,timeout=35)
    body=r.get("body",b"")
    text=body.decode("utf-8","replace")
    print(
        f"BAIDU_PAGE|ok={int(r.get('ok',False))}|status={r.get('status','')}|bytes={len(body)}|"
        f"sha256={hashlib.sha256(body).hexdigest() if body else ''}|final={clean(r.get('final',''))}|"
        f"content_type={clean(r.get('headers',{}).get('Content-Type'))}|error={clean(r.get('error',''))}"
    )
    for m in TITLE_RE.finditer(text):
        print(f"BAIDU_TITLE|value={clean(TAG_RE.sub(' ',m.group(1)),1800)}")
    for m in META_RE.finditer(text):
        print(f"BAIDU_META|value={clean(m.group(1),2200)}")
    for phrase in STATE_PHRASES:
        count=text.count(phrase)
        if count:
            print(f"BAIDU_STATE|phrase={clean(phrase)}|count={count}")
    seen=set()
    for label,patt in SAFE_PATTERNS:
        for m in patt.finditer(text):
            value=clean(m.group(1),1200)
            if (label,value) in seen:
                continue
            seen.add((label,value))
            print(f"BAIDU_PUBLIC_FIELD|kind={label}|value={value}")

    for target in (SHARE,SHARE+"/"):
        for mode in ("exact","prefix"):
            rr,rows=cdx(target,mode)
            print(
                f"WAYBACK|target={clean(target)}|mode={mode}|ok={int(rr.get('ok',False))}|"
                f"status={rr.get('status','')}|rows={len(rows)}|error={clean(rr.get('error',''))}"
            )
            for row in rows[:100]:
                print("WAYBACK_ROW|"+"|".join(
                    f"{k}={clean(row.get(k,''))}"
                    for k in ("timestamp","original","statuscode","mimetype","digest","length","redirect")
                ))

    ir,docs=ia_search()
    print(
        f"IA_SEARCH|ok={int(ir.get('ok',False))}|status={ir.get('status','')}|docs={len(docs)}|"
        f"error={clean(ir.get('error',''))}"
    )
    for doc in docs:
        print(f"IA_DOC|value={clean(json.dumps(doc,ensure_ascii=False,sort_keys=True),2200)}")

    if seen:
        print("RESOLUTION|PUBLIC_BAIDU_FILE_METADATA_EXPOSED|metadata requires comparison; no payload access attempted")
    elif any(p in text for p in ("提取码","请输入密码","请输入提取码")):
        print("RESOLUTION|PUBLIC_SHARE_LANDING_REQUIRES_EXTRACTION_CODE|do not guess or bypass")
    elif r.get("ok"):
        print("RESOLUTION|PUBLIC_SHARE_LANDING_REACHED_NO_SAFE_FILE_METADATA|retain exact share ID only")
    else:
        print("RESOLUTION|PUBLIC_SHARE_LANDING_UNREACHABLE_FROM_CI|do not infer share death")
    print("EVIDENCE_BOUNDARY|anonymous landing metadata cannot establish payload cleanliness, historical provenance or byte relationship to known StoneAge clients.")


if __name__=="__main__":
    main()
