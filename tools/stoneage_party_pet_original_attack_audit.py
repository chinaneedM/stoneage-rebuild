"""Original real-header ordinary player attack inside the complete round driver.
Unchanged original gameplay helpers; controlled single live enemy, no equipment.
"""
from __future__ import annotations
import argparse,hashlib,json,re,subprocess,tempfile
from pathlib import Path
from tools.stoneage_party_pet_original_round_audit import (
 round_native,round_originals,ROUND_OBSERVATIONS,
 EXIT_ANCHOR,patch_source,solo_domain,pinned_identity,PIN_PATH,compile_probe,
 specimen,loaded_oracle,eligible,pp_file,PINNED,LAYOUTS,definition,
)
ATTACK_NAMES=("BATTLE_Attack","BATTLE_AttackSeq","BATTLE_DamageCalc",
 "BATTLE_CriticalCheckPlayer","BATTLE_CriticalCheck","BATTLE_CriDamageCalc",
 "BATTLE_DuckCheck","BATTLE_ArrangeCheck","BATTLE_GetDamageReact","BATTLE_DamageSub",
 "BATTLE_DamageWakeUp","BATTLE_getReactFlg","BATTLE_GetAttr","BATTLE_AttrCalc",
 "BATTLE_AttrAdjust","BATTLE_FieldAttAdjust","BATTLE_GuardAdjust","BATTLE_GuardianCheck",
 "BATTLE_ItemCrushSeq","BATTLE_ItemCrushCheck","BATTLE_TargetAdjust","BATTLE_DefaultAttacker",
 "BATTLE_Counter","BATTLE_CounterCheck")

def attack_originals(profile,battle,event,root=None):
    bodies={}
    for n in ATTACK_NAMES:
        if profile=='bismarck' and n=='BATTLE_ArrangeCheck':
            if re.search(r'\bBATTLE_ArrangeCheck\s*\(',event):raise ValueError('Bismarck arrangement profile drift')
            continue
        if profile=='bismarck' and n=='BATTLE_AttrCalc':
            magic=pp_file(profile,root,LAYOUTS[profile]/'battle/battle_magic.c')
            bodies[n]=definition(magic,n)
            continue
        try:bodies[n]=definition(event,n)
        except ValueError:bodies[n]=definition(battle,n)
    return bodies

ATTACK_SETUP=r"""
  int enemy_actor=battle->Side[1].Entry[5].ENTRY_FIELD;
  demand(enemy_actor>=4&&enemy_actor<7&&CHAR_CHECKINDEX(enemy_actor),"original current enemy allocator slot");
  int enemy_no=BATTLE_Index2No(battle_at,enemy_actor);
  demand(enemy_no>=SIDE_OFFSET&&BATTLE_No2Index(battle_at,enemy_no)==enemy_actor,"original actual live enemy target");
  slots[0].workint[CHAR_WORKBATTLECOM1]=BATTLE_COM_ATTACK;
  slots[0].workint[CHAR_WORKBATTLECOM2]=enemy_no;
  slots[0].data[CHAR_VITAL]=10000;slots[0].data[CHAR_STR]=8500;
  slots[0].data[CHAR_TOUGH]=0;slots[0].data[CHAR_DEX]=10000;
  slots[enemy_actor].data[CHAR_VITAL]=10000;slots[enemy_actor].data[CHAR_STR]=0;
  slots[enemy_actor].data[CHAR_TOUGH]=2500;slots[enemy_actor].data[CHAR_DEX]=10000;
  for(int q=0;q<2;q++){
    int actor=q?enemy_actor:0;
    int attrs[]={CHAR_EARTHAT,CHAR_WATERAT,CHAR_FIREAT,CHAR_WINDAT};
    for(int i=0;i<4;i++)slots[actor].data[attrs[i]]=0;
    (void)CHAR_complianceParameter(actor);
  }
  slots[enemy_actor].data[CHAR_HP]=500;
  demand(slots[0].workint[CHAR_WORKATTACKPOWER]==100,"original recomputed player attack100");
  demand(slots[enemy_actor].workint[CHAR_WORKDEFENCEPOWER]==40&&slots[enemy_actor].workint[CHAR_WORKMAXHP]==525,"original recomputed enemy defense40 maxhp525");
"""

def attack_observations():
    # The accepted guard oracle is extended by a fixed independent damage oracle.
    s=ROUND_OBSERVATIONS
    s=s.replace('  Char prepared_round[7];',ATTACK_SETUP+'  Char prepared_round[7];',1)
    s=s.replace('  rng_mode=0;','  rng_mode=2;',1)
    s=s.replace('  BATTLE expected_round_arena=*battle;',
      '  expected_round[enemy_actor].data[CHAR_HP]=427;\n'
      '  expected_round[enemy_actor].data[CHAR_DAMAGECOUNT]++;\n'
      '  expected_round[0].flg[CHAR_ISATTACKED/8]|=CHAR_flgbitmaskpattern[CHAR_ISATTACKED%8];\n'
      '  BATTLE expected_round_arena=*battle;',1)
    s=s.replace('  expected_round_arena.PartTime=0;',
                '  expected_round_arena.PartTime=0;expected_round_arena.flgTime+=150;',1)
    s=s.replace('demand(slots[actor].data[CHAR_HP]==prepared_round[actor].data[CHAR_HP],"all guard no damage");',
                'if(slots[actor].data[CHAR_HP]!=expected_round[actor].data[CHAR_HP]){printf("ATTACK_HP_DELTA|actor=%d|expected=%d|actual=%d\\n",actor,expected_round[actor].data[CHAR_HP],slots[actor].data[CHAR_HP]);fflush(stdout);}\n'
                'demand(slots[actor].data[CHAR_HP]==expected_round[actor].data[CHAR_HP],"exact single enemy physical damage");')
    s=s.replace('REAL_HEADER_GUARD_ROUND|','REAL_HEADER_ATTACK_ROUND|')
    s=s.replace('guard_round=1','attack_round=1').replace('hp_unchanged=1','enemy_damage=73').replace('damage_executed=0','damage_executed=1')
    s=s.replace('all ready actual original Command/Battling dispatch','all ready actual original ordinary attack dispatch')
    s=s.replace('complete nonterminal guard round turn1','complete nonterminal ordinary attack round turn1')
    s=s.replace('guard-round','attack-round').replace('populated guard control','populated attack control')
    s=s.replace('  demand(battle->turn==1',
      '  char attack_packet[128];snprintf(attack_packet,sizeof attack_packet,"BH|a0|r%X|f%X|d49|p0|FF|",enemy_no,BCF_NORMAL|BCF_GUARD);\n'
      '  demand(strstr(szAllBattleString,attack_packet)!=NULL,"original ordinary physical output target damage flags");\n'
      '  demand(battle->turn==1',1)
    return '{\n'+s+'\n}\n'

ATTACK_OBSERVATIONS=attack_observations()

def attack_native(profile,source,battle,event,root):
    native,has_lua=round_native(profile,source,battle,event,root)
    bodies=attack_originals(profile,battle,event,root)
    base=pp_file(profile,root,LAYOUTS[profile]/'char/char_base.c')
    bodies['CHAR_getFunctionPointer']=definition(base,'CHAR_getFunctionPointer')
    extra='#include <math.h>\n'
    for n in ('BATTLE_CounterCheckPlayer','BATTLE_CounterCheckPet'):
        body=definition(event,n)
        extra+=body[:body.index('{')].strip()+';\n'
    for n in ('gKawashiPara','gCriticalPara','gCounterPara'):
        m=re.search(r'(?m)^float\s+'+n+r'\b[^;{}]*;',event)
        if not m:raise ValueError('original physical declaration missing '+n)
        extra+=m[0]+'\n'
    if not re.search(r'(?m)^char\s*\*aszStatus\[',native):
        m=re.search(r'(?m)^char\s*\*aszStatus\[[^;]*;',event)
        if not m:raise ValueError('original status names missing')
        extra+=m[0]+'\n'
    for n,b in bodies.items():
        try:prior=definition(native,n)
        except ValueError:pass
        else:native=native.replace(prior,'',1)
        extra+=b[:b.index('{')].strip()+';\n'
    extra+='\n'.join(bodies.values())+'\n'
    anchor='int main(int argc,char **argv){'
    if native.count(anchor)!=1 or native.count(ROUND_OBSERVATIONS)!=1:raise ValueError('attack anchor drift')
    native=native.replace(anchor,extra+anchor,1)
    return native.replace(ROUND_OBSERVATIONS,ROUND_OBSERVATIONS+ATTACK_OBSERVATIONS.replace("ENTRY_FIELD","char_index" if profile=="bismarck" else "charaindex"),1),has_lua

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
        native,has_lua=attack_native(profile,source,battle,event,roots[profile])
        traps=None
        runs=[]
        with tempfile.TemporaryDirectory(prefix="stoneage-original-attack-round-") as tmp:
            for opt in ("-O0","-O2"):
                exe=Path(tmp)/("probe"+opt)
                traps=compile_probe(profile,roots[profile],native,exe,opt,None if opt=="-O0" else traps,link_libraries=('-lm',))
                execute=subprocess.run([str(exe),*map(str,paths)],
                                     input="".join(f"{selected} {mode}\n" for mode in range(4)),
                                     capture_output=True,text=True)
                if execute.returncode or any(not l.startswith("TRACE|") for l in execute.stderr.splitlines() if l.strip()):
                    frames=re.findall(r"probe-(?:O0|O2)\(\+(0x[0-9a-f]+)\)",execute.stderr)
                    symbols=subprocess.run(["addr2line","-f","-C","-e",str(exe),*frames],
                                           capture_output=True,text=True).stdout if frames else "NO_FRAMES"
                    raise ValueError("native original attack round "+profile+" "+opt+
                                     " code="+str(execute.returncode)+" stderr="+execute.stderr[-4400:]+
                                     " symbols="+symbols+" stdout="+execute.stdout[-1500:])
                waits=[x for x in execute.stdout.splitlines() if x.startswith("REAL_HEADER_ATTACK_ROUND|")]
                if len(waits)!=4 or execute.stdout.count("REAL_HEADER_EXIT|")!=4:
                    raise ValueError("missing four real attack-round/Exit cycles")
                for mode,row in enumerate(waits):
                    if f"|mode={mode}|battle={mode%3}|turn=1|" not in row:
                        raise ValueError("battle cursor/turn drift "+row)
                runs.append(execute.stdout)
        if runs[0]!=runs[1]:
            raise ValueError("original attack-round trace O0/O2 divergence "+profile)
        print(f"PROFILE|{profile}|attack_rounds_per_optimization=4|guard_rounds_per_optimization=4|encounters_per_optimization=4|optimizations=O0,O2|sha256={hashlib.sha256(runs[0].encode()).hexdigest()}",flush=True)
        originals=attack_originals(profile,battle,event,roots[profile])
        char=pp_file(profile,roots[profile],LAYOUTS[profile]/'char/char_base.c')
        originals['CHAR_getFunctionPointer']=definition(char,'CHAR_getFunctionPointer')
        if profile=='bismarck':
            workspace=pp_file(profile,roots[profile],LAYOUTS[profile].parent/'common/workspace.c')
            originals['strncatsafe']=definition(workspace,'strncatsafe')
        battle_path=roots[profile]/LAYOUTS[profile]/"battle/battle.c"
        print(f"PROVENANCE|{profile}|commit={PINNED[profile]}|battle_file_sha256={hashlib.sha256(battle_path.read_bytes()).hexdigest()}",flush=True)
        for name,body in originals.items():
            print(f"ORIGINAL_FUNCTION|{profile}|{name}|preprocessed_body_sha256={hashlib.sha256(body.encode()).hexdigest()}",flush=True)
        for row in runs[0].splitlines():
            if row.startswith(("REAL_HEADER_ATTACK_ROUND|","REAL_HEADER_GUARD_ROUND|")):print("ACTUAL|"+profile+"|"+row,flush=True)
    print("BOUNDARY|full_original_Battling;controlled_single_player_attack_guarded_enemy;no_terminal_Finish",flush=True)
    print("OPEN|death_terminal_Finish_profit_natural_AI_network_Lua",flush=True)
    print("RESOLUTION|ORIGINAL_REAL_HEADER_PARTY_PET_ATTACK_ROUND_BOUNDED_PASS",flush=True)

if __name__=="__main__":
    main()
