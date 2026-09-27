#!/usr/bin/env python3
"""Audit recovered-2.5 encounter master data against the versioned stable world."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
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
from tools.stoneage_versioned_world_geometry import parse_versioned_world_geometry
from tools.stoneage_versioned_world_manifest import build_versioned_world_manifest
from tools.stoneage_world_map_library import parse_stable_later_map_manifest


@dataclass(frozen=True)
class EncounterRuntimeAudit:
    stable_area_count: int
    unresolved_positive_group_ref_count: int
    affected_area_count: int
    stable_referenced_group_count: int
    referenced_group_missing_enemy_ref_count: int
    referenced_group_affected_count: int


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


def audit_adapter(adapter: VersionedEncounterRuntimeAdapter) -> EncounterRuntimeAudit:
    referenced_group_ids = {
        int(group_id)
        for area in adapter.encounter_areas
        for group_id, weight in area.group_slots
        if int(group_id) >= 0 and int(weight) > 0
    }
    missing_enemy_refs = 0
    affected_groups = 0
    for group_id in sorted(referenced_group_ids & set(adapter.groups)):
        group = adapter.groups[group_id]
        missing = {
            int(enemy_id)
            for enemy_id, weight in group.enemy_slots
            if (
                int(enemy_id) >= 0
                and int(weight) > 0
                and int(enemy_id) not in adapter.enemies
            )
        }
        if missing:
            affected_groups += 1
            missing_enemy_refs += len(missing)

    return EncounterRuntimeAudit(
        stable_area_count=len(adapter.encounter_areas),
        unresolved_positive_group_ref_count=len(
            adapter.unresolved_positive_group_refs
        ),
        affected_area_count=len(adapter.specimen_defect_area_indices),
        stable_referenced_group_count=len(referenced_group_ids),
        referenced_group_missing_enemy_ref_count=missing_enemy_refs,
        referenced_group_affected_count=affected_groups,
    )


def analyze(
    *,
    lineage_report: Path,
    coverage_report: Path,
    geometry_report: Path,
    data_dir: Path,
    setup: Path | None = None,
) -> tuple[VersionedEncounterRuntimeAdapter, EncounterRuntimeAudit]:
    maps = parse_stable_later_map_manifest(
        lineage_report.read_text(encoding="utf-8")
    )
    world = build_versioned_world_manifest(
        maps=maps,
        coverage_text=coverage_report.read_text(encoding="utf-8"),
    )
    geometry = parse_versioned_world_geometry(
        world=world,
        text=geometry_report.read_text(encoding="utf-8"),
    )

    config = setup_values(setup)
    enc_path = configured_file(
        data_dir, config, "encountfile", ["encount*.txt"]
    )
    group_path = configured_file(
        data_dir, config, "groupfile", ["group*.txt"]
    )
    enemy_path = configured_file(
        data_dir, config, "enemyfile", ["enemy*.txt"]
    )
    if not enc_path or not group_path or not enemy_path:
        raise ValueError("active encounter/group/enemy source files are required")

    _eraw, enc_rows, enc_bad, _ew = parse_encount(enc_path)
    _graw, group_rows, group_bad, _gw = parse_group(group_path)
    _xraw, enemy_rows, enemy_bad, _xw, _prefix = parse_enemy(enemy_path)
    if enc_bad or group_bad or enemy_bad:
        raise ValueError(
            "active encounter/group/enemy source contains malformed rows"
        )

    areas = tuple(_area(row) for row in enc_rows)
    groups = {}
    for row in group_rows:
        bridge = _group(row)
        # The recovered active file contains one duplicate GROUP_ID. The
        # existence set is unambiguous for defect classification; retain the
        # first row here instead of inventing a merge.
        groups.setdefault(bridge.group_id, bridge)
    enemies = {}
    for row in enemy_rows:
        bridge = _enemy(row)
        enemies.setdefault(bridge.enemy_id, bridge)

    adapter = build_versioned_encounter_runtime_adapter(
        world_geometry=geometry,
        all_encounter_areas=areas,
        groups=groups,
        enemies=enemies,
    )
    return adapter, audit_adapter(adapter)


def emit(adapter: VersionedEncounterRuntimeAdapter, audit: EncounterRuntimeAudit) -> None:
    print("StoneAge recovered-2.5 stable-world encounter runtime audit — R1")
    print(
        "SCOPE|derived-encounter-integrity-only|no-original-rows|"
        "no-names|no-dialogue|no-map-payload"
    )
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print(f"COUNT|stable_encounter_areas|{audit.stable_area_count}")
    print(
        "COUNT|stable_unresolved_positive_group_refs|"
        f"{audit.unresolved_positive_group_ref_count}"
    )
    print(
        "COUNT|stable_affected_encounter_areas|"
        f"{audit.affected_area_count}"
    )
    print(
        "COUNT|stable_referenced_groups|"
        f"{audit.stable_referenced_group_count}"
    )
    print(
        "COUNT|stable_referenced_group_missing_enemy_refs|"
        f"{audit.referenced_group_missing_enemy_ref_count}"
    )
    print(
        "COUNT|stable_referenced_groups_affected_by_missing_enemy|"
        f"{audit.referenced_group_affected_count}"
    )
    for area_index in adapter.specimen_defect_area_indices:
        count = sum(
            defect.area_index == area_index
            for defect in adapter.unresolved_positive_group_refs
        )
        floor = next(
            area.floor for area in adapter.encounter_areas
            if area.index == area_index
        )
        print(
            "SPECIMEN_DEFECT_AREA|"
            f"index={area_index}|floor={floor}|"
            f"unresolved_positive_group_refs={count}"
        )
    print(
        "RULE|positive-weight missing group/enemy references remain hard "
        "errors; no synthetic group/enemy is created"
    )
    print("RESOLUTION|VERSIONED_ENCOUNTER_RUNTIME_AUDITED")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lineage-report", type=Path, required=True)
    parser.add_argument("--coverage-report", type=Path, required=True)
    parser.add_argument("--geometry-report", type=Path, required=True)
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--setup", type=Path)
    args = parser.parse_args()
    adapter, audit = analyze(
        lineage_report=args.lineage_report,
        coverage_report=args.coverage_report,
        geometry_report=args.geometry_report,
        data_dir=args.data_dir,
        setup=args.setup,
    )
    emit(adapter, audit)


if __name__ == "__main__":
    main()
