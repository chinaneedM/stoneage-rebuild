"""Bounded, pinned descendant-source preflight for party/pet battle admission.

STATIC evidence only: not a native runtime test, Taiwan-v1 proof, or semantic
oracle for party/pet Exit. Original source bytes remain in transient CI clones.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

from tools.stoneage_enemy_creation_audit import definition
from tools.stoneage_enemy_loader_audit import pp_file
from tools.stoneage_guard_break2_source_audit import LAYOUTS, PINNED


FUNCTIONS = ("BATTLE_PetDefaultEntry", "BATTLE_PartyNewEntry", "BATTLE_ClearGetExp")
PROFILES = ("gavin", "bismarck")


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def compact(raw: str) -> str:
    # Only whitespace normalization. Real functions are extracted from
    # preprocessed, profile-selected original C; no C bodies are rewritten.
    return re.sub(r"\s+", "", raw)


def require(name: str, text: str, tokens: tuple[str, ...]) -> None:
    absent = [token for token in tokens if token not in text]
    if absent:
        raise ValueError(f"{name}: missing source anchors {absent}")


def classify(profile: str, original: dict[str, str]) -> dict:
    if profile not in PROFILES:
        raise ValueError("unaccepted source profile")
    pet, party, exp = (compact(original[k]) for k in FUNCTIONS)
    require("pet", pet, (
        "CHAR_DEFAULTPET", "CHAR_getCharPet(", "CHAR_CHECKINDEX(",
        "CHAR_ISDIE", "CHAR_HP", "BATTLE_NewEntry(",
        "CHAR_setInt(", "returnret;", "pno==-1", "ret=0",
    ))
    require("party", party, (
        "BATTLE_NewEntry(", "CAflush(", "CDflush(",
        "BATTLE_PetDefaultEntry(", "BATTLE_ClearGetExp(",
        "CHAR_WORKPARTYINDEX1", "CHAR_WORKBATTLEMODE",
        "returniRet;",
    ))
    require("exp", exp, (
        "CHAR_CHECKINDEX(", "CHAR_WORKGETEXP",
        "CHAR_MAXPETHAVE", "CHAR_getCharPet(", "CHAR_setWorkInt(",
        "return0;",
    ))
    if "CHAR_setWorkInt(pindex,CHAR_WORKGETEXP,0)" not in exp:
        raise ValueError("pet GETEXP roster reset is not evidenced")
    if "CHAR_setWorkInt(" not in exp or "CHAR_WORKGETEXP,0" not in exp:
        raise ValueError("player GETEXP reset is not evidenced")
    if not re.search(r"for\(i=0;i<CHAR_MAXPETHAVE;i\+\+\)", exp):
        raise ValueError("full owned-pet reset loop not evidenced")
    if "i+CHAR_WORKPARTYINDEX1" not in party:
        raise ValueError("party member index source not evidenced")
    if "ret=0;" not in pet or re.search(r"\bret=(?!0;)", pet):
        raise ValueError("pet entry return/assignment needs manual review")
    if profile == "gavin":
        require("Gavin party", party, ("i<CHAR_PARTYMAX", "!=0"))
        if "i<getPartyNum(" in party:
            raise ValueError("Gavin unexpectedly uses dynamic capacity")
        guard = "nonzero mode excludes teammate; fixed CHAR_PARTYMAX loop"
        cap = "CHAR_PARTYMAX"
    else:
        require("Bismarck party", party, (
            "i<getPartyNum(", "BATTLE_CHARMODE_NONE",
            "BATTLE_CHARMODE_FINAL",
        ))
        guard = "NONE and FINAL teammate modes admitted; dynamic getPartyNum loop"
        cap = "getPartyNum"
    return {
        "party_capacity_source": cap,
        "teammate_mode_guard": guard,
        "default_pet_selected_slot_required": True,
        "default_pet_alive_hp_guard": True,
        "pet_entry_return_observation": "ret initialized to zero; wrapper does not propagate BATTLE_NewEntry result in selected #if 1 branch",
        "clear_get_exp_player_and_owned_pets": True,
        "static_evidence_only": True,
        "runtime_party_pet_admission": "OPEN",
        "runtime_exit_profit": "OPEN",
    }


def analyze(profile: str, root: Path) -> dict:
    if profile not in PROFILES:
        raise ValueError("profile not in accepted scope")
    actual = subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", "HEAD"], text=True
    ).strip()
    if actual != PINNED[profile]:
        raise ValueError(f"unpinned {profile} source: {actual}")
    relative = LAYOUTS[profile] / "battle/battle.c"
    source = root / relative
    bodies = {
        name: definition(pp_file(profile, root, relative), name)
        for name in FUNCTIONS
    }
    observations = classify(profile, bodies)
    return {
        "profile": profile,
        "source_commit": actual,
        "battle_path": relative.as_posix(),
        "battle_file_sha256": sha256(source.read_bytes()),
        "original_preprocessed_function_sha256": {
            k: sha256(compact(v).encode("utf-8")) for k, v in bodies.items()
        },
        "observations": observations,
        "evidence_status": "STATIC_PINNED_DESCENDANT_SOURCE_PREFLIGHT_NO_RUNTIME_PROMOTION",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gavin-dir", required=True, type=Path)
    parser.add_argument("--bismarck-dir", required=True, type=Path)
    args = parser.parse_args()
    records = [analyze("gavin", args.gavin_dir), analyze("bismarck", args.bismarck_dir)]
    assert records[0]["observations"]["party_capacity_source"] != records[1]["observations"]["party_capacity_source"]
    print(json.dumps(
        {"schema": "stoneage.party-pet-source-preflight.r1",
         "result": "PASS", "profiles": records,
         "excluded": ["Iris profile", "party/pet executed entry or Exit",
                      "original profit/Init/TaskLoop", "1999-JSS/Taiwan-v1 membership"]},
        ensure_ascii=False, sort_keys=True, separators=(",", ":"),
    ))


if __name__ == "__main__":
    main()
