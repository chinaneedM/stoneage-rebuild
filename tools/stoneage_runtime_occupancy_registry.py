#!/usr/bin/env python3
"""Live runtime occupancy registry for engine-neutral local movement.

Static map collision and live object overlap remain separate evidence surfaces.
This registry owns only transient live-session object positions and explicit
overability state. It deliberately does not infer CHAR_ISOVERED or
ITEM_ISOVERED from presentation/template fields such as NpcRuntimeState.walkable.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from tools.stoneage_map_collision_model import (
    CHARACTER,
    GOLD,
    ITEM,
    OTHER,
    DynamicOccupant,
)
from tools.stoneage_singleplayer_domain import MapPosition


LIVE_OCCUPANCY_STATE_PROFILE = "STONEAGE_LOCAL_LIVE_OCCUPANCY_STATE_R1"


@dataclass(frozen=True)
class LiveRuntimeObject:
    object_id: str
    kind: str
    position: MapPosition
    overable: bool
    provenance: str

    def __post_init__(self) -> None:
        object_id = str(self.object_id).strip()
        provenance = str(self.provenance).strip()
        kind = str(self.kind)
        if not object_id:
            raise ValueError("live occupancy object_id must be non-empty")
        if kind not in {CHARACTER, ITEM, GOLD, OTHER}:
            raise ValueError(f"unsupported live occupancy kind: {kind}")
        if not isinstance(self.position, MapPosition):
            raise TypeError("live occupancy position must be MapPosition")
        if not provenance:
            raise ValueError("live occupancy provenance must be non-empty")
        object.__setattr__(self, "object_id", object_id)
        object.__setattr__(self, "kind", kind)
        object.__setattr__(self, "overable", bool(self.overable))
        object.__setattr__(self, "provenance", provenance)

    def as_dynamic_occupant(self) -> DynamicOccupant:
        return DynamicOccupant(kind=self.kind, overable=self.overable)


@dataclass(frozen=True)
class RuntimeOccupancyQuery:
    position: MapPosition
    objects: tuple[LiveRuntimeObject, ...]

    @property
    def occupants(self) -> tuple[DynamicOccupant, ...]:
        return tuple(obj.as_dynamic_occupant() for obj in self.objects)

    @property
    def object_ids(self) -> tuple[str, ...]:
        return tuple(obj.object_id for obj in self.objects)

    @property
    def provenances(self) -> tuple[str, ...]:
        return tuple(obj.provenance for obj in self.objects)


class RuntimeDynamicOccupancyRegistry:
    """Mutable live-session registry with deterministic destination queries."""

    profile_id = LIVE_OCCUPANCY_STATE_PROFILE

    def __init__(self) -> None:
        self._objects: dict[str, LiveRuntimeObject] = {}

    @property
    def objects(self) -> Mapping[str, LiveRuntimeObject]:
        return MappingProxyType(dict(self._objects))

    def upsert(self, obj: LiveRuntimeObject) -> None:
        if not isinstance(obj, LiveRuntimeObject):
            raise TypeError("occupancy registry accepts LiveRuntimeObject values")
        self._objects[obj.object_id] = obj

    def remove(self, object_id: str) -> LiveRuntimeObject | None:
        return self._objects.pop(str(object_id), None)

    def move(self, object_id: str, position: MapPosition) -> LiveRuntimeObject:
        key = str(object_id)
        if key not in self._objects:
            raise KeyError(f"live occupancy object not found: {key}")
        current = self._objects[key]
        updated = LiveRuntimeObject(
            object_id=current.object_id,
            kind=current.kind,
            position=position,
            overable=current.overable,
            provenance=current.provenance,
        )
        self._objects[key] = updated
        return updated

    def set_overable(self, object_id: str, overable: bool) -> LiveRuntimeObject:
        key = str(object_id)
        if key not in self._objects:
            raise KeyError(f"live occupancy object not found: {key}")
        current = self._objects[key]
        updated = LiveRuntimeObject(
            object_id=current.object_id,
            kind=current.kind,
            position=current.position,
            overable=bool(overable),
            provenance=current.provenance,
        )
        self._objects[key] = updated
        return updated

    def query(self, position: MapPosition) -> RuntimeOccupancyQuery:
        if not isinstance(position, MapPosition):
            raise TypeError("occupancy query position must be MapPosition")
        rows = tuple(
            sorted(
                (
                    obj for obj in self._objects.values()
                    if obj.position == position
                ),
                key=lambda obj: obj.object_id,
            )
        )
        return RuntimeOccupancyQuery(position=position, objects=rows)

    def register_character(
        self,
        *,
        object_id: str,
        position: MapPosition,
        overable: bool,
        provenance: str,
    ) -> LiveRuntimeObject:
        obj = LiveRuntimeObject(
            object_id=object_id,
            kind=CHARACTER,
            position=position,
            overable=overable,
            provenance=provenance,
        )
        self.upsert(obj)
        return obj

    def register_item(
        self,
        *,
        object_id: str,
        position: MapPosition,
        overable: bool,
        provenance: str,
    ) -> LiveRuntimeObject:
        obj = LiveRuntimeObject(
            object_id=object_id,
            kind=ITEM,
            position=position,
            overable=overable,
            provenance=provenance,
        )
        self.upsert(obj)
        return obj

    def register_gold(
        self,
        *,
        object_id: str,
        position: MapPosition,
        provenance: str,
    ) -> LiveRuntimeObject:
        obj = LiveRuntimeObject(
            object_id=object_id,
            kind=GOLD,
            position=position,
            overable=True,
            provenance=provenance,
        )
        self.upsert(obj)
        return obj

    def register_npc_runtime_state(
        self,
        state,
        *,
        overable: bool,
        provenance: str,
    ) -> LiveRuntimeObject:
        """Register an NPC bridge state without guessing overability.

        The caller must supply overable from the behavior/runtime layer.
        NpcRuntimeState.walkable is intentionally ignored because no evidence
        chain currently establishes it as an alias of server CHAR_ISOVERED.
        """
        required = ("runtime_object_id", "floor_id", "x", "y")
        if any(not hasattr(state, name) for name in required):
            raise TypeError("state does not expose required NPC runtime fields")
        return self.register_character(
            object_id=f"char:{int(state.runtime_object_id)}",
            position=MapPosition(
                int(state.floor_id),
                int(state.x),
                int(state.y),
            ),
            overable=bool(overable),
            provenance=provenance,
        )
