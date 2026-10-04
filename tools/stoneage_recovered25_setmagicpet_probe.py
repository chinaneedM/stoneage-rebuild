"""Derived-only full SetMagicPet family probe of the verified recovered25 bundle."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from tools.stoneage_recovered25_petskill_runtime import load_recovered25_petskill_runtime
from tools.stoneage_recovered25_enemybase_runtime import load_recovered25_enemybase_runtime
from tools.stoneage_setmagicpet_model import (
    CALLBACK_NAME,
    SetMagicPetSourceDomain,
    parse_setmagicpet_option,
)

EXPECTED_PETSKILL_SHA256="f9cefefda40e3a5de9b8cdcb9f8d5c75cd768257bb9b12f7591e86d61fe2f6d4"
EXPECTED_REFERENCED_IDS=(601,)
EXPECTED_SLOT_REFERENCES=6
EXPECTED_TEMPLATES=6
EXPECTED_CALLBACK_IDS=(601,602,603,604)
EXPECTED_ROWS={
    601:(1,2,2,2500,8,"9f79d3271fc37e9a8f16a0fc664a3149efab9b2fb2d8026a89032c331f6ea6a8",3,15,"TGH"),
    602:(1,2,2,2500,9,"f696651e7561190d5f9018aa246dd0a5ba8d9ea7b35a92d94b5e9a0a53b272de",3,3000,"HP"),
    603:(1,2,2,2500,8,"9e56ba09b3efd92d37969ff10b39441ce14e9fc3eddbe7c806ee3e5a243cb39d",3,10,"STR"),
    604:(1,2,2,2500,8,"3c627e924f3b3f5e19f2d7c6db7811e174ac6958c2ba3f4067f98822def3cbf2",3,15,"DEX"),
}


def analyze_runtime_objects(petskills,enemybase,*,expected_ids=EXPECTED_CALLBACK_IDS):
    entries=tuple(sorted(
        (entry for entry in petskills.skills.values() if entry.function_name==CALLBACK_NAME),
        key=lambda entry:entry.skill_id,
    ))
    counts={entry.skill_id:0 for entry in entries}
    templates=set()
    for tempno,template in enemybase.templates.items():
        for raw_skill_id in template.skill_slot_ids:
            skill_id=int(raw_skill_id)
            if skill_id>0 and skill_id in counts:
                counts[skill_id]+=1
                templates.add(int(tempno))
    rows=[]
    for entry in entries:
        raw=bytes(entry.option_bytes)
        parsed=None
        try:
            parsed=parse_setmagicpet_option(raw)
        except SetMagicPetSourceDomain:
            pass
        rows.append({
            "id":int(entry.skill_id),
            "field":int(entry.field),
            "target":int(entry.target),
            "cost":int(entry.cost),
            "illegal":int(entry.illegal),
            "slot_references":int(counts[entry.skill_id]),
            "option_bytes":len(raw),
            "option_sha256":hashlib.sha256(raw).hexdigest(),
            "parse_safe":parsed is not None,
            "turn":None if parsed is None else parsed.turn,
            "amount":None if parsed is None else parsed.amount,
            "kind":None if parsed is None else parsed.kind,
            "recognized_kind":bool(parsed is not None and parsed.safe_recognized_kind),
        })
    ids=tuple(entry.skill_id for entry in entries)
    referenced=tuple(sorted(skill_id for skill_id,count in counts.items() if count))
    references_match=(
        referenced==EXPECTED_REFERENCED_IDS
        and sum(counts.values())==EXPECTED_SLOT_REFERENCES
        and len(templates)==EXPECTED_TEMPLATES
    )
    row_map={row["id"]:row for row in rows}
    exact_rows=(
        ids==tuple(EXPECTED_ROWS)
        and all(
            (
                row_map[skill_id]["field"],
                row_map[skill_id]["target"],
                row_map[skill_id]["cost"],
                row_map[skill_id]["illegal"],
                row_map[skill_id]["option_bytes"],
                row_map[skill_id]["option_sha256"],
                row_map[skill_id]["turn"],
                row_map[skill_id]["amount"],
                row_map[skill_id]["kind"],
            ) == EXPECTED_ROWS[skill_id]
            for skill_id in EXPECTED_ROWS
        )
    )
    return {
        "rows":tuple(rows),
        "callback_ids":ids,
        "referenced_ids":referenced,
        "slot_references":sum(counts.values()),
        "templates":len(templates),
        "references_match":references_match,
        "population_closed":expected_ids is not None and ids==expected_ids and references_match,
        "exact_rows_match":exact_rows,
        "all_options_parse_safe":bool(rows) and all(row["parse_safe"] for row in rows),
        "all_kinds_recognized":bool(rows) and all(row["recognized_kind"] for row in rows),
    }


def emit(result):
    print("StoneAge recovered25 SetMagicPet full callback probe — R1")
    print("No names/descriptions/raw OPTION rows/assets stored.")
    print(f"COUNT|setmagicpet_skill_rows|{len(result['rows'])}")
    print(f"COUNT|enemybase_slot_references|{result['slot_references']}")
    print(f"COUNT|enemybase_templates|{result['templates']}")
    for row in result["rows"]:
        print("SETMAGICPET_ROW|"+"|".join(
            f"{key}={int(value) if isinstance(value,bool) else value}"
            for key,value in row.items()
        ))
    print(
        "RESOLUTION|RECOVERED25_SETMAGICPET_POPULATION_"
        +("CLOSED" if result["population_closed"] else "OPEN")
    )
    print(
        "RESOLUTION|RECOVERED25_SETMAGICPET_EXACT_ROWS_"
        +("CLOSED" if result["exact_rows_match"] else "OPEN")
    )
    print(
        "RESOLUTION|RECOVERED25_SETMAGICPET_OPTION_DOMAIN_"
        +("SAFE" if result["all_options_parse_safe"] and result["all_kinds_recognized"] else "OPEN")
    )
    print("RESOLUTION|RECOVERED25_SETMAGICPET_ORDERED_RUNTIME_OPEN")


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--data-dir",type=Path,required=True)
    parser.add_argument("--setup",type=Path)
    args=parser.parse_args()
    pets=load_recovered25_petskill_runtime(data_dir=args.data_dir,setup=args.setup)
    enemies=load_recovered25_enemybase_runtime(data_dir=args.data_dir,setup=args.setup)
    digest=hashlib.sha256((args.data_dir/pets.source_file).read_bytes()).hexdigest()
    if digest!=EXPECTED_PETSKILL_SHA256:
        raise SystemExit("full petskill hash drift")
    result=analyze_runtime_objects(pets,enemies)
    emit(result)
    print("DATA_SHA256|file=petskill|sha256="+digest)
    if not result["references_match"]:
        raise SystemExit("SetMagicPet positive reference population drift")
    if EXPECTED_CALLBACK_IDS is not None and not result["population_closed"]:
        raise SystemExit("SetMagicPet full callback population drift")
    if not result["exact_rows_match"]:
        raise SystemExit("SetMagicPet exact metadata/OPTION/parse drift")
    if not (result["all_options_parse_safe"] and result["all_kinds_recognized"]):
        raise SystemExit("SetMagicPet OPTION domain drift")


if __name__=="__main__":
    main()
