#!/usr/bin/env python3
"""Recovered25 Combined selected-magic cross-link probe.

This is a derived-only bridge from the already pinned Combined OPTION magic IDs
into recovered magic.txt.  It stores code function tokens and numeric metadata,
never recovered names/comments/raw OPTION text.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from tools.stoneage_magic_probe import parse as parse_magic, sha256
from tools.stoneage_recovered25_combined_probe import EXPECTED_EXACT_ROWS

EXPECTED_MAGIC_IDS=(
    20,21,22,23,24,25,61,71,81,91,101,121,
    139,159,169,179,189,240,306,
)
EXPECTED_MAGIC_SHA256=None
EXPECTED_EXACT_MAGIC_ROWS=None


def combined_magic_ids():
    if EXPECTED_EXACT_ROWS is None:
        raise ValueError("Combined exact-row reference must be pinned first")
    return tuple(sorted({
        int(magic_id)
        for row in EXPECTED_EXACT_ROWS
        for magic_id in row[12]
    }))


def _ascii_function(raw:bytes)->str:
    try:
        token=bytes(raw).decode("ascii","strict")
    except UnicodeDecodeError as exc:
        raise ValueError("Combined selected magic function token is not ASCII") from exc
    if not token.startswith("MAGIC_"):
        raise ValueError("Combined selected magic function token lacks MAGIC_ prefix")
    return token


def analyze_parsed_rows(
    parsed,
    malformed,
    *,
    expected_exact_rows=EXPECTED_EXACT_MAGIC_ROWS,
):
    by_id={}
    for fields,values in parsed:
        magic_id=int(values["ID"])
        if magic_id in by_id:
            raise ValueError(f"duplicate recovered magic ID {magic_id}")
        by_id[magic_id]=(fields,values)

    source_ids=combined_magic_ids()
    ids_match=source_ids==EXPECTED_MAGIC_IDS
    rows=[]
    missing=[]
    for magic_id in EXPECTED_MAGIC_IDS:
        record=by_id.get(int(magic_id))
        if record is None:
            missing.append(int(magic_id))
            continue
        fields,values=record
        if len(fields)<4:
            raise ValueError(f"magic {magic_id} lacks function/option columns")
        function=_ascii_function(fields[2])
        option=bytes(fields[3])
        function_raw=bytes(fields[2])
        rows.append({
            "id":int(magic_id),
            "function":function,
            "function_sha256":hashlib.sha256(function_raw).hexdigest(),
            "field":int(values["FIELD"]),
            "target":int(values["TARGET"]),
            "target_deadflg":int(values["TARGET_DEADFLG"]),
            "idx":None if values.get("IDX") is None else int(values["IDX"]),
            "option_bytes":len(option),
            "option_sha256":hashlib.sha256(option).hexdigest(),
            "option_contains_nul":b"\0" in option,
        })

    exact_rows_closed=False
    if expected_exact_rows is not None:
        actual=tuple(
            (
                row["id"],row["function"],row["function_sha256"],
                row["field"],row["target"],row["target_deadflg"],row["idx"],
                row["option_bytes"],row["option_sha256"],
                row["option_contains_nul"],
            )
            for row in rows
        )
        exact_rows_closed=actual==tuple(expected_exact_rows)

    return {
        "combined_magic_ids":source_ids,
        "ids_match":ids_match,
        "rows":tuple(rows),
        "missing":tuple(missing),
        "malformed":int(malformed),
        "population_closed":bool(
            ids_match
            and not missing
            and len(rows)==len(EXPECTED_MAGIC_IDS)
            and int(malformed)==0
        ),
        "exact_rows_closed":exact_rows_closed,
    }


def analyze(data_dir:Path):
    data_dir=Path(data_dir)
    path=data_dir/"magic.txt"
    if not path.is_file():
        raise ValueError("recovered25 magic.txt not found")
    _,parsed,malformed,_,_=parse_magic(path)
    result=analyze_parsed_rows(parsed,malformed)
    digest=sha256(path)
    if (
        EXPECTED_MAGIC_SHA256 is not None
        and digest!=EXPECTED_MAGIC_SHA256
    ):
        raise ValueError("recovered25 magic.txt full-file hash drift")
    return result,digest


def emit(result,digest):
    print("StoneAge recovered25 Combined selected-magic cross-link — R1")
    print("No recovered names/comments/raw magic OPTION text or assets stored.")
    print(f"COUNT|combined_magic_ids|{len(result['combined_magic_ids'])}")
    print(f"COUNT|magic_rows_matched|{len(result['rows'])}")
    print(f"COUNT|magic_parse_malformed|{result['malformed']}")
    for row in result["rows"]:
        idx="NONE" if row["idx"] is None else str(row["idx"])
        print(
            "COMBINED_MAGIC_ROW|"
            f"id={row['id']}|function={row['function']}|"
            f"function_sha256={row['function_sha256']}|"
            f"field={row['field']}|target={row['target']}|"
            f"target_deadflg={row['target_deadflg']}|idx={idx}|"
            f"option_bytes={row['option_bytes']}|"
            f"option_sha256={row['option_sha256']}|"
            f"option_contains_nul={int(row['option_contains_nul'])}"
        )
    print(
        "RESOLUTION|RECOVERED25_COMBINED_MAGIC_CROSSLINK_"
        +("CLOSED" if result["population_closed"] else "OPEN")
    )
    print(
        "RESOLUTION|RECOVERED25_COMBINED_MAGIC_EXACT_ROWS_"
        +("CLOSED" if result["exact_rows_closed"] else "OPEN")
    )
    print("DATA_SHA256|file=magic|sha256="+digest)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--data-dir",type=Path,required=True)
    args=ap.parse_args()
    result,digest=analyze(args.data_dir)
    emit(result,digest)
    if not result["population_closed"]:
        raise SystemExit("Combined selected-magic cross-link drift")
    if (
        EXPECTED_EXACT_MAGIC_ROWS is not None
        and not result["exact_rows_closed"]
    ):
        raise SystemExit("Combined selected-magic exact row drift")


if __name__=="__main__":
    main()
