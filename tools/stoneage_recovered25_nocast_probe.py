#!/usr/bin/env python3
"""Hard-probe Nocast OPTION grammar and enemybase usage; never dump raw rows."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from tools.stoneage_nocast_model import CALLBACK_NAME, parse_nocast_option
from tools.stoneage_recovered25_enemybase_runtime import load_recovered25_enemybase_runtime
from tools.stoneage_recovered25_petskill_runtime import load_recovered25_petskill_runtime


def analyze_runtime_objects(petskills, enemybase):
    entries = tuple(sorted((entry for entry in petskills.skills.values()
                            if entry.function_name == CALLBACK_NAME),
                           key=lambda entry: int(entry.skill_id)))
    ids = {int(entry.skill_id) for entry in entries}
    refs = 0
    templates = set()
    for tempno, template in enemybase.templates.items():
        uses = sum(int(raw) in ids for raw in template.skill_slot_ids if int(raw) > 0)
        refs += uses
        if uses:
            templates.add(int(tempno))
    rows = []
    for entry in entries:
        raw = bytes(entry.option_bytes)
        same = False
        grammar = False
        turn = success = None
        try:
            same = raw.decode("cp950", "strict") == raw.decode("big5", "strict")
            cp = parse_nocast_option(raw, encoding="cp950")
            big = parse_nocast_option(raw, encoding="big5")
            turn, success = cp.turn, cp.success_offset
            grammar = same and cp == big and turn > 0 and success > 0 and b"\0" not in raw
        except (ValueError, UnicodeError):
            pass
        rows.append({
            "id": int(entry.skill_id), "field": int(entry.field),
            "target": int(entry.target), "cost": int(entry.cost),
            "illegal": int(entry.illegal), "option_bytes": len(raw),
            "option_sha256": hashlib.sha256(raw).hexdigest(),
            "cp950_big5_same": same, "grammar_closed": grammar,
            "turn": turn, "success_offset": success,
        })
    return {
        "rows": tuple(rows), "slot_references": refs, "templates": len(templates),
        "domain_closed": (tuple(row["id"] for row in rows) == (580,)
                          and refs == 18 and len(templates) == 16
                          and all(row["field"] == 1 and row["grammar_closed"] for row in rows)),
    }


def analyze(data_dir: Path, setup: Path | None):
    return analyze_runtime_objects(
        load_recovered25_petskill_runtime(data_dir=data_dir, setup=setup),
        load_recovered25_enemybase_runtime(data_dir=data_dir, setup=setup),
    )


def emit(result):
    print("StoneAge recovered25 Nocast domain probe — R1")
    print("No original names/comments/raw OPTION text/source rows are stored.")
    print(f"COUNT|nocast_skill_rows|{len(result['rows'])}")
    print(f"COUNT|enemybase_slot_references|{result['slot_references']}")
    print(f"COUNT|enemybase_templates|{result['templates']}")
    for row in result["rows"]:
        print("NOCAST_ROW|" + "|".join(f"{key}={int(value) if isinstance(value, bool) else value}"
                                      for key, value in row.items()))
    print("RESOLUTION|RECOVERED25_NOCAST_OPTION_DOMAIN_"
          + ("CLOSED" if result["domain_closed"] else "OPEN"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--setup", type=Path)
    args = parser.parse_args()
    emit(analyze(args.data_dir, args.setup))


if __name__ == "__main__":
    main()
