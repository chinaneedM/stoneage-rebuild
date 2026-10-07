#!/usr/bin/env python3
"""Native default-feature composition for BecomePig with item/NPC/map timers R1.

Exact original conditional blocks are extracted transiently from each pinned
source profile. Repository output stores only independent tooling, hashes and
derived semantic rows; original source bytes are never committed.
"""
from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import re
import subprocess
import tempfile

from tools.stoneage_guard_break2_source_audit import PINNED, LAYOUTS, _text, _sha
from tools.stoneage_mdfyattack_source_audit import _definition, _strip
from tools.stoneage_becomepig_native_audit import _if_with, _features


RESOLUTION = (
    "BECOMEPIG_ITEM_NPC_MAP_TIMER_NATIVE_COMPOSITION_PASS_"
    "ZERO_RUNTIME_PROMOTIONS"
)
REQUIRED_FEATURES = {
    "_ITEM_METAMO",
    "_NPCCHANGE_PLAYERIMG",
    "_MAP_TIME",
    "_ITEM_UNBECOMEPIG",
    "_FIXBUG_ATTACKBOW",
    "_PETSKILL_BECOMEPIG",
}


def _net_path(name: str, root: Path) -> Path:
    base = root / LAYOUTS[name]
    return base / ("net/net.c" if name == "bismarck" else "net.c")


def _compact(text: str) -> str:
    return re.sub(r"\s+", "", _strip(text))


def _parts(name: str, root: Path) -> dict[str, str]:
    base = root / LAYOUTS[name]
    net_path = _net_path(name, root)
    item_path = base / "item/item_event.c"
    npc_path = base / "npc/npc_eventaction.c"
    net = _text(net_path).replace("char_index", "charaindex")
    item = _text(item_path).replace("char_index", "charaindex")
    npc = _text(npc_path).replace("char_index", "charaindex")

    item_fn = _definition(item, "ITEM_metamo", raw_window=True)
    recovery_fn = _definition(item, "ITEM_useRecovery_Field", raw_window=True)
    npc_fn = _definition(npc, "NPC_ActionChangePlayerBBI", raw_window=True)

    item_guard = _if_with(
        item_fn,
        r"if\s*\(\s*CHAR_getInt\s*\(\s*charaindex\s*,\s*CHAR_BECOMEPIG\s*\)\s*>\s*-1\s*\)",
        "CHAR_BECOMEPIG",
    )
    npc_guard = _if_with(
        npc_fn,
        r"if\s*\(\s*CHAR_getInt\s*\(\s*charindex\s*,\s*CHAR_BECOMEPIG\s*\)\s*>\s*-1\s*\)",
        "CHAR_BECOMEPIG",
    )
    recovery = _if_with(
        recovery_fn,
        r"if\s*\(\s*CHAR_getInt\s*\(\s*toindex\s*,\s*CHAR_BECOMEPIG\s*\)\s*>\s*-1\s*\)",
        "CHAR_DelItemMess",
    )
    item_timer = _if_with(
        net,
        r"if\s*\(\s*CHAR_getWorkInt\s*\([^;{}]*CHAR_WORKITEMMETAMO",
        "CHAR_WORKNPCMETAMO",
    )
    map_timer = _if_with(
        net,
        r"if\s*\(\s*CHAR_getWorkInt\s*\([^)]*CHAR_WORK_MAP_TIME[^)]*\)\s*>\s*0",
        "CHAR_warpToSpecificPoint",
    )

    item_compact = _compact(item_fn)
    npc_compact = _compact(npc_fn)
    recovery_fn_compact = _compact(recovery_fn)
    recovery_compact = _compact(recovery)
    item_timer_compact = _compact(item_timer)
    map_timer_compact = _compact(map_timer)

    item_pig = item_compact.find("CHAR_BECOMEPIG")
    item_set = item_compact.find("CHAR_setWorkInt(charaindex,CHAR_WORKITEMMETAMO", item_pig + 1)
    npc_pig = npc_compact.find("CHAR_BECOMEPIG")
    npc_item_clear = npc_compact.find("CHAR_setWorkInt(charindex,CHAR_WORKITEMMETAMO,0", npc_pig + 1)
    npc_set = npc_compact.find("CHAR_setWorkInt(charindex,CHAR_WORKNPCMETAMO", npc_pig + 1)
    net_item_pos = net.find(item_timer)
    net_map_pos = net.find(map_timer)

    static = {
        "item_pig_guard_before_item_metamorph_write":
            item_pig >= 0 and item_set > item_pig,
        "npc_pig_guard_before_item_clear_and_npc_metamorph_write":
            npc_pig >= 0 and npc_item_clear > npc_pig and npc_set > npc_item_clear,
        "recovery_keyword_gate_precedes_active_pig_clear":
            recovery_fn_compact.find("strstr(arg,") >= 0
            and recovery_fn_compact.find("strstr(arg,")
            < recovery_fn_compact.find("CHAR_getInt(toindex,CHAR_BECOMEPIG"),
        "recovery_clears_pig_before_compliance_and_item_consumption":
            recovery_compact.find("CHAR_setInt(toindex,CHAR_BECOMEPIG,-1)") >= 0
            and recovery_compact.find("CHAR_setInt(toindex,CHAR_BECOMEPIG,-1)")
            < recovery_compact.find("CHAR_complianceParameter(toindex)")
            < recovery_compact.find("CHAR_DelItemMess(charaindex,haveitemindex,0)"),
        "item_timeout_clears_item_and_npc_then_compliance":
            item_timer_compact.find("CHAR_setWorkInt")
            < item_timer_compact.find("CHAR_WORKNPCMETAMO")
            < item_timer_compact.find("CHAR_complianceParameter"),
        "map_timer_battle_guard_decrements_by10_then_warp_hp1_charmminus3":
            all(
                token in map_timer_compact
                for token in (
                    "CHAR_WORKBATTLEMODE",
                    "BATTLE_CHARMODE_NONE",
                    "CHAR_WORK_MAP_TIME)-10",
                    "CHAR_warpToSpecificPoint",
                    "30008",
                    "39",
                    "38",
                    "CHAR_HP,1",
                    "CHAR_AddCharm",
                    "-3",
                )
            ),
        "item_timer_precedes_map_timer_in_system_loop":
            net_item_pos >= 0 and net_map_pos > net_item_pos,
    }
    if not all(static.values()):
        raise ValueError(f"{name}: item/NPC/map source-order drift: {static}")

    return {
        "item_guard": item_guard,
        "npc_guard": npc_guard,
        "recovery": recovery,
        "item_timer": item_timer,
        "map_timer": map_timer,
        "net_sha256": _sha(net_path),
        "item_sha256": _sha(item_path),
        "npc_sha256": _sha(npc_path),
        "item_guard_sha256": hashlib.sha256(item_guard.encode()).hexdigest(),
        "npc_guard_sha256": hashlib.sha256(npc_guard.encode()).hexdigest(),
        "recovery_sha256": hashlib.sha256(recovery.encode()).hexdigest(),
        "item_timer_sha256": hashlib.sha256(item_timer.encode()).hexdigest(),
        "map_timer_sha256": hashlib.sha256(map_timer.encode()).hexdigest(),
        **static,
    }


def expected_rows() -> list[tuple[int, ...]]:
    # G: active pig blocks both item and NPC metamorph guards.
    g = (5, 0, 0, 2)
    # R: cure clears pig, calls compliance, consumes item; both guards then fall through.
    r = (-1, 1, 1, 1, 1, 1)
    # T: expired item metamorph and expiring map timer execute in source order.
    t = (0, 0, 5, 1, 0, 1, 1, -3, 2)
    # E: strict item expiry (< now), equality does not clear.
    e = (100, 7, 5, 0)
    # B: map timer pauses while battle mode is non-NONE.
    b = (10, 5, 0, 0)
    return [g, r, t, e, b]


def _source(name: str, root: Path) -> tuple[str, dict]:
    active = _features(name, root)
    missing = REQUIRED_FEATURES - active
    if missing:
        raise ValueError(f"{name}: required default features disabled: {sorted(missing)}")
    p = _parts(name, root)

    prefix = r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>
typedef int BOOL;
#define TRUE 1
#define FALSE 0
#define BATTLE_CHARMODE_NONE 0
#define BATTLE_CHARMODE_BATTLE 1
#define CHAR_BECOMEPIG 1
#define CHAR_HP 2
#define CHAR_WORKITEMMETAMO 10
#define CHAR_WORKNPCMETAMO 11
#define CHAR_WORKOBJINDEX 12
#define CHAR_WORK_MAP_TIME 13
#define CHAR_WORKBATTLEMODE 14
#define CHAR_P_STRING_BASEBASEIMAGENUMBER 20
#define CHAR_P_STRING_HP 21
#define CHAR_P_STRING_CHARM 22
#define CHAR_COLORWHITE 1
#define CHAR_COLORRED 2
#define CHAR_COLORYELLOW 3

typedef struct {int use;int charaindex;} NativeConnect;
static NativeConnect Connect[1];
static struct timeval NowTime;
static int ints[8][64],works[8][64];
static int compliance_calls,sendc_calls,sendp_calls,talk_calls,delete_calls;
static int warp_calls,warp_floor,warp_x,warp_y,charm_delta;
static int item_fallthrough,npc_fallthrough;

int CHAR_getInt(int i,int f){return ints[i][f];}
int CHAR_setInt(int i,int f,int v){return ints[i][f]=v;}
int CHAR_getWorkInt(int i,int f){return works[i][f];}
int CHAR_setWorkInt(int i,int f,int v){return works[i][f]=v;}
void CHAR_complianceParameter(int i){(void)i;compliance_calls++;}
void CHAR_sendCToArroundCharacter(int i){(void)i;sendc_calls++;}
void CHAR_send_P_StatusString(int i,int f){(void)i;(void)f;sendp_calls++;}
void CHAR_talkToCli(int i,int to,const char *s,int color){(void)i;(void)to;(void)s;(void)color;talk_calls++;}
void CHAR_DelItemMess(int i,int slot,int flag){(void)i;(void)slot;(void)flag;delete_calls++;}
int CHAR_warpToSpecificPoint(int i,int f,int x,int y){(void)i;warp_calls++;warp_floor=f;warp_x=x;warp_y=y;return 1;}
int CHAR_AddCharm(int i,int delta){(void)i;charm_delta+=delta;return charm_delta;}

static void reset_state(void){
  memset(ints,0,sizeof(ints));memset(works,0,sizeof(works));
  Connect[0].use=1;Connect[0].charaindex=1;NowTime.tv_sec=100;
  compliance_calls=sendc_calls=sendp_calls=talk_calls=delete_calls=0;
  warp_calls=warp_floor=warp_x=warp_y=charm_delta=0;
  item_fallthrough=npc_fallthrough=0;
  ints[1][CHAR_HP]=99;
  works[1][CHAR_WORKOBJINDEX]=123;
}
'''

    wrappers = r'''
static void item_guard_probe(void){
  int charaindex=1;
''' + p["item_guard"] + r'''
  item_fallthrough++;
}

static int npc_guard_probe(void){
  int charindex=1;
''' + p["npc_guard"] + r'''
  npc_fallthrough++;
  return TRUE;
}

static void recovery_probe(void){
  int charaindex=1,toindex=1,haveitemindex=0;
''' + p["recovery"] + r'''
}

static void item_timer_probe(void){
  int i=0,charaindex=1;
  (void)charaindex;
''' + p["item_timer"] + r'''
}

static void map_timer_probe(void){
  int i=0,charaindex=1;
  (void)charaindex;
''' + p["map_timer"] + r'''
}

int main(void){
  reset_state();
  ints[1][CHAR_BECOMEPIG]=5;
  item_guard_probe();
  (void)npc_guard_probe();
  printf("G %d %d %d %d\n",ints[1][CHAR_BECOMEPIG],item_fallthrough,npc_fallthrough,talk_calls);

  reset_state();
  ints[1][CHAR_BECOMEPIG]=5;
  recovery_probe();
  item_guard_probe();
  (void)npc_guard_probe();
  printf("R %d %d %d %d %d %d\n",ints[1][CHAR_BECOMEPIG],compliance_calls,delete_calls,
    item_fallthrough,npc_fallthrough,talk_calls);

  reset_state();
  ints[1][CHAR_BECOMEPIG]=5;
  works[1][CHAR_WORKITEMMETAMO]=90;
  works[1][CHAR_WORKNPCMETAMO]=7;
  works[1][CHAR_WORK_MAP_TIME]=10;
  works[1][CHAR_WORKBATTLEMODE]=BATTLE_CHARMODE_NONE;
  item_timer_probe();
  map_timer_probe();
  printf("T %d %d %d %d %d %d %d %d %d\n",
    works[1][CHAR_WORKITEMMETAMO],works[1][CHAR_WORKNPCMETAMO],ints[1][CHAR_BECOMEPIG],
    compliance_calls,works[1][CHAR_WORK_MAP_TIME],warp_calls,ints[1][CHAR_HP],charm_delta,talk_calls);

  reset_state();
  ints[1][CHAR_BECOMEPIG]=5;
  works[1][CHAR_WORKITEMMETAMO]=100;
  works[1][CHAR_WORKNPCMETAMO]=7;
  item_timer_probe();
  printf("E %d %d %d %d\n",works[1][CHAR_WORKITEMMETAMO],works[1][CHAR_WORKNPCMETAMO],
    ints[1][CHAR_BECOMEPIG],compliance_calls);

  reset_state();
  ints[1][CHAR_BECOMEPIG]=5;
  works[1][CHAR_WORK_MAP_TIME]=10;
  works[1][CHAR_WORKBATTLEMODE]=BATTLE_CHARMODE_BATTLE;
  map_timer_probe();
  printf("B %d %d %d %d\n",works[1][CHAR_WORK_MAP_TIME],ints[1][CHAR_BECOMEPIG],
    warp_calls,charm_delta);
  return 0;
}
'''
    return prefix + wrappers, p


def _parse_rows(stdout: str) -> list[tuple[int, ...]]:
    expected_labels = ["G", "R", "T", "E", "B"]
    lines = stdout.splitlines()
    if len(lines) != len(expected_labels):
        raise ValueError(f"native row count drift: {len(lines)}")
    rows = []
    for label, line in zip(expected_labels, lines):
        bits = line.split()
        if not bits or bits[0] != label:
            raise ValueError(f"native row label drift: {line!r}")
        rows.append(tuple(map(int, bits[1:])))
    return rows


def analyze_profile(name: str, root: Path) -> dict:
    root = root.resolve()
    head = subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", "HEAD"], text=True
    ).strip()
    dirty = subprocess.check_output(
        ["git", "-C", str(root), "status", "--porcelain"], text=True
    ).strip()
    if head != PINNED[name] or dirty:
        raise ValueError(f"{name}: pinned source commit/tree drift")

    source, meta = _source(name, root)
    expected = expected_rows()
    baseline = None
    for optimization in ("-O0", "-O2"):
        with tempfile.TemporaryDirectory(prefix=f"sa-becomepig-item-npc-map-{name}-") as folder:
            cpath = Path(folder) / "oracle.c"
            binary = Path(folder) / "oracle"
            cpath.write_text(source, encoding="utf-8")
            built = subprocess.run(
                [
                    "cc", "-std=c11", optimization, "-g", "-fno-omit-frame-pointer",
                    "-fsanitize=address,undefined", "-fno-sanitize-recover=all",
                    "-Wno-return-type", str(cpath), "-o", str(binary),
                ],
                capture_output=True, text=True,
            )
            if built.returncode:
                raise ValueError(
                    f"{name}/{optimization}: compile failed: {built.stderr[-12000:]}"
                )
            run = subprocess.run(
                [str(binary)], capture_output=True, text=True,
                env={
                    **os.environ,
                    "ASAN_OPTIONS": "detect_leaks=0:abort_on_error=1:symbolize=1",
                },
            )
            if run.returncode or run.stderr:
                raise ValueError(
                    f"{name}/{optimization}: execution/ASan/UBSan failed rc={run.returncode}; "
                    f"stderr={run.stderr[-6000:]}; stdout={run.stdout[-6000:]}"
                )
            rows = _parse_rows(run.stdout)
        if rows != expected:
            raise ValueError(f"{name}/{optimization}: semantic rows drift: {rows} != {expected}")
        if baseline is None:
            baseline = rows
        elif rows != baseline:
            raise ValueError(f"{name}: O0/O2 semantic drift")

    return {
        "profile": name,
        "commit": head,
        "optimizations": 2,
        "scenarios_per_optimization": len(expected),
        "native_comparisons": 2 * len(expected),
        "net_sha256": meta["net_sha256"],
        "item_sha256": meta["item_sha256"],
        "npc_sha256": meta["npc_sha256"],
        "item_guard_sha256": meta["item_guard_sha256"],
        "npc_guard_sha256": meta["npc_guard_sha256"],
        "recovery_sha256": meta["recovery_sha256"],
        "item_timer_sha256": meta["item_timer_sha256"],
        "map_timer_sha256": meta["map_timer_sha256"],
        "item_pig_guard_before_item_metamorph_write":
            meta["item_pig_guard_before_item_metamorph_write"],
        "npc_pig_guard_before_item_clear_and_npc_metamorph_write":
            meta["npc_pig_guard_before_item_clear_and_npc_metamorph_write"],
        "item_timer_precedes_map_timer_in_system_loop":
            meta["item_timer_precedes_map_timer_in_system_loop"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    for name in PINNED:
        parser.add_argument("--" + name + "-dir", type=Path, required=True)
    args = parser.parse_args()

    print("StoneAge BecomePig item/NPC/map timer native composition R1")
    total = 0
    for name in PINNED:
        row = analyze_profile(name, getattr(args, name + "_dir"))
        total += row["native_comparisons"]
        print(
            "PROFILE|"
            + "|".join(
                f"{k}={int(v) if isinstance(v, bool) else v}"
                for k, v in row.items()
            )
        )
    print(f"TOTAL|native_comparisons={total}|profiles={len(PINNED)}")
    print("FACT|active_BecomePig_blocks_item_and_NPC_metamorph_before_their_state_writes")
    print("FACT|unpig_recovery_clears_BecomePig_then_compliance_and_item_consumption_then_metamorph_guards_fall_through")
    print("FACT|expired_item_metamorph_clears_item_and_NPC_metamorph_but_preserves_BecomePig_and_calls_compliance")
    print("FACT|map_timer_decrements_by10_only_outside_battle_and_on_expiry_warps_sets_HP1_and_charm_minus3_without_direct_BecomePig_write")
    print("FACT|item_metamorph_timeout_precedes_map_timer_block_in_default_system_loop")
    print("BOUNDARY|exact_original_conditional_blocks_with_controlled_compliance_presentation_item_lookup_and_warp_implementation")
    print("BOUNDARY|pinned_descendant_default_feature_native_composition_only_no_historical_build_PRNG_or_runtime_promotion")
    print(f"RESOLUTION|{RESOLUTION}")


if __name__ == "__main__":
    main()
