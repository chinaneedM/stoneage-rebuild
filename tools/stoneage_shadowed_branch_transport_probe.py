#!/usr/bin/env python3
"""Audit non-classic recovered25 transport ingress into the shadowed Warp branch.

Scope is deliberately narrow and provenance-safe. The canonical ordered classic-
Warp runtime defines the currently reachable floor set and the eleven resolved
supplemental floors outside that closure. This probe then inspects recovered25
NPC data for three already-understood transport classes:

- WarpMan: dialogue-triggered WARP candidate destinations;
- FMWarpMan: family/schedule-gated WARP1/WARP2 destinations;
- Airplane: recovered cross-floor route transitions.

Bus is explicitly excluded as a cross-floor ingress mechanism because its
recovered route points are x,y only and the closed transport core does not warp
floors.

Only derived floor-level edges/counts are emitted. No NPC/template names,
argument filenames, dialogue, item IDs, coordinates, or raw argument payloads
are retained.
"""

from __future__ import annotations

import argparse
import collections
from dataclasses import dataclass
from pathlib import Path

from tools.stoneage_ordered_warp_runtime import (
    load_ordered_materializable_runtime,
)
from tools.stoneage_transport_usage_probe import (
    assigned_file,
    iter_blocks,
    magic_kind,
    merge_file,
    template_map,
)


WARPMAN = "WarpMan"
FMWARPMAN = "FMWarpMan"
AIRPLANE = "Airplane"
BUS = "Bus"

INTERACTIVE_DIALOGUE = "INTERACTIVE_DIALOGUE"
CONDITIONAL_FAMILY_SCHEDULE = "CONDITIONAL_FAMILY_SCHEDULE"
INTERACTIVE_AIR_ROUTE = "INTERACTIVE_AIR_ROUTE"

OUTPUT_RESOLUTION = "RESOLUTION|SHADOWED_BRANCH_NONCLASSIC_INGRESS_AUDITED"


def _int(value: bytes | None, default: int = 0) -> int:
    if value is None:
        return default
    try:
        return int(value.strip(), 10)
    except ValueError:
        return default


def _field(data: bytes, key: bytes) -> bytes | None:
    wanted = key.strip().lower()
    for token in data.split(b"|"):
        token = token.strip()
        if b":" not in token:
            continue
        name, value = token.split(b":", 1)
        if name.strip().lower() == wanted:
            return value.strip()
    return None


def _assigned_data(npc_dir: Path, arg: bytes) -> bytes | None:
    filename = assigned_file(arg)
    if filename is None:
        return arg
    path = npc_dir / filename
    if not path.is_file():
        return None
    return merge_file(path)


def _triple(value: bytes) -> tuple[int, int, int] | None:
    parts = tuple(part.strip() for part in value.split(b","))
    if len(parts) < 3:
        return None
    try:
        return int(parts[0]), int(parts[1]), int(parts[2])
    except ValueError:
        return None


def _warpman_destinations(data: bytes) -> tuple[int, ...]:
    value = _field(data, b"WARP")
    if value is None:
        return ()
    floors = []
    for point in value.split(b";")[:20]:
        parsed = _triple(point)
        if parsed is not None and parsed[0] > 0:
            floors.append(parsed[0])
    return tuple(floors)


def _fmwarpman_destinations(data: bytes) -> tuple[int, ...]:
    floors = []
    for key in (b"WARP1", b"WARP2"):
        value = _field(data, key)
        if value is None:
            continue
        parsed = _triple(value)
        if parsed is not None and parsed[0] > 0:
            floors.append(parsed[0])
    return tuple(floors)


def _airplane_floor_transitions(
    *,
    source_floor: int,
    data: bytes,
) -> tuple[tuple[int, int], ...]:
    routenum = _int(_field(data, b"routenum"), 0)
    edges = []
    for route_index in range(1, max(0, routenum) + 1):
        route = _field(data, f"routeto{route_index}".encode())
        if route is None:
            continue
        current_floor = int(source_floor)
        for point in route.split(b";"):
            parsed = _triple(point)
            if parsed is None:
                continue
            next_floor = int(parsed[0])
            if next_floor <= 0:
                continue
            if next_floor != current_floor:
                edges.append((current_floor, next_floor))
            current_floor = next_floor
    return tuple(edges)


@dataclass(frozen=True)
class NonClassicFloorEdge:
    kind: str
    source_floor: int
    destination_floor: int
    condition_class: str
    source_currently_reachable: bool
    destination_is_shadowed_branch: bool

    def __post_init__(self) -> None:
        if self.kind not in {WARPMAN, FMWARPMAN, AIRPLANE}:
            raise ValueError("unsupported non-classic transport kind")
        if int(self.source_floor) < 0 or int(self.destination_floor) < 0:
            raise ValueError("transport floor id cannot be negative")
        if self.condition_class not in {
            INTERACTIVE_DIALOGUE,
            CONDITIONAL_FAMILY_SCHEDULE,
            INTERACTIVE_AIR_ROUTE,
        }:
            raise ValueError("invalid transport condition class")
        object.__setattr__(self, "source_floor", int(self.source_floor))
        object.__setattr__(self, "destination_floor", int(self.destination_floor))


@dataclass(frozen=True)
class NonClassicIngressAudit:
    shadowed_branch_floor_ids: tuple[int, ...]
    classic_reachable_floor_ids: frozenset[int]
    edges: tuple[NonClassicFloorEdge, ...]
    reference_counts: collections.Counter

    @property
    def potential_ingress(self) -> tuple[NonClassicFloorEdge, ...]:
        return tuple(
            edge
            for edge in self.edges
            if edge.source_currently_reachable
            and edge.destination_is_shadowed_branch
        )

    @property
    def counts(self) -> dict[str, int]:
        out = {
            "classic_reachable_floor_ids": len(self.classic_reachable_floor_ids),
            "shadowed_branch_floor_ids": len(self.shadowed_branch_floor_ids),
            "derived_nonclassic_floor_edges": len(self.edges),
            "potential_ingress_edges": len(self.potential_ingress),
            "potential_ingress_destination_floors": len({
                edge.destination_floor for edge in self.potential_ingress
            }),
            "bus_cross_floor_edges": 0,
        }
        for kind in (WARPMAN, FMWARPMAN, AIRPLANE):
            out[f"{kind}:refs"] = int(self.reference_counts[(kind, "refs")])
            out[f"{kind}:resolved_args"] = int(
                self.reference_counts[(kind, "resolved_args")]
            )
            out[f"{kind}:missing_args"] = int(
                self.reference_counts[(kind, "missing_args")]
            )
            out[f"{kind}:derived_edges"] = sum(
                edge.kind == kind for edge in self.edges
            )
            out[f"{kind}:potential_ingress_edges"] = sum(
                edge.kind == kind for edge in self.potential_ingress
            )
        out[f"{BUS}:refs"] = int(self.reference_counts[(BUS, "refs")])
        return out


def analyze(npc_dir: Path) -> NonClassicIngressAudit:
    runtime = load_ordered_materializable_runtime()
    reached = runtime.reachable_floor_ids
    shadowed = tuple(runtime.unreachable_resolved_supplemental_ids)
    shadowed_set = set(shadowed)

    files = sorted(
        (path for path in npc_dir.rglob("*") if path.is_file()),
        key=lambda path: str(path).lower(),
    )
    templates = template_map([
        path for path in files if magic_kind(path) == "template"
    ])
    names = {
        kind: {
            name
            for name, definitions in templates.items()
            if len(definitions) == 1
            and definitions[0] == kind.encode()
        }
        for kind in (WARPMAN, FMWARPMAN, AIRPLANE, BUS)
    }

    counts = collections.Counter()
    edges: list[NonClassicFloorEdge] = []

    for create_path in (
        path for path in files if magic_kind(path) == "create"
    ):
        for entries in iter_blocks(create_path):
            fields: dict[bytes, bytes] = {}
            enemies: list[bytes] = []
            for key, value in entries:
                if key == b"enemy":
                    enemies.append(value)
                else:
                    fields[key] = value
            source_floor = _int(fields.get(b"floorid"), 0)
            if source_floor <= 0:
                continue
            if b"borncenter" not in fields and b"borncorner" not in fields:
                continue

            for value in enemies:
                template_name, separator, arg = value.partition(b"|")
                template_name = template_name.strip()
                kind = next(
                    (
                        candidate
                        for candidate in (WARPMAN, FMWARPMAN, AIRPLANE, BUS)
                        if template_name in names[candidate]
                    ),
                    None,
                )
                if kind is None:
                    continue
                counts[(kind, "refs")] += 1

                if kind == BUS:
                    continue

                data = _assigned_data(
                    npc_dir,
                    arg if separator else b"",
                )
                if data is None:
                    counts[(kind, "missing_args")] += 1
                    continue
                counts[(kind, "resolved_args")] += 1

                if kind == WARPMAN:
                    for destination_floor in _warpman_destinations(data):
                        edges.append(
                            NonClassicFloorEdge(
                                kind=WARPMAN,
                                source_floor=source_floor,
                                destination_floor=destination_floor,
                                condition_class=INTERACTIVE_DIALOGUE,
                                source_currently_reachable=(
                                    source_floor in reached
                                ),
                                destination_is_shadowed_branch=(
                                    destination_floor in shadowed_set
                                ),
                            )
                        )
                elif kind == FMWARPMAN:
                    for destination_floor in _fmwarpman_destinations(data):
                        edges.append(
                            NonClassicFloorEdge(
                                kind=FMWARPMAN,
                                source_floor=source_floor,
                                destination_floor=destination_floor,
                                condition_class=CONDITIONAL_FAMILY_SCHEDULE,
                                source_currently_reachable=(
                                    source_floor in reached
                                ),
                                destination_is_shadowed_branch=(
                                    destination_floor in shadowed_set
                                ),
                            )
                        )
                elif kind == AIRPLANE:
                    for from_floor, to_floor in _airplane_floor_transitions(
                        source_floor=source_floor,
                        data=data,
                    ):
                        edges.append(
                            NonClassicFloorEdge(
                                kind=AIRPLANE,
                                source_floor=from_floor,
                                destination_floor=to_floor,
                                condition_class=INTERACTIVE_AIR_ROUTE,
                                source_currently_reachable=(
                                    from_floor in reached
                                ),
                                destination_is_shadowed_branch=(
                                    to_floor in shadowed_set
                                ),
                            )
                        )

    return NonClassicIngressAudit(
        shadowed_branch_floor_ids=shadowed,
        classic_reachable_floor_ids=reached,
        edges=tuple(edges),
        reference_counts=counts,
    )


def emit(audit: NonClassicIngressAudit) -> None:
    print("StoneAge shadowed-branch non-classic transport ingress audit — R1")
    print(
        "SCOPE|ordered classic-Warp shadowed branch|"
        "WarpMan+FMWarpMan+Airplane floor-level ingress only"
    )
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print(
        "RULE|interactive/conditional transport edges are evidence of possible "
        "player ingress, not unconditional classic-Warp edges"
    )
    print(
        "EXCLUSION|Bus|recovered route points are x,y only and do not create "
        "cross-floor transport edges"
    )
    for key in sorted(audit.counts):
        print(f"COUNT|{key}|{audit.counts[key]}")
    print(
        "SHADOWED_BRANCH|floors="
        + ",".join(str(floor) for floor in audit.shadowed_branch_floor_ids)
    )
    for edge in sorted(
        audit.potential_ingress,
        key=lambda row: (
            row.kind,
            row.source_floor,
            row.destination_floor,
            row.condition_class,
        ),
    ):
        print(
            "POTENTIAL_INGRESS|"
            f"kind={edge.kind}|source_floor={edge.source_floor}|"
            f"destination_floor={edge.destination_floor}|"
            f"condition={edge.condition_class}"
        )
    print(OUTPUT_RESOLUTION)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--npc-dir", type=Path, required=True)
    args = parser.parse_args()
    emit(analyze(args.npc_dir))


if __name__ == "__main__":
    main()
