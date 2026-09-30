#!/usr/bin/env python3
"""Runtime dynamic-occupancy layer above recovered25 static collision routing.

Static collision provenance remains owned by the recovered25 collision router.
Dynamic destination overlap is a distinct live-session gate using the already
reconstructed stable-descendant CHAR_walk object-overability rules.

This layer deliberately does not reinterpret client hit-map cells as server
WALKABLE/HAVEHEIGHT semantics and does not infer live occupants from static map
payloads.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from tools.stoneage_map_collision_model import (
    CollisionDecision,
    DynamicOccupant,
    dynamic_overlap_allowed,
)
from tools.stoneage_recovered25_collision_router import (
    RoutedCollisionVerdict,
)
from tools.stoneage_singleplayer_domain import MapPosition


DYNAMIC_OCCUPANCY_PROFILE = "STONEAGE_DESCENDANT_LIVE_OBJECT_OVERABILITY_R1"
DYNAMIC_OCCUPANCY_EVIDENCE_CLASS = (
    "PINNED_STABLE_DESCENDANT_CHAR_WALK_LIVE_OBJECT_OVERLAP"
)


@dataclass(frozen=True)
class RuntimeCollisionWithOccupancyVerdict:
    static: RoutedCollisionVerdict
    dynamic: CollisionDecision
    decision: CollisionDecision
    dynamic_profile: str = DYNAMIC_OCCUPANCY_PROFILE
    dynamic_evidence_class: str = DYNAMIC_OCCUPANCY_EVIDENCE_CLASS

    @property
    def static_allowed(self) -> bool:
        return bool(self.static.decision.allowed)

    @property
    def dynamic_allowed(self) -> bool:
        return bool(self.dynamic.allowed)


def resolve_runtime_collision_with_occupancy(
    *,
    router,
    origin: MapPosition,
    destination: MapPosition,
    destination_occupants: Sequence[DynamicOccupant] = (),
) -> RuntimeCollisionWithOccupancyVerdict:
    """Compose one static routed verdict with one independent live-object gate.

    Ordering mirrors the recovered stable descendant movement boundary:
    static entry must succeed before target-cell live-object overability is
    relevant. Static denial is never overridden by dynamic state.
    """

    static = router.routed_step_verdict(
        origin=origin,
        destination=destination,
    )
    if not static.decision.allowed:
        dynamic = CollisionDecision(
            False,
            "dynamic_occupancy_not_evaluated_static_denied",
        )
        return RuntimeCollisionWithOccupancyVerdict(
            static=static,
            dynamic=dynamic,
            decision=static.decision,
        )

    dynamic = dynamic_overlap_allowed(tuple(destination_occupants))
    if not dynamic.allowed:
        return RuntimeCollisionWithOccupancyVerdict(
            static=static,
            dynamic=dynamic,
            decision=dynamic,
        )

    return RuntimeCollisionWithOccupancyVerdict(
        static=static,
        dynamic=dynamic,
        decision=CollisionDecision(True),
    )
