"""Lookup source-qualified Taiwan 8.5 preserved-PC program album rows.

This does NOT enumerate actual official pet species or server Pet IDs.
"""
import argparse
import gzip
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


def attach_visual_routes(rows):
    """Attach sampled pixels to the same executable and original 28-byte row."""
    from tools.stoneage_pet_high_first_tw85_pixels import PET09, SCOPE, TARGET

    atlas = json.loads(PET09.read_bytes())
    with gzip.open(TARGET, "rt", encoding="utf-8") as stream:
        receipt = json.load(stream)
    if receipt["scope"] != SCOPE:
        raise ValueError("unexpected TW85 visual receipt scope")
    animation_by_group = {row["physical_group"]: row for row in receipt["sequences"]}
    routes_by_row = {}
    for record in atlas["records"]:
        groups = record["original_physical_sprite_occurrences"]
        for program, route in record["original_native_program_routes"].items():
            if route["status"] != "SOURCE_LOCAL_NAMED_ROUTE":
                continue
            key = (program, route["local_album_slot"], route["original_28b_record_sha256"])
            routes_by_row.setdefault(key, []).extend({
                "spr": record["tw85_original_spr_no_not_official_pet_id"],
                "source_group_index": item["original_source_group_index"],
                "sample": animation_by_group.get(item["original_source_group_index"]),
            } for item in groups)
    for row in rows:
        key = (row["source_program"], row["slot"], row["original_row_sha256"])
        candidates = routes_by_row.get(key)
        if candidates:
            alias = str(row["source_portrait_alias"])
            row["original_visual_candidates"] = {
                "source_grade": SCOPE,
                "portrait_blocks": [receipt["observed_blocks"][str(index)]
                                    for index, _ in receipt["portraits_by_original_alias"][alias]],
                "sprite_groups": candidates,
            }
    return rows


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--query", default="")
    p.add_argument("--original-i32", type=int)
    p.add_argument("--program", choices=("sa.exe", "sb.exe", "sc.exe", "sd.exe"))
    p.add_argument("--limit", type=int, default=100)
    p.add_argument("--summary", action="store_true")
    p.add_argument("--visual", action="store_true", help="include verified portrait and action references")
    a = p.parse_args()
    if not 1 <= a.limit <= 2000:
        p.error("limit must be 1-2000")
    data = load()
    if a.summary:
        print(json.dumps(data["measurements_not_official_species"], ensure_ascii=False, indent=2))
    else:
        rows = query(data, name=a.query, original_i32=a.original_i32, program=a.program, limit=a.limit)
        if a.visual:
            attach_visual_routes(rows)
        print(json.dumps(rows, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
