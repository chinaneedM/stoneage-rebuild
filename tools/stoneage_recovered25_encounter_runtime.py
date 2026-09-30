#!/usr/bin/env python3
"""Recovered25 encounter runtime loader for the local reconstruction stack.

This module turns the already verified recovered-2.5 encounter/group/enemy
master-data surface into the versioned encounter adapter used by the
engine-neutral runtime. It does not repair preservation defects or promote
recovered25 data into Taiwan-v1 historical membership.
"""

from __future__ import annotations

from pathlib import Path

from tools.stoneage_encount_chain_probe import (
    configured_file,
    parse_encount,
    parse_enemy,
    parse_group,
    setup_values,
)
from tools.stoneage_tw10_25_encounter_bridge import (
    EncounterAreaBridge,
    EnemyVariantBridge,
    GroupBridge,
)
from tools.stoneage_versioned_encounter_runtime import (
    VersionedEncounterRuntimeAdapter,
    build_versioned_encounter_runtime_adapter,
)
from tools.stoneage_versioned_world_geometry import (
    WORLD_GEOMETRY_REPORT_REF,
    parse_versioned_world_geometry,
)
from tools.stoneage_versioned_world_manifest import (
    COVERAGE_REPORT_REF,
    build_versioned_world_manifest,
)
from tools.stoneage_world_map_library import (
    LINEAGE_REPORT_REF,
    parse_stable_later_map_manifest,
)


ROOT = Path(__file__).resolve().parents[1]


def _area(row: dict) -> EncounterAreaBridge:
    return EncounterAreaBridge(
        index=int(row["index"]),
        floor=int(row["floor"]),
        min_x=min(int(row["x1"]), int(row["x2"])),
        min_y=min(int(row["y1"]), int(row["y2"])),
        max_x=max(int(row["x1"]), int(row["x2"])),
        max_y=max(int(row["y1"]), int(row["y2"])),
        probability_min=int(row["pmin"]),
        probability_max=int(row["pmax"]),
        enemy_max_num=int(row["enemymax"]),
        zorder=int(row["zorder"]),
        group_slots=tuple(
            (int(group_id), int(weight))
            for group_id, weight in zip(
                row["groupids"], row["groupprobs"]
            )
        ),
    )


def _group(row: dict) -> GroupBridge:
    return GroupBridge(
        group_id=int(row["id"]),
        appear_by_item_id=int(row["appear_item"]),
        not_appear_by_item_id=int(row["notappear_item"]),
        enemy_slots=tuple(
            (int(enemy_id), int(weight))
            for enemy_id, weight in zip(
                row["enemyids"], row["enemyprobs"]
            )
        ),
    )


def _enemy(row: dict) -> EnemyVariantBridge:
    lv_min = int(row["lv_min"])
    lv_max = int(row["lv_max"])
    if lv_min == 0:
        lv_min = lv_max
    return EnemyVariantBridge(
        enemy_id=int(row["id"]),
        tempno=int(row["tempno"]),
        level_min=min(lv_min, lv_max),
        level_max=max(lv_min, lv_max),
        create_max=int(row["create_max"]),
        create_min_declared=int(row["create_min"]),
        tactics=int(row["tactics"]),
        exp_override=int(row["exp"]),
        duel_point=int(row["duelpoint"]),
        style=int(row["style"]),
        capturable=bool(int(row["petflg"])),
        drop_slots=tuple(
            (int(item_id), int(weight))
            for item_id, weight in zip(
                row["itemids"], row["itemprobs"]
            )
        ),
    )


def load_recovered25_encounter_runtime(
    *,
    data_dir: Path,
    setup: Path | None = None,
    lineage_report: Path = ROOT / LINEAGE_REPORT_REF,
    coverage_report: Path = ROOT / COVERAGE_REPORT_REF,
    geometry_report: Path = ROOT / WORLD_GEOMETRY_REPORT_REF,
) -> VersionedEncounterRuntimeAdapter:
    """Load the verified active encounter chain into the stable-world adapter."""

    data_dir = Path(data_dir)
    if not data_dir.is_dir():
        raise ValueError("recovered25 encounter data_dir must be a directory")
    if setup is not None and not Path(setup).is_file():
        raise ValueError("recovered25 encounter setup must be a file")

    maps = parse_stable_later_map_manifest(
        Path(lineage_report).read_text(encoding="utf-8")
    )
    world = build_versioned_world_manifest(
        maps=maps,
        coverage_text=Path(coverage_report).read_text(encoding="utf-8"),
    )
    geometry = parse_versioned_world_geometry(
        world=world,
        text=Path(geometry_report).read_text(encoding="utf-8"),
    )

    config = setup_values(None if setup is None else Path(setup))
    enc_path = configured_file(
        data_dir,
        config,
        "encountfile",
        ["encount*.txt"],
    )
    group_path = configured_file(
        data_dir,
        config,
        "groupfile",
        ["group*.txt"],
    )
    enemy_path = configured_file(
        data_dir,
        config,
        "enemyfile",
        ["enemy*.txt"],
    )
    if enc_path is None or group_path is None or enemy_path is None:
        raise ValueError(
            "active recovered25 encounter/group/enemy files are required"
        )

    _enc_raw, enc_rows, enc_bad, _enc_width = parse_encount(enc_path)
    _group_raw, group_rows, group_bad, _group_width = parse_group(group_path)
    (
        _enemy_raw,
        enemy_rows,
        enemy_bad,
        _enemy_width,
        _enemy_prefix,
    ) = parse_enemy(enemy_path)
    if enc_bad or group_bad or enemy_bad:
        raise ValueError(
            "active recovered25 encounter/group/enemy source has malformed rows"
        )

    areas = tuple(_area(row) for row in enc_rows)

    groups: dict[int, GroupBridge] = {}
    for row in group_rows:
        bridge = _group(row)
        # The verified active specimen contains one duplicate GROUP_ID.
        # Preserve loader-first identity for the existence/runtime join rather
        # than inventing a merge across duplicate rows.
        groups.setdefault(bridge.group_id, bridge)

    enemies: dict[int, EnemyVariantBridge] = {}
    for row in enemy_rows:
        bridge = _enemy(row)
        enemies.setdefault(bridge.enemy_id, bridge)

    return build_versioned_encounter_runtime_adapter(
        world_geometry=geometry,
        all_encounter_areas=areas,
        groups=groups,
        enemies=enemies,
    )
