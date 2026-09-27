#!/usr/bin/env python3
"""Extract versioned non-dialogue world geometry from recovered StoneAge data.

The output intentionally retains only deterministic structural metadata:
- NPC create birth/move rectangles and basic numeric spawn controls;
- classic overlap Warp source-region -> destination geometry;
- encounter rectangles and numeric encounter envelope.

It never stores NPC names, dialogue, template names, arbitrary NPC arguments,
item/quest conditions, or map payload bytes.

All recovered server semantics are tagged as recovered25/LATER_RECOVERED and
must never be interpreted as Taiwan-v1 membership.
"""

from __future__ import annotations

import argparse
import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

from tools.stoneage_encount_chain_probe import (
    configured_file,
    parse_encount,
    setup_values as encounter_setup_values,
)
from tools.stoneage_npc_world_graph_probe import (
    collect_server_map_ids,
    iter_blocks,
    magic_kind,
)
from tools.stoneage_warp_transition_model import parse_legacy_warp_arg
from tools.stoneage_world_map_library import (
    parse_stable_later_map_manifest,
)


SOURCE_VERSION = "recovered25"
EVIDENCE_ROLE = "LATER_RECOVERED"
CLASSIC_WARP_FUNCTIONSET = b"warp"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _int(value: bytes | None, default: int = 0) -> int:
    if value is None:
        return int(default)
    try:
        return int(value.strip(), 10)
    except (ValueError, TypeError):
        return int(default)


def _four_ints(value: bytes) -> tuple[int, int, int, int]:
    """Mirror descendant getFourIntsFromString(): missing comma fields -> 0."""
    pieces = [piece.strip() for piece in value.strip().split(b",")]
    if len(pieces) > 4:
        raise ValueError(
            f"expected at most four integer fields, got {len(pieces)}"
        )
    out: list[int] = []
    try:
        for piece in pieces:
            out.append(int(piece, 10) if piece else 0)
    except ValueError as exc:
        raise ValueError("invalid four-integer NPC geometry") from exc
    while len(out) < 4:
        out.append(0)
    return tuple(out)  # type: ignore[return-value]

def _rect_from_fields(
    fields: dict[bytes, bytes],
    *,
    center_key: bytes,
    corner_key: bytes,
) -> tuple[int, int, int, int] | None:
    if corner_key in fields:
        x1, y1, x2, y2 = _four_ints(fields[corner_key])
        return (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
    if center_key in fields:
        x, y, width, height = _four_ints(fields[center_key])
        return (
            x - int(width / 2),
            y - int(height / 2),
            x + int(width / 2),
            y + int(height / 2),
        )
    return None


def _template_functionsets(npc_dir: Path) -> dict[bytes, bytes]:
    first: dict[bytes, bytes] = {}
    template_paths = sorted(
        (
            path for path in npc_dir.rglob("*")
            if path.is_file() and magic_kind(path) == "template"
        ),
        key=lambda path: str(path).lower(),
    )
    for path in template_paths:
        for entries in iter_blocks(path):
            fields: dict[bytes, bytes] = {}
            for key, value in entries:
                fields[key] = value
            name = fields.get(b"templatename", b"").strip()
            if name and name.lower() not in first:
                first[name.lower()] = fields.get(
                    b"functionset", b""
                ).strip().lower()
    return first


@dataclass(frozen=True)
class NpcPlacementGeometry:
    floor_id: int
    placement_id: int
    birth_rect: tuple[int, int, int, int]
    move_rect: tuple[int, int, int, int]
    direction: int
    create_num: int
    respawn_time: int
    boundary: int
    ignore_invincible: int
    resolved_template_refs: int
    classic_warp_refs: int

    def __post_init__(self) -> None:
        object.__setattr__(self, "floor_id", int(self.floor_id))
        object.__setattr__(self, "placement_id", int(self.placement_id))
        for name in ("birth_rect", "move_rect"):
            rect = tuple(int(value) for value in getattr(self, name))
            if len(rect) != 4:
                raise ValueError(f"{name} must have four values")
            x1, y1, x2, y2 = rect
            if x1 > x2 or y1 > y2:
                raise ValueError(f"{name} is not normalized")
            object.__setattr__(self, name, rect)
        for name in (
            "direction",
            "create_num",
            "respawn_time",
            "boundary",
            "ignore_invincible",
            "resolved_template_refs",
            "classic_warp_refs",
        ):
            object.__setattr__(self, name, int(getattr(self, name)))
        if self.resolved_template_refs < 0 or self.classic_warp_refs < 0:
            raise ValueError("NPC template-ref counts cannot be negative")
        if self.classic_warp_refs > self.resolved_template_refs:
            raise ValueError("classic warp refs cannot exceed resolved refs")


@dataclass(frozen=True)
class ClassicWarpGeometry:
    source_floor: int
    placement_id: int
    source_rect: tuple[int, int, int, int]
    destination_floor: int
    destination_x: int
    destination_y: int
    conditional_time: bool
    destination_is_stable_candidate: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "source_floor", int(self.source_floor))
        object.__setattr__(self, "placement_id", int(self.placement_id))
        rect = tuple(int(value) for value in self.source_rect)
        if len(rect) != 4:
            raise ValueError("source_rect must have four values")
        if rect[0] > rect[2] or rect[1] > rect[3]:
            raise ValueError("source_rect is not normalized")
        object.__setattr__(self, "source_rect", rect)
        object.__setattr__(
            self, "destination_floor", int(self.destination_floor)
        )
        object.__setattr__(
            self, "destination_x", int(self.destination_x)
        )
        object.__setattr__(
            self, "destination_y", int(self.destination_y)
        )
        object.__setattr__(
            self, "conditional_time", bool(self.conditional_time)
        )
        object.__setattr__(
            self,
            "destination_is_stable_candidate",
            bool(self.destination_is_stable_candidate),
        )

    @property
    def source_is_single_cell(self) -> bool:
        x1, y1, x2, y2 = self.source_rect
        return x1 == x2 and y1 == y2


@dataclass(frozen=True)
class EncounterAreaGeometry:
    index: int
    floor_id: int
    rect: tuple[int, int, int, int]
    probability_min: int
    probability_max: int
    enemy_max_num: int
    zorder: int
    positive_group_ref_count: int

    def __post_init__(self) -> None:
        for name in (
            "index",
            "floor_id",
            "probability_min",
            "probability_max",
            "enemy_max_num",
            "zorder",
            "positive_group_ref_count",
        ):
            object.__setattr__(self, name, int(getattr(self, name)))
        rect = tuple(int(value) for value in self.rect)
        if len(rect) != 4:
            raise ValueError("encounter rect must have four values")
        if rect[0] > rect[2] or rect[1] > rect[3]:
            raise ValueError("encounter rect is not normalized")
        object.__setattr__(self, "rect", rect)
        if self.positive_group_ref_count < 0:
            raise ValueError("positive group-ref count cannot be negative")


@dataclass(frozen=True)
class WorldGeometry:
    placements: tuple[NpcPlacementGeometry, ...]
    classic_warps: tuple[ClassicWarpGeometry, ...]
    encounters: tuple[EncounterAreaGeometry, ...]
    stable_floor_ids: tuple[int, ...]

    def __post_init__(self) -> None:
        placements = tuple(self.placements)
        warps = tuple(self.classic_warps)
        encounters = tuple(self.encounters)
        stable = tuple(sorted(set(int(value) for value in self.stable_floor_ids)))
        stable_set = set(stable)
        if any(row.floor_id not in stable_set for row in placements):
            raise ValueError("NPC placement lies outside stable map candidates")
        if any(row.source_floor not in stable_set for row in warps):
            raise ValueError("classic warp source lies outside stable map candidates")
        if any(row.floor_id not in stable_set for row in encounters):
            raise ValueError("encounter area lies outside stable map candidates")
        object.__setattr__(self, "placements", placements)
        object.__setattr__(self, "classic_warps", warps)
        object.__setattr__(self, "encounters", encounters)
        object.__setattr__(self, "stable_floor_ids", stable)


def _parse_create_geometry(
    npc_dir: Path,
    stable_floor_ids: set[int],
) -> tuple[
    tuple[NpcPlacementGeometry, ...],
    tuple[ClassicWarpGeometry, ...],
]:
    functionsets = _template_functionsets(npc_dir)
    create_paths = sorted(
        (
            path for path in npc_dir.rglob("*")
            if path.is_file() and magic_kind(path) == "create"
        ),
        key=lambda path: str(path).lower(),
    )

    placements: list[NpcPlacementGeometry] = []
    warps: list[ClassicWarpGeometry] = []
    placement_id = 0

    for path in create_paths:
        for entries in iter_blocks(path):
            fields: dict[bytes, bytes] = {}
            enemies: list[tuple[bytes, bytes | None]] = []
            for key, value in entries:
                if key == b"enemy":
                    name, separator, arg = value.partition(b"|")
                    enemies.append(
                        (
                            name.strip().lower(),
                            arg if separator else None,
                        )
                    )
                else:
                    fields[key] = value

            floor_id = _int(fields.get(b"floorid"), 0)
            birth = _rect_from_fields(
                fields,
                center_key=b"borncenter",
                corner_key=b"borncorner",
            )
            if floor_id not in stable_floor_ids or birth is None:
                continue
            move = _rect_from_fields(
                fields,
                center_key=b"movecenter",
                corner_key=b"movecorner",
            ) or birth

            resolved = 0
            classic_warp_refs = 0
            for template_name, arg in enemies:
                functionset = functionsets.get(template_name)
                if functionset is None:
                    continue
                resolved += 1
                if functionset != CLASSIC_WARP_FUNCTIONSET or arg is None:
                    continue
                parsed = parse_legacy_warp_arg(
                    arg.decode("utf-8", "replace")
                )
                if parsed is None:
                    continue
                classic_warp_refs += 1
                destination_floor, destination_x, destination_y = (
                    parsed["destination"]
                )
                warps.append(
                    ClassicWarpGeometry(
                        source_floor=floor_id,
                        placement_id=placement_id,
                        source_rect=birth,
                        destination_floor=destination_floor,
                        destination_x=destination_x,
                        destination_y=destination_y,
                        conditional_time=bool(parsed["time_token"]),
                        destination_is_stable_candidate=(
                            destination_floor in stable_floor_ids
                        ),
                    )
                )

            if resolved <= 0:
                continue
            placements.append(
                NpcPlacementGeometry(
                    floor_id=floor_id,
                    placement_id=placement_id,
                    birth_rect=birth,
                    move_rect=move,
                    direction=_int(fields.get(b"dir"), 0),
                    create_num=_int(fields.get(b"createnum"), 0),
                    respawn_time=_int(fields.get(b"time"), 0),
                    boundary=_int(fields.get(b"boundary"), 1),
                    ignore_invincible=_int(
                        fields.get(b"ignoreinvincible"), 0
                    ),
                    resolved_template_refs=resolved,
                    classic_warp_refs=classic_warp_refs,
                )
            )
            placement_id += 1

    return tuple(placements), tuple(warps)


def _parse_encounter_geometry(
    data_dir: Path,
    setup: Path | None,
    stable_floor_ids: set[int],
) -> tuple[EncounterAreaGeometry, ...]:
    config = encounter_setup_values(setup)
    path = configured_file(
        data_dir,
        config,
        "encountfile",
        ["encount*.txt"],
    )
    if path is None:
        raise ValueError("recovered data has no active encounter file")
    _raw, rows, malformed, _widths = parse_encount(path)
    if malformed:
        raise ValueError(
            f"active encounter file contains {malformed} malformed rows"
        )

    out = []
    for row in rows:
        floor_id = int(row["floor"])
        if floor_id not in stable_floor_ids:
            continue
        out.append(
            EncounterAreaGeometry(
                index=int(row["index"]),
                floor_id=floor_id,
                rect=(
                    min(int(row["x1"]), int(row["x2"])),
                    min(int(row["y1"]), int(row["y2"])),
                    max(int(row["x1"]), int(row["x2"])),
                    max(int(row["y1"]), int(row["y2"])),
                ),
                probability_min=int(row["pmin"]),
                probability_max=int(row["pmax"]),
                enemy_max_num=int(row["enemymax"]),
                zorder=int(row["zorder"]),
                positive_group_ref_count=sum(
                    1
                    for group_id, weight in zip(
                        row["groupids"], row["groupprobs"]
                    )
                    if int(group_id) >= 0 and int(weight) > 0
                ),
            )
        )
    return tuple(out)


def analyze_world_geometry(
    *,
    lineage_report: Path,
    npc_dir: Path,
    data_dir: Path,
    map_dir: Path,
    setup: Path | None = None,
) -> WorldGeometry:
    manifest = parse_stable_later_map_manifest(
        lineage_report.read_text(encoding="utf-8")
    )
    stable_floor_ids = {
        candidate.floor_id for candidate in manifest.candidates
    }
    server_map_ids, _map_files = collect_server_map_ids(map_dir)
    if not server_map_ids:
        raise ValueError("recovered server map set is empty")
    effective_stable_floor_ids = stable_floor_ids & server_map_ids
    placements, warps = _parse_create_geometry(
        npc_dir,
        effective_stable_floor_ids,
    )
    encounters = _parse_encounter_geometry(
        data_dir,
        setup,
        stable_floor_ids,
    )
    return WorldGeometry(
        placements=placements,
        classic_warps=warps,
        encounters=encounters,
        stable_floor_ids=tuple(stable_floor_ids),
    )


def emit(
    geometry: WorldGeometry,
    *,
    lineage_report_sha256: str,
) -> None:
    print("StoneAge recovered-2.5 stable-map world geometry — R1")
    print(
        "SCOPE|derived-numeric-world-geometry-only|"
        "no-npc-names|no-template-names|no-dialogue|"
        "no-arbitrary-arguments|no-map-payload"
    )
    print(f"SEMANTIC_SOURCE_VERSION|{SOURCE_VERSION}")
    print(f"EVIDENCE_ROLE|{EVIDENCE_ROLE}")
    print(f"LINEAGE_REPORT_SHA256|{lineage_report_sha256}")
    print(
        "RULE|all emitted NPC/warp/encounter semantics are recovered25 "
        "LATER_RECOVERED and do not prove Taiwan-v1 membership"
    )
    print(
        "WARP_RULE|only classic functionset=Warp with parseable "
        "floor|x|y|optional-time is emitted; WarpMan/FMWarpMan excluded"
    )
    print(f"COUNT|stable_floor_candidates|{len(geometry.stable_floor_ids)}")
    print(f"COUNT|npc_placements|{len(geometry.placements)}")
    print(f"COUNT|classic_warp_edges|{len(geometry.classic_warps)}")
    print(
        "COUNT|classic_warp_single_cell_sources|"
        f"{sum(row.source_is_single_cell for row in geometry.classic_warps)}"
    )
    print(
        "COUNT|classic_warp_conditional_time|"
        f"{sum(row.conditional_time for row in geometry.classic_warps)}"
    )
    print(
        "COUNT|classic_warp_destinations_stable|"
        f"{sum(row.destination_is_stable_candidate for row in geometry.classic_warps)}"
    )
    print(f"COUNT|encounter_areas|{len(geometry.encounters)}")

    for row in geometry.placements:
        bx1, by1, bx2, by2 = row.birth_rect
        mx1, my1, mx2, my2 = row.move_rect
        print(
            "NPC_PLACEMENT|"
            f"floor={row.floor_id}|placement={row.placement_id}|"
            f"birth={bx1},{by1},{bx2},{by2}|"
            f"move={mx1},{my1},{mx2},{my2}|"
            f"dir={row.direction}|create_num={row.create_num}|"
            f"respawn_time={row.respawn_time}|boundary={row.boundary}|"
            f"ignore_invincible={row.ignore_invincible}|"
            f"resolved_templates={row.resolved_template_refs}|"
            f"classic_warp_refs={row.classic_warp_refs}"
        )

    for row in geometry.classic_warps:
        x1, y1, x2, y2 = row.source_rect
        print(
            "CLASSIC_WARP|"
            f"floor={row.source_floor}|placement={row.placement_id}|"
            f"source={x1},{y1},{x2},{y2}|"
            f"to={row.destination_floor},{row.destination_x},{row.destination_y}|"
            f"conditional_time={int(row.conditional_time)}|"
            f"destination_stable={int(row.destination_is_stable_candidate)}"
        )

    for row in geometry.encounters:
        x1, y1, x2, y2 = row.rect
        print(
            "ENCOUNTER_AREA|"
            f"index={row.index}|floor={row.floor_id}|"
            f"rect={x1},{y1},{x2},{y2}|"
            f"prob_min={row.probability_min}|"
            f"prob_max={row.probability_max}|"
            f"enemy_max={row.enemy_max_num}|"
            f"zorder={row.zorder}|"
            f"positive_group_refs={row.positive_group_ref_count}"
        )

    print("RESOLUTION|VERSIONED_WORLD_GEOMETRY_CLASSIFIED")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lineage-report", type=Path, required=True)
    parser.add_argument("--npc-dir", type=Path, required=True)
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--map-dir", type=Path, required=True)
    parser.add_argument("--setup", type=Path)
    args = parser.parse_args()

    geometry = analyze_world_geometry(
        lineage_report=args.lineage_report,
        npc_dir=args.npc_dir,
        data_dir=args.data_dir,
        map_dir=args.map_dir,
        setup=args.setup,
    )
    emit(
        geometry,
        lineage_report_sha256=_sha256(args.lineage_report),
    )


if __name__ == "__main__":
    main()
