#!/usr/bin/env python3
"""Strict grammar and identity guard for derived TW1.0 R3 instruction reports.

This validator NEVER reads the old executable, save file or disc. It rejects
any unexpected report line and never promotes candidates to runtime facts.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
import re

from tools.stoneage_tw10_savedata_instruction_probe import (
    RUNTIME_SHA256, SAVEDATA_SHA256, WORD_RVAS, EXPECTED_STRING_RVA
)

TITLE = "StoneAge Taiwan v1.0 savedata instruction alignment probe — R3"
SCOPE = "SCOPE|accepted-clean-disc|four-address-words|static-alignment-only|derived-metadata"
RESOLUTION = "RESOLUTION|TW10_SAVEDATA_FOUR_WORD_ALIGNMENT_SURFACE_ONLY"
PREFIXES = ("IDENTITY","PATH","WORD","CANDIDATE","FORWARD_API","COUNT")
EXPECTED_FIELDS = {
    "IDENTITY": {"runtime_sha256","savedata_sha256"},
    "PATH": {"string_rva","target_va","section"},
    "WORD": {"n","rva","linear_overlap","linear_whole",
             "linear_start_at_word","alternate_ref_candidates"},
    "CANDIDATE": {"word","n","start_rva","end_rva","mnemonic","word_operand_offset",
                  "linear_start_match","linear_incoming_direct_edges",
                  "forward_64_file_api_count"},
    "FORWARD_API": {"word","candidate","dll","name","count"},
    "COUNT": {"word_sites","alignment_candidates"}
}
SAFE_VALUE = re.compile(r"^[A-Za-z0-9_.-]+$")
MAX_REPORT_BYTES = 25000
MAX_CANDIDATES = 100


def fields(line: str) -> tuple[str, dict[str, str]]:
    label, *entries = line.split("|")
    if label not in PREFIXES:
        raise ValueError("unexpected report row")
    info = {}
    for entry in entries:
        if "=" not in entry:
            raise ValueError("non-field report content")
        k, v = entry.split("=",1)
        if (not SAFE_VALUE.fullmatch(k) or
                not SAFE_VALUE.fullmatch(v) or k in info):
            raise ValueError("invalid/duplicate report field")
        info[k] = v
    if set(info) != EXPECTED_FIELDS[label]:
        raise ValueError("invalid report schema")
    return label, info


def number(item: str, maximum: int=1_000_000):
    if not re.fullmatch(r"(?:0x[0-9a-f]+|[0-9]+)", item):
        raise ValueError("invalid numeric report field")
    value = int(item, 16) if item.startswith("0x") else int(item)
    if not 0 <= value <= maximum:
        raise ValueError("unbounded report integer")
    return value


def validate(text: str):
    if len(text.encode("utf-8")) > MAX_REPORT_BYTES:
        raise ValueError("oversized report")
    rows = text.strip().splitlines()
    if len(rows) < 10 or rows[0] != TITLE or rows[1] != SCOPE:
        raise ValueError("report header/coverage mismatch")
    if (rows[-1] != RESOLUTION or
            not rows[-2].startswith("BOUNDARY|Four matching address words")):
        raise ValueError("missing explicit non-runtime resolution and caveat")
    parsed = [fields(row) for row in rows[2:-2]]
    counts = Counter(k for k, _ in parsed)
    for tag in ("IDENTITY","PATH","COUNT"):
        if counts[tag] != 1:
            raise ValueError(f"{tag} row cardinality")
    if counts["WORD"] != 4 or counts["CANDIDATE"] > MAX_CANDIDATES:
        raise ValueError("word/candidate count")
    rowmap = {k:[d for tag,d in parsed if tag==k] for k in PREFIXES}
    identity = rowmap["IDENTITY"][0]
    if identity["runtime_sha256"] != RUNTIME_SHA256 or identity["savedata_sha256"] != SAVEDATA_SHA256:
        raise ValueError("unrecognized original hash pins")
    path = rowmap["PATH"][0]
    if (number(path["string_rva"]) != EXPECTED_STRING_RVA or
            number(path["target_va"]) != 0x463634 or path["section"] != ".data"):
        raise ValueError("unrecognized original path target")
    sites = rowmap["WORD"]
    site_by_num = {}
    candidate_counts = {}
    for expected_num, (expected_rva, row) in enumerate(zip(WORD_RVAS, sites),1):
        n = number(row["n"])
        if n != expected_num or number(row["rva"]) != expected_rva:
            raise ValueError("missing/reordered four original address words")
        overlap = number(row["linear_overlap"])
        whole = number(row["linear_whole"])
        if whole > overlap or number(row["linear_start_at_word"]) > 1:
            raise ValueError("invalid linear alignment summary")
        candidate_counts[n] = number(row["alternate_ref_candidates"], MAX_CANDIDATES)
        site_by_num[n] = expected_rva
    candidates = {}
    for row in rowmap["CANDIDATE"]:
        word, n = number(row["word"]), number(row["n"])
        if word not in site_by_num or (word,n) in candidates:
            raise ValueError("duplicate or unknown candidate key")
        rva = site_by_num[word]
        start,end = number(row["start_rva"]),number(row["end_rva"])
        if not (start <= rva and rva+4 <= end and 4 <= end-start <= 15):
            raise ValueError("invalid x86 instruction candidate window")
        if number(row["word_operand_offset"]) != rva-start:
            raise ValueError("incorrect operand position")
        if number(row["linear_start_match"]) > 1:
            raise ValueError("invalid boolean field")
        if not re.fullmatch(r"[a-z][a-z0-9]*",row["mnemonic"]):
            raise ValueError("unexpected mnemonic")
        number(row["linear_incoming_direct_edges"])
        number(row["forward_64_file_api_count"])
        candidates[(word,n)] = row
    for word, expected_count in candidate_counts.items():
        indices = {n for (w,n) in candidates if w==word}
        if indices != set(range(1,expected_count+1)):
            raise ValueError("candidate index/gap mismatch")
    file_api_count = Counter()
    for row in rowmap["FORWARD_API"]:
        word,n = number(row["word"]),number(row["candidate"])
        if (word,n) not in candidates:
            raise ValueError("API without corresponding candidate")
        if (not row["dll"].lower().endswith(".dll") or
                not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", row["name"])):
            raise ValueError("unknown API metadata shape")
        file_api_count[(word,n)] += number(row["count"])
    for key,row in candidates.items():
        if file_api_count[key] != number(row["forward_64_file_api_count"]):
            raise ValueError("forward API count mismatch")
    count = rowmap["COUNT"][0]
    if number(count["word_sites"]) != 4 or number(count["alignment_candidates"]) != len(candidates):
        raise ValueError("final report count mismatch")
    return {
        "schema":"tw10-savedata-r3-derived-report-guard-r1",
        "status":"DERIVED_FORMAT_AND_CUSTODY_ONLY",
        "runtime_sha256":RUNTIME_SHA256,
        "savedata_sha256":SAVEDATA_SHA256,
        "word_sites":4,
        "candidates":len(candidates),
        "forward_file_api_mentions":sum(file_api_count.values()),
        "actual_instruction_reachability_admitted":False,
        "original_128_byte_format_admitted":False,
        "contains_original_payload":False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--report",type=Path,required=True)
    args=parser.parse_args()
    print(json.dumps(validate(args.report.read_text(encoding="utf-8")),
                     sort_keys=True))


if __name__ == "__main__":
    main()
