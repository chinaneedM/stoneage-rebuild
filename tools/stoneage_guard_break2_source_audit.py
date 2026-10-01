#!/usr/bin/env python3
"""Reproduce GuardBreak2 semantics from three pinned source profiles.

Only hashes, enum values, and semantic booleans are emitted. Original source
text is never copied into the reconstruction repository.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re
import subprocess
import tempfile

from tools.stoneage_guard_break2_model import (
    CALLBACK_NAME,
    COMMAND_NAME,
    FEATURE_NAME,
    SOURCE_PETSKILL_SYMBOL_NAME,
)

PINNED = {
    "gavin": "1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56",
    "iris": "9e6c8ce2cd8ed532a7157773acd1c61582c178b5",
    "bismarck": "999ffdf1d220ec6666eb65339180689c9caf1876",
}
LAYOUTS = {
    "gavin": Path("gmsv/src"),
    "iris": Path("Source/gmsv"),
    "bismarck": Path("server/gmsv"),
}


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _text(path: Path) -> str:
    return path.read_bytes().decode("utf-8", "replace")


def _compact(text: str) -> str:
    return re.sub(r"\s+", "", text)


def _function(text: str, signature: str) -> str:
    """Return the first definition, skipping earlier C prototypes."""
    search_from = 0
    while True:
        start = text.find(signature, search_from)
        if start < 0:
            raise ValueError(f"missing function definition: {signature}")
        brace = text.find("{", start)
        semicolon = text.find(";", start)
        if brace >= 0 and (semicolon < 0 or brace < semicolon):
            break
        search_from = start + len(signature)

    depth = 0
    for index in range(brace, len(text)):
        char = text[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[start:index + 1]
    raise ValueError(f"unterminated function: {signature}")


def _git_head(root: Path) -> str:
    return subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        text=True,
    ).strip()


def _enum_probe(base: Path) -> tuple[int, int, int]:
    code = r"""
    #include <stdio.h>
    #include "battle.h"
    #include "pet_skillinfo.h"
    int main(void) {
      printf("%d %d %d\n",
        BATTLE_COM_S_GBREAK2,
        PETSKILL_GUARDBREAK2,
        PETSKILL_SACRIFICE);
      return 0;
    }
    """
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        src = root / "probe.c"
        exe = root / "probe"
        src.write_text(code)
        subprocess.run(
            [
                "cc", "-std=c99", "-O0",
                "-I", str(base),
                "-I", str(base / "include"),
                "-I", str(base / "common"),
                "-I", str(base / "lua"),
                str(src), "-o", str(exe),
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out = subprocess.check_output([str(exe)], text=True).strip()
    values = tuple(map(int, out.split()))
    if len(values) != 3:
        raise ValueError("unexpected GuardBreak2 enum probe output")
    return values


def analyze_profile(name: str, root: Path):
    expected = PINNED[name]
    actual = _git_head(root)
    if actual != expected:
        raise ValueError(f"{name} source HEAD drift: {actual} != {expected}")
    base = root / LAYOUTS[name]
    paths = {
        "pet_skill": base / "battle/pet_skill.c",
        "battle": base / "battle/battle.c",
        "battle_event": base / "battle/battle_event.c",
        "version": base / "include/version.h",
        "battle_h": base / "include/battle.h",
        "petskill_h": base / "include/pet_skillinfo.h",
    }
    data = {key: _text(path) for key, path in paths.items()}

    feature_active = bool(re.search(
        rf"^\s*#\s*define\s+{re.escape(FEATURE_NAME)}\b",
        data["version"],
        re.MULTILINE,
    ))

    pet_fn = _function(data["pet_skill"], f"int {CALLBACK_NAME}")
    pet_compact = _compact(pet_fn)
    callback_command = (
        "CHAR_WORKBATTLECOM1" in pet_compact
        and COMMAND_NAME in pet_compact
    )
    callback_target = (
        "CHAR_WORKBATTLECOM2" in pet_compact
        and ("toNo" in pet_fn or "toindex" in pet_fn)
    )
    callback_ignores_option = (
        "PETSKILL_getChar" not in pet_fn
        and "CHAR_WORKBATTLECOM3" not in pet_fn
    )

    battle_compact = _compact(data["battle"])
    case = battle_compact.find(f"case{COMMAND_NAME}:")
    next_window = battle_compact[case:case + 1000] if case >= 0 else ""
    dispatch_target_adjust = (
        case >= 0
        and "BATTLE_TargetAdjust(" in next_window
        and "BATTLE_S_GBreak2(" in next_window
    )

    attack_fn = _compact(_function(data["battle_event"], "static int BATTLE_AttackSeq"))
    branch = attack_fn.find(f"if(opt=={COMMAND_NAME})")
    one_three = attack_fn.find("(*pDamage)=(*pDamage)*1.3", branch)
    zero_seven = attack_fn.find("(*pDamage)=(*pDamage)*0.7", branch)
    guard_adjust = attack_fn.find("BATTLE_GuardAdjust((*pDamage))", branch)
    guard_multiplier_order = (
        branch >= 0
        and one_three > branch
        and zero_seven > one_three
        and guard_adjust > zero_seven
        and "CHAR_WORKBATTLECOM1" in attack_fn[branch:zero_seven + 100]
        and "BATTLE_COM_GUARD" in attack_fn[branch:zero_seven + 100]
    )

    event_fn = _compact(_function(data["battle_event"], "int BATTLE_S_GBreak2"))
    event_attackseq = (
        "BATTLE_AttackSeq(" in event_fn
        and COMMAND_NAME in event_fn
    )
    event_damage_sub = "BATTLE_DamageSub(" in event_fn
    event_marks_guardbreak = (
        "BCF_GUARD" in event_fn and "BCF_GBREAK" in event_fn
    )

    command_value, source_skill_id, source_sacrifice_id = _enum_probe(base)
    source_symbol_order = (
        source_skill_id == 542 and source_sacrifice_id == 543
    )

    gates = {
        "feature_active": feature_active,
        "callback_command": callback_command,
        "callback_target": callback_target,
        "callback_ignores_option": callback_ignores_option,
        "dispatch_target_adjust": dispatch_target_adjust,
        "guard_multiplier_order": guard_multiplier_order,
        "event_attackseq": event_attackseq,
        "event_damage_sub": event_damage_sub,
        "event_marks_guardbreak": event_marks_guardbreak,
        "source_symbol_order": source_symbol_order,
    }
    if not all(gates.values()):
        raise ValueError(f"{name} GuardBreak2 source audit did not converge: {gates}")

    return {
        "name": name,
        "commit": actual,
        "command_value": command_value,
        "source_skill_id": source_skill_id,
        "source_sacrifice_id": source_sacrifice_id,
        "gates": gates,
        "hashes": {key: _sha(path) for key, path in paths.items()},
    }


def emit(rows) -> None:
    print("StoneAge GuardBreak2 fixed-source audit — R1")
    print("No original source text is stored.")
    for row in rows:
        fields = [
            f"profile={row['name']}",
            f"commit={row['commit']}",
            f"command_value={row['command_value']}",
            f"source_skill_symbol_id={row['source_skill_id']}",
            f"source_sacrifice_symbol_id={row['source_sacrifice_id']}",
        ]
        fields.extend(
            f"{key}={int(value)}"
            for key, value in sorted(row["gates"].items())
        )
        print("PROFILE|" + "|".join(fields))
        for key, value in sorted(row["hashes"].items()):
            print(
                "SOURCE_SHA256|"
                f"profile={row['name']}|file={key}|sha256={value}"
            )
    command_values={row["command_value"] for row in rows}
    source_ids={row["source_skill_id"] for row in rows}
    closed=(
        len(rows)==3
        and len(command_values)==1
        and source_ids=={542}
        and all(all(row["gates"].values()) for row in rows)
    )
    print(
        "RESOLUTION|GUARDBREAK2_FIXED_SOURCE_"
        + ("CLOSED" if closed else "OPEN")
    )


def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument("--gavin-dir",type=Path,required=True)
    parser.add_argument("--iris-dir",type=Path,required=True)
    parser.add_argument("--bismarck-dir",type=Path,required=True)
    args=parser.parse_args()
    rows=[
        analyze_profile("gavin",args.gavin_dir),
        analyze_profile("iris",args.iris_dir),
        analyze_profile("bismarck",args.bismarck_dir),
    ]
    emit(rows)


if __name__ == "__main__":
    main()
