#!/usr/bin/env python3
"""PET126Q: source-bounded file-helper forwarding in original 2D PC client.

No original executable is run or published; native CRT symbol names remain open.
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from tools.stoneage_pet126p_cn50_album_io import inspect as prior_inspect
from tools.stoneage_pet126l_cn50_table_graphic_probe import EXPECTED
from tools.stoneage_pet126m_cn50_pe_album_xrefs import parse_objdump

ROOT = Path(__file__).resolve().parents[1]
PREVIOUS = ROOT / "research/recovered/STONEAGE-PET126P-CN50-ORIGINAL-ALBUM13-305X80-FILE-ACCESS-R1.json"
FORWARD = {
 "open": (0x45f182,0x45f151,["push   0x40","push   DWORD PTR [esp+0xc]","push   DWORD PTR [esp+0xc]"]),
 "seek": (0x45ed40,0x45ed6c,["push   DWORD PTR [ebp+0x10]","push   DWORD PTR [ebp+0xc]","push   DWORD PTR [ebp+0x8]"]),
 "read": (0x45f018,0x45f047,["push   DWORD PTR [ebp+0x14]","push   DWORD PTR [ebp+0x10]","push   DWORD PTR [ebp+0xc]","push   DWORD PTR [ebp+0x8]"])
}
CORES=(0x45f151,0x45ed6c,0x45f047,0x45efcc)

def bounded_entry(code,entry,limit=90):
    idx=next((i for i,x in enumerate(code) if x["address"]==entry),None)
    if idx is None:raise ValueError("missing-original-PE-entry:"+hex(entry))
    out=[]
    for x in code[idx:idx+limit]:
        out.append(x)
        if x["instruction"].split()[0] in ("ret","retf"): break
    return out,out[-1]["instruction"].split()[0] in ("ret","retf")

def check_forward(code,entry,target,pushes):
    seq,returned=bounded_entry(code,entry)
    call="call   "+hex(target)
    hits=[i for i,x in enumerate(seq) if x["instruction"]==call]
    if len(hits)!=1:raise ValueError("missing-or-ambiguous-inner-call:"+hex(entry))
    i=hits[0]
    if [x["instruction"] for x in seq[i-len(pushes):i]]!=pushes:
        raise ValueError("forward-operands-mismatch:"+hex(entry))
    return {"wrapper_va":hex(entry),"inner_va":hex(target),
      "source_immediate_pushes":pushes,"inner_call_va":hex(seq[i]["address"]),
      "first_return_found":returned,"decoded_count":len(seq),
      "C_runtime_symbol_proven":False}

def core_prefix(code,entry):
    seq,returned=bounded_entry(code,entry,limit=32)
    return {"entry_va":hex(entry),"static_instruction_prefix":[
      {"va":hex(x["address"]),"ins":x["instruction"]} for x in seq],
      "first_return_within_32":returned,"only_linear_static_context":True,
      "C_runtime_symbol_proven":False}

def inspect(path):
    raw=path.read_bytes()
    if (len(raw),hashlib.sha256(raw).hexdigest())!=EXPECTED["sa_5000.exe"]:
        raise ValueError("original-PC-source-SHA-changed")
    previous=json.loads(PREVIOUS.read_text("utf-8"))
    if previous["source"]["sha256"]!=EXPECTED["sa_5000.exe"][1]:
        raise ValueError("PET126P-receipt-SHA-mismatch")
    prior=prior_inspect(path)
    if prior["source_exe_sha256"]!=EXPECTED["sa_5000.exe"][1]:
        raise ValueError("source-chain-mismatch")
    result=subprocess.run(["objdump","-d","-M","intel","-j",".text",str(path)],
      capture_output=True,text=True,timeout=90)
    if result.returncode:raise ValueError("original-PC-static-objdump-failed")
    code=parse_objdump(result.stdout)
    if len(code)!=131461:raise ValueError("source-original-disassembly-count-changed")
    wrappers={name:check_forward(code,*args) for name,args in FORWARD.items()}
    original_call_sites=prior["bounded_native_function"]["all_in_bound_calls_with_source_neighborhood"]
    callee_names=[x["call_instruction"].strip().split()[-1] for x in original_call_sites]
    if not all(hex(x) in callee_names for x in (0x45f182,0x45ed40,0x45f018,0x45ef9b)):
        raise ValueError("PET126P-source-callee-list-regressed")
    return {"schema":"stoneage.pet126q.original_classic_pc_file_helper_forwarding.r1",
      "active_module":"PET","date":"2026-11-21","scope":"ORIGINAL_CLASSIC_PC_ONLY",
      "source":{"carrier":"CN50_THIRD_PARTY_PRESERVED_NOT_OFFICIAL_PRESSING_CERTIFIED",
        "exe_sha256":hashlib.sha256(raw).hexdigest(),"exe_size":len(raw),
        "original_EXE_executed":False,"original_EXE_published":False,
        "prior":"research/recovered/STONEAGE-PET126P-CN50-ORIGINAL-ALBUM13-305X80-FILE-ACCESS-R1.json"},
      "verified_compiled_argument_forwarding":wrappers,
      "original_callee_static_bounded_prefixes":[core_prefix(code,x) for x in CORES],
      "native_album_context_call_targets":callee_names,
      "qualification":{"seek_symbol_fseek_proven":False,"read_symbol_fread_proven":False,
        "open_symbol_fopen_proven":False,"close_symbol_fclose_proven":False,
        "actual_album_file_obtained":False,"actual_file_IO_executed":False,
        "native_graphic_pet_selector_found":False,"actual_official_pet_release_new":0,
        "source_bound_stop_after_this_helper_check":True,"pet_closed":False,
        "stage_a":"7_PARTIAL_2_OPEN","stage_b_wiki":"GATED",
        "r79":"PAUSED_NON_BLOCKING","overall_percent":None,
        "original_current_blob_unchanged":"c89e0e33537990aa2132b47c40fef49a985a935c"},
      "next":"Close generic file-helper branch without further source; seek original same-build PC pet name-to-graphic binding or actual runtime album bytes; then source-bounded PET module field review."}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--program",required=True,type=Path)
    p.add_argument("--output",required=True,type=Path)
    v=p.parse_args()
    v.output.write_text(json.dumps(inspect(v.program),ensure_ascii=False,indent=2,sort_keys=True)+"\n","utf-8")
    print("PET126Q_CLASSIC_PC_SOURCE_FORWARD_PASS|NO_CRT_SYMBOL_OR_LIVE_PET_PROOF")
if __name__=="__main__":main()
