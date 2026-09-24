#!/usr/bin/env python3
"""Recover exact evidence-derived 21CN mirrors of the StoneAge 2.5 sa25up.zip updater.

All target URLs are taken from archived native 21CN catalogue/router pages for record
20165. Wayback CDX is queried first. Only HTTP-200 ZIP-sized captures are replayed,
transiently hashed and inventoried; proprietary ZIP bytes are never written to the repo.
"""
from __future__ import annotations

import concurrent.futures
import hashlib
import io
import json
import time
import urllib.parse
import urllib.request
import zipfile

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"

TARGETS=(
    ("direct-file","http://download.21cn.com/file/game/maoxian/sa25up.zip"),
    ("images-download-file","http://images.21cn.com/download/file/game/maoxian/sa25up.zip"),
    ("direct-file1","http://download.21cn.com/file1/game/maoxian/sa25up.zip"),
    ("dg-file1","http://dg.download.21cn.com/file1/game/maoxian/sa25up.zip"),
    ("dg-file1-21cn","http://dg.download.21cn.com/file1_21cn/game/maoxian/sa25up.zip"),
    ("dg-file1xjy","http://dg.download.21cn.com/file1xjy/game/maoxian/sa25up.zip"),
    ("dg-file1xzm","http://dg.download.21cn.com/file1xzm/game/maoxian/sa25up.zip"),
)
EXPECTED_MIN=7_500_000
EXPECTED_MAX=10_500_000
MAX_FETCH=12_000_000


def clean(v,limit=2600):
    return " ".join(str(v or "").split()).replace("|","%7C")[:limit]


def fetch(url,timeout=30,max_bytes=2_000_000,attempts=2):
    last=None
    for n in range(attempts):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,application/zip,*/*"})
            with urllib.request.urlopen(req,timeout=timeout) as r:
                body=r.read(max_bytes+1)
                if len(body)>max_bytes:
                    raise ValueError("response-too-large")
                return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),body
        except Exception as exc:
            last=exc
            if n+1<attempts:
                time.sleep(0.8*(n+1))
    raise last


def cdx_url(url):
    params=[
        ("url",url),("matchType","exact"),("output","json"),
        ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
        ("from","2002"),("to","2006"),("limit","1000"),
    ]
    return CDX+"?"+urllib.parse.urlencode(params)


def parse_cdx(body):
    data=json.loads(body.decode("utf-8","replace"))
    if not isinstance(data,list) or not data or not isinstance(data[0],list):
        return ()
    header=data[0]
    return tuple(dict(zip(header,row)) for row in data[1:] if isinstance(row,list))


def replay_url(row):
    return f"https://web.archive.org/web/{row['timestamp']}id_/{row['original']}"


def intish(v):
    try:
        return int(str(v or "").strip())
    except Exception:
        return None


def candidate_row(row):
    if str(row.get("statuscode") or "")!="200":
        return False
    length=intish(row.get("length"))
    if length is None:
        return True
    return EXPECTED_MIN <= length <= EXPECTED_MAX


def inventory_zip(body):
    out=[]
    with zipfile.ZipFile(io.BytesIO(body)) as zf:
        for info in zf.infolist():
            out.append({
                "name":info.filename,
                "size":info.file_size,
                "compressed":info.compress_size,
                "crc":f"{info.CRC:08x}",
                "date":"%04d-%02d-%02d %02d:%02d:%02d"%info.date_time,
                "is_dir":info.is_dir(),
            })
    return tuple(out)


def one_cdx(entry):
    label,url=entry
    try:
        st,final,hdr,body=fetch(cdx_url(url),25,3_000_000,2)
        return label,url,st,final,body,parse_cdx(body),None
    except Exception as exc:
        return label,url,None,None,None,(),(type(exc).__name__,str(exc))


def one_replay(entry):
    label,row=entry
    try:
        st,final,hdr,body=fetch(replay_url(row),45,MAX_FETCH,2)
        return label,row,st,final,hdr,body,None
    except Exception as exc:
        return label,row,None,None,None,None,(type(exc).__name__,str(exc))


def main():
    print("StoneAge 2.5 exact 21CN sa25up mirror recovery — R1")
    print("SCOPE|evidence-derived-exact-urls|wayback-cdx+transient-zip-replay|no-proprietary-payload-commit")
    print("EXPECTED|catalogue_size=8473K/8.27M|catalogue_date=2002-01-31|record=20165")
    errors=[]
    rows_by_key={}
    all_rows=[]

    with concurrent.futures.ThreadPoolExecutor(max_workers=7) as ex:
        for label,url,st,final,body,rows,error in ex.map(one_cdx,TARGETS):
            if error:
                errors.append((f"cdx:{label}",error[0],error[1]))
                continue
            print(
                f"CDX_QUERY|label={label}|url={clean(url)}|status={st}|bytes={len(body)}|"
                f"sha256={hashlib.sha256(body).hexdigest()}|rows={len(rows)}|final={clean(final)}"
            )
            for row in rows:
                print(
                    f"CDX_ROW|label={label}|timestamp={clean(row.get('timestamp'))}|"
                    f"original={clean(row.get('original'))}|status={clean(row.get('statuscode'))}|"
                    f"mime={clean(row.get('mimetype'))}|length={clean(row.get('length'))}|"
                    f"digest={clean(row.get('digest'))}|redirect={clean(row.get('redirect'))}|"
                    f"zip_size_candidate={1 if candidate_row(row) else 0}"
                )
                key=(label,str(row.get("timestamp") or ""),str(row.get("original") or ""))
                rows_by_key[key]=row
                all_rows.append((label,row))

    candidates=[]
    seen_digest=set()
    for label,row in all_rows:
        if not candidate_row(row):
            continue
        # Avoid refetching captures with identical archive digest within one exact URL lineage.
        d=str(row.get("digest") or "")
        key=(label,d) if d else (label,str(row.get("timestamp") or ""))
        if key in seen_digest:
            continue
        seen_digest.add(key)
        candidates.append((label,row))

    recovered=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        for label,row,st,final,hdr,body,error in ex.map(one_replay,candidates):
            ts=str(row.get("timestamp") or "")
            if error:
                errors.append((f"replay:{label}:{ts}",error[0],error[1]))
                continue
            magic=body[:4].hex()
            is_zip=body.startswith(b"PK\x03\x04") or body.startswith(b"PK\x05\x06") or body.startswith(b"PK\x07\x08")
            print(
                f"REPLAY|label={label}|timestamp={clean(ts)}|status={st}|bytes={len(body)}|"
                f"sha256={hashlib.sha256(body).hexdigest()}|md5={hashlib.md5(body).hexdigest()}|"
                f"content_type={clean(hdr.get('Content-Type'))}|magic={magic}|zip={1 if is_zip else 0}|final={clean(final)}"
            )
            if not is_zip:
                continue
            try:
                inv=inventory_zip(body)
            except Exception as exc:
                errors.append((f"zip:{label}:{ts}",type(exc).__name__,str(exc)))
                continue
            recovered.append((label,row,body,inv))
            total=sum(x["size"] for x in inv if not x["is_dir"])
            print(
                f"ZIP|label={label}|timestamp={clean(ts)}|files={sum(not x['is_dir'] for x in inv)}|"
                f"dirs={sum(x['is_dir'] for x in inv)}|uncompressed_bytes={total}|"
                f"archive_sha256={hashlib.sha256(body).hexdigest()}"
            )
            for n,item in enumerate(inv,1):
                print(
                    f"ZIP_ENTRY|label={label}|timestamp={clean(ts)}|order={n}|name={clean(item['name'],3000)}|"
                    f"size={item['size']}|compressed={item['compressed']}|crc32={item['crc']}|date={item['date']}|dir={1 if item['is_dir'] else 0}"
                )

    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|targets|{len(TARGETS)}")
    print(f"COUNT|cdx_rows|{len(all_rows)}")
    print(f"COUNT|zip_size_candidates|{len(candidates)}")
    print(f"COUNT|recovered_zip_captures|{len(recovered)}")
    print(f"COUNT|errors|{len(errors)}")
    if recovered:
        print("RESOLUTION|SA25UP_ZIP_RECOVERED|compare updater inventory/hash against bridge and map/resource baselines before historical promotion")
    elif candidates:
        print("RESOLUTION|SA25UP_CANDIDATE_CAPTURE_NOT_RECOVERED_AS_ZIP|inspect replay failures/content types only")
    elif errors:
        print("RESOLUTION|PARTIAL_MIRROR_INDEX_FAILURE|retry only failed exact mirror surfaces")
    else:
        print("RESOLUTION|NO_ARCHIVED_200_SA25UP_ZIP|all evidence-derived exact mirror generations bounded in tested Wayback CDX")
    print(
        "EVIDENCE_BOUNDARY|a recovered 21CN mirror ZIP would establish bytes distributed by 21CN; "
        "operator-master byte identity still requires independent comparison/provenance."
    )


if __name__=="__main__":
    main()
