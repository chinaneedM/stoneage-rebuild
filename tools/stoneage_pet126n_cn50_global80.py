#!/usr/bin/env python3
"""PET126N: bounded source-verified CN5 PC album-to-80-byte-global provenance probe.

Do not execute the program or publish copyrighted executable/resource bytes.
Linear disassembly and number coincidences do not demonstrate game execution,
same-version SPR selector, or operator-issued pets.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import struct
import subprocess
from pathlib import Path

from tools.stoneage_pet126m_cn50_pe_album_xrefs import (
    PINNED_OFFSETS, ROOT, pe32_text_identity, parse_objdump,
)
from tools.stoneage_pet126l_cn50_table_graphic_probe import (
    EXPECTED, TABLE_OFFSET, source_rows, exact_pointer_literals,
)

M_RECEIPT = ROOT / "research/recovered/STONEAGE-PET126M-CN50-PE32-THREE-NAME-REFERENCE-STATIC-INSTRUCTION-R1.json"
RECORD_BASE = 0x3300CF4
COUNT_ADDRESS = 0x332E4BC
OTHER_BASE = 0x3358E1F
PE_MAGIC = b"PE\x00\x00"
OBSERVED_PREFIXES = ("adrn_", "real_", "spradrn_", "spr_")
NEIGHBOR_WINDOW_BEFORE = 9
NEIGHBOR_WINDOW_AFTER = 21

def pe_sections(data: bytes):
    pe = struct.unpack_from("<I", data, 0x3c)[0]
    if data[pe:pe+4] != PE_MAGIC:
        raise ValueError("not-original-pe")
    number, optional_len = struct.unpack_from("<H",data,pe+6)[0],struct.unpack_from("<H",data,pe+20)[0]
    optional = pe+24
    if struct.unpack_from("<H",data,optional)[0] != 0x10b:
        raise ValueError("not-pe32")
    image_base=struct.unpack_from("<I",data,optional+28)[0]
    size_of_image=struct.unpack_from("<I",data,optional+56)[0]
    sections=[]
    for k in range(number):
        at=optional+optional_len+k*40
        name=data[at:at+8].rstrip(b"\0").decode("ascii","replace")
        virt_size,virt_rva,raw_size,raw_offset=struct.unpack_from("<IIII",data,at+8)
        characteristics=struct.unpack_from("<I",data,at+36)[0]
        sections.append(dict(name=name,virtual_size=virt_size,virtual_rva=virt_rva,
                             raw_size=raw_size,raw_offset=raw_offset,
                             executable=bool(characteristics&0x20000000),
                             writable=bool(characteristics&0x80000000)))
    return image_base,size_of_image,sections

def section_for_va(image_base, sections, address):
    matches=[]
    for s in sections:
        start=image_base+s["virtual_rva"]
        end=start+max(s["virtual_size"],s["raw_size"])
        if start<=address<end:
            offset=address-start
            matches.append({
                "section":s["name"],"section_offset":offset,
                "backed_by_file_at_same_section_offset":offset<s["raw_size"],
                "writable":s["writable"],"executable":s["executable"]
            })
    return matches

def nearest_context(instructions, at, before=NEIGHBOR_WINDOW_BEFORE, after=NEIGHBOR_WINDOW_AFTER):
    for k,ins in enumerate(instructions):
        if ins["address"]<=at<ins["address"]+ins["encoded_length"]:
            section=instructions[max(0,k-before):k+after+1]
            return {"decoded_instruction_va":ins["address"],
                    "instruction":ins["instruction"],
                    "context":[{"va":x["address"],"ins":x["instruction"]} for x in section]}
    return {"decoded_instruction_va":None,"instruction":None,"context":[]}

def immediate_refs(instructions, original_va, radius=0):
    """Record only literal hex values in instructions; not data-flow proof."""
    refs=[]
    for ins in instructions:
        for token in re.findall(r"0x[0-9a-fA-F]+",ins["instruction"]):
            value=int(token,16)
            if original_va-radius<=value<=original_va+radius:
                refs.append({"instruction_va":ins["address"],"referenced_literal":value,
                             "relative_offset":value-original_va,
                             "instruction":ins["instruction"]})
    return refs

def inspect(program_path: Path):
    data=program_path.read_bytes()
    if (len(data),hashlib.sha256(data).hexdigest())!=EXPECTED["sa_5000.exe"]:
        raise ValueError("original-source-program-sha-mismatch")
    source_rows(data)
    old=json.loads(M_RECEIPT.read_text("utf-8"))
    if old["source_sha256"]!=EXPECTED["sa_5000.exe"][1]:
        raise ValueError("original-source-receipt-inconsistent")
    image_base, image_size, sections=pe_sections(data)
    xrefs=exact_pointer_literals(data,TABLE_OFFSET)
    if [x["file_offset"] for x in xrefs["literal_va_locations"]]!=list(PINNED_OFFSETS):
        raise ValueError("pet126m-three-xrefs-differ")
    for x in xrefs["literal_va_locations"]:
        if struct.unpack_from("<I",data,x["file_offset"])[0]!=image_base+xrefs["table_rva"]:
            raise ValueError("original-table-pointer-mismatch")
    command=["objdump","-d","-M","intel","-j",".text",str(program_path)]
    result=subprocess.run(command,capture_output=True,text=True,timeout=90)
    if result.returncode:
        raise ValueError("binutils-objdump-failed")
    instr=parse_objdump(result.stdout)
    if len(instr)!=old["disassembly_instruction_count"]:
        raise ValueError("original-linear-disassembly-size-disagrees")
    old_sites=old["exact_original_table_address_literal_sites"]
    context=[]
    for x,prior in zip(xrefs["literal_va_locations"],old_sites):
        if x["file_offset"]!=prior["literal_file_offset"]:
            raise ValueError("old-source-pointer-position-disagrees")
        decoded=nearest_context(instr,image_base+x["rva"])
        if decoded["instruction"]!=prior["decoded_instruction_text"]:
            raise ValueError("old-source-decoded-instruction-disagrees")
        context.append({
            "literal_source_file_offset":x["file_offset"],
            "compiled_table_pointer_instruction":decoded["instruction"],
            "short_bounded_disassembly_context":decoded["context"]
        })
    anchor=next((x for x in context if x["literal_source_file_offset"]==200343),None)
    if not anchor:
        raise ValueError("no-native-pet-table-indexing-site")
    selected=[entry["ins"] for entry in anchor["short_bounded_disassembly_context"]]
    if not ("imul   ecx,ecx,0x1c" in selected and
            "lea    eax,[esi+esi*4]" in selected and "shl    eax,0x4" in selected):
        raise ValueError("prior-source-28x80-index-chain-not-replayed")
    if not any(re.search(r"\[eax\+0x3300cf4\]",i) for i in selected):
        raise ValueError("unknown-follow-on-memory-reference")
    regions={hex(v):section_for_va(image_base,sections,v)
             for v in (image_base+xrefs["table_rva"],RECORD_BASE,COUNT_ADDRESS,OTHER_BASE)}
    refs=immediate_refs(instr,RECORD_BASE,80)
    counts=immediate_refs(instr,COUNT_ADDRESS)
    near=[x for x in refs if x["relative_offset"]!=0]
    ref_sample=[{"instruction_va":x["instruction_va"],
                 "relative_offset":x["relative_offset"],"instruction":x["instruction"]}
                for x in refs[:75]]
    return {
        "schema":"stoneage.pet126n.cn50_compiled_name_to_unknown_80b_global_source_audit.r1",
        "date":"2026-11-21","active_module":"PET","scope":"CLASSIC_PC_ONLY",
        "provenance":"THIRD_PARTY_PRESERVED_CN50_PC_CAB_NOT_OFFICIAL_PRESSING_PROVEN",
        "source_original_program_bytes":len(data),
        "source_original_program_sha256":hashlib.sha256(data).hexdigest(),
        "source_compiled_table_sha256":old["compiled_name_table_sha256"],
        "source_CAB_sha256":old["source_cab_sha256"],
        "pe_image_base":image_base,"pe_size_of_image":image_size,
        "pe_sections":[{"name":s["name"],"virtual_size":s["virtual_size"],
                        "raw_size":s["raw_size"],"writable":s["writable"]} for s in sections],
        "key_va_section_resolution":regions,
        "bounded_three_original_xref_instruction_contexts":context,
        "unknown_record_base_0x3300cf4":{
            "literal_range_radius_bytes":80,
            "literal_references_in_linear_text":len(refs),
            "exact_base_references":sum(x["relative_offset"]==0 for x in refs),
            "neighboring_constant_references":len(near),
            "references_first_75":ref_sample,
            "reference_list_truncated":len(refs)>75
        },
        "album_row_count_global_0x332e4bc":{
            "literal_references_in_linear_text":len(counts),
            "instructions_first_20":counts[:20],
            "reference_list_truncated":len(counts)>20
        },
        "original_exe_ascii_resource_filename_prefixes":{
            prefix:len(re.findall(re.escape(prefix.encode("ascii")),data))
            for prefix in OBSERVED_PREFIXES
        },
        "source_findings":{
            "table_28_byte_row_read_confirmed":True,
            "first_i32_times_80_into_global_range_confirmed":True,
            "global_region_equals_disk_adrn_record_not_proven":True,
            "native_name_to_SPR_selector_proven":False,
            "original_game_executed":False,
            "official_server_pet_issuance_verified":False,
            "new_official_species":0,
        },
        "next":"Use targeted same-source initialization/writers into the 80-byte memory region and correlate original bitmap/SPR index loader only if concretely supported, otherwise stop at exact missing native selector; do not infer official live pets."
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--program",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    result=inspect(args.program)
    args.output.write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print("PET126N_SOURCE_CHECKED|ORIGINAL_EXE_SHA_VERIFIED|80B_RUNTIME_REGION_NOT_ASSUMED_ADRN|NO_OFFICIAL_ISSUANCE")

if __name__=="__main__":
    main()
