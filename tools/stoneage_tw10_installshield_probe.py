#!/usr/bin/env python3
"""Probe the Taiwan v1.0 InstallShield payload and installed-file clues.

Uses an ephemeral verified raw CD image. Extracts InstallShield control files from the
disc, invokes unshield when possible, and emits only derived inventory/hashes/strings.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re
import subprocess
import tempfile

from tools.stoneage_tw10_technical_probe import find_rows, extract_row

INSTALL_TARGETS=(
    "StoneAge/data1.cab",
    "StoneAge/data1.hdr",
    "StoneAge/data2.cab",
    "StoneAge/layout.bin",
    "StoneAge/setup.inx",
    "StoneAge/Setup.exe",
    "StoneAge/Setup.ini",
)
MAP_RE=re.compile(r"(?i)(?:^|[/\\])map(?:[/\\]|$)|\.(?:map|dat)$")
STONE_RE=re.compile(r"(?i)(stoneage|sa_[0-9]+\.exe|real_[0-9]+\.bin|adrn_[0-9]+\.bin|spr_[0-9]+\.bin|battle)")
PRINTABLE=re.compile(rb"[\x20-\x7e]{5,}")


def clean(v,limit=1800):
    s=" ".join(str(v if v is not None else "").split())
    return "".join(ch for ch in s if ch>=" " and ch!="\x7f").replace("|","%7C")[:limit]


def digest(path:Path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):
            h.update(b)
    return h.hexdigest()


def run_unshield(cab:Path, out:Path):
    listed=subprocess.run(
        ["unshield","l",str(cab)],
        stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
        text=True,encoding="utf-8",errors="replace",timeout=60,check=False
    )
    extracted=subprocess.run(
        ["unshield","-d",str(out),"x",str(cab)],
        stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
        text=True,encoding="utf-8",errors="replace",timeout=120,check=False
    )
    return listed,extracted


def interesting_strings(path:Path):
    data=path.read_bytes()
    seen=set()
    for m in PRINTABLE.finditer(data):
        s=m.group().decode("ascii","replace")
        if (MAP_RE.search(s) or STONE_RE.search(s) or "waei" in s.lower() or "install" in s.lower()) and s not in seen:
            seen.add(s); yield s


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--bin",required=True)
    args=ap.parse_args()

    print("StoneAge Taiwan v1.0 InstallShield probe — R1")
    print("SCOPE|ephemeral-verified-disc|derived-installer-inventory-only|no-payload-commit")
    img,rows,layout,joliet=find_rows(args.bin)
    tmp=tempfile.TemporaryDirectory()
    root=Path(tmp.name)
    try:
        by={r["path"]:r for r in rows if not r["is_dir"]}
        print(f"FILESYSTEM|layout={layout}|joliet={int(joliet)}|entries={len(rows)}")
        missing=0
        for target in INSTALL_TARGETS:
            row=by.get(target)
            if not row:
                missing+=1; print(f"TARGET_MISSING|path={clean(target)}"); continue
            p=root/target
            extract_row(img,row,p)
            print(f"TARGET|path={clean(target)}|size={p.stat().st_size}|sha256={digest(p)}")
        print(f"COUNT|missing_targets|{missing}")

        for name in ("setup.inx","Setup.exe","Setup.ini"):
            p=root/"StoneAge"/name
            if not p.exists(): continue
            hits=list(interesting_strings(p))
            print(f"STRING_COUNT|path=StoneAge/{name}|hits={len(hits)}")
            for s in hits[:200]:
                print(f"STRING|path=StoneAge/{name}|text={clean(s)}")

        cab=root/"StoneAge/data1.cab"
        out=root/"unshield"
        if cab.exists():
            out.mkdir(parents=True,exist_ok=True)
            listed,extracted=run_unshield(cab,out)
            print(f"UNSHIELD|list_rc={listed.returncode}|extract_rc={extracted.returncode}")
            for line in listed.stdout.splitlines()[:300]:
                if line.strip():
                    print(f"UNSHIELD_LIST|text={clean(line)}")
            files=sorted(p for p in out.rglob("*") if p.is_file())
            print(f"COUNT|unshield_files|{len(files)}")
            print(f"COUNT|unshield_bytes|{sum(p.stat().st_size for p in files)}")
            map_count=0
            for p in files:
                rel=str(p.relative_to(out)).replace("\\","/")
                ismap=bool(MAP_RE.search(rel))
                if ismap: map_count+=1
                print(
                    f"INSTALLED_FILE|path={clean(rel)}|size={p.stat().st_size}|"
                    f"sha256={digest(p)}|map_like={int(ismap)}"
                )
            print(f"COUNT|map_like_installed_files|{map_count}")
            if extracted.returncode!=0:
                for line in extracted.stdout.splitlines()[-80:]:
                    if line.strip():
                        print(f"UNSHIELD_ERROR|text={clean(line)}")
    finally:
        img.close(); tmp.cleanup()


if __name__=="__main__":
    main()
