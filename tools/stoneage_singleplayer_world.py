#!/usr/bin/env python3
"""Historical map/warp topology boundary for the in-process StoneAge rebuild.

Map dimensions and classic overlap-warp semantics are evidence-backed. Exact
terrain/object collision semantics are not promoted here: the caller must pass
an explicit entry_allowed verdict from whatever validated collision layer is
available for the selected historical dataset.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from tools.stoneage_singleplayer_domain import (
    MapPosition,
    SinglePlayerHistoricalDomain,
)
from tools.stoneage_warp_transition_model import (
    PARTY_NONE,
    apply_warp,
    legacy_warp_init,
    overlap_warp_triggered,
    parse_legacy_warp_arg,
)


EARLY_MEMBERSHIP_PROVEN = "EARLY_MEMBERSHIP_PROVEN"
LATER_RECOVERED = "LATER_RECOVERED"
DESIGN_RECONSTRUCTED = "DESIGN_RECONSTRUCTED"

V1_RESOURCE_COMPATIBLE = "V1_RESOURCE_COMPATIBLE"
LATER_ONLY_RESOURCE_DEPENDENCY = "LATER_ONLY_RESOURCE_DEPENDENCY"
RESOURCE_RELATION_UNKNOWN = "RESOURCE_RELATION_UNKNOWN"

STABLE_LATER_MAP_CANDIDATE = "STABLE_LATER_MAP_CANDIDATE"

_CONTENT_ROLES = frozenset({
    EARLY_MEMBERSHIP_PROVEN,
    LATER_RECOVERED,
    DESIGN_RECONSTRUCTED,
})
_RESOURCE_ROLES = frozenset({
    V1_RESOURCE_COMPATIBLE,
    LATER_ONLY_RESOURCE_DEPENDENCY,
    RESOURCE_RELATION_UNKNOWN,
})
_QUALIFIERS = frozenset({STABLE_LATER_MAP_CANDIDATE})


@dataclass(frozen=True)
class WorldMapProvenance:
    """Structured concrete-map provenance for the modern reconstruction.

    The v1-direct map/cache *format* is a separate runtime fact. This object
    classifies concrete world content and prevents compatibility or later
    persistence from being silently promoted into Taiwan-v1 membership.
    """

    content_role: str
    resource_role: str = RESOURCE_RELATION_UNKNOWN
    source_versions: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    payload_sha256: str | None = None
    qualifiers: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        content_role = str(self.content_role)
        resource_role = str(self.resource_role)
        if content_role not in _CONTENT_ROLES:
            raise ValueError(f"unknown world-map content role: {content_role}")
        if resource_role not in _RESOURCE_ROLES:
            raise ValueError(f"unknown world-map resource role: {resource_role}")

        source_versions = tuple(str(v).strip() for v in self.source_versions)
        evidence_refs = tuple(str(v).strip() for v in self.evidence_refs)
        qualifiers = tuple(str(v).strip() for v in self.qualifiers)
        if any(not value for value in source_versions):
            raise ValueError("world-map source versions cannot contain blanks")
        if any(not value for value in evidence_refs):
            raise ValueError("world-map evidence refs cannot contain blanks")
        if any(not value for value in qualifiers):
            raise ValueError("world-map qualifiers cannot contain blanks")
        if len(source_versions) != len(set(source_versions)):
            raise ValueError("world-map source versions cannot contain duplicates")
        if len(evidence_refs) != len(set(evidence_refs)):
            raise ValueError("world-map evidence refs cannot contain duplicates")
        if len(qualifiers) != len(set(qualifiers)):
            raise ValueError("world-map qualifiers cannot contain duplicates")
        unknown_qualifiers = sorted(set(qualifiers) - _QUALIFIERS)
        if unknown_qualifiers:
            raise ValueError(
                f"unknown world-map provenance qualifiers: {unknown_qualifiers}"
            )

        payload_sha256 = self.payload_sha256
        if payload_sha256 is not None:
            payload_sha256 = str(payload_sha256).lower()
            if (
                len(payload_sha256) != 64
                or any(ch not in "0123456789abcdef" for ch in payload_sha256)
            ):
                raise ValueError("world-map payload_sha256 must be 64 hex digits")

        if content_role in {EARLY_MEMBERSHIP_PROVEN, LATER_RECOVERED}:
            if not source_versions:
                raise ValueError(
                    f"{content_role} world maps require source_versions"
                )
            if not evidence_refs:
                raise ValueError(
                    f"{content_role} world maps require evidence_refs"
                )
            if payload_sha256 is None:
                raise ValueError(
                    f"{content_role} concrete world maps require payload_sha256"
                )

        stable = STABLE_LATER_MAP_CANDIDATE in qualifiers
        if stable:
            if content_role != LATER_RECOVERED:
                raise ValueError(
                    "stable later candidate must remain LATER_RECOVERED"
                )
            if resource_role != V1_RESOURCE_COMPATIBLE:
                raise ValueError(
                    "stable later candidate must be V1_RESOURCE_COMPATIBLE"
                )
            if len(source_versions) < 2:
                raise ValueError(
                    "stable later candidate requires at least two source versions"
                )

        object.__setattr__(self, "content_role", content_role)
        object.__setattr__(self, "resource_role", resource_role)
        object.__setattr__(self, "source_versions", source_versions)
        object.__setattr__(self, "evidence_refs", evidence_refs)
        object.__setattr__(self, "payload_sha256", payload_sha256)
        object.__setattr__(self, "qualifiers", qualifiers)

    @property
    def claims_early_membership(self) -> bool:
        return self.content_role == EARLY_MEMBERSHIP_PROVEN


@dataclass(frozen=True)
class HistoricalMapDefinition:
    floor_id: int
    width: int
    height: int
    evidence: str = "RECOVERED_MAP_DIMENSIONS"
    provenance: WorldMapProvenance | None = None

    def __post_init__(self) -> None:
        floor_id = int(self.floor_id)
        width = int(self.width)
        height = int(self.height)
        if width <= 0 or height <= 0:
            raise ValueError("map width and height must be positive")
        provenance = self.provenance
        if provenance is not None and not isinstance(
            provenance, WorldMapProvenance
        ):
            raise TypeError("map provenance must be WorldMapProvenance or None")
        object.__setattr__(self, "floor_id", floor_id)
        object.__setattr__(self, "width", width)
        object.__setattr__(self, "height", height)

    def contains(self, position: MapPosition) -> bool:
        return (
            int(position.floor_id) == self.floor_id
            and 0 <= int(position.x) < self.width
            and 0 <= int(position.y) < self.height
        )


@dataclass(frozen=True)
class LegacyWarpEdge:
    """Classic invisible overlap Warp NPC edge.

    The optional historical time token is retained as evidence but deliberately
    not interpreted. R1 only activates edges explicitly marked active.
    """

    source: MapPosition
    destination: MapPosition
    time_token: str | None = None
    active: bool = True

    @classmethod
    def from_legacy_arg(
        cls,
        *,
        source: MapPosition,
        arg: str,
        active: bool = True,
    ) -> "LegacyWarpEdge":
        parsed = parse_legacy_warp_arg(arg)
        if parsed is None:
            raise ValueError("invalid classic Warp NPC argument")
        floor, x, y = parsed["destination"]
        return cls(
            source=source,
            destination=MapPosition(int(floor), int(x), int(y)),
            time_token=parsed["time_token"],
            active=bool(active),
        )


@dataclass(frozen=True)
class HistoricalWorldTopology:
    maps: Mapping[int, HistoricalMapDefinition]
    legacy_warps: tuple[LegacyWarpEdge, ...] = ()
    require_structured_provenance: bool = False

    @classmethod
    def from_provenance_maps(
        cls,
        maps: Mapping[int, HistoricalMapDefinition],
        *,
        legacy_warps: tuple[LegacyWarpEdge, ...] = (),
    ) -> "HistoricalWorldTopology":
        """Strict modern-world entry point requiring structured provenance."""
        return cls(
            maps=maps,
            legacy_warps=legacy_warps,
            require_structured_provenance=True,
        )

    def __post_init__(self) -> None:
        normalized = {int(key): value for key, value in self.maps.items()}
        for key, definition in normalized.items():
            if key != definition.floor_id:
                raise ValueError(
                    f"map key {key} does not match floor {definition.floor_id}"
                )
            if (
                bool(self.require_structured_provenance)
                and definition.provenance is None
            ):
                raise ValueError(
                    f"map {key} lacks structured world-map provenance"
                )
        object.__setattr__(self, "maps", MappingProxyType(normalized))
        object.__setattr__(
            self,
            "require_structured_provenance",
            bool(self.require_structured_provenance),
        )
        object.__setattr__(self, "legacy_warps", tuple(self.legacy_warps))

        seen_active_sources: set[MapPosition] = set()
        for edge in self.legacy_warps:
            if not self.is_valid_position(edge.source):
                raise ValueError(f"warp source outside recovered map bounds: {edge.source}")
            if not self.is_valid_position(edge.destination):
                raise ValueError(
                    f"warp destination outside recovered map bounds: {edge.destination}"
                )
            if edge.active:
                if edge.source in seen_active_sources:
                    raise ValueError(
                        "multiple active classic warp edges share one source cell; "
                        "time/condition semantics must be resolved explicitly first"
                    )
                seen_active_sources.add(edge.source)

    def is_valid_position(self, position: MapPosition) -> bool:
        definition = self.maps.get(int(position.floor_id))
        return definition is not None and definition.contains(position)

    def active_warp_at(self, position: MapPosition) -> LegacyWarpEdge | None:
        for edge in self.legacy_warps:
            if edge.active and edge.source == position:
                return edge
        return None

    def provenance_for_floor(self, floor_id: int) -> WorldMapProvenance | None:
        definition = self.maps.get(int(floor_id))
        if definition is None:
            return None
        return definition.provenance


@dataclass(frozen=True)
class WalkResolution:
    previous_position: MapPosition
    entered_position: MapPosition
    final_position: MapPosition
    moved: bool
    blocked_reason: str | None
    warp_triggered: bool
    encounter_suppressed: bool
    map_objmove_ok: bool | None = None


def place_player_on_topology(
    domain: SinglePlayerHistoricalDomain,
    topology: HistoricalWorldTopology,
    position: MapPosition,
) -> MapPosition:
    if not topology.is_valid_position(position):
        raise ValueError(f"position outside recovered map bounds: {position}")
    return domain.move_player(
        floor_id=position.floor_id,
        x=position.x,
        y=position.y,
    )


def resolve_player_walk(
    domain: SinglePlayerHistoricalDomain,
    topology: HistoricalWorldTopology,
    *,
    destination: MapPosition,
    entry_allowed: bool,
    action_is_walk: bool = True,
    map_objmove_ok: bool = True,
) -> WalkResolution:
    """Resolve one already-shaped historical walk attempt.

    entry_allowed is deliberately external. It represents the result of the
    selected historical collision/object-overability resolver. This boundary
    does not guess collision meaning from recovered MAP/DAT values.

    Ordinary walking cannot change floors directly. A classic Warp edge may
    change floor only after the source cell has been entered.
    """
    current = domain.world.player_position
    if current is None:
        raise ValueError("player position is required before walking")
    if not topology.is_valid_position(current):
        raise ValueError("current player position is outside loaded topology")

    if int(destination.floor_id) != int(current.floor_id):
        return WalkResolution(
            previous_position=current,
            entered_position=current,
            final_position=current,
            moved=False,
            blocked_reason="walk_floor_change_requires_warp",
            warp_triggered=False,
            encounter_suppressed=False,
        )
    if not topology.is_valid_position(destination):
        return WalkResolution(
            previous_position=current,
            entered_position=current,
            final_position=current,
            moved=False,
            blocked_reason="destination_out_of_bounds",
            warp_triggered=False,
            encounter_suppressed=False,
        )
    if not bool(entry_allowed):
        return WalkResolution(
            previous_position=current,
            entered_position=current,
            final_position=current,
            moved=False,
            blocked_reason="entry_rejected_by_collision_layer",
            warp_triggered=False,
            encounter_suppressed=False,
        )

    entered = domain.move_player(
        floor_id=destination.floor_id,
        x=destination.x,
        y=destination.y,
    )

    edge = topology.active_warp_at(entered)
    if edge is None:
        return WalkResolution(
            previous_position=current,
            entered_position=entered,
            final_position=entered,
            moved=True,
            blocked_reason=None,
            warp_triggered=False,
            encounter_suppressed=False,
        )

    triggered = overlap_warp_triggered(
        mover_is_player=True,
        action_is_walk=bool(action_is_walk),
        previous_xy=(current.x, current.y),
        event_xy=(entered.x, entered.y),
    )
    if not triggered:
        return WalkResolution(
            previous_position=current,
            entered_position=entered,
            final_position=entered,
            moved=True,
            blocked_reason=None,
            warp_triggered=False,
            encounter_suppressed=False,
        )

    destination_valid = topology.is_valid_position(edge.destination)
    initialized = legacy_warp_init(
        (
            f"{edge.destination.floor_id}|{edge.destination.x}|"
            f"{edge.destination.y}"
        ),
        destination_valid=destination_valid,
    )
    if not initialized["ok"]:
        raise ValueError("active classic warp edge failed destination validation")

    warped = apply_warp(
        current_position=(entered.floor_id, entered.x, entered.y),
        destination=(
            edge.destination.floor_id,
            edge.destination.x,
            edge.destination.y,
        ),
        destination_valid=destination_valid,
        party_mode=PARTY_NONE,
        character_type="player",
        map_objmove_ok=bool(map_objmove_ok),
    )
    if not warped["ok"]:
        raise ValueError("validated classic warp failed unexpectedly")

    final = MapPosition(*warped["position"])
    domain.move_player(
        floor_id=final.floor_id,
        x=final.x,
        y=final.y,
    )
    return WalkResolution(
        previous_position=current,
        entered_position=entered,
        final_position=final,
        moved=True,
        blocked_reason=None,
        warp_triggered=True,
        encounter_suppressed=True,
        map_objmove_ok=bool(warped["map_objmove_ok"]),
    )
