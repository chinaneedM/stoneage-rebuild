"""Reproduce PETSKILL_Lighttakeed facts at three pinned descendant commits."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import subprocess

from tools.stoneage_guard_break2_source_audit import (
    PINNED, LAYOUTS, _function, _sha, _text, _compact,
)
from tools.stoneage_weaken_source_audit import _enum_values

CALLBACK_NAME = "PETSKILL_Lighttakeed"
COMMAND_NAME = "BATTLE_COM_S_LIGHTTAKE"
FEATURE_NAME = "_BATTLE_LIGHTTAKE"


def _case_block(text: str, marker: str) -> str:
    start = text.find(marker)
    if start < 0:
        raise ValueError("missing case " + marker)
    brace = text.find("{", start)
    if brace < 0:
        raise ValueError("missing case block")
    depth = 0
    state = "code"
    i = brace
    while i < len(text):
        ch = text[i]
        nxt = text[i + 1] if i + 1 < len(text) else ""
        if state == "code":
            if ch == "/" and nxt == "/":
                state = "line"; i += 2; continue
            if ch == "/" and nxt == "*":
                state = "block"; i += 2; continue
            if ch == '"':
                state = "string"; i += 1; continue
            if ch == "'":
                state = "char"; i += 1; continue
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return text[start:i + 1]
        elif state == "line":
            if ch == "\n": state = "code"
        elif state == "block":
            if ch == "*" and nxt == "/":
                state = "code"; i += 2; continue
        elif state == "string":
            if ch == "\\": i += 2; continue
            if ch == '"': state = "code"
        elif state == "char":
            if ch == "\\": i += 2; continue
            if ch == "'": state = "code"
        i += 1
    raise ValueError("unterminated case block")


def analyze_profile(name: str, root: Path):
    root = Path(root).resolve()
    actual = subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", "HEAD"], text=True
    ).strip()
    dirty = subprocess.check_output(
        ["git", "-C", str(root), "status", "--porcelain"], text=True
    ).strip()
    if actual != PINNED[name] or dirty:
        raise ValueError(f"{name} source identity/tree drift")

    base = root / LAYOUTS[name]
    paths = {
        "pet": base / "battle/pet_skill.c",
        "battle": base / "battle/battle.c",
        "event": base / "battle/battle_event.c",
        "version": base / "include/version.h",
        "battle_h": base / "include/battle.h",
        "char_h": base / "include/char_base.h",
    }
    data = {key: _text(path) for key, path in paths.items()}
    includes = ["-I", str(base / "include")]
    if name == "bismarck":
        includes += ["-I", str(root / "server/common"), "-I", str(root / "shared/lua51")]
    macros = subprocess.check_output(
        ["cpp", "-dM", *includes, str(paths["version"])], text=True
    )
    active = set(re.findall(r"^#define\s+(\w+)", macros, re.M))
    enums = _enum_values([COMMAND_NAME, "BATTLE_CHARMODE_C_OK"], includes)

    pet_compact = _compact(data["pet"]).replace("char_index", "charaindex")
    callback = _compact(
        _function(data["pet"], "int " + CALLBACK_NAME)
    ).replace("char_index", "charaindex")
    battle_compact = _compact(data["battle"]).replace("char_index", "charaindex")
    dispatch = _case_block(battle_compact, "case" + COMMAND_NAME + ":")
    event_all = _compact(data["event"]).replace("char_index", "charaindex")
    damage_start = event_all.find("intBATTLE_S_AttackDamage(")
    lighttake_start = event_all.find("case" + COMMAND_NAME + ":", damage_start)
    if damage_start < 0 or lighttake_start < 0:
        raise ValueError("missing bounded AttackDamage/Lighttake slice")
    event_prefix = event_all[damage_start:lighttake_start]
    event_case = _case_block(event_all[lighttake_start:], "case" + COMMAND_NAME + ":")

    expected_style = "copy_plus_one" if name == "bismarck" else "copy"
    vars_ = (
        "CHAR_WORKDAMAGEVANISH",
        "CHAR_WORKDAMAGEABSROB",
        "CHAR_WORKDAMAGEREFLEC",
    )
    if expected_style == "copy_plus_one":
        style_ok = all(
            f"CHAR_getWorkInt(defindex,{var})" in event_case
            and f"CHAR_setWorkInt(attackindex,{var},Typenum+1)" in event_case
            for var in vars_
        )
    else:
        style_ok = all(
            f"CHAR_getWorkInt(defindex,{var})" in event_case
            and f"CHAR_setWorkInt(attackindex,{var},Typenum)" in event_case
            for var in vars_
        )

    switch_at = event_prefix.find("switch(skill_type)")
    if switch_at < 0:
        raise ValueError("missing BATTLE_S_AttackDamage skill switch")
    reaction_gate = event_prefix[:switch_at]
    gates = {
        "feature_active": FEATURE_NAME in active,
        "callback_registered":
            '{"' + CALLBACK_NAME + '",' + CALLBACK_NAME + ',0}' in pet_compact,
        "callback_rejects_player":
            "CHAR_WHICHTYPE)==CHAR_TYPEPLAYER)returnFALSE" in callback,
        "callback_sets_command_target_mode": all(
            token in callback for token in (
                "CHAR_WORKBATTLECOM1," + COMMAND_NAME,
                "CHAR_WORKBATTLECOM2,toNo",
                "CHAR_WORKBATTLEMODE,BATTLE_CHARMODE_C_OK",
            )
        ),
        "callback_attack_power_70": "CHAR_WORKFIXSTR)*0.7" in callback,
        "callback_defence_power_50": "CHAR_WORKFIXTOUGH)*0.5" in callback,
        "callback_packs_skill_array_low":
            "CHAR_SETWORKINT_LOW(charaindex,CHAR_WORKBATTLECOM3,array)" in callback,
        "callback_does_not_read_option": "PETSKILL_getChar" not in callback,
        "callback_no_rng": "RAND(" not in callback and "rand(" not in callback,
        "dispatch_target_adjust_then_attackdamage":
            dispatch.find("BATTLE_TargetAdjust(") >= 0
            and dispatch.find("BATTLE_S_AttackDamage(")
                > dispatch.find("BATTLE_TargetAdjust("),
        "dispatch_passes_low_skill_and_lighttake_command": all(
            token in dispatch for token in (
                "CHAR_GETWORKINT_LOW(charaindex,CHAR_WORKBATTLECOM3)",
                "BATTLE_S_AttackDamage(",
                COMMAND_NAME,
            )
        ),
        "reaction_gate_reads_damage_react":
            "ReactType=BATTLE_GetDamageReact(defindex)" in reaction_gate,
        "reaction_gate_recognizes_three_markers": all(
            token in reaction_gate for token in (
                'strstr(pszP,"VANISH")',
                'strstr(pszP,"ABSROB")',
                'strstr(pszP,"REFLEC")',
                "BATTLE_MD_VANISH",
                "BATTLE_MD_ABSROB",
                "BATTLE_MD_REFLEC",
            )
        ),
        "matching_reaction_is_neutralized":
            "if(ReactType==Statustype){react=0;}else{skill_type=-1;}"
            in reaction_gate,
        "event_reads_option":
            "PETSKILL_getChar(skill,PETSKILL_OPTION)" in event_prefix
            or "PETSKILL_getChar(skill,PETSKILL_OPTION)" in event_case,
        "event_three_counter_paths": all(
            token in event_case for token in (
                'strstr(pszP,"VANISH")',
                'strstr(pszP,"ABSROB")',
                'strstr(pszP,"REFLEC")',
                *vars_,
            )
        ),
        "event_profile_counter_transfer_matches": style_ok,
        "event_emits_standard_bh_frame": all(
            token in event_case for token in (
                '"BH|a%X|r%X|f%X|d%X|p%X|FF|"',
                "attackNo,defNo,flg,damage,petdamage",
                "BATTLESTR_ADD(szCommand)",
            )
        ),
        "event_no_rng": "RAND(" not in event_case and "rand(" not in event_case,
    }
    failed = {key: value for key, value in gates.items() if not value}
    if failed:
        raise ValueError(f"{name} Lighttakeed source gates failed: {failed}")

    return {
        "profile": name,
        "commit": actual,
        "command_value": enums[COMMAND_NAME],
        "mode_value": enums["BATTLE_CHARMODE_C_OK"],
        "counter_transfer_style": expected_style,
        "gates": gates,
        "hashes": {key: _sha(path) for key, path in paths.items()},
    }


def emit(rows):
    print("StoneAge Lighttakeed fixed-source audit — R1")
    print("Derived facts only; no original source text/assets stored.")
    for row in rows:
        print(
            "PROFILE|"
            f"name={row['profile']}|sha={row['commit']}|"
            f"command_value={row['command_value']}|"
            f"mode_value={row['mode_value']}|"
            f"counter_transfer_style={row['counter_transfer_style']}"
        )
        for key, value in sorted(row["gates"].items()):
            print(f"GATE|profile={row['profile']}|name={key}|pass={int(value)}")
        for key, value in sorted(row["hashes"].items()):
            print(
                f"SOURCE_SHA256|profile={row['profile']}|"
                f"file={key}|sha256={value}"
            )
    print("FACT|callback_fixed_work_powers=attack70_defence50")
    print("FACT|callback_option_reads=none")
    print("FACT|dispatch=target_adjust_then_attackdamage")
    print("FACT|reaction_markers=VANISH,ABSROB,REFLEC")
    print("FACT|matching_damage_reaction_is_neutralized_before_attack_sequence")
    print("FACT|nonmatching_active_damage_reaction_demotes_lighttake_skill_type")
    print("FACT|lighttake_callback_and_event_consume_no_rng")
    print("BOUNDARY|counter_transfer=gavin_iris_copy_bismarck_copy_plus_one")
    print("BOUNDARY|original_binary_compile_profile_and_numeric_command_open")
    print("RESOLUTION|LIGHTTAKEED_FIXED_SOURCE_CLOSED_CONDITIONAL_REFERENCE")


def main():
    parser = argparse.ArgumentParser()
    for name in PINNED:
        parser.add_argument("--" + name + "-dir", type=Path, required=True)
    args = parser.parse_args()
    emit([
        analyze_profile(name, getattr(args, name + "_dir"))
        for name in PINNED
    ])


if __name__ == "__main__":
    main()
