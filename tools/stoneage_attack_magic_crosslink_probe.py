#!/usr/bin/env python3
"""Cross-link recovered25 AttackMagic skills to magic/item/attmagic data.

The report is structural only: it emits IDs/counts/ranges and parsed numeric
mechanics, never recovered names/comments/option strings or binary payloads.
"""

from __future__ import annotations

import argparse
import collections
from pathlib import Path

from tools.stoneage_attack_magic_model import parse_source_shaped_option
from tools.stoneage_attmagic_probe import parse_attmagic
from tools.stoneage_itemset_schema_probe import (
    INDEX as ITEM_INDEX,
    SCHEMA as ITEM_SCHEMA,
    clean_rows as clean_item_rows,
    setup_itemsets,
    to_int as item_int,
)
from tools.stoneage_magic_probe import parse as parse_magic
from tools.stoneage_recovered25_petskill_runtime import (
    load_recovered25_petskill_runtime,
)

ATTACK_SKILL_FUNC = "PETSKILL_AttackMagic"
ATTACK_MAGIC_FUNC = b"MAGIC_AttMagic"
ATTR_INDEX = {"地": 0, "水": 1, "火": 2, "風": 3, "风": 3}


def _active_itemset_path(data_dir: Path, setup: Path | None) -> Path:
    config = setup_itemsets(setup)
    configured = []
    for value in config.values():
        name = Path(value.replace("\\", "/")).name
        if name and (data_dir / name).is_file():
            configured.append(name)
    unique = tuple(dict.fromkeys(configured))
    if len(unique) > 1:
        raise ValueError(
            "configured itemset files resolve to multiple recovered files"
        )
    if unique:
        return data_dir / unique[0]
    fallback = data_dir / "itemset.txt"
    if fallback.is_file():
        return fallback
    raise ValueError("active recovered25 itemset file not found")


def _item_index(path: Path):
    by_id = {}
    for row in clean_item_rows(path):
        if len(row) != len(ITEM_SCHEMA):
            raise ValueError("active recovered25 itemset row width drift")
        item_id = item_int(row[ITEM_INDEX["id"]])
        if item_id is None:
            raise ValueError("active recovered25 item ID is not decimal")
        if item_id in by_id:
            raise ValueError(f"duplicate recovered25 item ID {item_id}")
        by_id[item_id] = row
    return by_id


def _parse_attack_option(raw: bytes):
    try:
        cp950 = raw.decode("cp950", "strict")
        big5 = raw.decode("big5", "strict")
    except UnicodeDecodeError as exc:
        raise ValueError("attack-magic option is not strict CP950/Big5") from exc
    if cp950 != big5:
        raise ValueError("attack-magic option has CP950/Big5 divergence")
    parts = cp950.split("|")
    if len(parts) < 3:
        raise ValueError("attack-magic option lacks three pipe fields")
    attr_token = parts[0].strip()
    if attr_token not in ATTR_INDEX:
        raise ValueError("attack-magic option has unknown attribute token")
    try:
        power = int(parts[1].strip(), 10)
        magic_level = int(parts[2].strip(), 10)
    except ValueError as exc:
        raise ValueError("attack-magic option power/level is not decimal") from exc
    return ATTR_INDEX[attr_token], power, magic_level


def analyze(data_dir: Path, setup: Path | None = None):
    data_dir = Path(data_dir)
    setup = Path(setup) if setup is not None else None

    petskills = load_recovered25_petskill_runtime(
        data_dir=data_dir,
        setup=setup,
    )
    attack_skills = tuple(
        entry
        for entry in petskills.skills.values()
        if entry.function_name == ATTACK_SKILL_FUNC
    )

    skill_pairs = []
    for entry in attack_skills:
        parsed = parse_source_shaped_option(entry.ascii_option())
        if (
            parsed["magic"] is None
            or not parsed["item_marker_after_magic"]
            or parsed["item"] is None
        ):
            continue
        skill_pairs.append(
            (entry.skill_id, int(parsed["magic"]), int(parsed["item"]))
        )

    _, magic_parsed, magic_bad, _, _ = parse_magic(data_dir / "magic.txt")
    magic_by_id = {}
    for fields, values in magic_parsed:
        magic_id = int(values["ID"])
        if magic_id in magic_by_id:
            raise ValueError(f"duplicate recovered25 magic ID {magic_id}")
        magic_by_id[magic_id] = (fields, values)

    item_path = _active_itemset_path(data_dir, setup)
    item_by_id = _item_index(item_path)

    attmagic_path = data_dir / "attmagic.bin"
    if not attmagic_path.is_file():
        raise ValueError("recovered25 attmagic.bin not found")
    att_records = parse_attmagic(attmagic_path)
    if len(att_records) % 2:
        raise ValueError("recovered25 attmagic record count is not even")
    att_magicnum = len(att_records) // 2

    magic_rows = func_rows = idx_rows = idx_valid = 0
    item_rows = item_magic_match = 0
    att_pair_valid = 0
    idx_values = []
    item_mp_values = []
    attr_values = []
    power_values = []
    level_values = []
    option_structural = 0

    for _, magic_id, item_id in skill_pairs:
        magic = magic_by_id.get(magic_id)
        if magic is not None:
            magic_rows += 1
            fields, values = magic
            if len(fields) >= 4 and fields[2] == ATTACK_MAGIC_FUNC:
                func_rows += 1
            idx = values.get("IDX")
            if idx is not None:
                idx_rows += 1
                idx = int(idx)
                idx_values.append(idx)
                if 0 <= idx < att_magicnum:
                    idx_valid += 1
                    if 2 * idx + 1 < len(att_records):
                        att_pair_valid += 1
            if len(fields) >= 4:
                try:
                    attr, power, level = _parse_attack_option(fields[3])
                except ValueError:
                    pass
                else:
                    option_structural += 1
                    attr_values.append(attr)
                    power_values.append(power)
                    level_values.append(level)

        item = item_by_id.get(item_id)
        if item is not None:
            item_rows += 1
            linked_magic = item_int(item[ITEM_INDEX["magicid"]])
            if linked_magic == magic_id:
                item_magic_match += 1
            mp = item_int(item[ITEM_INDEX["magicusemp"]])
            if mp is not None:
                item_mp_values.append(mp)

    pair_count = len(skill_pairs)
    complete = (
        len(attack_skills) == 25
        and pair_count == 25
        and magic_rows == pair_count
        and func_rows == pair_count
        and idx_rows == pair_count
        and idx_valid == pair_count
        and option_structural == pair_count
        and item_rows == pair_count
        and item_magic_match == pair_count
        and len(item_mp_values) == pair_count
        and att_pair_valid == pair_count
        and magic_bad == 0
    )

    return {
        "attack_skill_count": len(attack_skills),
        "pair_count": pair_count,
        "magic_rows": magic_rows,
        "func_rows": func_rows,
        "idx_rows": idx_rows,
        "idx_valid": idx_valid,
        "idx_values": tuple(idx_values),
        "option_structural": option_structural,
        "attr_values": tuple(attr_values),
        "power_values": tuple(power_values),
        "level_values": tuple(level_values),
        "item_rows": item_rows,
        "item_magic_match": item_magic_match,
        "item_mp_values": tuple(item_mp_values),
        "att_raw_records": len(att_records),
        "att_magicnum": att_magicnum,
        "att_pair_valid": att_pair_valid,
        "magic_bad": magic_bad,
        "item_file": item_path.name,
        "complete": complete,
    }


def _range_text(values):
    if not values:
        return "min=NONE|max=NONE|distinct=0"
    return (
        f"min={min(values)}|max={max(values)}|distinct={len(set(values))}"
    )


def emit(data_dir: Path, setup: Path | None = None):
    r = analyze(data_dir, setup)
    print("StoneAge recovered25 AttackMagic cross-link probe — R1")
    print(
        "No recovered names/comments/options or attack-magic payload bytes "
        "are stored in this report."
    )
    print(f"ATTACK_SKILL_COUNT|{r['attack_skill_count']}")
    print(f"SKILL_MAGIC_ITEM_NUMERIC_PAIRS|{r['pair_count']}")
    print(f"MAGIC_ROWS_MATCHED|{r['magic_rows']}")
    print(f"MAGIC_FUNC_ATTACKMAGIC_MATCHED|{r['func_rows']}")
    print(f"MAGIC_IDX_PRESENT|{r['idx_rows']}")
    print(f"MAGIC_IDX_VALID|{r['idx_valid']}")
    print("MAGIC_IDX_STAT|" + _range_text(r["idx_values"]))
    print(f"MAGIC_OPTION_STRUCTURAL_MATCHED|{r['option_structural']}")
    for value, count in sorted(collections.Counter(r["attr_values"]).items()):
        print(f"MAGIC_ATTR_INDEX_COUNT|{value}|{count}")
    print("MAGIC_POWER_STAT|" + _range_text(r["power_values"]))
    print("MAGIC_LEVEL_STAT|" + _range_text(r["level_values"]))
    print(f"ACTIVE_ITEMSET|{r['item_file']}")
    print(f"ITEM_ROWS_MATCHED|{r['item_rows']}")
    print(f"ITEM_MAGICID_MATCHED|{r['item_magic_match']}")
    print("ITEM_MAGICUSEMP_STAT|" + _range_text(r["item_mp_values"]))
    print(f"ATTMAGIC_RAW_RECORD_COUNT|{r['att_raw_records']}")
    print(f"ATTMAGIC_EFFECTIVE_MAGIC_COUNT|{r['att_magicnum']}")
    print(f"ATTMAGIC_ADJACENT_RECORD_PAIRS_VALID|{r['att_pair_valid']}")
    print(f"MAGIC_PARSE_MALFORMED|{r['magic_bad']}")
    print(
        "RESOLUTION|"
        + (
            "RECOVERED25_ATTACKMAGIC_CROSSLINK_CLOSED"
            if r["complete"]
            else "RECOVERED25_ATTACKMAGIC_CROSSLINK_OPEN"
        )
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", type=Path, required=True)
    ap.add_argument("--setup", type=Path)
    args = ap.parse_args()
    emit(args.data_dir, args.setup)


if __name__ == "__main__":
    main()
