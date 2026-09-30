#!/usr/bin/env python3
"""Recovered25 server-backed collision provider.

This runtime layer supplies ordinary one-cell collision verdicts only for
materializable recovered25 floors whose recovered server LS2MAP payload is
unambiguous, dimension-consistent with the active runtime topology, and fully
covered by recovered mapset WALKABLE/HAVEHEIGHT metadata.

It fails closed for floors without a server map, divergent duplicate payloads,
dimension drift, or missing image metadata. It never substitutes Taiwan-v1
ADRN collision semantics.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Mapping, Sequence

from tools.stoneage_map_collision_model import (
    CollisionDecision,
    DynamicOccupant,
    ordinary_step_allowed,
)
from tools.stoneage_server_static_map import (
    RecoveredMapsetProfile,
    RecoveredServerStaticMap,
    parse_ls2map,
    parse_mapset_collision_profile,
)
from tools.stoneage_singleplayer_domain import MapPosition


SERVER_COLLISION_CLOSED = "SERVER_COLLISION_CLOSED"
NO_SERVER_MAP = "NO_SERVER_MAP"
DIVERGENT_SERVER_DUPLICATE = "DIVERGENT_SERVER_DUPLICATE"
SERVER_DIMENSION_MISMATCH = "SERVER_DIMENSION_MISMATCH"
MISSING_MAPSET_METADATA = "MISSING_MAPSET_METADATA"


@dataclass(frozen=True)
class Recovered25ServerCollisionSource:
    floor_id: int
    path: Path
    width: int
    height: int
    payload_sha256: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "floor_id", int(self.floor_id))
        object.__setattr__(self, "path", Path(self.path))
        object.__setattr__(self, "width", int(self.width))
        object.__setattr__(self, "height", int(self.height))
        digest = str(self.payload_sha256).lower()
        if len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
            raise ValueError("server collision source SHA-256 is invalid")
        object.__setattr__(self, "payload_sha256", digest)


@dataclass(frozen=True)
class Recovered25ServerCollisionFloor:
    floor_id: int
    status: str
    sources: tuple[Recovered25ServerCollisionSource, ...]
    selected_source: Recovered25ServerCollisionSource | None = None

    @property
    def supported(self) -> bool:
        return self.status == SERVER_COLLISION_CLOSED


class Recovered25ServerCollisionProvider:
    """Lazy collision provider over verified recovered server-map payloads."""

    def __init__(
        self,
        *,
        profile,
        adapter,
        server_map_root: Path,
        mapset_path: Path,
    ) -> None:
        self.profile = profile
        self.adapter = adapter
        self.server_map_root = Path(server_map_root)
        self.mapset_path = Path(mapset_path)
        if adapter.profile.contract_id != profile.contract_id:
            raise ValueError("collision provider adapter/profile contract drift")
        if not self.server_map_root.is_dir():
            raise ValueError("recovered server map root does not exist")
        if not self.mapset_path.is_file():
            raise ValueError("recovered mapset file does not exist")

        self.mapset = parse_mapset_collision_profile(self.mapset_path.read_bytes())
        sources, invalid_files = self._scan_sources()
        self.invalid_server_files = invalid_files
        floors = {}
        for floor_id, definition in sorted(adapter.topology.maps.items()):
            floors[int(floor_id)] = self._classify(
                int(floor_id),
                int(definition.width),
                int(definition.height),
                tuple(sources.get(int(floor_id), ())),
            )
        self.floors: Mapping[int, Recovered25ServerCollisionFloor] = (
            MappingProxyType(floors)
        )
        self._cache: dict[int, tuple[RecoveredServerStaticMap, object, object]] = {}

    def _scan_sources(
        self,
    ) -> tuple[dict[int, list[Recovered25ServerCollisionSource]], int]:
        by_floor: dict[int, list[Recovered25ServerCollisionSource]] = {}
        invalid = 0
        for path in sorted(
            self.server_map_root.rglob("*"),
            key=lambda p: str(p).lower(),
        ):
            if not path.is_file() or path.resolve() == self.mapset_path.resolve():
                continue
            try:
                raw = path.read_bytes()
                parsed = parse_ls2map(raw)
            except (OSError, ValueError):
                invalid += 1
                continue
            source = Recovered25ServerCollisionSource(
                floor_id=parsed.floor_id,
                path=path,
                width=parsed.width,
                height=parsed.height,
                payload_sha256=parsed.payload_sha256,
            )
            by_floor.setdefault(parsed.floor_id, []).append(source)
        return by_floor, invalid

    def _classify(
        self,
        floor_id: int,
        expected_width: int,
        expected_height: int,
        sources: tuple[Recovered25ServerCollisionSource, ...],
    ) -> Recovered25ServerCollisionFloor:
        if not sources:
            return Recovered25ServerCollisionFloor(
                floor_id=floor_id,
                status=NO_SERVER_MAP,
                sources=(),
            )

        by_digest: dict[str, list[Recovered25ServerCollisionSource]] = {}
        for source in sources:
            by_digest.setdefault(source.payload_sha256, []).append(source)
        if len(by_digest) > 1:
            return Recovered25ServerCollisionFloor(
                floor_id=floor_id,
                status=DIVERGENT_SERVER_DUPLICATE,
                sources=sources,
            )

        # Multiple files with the same SHA are payload-equivalent, so selecting
        # a deterministic path cannot alter runtime map bytes.
        selected = sorted(sources, key=lambda x: str(x.path).lower())[0]
        if (selected.width, selected.height) != (
            int(expected_width),
            int(expected_height),
        ):
            return Recovered25ServerCollisionFloor(
                floor_id=floor_id,
                status=SERVER_DIMENSION_MISMATCH,
                sources=sources,
            )

        parsed = self._read_verified_source(selected)
        missing = parsed.used_image_ids - set(self.mapset.images)
        if missing:
            return Recovered25ServerCollisionFloor(
                floor_id=floor_id,
                status=MISSING_MAPSET_METADATA,
                sources=sources,
            )

        return Recovered25ServerCollisionFloor(
            floor_id=floor_id,
            status=SERVER_COLLISION_CLOSED,
            sources=sources,
            selected_source=selected,
        )

    def _read_verified_source(
        self,
        source: Recovered25ServerCollisionSource,
    ) -> RecoveredServerStaticMap:
        raw = source.path.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        if digest != source.payload_sha256:
            raise ValueError(
                f"recovered server collision payload SHA drift for floor "
                f"{source.floor_id}"
            )
        parsed = parse_ls2map(raw)
        if parsed.floor_id != source.floor_id:
            raise ValueError("recovered server collision embedded floor-id drift")
        if (parsed.width, parsed.height) != (source.width, source.height):
            raise ValueError("recovered server collision dimension drift")
        return parsed

    @property
    def supported_floor_ids(self) -> frozenset[int]:
        return frozenset(
            floor_id
            for floor_id, row in self.floors.items()
            if row.supported
        )

    @property
    def unsupported_floor_ids(self) -> frozenset[int]:
        return frozenset(self.floors) - self.supported_floor_ids

    def coverage_counts(self) -> Mapping[str, int]:
        counts: dict[str, int] = {
            "materializable_floors": len(self.floors),
            "server_collision_closed": 0,
            "server_collision_uncovered": 0,
            NO_SERVER_MAP: 0,
            DIVERGENT_SERVER_DUPLICATE: 0,
            SERVER_DIMENSION_MISMATCH: 0,
            MISSING_MAPSET_METADATA: 0,
        }
        for row in self.floors.values():
            if row.supported:
                counts["server_collision_closed"] += 1
            else:
                counts["server_collision_uncovered"] += 1
                counts[row.status] = counts.get(row.status, 0) + 1
        return MappingProxyType(counts)

    def floor_status(self, floor_id: int) -> str:
        floor_id = int(floor_id)
        if floor_id not in self.floors:
            raise KeyError(f"floor {floor_id} is outside materializable topology")
        return self.floors[floor_id].status

    def _runtime_collision_objects(self, floor_id: int):
        floor_id = int(floor_id)
        if floor_id in self._cache:
            return self._cache[floor_id]
        if floor_id not in self.floors:
            raise KeyError(f"floor {floor_id} is outside materializable topology")
        row = self.floors[floor_id]
        if not row.supported or row.selected_source is None:
            raise ValueError(
                f"recovered25 server collision unavailable for floor "
                f"{floor_id}: {row.status}"
            )
        parsed = self._read_verified_source(row.selected_source)
        definition = self.adapter.topology.maps[floor_id]
        if (parsed.width, parsed.height) != (
            int(definition.width),
            int(definition.height),
        ):
            raise ValueError("runtime collision topology dimension drift")
        collision_map = parsed.collision_map()
        collision_profile = self.mapset.collision_profile_for(parsed)
        value = (parsed, collision_map, collision_profile)
        self._cache[floor_id] = value
        return value

    def ordinary_step_verdict(
        self,
        *,
        origin: MapPosition,
        destination: MapPosition,
        destination_occupants: Sequence[DynamicOccupant] = (),
        is_flying: bool = False,
    ) -> CollisionDecision:
        if int(origin.floor_id) != int(destination.floor_id):
            return CollisionDecision(False, "floor_change_not_an_ordinary_step")
        _, collision_map, collision_profile = self._runtime_collision_objects(
            int(origin.floor_id)
        )
        return ordinary_step_allowed(
            collision_map,
            collision_profile,
            origin=origin,
            destination=destination,
            destination_occupants=destination_occupants,
            is_flying=bool(is_flying),
        )
