#!/usr/bin/env python3
"""Summarize the large StoneAge 2.0 retail-carrier census report.

The raw census can exceed connector display limits. This parser emits only
strict IA/DiscMaster candidate rows, reported counts/errors and final
resolution so the recovery decision remains auditable without re-querying
external indexes.
"""
from __future__ import annotations
from pathlib import Path
import re

DEFAULT=Path("research/recovered/STONEAGE-SA20-RETAIL-CARRIER-CENSUS-R1.txt")

def parse(text:str):
    lines=text.splitlines()
    strict_ia=[x for x in lines if x.startswith("IA_HIT|") and "|strict=1|" in x]
    strict_dm=[x for x in lines if x.startswith("DM_HIT|") and "|strict=1|" in x]
    errors=[x for x in lines if x.startswith("ERROR|")]
    count_lines=[x for x in lines if x.startswith("COUNT|")]
    resolutions=[x for x in lines if x.startswith("RESOLUTION|")]
    targets=[x for x in lines if x.startswith("TARGET|")]
    return {
        "lines":len(lines),
        "strict_ia":strict_ia,
        "strict_dm":strict_dm,
        "errors":errors,
        "counts":count_lines,
        "resolutions":resolutions,
        "targets":targets,
    }

def main(path=DEFAULT):
    text=Path(path).read_text("utf-8",errors="replace")
    r=parse(text)
    print("StoneAge 2.0 retail client-disc census compact summary — R1")
    print(f"SOURCE|path={path}|bytes={Path(path).stat().st_size}|lines={r['lines']}")
    for x in r["targets"]: print(x)
    for x in r["counts"]: print(x)
    print(f"SUMMARY|strict_ia_rows={len(r['strict_ia'])}|strict_dm_rows={len(r['strict_dm'])}|errors={len(r['errors'])}")
    for i,x in enumerate(r["strict_ia"][:100],1): print(f"STRICT_IA|index={i}|row={x}")
    for i,x in enumerate(r["strict_dm"][:100],1): print(f"STRICT_DM|index={i}|row={x}")
    for i,x in enumerate(r["errors"][:100],1): print(f"ERROR_ROW|index={i}|row={x}")
    for x in r["resolutions"]: print(x)
    if len(r["strict_ia"])>100 or len(r["strict_dm"])>100 or len(r["errors"])>100:
        print("TRUNCATION|compact report caps each detailed class at 100 rows; aggregate counts remain complete")

if __name__=="__main__":
    main()
