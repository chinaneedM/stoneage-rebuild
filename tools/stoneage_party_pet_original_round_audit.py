"""Complete original real-header Command/Battling control round, all guard.
Preserve original gameplay helpers. Only outbound presentation is collected.
"""
from __future__ import annotations
import argparse,hashlib,json,re,subprocess,tempfile
from pathlib import Path
from tools.stoneage_party_pet_original_ai_audit import ai_native
from tools.stoneage_party_pet_command_wait_audit import (
 EXIT_ANCHOR,patch_source,solo_domain,pinned_identity,PIN_PATH,compile_probe,
 specimen,loaded_oracle,eligible,pp_file,PINNED,LAYOUTS,definition,
)
ROUND_NAMES=("BATTLE_Battling","EntrySort","EsCmp","Replacement_Entry","ComboCheck","ComboCheck2",
 "BATTLE_DexCalc","BATTLE_StatusSeq","BATTLE_MagicStatusSeq","BATTLE_GetWepon","BATTLE_GetAttackCount",
 "BATTLE_PetLoyalCheck","BATTLE_TargetListSet","BATTLE_CountAlive","BATTLE_No2Index","BATTLE_TargetCheck",
 "BATTLE_getRidePet","BATTLE_IsThrowWepon","BATTLE_NoAction","BATTLE_Guard","BATTLE_AddProfit","BATTLE_AddExpItem","BATTLE_getBattleDieIndex","BATTLE_OnlyRescue")

def round_originals(profile,battle,event):
    names=ROUND_NAMES+(('BATTLE_ProfessionStatusSeq',) if profile=='gavin' else ())
    bodies={}
    for n in names:
        try:bodies[n]=definition(battle,n)
        except ValueError:bodies[n]=definition(event,n)
    return bodies

ROUND_OBSERVATIONS=r"""
  Char round_baseline[7];memcpy(round_baseline,slots,sizeof round_baseline);
  BATTLE round_arena=*battle;int round_rng=rng_count,round_rng_mode=rng_mode;
  int round_settings=act_setting_packets,round_sends_before=round_sends;
  int live=0;
  for(int actor=0;actor<7;actor++){
    if(!slots[actor].use||CHAR_getWorkInt(actor,CHAR_WORKBATTLEINDEX)!=battle_at)continue;
    live++;
    slots[actor].workint[CHAR_WORKBATTLECOM1]=BATTLE_COM_GUARD;
    slots[actor].workint[CHAR_WORKBATTLEMODE]=BATTLE_CHARMODE_C_OK;
    slots[actor].workint[CHAR_WORKSEQUENCEPOWER]=actor*100;
    if(actor==2)slots[actor].data[CHAR_MODAI]=100;
    (void)CHAR_complianceParameter(actor);
    if(actor==2)slots[actor].workint[CHAR_WORKFIXAI]=100;
    if(actor>=4)slots[actor].workint[CHAR_WORKTACTICS]=0;
  }
  Char prepared_round[7];memcpy(prepared_round,slots,sizeof prepared_round);
  demand(live==4,"original single enemy populated guard control");
  rng_mode=0;
  Char expected_round[7];memcpy(expected_round,prepared_round,sizeof expected_round);
  for(int actor=0;actor<7;actor++)if(slots[actor].use&&CHAR_getWorkInt(actor,CHAR_WORKBATTLEINDEX)==battle_at){
    expected_round[actor].workint[CHAR_WORKBATTLEMODE]=BATTLE_CHARMODE_C_WAIT;
    expected_round[actor].workint[CHAR_WORKBATTLECOM1]=BATTLE_COM_NONE;
  }
  demand(round_baseline[2].workint[CHAR_WORKFIXAI]==0,"accepted fixture pet compliance AI zero");
  expected_round[2].workint[CHAR_WORKFIXAI]=0;
  BATTLE expected_round_arena=*battle;expected_round_arena.turn=1;
  expected_round_arena.PartTime=0;
  expected_round_arena.Side[0].flg&=~BSIDE_FLG_SURPRISE;
  expected_round_arena.Side[1].flg&=~BSIDE_FLG_SURPRISE;
  demand(BATTLE_Loop()==1,"all ready actual original Command/Battling dispatch");
  printf("ROUND_OBS|mode=%d|turn=%d|battle_mode=%d|sends=%d|settings=%d|text=%s\n",mode,battle->turn,battle->mode,round_sends-round_sends_before,act_setting_packets-round_settings,szAllBattleString);fflush(stdout);
  demand(battle->turn==1&&battle->mode==BATTLE_MODE_BATTLE,"complete nonterminal guard round turn1");
  demand(round_sends-round_sends_before==live,"original battle output sent to four participants");
  for(int actor=0;actor<7;actor++){
    demand(slots[actor].data[CHAR_HP]==prepared_round[actor].data[CHAR_HP],"all guard no damage");
    if(!slots[actor].use||CHAR_getWorkInt(actor,CHAR_WORKBATTLEINDEX)!=battle_at)continue;
    demand(CHAR_getWorkInt(actor,CHAR_WORKBATTLEMODE)==BATTLE_CHARMODE_C_WAIT,"original next round C_WAIT");
  }
  if(memcmp(expected_round,slots,sizeof expected_round)){
    for(int actor=0;actor<7;actor++)for(int w=0;w<CHAR_WORKDATAINTNUM;w++)if(expected_round[actor].workint[w]!=slots[actor].workint[w])printf("ROUND_CHAR_DELTA|actor=%d|work=%d|expected=%d|actual=%d\n",actor,w,expected_round[actor].workint[w],slots[actor].workint[w]);fflush(stdout);
  }
  if(memcmp(&expected_round_arena,battle,sizeof(BATTLE))){
    unsigned char *a=(unsigned char*)&expected_round_arena,*b=(unsigned char*)battle;
    for(int q=0;q<sizeof(BATTLE);q++)if(a[q]!=b[q])printf("ROUND_ARENA_DELTA|byte=%d|expected=%d|actual=%d\n",q,a[q],b[q]);fflush(stdout);
  }
  demand(!memcmp(expected_round,slots,sizeof expected_round),"complete all seven guard-round actor snapshots");
  demand(!memcmp(&expected_round_arena,battle,sizeof(BATTLE)),"complete exact guard-round arena delta");
  demand(BATTLE_CommandWait(battle_at,0)==FALSE,"next original input waits");
  printf("\nREAL_HEADER_GUARD_ROUND|mode=%d|battle=%d|turn=1|participants=4|guard_round=1|next_wait=1|packet_sends=4|hp_unchanged=1|round_executed=1|damage_executed=0\n",mode,battle_at);
  memcpy(slots,round_baseline,sizeof round_baseline);*battle=round_arena;rng_count=round_rng;rng_mode=round_rng_mode;
"""
OUTPUT=r"""
static int round_sends,round_talk;
BOOL BATTLE_CommandSend(int actor,char *s){if(!CHAR_CHECKINDEX(actor)||!s||!s[0])abort();round_sends++;return TRUE;}
void BATTLE_talkToCli(int actor,char *s,int color){if(!CHAR_CHECKINDEX(actor)||!s)abort();(void)color;round_talk++;}
"""

def round_native(profile,source,battle,event,root):
    native,has_lua=ai_native(profile,source,battle,event,root)
    originals=round_originals(profile,battle,event)
    char=pp_file(profile,root,LAYOUTS[profile]/'char/char_base.c')
    originals['CHAR_CanCureFlg']=definition(char,'CHAR_CanCureFlg')
    if profile=='bismarck':
        workspace=pp_file(profile,root,LAYOUTS[profile].parent/'common/workspace.c')
        originals['strncatsafe']=definition(workspace,'strncatsafe')
    # Exact original local scheduler type and function-pointer typedef.
    t=re.search(r'typedef struct\s*\{[^{}]*\}\s*BATTLE_CHARLIST\s*;',battle)
    f=re.search(r'typedef int \(\*FUNC\)\([^;]*;',battle)
    if not t or not f:raise ValueError('original scheduler declarations missing')
    extra='#include "item.h"\n#include "battle_magic.h"\n'+t[0]+f[0]+'\n'
    # Original declarations, preserving sizes and types.
    for n in ('szBattleString','pszBattleTop','szBadStatusString','gWeponType','gDamageDiv','gItemCrushRate'):
        m=re.search(r'(?m)^(?:char|float|int)\s+[^;{}]*\b'+n+r'\b[^;{}]*;',battle)
        if not m:raise ValueError('original global declaration missing '+n)
        extra+=m[0]+'\n'
    for n in ('gBattleDamageModyfy','gBattleDuckModyfy','gBattleStausChange','gBattleStausTurn','gDuckPer','gCriper','gBattleBadStatusTbl'):
        m=re.search(r'(?m)^(?:float|int)\s+[^;{}]*\b'+n+r'\b[^;{}]*;',event)
        if not m:raise ValueError('original event global missing '+n)
        extra+=m[0]+'\n'
    for n in ('BoomerangVsTbl','TargetIndex'):
        m=re.search(r'(?m)^int\s+'+n+r'\s*\[[^;]*?;',battle)
        if m:extra+=m[0]+'\n'
    m=re.search(r'(?m)^int\s+magic\s*,[^;]*;',battle)
    if m:extra+=m[0]+'\n'
    pet_enum=re.search(r'enum\s*\{[^{}]*PETAI_MODE_NORMAL[^{}]*\}\s*;',battle)
    if not pet_enum:raise ValueError('original pet loyalty enum missing')
    extra+=pet_enum[0]+'\n'
    bow=re.search(r'(?m)^(?:static\s+)?int\s+aBowW\s*\[[^;]*?\};',battle)
    if not bow:raise ValueError('original bow table missing')
    extra+=bow[0]+'\n'
    # Private original helper signatures absent from public headers.
    for n in ('BATTLE_TargetAdjust','BATTLE_changeRideImage','CHECK_ITEM_RELIFE','Compute_Down','WorkIceCrackPlay','Compute_Down_SARS','BATTLE_PetRandomSkill','BATTLE_AddDuelPoint','BATTLE_ItemDelCheck','Pet_Check_Die','BATTLE_UltimateExtra','BATTLE_NormalDeadExtra'):
        if not re.search(r'\b'+n+r'\s*\(', '\n'.join(originals.values())):continue
        for file in (battle,event):
            try:body=definition(file,n)
            except ValueError:continue
            extra+=body[:body.index('{')].strip()+';\n';break
        else:
            decl=re.search(r'(?m)^[^;{}\n]*\b'+n+r'\s*\([^;{}]*\)\s*;',battle+'\n'+event)
            if not decl:raise ValueError('missing original private helper signature '+n)
            extra+=decl[0]+'\n'
    for n,b in originals.items():
        try:old=definition(native,n)
        except ValueError:pass
        else:native=native.replace(old,'',1)
        extra+=b[:b.index('{')].strip()+';\n'
    extra+='\n'.join(originals.values())+'\n'
    # Output-only adapters do not approximate any gameplay helper.
    for n in ('BATTLE_CommandSend','_BATTLE_CommandSend','BATTLE_talkToCli'):
        try:old=definition(native,n)
        except ValueError:pass
        else:native=native.replace(old,'',1)
    anchor='int main(int argc,char **argv){'
    if native.count(anchor)!=1 or native.count(EXIT_ANCHOR)!=1:raise ValueError('round observation anchor drift')
    native=native.replace('int BATTLE_ai_all(int battleindex,int side,int turn);','int BATTLE_CountAlive(int,int);\nint BATTLE_ai_all(int battleindex,int side,int turn);',1)
    output=OUTPUT
    if profile=='bismarck':
        output=output.replace('BOOL BATTLE_CommandSend(int actor,char *s){',
                              'BOOL _BATTLE_CommandSend(int actor,char *s,char *file,int line){(void)file;(void)line;')
    native=native.replace(anchor,extra+output+anchor,1)
    return native.replace(EXIT_ANCHOR,ROUND_OBSERVATIONS+EXIT_ANCHOR,1),has_lua

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
        native,has_lua=round_native(profile,source,battle,event,roots[profile])
        traps=None
        runs=[]
        with tempfile.TemporaryDirectory(prefix="stoneage-original-guard-round-") as tmp:
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
                    raise ValueError("native original guard round "+profile+" "+opt+
                                     " code="+str(execute.returncode)+" stderr="+execute.stderr[-4400:]+
                                     " symbols="+symbols+" stdout="+execute.stdout[-1500:])
                waits=[x for x in execute.stdout.splitlines() if x.startswith("REAL_HEADER_GUARD_ROUND|")]
                if len(waits)!=4 or execute.stdout.count("REAL_HEADER_EXIT|")!=4:
                    raise ValueError("missing four real guard-round/Exit cycles")
                for mode,row in enumerate(waits):
                    if f"|mode={mode}|battle={mode%3}|turn=1|" not in row:
                        raise ValueError("battle cursor/turn drift "+row)
                runs.append(execute.stdout)
        if runs[0]!=runs[1]:
            raise ValueError("original guard-round trace O0/O2 divergence "+profile)
        print(f"PROFILE|{profile}|guard_rounds_per_optimization=4|encounters_per_optimization=4|optimizations=O0,O2|sha256={hashlib.sha256(runs[0].encode()).hexdigest()}",flush=True)
        originals=round_originals(profile,battle,event)
        char=pp_file(profile,roots[profile],LAYOUTS[profile]/'char/char_base.c')
        originals['CHAR_CanCureFlg']=definition(char,'CHAR_CanCureFlg')
        if profile=='bismarck':
            workspace=pp_file(profile,roots[profile],LAYOUTS[profile].parent/'common/workspace.c')
            originals['strncatsafe']=definition(workspace,'strncatsafe')
        battle_path=roots[profile]/LAYOUTS[profile]/"battle/battle.c"
        print(f"PROVENANCE|{profile}|commit={PINNED[profile]}|battle_file_sha256={hashlib.sha256(battle_path.read_bytes()).hexdigest()}",flush=True)
        for name,body in originals.items():
            print(f"ORIGINAL_FUNCTION|{profile}|{name}|preprocessed_body_sha256={hashlib.sha256(body.encode()).hexdigest()}",flush=True)
        for row in runs[0].splitlines():
            if row.startswith("REAL_HEADER_GUARD_ROUND|"):print("ACTUAL|"+profile+"|"+row,flush=True)
    print("BOUNDARY|full_original_Battling;controlled_all_guard;no_damage_or_terminal_Finish",flush=True)
    print("OPEN|ordinary_attack_damage_terminal_Finish_profit_network_Lua",flush=True)
    print("RESOLUTION|ORIGINAL_REAL_HEADER_PARTY_PET_GUARD_ROUND_BOUNDED_PASS",flush=True)

if __name__=="__main__":
    main()
