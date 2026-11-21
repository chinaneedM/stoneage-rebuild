#!/usr/bin/env python3
"""PET126P: bounded original PC CN5 compiled album_13.dat I/O-call investigation.

Static, SHA-pinned exact original EXE; no game execution, copied binary, published
commercial bytes, reconstructed proprietary implementation, or server claims.
Distinguish original instruction operands from guessed standard C library symbols.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

from tools.stoneage_pet126l_cn50_table_graphic_probe import EXPECTED, TABLE_OFFSET, source_rows, exact_pointer_literals
from tools.stoneage_pet126m_cn50_pe_album_xrefs import parse_objdump, pe32_text_identity
from tools.stoneage_pet126n_cn50_global80 import pe_sections
from tools.stoneage_pet126o_cn50_bounded_helpers import read_file_backed_cstring

ROOT = Path(__file__).resolve().parents[1]
PRIOR = ROOT / "research/recovered/STONEAGE-PET126O-CN50-ORIGINAL-ALBUM13-LOCAL-HELPERS-R1.json"

ENTRY = 0x430665
BOUNDED_END = 0x430750
KNOWN_HELPERS = (0x45F182,0x45ED40,0x45F1A0,0x45EF9B)
PINNED_NAME_VA = 0x485830
PINNED_MODE_VA = 0x46D300
MAX_CONTEXT_INSTRUCTIONS = 7

def bounded_instructions(disasm,begin,end):
    if begin>=end:raise ValueError("nonpositive-bound")
    within=[x for x in disasm if begin<=x["address"]<end]
    if not within or within[0]["address"]!=begin:
        raise ValueError("no-source-matching-entrypoint")
    return within

def source_call_context(items, radius=MAX_CONTEXT_INSTRUCTIONS):
    """Return small static caller contexts; not dynamic argument/data-flow proof."""
    selected=[]
    for idx,item in enumerate(items):
        if not item["instruction"].startswith("call"):
            continue
        before=items[max(0,idx-radius):idx]
        after=items[idx+1:idx+4]
        selected.append({
            "call_site_va":item["address"],"call_instruction":item["instruction"],
            "nearest_previous":[{"va":x["address"],"instruction":x["instruction"]} for x in before],
            "nearest_following":[{"va":x["address"],"instruction":x["instruction"]} for x in after]
        })
    return selected

def short_entry(items,base,count=14):
    idx=next((i for i,v in enumerate(items) if v["address"]==base),None)
    if idx is None:return {"entry_va":hex(base),"decoded":False,"first":[]}
    return {
        "entry_va":hex(base),"decoded":True,
        "first":[{"va":x["address"],"instruction":x["instruction"]} for x in items[idx:idx+count]]
    }

def exact_global_literal_sites(items,value):
    hits=[]
    for i in items:
        tokens=re.findall(r"0x[0-9a-fA-F]+",i["instruction"])
        if any(int(x,16)==value for x in tokens):
            hits.append({"va":i["address"],"instruction":i["instruction"]})
    return hits

def inspect(path:Path):
    program=path.read_bytes()
    if (len(program),hashlib.sha256(program).hexdigest())!=EXPECTED["sa_5000.exe"]:
        raise ValueError("original-program-sha-mismatch")
    source_rows(program)
    prior=json.loads(PRIOR.read_text("utf-8"))
    if prior["source"]["program_sha256"]!=EXPECTED["sa_5000.exe"][1]:
        raise ValueError("pet126o-source-not-same-original")
    imagebase,text=pe32_text_identity(program)
    b,_,sections=pe_sections(program)
    if b!=imagebase:raise ValueError("image-base-disagrees")
    xrefs=exact_pointer_literals(program,TABLE_OFFSET)
    if [x["file_offset"] for x in xrefs["literal_va_locations"]] != [199700,200343,214772]:
        raise ValueError("compiled-name-source-xrefs-changed")
    literal_path=read_file_backed_cstring(program,imagebase,sections,PINNED_NAME_VA)
    literal_mode=read_file_backed_cstring(program,imagebase,sections,PINNED_MODE_VA)
    if literal_path["short_literal"]!=r"data\album_13.dat" or literal_mode["short_literal"]!="r+b":
        raise ValueError("original-album-file-and-open-mode-literals-changed")
    if literal_path["span_sha256"]!=prior["helper_0x430665"]["original_local_file"]["source_sha256"]:
        raise ValueError("original-local-filename-not-prior-evidence")
    raw=subprocess.run(["objdump","-d","-M","intel","-j",".text",str(path)],
                       capture_output=True,text=True,timeout=90)
    if raw.returncode:raise ValueError("original-PE-disassembly-failed")
    allcode=parse_objdump(raw.stdout)
    if len(allcode)!=131461:raise ValueError("source-original-linear-disassembly-count-changed")
    body=bounded_instructions(allcode,ENTRY,BOUNDED_END)
    if len(body)>180:raise ValueError("original-I/O-source-window-too-large")
    calls=source_call_context(body)
    if not any(x["call_instruction"]=="call   0x45f182" for x in calls):
        raise ValueError("original-file-open-like-call-missing")
    if not any(x["call_instruction"]=="call   0x45ed40" for x in calls):
        raise ValueError("original-seek-read-helper-call-missing")
    instructions=[x["instruction"] for x in body]
    if not any("0x5f60" in x and x.startswith("imul") for x in instructions):
        raise ValueError("source-local-file-dynamic-0x5f60-stride-missing")
    if not any("0x332e4bc" in x and x.startswith("cmp") for x in instructions):
        raise ValueError("source-original-362-entries-range-check-missing")
    return {
      "schema":"stoneage.pet126p.cn50_pc_original_album_file_primitive_bound_r1",
      "date":"2026-11-21","active_module":"PET","scope":"ORIGINAL_CLASSIC_PC_ONLY",
      "provenance":"THIRD_PARTY_PRESERVED_CN50_5_0_NOT_AUTHENTICATED_OFFICIAL_PRESSING",
      "source_exe_name":"sa_5000.exe",
      "source_exe_bytes":len(program),"source_exe_sha256":hashlib.sha256(program).hexdigest(),
      "prior_original_file_path":"data\\album_13.dat","prior_original_file_mode":"r+b",
      "name_table_source_file_offsets":[199700,200343,214772],
      "bounded_native_function":{"start_va":hex(ENTRY),"end_va_exclusive":hex(BOUNDED_END),
        "instruction_count":len(body),
        "full_control_flow_proven":False,
        "returns_within_bound":[{"va":x["address"],"ins":x["instruction"]} for x in body if re.fullmatch(r"ret(?:\s+0x[0-9a-f]+)?",x["instruction"])],
        "source_initial_12_instructions":[{"va":x["address"],"ins":x["instruction"]} for x in body[:12]],
        "all_in_bound_calls_with_source_neighborhood":calls,
        "local_dynamic_stride_0x5f60":[{"va":x["address"],"ins":x["instruction"]} for x in body if "0x5f60" in x["instruction"]],
        "local_file_mode_address_literals":exact_global_literal_sites(body,PINNED_MODE_VA),
        "local_file_path_address_literals":exact_global_literal_sites(body,PINNED_NAME_VA),
      },
      "compiled_helper_entry_prefixes":[short_entry(allcode,x) for x in KNOWN_HELPERS],
      "original_installer_album_file_available":False,
      "original_installer_inventory_source":"research/recovered/STONEAGE-STONEAGE5-REAL-CAB-PAYLOAD-R1.json",
      "claims":{
        "same_source_file_mode_and_path_source_verified":True,
        "file_calls_static_not_runtime_executed":True,
        "helper_symbol_names_not_yet_proven":True,
        "original_album_file_record_bytes_not_available":True,
        "0x5f60_stride_purpose_unknown":True,
        "same_original_exe_spr_selector_found":False,
        "new_official_pet_species_proven":0,
        "original_server_release_unverified":True,
        "pets_module_closed":False,
        "overall_percent":None,
        "commercial_bytes_published":False
      },
      "next":"Interpret limited original file I/O arguments with source-evidenced call convention, otherwise stop; refocus PC-only PET source-based name-to-graphics link."
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--program",required=True,type=Path)
    p.add_argument("--output",required=True,type=Path)
    v=p.parse_args()
    out=inspect(v.program)
    v.output.write_text(json.dumps(out,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
    print("PET126P_ORIGINAL_PC_5_0_EXE_SHA_PASS|ALBUM_LOCAL_IO_SOURCE_CONTEXT|NO_PET_RELEASE_PROMOTION")
if __name__=="__main__": main()
