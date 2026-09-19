#!/usr/bin/env python3
"""Focused second-pass probe for Taiwan StoneAge v1.0 runtime identity and sound deltas.

Outputs only derived metadata:
- PE imports + version-resource strings for StoneAge.exe and sa_3.exe
- exact diagnosis of sound_1.bin vs standalone WAV differences
- numeric Taiwan v1.0 -> recovered 2.5 resource-generation comparison from committed reports

The accepted retail disc is consumed only on an ephemeral CI runner.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re
import struct
import tempfile

from tools.stoneage_tw10_technical_probe import (
    extract_row,
    find_rows,
    parse_addr_table,
)

ROOT = Path(__file__).resolve().parents[1]
TW_REPORT = ROOT / "research/recovered/STONEAGE-TW10-TECHNICAL-PROBE-R1.txt"
R25_REPORT = ROOT / "research/recovered/STONEAGE-25-RESOURCE-PROBE-R1.txt"
S25_REPORT = ROOT / "research/recovered/STONEAGE-25-SPR-PROBE-R1.txt"


def clean(value, limit=2500):
    text = " ".join(str(value if value is not None else "").split())
    return "".join(ch for ch in text if ch >= " " and ch != "\x7f").replace("|", "%7C")[:limit]


def digest(data):
    return hashlib.md5(data).hexdigest(), hashlib.sha1(data).hexdigest(), hashlib.sha256(data).hexdigest()


def first_diff(a, b):
    n = min(len(a), len(b))
    for i in range(n):
        if a[i] != b[i]:
            return i
    return n if len(a) != len(b) else -1


def common_prefix(a, b):
    n=min(len(a),len(b))
    i=0
    while i<n and a[i]==b[i]:
        i+=1
    return i


def common_suffix(a, b):
    n=min(len(a),len(b))
    i=0
    while i<n and a[-1-i]==b[-1-i]:
        i+=1
    return i


def parse_wave(data):
    """Return derived RIFF/WAVE chunk metadata and data-chunk digest, no payload."""
    out = {
        "riff": False,
        "wave": False,
        "riff_size": None,
        "fmt_audio_format": None,
        "fmt_channels": None,
        "fmt_sample_rate": None,
        "fmt_byte_rate": None,
        "fmt_block_align": None,
        "fmt_bits_per_sample": None,
        "data_size": None,
        "data_md5": None,
        "data_sha1": None,
        "chunks": [],
    }
    if len(data) < 12 or data[:4] != b"RIFF" or data[8:12] != b"WAVE":
        return out
    out["riff"] = True
    out["wave"] = True
    out["riff_size"] = struct.unpack_from("<I", data, 4)[0]
    pos = 12
    while pos + 8 <= len(data):
        cid = data[pos:pos+4]
        size = struct.unpack_from("<I", data, pos+4)[0]
        start = pos + 8
        end = min(len(data), start + size)
        name = cid.decode("ascii", "replace")
        out["chunks"].append((name, size, start))
        if cid == b"fmt " and end - start >= 16:
            vals = struct.unpack_from("<HHIIHH", data, start)
            (
                out["fmt_audio_format"],
                out["fmt_channels"],
                out["fmt_sample_rate"],
                out["fmt_byte_rate"],
                out["fmt_block_align"],
                out["fmt_bits_per_sample"],
            ) = vals
        elif cid == b"data":
            payload = data[start:end]
            out["data_size"] = size
            out["data_md5"] = hashlib.md5(payload).hexdigest()
            out["data_sha1"] = hashlib.sha1(payload).hexdigest()
        pos = start + size + (size & 1)
    return out


def pe_metadata(path):
    import pefile
    pe=pefile.PE(str(path), fast_load=False)
    imports=[]
    if hasattr(pe, "DIRECTORY_ENTRY_IMPORT"):
        for entry in pe.DIRECTORY_ENTRY_IMPORT:
            dll=entry.dll.decode("ascii","replace") if entry.dll else ""
            funcs=[]
            for imp in entry.imports:
                if imp.name:
                    funcs.append(imp.name.decode("ascii","replace"))
                elif imp.ordinal is not None:
                    funcs.append(f"#{imp.ordinal}")
            imports.append((dll, funcs))
    strings={}
    if hasattr(pe, "FileInfo"):
        for group in pe.FileInfo:
            for item in group:
                key=getattr(item,"Key",b"")
                if isinstance(key,bytes):
                    key=key.decode("utf-8","replace")
                if key=="StringFileInfo":
                    for st in getattr(item,"StringTable",[]):
                        for k,v in st.entries.items():
                            if isinstance(k,bytes):
                                k=k.decode("utf-8","replace")
                            if isinstance(v,bytes):
                                for enc in ("utf-8","utf-16le","cp950","latin-1"):
                                    try:
                                        v=v.decode(enc)
                                        break
                                    except Exception:
                                        continue
                            strings[str(k)]=str(v)
    fixed={}
    if getattr(pe,"VS_FIXEDFILEINFO",None):
        ffi=pe.VS_FIXEDFILEINFO[0]
        fixed={
            "file_version":f"{ffi.FileVersionMS>>16}.{ffi.FileVersionMS&0xffff}.{ffi.FileVersionLS>>16}.{ffi.FileVersionLS&0xffff}",
            "product_version":f"{ffi.ProductVersionMS>>16}.{ffi.ProductVersionMS&0xffff}.{ffi.ProductVersionLS>>16}.{ffi.ProductVersionLS&0xffff}",
            "file_flags":ffi.FileFlags,
            "file_type":ffi.FileType,
        }
    return imports,strings,fixed


def emit_pe(label,path):
    imports,strings,fixed=pe_metadata(path)
    print(
        f"PE_IDENTITY|label={label}|file_version={clean(fixed.get('file_version'))}|"
        f"product_version={clean(fixed.get('product_version'))}|file_flags={fixed.get('file_flags','')}|"
        f"file_type={fixed.get('file_type','')}|string_keys={len(strings)}|import_dlls={len(imports)}"
    )
    for k in sorted(strings):
        print(f"PE_VERSION_STRING|label={label}|key={clean(k)}|value={clean(strings[k])}")
    for dll,funcs in imports:
        print(f"PE_IMPORT_DLL|label={label}|dll={clean(dll)}|function_count={len(funcs)}")
        for fn in funcs:
            print(f"PE_IMPORT|label={label}|dll={clean(dll)}|name={clean(fn)}")


def extract_sound_inputs(bin_path):
    img,rows,layout,joliet=find_rows(bin_path)
    td=tempfile.TemporaryDirectory()
    root=Path(td.name)
    try:
        by={r["path"]:r for r in rows if not r["is_dir"]}
        targets=("StoneAge/StoneAge.exe","StoneAge/sa_3.exe","StoneAge/data/sound_1.bin","StoneAge/data/soundaddr_1.txt")
        for p in targets:
            extract_row(img,by[p],root/p)
        for r in rows:
            if not r["is_dir"] and r["path"].startswith("StoneAge/data/se/"):
                extract_row(img,r,root/r["path"])
        return img,td,root,layout,joliet
    except Exception:
        img.close()
        td.cleanup()
        raise


def diagnose_sound(root):
    table=parse_addr_table(root/"StoneAge/data/soundaddr_1.txt")
    container=(root/"StoneAge/data/sound_1.bin").read_bytes()
    files={}
    for p in (root/"StoneAge/data/se").rglob("*"):
        if p.is_file():
            files.setdefault(p.name.lower(),[]).append(p)

    exact=0
    mismatches=[]
    for idx,(off,size,name) in enumerate(table):
        seg=container[off:off+size]
        candidates=files.get(Path(name).name.lower(),[])
        if any(p.read_bytes()==seg for p in candidates):
            exact+=1
            continue
        candidate=candidates[0].read_bytes() if candidates else b""
        sm=digest(seg)
        fm=digest(candidate) if candidate else ("","","")
        sw=parse_wave(seg)
        fw=parse_wave(candidate) if candidate else {}
        mismatches.append({
            "index":idx,"offset":off,"size":size,"name":name,
            "standalone_size":len(candidate),"first_diff":first_diff(seg,candidate),
            "common_prefix":common_prefix(seg,candidate),"common_suffix":common_suffix(seg,candidate),
            "segment_md5":sm[0],"segment_sha1":sm[1],"file_md5":fm[0],"file_sha1":fm[1],
            "seg_wave":sw,"file_wave":fw,
        })
    print(f"SOUND_DIAG|records={len(table)}|exact={exact}|mismatch={len(mismatches)}|container_bytes={len(container)}")
    for m in mismatches:
        sw=m["seg_wave"]; fw=m["file_wave"]
        payload_equal=bool(sw.get("data_sha1") and sw.get("data_sha1")==fw.get("data_sha1"))
        fmt_equal=(
            sw.get("fmt_audio_format"),sw.get("fmt_channels"),sw.get("fmt_sample_rate"),
            sw.get("fmt_byte_rate"),sw.get("fmt_block_align"),sw.get("fmt_bits_per_sample")
        ) == (
            fw.get("fmt_audio_format"),fw.get("fmt_channels"),fw.get("fmt_sample_rate"),
            fw.get("fmt_byte_rate"),fw.get("fmt_block_align"),fw.get("fmt_bits_per_sample")
        )
        print(
            f"SOUND_MISMATCH|index={m['index']}|name={clean(m['name'])}|offset={m['offset']}|"
            f"table_size={m['size']}|standalone_size={m['standalone_size']}|"
            f"first_diff={m['first_diff']}|common_prefix={m['common_prefix']}|common_suffix={m['common_suffix']}|"
            f"segment_md5={m['segment_md5']}|standalone_md5={m['file_md5']}|"
            f"segment_sha1={m['segment_sha1']}|standalone_sha1={m['file_sha1']}|"
            f"segment_riff={int(bool(sw.get('riff')))}|standalone_riff={int(bool(fw.get('riff')))}|"
            f"segment_data_size={sw.get('data_size')}|standalone_data_size={fw.get('data_size')}|"
            f"payload_equal={int(payload_equal)}|fmt_equal={int(fmt_equal)}|"
            f"segment_rate={sw.get('fmt_sample_rate')}|standalone_rate={fw.get('fmt_sample_rate')}|"
            f"segment_bits={sw.get('fmt_bits_per_sample')}|standalone_bits={fw.get('fmt_bits_per_sample')}"
        )
        print(f"SOUND_CHUNKS|name={clean(m['name'])}|segment={clean(sw.get('chunks'))}|standalone={clean(fw.get('chunks'))}")


def kv_lines(path):
    d={}
    for line in path.read_text("utf-8",errors="replace").splitlines():
        if "|" not in line:
            continue
        parts=line.split("|")
        d.setdefault(parts[0],[]).append(parts[1:])
    return d


def single_metric(data,key):
    rows=data.get(key,[])
    if not rows:
        return None
    return rows[0][0] if rows[0] else None


def tw_real_metrics():
    vals={}
    for line in TW_REPORT.read_text("utf-8",errors="replace").splitlines():
        if line.startswith("REAL_ADRN_METRIC|"):
            body=line.split("|",1)[1]
            k,v=body.split("=",1)
            vals[k]=int(v)
        elif line.startswith("REAL_ADRN_COUNT|"):
            _,k,v=line.split("|",2)
            vals[k]=int(v)
        elif line.startswith("REAL_ADRN_FLAG|"):
            _,k,v=line.split("|",2)
            vals["flag_"+k]=int(v)
        elif line.startswith("SPR|"):
            for token in line.split("|")[1:]:
                if "=" in token:
                    k,v=token.split("=",1)
                    try: vals["spr_"+k]=int(v)
                    except ValueError: vals["spr_"+k]=v
        elif line.startswith("SPR_BITMAP_CLASS|"):
            _,k,v=line.split("|",2); vals["bitmap_"+k]=int(v)
    return vals


def legacy25_metrics():
    r={}
    for line in R25_REPORT.read_text("utf-8",errors="replace").splitlines():
        parts=line.split("|")
        if len(parts)==2 and parts[0] in {
            "ADRN_BYTES","REAL_BYTES","ADRN_RECORD_SIZE","ADRN_RECORD_COUNT","ADRN_REMAINDER",
            "ACTIVE_RECORDS","DUPLICATE_BITMAP_NUMBERS","CONTIGUOUS_ACTIVE_OFFSETS",
            "GAP_TRANSITIONS","OVERLAP_TRANSITIONS","UNREFERENCED_REAL_TAIL",
            "ADRN_SIZE_MATCH","ADRN_SIZE_MISMATCH","ADRN_SPECIAL_OR_IMPLAUSIBLE_DIMENSIONS",
        }:
            r[parts[0].lower()]=int(parts[1])
        elif len(parts)==3 and parts[0]=="RD_FLAG":
            r["flag_"+parts[1]]=int(parts[2])
    for line in S25_REPORT.read_text("utf-8",errors="replace").splitlines():
        parts=line.split("|")
        if len(parts)==2 and parts[0] in {
            "SPR_BYTES","RECORD_COUNT","REMAINDER","SPRNO_MIN","SPRNO_MAX",
            "DUPLICATE_SPRNOS","DUPLICATE_OFFSETS","ANIMATION_TOTAL","FRAME_TOTAL"
        }:
            r["spr_"+parts[0].lower()]=int(parts[1])
        elif len(parts)==3 and parts[0]=="BITMAP_CLASS":
            r["bitmap_"+parts[1]]=int(parts[2])
    return r


def emit_generation_compare():
    tw=tw_real_metrics(); later=legacy25_metrics()
    mappings=[
        ("adrn_records","record_count","adrn_record_count"),
        ("real_bytes","real_size","real_bytes"),
        ("duplicate_bitmap_numbers","duplicate_bitmap_numbers","duplicate_bitmap_numbers"),
        ("flag0","flag_0x00","flag_0x00"),
        ("flag1","flag_0x01","flag_0x01"),
        ("special_dimensions","special_or_implausible_dimensions","adrn_special_or_implausible_dimensions"),
        ("spr_records","spr_record_count","spr_record_count"),
        ("spr_animations","spr_animation_total","spr_animation_total"),
        ("spr_frames","spr_frame_total","spr_frame_total"),
        ("sentinel_frames","bitmap_sentinel_ffffffff","bitmap_sentinel_ffffffff"),
    ]
    for label,twk,lk in mappings:
        a=tw.get(twk); b=later.get(lk)
        ratio=(b/a if isinstance(a,int) and a else None)
        print(f"GEN_COMPARE|metric={label}|tw1={a}|v25={b}|delta={(b-a) if isinstance(a,int) and isinstance(b,int) else ''}|ratio={ratio if ratio is not None else ''}")
    print(
        "GEN_SCHEMA|"
        f"tw_adrn_record_size={tw.get('record_size')}|v25_adrn_record_size={later.get('adrn_record_size')}|"
        f"tw_adrn_remainder={tw.get('remainder')}|v25_adrn_remainder={later.get('adrn_remainder')}|"
        f"tw_spr_remainder={tw.get('spr_remainder')}|v25_spr_remainder={later.get('spr_remainder')}|"
        f"tw_duplicate_bitmap={tw.get('duplicate_bitmap_numbers')}|v25_duplicate_bitmap={later.get('duplicate_bitmap_numbers')}|"
        f"v25_duplicate_sprnos={later.get('spr_duplicate_sprnos')}|v25_duplicate_spr_offsets={later.get('spr_duplicate_offsets')}"
    )


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--bin", required=True)
    args=ap.parse_args()
    print("StoneAge Taiwan v1.0 runtime/sound focused probe — R1")
    print("SCOPE|accepted-clean-disc|derived-metadata-only|no-payload-commit")

    img,td,root,layout,joliet=extract_sound_inputs(args.bin)
    try:
        print(f"FILESYSTEM|layout={layout}|joliet={int(joliet)}")
        emit_pe("StoneAge.exe",root/"StoneAge/StoneAge.exe")
        emit_pe("sa_3.exe",root/"StoneAge/sa_3.exe")
        diagnose_sound(root)
        emit_generation_compare()
    finally:
        img.close()
        td.cleanup()


if __name__=="__main__":
    main()
