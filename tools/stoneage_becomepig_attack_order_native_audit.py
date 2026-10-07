#!/usr/bin/env python3
"""Controlled native composition for BecomePig ordinary attack ownership order R1.

Executes exact pinned reduced-profile physical AttackSeq/GuardianCheck and exact
DamageSub from the already accepted same-harness oracle, then adds exact original
BATTLE_Attack, BATTLE_Counter, BATTLE_TargetAdjust and the exact BecomePig
post-attack conditional. Counter eligibility, default-target selection and
presentation/network hooks are deliberately controlled seams.

No original source bytes are committed; only derived hashes and semantic rows
may be written to the repository.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re
import subprocess
import tempfile

from tools.stoneage_guard_break2_source_audit import PINNED, LAYOUTS, _text, _sha
from tools.stoneage_mdfyattack_source_audit import _definition, _strip
from tools.stoneage_becomepig_preaudit import postattack_block
from tools import stoneage_battlemodel_damagesub_profit_tail_source_audit as prior


RESOLUTION = (
    "BECOMEPIG_MAIN_GUARDIAN_COUNTER_RETARGET_NATIVE_COMPOSITION_PASS_"
    "ZERO_RUNTIME_PROMOTIONS"
)


def _trimmed_definition(text: str, name: str, return_token: str) -> str:
    raw = _definition(_strip(text), name, raw_window=True)
    at = raw.rfind(return_token)
    if at < 0:
        raise ValueError(f"{name}: final return token missing")
    end = raw.find("}", at + len(return_token))
    if end < 0:
        raise ValueError(f"{name}: closing brace missing after final return")
    return raw[: end + 1]


def _source_parts(name: str, root: Path) -> dict[str, str]:
    base = root / LAYOUTS[name]
    battle_path = base / "battle/battle.c"
    event_path = base / "battle/battle_event.c"
    battle = _text(battle_path).replace("char_index", "charaindex")
    event = _text(event_path).replace("char_index", "charaindex")
    return {
        "attack": _trimmed_definition(event, "BATTLE_Attack", "return iRet;"),
        "counter": _trimmed_definition(event, "BATTLE_Counter", "return iRet;"),
        "target_adjust": _trimmed_definition(
            battle, "BATTLE_TargetAdjust", "return defNo;"
        ),
        "postattack": postattack_block(battle),
        "battle_sha256": _sha(battle_path),
        "event_sha256": _sha(event_path),
    }


def _ensure_reduced_defines(head: str, extra: str) -> tuple[str, dict[str, int]]:
    existing_words = set(re.findall(r"\b[A-Za-z_]\w*\b", head))
    calls = set(re.findall(r"\b([A-Za-z_]\w*)\s*\(", extra))
    symbols = sorted(
        set(
            re.findall(
                r"\b(?:CHAR|BATTLE|BENT|ITEM|BCF|PETSKILL)_[A-Z][A-Z0-9_]*\b",
                extra,
            )
        )
    )
    fixed = {
        "BATTLE_COM_ATTACK": 77,
        "BATTLE_COM_S_NOGUARD": 78,
        "BATTLE_COM_S_BECOMEPIG": 79,
        "BCF_COUNTER": 1 << 4,
    }
    used_small = [
        int(x)
        for x in re.findall(r"^\s*#\s*define\s+\w+\s+(\d+)\s*$", head, re.M)
        if int(x) < 3900
    ]
    next_id = max([3000, *(x + 1 for x in used_small)])
    additions: list[str] = []
    assigned: dict[str, int] = {}
    for symbol in symbols:
        if symbol in existing_words or symbol in calls:
            continue
        if symbol in fixed:
            value = fixed[symbol]
        else:
            value = next_id
            next_id += 1
        additions.append(f"#define {symbol} {value}")
        assigned[symbol] = value
    for symbol, value in fixed.items():
        if symbol not in existing_words and symbol not in assigned:
            additions.append(f"#define {symbol} {value}")
            assigned[symbol] = value
    if next_id >= 4096:
        raise ValueError("native composition synthetic field keys exceed storage")
    return "\n".join(additions) + "\n", assigned


def _compose_source(name: str, root: Path) -> tuple[str, dict]:
    code, inherited = prior._same_harness_damage_source(name, root)
    main_at = code.rfind("int main(void){")
    if main_at < 0:
        raise ValueError("accepted exact-DamageSub harness main anchor missing")
    head = code[:main_at]

    parts = _source_parts(name, root)
    extra = "\n".join(
        (parts["attack"], parts["counter"], parts["target_adjust"], parts["postattack"])
    )
    defines, assigned = _ensure_reduced_defines(head, extra)

    # The accepted physical harness already executes the exact original
    # GuardianCheck. Rename that definition only, then interpose a transparent
    # recorder so this composition can prove which slot AttackSeq selected.
    renamed, count = re.subn(
        r"\b((?:static\s+)?int\s+)BATTLE_GuardianCheck\s*\(",
        r"\1BATTLE_GuardianCheck_EXACT(",
        head,
        count=1,
    )
    if count != 1:
        raise ValueError("exact GuardianCheck interposition anchor drift")
    head = (
        "static int native_last_guardian=-999,native_guardian_calls=0;\n"
        "int BATTLE_GuardianCheck(int,int);\n"
        + defines
        + renamed
    )
    helper_at = head.find("void BATTLE_BattleModel_ATTACK")
    if helper_at < 0:
        raise ValueError("accepted physical helper insertion anchor missing")
    recorder = r'''
int BATTLE_GuardianCheck(int attackindex,int defindex){
  native_guardian_calls++;
  native_last_guardian=BATTLE_GuardianCheck_EXACT(attackindex,defindex);
  return native_last_guardian;
}
'''
    head = head[:helper_at] + recorder + head[helper_at:]

    # Presentation is outside this gameplay-state witness. The accepted parent
    # harness intentionally aborts on print; make only that seam neutral here.
    abort_print = 'int print(char*fmt,...){hfail(36);return 0;}'
    if abort_print in head:
        head = head.replace(
            abort_print,
            'int print(char*fmt,...){(void)fmt;return 0;}',
            1,
        )

    controlled = r'''
static int native_counter_checks,native_default_target_calls,native_post_draws;
static int gBattleStausChange=-1,gBattleStausTurn=0;
#ifndef BATTLE_CHECKINDEX
#define BATTLE_CHECKINDEX(i) ((i)==0)
#endif
int BATTLE_CounterCheck(int attackindex,int defindex,int *per){
  (void)attackindex;(void)defindex;
  native_counter_checks++;
  if(per)*per=100;
  return TRUE;
}
int BATTLE_DefaultAttacker(int battleindex,int side){
  native_default_target_calls++;
  for(int p=0;p<SIDE_OFFSET;p++){
    int no=side*SIDE_OFFSET+p;
    if(BATTLE_TargetCheck(battleindex,no)==TRUE)return no;
  }
  return -1;
}
'''
    if not re.search(r"\bBATTLE_MagicEffect\s*\(", head):
        controlled += r'''
int BATTLE_MagicEffect(int b,int d,int *list,int a,int c){
  (void)b;(void)d;(void)list;(void)a;(void)c;return 0;
}
'''
    if not re.search(r"\bCHAR_talkToCli\s*\(", head):
        controlled += r'''
void CHAR_talkToCli(int i,int to,const char*s,int color){
  (void)i;(void)to;(void)s;(void)color;
}
'''
    if not re.search(r"\bCHAR_getChar\s*\(", head):
        controlled += r'''
char *CHAR_getChar(int i,int f){(void)i;(void)f;return "native-target";}
'''
    if not re.search(r"\bBATTLE_changeRideImage\s*\(", head):
        controlled += r'''
void BATTLE_changeRideImage(int i){(void)i;}
'''

    support = r'''
typedef struct {int Battle_Attack_ReturnData;} NativeAttackReturn;
static NativeAttackReturn Battle_Attack_ReturnData_x;
static int native_rand(void){native_post_draws++;return 0;}
#define rand native_rand

static void native_reset_trace(void){
  trace_length=0;trace[0]=0;
  attackseq_calls=damage_calls=target_checks=rand_calls=rngcount=0;
  native_guardian_calls=0;native_last_guardian=-999;
  native_counter_checks=native_default_target_calls=native_post_draws=0;
}

static void native_init_world(
    int owner_hp,int owner_guard_hp,int alt_hp,int enemy_hp,int enemy_guard_hp,
    int owner_guardian,int enemy_guardian){
  memset(ints,0,sizeof(ints));memset(works,0,sizeof(works));
  memset(flags,0,sizeof(flags));memset(valid,0,sizeof(valid));
  memset(pets,-1,sizeof(pets));memset(vectors,0,sizeof(vectors));
  memset(BattleArray,0,sizeof(BattleArray));
  for(int s=0;s<2;s++)for(int p=0;p<SIDE_OFFSET;p++){
    BattleArray[0].Side[s].Entry[p].charaindex=-1;
    BattleArray[0].Side[s].Entry[p].guardian=-1;
    BattleArray[0].Side[s].Entry[p].escape=7;
    for(int k=0;k<3;k++)BattleArray[0].Side[s].Entry[p].getitem[k]=-1;
  }
  valid[1]=valid[2]=valid[3]=valid[4]=valid[10]=1;
  BattleArray[0].Side[0].Entry[0].charaindex=1;
  BattleArray[0].Side[0].Entry[1].charaindex=4;
  BattleArray[0].Side[0].Entry[5].charaindex=2;
  BattleArray[0].Side[1].Entry[0].charaindex=10;
  BattleArray[0].Side[1].Entry[5].charaindex=3;
  BattleArray[0].type=BATTLE_TYPE_P_vs_E;
  BattleArray[0].norisk=1;BattleArray[0].field_att=0;BattleArray[0].att_pow=0;

  ints[1][CHAR_WHICHTYPE]=CHAR_TYPEPLAYER;
  ints[4][CHAR_WHICHTYPE]=CHAR_TYPEPLAYER;
  ints[2][CHAR_WHICHTYPE]=CHAR_TYPEPET;
  ints[3][CHAR_WHICHTYPE]=CHAR_TYPEPET;
  ints[10][CHAR_WHICHTYPE]=CHAR_TYPEENEMY;
  ints[1][CHAR_HP]=owner_hp;ints[2][CHAR_HP]=owner_guard_hp;
  ints[4][CHAR_HP]=alt_hp;ints[10][CHAR_HP]=enemy_hp;
  ints[3][CHAR_HP]=enemy_guard_hp;
  int ids[5]={1,2,3,4,10};
  for(int q=0;q<5;q++){
    int id=ids[q];
    ints[id][CHAR_LV]=20;
    works[id][CHAR_WORKMAXHP]=ints[id][CHAR_HP]>0?ints[id][CHAR_HP]:1;
    works[id][CHAR_WORKBATTLEINDEX]=0;
    works[id][CHAR_WORKBATTLECOM1]=BATTLE_COM_ATTACK;
    works[id][CHAR_WORKFIXDEX]=10;
    works[id][CHAR_WORKFIXLUCK]=0;
    works[id][CHAR_WORKDEFENCEPOWER]=40;
    works[id][CHAR_WORKQUICK]=40;
    works[id][CHAR_WORKFIXVITAL]=40;
    works[id][CHAR_WORKATTACKPOWER]=100;
    works[id][CHAR_WORKBATTLEFLG]|=CHAR_BATTLEFLG_NODUCK;
    vectors[id][4]=100;
    ints[id][CHAR_BECOMEPIG]=-1;
    ints[id][CHAR_BECOMEPIG_BBI]=100250;
    ints[id][CHAR_BASEIMAGENUMBER]=777;
    ints[id][CHAR_RIDEPET]=-1;
  }
  /* Give the requested defender and its counter-guardian deliberately
     different defence so the recorded Guardian choice is gameplay relevant. */
  works[10][CHAR_WORKDEFENCEPOWER]=400;
  works[3][CHAR_WORKDEFENCEPOWER]=5;
  works[10][CHAR_WORKFIXVITAL]=400;
  works[3][CHAR_WORKFIXVITAL]=5;

  if(owner_guardian){
    BattleArray[0].Side[0].Entry[0].guardian=5;
    works[2][CHAR_WORKBATTLEFLG]|=CHAR_BATTLEFLG_GUARDIAN;
  }
  if(enemy_guardian){
    BattleArray[0].Side[1].Entry[0].guardian=15;
    works[3][CHAR_WORKBATTLEFLG]|=CHAR_BATTLEFLG_GUARDIAN;
  }
  strcpy(option_buf,"100 60 100250");
  gDamageDiv=0.0;gBattleDuckModyfy=0;gBattleDamageModyfy=1.0;
  gCriticalPara=0.09;gWeponType=0;
  gBattleStausChange=-1;gBattleStausTurn=0;
  native_reset_trace();
}

static void native_apply_post(int defNo){
  int battleindex=0,charaindex=10;
  int COM=BATTLE_COM_S_BECOMEPIG;
  Battle_Attack_ReturnData_x.Battle_Attack_ReturnData=0;
'''

    post_tail = r'''
}

static void native_scenario_A(void){
  native_init_world(1000,1000,1000,1000,1000,1,0);
  works[10][CHAR_WORKBATTLECOM2]=0;
  int mainret=BATTLE_Attack(0,10,0);
  int main_guardian=native_last_guardian;
  int counterret=BATTLE_Counter(0,0,10);
  int counter_guardian=native_last_guardian;
  native_apply_post(0);
  printf("A %d %d %d %d %d %d %d %d %d %d %d|%s\n",
    mainret,main_guardian,counterret,counter_guardian,
    ints[1][CHAR_HP],ints[2][CHAR_HP],ints[10][CHAR_HP],
    ints[1][CHAR_BECOMEPIG],ints[2][CHAR_BECOMEPIG],
    ints[1][CHAR_BASEIMAGENUMBER],ints[2][CHAR_BASEIMAGENUMBER],trace);
}

static void native_scenario_B(void){
  native_init_world(1,1000,1000,1000,1000,0,0);
  works[10][CHAR_WORKBATTLECOM2]=0;
  int mainret=BATTLE_Attack(0,10,0);
  int defNo=BATTLE_TargetAdjust(0,10,1);
  native_apply_post(defNo);
  printf("B %d %d %d %d %d %d %d %d %d %d|%s\n",
    mainret,defNo,works[10][CHAR_WORKBATTLECOM2],native_default_target_calls,
    ints[1][CHAR_HP],ints[4][CHAR_HP],
    ints[1][CHAR_BECOMEPIG],ints[4][CHAR_BECOMEPIG],
    ints[1][CHAR_BASEIMAGENUMBER],ints[4][CHAR_BASEIMAGENUMBER],trace);
}

static void native_scenario_C(void){
  native_init_world(1000,1000,1000,1000,1000,0,1);
  int enemy_before=ints[10][CHAR_HP],guardian_before=ints[3][CHAR_HP];
  int counterret=BATTLE_Counter(0,0,10);
  printf("C %d %d %d %d %d %d %d|%s\n",
    counterret,native_last_guardian,native_guardian_calls,
    enemy_before,ints[10][CHAR_HP],guardian_before,ints[3][CHAR_HP],trace);
}

int main(void){
  native_scenario_A();
  native_scenario_B();
  native_scenario_C();
  return 0;
}
'''

    final = (
        head
        + "\n"
        + controlled
        + "\n"
        + parts["attack"]
        + "\n"
        + parts["counter"]
        + "\n"
        + parts["target_adjust"]
        + "\n"
        + support
        + parts["postattack"]
        + post_tail
    )
    return final, {
        **inherited,
        "battle_c_sha256": parts["battle_sha256"],
        "battle_event_c_sha256": parts["event_sha256"],
        "attack_body_sha256": hashlib.sha256(parts["attack"].encode()).hexdigest(),
        "counter_body_sha256": hashlib.sha256(parts["counter"].encode()).hexdigest(),
        "target_adjust_body_sha256": hashlib.sha256(
            parts["target_adjust"].encode()
        ).hexdigest(),
        "postattack_body_sha256": hashlib.sha256(
            parts["postattack"].encode()
        ).hexdigest(),
        "synthetic_defines": assigned,
    }


def _hp_ids(trace: str) -> list[int]:
    result = []
    for token in trace.rstrip(",").split(","):
        if token.startswith("H:"):
            _, ident, _ = token.split(":", 2)
            result.append(int(ident))
    return result


def _validate_rows(rows: list[str]) -> dict[str, int]:
    if len(rows) != 3:
        raise ValueError(f"native composition row count drift: {len(rows)}")
    parsed = {}
    traces = {}
    for line in rows:
        left, trace = line.split("|", 1)
        bits = left.split()
        parsed[bits[0]] = tuple(map(int, bits[1:]))
        traces[bits[0]] = trace
    if set(parsed) != {"A", "B", "C"}:
        raise ValueError("native composition scenario labels drift")

    a = parsed["A"]
    if len(a) != 11:
        raise ValueError("scenario A shape drift")
    (
        _mainret, main_guardian, _counterret, _counter_guardian,
        _owner_hp, _pet_hp, _enemy_hp, owner_pig, pet_pig,
        owner_image, pet_image,
    ) = a
    aid = _hp_ids(traces["A"])
    if main_guardian != 5:
        raise ValueError(f"scenario A main Guardian drift: {main_guardian}")
    if len(aid) < 2 or aid[0] != 2 or aid[1] != 10:
        raise ValueError(f"scenario A damage ownership drift: {aid}")
    if not (owner_pig >= 0 and pet_pig == -1):
        raise ValueError(
            f"scenario A post-effect ownership drift: owner={owner_pig}, pet={pet_pig}"
        )
    if not (owner_image == 100250 and pet_image == 777):
        raise ValueError("scenario A post-effect image ownership drift")

    b = parsed["B"]
    if len(b) != 10:
        raise ValueError("scenario B shape drift")
    (
        _mainret, final_defno, stored_defno, default_calls,
        owner_hp, _alt_hp, owner_pig, alt_pig, owner_image, alt_image,
    ) = b
    bid = _hp_ids(traces["B"])
    if not bid or bid[0] != 1 or owner_hp != 0:
        raise ValueError(f"scenario B lethal requested-target drift: {bid}, hp={owner_hp}")
    if final_defno != 1 or stored_defno != 1 or default_calls != 1:
        raise ValueError(
            "scenario B exact TargetAdjust did not replace dead requested target "
            f"with controlled live slot1: {b}"
        )
    if not (owner_pig == -1 and alt_pig >= 0):
        raise ValueError("scenario B final-defNo BecomePig ownership drift")
    if not (owner_image == 777 and alt_image == 100250):
        raise ValueError("scenario B final-defNo image ownership drift")

    c = parsed["C"]
    if len(c) != 7:
        raise ValueError("scenario C shape drift")
    (
        _counterret, counter_guardian, guardian_calls,
        enemy_before, enemy_after, guard_before, guard_after,
    ) = c
    cid = _hp_ids(traces["C"])
    if counter_guardian != 15 or guardian_calls < 1:
        raise ValueError(
            f"scenario C exact Counter AttackSeq Guardian selection drift: {c}"
        )
    if not cid or cid[0] != 10:
        raise ValueError(
            "scenario C counter DamageSub recipient normalized to Guardian; "
            f"HP writes={cid}"
        )
    if not (enemy_after < enemy_before and guard_after == guard_before):
        raise ValueError(
            "scenario C Guardian influenced AttackSeq but counter caller recipient "
            f"was not original defender: {c}"
        )
    return {
        "main_guardian_recipient_cases": 1,
        "retarget_posteffect_cases": 1,
        "counter_guardian_distinction_cases": 1,
    }


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

    source, meta = _compose_source(name, root)
    baseline = None
    summary = None
    for optimization in ("-O0", "-O2"):
        with tempfile.TemporaryDirectory(
            prefix=f"sa-becomepig-attack-order-{name}-"
        ) as folder:
            c_path = Path(folder) / "oracle.c"
            binary = Path(folder) / "oracle"
            c_path.write_text(source, encoding="utf-8")
            built = subprocess.run(
                [
                    "cc", "-std=c11", optimization,
                    "-fsanitize=undefined", "-fno-sanitize-recover=all",
                    "-Wno-unused-value", "-Wno-unused-variable",
                    str(c_path), "-lm", "-o", str(binary),
                ],
                capture_output=True, text=True,
            )
            if built.returncode:
                raise ValueError(
                    f"{name}/{optimization}: native composition compile failed: "
                    + built.stderr[-16000:]
                )
            run = subprocess.run(
                [str(binary)], capture_output=True, text=True
            )
            if run.returncode or run.stderr:
                raise ValueError(
                    f"{name}/{optimization}: native composition execution/UBSan "
                    f"failed rc={run.returncode}; stderr={run.stderr[-6000:]}; "
                    f"stdout={run.stdout[-6000:]}"
                )
            rows = run.stdout.splitlines()
        current = _validate_rows(rows)
        if baseline is None:
            baseline = rows
            summary = current
        elif rows != baseline:
            raise ValueError(f"{name}: O0/O2 semantic row drift")

    return {
        "profile": name,
        "commit": head,
        "optimizations": 2,
        "native_scenarios_per_optimization": 3,
        "native_comparisons": 6,
        **(summary or {}),
        "battle_c_sha256": meta["battle_c_sha256"],
        "battle_event_c_sha256": meta["battle_event_c_sha256"],
        "attack_body_sha256": meta["attack_body_sha256"],
        "counter_body_sha256": meta["counter_body_sha256"],
        "target_adjust_body_sha256": meta["target_adjust_body_sha256"],
        "postattack_body_sha256": meta["postattack_body_sha256"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    for name in PINNED:
        parser.add_argument("--" + name + "-dir", required=True, type=Path)
    args = parser.parse_args()

    print("StoneAge BecomePig main/Guardian/counter/retarget native composition R1")
    total = 0
    for name in PINNED:
        row = analyze_profile(name, getattr(args, name + "_dir"))
        total += row["native_comparisons"]
        print(
            "PROFILE|"
            + "|".join(f"{key}={value}" for key, value in row.items())
        )
    print(f"TOTAL|native_comparisons={total}|profiles={len(PINNED)}")
    print("FACT|exact_ordinary_Attack_AttackSeq_Guardian_and_exact_DamageSub_route_main_hit_to_Guardian")
    print("FACT|exact_TargetAdjust_replaces_dead_requested_target_and_BecomePig_posteffect_uses_final_defNo")
    print("FACT|exact_Counter_AttackSeq_can_select_Guardian_while_counter_caller_DamageSub_still_hits_original_defender")
    print("BOUNDARY|reduced_feature_profile_controlled_CounterCheck_DefaultAttacker_presentation_rng_and_no_item_ride_status_sideeffects")
    print("BOUNDARY|pinned_descendant_native_composition_only_no_historical_build_ABI_PRNG_or_runtime_promotion")
    print(f"RESOLUTION|{RESOLUTION}")


if __name__ == "__main__":
    main()
