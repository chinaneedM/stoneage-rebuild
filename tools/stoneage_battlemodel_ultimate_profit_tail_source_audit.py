"""Exact full Battling/Guardian/DamageSub/ultimate profit-tail differential.

Original functions stay unchanged except mechanical symbol renames for tracing.
Reuse the accepted reduced no-ride driver seams, capture the actual pre-profit
boundary, and compare its exit/accounting state with the canonical binder.
Only metadata and semantic witnesses are emitted; original source is transient.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass, replace
import json
from pathlib import Path
import re
import subprocess
import tempfile

from tools.stoneage_guard_break2_source_audit import PINNED
from tools import stoneage_battlemodel_full_battling_profit_tail_source_audit as prior
from tools.stoneage_profit_exit_runtime_binder import resolve_profit_boundary_scans
from tools.stoneage_profit_exit_scan_model import resolve_profit_exit_scan


@dataclass(frozen=True)
class Case:
    name: str
    guardian: int
    owner_hp: int
    pet_hp: int
    owner_max: int
    pet_max: int
    overkill: int = 0
    selected: int = 0
    no_risk: int = 0

    def row(self):
        return (self.guardian, self.owner_hp, self.pet_hp, 100,
                self.owner_max, self.pet_max, self.overkill,
                self.selected, self.no_risk)


def cases():
    base = (
        Case("normal_both", 1, 1, 1, 1000, 1000),
        Case("ultimate2_both_owner_first", 1, 1, 1, 10, 10),
        Case("ultimate2_owner_normal_pet", 1, 1, 1, 10, 1000),
        Case("normal_owner_ultimate2_pet", 1, 1, 1, 1000, 10),
        Case("ultimate2_pet_only", 1, 1000, 1, 1000, 10),
        Case("ultimate2_owner_only", 0, 1, 1000, 10, 1000),
        Case("ultimate1_both_owner_first", 1, 1, 1, 1000, 1000, 2000),
        Case("ultimate2_both_unselected", 1, 1, 1, 10, 10, selected=-1),
    )
    return base + tuple(replace(c, name=c.name+"_norisk", no_risk=1) for c in base)


def _source(name: str, root: Path):
    code, meta = prior._full_source(name, root)
    change = prior._replace_once
    # Match the accepted ID638 work carrier (four objects, type5 physical).
    # Status/presentation remain the same declared neutral seams. Only the
    # target-selection draw is fixed to slot-order index0; physical draws stay
    # at their accepted high endpoint, preserving the noncritical witness.
    code = change(code, "(2<<16)|4", "(4<<16)|5", "ID638 work carrier")
    code = change(code, 'option_buf[256]="4|2|||||10"',
                  'option_buf[256]="5|4|||||10"', "bounded ID638 option carrier")
    code = change(code, "int v=hi;", "int v=(lo==0&&hi==1)?0:hi;", "target-selection draw")
    code = change(code, "int ge,oh,ph,dmg;", "int ge,oh,ph,dmg,om,pm,ok,sel,nr;", "input vars")
    code = change(code, 'scanf("%d%d%d%d",&ge,&oh,&ph,&dmg)==4',
                  'scanf("%d%d%d%d%d%d%d%d%d",&ge,&oh,&ph,&dmg,&om,&pm,&ok,&sel,&nr)==9', "input row")
    code = change(code, "BattleArray[0].norisk=0;", "BattleArray[0].norisk=nr;", "no risk")
    code = change(code, "ints[1][CHAR_DEFAULTPET]=0;", "ints[1][CHAR_DEFAULTPET]=sel;", "selected pet")
    for cid, var in ((1, "om"), (2, "pm")):
        code = change(code, f"works[{cid}][CHAR_WORKMAXHP]=1000;",
                      f"works[{cid}][CHAR_WORKMAXHP]={var};", "max hp")
        code = change(code, f"works[{cid}][CHAR_WORKULTIMATE]=0;",
                      f"works[{cid}][CHAR_WORKULTIMATE]=ok;", "accumulated overkill")
    # Trace around the unchanged exact DamageSub body, including returned kind.
    old = "return BATTLE_DamageSub_EXACT(\n      attackindex,defindex,pDamage,pPetDamage,pRefrect);"
    new = """note('T',defindex,ints[defindex][CHAR_HP]);
  int kind=BATTLE_DamageSub_EXACT(
      attackindex,defindex,pDamage,pPetDamage,pRefrect);
  note('U',defindex,kind);return kind;"""
    code = change(code, old, new, "DamageSub tracing wrapper")
    # Rename only the original definition. The full unchanged Battling body
    # calls the observation wrapper, which then executes that exact definition.
    code, count = re.subn(r"\bint BATTLE_AddProfit\(", "int BATTLE_AddProfit_EXACT(", code)
    if count != 1:
        raise ValueError("exact AddProfit definition drift")
    battling, _, _ = prior._exact_battling(name, root)
    observation = r'''
static int profit_calls,pre_owner_hp,pre_pet_hp,pre_owner_ult,pre_pet_ult;
int BATTLE_AddProfit(int b,int *list){
  if(profit_calls++==0){
    pre_owner_hp=ints[1][CHAR_HP];pre_pet_hp=ints[2][CHAR_HP];
    pre_owner_ult=!!(BattleArray[0].Side[0].Entry[0].flg&BENT_FLG_ULTIMATE);
    pre_pet_ult=!!(BattleArray[0].Side[0].Entry[5].flg&BENT_FLG_ULTIMATE);
    note('B',1,pre_owner_hp);note('B',2,pre_pet_hp);
  }
  return BATTLE_AddProfit_EXACT(b,list);
}
'''
    code = change(code, battling, observation+"\n"+battling, "profit observation wrapper")
    code = change(code, "int battling_rc=BATTLE_Battling(battleindex);",
                  "profit_calls=0;int battling_rc=BATTLE_Battling(battleindex);"
                  "if(profit_calls!=1)hfail(60);", "one native command tail")
    code = change(code,
                  "if(BATTLE_AddProfit(battleindex,aAttackList)!=BATTLE_ERR_NONE)hfail(41);",
                  """static int before_ints[32][4096],before_works[32][4096],before_flags[32][4096];
    int before_pets[32][5],before_valid[32];BATTLE before_battle=BattleArray[0];
    memcpy(before_ints,ints,sizeof(ints));memcpy(before_works,works,sizeof(works));
    memcpy(before_flags,flags,sizeof(flags));memcpy(before_pets,pets,sizeof(pets));
    memcpy(before_valid,valid,sizeof(valid));
    if(BATTLE_AddProfit(battleindex,aAttackList)!=BATTLE_ERR_NONE)hfail(41);
    if(memcmp(before_ints,ints,sizeof(ints))||memcmp(before_works,works,sizeof(works))||
       memcmp(before_flags,flags,sizeof(flags))||memcmp(before_pets,pets,sizeof(pets))||
       memcmp(before_valid,valid,sizeof(valid))||memcmp(&before_battle,&BattleArray[0],sizeof(BATTLE)))hfail(61);""",
                  "whole-state duplicate suppression")
    start = code.index('    printf("%d %d %d %d %d %d %d %d %d %d %d %d|')
    end = code.index("    if(first_deaths!=", start)
    output = r'''    printf("%d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d|%s\n",
      pre_owner_hp,pre_pet_hp,pre_owner_ult,pre_pet_ult,
      ints[1][CHAR_HP],flags[1][CHAR_ISDIE],ints[1][CHAR_DEADCOUNT],works[1][901],
      ints[2][CHAR_HP],flags[2][CHAR_ISDIE],ints[2][CHAR_DEADCOUNT],works[2][900],
      ints[1][CHAR_DEFAULTPET],ints[1][CHAR_DEADPETCOUNT],
      BATTLE_Index2No(0,1),BATTLE_Index2No(0,2),profit_calls,damage_calls,rand_calls,
      trace);
'''
    code = code[:start]+output+code[end:]
    meta = dict(meta, original_addprofit_body_mechanical_rename_only=True,
                actual_preprofit_hp_ultimate_capture=True,
                id638_work_type=5,id638_work_objects=4,
                status_and_presentation_option_neutralized=True)
    return code, meta


def _expected(case: Case, hp, ultimate):
    # Reuse the accepted canonical boundary fixture, replacing its actual
    # native inputs; do not predict damage or ultimate flags in this adapter.
    seed = prior._canonical_binder_expected(*hp)
    snap = seed.steps[0].result.before
    authority = replace(snap.authority, selected_pet_id="2" if case.selected == 0 else None)
    snapshot = replace(snap, authority=authority, no_risk=bool(case.no_risk),
                       characters={pid: replace(c, ultimate=bool(ultimate[i])) if pid in {"1","2"} else c
                                   for pid,c in snap.characters.items()
                                   for i in [0 if pid == "1" else 1]})
    scan = resolve_profit_exit_scan(snapshot, recipient_id="10")
    # Actual runtime binder, independently from the direct immutable scan.
    from tools.stoneage_battle_round_model import OrdinaryProfitBoundarySnapshot, OrdinaryRoundEvent, PROFIT_BOUNDARY_BATTLEMODEL_COMMAND_TAIL
    from tools.stoneage_battle_status_model import BaseBattleStatusRuntime
    from tools.stoneage_singleplayer_battle import BattleParticipant, BattleSession
    participants = {
        pid: BattleParticipant(participant_id=pid,side="enemy" if pid == "10" else "player",
                               kind=c.kind,level=c.level,hp=c.hp,max_hp=max(1,c.hp),
                               attack=1,defense=1,quick=1,name=pid)
        for pid,c in snapshot.characters.items()
    }
    status = {pid:BaseBattleStatusRuntime() for pid in participants}
    event = OrdinaryRoundEvent("10",10,900,0,"battlemodel_action",battlemodel_skill_id=638)
    boundary = OrdinaryProfitBoundarySnapshot(
        boundary_kind=PROFIT_BOUNDARY_BATTLEMODEL_COMMAND_TAIL,trigger_event_indexes=(0,),
        hp_by_slot={0:hp[0],5:hp[1],10:100},
        occupied_participant_id_by_slot={0:"1",5:"2",10:"10"},
        ultimate_kind_by_slot={slot:2 for slot,flag in zip((0,5),ultimate) if flag},
        prior_processed_death_ids=(),default_pet_authorities_by_owner_id={"1":authority},
        base_status_runtime_by_participant_id=status,nocast_overlay=None)
    binder = resolve_profit_boundary_scans(
        session=BattleSession(None,None,participants["1"],(participants["2"],),(participants["10"],)),
        boundaries=(boundary,),events=(event,),
        persistent_hp_by_participant_id={pid:c.hp for pid,c in snapshot.characters.items()},
        pending_exp_by_participant_id={"10":0},pending_pet_variable_ai_by_participant_id={"2":0},
        pending_player_charm_delta=0,pending_player_dead_pet_count_delta=0,
        base_status_runtime_by_participant_id=status,nocast_overlay=None,
        initial_processed_death_ids=(),no_risk=bool(case.no_risk))
    if scan.after != binder.final_snapshot:
        raise ValueError("direct immutable scan/canonical runtime binder drift")
    chars=scan.after.characters
    expected = tuple(v for pid in ("1","2") for v in (
        chars[pid].hp,int(chars[pid].isdie),chars[pid].death_count,
        chars[pid].charm_delta if pid == "1" else chars[pid].variable_ai_delta))
    expected += (-1 if scan.after.authority.selected_pet_id is None else 0,
                 chars["1"].dead_pet_count,
                 -1 if chars["1"].occupied_slot is None else chars["1"].occupied_slot,
                 -1 if chars["2"].occupied_slot is None else chars["2"].occupied_slot)
    return scan,expected


def analyze_profile(name: str, root: Path):
    head=subprocess.check_output(["git","-C",str(root),"rev-parse","HEAD"],text=True).strip()
    dirty=subprocess.check_output(["git","-C",str(root),"status","--porcelain"],text=True).strip()
    if head != PINNED[name] or dirty:
        raise ValueError("pinned source commit/tree drift")
    code,meta=_source(name,root)
    vectors=cases()
    with tempfile.TemporaryDirectory(prefix="sa-bm-ultimate-tail-") as folder:
        source=Path(folder)/"oracle.c";binary=Path(folder)/"oracle"
        source.write_text(code,encoding="utf-8")
        built=subprocess.run(["cc","-std=c11","-O0","-Wno-unused-value","-Wno-unused-variable",
                              "-Wno-implicit-function-declaration","-Wno-int-conversion",
                              str(source),"-lm","-o",str(binary)],capture_output=True,text=True)
        if built.returncode:
            raise ValueError("ultimate full-driver compile failed: "+built.stderr[-8000:])
        ran=subprocess.run([str(binary)],input="".join(" ".join(map(str,c.row()))+"\n" for c in vectors),
                           capture_output=True,text=True)
        if ran.returncode:
            raise ValueError("ultimate full-driver failed: "+ran.stderr[-4000:]+ran.stdout[-4000:])
    rows=ran.stdout.splitlines()
    if len(rows)!=len(vectors):
        raise ValueError("ultimate full-driver row count drift")
    witnesses=[]
    for case,row in zip(vectors,rows):
        values,trace=row.split("|",1);got=tuple(map(int,values.split()))
        if len(got)!=19:
            raise ValueError("ultimate output shape drift")
        scan,expected=_expected(case,got[:2],got[2:4])
        if got[4:16]!=expected:
            raise ValueError(f"{name}/{case.name}: {got[4:16]} != {expected}; trace={trace}")
        semantic=[x for x in trace.rstrip(",").split(",") if x]
        boundary_at=next(i for i,x in enumerate(semantic) if x.startswith("B:"))
        hp_order=tuple(x.split(":")[1] for x in semantic[:boundary_at] if x.startswith("H:"))
        death_order=tuple(x.split(":")[1] for x in semantic[boundary_at:] if x.startswith("D:"))
        if death_order!=scan.processed_death_ids:
            raise ValueError("native death order/duplicate suppression drift")
        native_exits=tuple(x.split(":")[1] for x in semantic if x.startswith("X:"))
        scan_exits=tuple(e.participant_id for e in scan.effects if e.kind == "exit_request")
        if native_exits!=scan_exits:
            raise ValueError("native exit request chronology drift")
        if any(x.startswith(("F:","D:","X:")) for x in semantic[:boundary_at]):
            raise ValueError("death/exit before native command-tail profit")
        if case.guardian and not hp_order[:1]==("2",):
            raise ValueError("original Guardian first victim drift")
        if case.guardian and case.owner_hp==1 and hp_order!=("2","1"):
            raise ValueError("pet5->owner0 native hit chronology drift")
        if "ultimate2_both_owner_first" in case.name:
            if got[2:4]!=(1,1) or death_order!=("1",) or got[12]!=0:
                raise ValueError("owner-first ultimate skips pet death and retains selection")
        if "ultimate1_both_owner_first" in case.name:
            kinds=[int(x.split(":")[2]) for x in semantic if x.startswith("U:")]
            if kinds!=[1,1]:
                raise ValueError("accumulated-overkill ultimate1 witness drift")
        if "ultimate2_pet_only" in case.name and (got[2:4]!=(0,1) or got[12]!=-1):
            raise ValueError("standalone pet ultimate selection clear drift")
        if got[16]!=2:
            raise ValueError("exact one command tail plus idempotent repeat required")
        witnesses.append(dict(case=case.name,preprofit_hp=got[:2],ultimate_flags=got[2:4],
                              hit_hp_write_ids=hp_order,processed_death_ids=death_order,
                              exit_request_ids=native_exits,repeat_entire_state_unchanged=True,
                              final_default_pet_slot=got[12],final_occupied_slots=got[14:16]))
    return dict(profile=name,commit=head,native_ultimate_full_battling_cases=len(vectors),
                canonical_runtime_binder_comparisons=len(vectors),witnesses=witnesses,**meta)


def main():
    parser=argparse.ArgumentParser()
    for name in PINNED:
        parser.add_argument("--"+name+"-dir",required=True,type=Path)
    args=parser.parse_args();total=0
    for name in PINNED:
        result=analyze_profile(name,getattr(args,name+"_dir"));total+=result["native_ultimate_full_battling_cases"]
        print("PROFILE|"+json.dumps(result,sort_keys=True))
    print(f"TOTAL|native_ultimate_full_battling_cases={total}|profiles={len(PINNED)}")
    print("BOUNDARY|accepted_reduced_driver_helpers_unchanged;ride_items_AI_packets_original_build_version_OPEN")
    print("RESOLUTION|BATTLEMODEL_ULTIMATE_FULL_BATTLING_PROFIT_TAIL_NATIVE_PASS")


if __name__ == "__main__":
    main()
