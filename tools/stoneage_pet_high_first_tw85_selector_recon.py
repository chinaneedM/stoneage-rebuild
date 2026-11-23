"""PET-HIGH-FIRST-08: source-hashed original TW85 PC album-selector code reconnaissance.

All original compressed/unpacked PE and full disassembly stay on the runner.
Only bounded instruction-derived metadata, file offsets and hashes are published.
A numeric value or xref never alone proves a pet/SPR selector or official release.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess

from tools.stoneage_pet126m_cn50_pe_album_xrefs import parse_objdump
from tools.stoneage_pet_high_first_tw85_native import MANIFEST, parse_pe, sha
from tools.stoneage_pet_high_first_tw85_lookup import load as load_album

PROGRAMS = ("sa.exe", "sb.exe", "sc.exe", "sd.exe")
BASE_GRAPHIC = 100250
SOURCE_GRADE = "UNVERIFIED_COMMUNITY_PRESERVED_CLAIMED_WAYI85_INSTALLER"
IMM_RE = re.compile(r"(?<![\w])0x([0-9a-fA-F]{2,8})(?![\w])")
TARGET_BOUND = 900


def pe_info(raw):
    if raw[:2] != b"MZ":
        raise ValueError("expected source PE")
    pe = struct.unpack_from("<I", raw, 0x3c)[0]
    if raw[pe:pe + 4] != b"PE\0\0":
        raise ValueError("expected PE marker")
    optional = pe + 24
    magic = struct.unpack_from("<H", raw, optional)[0]
    if magic != 0x10B:
        raise ValueError("expected PE32 not PE32+")
    imagebase = struct.unpack_from("<I", raw, optional + 28)[0]
    sections = parse_pe(raw)["sections"]
    return imagebase, sections


def file_offset_to_va(raw_offset, imagebase, sections):
    for section in sections:
        start = section["file_offset"]
        if start <= raw_offset < start + section["raw_size"]:
            return imagebase + section["virtual_address"] + raw_offset - start, section["name"]
    raise ValueError("original album source file offset outside mapped PE section")


def source_identity(filename, orig, raw):
    if len(raw) != orig["size"] or sha(raw) != orig["sha256"]:
        raise ValueError("original source program bytes drifted: " + filename)


def window(parsed, index, radius=5):
    return [{"va": row["address"], "length": row["encoded_length"],
             "asm": row["instruction"][:130]} for row in parsed[max(0, index-radius):index+radius+1]]


def probe_one(folder, root, filename, album):
    src = next(f for f in root["inspection"]["inventory"]["samples"][0]["files"]
               if Path(f["path"]).name == filename)
    packed_file = folder / src["path"]
    compressed = packed_file.read_bytes()
    source_identity(filename, src, compressed)
    unpacked_file = folder / ("PET08_UNPACKED_" + filename)
    p = subprocess.run(["upx", "-d", "-q", "-o", str(unpacked_file), str(packed_file)],
                       capture_output=True, text=True, timeout=120)
    if p.returncode or not unpacked_file.is_file():
        raise ValueError("original UPX static decoder failed for "+filename+": "+p.stderr[-350:])
    raw = unpacked_file.read_bytes()
    if not 100_000 <= len(raw) <= 4_000_000:
        raise ValueError("unpacked PE size source bounds failed")
    imagebase, sections = pe_info(raw)
    first=album["programs"][filename]["source_records"][0]
    start=album["programs"][filename]["grid_first_byte"]
    if sha(raw[start:start+28]) != first["original_row_sha256"]:
        raise ValueError("source table anchor SHA mismatch in new static unpack")
    table_va, table_section = file_offset_to_va(start, imagebase, sections)
    table_end_va = table_va + 28 * album["programs"][filename]["total_grid_slots"]
    static= subprocess.run(["objdump", "-d", "-M", "intel", "-w", str(unpacked_file)],
                           capture_output=True, text=True, timeout=100)
    if static.returncode:
        raise ValueError("objdump failed on verified original PE file "+filename)
    code = parse_objdump(static.stdout)
    if len(code) < 5000:
        raise ValueError("unexpectedly sparse original code disassembly")

    refs = []
    magic = []
    for i, row in enumerate(code):
        vals={int(n,16) for n in IMM_RE.findall(row["instruction"])}
        if not vals:
            continue
        matching = sorted(v for v in vals if table_va - 256 <= v <= table_end_va + 256)
        magic_ref = any(BASE_GRAPHIC - 3 <= v <= BASE_GRAPHIC + 3 for v in vals)
        if matching:
            refs.append((i, matching, row["address"]))
        if magic_ref:
            magic.append((i, sorted(v for v in vals if BASE_GRAPHIC -3 <= v <= BASE_GRAPHIC+3),row["address"]))
    exact_refs=[(i,v,a) for i,v,a in refs if any(abs(target-table_va) <= 32 for target in v)]
    # Avoid dumping whole source program, retain short diagnostic instruction context
    return {
        "name": filename,
        "packed_exe_sha256": src["sha256"],
        "unpacked_exe_sha256": sha(raw),
        "unpacked_exe_bytes": len(raw),
        "image_base": imagebase,
        "album_source_first_file_offset": start,
        "album_source_first_va": table_va,
        "album_source_section": table_section,
        "album_source_last_va_exclusive": table_end_va,
        "album_source_first_28byte_sha256": first["original_row_sha256"],
        "disassembled_instruction_count": len(code),
        "album_range_immediate_refs_count": len(refs),
        "album_first_32bytes_immediate_refs_count": len(exact_refs),
        "base_graphic_100250_nearby_literals_count": len(magic),
        "album_first_immediate_ref_windows": [
            {"ref_instruction_va": a, "immediate_values": v,"instructions":window(code,i,5)}
            for i,v,a in exact_refs[:14]],
        "other_album_range_ref_windows": [
            {"ref_instruction_va": a, "immediate_values": v,"instructions":window(code,i,3)}
            for i,v,a in refs if not any(abs(target-table_va) <= 32 for target in v)][:14],
        "graphic_base_ref_windows": [
            {"ref_instruction_va": a, "immediate_values": v,"instructions":window(code,i,7)}
            for i,v,a in magic[:16]],
        "full_source_program_execution": False,
        "native_path_proved": False,
        "official_pet_release_verified": False,
    }


def selftest():
    example=[{"file_offset":512, "raw_size":128,"virtual_address":0x2000,"name":".rdata"}]
    assert file_offset_to_va(516, 0x400000, example)==(0x402004,".rdata")
    assert "0x1879a" in "cmp eax,0x1879a"
    assert int("1879a",16)==100250
    assert [int(n,16) for n in IMM_RE.findall("cmp eax,0x1879a")] == [100250]
    assert not IMM_RE.findall("0xsomething")
    print("PET08_SELECTOR_SELFTEST_PASS",flush=True)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source-root",type=Path)
    p.add_argument("--output",type=Path)
    p.add_argument("--self-test",action="store_true")
    p.add_argument("--log-json",action="store_true")
    a=p.parse_args()
    if a.self_test:
        selftest()
        return
    if not a.source_root or not a.output:
        p.error("--source-root and --output required")
    original = json.loads(MANIFEST.read_text(encoding="utf-8"))
    album=load_album()
    report={"schema":"stoneage.pet.high_first_08.original_pe_native_selector_recon.r1",
            "source_grade":SOURCE_GRADE,
            "input_original_exe_source_verified":True,
            "original_exe_or_game_executed":False,
            "native_name_to_spr_selector_verified":False,
            "files":[]}
    for filename in PROGRAMS:
        item=probe_one(a.source_root,original,filename,album)
        report["files"].append(item)
        print("PET08_SOURCE_PROBE "+json.dumps({
            k:item[k] for k in ("name","album_source_first_va","album_range_immediate_refs_count",
                                "album_first_32bytes_immediate_refs_count",
                                "base_graphic_100250_nearby_literals_count","disassembled_instruction_count")
        },sort_keys=True),flush=True)
    report["summary"]={
        "original_verified_exes":len(report["files"]),
        "total_album_range_code_immediate_refs":sum(f["album_range_immediate_refs_count"] for f in report["files"]),
        "total_graphic_base_code_immediate_refs":sum(f["base_graphic_100250_nearby_literals_count"] for f in report["files"]),
        "native_spr_to_name_mapping_proven_count":0,
        "official_live_pet_issuance_proven_count":0}
    output=(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+"\n").encode()
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_bytes(output)
    print("PET08_REPORT_SHA256="+sha(output),flush=True)
    print("PET08_REPORT_SUMMARY="+json.dumps(report["summary"],sort_keys=True),flush=True)
    if a.log_json:
        data=base64.b64encode(output).decode("ascii")
        print("PET08_BASE64_START",flush=True)
        for i in range(0,len(data),2600):
            print("PET08_B64 "+data[i:i+2600],flush=True)
        print("PET08_BASE64_END",flush=True)


if __name__=="__main__":
    main()
