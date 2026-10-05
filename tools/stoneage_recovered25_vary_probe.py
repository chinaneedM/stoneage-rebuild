"""Derived-only recovered25 PETSKILL_Vary population/data probe."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re
from types import MappingProxyType

from tools.stoneage_recovered25_petskill_runtime import (
    load_recovered25_petskill_runtime,
)
from tools.stoneage_recovered25_enemybase_runtime import (
    load_recovered25_enemybase_runtime,
)

CALLBACK_NAME="PETSKILL_Vary"
EXPECTED_PETSKILL_SHA256="f9cefefda40e3a5de9b8cdcb9f8d5c75cd768257bb9b12f7591e86d61fe2f6d4"
EXPECTED_CALLBACK_IDS=(600,)
EXPECTED_REFERENCED_IDS=(600,)
EXPECTED_SLOT_REFERENCES=4
EXPECTED_TEMPLATES=4
BASE_ALLOWED_TEMPNOS=frozenset({981,982,983,984})


def _c_float_after(raw: bytes, marker: bytes) -> float | None:
    pos=raw.find(marker)
    if pos < 0:
        return None
    tail=raw[pos+len(marker):].decode("latin-1","replace")
    match=re.match(
        r"\\s*[+-]?(?:(?:\\d+(?:\\.\\d*)?)|(?:\\.\\d+))"
        r"(?:[eE][+-]?\\d+)?",
        tail,
    )
    if match is None:
        return None
    return float(match.group(0))


def _cp950_values(raw: bytes):
    return {
        "attack_percent":_c_float_after(raw,"攻%".encode("cp950")),
        "defense_percent":_c_float_after(raw,"防%".encode("cp950")),
        "quick_percent":_c_float_after(raw,"敏%".encode("cp950")),
    }


def _marker_presence(raw: bytes):
    markers={
        "utf8_attack":"攻%".encode("utf-8"),
        "utf8_defense":"防%".encode("utf-8"),
        "utf8_quick":"敏%".encode("utf-8"),
        "utf8_image_simplified":"图%".encode("utf-8"),
        "utf8_image_traditional":"圖%".encode("utf-8"),
        "cp950_attack":"攻%".encode("cp950"),
        "cp950_defense":"防%".encode("cp950"),
        "cp950_quick":"敏%".encode("cp950"),
        "cp950_image_traditional":"圖%".encode("cp950"),
        "gbk_attack":"攻%".encode("gbk"),
        "gbk_defense":"防%".encode("gbk"),
        "gbk_quick":"敏%".encode("gbk"),
        "gbk_image_simplified":"图%".encode("gbk"),
        "gbk_image_traditional":"圖%".encode("gbk"),
    }
    return MappingProxyType({
        key:needle in raw for key,needle in markers.items()
    })


def analyze_runtime_objects(petskills,enemybase):
    entries=tuple(sorted(
        (
            entry for entry in petskills.skills.values()
            if entry.function_name==CALLBACK_NAME
        ),
        key=lambda entry:entry.skill_id,
    ))
    counts={entry.skill_id:0 for entry in entries}
    template_rows=[]
    for tempno,template in sorted(enemybase.templates.items()):
        hit_slots=tuple(
            index
            for index,raw_skill_id in enumerate(template.skill_slot_ids,1)
            if int(raw_skill_id) in counts
        )
        if not hit_slots:
            continue
        for index in hit_slots:
            counts[int(template.skill_slot_ids[index-1])]+=1
        template_rows.append({
            "tempno":int(tempno),
            "graphic_id":int(template.graphic_id),
            "skill_slots":tuple(int(x) for x in hit_slots),
            "base_allowed_tempno":int(tempno) in BASE_ALLOWED_TEMPNOS,
        })

    rows=[]
    for entry in entries:
        raw=bytes(entry.option_bytes)
        rows.append({
            "id":int(entry.skill_id),
            "field":int(entry.field),
            "target":int(entry.target),
            "cost":int(entry.cost),
            "illegal":int(entry.illegal),
            "slot_references":int(counts[entry.skill_id]),
            "option_bytes":len(raw),
            "option_sha256":hashlib.sha256(raw).hexdigest(),
            "option_contains_nul":b"\0" in raw,
            "ascii_percent_count":raw.count(b"%"),
            "markers":_marker_presence(raw),
            "cp950_values":_cp950_values(raw),
        })

    ids=tuple(row["id"] for row in rows)
    referenced=tuple(sorted(k for k,v in counts.items() if v))
    population_closed=(
        ids==EXPECTED_CALLBACK_IDS
        and referenced==EXPECTED_REFERENCED_IDS
        and sum(counts.values())==EXPECTED_SLOT_REFERENCES
        and len(template_rows)==EXPECTED_TEMPLATES
    )
    return {
        "rows":tuple(rows),
        "callback_ids":ids,
        "referenced_ids":referenced,
        "slot_references":sum(counts.values()),
        "templates":tuple(template_rows),
        "population_closed":population_closed,
        "all_positive_templates_base_allowed":(
            bool(template_rows)
            and all(row["base_allowed_tempno"] for row in template_rows)
        ),
    }


def emit(result):
    print("StoneAge recovered25 PETSKILL_Vary probe — R1 first pass")
    print("No names/descriptions/raw OPTION bytes/assets stored.")
    print(f"COUNT|vary_skill_rows|{len(result['rows'])}")
    print(f"COUNT|enemybase_slot_references|{result['slot_references']}")
    print(f"COUNT|enemybase_templates|{len(result['templates'])}")
    for row in result["rows"]:
        base=(
            "VARY_ROW|"
            f"id={row['id']}|field={row['field']}|target={row['target']}|"
            f"cost={row['cost']}|illegal={row['illegal']}|"
            f"slot_references={row['slot_references']}|"
            f"option_bytes={row['option_bytes']}|"
            f"option_sha256={row['option_sha256']}|"
            f"option_contains_nul={int(row['option_contains_nul'])}|"
            f"ascii_percent_count={row['ascii_percent_count']}"
        )
        print(base)
        marker_bits="|".join(
            f"{key}={int(value)}"
            for key,value in sorted(row["markers"].items())
        )
        print(f"VARY_OPTION_MARKERS|id={row['id']}|{marker_bits}")
        values=row["cp950_values"]
        print(
            "VARY_OPTION_VALUES|"
            f"id={row['id']}|"
            f"attack_percent={values['attack_percent']}|"
            f"defense_percent={values['defense_percent']}|"
            f"quick_percent={values['quick_percent']}"
        )
    for row in result["templates"]:
        slots=",".join(str(x) for x in row["skill_slots"])
        print(
            "VARY_TEMPLATE|"
            f"tempno={row['tempno']}|graphic_id={row['graphic_id']}|"
            f"skill_slots={slots}|"
            f"base_allowed_tempno={int(row['base_allowed_tempno'])}"
        )
    print(
        "RESOLUTION|RECOVERED25_VARY_POPULATION_"
        +("CLOSED" if result["population_closed"] else "OPEN")
    )
    print(
        "RESOLUTION|RECOVERED25_VARY_BASE_TEMPID_DOMAIN_"
        +("CLOSED" if result["all_positive_templates_base_allowed"] else "OPEN")
    )
    print("RESOLUTION|RECOVERED25_VARY_EXACT_OPTION_SEMANTICS_OPEN")


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
        raise SystemExit("Vary callback/reference population drift")


if __name__=="__main__":
    main()
