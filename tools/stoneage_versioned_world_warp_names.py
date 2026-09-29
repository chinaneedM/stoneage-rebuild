#!/usr/bin/env python3
"""Recovered-name diagnostics for versioned classic warp geometry.

This is a read-only diagnostic join. It never changes warp behavior, never
cleans recovered text into UI labels, and never promotes recovered-2.5 naming
evidence into Taiwan-v1 history.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from tools.stoneage_versioned_world_geometry import (
    VersionedClassicWarpGeometry,
    VersionedWorldGeometryManifest,
)
from tools.stoneage_versioned_world_names import (
    VersionedWorldNameOverlay,
)


RESOLVED = "RESOLVED"
UNRESOLVED = "UNRESOLVED"
ABSENT = "ABSENT"
OUTSIDE_STABLE_WORLD = "OUTSIDE_STABLE_WORLD"


@dataclass(frozen=True)
class VersionedClassicWarpNameDiagnostic:
    warp: VersionedClassicWarpGeometry
    source_name_state: str
    destination_name_state: str
    source_recovered_text: str | None
    destination_recovered_text: str | None

    def __post_init__(self) -> None:
        allowed_source = {RESOLVED, UNRESOLVED, ABSENT}
        allowed_destination = allowed_source | {OUTSIDE_STABLE_WORLD}
        if self.source_name_state not in allowed_source:
            raise ValueError("invalid source name state")
        if self.destination_name_state not in allowed_destination:
            raise ValueError("invalid destination name state")
        if (
            self.source_name_state == RESOLVED
            and self.source_recovered_text is None
        ):
            raise ValueError("resolved source name requires recovered text")
        if (
            self.source_name_state != RESOLVED
            and self.source_recovered_text is not None
        ):
            raise ValueError(
                "unresolved source name cannot expose selected text"
            )
        if (
            self.destination_name_state == RESOLVED
            and self.destination_recovered_text is None
        ):
            raise ValueError(
                "resolved destination name requires recovered text"
            )
        if (
            self.destination_name_state != RESOLVED
            and self.destination_recovered_text is not None
        ):
            raise ValueError(
                "unresolved destination name cannot expose selected text"
            )


@dataclass(frozen=True)
class VersionedWorldWarpNameDiagnostics:
    geometry: VersionedWorldGeometryManifest
    names: VersionedWorldNameOverlay
    rows: tuple[VersionedClassicWarpNameDiagnostic, ...]

    def __post_init__(self) -> None:
        rows = tuple(self.rows)
        if self.geometry.source_version != self.names.evidence.source_version:
            raise ValueError("warp/name semantic source version drift")

        geometry_world = self.geometry.world.by_floor
        names_world = self.names.world.by_floor
        if set(geometry_world) != set(names_world):
            raise ValueError("warp/name world floor set drift")
        for floor_id in geometry_world:
            if (
                geometry_world[floor_id].map_sha256
                != names_world[floor_id].map_sha256
            ):
                raise ValueError(
                    f"warp/name world map identity drift for floor {floor_id}"
                )

        if len(rows) != len(self.geometry.classic_warps):
            raise ValueError("warp/name diagnostic row count drift")
        for diagnostic, warp in zip(rows, self.geometry.classic_warps):
            if diagnostic.warp != warp:
                raise ValueError("warp/name diagnostic ordering drift")

        object.__setattr__(self, "rows", rows)

    @property
    def counts(self) -> Mapping[str, int]:
        counts: dict[str, int] = {"total": len(self.rows)}
        for row in self.rows:
            source_key = f"source:{row.source_name_state}"
            destination_key = f"destination:{row.destination_name_state}"
            pair_key = (
                f"pair:{row.source_name_state}"
                f"->{row.destination_name_state}"
            )
            counts[source_key] = counts.get(source_key, 0) + 1
            counts[destination_key] = counts.get(destination_key, 0) + 1
            counts[pair_key] = counts.get(pair_key, 0) + 1
        return MappingProxyType(counts)

    @property
    def distinct_floor_pairs(self) -> tuple[tuple[int, int], ...]:
        return tuple(
            sorted({
                (row.warp.source_floor, row.warp.destination_floor)
                for row in self.rows
            })
        )


def _state_for_floor(
    *,
    floor_id: int,
    stable: bool,
    names: VersionedWorldNameOverlay,
) -> tuple[str, str | None]:
    if not stable:
        return OUTSIDE_STABLE_WORLD, None
    if floor_id in names.by_floor:
        return RESOLVED, names.by_floor[floor_id].text
    if floor_id in names.unresolved_by_floor:
        return UNRESOLVED, None
    return ABSENT, None


def build_versioned_warp_name_diagnostics(
    *,
    geometry: VersionedWorldGeometryManifest,
    names: VersionedWorldNameOverlay,
) -> VersionedWorldWarpNameDiagnostics:
    rows: list[VersionedClassicWarpNameDiagnostic] = []
    stable_ids = set(geometry.world.by_floor)

    for warp in geometry.classic_warps:
        source_state, source_text = _state_for_floor(
            floor_id=warp.source_floor,
            stable=warp.source_floor in stable_ids,
            names=names,
        )
        destination_state, destination_text = _state_for_floor(
            floor_id=warp.destination_floor,
            stable=warp.destination_is_stable_candidate,
            names=names,
        )
        rows.append(
            VersionedClassicWarpNameDiagnostic(
                warp=warp,
                source_name_state=source_state,
                destination_name_state=destination_state,
                source_recovered_text=source_text,
                destination_recovered_text=destination_text,
            )
        )

    return VersionedWorldWarpNameDiagnostics(
        geometry=geometry,
        names=names,
        rows=tuple(rows),
    )
