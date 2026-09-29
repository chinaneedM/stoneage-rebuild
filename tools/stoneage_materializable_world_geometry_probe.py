#!/usr/bin/env python3
"""Build strict recovered25 materializable classic-Warp geometry.

The represented world is the immutable 761-floor stable manifest plus the
supplemental extension. Resolved supplemental maps may participate in runtime
geometry; unresolved supplemental floors remain represented but quarantined.

This probe preserves full recovered source geometry and validates both source
and destination coordinates against the materializable map definitions. It
does not interpret conditional-time tokens.
"""

from __future__ import annotations

import argparse
import collections
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

from tools.stoneage_supplemental_world_manifest import (
    parse_supplemental_world_audit,
)
from tools.stoneage_versioned_world_geometry_probe import (
    ClassicWarpGeometry,
    _parse_create_geometry,
)
from tools.stoneage_versioned_world_manifest import (
    build_versioned_world_manifest,
)
from tools.stoneage_world_map_library import (
    parse_stable_later_map_manifest,
)


UNRESOLVED_SOURCE = "UNRESOLVED_SOURCE"
UNRESOLVED_DESTINATION = "UNRESOLVED_DESTINATION"
OUTSIDE_REPRESENTED_WORLD = "OUTSIDE_REPRESENTED_WORLD"
NON_SINGLE_SOURCE = "NON_SINGLE_SOURCE"
SOURCE_OUT_OF_BOUNDS = "SOURCE_OUT_OF_BOUNDS"
DESTINATION_OUT_OF_BOUNDS = "DESTINATION_OUT_OF_BOUNDS"


@dataclass(frozen=True)
class MaterializableWarpGeometry:
    source_floor: int
    source_x: int
    source_y: int
    placement_id: int
    destination_floor: int
    destination_x: int
    destination_y: int
    conditional_time: bool


@dataclass(frozen=True)
class QuarantinedWarpGeometry:
    warp: ClassicWarpGeometry
    reason: str


@dataclass(frozen=True)
class MaterializableWorldGeometryAudit:
    stable_floor_ids: frozenset[int]
    resolved_supplemental_ids: frozenset[int]
    unresolved_supplemental_ids: frozenset[int]
    materializable_warps: tuple[MaterializableWarpGeometry, ...]
    quarantined_warps: tuple[QuarantinedWarpGeometry, ...]
    classic_warps_from_represented_sources: int

    @property
    def counts(self) -> dict[str, int]:
        out = {
            "stable_floor_ids": len(self.stable_floor_ids),
            "resolved_supplemental_floor_ids": len(
                self.resolved_supplemental_ids
            ),
            "unresolved_supplemental_floor_ids": len(
                self.unresolved_supplemental_ids
            ),
            "represented_floor_ids": (
                len(self.stable_floor_ids)
                + len(self.resolved_supplemental_ids)
                + len(self.unresolved_supplemental_ids)
            ),
            "materializable_floor_ids": (
                len(self.stable_floor_ids)
                + len(self.resolved_supplemental_ids)
            ),
            "classic_warps_from_represented_sources": int(
                self.classic_warps_from_represented_sources
            ),
            "materializable_classic_warps": len(self.materializable_warps),
            "quarantined_classic_warps": len(self.quarantined_warps),
            "conditional_time_materializable_warps": sum(
                row.conditional_time for row in self.materializable_warps
            ),
        }
        for row in self.quarantined_warps:
            key = f"quarantine_reason:{row.reason}:edges"
            out[key] = out.get(key, 0) + 1
        return out


def _contains(
    dimensions: Mapping[int, tuple[int, int]],
    floor_id: int,
    x: int,
    y: int,
) -> bool:
    width, height = dimensions[int(floor_id)]
    return 0 <= int(x) < width and 0 <= int(y) < height


def classify_warps(
    *,
    materializable_dimensions: Mapping[int, tuple[int, int]],
    unresolved_floor_ids: set[int],
    represented_floor_ids: set[int],
    warps: tuple[ClassicWarpGeometry, ...],
) -> MaterializableWorldGeometryAudit:
    dimensions = {
        int(floor_id): (int(size[0]), int(size[1]))
        for floor_id, size in materializable_dimensions.items()
    }
    unresolved = set(int(v) for v in unresolved_floor_ids)
    represented = set(int(v) for v in represented_floor_ids)
    materializable_ids = set(dimensions)

    if materializable_ids & unresolved:
        raise ValueError("floor cannot be both materializable and unresolved")
    if materializable_ids | unresolved != represented:
        raise ValueError("represented floor partition drift")

    accepted: list[MaterializableWarpGeometry] = []
    quarantined: list[QuarantinedWarpGeometry] = []

    for warp in warps:
        source = int(warp.source_floor)
        destination = int(warp.destination_floor)

        if source not in represented:
            raise ValueError(
                f"parser emitted warp from unrepresented source floor {source}"
            )
        if source in unresolved:
            quarantined.append(
                QuarantinedWarpGeometry(warp=warp, reason=UNRESOLVED_SOURCE)
            )
            continue
        if not warp.source_is_single_cell:
            quarantined.append(
                QuarantinedWarpGeometry(warp=warp, reason=NON_SINGLE_SOURCE)
            )
            continue

        sx, sy, _sx2, _sy2 = warp.source_rect
        if not _contains(dimensions, source, sx, sy):
            quarantined.append(
                QuarantinedWarpGeometry(warp=warp, reason=SOURCE_OUT_OF_BOUNDS)
            )
            continue

        if destination in unresolved:
            quarantined.append(
                QuarantinedWarpGeometry(
                    warp=warp,
                    reason=UNRESOLVED_DESTINATION,
                )
            )
            continue
        if destination not in represented:
            quarantined.append(
                QuarantinedWarpGeometry(
                    warp=warp,
                    reason=OUTSIDE_REPRESENTED_WORLD,
                )
            )
            continue
        if destination not in materializable_ids:
            raise ValueError(
                f"represented destination {destination} lacks map dimensions"
            )
        if not _contains(
            dimensions,
            destination,
            warp.destination_x,
            warp.destination_y,
        ):
            quarantined.append(
                QuarantinedWarpGeometry(
                    warp=warp,
                    reason=DESTINATION_OUT_OF_BOUNDS,
                )
            )
            continue

        accepted.append(
            MaterializableWarpGeometry(
                source_floor=source,
                source_x=sx,
                source_y=sy,
                placement_id=int(warp.placement_id),
                destination_floor=destination,
                destination_x=int(warp.destination_x),
                destination_y=int(warp.destination_y),
                conditional_time=bool(warp.conditional_time),
            )
        )

    stable_placeholder: frozenset[int] = frozenset()
    return MaterializableWorldGeometryAudit(
        stable_floor_ids=stable_placeholder,
        resolved_supplemental_ids=frozenset(materializable_ids),
        unresolved_supplemental_ids=frozenset(unresolved),
        materializable_warps=tuple(accepted),
        quarantined_warps=tuple(quarantined),
        classic_warps_from_represented_sources=len(warps),
    )


def analyze(
    *,
    lineage_text: str,
    coverage_text: str,
    supplemental_audit_text: str,
    npc_dir: Path,
) -> MaterializableWorldGeometryAudit:
    stable_maps = parse_stable_later_map_manifest(lineage_text)
    stable_world = build_versioned_world_manifest(
        maps=stable_maps,
        coverage_text=coverage_text,
    )
    extension = parse_supplemental_world_audit(
        stable_world=stable_world,
        text=supplemental_audit_text,
    )

    materializable = extension.materializable_map_definitions
    represented = set(extension.reachable_floor_ids)
    unresolved = set(extension.unresolved_by_floor)
    _placements, warps = _parse_create_geometry(npc_dir, represented)

    classified = classify_warps(
        materializable_dimensions={
            floor_id: (definition.width, definition.height)
            for floor_id, definition in materializable.items()
        },
        unresolved_floor_ids=unresolved,
        represented_floor_ids=represented,
        warps=warps,
    )
    return MaterializableWorldGeometryAudit(
        stable_floor_ids=frozenset(stable_world.by_floor),
        resolved_supplemental_ids=frozenset(extension.resolved_by_floor),
        unresolved_supplemental_ids=frozenset(extension.unresolved_by_floor),
        materializable_warps=classified.materializable_warps,
        quarantined_warps=classified.quarantined_warps,
        classic_warps_from_represented_sources=(
            classified.classic_warps_from_represented_sources
        ),
    )


def emit(audit: MaterializableWorldGeometryAudit) -> None:
    print("StoneAge materializable recovered world Warp geometry — R1")
    print(
        "SCOPE|761 stable + resolved supplemental maps|classic Warp source and "
        "destination bounds|unresolved floors quarantined"
    )
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print(
        "RULE|conditional-time presence is preserved but not interpreted; "
        "unresolved floor payloads never enter materializable geometry"
    )
    for key in sorted(audit.counts):
        print(f"COUNT|{key}|{audit.counts[key]}")

    for row in audit.materializable_warps:
        print(
            "MATERIALIZABLE_WARP|"
            f"source={row.source_floor},{row.source_x},{row.source_y}|"
            f"placement={row.placement_id}|"
            f"destination={row.destination_floor},"
            f"{row.destination_x},{row.destination_y}|"
            f"conditional_time={int(row.conditional_time)}"
        )

    for row in audit.quarantined_warps:
        warp = row.warp
        x1, y1, x2, y2 = warp.source_rect
        print(
            "QUARANTINED_WARP|"
            f"source_floor={warp.source_floor}|placement={warp.placement_id}|"
            f"source={x1},{y1},{x2},{y2}|"
            f"destination={warp.destination_floor},"
            f"{warp.destination_x},{warp.destination_y}|"
            f"conditional_time={int(warp.conditional_time)}|"
            f"reason={row.reason}"
        )

    print("RESOLUTION|MATERIALIZABLE_RECOVERED_WORLD_WARP_GEOMETRY_CLOSED")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lineage-report", type=Path, required=True)
    parser.add_argument("--coverage-report", type=Path, required=True)
    parser.add_argument("--supplemental-audit", type=Path, required=True)
    parser.add_argument("--npc-dir", type=Path, required=True)
    args = parser.parse_args()
    emit(
        analyze(
            lineage_text=args.lineage_report.read_text(encoding="utf-8"),
            coverage_text=args.coverage_report.read_text(encoding="utf-8"),
            supplemental_audit_text=args.supplemental_audit.read_text(
                encoding="utf-8"
            ),
            npc_dir=args.npc_dir,
        )
    )


if __name__ == "__main__":
    main()
