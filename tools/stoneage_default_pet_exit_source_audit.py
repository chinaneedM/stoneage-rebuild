"""Native DEFAULTPET selection witnesses at three clean descendant pins.

Only BATTLE_PetDefaultExit is executed. Getters and BATTLE_Exit are controlled
stubs; full cleanup/profit/occupancy and the original build remain uncertified.
Original function text exists only in a temporary directory.
"""
from __future__ import annotations

import argparse
from itertools import product
from pathlib import Path
import subprocess
import tempfile

from tools.stoneage_guard_break2_source_audit import PINNED, LAYOUTS, _text, _sha, _compact
from tools.stoneage_mdfyattack_source_audit import _definition, _strip


PREFIX = r'''
#include <stdio.h>
#define FALSE 0
#define CHAR_TYPEPLAYER 1
#define CHAR_WHICHTYPE 0
#define CHAR_DEFAULTPET 1
#define BATTLE_ERR_CHARAINDEX -11
static int valid,kind,selection,lookup_result,exit_result;
static int lookup_calls,exit_calls,seen_selection,seen_pet,seen_battle;
int CHAR_CHECKINDEX(int index){return index==7 && valid;}
int CHAR_getInt(int index,int field){return field==CHAR_WHICHTYPE?kind:selection;}
int CHAR_getCharPet(int owner,int slot){
  if(owner!=7)return -99;
  lookup_calls++;seen_selection=slot;return lookup_result;
}
int BATTLE_Exit(int pet,int battle){
  exit_calls++;seen_pet=pet;seen_battle=battle;return exit_result;
}
'''

MAIN = r'''
int main(void){
  while(scanf("%d%d%d%d%d",&valid,&kind,&selection,&lookup_result,&exit_result)==5){
    lookup_calls=exit_calls=0;seen_selection=seen_pet=seen_battle=-99;
    int result=BATTLE_PetDefaultExit(7,13);
    printf("%d %d %d %d %d %d %d\n",result,lookup_calls,exit_calls,
           seen_selection,seen_pet,seen_battle,selection);
  }
  return 0;
}
'''


def analyze_profile(name: str, root: Path) -> dict:
    root = root.resolve()
    head = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
    dirty = subprocess.check_output(["git", "-C", str(root), "status", "--porcelain"], text=True).strip()
    if head != PINNED[name] or dirty:
        raise ValueError("pinned source commit/tree drift")
    path = root / LAYOUTS[name] / "battle/battle.c"
    text = _text(path)
    body = _definition(text, "BATTLE_PetDefaultExit")
    # Static observations are separate from the native helper certificate.
    # Bismarck renamed these identifiers; only static anchors normalize them.
    # The compiled original helper is never rewritten.
    normalized = text.replace("char_index", "charaindex").replace("enemy_index", "enemyindex")
    ultimate = _compact(_strip(_definition(normalized, "BATTLE_UltimateExtra", raw_window=True)))
    exit_body = _compact(_strip(_definition(normalized, "_BATTLE_Exit", raw_window=True)))
    required = (
        (ultimate, "BATTLE_PetDefaultExit(enemyindex,battleindex);"),
        (ultimate, "CHAR_setInt(playerindex,CHAR_DEFAULTPET,-1);"),
        (exit_body, "intpetindex=pEntry[i+5].charaindex;"),
        (exit_body, "pEntry[i+5].charaindex=-1;"),
    )
    if any(token not in source for source, token in required):
        raise ValueError("ultimate selection or paired-occupancy source anchor drift")
    cases = list(product((0, 1), (1, 2, 3), (-1, 0, 4), (-1, 2, 3), (-3, 0, 5)))
    with tempfile.TemporaryDirectory(prefix="sa-default-pet-exit-") as folder:
        source, binary = Path(folder) / "oracle.c", Path(folder) / "oracle"
        source.write_text(PREFIX + "\n" + body + "\n" + MAIN)
        subprocess.run(["cc", "-std=c99", "-O0", str(source), "-o", str(binary)],
                       check=True, capture_output=True, text=True)
        rows = subprocess.check_output([str(binary)],
            input="".join(" ".join(map(str, c)) + "\n" for c in cases), text=True).splitlines()
    if len(rows) != len(cases):
        raise ValueError("native helper case count drift")
    for (valid, kind, selection, pet, error), row in zip(cases, rows):
        if not valid:
            wanted = (-11, 0, 0, -99, -99, -99, selection)
        elif kind != 1 or selection < 0:
            wanted = (0, 0, 0, -99, -99, -99, selection)
        else:
            wanted = (1 if error == 0 else -error, 1, 1, selection, pet, 13, selection)
        if tuple(map(int, row.split())) != wanted:
            raise ValueError(f"DEFAULTPET helper drift: {(valid, kind, selection, pet, error)}")
    return {"profile": name, "sha": head, "source_sha256": _sha(path),
            "native_default_pet_exit_cases": len(cases)}


def main() -> None:
    parser = argparse.ArgumentParser()
    for name in PINNED:
        parser.add_argument("--" + name + "-dir", required=True, type=Path)
    args = parser.parse_args()
    total = 0
    for name in PINNED:
        result = analyze_profile(name, getattr(args, name + "_dir"))
        total += result["native_default_pet_exit_cases"]
        print("PROFILE|" + "|".join(f"{k}={v}" for k, v in result.items()))
    print(f"TOTAL|native_default_pet_exit_cases={total}")
    print("FACT|helper_uses_explicit_DEFAULTPET_lookup_not_active_pet_count")
    print("STATIC|player_exit_also_has_independent_entry_i_plus5_cleanup")
    print("STATIC|pet_ultimate_clears_owner_DEFAULTPET")
    print("BOUNDARY|controlled_getters_and_exit_result_only_no_full_cleanup_profit_or_occupancy_native_certificate")
    print("RESOLUTION|EXPLICIT_DEFAULT_PET_EXIT_HELPER_NATIVE_PASS")


if __name__ == "__main__":
    main()
