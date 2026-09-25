#!/usr/bin/env python3
"""Summarize the large StoneAge 2.0 retail-carrier preservation census.

Keeps only audit-critical rows: header/scope/target, strict hits, aggregate
counts, errors and final resolution. This avoids treating a >1 MiB diagnostic
report as unreadable while preserving the exact raw report in the repository.
"""
from __future__ import annotations
from pathlib import Path

RAW=Path("research/recovered/STONEAGE-SA20-RETAIL-CARRIER-CENSUS-R1.txt")

KEEP_PREFIXES=(
    "StoneAge 2.0 retail client-disc preservation census",
    "SCOPE|",
    "TARGET|",
    "COUNT|",
    "ERROR|",
    "RESOLUTION|",
    "EVIDENCE_BOUNDARY|",
)

def keep(line:str)->bool:
    return (
        line.startswith(KEEP_PREFIXES)
        or ("|strict=1|" in line and line.startswith(("IA_HIT|","DM_HIT|")))
    )

def summarize(text:str)->str:
    rows=[line for line in text.splitlines() if keep(line)]
    return "\n".join(rows)+"\n"

def main():
    print(summarize(RAW.read_text(encoding="utf-8")),end="")

if __name__=="__main__":
    main()
