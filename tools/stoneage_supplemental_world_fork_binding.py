#!/usr/bin/env python3
"""Bind the explicit floor-130 version fork into the supplemental world.

The base supplemental extension deliberately excludes floor 130 from its
materializable topology. This binding enriches that unresolved floor with the
separate arbitration evidence and exposes candidate map definitions only by an
explicit candidate-path request. There is intentionally no default candidate.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from tools.stoneage_floor130_arbitration import (
    Floor130Arbitration,
    Floor130CandidateArbitration,
    PRESERVE_VERSION_FORK,
    RECOVERED25_AUDIT_REF,
    LINEAGE_AUDIT_REF,
)
from tools.stoneage_singleplayer_world import (
    HistoricalMapDefinition,
    LATER_RECOVERED,
    RESOURCE_RELATION_UNKNOWN,
    WorldMapProvenance,
)
from tools.stoneage_supplemental_world_manifest import (
    SUPPLEMENTAL_AUDIT_REPORT_REF,
    SupplementalWorldExtension,
)


FORKED_SUPPLEMENTAL_MAP_EVIDENCE = "RECOVERED25_SUPPLEMENTAL_VERSION_FORK"


@dataclass(frozen=True)
class SupplementalForkCandidate:
    floor_id: int
    path: str
    width: int
    height: int
    sha256: str
    arbitration: Floor130CandidateArbitration

    def __post_init__(self) -> None:
        if int(self.floor_id) != 130:
            raise ValueError("current supplemental fork binding is floor-130 only")
        if self.path != self.arbitration.path:
            raise ValueError("fork candidate path/arbitration drift")
        if self.sha256.lower() != self.arbitration.sha256.lower():
            raise ValueError("fork candidate SHA/arbitration drift")
        if int(self.width) <= 0 or int(self.height) <= 0:
            raise ValueError("fork candidate dimensions must be positive")
        object.__setattr__(self, "floor_id", 130)
        object.__setattr__(self, "width", int(self.width))
        object.__setattr__(self, "height", int(self.height))
        object.__setattr__(self, "sha256", self.sha256.lower())

    @property
    def provenance(self) -> WorldMapProvenance:
        return WorldMapProvenance(
            content_role=LATER_RECOVERED,
            resource_role=RESOURCE_RELATION_UNKNOWN,
            source_versions=("recovered25",),
            evidence_refs=(
                SUPPLEMENTAL_AUDIT_REPORT_REF,
                RECOVERED25_AUDIT_REF,
                LINEAGE_AUDIT_REF,
            ),
            payload_sha256=self.sha256,
        )

    def to_map_definition(self) -> HistoricalMapDefinition:
        return HistoricalMapDefinition(
            floor_id=self.floor_id,
            width=self.width,
            height=self.height,
            evidence=FORKED_SUPPLEMENTAL_MAP_EVIDENCE,
            provenance=self.provenance,
        )


@dataclass(frozen=True)
class SupplementalWorldForkBinding:
    extension: SupplementalWorldExtension
    floor_id: int
    resolution: str
    candidates: tuple[SupplementalForkCandidate, ...]
    selected_path: str | None = None

    def __post_init__(self) -> None:
        if int(self.floor_id) != 130:
            raise ValueError("supplemental fork binding is currently floor-130 only")
        if self.resolution != PRESERVE_VERSION_FORK:
            raise ValueError("supplemental fork binding must preserve version fork")
        if self.selected_path is not None:
            raise ValueError("supplemental fork binding cannot define a default path")
        rows = tuple(self.candidates)
        if len(rows) != 2:
            raise ValueError("floor130 fork binding requires exactly two candidates")
        if len({row.path for row in rows}) != 2:
            raise ValueError("floor130 fork candidates must have distinct paths")
        if len({row.sha256 for row in rows}) != 2:
            raise ValueError("floor130 fork candidates must remain byte-divergent")
        if 130 not in self.extension.unresolved_by_floor:
            raise ValueError("floor130 is no longer unresolved in supplemental extension")
        if 130 in self.extension.materializable_map_definitions:
            raise ValueError("floor130 leaked into default materializable topology")
        object.__setattr__(self, "floor_id", 130)
        object.__setattr__(self, "candidates", rows)

    @property
    def by_path(self) -> Mapping[str, SupplementalForkCandidate]:
        return MappingProxyType({row.path: row for row in self.candidates})

    @property
    def default_map_definition(self) -> None:
        """No implicit version choice exists for the recovered fork."""
        return None

    def candidate_map_definition(self, path: str) -> HistoricalMapDefinition:
        """Return a concrete candidate only after an explicit path choice."""
        path = str(path)
        if path not in self.by_path:
            raise KeyError(f"unknown floor130 fork candidate: {path}")
        return self.by_path[path].to_map_definition()


def bind_floor130_version_fork(
    *,
    extension: SupplementalWorldExtension,
    arbitration: Floor130Arbitration,
) -> SupplementalWorldForkBinding:
    if arbitration.floor_id != 130:
        raise ValueError("floor130 arbitration id drift")
    if arbitration.resolution != PRESERVE_VERSION_FORK:
        raise ValueError("floor130 arbitration no longer preserves fork")
    if arbitration.selected_path is not None:
        raise ValueError("floor130 arbitration unexpectedly selected a path")

    unresolved = extension.unresolved_by_floor.get(130)
    if unresolved is None:
        raise ValueError("supplemental extension has no unresolved floor 130")

    dimensions_by_path = dict(zip(
        unresolved.server_paths,
        unresolved.server_dimensions,
    ))
    hashes_by_path = dict(zip(
        unresolved.server_paths,
        unresolved.server_sha256s,
    ))

    if set(dimensions_by_path) != set(arbitration.by_path):
        raise ValueError("floor130 unresolved/arbitration path-set drift")

    candidates = []
    for path in sorted(arbitration.by_path):
        arb = arbitration.by_path[path]
        if hashes_by_path[path].lower() != arb.sha256.lower():
            raise ValueError(f"floor130 unresolved/arbitration SHA drift for {path}")
        width, height = dimensions_by_path[path]
        candidates.append(
            SupplementalForkCandidate(
                floor_id=130,
                path=path,
                width=width,
                height=height,
                sha256=hashes_by_path[path],
                arbitration=arb,
            )
        )

    return SupplementalWorldForkBinding(
        extension=extension,
        floor_id=130,
        resolution=arbitration.resolution,
        candidates=tuple(candidates),
        selected_path=None,
    )
