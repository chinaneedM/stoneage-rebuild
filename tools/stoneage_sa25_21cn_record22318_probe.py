#!/usr/bin/env python3
"""Trace the exact 21CN native StoneAge record id=22318 and its download topology.

Metadata/HTML only. No linked ZIP/client payload is fetched.
"""
from __future__ import annotations

import hashlib
import html
import json
import re
import urllib.parse
import urllib.request

from tools.stoneage_sa25_host_identity_probe import declared_charset, decode, title, visible

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
TARGET_ID="22318"
CONTROL_ID="8247"
HOSTS=("202.104.32.168","download.21cn.com")
TOKENS=("石器时代","石器時代","免费服务器","免費服務器","精灵王","精靈王","sa25","stoneage")
ATTR_RE=re.compile(r"""(?is)(?:href|src)\s*=\s*["']?([^"'\s>]+)""")


def clean(v,limit=2200):
    return " ".join(str(v or "").split()).replace("|","%7C")[:limit]


def fetch(url,timeout=25,max_bytes=3_000_000):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/html,*/*"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        body=r.read(max_bytes+1)
        if len(body)>max_bytes:
            raise ValueError("response-too-large")
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),body


def cdx_url(url,match="exact",limit=500):
    p=[
        ("url",url),("matchType",match),("output","json"),
        ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
        ("from","2001"),("to","2005"),("limit",str(limit)),
    ]
    return CDX+"?"+urllib.parse.urlencode(p)


def parse_cdx(body):
    data=json.loads(body.decode("utf-8","replace"))
    if not isinstance(data,list) or not data or not isinstance(data[0],list):
        return ()
    h=data[0]
    return tuple(dict(zip(h,row)) for row in data[1:] if isinstance(row,list))


def replay_url(row):
    return f"https://web.archive.org/web/{row['timestamp']}id_/{row['original']}"


def relevant_attrs(text):
    out=[]; seen=set()
    for raw in ATTR_RE.findall(text):
        v=html.unescape(raw.strip())
        low=v.lower()
        if (
            "downit.php" in low or "sa25" in low or "stoneage" in low
            or "/file/game/" in low or "22318" in low
        ):
            if v not in seen:
                seen.add(v); out.append(v)
    return tuple(out)


def token_hits(body,text):
    hits=[]
    low=text.lower()
    for token in TOKENS:
        found=token.lower() in low
        if not found and any(ord(ch)>127 for ch in token):
            for enc in ("gb2312","gbk","gb18030","big5","cp950"):
                try:
                    if token.encode(enc) in body:
                        found=True; break
                except Exception:
                    pass
        if found: hits.append(token)
    return tuple(dict.fromkeys(hits))


def context(text,tokens,radius=800):
    v=visible(text); low=v.lower()
    pos=[]
    for t in tokens:
        i=low.find(t.lower())
        if i>=0: pos.append(i)
    if not pos:
        # Native 21CN titles can still be useful even if related-page tokens caused the original broad hit.
        return v[:1800]
    i=min(pos)
    return v[max(0,i-radius):min(len(v),i+radius*2)]


def emit_cdx(label,rows):
    print(f"CDX_COUNT|label={label}|rows={len(rows)}")
    for row in rows:
        print(
            f"CDX_ROW|label={label}|timestamp={clean(row.get('timestamp'))}|original={clean(row.get('original'))}|"
            f"status={clean(row.get('statuscode'))}|mime={clean(row.get('mimetype'))}|length={clean(row.get('length'))}|"
            f"digest={clean(row.get('digest'))}|redirect={clean(row.get('redirect'))}"
        )


def main():
    print("StoneAge 2.5 exact 21CN record 22318 trace — R1")
    print("SCOPE|native-list-record+downit-metadata+file-neighborhood|no-linked-game-payload")
    errors=[]
    list_rows=[]

    # Exact list.php records on IP and evidence-derived hostname, plus control id=8247.
    for record_id in (TARGET_ID,CONTROL_ID):
        for host in HOSTS:
            label=f"list-{record_id}-{host}"
            url=f"http://{host}/list.php?id={record_id}"
            try:
                st,final,hdr,body=fetch(cdx_url(url,"exact",200),30)
                rows=parse_cdx(body)
                print(f"CDX_QUERY|label={label}|status={st}|bytes={len(body)}|sha256={hashlib.sha256(body).hexdigest()}|final={clean(final)}")
                emit_cdx(label,rows)
                if record_id==TARGET_ID:
                    list_rows.extend(rows)
            except Exception as e:
                errors.append((label,type(e).__name__,str(e)))

    # Replay target detail pages only; HTML is safe and small.
    seen=set()
    for row in sorted(list_rows,key=lambda r:(str(r.get("timestamp") or ""),str(r.get("original") or ""))):
        key=(str(row.get("timestamp") or ""),str(row.get("original") or ""))
        if key in seen: continue
        seen.add(key)
        try:
            st,final,hdr,body=fetch(replay_url(row),25,1_500_000)
            enc,text=decode(body,declared_charset(body))
            hits=token_hits(body,text)
            attrs=relevant_attrs(text)
            print(
                f"PAGE|timestamp={clean(row.get('timestamp'))}|original={clean(row.get('original'))}|"
                f"status={st}|bytes={len(body)}|sha256={hashlib.sha256(body).hexdigest()}|"
                f"encoding={clean(enc)}|title={clean(title(text),1400)}|tokens={clean(','.join(hits))}|attrs={len(attrs)}|final={clean(final)}"
            )
            print(f"CONTEXT|timestamp={clean(row.get('timestamp'))}|value={clean(context(text,hits),3400)}")
            for n,a in enumerate(attrs[:100],1):
                print(f"ATTR|timestamp={clean(row.get('timestamp'))}|order={n}|value={clean(a,2200)}")
        except Exception as e:
            errors.append((f"replay:{key[0]}:{key[1]}",type(e).__name__,str(e)))

    # Map all downit variants for this record. CDX redirect metadata is enough;
    # do not replay redirects because that could fetch a software payload.
    for host in HOSTS:
        label=f"downit-{host}"
        prefix=f"http://{host}/downit.php?id={TARGET_ID}"
        try:
            st,final,hdr,body=fetch(cdx_url(prefix,"prefix",500),30)
            rows=parse_cdx(body)
            print(f"CDX_QUERY|label={label}|status={st}|bytes={len(body)}|sha256={hashlib.sha256(body).hexdigest()}|final={clean(final)}")
            emit_cdx(label,rows)
        except Exception as e:
            errors.append((label,type(e).__name__,str(e)))

    # Probe plausible native file directories and exact known sidecar/zip names as metadata only.
    metadata_targets=(
        ("ip-record-dir",f"http://202.104.32.168/file/game/maoxian/{TARGET_ID}/","prefix"),
        ("host-record-dir",f"http://download.21cn.com/file/game/maoxian/{TARGET_ID}/","prefix"),
        ("host-sa25up-jpg","http://download.21cn.com/file/game/maoxian/sa25up.jpg","exact"),
        ("host-sa25up-zip","http://download.21cn.com/file/game/maoxian/sa25up.zip","exact"),
        ("ip-sa25up-jpg","http://202.104.32.168/file/game/maoxian/sa25up.jpg","exact"),
        ("ip-sa25up-zip","http://202.104.32.168/file/game/maoxian/sa25up.zip","exact"),
    )
    for label,url,match in metadata_targets:
        try:
            st,final,hdr,body=fetch(cdx_url(url,match,1000),30)
            rows=parse_cdx(body)
            print(f"CDX_QUERY|label={label}|status={st}|bytes={len(body)}|sha256={hashlib.sha256(body).hexdigest()}|final={clean(final)}")
            emit_cdx(label,rows)
        except Exception as e:
            errors.append((label,type(e).__name__,str(e)))

    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|target_list_rows|{len(list_rows)}")
    print(f"COUNT|errors|{len(errors)}")
    print("RESOLUTION|EXACT_21CN_22318_TRACE_COMPLETE|classify native record versus sa25up sidecar/downit topology from emitted metadata")
    print(
        "EVIDENCE_BOUNDARY|21CN-native record metadata can establish catalogue/title/date/link topology; "
        "without recovered ZIP bytes or an operator chain it cannot establish clean-client or official-package provenance."
    )


if __name__=="__main__":
    main()
