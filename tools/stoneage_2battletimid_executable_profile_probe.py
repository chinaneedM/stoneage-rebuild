#!/usr/bin/env python3
"""Bounded 2BattleTimid preserved-executable charset discriminator.

Callback and post-damage parser symbols are prerequisite identities.
Presence of an unrelated UTF-8/Big5 string cannot select their literal charset.
This bounded symbol assay therefore reports its evidence limit explicitly.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re
import subprocess


SYMBOLS=("PETSKILL_2BattleTimid","BATTLE_S_AttackDamage")


def _run(argv: list[str]) -> str:
    try:
        proc=subprocess.run(
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


def _has_symbol(path: Path, symbol: str) -> bool:
    return bool(re.search(
        rf"(^|\s){re.escape(symbol)}($|\s)",
        _run(["nm","-a",str(path)]),
        re.MULTILINE,
    ))


def classify_2battletimid_profile(
    *,
    petskill_symbol_present: bool,
    attackdamage_symbol_present: bool,
) -> str:
    if not attackdamage_symbol_present:
        return "inconclusive_attackdamage_symbol_unavailable"
    if not petskill_symbol_present:
        return "inconclusive_callback_symbol_unavailable"
    # Function symbols alone do not establish which literal addresses reach
    # these parsers. No global string count or encoding majority chooses a build.
    return "inconclusive_no_callback_local_literal_identity"


def analyze_search_root(root: Path) -> list[str]:
    root=Path(root)
    elf_candidates=[]
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        try:
            with path.open("rb") as handle:
                magic=handle.read(4)
        except OSError:
            continue
        if magic==b"\x7fELF":
            elf_candidates.append(path)

    rows=[
        "StoneAge recovered25 PETSKILL_2BattleTimid executable-profile probe — R1",
        "Derived facts only; no executable bytes/source text stored.",
        f"SCAN|elf_candidates={len(elf_candidates)}",
    ]
    carriers=[]
    for index,path in enumerate(elf_candidates):
        data=path.read_bytes()
        flags={symbol:_has_symbol(path,symbol) for symbol in SYMBOLS}
        if any(flags.values()):
            carriers.append((path,flags))
        rows.append(
            "ELF_CANDIDATE|"
            f"index={index}|size={len(data)}|"
            f"sha256={hashlib.sha256(data).hexdigest()}|"
            f"petskill_2battletimid_symbol={int(flags['PETSKILL_2BattleTimid'])}|"
            f"attackdamage_symbol={int(flags['BATTLE_S_AttackDamage'])}"
        )

    if len(carriers)==1:
        path,flags=carriers[0]
        profile=classify_2battletimid_profile(
            petskill_symbol_present=flags["PETSKILL_2BattleTimid"],
            attackdamage_symbol_present=flags["BATTLE_S_AttackDamage"],
        )
        rows.extend([
            f"SYMBOL|name=PETSKILL_2BattleTimid|present={int(flags['PETSKILL_2BattleTimid'])}",
            f"SYMBOL|name=BATTLE_S_AttackDamage|present={int(flags['BATTLE_S_AttackDamage'])}",
            f"PROFILE_SIGNAL|literal_charset={profile}",
        ])
    elif len(carriers)==0:
        rows.extend([
            "SYMBOL|name=PETSKILL_2BattleTimid|present=0",
            "SYMBOL|name=BATTLE_S_AttackDamage|present=0",
            "PROFILE_SIGNAL|literal_charset=inconclusive_attackdamage_symbol_unavailable",
        ])
    else:
        rows.append(
            "PROFILE_SIGNAL|literal_charset="
            "inconclusive_multiple_symbol_carriers"
        )

    rows.extend([
        "BOUNDARY|utf8_vs_big5_not_selected_without_unique_dataflow_identity=1",
        "BOUNDARY|global_string_encoding_and_unlinked_literals_not_promoted_to_profile_truth=1",
        "RESOLUTION|2BATTLETIMID_EXECUTABLE_PROFILE_DISCRIMINATOR_ATTEMPTED",
    ])
    return rows


def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--search-root",type=Path,required=True)
    args=parser.parse_args()
    if not args.search_root.is_dir():
        raise SystemExit("recovered service root not found")
    print("\n".join(analyze_search_root(args.search_root)))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
