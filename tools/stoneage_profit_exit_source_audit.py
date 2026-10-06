"""Bounded original PvE profit/exit composition at three clean source pins.

Original bodies, enums and status table exist only in a TemporaryDirectory.
Field getters and external notifications are controlled harness seams. This
does not certify the original command driver or the modern lethal638 runtime.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from hashlib import sha256
from itertools import product
from pathlib import Path
import re
import subprocess
import tempfile

from tools.stoneage_guard_break2_source_audit import PINNED, LAYOUTS, _text, _sha, _compact
from tools.stoneage_mdfyattack_source_audit import _definition, _strip


FUNCTIONS = (
    "BATTLE_BadStatusAllClr", "_BATTLE_Exit", "BATTLE_PetDefaultExit",
    "BATTLE_UltimateExtra", "BATTLE_NormalDeadExtra", "BATTLE_AddExpItem",
    "BATTLE_AddProfit",
)
STATUS_FIELDS = (
    "CHAR_WORKPOISON", "CHAR_WORKPARALYSIS", "CHAR_WORKSLEEP",
    "CHAR_WORKSTONE", "CHAR_WORKDRUNK", "CHAR_WORKCONFUSION",
    "CHAR_WORKWEAKEN", "CHAR_WORKDEEPPOISON", "CHAR_WORKBARRIER", "CHAR_WORKNOCAST",
)
ENUM_SYMBOLS = (
    ("char_base.h", "CHAR_TYPEPLAYER"), ("char_base.h", "CHAR_PETMAIL_NONE"),
    ("battle.h", "BATTLE_TYPE_P_vs_E"), ("battle.h", "BATTLE_CHARMODE_FINAL"),
    ("battle.h", "BATTLE_ERR_NONE"), ("battle.h", "BATTLE_S_TYPE_PLAYER"),
    ("battle.h", "BATTLE_COM_NONE"), ("battle_event.h", "BATTLE_ST_END"),
)
SOURCE_MACROS = (
    "BATTLE_ENTRY_MAX", "SIDE_OFFSET", "CHAR_MAXPETHAVE", "BENT_FLG_ULTIMATE",
    "CH_FIX_PLAYERDEAD", "CH_FIX_PLAYEULTIMATE", "AI_FIX_PLAYERDEAD",
    "AI_FIX_PLAYERULTIMATE", "AI_FIX_PETDEAD", "AI_FIX_PETULTIMATE",
    "AI_FIX_PETWIN", "AI_FIX_PETGOLDWIN", "CHAR_BATTLEFLG_ULTIMATE",
)


STUBS = r'''
typedef struct {union {int charaindex;int char_index;};int escape,flg,getitem[3];} BATTLE_ENTRY;
typedef struct {int type;BATTLE_ENTRY Entry[10];} BATTLE_SIDE;
typedef struct {int dpbattle,type,norisk,use; BATTLE_SIDE Side[2];} BATTLE;
static BATTLE BattleArray[1];
static int elder_success,warp_calls;
static char trace[65536];
static int trace_length;
void note(char kind,int id,int value){trace_length+=snprintf(trace+trace_length,sizeof(trace)-trace_length,"%c:%d:%d,",kind,id,value);if(trace_length>=sizeof(trace)-128)abort();}
int status_field(int field){for(int i=1;i<BATTLE_ST_END;i++)if(StatusTbl[i]==field)return 1;return 0;}

static int ints[32][512],works[32][512],flags[32][512],pets[32][5],valid[32];
int CHAR_CHECKINDEX(int i){return i>=0&&i<32&&valid[i];}
int BATTLE_CHECKINDEX(int i){return i==0;}
int BATTLE_CHECKSIDE(int i){return i==0||i==1;}
int CHAR_getInt(int i,int f){if(!CHAR_CHECKINDEX(i))abort();if(f==CHAR_DEFAULTPET)note('R',i,ints[i][f]);return ints[i][f];}
int CHAR_getWorkInt(int i,int f){if(!CHAR_CHECKINDEX(i))abort();return works[i][f];}
int CHAR_getFlg(int i,int f){if(!CHAR_CHECKINDEX(i))abort();return flags[i][f];}
int CHAR_setInt(int i,int f,int v){if(!CHAR_CHECKINDEX(i))abort();if(f==CHAR_DEFAULTPET)note('S',i,v);if(f==CHAR_HP)note('H',i,v);if(f==CHAR_DEADCOUNT)note('D',i,v);if(f==CHAR_DEADPETCOUNT)note('P',i,v);return ints[i][f]=v;}
int CHAR_setWorkInt(int i,int f,int v){if(!CHAR_CHECKINDEX(i))abort();if(status_field(f))note('Z',i,v);return works[i][f]=v;}
int CHAR_setFlg(int i,int f,int v){if(!CHAR_CHECKINDEX(i))abort();if(f==CHAR_ISDIE)note('F',i,v);return flags[i][f]=v;}
int CHAR_getCharPet(int i,int slot){if(!CHAR_CHECKINDEX(i)||slot<0||slot>=5)abort();return pets[i][slot];}
int BATTLE_No2Index(int b,int no){if(b!=0||no<0||no>=20)abort();return BattleArray[0].Side[no/10].Entry[no%10].charaindex;}
int CHAR_getItemIndex(int i,int slot){return -1;}
int ITEM_CHECKINDEX(int i){return 0;}
int ITEM_getWorkInt(int i,int f){abort();}
int getFdnum(void){abort();}
int CHAR_setItemIndex(int i,int slot,int v){abort();}
int RAND(int lo,int hi){abort();}
int BATTLE_ItemDelCheck(int i){abort();}
int ITEM_endExistItemsOne(int i){abort();}
int BATTLE_getRidePet(int i){return -1;}
int CHAR_setMaxExp(int i,int v){return ints[i][CHAR_EXP]=v;}
int CHAR_PetAddVariableAi(int i,int delta){note('A',i,delta);return works[i][500]+=delta;}
int CHAR_AddCharm(int i,int delta){note('C',i,delta);return works[i][501]+=delta;}
int CHAR_getElderPosition(int elder,int*f,int*x,int*y){*f=8000;*x=1;*y=2;return elder_success;}
int CHAR_warpToSpecificPoint(int i,int f,int x,int y){if(f!=8000||x!=1||y!=2)abort();warp_calls++;note('W',i,f);return 0;}
int getBattleDebugMsg(void){return 0;}
int CHAR_DischargePartyNoMsg(int i){return 0;}
int BATTLE_talkToCli(int i,char*s,int c){return 0;}
int CHAR_endCharOneArray(int i){valid[i]=0;return 0;}
int CHAR_complianceParameter(int i){return 0;}
int CHAR_Skillupsend(int i){return 0;}
int CHAR_send_P_StatusString(int i,int flags){return 0;}
int CHAR_send_K_StatusString(int i,int k,int flags){return 0;}
int CHAR_PartyUpdate(int i,int flags){return 0;}
int getfdFromCharaIndex(int i){return i;}
int getfdFromchar_index(int i){return i;}
int GmsvServer_FS_send(int fd,int flg){return 0;}
int GmsvServer_XYD_send(int fd,int x,int y,int dir){return 0;}
int lssproto_FS_send(int fd,int flg){return 0;}
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
int occupied(int id){for(int j=0;j<2;j++)for(int i=0;i<BATTLE_ENTRY_MAX;i++)if(BattleArray[0].Side[j].Entry[i].charaindex==id)return j*SIDE_OFFSET+i;return -1;}
int status_count(int id){int n=0;for(int i=1;i<BATTLE_ST_END;i++)n+=works[id][StatusTbl[i]]!=0;return n;}
void snapshot(int id){printf(" %d %d %d %d %d %d %d %d %d %d %d",valid[id],occupied(id),ints[id][CHAR_HP],flags[id][CHAR_ISDIE],ints[id][CHAR_DEADCOUNT],works[id][500],status_count(id),works[id][CHAR_WORKBATTLEMODE],works[id][CHAR_WORKBATTLEINDEX],occupied(id)<0?-1:BattleArray[0].Side[occupied(id)/SIDE_OFFSET].Entry[occupied(id)%SIDE_OFFSET].escape,works[id][CHAR_WORKBATTLECOM1]);}
'''
MAIN = r'''
int main(void){
  int mode,oh,ph,ou,pu,od,pd,sel,level,norisk,side,elder,owner_slot;
  if(BATTLE_ENTRY_MAX!=10||SIDE_OFFSET!=10||CHAR_MAXPETHAVE!=5||BATTLE_ST_END!=11)abort();
  if(StatusTbl[0]!=-1)abort();
  int expected_fields[10]={CHAR_WORKPOISON,CHAR_WORKPARALYSIS,CHAR_WORKSLEEP,CHAR_WORKSTONE,CHAR_WORKDRUNK,CHAR_WORKCONFUSION,CHAR_WORKWEAKEN,CHAR_WORKDEEPPOISON,CHAR_WORKBARRIER,CHAR_WORKNOCAST};
  for(int i=0;i<10;i++)if(StatusTbl[i+1]!=expected_fields[i])abort();
  while(scanf("%d%d%d%d%d%d%d%d%d%d%d%d%d",&mode,&oh,&ph,&ou,&pu,&od,&pd,&sel,&level,&norisk,&side,&elder,&owner_slot)==13){
    memset(&BattleArray,0,sizeof(BattleArray));memset(ints,0,sizeof(ints));memset(works,0,sizeof(works));memset(flags,0,sizeof(flags));memset(valid,0,sizeof(valid));
    memset(pets,-1,sizeof(pets));trace_length=warp_calls=0;trace[0]=0;elder_success=elder;
    BattleArray[0].use=TRUE;BattleArray[0].type=BATTLE_TYPE_P_vs_E;BattleArray[0].norisk=norisk;
    for(int j=0;j<2;j++){BattleArray[0].Side[j].type=j==side?BATTLE_S_TYPE_PLAYER:BATTLE_S_TYPE_ENEMY;for(int i=0;i<10;i++){BattleArray[0].Side[j].Entry[i].charaindex=-1;BattleArray[0].Side[j].Entry[i].escape=7;for(int k=0;k<3;k++)BattleArray[0].Side[j].Entry[i].getitem[k]=-1;}}
    int ids[4]={1,2,3,10};
    for(int k=0;k<4;k++){int id=ids[k];valid[id]=1;ints[id][CHAR_LV]=id==1?level:10;ints[id][CHAR_WHICHTYPE]=id==1?CHAR_TYPEPLAYER:(id==10?CHAR_TYPEENEMY:CHAR_TYPEPET);ints[id][CHAR_HP]=20;works[id][CHAR_WORKBATTLEMODE]=BATTLE_CHARMODE_BATTLE;works[id][CHAR_WORKBATTLEINDEX]=0;works[id][CHAR_WORKBATTLECOM1]=99;for(int i=1;i<BATTLE_ST_END;i++)works[id][StatusTbl[i]]=9;}
    pets[1][0]=2;pets[1][1]=3;ints[1][CHAR_DEFAULTPET]=sel;works[2][CHAR_WORKPLAYERINDEX]=works[3][CHAR_WORKPLAYERINDEX]=1;
    ints[1][CHAR_HP]=oh;ints[2][CHAR_HP]=ph;ints[3][CHAR_HP]=0;works[3][CHAR_WORKBATTLEMODE]=BATTLE_CHARMODE_NONE;works[3][CHAR_WORKBATTLEINDEX]=77;
    flags[1][CHAR_ISDIE]=od;flags[2][CHAR_ISDIE]=pd;
    BattleArray[0].Side[side].Entry[owner_slot].charaindex=1;BattleArray[0].Side[side].Entry[owner_slot].flg=ou?BENT_FLG_ULTIMATE:0;
    BattleArray[0].Side[side].Entry[owner_slot+5].charaindex=2;BattleArray[0].Side[side].Entry[owner_slot+5].flg=pu?BENT_FLG_ULTIMATE:0;
    BattleArray[0].Side[1-side].Entry[0].charaindex=10;
    int bid[2]={(1-side)*SIDE_OFFSET,-1};
    if(mode==1){ints[1][CHAR_HP]=20;ints[2][CHAR_HP]=0;flags[1][CHAR_ISDIE]=flags[2][CHAR_ISDIE]=0;BattleArray[0].Side[side].Entry[owner_slot+5].flg=BENT_FLG_ULTIMATE;}
    if(mode==2){ints[3][CHAR_HP]=20;works[3][CHAR_WORKBATTLEMODE]=BATTLE_CHARMODE_BATTLE;works[3][CHAR_WORKBATTLEINDEX]=0;BattleArray[0].Side[side].Entry[(owner_slot+1)%5+5].charaindex=3;}
    if(mode==3){ints[1][CHAR_HP]=ints[2][CHAR_HP]=20;BattleArray[0].Side[side].Entry[owner_slot].flg=BattleArray[0].Side[side].Entry[owner_slot+5].flg=0;ints[10][CHAR_HP]=0;ints[10][CHAR_EXP]=100;flags[1][CHAR_ISDIE]=flags[2][CHAR_ISDIE]=0;flags[10][CHAR_ISDIE]=pd;BattleArray[0].Side[1-side].Entry[0].flg=pu?BENT_FLG_ULTIMATE:0;bid[0]=side*SIDE_OFFSET+owner_slot;}
    if(BATTLE_AddProfit(0,bid)!=BATTLE_ERR_NONE)abort();
    if(mode==1){ints[1][CHAR_HP]=0;if(BATTLE_AddProfit(0,bid)!=BATTLE_ERR_NONE)abort();}
    if(BATTLE_AddProfit(0,bid)!=BATTLE_ERR_NONE)abort();
    printf("%d %d %d %d %d %d %d %d %d %d",ints[1][CHAR_DEFAULTPET],works[1][501],ints[1][CHAR_DEADPETCOUNT],works[1][CHAR_WORKGETEXP],ints[1][CHAR_KILLPETCOUNT],warp_calls,pets[1][0],pets[1][1],ints[10][CHAR_EXP],works[10][CHAR_WORKBATTLEFLG]);
    for(int k=0;k<4;k++)snapshot(ids[k]);
    printf("|%s\n",trace);
  }
  return 0;
}
'''


@dataclass(frozen=True)
class Case:
    mode: int = 0  # simultaneous scan, pet then player, separate selected entry, enemy profit
    owner_hp: int = 0
    pet_hp: int = 0
    owner_ultimate: int = 1
    pet_ultimate: int = 1
    owner_isdie: int = 0
    pet_isdie: int = 0
    selection: int = 0  # -1 none; 0 paired pet; 1 carried pet
    level: int = 11
    norisk: int = 0
    side: int = 0
    elder_success: int = 0
    owner_slot: int = 0

    def row(self):
        return tuple(getattr(self, name) for name in self.__dataclass_fields__)


def cases():
    result = [Case(0, *row) for row in product(
        (0, 20), (0, 20), (0, 1), (0, 1), (0, 1), (0, 1),
        (-1, 0, 1), (10, 11), (0, 1), (0, 1), (0, 1), (0, 4))]
    for mode in (1, 2):
        result += [Case(mode=mode, selection=sel, level=lv, norisk=risk,
                        side=side, owner_ultimate=ult, elder_success=elder, owner_slot=slot)
                   for sel, lv, risk, side, ult, elder, slot in product(
                       (-1, 0, 1), (10, 11), (0, 1), (0, 1), (0, 1), (0, 1), (0, 4))]
    result += [Case(mode=3, level=lv, pet_ultimate=ult, pet_isdie=die, owner_slot=slot)
               for lv, ult, die, slot in product((1, 10, 30), (0, 1), (0, 1), (0, 4))]
    return result


def _enum(text, symbol):
    matches = re.findall(r"\benum\s*\{[^{}]*\}", text, re.S)
    found = [block for block in matches if re.search(r"\b"+re.escape(symbol)+r"\b", block)]
    if len(found) != 1:
        raise ValueError("ambiguous original header enum: " + symbol)
    return found[0] + ";\n"


def _source(root):
    battle = root / "battle/battle.c"
    event = root / "battle/battle_event.c"
    headers = {name: _strip(_text(root / "include" / name))
               for name in ("char_base.h", "battle.h", "battle_event.h")}
    clean = _strip(_text(battle))
    bodies = []
    for name in FUNCTIONS:
        window = _definition(clean, name, raw_window=True)
        # Drop only the next function's outer preprocessor directives after the
        # last closing brace. Internal conditional source code is unchanged.
        bodies.append(window[:window.rfind("}")+1])
    enums = "".join(_enum(headers[h], symbol) for h, symbol in ENUM_SYMBOLS)
    table = re.search(r"\bint\s+StatusTbl\s*\[\s*\]\s*=\s*\{.*?\};",
                      _strip(_text(event)), re.S)
    if table is None:
        raise ValueError("missing original status table")
    # Resolve conditional original header macros with all build features off.
    # In particular Bismarck's _MULTIPLAYER_ layout has separate 12/10 paths.
    header_input = re.sub(r"^\s*#\s*include[^\n]*", "",
                          "\n".join(headers.values()), flags=re.M)
    macro_profile = subprocess.run(["cc", "-E", "-dM", "-x", "c", "-"],
        input=header_input, capture_output=True, text=True, check=True).stdout
    macros = []
    for name in SOURCE_MACROS:
        found = re.findall(r"^\s*#\s*define\s+"+name+r"\b[^\n]*", macro_profile, re.M)
        if len(found) != 1:
            raise ValueError("ambiguous original header macro: " + name)
        macros.append(found[0].strip())
    body = "\n".join(bodies)
    declared = set(re.findall(r"\b[A-Z][A-Z_0-9]*\b", enums)) | set(SOURCE_MACROS)
    calls = set(re.findall(r"\b\w+(?=\s*\()", body))
    fields = sorted(set(re.findall(r"\b(?:CHAR|BATTLE|BENT|ITEM)_[A-Z][A-Z_0-9]*\b", body))
                    | set(STATUS_FIELDS))
    # Synthetic enum numbers are getter keys only. Source type/command/status,
    # errors, layouts and arithmetic constants are taken from original headers.
    symbolic = [name for name in fields if name not in declared | calls | {"BATTLE_ENTRY", "BATTLE"}]
    prefix = ("#include <stdio.h>\n#include <stdlib.h>\n#include <string.h>\n"
              "#include <time.h>\n#define BOOL int\n#define TRUE 1\n#define FALSE 0\n")
    prefix += "\n".join(macros) + "\n" + enums
    prefix += "".join(f"#define {name} {idx+32}\n" for idx, name in enumerate(symbolic))
    # The exact original declaration is compiled, including all ten
    # unconditional statuses. No six-entry substitute is permitted.
    # Static call-site gates are deliberately separate from native execution.
    # Neither the full Battling driver nor BattleModel is compiled by this audit.
    driver = _definition(clean, "BATTLE_Battling", raw_window=True)
    bm = _definition(_strip(_text(event)), "BATTLE_BattleModel", raw_window=True)
    compact = _compact(driver)
    anchors = (
        "BATTLE_BattleModel(battleindex,attackNo,myside);break;",
        "BATTLESTR_ADD(szBadStatusString);BATTLE_AddProfit(battleindex,aAttackList);",
        "BATTLE_AddProfit(battleindex,aAttackList);if(++attack_count>=attack_max)break;",
        "aAttackList[0]=attackNoSub;aAttackList[1]=-1;BATTLE_AddProfit(battleindex,aAttackList);",
    )
    if any(a not in compact for a in anchors) or "BATTLE_AddProfit(" in _compact(bm):
        raise ValueError("static profit boundary source drift")
    return prefix + table.group(0) + "\n" + STUBS + "\n" + body + "\n" + MAIN, {
        "battle_c_sha256": _sha(battle), "battle_event_c_sha256": _sha(event),
        "header_sha256": {n: _sha(root / "include" / n) for n in headers},
        "function_comment_stripped_sha256": {
            name: sha256(body.encode()).hexdigest() for name, body in zip(FUNCTIONS, bodies)},
        "static_profit_boundary_anchors": len(anchors),
        "static_battlemodel_internal_profit_calls": 0,
    }


def _expected(case):
    # An independent state-machine expectation for injected death snapshots.
    # This is an audit witness, not the production runtime or a guessed original
    # command driver. The native scan itself chooses processing order.
    state = {i: dict(valid=1, occupied=-1, hp=20, die=0, deaths=0, ai=0,
                     statuses=10, mode=4, battle=0, com=99)
             for i in (1, 2, 3, 10)}
    state[1].update(occupied=case.side*10+case.owner_slot, hp=case.owner_hp, die=case.owner_isdie)
    state[2].update(occupied=case.side*10+case.owner_slot+5, hp=case.pet_hp, die=case.pet_isdie)
    state[3].update(hp=0, mode=0, battle=77)
    state[10].update(occupied=(1-case.side)*10)
    selection, charm, deadpets, exp, kills, warps = case.selection, 0, 0, 0, 0, 0
    enemy_exp, enemy_ultimate = (100 if case.mode == 3 else 0), 0
    ultimate = {1: case.owner_ultimate, 2: case.pet_ultimate, 3: 0, 10: 0}
    trace = []
    divisor = 2 if case.level <= 10 else 1

    def note(tag, who, value):
        trace.append(f"{tag}:{who}:{value}")

    def read_selection():
        note("R", 1, selection)
        return {0: 2, 1: 3}.get(selection)

    def loyalty(who, delta):
        state[who]["ai"] += delta
        note("A", who, delta)

    def exit_entry(who):
        note("X", who, 0)
        entry = state[who]
        slot = entry["occupied"]
        if slot < 0:
            return
        entry.update(occupied=-1, mode=6, battle=-1)
        if who == 10:
            entry["valid"] = 0
        elif who == 1:
            # Source scan has already marked this dead player. Exit heals and
            # clears it; selected helper and paired occupancy are separate.
            entry.update(hp=1, die=0, statuses=0)
            note("F", 1, 0)
            note("H", 1, 1)
            for _ in STATUS_FIELDS:
                note("Z", 1, 0)
            note("F", 1, 0)  # Original BadStatusAllClr also clears ISDIE.
            for pet in (2, 3):
                p = state[pet]
                if p["occupied"] == slot+5:
                    p.update(occupied=-1, mode=0, battle=-1)
                if p["die"] or p["hp"] <= 0:
                    p.update(hp=1, die=0)
                    note("F", pet, 0)
                    note("H", pet, 1)
                p.update(statuses=0, mode=0)
                for _ in STATUS_FIELDS:
                    note("Z", pet, 0)
                p["die"] = 0
                note("F", pet, 0)

    def scan():
        nonlocal selection, charm, deadpets, exp, kills, warps, enemy_exp, enemy_ultimate
        order = sorted((p["occupied"], who) for who, p in state.items()
                       if p["occupied"] >= 0)
        for slot, who in order:
            p = state[who]
            # Earlier exit/roster healing can invalidate a captured scan entry.
            if p["occupied"] != slot or not p["valid"] or p["hp"] > 0 or p["die"]:
                continue
            if case.mode == 3 and who == 10:
                exp += 100 if case.level <= 15 else 1
                kills += 1
                enemy_exp = 0
            p["die"] = 1
            p["deaths"] += 1
            note("F", who, 1)
            note("D", who, p["deaths"])
            if who == 1:
                if ultimate[1]:
                    pet = read_selection()
                    if pet is not None:
                        exit_entry(pet)
                if not case.norisk:
                    delta = (-4 if ultimate[1] else -2)//divisor
                    charm += delta
                    note("C", 1, delta)
                    pet = read_selection()
                    if pet is not None:
                        loyalty(pet, (-1000 if ultimate[1] else -100)//divisor)
                    if not ultimate[1]:
                        p["com"] = 0
                if ultimate[1]:
                    if case.elder_success:
                        warps += 1
                        note("W", 1, 8000)
                    exit_entry(1)
            elif who in (2, 3):
                if ultimate[who]:
                    selection = -1
                    note("S", 1, -1)
                if not case.norisk:
                    loyalty(who, (-1000 if ultimate[who] else -500)//divisor)
                if ultimate[who] or not case.norisk:
                    deadpets += 1
                    note("P", 1, deadpets)
                if ultimate[who]:
                    exit_entry(who)
                elif not case.norisk:
                    p["com"] = 0
            elif ultimate[who]:
                enemy_ultimate = 1
                exit_entry(who)

    if case.mode == 1:
        state[1].update(hp=20, die=0)
        state[2].update(hp=0, die=0)
        ultimate[2] = 1
    elif case.mode == 2:
        state[3].update(hp=20, occupied=case.side*10+(case.owner_slot+1)%5+5, mode=4, battle=0)
    elif case.mode == 3:
        state[1].update(hp=20, die=0)
        state[2].update(hp=20, die=0)
        state[10].update(hp=0, die=case.pet_isdie)
        ultimate[1] = ultimate[2] = 0
        ultimate[10] = case.pet_ultimate
    scan()
    if case.mode == 1:
        state[1]["hp"] = 0
        scan()
    scan()  # Repeating a profit call must not duplicate death/profit effects.
    result = [selection, charm, deadpets, exp, kills, warps, 2, 3, enemy_exp, enemy_ultimate]
    for who in (1, 2, 3, 10):
        p = state[who]
        escape = -1 if p["occupied"] < 0 else 7
        result.extend(p[key] for key in ("valid", "occupied", "hp", "die", "deaths", "ai",
                                          "statuses", "mode", "battle"))
        result.extend((escape, p["com"]))
    return tuple(result), trace


def _adapter_expected(case):
    # Test-only translation of the same injected boundary into the independent
    # immutable adapter. No original source or audit expectation is imported by
    # the adapter. Retain the original expectation as a second comparison.
    from dataclasses import replace
    from tools.stoneage_default_pet_exit_model import DefaultPetExitAuthority
    from tools.stoneage_profit_exit_scan_model import (
        ProfitExitCharacter, ProfitExitSnapshot, resolve_profit_exit_scan,
    )
    characters = {
        str(i): ProfitExitCharacter(str(i), "player" if i == 1 else "enemy" if i == 10 else "pet",
            case.level if i == 1 else 10, 20, None,
            status_counters=(9,) * 10, command=99, escape=7)
        for i in (1, 2, 3, 10)
    }
    def update(pid, **values):
        characters[pid] = replace(characters[pid], **values)
    update("1", occupied_slot=case.side*10+case.owner_slot, hp=case.owner_hp,
           isdie=bool(case.owner_isdie), ultimate=bool(case.owner_ultimate))
    update("2", occupied_slot=case.side*10+case.owner_slot+5, hp=case.pet_hp,
           isdie=bool(case.pet_isdie), ultimate=bool(case.pet_ultimate))
    update("3", hp=0, battle_mode="none", battle_index=77)
    update("10", occupied_slot=(1-case.side)*10)
    if case.mode == 1:
        update("1", hp=20, isdie=False)
        update("2", hp=0, isdie=False, ultimate=True)
    elif case.mode == 2:
        update("3", hp=20, occupied_slot=case.side*10+(case.owner_slot+1)%5+5,
               battle_mode="battle", battle_index=0)
    elif case.mode == 3:
        update("1", hp=20, isdie=False, ultimate=False)
        update("2", hp=20, isdie=False, ultimate=False)
        update("10", hp=0, reward_exp=100, isdie=bool(case.pet_isdie),
               ultimate=bool(case.pet_ultimate))
    authority = DefaultPetExitAuthority("1", {0: "2", 1: "3"}.get(case.selection),
        ("2", "3"), {pid: characters[pid].occupied_slot for pid in ("2", "3")
                     if characters[pid].occupied_slot is not None})
    snapshot = ProfitExitSnapshot(characters, authority, case.side, bool(case.norisk),
                                 (8000, 1, 2) if case.elder_success else None)
    recipient = "1" if case.mode == 3 else "10"
    trace, warps = [], 0
    def scan():
        nonlocal snapshot, warps
        result = resolve_profit_exit_scan(snapshot, recipient_id=recipient)
        snapshot = result.after
        trace.extend(result.effects)
        warps += len(result.warp_requests)
    scan()
    if case.mode == 1:
        chars = dict(snapshot.characters)
        chars["1"] = replace(chars["1"], hp=0)
        snapshot = replace(snapshot, characters=chars)
        scan()
    scan()
    chars = snapshot.characters
    selected = snapshot.authority.selected_pet_id
    owner, enemy = chars["1"], chars["10"]
    result = [-1 if selected is None else snapshot.authority.owned_pet_ids.index(selected),
              owner.charm_delta, owner.dead_pet_count, owner.pending_exp, owner.kill_count,
              warps, 2, 3, enemy.reward_exp, int(enemy.enemy_ultimate)]
    mode = {"none": 0, "battle": 4, "final": 6}
    for pid in ("1", "2", "3", "10"):
        c = chars[pid]
        result.extend((int(c.valid), -1 if c.occupied_slot is None else c.occupied_slot,
                       c.hp, int(c.isdie), c.death_count, c.variable_ai_delta,
                       sum(v != 0 for v in c.status_counters), mode[c.battle_mode],
                       c.battle_index, -1 if c.occupied_slot is None else c.escape, c.command))
    tags = {"selection_read": "R", "selection_write": "S", "hp": "H",
            "death_count": "D", "dead_pet_count": "P", "status_clear": "Z",
            "isdie": "F", "variable_ai_delta": "A", "charm_delta": "C",
            "warp_request": "W", "exit_request": "X"}
    return tuple(result), [f"{tags[e.kind]}:{e.participant_id}:{e.value}" for e in trace]


def analyze_profile(name: str, root: Path, *, verify_scan_model: bool = False):
    root = root.resolve()
    head = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
    dirty = subprocess.check_output(["git", "-C", str(root), "status", "--porcelain"], text=True).strip()
    if head != PINNED[name] or dirty:
        raise ValueError("pinned source commit/tree drift")
    code, hashes = _source(root / LAYOUTS[name])
    vectors = cases()
    with tempfile.TemporaryDirectory(prefix="sa-native-profit-exit-") as folder:
        source, binary = Path(folder)/"oracle.c", Path(folder)/"oracle"
        source.write_text(code)
        compiled = subprocess.run(["cc", "-std=c11", "-O0", "-Werror=implicit-function-declaration",
                                   str(source), "-o", str(binary)], capture_output=True, text=True)
        if compiled.returncode:
            raise ValueError("native compilation failed: " + compiled.stderr)
        rows = subprocess.check_output([str(binary)], input="".join(
            " ".join(map(str, c.row()))+"\n" for c in vectors), text=True).splitlines()
    if len(rows) != len(vectors):
        raise ValueError("native case count drift")
    for case, row in zip(vectors, rows):
        actual, trace = row.split("|", 1)
        got = tuple(map(int, actual.split()))
        wanted, wanted_trace = _expected(case)
        if got != wanted:
            raise ValueError(f"native profit/exit drift: {case}: {got} != {wanted}; {trace}")
        semantic = [t for t in trace.rstrip(",").split(",") if t]
        if semantic != wanted_trace:
            raise ValueError(f"native chronological trace drift: {case}: {semantic} != {wanted_trace}")
        if verify_scan_model:
            model_state, model_trace = _adapter_expected(case)
            if got != model_state or semantic != model_trace:
                raise ValueError(f"immutable scan/native drift: {case}: {got} != {model_state}; {semantic} != {model_trace}")
    return {"profile": name, "commit": head, "native_profit_exit_cases": len(vectors),
            "immutable_scan_model_native_comparisons": len(vectors) if verify_scan_model else 0,
            "original_functions": len(FUNCTIONS), "unconditional_status_fields": 10,
            **hashes}


def main():
    parser = argparse.ArgumentParser()
    for name in PINNED:
        parser.add_argument("--"+name+"-dir", required=True, type=Path)
    parser.add_argument("--verify-scan-model", action="store_true")
    args = parser.parse_args()
    total = 0
    for name in PINNED:
        result = analyze_profile(name, getattr(args, name+"_dir"), verify_scan_model=args.verify_scan_model)
        total += result["native_profit_exit_cases"]
        import json
        print("PROFILE|" + json.dumps(result, sort_keys=True))
    print(f"TOTAL|native_profit_exit_cases={total}|original_functions=7|status_fields=10")
    print("BOUNDARY|declared_feature_off_PvE_no_items_no_ride_controlled_notifications_getters_penalty_delta_helpers")
    print("OPEN|full_command_driver_attack_to_profit_bridge_modern_lethal638_runtime_original_build_membership")
    print("RESOLUTION|BOUNDED_PVE_PROFIT_EXIT_NATIVE_COMPOSITION_PASS")
    if args.verify_scan_model:
        print(f"MODEL|immutable_scan_model_native_comparisons={total}")
        print("RESOLUTION|IMMUTABLE_PVE_PROFIT_EXIT_SCAN_MODEL_NATIVE_PASS")


if __name__ == "__main__":
    main()
