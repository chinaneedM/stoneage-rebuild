"""Full original BATTLE_Battling -> BattleModel -> profit-tail native audit R1.

This is the next strengthening step after the accepted same-harness exact
DamageSub witness.  It keeps the exact pinned BATTLE_Battling function with its
original preprocessor context, enables only the already-admitted
_PETSKILL_BATTLE_MODEL path, and executes that command driver in the same
transient program as exact Guardian/AttackSeq, exact DamageSub, exact
BattleModel/helper and exact tail AddProfit.

The first implementation deliberately keeps scheduler/status/presentation
helpers controlled.  Those seams are fail-closed or neutral and are reported
explicitly; they are not historical certificates.  The gate is accepted only
when the exact command-driver body itself executes and its gameplay chronology
matches the immutable profit/exit scan used by prior milestones.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
from pathlib import Path
import re
import subprocess
import tempfile

from tools.stoneage_guard_break2_source_audit import (
    PINNED, LAYOUTS, _text, _sha, _function,
)
from tools import stoneage_battlemodel_damagesub_profit_tail_source_audit as prior


CONTROLLED_DRIVER_HELPERS = (
    "BATTLE_DexCalc",
    "EntrySort",
    "ComboCheck",
    "BATTLE_StatusSeq",
    "BATTLE_GetAttackCount",
    "BATTLE_PetLoyalCheck",
    "BATTLE_TargetListSet",
    "BATTLE_CountAlive",
    "BATTLE_CommandSend",
)


def _exact_battling(name: str, root: Path):
    path = root / LAYOUTS[name] / "battle/battle.c"
    text = _text(path)
    body = _function(text, "static int BATTLE_Battling")
    compact = re.sub(r"/\*.*?\*/|//[^\n]*|\s+", "", body, flags=re.S)
    case = (
        "#ifdef_PETSKILL_BATTLE_MODEL"
        "caseBATTLE_COM_S_BATTLE_MODEL:"
        "BATTLE_BattleModel(battleindex,attackNo,myside);break;"
        "#endif"
    )
    if case not in compact:
        raise ValueError("full Battling BattleModel conditional case drift")
    case_at = compact.index("caseBATTLE_COM_S_BATTLE_MODEL:")
    tail_at = compact.find(
        "BATTLESTR_ADD(szBadStatusString);"
        "BATTLE_AddProfit(battleindex,aAttackList);",
        case_at,
    )
    if tail_at < 0 or tail_at <= case_at:
        raise ValueError("full Battling common AddProfit tail drift")
    return body, _sha(path), sha256(body.encode()).hexdigest()


def _replace_once(code: str, old: str, new: str, label: str) -> str:
    if code.count(old) != 1:
        raise ValueError(f"{label} anchor drift: count={code.count(old)}")
    return code.replace(old, new, 1)


def _missing_defines(code: str, battling: str) -> str:
    existing = set(re.findall(r"^#define\s+(\w+)\b", code, re.M))
    calls = set(re.findall(r"\b([A-Za-z_]\w*)\s*\(", battling))
    tokens = set(re.findall(
        r"\b(?:CHAR|BATTLE|BENT|BSIDE|ITEM|TARGET|PETSKILL|PET|BCF|AI|CH)_[A-Z][A-Z0-9_]*\b",
        battling,
    ))
    type_names = {"BATTLE", "BATTLE_ENTRY", "BATTLE_SIDE", "BATTLE_CHARLIST"}
    fixed = {
        "BATTLE_CHARMODE_C_OK": 2801,
        "BATTLE_CHARMODE_RESCUE": 2802,
        "BATTLE_ATTR_NONE": 0,
        "ITEM_FIST": 0,
        "ITEM_BREAKTHROW": 2803,
        "BSIDE_FLG_SURPRISE": 1 << 0,
        "CHAR_COLORYELLOW": 1,
        "PET_STAT_SELECT": 1,
    }
    numeric = [
        int(x)
        for x in re.findall(r"^#define\s+\w+\s+(\d+)\s*$", code, re.M)
        if int(x) < 4000
    ]
    next_id = max([2804, *(x + 1 for x in numeric)])
    out = []
    for symbol, value in fixed.items():
        if symbol not in existing:
            out.append(f"#define {symbol} {value}")
            existing.add(symbol)
    for symbol in sorted(tokens):
        if symbol in existing or symbol in calls or symbol in type_names:
            continue
        out.append(f"#define {symbol} {next_id}")
        existing.add(symbol)
        next_id += 1
    if next_id >= 4096:
        raise ValueError(
            f"full Battling synthetic getter/command keys exceed storage: {next_id}"
        )
    return "\n".join(out) + "\n"


def _missing_call_stubs(code: str, battling: str) -> str:
    macros = set(re.findall(r"^#define\s+(\w+)\b", code, re.M))
    defined = set(re.findall(
        r"\b(?:static\s+)?(?:(?:int|void|BOOL|float)\s+|char\s*\*\s*)"
        r"([A-Za-z_]\w*)\s*\([^;{}]*\)\s*\{",
        code,
        re.S,
    ))
    calls = set(re.findall(r"\b([A-Za-z_]\w*)\s*\(", battling))
    skip = {
        "if", "for", "while", "switch", "sizeof",
        "sprintf", "snprintf", "printf", "sscanf",
        "memset", "memcpy", "memmove", "strcat", "strncat", "strlen",
        "strcpy", "strncpy", "strcmp", "strncmp", "strstr", "strchr",
        "atoi", "atol", "abs", "qsort", "rand", "time",
        *CONTROLLED_DRIVER_HELPERS,
        "BATTLE_Battling", "PETSKILL_getChar",
    }
    lines = []
    for name in sorted(calls - defined - macros - skip):
        lines.append(f"int {name}(){{return 0;}}")
    return "\n".join(lines) + "\n"


def _full_source(name: str, root: Path):
    code, meta = prior._same_harness_damage_source(name, root)
    battling, battle_sha, battling_sha = _exact_battling(name, root)

    old_entry = (
        "typedef struct {union {int charaindex;int char_index;};"
        "int escape,flg,getitem[3],guardian;} BATTLE_ENTRY;"
    )
    new_entry = (
        "typedef struct {union {int charaindex;int char_index;};"
        "int escape,flg,getitem[3],guardian,bid;} BATTLE_ENTRY;"
    )
    code = _replace_once(code, old_entry, new_entry, "full Battling entry layout")

    old_side = "typedef struct {int type;BATTLE_ENTRY Entry[10];} BATTLE_SIDE;"
    new_side = "typedef struct {int type,flg;BATTLE_ENTRY Entry[10];} BATTLE_SIDE;"
    code = _replace_once(code, old_side, new_side, "full Battling side layout")

    old_battle = (
        "typedef struct {int dpbattle,type,norisk,use,field_att,att_pow; "
        "BATTLE_SIDE Side[2];} BATTLE;"
    )
    new_battle = """typedef struct BATTLE_TAG {
  int dpbattle,type,norisk,use,field_att,att_pow,att_count,turn,mode,flgTime;
  int iEntryBack[20],iEntryBack2[20];
  int ice_array[20],ice_attackNo[20],ice_bout[20],ice_charaindex[20],
      ice_char_index[20],ice_count,ice_level[20],ice_toNo[20],ice_use[20];
  struct BATTLE_TAG *pNext;
  BATTLE_SIDE Side[2];
} BATTLE;"""
    code = _replace_once(code, old_battle, new_battle, "full Battling battle layout")

    main_at = code.rfind("int main(void){")
    if main_at < 0:
        raise ValueError("same-harness main anchor drift")
    head = code[:main_at]
    main = code[main_at:]

    driver_types = r'''
#define arraysizeof(a) ((int)(sizeof(a)/sizeof((a)[0])))
typedef struct {
  union {int charaindex;int char_index;};
  int side,dex,num,combo,sequence;
} BATTLE_CHARLIST;
static char szBattleString[65536],szAllBattleString[65536],szBadStatusString[65536];
static char *pszBattleTop=szBattleString,*pszBattleLast=szBattleString+sizeof(szBattleString);
static int gBattleStausChange,gBattleStausTurn,gWeponType;
static int BoomerangVsTbl[20][20];
'''
    controlled = r'''
int BATTLE_DexCalc(int c){return CHAR_getWorkInt(c,CHAR_WORKQUICK);}
void EntrySort(BATTLE_CHARLIST *list,int n){(void)list;(void)n;}
void ComboCheck(BATTLE_CHARLIST *list,int n){(void)list;(void)n;}
int BATTLE_StatusSeq(int c){(void)c;return 0;}
int BATTLE_GetAttackCount(int c){(void)c;return 1;}
int BATTLE_PetLoyalCheck(int b,int no,int c){(void)b;(void)no;(void)c;return 0;}
int BATTLE_TargetListSet(int c,int no,int*out){
  (void)c;(void)no;if(out){out[0]=-1;}return 0;
}
int BATTLE_CountAlive(int b,int side){
  int alive=0;
  for(int p=0;p<10;p++){
    int id=BattleArray[b].Side[side].Entry[p].charaindex;
    if(CHAR_CHECKINDEX(id)&&CHAR_getInt(id,CHAR_HP)>0&&!CHAR_getFlg(id,CHAR_ISDIE))alive++;
  }
  return alive;
}
int BATTLE_CommandSend(int c,char*s){(void)c;(void)s;return 0;}
'''

    defines = _missing_defines(head + driver_types, battling)
    stubs = _missing_call_stubs(head + driver_types + controlled, battling)

    main = _replace_once(
        main,
        "BattleArray[0].Side[s].Entry[p].guardian=-1;",
        "BattleArray[0].Side[s].Entry[p].guardian=-1;"
        "BattleArray[0].Side[s].Entry[p].bid=s*10+p;",
        "full Battling bid initialization",
    )
    reset_anchor = (
        "BattleArray[0].use=TRUE;BattleArray[0].dpbattle=0;"
        "BattleArray[0].type=BATTLE_TYPE_P_vs_E;"
    )
    reset_extra = (
        reset_anchor
        + "BattleArray[0].field_att=BATTLE_ATTR_NONE;BattleArray[0].turn=1;"
        + "BattleArray[0].pNext=NULL;"
        + "for(int q=0;q<20;q++){BattleArray[0].iEntryBack[q]=-1;"
        + "BattleArray[0].iEntryBack2[q]=-1;}"
    )
    main = _replace_once(
        main, reset_anchor, reset_extra, "full Battling battle reset"
    )

    old_modes = (
        "works[1][CHAR_WORKBATTLEMODE]=works[2][CHAR_WORKBATTLEMODE]="
        "works[10][CHAR_WORKBATTLEMODE]=BATTLE_CHARMODE_BATTLE;"
    )
    new_modes = (
        "works[1][CHAR_WORKBATTLEMODE]=works[2][CHAR_WORKBATTLEMODE]="
        "BATTLE_CHARMODE_BATTLE;"
        "works[10][CHAR_WORKBATTLEMODE]=BATTLE_CHARMODE_C_OK;"
    )
    main = _replace_once(main, old_modes, new_modes, "full Battling mode setup")

    old_commands = (
        "works[1][CHAR_WORKBATTLECOM1]=works[2][CHAR_WORKBATTLECOM1]="
        "works[10][CHAR_WORKBATTLECOM1]=77;"
    )
    new_commands = (
        "works[1][CHAR_WORKBATTLECOM1]=works[2][CHAR_WORKBATTLECOM1]="
        "BATTLE_COM_NONE;"
        "works[10][CHAR_WORKBATTLECOM1]=BATTLE_COM_S_BATTLE_MODEL;"
    )
    main = _replace_once(
        main, old_commands, new_commands, "full Battling command setup"
    )

    old_dispatch = """    int battleindex=0,attackNo=10,myside=1;
    int aAttackList[2]={10,-1};char szBadStatusString[2]={0};
    BATTLE_BattleModel(battleindex,attackNo,myside);
    BATTLESTR_ADD(szBadStatusString);
    if(BATTLE_AddProfit(battleindex,aAttackList)!=BATTLE_ERR_NONE)hfail(40);
    int first_deaths=ints[1][CHAR_DEADCOUNT]+ints[2][CHAR_DEADCOUNT];
"""
    new_dispatch = """    int battleindex=0;
    int aAttackList[2]={10,-1};
    int battling_rc=BATTLE_Battling(battleindex);
    if(battling_rc!=BATTLE_ERR_NONE)hfail(40);
    int first_deaths=ints[1][CHAR_DEADCOUNT]+ints[2][CHAR_DEADCOUNT];
"""
    main = _replace_once(
        main, old_dispatch, new_dispatch, "full Battling dispatch replacement"
    )

    full = (
        defines + head + driver_types + controlled + stubs
        + "\n" + battling + "\n" + main
    )
    meta = dict(meta)
    meta.update({
        "battle_c_sha256": battle_sha,
        "full_battling_body_sha256": battling_sha,
        "executed_full_battling_case_body": True,
        "full_battling_conditional_source_context_preserved": True,
        "controlled_driver_helpers": CONTROLLED_DRIVER_HELPERS,
    })
    return full, meta


def analyze_profile(name: str, root: Path):
    root = root.resolve()
    head = subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", "HEAD"], text=True
    ).strip()
    dirty = subprocess.check_output(
        ["git", "-C", str(root), "status", "--porcelain"], text=True
    ).strip()
    if head != PINNED[name] or dirty:
        raise ValueError("pinned source commit/tree drift")

    code, meta = _full_source(name, root)
    vectors = prior.cases()
    with tempfile.TemporaryDirectory(prefix="sa-bm-full-battling-tail-") as folder:
        source = Path(folder) / "oracle.c"
        binary = Path(folder) / "oracle"
        source.write_text(code, encoding="utf-8")
        built = subprocess.run(
            [
                "cc", "-std=c11", "-O0", "-Wno-unused-value",
                "-Wno-unused-variable", "-Wno-implicit-function-declaration",
                "-Wno-int-conversion", str(source), "-lm", "-o", str(binary),
            ],
            capture_output=True, text=True,
        )
        if built.returncode:
            raise ValueError(
                "full Battling compile failed: " + built.stderr[-16000:]
            )
        executed = subprocess.run(
            [str(binary)],
            input="".join(" ".join(map(str, c.row())) + "\n" for c in vectors),
            text=True, capture_output=True,
        )
        if executed.returncode:
            raise ValueError(
                "full Battling execution failed: "
                f"returncode={executed.returncode}; stderr={executed.stderr[-8000:]}; "
                f"stdout={executed.stdout[-8000:]}"
            )
        rows = executed.stdout.splitlines()

    if len(rows) != len(vectors):
        raise ValueError("full Battling output row count drift")

    for case, row in zip(vectors, rows):
        values, trace = row.split("|", 1)
        got = tuple(map(int, values.split()))
        if len(got) != 12:
            raise ValueError("full Battling output shape drift")
        (
            _, damage_calls, target_checks, rand_calls,
            owner_hp, owner_die, owner_deaths, owner_charm,
            pet_hp, pet_die, pet_deaths, pet_ai,
        ) = got
        result = prior._scan_expected(owner_hp, pet_hp)
        after = result.after.characters
        actual = (
            owner_die, owner_deaths, owner_charm,
            pet_die, pet_deaths, pet_ai,
        )
        expected = (
            int(after["1"].isdie), after["1"].death_count, after["1"].charm_delta,
            int(after["2"].isdie), after["2"].death_count,
            after["2"].variable_ai_delta,
        )
        if actual != expected:
            raise ValueError(
                f"full Battling profit state drift {case}: "
                f"{actual} != {expected}; full={got}; trace={trace}"
            )
        semantic = [x for x in trace.rstrip(",").split(",") if x]
        first_death = next(
            (i for i, x in enumerate(semantic) if x.startswith("F:")),
            len(semantic),
        )
        hp_writes = [
            x for x in semantic[:first_death] if x.startswith("H:")
        ]
        if case.guardian_enabled:
            if not hp_writes or not hp_writes[0].startswith("H:2:"):
                raise ValueError(
                    f"full Battling first Guardian target drift: {hp_writes}"
                )
            if case.owner_hp == 1 and case.pet_hp == 1:
                if len(hp_writes) < 2 or not hp_writes[1].startswith("H:1:"):
                    raise ValueError(
                        "full Battling second target did not fall back to owner: "
                        f"{hp_writes}"
                    )
                if result.processed_death_ids != ("1", "2"):
                    raise ValueError("full Battling multi-victim scan order drift")
        else:
            if not hp_writes or not hp_writes[0].startswith("H:1:"):
                raise ValueError(
                    f"full Battling no-Guardian target drift: {hp_writes}"
                )
        if damage_calls != len(hp_writes):
            raise ValueError(
                f"full Battling DamageSub/write drift: "
                f"calls={damage_calls}, writes={hp_writes}"
            )
        if rand_calls <= 0 or target_checks < damage_calls:
            raise ValueError("full Battling chronology counters drift")

    return {
        "profile": name,
        "commit": head,
        "native_full_battling_tail_cases": len(vectors),
        **meta,
    }


def main():
    parser = argparse.ArgumentParser()
    for name in PINNED:
        parser.add_argument("--" + name + "-dir", required=True, type=Path)
    args = parser.parse_args()
    total = 0
    for name in PINNED:
        result = analyze_profile(name, getattr(args, name + "_dir"))
        total += result["native_full_battling_tail_cases"]
        import json
        print("PROFILE|" + json.dumps(result, sort_keys=True))
    print(
        "TOTAL|native_full_battling_tail_cases="
        f"{total}|profiles={len(PINNED)}"
    )
    print("FACT|exact_original_full_BATTLE_Battling_body_dispatches_BattleModel_and_reaches_common_tail_AddProfit_in_same_transient_program")
    print("FACT|exact_original_Guardian_AttackSeq_DamageSub_BattleModel_helper_and_tail_AddProfit_remain_linked_under_full_command_driver")
    print("FACT|full_command_driver_gameplay_chronology_matches_immutable_profit_exit_scan_in_reduced_profile")
    print("BOUNDARY|driver_scheduler_status_presentation_and_unrelated_command_helpers_controlled_feature_off_no_ride_no_equipment_noncritical")
    print("OPEN|lethal638_build_version_wider_recipients_ride_items_automatic_AI_packet_presentation_history")
    print("RESOLUTION|BATTLEMODEL_FULL_BATTLING_PROFIT_TAIL_NATIVE_PASS")


if __name__ == "__main__":
    main()
