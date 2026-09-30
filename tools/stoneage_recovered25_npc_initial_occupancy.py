#!/usr/bin/env python3
"""Recovered25 initial NPC occupancy manifest.

This layer composes two already-audited but intentionally separate surfaces:

* recovered25 NPC placement/template projection (LATER_RECOVERED);
* pinned stable-descendant CHAR_ISOVERED behavior classification.

It resolves only the initial live-character overlap state. Static map collision
remains owned by the recovered25 collision router, and future runtime mutations
must update the live occupancy registry explicitly.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Mapping

from tools.stoneage_map_collision_model import CHARACTER
from tools.stoneage_runtime_occupancy_registry import (
    RuntimeDynamicOccupancyRegistry,
)
from tools.stoneage_singleplayer_domain import MapPosition
from tools.stoneage_singleplayer_world import LATER_RECOVERED
from tools.stoneage_versioned_npc_overability_profile import (
    VersionedNpcOverabilityProfile,
    load_recovered25_npc_overability_profile,
)
from tools.stoneage_versioned_npc_runtime_projection import (
    VersionedGenericNpcSpawnProjection,
    build_versioned_generic_npc_spawn_projection,
)
from tools.stoneage_versioned_npc_spawn_catalogue import (
    build_versioned_npc_spawn_catalogue,
)
from tools.stoneage_versioned_npc_template_binding import (
    TEMPLATE_BINDING_REPORT_REF,
    parse_versioned_npc_template_bindings,
)
from tools.stoneage_versioned_npc_template_profile import (
    TEMPLATE_PROFILE_REPORT_REF,
    parse_versioned_npc_template_profiles,
)
from tools.stoneage_versioned_world_geometry import (
    WORLD_GEOMETRY_REPORT_REF,
    parse_versioned_world_geometry,
)
from tools.stoneage_versioned_world_manifest import (
    COVERAGE_REPORT_REF,
    build_versioned_world_manifest,
)
from tools.stoneage_world_map_library import (
    LINEAGE_REPORT_REF,
    parse_stable_later_map_manifest,
)


SEMANTIC_SOURCE_VERSION = "recovered25"
INITIAL_NPC_OCCUPANCY_PROFILE = "RECOVERED25_INITIAL_NPC_OCCUPANCY_R1"
INITIAL_NPC_OCCUPANCY_EVIDENCE_CLASS = (
    "LATER_RECOVERED_PLACEMENT_PLUS_PINNED_STABLE_DESCENDANT_OVERABILITY"
)
ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Recovered25NpcInitialOccupancySeed:
    placement_id: int
    functionset: str
    position: MapPosition
    overable: bool
    overability_classification: str
    spawn_integrity_eligible: bool
    provenance: str
    source_version: str = SEMANTIC_SOURCE_VERSION
    evidence_role: str = LATER_RECOVERED

    def __post_init__(self) -> None:
        object.__setattr__(self, "placement_id", int(self.placement_id))
        object.__setattr__(self, "functionset", str(self.functionset))
        object.__setattr__(self, "overable", bool(self.overable))
        object.__setattr__(
            self,
            "spawn_integrity_eligible",
            bool(self.spawn_integrity_eligible),
        )
        object.__setattr__(
            self,
            "overability_classification",
            str(self.overability_classification),
        )
        provenance = str(self.provenance).strip()
        if self.placement_id < 0:
            raise ValueError("NPC occupancy placement_id cannot be negative")
        if not self.functionset:
            raise ValueError("NPC occupancy functionset cannot be empty")
        if not isinstance(self.position, MapPosition):
            raise TypeError("NPC occupancy position must be MapPosition")
        if not self.overability_classification:
            raise ValueError("NPC occupancy classification cannot be empty")
        if not provenance:
            raise ValueError("NPC occupancy provenance cannot be empty")
        if self.source_version != SEMANTIC_SOURCE_VERSION:
            raise ValueError("NPC occupancy source-version drift")
        if self.evidence_role != LATER_RECOVERED:
            raise ValueError("NPC occupancy placement must remain LATER_RECOVERED")
        object.__setattr__(self, "provenance", provenance)

    @property
    def object_id(self) -> str:
        return f"npc-placement:{self.placement_id}"


@dataclass(frozen=True)
class Recovered25NpcInitialOccupancyManifest:
    projection: VersionedGenericNpcSpawnProjection
    overability_profile: VersionedNpcOverabilityProfile
    rows: tuple[Recovered25NpcInitialOccupancySeed, ...]
    source_version: str = SEMANTIC_SOURCE_VERSION
    profile_id: str = INITIAL_NPC_OCCUPANCY_PROFILE
    evidence_class: str = INITIAL_NPC_OCCUPANCY_EVIDENCE_CLASS

    def __post_init__(self) -> None:
        rows = tuple(self.rows)
        if self.source_version != SEMANTIC_SOURCE_VERSION:
            raise ValueError("NPC occupancy manifest source-version drift")
        if self.projection.source_version != self.source_version:
            raise ValueError("NPC occupancy projection source-version drift")
        if self.overability_profile.source_version != self.source_version:
            raise ValueError("NPC occupancy overability source-version drift")
        if len(rows) != len(self.projection.intents):
            raise ValueError("NPC occupancy row/projection count drift")

        by_id: dict[int, Recovered25NpcInitialOccupancySeed] = {}
        functionset_counts: dict[str, int] = {}
        for row in rows:
            if row.placement_id in by_id:
                raise ValueError(
                    f"duplicate NPC occupancy placement {row.placement_id}"
                )
            by_id[row.placement_id] = row
            functionset_counts[row.functionset] = (
                functionset_counts.get(row.functionset, 0) + 1
            )
        if set(by_id) != set(self.projection.by_placement):
            raise ValueError("NPC occupancy placement coverage drift")
        if set(functionset_counts) != set(self.overability_profile.rules):
            raise ValueError("NPC occupancy functionset coverage drift")
        for functionset, rule in self.overability_profile.rules.items():
            if functionset_counts[functionset] != rule.placement_count:
                raise ValueError(
                    f"NPC occupancy placement count drift for {functionset}"
                )
        object.__setattr__(self, "rows", rows)

    @property
    def by_placement(self) -> Mapping[int, Recovered25NpcInitialOccupancySeed]:
        return MappingProxyType({row.placement_id: row for row in self.rows})

    @property
    def seedable_rows(self) -> tuple[Recovered25NpcInitialOccupancySeed, ...]:
        return tuple(row for row in self.rows if row.spawn_integrity_eligible)

    @property
    def quarantined_rows(self) -> tuple[Recovered25NpcInitialOccupancySeed, ...]:
        return tuple(row for row in self.rows if not row.spawn_integrity_eligible)

    @property
    def classification_counts(self) -> Mapping[str, int]:
        counts: dict[str, int] = {}
        for row in self.rows:
            counts[row.overability_classification] = (
                counts.get(row.overability_classification, 0) + 1
            )
        return MappingProxyType(counts)

    def populate_registry(
        self,
        registry: RuntimeDynamicOccupancyRegistry,
    ) -> tuple[str, ...]:
        if not isinstance(registry, RuntimeDynamicOccupancyRegistry):
            raise TypeError("NPC occupancy seed requires RuntimeDynamicOccupancyRegistry")
        seeded = []
        existing = registry.objects
        for row in self.seedable_rows:
            object_id = row.object_id
            current = existing.get(object_id)
            if current is not None:
                if (
                    current.kind != CHARACTER
                    or current.position != row.position
                    or current.overable != row.overable
                    or current.provenance != row.provenance
                ):
                    raise ValueError(
                        f"conflicting pre-existing NPC occupancy object {object_id}"
                    )
                seeded.append(object_id)
                continue
            registry.register_character(
                object_id=object_id,
                position=row.position,
                overable=row.overable,
                provenance=row.provenance,
            )
            seeded.append(object_id)
        return tuple(seeded)


def build_recovered25_npc_initial_occupancy_manifest(
    *,
    projection: VersionedGenericNpcSpawnProjection,
    overability_profile: VersionedNpcOverabilityProfile,
) -> Recovered25NpcInitialOccupancyManifest:
    counts: dict[str, int] = {}
    for intent in projection.intents:
        counts[intent.functionset] = counts.get(intent.functionset, 0) + 1
    if set(counts) != set(overability_profile.rules):
        raise ValueError("NPC occupancy projection/overability functionset drift")
    for functionset, count in counts.items():
        if overability_profile.rules[functionset].placement_count != count:
            raise ValueError(
                f"NPC occupancy projection count mismatch for {functionset}"
            )

    rows = []
    for intent in projection.intents:
        position = intent.deterministic_birth_position
        if position is None:
            raise ValueError(
                f"NPC occupancy placement {intent.placement_id} lacks deterministic birth"
            )
        rule = overability_profile.rule_for_functionset(intent.functionset)
        overable = overability_profile.initial_overable_for_functionset(
            intent.functionset
        )
        rows.append(
            Recovered25NpcInitialOccupancySeed(
                placement_id=intent.placement_id,
                functionset=intent.functionset,
                position=position,
                overable=overable,
                overability_classification=rule.classification,
                spawn_integrity_eligible=intent.spawn_integrity_eligible,
                provenance=(
                    f"{SEMANTIC_SOURCE_VERSION}:npc-placement:"
                    f"{intent.placement_id}:overability:{rule.classification}"
                ),
            )
        )
    return Recovered25NpcInitialOccupancyManifest(
        projection=projection,
        overability_profile=overability_profile,
        rows=tuple(rows),
    )


def _repo_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def load_recovered25_npc_initial_occupancy_manifest(
) -> Recovered25NpcInitialOccupancyManifest:
    maps = parse_stable_later_map_manifest(_repo_text(LINEAGE_REPORT_REF))
    world = build_versioned_world_manifest(
        maps=maps,
        coverage_text=_repo_text(COVERAGE_REPORT_REF),
    )
    geometry = parse_versioned_world_geometry(
        world=world,
        text=_repo_text(WORLD_GEOMETRY_REPORT_REF),
    )
    spawn = build_versioned_npc_spawn_catalogue(geometry)
    bindings = parse_versioned_npc_template_bindings(
        spawn_catalogue=spawn,
        text=_repo_text(TEMPLATE_BINDING_REPORT_REF),
    )
    profiles = parse_versioned_npc_template_profiles(
        bindings=bindings,
        text=_repo_text(TEMPLATE_PROFILE_REPORT_REF),
    )
    projection = build_versioned_generic_npc_spawn_projection(
        spawn_catalogue=spawn,
        bindings=bindings,
        profiles=profiles,
    )
    return build_recovered25_npc_initial_occupancy_manifest(
        projection=projection,
        overability_profile=load_recovered25_npc_overability_profile(),
    )
