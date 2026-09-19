#!/usr/bin/env python3
"""Technical reverse-engineering probe for the accepted Taiwan StoneAge v1.0 disc.

Consumes an ephemeral local raw CD image and emits only derived metadata:
- early REAL/ADRN and SPR/SPRADRN structural results using the existing 2.5 parsers
- PE section/import/string comparison for StoneAge.exe vs sa_3.exe
- validation of battletxt_1.txt -> battle_1.bin and soundaddr_1.txt -> sound_1.bin
- bounded installer-script/CAB metadata

No proprietary payload bytes are committed.
"""

from __future__ import annotations

import argparse
import collections
import datetime
import hashlib
import os
from pathlib import Path
import re
import struct
import subprocess
import tempfile

from tools.stoneage_resource_probe import analyze_real_adrn
from tools.stoneage_spr_probe import analyze as analyze_spr
from tools.stoneage_tw2000_clean_client_acceptance import (
    detect_layout,
    walk_full,
)

TARGET_PATHS = (
    "StoneAge/StoneAge.exe",
    "StoneAge/sa_3.exe",
    "StoneAge/Setup.exe",
    "StoneAge/setup.inx",
    "StoneAge/data1.cab",
    "StoneAge/data1.hdr",
    "StoneAge/data/real_1.bin",
    "StoneAge/data/adrn_1.bin",
    "StoneAge/data/spr_1.bin",
    "StoneAge/data/spradrn_1.bin",
    "StoneAge/data/battle_1.bin",
    "StoneAge/data/battletxt_1.txt",
    "StoneAge/data/sound_1.bin",
    "StoneAge/data/soundaddr_1.txt",
)

ASCII_RE = re.compile(rb"[\x20-\x7e]{4,}")
RELEVANT_STRING = re.compile(
    r"(?i)(stone|waei|hwaei|server|update|patch|version|\.ini\b|\.dat\b|\.bin\b|"
    r"\.spr\b|\.sab\b|tcp|udp|socket|connect|login|account|passwd|password|"
    r"http|ftp|mail|sa_[0-9]|setup)"
)


def clean(value, limit=2000):
    text = " ".join(str(value if value is not None else "").split())
    return "".join(ch for ch in text if ch >= " " and ch != "\x7f").replace("|", "%7C")[:limit]


def find_rows(bin_path):
    img, pvd, layout = detect_layout(bin_path)
    joliet = None
    try:
        from tools.stoneage_netpower_remote_iso_scan import find_joliet
        joliet_vd = find_joliet(img)
        rows = walk_full(img, joliet_vd, True) if joliet_vd is not None else walk_full(img, pvd, False)
        joliet = joliet_vd is not None
        return img, rows, layout, joliet
    except Exception:
        img.close()
        raise


def extract_row(img, row, out_path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("wb") as f:
        for chunk in img.iter_extent(row["lba"], row["size"]):
            f.write(chunk)


def hash_bytes(data):
    return (
        hashlib.md5(data).hexdigest(),
        hashlib.sha1(data).hexdigest(),
        hashlib.sha256(data).hexdigest(),
    )


def pe_sections(data):
    if len(data) < 0x40 or data[:2] != b"MZ":
        return None
    pe_off = struct.unpack_from("<I", data, 0x3C)[0]
    if pe_off + 24 > len(data) or data[pe_off:pe_off+4] != b"PE\x00\x00":
        return None
    machine, nsec, timestamp = struct.unpack_from("<HHI", data, pe_off + 4)
    opt_size = struct.unpack_from("<H", data, pe_off + 20)[0]
    opt_off = pe_off + 24
    entry = image_base = subsystem = 0
    if opt_off + opt_size <= len(data) and opt_size >= 70:
        magic = struct.unpack_from("<H", data, opt_off)[0]
        entry = struct.unpack_from("<I", data, opt_off + 16)[0]
        if magic == 0x10B and opt_size >= 70:
            image_base = struct.unpack_from("<I", data, opt_off + 28)[0]
            subsystem = struct.unpack_from("<H", data, opt_off + 68)[0]
    sec_off = opt_off + opt_size
    sections = []
    for idx in range(nsec):
        off = sec_off + idx * 40
        if off + 40 > len(data):
            break
        raw_name = data[off:off+8].split(b"\0", 1)[0]
        name = raw_name.decode("ascii", "replace")
        virtual_size, virtual_addr, raw_size, raw_ptr = struct.unpack_from("<IIII", data, off + 8)
        characteristics = struct.unpack_from("<I", data, off + 36)[0]
        raw = data[raw_ptr:raw_ptr+raw_size] if raw_ptr + raw_size <= len(data) else b""
        sections.append({
            "name": name,
            "virtual_size": virtual_size,
            "virtual_addr": virtual_addr,
            "raw_size": raw_size,
            "raw_ptr": raw_ptr,
            "characteristics": characteristics,
            "sha256": hashlib.sha256(raw).hexdigest(),
        })
    return {
        "machine": machine,
        "sections": sections,
        "timestamp": timestamp,
        "entry": entry,
        "image_base": image_base,
        "subsystem": subsystem,
    }


def ascii_strings(data, limit=500):
    seen = set()
    out = []
    for match in ASCII_RE.finditer(data):
        s = match.group().decode("ascii", "replace")
        if RELEVANT_STRING.search(s) and s not in seen:
            seen.add(s)
            out.append(s)
            if len(out) >= limit:
                break
    return out


def utf16_strings(data, limit=200):
    # Capture simple printable UTF-16LE runs without decoding arbitrary binary spans.
    pattern = re.compile(rb"(?:[\x20-\x7e]\x00){4,}")
    seen = set()
    out = []
    for match in pattern.finditer(data):
        try:
            s = match.group().decode("utf-16le")
        except UnicodeDecodeError:
            continue
        if RELEVANT_STRING.search(s) and s not in seen:
            seen.add(s)
            out.append(s)
            if len(out) >= limit:
                break
    return out


def objdump_imports(path):
    try:
        proc = subprocess.run(
            ["objdump", "-p", str(path)],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
        )
    except Exception as exc:
        return [], f"{type(exc).__name__}:{exc}"
    dlls = []
    funcs = []
    for line in proc.stdout.splitlines():
        s = line.strip()
        if s.startswith("DLL Name:"):
            dlls.append(s.split(":", 1)[1].strip())
        elif re.match(r"^[0-9a-fA-F]+\s+[0-9a-fA-F]+\s+\S+", s):
            parts = s.split()
            if len(parts) >= 3:
                funcs.append(parts[-1])
    return sorted(set(dlls)), "" if proc.returncode == 0 else f"returncode={proc.returncode}"


def print_exe(label, path):
    data = path.read_bytes()
    md5, sha1, sha256 = hash_bytes(data)
    pe = pe_sections(data)
    print(
        f"EXE|label={label}|name={path.name}|size={len(data)}|md5={md5}|sha1={sha1}|sha256={sha256}|"
        f"pe={int(pe is not None)}"
    )
    if pe:
        try:
            stamp = datetime.datetime.fromtimestamp(
                pe["timestamp"], datetime.timezone.utc
            ).isoformat()
        except Exception:
            stamp = ""
        print(
            f"PE|label={label}|machine={pe['machine']}|timestamp={pe['timestamp']}|"
            f"timestamp_utc={clean(stamp)}|entry=0x{pe['entry']:x}|"
            f"image_base=0x{pe['image_base']:x}|subsystem={pe['subsystem']}|"
            f"section_count={len(pe['sections'])}"
        )
        for sec in pe["sections"]:
            print(
                f"PE_SECTION|label={label}|name={clean(sec['name'])}|"
                f"vaddr=0x{sec['virtual_addr']:x}|vsize={sec['virtual_size']}|"
                f"raw_ptr={sec['raw_ptr']}|raw_size={sec['raw_size']}|"
                f"characteristics=0x{sec['characteristics']:08x}|sha256={sec['sha256']}"
            )
    dlls, err = objdump_imports(path)
    print(f"IMPORT_DLLS|label={label}|count={len(dlls)}|values={','.join(dlls)}|error={clean(err)}")
    for s in ascii_strings(data):
        print(f"STRING|label={label}|encoding=ascii|text={clean(s,2500)}")
    for s in utf16_strings(data):
        print(f"STRING|label={label}|encoding=utf16le|text={clean(s,2500)}")


def compare_exes(a, b):
    da = a.read_bytes()
    db = b.read_bytes()
    n = min(len(da), len(db))
    same = sum(1 for x, y in zip(da[:n], db[:n]) if x == y)
    prefix = 0
    for x, y in zip(da, db):
        if x != y:
            break
        prefix += 1
    suffix = 0
    for x, y in zip(reversed(da), reversed(db)):
        if x != y:
            break
        suffix += 1
    print(
        f"EXE_COMPARE|a={a.name}|b={b.name}|a_size={len(da)}|b_size={len(db)}|"
        f"common_prefix={prefix}|common_suffix={suffix}|"
        f"same_positions_minlen={same}|minlen={n}|same_ratio={same/max(1,n):.6f}"
    )
    pa = pe_sections(da)
    pb = pe_sections(db)
    if pa and pb:
        by_name_a = {s["name"]: s for s in pa["sections"]}
        by_name_b = {s["name"]: s for s in pb["sections"]}
        for name in sorted(set(by_name_a) | set(by_name_b)):
            sa = by_name_a.get(name)
            sb = by_name_b.get(name)
            print(
                f"EXE_SECTION_COMPARE|name={clean(name)}|"
                f"a_raw={sa['raw_size'] if sa else ''}|b_raw={sb['raw_size'] if sb else ''}|"
                f"a_sha256={sa['sha256'] if sa else ''}|b_sha256={sb['sha256'] if sb else ''}|"
                f"identical={int(bool(sa and sb and sa['sha256']==sb['sha256']))}"
            )


def emit_real_adrn(adrn, real):
    r = analyze_real_adrn(adrn, real)
    print("REAL_ADRN|generation=tw_v1")
    for key in (
        "adrn_size", "real_size", "record_size", "record_count", "remainder",
        "active_records", "duplicate_bitmap_numbers", "nondecreasing_active_offsets",
        "contiguous_active_offsets", "gap_transitions", "overlap_transitions",
        "max_referenced_end", "unreferenced_real_tail",
    ):
        print(f"REAL_ADRN_METRIC|{key}={r[key]}")
    for key in sorted(r["counts"]):
        print(f"REAL_ADRN_COUNT|{key}|{r['counts'][key]}")
    for key, value in sorted(r["flags"].items()):
        print(f"REAL_ADRN_FLAG|{key}|{value}")
    for row in r["samples"][:12]:
        print("REAL_ADRN_SAMPLE|" + "|".join(map(str, row)))
    for row in r["bad"][:12]:
        print("REAL_ADRN_BAD|" + "|".join(map(str, row)))


def emit_spr(spradrn, spr, adrn):
    r = analyze_spr(spradrn, spr, adrn)
    print(
        f"SPR|record_count={r['record_count']}|remainder={r['remainder']}|"
        f"spr_bytes={r['spr_bytes']}|sprno_min={r['sprno_min']}|sprno_max={r['sprno_max']}|"
        f"animation_total={r['animation_total']}|frame_total={r['frame_total']}|"
        f"parse_success={r['counts'].get('parse_success',0)}|"
        f"parse_failure={r['counts'].get('parse_failure',0)}|"
        f"aggregate={r['aggregate']}"
    )
    for key, value in sorted(r["counts"].items()):
        print(f"SPR_COUNT|{key}|{value}")
    for key, value in sorted(r["bitmap_classes"].items()):
        print(f"SPR_BITMAP_CLASS|{key}|{value}")
    for key, value in sorted(r["sound_classes"].items()):
        print(f"SPR_SOUND_CLASS|{key}|{value}")
    for row in r["samples"][:12]:
        print("SPR_SAMPLE|" + "|".join(map(str, row)))
    for row in r["failures"][:20]:
        print("SPR_FAILURE|" + "|".join(map(str, row)))


def parse_addr_table(path):
    text = path.read_text("utf-8", errors="replace")
    rows = []
    for token in text.split():
        parts = token.split(":", 2)
        if len(parts) != 3:
            continue
        try:
            offset = int(parts[0])
            size = int(parts[1])
        except ValueError:
            continue
        rows.append((offset, size, parts[2]))
    return rows


def validate_concat(label, table_path, container_path, extracted_root):
    rows = parse_addr_table(table_path)
    blob = container_path.read_bytes()
    ok_bounds = 0
    exact_individual = 0
    missing_individual = 0
    mismatch_individual = 0
    gaps = 0
    overlaps = 0
    prev_end = None
    basename_map = collections.defaultdict(list)
    for p in extracted_root.rglob("*"):
        if p.is_file():
            basename_map[p.name.lower()].append(p)

    for offset, size, name in rows:
        if 0 <= offset <= len(blob) and offset + size <= len(blob):
            ok_bounds += 1
        if prev_end is not None:
            if offset > prev_end:
                gaps += 1
            elif offset < prev_end:
                overlaps += 1
        prev_end = offset + size
        candidates = basename_map.get(Path(name).name.lower(), [])
        if not candidates:
            missing_individual += 1
            continue
        segment = blob[offset:offset+size]
        matched = False
        for candidate in candidates:
            try:
                if candidate.read_bytes() == segment:
                    matched = True
                    break
            except Exception:
                pass
        if matched:
            exact_individual += 1
        else:
            mismatch_individual += 1

    max_end = max((o+s for o,s,_ in rows), default=0)
    print(
        f"CONCAT|label={label}|records={len(rows)}|container_bytes={len(blob)}|"
        f"in_bounds={ok_bounds}|max_end={max_end}|tail={max(0,len(blob)-max_end)}|"
        f"gaps={gaps}|overlaps={overlaps}|exact_individual={exact_individual}|"
        f"missing_individual={missing_individual}|mismatch_individual={mismatch_individual}"
    )
    for row in rows[:20]:
        print(f"CONCAT_SAMPLE|label={label}|offset={row[0]}|size={row[1]}|name={clean(row[2])}")


def cab_list(label, path):
    try:
        proc = subprocess.run(
            ["7z", "l", "-slt", str(path)],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
        )
    except Exception as exc:
        print(f"CAB_ERROR|label={label}|kind={type(exc).__name__}|message={clean(exc)}")
        return
    relevant=[]
    for line in proc.stdout.splitlines():
        s=line.strip()
        if s.startswith(("Path = ","Size = ","Packed Size = ","Method = ","Files = ","Folders = ")):
            relevant.append(s)
    print(f"CAB|label={label}|returncode={proc.returncode}|lines={len(relevant)}")
    for s in relevant[:120]:
        print(f"CAB_META|label={label}|text={clean(s,1800)}")


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--bin", required=True)
    args=ap.parse_args()

    print("StoneAge Taiwan v1.0 technical reverse-engineering probe — R1")
    print("SCOPE|ephemeral-clean-disc|derived-structure-only|no-payload-commit")

    img, rows, layout, joliet = find_rows(args.bin)
    temp = tempfile.TemporaryDirectory()
    root=Path(temp.name)
    try:
        by_path={row["path"]:row for row in rows if not row["is_dir"]}
        print(f"FILESYSTEM|layout={layout}|joliet={int(joliet)}|entries={len(rows)}")
        missing=[]
        for target in TARGET_PATHS:
            row=by_path.get(target)
            if row is None:
                missing.append(target)
                print(f"TARGET_MISSING|path={clean(target)}")
                continue
            out=root/target
            extract_row(img,row,out)
            print(f"TARGET_EXTRACTED|path={clean(target)}|size={row['size']}")
        # Extract individual battle/sound members for direct concat validation.
        for row in rows:
            p=row["path"]
            if row["is_dir"]:
                continue
            if p.startswith("StoneAge/data/battlemap/") or p.startswith("StoneAge/data/se/") or p.startswith("StoneAge/data/pal/"):
                extract_row(img,row,root/p)
        print(f"COUNT|missing_targets|{len(missing)}")

        exe_a=root/"StoneAge/StoneAge.exe"
        exe_b=root/"StoneAge/sa_3.exe"
        if exe_a.exists():
            print_exe("StoneAge.exe",exe_a)
        if exe_b.exists():
            print_exe("sa_3.exe",exe_b)
        if exe_a.exists() and exe_b.exists():
            compare_exes(exe_a,exe_b)

        setup_inx=root/"StoneAge/setup.inx"
        if setup_inx.exists():
            data=setup_inx.read_bytes()
            print(f"SETUP_INX|size={len(data)}|sha256={hashlib.sha256(data).hexdigest()}")
            for s in ascii_strings(data,300):
                print(f"SETUP_STRING|encoding=ascii|text={clean(s,2500)}")
            for s in utf16_strings(data,150):
                print(f"SETUP_STRING|encoding=utf16le|text={clean(s,2500)}")

        data1=root/"StoneAge/data1.cab"
        if data1.exists():
            cab_list("StoneAge/data1.cab",data1)

        real=root/"StoneAge/data/real_1.bin"
        adrn=root/"StoneAge/data/adrn_1.bin"
        spr=root/"StoneAge/data/spr_1.bin"
        spradrn=root/"StoneAge/data/spradrn_1.bin"
        if real.exists() and adrn.exists():
            emit_real_adrn(adrn,real)
        if spr.exists() and spradrn.exists() and adrn.exists():
            emit_spr(spradrn,spr,adrn)

        battletxt=root/"StoneAge/data/battletxt_1.txt"
        battle=root/"StoneAge/data/battle_1.bin"
        if battletxt.exists() and battle.exists():
            validate_concat("battle",battletxt,battle,root)

        soundtxt=root/"StoneAge/data/soundaddr_1.txt"
        sound=root/"StoneAge/data/sound_1.bin"
        if soundtxt.exists() and sound.exists():
            validate_concat("sound",soundtxt,sound,root)
    finally:
        img.close()
        temp.cleanup()


if __name__=="__main__":
    main()
