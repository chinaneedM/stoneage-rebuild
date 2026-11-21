#!/usr/bin/env python3
"""PET126M: bounded original mainland 5.0 PE32 .text table-address xref decoding.

Reads a private, source-hashed original executable without executing it.
Produces only short derived instruction-level metadata for the three confirmed
compiled pet-album table-address literals, NOT the original code or game assets.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
import subprocess
from pathlib import Path

from tools.stoneage_pet126l_cn50_table_graphic_probe import (
    EXPECTED, TABLE_OFFSET, source_rows, exact_pointer_literals,
)

ROOT = Path(__file__).resolve().parents[1]
PRIOR = ROOT / "research/recovered/STONEAGE-PET126L-CN50-COMPILED-NAME-SAME-CAB-KEY-AUDIT-R1.json"
PINNED_OFFSETS = (199700, 200343, 214772)
MAX_WINDOW = 5


def parse_objdump(text: str):
    """Parse GNU binutils Intel disassembly; reject empty/incomplete disassembly."""
    result = []
    for line in text.splitlines():
        match = re.match(r"^\s*([0-9a-fA-F]+):\s+((?:[0-9a-fA-F]{2}(?:[ \t]+|$))+)(.*)$", line)
        if not match:
            continue
        try:
            addr = int(match.group(1), 16)
            raw_bytes = bytes.fromhex(match.group(2))
        except ValueError:
            continue
        instruction = match.group(3).strip()
        if not raw_bytes or not instruction:
            continue
        # No original opcode bytes in the public result.
        result.append({"address": addr, "encoded_length": len(raw_bytes),
                       "instruction": instruction[:180]})
    if not result:
        raise ValueError("objdump-produced-no-usable-instructions")
    return result


def locate_xrefs(disassembly, xrefs, image_base):
    """Exact source literal positions vs section-address-aware linear disassembly."""
    index = {i["address"]: k for k,i in enumerate(disassembly)}
    matches = []
    for ref in xrefs:
        va = image_base + ref["rva"]
        containing = [
            i for i in disassembly
            if i["address"] <= va < i["address"] + i["encoded_length"]
        ]
        # Multiple overlapping linear decoded entries indicate ambiguity.
        if len(containing) != 1:
            matches.append({
                "literal_file_offset": ref["file_offset"], "literal_va": va,
                "decoded_instruction_count": len(containing),
                "instruction_attribution": "AMBIGUOUS_OR_UNPARSED",
                "context": []
            })
            continue
        instr = containing[0]
        offset_in_instruction = va - instr["address"]
        k = index[instr["address"]]
        context = []
        for e in disassembly[max(0, k - MAX_WINDOW):k + MAX_WINDOW + 1]:
            context.append({
                "virtual_address": e["address"],
                "instruction": e["instruction"],
                "contains_original_table_literal": e["address"] == instr["address"]
            })
        matches.append({
            "literal_file_offset": ref["file_offset"],
            "literal_va": va,
            "decoded_instruction_count": 1,
            "instruction_attribution": "SINGLE_LINEAR_DISASSEMBLY_INSTRUCTION",
            "decoded_instruction_virtual_address": instr["address"],
            "literal_offset_within_decoded_instruction": offset_in_instruction,
            "decoded_instruction_byte_length": instr["encoded_length"],
            "decoded_instruction_text": instr["instruction"],
            "context": context
        })
    return matches


def pe32_text_identity(program):
    pe = struct.unpack_from("<I", program, 0x3c)[0]
    if program[pe:pe + 4] != b"PE\x00\x00":
        raise ValueError("original-program-not-pe")
    section_count = struct.unpack_from("<H", program, pe + 6)[0]
    optional_len = struct.unpack_from("<H", program, pe + 20)[0]
    optional = pe + 24
    if struct.unpack_from("<H", program, optional)[0] != 0x10b:
        raise ValueError("not-PE32")
    image_base = struct.unpack_from("<I", program, optional + 28)[0]
    records = []
    for i in range(section_count):
        off = optional + optional_len + 40*i
        name = program[off:off + 8].rstrip(b"\x00").decode("ascii", "replace")
        length, rva, size, file_start = struct.unpack_from("<IIII",program,off + 8)
        records.append((name, rva, file_start, size))
    section = [x for x in records if x[0] == ".text"]
    if len(section) != 1:
        raise ValueError("not-one-text-section")
    return image_base,section[0]


def inspect(program_path: Path):
    program = program_path.read_bytes()
    if (len(program), hashlib.sha256(program).hexdigest()) != EXPECTED["sa_5000.exe"]:
        raise ValueError("original-program-SHA-invalid")
    source_rows(program)
    prior = json.loads(PRIOR.read_text(encoding="utf-8"))
    if prior["original_program_sha256"] != EXPECTED["sa_5000.exe"][1]:
        raise ValueError("prior-source-program-not-matching")
    xref = exact_pointer_literals(program,TABLE_OFFSET)
    if [x["file_offset"] for x in xref["literal_va_locations"]] != list(PINNED_OFFSETS):
        raise ValueError("prior-original-table-address-xrefs-do-not-replay")
    if xref["literal_rva_hits"] != 0:
        raise ValueError("unexpected-relative-address-reference")
    image_base, section = pe32_text_identity(program)
    if not all(section[2] <= x < section[2]+section[3] for x in PINNED_OFFSETS):
        raise ValueError("xref-outside-text")
    for x in xref["literal_va_locations"]:
        if struct.unpack_from("<I",program,x["file_offset"])[0] != image_base + x["rva"]:
            raise ValueError("original-address-literal-PE-mapping-failed")
    command = ["objdump","-d","-M","intel","-j",".text",str(program_path)]
    result = subprocess.run(command,capture_output=True,text=True,timeout=90)
    if result.returncode:
        raise ValueError("objdump-failed:"+result.stderr[-800:])
    instructions = parse_objdump(result.stdout)
    # GNU objdump addresses are PE image-base-relative VAs.
    matches = locate_xrefs(instructions,xref["literal_va_locations"],image_base)
    return {
        "schema":"stoneage.pet126m.cn50_pet_album_pe_text_reference_context.r1",
        "date":"2026-11-21","active_module":"PET","scope":"ORIGINAL_CLASSIC_PC_ONLY",
        "carrier":"STONEAGE5_THIRD_PARTY_PRESERVED_ORIGINAL_PC_CAB_NOT_INDEPENDENTLY_OFFICIAL_PRESSING_CERTIFIED",
        "source_file":"sa_5000.exe","source_sha256":EXPECTED["sa_5000.exe"][1],
        "compiled_name_table_sha256":prior["original_table_sha256"],
        "source_cab_sha256":prior["source_cab_sha256"],
        "pe_image_base":image_base,
        "source_text_section":{"rva":section[1],"raw_file_offset":section[2],
                               "raw_section_size":section[3]},
        "disassembler":"GNU_BINUTILS_OBJDUMP_INTEL_LINEAR_DISASSEMBLY",
        "disassembly_instruction_count":len(instructions),
        "exact_original_table_address_literal_sites":matches,
        "claims":{
            "full_pe_binary_hash_verified":True,"all_three_literal_positions_verified":True,
            "static_linear_disassembly_only_not_native_execution":True,
            "bytes_of_proprietary_program_published":False,
            "instruction_adjacent_window_not_control_flow_or_runtime_proof":True,
            "same_version_name_to_spr_selector_proven":False,
            "official_live_pet_release_proven":False,
            "new_official_species":0,
            "pet_module_closed":False,
        },
        "next":"Investigate actual compiled reads and caller/control-flow of the three short-context references only where decoder evidence is coherent; original same-deployment graphics identity and official live pet issuance remain independently unresolved."
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--program",required=True,type=Path)
    p.add_argument("--output",required=True,type=Path)
    args=p.parse_args()
    r=inspect(args.program)
    args.output.write_text(json.dumps(r,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("PET126M_STATIC_XREFS|"+str(len(r["exact_original_table_address_literal_sites"]))+
          "|never_executed|species_not_inferred")


if __name__=="__main__":
    main()
