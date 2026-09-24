#!/usr/bin/env python3
"""Transiently analyze archived historical StoneAge map.exe captures.

The source-derived mirror target is preserved by Wayback at two timestamps.
This probe downloads each capture only into a temporary directory, derives
hash/archive/file-map metadata, validates map/<n>.dat against the known
three-plane cache shape, and prints derived metadata. No package or DAT bytes
are written into the repository.
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
import re
import struct
import subprocess
import shutil
import tempfile
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
MAX_PACKAGE=64*1024*1024
MAX_EXTRACTED=512*1024*1024
ORIGINAL="http://www.wuxitianlong.com:80/sa/map.exe"
CAPTURES=(
    ("20030623234451",ORIGINAL),
    ("20031210092426",ORIGINAL),
)
MAP_RE=re.compile(r"(?i)(?:^|[/\\])map[/\\](\d+)\.dat$")


def clean(value,limit=1800):
    text=" ".join(str(value if value is not None else "").split())
    return "".join(ch for ch in text if ch>=" " and ch!="\x7f").replace("|","%7C")[:limit]


def replay_url(timestamp,original):
    return f"https://web.archive.org/web/{timestamp}id_/{original}"


def fetch_bounded(url,limit=MAX_PACKAGE,timeout=45):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"*/*"})
    with urllib.request.urlopen(req,timeout=timeout) as response:
        data=response.read(limit+1)
        if len(data)>limit:
            raise ValueError(f"capture exceeds {limit} byte safety cap")
        return {
            "status":int(getattr(response,"status",response.getcode())),
            "final":response.geturl(),
            "headers":dict(response.headers),
            "data":data,
        }


def signature(data):
    raw=bytes(data)
    if raw.startswith(b"MZ"):
        return "pe-mz"
    if raw.startswith(b"PK\x03\x04"):
        return "zip"
    if raw.startswith(b"Rar!"):
        return "rar"
    if raw.startswith(b"7z\xbc\xaf\x27\x1c"):
        return "7z"
    if raw.startswith(b"MSCF"):
        return "cab"
    if raw.lstrip()[:16].lower().startswith((b"<html",b"<!doctype")):
        return "html"
    return "other:"+raw[:16].hex()


def seven_zip_command():
    return shutil.which("7zz") or shutil.which("7z") or "7z"


def run7z(args,timeout=120):
    proc=subprocess.run(
        [seven_zip_command(),*args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
        check=False,
    )
    return proc.returncode,proc.stdout.decode("utf-8","replace"),proc.stderr.decode("utf-8","replace")


def archive_entries(path):
    code,out,err=run7z(["l","-slt","-ba",str(path)])
    rows=[]
    current={}
    for line in out.splitlines()+[""]:
        if not line.strip():
            if current.get("Path") and "Size" in current:
                rows.append(current)
            current={}
            continue
        if " = " in line:
            key,value=line.split(" = ",1)
            current[key.strip()]=value.strip()
    return code,tuple(rows),err


def parse_map_dat(data):
    raw=bytes(data)
    if len(raw)<8:
        return None
    width,height=struct.unpack_from("<II",raw,0)
    if width<1 or height<1:
        return None
    cells=width*height
    expected=8+cells*6
    if expected!=len(raw):
        return None
    values=struct.unpack_from(f"<{cells*3}H",raw,8)
    tile=values[:cells]
    parts=values[cells:cells*2]
    event=values[cells*2:]
    return {
        "width":width,
        "height":height,
        "cells":cells,
        "tile_nonzero":sum(v!=0 for v in tile),
        "parts_nonzero":sum(v!=0 for v in parts),
        "event_nonzero":sum(v!=0 for v in event),
        "tile_max":max(tile,default=0),
        "parts_max":max(parts,default=0),
        "event_max":max(event,default=0),
    }


def safe_extract(archive_path,out_dir):
    code,out,err=run7z(["x","-y",f"-o{out_dir}",str(archive_path)],timeout=180)
    total=0
    for root,dirs,files in os.walk(out_dir):
        for name in files:
            p=Path(root)/name
            try:
                total+=p.stat().st_size
            except OSError:
                continue
            if total>MAX_EXTRACTED:
                raise ValueError(f"extracted data exceeds {MAX_EXTRACTED} byte safety cap")
    return code,total,err


def iter_map_files(root):
    rows=[]
    root=Path(root)
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel=path.relative_to(root).as_posix()
        m=MAP_RE.search(rel)
        if m:
            rows.append((int(m.group(1)),rel,path))
    return tuple(sorted(rows,key=lambda row:(row[0],row[1].lower())))


def main():
    print("StoneAge historical map.exe capture analysis — R1")
    print("SCOPE|Wayback-capture-transient-download+archive-list+map-dat-validation|derived-metadata-only|no-payload-commit")
    print(f"ORIGINAL|{ORIGINAL}")

    capture_summaries=[]
    with tempfile.TemporaryDirectory(prefix="stoneage-map-pack-") as td:
        work=Path(td)
        for timestamp,original in CAPTURES:
            replay=replay_url(timestamp,original)
            try:
                result=fetch_bounded(replay)
            except Exception as exc:
                print(f"ERROR|timestamp={timestamp}|phase=fetch|kind={type(exc).__name__}|message={clean(exc)}")
                continue

            data=result["data"]
            sha=hashlib.sha256(data).hexdigest()
            md5=hashlib.md5(data).hexdigest()
            sig=signature(data)
            archive=work/f"{timestamp}.bin"
            archive.write_bytes(data)
            print(
                f"CAPTURE|timestamp={timestamp}|status={result['status']}|bytes={len(data)}|"
                f"sha256={sha}|md5={md5}|signature={sig}|"
                f"content_type={clean(result['headers'].get('Content-Type',''))}|final={clean(result['final'])}"
            )

            list_code,entries,list_err=archive_entries(archive)
            file_entries=[row for row in entries if row.get("Folder","-")!="+"]
            map_entry_count=sum(1 for row in file_entries if MAP_RE.search(str(row.get("Path",""))))
            print(
                f"ARCHIVE|timestamp={timestamp}|7z_code={list_code}|entries={len(file_entries)}|"
                f"map_entries={map_entry_count}|error={clean(list_err)}"
            )
            for row in file_entries:
                p=str(row.get("Path",""))
                if MAP_RE.search(p):
                    print(
                        f"ARCHIVE_MAP_ENTRY|timestamp={timestamp}|path={clean(p)}|"
                        f"size={clean(row.get('Size'))}|packed={clean(row.get('Packed Size'))}|"
                        f"crc={clean(row.get('CRC'))}|method={clean(row.get('Method'))}"
                    )

            extract_dir=work/f"extract-{timestamp}"
            extract_dir.mkdir()
            extract_code,extracted_bytes,extract_err=safe_extract(archive,extract_dir)
            maps=iter_map_files(extract_dir)
            parsed=0
            invalid=0
            map_ids=[]
            total_map_bytes=0
            hashes=[]
            for map_id,rel,path in maps:
                raw=path.read_bytes()
                total_map_bytes+=len(raw)
                meta=parse_map_dat(raw)
                file_sha=hashlib.sha256(raw).hexdigest()
                hashes.append(file_sha)
                map_ids.append(map_id)
                if meta is None:
                    invalid+=1
                    print(
                        f"MAP|timestamp={timestamp}|id={map_id}|path={clean(rel)}|bytes={len(raw)}|"
                        f"sha256={file_sha}|valid_three_plane=0"
                    )
                    continue
                parsed+=1
                print(
                    f"MAP|timestamp={timestamp}|id={map_id}|path={clean(rel)}|bytes={len(raw)}|"
                    f"sha256={file_sha}|valid_three_plane=1|width={meta['width']}|height={meta['height']}|"
                    f"cells={meta['cells']}|tile_nonzero={meta['tile_nonzero']}|"
                    f"parts_nonzero={meta['parts_nonzero']}|event_nonzero={meta['event_nonzero']}|"
                    f"tile_max={meta['tile_max']}|parts_max={meta['parts_max']}|event_max={meta['event_max']}"
                )
            mapset_digest=hashlib.sha256(
                "\n".join(f"{mid}:{h}" for mid,h in zip(map_ids,hashes)).encode("ascii")
            ).hexdigest()
            print(
                f"EXTRACT|timestamp={timestamp}|tool={clean(seven_zip_command())}|7z_code={extract_code}|extracted_bytes={extracted_bytes}|"
                f"map_files={len(maps)}|valid_three_plane={parsed}|invalid_map_files={invalid}|"
                f"map_bytes={total_map_bytes}|map_id_min={min(map_ids) if map_ids else ''}|"
                f"map_id_max={max(map_ids) if map_ids else ''}|mapset_sha256={mapset_digest}|"
                f"error={clean(extract_err)}"
            )
            capture_summaries.append({
                "timestamp":timestamp,"sha256":sha,"bytes":len(data),
                "maps":len(maps),"parsed":parsed,"mapset":mapset_digest,
            })

    if len(capture_summaries)>=2:
        first=capture_summaries[0]
        for other in capture_summaries[1:]:
            both_usable=first["parsed"]>0 and other["parsed"]>0
            print(
                f"COMPARE|a={first['timestamp']}|b={other['timestamp']}|"
                f"package_same={int(first['sha256']==other['sha256'])}|"
                f"package_bytes_same={int(first['bytes']==other['bytes'])}|"
                f"both_maps_usable={int(both_usable)}|"
                f"map_count_same={int(both_usable and first['maps']==other['maps'])}|"
                f"mapset_same={int(both_usable and first['mapset']==other['mapset'])}"
            )

    usable=[row for row in capture_summaries if row["parsed"]>0]
    if usable:
        print("RESOLUTION|HISTORICAL_MAP_PACK_BYTES_RECOVERED|derived map-cache corpus available for descendant comparison only")
    elif capture_summaries:
        print("RESOLUTION|CAPTURE_RECOVERED_NO_VALID_MAP_DAT|archive bytes recovered but no validated map cache")
    else:
        print("RESOLUTION|INCONCLUSIVE|no capture bytes recovered")


if __name__=="__main__":
    main()
