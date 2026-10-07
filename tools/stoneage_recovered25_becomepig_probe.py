"""Derived-only recovered25 BecomePig population and placement discovery."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from tools.stoneage_recovered25_petskill_runtime import load_recovered25_petskill_runtime
from tools.stoneage_recovered25_enemybase_runtime import (
    load_recovered25_enemybase_runtime, _active_enemybase_path,
)

CALLBACK_NAME="PETSKILL_BecomePig"
EXPECTED_PETSKILL_SHA256="f9cefefda40e3a5de9b8cdcb9f8d5c75cd768257bb9b12f7591e86d61fe2f6d4"
EXPECTED_ENEMYBASE_SHA256="1be7d5226798f7abaabe1f1e74aa1533fcd10e3eaf43f6497d63afa91df3e8b7"
EXPECTED_REFERENCED_IDS=(631,635)
EXPECTED_POSITIVE_USES=2
EXPECTED_POSITIVE_TEMPLATES=2
# Complete identities remain intentionally unpinned during first discovery.
EXPECTED_CALLBACK_IDS=None
EXPECTED_EXACT_ROWS=None
EXPECTED_TEMPLATE_ROWS=None


def analyze_runtime_objects(
    petskills,
    enemybase,
    *,
    expected_callback_ids=EXPECTED_CALLBACK_IDS,
    expected_exact_rows=EXPECTED_EXACT_ROWS,
    expected_template_rows=EXPECTED_TEMPLATE_ROWS,
):
    entries=sorted(
        (entry for entry in petskills.skills.values()
         if entry.function_name==CALLBACK_NAME),
        key=lambda entry:int(entry.skill_id),
    )
    counts={int(entry.skill_id):0 for entry in entries}
    templates=[]
    for tempno,template in sorted(enemybase.templates.items()):
        slots=tuple(
            index for index,skill_id in enumerate(template.skill_slot_ids,1)
            if int(skill_id) in counts
        )
        if not slots:
            continue
        for index in slots:
            counts[int(template.skill_slot_ids[index-1])]+=1
        templates.append({
            "tempno":int(tempno),
            "graphic_id":int(template.graphic_id),
            "base_vital":int(template.base_vital),
            "base_strength":int(template.base_strength),
            "base_toughness":int(template.base_toughness),
            "base_dexterity":int(template.base_dexterity),
            "ai":int(template.ai),
            "skill_slots":slots,
            "skill_ids":tuple(int(template.skill_slot_ids[index-1]) for index in slots),
        })

    rows=[]
    for entry in entries:
        raw=bytes(entry.option_bytes)
        try:
            cp950=raw.decode("cp950","strict")
            big5=raw.decode("big5","strict")
            codec_agrees=cp950==big5
        except UnicodeError:
            codec_agrees=False
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
            "option_ascii":raw.isascii(),
            "cp950_big5_agrees":codec_agrees,
        })

    callback_ids=tuple(row["id"] for row in rows)
    referenced_ids=tuple(sorted(skill_id for skill_id,count in counts.items() if count))
    exact_rows=tuple(tuple(row[key] for key in (
        "id","field","target","cost","illegal","slot_references",
        "option_bytes","option_sha256","option_contains_nul",
        "option_ascii","cp950_big5_agrees",
    )) for row in rows)
    exact_templates=tuple((
        row["tempno"],row["graphic_id"],row["base_vital"],row["base_strength"],
        row["base_toughness"],row["base_dexterity"],row["ai"],
        row["skill_slots"],row["skill_ids"],
    ) for row in templates)
    uses=sum(counts.values())
    return {
        "rows":tuple(rows),
        "templates":tuple(templates),
        "callback_ids":callback_ids,
        "referenced_ids":referenced_ids,
        "slot_references":uses,
        "positive_references_closed":(
            referenced_ids==EXPECTED_REFERENCED_IDS
            and uses==EXPECTED_POSITIVE_USES
            and len(templates)==EXPECTED_POSITIVE_TEMPLATES
        ),
        "population_closed":expected_callback_ids is not None and callback_ids==expected_callback_ids,
        "exact_rows_closed":expected_exact_rows is not None and exact_rows==expected_exact_rows,
        "exact_templates_closed":expected_template_rows is not None and exact_templates==expected_template_rows,
    }


def emit(result):
    print("StoneAge recovered25 BecomePig probe — R1 discovery")
    print("Derived facts only; no names/descriptions/raw OPTION bytes/assets stored.")
    print("COUNT|callback_rows|"+str(len(result["rows"])))
    print("COUNT|enemybase_slot_references|"+str(result["slot_references"]))
    print("COUNT|enemybase_templates|"+str(len(result["templates"])))
    for row in result["rows"]:
        print("BECOMEPIG_ROW|"+"|".join(
            f"{key}={int(value) if isinstance(value,bool) else value}"
            for key,value in row.items()
        ))
    for row in result["templates"]:
        print("BECOMEPIG_TEMPLATE|"+"|".join(
            f"{key}={','.join(map(str,value)) if isinstance(value,tuple) else value}"
            for key,value in row.items()
        ))
    for name in ("positive_references","population","exact_rows","exact_templates"):
        print(
            "RESOLUTION|RECOVERED25_BECOMEPIG_"+name.upper()+"_"+
            ("CLOSED" if result[name+"_closed"] else "OPEN")
        )


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--data-dir",type=Path,required=True)
    parser.add_argument("--setup",type=Path)
    parser.add_argument("--discover",action="store_true")
    args=parser.parse_args()
    pets=load_recovered25_petskill_runtime(data_dir=args.data_dir,setup=args.setup)
    enemies=load_recovered25_enemybase_runtime(data_dir=args.data_dir,setup=args.setup)
    digest=hashlib.sha256((args.data_dir/pets.source_file).read_bytes()).hexdigest()
    if digest!=EXPECTED_PETSKILL_SHA256:
        raise SystemExit("full petskill hash drift")
    enemy_digest=hashlib.sha256(_active_enemybase_path(args.data_dir,args.setup).read_bytes()).hexdigest()
    if enemy_digest!=EXPECTED_ENEMYBASE_SHA256:
        raise SystemExit("full active enemybase hash drift")
    result=analyze_runtime_objects(pets,enemies)
    emit(result)
    print("DATA_SHA256|file=petskill|sha256="+digest)
    print("DATA_SHA256|file=enemybase|sha256="+enemy_digest)
    if not result["positive_references_closed"]:
        raise SystemExit("BecomePig pressure/positive reference identity drift")
    if args.discover:
        print("BOUNDARY|discovery_only_complete_population_and_exact_identity_not_accepted")
        return
    if not all(result[key+"_closed"] for key in ("population","exact_rows","exact_templates")):
        raise SystemExit("BecomePig exact population/row/template identity drift")


if __name__=="__main__":
    main()
