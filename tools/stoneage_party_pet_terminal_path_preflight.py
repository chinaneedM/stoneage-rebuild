"""Fail-closed terminal/reward source preflight for pinned late StoneAge descendants.

SOURCE ONLY. This does not execute a lethal hit, BATTLE_Finish or profit.
No original source or assets are written to project outputs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

from tools.stoneage_party_pet_original_round_audit import (
    PINNED, LAYOUTS, definition, pp_file,
)

NAMES = (
    "BATTLE_FinishSet", "BATTLE_Finish", "BATTLE_GetProfit",
    "BATTLE_GetExpGold", "BATTLE_GetDuelPoint", "BATTLE_AddProfit",
    "BATTLE_CountAlive", "BATTLE_getBattleDieIndex",
)
# Accepted attack-round receipt: these hashes are independent frozen
# observations of the same complete preprocessed original bodies.
PREVIOUS_FINGERPRINTS = {
    "gavin": {
        "BATTLE_FinishSet": "eac56e7cdb00f373095544450ab347bfd1d4927159f9501f3f31cd4092172b65",
        "BATTLE_Finish": "e440d90b269bcb0620dcd96fda4758a0720bf367f14936f035ab9bbc787006e4",
        "BATTLE_GetProfit": "35edd4961868b6a4d50cade0c6141b1659cb28ba914e8ccd93c4a9347bcc855d",
    },
    "bismarck": {
        "BATTLE_FinishSet": "0488daa7341cd31b1ea16ce03830bcc009c58c0da597919855eb8516e16f9f4d",
        "BATTLE_Finish": "b369c2af159f182ed7e918ec083f73ae76ade2e3e3f907ae7525306f5ec035b8",
        "BATTLE_GetProfit": "5682714a9f08532fc7c492b854f09a8304a8f5fc0fe4c661a0a28bceb7f10e94",
    },
}
NAMED_CALL = re.compile(r"\b((?:BATTLE|CHAR|NPC|NETWATCH|PET)_[A-Za-z0-9_]+)\s*\(")


def functions(battle_source: str) -> dict[str, str]:
    return {name: definition(battle_source, name) for name in NAMES}


def inspect_terminal(profile: str, bodies: dict[str, str], *, check_fingerprints=True) -> dict:
    if profile not in PREVIOUS_FINGERPRINTS:
        raise ValueError("unrecognized source profile")
    missing = set(NAMES) - set(bodies)
    if missing:
        raise ValueError("missing original terminal definitions: " + ",".join(sorted(missing)))

    for name, sha in PREVIOUS_FINGERPRINTS[profile].items():
        if check_fingerprints and hashlib.sha256(bodies[name].encode()).hexdigest() != sha:
            raise ValueError("accepted original terminal body drift: " + profile + "/" + name)

    def called(name: str) -> set[str]:
        return set(NAMED_CALL.findall(bodies[name])) - {name}

    if not re.search(
        r"BattleArray\s*\[\s*battleindex\s*\]\s*\.\s*mode\s*=\s*BATTLE_MODE_FINISH\s*;",
        bodies["BATTLE_FinishSet"],
    ):
        raise ValueError("FinishSet mode-transition write missing")
    if not {"BATTLE_GetDuelPoint", "BATTLE_GetExpGold"} <= called("BATTLE_GetProfit"):
        raise ValueError("GetProfit must retain both reward routes")
    if not {"BATTLE_GetProfit", "BATTLE_Exit", "BATTLE_DeleteBattle"} <= called("BATTLE_Finish"):
        raise ValueError("Finish reward, exit or arena release route missing")
    if not {"BATTLE_GetExp", "CHAR_LevelUpCheck", "CHAR_PetLevelUp"} <= called("BATTLE_GetExpGold"):
        raise ValueError("GetExpGold experience or actor/pet leveling route missing")

    # This is the optional WinFunc conditional, not the final victory
    # predicate. In particular the two original profiles do not agree.
    sentinel = "0" if profile == "gavin" else "-1"
    pattern = r"\.winside\s*==\s*" + re.escape(sentinel) + r"\s*&&"
    if not re.search(pattern, bodies["BATTLE_Finish"]):
        raise ValueError("source-profile WinFunc sentinel changed: " + profile)

    return {
        "profile": profile,
        "original_profile_winside_in_WinFunc_condition": sentinel,
        "finishset_mode_write": True,
        "reward_dispatch": ["BATTLE_GetDuelPoint", "BATTLE_GetExpGold"],
        "finish_named_routes": ["BATTLE_GetProfit", "BATTLE_Exit", "BATTLE_DeleteBattle"],
        "exp_gold_named_routes": ["BATTLE_GetExp", "CHAR_LevelUpCheck", "CHAR_PetLevelUp"],
        "body_checks": {
            name: {
                "preprocessed_sha256": hashlib.sha256(body.encode()).hexdigest(),
                "body_bytes_utf8": len(body.encode()),
                "named_call_inventory": sorted(called(name)),
            }
            for name, body in bodies.items()
        },
    }


def check_checkout(profile: str, path: Path) -> None:
    sha = subprocess.check_output(
        ["git", "-C", str(path), "rev-parse", "HEAD"], text=True,
    ).strip()
    dirty = subprocess.check_output(
        ["git", "-C", str(path), "status", "--porcelain"], text=True,
    ).strip()
    if sha != PINNED[profile] or dirty:
        raise ValueError("pinned clean source required: " + profile)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gavin-dir", required=True, type=Path)
    parser.add_argument("--bismarck-dir", required=True, type=Path)
    args = parser.parse_args()
    results = []
    for profile in ("gavin", "bismarck"):
        root = getattr(args, profile + "_dir")
        check_checkout(profile, root)
        file_path = root / LAYOUTS[profile] / "battle/battle.c"
        battle = pp_file(profile, root, LAYOUTS[profile] / "battle/battle.c")
        record = inspect_terminal(profile, functions(battle))
        record["pinned_commit"] = PINNED[profile]
        record["original_battle_file_sha256"] = hashlib.sha256(file_path.read_bytes()).hexdigest()
        results.append(record)
        print(
            "SOURCE_PROFILE|{}|functions={}|original_file_sha256={}|finish_preprocessed_sha256={}".format(
                profile, len(NAMES), record["original_battle_file_sha256"],
                record["body_checks"]["BATTLE_Finish"]["preprocessed_sha256"],
            ),
            flush=True,
        )
    print("SOURCE_ROUTE_MATRIX|" + json.dumps(results, sort_keys=True, ensure_ascii=True))
    print("BOUNDARY|source_only;WinFunc_sentinel_not_victory_oracle;no_lethal_or_Finish_or_profit_execution")
    print("OPEN|lethal_HP_death_winside_FinishSet_full_Finish_GetProfit_Exit_DeleteBattle")
    print("RESOLUTION|ORIGINAL_PARTY_PET_TERMINAL_PATH_SOURCE_PREFLIGHT_PASS")


if __name__ == "__main__":
    main()
