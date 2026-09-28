#!/usr/bin/env python3
"""Engine-neutral parser for anonymous NPC template runtime profiles."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from tools.stoneage_singleplayer_world import LATER_RECOVERED
from tools.stoneage_versioned_npc_template_binding import (
    VersionedNpcTemplateBindingManifest,
)


TEMPLATE_PROFILE_REPORT_REF = (
    "research/recovered/STONEAGE-25-STABLE-NPC-TEMPLATE-PROFILES-R1.txt"
)
SEMANTIC_SOURCE_VERSION = "recovered25"

GRAPHIC_RESOLUTIONS = {"DEFAULT_ZERO", "NUMERIC", "OPAQUE_SYMBOL"}
TYPE_RESOLUTIONS = {"DEFAULT_SPR_PET001", "NUMERIC", "OPAQUE_SYMBOL"}


def _sha256(value: str, label: str) -> str:
    value = str(value).lower()
    if len(value) != 64 or any(
        char not in "0123456789abcdef" for char in value
    ):
        raise ValueError(f"{label} must be 64 hex digits")
    return value


def _pair(value: str, label: str) -> tuple[int, int]:
    parts = str(value).split(",")
    if len(parts) != 2:
        raise ValueError(f"{label} requires min,max")
    lo, hi = (int(parts[0]), int(parts[1]))
    if lo > hi:
        raise ValueError(f"{label} is not normalized")
    return lo, hi


def _optional_int(value: str) -> int | None:
    return None if value == "" else int(value)


def _optional_sha(value: str, label: str) -> str | None:
    return None if value == "" else _sha256(value, label)


def _fields(line: str, prefix: str) -> dict[str, str]:
    parts = line.split("|")
    if not parts or parts[0] != prefix:
        raise ValueError(f"expected {prefix} record")
    out = {}
    for part in parts[1:]:
        if "=" not in part:
            raise ValueError(f"malformed {prefix} field: {part}")
        key, value = part.split("=", 1)
        if not key or key in out:
            raise ValueError(f"duplicate/blank {prefix} field: {key}")
        out[key] = value
    return out


@dataclass(frozen=True)
class AnonymousNpcTemplateRuntimeProfile:
    template_key: str
    variant_fingerprint: str
    functionset: str
    make_at_nobody: int
    make_at_no_see: int
    graphic_resolution: str
    graphic_value: int | None
    graphic_token_key: str | None
    type_resolution: str
    type_value: int | None
    type_token_key: str | None
    hp_range: tuple[int, int]
    mp_range: tuple[int, int]
    strength_range: tuple[int, int]
    toughness_range: tuple[int, int]
    flying: int
    loop_interval: int
    direct_override_count: int
    source_version: str = SEMANTIC_SOURCE_VERSION
    evidence_role: str = LATER_RECOVERED

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "template_key", _sha256(self.template_key, "template key")
        )
        object.__setattr__(
            self,
            "variant_fingerprint",
            _sha256(self.variant_fingerprint, "variant fingerprint"),
        )
        if self.graphic_resolution not in GRAPHIC_RESOLUTIONS:
            raise ValueError("unknown graphic resolution")
        if self.type_resolution not in TYPE_RESOLUTIONS:
            raise ValueError("unknown type resolution")
        for name in (
            "make_at_nobody",
            "make_at_no_see",
            "flying",
            "loop_interval",
            "direct_override_count",
        ):
            object.__setattr__(self, name, int(getattr(self, name)))
        if self.direct_override_count < 0:
            raise ValueError("direct override count cannot be negative")
        for name in (
            "hp_range",
            "mp_range",
            "strength_range",
            "toughness_range",
        ):
            pair = tuple(int(value) for value in getattr(self, name))
            if len(pair) != 2 or pair[0] > pair[1]:
                raise ValueError(f"{name} is invalid")
            object.__setattr__(self, name, pair)
        if self.graphic_resolution == "NUMERIC":
            if self.graphic_value is None or self.graphic_token_key is not None:
                raise ValueError("numeric graphic requires value only")
        elif self.graphic_resolution == "OPAQUE_SYMBOL":
            if self.graphic_value is not None or self.graphic_token_key is None:
                raise ValueError("opaque graphic requires token hash only")
        elif self.graphic_value is not None or self.graphic_token_key is not None:
            raise ValueError("default graphic cannot carry explicit token/value")

        if self.type_resolution == "NUMERIC":
            if self.type_value is None or self.type_token_key is not None:
                raise ValueError("numeric type requires value only")
        elif self.type_resolution == "OPAQUE_SYMBOL":
            if self.type_value is not None or self.type_token_key is None:
                raise ValueError("opaque type requires token hash only")
        elif self.type_value is not None or self.type_token_key is not None:
            raise ValueError("default type cannot carry explicit token/value")

        if self.evidence_role != LATER_RECOVERED:
            raise ValueError(
                "recovered NPC template profile must remain LATER_RECOVERED"
            )

    @property
    def has_symbolic_graphic_or_type(self) -> bool:
        return (
            self.graphic_resolution == "OPAQUE_SYMBOL"
            or self.type_resolution == "OPAQUE_SYMBOL"
        )

    @property
    def has_direct_callback_override(self) -> bool:
        return self.direct_override_count > 0


@dataclass(frozen=True)
class VersionedNpcTemplateRuntimeProfiles:
    bindings: VersionedNpcTemplateBindingManifest
    profiles_by_identity: Mapping[
        str, tuple[AnonymousNpcTemplateRuntimeProfile, ...]
    ]
    source_version: str = SEMANTIC_SOURCE_VERSION

    def __post_init__(self) -> None:
        grouped = {
            str(key): tuple(value)
            for key, value in self.profiles_by_identity.items()
        }
        if self.source_version != self.bindings.source_version:
            raise ValueError("NPC template profile source-version drift")
        if set(grouped) != set(self.bindings.identities):
            raise ValueError(
                "NPC template profile identities do not match binding manifest"
            )

        for key, profiles in grouped.items():
            identity = self.bindings.identities[key]
            if len(profiles) != identity.variant_count:
                raise ValueError(
                    f"runtime profile variant count drift for {key}"
                )
            fingerprints = {
                profile.variant_fingerprint for profile in profiles
            }
            if len(fingerprints) != identity.variant_fingerprint_count:
                raise ValueError(
                    f"runtime profile fingerprint count drift for {key}"
                )
            if any(profile.template_key != key for profile in profiles):
                raise ValueError("runtime profile template key drift")
            if any(
                profile.source_version != self.source_version
                for profile in profiles
            ):
                raise ValueError("runtime profile source-version drift")

            functionsets = {profile.functionset for profile in profiles}
            if identity.functionset_is_consensus:
                if functionsets != {identity.functionset_consensus}:
                    raise ValueError(
                        f"runtime profile functionset drift for {key}"
                    )
            else:
                if len(functionsets) != identity.functionset_variant_count:
                    raise ValueError(
                        f"runtime profile functionset-variant drift for {key}"
                    )

        object.__setattr__(
            self, "profiles_by_identity", MappingProxyType(grouped)
        )

    @property
    def profile_variant_count(self) -> int:
        return sum(
            len(profiles)
            for profiles in self.profiles_by_identity.values()
        )

    @property
    def symbolic_profile_variants(
        self,
    ) -> tuple[AnonymousNpcTemplateRuntimeProfile, ...]:
        return tuple(
            profile
            for profiles in self.profiles_by_identity.values()
            for profile in profiles
            if profile.has_symbolic_graphic_or_type
        )

    @property
    def direct_override_profile_variants(
        self,
    ) -> tuple[AnonymousNpcTemplateRuntimeProfile, ...]:
        return tuple(
            profile
            for profiles in self.profiles_by_identity.values()
            for profile in profiles
            if profile.has_direct_callback_override
        )

    def unique_profile_for_placement(
        self, placement_id: int
    ) -> AnonymousNpcTemplateRuntimeProfile:
        binding = self.bindings.by_placement[int(placement_id)]
        if not binding.concrete_template_binding_is_unique:
            raise ValueError(
                f"placement {placement_id} has duplicate template-name variants"
            )
        profiles = self.profiles_by_identity[binding.template_key]
        if len(profiles) != 1:
            raise ValueError("unique binding does not resolve one profile")
        return profiles[0]

    def runtime_equivalent_profile_for_placement(
        self, placement_id: int
    ) -> AnonymousNpcTemplateRuntimeProfile:
        """Return one profile when all duplicate source variants are byte-identical."""
        binding = self.bindings.by_placement[int(placement_id)]
        identity = self.bindings.identities[binding.template_key]
        if not identity.runtime_variants_are_byte_equivalent:
            raise ValueError(
                f"placement {placement_id} has non-equivalent template variants"
            )
        profiles = self.profiles_by_identity[binding.template_key]
        if not profiles:
            raise ValueError("runtime-equivalent binding has no profile")
        fingerprints = {
            profile.variant_fingerprint for profile in profiles
        }
        if len(fingerprints) != 1:
            raise ValueError(
                "byte-equivalent identity unexpectedly has multiple fingerprints"
            )
        first = profiles[0]
        if any(profile != first for profile in profiles[1:]):
            raise ValueError(
                "same template fingerprint produced divergent runtime profiles"
            )
        return first


def parse_versioned_npc_template_profiles(
    *,
    bindings: VersionedNpcTemplateBindingManifest,
    text: str,
) -> VersionedNpcTemplateRuntimeProfiles:
    source_version: str | None = None
    evidence_role: str | None = None
    counts: dict[str, int] = {}
    grouped: dict[str, list[AnonymousNpcTemplateRuntimeProfile]] = {}
    resolution = False

    for raw in str(text).splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("SEMANTIC_SOURCE_VERSION|"):
            if source_version is not None:
                raise ValueError("duplicate template-profile source version")
            source_version = line.split("|", 1)[1]
            continue
        if line.startswith("EVIDENCE_ROLE|"):
            if evidence_role is not None:
                raise ValueError("duplicate template-profile evidence role")
            evidence_role = line.split("|", 1)[1]
            continue
        if line.startswith("COUNT|"):
            parts = line.split("|")
            if len(parts) != 3:
                raise ValueError(f"malformed COUNT row: {line}")
            counts[parts[1]] = int(parts[2])
            continue
        if line.startswith("TEMPLATE_PROFILE|"):
            fields = _fields(line, "TEMPLATE_PROFILE")
            profile = AnonymousNpcTemplateRuntimeProfile(
                template_key=fields["template_key"],
                variant_fingerprint=fields["variant"],
                functionset=fields["functionset"],
                make_at_nobody=int(fields["make_at_nobody"]),
                make_at_no_see=int(fields["make_at_no_see"]),
                graphic_resolution=fields["graphic_resolution"],
                graphic_value=_optional_int(fields["graphic_value"]),
                graphic_token_key=_optional_sha(
                    fields["graphic_token_key"],
                    "graphic token key",
                ),
                type_resolution=fields["type_resolution"],
                type_value=_optional_int(fields["type_value"]),
                type_token_key=_optional_sha(
                    fields["type_token_key"],
                    "type token key",
                ),
                hp_range=_pair(fields["hp"], "hp"),
                mp_range=_pair(fields["mp"], "mp"),
                strength_range=_pair(fields["strength"], "strength"),
                toughness_range=_pair(fields["toughness"], "toughness"),
                flying=int(fields["flying"]),
                loop_interval=int(fields["loop_interval"]),
                direct_override_count=int(fields["direct_overrides"]),
                source_version=source_version or "",
                evidence_role=evidence_role or "",
            )
            grouped.setdefault(profile.template_key, []).append(profile)
            continue
        if line == "RESOLUTION|ANONYMOUS_NPC_TEMPLATE_RUNTIME_PROFILES_CLASSIFIED":
            resolution = True

    if source_version is None:
        raise ValueError("template profile report lacks source version")
    if evidence_role != LATER_RECOVERED:
        raise ValueError(
            "template profile report must remain LATER_RECOVERED"
        )
    if not resolution:
        raise ValueError("template profile report lacks closed resolution")

    actual_variants = sum(len(rows) for rows in grouped.values())
    if (
        "referenced_template_identities" not in counts
        or counts["referenced_template_identities"] != len(grouped)
    ):
        raise ValueError("template profile identity count drift")
    if (
        "runtime_profile_variants" not in counts
        or counts["runtime_profile_variants"] != actual_variants
    ):
        raise ValueError("template profile variant count drift")

    return VersionedNpcTemplateRuntimeProfiles(
        bindings=bindings,
        profiles_by_identity={
            key: tuple(rows) for key, rows in grouped.items()
        },
        source_version=source_version,
    )
