#!/usr/bin/env python3
"""Emit derived reachability for the create-order-resolved default runtime."""

from tools.stoneage_ordered_warp_runtime import (
    load_ordered_materializable_runtime,
)


def main() -> None:
    runtime = load_ordered_materializable_runtime()
    strict = runtime.strict_runtime
    reached = runtime.reachable_floor_ids
    resolved = runtime.resolved_supplemental_floor_ids
    unreachable = runtime.unreachable_resolved_supplemental_ids

    print("StoneAge create-order-resolved materializable runtime — R1")
    print(
        "SCOPE|826 materializable maps|same-file ambiguous Warp ordering "
        "resolved by descendant runtime control"
    )
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print(
        "CONTROL_ROLE|PINNED_DESCENDANT|first-created object wins same-cell "
        "overlap event; cross-file ordering is never inferred"
    )
    print(f"COUNT|materializable_floor_ids|{len(runtime.topology.maps)}")
    print(
        f"COUNT|raw_materializable_warp_records|"
        f"{strict.raw_materializable_warp_records}"
    )
    print(
        f"COUNT|strict_unambiguous_active_warps|"
        f"{len(strict.topology.legacy_warps)}"
    )
    print(
        f"COUNT|create_order_resolved_ambiguous_sources|"
        f"{len(runtime.ordered_resolutions)}"
    )
    print(
        f"COUNT|create_order_unresolved_ambiguous_sources|"
        f"{len(runtime.unresolved_ambiguous_sources)}"
    )
    print(
        f"COUNT|shadowed_ambiguous_candidates|"
        f"{sum(len(row.shadowed) for row in runtime.ordered_resolutions)}"
    )
    print(
        f"COUNT|deferred_conditional_warps|"
        f"{len(strict.deferred_conditional_warps)}"
    )
    print(
        f"COUNT|active_runtime_warps|{len(runtime.topology.legacy_warps)}"
    )
    print(f"COUNT|reachable_floor_ids|{len(reached)}")
    print(
        "COUNT|reachable_resolved_supplemental_floors|"
        f"{len(resolved & reached)}"
    )
    print(
        "COUNT|shadowed_branch_resolved_supplemental_floors|"
        f"{len(unreachable)}"
    )

    for row in runtime.ordered_resolutions:
        selected = row.selected
        print(
            "ORDERED_AMBIGUOUS_WARP|"
            f"source={row.source.floor_id},{row.source.x},{row.source.y}|"
            f"selected_placement={selected.placement_id}|"
            f"destination={selected.destination.floor_id},"
            f"{selected.destination.x},{selected.destination.y}|"
            f"shadowed_placements={','.join(str(x.placement_id) for x in row.shadowed)}"
        )
    for floor_id in unreachable:
        print(f"SHADOWED_BRANCH_FLOOR|floor={floor_id}")

    print("RESOLUTION|CREATE_ORDER_RESOLVED_RUNTIME_CLOSED")


if __name__ == "__main__":
    main()
