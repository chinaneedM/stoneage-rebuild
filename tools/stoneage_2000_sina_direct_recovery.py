#!/usr/bin/env python3
"""Transiently recover the exact 2000 Sina StoneAge map ZIP if archived.

The direct route is first-party routing evidence recovered from Sina's archived
CGI page. This tool asks the Wayback availability API for exact snapshots and,
only if an exact archived object is available, reads at most 4 MiB, hashes it,
validates ZIP structure, and emits an entry inventory. Payload bytes are never
written to the repository.
"""
from __future__ import annotations
import hashlib, io, json, zipfile, urllib.parse, urllib.request

UA="stoneage-rebuild-archaeology/1.0"
TARGET="http://202.106.184.193/downfiles/map_1212/samap_1220.zip"
EXPECTED_KIB=1410
MAX_BYTES=4*1024*1024
AVAIL="https://archive.org/wayback/available"
DATES=("20001220","20010101","20010126","20010201","20011220","20020101","20051103")

def clean(v,n=6000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=50,max_bytes=MAX_BYTES):
    req=urllib.request.Request(url,headers={
        "User-Agent":UA,
        "Accept":"application/json,application/zip,application/octet-stream,*/*;q=0.5",
        "Accept-Encoding":"identity",
    })
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b

def availability(date):
    q=AVAIL+"?"+urllib.parse.urlencode({"url":TARGET,"timestamp":date})
    st,final,h,b=fetch(q,timeout=30,max_bytes=1024*1024)
    d=json.loads(b.decode("utf-8"))
    c=(d.get("archived_snapshots") or {}).get("closest") or {}
    return st,c if c.get("available") else None

def replay_url(timestamp):
    return f"https://web.archive.org/web/{timestamp}id_/{TARGET}"

def zip_inventory(body):
    if len(body)>MAX_BYTES:
        raise ValueError("payload exceeds bounded recovery cap")
    bio=io.BytesIO(body)
    if not zipfile.is_zipfile(bio):
        return (),False
    bio.seek(0)
    rows=[]
    with zipfile.ZipFile(bio) as z:
        for info in z.infolist():
            rows.append({
                "name":info.filename,
                "size":info.file_size,
                "compressed":info.compress_size,
                "crc32":f"{info.CRC:08x}",
                "dir":info.is_dir(),
            })
    return tuple(rows),True

def choose_capture(captures):
    # Prefer an archived HTTP-200 object closest to the historical distribution.
    rows=[c for c in captures if str(c.get("status") or "")=="200" and c.get("timestamp")]
    if not rows:return None
    rows.sort(key=lambda c:(abs(int(str(c["timestamp"])[:8])-20001220),str(c["timestamp"])))
    return rows[0]

def main():
    print("StoneAge 2000 Sina direct-route transient recovery — R1")
    print("SCOPE|exact archived URL availability + bounded transient body + hash/ZIP inventory|payload-not-retained")
    print(f"TARGET|url={TARGET}|stated_size_kib={EXPECTED_KIB}|max_bytes={MAX_BYTES}")
    errors=[];caps=[];seen=set()
    for date in DATES:
        try:
            st,c=availability(date)
            print(f"AVAIL|date={date}|status={st}|hit={int(c is not None)}|timestamp={clean(c.get('timestamp') if c else '')}|capture={clean(c.get('url') if c else '')}|http_status={clean(c.get('status') if c else '')}")
            if c and c.get("timestamp"):
                key=(str(c.get("timestamp")),str(c.get("url")))
                if key not in seen:
                    seen.add(key);caps.append(c)
        except Exception as e:
            errors.append((f"avail:{date}",type(e).__name__,str(e)))
    chosen=choose_capture(caps)
    print(f"COUNT|unique_captures|{len(caps)}")
    if chosen:
        ts=str(chosen.get("timestamp"))
        print(f"CHOSEN|timestamp={clean(ts)}|capture={clean(chosen.get('url'))}|http_status={clean(chosen.get('status'))}")
        try:
            st,final,h,b=fetch(replay_url(ts),timeout=60,max_bytes=MAX_BYTES)
            overflow=int(len(b)>MAX_BYTES)
            if overflow:b=b[:MAX_BYTES]
            print(f"REPLAY|status={st}|bytes={len(b)}|overflow={overflow}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
            for k,v in sorted(h.items(),key=lambda kv:kv[0].lower()):
                if k.lower() in ("content-type","content-length","x-archive-orig-content-type","x-archive-orig-content-length","x-archive-orig-last-modified","x-archive-orig-etag"):
                    print(f"HEADER|key={clean(k)}|value={clean(v)}")
            rows,iszip=zip_inventory(b)
            print(f"ZIP|valid={int(iszip)}|entries={len(rows)}")
            for i,r in enumerate(rows,1):
                print(f"ZIP_ENTRY|index={i}|name={clean(r['name'])}|size={r['size']}|compressed={r['compressed']}|crc32={r['crc32']}|dir={int(r['dir'])}")
            if iszip:
                print("RESOLUTION|EXACT_ZIP_RECOVERED|compare extracted field-map files against Taiwan v1.0 and later proven corpora")
            else:
                print("RESOLUTION|ARCHIVE_OBJECT_NOT_ZIP|inspect replay headers/body classification before any provenance claim")
        except Exception as e:
            errors.append(("replay",type(e).__name__,str(e)))
            print("RESOLUTION|CAPTURE_REPLAY_FAILED|retain exact capture timestamp and retry via alternate replay surface")
    else:
        print("RESOLUTION|NO_EXACT_ARCHIVED_OBJECT|continue independent mirror/cache search from recovered direct route")
    for s,k,m in errors:
        print(f"ERROR|scope={clean(s)}|kind={clean(k)}|message={clean(m)}")
    print(f"COUNT|errors|{len(errors)}")
    print("EVIDENCE_BOUNDARY|only an exact recovered ZIP body can establish package contents; derived hashes/inventory may be committed, payload bytes may not.")

if __name__=="__main__":
    main()
