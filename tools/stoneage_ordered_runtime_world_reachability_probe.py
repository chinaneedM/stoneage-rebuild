#!/usr/bin/env python3
"""Audit reachability of the ordered executable recovered25 runtime world.

This layer uses only active Warp edges after:
- exact duplicate collapse;
- same-file create-order arbitration for all recoverable ambiguous sources;
- conditional-time Warp deferral;
- floor-130 and other non-materializable edge quarantine.

Shadowed candidates are retained as evidence and inspected as possible blocked
ingress into otherwise materializable-but-unreachable supplemental components.
"""

from __future__ import annotations

import argparse
import collections
from dataclasses import dataclass
from pathlib import Path

from tools.stoneage_ordered_runtime_world_topology import (
    CREATE_ORDER_REPORT_REF,
    OrderedMaterializableRuntimeTopology,
    apply_create_order_arbitration,
)
from tools.stoneage_materializable_world_topology import (
    GEOMETRY_REPORT_REF,
    build_materializable_runtime_topology,
)
from tools.stoneage_supplemental_world_manifest import (
    SUPPLEMENTAL_AUDIT_REPORT_REF,
    parse_supplemental_world_audit,
)
from tools.stoneage_versioned_world_manifest import (
    COVERAGE_REPORT_REF,
    build_versioned_world_manifest,
)
from tools.stoneage_world_map_library import (
    LINEAGE_REPORT_REF,
    parse_stable_later_map_manifest,
)


OUTPUT_RESOLUTION = "RESOLUTION|ORDERED_RUNTIME_WORLD_REACHABILITY_CLOSED"


@dataclass(frozen=True)
class OrphanResolvedFloor:
    floor_id: int
    active_incoming: int
    active_outgoing: int


@dataclass(frozen=True)
class ShadowedIngress:
    source_floor: int
    source_x: int
    source_y: int
    selected_placement: int
    selected_destination_floor: int
    shadowed_placement: int
    shadowed_destination_floor: int
    shadowed_destination_x: int
    shadowed_destination_y: int


@dataclass(frozen=True)
class OrderedRuntimeReachabilityAudit:
    runtime: OrderedMaterializableRuntimeTopology
    reached_floor_ids: frozenset[int]
    resolved_reached_ids: frozenset[int]
    orphan_rows: tuple[OrphanResolvedFloor, ...]
    max_resolved_depth: int
    shadowed_ingress: tuple[ShadowedIngress, ...]

    @property
    def counts(self) -> dict[str, int]:
        extension = self.runtime.base.extension
        return {
            "stable_seed_floors": len(extension.stable_world.by_floor),
            "resolved_supplemental_floor_ids": len(extension.resolved_by_floor),
            "unresolved_supplemental_floor_ids": len(
                extension.unresolved_by_floor
            ),
            "materializable_floor_ids": len(
                extension.materializable_floor_ids
            ),
            "active_runtime_warps": len(self.runtime.topology.legacy_warps),
            "ordered_source_resolutions": len(
                self.runtime.ordered_resolutions
            ),
            "shadowed_candidate_records": (
                self.runtime.shadowed_candidate_records
            ),
            "unresolved_cross_file_sources": len(
                self.runtime.unresolved_cross_file_sources
            ),
            "deferred_conditional_warps": len(
                self.runtime.base.deferred_conditional_warps
            ),
            "reachable_floor_ids": len(self.reached_floor_ids),
            "reachable_resolved_supplemental_floors": len(
                self.resolved_reached_ids
            ),
            "orphan_resolved_supplemental_floors": len(self.orphan_rows),
            "max_reachable_resolved_supplemental_depth": int(
                self.max_resolved_depth
            ),
            "shadowed_ingress_candidates": len(self.shadowed_ingress),
        }


def compute_ordered_runtime_reachability(
    runtime: OrderedMaterializableRuntimeTopology,
) -> OrderedRuntimeReachabilityAudit:
    extension = runtime.base.extension
    stable = set(extension.stable_world.by_floor)
    resolved = set(extension.resolved_by_floor)
    materializable = set(extension.materializable_floor_ids)

    outgoing: dict[int, list[int]] = collections.defaultdict(list)
    incoming_count = collections.Counter()
    outgoing_count = collections.Counter()
    for edge in runtime.topology.legacy_warps:
        sf = edge.source.floor_id
        df = edge.destination.floor_id
        if sf not in materializable or df not in materializable:
            raise ValueError("active ordered Warp escaped materializable map set")
        outgoing[sf].append(df)
        outgoing_count[sf] += 1
        incoming_count[df] += 1

    depth = {floor_id: 0 for floor_id in stable}
    queue = list(sorted(stable))
    for floor_id in queue:
        for destination in outgoing.get(floor_id, ()):
            if destination in depth:
                continue
            depth[destination] = depth[floor_id] + 1
            queue.append(destination)

    reached = frozenset(depth)
    reached_resolved = frozenset(resolved & set(reached))
    orphan_ids = tuple(sorted(resolved - set(reached)))
    orphan_rows = tuple(
        OrphanResolvedFloor(
            floor_id=floor_id,
            active_incoming=int(incoming_count[floor_id]),
            active_outgoing=int(outgoing_count[floor_id]),
        )
        for floor_id in orphan_ids
    )
    max_depth = max(
        (depth[floor_id] for floor_id in reached_resolved),
        default=0,
    )

    shadowed_ingress = []
    orphan_set = set(orphan_ids)
    for resolution in runtime.ordered_resolutions:
        source_reachable = resolution.source.floor_id in reached
        if not source_reachable:
            continue
        for row in resolution.shadowed:
            if row.destination.floor_id not in orphan_set:
                continue
            shadowed_ingress.append(
                ShadowedIngress(
                    source_floor=resolution.source.floor_id,
                    source_x=resolution.source.x,
                    source_y=resolution.source.y,
                    selected_placement=resolution.selected.placement_id,
                    selected_destination_floor=(
                        resolution.selected.destination.floor_id
                    ),
                    shadowed_placement=row.placement_id,
                    shadowed_destination_floor=row.destination.floor_id,
                    shadowed_destination_x=row.destination.x,
                    shadowed_destination_y=row.destination.y,
                )
            )

    return OrderedRuntimeReachabilityAudit(
        runtime=runtime,
        reached_floor_ids=reached,
        resolved_reached_ids=reached_resolved,
        orphan_rows=orphan_rows,
        max_resolved_depth=max_depth,
        shadowed_ingress=tuple(shadowed_ingress),
    )


def load_ordered_runtime_reachability(
) -> OrderedRuntimeReachabilityAudit:
    stable_maps = parse_stable_later_map_manifest(
        Path(LINEAGE_REPORT_REF).read_text(encoding="utf-8")
    )
    stable_world = build_versioned_world_manifest(
        maps=stable_maps,
        coverage_text=Path(COVERAGE_REPORT_REF).read_text(encoding="utf-8"),
    )
    extension = parse_supplemental_world_audit(
        stable_world=stable_world,
        text=Path(SUPPLEMENTAL_AUDIT_REPORT_REF).read_text(
            encoding="utf-8"
        ),
    )
    base = build_materializable_runtime_topology(
        extension=extension,
        geometry_text=Path(GEOMETRY_REPORT_REF).read_text(encoding="utf-8"),
    )
    ordered = apply_create_order_arbitration(
        runtime=base,
        create_order_text=Path(CREATE_ORDER_REPORT_REF).read_text(
            encoding="utf-8"
        ),
    )
    return compute_ordered_runtime_reachability(ordered)


def emit(audit: OrderedRuntimeReachabilityAudit) -> None:
    print("StoneAge ordered executable runtime world reachability — R1")
    print(
        "SCOPE|761 stable seeds -> ordered active classic Warp BFS|"
        "same-file first-match applied; shadowed and conditional evidence inactive"
    )
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print(
        "RULE|shadowed Warp candidates are preserved as evidence and cannot become "
        "active unless the ordering model is superseded"
    )
    for key in sorted(audit.counts):
        print(f"COUNT|{key}|{audit.counts[key]}")

    for row in audit.orphan_rows:
        print(
            "ORPHAN_RESOLVED_SUPPLEMENTAL|"
            f"floor={row.floor_id}|"
            f"active_incoming={row.active_incoming}|"
            f"active_outgoing={row.active_outgoing}"
        )

    for row in audit.shadowed_ingress:
        print(
            "SHADOWED_INGRESS|"
            f"source={row.source_floor},{row.source_x},{row.source_y}|"
            f"selected_placement={row.selected_placement}|"
            f"selected_destination_floor={row.selected_destination_floor}|"
            f"shadowed_placement={row.shadowed_placement}|"
            f"shadowed_destination="
            f"{row.shadowed_destination_floor},"
            f"{row.shadowed_destination_x},"
            f"{row.shadowed_destination_y}"
        )

    print(OUTPUT_RESOLUTION)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.parse_args()
    emit(load_ordered_runtime_reachability())


if __name__ == "__main__":
    main()
