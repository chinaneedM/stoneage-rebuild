"""Finite 1999 JSS first-party source census: lexical pointers, not pet releases.

Uses the existing certified single archived operator source. Never stores raw
HTML in public Git, and never promotes a word hit into an official species.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen

from tools.stoneage_jss_pet_patch_history import URL, SHA, change_rows
from tools.stoneage_jss_pet_faq import compact, require

SOURCE_BYTES = 11239
LABELS = {
    "PET": "ペット",
    "DINOSAUR": "恐竜",
    "CAPTURE": "捕獲",
    "PET_MAIL": "ペットメール",
    "RARE": "レア",
    "PRIZE": "賞品",
    "PRESENT": "プレゼント",
    "GAME_PET_NAME_URIURI": "ウリウリ",
    "SKILL": "技",
    "UPDATE_ADD": "追加",
    "BUG_FIX": "修正",
    "EVENT": "イベント",
    "PET_SHOP": "ペットショップ",
}
KNOWN_NO_RELEASE_KEYS = (
    "GAME_PET_NAME_URIURI", "PRESENT", "PRIZE", "PET", "DINOSAUR", "CAPTURE"
)


def build(raw: bytes, final_url: str) -> dict:
    require(final_url == URL, "source URL/capture changed")
    require(len(raw) == SOURCE_BYTES and hashlib.sha256(raw).hexdigest() == SHA,
            "qualified original source bytes do not match fixed custody")
    rows = change_rows(raw.decode("shift_jis", errors="strict"))
    require(len(rows) == 40 and rows[-1]["date"] == "1999-10-18"
            and rows[0]["date"] == "2000-09-11", "wrong source history coverage")
    chosen = [(i, r) for i, r in enumerate(rows) if r["date"].startswith("1999-")]
    require(len(chosen) == 15, "1999 source-row count changed")
    result_rows = []
    for idx, row in chosen:
        raw_clauses = [compact(c) for c in row["text"].split("・")]
        clauses = [c for c in raw_clauses if c]
        require(clauses, "empty original update entry")
        result_rows.append({
            "original_source_order": idx,
            "operator_written_date": row["date"],
            "date_as_written": row["date_as_written"],
            "weekday_as_written": row["weekday_as_written"],
            "weekday_matches_calendar": row["weekday_matches_calendar"],
            "entry_text_characters": len(row["text"]),
            "entry_body_sha256": hashlib.sha256(row["text"].encode("utf-8")).hexdigest(),
            "clause_count": len(clauses),
            "clauses": [
                {
                    "clause_order_in_entry": n,
                    "normalized_characters": len(clause),
                    "normalized_sha256": hashlib.sha256(clause.encode("utf-8")).hexdigest(),
                    "literal_signals": [key for key, literal in LABELS.items() if literal in clause],
                    "official_pet_species_name_identified": False,
                    "official_obtainable_pet_record_proven": False,
                }
                for n, clause in enumerate(clauses)
            ],
        })
    require(sorted([x["original_source_order"] for x in result_rows]) == list(range(25, 40)),
            "original 1999 source-order positions unexpected")
    hits = {key: sum(1 for row in result_rows for c in row["clauses"]
                     if key in c["literal_signals"]) for key in LABELS}
    return {
        "schema": "stoneage.pet31.jss1999_all_operator_update_entries_lexical_census.r1",
        "source": {"url": URL, "bytes": SOURCE_BYTES, "sha256": SHA,
                   "actual_archive_capture": "20010417162544"},
        "original_operator_history": {"total_rows_1999_through_2000": 40,
                                     "source_rows_1999": 15,
                                     "first_1999_operator_date": "1999-10-18",
                                     "last_1999_operator_date": "1999-12-20"},
        "matching_rule": "FIXED_LITERAL_OCCURRENCE_IN_NORMALIZED_FIRST_PARTY_TEXT",
        "signals": LABELS,
        "lexical_hit_clause_counts": hits,
        "dated_rows_1999": result_rows,
        "new_official_species_records": [],
        "year_1999_historically_complete": False,
        "year_1999_source_bounded_reviewed": False,
        "negative_non_matches_prove_no_pets": False,
        "new_JSS_named_reward_or_native_pet_ID_from_keyword_scan_proven": False,
        "raw_original_html_or_images_published": False,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    if args.input:
        raw, final = args.input.read_bytes(), URL
    else:
        with urlopen(Request(URL, headers={"User-Agent": "StoneAge-Historical-Research/1.0"}),
                     timeout=60) as response:
            raw, final = response.read(), response.url
    result = build(raw, final)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    print(json.dumps({
        "source_bytes": result["source"]["bytes"],
        "source_sha256": result["source"]["sha256"],
        "1999_rows": len(result["dated_rows_1999"]),
        "1999_clauses": sum(x["clause_count"] for x in result["dated_rows_1999"]),
        "source_orders": [x["original_source_order"] for x in result["dated_rows_1999"]],
        "literal_hits": result["lexical_hit_clause_counts"],
        "official_species_proven": 0,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
