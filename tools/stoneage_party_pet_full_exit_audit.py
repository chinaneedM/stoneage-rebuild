"""Execute original real-header populated party/pet battle teardown and slot reuse.

Extends the accepted actual original combined entry domain; cannot promote
the original 1999 client or complete victory/profit without independent tests.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import subprocess
import tempfile
import hashlib
import json
import re

from tools.stoneage_party_pet_realheader_audit import native as admission_native, patch_source
from tools.stoneage_player_battle_audit import domain as solo_domain, pinned_identity, PIN_PATH
from tools.stoneage_enemy_entry_exit_audit import compile_probe
from tools.stoneage_enemy_loader_audit import specimen, loaded_oracle, eligible
from tools.stoneage_guard_break2_source_audit import PINNED, LAYOUTS
from tools.stoneage_enemy_loader_audit import pp_file
from tools.stoneage_enemy_creation_audit import definition

EXPECTED_INSERT=r"""
  /* Owner exit must release paired pet without inventing a pet packet. */
  int exit0=BATTLE_Exit(0,battle_at);
  demand(exit0==0,"leader original Exit return");
  demand(battle->Side[0].Entry[0].ENTRY_FIELD==-1,"leader slot released");
  demand(battle->Side[0].Entry[5].ENTRY_FIELD==-1,"owned pet paired slot released");
  demand(battle->Side[0].Entry[1].ENTRY_FIELD==1,"teammate retained until own Exit");
  demand(slots[0].workint[CHAR_WORKBATTLEINDEX]==-1,"leader leave battle index");
  demand(slots[0].workint[CHAR_WORKBATTLEMODE]==BATTLE_CHARMODE_FINAL,"leader FINAL on direct Exit");
  demand(slots[2].workint[CHAR_WORKBATTLEINDEX]==-1,"paired pet leave battle index");
  demand(slots[2].workint[CHAR_WORKBATTLEMODE]==BATTLE_CHARMODE_NONE,"pet NONE after owner Exit");
  demand(slots[0].data[CHAR_DEFAULTPET]==0&&slots[0].unionTable.indexOfPet[0]==2,"owned pet preserved on Exit");
  demand(slots[2].use,"owned pet remains live");
  demand(searchObjectFromCharaIndex(0)==0&&searchObjectFromCharaIndex(1)==1,"world objects preserved after leader exit");
  int exit1=BATTLE_Exit(1,battle_at);
  demand(exit1==0,"party member original Exit return");
  demand(battle->Side[0].Entry[1].ENTRY_FIELD==-1,"member slot released");
  demand(slots[1].workint[CHAR_WORKBATTLEINDEX]==-1,"member leave battle index");
  demand(slots[1].workint[CHAR_WORKBATTLEMODE]==BATTLE_CHARMODE_FINAL,"member FINAL on direct Exit");
  BATTLE_ExitAll(battle_at);
  int del=BATTLE_DeleteBattle(battle_at);
  demand(del==0,"original arena delete");
  demand(BattleArray[battle_at].use==0,"battle pool freed");
  demand(Battle_getTotalBattleNum()==0,"battle total freed");
  demand(slots[2].use&&slots[0].use&&slots[1].use,"three living actors preserved");
  printf("\nREAL_HEADER_EXIT|array=%d|mode=%d|battle=%d|leader_slot=-1|member_slot=-1|pet_slot=-1|pet_mode=NONE|owned=2|battle_deleted=1\n",array,mode,battle_at);
"""
MARKER=r"""  /* Exit is intentionally not asserted by this first admission gate.
     The accepted solo teardown is not equivalent to populated pet Exit. */
"""
# The original RIDEPET_getPETindex predicate requires a nonzero intersection
# of ride-license bits and ride-code bits to return a nonnegative index.
# This controlled fixture has CHAR_LOWRIDEPETS==0, so the exact predicate
# must return -1 without needing the original ride-code table. Anything
# beyond that bounded domain remains a hard failure, not simulated game code.
ZERO_LICENSE_RIDE=r"""
static int zero_license_ride_queries=0;
int RIDEPET_getPETindex(int petNo,int learnCode){
  (void)petNo;
  if(learnCode!=0){fputs("RIDE_LICENSE_SCOPE_VIOLATION",stderr);abort();}
  zero_license_ride_queries++;
  return -1;
}
"""
# The original Exit graph broadcasts refreshed world-character state.
# This is an explicit packet-output collector, not a claim to reproduce
# original transport or all visible players in a real map.
WORLD_BROADCAST=r"""
static int world_broadcasts=0;
void CHAR_sendCToArroundCharacter(int objindex){
  if(objindex<0||objindex>1||searchObjectFromCharaIndex(objindex)!=objindex){
    fputs("WORLD_BROADCAST_SCOPE_VIOLATION",stderr);abort();
  }
  world_broadcasts++;
}
"""
# An owned pet's battle-return state is sent to its player in the original
# K-status packet API. Transport remains outside this test. Only player0's
# exactly selected and retained roster slot0 is admitted by this collector.
PET_STATUS=r"""
static int owned_pet_status_packets=0;
BOOL CHAR_send_K_StatusString(int player,int roster_slot,unsigned int mask){
  if(player!=0||roster_slot!=0||!mask||CHAR_getCharPet(0,0)!=2){
    fputs("PET_STATUS_SCOPE_VIOLATION",stderr);abort();
  }
  owned_pet_status_packets++;
  return TRUE;
}
"""
def make_native(profile,source):
    original=admission_native(profile,source)
    # The prior entry-only network collector admits 0/1. During owned-pet
    # teardown, original compliance may address the real pet actor index 2.
    # This change is limited to the typed status output collector only.
    actor="char_index" if profile=="bismarck" else "charaindex"
    status=definition(original,"CHAR_send_P_StatusString")
    scoped=f"if({actor}!=0&&{actor}!=1)abort();status_count++;"
    if status.count(scoped)!=1:raise ValueError("accepted teammate status collector drift")
    expanded=f"if({actor}!=0&&{actor}!=1&&{actor}!=2)abort();status_count++;"
    original=original.replace(status,status.replace(scoped,expanded),1)
    # Original healthy teammate Exit reaches the same battle-time guard.
    # Preserve all pinned fd/clock/time expectations; allow only the two
    # concrete player actors in this controlled battle.
    timer=definition(original,"CheckDefBTime")
    solo=f"if({actor}!=0||fd!=7||lowTime!=1000||battletime!=2||addTime!=0)abort();"
    pair=f"if(({actor}!=0&&{actor}!=1)||fd!=7||lowTime!=1000||battletime!=2||addTime!=0)abort();"
    if timer.count(solo)!=1:raise ValueError("accepted battle time collector drift")
    original=original.replace(timer,timer.replace(solo,pair),1)
    if original.count(MARKER)!=1:raise ValueError("accepted admission body changed")
    anchor="int main(int argc,char **argv){"
    if original.count(anchor)!=1:raise ValueError("actual original main anchor drift")
    original=original.replace(anchor,ZERO_LICENSE_RIDE+WORLD_BROADCAST+PET_STATUS+anchor,1)
    field="char_index" if profile=="bismarck" else "charaindex"
    return original.replace(MARKER,EXPECTED_INSERT.replace("ENTRY_FIELD",field),1)

def main():
    ap=argparse.ArgumentParser()
    for p in PINNED:ap.add_argument("--"+p+"-dir",type=Path,required=True)
    args=ap.parse_args()
    roots={p:getattr(args,p+"_dir") for p in PINNED}
    for p,root in roots.items():
        if subprocess.check_output(["git","-C",str(root),"rev-parse","HEAD"],text=True).strip()!=PINNED[p]:
            raise ValueError("source pin drift "+p)
        if subprocess.check_output(["git","-C",str(root),"status","--porcelain"],text=True).strip():
            raise ValueError("dirty source "+p)
    paths,receipt=specimen(roots["gavin"])
    accepted=json.loads(PIN_PATH.read_text())
    if receipt!=accepted["preserved_specimen"]:raise ValueError("specimen drift")
    for profile in ("gavin","bismarck"):
        source,identity,*_=solo_domain(profile,roots[profile])
        if pinned_identity(identity)!=accepted["profiles"][profile]["identity"]:
            raise ValueError("accepted solo source drift")
        source=patch_source(source,profile)
        source+="\n"+definition(pp_file(profile,roots[profile],LAYOUTS[profile]/"battle/battle.c"),"BATTLE_Index2No")+"\n"
        loader=identity["accepted_pool_identity"]["accepted_entry_identity"]["accepted_ownership_identity"]["accepted_loader_identity"]
        temps,enemies=loaded_oracle(profile,loader,*[p.read_bytes() for p in paths],32,32)
        _,_,_,_,_,ride=solo_domain(profile,roots[profile])
        selection=eligible(loader,temps,enemies,ride)[0]
        native=make_native(profile,source)
        with tempfile.TemporaryDirectory(prefix="stoneage-realheader-party-exit-") as d:
            observations=[]
            for opt in ("-O0","-O2"):
                exe=Path(d)/("probe"+opt)
                compile_probe(profile,roots[profile],native,exe,opt,
                    [x for x in accepted["profiles"][profile]["unreachable_traps"] if x not in ("BATTLE_Index2No","RIDEPET_getPETindex","CHAR_sendCToArroundCharacter","CHAR_send_K_StatusString")])
                run=subprocess.run([str(exe),*map(str,paths)],input=f"{selection} 0\n",capture_output=True,text=True)
                if run.returncode or any(not line.startswith("TRACE|") for line in run.stderr.splitlines() if line.strip()):
                    offsets=re.findall(r"probe-(?:O0|O2)\(\+(0x[0-9a-f]+)\)",run.stderr)
                    symbols=subprocess.run(["addr2line","-f","-C","-e",str(exe),*offsets],
                                           capture_output=True,text=True).stdout if offsets else "NO_OFFSETS"
                    raise ValueError("actual original party/pet Exit "+profile+" "+opt+
                                     " rc="+str(run.returncode)+" stderr="+run.stderr[-7000:]+
                                     " symbols="+symbols+" stdout="+run.stdout[-2000:])
                if run.stdout.count("REAL_HEADER_ENTRY|")!=1 or run.stdout.count("REAL_HEADER_EXIT|")!=1:
                    raise ValueError("missing actual entry/exit outputs")
                observations.append(run.stdout)
            if observations[0]!=observations[1]:
                raise ValueError("actual original populated player/pet Exit optimization mismatch")
            print("PROFILE|"+profile+"|original_sources=PINNED|cycles=2|optimizations=O0,O2|sha256="+
                  hashlib.sha256(observations[0].encode()).hexdigest(),flush=True)
            for line in observations[0].splitlines():
                if line.startswith("REAL_HEADER_ENTRY|") or line.startswith("REAL_HEADER_EXIT|"):
                    print("ACTUAL|"+profile+"|"+line,flush=True)
    print("RESOLUTION|ORIGINAL_REAL_HEADER_PARTY_PET_EXIT_AND_DELETE_BOUNDED_PASS_NO_PROFIT_CLAIM",flush=True)
if __name__=="__main__":main()
