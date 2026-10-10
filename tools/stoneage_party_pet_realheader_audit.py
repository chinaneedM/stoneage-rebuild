"""Real-header original party + owned selected pet CreateVsEnemy admission bridge.

Composes accepted solo original-source closures. Controlled *preparation* of a
live pet via original CHAR_initCharOneArray; no standalone legacy sources ship.
This is a bounded native execution of real BATTLE_NewEntry, not profit/full Exit.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import subprocess
import tempfile
from tools.stoneage_player_battle_audit import domain as solo_domain, native_source as solo_native, pinned_identity, PIN_PATH
from tools.stoneage_enemy_entry_exit_audit import compile_probe
from tools.stoneage_enemy_loader_audit import specimen
from tools.stoneage_guard_break2_source_audit import PINNED, LAYOUTS
from tools.stoneage_enemy_loader_audit import pp_file
from tools.stoneage_enemy_creation_audit import definition
import hashlib
import json
import re

BODY=r"""
#include <execinfo.h>
#include <signal.h>
#include <unistd.h>
static void fataltrace(int sig){void *pc[32];int n=backtrace(pc,32);dprintf(2,"ABORT_TRACE|signal=%d|frames=%d\n",sig,n);backtrace_symbols_fd(pc,n,2);_Exit(130+sig);}
static void demand(int truth,const char *name){
 if(!truth){dprintf(2,"REAL_HEADER_FAIL|%s\n",name);abort();}
}
int main(int argc,char **argv){
 signal(SIGABRT,fataltrace);signal(SIGSEGV,fataltrace);
 write(2,"TRACE|MAIN_ENTER\n",sizeof("TRACE|MAIN_ENTER\n")-1);
 demand(argc==3&&sizeof(void*)==8&&sizeof(int)==4,"host");
SETUP
 write(2,"TRACE|MEM_INIT\n",sizeof("TRACE|MEM_INIT\n")-1);
 demand(memInit(),"memory init");
 demand(ENEMYTEMP_initEnemy(argv[1])&&ENEMY_initEnemy(argv[2]),"master loaders");
 write(2,"TRACE|ARENA\n",sizeof("TRACE|ARENA\n")-1);
 demand(BATTLE_initBattleArray(3),"battle arena");
 MAP_map=controlled_map;MAP_idtblsize=1;
 JUMP
 controlled_map[0].id=1;controlled_map[0].xsiz=controlled_map[0].ysiz=2;
 controlled_map[0].olink=controlled_links;
 initCharCounter[0]=(INITCHARCOUNTER){0,0,2};
 initCharCounter[1]=(INITCHARCOUNTER){2,2,4};
 initCharCounter[2]=(INITCHARCOUNTER){4,4,7};
 write(2,"TRACE|WORLD_OBJECTS\n",sizeof("TRACE|WORLD_OBJECTS\n")-1);
 demand(initObjectArray(2),"world objects");
 for(int i=0;i<2;i++){
  int c,o;demand(CHAR_createCharacter(CHAR_TYPEPLAYER,1,1,1,0,&c,&o,1)&&c==i&&o==i,"world players");
  slots[i].data[CHAR_VITAL]=10000;
  slots[i].data[CHAR_STR]=10000;
  slots[i].data[CHAR_TOUGH]=10000;
  slots[i].data[CHAR_DEX]=10000;
  slots[i].data[CHAR_HP]=20;
  slots[i].data[CHAR_BECOMEPIG]=-1;
  slots[i].data[CHAR_DEFAULTPET]=-1;
  slots[i].data[CHAR_RIDEPET]=-1;
  slots[i].workint[CHAR_WORKBATTLEMODE]=BATTLE_CHARMODE_NONE;
  slots[i].workint[CHAR_WORKBATTLEINDEX]=-1;
  slots[i].workint[CHAR_WORKPETFOLLOW]=-1;
  slots[i].workint[CHAR_WORKPETFALL]=0;
  slots[i].workint[CHAR_WORKACTION]=-1;
  slots[i].workint[CHAR_WORKPARTYMODE]=CHAR_PARTY_NONE;
  slots[i].workint[CHAR_WORKGETEXP]=777;
  slots[i].workint[CHAR_WORKFD]=7;
  slots[i].workint[CHAR_WORKTICKETTIME]=slots[i].workint[CHAR_WORKTICKETTIMESTART]=0;
  for(int j=0;j<CHAR_PARTYMAX;j++)slots[i].workint[CHAR_WORKPARTYINDEX1+j]=-1;
  for(int j=0;j<CHAR_MAXPETHAVE;j++)slots[i].unionTable.indexOfPet[j]=-1;
  memset(slots[i].haveSkill,0,sizeof(slots[i].haveSkill));
 }
 SPECIAL
 demand(CHAR_complianceParameter(0),"leader compliance");
 demand(CHAR_complianceParameter(1),"member compliance");
 slots[0].workint[CHAR_WORKPARTYINDEX1+1]=1;
 slots[0].workint[CHAR_WORKPARTYMODE]=CHAR_PARTY_LEADER;
 slots[1].workint[CHAR_WORKPARTYMODE]=CHAR_PARTY_CLIENT;
 Char pet;
 memset(&pet,0,sizeof pet);
 pet.data[CHAR_WHICHTYPE]=CHAR_TYPEPET;
 pet.data[CHAR_HP]=20;
 pet.data[CHAR_VITAL]=10000;
 pet.data[CHAR_STR]=10000;
 pet.data[CHAR_TOUGH]=10000;
 pet.data[CHAR_DEX]=10000;
 pet.workint[CHAR_WORKPLAYERINDEX]=0;
 pet.workint[CHAR_WORKBATTLEMODE]=BATTLE_CHARMODE_NONE;
 pet.workint[CHAR_WORKBATTLEINDEX]=-1;
 pet.workint[CHAR_WORKGETEXP]=777;
 for(int i=0;i<CHAR_MAXPETHAVE;i++)pet.unionTable.indexOfPet[i]=-1;
 write(2,"TRACE|PET_ALLOC\n",sizeof("TRACE|PET_ALLOC\n")-1);
 int petIndex=CHAR_initCharOneArray(&pet);
 demand(petIndex==2,"real pet allocator index");
 slots[0].unionTable.indexOfPet[0]=petIndex;
 slots[0].data[CHAR_DEFAULTPET]=0;
 demand(CHAR_getCharPet(0,0)==2,"original owner pet accessor");
 demand(CHAR_getInt(0,CHAR_DEFAULTPET)==0,"original selected pet accessor");
 demand(CHAR_getWorkInt(2,CHAR_WORKPLAYERINDEX)==0,"pet owner");
 demand(CHAR_getInt(2,CHAR_HP)==20,"pet HP");
 int array,mode;
 while(scanf("%d%d",&array,&mode)==2){
  slots[0].workint[CHAR_WORKBATTLEMODE]=BATTLE_CHARMODE_NONE;
  slots[1].workint[CHAR_WORKBATTLEMODE]=BATTLE_CHARMODE_NONE;
  slots[2].workint[CHAR_WORKBATTLEMODE]=BATTLE_CHARMODE_NONE;
  slots[0].workint[CHAR_WORKBATTLEINDEX]=-1;
  slots[1].workint[CHAR_WORKBATTLEINDEX]=-1;
  slots[2].workint[CHAR_WORKBATTLEINDEX]=-1;
  slots[0].workint[CHAR_WORKGETEXP]=777;
  slots[1].workint[CHAR_WORKGETEXP]=777;
  slots[2].workint[CHAR_WORKGETEXP]=777;
  born=0;rng_mode=mode;clock_count=netwatch_count=0;
  encounter_count=field_count=fd_count=0;
  ca_count=cd_count=recv_count=en_count=effect_count=0;
  monitor_count=status_count=checkfd_count=skill_count=nc_count=xyd_count=0;
  for(int k=0;k<3;k++)encounter_table[k]=array;
  encounter_table[1]=-1;
  battle_at=BATTLE_searchCnt%3;
  write(2,"TRACE|CREATE\n",sizeof("TRACE|CREATE\n")-1);
 int result=BATTLE_CreateVsEnemy(0,0,-1);
 fprintf(stderr,"TRACE|CREATE_RETURN|%d\\n",result);
  if(result)dprintf(2,"CREATE_RETURN|%d\n",result);
  demand(result==0,"real battle create");
  BATTLE *battle=&BattleArray[battle_at];
  demand(battle->Side[0].Entry[0].ENTRY_FIELD==0,"leader front entry");
  demand(battle->Side[0].Entry[1].ENTRY_FIELD==1,"member front entry");
  demand(battle->Side[0].Entry[5].ENTRY_FIELD==2,"selected pet back entry");
  demand(battle->Side[0].Entry[5].bid==5,"selected pet bid");
  demand(battle->Side[1].Entry[5].ENTRY_FIELD>=4,"actual enemy entry");
  demand(slots[0].workint[CHAR_WORKBATTLEINDEX]==battle_at,"leader index");
  demand(slots[1].workint[CHAR_WORKBATTLEINDEX]==battle_at,"member index");
  demand(slots[2].workint[CHAR_WORKBATTLEINDEX]==battle_at,"pet index");
  demand(slots[0].workint[CHAR_WORKGETEXP]==0,"leader exp");
  demand(slots[1].workint[CHAR_WORKGETEXP]==0,"member exp");
  demand(slots[2].workint[CHAR_WORKGETEXP]==0,"pet exp");
  demand(slots[0].data[CHAR_DEFAULTPET]==0&&slots[0].unionTable.indexOfPet[0]==2,"pet selection retained");
  demand(searchObjectFromCharaIndex(0)==0&&searchObjectFromCharaIndex(1)==1,"world actor ownership");
  printf("REAL_HEADER_ENTRY|array=%d|mode=%d|battle=%d|leader=0|member=1|pet=2|pet_bid=5|GETEXP=0\n",array,mode,battle_at);
  /* Exit is intentionally not asserted by this first admission gate.
     The accepted solo teardown is not equivalent to populated pet Exit. */
  break;
 }
 endObjectOne(0);endObjectOne(1);memEnd();
 return 0;
}
"""
def patch_source(src,profile):
    # Original network/skill/status output is consumed by explicit test
    # collectors; a second player must be allowed, not rewritten into leader0.
    var="char_index" if profile=="bismarck" else "charaindex"
    for counter in ("ca_count","cd_count","status_count","skill_count"):
        expected=f"if({var}!=0)abort();{counter}++;"
        replacement=f"if({var}!=0&&{var}!=1)abort();{counter}++;"
        if expected not in src:
            raise ValueError("collector anchor drift "+counter)
        src=src.replace(expected,replacement,1)
    fd='int getfdFromCharaIndex(int actor){if(actor!=0)abort();fd_count++;return -1;}'
    if src.count(fd)!=1:raise ValueError('original solo fd collector drift')
    src=src.replace(fd,fd.replace('actor!=0','actor!=0&&actor!=1'))
    return src

def native(profile,source):
    body=solo_native(profile,source)
    ix=body.index("int main(int argc,char **argv){")
    prefix=body[:ix]
    setup="if(!configmem(64,262144))return 11;" if profile=="gavin" else "sUnitSize=64;sUnitNumTotal=262144;"
    jump="static int controlled_jump[2]={-1,0};MAP_idjumptbl=controlled_jump;" if profile=="gavin" else "MAP_idjumptbl[0]=-1;MAP_idjumptbl[1]=0;"
    special="for(int q=0;q<2;q++){slots[q].workint[CHAR_WORKSTREETVENDOR]=-1;slots[q].workint[CHAR_WORKANGELMODE]=0;slots[q].data[PROFESSION_CLASS]=PROFESSION_CLASS_NONE;}" if profile=="gavin" else "for(int q=0;q<2;q++){slots[q].workint[CHAR_WORKNOCAST]=777;slots[q].workint[CHAR_WORK_SHOWBATTLETIME]=0;}"
    body=BODY.replace("SETUP",setup).replace("JUMP",jump).replace("SPECIAL",special)
    return prefix+body.replace("ENTRY_FIELD","char_index" if profile=="bismarck" else "charaindex")

def main():
    parser=argparse.ArgumentParser()
    for profile in PINNED:parser.add_argument("--"+profile+"-dir",type=Path,required=True)
    args=parser.parse_args();roots={k:getattr(args,k+"_dir") for k in PINNED}
    for k,p in roots.items():
        if subprocess.check_output(["git","-C",str(p),"rev-parse","HEAD"],text=True).strip()!=PINNED[k]:
            raise ValueError("pin drift "+k)
        if subprocess.check_output(["git","-C",str(p),"status","--porcelain"],text=True).strip():
            raise ValueError("dirty source "+k)
    paths,receipt=specimen(roots["gavin"])
    pins=json.loads(PIN_PATH.read_text())
    if receipt!=pins["preserved_specimen"]:raise ValueError("master specimen drift")
    # Admission only: one preserved original record with fixed per-birth RNG,
    # no claim of exhaustive encounter/party/pet coverage.
    for profile in ("gavin","bismarck"):
        source,identity,*_=solo_domain(profile,roots[profile])
        if pinned_identity(identity)!=pins["profiles"][profile]["identity"]:
            raise ValueError("accepted solo source changed")
        source=patch_source(source,profile)
        # Pet placement requires the ACTUAL original BATTLE_Index2No body;
        # the accepted solo composition never reached this function.
        extra=definition(pp_file(profile,roots[profile],LAYOUTS[profile]/'battle/battle.c'),'BATTLE_Index2No')
        source+='\n'+extra+'\n'
        sample=json.loads((Path(__file__).resolve().parents[1]/"research/recovered/STONEAGE-PLAYER-BATTLE-VALIDATION-R1.json").read_text())
        # Eligible record selection is selected by same accepted loader oracle.
        from tools.stoneage_enemy_loader_audit import loaded_oracle,eligible
        loader=identity["accepted_pool_identity"]["accepted_entry_identity"]["accepted_ownership_identity"]["accepted_loader_identity"]
        temps,enemies=loaded_oracle(profile,loader,*[p.read_bytes() for p in paths],32,32)
        chosen=eligible(loader,temps,enemies,identity["accepted_pool_identity"]["accepted_entry_identity"]["accepted_ownership_identity"]["accepted_loader_identity"].get("ride",[])) if False else None
        # Prefer the already accepted runner's selected-cases API; read its
        # preserved ride candidate state from the solo-domain sixth return.
        _,_,_,_,_,ride=solo_domain(profile,roots[profile])
        chosen=eligible(loader,temps,enemies,ride)[0]
        csource=native(profile,source)
        with tempfile.TemporaryDirectory(prefix="stoneage-realheader-party-pet-") as d:
            out=[]
            for opt in ("-O0","-O2"):
                exe=Path(d)/("probe"+opt)
                compile_probe(profile,roots[profile],csource,exe,opt,[n for n in pins["profiles"][profile]["unreachable_traps"] if n!="BATTLE_Index2No"])
                run=subprocess.run([str(exe),*map(str,paths)],input=f"{chosen} 0\n",capture_output=True,text=True)
                if run.returncode or any(not line.startswith("TRACE|") for line in run.stderr.splitlines() if line.strip()):
                    offsets=re.findall(r"probe-(?:O0|O2)\(\+(0x[0-9a-f]+)\)",run.stderr)
                    symbols=subprocess.run(["addr2line","-f","-C","-e",str(exe),*offsets],capture_output=True,text=True).stdout if offsets else "NO_OFFSETS"
                    raise ValueError("real-header "+profile+" "+opt+" "+run.stderr[-5000:]+" code="+str(run.returncode)+" symbols="+symbols+" stdout "+run.stdout[-2000:])
                if "REAL_HEADER_ENTRY|" not in run.stdout:raise ValueError("no real admission")
                out.append(run.stdout)
            if out[0]!=out[1]:raise ValueError("real-header optimization disagreement")
            print("PROFILE|"+profile+"|input_original_bodies_and_headers=PINNED|original_player_pet_slots=0,1,2|optimizations=O0,O2|sha256="+hashlib.sha256(out[0].encode()).hexdigest())
            print(out[0].strip())
    print("RESOLUTION|REAL_HEADER_PARTY_PET_CREATE_ENTRY_ONLY_EXIT_PROFIT_OPEN_NO_HISTORICAL_PROMOTION")
if __name__=="__main__":main()
