#!/usr/bin/env python3
"""Bounded Internet Archive metadata + optical filesystem probe for item sa-arena.

The probe never downloads the full disc. It reads IA metadata, the tiny CUE
sheet, and only the raw sectors needed for ISO9660 volume/root/first-level
directory metadata. HTTP Range must be honored or sector parsing stops.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import struct
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0 (+https://github.com/chinaneedM/stoneage-rebuild)"
IDENTIFIER="sa-arena"
META=f"https://archive.org/metadata/{IDENTIFIER}"
DOWNLOAD=f"https://archive.org/download/{IDENTIFIER}/"
SECTOR=2048
MAX_DIR_BYTES=262144
MAX_SMALL_BYTES=65536
MAX_EXE_PREFIX=524288
TEXT_NAMES={"AUTORUN.INF","README.TXT"}
STRING_KEY_RE=re.compile(r"(?i)(stone\s*age|stoneage|sa[_ -]?arena|arena|waei|wgs|installshield|install|setup|version|product|client|www\\.|https?://|2\\.5|3\\.0|4\\.0)")
IMAGE_EXTS=(".iso",".img",".bin",".nrg",".mdf",".ccd",".cue")
CUE_FILE_RE=re.compile(r'^FILE\s+"([^"]+)"\s+(\S+)',re.I)
CUE_TRACK_RE=re.compile(r"^TRACK\s+(\d+)\s+(\S+)",re.I)
CUE_INDEX_RE=re.compile(r"^INDEX\s+01\s+(\d+):(\d+):(\d+)",re.I)


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
        if name.lower().endswith(IMAGE_EXTS):
            out.append(row)
    return tuple(out)


def download_url(name):
    return DOWNLOAD+urllib.parse.quote(str(name),safe="/")


def small_get(url,timeout=30,limit=MAX_SMALL_BYTES):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        data=r.read(limit+1)
        if len(data)>limit:
            raise ValueError("small-object-limit-exceeded")
        return int(getattr(r,"status",r.getcode())),data


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


def parse_cue(text):
    current_file=""
    current_track=None
    tracks=[]
    for raw in text.splitlines():
        line=raw.strip()
        m=CUE_FILE_RE.match(line)
        if m:
            current_file=m.group(1)
            continue
        m=CUE_TRACK_RE.match(line)
        if m:
            current_track={
                "number":int(m.group(1)),
                "mode":m.group(2).upper(),
                "file":current_file,
                "index_frames":0,
            }
            tracks.append(current_track)
            continue
        m=CUE_INDEX_RE.match(line)
        if m and current_track is not None:
            mm,ss,ff=(int(m.group(i)) for i in range(1,4))
            current_track["index_frames"]=(mm*60+ss)*75+ff
    return tuple(tracks)


def mode_layout(mode):
    mode=str(mode).upper()
    if mode=="MODE1/2352":
        return 2352,16,2048
    if mode=="MODE2/2352":
        return 2352,24,2048
    if mode=="MODE1/2048":
        return 2048,0,2048
    raise ValueError("unsupported-track-mode:"+mode)


def logical_sector_read(url,lba,count,track_start_frames,mode):
    raw_size,data_offset,user_size=mode_layout(mode)
    if user_size!=SECTOR:
        raise ValueError("unsupported-user-sector-size")
    first=track_start_frames+lba
    start=first*raw_size
    end=(first+count)*raw_size-1
    status,cr,raw,honored=range_get(url,start,end)
    if not honored:
        return status,cr,b"",False
    needed=count*raw_size
    if len(raw)<needed:
        raise ValueError("short-raw-range")
    out=bytearray()
    for i in range(count):
        base=i*raw_size+data_offset
        out.extend(raw[base:base+SECTOR])
    return status,cr,bytes(out),True


def capped_sector_count(size):
    return max(0,min(math.ceil(int(size)/SECTOR),math.ceil(MAX_DIR_BYTES/SECTOR)))


def read_extent_prefix(url,entry,limit,track_start_frames,mode):
    want=min(int(entry["size"]),int(limit))
    if want<=0:
        return b""
    count=math.ceil(want/SECTOR)
    status,cr,data,honored=logical_sector_read(
        url,int(entry["extent"]),count,track_start_frames,mode
    )
    print(
        f"RANGE_FILE|name={clean(entry['name'])}|status={status}|honored={int(honored)}|"
        f"requested={want}|bytes={len(data)}|content_range={clean(cr)}"
    )
    if not honored:
        return b""
    return data[:want]


def decode_text(data):
    best=""
    best_enc=""
    for enc in ("utf-8","gb18030","big5","cp949","latin1"):
        try:
            text=data.decode(enc)
        except Exception:
            continue
        score=sum(ch.isprintable() or ch in "\r\n\t" for ch in text)
        if score>len(best):
            best=text
            best_enc=enc
    return best_enc,best


def evidence_lines(text,limit=40):
    out=[]; seen=set()
    for line in text.replace("\x00"," ").splitlines():
        line=" ".join(line.split())
        if not line or not (
            STRING_KEY_RE.search(line)
            or re.search(r"[石器時代华華义義精靈灵王傳传說说版本客戶用户戶端安裝装疯狂原始]",line)
        ):
            continue
        line=clean(line,500)
        if line and line not in seen:
            seen.add(line); out.append(line)
        if len(out)>=limit:
            break
    return tuple(out)


def binary_strings(data,limit=80):
    values=[]
    for m in re.finditer(rb"[\x20-\x7e]{6,}",data):
        values.append(m.group(0).decode("ascii","replace"))
    for m in re.finditer(rb"(?:[\x20-\x7e]\x00){6,}",data):
        values.append(m.group(0).decode("utf-16le","replace"))
    out=[]; seen=set()
    for value in values:
        value=" ".join(value.split())
        if STRING_KEY_RE.search(value) and value not in seen:
            seen.add(value); out.append(clean(value,700))
        if len(out)>=limit:
            break
    return tuple(out)


def pe_summary(data):
    if len(data)<0x40 or data[:2]!=b"MZ":
        return None
    peoff=struct.unpack_from("<I",data,0x3c)[0]
    if peoff+92>len(data) or data[peoff:peoff+4]!=b"PE\x00\x00":
        return {"mz":1,"pe_offset":peoff,"pe_complete":0}
    machine,sections,timestamp=struct.unpack_from("<HHI",data,peoff+4)
    opt=peoff+24
    magic=struct.unpack_from("<H",data,opt)[0]
    subsystem=struct.unpack_from("<H",data,opt+68)[0] if opt+70<=len(data) else -1
    return {
        "mz":1,"pe_offset":peoff,"pe_complete":1,"machine":machine,
        "sections":sections,"timestamp":timestamp,"optional_magic":magic,
        "subsystem":subsystem,
    }


def probe_root_files(index,url,entries,track,errors):
    for entry in entries:
        name=str(entry["name"]).upper()
        if entry["is_dir"]:
            continue
        if name in TEXT_NAMES and int(entry["size"])<=MAX_SMALL_BYTES:
            try:
                data=read_extent_prefix(
                    url,entry,MAX_SMALL_BYTES,track["index_frames"],track["mode"]
                )
                if not data:
                    continue
                enc,text=decode_text(data)
                print(
                    f"TEXT_FILE|index={index}|name={clean(entry['name'])}|size={entry['size']}|"
                    f"sha256={hashlib.sha256(data).hexdigest()}|encoding={clean(enc)}"
                )
                rows=evidence_lines(text)
                print(f"COUNT|index={index}|name={clean(entry['name'])}|evidence_lines={len(rows)}")
                for n,line in enumerate(rows,1):
                    print(f"TEXT_EVIDENCE|index={index}|name={clean(entry['name'])}|line={n}|value={line}")
            except Exception as exc:
                errors.append((f"file:{entry['name']}",type(exc).__name__,str(exc)))
        elif name.endswith(".EXE"):
            try:
                data=read_extent_prefix(
                    url,entry,MAX_EXE_PREFIX,track["index_frames"],track["mode"]
                )
                if not data:
                    continue
                pe=pe_summary(data)
                print(
                    f"EXE_PREFIX|index={index}|name={clean(entry['name'])}|file_size={entry['size']}|"
                    f"prefix_bytes={len(data)}|prefix_sha256={hashlib.sha256(data).hexdigest()}"
                )
                if pe:
                    print("PE|index="+str(index)+"|name="+clean(entry["name"])+"|"+
                          "|".join(f"{k}={clean(v)}" for k,v in pe.items()))
                rows=binary_strings(data)
                print(f"COUNT|index={index}|name={clean(entry['name'])}|key_strings={len(rows)}")
                for n,value in enumerate(rows,1):
                    print(f"EXE_STRING|index={index}|name={clean(entry['name'])}|n={n}|value={value}")
            except Exception as exc:
                errors.append((f"exe:{entry['name']}",type(exc).__name__,str(exc)))


def emit_tree(index,url,track,errors):
    mode=track["mode"]
    start_frames=track["index_frames"]
    st,cr,pvd,h=logical_sector_read(url,16,1,start_frames,mode)
    print(
        f"RANGE_PVD|index={index}|track={track['number']}|mode={clean(mode)}|"
        f"track_start_frames={start_frames}|status={st}|honored={int(h)}|content_range={clean(cr)}"
    )
    if not h:
        return False
    info=parse_pvd(pvd)
    print(
        f"ISO9660|index={index}|track={track['number']}|mode={clean(mode)}|"
        f"volume_id={clean(info['volume_id'])}|system_id={clean(info['system_id'])}|"
        f"volume_sectors={info['volume_space_sectors']}|volume_bytes={info['volume_space_sectors']*SECTOR}|"
        f"root_extent={info['root_extent']}|root_size={info['root_size']}"
    )
    n=capped_sector_count(info["root_size"])
    if not n:
        return True
    st2,cr2,root,h2=logical_sector_read(url,info["root_extent"],n,start_frames,mode)
    print(f"RANGE_ROOT|index={index}|status={st2}|honored={int(h2)}|bytes={len(root)}|content_range={clean(cr2)}")
    if not h2:
        return True
    entries=parse_directory(root)
    print(f"COUNT|index={index}|root_entries|{len(entries)}")
    subdirs=[]
    for e in entries:
        print(
            f"ROOT|index={index}|name={clean(e['name'])}|dir={int(e['is_dir'])}|"
            f"extent={e['extent']}|size={e['size']}|flags={e['flags']}"
        )
        if e["is_dir"] and e["name"] not in (".",".."):
            subdirs.append(e)
    probe_root_files(index,url,entries,track,errors)
    for e in subdirs[:24]:
        count=capped_sector_count(e["size"])
        if not count:
            continue
        try:
            st3,cr3,body,h3=logical_sector_read(url,e["extent"],count,start_frames,mode)
            print(
                f"RANGE_DIR|index={index}|dir={clean(e['name'])}|status={st3}|"
                f"honored={int(h3)}|bytes={len(body)}|content_range={clean(cr3)}"
            )
            if not h3:
                continue
            children=parse_directory(body)
            print(f"COUNT|index={index}|dir={clean(e['name'])}|entries={len(children)}")
            for ch in children[:250]:
                print(
                    f"ENTRY|index={index}|parent={clean(e['name'])}|name={clean(ch['name'])}|"
                    f"dir={int(ch['is_dir'])}|extent={ch['extent']}|size={ch['size']}|flags={ch['flags']}"
                )
        except Exception as exc:
            errors.append((f"dir:{e['name']}",type(exc).__name__,str(exc)))
    return True


def main():
    print("StoneAge sa-arena Internet Archive optical-carrier probe — R3")
    print("SCOPE|IA-metadata+CUE+bounded-raw-sector-filesystem+small-text+EXE-prefix-reads|no-full-disc-download|no-payload-commit")
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
    by_name={}
    for i,row in enumerate(candidates,1):
        name=str(row.get("name") or "")
        by_name[name.lower()]=row
        print(
            f"OPTICAL|index={i}|name={clean(name,2200)}|size={clean(row.get('size'))}|"
            f"md5={clean(row.get('md5'))}|sha1={clean(row.get('sha1'))}|"
            f"crc32={clean(row.get('crc32'))}|source={clean(row.get('source'))}|format={clean(row.get('format'))}"
        )

    parsed=0
    cue_rows=[r for r in candidates if str(r.get("name") or "").lower().endswith(".cue")]
    for ci,cue_row in enumerate(cue_rows,1):
        cue_name=str(cue_row.get("name") or "")
        try:
            st,cue_bytes=small_get(download_url(cue_name))
            cue_text=cue_bytes.decode("utf-8","replace")
            tracks=parse_cue(cue_text)
            print(f"CUE|index={ci}|name={clean(cue_name)}|status={st}|bytes={len(cue_bytes)}|tracks={len(tracks)}")
            for t in tracks:
                print(
                    f"TRACK|cue={ci}|number={t['number']}|mode={clean(t['mode'])}|"
                    f"file={clean(t['file'])}|index_frames={t['index_frames']}"
                )
            for t in tracks:
                if not t["mode"].startswith("MODE"):
                    continue
                row=by_name.get(str(t["file"]).lower())
                if row is None:
                    print(f"TRACK_SKIP|cue={ci}|number={t['number']}|reason=referenced-bin-not-in-IA-metadata")
                    continue
                try:
                    if emit_tree(ci,download_url(row.get("name")),t,errors):
                        parsed+=1
                        break
                except ValueError as exc:
                    print(f"TRACK_SKIP|cue={ci}|number={t['number']}|reason={clean(exc)}")
                except Exception as exc:
                    errors.append((f"track:{t['number']}",type(exc).__name__,str(exc)))
        except Exception as exc:
            errors.append((f"cue:{cue_name}",type(exc).__name__,str(exc)))

    iso_rows=[r for r in candidates if str(r.get("name") or "").lower().endswith(".iso")]
    for i,row in enumerate(iso_rows,1):
        try:
            t={"number":1,"mode":"MODE1/2048","index_frames":0}
            if emit_tree(1000+i,download_url(row.get("name")),t,errors):
                parsed+=1
        except Exception as exc:
            errors.append((f"iso:{row.get('name')}",type(exc).__name__,str(exc)))

    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|cue_candidates|{len(cue_rows)}")
    print(f"COUNT|iso_candidates|{len(iso_rows)}")
    print(f"COUNT|filesystem_tracks_parsed|{parsed}")
    print(f"COUNT|errors|{len(errors)}")
    if parsed:
        print("RESOLUTION|OPTICAL_FILESYSTEM_METADATA_RECOVERED|classify carrier/version from volume and directory traits before deeper reads")
    elif candidates:
        print("RESOLUTION|OPTICAL_METADATA_ONLY|bounded sector surface did not yield a supported ISO9660 filesystem")
    else:
        print("RESOLUTION|NO_OPTICAL_IMAGE_IN_ITEM_METADATA|item is not a usable optical-image lead")
    print("EVIDENCE_BOUNDARY|IA title/date/creator are uploader metadata unless independently sourced; preserved BIN/CUE hashes and filesystem structures describe the archived object but do not alone prove original pressing/mastering or historical StoneAge version.")

if __name__=="__main__":
    main()
