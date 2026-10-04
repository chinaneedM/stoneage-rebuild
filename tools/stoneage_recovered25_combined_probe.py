"""Derived-only Combined population/metadata/OPTION probe for recovered25."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re

from tools.stoneage_recovered25_petskill_runtime import (
    load_recovered25_petskill_runtime,
)
from tools.stoneage_recovered25_enemybase_runtime import (
    load_recovered25_enemybase_runtime,
)
from tools.stoneage_combined_model import CALLBACK_NAME

EXPECTED_PETSKILL_SHA256="f9cefefda40e3a5de9b8cdcb9f8d5c75cd768257bb9b12f7591e86d61fe2f6d4"
EXPECTED_CALLBACK_IDS=(627,632,637)
EXPECTED_REFERENCED_IDS=(627,632,637)
EXPECTED_SLOT_REFERENCES=5
EXPECTED_TEMPLATES=5
EXPECTED_EXACT_ROWS=None


def _ascii_int(token:bytes):
    stripped=token.strip()
    if not re.fullmatch(rb"[+-]?\d+",stripped):
        return None
    try:
        return int(stripped.decode("ascii"))
    except (UnicodeDecodeError,ValueError):
        return None


def _option_structure(raw:bytes):
    parts=raw.split(b"|")
    marker=parts[0] if parts else b""
    declared=_ascii_int(parts[1]) if len(parts)>1 else None
    effective=(
        None if declared is None
        else min(int(declared),10)
    )
    tokens=()
    token_ints=()
    if effective is not None and effective>0:
        tokens=tuple(parts[2:2+effective])
        token_ints=tuple(_ascii_int(token) for token in tokens)
    enough=(
        effective is not None
        and effective>0
        and len(parts)>=2+effective
    )
    well=bool(
        enough
        and len(token_ints)==effective
        and all(value is not None for value in token_ints)
    )
    return {
        "marker_sha256":hashlib.sha256(marker).hexdigest(),
        "declared_count":declared,
        "effective_count":effective,
        "magic_ids":tuple(
            int(value) for value in token_ints if value is not None
        ),
        "well_formed":well,
    }


def analyze_runtime_objects(
    petskills,enemybase,*,expected_exact_rows=EXPECTED_EXACT_ROWS
):
    entries=tuple(sorted(
        (
            entry for entry in petskills.skills.values()
            if entry.function_name==CALLBACK_NAME
        ),
        key=lambda entry:int(entry.skill_id),
    ))
    counts={int(entry.skill_id):0 for entry in entries}
    templates=set()
    for tempno,template in enemybase.templates.items():
        hit=False
        for raw_skill_id in template.skill_slot_ids:
            skill_id=int(raw_skill_id)
            if skill_id>0 and skill_id in counts:
                counts[skill_id]+=1
                hit=True
        if hit:
            templates.add(int(tempno))

    rows=[]
    for entry in entries:
        raw=bytes(entry.option_bytes)
        structure=_option_structure(raw)
        rows.append({
            "id":int(entry.skill_id),
            "field":int(entry.field),
            "target":int(entry.target),
            "cost":int(entry.cost),
            "illegal":int(entry.illegal),
            "slot_references":int(counts[int(entry.skill_id)]),
            "option_bytes":len(raw),
            "option_sha256":hashlib.sha256(raw).hexdigest(),
            "option_contains_nul":b"\0" in raw,
            **structure,
        })
    ids=tuple(row["id"] for row in rows)
    referenced=tuple(sorted(k for k,v in counts.items() if v))
    population_closed=(
        ids==EXPECTED_CALLBACK_IDS
        and referenced==EXPECTED_REFERENCED_IDS
        and sum(counts.values())==EXPECTED_SLOT_REFERENCES
        and len(templates)==EXPECTED_TEMPLATES
    )
    all_well_formed=bool(rows) and all(row["well_formed"] for row in rows)
    exact_rows_closed=False
    if expected_exact_rows is not None:
        actual=tuple(
            (
                row["id"],row["field"],row["target"],row["cost"],row["illegal"],
                row["slot_references"],row["option_bytes"],
                row["option_sha256"],row["option_contains_nul"],
                row["marker_sha256"],row["declared_count"],
                row["effective_count"],row["magic_ids"],row["well_formed"],
            )
            for row in rows
        )
        exact_rows_closed=actual==tuple(expected_exact_rows)
    return {
        "rows":tuple(rows),
        "callback_ids":ids,
        "referenced_ids":referenced,
        "slot_references":sum(counts.values()),
        "templates":len(templates),
        "population_closed":population_closed,
        "all_well_formed":all_well_formed,
        "exact_rows_closed":exact_rows_closed,
    }


def emit(result):
    print("StoneAge recovered25 Combined probe — R1")
    print("No names/descriptions/raw OPTION bytes/assets stored.")
    print(f"COUNT|combined_skill_rows|{len(result['rows'])}")
    print(f"COUNT|enemybase_slot_references|{result['slot_references']}")
    print(f"COUNT|enemybase_templates|{result['templates']}")
    print(
        "COUNT|well_formed_rows|"
        +str(sum(1 for row in result["rows"] if row["well_formed"]))
    )
    for row in result["rows"]:
        scalar_keys=(
            "id","field","target","cost","illegal","slot_references",
            "option_bytes","option_sha256","option_contains_nul",
            "marker_sha256","declared_count","effective_count","well_formed",
        )
        fields=[
            f"{key}={int(row[key]) if isinstance(row[key],bool) else row[key]}"
            for key in scalar_keys
        ]
        fields.append(
            "magic_ids="+",".join(str(value) for value in row["magic_ids"])
        )
        print("COMBINED_ROW|"+"|".join(fields))
    print(
        "RESOLUTION|RECOVERED25_COMBINED_POPULATION_"
        +("CLOSED" if result["population_closed"] else "OPEN")
    )
    print(
        "RESOLUTION|RECOVERED25_COMBINED_WELLFORMED_OPTION_"
        +("CLOSED" if result["all_well_formed"] else "OPEN")
    )
    print(
        "RESOLUTION|RECOVERED25_COMBINED_EXACT_ROWS_"
        +("CLOSED" if result["exact_rows_closed"] else "OPEN")
    )
    print("RESOLUTION|RECOVERED25_COMBINED_ORDERED_RUNTIME_OPEN")


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--data-dir",type=Path,required=True)
    parser.add_argument("--setup",type=Path)
    args=parser.parse_args()
    pets=load_recovered25_petskill_runtime(
        data_dir=args.data_dir,setup=args.setup
    )
    enemies=load_recovered25_enemybase_runtime(
        data_dir=args.data_dir,setup=args.setup
    )
    digest=hashlib.sha256(
        (args.data_dir/pets.source_file).read_bytes()
    ).hexdigest()
    if digest!=EXPECTED_PETSKILL_SHA256:
        raise SystemExit("full petskill hash drift")
    result=analyze_runtime_objects(pets,enemies)
    emit(result)
    print("DATA_SHA256|file=petskill|sha256="+digest)
    if not result["population_closed"]:
        raise SystemExit("Combined callback/reference population drift")
    if not result["all_well_formed"]:
        raise SystemExit("Combined actual OPTION leaves safe source domain")
    if (
        EXPECTED_EXACT_ROWS is not None
        and not result["exact_rows_closed"]
    ):
        raise SystemExit("Combined exact metadata/OPTION drift")


if __name__=="__main__":
    main()
