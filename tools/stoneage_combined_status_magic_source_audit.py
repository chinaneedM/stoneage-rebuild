"""Transient actual-source ordinary status-magic parser comparisons.

Reports contain hashes/semantic values only. Full battle effect functions
are supplied collector seams; no ordered target/status mutation is claimed.
"""
import argparse
import hashlib
import os
from pathlib import Path
import re
import subprocess
import tempfile

from tools.stoneage_guard_break2_source_audit import PINNED,LAYOUTS,_sha,_text,_function
from tools.stoneage_mdfyattack_source_audit import _strip
from tools.stoneage_weaken_source_audit import _array,_preprocess,_enum_values
from tools.stoneage_combined_direct_magic_source_audit import _normalize
from tools.stoneage_refresh_model import _BASELINE,BUILD_CHARSETS,PROFILE_FACTS
from tools.stoneage_combined_status_magic_model import (
    STATUS_MAGIC_IDS,SUCCESS_MARKERS,CombinedStatusMagicDomain,parse_status_magic_option,
    validate_actual_outcomes,
)
from tools.stoneage_recovered25_combined_magic_probe import analyze as analyze_crosslinks
from tools.stoneage_magic_probe import parse as parse_magic


def _definition(text,name):
    # These definitions have comments between ')' and '{'.
    match=re.search(r"\bint\s+"+re.escape(name)+r"\s*\(",text)
    if match is None:
        raise ValueError("missing ordinary magic definition: "+name)
    return _function(text,match.group())


def _native(source,profile,charset,*,actual_options):
    prefix=r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define TRUE 1
#define FALSE 0
#define CHAR_WORKBATTLEINDEX 0
#define MAGIC_OPTION 0
#define MAGIC_EFFECT_USER 9
#define SPR_tyusya 1
#define SPR_hoshi 2
#define BATTLE_ST_NONE 0
static char *option;
static int calls,status_out,turn_out,success_out,effect_out;
char *MAGIC_getChar(int a,int b){return option;}
int CHAR_getWorkInt(int a,int b){return 0;}
int BATTLE_Index2No(int a,int b){return 0;}
void BATTLE_MultiStatusChange(int b,int a,int t,int s,int turn,int use,int effect,int success){
 calls++;status_out=s;turn_out=turn;success_out=success;effect_out=effect;}
void BATTLE_MultiStatusRecovery(int b,int a,int t,int s,int use,int effect){
 calls++;status_out=s;effect_out=effect;}
'''
    prefix+="#define BATTLE_ST_END "+str(PROFILE_FACTS[profile][0])+"\n"
    main=r'''
int main(void){char hex[8192];int kind;
 while(scanf("%d%8191s",&kind,hex)==2){
  option=NULL;
  if(strcmp(hex,"NULL")!=0){
   size_t n=strcmp(hex,"EMPTY")==0?0:strlen(hex)/2;
   option=malloc(n+1);if(!option)abort();
   for(size_t i=0;i<n;i++){unsigned v;if(sscanf(hex+2*i,"%2x",&v)!=1)abort();option[i]=(char)v;}
   option[n]=0;
  }
  calls=0;status_out=turn_out=success_out=effect_out=-1;
  int ret=kind?MAGIC_StatusChange_Battle(0,1,0,0):MAGIC_StatusRecovery_Battle(0,1,0,0);
  printf("%d %d %d %d %d %d\n",ret,calls,status_out,turn_out,success_out,effect_out);
  free(option);
 }
 return 0;
}
'''
    vectors=[("recovery",b""),("change",b"")]
    marker=SUCCESS_MARKERS[profile]
    for label in _BASELINE[profile]:
        vectors.append(("recovery",label.encode(charset)))
    for label in _BASELINE[profile][1:]:
        for suffix in (
            " turn=3 "+marker+"=75", " turn=x "+marker+"=x",
            " turn=0", " "+marker+"=99 turn=-2",
            " turn12 "+marker+"34", " turn=3x "+marker+"=50",
            " turn=3 "+marker+"=", " turn=3 "+marker+"45",
            " turn=3 "+marker+"=-7",
        ):
            vectors.append(("change",(label+suffix).encode(charset)))
    if profile=="bismarck":
        vectors += [("recovery",b"plain"),("change",b"plain"),
                    ("recovery",("x"+_BASELINE[profile][10]).encode(charset))]
    # Preclassify each recovered OPTION using the independent byte model.
    actual=[]
    for magic_id,raw in sorted(actual_options.items()):
        kind="recovery" if magic_id==61 else "change"
        try:
            out=parse_status_magic_option(raw,kind=kind,profile=profile,execution_charset=charset)
        except CombinedStatusMagicDomain as exc:
            actual.append(dict(magic_id=magic_id,kind=kind,raw=raw,reason=str(exc),out=None))
        else:
            actual.append(dict(magic_id=magic_id,kind=kind,raw=raw,reason="defined",out=out))
            vectors.append((kind,raw))

    def line(kind,raw):
        return str(int(kind=="change"))+" "+("NULL" if raw is None else raw.hex() or "EMPTY")

    expected=[]
    for kind,raw in vectors:
        out=parse_status_magic_option(raw,kind=kind,profile=profile,execution_charset=charset)
        if not out.accepted:
            values=(0,0,-1,-1,-1,-1)
        else:
            values=(1,1,out.status,out.turn if kind=="change" else -1,
                    out.success if kind=="change" else -1,2 if kind=="change" else 1)
        expected.append(" ".join(map(str,values)))
    unsafe=[("change",None),("recovery",None),
            ("change",(_BASELINE[profile][1]+" ").encode(charset)),
            ("change",(_BASELINE[profile][1]+" turn").encode(charset))]
    if PROFILE_FACTS[profile][1]<PROFILE_FACTS[profile][0]:
        unsafe += [("change",b"x"),("recovery",b"x")]
    unsafe += [(row["kind"],row["raw"]) for row in actual if row["out"] is None]
    with tempfile.TemporaryDirectory() as directory:
        p=Path(directory);src=p/"parser.c";exe=p/"parser"
        src.write_text(prefix+source+main)
        build=subprocess.run(["cc","-std=c11","-w","-fexec-charset="+charset,
            "-fsanitize=address,undefined","-fno-sanitize-recover=all","-fno-pie","-no-pie",
            str(src),"-o",str(exe)],capture_output=True,text=True)
        if build.returncode:
            raise ValueError(f"{profile}/{charset} compile failure: "+build.stderr[-1500:])
        env=dict(os.environ,ASAN_OPTIONS="detect_leaks=0",UBSAN_OPTIONS="halt_on_error=1")
        run=subprocess.run([str(exe)],input="\n".join(line(k,r) for k,r in vectors)+"\n",
                           capture_output=True,text=True,env=env)
        if run.returncode:
            raise ValueError(f"{profile}/{charset} defined witness failure: "+run.stderr[-1800:])
        observed=run.stdout.splitlines()
        if observed!=expected:
            pos=next((i for i,(a,b) in enumerate(zip(observed,expected)) if a!=b),min(len(observed),len(expected)))
            raise ValueError(f"{profile}/{charset} parser mismatch {pos}: {observed[pos:pos+1]} vs {expected[pos:pos+1]}")
        for kind,raw in unsafe:
            try:
                parse_status_magic_option(raw,kind=kind,profile=profile,execution_charset=charset)
            except CombinedStatusMagicDomain:
                pass
            else:
                raise ValueError("unsafe native witness was not independently rejected")
            bad=subprocess.run([str(exe)],input=line(kind,raw)+"\n",capture_output=True,text=True,env=env)
            if bad.returncode==0 or not any(word in bad.stderr for word in
                ("runtime error:","AddressSanitizer","UndefinedBehaviorSanitizer")):
                raise ValueError(f"{profile}/{charset} expected parser diagnostic absent")
    for row in actual:
        row.pop("raw")
    return dict(charset=charset,defined_cases=len(vectors),unsafe_diagnostics=len(unsafe),actual=actual)


def analyze_profile(profile,root,*,actual_options):
    root=Path(root).resolve()
    head=subprocess.check_output(["git","-C",str(root),"rev-parse","HEAD"],text=True).strip()
    if head!=PINNED[profile] or subprocess.check_output(["git","-C",str(root),"status","--porcelain"],text=True).strip():
        raise ValueError("clean pinned source identity drift")
    base=root/LAYOUTS[profile]
    paths={"magic":base/"battle/battle_magic.c","event":base/"battle/battle_event.c",
           "version":base/"include/version.h","battle_h":base/"include/battle.h"}
    includes=["-I",str(base/"include")]
    if profile=="bismarck":
        includes += ["-I",str(root/"server/common"),"-I",str(root/"shared/lua51")]
    magic=_text(paths["magic"]);event=_text(paths["event"])
    funcs=[_definition(magic,"MAGIC_StatusChange_Battle"),_definition(magic,"MAGIC_StatusRecovery_Battle")]
    globals=""
    if profile=="bismarck":
        for key in ("szTurn","szSuccess"):
            match=re.search(r'const\s+char\s+'+key+r'\[\]\s*=\s*"[^\"]*"\s*;',magic)
            if match is None:raise ValueError("missing Bismarck parser marker")
            globals+=match.group()+"\n"
    source=_preprocess(_array(event,"aszStatus")+"\n"+globals+"\n"+"\n".join(funcs),includes,paths["version"])
    labels=len(re.findall(r'"[^\"]*"',_array(source,"aszStatus")))
    end=_enum_values(["BATTLE_ST_END"],includes)["BATTLE_ST_END"]
    change=_normalize(_strip(_definition(source,"MAGIC_StatusChange_Battle")))
    recovery=_normalize(_strip(_definition(source,"MAGIC_StatusRecovery_Battle")))
    gates={
        "profile_status_table_facts": (end,labels)==PROFILE_FACTS[profile][:2],
        "change_excludes_zero_recovery_includes_zero": "i=1;i<BATTLE_ST_END;i++" in change and "i=0;i<BATTLE_ST_END;i++" in recovery,
        "both_scan_first_two_bytes":all("strncmp(pszP,aszStatus[i],2)" in fn for fn in (change,recovery)),
        "both_advance_body_two_plus_loop_one":all("pszP++" in fn and "pszP+=2;" in fn for fn in (change,recovery)),
        "both_option_null_is_unguarded":all("if(magicarg==NULL)" not in fn and "pszP=magicarg" in fn for fn in (change,recovery)),
        "turn_search_overwrites_pointer_before_success":
            "(pszP=strstr(pszP,szTurn))!=" in change and "(pszP=strstr(pszP,szSuccess))!=" in change,
        "sizeof_marker_skip_and_defaults":all(x in change for x in ("turn=3","Success=15","pszP+=sizeof(szTurn)","pszP+=sizeof(szSuccess)")),
        "selected_multi_effects_collected": "BATTLE_MultiStatusChange(" in change and "BATTLE_MultiStatusRecovery(" in recovery,
        "no_parser_rng": all("RAND(" not in fn and "rand(" not in fn for fn in (change,recovery)),
    }
    marker=re.search(r'(?:const\s+)?char\s+szSuccess\[\]\s*=\s*"([^\"]*)"',source)
    gates["success_marker_matches_profile"]=marker is not None and marker.group(1)==SUCCESS_MARKERS[profile]
    if not all(gates.values()):raise ValueError(f"{profile} source gates failed: "+str([k for k,v in gates.items() if not v]))
    return dict(profile=profile,sha=head,gates=gates,labels=labels,end=end,
        hashes={key:_sha(path) for key,path in paths.items()},
        builds=[_native(source,profile,charset,actual_options=actual_options) for charset in BUILD_CHARSETS[profile]])


def recovered_options(data_dir):
    result,digest=analyze_crosslinks(Path(data_dir))
    if not result["population_closed"] or not result["exact_rows_closed"]:
        raise ValueError("recovered magic crosslink must be exact before parser audit")
    _,rows,_,_,_=parse_magic(Path(data_dir)/"magic.txt")
    options={int(values["ID"]):bytes(fields[3]) for fields,values in rows if int(values["ID"]) in STATUS_MAGIC_IDS}
    if tuple(sorted(options))!=STATUS_MAGIC_IDS:raise ValueError("status magic population drift")
    return options,digest


def emit(results,digest):
    if digest:
        signatures=[]
        for row in results:
            for build in row["builds"]:
                for actual in build["actual"]:
                    out=actual["out"]
                    signatures.append((row["profile"],build["charset"],actual["magic_id"],actual["kind"],
                        "defined" if out is not None else "unsafe",
                        out.accepted if out is not None else None,
                        out.status if out is not None else None,
                        out.turn if out is not None else None,
                        out.success if out is not None else None,actual["reason"]))
        validate_actual_outcomes(signatures)
    print("StoneAge Combined ordinary status-magic parser audit — R1")
    print("Derived hashes and semantic fields only; exact NUL-terminated native OPTION witnesses.")
    print("Battle mutation collectors are stubs; original build charset and ordered runtime remain OPEN.")
    for row in results:
        print(f"PROFILE|name={row['profile']}|sha={row['sha']}|status_end={row['end']}|labels={row['labels']}")
        for key,value in sorted(row["gates"].items()):print(f"GATE|profile={row['profile']}|name={key}|pass={int(value)}")
        for build in row["builds"]:
            print(f"NATIVE|profile={row['profile']}|charset={build['charset']}|defined_cases={build['defined_cases']}|unsafe_diagnostics={build['unsafe_diagnostics']}|asan_ubsan_pass=1")
            for actual in build["actual"]:
                out=actual["out"]
                suffix=(f"accepted={int(out.accepted)}|status={out.status}|turn={out.turn}|success={out.success}" if out is not None else "reason="+actual["reason"])
                print(f"ACTUAL|profile={row['profile']}|charset={build['charset']}|magic_id={actual['magic_id']}|kind={actual['kind']}|domain={'defined' if out is not None else 'unsafe'}|{suffix}")
        for key,value in sorted(row["hashes"].items()):print(f"SOURCE_SHA256|profile={row['profile']}|file={key}|sha256={value}")
    print("FACT|status_match_body_plus2_and_loop_plus1_moves_cursor_three_bytes")
    print("FACT|missing_turn_overwrites_cursor_NULL_before_success_strstr")
    print("FACT|success_marker=gavin_single_han_iris_greek_bismarck_two_han")
    print("BOUNDARY|gavin_iris_status_table_32_vs_scan44_nonmatch_unsafe")
    print("BOUNDARY|safe_baseline_only_for_short_tables_extended_label_admission_open")
    print("BOUNDARY|MP_item_pool_target_membership_status_mutation_RNG_and_persistence_not_closed")
    print("RESOLUTION|COMBINED_STATUS_MAGIC_PARSER_REFERENCE_CLOSED_CONDITIONAL_BUILD")
    if digest:
        print("DATA_SHA256|file=magic|sha256="+digest)
        print("RESOLUTION|RECOVERED25_COMBINED_STATUS_MAGIC_ACTUAL_BYTE_AUDIT_CLOSED_CONDITIONAL_BUILD")
        print("RESOLUTION|RECOVERED25_COMBINED_STATUS_MAGIC_EXACT_OUTCOME_MATRIX_CLOSED")
    else:
        print("RESOLUTION|RECOVERED25_COMBINED_STATUS_MAGIC_ACTUAL_BYTE_AUDIT_OPEN")
    print("RESOLUTION|RECOVERED25_COMBINED_ORDERED_RUNTIME_OPEN")


def main():
    parser=argparse.ArgumentParser()
    for name in PINNED:parser.add_argument("--"+name+"-dir",type=Path,required=True)
    parser.add_argument("--data-dir",type=Path)
    args=parser.parse_args()
    options,digest=({},None) if args.data_dir is None else recovered_options(args.data_dir)
    emit([analyze_profile(name,getattr(args,name+"_dir"),actual_options=options) for name in PINNED],digest)


if __name__=="__main__":main()
