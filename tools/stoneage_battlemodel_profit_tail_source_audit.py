"""Native BattleModel dispatch-tail to AddProfit splice witness R1.

This is deliberately narrower than a full BATTLE_Battling execution. It
executes the exact original BattleModel planner/helper and exact original PvE
profit/exit bodies in one transient C program. The Battling case/tail source
anchors are checked, and the harness invokes them in that exact order.

BATTLE_AttackSeq is a controlled guardian-protocol seam in this milestone.
Actual original GuardianCheck/AttackSeq is independently certified by the
physical source audit but is not yet linked into this same C program.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re
import subprocess
import tempfile

from tools.stoneage_guard_break2_source_audit import (
    PINNED, LAYOUTS, _text, _sha, _compact,
)
from tools.stoneage_mdfyattack_source_audit import _definition, _strip
from tools.stoneage_battletimid_source_audit import _case_block
from tools.stoneage_profit_exit_source_audit import (
    FUNCTIONS as PROFIT_FUNCTIONS,
    STATUS_FIELDS,
    SOURCE_MACROS,
    _enum,
)
from tools.stoneage_default_pet_exit_model import DefaultPetExitAuthority
from tools.stoneage_profit_exit_scan_model import (
    ProfitExitCharacter,
    ProfitExitSnapshot,
    resolve_profit_exit_scan,
)


COMMAND="BATTLE_COM_S_BATTLE_MODEL"


@dataclass(frozen=True)
class Case:
    guardian_enabled: int
    owner_hp: int
    pet_hp: int
    damage: int = 20

    def row(self):
        return (self.guardian_enabled,self.owner_hp,self.pet_hp,self.damage)


def cases():
    return (
        Case(1,10,10,20),  # guardian dies first, owner dies second
        Case(1,30,10,20),  # guardian dies, owner survives
        Case(0,10,10,20),  # no guardian: owner dies on first helper call
    )


def _macro_profile(headers: str) -> dict[str,str]:
    pre=subprocess.run(
        ["cc","-E","-dM","-x","c","-"],
        input=headers,capture_output=True,text=True,check=True,
    ).stdout
    result={}
    for name in SOURCE_MACROS:
        found=re.findall(r"^\s*#\s*define\s+"+name+r"\b[^\n]*",pre,re.M)
        if len(found)!=1:
            raise ValueError("ambiguous original header macro: "+name)
        result[name]=found[0].strip()
    return result


def _feature_off_enum_value(header_text: str, symbol: str) -> int:
    """Compile one original enum block with all optional build features off."""
    block=_enum(_strip(header_text),symbol)
    code=(
        "#include <stdio.h>\n"
        + block
        + "\nint main(void){printf(\"%d\\n\"," + symbol + ");return 0;}\n"
    )
    with tempfile.TemporaryDirectory(prefix="sa-feature-off-enum-") as folder:
        source=Path(folder)/"enum.c"
        binary=Path(folder)/"enum"
        source.write_text(code,encoding="utf-8")
        built=subprocess.run(
            ["cc","-std=c11","-O0",str(source),"-o",str(binary)],
            capture_output=True,text=True,
        )
        if built.returncode:
            raise ValueError(
                "feature-off enum compilation failed: "+built.stderr[-2500:]
            )
        return int(subprocess.check_output([str(binary)],text=True).strip())


def _raw_function_body(text: str, name: str) -> str:
    window=_definition(_strip(text),name,raw_window=True)
    return window[:window.rfind("}")+1]


def _exact_function_body(text: str, name: str) -> str:
    return _definition(_strip(text),name)


def _source(name: str, root: Path):
    base=root/LAYOUTS[name]
    battle_path=base/"battle/battle.c"
    event_path=base/"battle/battle_event.c"
    battle=_text(battle_path)
    event=_text(event_path)
    headers={
        n:_text(base/"include"/n)
        for n in ("char_base.h","battle.h","battle_event.h")
    }
    header_input=re.sub(
        r"^\s*#\s*include[^\n]*","",
        "\n".join(headers.values()),flags=re.M,
    )
    macros=_macro_profile(header_input)
    if not all(
        int(re.search(r"\b(\d+)\b",macros[k]).group(1))==v
        for k,v in (("BATTLE_ENTRY_MAX",10),("SIDE_OFFSET",10),("CHAR_MAXPETHAVE",5))
    ):
        raise ValueError("dispatch-tail witness requires original reduced SIDE_OFFSET10 layout")
    st_end=_feature_off_enum_value(
        headers["battle_event.h"],
        "BATTLE_ST_END",
    )
    if st_end!=11:
        raise ValueError("dispatch-tail witness requires original ten status fields")

    clean_battle=_strip(battle)
    clean_event=_strip(event)
    profit="\n".join(_raw_function_body(clean_battle,n) for n in PROFIT_FUNCTIONS)
    # Reuse the exact balanced function extraction already used by the accepted
    # BattleModel lifecycle/source audits. The raw windows include surrounding
    # feature guards and are unsuitable for direct standalone concatenation.
    helper=_exact_function_body(clean_event,"BATTLE_BattleModel_ATTACK")
    model=_exact_function_body(clean_event,"BATTLE_BattleModel")

    case_at=battle.find("case "+COMMAND+":")
    if case_at<0:
        raise ValueError("missing BattleModel dispatch case")
    case_source=_case_block(battle[case_at:],"case "+COMMAND+":")
    compact_case=_compact(_strip(case_source))
    if "BATTLE_BattleModel(battleindex,attackNo,myside);break;" not in compact_case:
        raise ValueError("BattleModel dispatch case source drift")
    compact_driver=_compact(_strip(_definition(clean_battle,"BATTLE_Battling",raw_window=True)))
    tail_anchor="BATTLESTR_ADD(szBadStatusString);BATTLE_AddProfit(battleindex,aAttackList);"
    if tail_anchor not in compact_driver:
        raise ValueError("BattleModel command-tail AddProfit anchor drift")
    if "BATTLE_AddProfit(" in _compact(model):
        raise ValueError("BattleModel unexpectedly contains internal AddProfit")

    table=re.search(
        r"\bint\s+StatusTbl\s*\[\s*\]\s*=\s*\{.*?\};",
        clean_event,re.S,
    )
    if table is None:
        raise ValueError("missing original StatusTbl")

    combined=profit+"\n"+helper+"\n"+model
    calls=set(re.findall(r"\b\w+(?=\s*\()",combined))
    fields=set(re.findall(r"\b(?:CHAR|BATTLE|BENT|ITEM|TARGET|PETSKILL|BCF)_[A-Z][A-Z_0-9]*\b",combined))
    fields.update(STATUS_FIELDS)
    semantic={
        "BATTLE_ENTRY","BATTLE_SIDE","BATTLE",
        "BATTLE_ENTRY_MAX","SIDE_OFFSET","CHAR_MAXPETHAVE","BENT_FLG_ULTIMATE",
        "CH_FIX_PLAYERDEAD","CH_FIX_PLAYEULTIMATE","AI_FIX_PLAYERDEAD",
        "AI_FIX_PLAYERULTIMATE","AI_FIX_PETDEAD","AI_FIX_PETULTIMATE",
        "AI_FIX_PETWIN","AI_FIX_PETGOLDWIN","CHAR_BATTLEFLG_ULTIMATE",
    }
    fixed={
        "TRUE":1,"FALSE":0,
        "BATTLE_ST_END":st_end,
        "BATTLE_COM_S_BATTLE_MODEL":900,
        "BATTLE_COM_NONE":0,
        "BATTLE_RET_ALLGUARD":1,
        "BATTLE_RET_MISS":2,
        "BATTLE_RET_DODGE":3,
        "BATTLE_RET_NORMAL":4,
        "BATTLE_RET_CRITICAL":5,
        "BATTLE_RET_ARRANGE":6,
        "BATTLE_MD_ABSROB":1,
        "BATTLE_MD_VANISH":2,
        "TARGET_SIDE_0":20,
        "TARGET_SIDE_1":21,
        "PETSKILL_OPTION":0,
        "BATTLE_S_TYPE_PLAYER":101,
        "BATTLE_S_TYPE_ENEMY":102,
        "BATTLE_TYPE_P_vs_E":103,
        "BATTLE_TYPE_P_vs_P":107,
        "BATTLE_CHARMODE_NONE":104,
        "BATTLE_CHARMODE_BATTLE":105,
        "BATTLE_CHARMODE_FINAL":106,
        "BATTLE_ERR_NONE":0,
        "CHAR_TYPEPLAYER":201,
        "CHAR_TYPEPET":202,
        "CHAR_TYPEENEMY":203,
        "CHAR_PETMAIL_NONE":0,
    }
    # These are synthetic control/field numbers only. Arithmetic/layout penalty
    # macros above retain the pinned original definitions.
    next_id=300
    defines=[]
    for symbol in sorted(fields):
        if symbol in semantic:
            continue
        if symbol in fixed:
            defines.append(f"#define {symbol} {fixed[symbol]}")
        elif symbol not in calls:
            defines.append(f"#define {symbol} {next_id}")
            next_id+=1
    for symbol,value in fixed.items():
        if symbol not in fields and symbol not in {"TRUE","FALSE","BATTLE_ST_END"}:
            defines.append(f"#define {symbol} {value}")

    macro_lines="\n".join(macros[k] for k in SOURCE_MACROS)
    prefix=r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#define BOOL int
#define TRUE 1
#define FALSE 0
#define min(a,b) ((a)<(b)?(a):(b))
#define max(a,b) ((a)>(b)?(a):(b))
typedef struct {union {int charaindex;int char_index;};int escape,flg,getitem[3];} BATTLE_ENTRY;
typedef struct {int type;BATTLE_ENTRY Entry[10];} BATTLE_SIDE;
typedef struct {int dpbattle,type,norisk,use; BATTLE_SIDE Side[2];} BATTLE;
typedef struct {int index,target,actionNumber;} AttackObject;
static BATTLE BattleArray[1];
static int ints[32][1024],works[32][1024],flags[32][1024],pets[32][5],valid[32];
static int guardian_enabled,attack_damage,attackseq_calls,damage_calls,target_checks,rand_calls;
static char option_buf[256]="4|2|||||10";
static char trace[65536];static int trace_length;
float gDamageDiv;
void note(char kind,int id,int value){trace_length+=snprintf(trace+trace_length,sizeof(trace)-trace_length,"%c:%d:%d,",kind,id,value);if(trace_length>=sizeof(trace)-128)abort();}
int CHAR_CHECKINDEX(int i){return i>=0&&i<32&&valid[i];}
int BATTLE_CHECKINDEX(int i){return i==0;}
int BATTLE_CHECKSIDE(int i){return i==0||i==1;}
int CHAR_getInt(int i,int f){if(!CHAR_CHECKINDEX(i))abort();if(f==CHAR_DEFAULTPET)note('R',i,ints[i][f]);return ints[i][f];}
int CHAR_getWorkInt(int i,int f){if(!CHAR_CHECKINDEX(i))abort();return works[i][f];}
int CHAR_getFlg(int i,int f){if(!CHAR_CHECKINDEX(i))abort();return flags[i][f];}
int CHAR_setInt(int i,int f,int v){if(!CHAR_CHECKINDEX(i))abort();if(f==CHAR_DEFAULTPET)note('S',i,v);if(f==CHAR_HP)note('H',i,v);if(f==CHAR_DEADCOUNT)note('D',i,v);if(f==CHAR_DEADPETCOUNT)note('P',i,v);return ints[i][f]=v;}
int CHAR_setWorkInt(int i,int f,int v){if(!CHAR_CHECKINDEX(i))abort();return works[i][f]=v;}
int CHAR_setFlg(int i,int f,int v){if(!CHAR_CHECKINDEX(i))abort();if(f==CHAR_ISDIE)note('F',i,v);return flags[i][f]=v;}
int CHAR_getCharPet(int i,int slot){if(!CHAR_CHECKINDEX(i)||slot<0||slot>=5)abort();return pets[i][slot];}
int BATTLE_No2Index(int b,int no){if(b!=0||no<0||no>=20)abort();return BattleArray[0].Side[no/10].Entry[no%10].charaindex;}
int BATTLE_Index2No(int b,int id){for(int s=0;s<2;s++)for(int p=0;p<10;p++)if(BattleArray[b].Side[s].Entry[p].charaindex==id)return s*10+p;return -1;}
int BATTLE_TargetCheck(int b,int no){target_checks++;int id=BATTLE_No2Index(b,no);return CHAR_CHECKINDEX(id)&&ints[id][CHAR_HP]>0;}
int BATTLE_AttackSeq(int a,int d,int *damage,int *guardian,int ignored){
  attackseq_calls++;*damage=attack_damage;*guardian=-1;
  if(guardian_enabled&&d==1&&ints[2][CHAR_HP]>0)*guardian=5;
  return BATTLE_RET_NORMAL;
}
int BATTLE_DamageSub(int a,int d,int *damage,int *pet,int *react){
  damage_calls++;*pet=0;if(react)*react=-1;
  ints[d][CHAR_HP]-=*damage;if(ints[d][CHAR_HP]<0)ints[d][CHAR_HP]=0;
  note('M',d,*damage);return 0;
}
int BATTLE_getReactFlg(int d,int r){return 0;}
void BATTLE_DamageWakeUp(int b,int d){}
int BATTLE_ItemCrushSeq(int d){return 0;}
int BATTLE_StatusAttackCheck(int a,int d,int e,int h,int p,float f,int*out){return 0;}
void BATTLE_BadStatusString(int slot,int effect){}
void BATTLE_MultiList(int b,int target,int*out){out[0]=0;out[1]=-1;}
void BATTLE_NoAction(int b,int a){abort();}
char *PETSKILL_getChar(int array,int pos){return option_buf;}
int getStringFromIndexWithDelim(const char *src,const char *delim,int want,char*out,int outsz){
  if(!src||!delim||!delim[0]||want<=0||outsz<=0)return FALSE;
  char d=delim[0];const char *start=src;int idx=1;
  while(idx<want){const char*p=strchr(start,d);if(!p)return FALSE;start=p+1;idx++;}
  const char *end=strchr(start,d);size_t n=end?(size_t)(end-start):strlen(start);
  if(n>=(size_t)outsz)n=(size_t)outsz-1;memcpy(out,start,n);out[n]='\0';return TRUE;
}
int RAND(int lo,int hi){rand_calls++;if(lo>hi)abort();return lo;}
#define CHAR_GETWORKINT_LOW(i,p) ((int)((unsigned int)CHAR_getWorkInt(i,p)&0xffffU))
#define CHAR_GETWORKINT_HIGH(i,p) ((int)(((unsigned int)CHAR_getWorkInt(i,p)>>16)&0xffffU))
#define BATTLESTR_ADD(s) ((void)0)
int BATTLE_getRidePet(int i){return -1;}
int CHAR_getItemIndex(int i,int slot){return -1;}
int ITEM_CHECKINDEX(int i){return 0;}
int ITEM_getWorkInt(int i,int f){abort();}
int getFdnum(void){abort();}
int CHAR_setItemIndex(int i,int slot,int v){abort();}
int BATTLE_ItemDelCheck(int i){abort();}
int ITEM_endExistItemsOne(int i){abort();}
int CHAR_setMaxExp(int i,int v){return ints[i][CHAR_EXP]=v;}
int CHAR_PetAddVariableAi(int i,int delta){note('A',i,delta);return works[i][900]+=delta;}
int CHAR_AddCharm(int i,int delta){note('C',i,delta);return works[i][901]+=delta;}
int CHAR_getElderPosition(int elder,int*f,int*x,int*y){return 0;}
int CHAR_warpToSpecificPoint(int i,int f,int x,int y){abort();}
int getBattleDebugMsg(void){return 0;}
int CHAR_DischargePartyNoMsg(int i){return 0;}
int BATTLE_talkToCli(int i,char*s,int c){return 0;}
int CHAR_endCharOneArray(int i){valid[i]=0;return 0;}
int CHAR_complianceParameter(int i){return 0;}
int CHAR_Skillupsend(int i){return 0;}
int CHAR_send_P_StatusString(int i,int f){return 0;}
int CHAR_send_K_StatusString(int i,int k,int f){return 0;}
int CHAR_PartyUpdate(int i,int f){return 0;}
int getfdFromCharaIndex(int i){return i;}
int getfdFromchar_index(int i){return i;}
int GmsvServer_FS_send(int fd,int f){return 0;}
int GmsvServer_XYD_send(int fd,int x,int y,int dir){return 0;}
int lssproto_FS_send(int fd,int f){return 0;}
int lssproto_XYD_send(int fd,int x,int y,int dir){return 0;}
int print(char*fmt,...){abort();}
int BATTLE_AddDuelPoint(int b,int*list){abort();}
#define BATTLE_Exit(i,b) traced_exit(__FILE__,__LINE__,i,b)
int _BATTLE_Exit(char*,int,int,int);
int BATTLE_PetDefaultExit(int,int);
void BATTLE_UltimateExtra(int,int,int);
void BATTLE_NormalDeadExtra(int,int,int);
int BATTLE_AddExpItem(int,int*);
int traced_exit(char*file,int line,int id,int battle){note('X',id,0);return _BATTLE_Exit(file,line,id,battle);}
int status_field(int f){for(int i=1;i<BATTLE_ST_END;i++)if(StatusTbl[i]==f)return 1;return 0;}
'''
    status_array='static char *aszStatus[64]={"","x","x","x","x","x","x","x","x","x","x"};\n'
    main=r'''
int main(void){
  int ge,oh,ph,dmg;
  while(scanf("%d%d%d%d",&ge,&oh,&ph,&dmg)==4){
    memset(&BattleArray,0,sizeof(BattleArray));memset(ints,0,sizeof(ints));
    memset(works,0,sizeof(works));memset(flags,0,sizeof(flags));memset(valid,0,sizeof(valid));
    memset(pets,-1,sizeof(pets));trace_length=0;trace[0]=0;
    guardian_enabled=ge;attack_damage=dmg;attackseq_calls=damage_calls=target_checks=rand_calls=0;
    BattleArray[0].use=TRUE;BattleArray[0].dpbattle=0;BattleArray[0].type=BATTLE_TYPE_P_vs_E;
    BattleArray[0].norisk=0;BattleArray[0].Side[0].type=BATTLE_S_TYPE_PLAYER;
    BattleArray[0].Side[1].type=BATTLE_S_TYPE_ENEMY;
    for(int s=0;s<2;s++)for(int p=0;p<10;p++){BattleArray[0].Side[s].Entry[p].charaindex=-1;BattleArray[0].Side[s].Entry[p].escape=7;for(int k=0;k<3;k++)BattleArray[0].Side[s].Entry[p].getitem[k]=-1;}
    valid[1]=valid[2]=valid[10]=1;
    ints[1][CHAR_WHICHTYPE]=CHAR_TYPEPLAYER;ints[2][CHAR_WHICHTYPE]=CHAR_TYPEPET;ints[10][CHAR_WHICHTYPE]=CHAR_TYPEENEMY;
    ints[1][CHAR_LV]=11;ints[2][CHAR_LV]=20;ints[10][CHAR_LV]=20;
    ints[1][CHAR_HP]=oh;ints[2][CHAR_HP]=ph;ints[10][CHAR_HP]=100;
    ints[1][CHAR_DEFAULTPET]=0;pets[1][0]=2;works[2][CHAR_WORKPLAYERINDEX]=1;
    works[1][CHAR_WORKBATTLEMODE]=works[2][CHAR_WORKBATTLEMODE]=works[10][CHAR_WORKBATTLEMODE]=BATTLE_CHARMODE_BATTLE;
    works[1][CHAR_WORKBATTLEINDEX]=works[2][CHAR_WORKBATTLEINDEX]=works[10][CHAR_WORKBATTLEINDEX]=0;
    works[1][CHAR_WORKBATTLECOM1]=works[2][CHAR_WORKBATTLECOM1]=works[10][CHAR_WORKBATTLECOM1]=77;
    BattleArray[0].Side[0].Entry[0].charaindex=1;
    BattleArray[0].Side[0].Entry[5].charaindex=2;
    BattleArray[0].Side[1].Entry[0].charaindex=10;
    works[10][CHAR_WORKBATTLECOM2]=(2<<16)|4;works[10][CHAR_WORKBATTLECOM3]=0;
    int battleindex=0,attackNo=10,myside=1;
    int aAttackList[2]={10,-1};char szBadStatusString[2]={0};
    switch(BATTLE_COM_S_BATTLE_MODEL){
DISPATCH_CASE
    }
    BATTLESTR_ADD(szBadStatusString);
    if(BATTLE_AddProfit(battleindex,aAttackList)!=BATTLE_ERR_NONE)abort();
    int first_deaths=ints[1][CHAR_DEADCOUNT]+ints[2][CHAR_DEADCOUNT];
    if(BATTLE_AddProfit(battleindex,aAttackList)!=BATTLE_ERR_NONE)abort();
    printf("%d %d %d %d %d %d %d %d %d %d %d %d|%s\n",
      attackseq_calls,damage_calls,target_checks,rand_calls,
      ints[1][CHAR_HP],flags[1][CHAR_ISDIE],ints[1][CHAR_DEADCOUNT],works[1][901],
      ints[2][CHAR_HP],flags[2][CHAR_ISDIE],ints[2][CHAR_DEADCOUNT],works[2][900],
      trace);
    if(first_deaths!=ints[1][CHAR_DEADCOUNT]+ints[2][CHAR_DEADCOUNT])abort();
  }
  return 0;
}
'''.replace("DISPATCH_CASE",case_source)
    code=(
        "#include <math.h>\n"+macro_lines+"\n#define BATTLE_ST_END "+str(st_end)+"\n"
        +"\n".join(defines)+"\n"+table.group(0)+"\n"+prefix+"\n"+status_array
        +profit+"\n"+helper+"\n"+model+"\n"+main
    )
    return code,{
        "battle_c_sha256":_sha(battle_path),
        "battle_event_c_sha256":_sha(event_path),
        "static_dispatch_case_anchor":True,
        "static_tail_addprofit_anchor":True,
        "battlemodel_internal_profit_calls":0,
    }


def _expected(case: Case):
    owner_hp=int(case.owner_hp);pet_hp=int(case.pet_hp)
    attackseq=damage_calls=target_checks=rand_calls=0
    damage_trace=[]
    # BattleModel with one living target and object_count=2 owns one excess RAND.
    rand_calls=1
    for _ in range(2):
        target_checks+=1
        if owner_hp<=0:
            continue
        attackseq+=1
        if case.guardian_enabled and pet_hp>0:
            pet_hp=max(0,pet_hp-case.damage);damage_trace.append(("M",2,case.damage))
        else:
            owner_hp=max(0,owner_hp-case.damage);damage_trace.append(("M",1,case.damage))
        damage_calls+=1

    chars={
        "1":ProfitExitCharacter("1","player",11,owner_hp,0,status_counters=(0,)*10,command=77),
        "2":ProfitExitCharacter("2","pet",20,pet_hp,5,status_counters=(0,)*10,command=77),
        "10":ProfitExitCharacter("10","enemy",20,100,10,status_counters=(0,)*10,command=77),
    }
    snap=ProfitExitSnapshot(
        chars,
        DefaultPetExitAuthority("1","2",("2",),{"2":5}),
        0,
        False,
        None,
    )
    result=resolve_profit_exit_scan(snap,recipient_id="10")
    after=result.after.characters
    expected=(
        attackseq,damage_calls,target_checks,rand_calls,
        after["1"].hp,int(after["1"].isdie),after["1"].death_count,after["1"].charm_delta,
        after["2"].hp,int(after["2"].isdie),after["2"].death_count,after["2"].variable_ai_delta,
    )
    return expected,damage_trace,result


def analyze_profile(name: str, root: Path):
    root=root.resolve()
    head=subprocess.check_output(["git","-C",str(root),"rev-parse","HEAD"],text=True).strip()
    dirty=subprocess.check_output(["git","-C",str(root),"status","--porcelain"],text=True).strip()
    if head!=PINNED[name] or dirty:
        raise ValueError("pinned source commit/tree drift")
    code,meta=_source(name,root)
    vectors=cases()
    with tempfile.TemporaryDirectory(prefix="sa-bm-profit-tail-") as folder:
        source=Path(folder)/"oracle.c";binary=Path(folder)/"oracle"
        source.write_text(code,encoding="utf-8")
        built=subprocess.run(
            ["cc","-std=c11","-O0","-Wno-unused-value","-Wno-unused-variable",str(source),"-lm","-o",str(binary)],
            capture_output=True,text=True,
        )
        if built.returncode:
            raise ValueError("native dispatch-tail compile failed: "+built.stderr[-8000:])
        rows=subprocess.check_output(
            [str(binary)],
            input="".join(" ".join(map(str,c.row()))+"\n" for c in vectors),
            text=True,
        ).splitlines()
    if len(rows)!=len(vectors):
        raise ValueError("native dispatch-tail row count drift")
    for case,row in zip(vectors,rows):
        values,trace=row.split("|",1)
        got=tuple(map(int,values.split()))
        wanted,damage_trace,result=_expected(case)
        if got!=wanted:
            raise ValueError(f"native dispatch-tail state drift {case}: {got} != {wanted}; {trace}")
        semantic=[x for x in trace.rstrip(",").split(",") if x]
        damage=[f"{k}:{pid}:{value}" for k,pid,value in damage_trace]
        if semantic[:len(damage)]!=damage:
            raise ValueError(f"damage routing trace drift {case}: {semantic} does not start {damage}")
        first_death=next((i for i,x in enumerate(semantic) if x.startswith("F:")),len(semantic))
        if first_death < len(damage):
            raise ValueError("AddProfit death processing began before all BattleModel tail damage")
        if case.guardian_enabled and case.owner_hp==10 and case.pet_hp==10:
            if damage!=["M:2:20","M:1:20"]:
                raise ValueError("controlled guardian protocol did not route pet then owner")
            if result.processed_death_ids!=("1","2"):
                raise ValueError("multi-victim whole scan did not process owner then pet")
    return {
        "profile":name,
        "commit":head,
        "native_dispatch_tail_cases":len(vectors),
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
        total+=result["native_dispatch_tail_cases"]
        import json
        print("PROFILE|"+json.dumps(result,sort_keys=True))
    print(f"TOTAL|native_dispatch_tail_cases={total}|profiles={len(PINNED)}")
    print("FACT|exact_original_BattleModel_planner_helper_executes_before_single_command_tail_original_AddProfit")
    print("FACT|controlled_guardian_protocol_routes_first_hit_to_pet_and_second_hit_to_owner_before_tail_scan")
    print("FACT|multi_victim_tail_scan_processes_owner_slot0_then_pet_slot5_and_repeat_profit_does_not_duplicate")
    print("BOUNDARY|AttackSeq_guardian_protocol_controlled_in_this_splice;original_AttackSeq_GuardianCheck_is_separately_native_certified_but_not_same_harness")
    print("OPEN|full_BATTLE_Battling_body_same_harness_original_GuardianCheck_lethal638_modern_admission")
    print("RESOLUTION|BATTLEMODEL_DISPATCH_TAIL_PROFIT_SPLICE_NATIVE_PASS")


if __name__=="__main__":
    main()
