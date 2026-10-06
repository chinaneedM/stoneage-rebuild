"""Transient original empty-equipment ItemCrush and helper chronology audit.

Native Check/Seq, original legacy ItemCrush empty scan and original helper run
at clean pins. Equipped mutations trap; physical/status math is controlled.
Raw rand values are supplied, not a claim about any original libc generator.
"""
from __future__ import annotations

import argparse
from itertools import product
from pathlib import Path
import re
import subprocess
import tempfile

from tools.stoneage_guard_break2_source_audit import PINNED, LAYOUTS, _text, _sha, _function
from tools.stoneage_battlemodel_hit_lifecycle_source_audit import PREFIX
from tools.stoneage_battlemodel_source_audit import _normalized_identifier
from tools.stoneage_mdfyattack_source_audit import _definition
from tools.stoneage_battlemodel_itemcrush_model import (
    EmptyEquipmentParticipant, BattleModelItemCrushContext, resolve_empty_equipment_itemcrush,
    SOURCE_DEFAULT_ITEMCRUSH_RATE,
)

RAW_VALUES = (0,49,50,66,67,83,84,99,6,2**31-1)


def _body(text, name, argc):
    matches = re.finditer(r"\b(?:static\s+)?int\s+"+name+r"\s*\(([^;{}]*)\)\s*\{",text)
    matches = [m for m in matches if m.group(1).count(",")+1 == argc]
    if len(matches) != 1:
        raise ValueError("ambiguous exact ItemCrush definition "+name)
    return _function(text, matches[0].group(0)[:-1].rstrip())


def _context(name, variant, kind):
    participants = {0:EmptyEquipmentParticipant("player","player",10,(-1,)*5),
                    10:EmptyEquipmentParticipant("enemy","enemy",10,(-1,)*5)}
    count = 7 if "pet" in variant else 5
    participants[5] = EmptyEquipmentParticipant("pet","pet",10,(-1,)*count)
    participants[1] = EmptyEquipmentParticipant("guardian",kind,10,(-1,)*(count if kind=="pet" else 5))
    return BattleModelItemCrushContext(name, variant, SOURCE_DEFAULT_ITEMCRUSH_RATE,2**31-1,participants)


def cases():
    standalone = [(0,k,100,0,4,1,-1,c,r) for k,c,r in product((1,2,3),(9,10),RAW_VALUES)]
    helper = [(1,k,hp,dmg,ret,live,g,c,RAW_VALUES[i%len(RAW_VALUES)])
        for i,(k,hp,dmg,ret,live,g,c) in enumerate(product((1,2),(5,100),(0,10),
            (1,2,3,4,5),(0,1),(-1,1),(9,10)))]
    return tuple(standalone+helper)


EXTRA = r'''
#define CHAR_TYPEENEMY 3
#define CHAR_LV 3
#define arraysizeof(a) (sizeof(a)/sizeof((a)[0]))
static int gItemCrushRate=400000;
static char *aszCrushTbl[]={"unreachable","unreachable"};
static int checkroll,rawvalue,checkcount,rawcount,deathcount,phase,crushphase,statusphase;
static int lookupcount,lookups[32][2],native_target;
static char szBadStatusString[256];
void mutation_trap(void){fprintf(stderr,"unexpected equipped mutation\n");exit(96);}
#define ITEM_setInt(...) mutation_trap()
#define ITEM_setChar(...) mutation_trap()
#define LogItem(...) mutation_trap()
#define CHAR_sendItemDataOne(...) mutation_trap()
#define CHAR_complianceParameter(...) mutation_trap()
#define CHAR_send_P_StatusString(...) mutation_trap()
#define CHAR_getChar(...) "unreachable"
#define ITEM_getChar(...) "unreachable"
#define CHAR_getUseName(...) "unreachable"
int CHAR_getItemIndex(int c,int slot){
 if(lookupcount>=32)exit(97);
 lookups[lookupcount][0]=c;lookups[lookupcount++][1]=slot;return -1;
}
int ITEM_CHECKINDEX(int i){return 0;}
int ITEM_getInt(int i,int p){mutation_trap();return 0;}
int owned_raw_rand(void){rawcount++;crushphase=++phase;return rawvalue;}
#define rand owned_raw_rand
int BATTLE_ItemCrushCheck(int c
#ifdef _TAKE_ITEMDAMAGE
,int flg
#endif
);
static int BATTLE_ItemCrushSeq(
#ifdef _TAKE_ITEMDAMAGE
int a,int d,int damage
#else
int d
#endif
);
'''

MAIN = r'''
int main(void){
 int mode,kind,hp,dmg,ret,live,g;
 while(scanf("%d%d%d%d%d%d%d%d%d",&mode,&kind,&hp,&dmg,&ret,&live,&g,&checkroll,&rawvalue)==9){
  memset(stats,0,sizeof(stats));memset(works,0,sizeof(works));memset(BattleArray,0,sizeof(BattleArray));
  for(int i=0;i<16;i++)StatusTbl[i]=i+4;
  for(int i=0;i<20;i++){stats[i][CHAR_HP]=hp;stats[i][CHAR_LV]=10;stats[i][CHAR_WHICHTYPE]=CHAR_TYPEPLAYER;}
  stats[10][CHAR_WHICHTYPE]=CHAR_TYPEENEMY;
  native_target=kind==CHAR_TYPEPET?5:0;
  stats[native_target][CHAR_WHICHTYPE]=kind;stats[1][CHAR_WHICHTYPE]=kind;
  target_live=live;guardian_live=1;seq_state=ret;seq_damage=dmg;seq_guardian=g;
  reaction=0;status_hit=0;gDamageDiv=0;damage_roll=49;
  checkcount=rawcount=deathcount=phase=crushphase=statusphase=lookupcount=status_calls=0;
  int result=0;
  if(mode==0){
#ifdef _TAKE_ITEMDAMAGE
   result=BATTLE_ItemCrushSeq(10,native_target,dmg);
#else
   result=BATTLE_ItemCrushSeq(native_target);
#endif
  }else{
   AttackObject object={0,native_target,123};
   BATTLE_BattleModel_ATTACK(0,10,&object,2,1,30,5);
  }
  printf("%d %d %d %d %d %d %d %d",result,checkcount,rawcount,deathcount,status_calls,crushphase,statusphase,lookupcount);
  for(int i=0;i<lookupcount;i++)printf(" %d %d",lookups[i][0],lookups[i][1]);printf("\n");
 }
 return 0;
}
'''


def analyze_profile(name, root):
    root=root.resolve()
    sha=subprocess.check_output(["git","-C",str(root),"rev-parse","HEAD"],text=True).strip()
    dirty=subprocess.check_output(["git","-C",str(root),"status","--porcelain"],text=True).strip()
    if sha!=PINNED[name] or dirty:
        raise ValueError("pinned source commit/tree drift")
    event=root/LAYOUTS[name]/"battle/battle_event.c"
    battle=root/LAYOUTS[name]/"battle/battle.c"
    header=root/LAYOUTS[name]/"include/char_base.h"
    source=_text(event)
    rate=re.search(r"\bgItemCrushRate\s*=\s*(\d+)\s*;",_text(battle))
    if not rate or int(rate.group(1))!=SOURCE_DEFAULT_ITEMCRUSH_RATE:
        raise ValueError("source default ItemCrush rate drift")
    equipenum=re.search(r"typedef\s+enum\s*\{[^{}]*\bCHAR_EQUIPPLACENUM\b[^{}]*\}\s*CHAR_EquipPlace\s*;",_text(header),re.S)
    if not equipenum:
        raise ValueError("missing original reduced equipment enum")
    petenum = re.search(r"typedef\s+enum\s*\{[^{}]*\bCHAR_PETITEMNUM\b[^{}]*\}\s*CHAR_petitem\s*;",_text(header),re.S)
    prefix=PREFIX.replace("int BATTLE_ItemCrushSeq(int d){crush_calls++;return 0;}","")
    prefix=prefix.replace("if(n==0)return target_live;","if(n==native_target)return target_live;")
    # Native target declaration must precede the controlled TargetCheck stub.
    prefix=prefix.replace("int BATTLE_TargetCheck", "static int native_target;\nint BATTLE_TargetCheck",1)
    prefix=prefix.replace("int RAND(int lo,int hi){rng_calls++;if(lo!=1||hi!=100)exit(95);return damage_roll;}",
        "int RAND(int lo,int hi);" )
    prefix=prefix.replace("status_calls++;", "status_calls++;statusphase=++phase;",1)
    prefix=prefix.replace("static int sentinel,protocol_calls,crush_calls;",
        "static int sentinel,protocol_calls,crush_calls;\nstatic int phase,statusphase;")
    extra=EXTRA.replace(",phase,crushphase,statusphase;",",crushphase;").replace(",native_target;",";")
    extra+='''\nint RAND(int lo,int hi){
 if(lo==1&&hi==gItemCrushRate){checkcount++;crushphase=++phase;return checkroll;}
 if(lo==1&&hi==100){deathcount++;phase++;return damage_roll;}
 fprintf(stderr,"unexpected equipment RAND %d %d\\n",lo,hi);exit(98);
}\n'''
    variants=("legacy","take_itemdamage") if name!="bismarck" else (
        "legacy","take_itemdamage","take_itemdamage_fix","take_itemdamage_pet","take_itemdamage_pet_fix")
    allcases=cases()
    count=0
    for variant in variants:
        take=variant!="legacy"
        bodies=[_body(source,"BATTLE_ItemCrushCheck",2 if take else 1)]
        if take:
            bodies.append("int BATTLE_ItemCrush(int a,int slot,int damage,int flg){mutation_trap();return 0;}")
        else:
            bodies.append(_body(source,"BATTLE_ItemCrush",1))
        bodies.append(_body(source,"BATTLE_ItemCrushSeq",3 if take else 1))
        bodies.append(_normalized_identifier(_definition(source,"BATTLE_BattleModel_ATTACK")))
        text="\n".join(bodies)
        names=set(re.findall(r"\b(?:CHAR|ITEM|BREAK)_[A-Z][A-Z0-9_]*\b",text))
        supplied=set(re.findall(r"\b(?:CHAR|ITEM)_[A-Z][A-Z0-9_]*\b",prefix+extra+equipenum.group(0)+(petenum.group(0) if petenum else "")))
        constants="\n".join(f'#define {n} "unreachable"' if n.startswith("BREAK_") else f"#define {n} {i+20}"
                            for i,n in enumerate(sorted(names-supplied)))
        macros=("#define _TAKE_ITEMDAMAGE\n" if take else "")
        if "pet" in variant: macros+="#define _TAKE_ITEMDAMAGE_FOR_PET\n"
        if "fix" in variant: macros+="#define _TAKE_ITEMDAMAGE_FIX\n"
        with tempfile.TemporaryDirectory(prefix="sa-itemcrush-") as folder:
            c, binary=Path(folder)/"oracle.c",Path(folder)/"oracle"
            c.write_text(macros+constants+"\n"+equipenum.group(0)+"\n"+(petenum.group(0) if petenum else "")+
                "\n"+prefix+extra+text+MAIN)
            result=subprocess.run(["cc","-std=c99","-O0",str(c),"-o",str(binary)],text=True,capture_output=True)
            if result.returncode:
                raise ValueError("ItemCrush native compile failed: "+result.stderr[-5000:])
            rows=subprocess.check_output([str(binary)],input="".join(" ".join(map(str,v))+"\n" for v in allcases),text=True).splitlines()
        if len(rows)!=len(allcases):raise ValueError("native ItemCrush row count drift")
        for index,(v,row) in enumerate(zip(allcases,rows)):
            mode,kind,hp,dmg,ret,live,g,checkroll,raw=v
            target=5 if kind==2 else 0
            actual=1 if mode and g==1 else target
            survives=hp-(0 if ret==3 else dmg)>0
            reached=not mode or (live and survives)
            death=int(bool(mode and live and not survives and kind!=1 and ret==5))
            status=int(bool(mode and live and survives and dmg>0 and ret not in (2,3)))
            check=rawcalls=0; lookups=[]
            if reached:
                ctx=_context(name,variant,{1:"player",2:"pet",3:"enemy"}[kind])
                if mode==0 and kind==3:
                    ctx=BattleModelItemCrushContext(name,variant,400000,2**31-1,
                        {**ctx.participants,0:EmptyEquipmentParticipant("enemy-target","enemy",10,(-1,)*5)})
                def owned(owner,low,high):
                    nonlocal check,rawcalls
                    if owner=="itemcrush_check":check+=1;return checkroll
                    if owner=="itemcrush_raw_rand":rawcalls+=1;return raw
                    raise ValueError("unexpected ItemCrush owner")
                resolved=resolve_empty_equipment_itemcrush(ctx,actor_slot=10,defender_slot=actual,take=owned)
                lookups=[(actual,s) for s in resolved.defender_lookup_slots]
                if resolved.attacker_weapon_looked_up:lookups.append((10,2))
            crushphase=int(bool(check or rawcalls))
            statusphase=(crushphase+1) if status else 0
            expected=(0,check,rawcalls,death,status,crushphase,statusphase,len(lookups),
                      *(i for pair in lookups for i in pair))
            native=tuple(map(int,row.split()))
            if native!=expected:
                raise ValueError(f"ItemCrush mismatch {name}/{variant}/{index} {v}: {native} != {expected}")
            count+=1
    return count,len(variants),{"event":_sha(event),"battle":_sha(battle),"char_base":_sha(header)}


def main():
    parser=argparse.ArgumentParser()
    for name in PINNED:parser.add_argument("--"+name+"-dir",required=True,type=Path)
    args=parser.parse_args()
    print("StoneAge equipment-free ItemCrush native chronology")
    total=0
    for name in PINNED:
        count,variants,hashes=analyze_profile(name,getattr(args,name+"_dir"));total+=count
        print(f"PROFILE|profile={name}|sha={PINNED[name]}|variants={variants}|itemcrush_model_native_comparisons={count}")
        for file,digest in hashes.items():print(f"SOURCE|profile={name}|file={file}|sha256={digest}")
    print(f"TOTAL|itemcrush_model_native_comparisons={total}|source_default_rate=400000")
    print("FACT|surviving_DODGE_MISS_ALLGUARD_zero_damage_reach_ItemCrush;actual_Guardian_precedes_status;empty_equipment_still_owns_checks")
    print("BOUNDARY|declared_reduced5_pet7_feature_variants;controlled_physical_status_and_libc_values;equipped_mutation_original_build_full_runtime_OPEN")
    print("RESOLUTION|BATTLEMODEL_EMPTY_EQUIPMENT_ITEMCRUSH_NATIVE_CHRONOLOGY_PASS")


if __name__=="__main__":main()
