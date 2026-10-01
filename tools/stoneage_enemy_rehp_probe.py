#!/usr/bin/env python3
"""Hard-probe recovered25 ENEMYSKILL_ReHP use and reachable target HP domain.

The report deliberately retains only execution-relevant IDs, counts, hashes and
bounds. It does not reproduce source table rows or display names.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
from typing import Mapping, Sequence

from tools.stoneage_encount_chain_probe import (
    configured_file,
    parse_enemy,
    parse_group,
    setup_values,
)
from tools.stoneage_enemybase_probe import analyze as analyze_enemybase
from tools.stoneage_player_growth_model import base_derived_stats
from tools.stoneage_recovered25_petskill_runtime import (
    load_recovered25_petskill_runtime,
)
from tools.stoneage_tw10_25_bridge_model import PetTemplateBridge


REHP_CALLBACK = "ENEMYSKILL_ReHP"
RAND_POWER_LOWER = 100


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def normalized_levels(row: Mapping[str, int]) -> tuple[int, int]:
    lo = int(row["lv_min"])
    hi = int(row["lv_max"])
    if lo == 0:
        lo = hi
    lo, hi = min(lo, hi), max(lo, hi)
    if lo < 1:
        raise ValueError("enemy variant has no valid level >= 1")
    return lo, hi


def minimum_birth_max_hp(
    template: PetTemplateBridge,
    *,
    level_min: int,
    level_max: int,
) -> dict[str, int | tuple[int, int, int, int]]:
    """Return the exact minimum reachable birth max-HP for one level interval.

    For positive birth scale, max HP is linear in the individualized four base
    components and in the ten spawn-allocation points. The minimum therefore
    uses each component's smallest valid -2..2 birth offset and places all ten
    allocation draws on a non-vital component (coefficient 1 rather than 4).
    The final max-HP value is still evaluated by the shared fixed-descendant
    base_derived_stats projection rather than by a separate approximation.
    """

    required = (
        template.init_num,
        template.level_up_point,
        template.base_vital,
        template.base_strength,
        template.base_toughness,
        template.base_dexterity,
    )
    if any(value is None for value in required):
        raise ValueError("enemybase template lacks birth inputs")

    lo = int(level_min)
    hi = int(level_max)
    if lo < 1 or hi < lo:
        raise ValueError("invalid enemy level interval")
    init_num = int(template.init_num)
    level_up = int(template.level_up_point)
    endpoint_scales = (
        ((lo - 1) * level_up) + init_num,
        ((hi - 1) * level_up) + init_num,
    )
    if min(endpoint_scales) <= 0:
        raise ValueError("enemy birth scale is non-positive in reachable level interval")
    if endpoint_scales[0] <= endpoint_scales[1]:
        level = lo
        scale = endpoint_scales[0]
    else:
        level = hi
        scale = endpoint_scales[1]

    bases = (
        int(template.base_vital),
        int(template.base_strength),
        int(template.base_toughness),
        int(template.base_dexterity),
    )
    individualized = []
    offsets = []
    for base in bases:
        choices = tuple(
            (base + offset, offset)
            for offset in range(-2, 3)
            if 0 <= base + offset <= 255
        )
        if not choices:
            raise ValueError("enemy birth base has no valid -2..2 individualized value")
        value, offset = min(choices)
        individualized.append(value)
        offsets.append(offset)

    # Ten source allocation draws can all resolve to strength (roll value 1).
    current_base = (
        individualized[0],
        individualized[1] + 10,
        individualized[2],
        individualized[3],
    )
    internal = tuple(scale * value for value in current_base)
    max_hp = int(base_derived_stats(*internal)["max_hp"])
    return {
        "max_hp": max_hp,
        "level": level,
        "scale": scale,
        "birth_offsets": tuple(offsets),
        "allocation_counts": (0, 10, 0, 0),
    }


def analyze_rehp_domain(
    *,
    rehp_skill_ids: Sequence[int],
    enemybase_rows: Sequence[Mapping[str, object]],
    enemy_rows: Sequence[Mapping[str, object]],
    group_rows: Sequence[Mapping[str, object]],
) -> dict[str, object]:
    skill_ids = frozenset(int(value) for value in rehp_skill_ids)
    if not skill_ids:
        raise ValueError("no recovered ReHP skill ID")

    template_by_id: dict[int, PetTemplateBridge] = {}
    rehp_slot_refs = 0
    rehp_tempnos: set[int] = set()
    for row in enemybase_rows:
        template = PetTemplateBridge.from_enemybase(row)
        if template.tempno in template_by_id:
            raise ValueError(f"duplicate enemybase TEMPNO {template.tempno}")
        template_by_id[template.tempno] = template
        slots = tuple(int(row.get(f"PETSKILL{i}", 0)) for i in range(1, 8))
        hits = sum(1 for skill_id in slots if skill_id in skill_ids)
        if hits:
            rehp_slot_refs += hits
            rehp_tempnos.add(template.tempno)

    variant_by_id = {int(row["id"]): row for row in enemy_rows}
    if len(variant_by_id) != len(enemy_rows):
        raise ValueError("duplicate active enemy variant ID")
    missing_templates = sorted(
        {
            int(row["tempno"])
            for row in enemy_rows
            if int(row["tempno"]) not in template_by_id
        }
    )
    if missing_templates:
        raise ValueError("active enemy variants reference missing enemybase templates")

    caster_variants = {
        enemy_id
        for enemy_id, row in variant_by_id.items()
        if int(row["tempno"]) in rehp_tempnos and int(row["create_max"]) > 0
    }

    rehp_groups: list[int] = []
    group_targets: dict[int, tuple[int, ...]] = {}
    for group in group_rows:
        pairs = tuple(
            (int(enemy_id), int(weight))
            for enemy_id, weight in zip(group["enemyids"], group["enemyprobs"])
            if int(enemy_id) >= 0 and int(weight) > 0
        )
        present_casters = tuple(
            enemy_id for enemy_id, _weight in pairs if enemy_id in caster_variants
        )
        if not present_casters:
            continue
        targets = tuple(
            sorted(
                {
                    enemy_id
                    for enemy_id, _weight in pairs
                    if enemy_id in variant_by_id
                    and int(variant_by_id[enemy_id]["create_max"]) > 0
                }
            )
        )
        if not targets:
            raise ValueError("ReHP group has no spawnable enemy targets")
        group_id = int(group["id"])
        rehp_groups.append(group_id)
        group_targets[group_id] = targets

    target_variant_ids = tuple(
        sorted({x for values in group_targets.values() for x in values})
    )
    variant_minima: dict[int, dict[str, object]] = {}
    for enemy_id in target_variant_ids:
        row = variant_by_id[enemy_id]
        lo, hi = normalized_levels(row)
        template = template_by_id[int(row["tempno"])]
        minimum = minimum_birth_max_hp(
            template,
            level_min=lo,
            level_max=hi,
        )
        variant_minima[enemy_id] = {
            "tempno": int(row["tempno"]),
            "level_min": lo,
            "level_max": hi,
            **minimum,
        }

    if variant_minima:
        min_variant = min(
            variant_minima,
            key=lambda enemy_id: (
                int(variant_minima[enemy_id]["max_hp"]),
                enemy_id,
            ),
        )
        min_hp = int(variant_minima[min_variant]["max_hp"])
        groups_for_min = tuple(
            sorted(
                group_id
                for group_id, targets in group_targets.items()
                if min_variant in targets
            )
        )
    else:
        min_variant = None
        min_hp = None
        groups_for_min = ()

    return {
        "rehp_skill_ids": tuple(sorted(skill_ids)),
        "rehp_slot_refs": rehp_slot_refs,
        "rehp_tempnos": tuple(sorted(rehp_tempnos)),
        "caster_variant_ids": tuple(sorted(caster_variants)),
        "rehp_group_ids": tuple(sorted(set(rehp_groups))),
        "target_variant_ids": target_variant_ids,
        "variant_minima": variant_minima,
        "minimum_target_variant": min_variant,
        "minimum_target_max_hp": min_hp,
        "minimum_target_groups": groups_for_min,
        "rand_power_domain_safe": bool(
            min_hp is not None and min_hp >= RAND_POWER_LOWER
        ),
    }


def _active_enemybase_rows(
    data_dir: Path,
    setup: Path,
) -> tuple[str, str, list[dict]]:
    _configured, files = analyze_enemybase(data_dir, setup)
    active = [entry for entry in files if entry["active"]]
    if len(active) != 1:
        raise ValueError("expected exactly one active recovered25 enemybase file")
    chosen = active[0]
    return chosen["name"], chosen["sha"], chosen["rows"]


def emit(data_dir: Path, setup: Path) -> None:
    data_dir = Path(data_dir)
    setup = Path(setup)
    runtime = load_recovered25_petskill_runtime(
        data_dir=data_dir,
        setup=setup,
    )
    rehp_skill_ids = tuple(
        sorted(
            skill_id
            for skill_id, entry in runtime.skills.items()
            if entry.function_name == REHP_CALLBACK
        )
    )

    config = setup_values(setup)
    enemy_path = configured_file(
        data_dir,
        config,
        "enemyfile",
        ["enemy*.txt"],
    )
    group_path = configured_file(
        data_dir,
        config,
        "groupfile",
        ["group*.txt"],
    )
    if enemy_path is None or group_path is None:
        raise ValueError("active recovered25 enemy/group files are required")
    (
        _enemy_raw,
        enemy_rows,
        enemy_bad,
        _enemy_widths,
        _enemy_prefix,
    ) = parse_enemy(enemy_path)
    _group_raw, group_rows, group_bad, _group_widths = parse_group(group_path)
    if enemy_bad or group_bad:
        raise ValueError("active recovered25 enemy/group tables contain malformed rows")

    (
        enemybase_name,
        enemybase_sha,
        enemybase_rows,
    ) = _active_enemybase_rows(data_dir, setup)
    result = analyze_rehp_domain(
        rehp_skill_ids=rehp_skill_ids,
        enemybase_rows=enemybase_rows,
        enemy_rows=enemy_rows,
        group_rows=group_rows,
    )

    print("StoneAge recovered ENEMYSKILL_ReHP hard probe — R1")
    print("No display names or source table rows are stored in this report.")
    print(f"CALLBACK|{REHP_CALLBACK}")
    print(
        "ACTIVE_PETSKILL|"
        f"file={runtime.source_file}|"
        f"sha256={sha256(data_dir / runtime.source_file)}"
    )
    print(
        f"ACTIVE_ENEMYBASE|file={enemybase_name}|sha256={enemybase_sha}"
    )
    print(
        f"ACTIVE_ENEMY|file={enemy_path.name}|"
        f"sha256={sha256(enemy_path)}|rows={len(enemy_rows)}"
    )
    print(
        f"ACTIVE_GROUP|file={group_path.name}|"
        f"sha256={sha256(group_path)}|rows={len(group_rows)}"
    )
    print(
        "REHP_SKILL_IDS|"
        f"count={len(result['rehp_skill_ids'])}|"
        f"ids={','.join(map(str, result['rehp_skill_ids'])) or 'NONE'}"
    )
    print(
        "REHP_ENEMYBASE_REFERENCES|"
        f"slot_refs={result['rehp_slot_refs']}|"
        f"templates={len(result['rehp_tempnos'])}"
    )
    print(
        "REHP_RUNTIME_GRAPH|"
        f"caster_variants={len(result['caster_variant_ids'])}|"
        f"groups={len(result['rehp_group_ids'])}|"
        f"potential_target_variants={len(result['target_variant_ids'])}"
    )
    if result["minimum_target_variant"] is None:
        print("REHP_TARGET_MIN_MAXHP|status=UNRESOLVED_NO_RUNTIME_TARGET")
    else:
        details = result["variant_minima"][result["minimum_target_variant"]]
        print(
            "REHP_TARGET_MIN_MAXHP|"
            f"max_hp={result['minimum_target_max_hp']}|"
            f"enemy_id={result['minimum_target_variant']}|"
            f"tempno={details['tempno']}|"
            f"level={details['level']}|"
            f"level_range={details['level_min']}..{details['level_max']}|"
            f"groups={','.join(map(str, result['minimum_target_groups']))}"
        )
    print(
        "REHP_RAND_100_MAXHP_DOMAIN|"
        f"lower={RAND_POWER_LOWER}|"
        "min_reachable_target_max_hp="
        f"{result['minimum_target_max_hp'] if result['minimum_target_max_hp'] is not None else 'UNKNOWN'}|"
        f"safe={1 if result['rand_power_domain_safe'] else 0}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--setup", type=Path, required=True)
    args = parser.parse_args()
    emit(args.data_dir, args.setup)


if __name__ == "__main__":
    main()
