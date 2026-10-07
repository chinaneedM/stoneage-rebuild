"""Transient original-C BecomePig witnesses, with explicit undefined-domain exclusion."""
from __future__ import annotations

import argparse
import hashlib
import itertools
from pathlib import Path
import re
import subprocess
import tempfile

from tools.stoneage_becomepig_preaudit import analyze_profile as source_audit, postattack_block
from tools.stoneage_guard_break2_source_audit import PINNED, LAYOUTS, _text, _function, _compact
from tools.stoneage_mdfyattack_source_audit import _definition, _strip
from tools.stoneage_recovered25_becomepig_probe import (
    analyze_runtime_objects, EXPECTED_PETSKILL_SHA256, EXPECTED_ENEMYBASE_SHA256,
)
from tools.stoneage_recovered25_petskill_runtime import load_recovered25_petskill_runtime
from tools.stoneage_recovered25_enemybase_runtime import (
    load_recovered25_enemybase_runtime, _active_enemybase_path,
)

INT_MIN = -(2**31)
INT_MAX = 2**31-1
SENTINEL = -123456789
EXPECTED_NATIVE_OPTIONS = {
    "gavin": ((628,-1,False,None,None,None),(631,2,True,30,180,100250),(635,3,True,30,180,100388)),
    "iris": ((628,-1,False,None,None,None),(631,2,True,30,180,100250),(635,3,True,30,180,100388)),
    "bismarck": ((628,-1,False,30,60,100250),(631,2,True,30,60,100250),(635,3,True,30,60,100250)),
}


def check_native_option_identities(name, rows):
    observed = tuple(tuple(row[key] for key in ("id","conversions","initialized_rate_time",
                     "effective_rate","effective_time","effective_image")) for row in rows)
    if observed != EXPECTED_NATIVE_OPTIONS[name]:
        raise ValueError("actual native conversion/effective profile identity drift")


def checked_decimal_prefix(raw: bytes) -> tuple[int, ...]:
    """Determine safe decimal conversion domains before invoking native sscanf.

    This is a safety check/oracle for three %d conversions, not a replacement
    for the source parser. Native conversion counts must independently agree.
    """
    if not raw.isascii() or b"\0" in raw or len(raw) >= 256:
        raise ValueError("unsupported native OPTION byte domain")
    text = raw.decode("ascii")
    values = []
    for _ in range(3):
        text = text.lstrip(" \t\r\n\v\f")
        match = re.match(r"[+-]?[0-9]+", text)
        if match is None:
            break
        value = int(match.group(), 10)
        if not INT_MIN <= value <= INT_MAX:
            raise ValueError("native decimal conversion overflow domain excluded")
        values.append(value)
        text = text[match.end():]
    return tuple(values)


def _if_with(source: str, pattern: str, required: str) -> str:
    matches = []
    for m in re.finditer(pattern, source):
        block = _function(source[m.start():], m.group())
        if required in _compact(_strip(block)):
            matches.append(block)
    if len(matches) != 1:
        raise ValueError("expected one isolated original conditional")
    return matches[0]


def _features(name: str, root: Path) -> set[str]:
    base = root/LAYOUTS[name]
    includes = ["-I", str(base/"include")]
    if name == "bismarck":
        includes += ["-I", str(root/"server/common"), "-I", str(root/"shared/lua51")]
    out = subprocess.check_output(["cpp", "-dM", *includes, str(base/"include/version.h")], text=True)
    active = set(re.findall(r"^#define\s+(\w+)", out, re.M))
    required = {"_PETSKILL_BECOMEPIG"}
    if name != "bismarck":
        required |= {"_EQUIT_ARRANGE", "_PREVENT_TEAMATTACK"}
    if not required <= active or (name == "bismarck" and active & {"_EQUIT_ARRANGE", "_PREVENT_TEAMATTACK"}):
        raise ValueError("default-header feature profile drift")
    return active


def _run_c(source: str, payload: str, *, optimization: str) -> list[tuple[int, ...]]:
    with tempfile.TemporaryDirectory(prefix="sa-becomepig-native-") as directory:
        c = Path(directory)/"oracle.c"
        exe = Path(directory)/"oracle"
        c.write_text(source)
        result = subprocess.run(
            ["cc", "-std=c99", optimization, "-fsanitize=undefined",
             "-fno-sanitize-recover=all", str(c), "-o", str(exe)],
            text=True, capture_output=True,
        )
        if result.returncode:
            raise ValueError("isolated original-C compile failed: "+result.stderr[-2500:])
        result = subprocess.run([str(exe)], input=payload, text=True, capture_output=True)
        if result.returncode or result.stderr:
            raise ValueError("isolated original-C execution/UBSan failed: "+result.stderr[-1200:])
        return [tuple(map(int, line.split())) for line in result.stdout.splitlines()]


def _assert_rows(got, expected, label):
    if got != expected:
        for i, (a, b) in enumerate(zip(got, expected)):
            if a != b:
                raise ValueError(f"{label} mismatch at witness {i}: {a} != {b}")
        raise ValueError(label+" native output length mismatch")


def _post_source(name: str, root: Path, active: set[str]) -> str:
    base = root/LAYOUTS[name]
    pet = _text(base/"battle/pet_skill.c")
    battle = _text(base/"battle/battle.c")
    callback = _definition(pet, "PETSKILL_BecomePig")
    getter = _definition(pet, "PETSKILL_getChar")
    block = postattack_block(battle)
    macros = []
    header = _text(base/"include/battle.h")
    for symbol in ("CHAR_GETWORKINT_LOW", "CHAR_SETWORKINT_LOW"):
        match = re.search(r"^\s*#define\s+"+symbol+r"(?:[^\n]*\\\n)*[^\n]*", header, re.M)
        if match is None:
            raise ValueError("packed low-array macro missing")
        macros.append(match.group())
    parse = re.search(r'if\s*\(\s*pszOption[^)]*\)\s*sscanf\s*\([^;]+;\s*else\s*petrate\s*=[^;]+;', block)
    if parse is None:
        raise ValueError("original OPTION branch missing")
    prefix = r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define TRUE 1
#define SIDE_OFFSET 10
#define BATTLE_COM_S_BECOMEPIG 100
#define BATTLE_CHARMODE_C_OK 9
#define BATTLE_RET_MISS 1
#define BATTLE_RET_DODGE 2
#define BATTLE_RET_ALLGUARD 3
#define BATTLE_RET_ARRANGE 4
#define CHAR_TYPEPLAYER 1
#define CHAR_WHICHTYPE 0
#define CHAR_BECOMEPIG 1
#define CHAR_BECOMEPIG_BBI 2
#define CHAR_RIDEPET 3
#define CHAR_BASEIMAGENUMBER 4
#define CHAR_WORKBATTLECOM1 0
#define CHAR_WORKBATTLECOM2 1
#define CHAR_WORKBATTLEMODE 2
#define CHAR_WORKBATTLECOM3 3
#define CHAR_WORKITEMMETAMO 4
#define CHAR_WORKNPCMETAMO 5
#define CHAR_WORKFOXROUND 6
#define CHAR_WORKPETFALL 7
#define CHAR_NAME 0
#define CHAR_COLORYELLOW 1
#define PETSKILL_OPTION 0
typedef int PETSKILL_DATACHAR;
typedef struct {struct {char string[256];} string[1];} Petskill;
static Petskill PETSKILL_petskill[1];
static struct {int Battle_Attack_ReturnData;} Battle_Attack_ReturnData_x;
static int actor[8], ints[8], works[8];
static int g_alive,g_same,g_draw;
static int targets,types,sides,counters,indexchecks,draws,magic,ridemoves,talks;
static int check_index(int i){indexchecks++;return i==0;}
#define PETSKILL_CHECKINDEX(i) check_index(i)
#define PETSKILL_CHECKCHARDATAINDEX(i) ((i)==0)
int CHAR_getWorkInt(int i,int f){return i==10?actor[f]:works[f];}
void CHAR_setWorkInt(int i,int f,int v){if(i==10)actor[f]=v;else works[f]=v;}
int CHAR_getInt(int i,int f){(void)i;if(f==CHAR_WHICHTYPE)types++;if(f==CHAR_BECOMEPIG)counters++;return ints[f];}
void CHAR_setInt(int i,int f,int v){(void)i;ints[f]=v;}
int BATTLE_TargetCheck(int b,int d){(void)b;(void)d;targets++;return g_alive;}
int BATTLE_No2Index(int b,int d){(void)b;return d;}
int BATTLE_CheckSameSide(int a,int d){(void)a;(void)d;sides++;return g_same;}
int harness_rand(void){draws++;return g_draw;}
#define rand harness_rand
void BATTLE_MultiList(int b,int d,int *l){(void)b;(void)d;l[0]=-1;}
void BATTLE_MagicEffect(int b,int d,int *l,int a,int c){(void)b;(void)d;(void)l;if(a!=101120||c!=101750)abort();magic++;}
void BATTLE_changeRideImage(int i){(void)i;ridemoves++;}
char *CHAR_getChar(int i,int f){(void)i;(void)f;return "native-target";}
void CHAR_talkToCli(int i,int a,const char *s,int c){(void)i;(void)a;(void)s;(void)c;talks++;}
int print(const char *s,...){(void)s;return 0;}
'''
    prefix += "\n"+"\n".join("#define "+x for x in ("_EQUIT_ARRANGE", "_PREVENT_TEAMATTACK") if x in active)
    prefix += "\n"+"\n".join(macros)+"\n"+getter+"\n"+callback
    source = prefix+r'''
static void parse_probe(void){
 char *pszOption=PETSKILL_getChar(0,PETSKILL_OPTION);
 int petrate=-123456789,pettime=-123456789,pigbbi=100250;
 int a=-123456789,b=-123456789,c=100250;
 int count=sscanf(pszOption,"%d%d%d",&a,&b,&c);
'''+parse.group()+r'''
 printf("%d %d %d %d %d %d %d %d\n",count,a,b,c,petrate,pettime,pigbbi,(pszOption=="\0"));
}
static void callback_probe(int target,int array){
 memset(actor,0,sizeof(actor));actor[3]=0x12340000;
 int result=PETSKILL_BecomePig(10,target,array,NULL);
 printf("%d %d %d %d %d\n",result,actor[0],actor[1],actor[2],actor[3]);
}
static void one(int command,int result,int alive,int draw,int player,int same,int pig,int ride){
 int battleindex=0,defNo=5,charaindex=10;
 int COM=command?BATTLE_COM_S_BECOMEPIG:0;
 memset(actor,0,sizeof(actor));memset(ints,0,sizeof(ints));memset(works,0,sizeof(works));
 ints[0]=player?1:2;ints[1]=pig;ints[2]=999;ints[3]=ride;ints[4]=777;
 works[4]=7;works[5]=8;works[6]=9;
 g_alive=alive;g_same=same;g_draw=draw;
 targets=types=sides=counters=indexchecks=draws=magic=ridemoves=talks=0;
 Battle_Attack_ReturnData_x.Battle_Attack_ReturnData=result;
'''+block+r'''
 printf("%d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d\n",
 targets,types,sides,counters,indexchecks,draws,magic,ridemoves,talks,
 ints[1],ints[2],ints[3],ints[4],works[4],works[5],works[6],works[7],actor[3]);
}
static int unhex(char c){if(c>='0'&&c<='9')return c-'0';return c-'a'+10;}
int main(void){
 int kind,a,b,c,d,e,f,g,h;
 char hex[512];
 while(scanf("%d",&kind)==1){
  if(kind==0){scanf("%511s",hex);size_t n=strcmp(hex,"-")==0?0:strlen(hex)/2;
   for(size_t i=0;i<n;i++)PETSKILL_petskill[0].string[0].string[i]=(char)(unhex(hex[2*i])*16+unhex(hex[2*i+1]));
   PETSKILL_petskill[0].string[0].string[n]=0;parse_probe();
  }else if(kind==1){if(scanf("%d%d%d%d%d%d%d%d",&a,&b,&c,&d,&e,&f,&g,&h)!=8)return 2;one(a,b,c,d,e,f,g,h);
  }else if(kind==2){if(scanf("%d%d",&a,&b)!=2)return 3;callback_probe(a,b);
  }else if(kind==3){char *bad=PETSKILL_getChar(-1,PETSKILL_OPTION);char *badfield=PETSKILL_getChar(0,1);
   printf("%d %d %d %d\n",bad==NULL,bad!=NULL&&bad[0]==0,badfield==NULL,badfield!=NULL&&badfield[0]==0);
  }else return 4;
 }
 return 0;
}
'''
    return source.replace("char_index", "charaindex")


def _post_expected(v, rate, duration, image, *, guarded):
    command,result,alive,draw,player,same,pig,ride = v
    eligible_command = command and result not in (1,2,3) and not (guarded and result==4)
    target = bool(eligible_command)
    types = bool(target and alive)
    sides = bool(types and player and guarded)
    pigread = bool(types and player and (not guarded or not same))
    eligible = bool(pigread and pig < 2000000000)
    success = bool(eligible and draw < rate)
    newpig = duration if pig==-1 else duration+pig
    if success and (not INT_MIN <= newpig <= INT_MAX or (pig==-1 and duration==INT_MAX)):
        raise ValueError("original signed addition overflow domain excluded")
    # The successful path reads compute and reads the counter again for its message.
    return (int(target),int(types),int(sides),int(pigread)+2*int(success),int(eligible),int(eligible),
            int(success),int(success and ride!=-1),int(success),
            newpig if success else pig,image if success else 999,-1 if success else ride,
            image if success else 777,0 if success else 7,0 if success else 8,
            -1 if success else 9,int(success and ride!=-1),0)


def audit_postattack(name: str, root: Path, options: dict[int, bytes]) -> dict:
    source_audit(name, root)
    active = _features(name, root)
    c = _post_source(name, root, active)
    guarded = name != "bismarck"
    callbacks = tuple(itertools.product((0,5,19,20), (0,1,65535,-1)))
    payload = "".join(f"2 {t} {a}\n" for t,a in callbacks)+"3\n"
    expected = [(1,100,t,9,0x12340000|(a&0xffff)) for t,a in callbacks]
    expected.append((0,1,0,1) if name=="bismarck" else (1,0,1,0))
    metadata = []
    casecount = 0
    excluded = []
    for skill_id, raw in sorted(options.items()):
        values = checked_decimal_prefix(raw)
        conversions = len(values) if values or raw.strip() else -1
        # The missing third conversion retains the separately initialized image.
        a = values[0] if len(values)>0 else SENTINEL
        b = values[1] if len(values)>1 else SENTINEL
        image = values[2] if len(values)>2 else 100250
        effective = (a,b,image) if guarded else (30,60,100250)
        payload += "0 "+(raw.hex() or "-")+"\n"
        expected.append((conversions,a,b,image,*effective,0))
        safe = not guarded or len(values)>=2
        metadata.append({"id":skill_id,"option_sha256":hashlib.sha256(raw).hexdigest(),
                         "conversions":conversions,"initialized_rate_time":len(values)>=2,
                         "effective_rate":effective[0] if safe else None,
                         "effective_time":effective[1] if safe else None,
                         "effective_image":effective[2] if safe else None})
        if not safe:
            excluded.append(skill_id)
            continue
        rate,duration,image = effective
        draws = tuple(sorted({0,99,max(0,min(99,rate-1)),max(0,min(99,rate))}))
        vectors = itertools.product((0,1),range(5),(0,1),draws,(0,1),(0,1),(-8,-2,-1,0,1,1999999999,2000000000),(-1,55))
        for vector in vectors:
            row = _post_expected(vector,rate,duration,image,guarded=guarded)
            payload += "1 "+" ".join(map(str,vector))+"\n"
            expected.append(row)
            casecount += 1
    for optimization in ("-O0", "-O2"):
        _assert_rows(_run_c(c,payload,optimization=optimization), expected, name+" postattack")
    return {"profile":name,"callback_cases":len(callbacks),"invalid_getter_probes":1,
            "postattack_cases_per_optimization":casecount,"optimizations":2,
            "excluded_underspecified_ids":tuple(excluded),"options":metadata,
            "arrange_same_side_guard_active":guarded}


def load_verified_options(data_dir: Path, setup: Path | None) -> dict[int, bytes]:
    pets = load_recovered25_petskill_runtime(data_dir=data_dir, setup=setup)
    enemies = load_recovered25_enemybase_runtime(data_dir=data_dir, setup=setup)
    for path, wanted in ((data_dir/pets.source_file,EXPECTED_PETSKILL_SHA256),
                         (_active_enemybase_path(data_dir,setup),EXPECTED_ENEMYBASE_SHA256)):
        if hashlib.sha256(path.read_bytes()).hexdigest()!=wanted:
            raise ValueError("verified actual-data whole-file identity drift")
    r = analyze_runtime_objects(pets,enemies)
    if not all(r[x+"_closed"] for x in ("positive_references","population","exact_rows","exact_templates")):
        raise ValueError("actual BecomePig row/OPTION/placement identity drift")
    return {i:bytes(pets.skills[i].option_bytes) for i in r["callback_ids"]}


def main():
    parser=argparse.ArgumentParser()
    for name in PINNED:
        parser.add_argument("--"+name+"-dir",type=Path,required=True)
    parser.add_argument("--data-dir",type=Path,required=True)
    parser.add_argument("--setup",type=Path)
    args=parser.parse_args()
    options=load_verified_options(args.data_dir,args.setup)
    total=0
    for name in PINNED:
        r=audit_postattack(name,getattr(args,name+"_dir").resolve(),options)
        check_native_option_identities(name,r["options"])
        total+=r["postattack_cases_per_optimization"]*r["optimizations"]
        print(f"PROFILE|name={name}|sha={PINNED[name]}|callback_cases={r['callback_cases']}|postattack_cases_per_optimization={r['postattack_cases_per_optimization']}|optimizations=2|guard_active={int(r['arrange_same_side_guard_active'])}")
        for row in r["options"]:
            print("NATIVE_OPTION|profile="+name+"|"+"|".join(f"{k}={int(v) if isinstance(v,bool) else v}" for k,v in row.items()))
        print(f"EXCLUDED|profile={name}|underspecified_postattack_ids="+",".join(map(str,r["excluded_underspecified_ids"])))
    print(f"TOTAL|postattack_native_comparisons={total}")
    print("BOUNDARY|exact_original_blocks_callbacks_getter_and_low_array_macros_transient_only")
    print("BOUNDARY|UBSan_O0_O2_controlled_rng_valid_row_buffers_no_uninitialized_read_or_signed_overflow_domain")
    print("OPEN|original_rng_enum_compiler_executable_ordered_round_world_clock_and_persistent_runtime")
    print("RESOLUTION|BECOMEPIG_BOUNDED_EXACT_POSTATTACK_NATIVE_PASS_ZERO_RUNTIME_PROMOTIONS")


if __name__=="__main__":
    main()
