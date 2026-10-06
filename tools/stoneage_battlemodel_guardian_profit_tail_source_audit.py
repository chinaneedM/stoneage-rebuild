"""Same-harness original AttackSeq/GuardianCheck -> BattleModel -> AddProfit R1.

Builds on the accepted dispatch-tail splice but replaces its controlled
BATTLE_AttackSeq seam with the exact pinned original reduced physical function
set already used by the independent physical audit.

Still bounded: feature-off, no ride/equipment, neutral field, controlled
DamageSub/status/presentation/notifications. Full BATTLE_Battling remains open.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re
import subprocess
import tempfile

from tools.stoneage_guard_break2_source_audit import (
    PINNED, LAYOUTS, _text, _sha, _function,
)
from tools.stoneage_battlemodel_physical_source_audit import (
    FUNCTIONS as PHYSICAL_FUNCTIONS,
)
from tools import stoneage_battlemodel_profit_tail_source_audit as tail
from tools.stoneage_default_pet_exit_model import DefaultPetExitAuthority
from tools.stoneage_profit_exit_scan_model import (
    ProfitExitCharacter,
    ProfitExitSnapshot,
    resolve_profit_exit_scan,
)


@dataclass(frozen=True)
class Case:
    guardian_enabled: int
    owner_hp: int
    pet_hp: int
    attack_power: int = 100

    def row(self):
        return (
            int(self.guardian_enabled),
            int(self.owner_hp),
            int(self.pet_hp),
            int(self.attack_power),
        )


def cases():
    return (
        Case(1,1,1,100),
        Case(1,100000,1,100),
        Case(0,1,1,100),
    )


def _physical_parts(name: str, root: Path):
    base=root/LAYOUTS[name]
    event_path=base/"battle/battle_event.c"
    event=_text(event_path)
    bodies=[]
    for function_name in PHYSICAL_FUNCTIONS:
        source_text=(
            _text(base/"battle/battle_magic.c")
            if name=="bismarck" and function_name=="BATTLE_AttrCalc"
            else event
        )
        match=re.search(
            r"\b(?:static\s+)?(?:int|BOOL|float)\s+"
            + re.escape(function_name)
            + r"\s*\(",
            source_text,
        )
        if not match:
            raise ValueError("missing exact physical definition "+function_name)
        bodies.append(_function(source_text,match.group(0)))
    body="\n".join(bodies)
    macros=[]
    for macro in (
        "DAMAGE_RATE","D_16","D_8","KAWASHI_MAX_RATE",
        "AJ_SAME","AJ_UP","AJ_DOWN","ATTR_MAX","D_ATTR",
    ):
        match=re.search(r"^\s*#define\s+"+macro+r"[^\n]*",event,re.M)
        if not match:
            raise ValueError("missing native physical constant "+macro)
        macros.append(match.group(0))
    return body,tuple(macros),_sha(event_path)


def _same_harness_source(name: str, root: Path):
    code,meta=tail._source(name,root)
    physical,macros,event_sha=_physical_parts(name,root)

    old_stub='''int BATTLE_AttackSeq(int a,int d,int *damage,int *guardian,int ignored){
  attackseq_calls++;*damage=attack_damage;*guardian=-1;
  if(guardian_enabled&&d==1&&ints[2][CHAR_HP]>0)*guardian=5;
  return BATTLE_RET_NORMAL;
}
'''
    if old_stub not in code:
        raise ValueError("accepted splice AttackSeq seam drift")
    code=code.replace(old_stub,"/* exact original physical AttackSeq inserted below */\n")

    old_entry="typedef struct {union {int charaindex;int char_index;};int escape,flg,getitem[3];} BATTLE_ENTRY;"
    new_entry="typedef struct {union {int charaindex;int char_index;};int escape,flg,getitem[3],guardian;} BATTLE_ENTRY;"
    if old_entry not in code:
        raise ValueError("splice entry layout anchor drift")
    code=code.replace(old_entry,new_entry)

    old_battle="typedef struct {int dpbattle,type,norisk,use; BATTLE_SIDE Side[2];} BATTLE;"
    new_battle="typedef struct {int dpbattle,type,norisk,use,field_att,att_pow; BATTLE_SIDE Side[2];} BATTLE;"
    if old_battle not in code:
        raise ValueError("splice battle layout anchor drift")
    code=code.replace(old_battle,new_battle)

    old_arrays="static int ints[32][1024],works[32][1024],flags[32][1024],pets[32][5],valid[32];"
    new_arrays=old_arrays+"\nstatic int vectors[32][5],rnglow[64],rnghigh[64],rngval[64],rngcount;"
    if old_arrays not in code:
        raise ValueError("splice array anchor drift")
    code=code.replace(old_arrays,new_arrays)

    old_globals="float gDamageDiv;"
    new_globals='''float gDamageDiv;
static float gDuckPer,gKawashiPara,gCriticalPara=0.09;
static float gBattleDuckModyfy=0,gBattleDamageModyfy=1,gCriper;
static int gWeponType=0;'''
    if old_globals not in code:
        raise ValueError("splice globals anchor drift")
    code=code.replace(old_globals,new_globals)

    old_rand="int RAND(int lo,int hi){rand_calls++;if(lo>hi)hfail(21);return lo;}"
    new_rand='''int RAND(int lo,int hi){
  rand_calls++;if(lo>hi)hfail(21);
  int v=hi;
  if(rngcount<64){rnglow[rngcount]=lo;rnghigh[rngcount]=hi;rngval[rngcount]=v;}
  rngcount++;
  return v;
}'''
    if old_rand not in code:
        raise ValueError("splice RAND seam drift")
    code=code.replace(old_rand,new_rand)

    target_anchor="int BATTLE_TargetCheck(int b,int no){target_checks++;if(no<0||no>=20)return FALSE;int id=BATTLE_No2Index(b,no);return CHAR_CHECKINDEX(id)&&ints[id][CHAR_HP]>0;}\n"
    extra='''int BATTLE_GetWepon(int c){return 0;}
int BATTLE_IsThrowWepon(int c){return FALSE;}
int BATTLE_adjustRidePet3A(int c,int pet,int p,int side){hfail(50);return 0;}
int ITEM_getInt(int c,int p){return 0;}
void BATTLE_GetAttr(int c,int *v){memcpy(v,vectors[c],sizeof(vectors[c]));}
int BATTLE_CanMoveCheck(int c){return !(works[c][CHAR_WORKSLEEP]>0||works[c][CHAR_WORKPARALYSIS]>0||works[c][CHAR_WORKSTONE]>0);}
int BATTLE_GetDamageReact(int c){return works[c][CHAR_WORKDAMAGEVANISH]||works[c][CHAR_WORKDAMAGEABSROB]||works[c][CHAR_WORKDAMAGEREFLEC];}
void PROFESSION_SKILL_WEAPON_FOCUS_LVEVEL_UP(int c,char *s){}
void PROFESSION_SKILL_DUAL_WEAPON_LVEVEL_UP(int c,char *s){}
'''
    if target_anchor not in code:
        raise ValueError("splice TargetCheck anchor drift")
    code=code.replace(target_anchor,target_anchor+extra)

    # Add exact physical bodies immediately before the exact BattleModel helper.
    helper_at=code.find("void BATTLE_BattleModel_ATTACK")
    if helper_at<0:
        raise ValueError("missing exact BattleModel helper in splice")
    code=code[:helper_at]+physical+"\n"+code[helper_at:]

    # Define physical-only field/command names not already provided by the
    # accepted splice generator. Preserve bit semantics for battle flags.
    existing=set(re.findall(r"^#define\s+(\w+)\b",code,re.M))
    physical_names=sorted(set(re.findall(
        r"\b(?:CHAR|BATTLE|ITEM|AI)_[A-Z][A-Z0-9_]*\b",
        physical,
    )))
    physical_calls=set(re.findall(r"\b([A-Za-z_]\w*)\s*\(",physical))
    fixed={
        "CHAR_BATTLEFLG_NODUCK":1,
        "CHAR_BATTLEFLG_ABIO":2,
        "CHAR_BATTLEFLG_GUARDIAN":4,
        "CHAR_WORKDAMAGEVANISH":1750,
        "CHAR_WORKDAMAGEABSROB":1751,
        "CHAR_WORKDAMAGEREFLEC":1752,
    }
    next_id=1800
    additions=[]
    for symbol in physical_names:
        if symbol in existing or symbol in physical_calls:
            continue
        additions.append(f"#define {symbol} {fixed.get(symbol,next_id)}")
        if symbol not in fixed:
            next_id+=1
    for symbol in (
        "CHAR_WORKDAMAGEVANISH",
        "CHAR_WORKDAMAGEABSROB",
        "CHAR_WORKDAMAGEREFLEC",
    ):
        if symbol not in existing and not any(
            line.startswith("#define "+symbol+" ") for line in additions
        ):
            additions.append(f"#define {symbol} {fixed[symbol]}")
    prelude=(
        "#define _BATTLE_NEWPOWER\n"
        "#define ATTACKSIDE 0\n#define DEFFENCESIDE 1\n"
        +"\n".join(macros)+"\n"
        +"\n".join(additions)+"\n"
    )
    code=prelude+code

    # Entry guardian defaults and physical state setup.
    old_init="for(int s=0;s<2;s++)for(int p=0;p<10;p++){BattleArray[0].Side[s].Entry[p].charaindex=-1;BattleArray[0].Side[s].Entry[p].escape=7;for(int k=0;k<3;k++)BattleArray[0].Side[s].Entry[p].getitem[k]=-1;}"
    new_init="for(int s=0;s<2;s++)for(int p=0;p<10;p++){BattleArray[0].Side[s].Entry[p].charaindex=-1;BattleArray[0].Side[s].Entry[p].escape=7;BattleArray[0].Side[s].Entry[p].guardian=-1;for(int k=0;k<3;k++)BattleArray[0].Side[s].Entry[p].getitem[k]=-1;}"
    if old_init not in code:
        raise ValueError("splice entry-init anchor drift")
    code=code.replace(old_init,new_init)

    old_reset="memset(pets,-1,sizeof(pets));trace_length=0;trace[0]=0;\n    guardian_enabled=ge;attack_damage=dmg;attackseq_calls=damage_calls=target_checks=rand_calls=0;"
    new_reset='''memset(pets,-1,sizeof(pets));memset(vectors,0,sizeof(vectors));trace_length=0;trace[0]=0;
    guardian_enabled=ge;attack_damage=dmg;attackseq_calls=damage_calls=target_checks=rand_calls=rngcount=0;
    gDamageDiv=0.0;gBattleDuckModyfy=0;gBattleDamageModyfy=1;gCriticalPara=0.09;'''
    if old_reset not in code:
        raise ValueError("splice reset anchor drift")
    code=code.replace(old_reset,new_reset)

    setup_anchor="works[1][CHAR_WORKBATTLECOM1]=works[2][CHAR_WORKBATTLECOM1]=works[10][CHAR_WORKBATTLECOM1]=77;\n"
    setup_extra='''    works[1][CHAR_WORKFIXDEX]=10;works[2][CHAR_WORKFIXDEX]=10;works[10][CHAR_WORKFIXDEX]=100;
    works[1][CHAR_WORKFIXLUCK]=works[2][CHAR_WORKFIXLUCK]=0;works[10][CHAR_WORKFIXLUCK]=999;
    works[1][CHAR_WORKDEFENCEPOWER]=works[2][CHAR_WORKDEFENCEPOWER]=40;works[10][CHAR_WORKDEFENCEPOWER]=80;
    works[1][CHAR_WORKQUICK]=works[2][CHAR_WORKQUICK]=40;works[10][CHAR_WORKQUICK]=60;
    works[1][CHAR_WORKFIXVITAL]=works[2][CHAR_WORKFIXVITAL]=40;works[10][CHAR_WORKFIXVITAL]=80;
    works[10][CHAR_WORKATTACKPOWER]=dmg;
    works[1][CHAR_WORKBATTLEFLG]|=CHAR_BATTLEFLG_NODUCK;
    for(int id=1;id<=10;id++){vectors[id][4]=100;}
'''
    if setup_anchor not in code:
        raise ValueError("splice work-setup anchor drift")
    code=code.replace(setup_anchor,setup_anchor+setup_extra)

    occupancy_anchor="BattleArray[0].Side[1].Entry[0].charaindex=10;\n"
    guardian_setup='''    if(ge){
      BattleArray[0].Side[0].Entry[0].guardian=5;
      works[2][CHAR_WORKBATTLEFLG]|=CHAR_BATTLEFLG_GUARDIAN;
    }
'''
    if occupancy_anchor not in code:
        raise ValueError("splice occupancy anchor drift")
    code=code.replace(occupancy_anchor,occupancy_anchor+guardian_setup)

    meta=dict(meta)
    meta.update({
        "same_harness_original_attackseq_guardiancheck":True,
        "physical_event_sha256":event_sha,
        "physical_function_count":len(PHYSICAL_FUNCTIONS),
        "damage_sub_controlled":True,
    })
    return code,meta


def _scan_expected(owner_hp: int, pet_hp: int):
    chars={
        "1":ProfitExitCharacter(
            "1","player",11,int(owner_hp),0,
            status_counters=(0,)*10,command=77,
        ),
        "2":ProfitExitCharacter(
            "2","pet",20,int(pet_hp),5,
            status_counters=(0,)*10,command=77,
        ),
        "10":ProfitExitCharacter(
            "10","enemy",20,100,10,
            status_counters=(0,)*10,command=77,
        ),
    }
    return resolve_profit_exit_scan(
        ProfitExitSnapshot(
            chars,
            DefaultPetExitAuthority("1","2",("2",),{"2":5}),
            0,False,None,
        ),
        recipient_id="10",
    )


def analyze_profile(name: str, root: Path):
    root=root.resolve()
    head=subprocess.check_output(
        ["git","-C",str(root),"rev-parse","HEAD"],text=True
    ).strip()
    dirty=subprocess.check_output(
        ["git","-C",str(root),"status","--porcelain"],text=True
    ).strip()
    if head!=PINNED[name] or dirty:
        raise ValueError("pinned source commit/tree drift")

    code,meta=_same_harness_source(name,root)
    vectors=cases()
    with tempfile.TemporaryDirectory(prefix="sa-bm-guardian-profit-tail-") as folder:
        source=Path(folder)/"oracle.c"
        binary=Path(folder)/"oracle"
        source.write_text(code,encoding="utf-8")
        built=subprocess.run(
            ["cc","-std=c11","-O0","-Wno-unused-value","-Wno-unused-variable",
             str(source),"-lm","-o",str(binary)],
            capture_output=True,text=True,
        )
        if built.returncode:
            raise ValueError(
                "same-harness guardian compile failed: "+built.stderr[-10000:]
            )
        executed=subprocess.run(
            [str(binary)],
            input="".join(" ".join(map(str,c.row()))+"\n" for c in vectors),
            text=True,capture_output=True,
        )
        if executed.returncode:
            raise ValueError(
                "same-harness guardian execution failed: "
                f"returncode={executed.returncode}; stderr={executed.stderr[-5000:]}; "
                f"stdout={executed.stdout[-5000:]}"
            )
        rows=executed.stdout.splitlines()

    if len(rows)!=len(vectors):
        raise ValueError("same-harness guardian row count drift")

    for case,row in zip(vectors,rows):
        values,trace=row.split("|",1)
        got=tuple(map(int,values.split()))
        if len(got)!=12:
            raise ValueError("same-harness output shape drift")
        _,damage_calls,target_checks,rand_calls,owner_hp,owner_die,owner_deaths,owner_charm,pet_hp,pet_die,pet_deaths,pet_ai=got
        result=_scan_expected(owner_hp,pet_hp)
        after=result.after.characters
        expected=(
            int(after["1"].isdie),after["1"].death_count,after["1"].charm_delta,
            int(after["2"].isdie),after["2"].death_count,after["2"].variable_ai_delta,
        )
        actual=(owner_die,owner_deaths,owner_charm,pet_die,pet_deaths,pet_ai)
        if actual!=expected:
            raise ValueError(
                f"same-harness profit state drift {case}: {actual} != {expected}; {trace}"
            )
        semantic=[x for x in trace.rstrip(",").split(",") if x]
        damage=[x for x in semantic if x.startswith("M:")]
        death_first=next(
            (i for i,x in enumerate(semantic) if x.startswith("F:")),
            len(semantic),
        )
        if death_first < len(damage):
            raise ValueError("tail AddProfit began before all same-harness damage writes")
        if case.guardian_enabled:
            if not damage or not damage[0].startswith("M:2:"):
                raise ValueError(
                    f"original GuardianCheck did not route first hit to pet: {damage}"
                )
            if case.owner_hp==1 and case.pet_hp==1:
                if len(damage)!=2 or not damage[1].startswith("M:1:"):
                    raise ValueError(
                        f"post-hit target validation did not move second damage to owner: {damage}"
                    )
                if result.processed_death_ids!=("1","2"):
                    raise ValueError("same-harness multi-victim scan order drift")
        else:
            if not damage or not damage[0].startswith("M:1:"):
                raise ValueError("no-Guardian vector did not damage owner first")
        if damage_calls!=len(damage):
            raise ValueError("DamageSub trace/count drift")
        if target_checks < damage_calls:
            raise ValueError("BattleModel target validation count underflow")
        if rand_calls<=0:
            raise ValueError("same-harness original physical path consumed no RNG")

    return {
        "profile":name,
        "commit":head,
        "native_same_harness_guardian_tail_cases":len(vectors),
        **meta,
    }


def main():
    parser=argparse.ArgumentParser()
    for name in PINNED:
        parser.add_argument("--"+name+"-dir",required=True,type=Path)
    args=parser.parse_args()
    total=0
    for name in PINNED:
        result=analyze_profile(name,getattr(args,name+"_dir"))
        total+=result["native_same_harness_guardian_tail_cases"]
        import json
        print("PROFILE|"+json.dumps(result,sort_keys=True))
    print(
        f"TOTAL|native_same_harness_guardian_tail_cases={total}|profiles={len(PINNED)}"
    )
    print("FACT|exact_original_AttackSeq_GuardianCheck_BattleModel_helper_and_original_tail_AddProfit_link_in_one_transient_program")
    print("FACT|dead_guardian_candidate_can_be_returned_by_GuardianCheck_before_ISDIE_but_BattleModel_post_AttackSeq_TargetCheck_controls_actual_DamageSub_target")
    print("FACT|same_harness_multi_victim_damage_finishes_before_source_order_tail_scan_and_repeat_profit_is_idempotent")
    print("BOUNDARY|DamageSub_status_presentation_notifications_getters_controlled_feature_off_no_ride_no_equipment_newpower")
    print("OPEN|exact_original_DamageSub_same_harness_full_BATTLE_Battling_body_lethal638_modern_admission")
    print("RESOLUTION|BATTLEMODEL_SAME_HARNESS_GUARDIAN_PROFIT_TAIL_NATIVE_PASS")


if __name__=="__main__":
    main()
