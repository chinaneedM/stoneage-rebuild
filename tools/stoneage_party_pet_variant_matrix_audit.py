"""Bounded original real-header party/owned-pet negative admission matrix.

This is NOT a simulated battle implementation: it composes the previously
accepted native source recovery, real headers, original CreateVsEnemy and
original Exit/Delete calls. It only changes a constructed test driver's
preconditions, observations and expected outputs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile

from tools.stoneage_party_pet_full_exit_audit import make_reentry_native
from tools.stoneage_party_pet_realheader_audit import patch_source
from tools.stoneage_player_battle_audit import domain as solo_domain, pinned_identity, PIN_PATH
from tools.stoneage_enemy_entry_exit_audit import compile_probe
from tools.stoneage_enemy_loader_audit import specimen, loaded_oracle, eligible, pp_file
from tools.stoneage_guard_break2_source_audit import PINNED, LAYOUTS
from tools.stoneage_enemy_creation_audit import definition

SCENARIOS = (
    "healthy", "member_busy", "member_final", "no_default",
    "missing_selected_slot", "pet_zero_hp", "pet_dead_flag",
    "pet_roster_unlinked",
)
ENTRY_RESET = "  slots[2].workint[CHAR_WORKBATTLEINDEX]=-1;\n"
DRIVER_START = "  BATTLE *battle=&BattleArray[battle_at];\n"
DRIVER_END = "  /* bounded multi-battle reentry */\n"

# This is controlled fixture state, not original game code. Restore every
# named precondition before calling original battle functions. In particular,
# a 777 GETEXP sentinel distinguishes a skipped teammate/absent owned pet
# from successful original ClearGetExp.
PRECONDITIONS = r"""
  demand(scenario>=0&&scenario<8,"variant index");
  slots[0].data[CHAR_DEFAULTPET]=0;
  slots[0].unionTable.indexOfPet[0]=2;
  slots[2].data[CHAR_HP]=20;
  slots[2].flg[CHAR_ISDIE/8] &= (unsigned char)~(1u<<(CHAR_ISDIE%8));
  if(scenario==1)slots[1].workint[CHAR_WORKBATTLEMODE]=BATTLE_CHARMODE_C_WAIT;
  if(scenario==2)slots[1].workint[CHAR_WORKBATTLEMODE]=BATTLE_CHARMODE_FINAL;
  if(scenario==3)slots[0].data[CHAR_DEFAULTPET]=-1;
  if(scenario==4)slots[0].data[CHAR_DEFAULTPET]=1;
  if(scenario==5)slots[2].data[CHAR_HP]=0;
  if(scenario==6)slots[2].flg[CHAR_ISDIE/8] |= (unsigned char)(1u<<(CHAR_ISDIE%8));
  if(scenario==7)slots[0].unionTable.indexOfPet[0]=-1;
"""
OBSERVATIONS = r"""
  BATTLE *battle=&BattleArray[battle_at];
  int want_member=(scenario!=1&&(scenario!=2||IS_BISMARCK));
  int want_pet=(scenario<=2);
  int want_selection=(scenario<=2)?0:-1;
  int want_pet_exp=(scenario==7)?777:0;
  demand(battle->Side[0].Entry[0].ENTRY_FIELD==0,"variant leader front");
  demand(battle->Side[0].Entry[1].ENTRY_FIELD==(want_member?1:-1),"variant teammate front");
  demand(battle->Side[0].Entry[5].ENTRY_FIELD==(want_pet?2:-1),"variant selected pet rear");
  demand(slots[0].workint[CHAR_WORKBATTLEINDEX]==battle_at,"variant leader index");
  demand(slots[1].workint[CHAR_WORKBATTLEINDEX]==(want_member?battle_at:-1),"variant teammate index");
  demand(slots[2].workint[CHAR_WORKBATTLEINDEX]==(want_pet?battle_at:-1),"variant pet index");
  demand(slots[0].workint[CHAR_WORKGETEXP]==0,"variant leader experience reset");
  demand(slots[1].workint[CHAR_WORKGETEXP]==(want_member?0:777),"variant teammate experience reset");
  demand(slots[2].workint[CHAR_WORKGETEXP]==want_pet_exp,"variant pet experience reset");
  demand(slots[0].data[CHAR_DEFAULTPET]==want_selection,"variant original selected pet normalization");
  demand(slots[0].unionTable.indexOfPet[0]==(scenario==7?-1:2),"variant original roster ownership");
  demand(slots[2].use,"variant retained allocated pet");
  demand(searchObjectFromCharaIndex(0)==0&&searchObjectFromCharaIndex(1)==1,"variant world registration");
  dprintf(2,"TRACE|HP_BEFORE_EXIT|scenario=%d|hp=%d\n",scenario,slots[2].data[CHAR_HP]);
  int leader_exit=BATTLE_Exit(0,battle_at);
  demand(leader_exit==0,"variant original leader Exit");
  demand(battle->Side[0].Entry[0].ENTRY_FIELD==-1,"variant leader slot exited");
  demand(battle->Side[0].Entry[5].ENTRY_FIELD==-1,"variant pet slot exited");
  demand(battle->Side[0].Entry[1].ENTRY_FIELD==(want_member?1:-1),"variant member retained before own Exit");
  demand(slots[0].workint[CHAR_WORKBATTLEINDEX]==-1,"variant leader index cleared");
  demand(slots[2].workint[CHAR_WORKBATTLEINDEX]==-1,"variant pet index cleared");
  demand(slots[2].workint[CHAR_WORKBATTLEMODE]==BATTLE_CHARMODE_NONE,"variant pet not in battle");
  if(want_member){
    demand(BATTLE_Exit(1,battle_at)==0,"variant original teammate Exit");
    demand(battle->Side[0].Entry[1].ENTRY_FIELD==-1,"variant teammate slot exited");
  }
  BATTLE_ExitAll(battle_at);
  demand(BATTLE_DeleteBattle(battle_at)==0,"variant original delete");
  demand(!BattleArray[battle_at].use&&Battle_getTotalBattleNum()==0,"variant battle pool freed");
  demand(slots[0].use&&slots[1].use&&slots[2].use,"variant original actors retained");
  demand(slots[0].data[CHAR_DEFAULTPET]==want_selection,"variant selected pet retained after Exit");
  demand(slots[0].unionTable.indexOfPet[0]==(scenario==7?-1:2),"variant owned pet retained after Exit");
  dprintf(2,"TRACE|HP_VARIANT|scenario=%d|post_exit=%d\n",scenario,slots[2].data[CHAR_HP]);
  demand(slots[2].data[CHAR_HP]==((scenario==5||scenario==6)?1:20),"variant pet HP compliant after Exit");
  dprintf(2,"TRACE|FLAG_VARIANT|scenario=%d|post_exit=%d\n",scenario,!!(slots[2].flg[CHAR_ISDIE/8]&(1u<<(CHAR_ISDIE%8))));
  demand(!(slots[2].flg[CHAR_ISDIE/8]&(1u<<(CHAR_ISDIE%8))),"variant pet death flag reset by original Exit");
  demand(searchObjectFromCharaIndex(0)==0&&searchObjectFromCharaIndex(1)==1,"variant world actors retained after Exit");
  printf("\nMATRIX|scenario=%d|mode=%d|battle=%d|member=%d|pet=%d|default=%d|owned=%d|pet_HP=%d|pet_dead=%d|pet_exp=%d|arena_freed=1\n",
    scenario,mode,battle_at,want_member,want_pet,slots[0].data[CHAR_DEFAULTPET],
    slots[0].unionTable.indexOfPet[0],slots[2].data[CHAR_HP],
    !!(slots[2].flg[CHAR_ISDIE/8]&(1u<<(CHAR_ISDIE%8))),slots[2].workint[CHAR_WORKGETEXP]);
"""

def native(profile: str, source: str) -> str:
    original = make_reentry_native(profile, source)
    # Each replacement has a one-shot guard, so newly changed accepted
    # fixture code cannot accidentally turn this into a different probe.
    required = (
        (ENTRY_RESET, ENTRY_RESET+PRECONDITIONS),
        ("int array,mode;\n while(scanf(\"%d%d\",&array,&mode)==2){",
         "int array,mode,scenario;\n while(scanf(\"%d%d%d\",&array,&mode,&scenario)==3){"),
    )
    for old, new in required:
        if original.count(old)!=1:
            raise ValueError("accepted native variant precondition anchor drift "+repr(old))
        original=original.replace(old,new,1)
    begin=original.index(DRIVER_START)
    end=original.index(DRIVER_END,begin)
    body=OBSERVATIONS.replace("ENTRY_FIELD","char_index" if profile=="bismarck" else "charaindex")
    body=body.replace("IS_BISMARCK","1" if profile=="bismarck" else "0")
    return original[:begin]+body+original[end:]


def main():
    ap=argparse.ArgumentParser()
    for p in PINNED:ap.add_argument("--"+p+"-dir",type=Path,required=True)
    args=ap.parse_args()
    roots={p:getattr(args,p+"_dir") for p in PINNED}
    for profile,root in roots.items():
        head=subprocess.check_output(["git","-C",str(root),"rev-parse","HEAD"],text=True).strip()
        clean=subprocess.check_output(["git","-C",str(root),"status","--porcelain"],text=True).strip()
        if head!=PINNED[profile] or clean:
            raise ValueError("original source pin/cleanliness "+profile)
    paths,receipt=specimen(roots["gavin"])
    accepted=json.loads(PIN_PATH.read_text())
    if receipt!=accepted["preserved_specimen"]:
        raise ValueError("accepted preserved original master drift")
    for profile in ("gavin","bismarck"):
        source,identity,*rest=solo_domain(profile,roots[profile])
        if pinned_identity(identity)!=accepted["profiles"][profile]["identity"]:
            raise ValueError("accepted original solo domain identity drift "+profile)
        source=patch_source(source,profile)
        source+="\n"+definition(pp_file(profile,roots[profile],LAYOUTS[profile]/"battle/battle.c"),"BATTLE_Index2No")+"\n"
        loader=identity["accepted_pool_identity"]["accepted_entry_identity"]["accepted_ownership_identity"]["accepted_loader_identity"]
        templates,enemies=loaded_oracle(profile,loader,*[p.read_bytes() for p in paths],32,32)
        ride=rest[-1]
        selection=eligible(loader,templates,enemies,ride)[0]
        source=native(profile,source)
        traps=[x for x in accepted["profiles"][profile]["unreachable_traps"] if
               x not in ("BATTLE_Index2No","RIDEPET_getPETindex","CHAR_sendCToArroundCharacter","CHAR_send_K_StatusString")]
        observations=[]
        with tempfile.TemporaryDirectory(prefix="stoneage-party-negative-") as d:
            for opt in ("-O0","-O2"):
                exe=Path(d)/("probe"+opt)
                compile_probe(profile,roots[profile],source,exe,opt,traps)
                case_input="".join(f"{selection} {i%4} {i}\n" for i in range(len(SCENARIOS)))
                run=subprocess.run([str(exe),*map(str,paths)],input=case_input,
                                   capture_output=True,text=True)
                if run.returncode or any(not l.startswith("TRACE|") for l in run.stderr.splitlines() if l.strip()):
                    addrs=re.findall(r"probe-(?:O0|O2)\(\+(0x[0-9a-f]+)\)",run.stderr)
                    trace=subprocess.run(["addr2line","-f","-C","-e",str(exe),*addrs],
                                         capture_output=True,text=True).stdout if addrs else "NO_BACKTRACE_OFFSETS"
                    raise ValueError("original negative variant "+profile+" "+opt+
                                     " rc="+str(run.returncode)+
                                     " stderr="+run.stderr[-4500:]+
                                     " symbols="+trace+" stdout="+run.stdout[-1700:])
                lines=[l for l in run.stdout.splitlines() if l.startswith("MATRIX|")]
                if len(lines)!=len(SCENARIOS):raise ValueError("missing negative matrix cases "+profile+" rows="+str(len(lines))+" stdout_tail="+run.stdout[-1700:])
                for i,l in enumerate(lines):
                    if f"|scenario={i}|mode={i%4}|battle={i%3}|" not in l:
                        raise ValueError("negative matrix sequence/cursor "+profile+" "+str(i))
                    if "|arena_freed=1" not in l:raise ValueError("negative matrix arena not freed")
                observations.append(run.stdout)
        if observations[0]!=observations[1]:
            raise ValueError("original negative matrix O0/O2 divergence "+profile)
        sha=hashlib.sha256(observations[0].encode()).hexdigest()
        print(f"PROFILE|{profile}|scenarios={len(SCENARIOS)}|cycles={2*len(SCENARIOS)}|pool_cursor=0,1,2,0,1,2,0,1|optimizations=O0,O2|sha256={sha}",flush=True)
        for line in observations[0].splitlines():
            if line.startswith("MATRIX|"):print("ACTUAL|"+profile+"|"+line,flush=True)
    print("BOUNDARY|controlled_healthy_players_2_owned_pet_2_original_pinned_descendants_not_1999_2000_or_full_runtime",flush=True)
    print("OPEN|natural_party_roster_other_pets_profit_Init_TaskLoop_true_transport_original_reclaimer_full_server",flush=True)
    print("RESOLUTION|ORIGINAL_REAL_HEADER_PARTY_PET_NEGATIVE_MATRIX_BOUNDED_PASS_NO_HISTORICAL_PROMOTION",flush=True)


if __name__=="__main__":
    main()
