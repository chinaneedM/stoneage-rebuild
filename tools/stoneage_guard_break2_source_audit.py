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
    """Return the first C definition, ignoring comments/string brace noise."""
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
    state = "code"
    index = brace
    while index < len(text):
        char = text[index]
        nxt = text[index + 1] if index + 1 < len(text) else ""

        if state == "code":
            if char == "/" and nxt == "/":
                state = "line_comment"
                index += 2
                continue
            if char == "/" and nxt == "*":
                state = "block_comment"
                index += 2
                continue
            if char == '"':
                state = "string"
                index += 1
                continue
            if char == "'":
                state = "char"
                index += 1
                continue
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    return text[start:index + 1]
            index += 1
            continue

        if state == "line_comment":
            if char == "\n":
                state = "code"
            index += 1
            continue

        if state == "block_comment":
            if char == "*" and nxt == "/":
                state = "code"
                index += 2
                continue
            index += 1
            continue

        if state in {"string", "char"}:
            quote = '"' if state == "string" else "'"
            if char == "\\":
                index += 2
                continue
            if char == quote:
                state = "code"
            index += 1
            continue

    raise ValueError(f"unterminated function: {signature}")


def _definition_window(
    text: str,
    function_name: str,
    *,
    max_chars: int = 12000,
) -> str:
    """Locate a real C definition and return a bounded raw-source window.

    Raw source may be brace-unbalanced before preprocessing because mutually
    exclusive #ifdef branches are all present at once. Semantic auditing here
    therefore anchors on a definition-shaped regex rather than pretending to
    parse preprocessor-dependent C.
    """
    pattern=re.compile(
        rf"\b(?:static\s+)?(?:int|void|BOOL)\s+"
        rf"{re.escape(function_name)}\s*\([^;{{}}]*\)\s*\{{",
        re.DOTALL,
    )
    match=pattern.search(text)
    if match is None:
        raise ValueError(f"missing function definition: {function_name}")
    return text[match.start():match.start()+int(max_chars)]


def _git_head(root: Path) -> str:
    return subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        text=True,
    ).strip()


def _macro_int(text: str, name: str) -> int:
    match=re.search(
        rf"^\s*#\s*define\s+{re.escape(name)}\s*\(\s*(-?\d+)\s*\)",
        text,
        re.MULTILINE,
    )
    if match is None:
        raise ValueError(f"missing integer macro: {name}")
    return int(match.group(1))


def _symbol_probe(battle_header: str, petskill_header: str):
    source_skill_id=_macro_int(
        petskill_header,
        SOURCE_PETSKILL_SYMBOL_NAME,
    )
    source_sacrifice_id=_macro_int(
        petskill_header,
        "PETSKILL_SACRIFICE",
    )
    command_symbol_present=bool(re.search(
        rf"^\s*{re.escape(COMMAND_NAME)}\s*,",
        battle_header,
        re.MULTILINE,
    ))
    return command_symbol_present,source_skill_id,source_sacrifice_id


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

    event_fn = _compact(
        _definition_window(
            data["battle_event"],
            "BATTLE_S_GBreak2",
            max_chars=9000,
        )
    )
    event_attackseq = (
        "BATTLE_AttackSeq(" in event_fn
        and COMMAND_NAME in event_fn
    )
    event_damage_sub = "BATTLE_DamageSub(" in event_fn
    event_marks_guardbreak = (
        "BCF_GUARD" in event_fn and "BCF_GBREAK" in event_fn
    )

    (
        battle_header_command_symbol,
        source_skill_id,
        source_sacrifice_id,
    ) = _symbol_probe(data["battle_h"],data["petskill_h"])
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
        "battle_header_command_symbol": battle_header_command_symbol,
        "source_symbol_order": source_symbol_order,
    }
    if not all(gates.values()):
        raise ValueError(f"{name} GuardBreak2 source audit did not converge: {gates}")

    return {
        "name": name,
        "commit": actual,
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
    source_ids={row["source_skill_id"] for row in rows}
    closed=(
        len(rows)==3
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
