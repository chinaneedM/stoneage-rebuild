#!/usr/bin/env python3
"""Bounded Internet Archive metadata + ISO9660 range probe for item sa-arena.

Purpose: determine whether the public 2002 Beijing-Waei-labelled CD image is a
useful StoneAge client carrier without downloading the whole optical image.
Only IA metadata and small HTTP Range reads of ISO9660 descriptors/directories
are used. If a server ignores Range, the probe refuses to treat the response as
a sector read.
"""
from __future__ import annotations

import json
import struct
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0 (+https://github.com/chinaneedM/stoneage-rebuild)"
IDENTIFIER="sa-arena"
META=f"https://archive.org/metadata/{IDENTIFIER}"
DOWNLOAD=f"https://archive.org/download/{IDENTIFIER}/"
SECTOR=2048
MAX_DIR_BYTES=262144
IMAGE_EXTS=(".iso",".img",".bin",".nrg",".mdf",".ccd",".cue")


def clean(v,n=1800):
    if isinstance(v,list):
        v=",".join(str(x) for x in v)
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]


def get_json(url,timeout=30):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        return json.load(r)


def optical_candidates(files):
    out=[]
    for row in files or []:
        name=str(row.get("name") or "")
        low=name.lower()
        if low.endswith(IMAGE_EXTS):
            out.append(row)
    return tuple(out)


def download_url(name):
    return DOWNLOAD+urllib.parse.quote(str(name),safe="/")


def range_get(url,start,end,timeout=35):
    req=urllib.request.Request(url,headers={
        "User-Agent":UA,
        "Range":f"bytes={start}-{end}",
        "Accept-Encoding":"identity",
    })
    with urllib.request.urlopen(req,timeout=timeout) as r:
        status=int(getattr(r,"status",r.getcode()))
        content_range=str(r.headers.get("Content-Range") or "")
        want=end-start+1
        data=r.read(want+1)
        honored=(status==206 and content_range.lower().startswith("bytes "))
        if not honored:
            return status,content_range,b"",False
        return status,content_range,data[:want],True


def decode_ascii(raw):
    return raw.decode("ascii","replace").rstrip(" \x00")


def parse_pvd(buf):
    if len(buf)<SECTOR:
        raise ValueError("short-pvd")
    if buf[0]!=1 or buf[1:6]!=b"CD001":
        raise ValueError("not-iso9660-pvd")
    root_len=buf[156]
    if root_len<34 or 156+root_len>len(buf):
        raise ValueError("bad-root-record")
    root=buf[156:156+root_len]
    return {
        "system_id":decode_ascii(buf[8:40]),
        "volume_id":decode_ascii(buf[40:72]),
        "volume_space_sectors":struct.unpack_from("<I",buf,80)[0],
        "root_extent":struct.unpack_from("<I",root,2)[0],
        "root_size":struct.unpack_from("<I",root,10)[0],
    }


def parse_directory(buf):
    rows=[]
    pos=0
    total=len(buf)
    while pos<total:
        ln=buf[pos]
        if ln==0:
            pos=((pos//SECTOR)+1)*SECTOR
            continue
        if ln<34 or pos+ln>total:
            break
        rec=buf[pos:pos+ln]
        name_len=rec[32]
        if 33+name_len>len(rec):
            break
        raw_name=rec[33:33+name_len]
        if raw_name==b"\x00":
            name="."
        elif raw_name==b"\x01":
            name=".."
        else:
            name=raw_name.decode("ascii","replace").split(";",1)[0]
        rows.append({
            "name":name,
            "extent":struct.unpack_from("<I",rec,2)[0],
            "size":struct.unpack_from("<I",rec,10)[0],
            "flags":rec[25],
            "is_dir":bool(rec[25]&2),
        })
        pos+=ln
    return tuple(rows)


def dir_range(extent,size):
    start=int(extent)*SECTOR
    length=max(0,min(int(size),MAX_DIR_BYTES))
    if not length:
        return start,start-1
    return start,start+length-1


def main():
    print("StoneAge sa-arena Internet Archive optical-carrier probe — R1")
    print("SCOPE|IA-metadata+bounded-ISO9660-range-reads|no-full-disc-download|no-payload-commit")
    errors=[]
    try:
        meta=get_json(META)
    except Exception as exc:
        print(f"FATAL|metadata|kind={type(exc).__name__}|message={clean(exc)}")
        return

    md=meta.get("metadata",{}) if isinstance(meta,dict) else {}
    print(
        "ITEM|identifier="+clean(md.get("identifier") or IDENTIFIER)+
        "|title="+clean(md.get("title"))+
        "|date="+clean(md.get("date"))+
        "|creator="+clean(md.get("creator"))+
        "|mediatype="+clean(md.get("mediatype"))+
        "|collection="+clean(md.get("collection"))+
        "|description="+clean(md.get("description"),3000)
    )

    candidates=optical_candidates(meta.get("files",[]))
    print(f"COUNT|optical_candidates|{len(candidates)}")
    for i,row in enumerate(candidates,1):
        print(
            f"OPTICAL|index={i}|name={clean(row.get('name'),2200)}|size={clean(row.get('size'))}|"
            f"md5={clean(row.get('md5'))}|sha1={clean(row.get('sha1'))}|"
            f"crc32={clean(row.get('crc32'))}|source={clean(row.get('source'))}|format={clean(row.get('format'))}"
        )

    iso_rows=[r for r in candidates if str(r.get("name") or "").lower().endswith(".iso")]
    parsed=0
    for i,row in enumerate(iso_rows,1):
        name=str(row.get("name") or "")
        url=download_url(name)
        try:
            st,cr,pvd,honored=range_get(url,16*SECTOR,17*SECTOR-1)
            print(f"RANGE_PVD|index={i}|name={clean(name)}|status={st}|honored={int(honored)}|content_range={clean(cr)}")
            if not honored:
                continue
            info=parse_pvd(pvd)
            parsed+=1
            print(
                f"ISO9660|index={i}|volume_id={clean(info['volume_id'])}|system_id={clean(info['system_id'])}|"
                f"volume_sectors={info['volume_space_sectors']}|volume_bytes={info['volume_space_sectors']*SECTOR}|"
                f"root_extent={info['root_extent']}|root_size={info['root_size']}"
            )
            start,end=dir_range(info["root_extent"],info["root_size"])
            if end<start:
                continue
            st2,cr2,root,h2=range_get(url,start,end)
            print(f"RANGE_ROOT|index={i}|status={st2}|honored={int(h2)}|bytes={len(root)}|content_range={clean(cr2)}")
            if not h2:
                continue
            entries=parse_directory(root)
            print(f"COUNT|index={i}|root_entries|{len(entries)}")
            subdirs=[]
            for e in entries:
                print(
                    f"ROOT|index={i}|name={clean(e['name'])}|dir={int(e['is_dir'])}|"
                    f"extent={e['extent']}|size={e['size']}|flags={e['flags']}"
                )
                if e["is_dir"] and e["name"] not in (".",".."):
                    subdirs.append(e)
            for e in subdirs[:20]:
                s,eend=dir_range(e["extent"],e["size"])
                if eend<s:
                    continue
                try:
                    st3,cr3,body,h3=range_get(url,s,eend)
                    print(f"RANGE_DIR|index={i}|dir={clean(e['name'])}|status={st3}|honored={int(h3)}|bytes={len(body)}|content_range={clean(cr3)}")
                    if not h3:
                        continue
                    children=parse_directory(body)
                    print(f"COUNT|index={i}|dir={clean(e['name'])}|entries={len(children)}")
                    for ch in children[:200]:
                        print(
                            f"ENTRY|index={i}|parent={clean(e['name'])}|name={clean(ch['name'])}|dir={int(ch['is_dir'])}|"
                            f"extent={ch['extent']}|size={ch['size']}|flags={ch['flags']}"
                        )
                except Exception as exc:
                    errors.append((f"dir:{name}:{e['name']}",type(exc).__name__,str(exc)))
        except Exception as exc:
            errors.append((f"iso:{name}",type(exc).__name__,str(exc)))

    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|iso_candidates|{len(iso_rows)}")
    print(f"COUNT|iso9660_parsed|{parsed}")
    print(f"COUNT|errors|{len(errors)}")
    if parsed:
        print("RESOLUTION|ISO9660_METADATA_RECOVERED|classify carrier from volume/root tree before any deeper read")
    elif candidates:
        print("RESOLUTION|OPTICAL_METADATA_ONLY|range/format surface did not yield ISO9660 metadata")
    else:
        print("RESOLUTION|NO_OPTICAL_IMAGE_IN_ITEM_METADATA|item is not a usable optical-image lead")
    print("EVIDENCE_BOUNDARY|IA title/date/creator are uploader metadata unless independently sourced; optical-file hashes and ISO9660 structures describe the preserved object but do not by themselves prove original pressing/mastering or StoneAge version.")

if __name__=="__main__":
    main()
