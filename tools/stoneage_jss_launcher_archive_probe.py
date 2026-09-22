#!/usr/bin/env python3
"""Derived-only probe for the archived first-party JSS StoneAge launcher."""

from __future__ import annotations
import datetime, hashlib, json, re, tempfile
from pathlib import Path
import urllib.parse, urllib.request

from tools.stoneage_tw10_technical_probe import pe_sections
from tools.stoneage_tw10_runtime_deep_probe import objdump_imports

UA="stoneage-rebuild-archaeology/1.0 (+https://github.com/chinaneedM/stoneage-rebuild)"
ORIGINAL="http://www.titan.co.jp/stoneage/stoneage.exe"
CDX="https://web.archive.org/cdx/search/cdx"
AVAIL="https://archive.org/wayback/available"
MAX_BYTES=1024*1024
KEY_DATES=("20010501","20010531","20010630","20010701","20010731","20010815")
ASCII_RE=re.compile(rb"[\x20-\x7e]{4,}")
RELEVANT=re.compile(r"(?i)(stoneage|titan|gamersdream|update|version|cksum|download|data\\|\.exe\b|\.dll\b|\.ini\b|\.txt\b|http|ftp|server|connect)")

def clean(v,limit=1800):
    s=" ".join(str(v if v is not None else "").split())
    return "".join(c for c in s if c>=" " and c!="\x7f").replace("|","%7C")[:limit]

def get_json(url,timeout=12):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8","replace"))

def get_bounded(url,timeout=15):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"*/*","Accept-Encoding":"identity","Range":f"bytes=0-{MAX_BYTES}"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        data=r.read(MAX_BYTES+1)
        if len(data)>MAX_BYTES:
            raise ValueError("replay exceeds 1 MiB safety bound")
        return int(getattr(r,"status",200)),r.geturl(),dict(r.headers),data

def cdx_endpoint():
    params=[("url",ORIGINAL),("matchType","exact"),("from","2000"),("to","2002"),
            ("output","json"),("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
            ("filter","statuscode:200"),("limit","100")]
    return CDX+"?"+urllib.parse.urlencode(params)

def parse_cdx(obj):
    if not isinstance(obj,list) or not obj or not isinstance(obj[0],list):
        return []
    header=obj[0]
    return [{str(header[i]):str(row[i]) if i<len(row) else "" for i in range(len(header))}
            for row in obj[1:] if isinstance(row,list)]

def availability(date):
    ep=AVAIL+"?"+urllib.parse.urlencode({"url":ORIGINAL,"timestamp":date})
    data=get_json(ep)
    c=data.get("archived_snapshots",{}).get("closest")
    if not isinstance(c,dict) or not c.get("available"):
        return None
    return {"timestamp":str(c.get("timestamp","")),"status":str(c.get("status","")),"url":str(c.get("url",""))}

def snapshots(cdx_rows,avail_rows):
    out={}
    for row in cdx_rows:
        ts=str(row.get("timestamp",""))
        original=str(row.get("original") or ORIGINAL)
        if ts:
            out[(ts,original)]={"timestamp":ts,"original":original,"source":"cdx",
                "status":str(row.get("statuscode","")),"mime":str(row.get("mimetype","")),
                "digest":str(row.get("digest","")),"length":str(row.get("length",""))}
    for cap in avail_rows:
        if cap and cap.get("timestamp"):
            key=(str(cap["timestamp"]),ORIGINAL)
            out.setdefault(key,{"timestamp":key[0],"original":ORIGINAL,"source":"availability",
                "status":str(cap.get("status","")),"mime":"","digest":"","length":""})
    return tuple(sorted(out.values(),key=lambda x:x["timestamp"]))

def replay_url(row):
    original=urllib.parse.quote(row["original"],safe=":/?&=%#+,;@[]!$'()*")
    return f"https://web.archive.org/web/{row['timestamp']}id_/{original}"

def hashes(data):
    return hashlib.md5(data).hexdigest(),hashlib.sha1(data).hexdigest(),hashlib.sha256(data).hexdigest()

def relevant_strings(data,limit=120):
    seen=set(); out=[]
    for m in ASCII_RE.finditer(data):
        s=m.group().decode("ascii","replace")
        if RELEVANT.search(s) and s not in seen:
            seen.add(s); out.append(s)
            if len(out)>=limit: break
    return out

def main():
    print("StoneAge JSS archived replacement launcher probe — R1")
    print("SCOPE|first-party-exact-url|bounded-transient-binary-analysis|derived-metadata-only")
    print("ORIGINAL|"+ORIGINAL)
    print(f"MAX_BYTES|{MAX_BYTES}")

    cdx_rows=[]; cdx_error=""
    try: cdx_rows=parse_cdx(get_json(cdx_endpoint()))
    except Exception as e: cdx_error=f"{type(e).__name__}:{e}"
    print(f"CDX|rows={len(cdx_rows)}|error={clean(cdx_error)}")
    for row in cdx_rows:
        print("CDX_ROW|"+ "|".join(clean(x) for x in (
            row.get("timestamp",""),row.get("statuscode",""),row.get("mimetype",""),
            row.get("length",""),row.get("digest",""),row.get("redirect",""),row.get("original",""))))

    avail=[]; avail_errors=[]
    for date in KEY_DATES:
        try: cap=availability(date)
        except Exception as e:
            cap=None; avail_errors.append((date,type(e).__name__,str(e)))
        avail.append(cap)
        if cap:
            print(f"AVAIL|requested={date}|available=1|timestamp={clean(cap['timestamp'])}|status={clean(cap['status'])}|snapshot={clean(cap['url'])}")
        else:
            print(f"AVAIL|requested={date}|available=0")
    for date,kind,msg in avail_errors:
        print(f"AVAIL_ERROR|requested={date}|kind={clean(kind)}|message={clean(msg)}")

    rows=snapshots(cdx_rows,avail)
    print(f"COUNT|candidate_snapshots|{len(rows)}")
    verified=[]
    with tempfile.TemporaryDirectory() as td:
        for idx,row in enumerate(rows):
            print(f"SNAPSHOT|timestamp={row['timestamp']}|source={row['source']}|status={clean(row['status'])}|mime={clean(row['mime'])}|length={clean(row['length'])}|digest={clean(row['digest'])}|original={clean(row['original'])}")
            url=replay_url(row)
            try: status,final,headers,data=get_bounded(url)
            except Exception as e:
                print(f"FETCH_ERROR|timestamp={row['timestamp']}|kind={type(e).__name__}|message={clean(e)}|replay={clean(url)}")
                continue
            pe=pe_sections(data) if data.startswith(b"MZ") else None
            print(f"FETCH|timestamp={row['timestamp']}|status={status}|bytes={len(data)}|mz={int(data.startswith(b'MZ'))}|pe={int(pe is not None)}|content_type={clean(headers.get('Content-Type',''))}|final={clean(final)}")
            if pe is None:
                print(f"NON_PE|timestamp={row['timestamp']}|prefix_hex={data[:32].hex()}|sha256={hashlib.sha256(data).hexdigest()}")
                continue
            md5,sha1,sha256=hashes(data)
            verified.append((row["timestamp"],len(data),sha256))
            try: stamp=datetime.datetime.fromtimestamp(pe["timestamp"],datetime.timezone.utc).isoformat()
            except Exception: stamp=""
            print(f"BINARY|timestamp={row['timestamp']}|size={len(data)}|md5={md5}|sha1={sha1}|sha256={sha256}")
            print(f"PE|timestamp={row['timestamp']}|machine={pe['machine']}|pe_timestamp={pe['timestamp']}|pe_timestamp_utc={clean(stamp)}|entry=0x{pe['entry']:x}|image_base=0x{pe['image_base']:x}|subsystem={pe['subsystem']}|section_count={len(pe['sections'])}")
            for sec in pe["sections"]:
                print(f"PE_SECTION|timestamp={row['timestamp']}|name={clean(sec['name'])}|vaddr=0x{sec['virtual_addr']:x}|vsize={sec['virtual_size']}|raw_size={sec['raw_size']}|sha256={sec['sha256']}")
            p=Path(td)/f"stoneage-{idx}.exe"; p.write_bytes(data)
            rc,imports=objdump_imports(p)
            dlls=sorted({d for d,_ in imports})
            print(f"IMPORTS|timestamp={row['timestamp']}|returncode={rc}|dll_count={len(dlls)}|function_count={len(set(f for _,f in imports))}|dlls={','.join(dlls)}")
            for dll in dlls:
                funcs=sorted(f for d,f in imports if d==dll)
                print(f"IMPORT_DLL|timestamp={row['timestamp']}|dll={clean(dll)}|count={len(funcs)}|functions={','.join(funcs)}")
            for s in relevant_strings(data):
                print(f"STRING|timestamp={row['timestamp']}|text={clean(s)}")
    print(f"COUNT|verified_pe_captures|{len(verified)}")
    print(f"COUNT|unique_sha256|{len(set(x[2] for x in verified))}")
    for ts,size,sha in verified:
        print(f"VERIFIED|timestamp={ts}|size={size}|sha256={sha}")
    print("RESOLUTION|"+("JSS_LAUNCHER_BYTES_ANALYZED|binary-not-committed" if verified else ("ARCHIVE_METADATA_ONLY|replay-bytes-unavailable" if rows else "NO_CAPTURE_DISCOVERED|archive-query-limited")))

if __name__=="__main__": main()
