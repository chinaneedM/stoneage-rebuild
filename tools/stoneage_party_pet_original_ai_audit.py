"""Full original AI decision functions composed with accepted real-header inputs.
Controlled tactics only; no all-ready Loop, Battling or completed action round.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from tools.stoneage_party_pet_command_input_audit import input_native
from tools.stoneage_party_pet_command_wait_audit import (
 EXIT_ANCHOR,patch_source,solo_domain,pinned_identity,PIN_PATH,compile_probe,
 specimen,loaded_oracle,eligible,pp_file,PINNED,LAYOUTS,definition,
)
AI_NAMES=("BATTLE_ai_all","BATTLE_ai_normal","GetSubdueAttribute")

def ai_originals(profile,root,battle):
    ai=pp_file(profile,root,LAYOUTS[profile]/"battle/battle_ai.c")
    result={n:definition(ai,n) for n in AI_NAMES}
    result["BATTLE_CanMoveCheck"]=definition(battle,"BATTLE_CanMoveCheck")
    return result

AI_OBSERVATIONS=r"""
  Char ai_baseline[7];memcpy(ai_baseline,slots,sizeof ai_baseline);
  BATTLE ai_arena=*battle;
  int ai_packets=act_setting_packets,ai_recv=recv_count,ai_rng_base=rng_count,ai_rng_mode=rng_mode;
  demand(BATTLE_ai_all(-1,1,0)==BATTLE_ERR_BATTLEINDEX,"AI invalid battle rejected");
  demand(BATTLE_ai_all(battle_at,2,0)==BATTLE_ERR_PARAM,"AI invalid side rejected");
  demand(BATTLE_ai_all(battle_at,0,0)==FALSE,"player side never receives enemy AI");
  demand(!memcmp(ai_baseline,slots,sizeof ai_baseline)&&!memcmp(&ai_arena,battle,sizeof(BATTLE))&&rng_count==ai_rng_base,"AI guards complete actor/arena/RNG unchanged");
  int enemy_count=0;
  for(int i=0;i<BATTLE_ENTRY_MAX;i++)if(CHAR_CHECKINDEX(battle->Side[1].Entry[i].ENTRY_FIELD))enemy_count++;
  demand(enemy_count>0,"live original spawned enemies for AI");
  for(int scenario=0;scenario<8;scenario++){
    memcpy(slots,ai_baseline,sizeof ai_baseline);*battle=ai_arena;
    for(int i=0;i<BATTLE_ENTRY_MAX;i++){
      int actor=battle->Side[1].Entry[i].ENTRY_FIELD;if(!CHAR_CHECKINDEX(actor))continue;
      demand(actor>=4&&actor<7,"AI original enemy slot");
      slots[actor].workint[CHAR_WORKTACTICS]=scenario==5?0:1;
      slots[actor].workint[CHAR_WORKBATTLECOM1]=scenario==4?BATTLE_COM_S_CHARGE:BATTLE_COM_NONE;
      slots[actor].workint[CHAR_WORKBATTLEMODE]=BATTLE_CHARMODE_C_WAIT;
      demand(CHAR_setWorkChar(actor,CHAR_WORKBATTLE_TACTICSOPTION,scenario==1?"at:1;3;1":"at:1;2;1"),"controlled original workchar preparation");
      demand(CHAR_setWorkChar(actor,CHAR_WORKBATTLE_ACT_CONDITION,""),"exclude NPC warp script");
      if(scenario==2)slots[actor].workint[CHAR_WORKPARALYSIS]=1;
    }
    if(scenario==3)battle->Side[1].flg|=BSIDE_FLG_SURPRISE;
    Char ai_expected[7];memcpy(ai_expected,slots,sizeof ai_expected);BATTLE prepared_ai_arena=*battle;
    if(scenario==6)CHAR_setFlg(0,CHAR_ISDIE,1);
    if(scenario==7)slots[0].workint[CHAR_WORKBATTLEMODE]=BATTLE_CHARMODE_RESCUE;
    /* snapshot fixture changes separately from original AI effects */
    memcpy(ai_expected,slots,sizeof ai_expected);
    int expected_rng=(scenario<3||scenario>=6)?2*enemy_count:0;
    for(int i=0;i<BATTLE_ENTRY_MAX;i++){
      int actor=battle->Side[1].Entry[i].ENTRY_FIELD;if(!CHAR_CHECKINDEX(actor)||scenario==5)continue;
      ai_expected[actor].workint[CHAR_WORKBATTLEMODE]=BATTLE_CHARMODE_C_OK;
      if(scenario==4)continue;
      ai_expected[actor].workint[CHAR_WORKBATTLECOM1]=(scenario==2||scenario==3)?BATTLE_COM_NONE:BATTLE_COM_ATTACK;
      if(scenario!=3)ai_expected[actor].workint[CHAR_WORKBATTLECOM2]=scenario==1?5:scenario>=6?1:0;
    }
    rng_mode=0;rng_count=0;
    demand(BATTLE_ai_all(battle_at,1,0)==TRUE,"full original enemy AI dispatch");
    if(memcmp(ai_expected,slots,sizeof ai_expected)){
      for(int actor=0;actor<7;actor++)for(int w=0;w<CHAR_WORKDATAINTNUM;w++)if(ai_expected[actor].workint[w]!=slots[actor].workint[w])printf("AI_DELTA|scenario=%d|actor=%d|work=%d|expected=%d|actual=%d\n",scenario,actor,w,ai_expected[actor].workint[w],slots[actor].workint[w]);fflush(stdout);
    }
    demand(!memcmp(ai_expected,slots,sizeof ai_expected),"full seven actor exact AI decision delta");
    demand(!memcmp(&prepared_ai_arena,battle,sizeof(BATTLE)),"complete arena unchanged by AI decisions");
    demand(rng_count==expected_rng,"exact controlled AI RNG calls");
    demand(act_setting_packets==ai_packets&&recv_count==ai_recv,"AI emits no input or network acknowledgements");
  }
  memcpy(slots,ai_baseline,sizeof ai_baseline);*battle=ai_arena;rng_mode=ai_rng_mode;rng_count=ai_rng_base;
  demand(battle->turn==0&&CHAR_getCharPet(0,0)==2,"AI decision separated from round and ownership");
  printf("\nREAL_HEADER_AI_DECISION|mode=%d|battle=%d|turn=0|enemies=%d|scenarios=8|player_target=0|pet_target=5|paralysis_none=1|surprise_none=1|charge_retained=1|tactics0_unchanged=1|allied_unchanged=1|arena_unchanged=1|dead_excluded=1|rescue_excluded=1|guards=3|round_executed=0\n",mode,battle_at,enemy_count);
"""

def ai_native(profile,source,battle,event,root):
    native,has_lua=input_native(profile,source,battle,event,root)
    ai=pp_file(profile,root,LAYOUTS[profile]/"battle/battle_ai.c")
    originals=ai_originals(profile,root,battle)
    old=definition(native,"BATTLE_ai_all")
    if 'UNREACHED_ORIGINAL' not in old:
        raise ValueError("accepted fail-closed AI anchor drift")
    start=ai.index('struct B_AI_RESULT {');end=ai.index('int BATTLE_ai_all(',start)
    declarations=ai[start:end]
    enum=re.search(r'typedef enum\s*\{[^{}]*B_AI_ATTACKMODE[^{}]*\}\s*B_AI_MODE\s*;',ai)
    attributes=re.search(r'enum\s*\{[^{}]*AI_ATT_EARTHAT[^{}]*\}\s*;',ai)
    if not enum or not attributes or declarations.count('BATTLE_ai_normal,')!=1:
        raise ValueError("original AI result/table/enum declaration drift")
    base=pp_file(profile,root,LAYOUTS[profile]/"char/char_base.c")
    util=pp_file(profile,root,LAYOUTS[profile]/"npc/npcutil.c")
    helpers=''
    for n in ('CHAR_CHECKCHARWORKDATAINDEX','_CHAR_getWorkChar'):
        try:definition(native,n)
        except ValueError:helpers+=definition(base,n)+'\n'
    helpers+=definition(util,'NPC_Util_GetStrFromStrWithDelim')+'\n'
    extra='#include "npcutil.h"\n'+declarations+enum[0]+'\n'+attributes[0]+'\n'+helpers
    extra+=originals['GetSubdueAttribute']+'\n'+originals['BATTLE_ai_normal']+'\n'
    try:old_move=definition(native,'BATTLE_CanMoveCheck')
    except ValueError:extra+=originals['BATTLE_CanMoveCheck']+'\n'
    else:native=native.replace(old_move,originals['BATTLE_CanMoveCheck'],1)
    native=native.replace(old,extra+originals['BATTLE_ai_all'],1)
    field='char_index' if profile=='bismarck' else 'charaindex'
    if native.count(EXIT_ANCHOR)!=1:raise ValueError('AI observation exit anchor drift')
    return native.replace(EXIT_ANCHOR,AI_OBSERVATIONS.replace('ENTRY_FIELD',field)+EXIT_ANCHOR,1),has_lua

def main():
    parser=argparse.ArgumentParser()
    for p in PINNED:parser.add_argument("--"+p+"-dir",type=Path,required=True)
    args=parser.parse_args()
    roots={p:getattr(args,p+"_dir") for p in PINNED}
    for profile,root in roots.items():
        sha=subprocess.check_output(["git","-C",str(root),"rev-parse","HEAD"],text=True).strip()
        dirty=subprocess.check_output(["git","-C",str(root),"status","--porcelain"],text=True).strip()
        if sha!=PINNED[profile] or dirty:
            raise ValueError("pinned source drift "+profile)
    paths,receipt=specimen(roots["gavin"])
    accepted=json.loads(PIN_PATH.read_text())
    if accepted["preserved_specimen"]!=receipt:raise ValueError("specimen drift")
    for profile in ("gavin","bismarck"):
        source,identity,*rest=solo_domain(profile,roots[profile])
        if pinned_identity(identity)!=accepted["profiles"][profile]["identity"]:
            raise ValueError("accepted original source identity drift "+profile)
        source=patch_source(source,profile)
        if profile=="bismarck":
            previous='if(strncmp(stage,"BATTLE_Finish.",14))abort();netwatch_count++;'
            new='if(strncmp(stage,"BATTLE_Finish.",14)&&!( (strcmp(stage,"BATTLE_Init")==0||strcmp(stage,"BATTLE_Command")==0)&&value>=0&&value<3&&BattleArray[value].use))abort();netwatch_count++;'
            if source.count(previous)!=1:
                raise ValueError("Bismarck monitor collector anchor drift")
            source=source.replace(previous,new,1)
        battle=pp_file(profile,roots[profile],LAYOUTS[profile]/"battle/battle.c")
        event=pp_file(profile,roots[profile],LAYOUTS[profile]/"battle/battle_event.c")
        source+="\n"+definition(battle,"BATTLE_Index2No")+"\n"
        loader=identity["accepted_pool_identity"]["accepted_entry_identity"]["accepted_ownership_identity"]["accepted_loader_identity"]
        templates,enemies=loaded_oracle(profile,loader,*[p.read_bytes() for p in paths],32,32)
        selected=eligible(loader,templates,enemies,rest[-1])[0]
        native,has_lua=ai_native(profile,source,battle,event,roots[profile])
        traps=None
        runs=[]
        with tempfile.TemporaryDirectory(prefix="stoneage-actual-original-ai-") as tmp:
            for opt in ("-O0","-O2"):
                exe=Path(tmp)/("probe"+opt)
                traps=compile_probe(profile,roots[profile],native,exe,opt,None if opt=="-O0" else traps)
                execute=subprocess.run([str(exe),*map(str,paths)],
                                     input="".join(f"{selected} {mode}\n" for mode in range(4)),
                                     capture_output=True,text=True)
                if execute.returncode or any(not l.startswith("TRACE|") for l in execute.stderr.splitlines() if l.strip()):
                    frames=re.findall(r"probe-(?:O0|O2)\(\+(0x[0-9a-f]+)\)",execute.stderr)
                    symbols=subprocess.run(["addr2line","-f","-C","-e",str(exe),*frames],
                                           capture_output=True,text=True).stdout if frames else "NO_FRAMES"
                    raise ValueError("native original AI "+profile+" "+opt+
                                     " code="+str(execute.returncode)+" stderr="+execute.stderr[-4400:]+
                                     " symbols="+symbols+" stdout="+execute.stdout[-1500:])
                waits=[x for x in execute.stdout.splitlines() if x.startswith("REAL_HEADER_AI_DECISION|")]
                if len(waits)!=4 or execute.stdout.count("REAL_HEADER_EXIT|")!=4:
                    raise ValueError("missing four real AI-decision/Exit cycles")
                for mode,row in enumerate(waits):
                    if f"|mode={mode}|battle={mode%3}|turn=0|" not in row:
                        raise ValueError("battle cursor/turn drift "+row)
                runs.append(execute.stdout)
        if runs[0]!=runs[1]:
            raise ValueError("original AI-decision trace O0/O2 divergence "+profile)
        print(f"PROFILE|{profile}|ai_scenarios_per_optimization=32|encounters_per_optimization=4|optimizations=O0,O2|sha256={hashlib.sha256(runs[0].encode()).hexdigest()}",flush=True)
        originals=ai_originals(profile,roots[profile],battle)
        ai_path=roots[profile]/LAYOUTS[profile]/"battle/battle_ai.c"
        print(f"PROVENANCE|{profile}|commit={PINNED[profile]}|ai_file_sha256={hashlib.sha256(ai_path.read_bytes()).hexdigest()}",flush=True)
        for name,body in originals.items():
            print(f"ORIGINAL_FUNCTION|{profile}|{name}|preprocessed_body_sha256={hashlib.sha256(body.encode()).hexdigest()}",flush=True)
        for row in runs[0].splitlines():
            if row.startswith("REAL_HEADER_AI_DECISION|"):print("ACTUAL|"+profile+"|"+row,flush=True)
    print("BOUNDARY|original_ai_all_normal_full_bodies;controlled_attack_scope;Battling_not_executed",flush=True)
    print("OPEN|actual_action_round_completion_BATTLE_Finish_profit_network_Lua",flush=True)
    print("RESOLUTION|ORIGINAL_REAL_HEADER_PARTY_PET_AI_DECISION_BOUNDED_PASS",flush=True)

if __name__=="__main__":
    main()
