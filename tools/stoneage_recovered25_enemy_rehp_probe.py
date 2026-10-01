#!/usr/bin/env python3
"""Hard-probe the recovered25 ENEMYSKILL_ReHP data/runtime domain.

The report intentionally stores only derived counts/mechanics. It does not
copy recovered names, comments or OPTION payload text.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from types import SimpleNamespace

from tools.stoneage_recovered25_encounter_runtime import (
    load_recovered25_encounter_runtime,
)
from tools.stoneage_recovered25_enemybase_runtime import (
    load_recovered25_enemybase_runtime,
)
from tools.stoneage_recovered25_petskill_runtime import (
    load_recovered25_petskill_runtime,
)
from tools.stoneage_tw10_25_bridge_model import build_pet_birth_bridge


REHP_CALLBACK = "ENEMYSKILL_ReHP"
HELP_CALLBACK = "ENEMYSKILL_EnemyHelp"


def minimum_possible_variant_max_hp(template, variant) -> int:
    """Minimum source-shaped spawn max HP over the variant's birth RNG domain.

    max_hp is monotone in the four internal stats. Birth offsets therefore use
    the smallest legal per-component value, and all ten allocation draws are
    placed in a non-vital stat because VITAL has HP weight four while the other
    three stats have weight one. Level scale is affine, so checking both level
    endpoints is sufficient even if a future recovered row has unusual growth.
    """

    bases = (
        template.base_vital,
        template.base_strength,
        template.base_toughness,
        template.base_dexterity,
    )
    if any(value is None for value in bases):
        raise ValueError("ReHP max-HP proof requires complete enemybase growth inputs")
    normalized = tuple(int(value) for value in bases)
    if any(value < 0 for value in normalized):
        raise ValueError("ReHP max-HP proof does not admit negative growth bases")
    offsets = tuple(-min(2, value) for value in normalized)
    levels = tuple(sorted({int(variant.level_min), int(variant.level_max)}))
    values = []
    for level in levels:
        birth = build_pet_birth_bridge(
            template,
            level=level,
            birth_offsets=offsets,
            # All ten points to STR. TOUGH/DEX are equivalent for max-HP weight.
            spawn_allocation_rolls=(1,) * 10,
        )
        values.append(int(birth.combat_projection()["max_hp"]))
    return min(values)


def _callback_skill_ids(petskill_runtime, callback: str) -> tuple[int, ...]:
    return tuple(
        sorted(
            int(entry.skill_id)
            for entry in petskill_runtime.skills.values()
            if entry.function_name == callback
        )
    )


def _template_skill_ref_count(enemybase_runtime, skill_ids: set[int]) -> tuple[int, set[int]]:
    refs = 0
    tempnos: set[int] = set()
    for tempno, template in enemybase_runtime.templates.items():
        for skill_id in template.skill_slot_ids:
            if int(skill_id) in skill_ids:
                refs += 1
                tempnos.add(int(tempno))
    return refs, tempnos


def analyze_runtime_objects(petskill_runtime, enemybase_runtime, encounter_runtime):
    rehp_ids = _callback_skill_ids(petskill_runtime, REHP_CALLBACK)
    if len(rehp_ids) != 1:
        raise ValueError("recovered25 ReHP probe requires exactly one callback row")
    rehp_id = int(rehp_ids[0])
    entry = petskill_runtime.skills[rehp_id]

    ref_count, rehp_tempnos = _template_skill_ref_count(
        enemybase_runtime, {rehp_id}
    )

    runtime_group_ids = {
        int(group_id)
        for area in encounter_runtime.encounter_areas
        for group_id, weight in area.group_slots
        if int(group_id) >= 0
        and int(weight) > 0
        and int(group_id) in encounter_runtime.groups
    }

    rehp_variant_ids = {
        int(enemy_id)
        for enemy_id, variant in encounter_runtime.enemies.items()
        if int(variant.tempno) in rehp_tempnos and int(variant.create_max) > 0
    }

    rehp_group_ids: set[int] = set()
    target_variant_ids: set[int] = set()
    for group_id in runtime_group_ids:
        group = encounter_runtime.groups[group_id]
        positive = tuple(
            int(enemy_id)
            for enemy_id, weight in group.enemy_slots
            if int(enemy_id) >= 0
            and int(weight) > 0
            and int(enemy_id) in encounter_runtime.enemies
            and int(encounter_runtime.enemies[int(enemy_id)].create_max) > 0
        )
        if any(enemy_id in rehp_variant_ids for enemy_id in positive):
            rehp_group_ids.add(group_id)
            target_variant_ids.update(positive)

    missing_rehp_tempnos = tuple(
        sorted(
            tempno
            for tempno in rehp_tempnos
            if not any(
                int(variant.tempno) == tempno
                for variant in encounter_runtime.enemies.values()
            )
        )
    )

    caster_min_values = []
    for enemy_id in sorted(rehp_variant_ids):
        variant = encounter_runtime.enemies[enemy_id]
        template = enemybase_runtime.templates[int(variant.tempno)]
        caster_min_values.append(
            minimum_possible_variant_max_hp(template, variant)
        )

    target_min_values = []
    target_tempnos: set[int] = set()
    for enemy_id in sorted(target_variant_ids):
        variant = encounter_runtime.enemies[enemy_id]
        target_tempnos.add(int(variant.tempno))
        template = enemybase_runtime.templates[int(variant.tempno)]
        target_min_values.append(
            minimum_possible_variant_max_hp(template, variant)
        )

    help_ids = set(_callback_skill_ids(petskill_runtime, HELP_CALLBACK))
    _help_refs, help_tempnos = _template_skill_ref_count(
        enemybase_runtime, help_ids
    )
    help_variant_ids = {
        int(enemy_id)
        for enemy_id, variant in encounter_runtime.enemies.items()
        if int(variant.tempno) in help_tempnos and int(variant.create_max) > 0
    }
    groups_with_help = set()
    for group_id in rehp_group_ids:
        group = encounter_runtime.groups[group_id]
        positive_ids = {
            int(enemy_id)
            for enemy_id, weight in group.enemy_slots
            if int(enemy_id) >= 0 and int(weight) > 0
        }
        if positive_ids & help_variant_ids:
            groups_with_help.add(group_id)

    caster_min = min(caster_min_values) if caster_min_values else None
    target_min = min(target_min_values) if target_min_values else None
    reversed_rand_closed = bool(
        ref_count == 31
        and not missing_rehp_tempnos
        and target_min is not None
        and target_min >= 100
        and not groups_with_help
    )

    return {
        "rehp_skill_id": rehp_id,
        "rehp_field": int(entry.field),
        "rehp_target": int(entry.target),
        "rehp_cost": int(entry.cost),
        "rehp_illegal": int(entry.illegal),
        "rehp_option_bytes": len(entry.option_bytes),
        "rehp_option_ascii": bool(entry.option_bytes.isascii()),
        "rehp_option_empty": not bool(entry.option_bytes),
        "enemybase_slot_references": int(ref_count),
        "enemybase_templates_with_rehp": len(rehp_tempnos),
        "runtime_rehp_variants": len(rehp_variant_ids),
        "runtime_rehp_groups": len(rehp_group_ids),
        "runtime_rehp_target_variants": len(target_variant_ids),
        "runtime_rehp_target_templates": len(target_tempnos),
        "missing_rehp_tempnos": missing_rehp_tempnos,
        "enemyhelp_skill_rows": len(help_ids),
        "runtime_rehp_groups_with_enemyhelp": len(groups_with_help),
        "rehp_caster_min_possible_max_hp": caster_min,
        "rehp_target_min_possible_max_hp": target_min,
        "reversed_rand_closed": reversed_rand_closed,
    }


def analyze(data_dir: Path, setup: Path | None):
    petskills = load_recovered25_petskill_runtime(
        data_dir=data_dir,
        setup=setup,
    )
    enemybase = load_recovered25_enemybase_runtime(
        data_dir=data_dir,
        setup=setup,
    )
    encounter = load_recovered25_encounter_runtime(
        data_dir=data_dir,
        setup=setup,
    )
    return analyze_runtime_objects(petskills, enemybase, encounter)


def emit(result) -> None:
    print("StoneAge recovered25 enemy ReHP probe — R1")
    print("No original names/comments/OPTION text are stored in this report.")
    print(f"COUNT|rehp_skill_rows|1")
    print(
        "REHP_ROW|"
        f"field={result['rehp_field']}|target={result['rehp_target']}|"
        f"cost={result['rehp_cost']}|illegal={result['rehp_illegal']}|"
        f"option_bytes={result['rehp_option_bytes']}|"
        f"option_ascii={int(result['rehp_option_ascii'])}|"
        f"option_empty={int(result['rehp_option_empty'])}"
    )
    for key in (
        "enemybase_slot_references",
        "enemybase_templates_with_rehp",
        "runtime_rehp_variants",
        "runtime_rehp_groups",
        "runtime_rehp_target_variants",
        "runtime_rehp_target_templates",
        "enemyhelp_skill_rows",
        "runtime_rehp_groups_with_enemyhelp",
    ):
        print(f"COUNT|{key}|{result[key]}")
    print(
        "COUNT|missing_rehp_tempnos|"
        f"{len(result['missing_rehp_tempnos'])}"
    )
    print(
        "MIN|rehp_caster_min_possible_max_hp|"
        f"{result['rehp_caster_min_possible_max_hp']}"
    )
    print(
        "MIN|rehp_target_min_possible_max_hp|"
        f"{result['rehp_target_min_possible_max_hp']}"
    )
    print(
        "RAND_REVERSED_EDGE|"
        f"closed={int(result['reversed_rand_closed'])}"
    )
    print(
        "RESOLUTION|"
        + (
            "RECOVERED25_ENEMY_REHP_DATA_DOMAIN_CLOSED"
            if result["reversed_rand_closed"]
            else "RECOVERED25_ENEMY_REHP_DATA_DOMAIN_OPEN"
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--setup", type=Path)
    args = parser.parse_args()
    emit(analyze(args.data_dir, args.setup))


if __name__ == "__main__":
    main()
