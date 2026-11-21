#!/usr/bin/env python3
"""PET126S: bounded native reads of the CN5 classic PC 80-byte album slot +36.

One exact-source static pass: byte-identify the saved original EXE, then scan the
already verified PE32 .text disassembly for direct uses of the specific runtime
record field and base. The procedure *does not* claim complete alias analysis,
native sprite selection, game execution, server issuance or official retail
pressing certification. No proprietary input/output bytes are committed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

from tools.stoneage_pet126m_cn50_pe_album_xrefs import parse_objdump, pe32_text_identity
from tools.stoneage_pet126k_cn50_original_exe_probe import EXPECTED
from tools.stoneage_pet126r_cn50_source_catalogue import (
    ROOT, actual_native_tail_field_bridge
)

PRIOR = ROOT / "research/recovered/STONEAGE-PET126R-CN50-PC-ORIGINAL-ALBUM-SOURCE-ACCEPTANCE-R1.json"
BASE_VA = 0x3300ca8
TAIL_VA = BASE_VA + 36
NAME_TAIL_VA = 0x482f68 + 24
MAX_CONTEXTS = 16

def exact_hex_tokens(instruction: str):
    return {int(token, 16) for token in re.findall(r"(?<![\w])0x[0-9a-fA-F]+(?![\w])", instruction)}

def classify_direct_field_instruction(instruction: str, address: int):
    """Classifies only explicit .text instructions naming 0x3300ccc.

    If an indexed alias indirectly accesses the field via another base register,
    it will not be seen. Non-mov operations are explicitly conservative.
    """
    if address not in exact_hex_tokens(instruction):
        return None
    fields = instruction.strip().split(None, 1)
    if len(fields) != 2:
        return "OTHER_LITERAL_NOT_CLASSIFIED"
    op, parts = fields
    operands = [x.strip() for x in parts.split(",", 1)]
    first, second = operands[0], operands[1] if len(operands) > 1 else ""
    first_ref = "[" in first and address in exact_hex_tokens(first)
    second_ref = "[" in second and address in exact_hex_tokens(second)
    if op == "lea" and second_ref:
        return "ADDRESS_ONLY_LEA_NOT_DEREFERENCE"
    if op == "mov" and first_ref:
        return "EXPLICIT_MEMORY_WRITE"
    if op == "mov" and second_ref:
        return "EXPLICIT_MEMORY_READ"
    if op in {"cmp", "test", "push"} and (first_ref or second_ref):
        return "EXPLICIT_MEMORY_TEST_OR_PUSH_READ"
    if op in {"add", "sub", "inc", "dec", "and", "or", "xor", "xchg"} and first_ref:
        return "MEMORY_READ_MODIFY_WRITE_OR_EXCHANGE"
    if first_ref or second_ref:
        return "DIRECT_FIELD_DEREFERENCE_OTHER_SEMANTICS"
    return "ADDRESS_LITERAL_WITHOUT_EXPLICIT_DEREFERENCE"

def occurrences(code, address, context=3):
    all_sites=[]
    for i,row in enumerate(code):
        cat=classify_direct_field_instruction(row["instruction"], address)
        if cat is None:
            continue
        all_sites.append({
          "va":hex(row["address"]),
          "category":cat,
          "instruction":row["instruction"],
          "nearby_before":[x["instruction"] for x in code[max(i-context,0):i]],
          "nearby_after":[x["instruction"] for x in code[i+1:i+context+1]]
        })
    by_cat={}
    for item in all_sites:
        by_cat[item["category"]]=by_cat.get(item["category"],0)+1
    return {
      "exact_instruction_hits":len(all_sites),
      "all_hit_instruction_addresses":[x["va"] for x in all_sites],
      "by_access_class":dict(sorted(by_cat.items())),
      "first_bounded_contexts":all_sites[:MAX_CONTEXTS],
      "contexts_truncated":len(all_sites)>MAX_CONTEXTS
    }

def inspect(path:Path):
    program=path.read_bytes()
    if (len(program),hashlib.sha256(program).hexdigest())!=EXPECTED["sa_5000.exe"]:
        raise ValueError("unqualified-original-PC-EXE")
    accepted=json.loads(PRIOR.read_text(encoding="utf-8"))
    if (accepted["original_program"]["sha256"]!=EXPECTED["sa_5000.exe"][1] or
        accepted["permanent_machine_derived"]["git_blob_sha"]!="8b1058a43c267dfeaa298d4c2c472209cebd24d9"):
        raise ValueError("prior-original-source-or-derived-catalogue-mismatch")
    imagebase,text=pe32_text_identity(program)
    sub=subprocess.run(["objdump","-d","-M","intel","-j",".text",str(path)],
        capture_output=True,text=True,timeout=90)
    if sub.returncode:
        raise ValueError("source-disassembly-failed")
    decoded=parse_objdump(sub.stdout)
    if len(decoded)!=131461:
        raise ValueError("unexpected-original-source-decoded-instruction-total")
    bridge=actual_native_tail_field_bridge(decoded)
    if not bridge["exact_original_static_adjacent_operand_transfer_verified"]:
        raise ValueError("previous-original-album-field-bridge-changed")
    direct=occurrences(decoded,TAIL_VA)
    base=occurrences(decoded,BASE_VA)
    tail=occurrences(decoded,NAME_TAIL_VA)
    sites={x["va"]:x for x in direct["first_bounded_contexts"]}
    # The known original source writer *must* be a direct write at 0x434774.
    if "0x434774" not in direct["all_hit_instruction_addresses"]:
        raise ValueError("expected-original-runtime-plus36-field-writer-missing")
    known=[x for x in decoded if x["address"]==0x434774]
    if len(known)!=1 or classify_direct_field_instruction(known[0]["instruction"],TAIL_VA)!="EXPLICIT_MEMORY_WRITE":
        raise ValueError("known-source-writer-not-actual-write")
    direct_read_categories=("EXPLICIT_MEMORY_READ","EXPLICIT_MEMORY_TEST_OR_PUSH_READ",
                            "MEMORY_READ_MODIFY_WRITE_OR_EXCHANGE",
                            "DIRECT_FIELD_DEREFERENCE_OTHER_SEMANTICS")
    direct_reads=sum(direct["by_access_class"].get(k,0) for k in direct_read_categories)
    result={
        "schema":"stoneage.pet126s.cn50_pc_exact_original_runtime_album_u32_consumer_bounded_scan.r1",
        "date":"2026-11-21","active_module":"PET","scope":"ORIGINAL_CLASSIC_2D_PC_ONLY",
        "source":{
            "exe":"sa_5000.exe","exe_bytes":len(program),"exe_sha256":hashlib.sha256(program).hexdigest(),
            "historical_original_official_pressing_certified":False,
            "original_exe_executed":False,"original_proprietary_binary_disclosed":False,
            "original_instruction_count":len(decoded),"objdump":"GNU_BINUTILS_INTEL_LINEAR_DISASSEMBLY",
            "pe_image_base":hex(imagebase)
        },
        "previous_verified_original_static_data_bridge":bridge,
        "native_direct_literal_field_address":hex(TAIL_VA),
        "native_record_base_address":hex(BASE_VA),
        "original_compiled_name_tail_address":hex(NAME_TAIL_VA),
        "native_direct_access_to_runtime_record_plus36":direct,
        "native_record_base_literal_reference":base,
        "compiled_table_tail_literal_reference":tail,
        "summary":{
           "exact_encoded_field_literals":direct["exact_instruction_hits"],
           "explicit_direct_memory_reader_or_mutator_sites":direct_reads,
           "known_original_source_writer_replayed":True,
           "indirect_alias_analysis_completed":False,
           "native_graphics_renderer_or_SPR_selector_proven":False,
           "native_pet_name_to_SPR_species_identity_proven":False,
           "official_live_pet_issuance_proven":False,
           "source_bounded_consumer_question_complete":True,
           "do_not_continue_generic_CRT_or_unbounded_static_reverse_engineering":True
        },
        "decision":{
          "classification":"EXACT_ADDRESS_SITE_CENSUS_SOURCE_BOUNDED_NOT_COMPLETE_DATAFLOW",
          "do_not_claim_absence_of_other_alias_readers":True,
          "native_real_sprite_selector":None,
          "original_server_pet_master":None,
          "new_official_species_verified":0,
          "pet_module_closed":False,
          "year_2026":"NOT_YEAR_AUDITED",
          "overall_percent":None,
          "next":"PET126T: integrate exact native +36 scan with PET126F seven-dimension original-PC source/gaps; stop this static subroutine trail unless independent original same-build selector or issued server master arrives."
        }
    }
    return result

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--program",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    report=inspect(args.program)
    args.output.write_text(json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf8")
    print("PET126S_ORIGINAL_PC_FIELD_CENSUS|direct="+
          str(report["summary"]["exact_encoded_field_literals"])+
          "|read_like="+str(report["summary"]["explicit_direct_memory_reader_or_mutator_sites"])+
          "|native_SPR_proven=NO|official_pet_species=0",flush=True)

if __name__ == "__main__":
    main()
