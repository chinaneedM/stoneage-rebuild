#!/usr/bin/env python3
"""Probe the exact Japanese StoneAge 1.74a Hangame install-chain candidates.

The probe is deliberately narrow: three official URLs already recovered from
2003-2004 archive indexes. Archived response bodies are read only up to a hard
cap. Binary payloads are never written to the repository; only hashes, CAB
metadata/member names and interesting HTML references are emitted.
"""

from __future__ import annotations

import concurrent.futures
import hashlib
import html
import json
import re
import struct
import urllib.error
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0 (+https://github.com/chinaneedM/stoneage-rebuild)"
CDX="https://web.archive.org/cdx/search/cdx"
AVAIL="https://archive.org/wayback/available"
MAX_BODY=256*1024
MAX_SNAPSHOTS_PER_TARGET=8

TARGETS=(
    ("hangame-control-cab","http://www.hangame.co.jp:80/publish/sa/HgSA.cab"),
    ("hangame-sadl","http://www.hangame.co.jp:80/publish/sa/sadl.asp"),
    ("hangame-sasetup","http://www.hangame.co.jp:80/publish/sa/sasetup.asp"),
    ("hangame-sasetup2","http://www.hangame.co.jp:80/publish/sa/sasetup2.asp"),
)
KEY_DATES=("20031212","20031214","20031215","20031217","20040115","20040428")

INTEREST_REF=re.compile(
    r"""(?ix)
    (
      https?://[^\s"'<>]+
      |
      [A-Za-z0-9_./:\\-]+\.(?:cab|exe|zip|asp)(?:[?#][^\s"'<>]*)?
    )
    """
)


def clean(value,limit=1200):
    value=" ".join(str(value if value is not None else "").split())
    return "".join(ch for ch in value if ch >= " " and ch != "\x7f").replace("|","%7C")[:limit]


def bounded_get(url,*,timeout=15):
    req=urllib.request.Request(
        url,
        headers={
            "User-Agent":UA,
            "Accept":"*/*",
            "Accept-Encoding":"identity",
            "Range":f"bytes=0-{MAX_BODY-1}",
        },
    )
    with urllib.request.urlopen(req,timeout=timeout) as response:
        body=response.read(MAX_BODY+1)
        return {
            "status":int(getattr(response,"status",200)),
            "final":response.geturl(),
            "headers":dict(response.headers),
            "body":body[:MAX_BODY],
            "truncated":len(body)>MAX_BODY,
        }


def get_json(url,*,timeout=12):
    req=urllib.request.Request(
        url,
        headers={"User-Agent":UA,"Accept":"application/json"},
    )
    with urllib.request.urlopen(req,timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8","replace"))


def cdx_exact(url):
    params=[
        ("url",url),("matchType","exact"),("from","2003"),("to","2004"),
        ("output","json"),
        ("fl","timestamp,original,mimetype,statuscode,digest,length,redirect"),
        ("filter","statuscode:200"),("limit","100"),
    ]
    endpoint=CDX+"?"+urllib.parse.urlencode(params)
    try:
        data=bounded_get(endpoint,timeout=12)["body"]
    except urllib.error.HTTPError as exc:
        if exc.code in (404,503):
            return [],f"HTTPError:{exc.code}"
        raise
    text=data.decode("utf-8","replace").strip()
    if not text:
        return [],None
    rows=json.loads(text)
    if not isinstance(rows,list) or not rows:
        return [],None
    header=rows[0]
    out=[]
    for row in rows[1:]:
        if not isinstance(row,list):
            continue
        out.append({
            str(header[i]):str(row[i]) if i < len(row) else ""
            for i in range(len(header))
        })
    return out,None


def availability(url,date):
    query=urllib.parse.urlencode({"url":url,"timestamp":date})
    data=get_json(AVAIL+"?"+query)
    closest=data.get("archived_snapshots",{}).get("closest")
    if not isinstance(closest,dict) or not closest.get("available"):
        return None
    return {
        "timestamp":str(closest.get("timestamp","")),
        "status":str(closest.get("status","")),
        "url":str(closest.get("url","")),
    }


def url_variants(url):
    parsed=urllib.parse.urlsplit(url)
    host=parsed.hostname or ""
    port=parsed.port
    variants=[url]
    netloc_no_port=host
    if parsed.username:
        netloc_no_port=parsed.username+"@"+netloc_no_port
    without_port=urllib.parse.urlunsplit(
        (parsed.scheme,netloc_no_port,parsed.path,parsed.query,parsed.fragment)
    )
    if without_port not in variants:
        variants.append(without_port)
    if port is None and parsed.scheme=="http":
        with_port=urllib.parse.urlunsplit(
            (parsed.scheme,host+":80",parsed.path,parsed.query,parsed.fragment)
        )
        if with_port not in variants:
            variants.append(with_port)
    return tuple(variants)


def signature(body):
    prefix=bytes(body[:32])
    if prefix.startswith(b"MSCF"):
        return "cab-mscf"
    if prefix.startswith(b"MZ"):
        return "pe-mz"
    lowered=prefix.lstrip().lower()
    if lowered.startswith(b"<html") or lowered.startswith(b"<!doctype"):
        return "html"
    return "other:"+prefix[:16].hex()


def decode_html(body):
    for encoding in ("utf-8","cp932","shift_jis","euc-jp"):
        try:
            return body.decode(encoding)
        except UnicodeDecodeError:
            pass
    return body.decode("latin-1","replace")


def interesting_html_refs(body):
    text=decode_html(body)
    refs={html.unescape(match.group(1)).strip() for match in INTEREST_REF.finditer(text)}
    return tuple(sorted(ref for ref in refs if ref))


def dos_timestamp(date_value,time_value):
    date_value=int(date_value)
    time_value=int(time_value)
    year=1980+((date_value>>9)&0x7F)
    month=(date_value>>5)&0x0F
    day=date_value&0x1F
    hour=(time_value>>11)&0x1F
    minute=(time_value>>5)&0x3F
    second=(time_value&0x1F)*2
    if not (1 <= month <= 12 and 1 <= day <= 31):
        return ""
    return f"{year:04d}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:{second:02d}"


def parse_cab(body):
    data=bytes(body)
    if len(data)<36 or data[:4] != b"MSCF":
        raise ValueError("not a complete CAB header")
    (
        _sig,_r1,cb_cabinet,_r2,coff_files,_r3,
        version_minor,version_major,c_folders,c_files,flags,set_id,i_cabinet,
    )=struct.unpack_from("<4sIIIII BBHHHHH",data,0)
    row={
        "claimed_size":int(cb_cabinet),
        "coff_files":int(coff_files),
        "version_major":int(version_major),
        "version_minor":int(version_minor),
        "folders":int(c_folders),
        "files":int(c_files),
        "flags":int(flags),
        "set_id":int(set_id),
        "cabinet_index":int(i_cabinet),
        "members":[],
    }
    cursor=int(coff_files)
    for index in range(int(c_files)):
        if cursor+16 > len(data):
            row["member_table_complete"]=False
            break
        cb_file,uoff_folder,i_folder,date_value,time_value,attribs=struct.unpack_from(
            "<IIHHHH",data,cursor
        )
        cursor+=16
        end=data.find(b"\x00",cursor)
        if end < 0:
            row["member_table_complete"]=False
            break
        raw_name=data[cursor:end]
        try:
            name=raw_name.decode("cp932")
        except UnicodeDecodeError:
            name=raw_name.decode("latin-1","replace")
        row["members"].append({
            "index":index,
            "name":name,
            "size":int(cb_file),
            "folder":int(i_folder),
            "folder_offset":int(uoff_folder),
            "timestamp":dos_timestamp(date_value,time_value),
            "attributes":int(attribs),
        })
        cursor=end+1
    else:
        row["member_table_complete"]=True
    return row


def select_snapshots(rows,availability_rows):
    merged={}
    for row in rows:
        ts=str(row.get("timestamp",""))
        original=str(row.get("original",""))
        if ts and original:
            merged[(ts,original)]={
                "timestamp":ts,
                "original":original,
                "status":str(row.get("statuscode","")),
                "mime":str(row.get("mimetype","")),
                "digest":str(row.get("digest","")),
                "length":str(row.get("length","")),
                "source":"cdx",
            }
    for original,cap in availability_rows:
        if not cap:
            continue
        ts=str(cap.get("timestamp",""))
        if not ts:
            continue
        merged.setdefault(
            (ts,original),
            {
                "timestamp":ts,
                "original":original,
                "status":str(cap.get("status","")),
                "mime":"",
                "digest":"",
                "length":"",
                "source":"availability",
            },
        )
    return tuple(
        sorted(merged.values(),key=lambda row:(row["timestamp"],row["original"]))[
            :MAX_SNAPSHOTS_PER_TARGET
        ]
    )


def replay_probe(snapshot):
    replay=f"https://web.archive.org/web/{snapshot['timestamp']}id_/{snapshot['original']}"
    try:
        fetched=bounded_get(replay,timeout=15)
    except Exception as exc:
        return {
            "ok":False,"replay":replay,"error":f"{type(exc).__name__}:{exc}",
            "status":"","final":"","content_type":"","bytes":0,"truncated":False,
            "signature":"","sha256":"","cab":None,"refs":(),
        }
    body=fetched["body"]
    sig=signature(body)
    cab=None
    refs=()
    if sig=="cab-mscf":
        try:
            cab=parse_cab(body)
        except Exception:
            cab=None
    elif sig=="html":
        refs=interesting_html_refs(body)
    return {
        "ok":True,
        "replay":replay,
        "error":"",
        "status":fetched["status"],
        "final":fetched["final"],
        "content_type":fetched["headers"].get("Content-Type",""),
        "bytes":len(body),
        "truncated":bool(fetched["truncated"]),
        "signature":sig,
        "sha256":hashlib.sha256(body).hexdigest(),
        "cab":cab,
        "refs":refs,
    }


def main():
    print("StoneAge Japan 1.74a exact Hangame install-chain probe — R1")
    print("SCOPE|three-recovered-official-urls|bounded-replay-read|derived-metadata-only|no-binary-commit")
    print(f"READ_CAP|bytes={MAX_BODY}|snapshots_per_target={MAX_SNAPSHOTS_PER_TARGET}")
    print("KEY_DATES|"+",".join(KEY_DATES))

    all_snapshots=[]
    for label,target in TARGETS:
        rows=[]
        cdx_errors=[]
        for variant in url_variants(target):
            try:
                found,error=cdx_exact(variant)
                rows.extend(found)
                if error:
                    cdx_errors.append((variant,error))
            except Exception as exc:
                cdx_errors.append((variant,f"{type(exc).__name__}:{exc}"))

        avail=[]
        avail_errors=[]
        for date in KEY_DATES:
            try:
                avail.append((target,availability(target,date)))
            except Exception as exc:
                avail_errors.append((date,f"{type(exc).__name__}:{exc}"))

        snapshots=select_snapshots(rows,avail)
        print(
            f"TARGET|label={clean(label)}|url={clean(target)}|"
            f"cdx_rows={len(rows)}|cdx_errors={len(cdx_errors)}|"
            f"availability_hits={sum(cap is not None for _,cap in avail)}|"
            f"availability_errors={len(avail_errors)}|selected_snapshots={len(snapshots)}"
        )
        for variant,error in cdx_errors:
            print(f"CDX_ERROR|label={clean(label)}|url={clean(variant)}|error={clean(error)}")
        for date,error in avail_errors:
            print(f"AVAIL_ERROR|label={clean(label)}|date={date}|error={clean(error)}")
        for snapshot in snapshots:
            print(
                f"SNAPSHOT|label={clean(label)}|timestamp={snapshot['timestamp']}|"
                f"source={snapshot['source']}|status={clean(snapshot['status'])}|"
                f"mime={clean(snapshot['mime'])}|length={clean(snapshot['length'])}|"
                f"digest={clean(snapshot['digest'])}|url={clean(snapshot['original'])}"
            )
            all_snapshots.append((label,snapshot))

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures=[
            (label,snapshot,pool.submit(replay_probe,snapshot))
            for label,snapshot in all_snapshots
        ]
        for label,snapshot,future in futures:
            result=future.result()
            print(
                f"FETCH|label={clean(label)}|timestamp={snapshot['timestamp']}|"
                f"ok={int(result['ok'])}|status={clean(result['status'])}|"
                f"bytes={result['bytes']}|truncated={int(result['truncated'])}|"
                f"signature={clean(result['signature'])}|sha256={clean(result['sha256'])}|"
                f"content_type={clean(result['content_type'])}|"
                f"final={clean(result['final'])}|error={clean(result['error'])}"
            )
            cab=result["cab"]
            if cab is not None:
                print(
                    f"CAB|label={clean(label)}|timestamp={snapshot['timestamp']}|"
                    f"claimed_size={cab['claimed_size']}|coff_files={cab['coff_files']}|"
                    f"format_version={cab['version_major']}.{cab['version_minor']}|"
                    f"folders={cab['folders']}|files={cab['files']}|flags={cab['flags']}|"
                    f"set_id={cab['set_id']}|cabinet_index={cab['cabinet_index']}|"
                    f"member_table_complete={int(cab['member_table_complete'])}"
                )
                for member in cab["members"]:
                    print(
                        f"CAB_FILE|label={clean(label)}|timestamp={snapshot['timestamp']}|"
                        f"index={member['index']}|name={clean(member['name'])}|"
                        f"size={member['size']}|folder={member['folder']}|"
                        f"folder_offset={member['folder_offset']}|"
                        f"timestamp={clean(member['timestamp'])}|attributes={member['attributes']}"
                    )
            for ref in result["refs"]:
                print(
                    f"HTML_REF|label={clean(label)}|timestamp={snapshot['timestamp']}|"
                    f"ref={clean(ref)}"
                )

    print(f"COUNT|selected_snapshots|{len(all_snapshots)}")


if __name__=="__main__":
    main()
