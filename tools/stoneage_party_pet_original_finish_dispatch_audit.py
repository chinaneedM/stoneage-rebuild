"""Bounded original second Loop -> BATTLE_Finish dispatch candidate.

Preserves preceding full original lethal Loop, original FinishSet and all
source-profile-specific win conditions. No gameplay stubs or fabricated rewards.
"""
from __future__ import annotations
import re
import hashlib
from tools.stoneage_party_pet_terminal_path_preflight import PREVIOUS_FINGERPRINTS
from tools.stoneage_party_pet_original_exp_audit import original_exp_parts
from tools.stoneage_party_pet_full_exit_audit import EXPECTED_INSERT
from tools import stoneage_party_pet_original_lethal_loop_audit as lethal
from tools import stoneage_party_pet_original_attack_audit as attack

TRANSPORT_COLLECTORS=r"""
static int finish_status_count,finish_rs_count;
static int finish_rs_fd[4];static char finish_rs_text[4][1024];
BOOL _CHAR_sendStatusString(int actor,char *category,char *file,int line){
 if(actor!=0||strcmp(category,"K0")||!file||line<=0){fprintf(stderr,"TRACE|STATUS_BAD|actor=%d|category=%s|line=%d\n",actor,category,line);abort();}
 finish_status_count++;return TRUE;
}
void lssproto_RS_send(int fd,char *data){
 if(!data||finish_rs_count>=4||strlen(data)>=sizeof finish_rs_text[0]){fprintf(stderr,"TRACE|RS_BAD|fd=%d|count=%d\n",fd,finish_rs_count);abort();}
 finish_rs_fd[finish_rs_count]=fd;
 strcpy(finish_rs_text[finish_rs_count++],data);
}
"""

FINISH_OBSERVATION = r"""
  int final_arena=BattleArray[battle_at].use;
  int final_total=Total_BattleNum;
  int final_mode=BattleArray[battle_at].mode;
  int final_winner=BattleArray[battle_at].winside;
  demand(final_arena&&final_mode==BATTLE_MODE_FINISH,"original lethal finish state before next Loop");
  demand(final_winner==EXPECTED_WIN_SIDE,"original pre-Finish winning side");
  for(int actor=0;actor<3;actor++){
    slots[actor].data[CHAR_LV]=100;slots[actor].data[CHAR_EXP]=0;
    BATTLE_BadStatusAllClr(actor);CHAR_complianceParameter(actor);
  }
  demand(slots[0].workint[CHAR_WORKGETEXP]==1&&slots[1].workint[CHAR_WORKGETEXP]==0&&slots[2].workint[CHAR_WORKGETEXP]==0,"raw lethal reward recipient oracle");
  Char expected_finish[7];memcpy(expected_finish,slots,sizeof expected_finish);
  for(int actor=0;actor<2;actor++){
    expected_finish[actor].data[CHAR_EXP]=actor?EXPECTED_MEMBER_EXP:EXPECTED_LEADER_EXP;
    expected_finish[actor].workint[CHAR_WORKGETEXP]=actor?EXPECTED_MEMBER_EXP:EXPECTED_LEADER_EXP;
    expected_finish[actor].workint[CHAR_WORKBATTLEMODE]=BATTLE_CHARMODE_FINAL;
    expected_finish[actor].workint[CHAR_WORKBATTLEINDEX]=-1;
    EXPECTED_PLAYER_PROFILE
  }
  expected_finish[2].workint[CHAR_WORKBATTLEMODE]=BATTLE_CHARMODE_NONE;
  expected_finish[2].workint[CHAR_WORKBATTLEINDEX]=-1;
  int final_enemy=battle->Side[1].Entry[5].ENTRY_FIELD;
  expected_finish[final_enemy].use=0;
  expected_finish[final_enemy].workint[CHAR_WORKBATTLEMODE]=BATTLE_CHARMODE_FINAL;
  expected_finish[final_enemy].workint[CHAR_WORKBATTLEINDEX]=-1;
  for(int q=0;q<3;q++){
    int actor=q==2?final_enemy:q;
    if(expected_finish[actor].data[CHAR_BASEIMAGENUMBER]==101749||expected_finish[actor].workint[CHAR_WORKFOXROUND]!=-1){
      expected_finish[actor].data[CHAR_BASEIMAGENUMBER]=expected_finish[actor].data[CHAR_BASEBASEIMAGENUMBER];
      expected_finish[actor].workint[CHAR_WORKFOXROUND]=-1;
    }
  }
  BATTLE expected_final_arena=*battle;
  expected_final_arena.use=0;expected_final_arena.mode=BATTLE_MODE_NONE;
  for(int side=0;side<2;side++)for(int i=0;i<BATTLE_ENTRY_MAX;i++){
    expected_final_arena.Side[side].Entry[i].ENTRY_FIELD=-1;
    expected_final_arena.Side[side].Entry[i].bid=-1;
    expected_final_arena.Side[side].Entry[i].escape=0;
    for(int j=0;j<GETITEM_MAX;j++)expected_final_arena.Side[side].Entry[i].getitem[j]=-1;
  }
  finish_status_count=finish_rs_count=0;finish_transport_phase=1;
  int finish_loop_ret=BATTLE_Loop();
  demand(finish_rs_count==2&&finish_status_count==1,"exact reward/status collector call counts");
  demand(finish_rs_fd[0]==7&&finish_rs_fd[1]==7,"explicit descriptor7 transport fixture");
  demand(!strcmp(finish_rs_text[0],EXPECTED_LEADER_PACKET)&&!strcmp(finish_rs_text[1],EXPECTED_MEMBER_PACKET),"original reward text independent base62 oracle");
  for(int r=0;r<finish_rs_count;r++)printf("FINISH_RS_OBS|fd=%d|data=%s\n",finish_rs_fd[r],finish_rs_text[r]);
  printf("ORIGINAL_FINISH_NEXT_LOOP|arena=%d|ret=%d|use=%d|mode=%d|total_before=%d|total_after=%d|winner_before=%d|actor0_mode=%d|actor1_mode=%d\n",
    battle_at,finish_loop_ret,BattleArray[battle_at].use,BattleArray[battle_at].mode,
    final_total,Total_BattleNum,final_winner,
    slots[0].workint[CHAR_WORKBATTLEMODE],slots[1].workint[CHAR_WORKBATTLEMODE]);
  fflush(stdout);
  if(memcmp(expected_finish,slots,sizeof expected_finish)){
    for(int a=0;a<7;a++){
      for(int i=0;i<CHAR_DATAINTNUM;i++)if(expected_finish[a].data[i]!=slots[a].data[i])printf("FINISH_DATA_DIFF|actor=%d|field=%d|expected=%d|actual=%d\n",a,i,expected_finish[a].data[i],slots[a].data[i]);
      for(int i=0;i<CHAR_WORKDATAINTNUM;i++)if(expected_finish[a].workint[i]!=slots[a].workint[i])printf("FINISH_WORK_DIFF|actor=%d|field=%d|expected=%d|actual=%d\n",a,i,expected_finish[a].workint[i],slots[a].workint[i]);
    }fflush(stdout);
  }
  demand(!memcmp(expected_finish,slots,sizeof expected_finish),"whole seven actor terminal oracle");
  demand(!memcmp(&expected_final_arena,battle,sizeof expected_final_arena),"whole arena terminal oracle");
  demand(BattleArray[battle_at].use==0,"original terminal arena released");
  demand(BattleArray[battle_at].mode==BATTLE_MODE_NONE,"original terminal arena mode NONE");
  demand(Total_BattleNum==final_total-1,"original terminal arena counter decremented");
  printf("REAL_HEADER_FINISH_DISPATCH|mode=%d|battle=%d|original_finish_loop=1|released=1\n",mode,battle_at);
  finish_transport_phase=0;
  /* Only test-fixture normalization; no gameplay code is modified. The
     inherited accepted Exit control then performs its own teardown. */

"""

def finish_observations(profile):
    script=lethal.LETHAL_ROUND_OBSERVATIONS
    anchor="memcpy(slots,round_baseline,sizeof round_baseline);*battle=round_arena;rng_count=round_rng;rng_mode=round_rng_mode;"
    if script.count(anchor)!=1:raise ValueError("accepted lethal round restoration anchor drift")
    sentinel="-1" if profile=="bismarck" else "0"
    result=script.replace(anchor,FINISH_OBSERVATION,1).replace("EXPECTED_WIN_SIDE",sentinel)
    result=result.replace('EXPECTED_LEADER_EXP','1000000' if profile=='bismarck' else '1').replace('EXPECTED_MEMBER_EXP','1000000' if profile=='bismarck' else '0')
    result=result.replace('EXPECTED_LEADER_PACKET','"-2|0|4c92,,,,,|||"' if profile=='bismarck' else '"-2|0|1,,,,,|||"').replace('EXPECTED_MEMBER_PACKET','"-2|0|4c92,,,,,|||"' if profile=='bismarck' else '"-2|0|0,,,,,|||"')
    return result.replace('EXPECTED_PLAYER_PROFILE' ,'expected_finish[actor].workint[CHAR_WORKNOCAST]=0;' if profile=='bismarck' else 'expected_finish[actor].workint[CHAR_DOOMTIME]=0;')

def finish_native(profile,source,battle,event,root):
    native,has_lua=lethal.lethal_round_native(profile,source,battle,event,root)
    timer=attack.definition(native,'CheckDefBTime')
    if timer.count('battletime!=2')!=1:raise ValueError('battle duration collector drift')
    native='static int finish_transport_phase;\n'+native.replace(timer,timer.replace('battletime!=2','battletime!=(finish_transport_phase?3:2)'),1)
    if profile=='bismarck':
        watch=attack.definition(native,'NETWATCH_set')
        if watch.count('strcmp(stage,"BATTLE_Command")==0')!=1:raise ValueError('monitor profile drift')
        native=native.replace(watch,watch.replace('strcmp(stage,"BATTLE_Command")==0','strcmp(stage,"BATTLE_Command")==0||strcmp(stage,"BATTLE_Finish")==0'),1)
    exit_control=EXPECTED_INSERT[EXPECTED_INSERT.index('  int exit0'):].replace('ENTRY_FIELD','char_index' if profile=='bismarck' else 'charaindex')
    if native.count(exit_control)!=1:raise ValueError('inherited manual Exit anchor drift')
    native=native.replace(exit_control,r"""
    demand(!BattleArray[battle_at].use&&Battle_getTotalBattleNum()==0,"automatic terminal Delete preserved");
    demand(slots[0].use&&slots[1].use&&slots[2].use,"three living actors retained");
    demand(slots[0].data[CHAR_DEFAULTPET]==0&&slots[0].unionTable.indexOfPet[0]==2,"terminal pet ownership retained");
    printf("REAL_HEADER_EXIT|array=%d|mode=%d|battle=%d|automatic=1|owned=2|battle_deleted=1\n",array,mode,battle_at);
    for(int actor=0;actor<3;actor++){slots[actor].data[CHAR_LV]=0;slots[actor].data[CHAR_EXP]=0;}
""",1)
    previous=lethal.LETHAL_ROUND_OBSERVATIONS.replace(
        "EXPECTED_WIN_SIDE","-1" if profile=="bismarck" else "0",
    ).replace("ENTRY_FIELD","char_index" if profile=="bismarck" else "charaindex")
    if native.count(previous)!=1:
        raise ValueError("accepted original lethal round body drift")
    native=native.replace(previous,finish_observations(profile).replace(
        "ENTRY_FIELD","char_index" if profile=="bismarck" else "charaindex"),1)
    bodies={}
    for n in ("BATTLE_Finish","BATTLE_GetProfit","BATTLE_GetExpGold","BATTLE_GetExp"):
        bodies[n]=attack.definition(battle,n)
    for n in ('BATTLE_Finish','BATTLE_GetProfit'):
        if hashlib.sha256(bodies[n].encode()).hexdigest()!=PREVIOUS_FINGERPRINTS[profile][n]:raise ValueError('accepted original terminal body drift '+n)
    anchor="int main(int argc,char **argv){"
    declarations,exp_parts=original_exp_parts(profile,battle,root)
    bodies.update(exp_parts)
    cfg=attack.pp_file(profile,root,attack.LAYOUTS[profile]/("configfile.c" if profile=="gavin" else "config_file.c"))
    data=attack.pp_file(profile,root,attack.LAYOUTS[profile]/"char/char_data.c")
    bodies['CHAR_LevelUpCheck']=attack.definition(data,'CHAR_LevelUpCheck')
    charbase=attack.pp_file(profile,root,attack.LAYOUTS[profile]/'char/char_base.c')
    bodies['CHAR_HandleExp']=attack.definition(charbase,'CHAR_HandleExp')
    if profile=='gavin':
        bodies['CHAR_GetLevelExp']=attack.definition(data,'CHAR_GetLevelExp')
        for n in ('getBattleDebugMsg','getMaxLevel','getYBLevel','getNeedLevelUpTbls','getChartrans','getPettrans'):
            bodies[n]=attack.definition(cfg,n)
            if cfg[max(0,cfg.index(bodies[n])-9):cfg.index(bodies[n])]=='unsigned ':bodies[n]='unsigned '+bodies[n]
        declarations+='\nint NeedLevelUpTbls[160];int MaxLevel=159;\n'
        setup='config.battleexp=1;config.yblevel=159;for(int i=0;i<160;i++)NeedLevelUpTbls[i]=10000000;'
    else:
        cfgtype=re.search(r'typedef struct tagServerConfig\s*\{[^{}]+\}\s*ServerConfig\s*;',cfg)
        if not cfgtype:raise ValueError('original server config missing')
        declarations+=cfgtype[0]+'\nServerConfig gServerConfig;\n'
        bodies['getBattleDebugMsg']=attack.definition(cfg,'getBattleDebugMsg')
        if cfg[max(0,cfg.index(bodies['getBattleDebugMsg'])-9):cfg.index(bodies['getBattleDebugMsg'])]=='unsigned ':bodies['getBattleDebugMsg']='unsigned '+bodies['getBattleDebugMsg']
        setup=''
    util=attack.pp_file(profile,root,attack.LAYOUTS[profile]/'util.c' if profile=='gavin' else attack.LAYOUTS[profile].parent/'common/workspace.c')
    bodies['cnv10to62']=attack.definition(util,'cnv10to62')
    native=native.replace(anchor,declarations+'\n'+TRANSPORT_COLLECTORS.replace('lssproto_RS_send','GmsvServer_RS_send' if profile=='bismarck' else 'lssproto_RS_send')+'\n'+anchor,1)
    for n,body in bodies.items():
        try:prior=attack.definition(native,n)
        except ValueError:pass
        else:native=native.replace(prior,"",1)
        # Add exact original signature declaration for potentially earlier use.
        native=native.replace(anchor,body[:body.index("{")].strip()+";\n"+anchor,1)
    # Original BATTLE_Loop is defined before our source-body insert at main;
    # preserve the original static linkage by declaring Finish before its use.
    loop=attack.definition(native,"BATTLE_Loop")
    if native.count(loop)!=1:raise ValueError("original Loop body declaration anchor drift")
    signature=bodies["BATTLE_Finish"][:bodies["BATTLE_Finish"].index("{")].strip()+";"
    native=native.replace(loop,signature+"\n"+loop,1)
    for name,body in bodies.items():print(f"FINISH_SOURCE|{profile}|{name}|sha256={hashlib.sha256(body.encode()).hexdigest()}",flush=True)
    print(f"FINISH_DECLARATIONS|{profile}|sha256={hashlib.sha256(declarations.encode()).hexdigest()}",flush=True)
    native=native.replace(anchor,"\n".join(bodies.values())+"\n"+anchor,1)
    native=native.replace(anchor,anchor+setup,1)
    return native,has_lua

def main():
    attack.main(native_builder=finish_native,extra_markers=(
        "REAL_HEADER_LETHAL_LOOP|","LETHAL_LOOP_MODE|","ORIGINAL_FINISH_NEXT_LOOP|",
        "REAL_HEADER_FINISH_DISPATCH|","FINISH_RS_OBS|",
    ))
    print("BOUNDARY|bounded_no_level_up_empty_item_second_Loop_Finish;synthetic_Gavin_thresholds;transport_collectors_not_real_network")
    print("RESOLUTION|ORIGINAL_REAL_HEADER_PARTY_PET_FINISH_DISPATCH_BOUNDED_PASS")

if __name__=="__main__":main()
