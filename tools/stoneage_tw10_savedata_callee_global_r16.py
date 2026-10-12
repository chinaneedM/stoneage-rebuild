"""R16 bounded original TW1.0 callee effects and third virtual-global reference scan.

Only exact verified original source bytes are processed transiently. All
callee summaries are syntax/model-bound candidate traces, NOT runtime effects,
ABI, caller continuation, initialization, ownership or native save.
"""
import argparse
import json
import tempfile
from pathlib import Path
from tools.stoneage_tw10_savedata_entrycalls_r15 import (
    inspect_verified as inspect_r15, RUNTIME_SHA256, SAVEDATA_SHA256
)
from tools.stoneage_tw10_savedata_helper_effects_r8 import summarize
from tools.stoneage_tw10_savedata_frontier_r12 import linear_references
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH, SAVEDATA_PATH
from tools.stoneage_tw10_technical_probe import find_rows, extract_row

SCHEMA="tw10-r16-original-bounded-cal lee-and-third-global".replace(" ","")
STATUS="PINNED_ORIGINAL_CONDITIONAL_HELPER_AND_GLOBAL_REFERENCES_EFFECTS_OPEN"
CALLEES=((0x484c0,144),(0x49900,80),(0x4a09c,80),(0x4a14d,80))
GLOBAL=0x172186c
FLAGS=("call_arguments_resolved","call_results_resolved",
       "caller_context_equivalence_proven","callee_effects_admitted",
       "actual_function_entries_proven","global_runtime_initialization_proven",
       "global_actual_value_proven","original_native_io_proven",
       "original_save_format_proven","heapalloc_ownership_proven",
       "original_bytes_published")

def callee_frontiers(dec,callee_specs=CALLEES):
    if len(set(root for root,_ in callee_specs))!=len(callee_specs):
        raise ValueError("duplicate callee roots")
    result=[]
    for root,cap in callee_specs:
        if type(cap) is not int or not 1<=cap<=160:
            raise ValueError("callee state cap")
        summary=summarize(dec,root,max_states=cap)
        if summary["root_rva"]!=root:
            raise ValueError("callee root mismatch")
        result.append({
            "root_rva":root,
            "state_cap":cap,
            "summary":summary,
            "function_entry_proven":False,
            "original_callee_effects_admitted":False,
            "calling_convention_proven":False,
            "caller_specific_values_proven":False,
            "original_runtime_path_proven":False,
        })
    return result

def third_global_references(dec,target=GLOBAL):
    scan=linear_references(dec,targets=(target,))
    if [x["global_rva"] for x in scan["globals"]]!=[target]:
        raise ValueError("global reference target changed")
    return scan

def inspect_verified(runtime,savedata):
    prior=inspect_r15(runtime,savedata)
    sites={(item["call_rva"],item["direct_target_rva"]) for item in prior["call_surfaces"]}
    for item in ((0x49444,0x484c0),(0x4945d,0x484c0),
                 (0x4946f,0x49900),(0x49e5f,0x4a09c),(0x49e6e,0x4a14d)):
        if item not in sites:
            raise ValueError("R15 exact original CALL source changed")
    eax=prior["upstream_inputs"][0]["origins"][0]
    if eax["rva"]!=0x49de3 or eax["semantic"]["memory_input"]["displacement_region"]["displacement_rva"]!=GLOBAL:
        raise ValueError("R15 original EAX input identity changed")
    with tempfile.TemporaryDirectory() as td:
        path=Path(td)/"sa_3.exe";path.write_bytes(runtime)
        data,pe,base,sections,_=image_layout(path)
    t=next(s for s in sections if s["name"]==".text")
    dec=Decoder(data[t["raw"]:t["raw"]+t["raw_size"]],t["rva"],base)
    return {
        "schema":SCHEMA,"status":STATUS,
        "runtime_sha256":RUNTIME_SHA256,"savedata_sha256":SAVEDATA_SHA256,
        "r15_source_call_sites":sorted(sites),
        "r15_upstream_global_rva":GLOBAL,
        "callee_frontiers":callee_frontiers(dec),
        "third_global_references":third_global_references(dec),
        "static_only":True,
        "callee_summaries_not_context_qualified":True,
        **{flag:False for flag in FLAGS}
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--bin",type=Path,required=True)
    args=p.parse_args()
    image,rows,_,_=find_rows(args.bin)
    try:
        files={row["path"]:row for row in rows if not row["is_dir"]}
        with tempfile.TemporaryDirectory() as td:
            exe=Path(td)/"sa_3.exe";saved=Path(td)/"savedata.dat"
            extract_row(image,files[RUNTIME_PATH],exe)
            extract_row(image,files[SAVEDATA_PATH],saved)
            obj=inspect_verified(exe.read_bytes(),saved.read_bytes())
    finally:
        image.close()
    print(json.dumps(obj,sort_keys=True))

if __name__=="__main__":
    main()
