"""Same-harness exact DamageSub + Guardian + BattleModel + tail AddProfit R1.

Extends the accepted same-harness original Guardian audit by replacing the
controlled DamageSub seam with the exact pinned original BATTLE_DamageSub body.

The original BattleModel helper leaves iPetDamage uninitialised before the call.
For this gameplay-state audit a wrapper seeds only that presentation/output
integer to zero, matching the independent accepted DamageSub oracle input. The
exact DamageSub body itself is unchanged after a mechanical symbol rename.
This does not certify historical packet/presentation bytes.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
import re
import subprocess
import tempfile

from tools.stoneage_guard_break2_source_audit import PINNED, LAYOUTS, _text, _sha
from tools.stoneage_mdfyattack_source_audit import _definition, _strip
from tools import stoneage_battlemodel_guardian_profit_tail_source_audit as guardian
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
        Case(1,1000,1,100),
        Case(0,1,1,100),
    )


def _exact_damage_body(name: str, root: Path):
    path=root/LAYOUTS[name]/"battle/battle_event.c"
    body=_definition(_strip(_text(path)),"BATTLE_DamageSub")
    return body,_sha(path)


def _same_harness_damage_source(name: str, root: Path):
    code,meta=guardian._same_harness_source(name,root)
    damage_body,event_sha=_exact_damage_body(name,root)

    old_stub='''int BATTLE_DamageSub(int a,int d,int *damage,int *pet,int *react){
  damage_calls++;*pet=0;if(react)*react=-1;
  ints[d][CHAR_HP]-=*damage;if(ints[d][CHAR_HP]<0)ints[d][CHAR_HP]=0;
  note('M',d,*damage);return 0;
}
'''
    if old_stub not in code:
        raise ValueError("accepted Guardian DamageSub seam drift")

    renamed=damage_body.replace(
        "BATTLE_DamageSub(",
        "BATTLE_DamageSub_EXACT(",
        1,
    )
    if renamed==damage_body:
        raise ValueError("exact DamageSub rename failed")

    forward=r'''
int BATTLE_getRidePet(int i);
int CHAR_getItemIndex(int i,int slot);
void BATTLE_changeRideImage(int i);
int print(char *fmt,...);
'''
    wrapper=r'''
int BATTLE_DamageSub(int attackindex,int defindex,int *pDamage,
                     int *pPetDamage,int *pRefrect){
  damage_calls++;
  /* Source BattleModel helper leaves this local presentation value
     uninitialised. Normalize only that undefined input; HP/ultimate/reaction
     work is still the exact original DamageSub body. */
  *pPetDamage=0;
  return BATTLE_DamageSub_EXACT(
      attackindex,defindex,pDamage,pPetDamage,pRefrect);
}
'''
    code=code.replace(
        old_stub,
        forward+"\n"+renamed+"\n"+wrapper,
    )

    # Enable only the source marker branch needed by the BattleModel call.
    code="#define _PETSKILL_BATTLE_MODEL\n"+code

    # Exact DamageSub no-ride dependency.
    target='int BATTLE_adjustRidePet3A(int c,int pet,int p,int side){hfail(50);return 0;}\n'
    if target not in code:
        raise ValueError("same-harness ride dependency anchor drift")
    code=code.replace(
        target,
        target+"void BATTLE_changeRideImage(int c){}\n",
    )

    # Add getter-key constants required only by the exact DamageSub body.
    existing=set(re.findall(r"^#define\s+(\w+)\b",code,re.M))
    names=sorted(set(re.findall(
        r"\b(?:CHAR|BATTLE|ITEM)_[A-Z][A-Z0-9_]*\b",
        damage_body,
    )))
    calls=set(re.findall(r"\b([A-Za-z_]\w*)\s*\(",damage_body))
    next_id=2600
    additions=[]
    for symbol in names:
        if symbol in existing or symbol in calls:
            continue
        additions.append(f"#define {symbol} {next_id}")
        next_id+=1
    if next_id>=4096:
        raise ValueError("DamageSub getter keys exceed same-harness storage")
    code="\n".join(additions)+"\n"+code

    # Make HP/maxHP and overkill accumulation internally consistent. The
    # primary witness remains deliberately non-ultimate; lethal/ultimate
    # composition stays a separate gate.
    anchor="    works[10][CHAR_WORKATTACKPOWER]=dmg;\n"
    setup='''    works[1][CHAR_WORKMAXHP]=1000;
    works[2][CHAR_WORKMAXHP]=1000;
    works[10][CHAR_WORKMAXHP]=1000;
    works[1][CHAR_WORKULTIMATE]=0;
    works[2][CHAR_WORKULTIMATE]=0;
    works[10][CHAR_WORKULTIMATE]=0;
'''
    if anchor not in code:
        raise ValueError("same-harness attack-power setup anchor drift")
    code=code.replace(anchor,anchor+setup)

    meta=dict(meta)
    meta.update({
        "same_harness_exact_damagesub_body":True,
        "damage_sub_event_sha256":event_sha,
        "damage_sub_comment_stripped_sha256":sha256(
            damage_body.encode()
        ).hexdigest(),
        "damage_sub_petdamage_ub_seeded_zero":True,
        "damage_sub_controlled":False,
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

    code,meta=_same_harness_damage_source(name,root)
    vectors=cases()
    with tempfile.TemporaryDirectory(prefix="sa-bm-damagesub-profit-tail-") as folder:
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
                "same-harness exact DamageSub compile failed: "
                +built.stderr[-12000:]
            )
        executed=subprocess.run(
            [str(binary)],
            input="".join(" ".join(map(str,c.row()))+"\n" for c in vectors),
            text=True,capture_output=True,
        )
        if executed.returncode:
            raise ValueError(
                "same-harness exact DamageSub execution failed: "
                f"returncode={executed.returncode}; stderr={executed.stderr[-6000:]}; "
                f"stdout={executed.stdout[-6000:]}"
            )
        rows=executed.stdout.splitlines()

    if len(rows)!=len(vectors):
        raise ValueError("same-harness exact DamageSub row count drift")

    for case,row in zip(vectors,rows):
        values,trace=row.split("|",1)
        got=tuple(map(int,values.split()))
        if len(got)!=12:
            raise ValueError("same-harness exact DamageSub output shape drift")
        _,damage_calls,target_checks,rand_calls,owner_hp,owner_die,owner_deaths,owner_charm,pet_hp,pet_die,pet_deaths,pet_ai=got
        result=_scan_expected(owner_hp,pet_hp)
        after=result.after.characters
        actual=(owner_die,owner_deaths,owner_charm,pet_die,pet_deaths,pet_ai)
        expected=(
            int(after["1"].isdie),after["1"].death_count,after["1"].charm_delta,
            int(after["2"].isdie),after["2"].death_count,after["2"].variable_ai_delta,
        )
        if actual!=expected:
            raise ValueError(
                f"exact DamageSub profit state drift {case}: "
                f"{actual} != {expected}; full={got}; trace={trace}"
            )
        semantic=[x for x in trace.rstrip(",").split(",") if x]
        first_death=next(
            (i for i,x in enumerate(semantic) if x.startswith("F:")),
            len(semantic),
        )
        preprofit=semantic[:first_death]
        hp_writes=[x for x in preprofit if x.startswith("H:")]
        if case.guardian_enabled:
            if not hp_writes or not hp_writes[0].startswith("H:2:"):
                raise ValueError(
                    f"exact DamageSub first Guardian target drift: {hp_writes}"
                )
            if case.owner_hp==1 and case.pet_hp==1:
                if len(hp_writes)<2 or not hp_writes[1].startswith("H:1:"):
                    raise ValueError(
                        f"exact DamageSub second target did not fall back to owner: {hp_writes}"
                    )
                if result.processed_death_ids!=("1","2"):
                    raise ValueError("exact DamageSub multi-victim scan order drift")
        else:
            if not hp_writes or not hp_writes[0].startswith("H:1:"):
                raise ValueError(
                    f"exact DamageSub no-Guardian target drift: {hp_writes}"
                )
        if damage_calls!=len(hp_writes):
            raise ValueError(
                f"exact DamageSub call/HP-write drift: calls={damage_calls}, writes={hp_writes}"
            )
        if any(x.startswith("S:1:-1") for x in semantic):
            raise ValueError(
                "noncritical exact DamageSub baseline unexpectedly entered pet ultimate"
            )
        if rand_calls<=0 or target_checks<damage_calls:
            raise ValueError("same-harness exact DamageSub chronology counters drift")

    return {
        "profile":name,
        "commit":head,
        "native_same_harness_exact_damagesub_tail_cases":len(vectors),
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
        total+=result["native_same_harness_exact_damagesub_tail_cases"]
        import json
        print("PROFILE|"+json.dumps(result,sort_keys=True))
    print(
        "TOTAL|native_same_harness_exact_damagesub_tail_cases="
        f"{total}|profiles={len(PINNED)}"
    )
    print("FACT|exact_original_AttackSeq_GuardianCheck_DamageSub_BattleModel_helper_and_tail_AddProfit_link_in_one_transient_program")
    print("FACT|exact_DamageSub_HP_writes_finish_before_tail_ISDIE_and_source_order_multi_victim_scan")
    print("FACT|undefined_BattleModel_iPetDamage_input_is_seeded_zero_only_at_DamageSub_wrapper_boundary_and_not_used_as_gameplay_certificate")
    print("BOUNDARY|feature_off_no_ride_no_equipment_no_reaction_noncritical_controlled_status_presentation_notifications_getters")
    print("OPEN|full_BATTLE_Battling_body_unseeded_historical_pPetDamage_presentation_lethal638_modern_admission")
    print("RESOLUTION|BATTLEMODEL_SAME_HARNESS_EXACT_DAMAGESUB_PROFIT_TAIL_NATIVE_PASS")


if __name__=="__main__":
    main()
