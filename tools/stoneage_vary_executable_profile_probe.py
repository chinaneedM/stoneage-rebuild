#!/usr/bin/env python3
"""Bounded recovered25 PETSKILL_Vary executable-profile discriminator."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re
import struct
import subprocess


VARY_CONSTANTS = (600, 981, 982, 983, 984, 101428, 101120)


def _run(argv: list[str]) -> str:
    try:
        proc = subprocess.run(
            argv,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except FileNotFoundError:
        return ""
    return proc.stdout or ""


def _little_u32_count(data: bytes, value: int) -> int:
    return data.count(struct.pack("<I", int(value)))


def _strstr_calls(disassembly: str) -> int:
    return sum(
        1
        for line in disassembly.splitlines()
        if re.search(r"\bcall\w*\b.*\bstrstr(?:@plt)?\b", line)
    )


def _has_vary_symbol(path: Path) -> bool:
    nm = _run(["nm", "-a", str(path)])
    return bool(re.search(r"(^|\s)PETSKILL_Vary($|\s)", nm, re.MULTILINE))


def classify_vary_profile(*, symbol_present: bool, strstr_calls: int) -> str:
    if not symbol_present:
        return "inconclusive_symbol_unavailable"
    if strstr_calls == 2:
        return "gavin_iris_attack_quick"
    if strstr_calls == 3:
        return "bismarck_attack_defense_quick"
    return "inconclusive_call_shape"


def _binary_rows(binary: Path) -> list[str]:
    data = binary.read_bytes()
    sha256 = hashlib.sha256(data).hexdigest()
    file_desc = _run(["file", "-b", str(binary)]).strip().replace("|", "/")
    symbol_present = _has_vary_symbol(binary)
    disassembly = ""
    if symbol_present:
        disassembly = _run(
            [
                "objdump",
                "-d",
                "-Mintel",
                "--disassemble=PETSKILL_Vary",
                str(binary),
            ]
        )
    calls = _strstr_calls(disassembly)
    profile = classify_vary_profile(
        symbol_present=symbol_present,
        strstr_calls=calls,
    )
    rows = [
        f"EXECUTABLE|size={len(data)}|sha256={sha256}",
        f"FORMAT|file={file_desc or 'unknown'}",
        f"SYMBOL|name=PETSKILL_Vary|present={1 if symbol_present else 0}",
        f"DISASM|petskill_vary_strstr_calls={calls}",
    ]
    for value in VARY_CONSTANTS:
        rows.append(
            f"U32LE|value={value}|count={_little_u32_count(data, value)}"
        )
    rows.append(f"PROFILE_SIGNAL|vary_option_parser={profile}")
    return rows


def analyze_search_root(root: Path) -> list[str]:
    root = Path(root)
    elf_candidates: list[Path] = []
    symbol_candidates: list[Path] = []
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        try:
            with path.open("rb") as handle:
                magic = handle.read(4)
        except OSError:
            continue
        if magic != b"\x7fELF":
            continue
        elf_candidates.append(path)
        if _has_vary_symbol(path):
            symbol_candidates.append(path)

    rows = [
        "StoneAge recovered25 PETSKILL_Vary executable-profile probe — R1",
        "Derived facts only; no executable bytes/source text stored.",
        f"SCAN|elf_candidates={len(elf_candidates)}|vary_symbol_carriers={len(symbol_candidates)}",
    ]
    for index, path in enumerate(elf_candidates):
        data = path.read_bytes()
        rows.append(
            "ELF_CANDIDATE|index="
            f"{index}|size={len(data)}|sha256={hashlib.sha256(data).hexdigest()}"
            f"|vary_symbol={1 if path in symbol_candidates else 0}"
        )

    if len(symbol_candidates) == 1:
        rows.extend(_binary_rows(symbol_candidates[0]))
    elif len(symbol_candidates) == 0:
        rows.extend(
            [
                "SYMBOL|name=PETSKILL_Vary|present=0",
                "DISASM|petskill_vary_strstr_calls=0",
                "PROFILE_SIGNAL|vary_option_parser=inconclusive_symbol_unavailable",
            ]
        )
    else:
        rows.extend(
            [
                "SYMBOL|name=PETSKILL_Vary|present=1",
                "DISASM|petskill_vary_strstr_calls=0",
                "PROFILE_SIGNAL|vary_option_parser=inconclusive_multiple_symbol_carriers",
            ]
        )

    rows.extend(
        [
            "BOUNDARY|animation_profile_not_selected_by_this_probe=1",
            "BOUNDARY|compiler_inlining_stripping_or_unrelated_constants=cannot_be_normalized_into_profile_truth",
            "RESOLUTION|VARY_EXECUTABLE_PROFILE_DISCRIMINATOR_ATTEMPTED",
        ]
    )
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--binary", type=Path)
    group.add_argument("--search-root", type=Path)
    args = parser.parse_args()
    if args.binary is not None:
        if not args.binary.is_file():
            raise SystemExit("recovered executable not found")
        rows = [
            "StoneAge recovered25 PETSKILL_Vary executable-profile probe — R1",
            "Derived facts only; no executable bytes/source text stored.",
            *_binary_rows(args.binary),
            "BOUNDARY|animation_profile_not_selected_by_this_probe=1",
            "BOUNDARY|compiler_inlining_stripping_or_unrelated_constants=cannot_be_normalized_into_profile_truth",
            "RESOLUTION|VARY_EXECUTABLE_PROFILE_DISCRIMINATOR_ATTEMPTED",
        ]
    else:
        if not args.search_root.is_dir():
            raise SystemExit("recovered service root not found")
        rows = analyze_search_root(args.search_root)
    print("\n".join(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
