#!/usr/bin/env python3
"""Bounded Taiwan 1.0 savedata instruction-word analysis (no execution).

Four literal address words in the accepted sa_3.exe .text were not decoded as
direct references by the earlier linear sweep. Try *every* x86 instruction
start within 15 bytes of each word, and distinguish alternative alignment
from independently reached code. All outputs are derived offsets/counts;
neither bytes nor disassembly operands are published.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import struct
import tempfile
from pathlib import Path

from capstone import Cs, CS_ARCH_X86, CS_MODE_32
from capstone.x86 import X86_OP_IMM
from tools.stoneage_tw10_technical_probe import find_rows, extract_row
from tools.stoneage_tw10_mapcache_binary_probe import (
    image_layout, imported_call, referenced_absolute_values, rva_to_offset
)
from tools.stoneage_tw10_savedata_probe import (
    RUNTIME_PATH, SAVEDATA_PATH, NEEDLE, FILE_APIS, text_instructions, offset_to_rva
)

RUNTIME_SHA256 = "cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a"
SAVEDATA_SHA256 = "5b26f54a9723cd2c5275f964457094fdf1fc33ca086cdaf55bb5350dfb04f3f9"
WORD_RVAS = (0x40065, 0x400e5, 0x40116, 0x402a1)
EXPECTED_STRING_RVA = 0x63634
MAX_X86_BYTES = 15
FOLLOW_BYTES = 64


def verify_hash(data: bytes, expected: str, label: str) -> None:
    actual = hashlib.sha256(data).hexdigest()
    if actual != expected:
        raise ValueError(f"{label} SHA256 mismatch: refusing cross-version inference")


def validate_word(data: bytes, sections: list, word_rva: int, target_va: int) -> int:
    """Assert that a *raw-backed* four-byte word matches the target address."""
    offset = rva_to_offset(sections, word_rva)
    sec = next((s for s in sections if
                s["rva"] <= word_rva and word_rva + 4 <= s["rva"] + s["raw_size"]), None)
    if offset is None or sec is None or sec["name"] != ".text":
        raise ValueError("word not completely raw-backed by .text")
    if offset + 4 > len(data) or struct.unpack_from("<I", data, offset)[0] != target_va:
        raise ValueError("four-byte target address mismatch")
    return offset


def candidate_instructions(raw: bytes, base: int, text_rva: int,
                           word_rva: int, target_va: int):
    """Possible single x86 instructions containing all four address bytes.

    Independent code reachability is NOT proved by alternative disassembly.
    """
    if not (text_rva <= word_rva and word_rva + 4 <= text_rva + len(raw)):
        raise ValueError("word outside raw .text")
    md = Cs(CS_ARCH_X86, CS_MODE_32)
    md.detail = True
    matches = []
    for start in range(max(text_rva, word_rva - MAX_X86_BYTES + 1), word_rva + 1):
        rel = start - text_rva
        decoded = list(md.disasm(raw[rel:rel + MAX_X86_BYTES], base + start, count=1))
        if not decoded:
            continue
        ins = decoded[0]
        end = start + ins.size
        if word_rva >= start and word_rva + 4 <= end and target_va in referenced_absolute_values(ins):
            matches.append({"start": start, "end": end, "mnemonic": ins.mnemonic,
                            "word_operand_offset": word_rva - start})
    return tuple(matches)


def linear_overlap(insns, base: int, word_rva: int):
    """Summarize linear decoding near a word, without claiming true alignment."""
    overlapping = [ins for ins in insns
                   if ins.address - base < word_rva + 4
                   and ins.address + ins.size - base > word_rva]
    whole = [i for i in overlapping if i.address - base <= word_rva
             and i.address + i.size - base >= word_rva + 4]
    return (len(overlapping), len(whole),
            int(any(i.address-base == word_rva for i in overlapping)))


def incoming_direct_targets(insns):
    """Count *linear-sweep* direct branch targets (unvalidated reachability)."""
    result = collections.Counter()
    for ins in insns:
        if not (ins.mnemonic in ("call", "jmp") or ins.mnemonic.startswith("j")):
            continue
        for op in ins.operands:
            if op.type == X86_OP_IMM:
                result[int(op.imm) & 0xffffffff] += 1
    return result


def adjacent_file_api(raw, base, text_rva, start_rva, imports):
    """Candidate-local forward 64-byte decode; NOT a proved control-flow graph."""
    rel = start_rva - text_rva
    md = Cs(CS_ARCH_X86, CS_MODE_32)
    md.detail = True
    apis = collections.Counter()
    if not 0 <= rel < len(raw):
        return apis
    for ins in md.disasm(raw[rel:rel + FOLLOW_BYTES], base + start_rva):
        found = imported_call(ins, imports)
        if found and found[1] in FILE_APIS:
            apis[found] += 1
    return apis


def probe(runtime: bytes, saved: bytes):
    verify_hash(runtime, RUNTIME_SHA256, "sa_3.exe")
    verify_hash(saved, SAVEDATA_SHA256, "savedata.dat")
    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "sa_3.exe"
        path.write_bytes(runtime)
        data, pe, base, sections, imports = image_layout(path)
    matches = []
    for off in range(len(data)):
        if data.startswith(NEEDLE, off):
            matches.append(off)
    if len(matches) != 1:
        raise ValueError("ambiguous savedata path location")
    string_rva, string_section = offset_to_rva(sections, matches[0])
    if string_rva != EXPECTED_STRING_RVA or string_section != ".data":
        raise ValueError("savedata path provenance differs from accepted baseline")
    target_va = base + string_rva
    text_sec, insns = text_instructions(data, base, sections)
    raw = data[text_sec["raw"]:text_sec["raw"] + text_sec["raw_size"]]
    incoming = incoming_direct_targets(insns)
    linear_starts = {ins.address - base for ins in insns}

    print("StoneAge Taiwan v1.0 savedata instruction alignment probe — R3")
    print("SCOPE|accepted-clean-disc|four-address-words|static-alignment-only|derived-metadata")
    print(f"IDENTITY|runtime_sha256={RUNTIME_SHA256}|savedata_sha256={SAVEDATA_SHA256}")
    print(f"PATH|string_rva=0x{string_rva:x}|target_va=0x{target_va:x}|section={string_section}")
    count = 0
    for n, word_rva in enumerate(WORD_RVAS, 1):
        validate_word(data, sections, word_rva, target_va)
        overlap, whole, start_at_word = linear_overlap(insns, base, word_rva)
        possibilities = candidate_instructions(raw, base, text_sec["rva"], word_rva, target_va)
        print(f"WORD|n={n}|rva=0x{word_rva:x}|linear_overlap={overlap}|"
              f"linear_whole={whole}|linear_start_at_word={start_at_word}|"
              f"alternate_ref_candidates={len(possibilities)}")
        for k, row in enumerate(possibilities, 1):
            count += 1
            addr = base + row["start"]
            api = adjacent_file_api(raw, base, text_sec["rva"], row["start"], imports)
            print(f"CANDIDATE|word={n}|n={k}|start_rva=0x{row['start']:x}|"
                  f"end_rva=0x{row['end']:x}|mnemonic={row['mnemonic']}|"
                  f"word_operand_offset={row['word_operand_offset']}|"
                  f"linear_start_match={int(row['start'] in linear_starts)}|"
                  f"linear_incoming_direct_edges={incoming[addr]}|"
                  f"forward_64_file_api_count={sum(api.values())}")
            for (dll, name), hits in sorted(api.items()):
                print(f"FORWARD_API|word={n}|candidate={k}|dll={dll}|name={name}|count={hits}")
    print(f"COUNT|word_sites={len(WORD_RVAS)}|alignment_candidates={count}")
    print("BOUNDARY|Four matching address words and alternate decodings are static facts;"
          " actual instruction alignment, indirect callsites, savedata IO reachability,"
          " early client framing/checksum and runtime persistence remain OPEN.")
    print("RESOLUTION|TW10_SAVEDATA_FOUR_WORD_ALIGNMENT_SURFACE_ONLY")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bin", required=True, help="verified StoneAge Taiwan v1.0 BIN")
    args = parser.parse_args()
    img, rows, _, _ = find_rows(args.bin)
    try:
        files = {x["path"]: x for x in rows if not x["is_dir"]}
        if RUNTIME_PATH not in files or SAVEDATA_PATH not in files:
            raise ValueError("accepted baseline files missing")
        with tempfile.TemporaryDirectory() as td:
            exe = Path(td) / "sa_3.exe"
            state = Path(td) / "savedata.dat"
            extract_row(img, files[RUNTIME_PATH], exe)
            extract_row(img, files[SAVEDATA_PATH], state)
            probe(exe.read_bytes(), state.read_bytes())
    finally:
        img.close()


if __name__ == "__main__":
    main()
