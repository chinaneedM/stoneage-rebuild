#!/usr/bin/env python3
"""Engine-neutral anonymous NPC template identity layer.

This parser consumes derived metadata only. It never needs template names,
dialogue, NPC arguments, or original recovered source rows.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from tools.stoneage_singleplayer_world import LATER_RECOVERED
from tools.stoneage_versioned_npc_spawn_catalogue import (
    VersionedNpcSpawnCatalogue,
)


TEMPLATE_BINDING_REPORT_REF = (
    "research/recovered/STONEAGE-25-STABLE-NPC-TEMPLATE-BINDINGS-R1.txt"
)
SEMANTIC_SOURCE_VERSION = "recovered25"

UNIQUE_NAME = "UNIQUE_NAME"
DUPLICATE_NAME_SAME_FUNCTIONSET = "DUPLICATE_NAME_SAME_FUNCTIONSET"
DUPLICATE_NAME_FUNCTIONSET_AMBIGUOUS = (
    "DUPLICATE_NAME_FUNCTIONSET_AMBIGUOUS"
)
_ALLOWED_STATUS = {
    UNIQUE_NAME,
    DUPLICATE_NAME_SAME_FUNCTIONSET,
    DUPLICATE_NAME_FUNCTIONSET_AMBIGUOUS,
}


def _fields(line: str, prefix: str) -> dict[str, str]:
    parts = line.split("|")
    if not parts or parts[0] != prefix:
        raise ValueError(f"expected {prefix} record")
    out: dict[str, str] = {}
    for part in parts[1:]:
        if "=" not in part:
            raise ValueError(f"malformed {prefix} field: {part}")
        key, value = part.split("=", 1)
        if not key or key in out:
            raise ValueError(f"duplicate/blank {prefix} field: {key}")
        out[key] = value
    return out


def _sha256_key(value: str) -> str:
    value = str(value).lower()
    if len(value) != 64 or any(
        char not in "0123456789abcdef" for char in value
    ):
        raise ValueError("anonymous template key must be 64 hex digits")
    return value


@dataclass(frozen=True)
class AnonymousNpcTemplateIdentity:
    key: str
    variant_count: int
    variant_fingerprint_count: int
    functionset_consensus: str
    functionset_variant_count: int
    stable_placement_count: int
    source_version: str = SEMANTIC_SOURCE_VERSION
    evidence_role: str = LATER_RECOVERED

    def __post_init__(self) -> None:
        object.__setattr__(self, "key", _sha256_key(self.key))
        for name in (
            "variant_count",
            "variant_fingerprint_count",
            "functionset_variant_count",
            "stable_placement_count",
        ):
            value = int(getattr(self, name))
            if value < 0:
                raise ValueError(f"{name} cannot be negative")
            object.__setattr__(self, name, value)
        if self.variant_count <= 0:
            raise ValueError("anonymous template identity requires a variant")
        if not 1 <= self.variant_fingerprint_count <= self.variant_count:
            raise ValueError("template fingerprint count outside variant range")
        if not 1 <= self.functionset_variant_count <= self.variant_count:
            raise ValueError("functionset variant count outside variant range")
        if self.stable_placement_count <= 0:
            raise ValueError("referenced template identity needs placements")
        if not str(self.functionset_consensus):
            raise ValueError("functionset consensus cannot be blank")
        if self.evidence_role != LATER_RECOVERED:
            raise ValueError(
                "anonymous recovered template identity must remain LATER_RECOVERED"
            )

    @property
    def concrete_variant_is_unique(self) -> bool:
        return self.variant_count == 1

    @property
    def functionset_is_consensus(self) -> bool:
        return (
            self.functionset_variant_count == 1
            and self.functionset_consensus != "<ambiguous>"
        )


@dataclass(frozen=True)
class VersionedNpcTemplateBinding:
    placement_id: int
    floor_id: int
    template_key: str
    variant_count: int
    functionset_consensus: str
    functionset_variant_count: int
    status: str
    classic_warp_geometry: bool
    source_version: str = SEMANTIC_SOURCE_VERSION
    evidence_role: str = LATER_RECOVERED

    def __post_init__(self) -> None:
        object.__setattr__(self, "placement_id", int(self.placement_id))
        object.__setattr__(self, "floor_id", int(self.floor_id))
        object.__setattr__(self, "template_key", _sha256_key(self.template_key))
        object.__setattr__(self, "variant_count", int(self.variant_count))
        object.__setattr__(
            self,
            "functionset_variant_count",
            int(self.functionset_variant_count),
        )
        object.__setattr__(
            self, "classic_warp_geometry", bool(self.classic_warp_geometry)
        )
        if self.variant_count <= 0:
            raise ValueError("template binding variant_count must be positive")
        if not 1 <= self.functionset_variant_count <= self.variant_count:
            raise ValueError(
                "template binding functionset variants outside variant range"
            )
        if self.status not in _ALLOWED_STATUS:
            raise ValueError(f"unknown template binding status {self.status}")
        if self.status == UNIQUE_NAME and self.variant_count != 1:
            raise ValueError("UNIQUE_NAME binding must have exactly one variant")
        if (
            self.status == DUPLICATE_NAME_SAME_FUNCTIONSET
            and (
                self.variant_count <= 1
                or self.functionset_variant_count != 1
                or self.functionset_consensus == "<ambiguous>"
            )
        ):
            raise ValueError("invalid duplicate/same-functionset binding")
        if (
            self.status == DUPLICATE_NAME_FUNCTIONSET_AMBIGUOUS
            and (
                self.variant_count <= 1
                or self.functionset_variant_count <= 1
                or self.functionset_consensus != "<ambiguous>"
            )
        ):
            raise ValueError("invalid duplicate/functionset-ambiguous binding")
        if self.evidence_role != LATER_RECOVERED:
            raise ValueError(
                "recovered template binding must remain LATER_RECOVERED"
            )

    @property
    def concrete_template_binding_is_unique(self) -> bool:
        return self.status == UNIQUE_NAME

    @property
    def functionset_is_consensus(self) -> bool:
        return self.functionset_consensus != "<ambiguous>"


@dataclass(frozen=True)
class VersionedNpcTemplateBindingManifest:
    spawn_catalogue: VersionedNpcSpawnCatalogue
    identities: Mapping[str, AnonymousNpcTemplateIdentity]
    bindings: tuple[VersionedNpcTemplateBinding, ...]
    source_version: str = SEMANTIC_SOURCE_VERSION

    def __post_init__(self) -> None:
        identities = {str(key): value for key, value in self.identities.items()}
        bindings = tuple(self.bindings)
        if self.source_version != self.spawn_catalogue.source_version:
            raise ValueError("NPC template binding source-version drift")

        for key, identity in identities.items():
            if key != identity.key:
                raise ValueError("anonymous template identity key drift")
            if identity.source_version != self.source_version:
                raise ValueError("anonymous template identity source drift")

        by_placement: dict[int, VersionedNpcTemplateBinding] = {}
        identity_counts: dict[str, int] = {}
        for binding in bindings:
            if binding.placement_id in by_placement:
                raise ValueError(
                    f"duplicate NPC template binding {binding.placement_id}"
                )
            by_placement[binding.placement_id] = binding
            identity_counts[binding.template_key] = (
                identity_counts.get(binding.template_key, 0) + 1
            )
            if binding.template_key not in identities:
                raise ValueError(
                    f"binding references unknown template key {binding.template_key}"
                )
            identity = identities[binding.template_key]
            if binding.variant_count != identity.variant_count:
                raise ValueError("binding/template variant-count drift")
            if (
                binding.functionset_consensus
                != identity.functionset_consensus
            ):
                raise ValueError("binding/template functionset consensus drift")
            if (
                binding.functionset_variant_count
                != identity.functionset_variant_count
            ):
                raise ValueError("binding/template functionset-count drift")

        spawn_by_id = self.spawn_catalogue.by_id
        if set(by_placement) != set(spawn_by_id):
            missing = sorted(set(spawn_by_id) - set(by_placement))
            extra = sorted(set(by_placement) - set(spawn_by_id))
            raise ValueError(
                "NPC template bindings do not cover spawn catalogue; "
                f"missing={missing}, extra={extra}"
            )
        for placement_id, binding in by_placement.items():
            if spawn_by_id[placement_id].floor_id != binding.floor_id:
                raise ValueError(
                    f"NPC template binding floor drift at {placement_id}"
                )

        if set(identity_counts) != set(identities):
            raise ValueError("unreferenced/missing anonymous template identities")
        for key, count in identity_counts.items():
            if identities[key].stable_placement_count != count:
                raise ValueError(
                    f"anonymous template placement count drift for {key}"
                )

        object.__setattr__(
            self, "identities", MappingProxyType(identities)
        )
        object.__setattr__(self, "bindings", bindings)

    @property
    def by_placement(self) -> Mapping[int, VersionedNpcTemplateBinding]:
        return MappingProxyType({
            binding.placement_id: binding for binding in self.bindings
        })

    @property
    def unique_concrete_bindings(
        self,
    ) -> tuple[VersionedNpcTemplateBinding, ...]:
        return tuple(
            binding for binding in self.bindings
            if binding.concrete_template_binding_is_unique
        )

    @property
    def duplicate_name_bindings(
        self,
    ) -> tuple[VersionedNpcTemplateBinding, ...]:
        return tuple(
            binding for binding in self.bindings
            if not binding.concrete_template_binding_is_unique
        )

    @property
    def direct_spawn_with_identity_eligible(
        self,
    ) -> tuple[VersionedNpcTemplateBinding, ...]:
        spawn_by_id = self.spawn_catalogue.by_id
        return tuple(
            binding for binding in self.bindings
            if (
                binding.concrete_template_binding_is_unique
                and spawn_by_id[binding.placement_id]
                    .direct_projection_eligible(
                        self.spawn_catalogue.world_geometry
                    )
            )
        )

    @property
    def classic_warp_functionset_inconsistencies(
        self,
    ) -> tuple[VersionedNpcTemplateBinding, ...]:
        return tuple(
            binding for binding in self.bindings
            if (
                binding.classic_warp_geometry
                and binding.functionset_consensus != "Warp"
            )
        )


def parse_versioned_npc_template_bindings(
    *,
    spawn_catalogue: VersionedNpcSpawnCatalogue,
    text: str,
) -> VersionedNpcTemplateBindingManifest:
    source_version: str | None = None
    evidence_role: str | None = None
    identities: dict[str, AnonymousNpcTemplateIdentity] = {}
    bindings: list[VersionedNpcTemplateBinding] = []
    counts: dict[str, int] = {}
    resolution = False

    for raw in str(text).splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("SEMANTIC_SOURCE_VERSION|"):
            if source_version is not None:
                raise ValueError("duplicate template-binding source version")
            source_version = line.split("|", 1)[1]
            continue
        if line.startswith("EVIDENCE_ROLE|"):
            if evidence_role is not None:
                raise ValueError("duplicate template-binding evidence role")
            evidence_role = line.split("|", 1)[1]
            continue
        if line.startswith("COUNT|"):
            parts = line.split("|")
            if len(parts) != 3:
                raise ValueError(f"malformed COUNT row: {line}")
            counts[parts[1]] = int(parts[2])
            continue
        if line.startswith("TEMPLATE_IDENTITY|"):
            fields = _fields(line, "TEMPLATE_IDENTITY")
            identity = AnonymousNpcTemplateIdentity(
                key=fields["key"],
                variant_count=int(fields["variants"]),
                variant_fingerprint_count=int(
                    fields["variant_fingerprints"]
                ),
                functionset_consensus=fields["functionset_consensus"],
                functionset_variant_count=int(
                    fields["functionset_variants"]
                ),
                stable_placement_count=int(
                    fields["stable_placements"]
                ),
                source_version=source_version or "",
                evidence_role=evidence_role or "",
            )
            if identity.key in identities:
                raise ValueError(
                    f"duplicate anonymous template identity {identity.key}"
                )
            identities[identity.key] = identity
            continue
        if line.startswith("PLACEMENT_TEMPLATE|"):
            fields = _fields(line, "PLACEMENT_TEMPLATE")
            bindings.append(
                VersionedNpcTemplateBinding(
                    placement_id=int(fields["placement"]),
                    floor_id=int(fields["floor"]),
                    template_key=fields["template_key"],
                    variant_count=int(fields["variants"]),
                    functionset_consensus=fields["functionset_consensus"],
                    functionset_variant_count=int(
                        fields["functionset_variants"]
                    ),
                    status=fields["status"],
                    classic_warp_geometry=bool(
                        int(fields["classic_warp_geometry"])
                    ),
                    source_version=source_version or "",
                    evidence_role=evidence_role or "",
                )
            )
            continue
        if line == "RESOLUTION|ANONYMOUS_NPC_TEMPLATE_BINDINGS_CLASSIFIED":
            resolution = True

    if source_version is None:
        raise ValueError("template binding report lacks source version")
    if evidence_role != LATER_RECOVERED:
        raise ValueError(
            "template binding report must remain LATER_RECOVERED"
        )
    if not resolution:
        raise ValueError("template binding report lacks closed resolution")
    if "stable_spawn_placements" not in counts:
        raise ValueError("template binding report lacks placement count")
    if counts["stable_spawn_placements"] != len(bindings):
        raise ValueError("template binding placement count drift")
    if len(bindings) != len(spawn_catalogue.placements):
        raise ValueError(
            "template binding count does not match spawn catalogue"
        )
    if (
        "unique_referenced_template_identities" in counts
        and counts["unique_referenced_template_identities"]
        != len(identities)
    ):
        raise ValueError("template identity count drift")

    return VersionedNpcTemplateBindingManifest(
        spawn_catalogue=spawn_catalogue,
        identities=identities,
        bindings=tuple(bindings),
        source_version=source_version,
    )
