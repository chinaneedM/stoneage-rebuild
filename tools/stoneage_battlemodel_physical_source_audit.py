"""Transient native physical AttackSeq composition in a declared reduced build.

Compiles pinned original Duck/Guardian/Critical/Damage/Attr/Guard/AttackSeq
bodies. Only participant getters, no-ride/equipment getters, CanMove and
reaction selection are controlled stubs. Emits derived counts/hashes only;
this does not select an original build or enable complete BattleModel runtime.
"""
from __future__ import annotations

import argparse
from itertools import product
from pathlib import Path
import re
import subprocess
import tempfile
from unittest.mock import patch

from tools.stoneage_guard_break2_source_audit import PINNED, LAYOUTS, _text, _sha, _function
from tools.stoneage_battlemodel_physical_attackseq import (
    PHYSICAL_SCOPE_R1, BattleModelPhysicalContext, BattleModelPhysicalProfile,
    resolve_battlemodel_physical_attackseq,
)
from tools.stoneage_battlemodel_hit_loop import BattleModelEntry, BattleModelAttackSeqRng
from tools.stoneage_battle_guardian_model import GuardianRegistration
from tools.stoneage_battle_damage_react_model import BaseDamageReactState
from tools.stoneage_battle_status_model import BaseBattleStatusState, BaseBattleStatusRuntime
from tools.stoneage_battlemodel_reference_model import PROFILE_UTF8, BattleModelAttackObject
from tools import stoneage_enemy_ai_battlemodel_bridge as bridge


FUNCTIONS = (
    "BATTLE_FieldAttAdjust", "BATTLE_AttrCalc", "BATTLE_AttrAdjust",
    "BATTLE_DamageCalc", "BATTLE_GuardAdjust", "BATTLE_CriticalCheckPlayer",
    "BATTLE_CriticalCheck", "BATTLE_CriDamageCalc", "BATTLE_GuardianCheck",
    "BATTLE_DuckCheck", "BATTLE_AttackSeq",
)


def controlled_cases():
    cases = []
    for power, defense, preset in product((23, 100), (10, 40, 130, 200),
            ((10000, 10000, 0, 100, 1), (10000, 399, 12, 25, 0), (1, 400, 3, 70, 0))):
        cases.append(dict(power=power, defense=defense, preset=preset))
    for name, value in (("sleep", 1), ("paralysis", 1), ("stone", 1),
                        ("confusion", 1), ("no_dodge", True), ("abio", True),
                        ("reaction", 1), ("reaction", 2), ("reaction", 3)):
        for drunk, command in product((0, 1), ("none", "guard")):
            cases.append({name: value, "drunk": drunk, "command": command})
    for command, confusion, cleared, floor in product(("none", "guard"), (0, 1), (False, True), (0, 1)):
        cases.append(dict(command=command, confusion=confusion, cleared=cleared,
                          no_dodge=True, preset=(10000, 0, 1, floor, 1)))
    for guardian_state in ("live", "dead", "sleep", "confusion", "paralysis", "stone", "barrier", "no_flag"):
        for roll in (500, 10000):
            cases.append(dict(guardian=guardian_state, ddex=60,
                              preset=(10000, roll, 0, 1, 0), guardian_command="guard"))
    for kind, luck, roll in product(("player", "pet"), (0, 20), (1, 2, 2000, 10000)):
        cases.append(dict(kind=kind, luck=luck, ddex=60, drunk=1,
                          preset=(20, roll, 400, 0, 1)))
    for roll in (399, 400):
        cases.append(dict(ddex=60, no_dodge=True, preset=(roll, 0, 1, 1, 1)))
    for elements, field in product((0, 1, 2), ("none", "earth")):
        cases.append(dict(elements=elements, field=field, no_dodge=True))
    return tuple(cases)


def _inputs(case, defense_profile, source_profile):
    from tests.test_stoneage_battlemodel_admission import fixture, spawned
    runtime, identities = fixture()
    with patch.object(bridge, "EXPECTED_ROW_IDENTITIES", identities):
        submission = bridge.resolve_enemy_ai_battlemodel_submission(
            spawned(), skill_slot=2, target_slot=5, petskill_runtime=runtime,
            profile=PROFILE_UTF8, source_profile=source_profile,
            powers_before=(case.get("power", 100), 80, 60))
    status = BaseBattleStatusState(**{name: case.get(name, 0)
        for name in ("sleep", "paralysis", "stone", "confusion")})
    reaction = {0: BaseDamageReactState(), 1: BaseDamageReactState(absorb=1),
                2: BaseDamageReactState(reflect=1), 3: BaseDamageReactState(vanish=1)}[case.get("reaction", 0)]
    entries = {0: BattleModelEntry("target", case.get("kind", "player"), 500, 500, 0,
        status_runtime=BaseBattleStatusRuntime(status=status), reaction=reaction,
        abio=case.get("abio", False), command_cleared=case.get("cleared", False)),
        10: BattleModelEntry("enemy", "enemy", 500, 500, 0,
            status_runtime=BaseBattleStatusRuntime(status=BaseBattleStatusState(drunk=case.get("drunk", 0))))}
    vectors = {0: ((0, 0, 0, 0), (0, 100, 0, 0), (50, 0, 50, 0))[case.get("elements", 0)],
               10: ((0, 0, 0, 0), (100, 0, 0, 0), (0, 50, 0, 50))[case.get("elements", 0)]}
    profiles = {0: BattleModelPhysicalProfile("target", 10, case.get("ddex", 100), case.get("luck", 0),
        case.get("defense", 40), 40, vectors[0], fixed_vital=40,
        command=case.get("command", "none"), no_dodge=case.get("no_dodge", False)),
        10: BattleModelPhysicalProfile("enemy", 10, 100, 999, 80, 60, vectors[10], fixed_vital=80)}
    guardians = {}
    if "guardian" in case:
        state = case["guardian"]
        gstatus = BaseBattleStatusState(**({state: 1} if state in {"sleep", "confusion", "paralysis", "stone"} else {}))
        entries[5] = BattleModelEntry("guardian", "pet", 0 if state == "dead" else 500, 500, 0,
            status_runtime=BaseBattleStatusRuntime(status=gstatus))
        profiles[5] = BattleModelPhysicalProfile("guardian", 20, 10, 999, 100, 40,
            (0, 0, 0, 0), fixed_vital=100, command=case.get("guardian_command", "none"))
        guardians[0] = GuardianRegistration(5, guardian_flag=state != "no_flag",
                                           guardian_barrier=1 if state == "barrier" else 0)
    field = case.get("field", "none")
    context = BattleModelPhysicalContext(PHYSICAL_SCOPE_R1, defense_profile,
        profiles, guardians, field_attr=field, field_power=0 if field == "none" else 100)
    return submission, entries, context


PREFIX = r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#define BOOL int
#define TRUE 1
#define FALSE 0
#define SIDE_OFFSET 10
#define BATTLE_TYPE_P_vs_E 99
#define min(a,b) ((a)<(b)?(a):(b))
#define max(a,b) ((a)>(b)?(a):(b))
typedef struct {int guardian;} Entry;
typedef struct {Entry Entry[10];} Side;
typedef struct {Side Side[2];int norisk,type,field_att,att_pow;} Battle;
static Battle BattleArray[1];
static int stats[20][512],works[20][512],vectors[20][5],valid[20],die[20];
static int preset[8],rnglow[16],rnghigh[16],rngval[16],rngcount;
static float gDuckPer,gKawashiPara,gCriticalPara=0.09;
static float gBattleDuckModyfy=0,gBattleDamageModyfy=1,gCriper;
static int gWeponType=0;
int owned_rand(int low,int high){
 if(rngcount>=8){fprintf(stderr,"RNG overflow\n");exit(2);}
 int v=preset[rngcount];if(v<low)v=low;if(v>high)v=high;
 rnglow[rngcount]=low;rnghigh[rngcount]=high;rngval[rngcount++]=v;return v;
}
#define RAND(a,b) owned_rand((int)(a),(int)(b))
int CHAR_getInt(int c,int p){return stats[c][p];}
int CHAR_getWorkInt(int c,int p){return works[c][p];}
int CHAR_getFlg(int c,int p){return die[c];}
int CHAR_CHECKINDEX(int c){return c>=0&&c<20&&valid[c];}
int CHAR_getItemIndex(int c,int p){return -1;}
int ITEM_CHECKINDEX(int c){return 0;}
int ITEM_getInt(int c,int p){return 0;}
int CHAR_GETWORKINT_HIGH(int c,int p){return 0;}
int BATTLE_getRidePet(int c){return -1;}
int BATTLE_adjustRidePet3A(int c,int pet,int p,int side){fprintf(stderr,"unexpected ride\n");exit(3);}
int BATTLE_GetWepon(int c){return 0;}
int BATTLE_IsThrowWepon(int c){return FALSE;}
int BATTLE_Index2No(int b,int c){return c;}
int BATTLE_No2Index(int b,int n){return n;}
void BATTLE_GetAttr(int c,int *v){memcpy(v,vectors[c],sizeof(vectors[c]));}
int BATTLE_CanMoveCheck(int c){return !(works[c][CHAR_WORKSLEEP]>0||works[c][CHAR_WORKPARALYSIS]>0||works[c][CHAR_WORKSTONE]>0);}
int BATTLE_GetDamageReact(int c){return works[c][CHAR_WORKDAMAGEVANISH]||works[c][CHAR_WORKDAMAGEABSROB]||works[c][CHAR_WORKDAMAGEREFLEC];}
void CHAR_PetAddVariableAi(int c,int p){}
void PROFESSION_SKILL_WEAPON_FOCUS_LVEVEL_UP(int c,char *s){}
void PROFESSION_SKILL_DUAL_WEAPON_LVEVEL_UP(int c,char *s){}
'''


def _driver(cases, defense_profile, source_profile):
    blocks = []
    for case in cases:
        submission, entries, context = _inputs(case, defense_profile, source_profile)
        setup = ["memset(stats,0,sizeof(stats));memset(works,0,sizeof(works));",
                 "memset(vectors,0,sizeof(vectors));memset(valid,0,sizeof(valid));memset(die,0,sizeof(die));",
                 "memset(BattleArray,0,sizeof(BattleArray));BattleArray[0].norisk=1;",
                 "for(int s=0;s<2;s++)for(int i=0;i<10;i++)BattleArray[0].Side[s].Entry[i].guardian=-1;",
                 "rngcount=0;"]
        for slot, entry in entries.items():
            p = context.profiles[slot]
            command = "BATTLE_COM_GUARD" if p.command == "guard" and not entry.command_cleared else "0"
            flags = (1 if p.no_dodge else 0) | (2 if entry.abio else 0)
            setup += [f"valid[{slot}]=1;die[{slot}]={int(entry.hp == 0)};",
                      f"stats[{slot}][CHAR_WHICHTYPE]=CHAR_TYPE{entry.kind.upper()};",
                      f"stats[{slot}][CHAR_LV]={p.level};works[{slot}][CHAR_WORKBATTLECOM1]={command};",
                      f"works[{slot}][CHAR_WORKBATTLEFLG]={flags};"]
            for key, value in {"FIXDEX": p.fixed_dex, "FIXLUCK": p.fixed_luck,
                "DEFENCEPOWER": p.defense_power, "QUICK": p.quick, "FIXVITAL": p.fixed_vital,
                **{name.upper(): getattr(entry.status_runtime.status, name)
                   for name in ("sleep", "paralysis", "stone", "confusion", "drunk")},
                "DAMAGEABSROB": entry.reaction.absorb, "DAMAGEREFLEC": entry.reaction.reflect,
                "DAMAGEVANISH": entry.reaction.vanish}.items():
                setup.append(f"works[{slot}][CHAR_WORK{key}]={value};")
            for i, value in enumerate((*p.elements, 100-sum(p.elements))):
                setup.append(f"vectors[{slot}][{i}]={value};")
        setup.append(f"works[10][CHAR_WORKATTACKPOWER]={submission.setup.powers[0]};")
        for slot, g in context.guardians.items():
            setup += [f"BattleArray[0].Side[0].Entry[{slot}].guardian={g.guardian_slot};",
                      f"works[{g.guardian_slot}][CHAR_WORKBATTLEFLG]|={4 if g.guardian_flag else 0};",
                      f"works[{g.guardian_slot}][CHAR_WORKBARRIER]={g.guardian_barrier};"]
        setup += [f"BattleArray[0].field_att={'0' if context.field_attr == 'none' else 'BATTLE_ATTR_'+context.field_attr.upper()};",
                  f"BattleArray[0].att_pow={context.field_power};"]
        values = case.get("preset", (10000, 10000, 0, 100, 1))
        setup += [f"preset[{i}]={v};" for i, v in enumerate((*values, *(1 for _ in range(8-len(values)))))]
        setup += ["int damage=0,guardian=-1;int ret=BATTLE_AttackSeq(10,0,&damage,&guardian,-1);",
                  'printf("%d %d %d %d",ret,damage,guardian,rngcount);',
                  'for(int i=0;i<rngcount;i++)printf(" %d %d %d",rnglow[i],rnghigh[i],rngval[i]);printf("\\n");']
        blocks.append("{\n" + "\n".join(setup) + "\n}")
    return "int main(void){\n" + "\n".join(blocks) + "\nreturn 0;}\n"


def analyze_profile(name, root):
    root = root.resolve()
    sha = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
    dirty = subprocess.check_output(["git", "-C", str(root), "status", "--porcelain"], text=True).strip()
    if sha != PINNED[name] or dirty:
        raise ValueError("pinned source commit/tree drift")
    path = root / LAYOUTS[name] / "battle/battle_event.c"
    text = _text(path)
    bodies = []
    for n in FUNCTIONS:
        source_text = (_text(root / LAYOUTS[name] / "battle/battle_magic.c")
                       if name == "bismarck" and n == "BATTLE_AttrCalc" else text)
        match = re.search(r"\b(?:static\s+)?(?:int|BOOL|float)\s+"+n+r"\s*\(", source_text)
        if not match:
            raise ValueError("missing exact physical definition "+n)
        bodies.append(_function(source_text, match.group(0)))
    bodies = "\n".join(bodies)
    fixed = {"CHAR_BATTLEFLG_NODUCK": 1, "CHAR_BATTLEFLG_ABIO": 2, "CHAR_BATTLEFLG_GUARDIAN": 4,
        "CHAR_TYPEPLAYER": 1, "CHAR_TYPEENEMY": 2, "CHAR_TYPEPET": 3,
        "BATTLE_RET_NORMAL": 0, "BATTLE_RET_CRITICAL": 1, "BATTLE_RET_DODGE": 2,
        "BATTLE_RET_MISS": 3, "BATTLE_RET_ALLGUARD": 4}
    names = sorted(set(re.findall(r"\b(?:CHAR|BATTLE|ITEM|AI)_[A-Z][A-Z0-9_]*\b", bodies + PREFIX)))
    names = [n for n in names if n not in {"CHAR_CHECKINDEX", "ITEM_CHECKINDEX", "CHAR_GETWORKINT_HIGH", "CHAR_GETWORKINT_LOW"}]
    constants = "\n".join(f"#define {n} {fixed.get(n, i+20)}" for i, n in enumerate(names))
    macros = []
    for n in ("DAMAGE_RATE", "D_16", "D_8", "KAWASHI_MAX_RATE", "AJ_SAME", "AJ_UP", "AJ_DOWN", "ATTR_MAX", "D_ATTR"):
        match = re.search(r"^\s*#define\s+"+n+r"[^\n]*", text, re.M)
        if not match:
            raise ValueError("missing native physical constant " + n)
        macros.append(match.group(0))
    cases = controlled_cases()
    count = 0
    for defense_profile in ("newpower_70pct", "preserved_old_mixed"):
        with tempfile.TemporaryDirectory(prefix="sa-physical-attackseq-") as folder:
            source, binary = Path(folder)/"oracle.c", Path(folder)/"oracle"
            source.write_text(constants + "\n" + "\n".join(macros) + "\n" +
                ("#define _BATTLE_NEWPOWER\n" if defense_profile == "newpower_70pct" else "") +
                "#define ATTACKSIDE 0\n#define DEFFENCESIDE 1\n" + PREFIX + "\n" + bodies + "\n" +
                _driver(cases, defense_profile, name))
            result = subprocess.run(["cc", "-std=c99", "-O0", str(source), "-lm", "-o", str(binary)],
                                    capture_output=True, text=True)
            if result.returncode:
                raise ValueError("native physical compilation failed: " + result.stderr[-6000:])
            rows = subprocess.check_output([str(binary)], text=True).splitlines()
        if len(rows) != len(cases):
            raise ValueError("native physical row count drift")
        for index, (case, row) in enumerate(zip(cases, rows)):
            submission, entries, context = _inputs(case, defense_profile, name)
            preset = case.get("preset", (10000, 10000, 0, 100, 1))
            tape = []
            def take(owner, low, high):
                value = min(high, max(low, preset[len(tape)] if len(tape) < len(preset) else 1))
                tape.append((owner, low, high, value))
                return value
            hit = resolve_battlemodel_physical_attackseq(submission, actor_slot=10,
                attack=BattleModelAttackObject(0, 0, 7), entries=entries,
                context=context, rng=BattleModelAttackSeqRng(take))
            expected = ({"normal": 0, "critical": 1, "dodge": 2, "miss": 3, "allguard": 4}[hit.outcome],
                hit.raw_damage, hit.guardian_slot if hit.guardian_slot is not None else -1, len(tape),
                *(v for _, low, high, value in tape for v in (low, high, value)))
            native = tuple(map(int, row.split()))
            if native != expected:
                raise ValueError(f"physical mismatch {name}/{defense_profile}/{index}: {case}: {native} != {expected}; owners={tape}")
            count += 1
    return _sha(path), count, (_sha(root / LAYOUTS[name] / "battle/battle_magic.c") if name == "bismarck" else None)


def main():
    parser = argparse.ArgumentParser()
    for name in PINNED:
        parser.add_argument("--"+name+"-dir", required=True, type=Path)
    args = parser.parse_args()
    print("StoneAge bounded equipment-free physical AttackSeq composition")
    for name in PINNED:
        digest, count, magic_digest = analyze_profile(name, getattr(args, name+"_dir"))
        print(f"PROFILE|profile={name}|sha={PINNED[name]}|source_sha256={digest}|physical_attackseq_model_native_comparisons={count}")
        if magic_digest:
            print(f"SOURCE|profile={name}|file=battle/battle_magic.c|sha256={magic_digest}")
    print("FACT|original_reduced_Duck_Guardian_Critical_Damage_Attr_Guard_AttackSeq_outcome_damage_RNG_bounds_order_match")
    print("BOUNDARY|controlled_getters_CanMove_reaction_no_ride_no_equipment_neutral_globals_no_later_features;original_build_full_runtime_OPEN")
    print("RESOLUTION|BATTLEMODEL_EQUIPMENT_FREE_PHYSICAL_ATTACKSEQ_MODEL_NATIVE_PASS")


if __name__ == "__main__":
    main()
