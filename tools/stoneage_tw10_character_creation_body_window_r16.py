"""Bounded source-byte audit of the Taiwan 1.0 create-character body writer.

Outputs numeric metadata, never executable or graphic assets. A candidate
32-dword window is NOT an authenticated 32-entry table or character roster.
"""
from __future__ import annotations
import argparse
import csv
import gzip
import hashlib
import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXE_SHA256 = "cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a"
EXE_LENGTH = 425984
BASE = 0x400000
TABLE_VA = 0x458e28
READ_RVA = 71013
WRITE_RVA = 71038
BODY_GLOBAL_RVA = 20934812
FACE_GLOBAL_RVA = 20936876
GROUP_SHA256 = "4db7809de4197eb90cca6dc04bda8550025e022c8232e2ebb902db0e9faf0175"
GROUP_FILE = ROOT / "research/recovered/tw10-resource-metadata/SPR-GROUP-R1.tsv.gz"

def require(condition, message):
    if not condition:
        raise ValueError(message)

def source_groups():
    data = GROUP_FILE.read_bytes()
    require(hashlib.sha256(data).hexdigest() == GROUP_SHA256, "original SPR metadata drift")
    with gzip.open(GROUP_FILE, "rt", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    require(len(rows) == 464, "original SPR groups drift")
    groups = [int(r["spr_no"]) for r in rows]
    require(len(set(groups)) == len(groups), "duplicate group keys")
    return set(groups)

def classify_window(values, groups):
    """Bounded, not a claim about native array size or actual selected index."""
    require(len(values) == 32 and all(isinstance(v, int) and 0 <= v <= 0xffffffff for v in values), "invalid window")
    out = []
    for i, value in enumerate(values):
        out.append({
            "relative_index": i, "dword": value,
            "matches_original_spr_group_key": value in groups,
            "within_compiled_animation_key_interval": 100000 <= value <= 132767,
            "within_original_bitmap_number_envelope": value <= 125995,
            "runtime_selected_index_verified": False,
            "same_build_role_or_portrait_verified": False,
        })
    return out

def inspect(exe):
    require(len(exe) == EXE_LENGTH and hashlib.sha256(exe).hexdigest() == EXE_SHA256, "wrong original TW1.0 executable")
    # The accepted TW1.0 PE file has RVA-aligned original code/table bytes here.
    from tools.stoneage_tw10_mapcache_binary_probe import image_layout, rva_to_offset
    from capstone import Cs, CS_ARCH_X86, CS_MODE_32
    from capstone.x86 import X86_OP_MEM, X86_OP_REG
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "sa_3.exe"
        p.write_bytes(exe)
        data, pe, base, sections, imports = image_layout(p)
    require(base == BASE, "unexpected original PE image base")
    def at(rva, size):
        offset = rva_to_offset(sections, rva)
        require(offset is not None and offset >= 0 and offset + size <= len(exe), "not entirely file backed")
        return exe[offset:offset + size]
    md = Cs(CS_ARCH_X86, CS_MODE_32)
    md.detail = True
    def one(rva):
        decoded = list(md.disasm(at(rva, 12), BASE + rva, count=1))
        require(len(decoded) == 1, "missing bounded original x86 instruction")
        return decoded[0]
    source = one(READ_RVA)
    require(source.mnemonic == "mov" and len(source.operands) == 2, "changed indexed source instruction")
    dst, src = source.operands
    require(dst.type == X86_OP_REG and source.reg_name(dst.reg) == "esi", "changed body-register source")
    require(src.type == X86_OP_MEM and src.mem.base == 0 and source.reg_name(src.mem.index) == "ecx"
            and src.mem.scale == 4 and src.mem.disp == TABLE_VA, "changed source table operand")
    sink = one(WRITE_RVA)
    require(sink.mnemonic == "mov" and len(sink.operands) == 2, "changed body-global store")
    require(sink.operands[0].type == X86_OP_MEM
            and sink.operands[0].mem.base == 0 and sink.operands[0].mem.index == 0
            and sink.operands[0].mem.disp == BASE + BODY_GLOBAL_RVA, "changed body destination")
    require(sink.operands[1].type == X86_OP_REG
            and sink.reg_name(sink.operands[1].reg) == "esi", "changed stored register")
    values = list(struct.unpack("<32I", at(TABLE_VA - BASE, 128)))
    groups = source_groups()
    candidates = classify_window(values, groups)
    return {
        "schema": "stoneage.tw10.character_creation_body_static_window.r16",
        "task": "ORIGINAL-CHARACTER-CREATION-CONTENT-16",
        "primary_source": {
            "identity": "TW10_ACCEPTED_RETAIL_SA_3_EXE",
            "sha256": EXE_SHA256, "bytes": EXE_LENGTH,
            "source_spr_group_gzip_sha256": GROUP_SHA256,
            "source_spr_group_count": len(groups),
        },
        "byte_anchors": {
            "table_operand_virtual_address": TABLE_VA,
            "table_base_rva": TABLE_VA - BASE,
            "indexed_read_rva": READ_RVA,
            "indexed_read_instruction_sha256": hashlib.sha256(at(READ_RVA, source.size)).hexdigest(),
            "body_global_store_rva": WRITE_RVA,
            "body_store_instruction_sha256": hashlib.sha256(at(WRITE_RVA, sink.size)).hexdigest(),
            "create_message_body_global_rva": BODY_GLOBAL_RVA,
            "create_message_face_global_rva": FACE_GLOBAL_RVA,
        },
        "bounded_window": {
            "starting_at_referenced_address": True,
            "sampled_dwords": 32, "actual_table_extent_verified": False,
            "index_upper_bound_verified": False,
            "actual_index_value_verified": False,
            "window_sha256": hashlib.sha256(at(TABLE_VA - BASE, 128)).hexdigest(),
            "values": candidates,
        },
        "findings": {
            "sampled_group_key_matches": sum(x["matches_original_spr_group_key"] for x in candidates),
            "sampled_animation_interval_members": sum(x["within_compiled_animation_key_interval"] for x in candidates),
            "selected_body_number": None,
            "selected_face_number": None,
            "selected_spr_group": None,
            "selected_bitmap": None,
            "original_character_count": None,
            "table_covers_every_character": False,
            "original_character_roster_verified": False,
            "original_client_executed": False,
            "server_create_accepted": False,
        },
        "limits": [
            "Static table read and global write are same-function syntactic observations, not complete control-flow or same-input runtime proof",
            "32 dwords are a bounded file-byte window, NOT an authenticated table length or valid index domain",
            "A numeric SPR-key coincidence does not certify selectable player identity, portrait, face, color or character count",
            "JSS2001/other-region character counts cannot be projected back onto TW1.0",
        ],
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--bin", type=Path, required=True, help="Accepted STONEAGE.bin disc member")
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    from tools.stoneage_tw10_technical_probe import find_rows, extract_row
    import tempfile
    image, rows, _, _ = find_rows(args.bin)
    try:
        target = next(r for r in rows if r["path"] == "StoneAge/sa_3.exe" and not r["is_dir"])
        with tempfile.TemporaryDirectory() as td:
            f = Path(td) / "sa_3.exe"
            extract_row(image, target, f)
            report = inspect(f.read_bytes())
    finally:
        image.close()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print("SOURCE_WINDOW_SHA256=" + report["bounded_window"]["window_sha256"])
    print("SPR_KEY_HITS=" + str(report["findings"]["sampled_group_key_matches"]))
    print("DERIVED_REPORT_SHA256=" + hashlib.sha256(args.output.read_bytes()).hexdigest())

if __name__ == "__main__":
    main()
