"""Pinned Combined direct-magic MP boundary and transient native witnesses.

Only source hashes, checked facts and witness counts are emitted. Native
tests execute the original accessor, DirectUse and four ordinary wrappers;
battle effects are explicit stubs, so this does not close effect execution.
"""
import argparse
import itertools
import os
from pathlib import Path
import re
import subprocess
import tempfile

from tools.stoneage_guard_break2_source_audit import PINNED, LAYOUTS, _sha, _text
from tools.stoneage_mdfyattack_source_audit import _definition, _strip
from tools.stoneage_weaken_source_audit import _preprocess, _array
from tools.stoneage_combined_source_audit import _normalize as _base_normalize
from tools.stoneage_combined_direct_magic_model import (
    EFFECTS, RuntimeItemZeroWitness, resolve_combined_direct_magic_route,
)

WRAPPERS = ("MAGIC_Recovery", "MAGIC_StatusChange", "MAGIC_StatusRecovery", "MAGIC_AttReverse")


def _normalize(text):
    return _base_normalize(text).replace("to_charaindex", "toindex")


def _native(source):
    # These constants/accessors are declared test seams, not historical enums.
    prefix = r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#define TRUE 1
#define FALSE 0
#define CHAR_TYPEPLAYER 1
#define CHAR_WHICHTYPE 0
#define CHAR_MP 1
#define CHAR_FMINDEX 2
#define CHAR_FMSPRITE 3
#define CHAR_FLOOR 4
#define CHAR_WORKNOCAST 0
#define CHAR_WORKBATTLEMODE 1
#define CHAR_WORKBATTLEINDEX 2
#define CHAR_COLORYELLOW 0
#define CHAR_COLORWHITE 0
#define BATTLE_CHARMODE_INIT 0
#define BATTLE_TYPE_P_vs_P 2
#define ITEM_MAGICUSEMP 0
#define MAGIC_FUNCNAME 0
#define MP_RATE 0.7
typedef int ITEM_DATAINT;
typedef int ITEM_DATA_ENUM;
typedef int (*MAGIC_CALLFUNC)(int,int,int,int);
int MAGIC_Recovery(int,int,int,int);
int MAGIC_StatusChange(int,int,int,int);
int MAGIC_StatusRecovery(int,int,int,int);
int MAGIC_AttReverse(int,int,int,int);
static struct {struct {int data[1];} itm;} ITEM_item[1];
static struct {struct {int data[1];} item;} ITEM_gExists[1];
static struct {int type;} BattleArray[1];
static int mp_now,valid,init,nocast,item_valid,known,helper_ret,effect_id;
static int item_reads,wrapper_calls,effect_calls,mp_arg;
int ITEM_CHECKINDEX(int index){item_reads++;return index==0&&item_valid;}
int ITEM_CHECKINTDATAINDEX(int element){return element==0;}
int CHAR_CHECKINDEX(int index){wrapper_calls++;return valid;}
int CHAR_getInt(int index,int field){if(field==CHAR_MP)return mp_now;return 0;}
void CHAR_setInt(int index,int field,int value){if(field==CHAR_MP)mp_now=value;}
int CHAR_getWorkInt(int index,int field){if(field==CHAR_WORKNOCAST)return nocast;
 if(field==CHAR_WORKBATTLEMODE)return init?0:1;return 0;}
int IsBATTLING(int index){return 1;}
void CHAR_talkToCli(int a,int b,const char*c,int d){}
int CHAR_getItemIndex(int a,int b){abort();}
int BATTLE_CheckSameSide(int a,int b){abort();}
int BATTLE_Index2No(int a,int b){return 0;}
void BATTLE_NoAction(int a,int b){abort();}
int print(const char *fmt,...){return 0;}
int getNoMagicMap(int i){return -1;}
void strncpysafe(char *out,size_t n,const char *in){snprintf(out,n,"%s",in);}
int MAGIC_getMagicArray(int magic){return magic;}
char *MAGIC_getChar(int array,int field){return "witness";}
MAGIC_CALLFUNC MAGIC_getMagicFuncPointer(char *token){
 MAGIC_CALLFUNC funcs[]={MAGIC_Recovery,MAGIC_StatusChange,MAGIC_StatusRecovery,MAGIC_AttReverse};
 return known?funcs[effect_id]:NULL;}
int seam(int mp){effect_calls++;mp_arg=mp;return helper_ret;}
int MAGIC_Recovery_Battle(int a,int b,int c,int mp){return seam(mp);}
int MAGIC_Recovery_Field(int a,int b){abort();}
int MAGIC_StatusChange_Battle(int a,int b,int c,int mp){return seam(mp);}
int MAGIC_StatusRecovery_Battle(int a,int b,int c,int mp){return seam(mp);}
int MAGIC_AttReverse_Battle(int a,int b,int c,int mp){return seam(mp);}
int _ITEM_getInt(char*,int,int,ITEM_DATAINT);
#define ITEM_getInt(i,e) _ITEM_getInt(__FILE__,__LINE__,i,e)
'''
    main = r'''
int main(void){int value,to;
 while(scanf("%d%d%d%d%d%d%d%d%d%d",&effect_id,&mp_now,&item_valid,&value,
             &valid,&init,&nocast,&known,&helper_ret,&to)==10){
  ITEM_item[0].itm.data[0]=ITEM_gExists[0].item.data[0]=value;
  item_reads=wrapper_calls=effect_calls=0;mp_arg=999999;
  int ret=MAGIC_DirectUse(0,100,to,0);
  printf("%d %d %d %d %d %d\n",ret,mp_now,item_reads,wrapper_calls,effect_calls,mp_arg);
 }
 return 0;
}
'''
    cases = []
    expected = []
    flags = ((1,0,0,1), (0,0,0,1), (1,1,0,1), (1,0,1,1), (1,0,0,0))
    for index, item, mp, flag, helper, target in itertools.product(
        range(4), (None, -3, 0, 3, 8), (0, 2, 8, 20), flags, (False, True), (0, 22)
    ):
        valid, init, nocast, known = flag
        witness = RuntimeItemZeroWitness(False) if item is None else RuntimeItemZeroWitness(True,item)
        out = resolve_combined_direct_magic_route(
            effect=EFFECTS[index], current_mp=mp, item_zero=witness,
            caster_valid=bool(valid), battle_mode_init=bool(init), nocast=nocast,
            function_present=bool(known), battle_effect_return=helper, target_slot=target,
        )
        cases.append(" ".join(map(str,(index,mp,int(item is not None),item or 0,*flag,int(helper),target))))
        expected.append(" ".join(map(str,(int(out.accepted),out.remaining_mp,out.item_reads,
            out.wrapper_calls,out.battle_effect_calls,out.mp_argument if out.battle_effect_calls else 999999))))
    with tempfile.TemporaryDirectory() as directory:
        p = Path(directory)
        src = p/"witness.c"
        src.write_text(prefix+source+main)
        exe = p/"witness"
        subprocess.run(["cc","-std=c11","-w","-fsanitize=address,undefined",
            "-fno-sanitize-recover=all","-fno-pie","-no-pie",str(src),"-o",str(exe)],
            check=True,capture_output=True,text=True)
        run = subprocess.run([str(exe)],input="\n".join(cases)+"\n",
            capture_output=True,text=True,env=dict(os.environ,ASAN_OPTIONS="detect_leaks=0"))
        if run.returncode:
            raise ValueError("native wrapper witness failed: "+run.stderr[-1500:])
        actual = run.stdout.splitlines()
        if actual != expected:
            first = next((i for i,(a,b) in enumerate(zip(actual,expected)) if a!=b),min(len(actual),len(expected)))
            raise ValueError(f"native wrapper mismatch at {first}: {actual[first:first+1]} vs {expected[first:first+1]}")
    return len(cases)


def analyze_profile(profile, root):
    root = Path(root).resolve()
    if subprocess.check_output(["git","-C",str(root),"rev-parse","HEAD"],text=True).strip()!=PINNED[profile]:
        raise ValueError("source pin drift")
    if subprocess.check_output(["git","-C",str(root),"status","--porcelain"],text=True).strip():
        raise ValueError("source tree drift")
    base = root/LAYOUTS[profile]
    paths = {key:base/value for key,value in {
        "magic":"magic/magic.c", "item":"item/item.c", "pet":"battle/pet_skill.c",
        "battle_magic":"battle/battle_magic.c", "event":"battle/battle_event.c",
        "version":"include/version.h",
    }.items()}
    data = {key:_text(path) for key,path in paths.items()}
    includes = ["-I",str(base/"include")]
    if profile=="bismarck":
        includes += ["-I",str(root/"server/common"),"-I",str(root/"shared/lua51")]
    direct = _definition(data["magic"],"MAGIC_DirectUse")
    wrappers = [_definition(data["magic"],name) for name in WRAPPERS]
    getter = _definition(data["item"],"_ITEM_getInt")
    check = _normalize(_strip(_definition(data["item"],"_ITEM_CHECKINDEX")))
    callback = _normalize(_strip(_definition(data["pet"],"PETSKILL_Combined")))
    source = _preprocess("\n".join([direct,*wrappers,getter]),includes,paths["version"])
    compact = _normalize(_strip(source))
    function_compacts = {name:_normalize(_strip(_definition(source,name))) for name in WRAPPERS}
    native_direct = _normalize(_strip(_definition(source,"MAGIC_DirectUse")))
    labels = len(re.findall(r'"[^\"]*"',_array(data["event"],"aszStatus")))
    gates = {
        "combined_clears_high_item_index": "CHAR_SETWORKINT_HIGH(charaindex,CHAR_WORKBATTLECOM3,0);" in callback,
        "combined_selection_draw_in_callback": "kill[rand()%count]" in callback,
        "nonplayer_itemnum_is_runtime_index": "else{itemindex=itemnum;}" in native_direct,
        "nocast_precedes_item_read": native_direct.index("CHAR_WORKNOCAST") < native_direct.index("ITEM_getInt("),
        "negative_item_mp_not_clamped": "if((mp=ITEM_getInt(itemindex,ITEM_MAGICUSEMP))<0){}" in native_direct,
        "direct_forwards_mp_to_wrapper": "ret=func(charaindex,toindex,marray,mp);" in native_direct,
        "invalid_item_accessor_returns_minus_one": "if(!ITEM_CHECKINDEX(index)){return-1;}" in compact,
        "item_validity_requires_live_use":
            ("ITEM_gExists" if profile=="bismarck" else "ITEM_item")+"[index].use==FALSE" in check,
        "all_wrappers_compare_and_deduct_mp": all(
            "CHAR_getInt(charaindex,CHAR_MP)<mp" in fn and
            "CHAR_getInt(charaindex,CHAR_MP)-mp" in fn for fn in function_compacts.values()),
        "recovery_all_rejected_after_deduction":
            function_compacts["MAGIC_Recovery"].index("CHAR_MP)-mp") < function_compacts["MAGIC_Recovery"].index("toindex==22"),
        "recovery_discards_battle_return": "returnMAGIC_Recovery_Battle(" not in function_compacts["MAGIC_Recovery"],
        "other_wrappers_propagate_battle_return": all(
            "return"+name+"_Battle(" in function_compacts[name] for name in WRAPPERS[1:]),
        "family_mp_rate_is_0_7": bool(re.search(r"#define\s+MP_RATE\s+0\.7\b",data["magic"])),
    }
    if not all(gates.values()):
        raise ValueError(f"{profile} direct-magic gate failure: {[k for k,v in gates.items() if not v]}")
    # Normalize variable spelling solely in the transient compile seam.
    source = source.replace("from_char_index","charaindex").replace("from_charaindex","charaindex").replace("char_index","charaindex").replace("to_char_index","toindex").replace("to_charaindex","toindex")
    return dict(profile=profile,sha=PINNED[profile],gates=gates,
        hashes={key:_sha(path) for key,path in paths.items()},
        native_cases=_native(source),status_label_count=labels)


def emit(rows):
    print("StoneAge Combined direct-magic MP boundary audit — R1")
    print("Original source is compiled transiently; only derived facts/hashes are stored.")
    for row in rows:
        print(f"PROFILE|name={row['profile']}|sha={row['sha']}|status_labels={row['status_label_count']}")
        for key,value in sorted(row["gates"].items()):
            print(f"GATE|profile={row['profile']}|name={key}|pass={int(value)}")
        print(f"NATIVE|profile={row['profile']}|defined_cases={row['native_cases']}|asan_ubsan_pass=1|battle_effects=stubbed")
        for key,value in sorted(row["hashes"].items()):
            print(f"SOURCE_SHA256|profile={row['profile']}|file={key}|sha256={value}")
    print("FACT|Combined_HIGH_COM3_zero_becomes_nonplayer_runtime_item_index_zero")
    print("FACT|ordinary_wrappers_use_forwarded_item_MP_for_comparison_and_deduction")
    print("FACT|witnessed_invalid_runtime_item_zero_accessor_minus1_can_increase_MP_by1")
    print("FACT|selection_draw_owned_by_callback_before_DirectUse_Nocast_gate")
    print("FACT|Recovery_returns_true_after_battle_helper_failure_except_all_target_rejection")
    print("BOUNDARY|runtime_item_pool_zero_state_not_proven_by_recovered_item_configuration")
    print("BOUNDARY|native_effects_stubbed_no_target_status_HP_or_attribute_mutation_claim")
    print("BOUNDARY|status_OPTION_execution_charset_and_safe_table_scan_still_require_actual_byte_audit")
    print("BOUNDARY|family_MP_modifiers_field_route_and_original_binary_profile_open")
    print("RESOLUTION|COMBINED_DIRECT_MAGIC_MP_BOUNDARY_CLOSED_CONDITIONAL_ITEM_STATE")
    print("RESOLUTION|RECOVERED25_COMBINED_ORDERED_RUNTIME_OPEN")


def main():
    parser=argparse.ArgumentParser()
    for name in PINNED:
        parser.add_argument("--"+name+"-dir",type=Path,required=True)
    args=parser.parse_args()
    emit([analyze_profile(name,getattr(args,name+"_dir")) for name in PINNED])


if __name__=="__main__":
    main()
