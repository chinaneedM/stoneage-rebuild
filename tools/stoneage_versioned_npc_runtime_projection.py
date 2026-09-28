#!/usr/bin/env python3
"""Compose versioned NPC spawn/template layers into generic runtime intents.

This layer remains intentionally earlier than function-specific INITFUNC behavior
and presentation text. It can feed the existing NpcRuntimeState boundary only
when the caller explicitly supplies behavior-dependent world object type and
display text; opaque graphic tokens require an explicit provenance-safe
resolution as well.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from tools.stoneage_singleplayer_domain import MapPosition
from tools.stoneage_singleplayer_world import LATER_RECOVERED
from tools.stoneage_tw10_25_bridge_model import NpcRuntimeState
from tools.stoneage_tw10_gameplay_model import TemplateRef
from tools.stoneage_versioned_npc_spawn_catalogue import (
    VersionedNpcSpawnCatalogue,
)
from tools.stoneage_versioned_npc_template_binding import (
    VersionedNpcTemplateBindingManifest,
)
from tools.stoneage_versioned_npc_template_profile import (
    AnonymousNpcTemplateRuntimeProfile,
    VersionedNpcTemplateRuntimeProfiles,
)


SEMANTIC_SOURCE_VERSION = "recovered25"
ANONYMOUS_TEMPLATE_NAMESPACE = "npc.template.sha256"

ISSUE_SPAWN_INTEGRITY = "SPAWN_INTEGRITY"
ISSUE_OPAQUE_GRAPHIC = "OPAQUE_GRAPHIC"
ISSUE_OPAQUE_TYPE = "OPAQUE_TYPE"


@dataclass(frozen=True)
class VersionedGenericNpcSpawnIntent:
    """One recovered create/template composition before class-specific behavior."""

    placement_id: int
    template_key: str
    functionset: str
    profile: AnonymousNpcTemplateRuntimeProfile
    floor_id: int
    birth_rect: tuple[int, int, int, int]
    move_rect: tuple[int, int, int, int]
    raw_direction: int
    normalized_direction: int
    population_cap: int
    respawn_delay_ms: int
    boundary_enabled: bool
    ignore_invincible_area: bool
    spawn_integrity_issues: tuple[str, ...]
    source_version: str = SEMANTIC_SOURCE_VERSION
    evidence_role: str = LATER_RECOVERED

    def __post_init__(self) -> None:
        object.__setattr__(self, "placement_id", int(self.placement_id))
        object.__setattr__(self, "floor_id", int(self.floor_id))
        object.__setattr__(self, "raw_direction", int(self.raw_direction))
        object.__setattr__(
            self, "normalized_direction", int(self.normalized_direction)
        )
        object.__setattr__(self, "population_cap", int(self.population_cap))
        object.__setattr__(
            self, "respawn_delay_ms", int(self.respawn_delay_ms)
        )
        object.__setattr__(
            self, "boundary_enabled", bool(self.boundary_enabled)
        )
        object.__setattr__(
            self,
            "ignore_invincible_area",
            bool(self.ignore_invincible_area),
        )
        object.__setattr__(
            self,
            "spawn_integrity_issues",
            tuple(str(value) for value in self.spawn_integrity_issues),
        )
        if self.template_key != self.profile.template_key:
            raise ValueError("generic NPC intent template/profile key drift")
        if self.functionset != self.profile.functionset:
            raise ValueError("generic NPC intent functionset/profile drift")
        if not 0 <= self.normalized_direction < 8:
            raise ValueError("normalized direction must be in 0..7")
        if self.evidence_role != LATER_RECOVERED:
            raise ValueError(
                "recovered generic NPC intent must remain LATER_RECOVERED"
            )

    @property
    def birth_is_single_cell(self) -> bool:
        x1, y1, x2, y2 = self.birth_rect
        return x1 == x2 and y1 == y2

    @property
    def deterministic_birth_position(self) -> MapPosition | None:
        if not self.birth_is_single_cell:
            return None
        x1, y1, _x2, _y2 = self.birth_rect
        return MapPosition(self.floor_id, x1, y1)

    @property
    def spawn_integrity_eligible(self) -> bool:
        return not self.spawn_integrity_issues

    @property
    def intrinsic_graphic_id(self) -> int | None:
        if self.profile.graphic_resolution == "NUMERIC":
            return self.profile.graphic_value
        if self.profile.graphic_resolution == "DEFAULT_ZERO":
            return 0
        return None

    @property
    def graphic_requires_external_resolution(self) -> bool:
        return self.profile.graphic_resolution == "OPAQUE_SYMBOL"

    @property
    def type_requires_external_resolution(self) -> bool:
        return self.profile.type_resolution == "OPAQUE_SYMBOL"

    @property
    def unresolved_structural_issues(self) -> tuple[str, ...]:
        issues = []
        if self.spawn_integrity_issues:
            issues.append(ISSUE_SPAWN_INTEGRITY)
        if self.graphic_requires_external_resolution:
            issues.append(ISSUE_OPAQUE_GRAPHIC)
        if self.type_requires_external_resolution:
            issues.append(ISSUE_OPAQUE_TYPE)
        return tuple(issues)

    def materialize_npc_runtime_state(
        self,
        *,
        runtime_object_id: int,
        display_name: str,
        object_type: int,
        default_level: int,
        default_name_color: int,
        resolved_graphic_id: int | None = None,
        default_self_title: str = "",
        default_walkable: int = 0,
        default_height: int = 0,
    ) -> NpcRuntimeState:
        """Bridge after explicit behavior/presentation inputs are supplied.

        object_type is deliberately caller-supplied because INITFUNC/functionset
        can specialize the generic shell. display_name is caller-supplied because
        presentation text is excluded from this reconstruction layer.
        """
        if not self.spawn_integrity_eligible:
            raise ValueError(
                f"placement {self.placement_id} is quarantined: "
                f"{self.spawn_integrity_issues}"
            )
        position = self.deterministic_birth_position
        if position is None:
            raise ValueError(
                f"placement {self.placement_id} needs an explicit spawn-point roll"
            )

        graphic = (
            self.intrinsic_graphic_id
            if resolved_graphic_id is None
            else int(resolved_graphic_id)
        )
        if graphic is None:
            raise ValueError(
                f"placement {self.placement_id} has opaque graphic token; "
                "resolved_graphic_id is required"
            )
        if graphic < 0:
            raise ValueError("resolved graphic ID cannot be negative")

        return NpcRuntimeState(
            runtime_object_id=int(runtime_object_id),
            template_ref=TemplateRef(
                ANONYMOUS_TEMPLATE_NAMESPACE,
                self.template_key,
                evidence="LATER_RECOVERED:recovered25",
            ),
            floor_id=position.floor_id,
            x=position.x,
            y=position.y,
            direction=self.raw_direction,
            base_graphic_id=graphic,
            name=str(display_name),
            object_type=int(object_type),
            level=int(default_level),
            name_color=int(default_name_color),
            self_title=str(default_self_title),
            walkable=int(default_walkable),
            height=int(default_height),
            create_index=self.placement_id,
        )


@dataclass(frozen=True)
class VersionedGenericNpcSpawnProjection:
    spawn_catalogue: VersionedNpcSpawnCatalogue
    bindings: VersionedNpcTemplateBindingManifest
    profiles: VersionedNpcTemplateRuntimeProfiles
    intents: tuple[VersionedGenericNpcSpawnIntent, ...]
    source_version: str = SEMANTIC_SOURCE_VERSION

    def __post_init__(self) -> None:
        intents = tuple(self.intents)
        if (
            self.source_version != self.spawn_catalogue.source_version
            or self.source_version != self.bindings.source_version
            or self.source_version != self.profiles.source_version
        ):
            raise ValueError("generic NPC projection source-version drift")
        if self.bindings.spawn_catalogue is not self.spawn_catalogue:
            raise ValueError("generic NPC projection binding/spawn chain drift")
        if self.profiles.bindings is not self.bindings:
            raise ValueError("generic NPC projection profile/binding chain drift")

        by_id: dict[int, VersionedGenericNpcSpawnIntent] = {}
        for intent in intents:
            if intent.placement_id in by_id:
                raise ValueError(
                    f"duplicate generic NPC intent {intent.placement_id}"
                )
            by_id[intent.placement_id] = intent
        if set(by_id) != set(self.spawn_catalogue.by_id):
            raise ValueError(
                "generic NPC intents do not cover spawn catalogue"
            )
        object.__setattr__(self, "intents", intents)

    @property
    def by_placement(self) -> Mapping[int, VersionedGenericNpcSpawnIntent]:
        return MappingProxyType({
            intent.placement_id: intent for intent in self.intents
        })

    @property
    def spawn_integrity_eligible(
        self,
    ) -> tuple[VersionedGenericNpcSpawnIntent, ...]:
        return tuple(
            intent for intent in self.intents
            if intent.spawn_integrity_eligible
        )

    @property
    def intrinsic_graphic_resolved(
        self,
    ) -> tuple[VersionedGenericNpcSpawnIntent, ...]:
        return tuple(
            intent for intent in self.intents
            if intent.intrinsic_graphic_id is not None
        )

    @property
    def spawn_safe_intrinsic_graphic_resolved(
        self,
    ) -> tuple[VersionedGenericNpcSpawnIntent, ...]:
        return tuple(
            intent for intent in self.intents
            if (
                intent.spawn_integrity_eligible
                and intent.intrinsic_graphic_id is not None
            )
        )

    @property
    def opaque_graphic_intents(
        self,
    ) -> tuple[VersionedGenericNpcSpawnIntent, ...]:
        return tuple(
            intent for intent in self.intents
            if intent.graphic_requires_external_resolution
        )

    @property
    def opaque_type_intents(
        self,
    ) -> tuple[VersionedGenericNpcSpawnIntent, ...]:
        return tuple(
            intent for intent in self.intents
            if intent.type_requires_external_resolution
        )


def build_versioned_generic_npc_spawn_projection(
    *,
    spawn_catalogue: VersionedNpcSpawnCatalogue,
    bindings: VersionedNpcTemplateBindingManifest,
    profiles: VersionedNpcTemplateRuntimeProfiles,
) -> VersionedGenericNpcSpawnProjection:
    intents = []
    for placement in spawn_catalogue.placements:
        binding = bindings.by_placement[placement.placement_id]
        profile = profiles.runtime_equivalent_profile_for_placement(
            placement.placement_id
        )
        intents.append(
            VersionedGenericNpcSpawnIntent(
                placement_id=placement.placement_id,
                template_key=binding.template_key,
                functionset=binding.functionset_consensus,
                profile=profile,
                floor_id=placement.floor_id,
                birth_rect=placement.birth_rect,
                move_rect=placement.move_rect,
                raw_direction=placement.raw_direction,
                normalized_direction=placement.normalized_direction,
                population_cap=placement.population_cap,
                respawn_delay_ms=placement.respawn_delay_ms,
                boundary_enabled=placement.boundary_enabled,
                ignore_invincible_area=placement.ignore_invincible_area,
                spawn_integrity_issues=placement.direct_projection_issues(
                    spawn_catalogue.world_geometry
                ),
            )
        )
    return VersionedGenericNpcSpawnProjection(
        spawn_catalogue=spawn_catalogue,
        bindings=bindings,
        profiles=profiles,
        intents=tuple(intents),
        source_version=spawn_catalogue.source_version,
    )
