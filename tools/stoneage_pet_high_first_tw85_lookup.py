"""Lookup source-qualified Taiwan 8.5 preserved-PC program album rows.

This does NOT enumerate actual official pet species or server Pet IDs.
"""
import argparse
import json
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / "research/pets/PET-HIGH-FIRST-TW85-ORIGINAL-PE-ALBUM-GRID-R1.json"


def load():
    report = json.loads(PATH.read_text(encoding="utf-8"))
    if (report["schema"] != "stoneage.pet.high_first_07.tw85_original_program_albums.r1"
            or not report["negative_evidence"]["counts_are_local_compiled_rows_not_unique_pet_species"]
            or report["measurements_not_official_species"]["official_live_species_confirmed_by_this_report"]):
        raise ValueError("album source grade mismatch")
    return report


def query(report, *, name="", original_i32=None, program=None, limit=100):
    rows = []
    for filename, info in report["programs"].items():
        if program and filename != program:
            continue
        for row in info["source_records"]:
            if name and name.casefold() not in row["original_name_cp950"].casefold():
                continue
            if original_i32 is not None and row["original_first_i32"] != original_i32:
                continue
            rows.append({"source_program": filename,
                         "source_grade": report["historical_source_scope"],
                         "official_live_pet_id_verified": False, **row})
            if len(rows) >= limit:
                return rows
    return rows


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--query", default="")
    p.add_argument("--original-i32", type=int)
    p.add_argument("--program", choices=("sa.exe", "sb.exe", "sc.exe", "sd.exe"))
    p.add_argument("--limit", type=int, default=100)
    p.add_argument("--summary", action="store_true")
    a = p.parse_args()
    if not 1 <= a.limit <= 2000:
        p.error("limit must be 1-2000")
    data = load()
    if a.summary:
        print(json.dumps(data["measurements_not_official_species"], ensure_ascii=False, indent=2))
    else:
        print(json.dumps(query(data, name=a.query, original_i32=a.original_i32,
                              program=a.program, limit=a.limit), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
