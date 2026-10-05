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


def classify_vary_profile(
    *,
    symbol_present: bool,
    strstr_calls: int,
) -> str:
    if not symbol_present:
        return "inconclusive_symbol_unavailable"
    if strstr_calls == 2:
        return "gavin_iris_attack_quick"
    if strstr_calls == 3:
        return "bismarck_attack_defense_quick"
    return "inconclusive_call_shape"


def analyze(binary: Path) -> list[str]:
    binary = Path(binary)
    data = binary.read_bytes()
    sha256 = hashlib.sha256(data).hexdigest()
    file_desc = _run(["file", "-b", str(binary)]).strip().replace("|", "/")
    nm = _run(["nm", "-a", str(binary)])
    symbol_present = bool(
        re.search(r"(^|\s)PETSKILL_Vary($|\s)", nm, re.MULTILINE)
    )
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
        "StoneAge recovered25 PETSKILL_Vary executable-profile probe — R1",
        "Derived facts only; no executable bytes/source text stored.",
        f"EXECUTABLE|size={len(data)}|sha256={sha256}",
        f"FORMAT|file={file_desc or 'unknown'}",
        f"SYMBOL|name=PETSKILL_Vary|present={1 if symbol_present else 0}",
        f"DISASM|petskill_vary_strstr_calls={calls}",
    ]
    for value in VARY_CONSTANTS:
        rows.append(
            f"U32LE|value={value}|count={_little_u32_count(data, value)}"
        )
    rows.extend(
        [
            f"PROFILE_SIGNAL|vary_option_parser={profile}",
            "BOUNDARY|animation_profile_not_selected_by_this_probe=1",
            "BOUNDARY|compiler_inlining_stripping_or_unrelated_constants=cannot_be_normalized_into_profile_truth",
            "RESOLUTION|VARY_EXECUTABLE_PROFILE_DISCRIMINATOR_ATTEMPTED",
        ]
    )
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--binary", required=True, type=Path)
    args = parser.parse_args()
    if not args.binary.is_file():
        raise SystemExit("recovered gmsv binary not found")
    print("\n".join(analyze(args.binary)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
