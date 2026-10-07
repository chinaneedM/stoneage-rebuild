#!/usr/bin/env python3
"""Audit pinned descendant source order for BecomePig ordinary attack flow.

The audit emits hashes and semantic order booleans only. Original descendant
source is a transient input and is never copied into this repository.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re
import subprocess

from tools.stoneage_guard_break2_source_audit import PINNED, LAYOUTS

REPORT_RESOLUTION = (
    "BECOMEPIG_ORIGINAL_MAIN_GUARDIAN_COUNTER_RETARGET_ORDER_"
    "SOURCE_PASS_ZERO_RUNTIME_PROMOTIONS"
)


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _text(path: Path) -> str:
    return path.read_bytes().decode("utf-8", "replace")


_DEF_RE = re.compile(
    r"\b(?:static\s+)?(?:int|void|BOOL)\s+"
    r"([A-Za-z_][A-Za-z0-9_]*)\s*\([^;{}]*\)\s*\{",
    re.DOTALL,
)


def _definition(text: str, name: str) -> str:
    """Return a raw definition region without brace-balancing preprocessor arms."""
    matches = list(_DEF_RE.finditer(text))
    for index, match in enumerate(matches):
        if match.group(1) != name:
            continue
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        return text[match.start():end]
    raise ValueError(f"missing definition {name}")


def _code_only(text: str) -> str:
    """Blank comments and quoted literals while preserving offsets/newlines."""
    out = list(text)
    i = 0
    state = "code"
    quote = ""
    while i < len(text):
        ch = text[i]
        nxt = text[i + 1] if i + 1 < len(text) else ""
        if state == "code":
            if ch == "/" and nxt == "/":
                out[i] = out[i + 1] = " "
                state = "line"
                i += 2
                continue
            if ch == "/" and nxt == "*":
                out[i] = out[i + 1] = " "
                state = "block"
                i += 2
                continue
            if ch in {'"', "'"}:
                quote = ch
                out[i] = " "
                state = "quote"
                i += 1
                continue
            i += 1
            continue
        if state == "line":
            if ch == "\n":
                state = "code"
            else:
                out[i] = " "
            i += 1
            continue
        if state == "block":
            if ch == "*" and nxt == "/":
                out[i] = out[i + 1] = " "
                state = "code"
                i += 2
            else:
                if ch != "\n":
                    out[i] = " "
                i += 1
            continue
        if state == "quote":
            if ch == "\\":
                out[i] = " "
                if i + 1 < len(text):
                    if text[i + 1] != "\n":
                        out[i + 1] = " "
                    i += 2
                else:
                    i += 1
                continue
            if ch == quote:
                out[i] = " "
                state = "code"
            elif ch != "\n":
                out[i] = " "
            i += 1
    return "".join(out)


def _pos(code: str, needle: str, *, start: int = 0) -> int:
    value = code.find(needle, start)
    if value < 0:
        raise ValueError(f"missing required source token: {needle}")
    return value


def _regex_pos(code: str, pattern: str, *, start: int = 0) -> int:
    match = re.search(pattern, code[start:], re.MULTILINE | re.DOTALL)
    if match is None:
        raise ValueError(f"missing required source pattern: {pattern}")
    return start + match.start()


def analyze_texts(battle_text: str, event_text: str) -> dict[str, bool | int]:
    """Return bounded structural facts from the exact pinned source bodies."""
    attackseq = _code_only(_definition(event_text, "BATTLE_AttackSeq"))
    attack = _code_only(_definition(event_text, "BATTLE_Attack"))
    counter = _code_only(_definition(event_text, "BATTLE_Counter"))
    battling = _code_only(_definition(battle_text, "BATTLE_Battling"))

    duck = _pos(attackseq, "BATTLE_DuckCheck")
    seq_guard_sentinel = _regex_pos(
        attackseq,
        r"if\s*\(\s*\*pGuardian\s*==\s*-1\s*\)",
        start=duck,
    )
    seq_guard = _pos(attackseq, "BATTLE_GuardianCheck", start=seq_guard_sentinel)
    seq_remap = _regex_pos(
        attackseq,
        r"defindex\s*=\s*GuardianIndex\s*;",
        start=seq_guard,
    )
    critical = _pos(attackseq, "BATTLE_CriticalCheck", start=seq_remap)

    main_seq = _pos(attack, "BATTLE_AttackSeq")
    main_guard_cond = _regex_pos(
        attack, r"if\s*\(\s*Guardian\s*>=\s*0\s*\)", start=main_seq
    )
    main_guard_remap = _regex_pos(
        attack,
        r"defindex\s*=\s*BATTLE_No2Index\s*\(\s*battleindex\s*,\s*Guardian\s*\)\s*;",
        start=main_guard_cond,
    )
    main_damage = _pos(attack, "BATTLE_DamageSub", start=main_guard_remap)

    counter_guardian_init = _regex_pos(
        counter, r"\bGuardian\s*=\s*-2\b"
    )
    counter_check = _pos(counter, "BATTLE_CounterCheck", start=counter_guardian_init)
    counter_seq = _pos(counter, "BATTLE_AttackSeq", start=counter_check)
    counter_scale = _regex_pos(
        counter, r"damage\s*\*=\s*0\.75\s*;", start=counter_seq
    )
    counter_damage = _pos(counter, "BATTLE_DamageSub", start=counter_scale)
    counter_between = counter[counter_seq:counter_damage]
    counter_guardian_remap = bool(
        re.search(
            r"defindex\s*=\s*BATTLE_No2Index\s*\([^;]*Guardian[^;]*\)\s*;",
            counter_between,
            re.DOTALL,
        )
    )

    main_call = _regex_pos(
        battling,
        r"ContFlg\s*=\s*BATTLE_Attack\s*\(\s*battleindex\s*,\s*attackNo\s*,\s*defNo\s*\)",
    )
    initial_adjust = battling.rfind("BATTLE_TargetAdjust", 0, main_call)
    if initial_adjust < 0:
        raise ValueError("missing target adjust before ordinary main hit")
    profit = _pos(battling, "BATTLE_AddProfit", start=main_call)
    repeat_adjust = _pos(battling, "BATTLE_TargetAdjust", start=profit)
    counter_loop = _regex_pos(
        battling,
        r"for\s*\(\s*k\s*=\s*0\s*;\s*k\s*<\s*5\s*&&\s*ContFlg\s*==\s*TRUE",
        start=repeat_adjust,
    )
    counter_call = _pos(battling, "BATTLE_Counter", start=counter_loop)
    post_pig = _regex_pos(
        battling,
        r"COM\s*==\s*BATTLE_COM_S_BECOMEPIG",
        start=counter_call,
    )
    post_pig_target_check = _pos(
        battling, "BATTLE_TargetCheck", start=post_pig
    )
    post_pig_defindex = _regex_pos(
        battling,
        r"defindex\s*=\s*BATTLE_No2Index\s*\(\s*battleindex\s*,\s*defNo\s*\)",
        start=post_pig,
    )

    return {
        "attackseq_guardiancheck_requires_minus1":
            duck < seq_guard_sentinel < seq_guard < seq_remap < critical,
        "attackseq_duck_guardian_remap_critical":
            duck < seq_guard_sentinel < seq_guard < seq_remap < critical,
        "main_attackseq_guardian_remap_damage":
            main_seq < main_guard_cond < main_guard_remap < main_damage,
        "counter_initializes_guardian_minus2_before_attackseq":
            counter_guardian_init < counter_check < counter_seq,
        "counter_minus2_bypasses_attackseq_guardiancheck":
            counter_guardian_init < counter_seq and seq_guard_sentinel < seq_guard,
        "counter_check_attackseq_scale_damage":
            counter_guardian_init < counter_check < counter_seq < counter_scale < counter_damage,
        "counter_caller_guardian_remap_between_seq_damage":
            counter_guardian_remap,
        "dispatch_adjust_main_profit_readjust_counter_postpig":
            initial_adjust < main_call < profit < repeat_adjust
            < counter_loop < counter_call < post_pig,
        "postpig_rechecks_target_then_resolves_defno":
            post_pig < post_pig_target_check < post_pig_defindex,
    }


def analyze_profile(name: str, root: Path) -> dict[str, str | bool | int]:
    root = root.resolve()
    head = subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", "HEAD"], text=True
    ).strip()
    dirty = subprocess.check_output(
        ["git", "-C", str(root), "status", "--porcelain"], text=True
    ).strip()
    if head != PINNED[name] or dirty:
        raise ValueError(f"{name}: pinned source commit/tree drift")

    battle_path = root / LAYOUTS[name] / "battle/battle.c"
    event_path = root / LAYOUTS[name] / "battle/battle_event.c"
    facts = analyze_texts(_text(battle_path), _text(event_path))
    if not all(
        value is True
        for key, value in facts.items()
        if key != "counter_caller_guardian_remap_between_seq_damage"
    ):
        raise ValueError(f"{name}: required attack-order fact failed: {facts}")
    if facts["counter_caller_guardian_remap_between_seq_damage"]:
        raise ValueError(f"{name}: counter Guardian caller behavior drift")

    return {
        "profile": name,
        "pin": PINNED[name],
        "battle_sha256": _sha(battle_path),
        "battle_event_sha256": _sha(event_path),
        **facts,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    for name in PINNED:
        parser.add_argument(f"--{name}-dir", type=Path, required=True)
    args = parser.parse_args()

    print("StoneAge BecomePig pinned descendant attack-order source audit R1")
    rows = []
    for name in PINNED:
        row = analyze_profile(name, getattr(args, f"{name}_dir"))
        rows.append(row)
        print(
            "PROFILE|"
            + "|".join(
                f"{key}={int(value) if isinstance(value, bool) else value}"
                for key, value in row.items()
            )
        )
    if len(rows) != 3:
        raise ValueError("expected exactly three source profiles")
    print("FACT|ordinary_dispatch_adjusts_target_before_main_hit")
    print("FACT|main_AttackSeq_redirects_to_Guardian_before_main_DamageSub")
    print("FACT|counter_initializes_Guardian_minus2_so_AttackSeq_bypasses_GuardianCheck_and_DamageSub_keeps_original_defender")
    print("FACT|ordinary_dispatch_runs_profit_and_repeat_retarget_before_counter_chain")
    print("FACT|BecomePig_postattack_gate_runs_after_counter_chain_and_rechecks_final_defNo")
    print("BOUNDARY|pinned_descendant_source_order_only_no_historical_build_or_PRNG_or_native_runtime_promotion")
    print(f"RESOLUTION|{REPORT_RESOLUTION}")


if __name__ == "__main__":
    main()
