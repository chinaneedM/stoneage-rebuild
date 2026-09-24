#!/usr/bin/env python3
"""Inspect the archived 21CN sa25up.jpg sidecar without preserving proprietary image bytes.

Fetches the dated Wayback replay transiently and emits only cryptographic/file/JPEG metadata.
"""
from __future__ import annotations

import hashlib
import struct
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
TIMESTAMP="20020517235842"
ORIGINAL="http://download.21cn.com:80/file/game/maoxian/sa25up.jpg"
REPLAY=f"https://web.archive.org/web/{TIMESTAMP}id_/{ORIGINAL}"


def clean(v,limit=1200):
    return " ".join(str(v or "").split()).replace("|","%7C")[:limit]


def fetch(url=REPLAY,timeout=30,max_bytes=2_000_000):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"image/jpeg,*/*"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        body=r.read(max_bytes+1)
        if len(body)>max_bytes:
            raise ValueError("image-too-large")
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),body


def jpeg_metadata(data: bytes):
    if len(data)<4 or data[:2]!=b"\xff\xd8":
        raise ValueError("not-jpeg")
    i=2
    width=height=bits=components=None
    comments=[]
    jfif=None
    exif=False
    icc=False
    photoshop=False
    segments=0
    while i+4<=len(data):
        if data[i]!=0xFF:
            i+=1
            continue
        while i<len(data) and data[i]==0xFF:
            i+=1
        if i>=len(data):
            break
        marker=data[i]; i+=1
        if marker in (0xD8,0xD9):
            continue
        if marker==0xDA:  # SOS; image data follows
            break
        if i+2>len(data):
            break
        seglen=struct.unpack(">H",data[i:i+2])[0]
        if seglen<2 or i+seglen>len(data):
            break
        payload=data[i+2:i+seglen]
        i+=seglen
        segments+=1
        if marker in tuple(range(0xC0,0xC4))+tuple(range(0xC5,0xC8))+tuple(range(0xC9,0xCC))+tuple(range(0xCD,0xD0)):
            if len(payload)>=6:
                bits=payload[0]
                height=struct.unpack(">H",payload[1:3])[0]
                width=struct.unpack(">H",payload[3:5])[0]
                components=payload[5]
        elif marker==0xFE:
            comments.append(payload.decode("latin1","replace"))
        elif marker==0xE0 and payload.startswith(b"JFIF\x00") and len(payload)>=12:
            jfif={
                "version":f"{payload[5]}.{payload[6]:02d}",
                "units":payload[7],
                "xdensity":struct.unpack(">H",payload[8:10])[0],
                "ydensity":struct.unpack(">H",payload[10:12])[0],
            }
        elif marker==0xE1 and payload.startswith(b"Exif\x00\x00"):
            exif=True
        elif marker==0xE2 and payload.startswith(b"ICC_PROFILE\x00"):
            icc=True
        elif marker==0xED and payload.startswith(b"Photoshop 3.0"):
            photoshop=True
    return {
        "width":width,"height":height,"bits":bits,"components":components,
        "comments":tuple(comments),"jfif":jfif,"exif":exif,"icc":icc,
        "photoshop":photoshop,"segments":segments,
    }


def main():
    print("StoneAge 2.5 21CN sa25up.jpg metadata probe — R1")
    print("SCOPE|dated-wayback-jpeg|derived-metadata-only|image-bytes-not-preserved")
    print(f"ARCHIVE|timestamp={TIMESTAMP}|original={ORIGINAL}")
    try:
        status,final,headers,body=fetch()
        meta=jpeg_metadata(body)
    except Exception as exc:
        print(f"ERROR|kind={type(exc).__name__}|message={clean(exc)}")
        print("RESOLUTION|SA25UP_JPG_METADATA_UNAVAILABLE")
        return
    print(
        f"FILE|status={status}|bytes={len(body)}|sha256={hashlib.sha256(body).hexdigest()}|"
        f"content_type={clean(headers.get('Content-Type'))}|last_modified={clean(headers.get('Last-Modified'))}|"
        f"final={clean(final)}"
    )
    print(
        f"JPEG|width={meta['width']}|height={meta['height']}|bits={meta['bits']}|components={meta['components']}|"
        f"segments={meta['segments']}|exif={1 if meta['exif'] else 0}|icc={1 if meta['icc'] else 0}|"
        f"photoshop={1 if meta['photoshop'] else 0}|comments={len(meta['comments'])}"
    )
    if meta["jfif"]:
        j=meta["jfif"]
        print(f"JFIF|version={j['version']}|units={j['units']}|xdensity={j['xdensity']}|ydensity={j['ydensity']}")
    for n,c in enumerate(meta["comments"],1):
        print(f"COMMENT|order={n}|value={clean(c,1800)}")
    print("RESOLUTION|SA25UP_JPG_METADATA_RECOVERED|use as dated 21CN same-stem sidecar evidence only")
    print(
        "EVIDENCE_BOUNDARY|the image path/date/hash and JPEG metadata do not identify the linked ZIP contents, "
        "prove official StoneAge distribution, or establish clean-client provenance."
    )


if __name__=="__main__":
    main()
