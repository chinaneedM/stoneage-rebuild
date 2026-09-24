#!/usr/bin/env python3
"""Map the historical host/file neighborhood around StoneAge 2.5 sa25up.zip.

This combines one dated archived source-page body with Wayback CDX host metadata.
It emits only link labels/URLs and archive metadata; no historical game payload is fetched.
"""
from __future__ import annotations

import collections
import hashlib
import html
import json
import re
import urllib.parse
import urllib.request

from tools.stoneage_sa25_pcpc_source_replay_probe import decode_body, replay_url

UA="stoneage-rebuild-archaeology/1.0"
SOURCE_TS="20030605104851"
SOURCE_ORIGINAL="http://pcpc.idv.tw:80/soft/soft.htm"
HOST="202.104.32.168"
CDX="https://web.archive.org/cdx/search/cdx"

ANCHOR_RE=re.compile(
    r"""(?is)<a\b[^>]*?href\s*=\s*["']?([^"'\s>]+)["']?[^>]*>(.*?)</a>"""
)


def clean(v,limit=1600):
    return " ".join(str(v or "").split()).replace("|","%7C")[:limit]


def fetch(url,timeout=40,max_bytes=12_000_000):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/html,*/*"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        body=r.read(max_bytes+1)
        if len(body)>max_bytes:
            raise ValueError("response-too-large")
        return int(getattr(r,"status",r.getcode())),r.geturl(),body


def strip_markup(text):
    return " ".join(html.unescape(re.sub(r"(?is)<[^>]+>"," ",text)).split())


def same_host_anchors(text):
    out=[]
    seen=set()
    for href,label_html in ANCHOR_RE.findall(text):
        href=html.unescape(href.strip())
        parsed=urllib.parse.urlsplit(href)
        if parsed.hostname!=HOST:
            continue
        label=strip_markup(label_html)
        key=(href,label)
        if key in seen:
            continue
        seen.add(key)
        out.append((href,label))
    return tuple(out)


def cdx_url(prefix,status200=False,limit=3000):
    params=[
        ("url",prefix),("matchType","prefix"),("output","json"),
        ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
        ("from","2001"),("to","2004"),("collapse","urlkey"),("limit",str(limit)),
    ]
    if status200:
        params.append(("filter","statuscode:200"))
    return CDX+"?"+urllib.parse.urlencode(params)


def parse_cdx(body):
    data=json.loads(body.decode("utf-8","replace"))
    if not isinstance(data,list) or not data or not isinstance(data[0],list):
        return ()
    header=data[0]
    return tuple(dict(zip(header,row)) for row in data[1:] if isinstance(row,list))


def path_bucket(url):
    try:
        p=urllib.parse.urlsplit(url).path
    except Exception:
        return "?"
    parts=[x for x in p.split("/") if x]
    if not parts:
        return "/"
    if len(parts)==1:
        return "/"+parts[0]
    return "/"+"/".join(parts[:2])+"/"


def html_identity_candidate(row):
    original=str(row.get("original") or "")
    mime=str(row.get("mimetype") or "").lower()
    if "html" not in mime:
        return False
    path=urllib.parse.urlsplit(original).path.lower()
    leaf=path.rstrip("/").rsplit("/",1)[-1]
    return (
        path in ("","/")
        or leaf in ("","index.htm","index.html","index.asp","default.htm","default.html","default.asp")
        or path.count("/")<=2
    )


def main():
    print("StoneAge 2.5 sa25up historical host-neighborhood probe — R1")
    print("SCOPE|dated-source-links+wayback-cdx-host-metadata|no-game-payload-download")
    print(f"HOST|{HOST}")

    errors=[]
    anchors=()
    try:
        url=replay_url(SOURCE_TS,SOURCE_ORIGINAL)
        st,final,body=fetch(url)
        enc,text=decode_body(body)
        anchors=same_host_anchors(text)
        print(
            f"SOURCE|timestamp={SOURCE_TS}|status={st}|bytes={len(body)}|"
            f"sha256={hashlib.sha256(body).hexdigest()}|encoding={clean(enc)}|"
            f"same_host_anchors={len(anchors)}|final={clean(final)}"
        )
        for n,(href,label) in enumerate(anchors,1):
            print(f"SOURCE_LINK|order={n}|label={clean(label,700)}|href={clean(href,1800)}")
    except Exception as e:
        errors.append(("source-page",type(e).__name__,str(e)))

    all_rows={}
    for label,prefix,status200,limit in (
        ("host-all",f"http://{HOST}/",False,3000),
        ("host-200",f"http://{HOST}/",True,3000),
        ("file-200",f"http://{HOST}/file/",True,3000),
        ("game-200",f"http://{HOST}/file/game/",True,3000),
    ):
        try:
            u=cdx_url(prefix,status200,limit)
            st,final,body=fetch(u,max_bytes=10_000_000)
            rows=parse_cdx(body)
            print(
                f"CDX|label={label}|prefix={clean(prefix)}|status={st}|bytes={len(body)}|"
                f"sha256={hashlib.sha256(body).hexdigest()}|rows={len(rows)}|final={clean(final)}"
            )
            for row in rows:
                key=(str(row.get("timestamp") or ""),str(row.get("original") or ""))
                all_rows[key]=row
            if label=="game-200":
                for row in rows:
                    print(
                        f"GAME200|timestamp={clean(row.get('timestamp'))}|original={clean(row.get('original'))}|"
                        f"status={clean(row.get('statuscode'))}|mime={clean(row.get('mimetype'))}|"
                        f"length={clean(row.get('length'))}|digest={clean(row.get('digest'))}|redirect={clean(row.get('redirect'))}"
                    )
            identities=[r for r in rows if html_identity_candidate(r)]
            for r in identities[:100]:
                print(
                    f"IDENTITY_HTML|query={label}|timestamp={clean(r.get('timestamp'))}|"
                    f"original={clean(r.get('original'))}|status={clean(r.get('statuscode'))}|"
                    f"mime={clean(r.get('mimetype'))}|length={clean(r.get('length'))}|digest={clean(r.get('digest'))}"
                )
        except Exception as e:
            errors.append((f"cdx:{label}",type(e).__name__,str(e)))

    buckets=collections.Counter(path_bucket(str(r.get("original") or "")) for r in all_rows.values())
    for bucket,count in buckets.most_common(50):
        print(f"PATH_BUCKET|path={clean(bucket)}|count={count}")

    # Emit rows closest to the known StoneAge directory and any sa25/stoneage URL token.
    focused=[]
    for row in all_rows.values():
        original=urllib.parse.unquote(str(row.get("original") or ""))
        low=original.lower()
        if "/file/game/maoxian/" in low or "sa25" in low or "stoneage" in low:
            focused.append(row)
    focused.sort(key=lambda r:(str(r.get("timestamp") or ""),str(r.get("original") or "")))
    for r in focused[:500]:
        print(
            f"FOCUSED|timestamp={clean(r.get('timestamp'))}|original={clean(r.get('original'))}|"
            f"status={clean(r.get('statuscode'))}|mime={clean(r.get('mimetype'))}|"
            f"length={clean(r.get('length'))}|digest={clean(r.get('digest'))}|redirect={clean(r.get('redirect'))}"
        )

    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|source_same_host_links|{len(anchors)}")
    print(f"COUNT|unique_cdx_rows|{len(all_rows)}")
    print(f"COUNT|focused_rows|{len(focused)}")
    print(f"COUNT|errors|{len(errors)}")
    if anchors or focused:
        print("RESOLUTION|HOST_NEIGHBORHOOD_MAPPED|use sibling link labels and HTML root candidates to identify host/mirror lineage")
    elif errors:
        print("RESOLUTION|PARTIAL_HOST_NEIGHBORHOOD_FAILURE|retry failed metadata surface only")
    else:
        print("RESOLUTION|NO_HOST_NEIGHBORHOOD_SIGNAL|tested source+CDX surfaces bounded")
    print(
        "EVIDENCE_BOUNDARY|same-host links and CDX rows map a historical download neighborhood only; "
        "they do not establish ownership, official StoneAge distribution, or payload identity."
    )


if __name__=="__main__":
    main()
