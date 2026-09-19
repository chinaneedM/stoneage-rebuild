#!/usr/bin/env python3
"""Deep derived-only runtime probe for accepted Taiwan StoneAge v1.0.

Emits import-function inventories, bounded string cross-references, runtime/updater
role signals, and exact diagnostics for sound_1.bin address-table mismatches.
Consumes only an ephemeral verified raw disc image; no payload bytes are committed.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re
import struct
import subprocess
import tempfile

from tools.stoneage_tw10_technical_probe import (
    find_rows,
    extract_row,
    pe_sections,
    parse_addr_table,
)

TARGETS = (
    "StoneAge/StoneAge.exe",
    "StoneAge/sa_3.exe",
    "StoneAge/data/sound_1.bin",
    "StoneAge/data/soundaddr_1.txt",
)

UPDATER_STRINGS = (
    b"/saupdate/newest.txt",
    b"/saupdate/%s",
    b"stoneage.waei.net",
    b"data\\real_*.bin",
    b"data\\adrn_*.bin",
    b"data\\spr_*.bin",
    b"updated",
)

RUNTIME_STRINGS = (
    b"ClientLogin",
    b"CharLogin",
    b"PPASSWORD",
    b"yStoneAge.exe",
    b"data\\real_%d.bin",
    b"data\\adrn_%d.bin",
    b"data\\spr_%d.bin",
    b"map\\%d.dat",
    b"wgs@mail.hwaei.com.tw",
)

LAUNCH_APIS = {
    "CreateProcessA", "CreateProcessW", "WinExec", "ShellExecuteA", "ShellExecuteW",
    "ShellExecuteExA", "ShellExecuteExW", "system", "_spawnl", "_spawnv",
}
NETWORK_APIS = {
    "WSAStartup", "socket", "connect", "send", "recv", "closesocket",
    "gethostbyname", "inet_addr", "htons", "select",
}
HTTP_APIS = {
    "InternetOpenA", "InternetOpenW", "InternetConnectA", "InternetConnectW",
    "HttpOpenRequestA", "HttpOpenRequestW", "HttpSendRequestA", "HttpSendRequestW",
    "HttpQueryInfoA", "HttpQueryInfoW", "InternetReadFile",
}


def clean(value, limit=1600):
    text = " ".join(str(value if value is not None else "").split())
    return "".join(ch for ch in text if ch >= " " and ch != "\x7f").replace("|", "%7C")[:limit]


def objdump_imports(path: Path):
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
    dll = ""
    result = []
    in_import_table = False
    for raw in proc.stdout.splitlines():
        line = raw.strip()
        if "The Import Tables" in line:
            in_import_table = True
            continue
        if not in_import_table:
            continue
        if line.startswith("The Export Tables") or line.startswith("PE File Base Relocations"):
            break
        if line.startswith("DLL Name:"):
            dll = line.split(":", 1)[1].strip()
            continue
        if not dll or not line:
            continue
        # Binutils PE import rows normally end with the imported member name.
        # Examples vary across versions, so accept a leading hex/ordinal field and
        # a final identifier while rejecting table headings.
        parts = line.split()
        if len(parts) < 2:
            continue
        if parts[-1] in {"Bound-To", "Member-Name"}:
            continue
        if not re.fullmatch(r"[A-Za-z_?@][A-Za-z0-9_?@$.-]*", parts[-1]):
            continue
        if not any(re.fullmatch(r"(?:0x)?[0-9A-Fa-f]+", p) for p in parts[:-1]):
            continue
        result.append((dll, parts[-1]))
    return proc.returncode, sorted(set(result))


def rva_from_file_offset(pe, file_offset):
    for sec in pe["sections"]:
        start = sec["raw_ptr"]
        end = start + sec["raw_size"]
        if start <= file_offset < end:
            return sec["virtual_addr"] + (file_offset - start), sec["name"]
    return None, ""


def text_section(pe, data):
    for sec in pe["sections"]:
        if sec["name"] == ".text":
            raw = data[sec["raw_ptr"]:sec["raw_ptr"] + sec["raw_size"]]
            return sec, raw
    return None, b""


def string_xrefs(label, data, needles):
    pe = pe_sections(data)
    if not pe:
        return
    text_sec, text = text_section(pe, data)
    for needle in needles:
        search = 0
        occurrences = []
        while True:
            pos = data.find(needle, search)
            if pos < 0:
                break
            rva, secname = rva_from_file_offset(pe, pos)
            occurrences.append((pos, rva, secname))
            search = pos + 1
        print(
            f"STRING_LOC|label={label}|text={clean(needle.decode('ascii','replace'))}|"
            f"occurrences={len(occurrences)}"
        )
        for pos, rva, secname in occurrences[:12]:
            if rva is None:
                print(
                    f"STRING_OCCURRENCE|label={label}|file_offset=0x{pos:x}|rva=|"
                    f"section={clean(secname)}|xrefs=0"
                )
                continue
            va = pe["image_base"] + rva
            ptr = struct.pack("<I", va)
            xrefs = []
            off = 0
            while True:
                hit = text.find(ptr, off)
                if hit < 0:
                    break
                xrefs.append(text_sec["virtual_addr"] + hit)
                off = hit + 1
            print(
                f"STRING_OCCURRENCE|label={label}|file_offset=0x{pos:x}|rva=0x{rva:x}|"
                f"va=0x{va:x}|section={clean(secname)}|xrefs={len(xrefs)}|"
                f"xref_rvas={','.join(f'0x{x:x}' for x in xrefs[:20])}"
            )


def emit_imports(label, path):
    rc, imports = objdump_imports(path)
    dlls = sorted({dll for dll, _ in imports})
    funcs = sorted({func for _, func in imports})
    print(
        f"IMPORTS|label={label}|returncode={rc}|dlls={len(dlls)}|functions={len(funcs)}|"
        f"dll_values={','.join(dlls)}"
    )
    for dll in dlls:
        members = sorted(func for d, func in imports if d == dll)
        print(
            f"IMPORT_DLL|label={label}|dll={clean(dll)}|count={len(members)}|"
            f"functions={','.join(members)}"
        )
    launch = sorted(set(funcs) & LAUNCH_APIS)
    network = sorted(set(funcs) & NETWORK_APIS)
    http = sorted(set(funcs) & HTTP_APIS)
    print(f"ROLE_SIGNAL|label={label}|kind=launch_api|values={','.join(launch)}")
    print(f"ROLE_SIGNAL|label={label}|kind=network_api|values={','.join(network)}")
    print(f"ROLE_SIGNAL|label={label}|kind=http_api|values={','.join(http)}")


def first_diff(a: bytes, b: bytes):
    n = min(len(a), len(b))
    for i in range(n):
        if a[i] != b[i]:
            return i
    if len(a) != len(b):
        return n
    return -1


def emit_sound_mismatches(root: Path):
    table = parse_addr_table(root / "StoneAge/data/soundaddr_1.txt")
    blob = (root / "StoneAge/data/sound_1.bin").read_bytes()
    se_root = root / "StoneAge/data/se"
    exact = 0
    mismatch = 0
    missing = 0
    for offset, size, name in table:
        path = se_root / Path(name).name
        if not path.exists():
            missing += 1
            print(
                f"SOUND_COMPARE|name={clean(name)}|status=missing|offset={offset}|"
                f"table_size={size}"
            )
            continue
        individual = path.read_bytes()
        segment = blob[offset:offset+size]
        if individual == segment:
            exact += 1
            continue
        mismatch += 1
        diff = first_diff(segment, individual)
        same_prefix = diff if diff >= 0 else min(len(segment), len(individual))
        print(
            f"SOUND_COMPARE|name={clean(name)}|status=mismatch|offset={offset}|"
            f"table_size={size}|individual_size={len(individual)}|first_diff={diff}|"
            f"same_prefix={same_prefix}|segment_sha1={hashlib.sha1(segment).hexdigest()}|"
            f"individual_sha1={hashlib.sha1(individual).hexdigest()}"
        )
    print(
        f"SOUND_SUMMARY|records={len(table)}|exact={exact}|mismatch={mismatch}|missing={missing}|"
        f"container_size={len(blob)}"
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bin", required=True)
    args = ap.parse_args()

    print("StoneAge Taiwan v1.0 deep runtime probe — R1")
    print("SCOPE|ephemeral-clean-disc|derived-import-xref-and-sound-diagnostics|no-payload-commit")

    img, rows, layout, joliet = find_rows(args.bin)
    tmp = tempfile.TemporaryDirectory()
    root = Path(tmp.name)
    try:
        by_path = {r["path"]: r for r in rows if not r["is_dir"]}
        print(f"FILESYSTEM|layout={layout}|joliet={int(joliet)}|entries={len(rows)}")
        for target in TARGETS:
            row = by_path.get(target)
            if row is None:
                print(f"TARGET_MISSING|path={clean(target)}")
                continue
            extract_row(img, row, root / target)
            print(f"TARGET_EXTRACTED|path={clean(target)}|size={row['size']}")
        for row in rows:
            if not row["is_dir"] and row["path"].startswith("StoneAge/data/se/"):
                extract_row(img, row, root / row["path"])

        updater = root / "StoneAge/StoneAge.exe"
        runtime = root / "StoneAge/sa_3.exe"
        if updater.exists():
            emit_imports("StoneAge.exe", updater)
            string_xrefs("StoneAge.exe", updater.read_bytes(), UPDATER_STRINGS)
        if runtime.exists():
            emit_imports("sa_3.exe", runtime)
            string_xrefs("sa_3.exe", runtime.read_bytes(), RUNTIME_STRINGS)
        if (root / "StoneAge/data/sound_1.bin").exists() and (root / "StoneAge/data/soundaddr_1.txt").exists():
            emit_sound_mismatches(root)
    finally:
        img.close()
        tmp.cleanup()


if __name__ == "__main__":
    main()
