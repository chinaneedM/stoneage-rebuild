"""Pinned command-entry census and original PETSKILL_Use guard witnesses.

Only hashes, call-site metadata, flags and counts are emitted. Original source
functions are compiled transiently; callback bodies are neutral trace seams.
This distinguishes entry admission from the separately accepted hit runtime.
"""
from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path
import re
import subprocess
import tempfile

from tools.stoneage_guard_break2_source_audit import PINNED, LAYOUTS, _text, _sha, _compact
from tools.stoneage_mdfyattack_source_audit import _definition, _strip

FLAGS = ("_PETSKILL_CHECKTYPE", "_OPEN_E_PETSKILL", "_ONE_PET_SKILL",
         "_ITEM_ATTSKILLMAGIC", "_PETSKILL_BATTLE_MODEL", "_FIXWOLF", "_PETSKILL_OPTIMUM", "_CFREE_petskill")


def cases():
    # Independent admission controls: four actual callback IDs and positive/
    # zero ILLEGAL; neutral tracing isolates the entry guard, not hit damage.
    return tuple(itertools.product((638, 641, 649, 650), (0, 10000, 20000),
        (1, 2, 3), (0, 1), (0, 1), (0, 2), (-1, 0, 2)))


def expected(case, *, checktype, open_enemy_skills):
    _skill, illegal, actor_type, has_array, has_callback, use_type, owner_mode = case
    blocked = (not has_array or (illegal != 0 and actor_type == 1 and not open_enemy_skills)
               or (checktype and actor_type == 1 and use_type & 2 and owner_mode in (-1, 0)))
    called = int(not blocked and has_callback)
    return (called, called, 0)  # return, callback count, callback argument drift


def native_entry(function, *, checktype=True, open_enemy_skills=False, fixwolf=True):
    prefix = r'''
#include <stdio.h>
#include <string.h>
#define TRUE 1
#define FALSE 0
#define CHAR_TYPEPET 1
#define CHAR_WHICHTYPE 1
#define CHAR_BASEIMAGENUMBER 2
#define CHAR_WORKPLAYERINDEX 1
#define CHAR_WORKBATTLEMODE 2
#define BATTLE_CHARMODE_NONE 0
#define PETSKILL_ILLEGAL 1
#define PETSKILL_USETYPE 2
#define PETSKILL_FUNCNAME 3
#define PETSKILL_NAME 4
typedef int (*PETSKILL_CALLFUNC)(int,int,int,char*);
static int skill,illegal,actor_type,has_array,has_callback,use_type,owner_mode;
static int calls,bad_args;
static char payload[]="independent-entry-control";
int CHAR_getPetSkill(int c,int slot){if(c!=7||slot!=2)bad_args++;return skill;}
int PETSKILL_getPetskillArray(int id){if(id!=skill)bad_args++;return has_array?17:-1;}
int PETSKILL_getInt(int a,int p){if(a!=17)bad_args++;return p==PETSKILL_ILLEGAL?illegal:use_type;}
int CHAR_getInt(int c,int p){return p==CHAR_WHICHTYPE?actor_type:0;}
int CHAR_getWorkInt(int c,int p){return p==CHAR_WORKPLAYERINDEX?owner_mode:owner_mode;}
#define CHAR_CHECKINDEX(i) ((i)>=0)
char *PETSKILL_getChar(int a,int p){return "trace_callback";}
int trace_callback(int c,int target,int array,char *data){
 calls++;if(c!=7||target!=5||array!=17||data!=payload)bad_args++;return 1;
}
PETSKILL_CALLFUNC PETSKILL_getPetskillFuncPointer(char *s){return has_callback?trace_callback:0;}
#define print(...) ((void)0)
void CHAR_setPetSkill(int c,int slot,int id){bad_args++;}
'''
    defines = ("#define _PETSKILL_CHECKTYPE\n" if checktype else "")
    defines += "#define _OPEN_E_PETSKILL\n" if open_enemy_skills else ""
    defines += "#define _FIXWOLF\n" if fixwolf else ""
    main = r'''
int main(void){
 while(scanf("%d%d%d%d%d%d%d",&skill,&illegal,&actor_type,&has_array,&has_callback,&use_type,&owner_mode)==7){
  calls=0;bad_args=0;int result=PETSKILL_Use(7,2,5,payload);
  printf("%d %d %d\n",result,calls,bad_args);
 }
 return 0;
}
'''
    vectors = cases()
    with tempfile.TemporaryDirectory() as directory:
        source = Path(directory) / "entry.c"
        binary = Path(directory) / "entry"
        source.write_text(prefix + defines + function + main)
        subprocess.run(["cc", "-w", "-O0", str(source), "-o", str(binary)], check=True, capture_output=True)
        result = subprocess.run([str(binary)], input="".join(" ".join(map(str, row)) + "\n" for row in vectors),
                                text=True, check=True, capture_output=True)
    rows = result.stdout.splitlines()
    if len(rows) != len(vectors):
        raise ValueError("native PETSKILL entry population drift")
    for vector, row in zip(vectors, rows):
        if tuple(map(int, row.split())) != expected(vector, checktype=checktype, open_enemy_skills=open_enemy_skills):
            raise ValueError("native PETSKILL entry guard/argument mismatch: " + repr(vector))
    return len(vectors)


def analyze_profile(name, root):
    root = Path(root).resolve()
    head = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
    dirty = subprocess.check_output(["git", "-C", str(root), "status", "--porcelain"], text=True).strip()
    if head != PINNED[name] or dirty:
        raise ValueError("command-entry pinned source commit/tree drift")
    base = root / LAYOUTS[name]
    names = ["battle/pet_skill.c", "battle/battle_ai.c", "battle/battle_command.c",
             "battle/battle.c", "char/enemy.c", "magic/magic.c", "include/version.h"]
    if (base / "callfromcli.c").is_file():
        names.append("callfromcli.c")
    texts = {path: _text(base / path) for path in names}
    inc = ["-I", str(base / "include")]
    if name == "bismarck":
        inc += ["-I", str(root / "server/common"), "-I", str(root / "shared/lua51")]
    macros = subprocess.check_output(["cpp", "-dM", *inc, str(base / "include/version.h")], text=True)
    active = set(re.findall(r"^#define\s+(\w+)", macros, re.M))
    function = _definition(texts["battle/pet_skill.c"], "PETSKILL_Use")
    loader = _compact(_strip(_definition(texts["battle/pet_skill.c"], "PETSKILL_initPetskill", raw_window=True)))
    use = _compact(_strip(function)).replace("char_index", "charaindex")
    magic = _compact(_strip(_definition(texts["magic/magic.c"], "MAGIC_AttSkill")))
    ai = _compact(_strip(_definition(texts["battle/battle_ai.c"], "BATTLE_ai_normal", raw_window=True)))
    enemy = _compact(_strip(_definition(texts["char/enemy.c"], "ENEMY_createEnemy", raw_window=True)))
    pet = _compact(_strip(_definition(texts["char/enemy.c"], "ENEMY_createPetFromEnemyIndex", raw_window=True)))
    command = _compact(_strip(texts["battle/battle_command.c"]))
    gates = {
        "OPTIMUM_ID_indexed_loader": "#ifdef_PETSKILL_OPTIMUM" in loader and "petskill_readlen=atoi(token)" in loader,
        "loader_final_effective_bound": "PETSKILL_petskillnum=petskill_readlen" in loader,

        "slot_to_id_to_runtime_array": "CHAR_getPetSkill(charaindex,havepetskill)" in use and "PETSKILL_getPetskillArray(petskillid)" in use,
        "illegal_pet_rejected_before_callback": use.index("PETSKILL_ILLEGAL") < use.index("func=PETSKILL_getPetskillFuncPointer") and "CHAR_TYPEPET" in use,
        "normal_ai_nonzero_wa_guard": "wa[i]!=0&&r<work" in ai,
        "normal_ai_slot_submission": bool(re.search(r"PETSKILL_Use\([^,]+,mode-B_AI_WAZAMODE0,result->target,NULL\)", ai)),
        "default_pet_W_command": 'strncmp(command,"W|",2)' in command and "CHAR_DEFAULTPET" in command and "PETSKILL_Use(petindex,iNum,ToNo,NULL)" in command,
        "equipment_magic_direct_dispatch": "PETSKILL_getPetskillFuncPointer" in magic and "PETSKILL_Use" not in magic and '"MAGICSKILL"' in magic,
        "magic_second_token_passed_without_ID_lookup": "skillID=atoi(buff1)" in magic and "PETSKILL_getPetskillArray" not in magic,
        "equipment_magic_SKILL_sentinel": 'strstr(magicarg,"SKILL")' in command and "MAGIC_AttSkill(" in command,
        "template_MODAI_is_character_MODAI": "CHAR_MODAI" in pet and "E_T_MODAI" in pet and "CHAR_WORKTACTICS" not in pet,
        "enemy_tactics_from_variant": "CHAR_WORKTACTICS" in enemy and "ENEMY_TACTICS" in enemy and "CHAR_WORKBATTLE_TACTICSOPTION" in enemy,
    }
    if not all(gates.values()):
        raise ValueError("command-entry source gate drift: " + repr(gates))
    calls = {symbol: [] for symbol in ("PETSKILL_Use", "PETSKILL_getPetskillFuncPointer", "PETSKILL_BattleModel")}
    # Definitions are included and labelled as lexical sites. This bounded C
    # census is not a whole-program pointer/opaque-script reachability proof.
    for path in sorted(base.rglob("*.c")):
        text = _strip(_text(path))
        for symbol in calls:
            count = len(re.findall(r"\b" + symbol + r"\s*\(", text))
            if count:
                calls[symbol].append({"path": path.relative_to(base).as_posix(), "lexical_sites_including_definitions": count})
    direct = native_entry(function, checktype="_PETSKILL_CHECKTYPE" in active,
                          fixwolf="_FIXWOLF" in active, open_enemy_skills="_OPEN_E_PETSKILL" in active)
    # Only Bismarck has the disabling guard. This is explicitly a counterfactual
    # macro experiment, never an assertion about the preserved active build.
    counterfactual = native_entry(function, open_enemy_skills=True) if name == "bismarck" else 0
    return dict(profile=name, source_commit=head, file_sha256={p: _sha(base / p) for p in names},
                flags={flag: flag in active for flag in FLAGS}, gates=gates, lexical_C_sites=calls,
                native_default_header_cases=direct, native_OPEN_E_counterfactual_cases=counterfactual)


def main():
    parser = argparse.ArgumentParser()
    for name in PINNED:
        parser.add_argument("--" + name + "-dir", type=Path, required=True)
    args = parser.parse_args()
    profiles = [analyze_profile(name, getattr(args, name + "_dir")) for name in PINNED]
    result = dict(schema="stoneage.battlemodel-command-entry-source.r1", profiles=profiles,
                  native_default_header_cases=sum(p["native_default_header_cases"] for p in profiles),
                  native_counterfactual_cases=sum(p["native_OPEN_E_counterfactual_cases"] for p in profiles),
                  resolution="BATTLEMODEL_COMMAND_ENTRY_PINNED_SOURCE_NATIVE_PASS")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
