"""PET08 finite source-code audit around local album selectors and sprite transforms.

Inspect hash-pinned, statically unpacked TW85 PC programs without execution.
Original programs, full disassembly and graphics never leave temporary runner.
"""
from __future__ import annotations

import argparse
import base64
from collections import Counter
import json
from pathlib import Path
import re
import subprocess

from tools.stoneage_pet126m_cn50_pe_album_xrefs import parse_objdump
from tools.stoneage_pet_high_first_tw85_native import MANIFEST, sha
from tools.stoneage_pet_high_first_tw85_lookup import load as load_album
from tools.stoneage_pet_high_first_tw85_selector_recon import (
    PROGRAMS, BASE_GRAPHIC, IMM_RE, file_offset_to_va, pe_info, source_identity,
)

SAVED = Path(__file__).resolve().parents[1]


def expected_instructions(code, addresses):
    """Source-constrained disassembly of exact addresses, not built-in assumptions."""
    return {x["address"]:x for x in code if x["address"] in addresses}


def excerpt(code, idx, before, after, maxlen=160):
    return [{"va": f"0x{x['address']:x}", "instruction":x["instruction"][:maxlen]}
            for x in code[max(idx-before,0):idx+after+1]]


def code_probe(src_root, name, manifest, album):
    entry = next(f for f in manifest["inspection"]["inventory"]["samples"][0]["files"]
                 if Path(f["path"]).name == name)
    packed = src_root / entry["path"]
    compressed = packed.read_bytes()
    source_identity(name, entry, compressed)
    dest = src_root / ("PET08_DEEP_UNPACKED_" + name)
    res = subprocess.run(["upx", "-d", "-q", "-o", str(dest),str(packed)],
                         capture_output=True, text=True, timeout=90)
    if res.returncode:
        raise RuntimeError("source UPX failed: " + res.stderr[-200:])
    raw=dest.read_bytes()
    base,sec=pe_info(raw)
    table=album["programs"][name]
    offset=table["grid_first_byte"]
    first=table["source_records"][0]
    if sha(raw[offset:offset+28])!=first["original_row_sha256"]:
        raise ValueError("unexpected original source row SHA")
    va,_=file_offset_to_va(offset,base,sec)
    rows=album["programs"][name]["total_grid_slots"]
    p=subprocess.run(["objdump","-d","-M","intel","-w",str(dest)],
                     capture_output=True,text=True, timeout=120)
    if p.returncode:
        raise ValueError("original source objdump failed")
    code=parse_objdump(p.stdout)
    exact=[]
    fieldrefs=[]
    graphic_lit=[]
    compare_threshold=[]
    for i,x in enumerate(code):
        values={int(s,16) for s in IMM_RE.findall(x["instruction"])}
        fields={v-va for v in values if va<=v<=va+28}
        if fields and (0 in fields or 4 in fields or 24 in fields):
            fieldrefs.append((i,x["address"],sorted(fields)))
        if BASE_GRAPHIC in values:
            graphic_lit.append((i,x["address"]))
        # CN50 original independently documented piecewise graph selector
        # constants; detect patterns instead of assuming shared code.
        if re.match(r"^(cmp|sub|add)\s+",x["instruction"]):
            selected=sorted(v for v in values if v in {
                0x4D7,0x4A2,0x494,0x489,0x3A2,0x3A1,0x39F,0x384,0xB4,
                0x379,0x376,0x36D,0x364,0x2E9,0x284,0x283,0x26D,0x185,
            })
            if selected:
                compare_threshold.append((i,x["address"],selected))
    for i,x in enumerate(code):
        if "imul" in x["instruction"] and "0x1c" in x["instruction"]:
            if any(abs(code[q]["address"]-x["address"])<70
                   for q,v,_ in fieldrefs):
                exact.append((i,x["address"],"imul_28_stride"))
        if re.search(r"lea\s+\w+,\[\w+\*8\+0x0\]",x["instruction"]):
            if any(abs(code[q]["address"]-x["address"])<70
                   for q,v,_ in fieldrefs):
                exact.append((i,x["address"],"lea_index8_stride"))
    # Capture only short subset for manual source investigation.
    important = sorted(set(i for i,_,_ in exact))[:12]
    tablepaths=[{"kind":reason,"va":f"0x{a:x}",
                 "disassembly":excerpt(code,i,34,44)}
                for i,a,reason in exact[:12]]
    thresholdsites=[{"va":f"0x{a:x}","constant":selected,
                     "disassembly":excerpt(code,i,13,17)}
                    for i,a,selected in compare_threshold[:22]]
    return {
        "file":name,
        "original_sha256":entry["sha256"],
        "unpacked_sha256":sha(raw),
        "table_first_va":f"0x{va:x}",
        "table_first_row_sha256":first["original_row_sha256"],
        "total_xrefs_to_table_fields_0_4_24":len(fieldrefs),
        "first_raw_table_field_xrefs":[{"va":f"0x{a:x}","field_offsets":f} for i,a,f in fieldrefs[:60]],
        "original_album_index_x28_code_sites":tablepaths,
        "native_selector_extended_source_windows": [
            {"kind":reason, "ref_va":f"0x{a:x}", "instructions":excerpt(code,i,145,55)}
            for i,a,reason in exact[:3]
        ],
        "graphic_base_100250_code_sites":[{"va":f"0x{a:x}", "disassembly":excerpt(code,i,28,28)}
                                           for i,a in graphic_lit[:4]],
        "CN50_piecewise_range_constants_in_source":len(compare_threshold),
        "candidate_threshold_instruction_windows":thresholdsites,
        "original_program_executed":False,
        "original_SPR_to_name_native_route_complete":False,
    }


def selftest():
    assert expected_instructions([{"address":17,"instruction":"x"}],{17})[17]["instruction"]=="x"
    assert expected_instructions([{"address":17,"instruction":"x"}],{18})=={}
    assert excerpt([{"address":1,"instruction":"a"}],0,3,3)[0]["instruction"]=="a"
    print("PET08_DEEP_SELFTEST_PASS",flush=True)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source-root",type=Path)
    p.add_argument("--output",type=Path)
    p.add_argument("--log-json",action="store_true")
    p.add_argument("--self-test",action="store_true")
    args=p.parse_args()
    if args.self_test:
        selftest()
        return
    if not args.source_root or not args.output:
        p.error("--source-root/--output required")
    manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
    album=load_album()
    results=[code_probe(args.source_root,name,manifest,album) for name in PROGRAMS]
    report={
        "schema":"stoneage.pet.high_first_08.native_pe_28byte_album_code_window_audit.r1",
        "source_grade":"UNVERIFIED_COMMUNITY_PRESERVED_CLAIMED_WAYI85_INSTALLER",
        "original_game_executed":False,
        "full_SPR_to_album_native_selector_proven":False,
        "files":results,
        "summary":{
            "all_four_PE_table_28byte_stride_confirmed":all(f["original_album_index_x28_code_sites"] for f in results),
            "verified_files":len(results),
            "total_table_field_xrefs":sum(f["total_xrefs_to_table_fields_0_4_24"] for f in results),
            "total_programs_with_source_100250_literal":sum(bool(f["graphic_base_100250_code_sites"]) for f in results),
            "official_pet_species_confirmed":0
        }}
    raw=(json.dumps(report,ensure_ascii=False,sort_keys=True,separators=(",",":"))+"\n").encode()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_bytes(raw)
    print("PET08_DEEP_SUMMARY="+json.dumps(report["summary"],sort_keys=True),flush=True)
    print("PET08_DEEP_SHA256="+sha(raw),flush=True)
    if args.log_json:
        enc=base64.b64encode(raw).decode()
        print("PET08_DEEP_B64_START")
        for start in range(0,len(enc),2600):
            print("PET08_DEEP_B64 "+enc[start:start+2600])
        print("PET08_DEEP_B64_END")


if __name__=="__main__":
    main()
