"""INTEGRATION07: source-qualified DAT/MAP gaps for the 14 QUEST05 no-match floors.

Reads only public, immutable, source-derived records. Not original binary recovery,
map geometry decoding, client execution, nor proof of official contemporaneous deployment.
"""
from __future__ import annotations

from collections import defaultdict
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REC = ROOT / "research" / "recovered"
INPUTS = {
    "q": ("STONEAGE-QUEST05-598-ORIGINAL-CREATE-FLOOR-MAP-AND-WARP-CROSSWALK-R1.json",
          "b004e488e1d0a93ca7c14eb90abb584b23f341fe"),
    "map": ("STONEAGE-MAP-SCENE-MODULE-01-ORIGINAL-SOURCE-MANIFEST-R1.json",
            "03675ee98d391f9ef0246315b2426f2a8b721fd3"),
    "alternate": ("STONEAGE-MAP-SCENE-MODULE-02-THREE-ORIGINAL-DAT-FLOOR-IMAGE-JOIN-R1.json",
                  "445b6f846ae3d541bcd3ff46bd916934a19171ec"),
    "prior": ("STONEAGE-INTEGRATION06-MAP1300-MAP-DAT-SIX-CREATE-SOURCE-R1.json",
              "5e1f49922731e55070cc6e43fbadf29a3609adeb"),
}
OUTPUT = REC / "STONEAGE-INTEGRATION07-FOURTEEN-UNMATCHED-DAT-QUALIFICATION-R1.json"
DAT_CATEGORIES = ("VERIFIED_INDEPENDENT_DAT", "INDEXED_DAT_READ_ERROR", "NO_SELECTED_DAT_MEMBER")
MAP_CATEGORIES = ("TWO_MAP_COPIES_SAME_SHA", "TWO_MAP_COPIES_DIFFERENT_SHA",
                  "MAP_EXTRACTION_ERROR_ONLY", "NO_SELECTED_MAP_MEMBER")


def git_blob(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


def sources():
    results = {}
    for key, (name, blob) in INPUTS.items():
        data = (REC / name).read_bytes()
        if git_blob(data) != blob:
            raise ValueError("Source Git blob changed or truncated: " + name)
        results[key] = json.loads(data)
    return results


def _rows(records, floor, suffix):
    target = f"{floor}.{suffix}".casefold()
    # The actual old source has lowercase 200.dat and 3000.dat; case-sensitive
    # comparison silently drops those two real extraction-failure records.
    return sorted((x for x in records if x[1].casefold() == target), key=lambda x: x[0])


def _map_original(x):
    return dict(group=x[0], original_filename=x[1], original_bytes=x[2],
                source_sha256=x[3], original_crc32=x[4],
                candidate_width=x[6], candidate_height=x[7])


def _read_failure(x):
    return dict(group=x[0], original_filename=x[1],
                expected_member_bytes=x[2], emitted_before_error=x[3],
                error_tag=x[4])


def derive():
    data = sources()
    q, m, alt, prior = (data[k] for k in ("q", "map", "alternate", "prior"))
    if len(q["source_CREATE_references"]) != 598 or len(q["floors"]) != 236:
        raise ValueError("Unexpected source CREATE inventory denominator")
    if m["original_rar_sha256"] != q["source_original_mixed25_RAR_sha256"]:
        raise ValueError("Original RAR source identity disagreement")
    if prior["source_counts"]["CREATE_rows"] != 6:
        raise ValueError("INTEGRATION06 1300 evidence changed")
    selected = sorted((r for r in q["floors"]
                       if r["map_status"] == "NO_MATCHING_DAT_IN_955"),
                      key=lambda r: r["source_floor_id"])
    floors = []
    for meta in selected:
        floor = meta["source_floor_id"]
        map_rows = _rows(m["original_decoded_source_rows"], floor, "MAP")
        map_errors = _rows(m["source_extraction_errors_not_reclassified_as_corruption"], floor, "MAP")
        dat_rows = _rows(m["original_decoded_source_rows"], floor, "DAT")
        dat_errors = _rows(m["source_extraction_errors_not_reclassified_as_corruption"], floor, "DAT")
        if dat_rows or len(dat_errors) > 1:
            raise ValueError("Unexpected DATA qualification scope: " + str(floor))
        alternate = alt["source_three_floors"].get(str(floor))
        map_shas = {r[3] for r in map_rows}
        if map_rows:
            map_status = ("TWO_MAP_COPIES_SAME_SHA" if len(map_shas) == 1
                          else "TWO_MAP_COPIES_DIFFERENT_SHA")
        elif map_errors:
            map_status = "MAP_EXTRACTION_ERROR_ONLY"
        else:
            map_status = "NO_SELECTED_MAP_MEMBER"
        dat_status = ("VERIFIED_INDEPENDENT_DAT" if alternate else
                      "INDEXED_DAT_READ_ERROR" if dat_errors else "NO_SELECTED_DAT_MEMBER")
        possible_map_sizes = [r[2] for r in map_rows] + [r[2] for r in map_errors]
        consistent = (any(3 * (size - 8) + 8 == dat_errors[0][2]
                          for size in possible_map_sizes) if dat_errors else None)
        refs = [i for i, r in enumerate(q["source_CREATE_references"])
                if r["source_floor_id"] == floor]
        if len(refs) != meta["source_CREATE_ref_count"]:
            raise ValueError("Q05 CREATE floor coverage mismatch: " + str(floor))
        floors.append({
            "floor_id": floor,
            "quest05_source_CREATE_count": meta["source_CREATE_ref_count"],
            "quest05_source_cohorts": meta["source_cohorts"],
            "quest05_CREATE_ref_indices": refs,
            "source_MAP_status": map_status,
            "source_MAP_full_original_rows": [_map_original(r) for r in map_rows],
            "source_MAP_original_read_errors": [_read_failure(r) for r in map_errors],
            "source_DAT_status": dat_status,
            "source_DAT_full_MAP01_rows": [_map_original(r) for r in dat_rows],
            "source_DAT_original_read_errors": [_read_failure(r) for r in dat_errors],
            "source_DAT_member_size_formula_consistent": consistent,
            "other_independently_qualified_DAT":
                dict(source_origin=alternate["source_origin"],
                     bytes=alternate["dat_bytes"],
                     sha256=alternate["dat_sha256"],
                     width=alternate["width"], height=alternate["height"])
                if alternate else None,
        })
    def count_category(category, kind):
        rows = [r for r in floors if r[kind] == category]
        return dict(floor_count=len(rows),
                    source_CREATE_count=sum(r["quest05_source_CREATE_count"] for r in rows))
    summary = {
        "source_QUEST05_total_CREATE_references": len(q["source_CREATE_references"]),
        "source_QUEST05_total_distinct_floors": len(q["floors"]),
        "source_QUEST05_unmatched_DAT_floor_count": len(floors),
        "source_QUEST05_unmatched_DAT_CREATE_count": sum(r["quest05_source_CREATE_count"] for r in floors),
        "selected_DAT_status": {x: count_category(x, "source_DAT_status") for x in DAT_CATEGORIES},
        "selected_MAP_status": {x: count_category(x, "source_MAP_status") for x in MAP_CATEGORIES},
        "original_DAT_error_record_floor_count": sum(bool(r["source_DAT_original_read_errors"]) for r in floors),
        "lowercase_DAT_filename_error_floors": [r["floor_id"] for r in floors
            if any(e["original_filename"].endswith(".dat") for e in r["source_DAT_original_read_errors"])],
        "source_MAP_different_SHA_floors": [r["floor_id"] for r in floors
            if r["source_MAP_status"] == "TWO_MAP_COPIES_DIFFERENT_SHA"],
        "source_DAT_independently_qualified_floors": [r["floor_id"] for r in floors
            if r["source_DAT_status"] == "VERIFIED_INDEPENDENT_DAT"],
        "source_no_selected_DAT_record_floors": [r["floor_id"] for r in floors
            if r["source_DAT_status"] == "NO_SELECTED_DAT_MEMBER"],
        "original_DAT_error_size_coherent_floors": sum(
            r["source_DAT_member_size_formula_consistent"] is True for r in floors),
    }
    original_floors = [r for r in floors if r["floor_id"] == 1300]
    if len(original_floors) != 1 or original_floors[0]["quest05_source_CREATE_count"] != prior["source_counts"]["CREATE_rows"]:
        raise ValueError("INTEGRATION06 source 1300 CREATE count divergence")
    return summary, floors


def validate():
    publication = json.loads(OUTPUT.read_text(encoding="utf-8"))
    summary, rows = derive()
    if publication["summary"] != summary or publication["floors"] != rows:
        raise ValueError("INTEGRATION07 report diverged from prior published source records")
    if publication["source_main"]["current_historical_git_blob"] != "c89e0e33537990aa2132b47c40fef49a985a935c":
        raise ValueError("Historical CURRENT-STATE integrity boundary changed")
    return summary


if __name__ == "__main__":
    print(json.dumps(validate(), ensure_ascii=False, indent=2, sort_keys=True))
