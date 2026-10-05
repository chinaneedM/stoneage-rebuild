#!/usr/bin/env python3
"""Transient native no-ride BattleModel DamageSub settlement witnesses.

Only derived results and hashes are retained. Common reaction selection is a
bounded stub; the original DamageSub body performs HP/counter/ultimate writes.
"""
from __future__ import annotations

import argparse
from itertools import product
from pathlib import Path
import re
import subprocess
import tempfile

from tools.stoneage_guard_break2_source_audit import PINNED, LAYOUTS, _text, _sha
from tools.stoneage_mdfyattack_source_audit import _definition


def _native_settlement(body: str, *, verify_runtime_model: bool = False) -> int:
    fixed = {
        "BATTLE_MD_NONE": 0, "BATTLE_MD_ABSROB": 1,
        "BATTLE_MD_REFLEC": 2, "BATTLE_MD_VANISH": 3,
        "BATTLE_COM_S_BATTLE_MODEL": 1000,
    }
    names = sorted(set(re.findall(r"\b(?:CHAR|BATTLE)_[A-Z][A-Z0-9_]*\b", body)))
    constants = "\n".join(
        f"#define {name} {fixed.get(name, index + 10)}"
        for index, name in enumerate(names)
    )
    prefix = r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define FALSE 0
#define SIDE_OFFSET 10
#define _PETSKILL_BATTLE_MODEL
#define BATTLE_TYPE_P_vs_P 99
#define min(a,b) ((a)<(b)?(a):(b))
#define max(a,b) ((a)>(b)?(a):(b))
typedef struct {int flg;} Entry;
typedef struct {Entry Entry[10];} Side;
typedef struct {int type; Side Side[2];} Battle;
static Battle BattleArray[1];
static int stats[2][256],workstats[2][256],invalid_reads;
int CHAR_getInt(int c,int p){if(c<0||c>=2){invalid_reads++;return 0;}return stats[c][p];}
int CHAR_setInt(int c,int p,int v){return stats[c][p]=v;}
int CHAR_getWorkInt(int c,int p){return workstats[c][p];}
int CHAR_setWorkInt(int c,int p,int v){return workstats[c][p]=v;}
int CHAR_getItemIndex(int c,int p){return 0;}
int BATTLE_IsThrowWepon(int i){return FALSE;}
int BATTLE_getRidePet(int c){return -1;}
void BATTLE_changeRideImage(int c){}
int BATTLE_Index2No(int b,int c){return c;}
int BATTLE_GetDamageReact(int c){
 if(workstats[c][CHAR_WORKDAMAGEVANISH]>0)return BATTLE_MD_VANISH;
 if(workstats[c][CHAR_WORKDAMAGEABSROB]>0)return BATTLE_MD_ABSROB;
 if(workstats[c][CHAR_WORKDAMAGEREFLEC]>0)return BATTLE_MD_REFLEC;
 return BATTLE_MD_NONE;
}
#define print(...) ((void)0)
'''
    main = r'''
int main(void){
 int marker,sentinel,kind,raw,dhp,charges;
 while(scanf("%d%d%d%d%d%d",&marker,&sentinel,&kind,&raw,&dhp,&charges)==6){
  memset(stats,0,sizeof(stats));memset(workstats,0,sizeof(workstats));
  stats[0][CHAR_HP]=150;stats[1][CHAR_HP]=dhp;
  workstats[0][CHAR_WORKMAXHP]=workstats[1][CHAR_WORKMAXHP]=200;
  workstats[1][CHAR_NPCWORKINT1]=marker?BATTLE_COM_S_BATTLE_MODEL:0;
  if(kind==1||kind==4)workstats[1][CHAR_WORKDAMAGEABSROB]=charges;
  if(kind==2||kind==4)workstats[1][CHAR_WORKDAMAGEREFLEC]=charges;
  if(kind==3||kind==4)workstats[1][CHAR_WORKDAMAGEVANISH]=charges;
  for(int hit=0;hit<2;hit++){
   int d=raw,p=0,r=sentinel;invalid_reads=0;
   int u=BATTLE_DamageSub(0,1,&d,&p,&r);
   printf("%d %d %d %d %d %d %d %d %d %d\n",stats[0][CHAR_HP],stats[1][CHAR_HP],
    workstats[1][CHAR_WORKDAMAGEABSROB],workstats[1][CHAR_WORKDAMAGEREFLEC],
    workstats[1][CHAR_WORKDAMAGEVANISH],d,p,r,u,invalid_reads);
  }
 }
 return 0;
}
'''
    cases = list(product((0, 1), (0, -1), range(5), (0, 1, 30, 300), (1, 100), (1, 2)))
    with tempfile.TemporaryDirectory() as directory:
        source = Path(directory) / "oracle.c"
        binary = Path(directory) / "oracle"
        source.write_text(constants + prefix + body + main)
        subprocess.run(["cc", "-w", "-O0", str(source), "-o", str(binary)], check=True)
        result = subprocess.run(
            [str(binary)], input="\n".join(" ".join(map(str, c)) for c in cases) + "\n",
            text=True, capture_output=True, check=True,
        )
    lines = result.stdout.splitlines()
    if len(lines) != len(cases) * 2:
        raise ValueError("native settlement witness count drift")
    model_checks = 0
    for case_index, (marker, sentinel, kind, raw, dhp, charges) in enumerate(cases):
        hp = [150, dhp]
        counters = [charges if kind in (1, 4) else 0,
                    charges if kind in (2, 4) else 0,
                    charges if kind in (3, 4) else 0]
        overkill = [0, 0]
        for hit in range(2):
            before_hp, before_counters, before_overkill = tuple(hp), tuple(counters), tuple(overkill)
            selected = (3 if counters[2] else 1 if counters[0] else 2 if counters[1] else 0)
            reaction = selected if sentinel != -1 else 0
            reported_reaction = sentinel
            ultimate = 0
            invalid_reads = 0
            victim = 1
            if raw > 0:
                reported_reaction = reaction
                if reaction:
                    counters[reaction - 1] -= 1
                if reaction == 1:
                    hp[1] = min(200, hp[1] + raw)
                elif reaction == 2 and marker:
                    # Original marker branch reads the absent ride index; its
                    # value is unused in this explicitly no-ride settlement.
                    invalid_reads = 1
                elif reaction == 3:
                    pass
                else:
                    victim = 0 if reaction == 2 else 1
                    hp[victim] -= raw
                deficit = max(0, -hp[victim])
                hp[victim] = max(0, hp[victim])
                if raw >= 260:
                    ultimate = 2
                elif deficit:
                    overkill[victim] += deficit
                    if overkill[victim] >= 260:
                        ultimate = 1
                if ultimate:
                    overkill[victim] = 0
            expected = (*hp, *counters, raw, 0, reported_reaction, ultimate, invalid_reads)
            actual = tuple(map(int, lines[case_index * 2 + hit].split()))
            if actual != expected:
                raise ValueError(f"settlement mismatch case={case_index} hit={hit}: {actual} != {expected}")
            if verify_runtime_model and marker == 1 and sentinel == 0:
                from tools.stoneage_battlemodel_hit_loop import resolve_battlemodel_marker_settlement
                from tools.stoneage_battle_damage_react_model import BaseDamageReactState
                from tools.stoneage_battle_core_model import (
                    BattleUltimateDamageInputs, resolve_battle_ultimate_damage,
                )
                modern = resolve_battlemodel_marker_settlement(
                    BaseDamageReactState(*before_counters), raw_damage=raw,
                    attacker_hp=before_hp[0], attacker_max_hp=200,
                    defender_hp=before_hp[1], defender_max_hp=200,
                )
                ultimate_model = resolve_battle_ultimate_damage(BattleUltimateDamageInputs(
                    raw, raw if modern.effective_kind == 0 else 0,
                    before_hp[1], 200, before_overkill[1],
                ))
                model = (modern.attacker_hp_after, modern.defender_hp_after,
                         modern.state_after.absorb, modern.state_after.reflect,
                         modern.state_after.vanish, modern.raw_damage,
                         ultimate_model.ultimate_kind)
                native = (*actual[:6], actual[8])
                if model != native:
                    raise ValueError(f"runtime model/native mismatch case={case_index} hit={hit}: {model} != {native}")
                model_checks += 1
    if verify_runtime_model and model_checks != 160:
        raise ValueError("runtime/native settlement comparison count drift")
    return len(lines)


def analyze_profile(name: str, root: Path, *, verify_runtime_model: bool = False) -> tuple[str, int]:
    root = root.resolve()
    sha = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
    dirty = subprocess.check_output(["git", "-C", str(root), "status", "--porcelain"], text=True).strip()
    if sha != PINNED[name] or dirty:
        raise ValueError(f"{name} pin/tree drift")
    source = root / LAYOUTS[name] / "battle/battle_event.c"
    body = _definition(_text(source), "BATTLE_DamageSub")
    return _sha(source), _native_settlement(body, verify_runtime_model=verify_runtime_model)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify-runtime-model", action="store_true")
    for name in PINNED:
        parser.add_argument(f"--{name}-dir", required=True, type=Path)
    args = parser.parse_args()
    print("StoneAge BattleModel no-ride native DamageSub settlement — R1")
    for name in PINNED:
        digest, count = analyze_profile(name, getattr(args, name + "_dir"),
                                        verify_runtime_model=args.verify_runtime_model)
        print(f"PROFILE|profile={name}|sha={PINNED[name]}|source_sha256={digest}|native_hits={count}")
        if args.verify_runtime_model:
            print(f"MODEL|profile={name}|physical_marker_model_native_comparisons=160")
    print("FACT|BattleModel_reflect_consumes_charge_preserves_both_HP_and_reports_positive_raw_damage")
    print("FACT|nonphysical_sentinel_bypasses_reactions_and_preserves_charges")
    print("FACT|raw_threshold_can_report_ultimate2_without_HP_loss")
    print("OPEN|reflect_marker_reads_absent_ride_index_in_no_ride_source_path")
    print("BOUNDARY|reduced_base_feature_profile_no_ride_nonthrowing_stubbed_reaction_priority_no_original_build_claim")
    print("RESOLUTION|BATTLEMODEL_NO_RIDE_SETTLEMENT_LOCAL_NATIVE_PASS")
    if args.verify_runtime_model:
        print("RESOLUTION|BATTLEMODEL_PHYSICAL_MARKER_RUNTIME_MODEL_NATIVE_PASS")


if __name__ == "__main__":
    main()
