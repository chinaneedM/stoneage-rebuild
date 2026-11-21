#!/usr/bin/env python3
"""PET126O source-verified bounded call-target analysis for original mainland PC 5.0.

No executable is run and no commercial code bytes are retained. Output describes
at most short static compiler instruction sequences. No claim of actual gameplay,
pet issuance, draw selection or full control-flow reconstruction is permitted.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

from tools.stoneage_pet126m_cn50_pe_album_xrefs import (
    ROOT, parse_objdump, pe32_text_identity,
)
from tools.stoneage_pet126l_cn50_table_graphic_probe import (
    EXPECTED, TABLE_OFFSET, source_rows, exact_pointer_literals,
)
from tools.stoneage_pet126n_cn50_global80 import pe_sections, section_for_va
PET126N = ROOT / "research/recovered/STONEAGE-PET126N-CN50-ORIGINAL-80BYTE-RUNTIME-SLOT-SOURCE-R1.json"
TARGETS=(0x45F560,0x430665)
WINDOW_LEN=50
SOURCE_3_XREFS=(199700,200343,214772)

def direct_calls(disasm,target):
    key=hex(target)
    return [{"caller_va":item["address"],"text":item["instruction"]}
            for item in disasm if re.fullmatch(r"call\s+"+re.escape(key),
                                               item["instruction"].strip())]

def entry_context(disasm,entry,maximum=WINDOW_LEN):
    index={x["address"]:k for k,x in enumerate(disasm)}
    if entry not in index:
        return {"entry_va":entry,"decoded_entry":False,"first_instructions":[],"first_return_va":None}
    first=disasm[index[entry]:index[entry]+maximum]
    first_return=next((x["address"] for x in first if re.fullmatch(r"ret(?:\s+0x[0-9a-f]+)?",x["instruction"])),None)
    return {"entry_va":entry,"decoded_entry":True,
            "first_instructions":[{"va":x["address"],"ins":x["instruction"]} for x in first[:32]],
            "bounded_instruction_count":len(first),
            "first_return_va_within_window":first_return,
            "calls_within_first_window":[{"va":x["address"],"target":x["instruction"]}
                for x in first if x["instruction"].startswith("call")][:15],
            "limited_lookahead_not_complete_control_flow":True}

def read_file_backed_cstring(program: bytes, image_base: int, sections, va: int):
    """At most 64 printable ASCII characters plus hashes, never original binary."""
    for section in sections:
        off=va-image_base-section["virtual_rva"]
        if 0<=off<section["raw_size"]:
            origin=section["raw_offset"]+off
            raw=program[origin:origin+96].split(b"\x00",1)[0]
            if not raw:return {"va":hex(va),"file_backed":True,"empty":True}
            printable=all(32<=x<127 for x in raw)
            return {"va":hex(va),"file_backed":True,"ascii_printable":printable,
                    "observed_span_length_capped_96":len(raw),
                    "span_sha256":hashlib.sha256(raw).hexdigest(),
                    "short_literal":raw[:64].decode("ascii") if printable and len(raw)<=64 else None}
    return {"va":hex(va),"file_backed":False,"short_literal":None}


def inspect(original:Path):
    data=original.read_bytes()
    if (len(data),hashlib.sha256(data).hexdigest()) != EXPECTED["sa_5000.exe"]:
        raise ValueError("source-program-original-sha-mismatch")
    source_rows(data)
    n=json.loads(PET126N.read_text("utf-8"))
    if n["source"]["exe_sha256"]!=EXPECTED["sa_5000.exe"][1]:
        raise ValueError("source-chain-pet126n-sha-mismatch")
    imagebase,text=pe32_text_identity(data)
    imagebase2,_,sections=pe_sections(data)
    if imagebase2!=imagebase:raise ValueError('pe-section-base-not-identical')
    e=exact_pointer_literals(data,TABLE_OFFSET)
    if [x["file_offset"] for x in e["literal_va_locations"]] != list(SOURCE_3_XREFS):
        raise ValueError("source-compiled-name-address-locations-disagree")
    proc=subprocess.run(["objdump","-d","-M","intel","-j",".text",str(original)],
                        text=True,capture_output=True,timeout=90)
    if proc.returncode:
        raise ValueError("source-original-objdump-failure")
    decoded=parse_objdump(proc.stdout)
    if len(decoded)!=131461:
        raise ValueError("source-original-disassembly-size-differs")
    known={0x45F560:(4394697,),0x430665:(4394033,4394703)}
    out=[]
    for entry in TARGETS:
        calls=direct_calls(decoded,entry)
        caller_positions={v["caller_va"] for v in calls}
        if not set(known[entry]).issubset(caller_positions):
            raise ValueError("prior-source-original-helper-callsite-unconfirmed:"+hex(entry))
        context=entry_context(decoded,entry)
        if not context["decoded_entry"]:
            raise ValueError("original-call-target-is-not-disassembled-entry:"+hex(entry))
        out.append({
            "entry_va":entry,"entry_hex":hex(entry),
            "text_section_valid":imagebase+text[1]<=entry<imagebase+text[1]+text[3],
            "total_direct_calls_in_original_text":len(calls),
            "source_confirmed_pet_album_call_sites":list(known[entry]),
            "direct_caller_va_first_30":[z["caller_va"] for z in calls[:30]],
            "call_sites_truncated":len(calls)>30,
            "bounded_entry_context":context
        })
    if out[0]["bounded_entry_context"]["first_instructions"][2]["ins"]!="jmp    0x45f5d1":
        raise ValueError("source-string-helper-jump-target-changed")
    target=entry_context(decoded,0x45f5d1,maximum=64)
    if not target["decoded_entry"]:raise ValueError("source-string-helper-body-unknown")
    extended_index=entry_context(decoded,0x430665,maximum=110)
    string_arguments=[read_file_backed_cstring(data,imagebase,sections,x)
                      for x in (0x46d300,0x485830)]
    return {
        "static_followup":{"0x45f560_jump_target":"0x45f5d1",
                           "0x45f5d1_first_32_instructions":target["first_instructions"],
                           "0x430665_first_return_within_110_instructions":extended_index["first_return_va_within_window"],
                           "0x430665_calls_within_110_instructions":extended_index["calls_within_first_window"],
                           "0x430665_string_argument_VAs":string_arguments,
                           "string_copy_semantics_not_assumed_without_operand_path":True},
        "schema":"stoneage.pet126o.cn50_original_pc_2_compiled_helper_entry_contexts.r1",
        "date":"2026-11-21", "active_module":"PET", "scope":"CLASSIC_PC_ONLY",
        "source_original_program_size":len(data),
        "source_original_program_sha256":hashlib.sha256(data).hexdigest(),
        "source_prior_pet126n_receipt":"research/recovered/STONEAGE-PET126N-CN50-ORIGINAL-80BYTE-RUNTIME-SLOT-SOURCE-R1.json",
        "source_three_album_pointer_file_offsets":SOURCE_3_XREFS,
        "source_80byte_record_base":"0x3300ca8",
        "functions":out,
        "limits":{"two_helper_entries_only":True,
                  "linear_disassembly_not_reachable_code_proof":True,
                  "entry_window_not_whole_function":True,
                  "zero_proprietary_binary_bytes_saved":True,
                  "original_game_not_executed":True,
                  "no_proven_original_pet_sprite_selector":True,
                  "no_original_server_live_pet_release":True,
                  "official_species_newly_proven":0,
                  "historical_pet_module_closed":False,
                  "overall_percent":None},
        "next":"Use any actual helper-entry instruction semantics to bound exact same-build text/graphic identity; do not enlarge anonymous reverse engineering when no original sprite-name selector"
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--program",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    result=inspect(args.program)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("PET126O_SOURCE_SHA_PASSED|2_ORIGINAL_HELPERS|NO_LIVE_PET_PROMOTION")

if __name__=="__main__":
    main()
