#!/usr/bin/env python3
"""Versioned recovered25 NPC initial overability profile.

This parser turns the committed multi-lineage audit report into a runtime-safe
manifest. It keeps evidence class explicit and resolves only initial
CHAR_ISOVERED state. Dynamic behavior must update the live occupancy registry
through explicit runtime events if future evidence introduces mutations.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Mapping

from tools.stoneage_singleplayer_world import LATER_RECOVERED


SEMANTIC_SOURCE_VERSION = "recovered25"
OVERABILITY_REPORT_REF = (
    Path(__file__).resolve().parents[1]
    / "research"
    / "recovered"
    / "STONEAGE-25-NPC-OVERABILITY-LINEAGE-R1.txt"
)

STATIC_BLOCKING = "STATIC_BLOCKING"
STATIC_OVERABLE = "STATIC_OVERABLE"
INHERITED_DEFAULT_OVERABLE = "INHERITED_DEFAULT_OVERABLE"
DYNAMIC = "DYNAMIC"
UNRESOLVED = "UNRESOLVED"
LINEAGE_DIVERGENT = "LINEAGE_DIVERGENT"

_SUPPORTED_INITIAL = {
    STATIC_BLOCKING,
    STATIC_OVERABLE,
    INHERITED_DEFAULT_OVERABLE,
}


@dataclass(frozen=True)
class VersionedNpcOverabilityRule:
    functionset: str
    placement_count: int
    classification: str
    initial_overable: bool | None
    provenance: str

    def __post_init__(self) -> None:
        functionset = str(self.functionset)
        classification = str(self.classification)
        placement_count = int(self.placement_count)
        provenance = str(self.provenance).strip()
        if not functionset:
            raise ValueError("NPC overability functionset must be non-empty")
        if placement_count < 1:
            raise ValueError("NPC overability placement_count must be positive")
        if classification not in {
            STATIC_BLOCKING,
            STATIC_OVERABLE,
            INHERITED_DEFAULT_OVERABLE,
            DYNAMIC,
            UNRESOLVED,
            LINEAGE_DIVERGENT,
        }:
            raise ValueError(
                f"unsupported NPC overability classification: {classification}"
            )
        if classification in _SUPPORTED_INITIAL:
            if self.initial_overable is None:
                raise ValueError(
                    "closed NPC overability rule requires initial value"
                )
        elif self.initial_overable is not None:
            raise ValueError(
                "open/dynamic NPC overability rule cannot claim one initial value"
            )
        if not provenance:
            raise ValueError("NPC overability provenance must be non-empty")

        object.__setattr__(self, "functionset", functionset)
        object.__setattr__(self, "placement_count", placement_count)
        object.__setattr__(self, "classification", classification)
        if self.initial_overable is not None:
            object.__setattr__(
                self, "initial_overable", bool(self.initial_overable)
            )
        object.__setattr__(self, "provenance", provenance)

    @property
    def initial_state_closed(self) -> bool:
        return self.initial_overable is not None


@dataclass(frozen=True)
class VersionedNpcOverabilityProfile:
    rules: Mapping[str, VersionedNpcOverabilityRule]
    source_version: str
    evidence_role: str
    total_placements: int
    default_char_isovered: int
    template_direct_callback_overrides: int

    def __post_init__(self) -> None:
        rules = {str(k): v for k, v in self.rules.items()}
        if self.source_version != SEMANTIC_SOURCE_VERSION:
            raise ValueError("NPC overability source-version drift")
        if "PINNED_STABLE_DESCENDANT" not in self.evidence_role:
            raise ValueError("NPC overability evidence role is not descendant-pinned")
        if int(self.default_char_isovered) != 1:
            raise ValueError("NPC default CHAR_ISOVERED is not closed to 1")
        if int(self.template_direct_callback_overrides) != 0:
            raise ValueError("NPC template direct callback overrides are not closed")
        if int(self.total_placements) != sum(
            rule.placement_count for rule in rules.values()
        ):
            raise ValueError("NPC overability placement total drift")
        if not rules:
            raise ValueError("NPC overability profile contains no rules")
        object.__setattr__(self, "rules", MappingProxyType(rules))
        object.__setattr__(self, "total_placements", int(self.total_placements))
        object.__setattr__(
            self, "default_char_isovered", int(self.default_char_isovered)
        )
        object.__setattr__(
            self,
            "template_direct_callback_overrides",
            int(self.template_direct_callback_overrides),
        )

    @property
    def unresolved_rules(self) -> tuple[VersionedNpcOverabilityRule, ...]:
        return tuple(
            rule for rule in self.rules.values()
            if not rule.initial_state_closed
        )

    @property
    def closed_placement_count(self) -> int:
        return sum(
            rule.placement_count
            for rule in self.rules.values()
            if rule.initial_state_closed
        )

    def rule_for_functionset(self, functionset: str) -> VersionedNpcOverabilityRule:
        key = str(functionset)
        if key not in self.rules:
            raise KeyError(f"NPC overability rule not found: {key}")
        return self.rules[key]

    def initial_overable_for_functionset(self, functionset: str) -> bool:
        rule = self.rule_for_functionset(functionset)
        if rule.initial_overable is None:
            raise ValueError(
                f"NPC overability initial state is not closed for "
                f"{rule.functionset}: {rule.classification}"
            )
        return bool(rule.initial_overable)


def _fields(line: str, prefix: str) -> dict[str, str]:
    parts = line.split("|")
    if not parts or parts[0] != prefix:
        raise ValueError(f"expected {prefix} row")
    fields = {}
    for part in parts[1:]:
        if "=" not in part:
            raise ValueError(f"malformed {prefix} field: {part}")
        key, value = part.split("=", 1)
        fields[key] = value
    return fields


def _initial_value(classification: str) -> bool | None:
    if classification == STATIC_BLOCKING:
        return False
    if classification in {STATIC_OVERABLE, INHERITED_DEFAULT_OVERABLE}:
        return True
    return None


def parse_versioned_npc_overability_profile(
    text: str,
) -> VersionedNpcOverabilityProfile:
    source_version = None
    evidence_role = None
    total_placements = None
    default_char_isovered = None
    template_overrides = None
    rules: dict[str, VersionedNpcOverabilityRule] = {}
    resolution = False

    for raw in str(text).splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("SEMANTIC_SOURCE_VERSION|"):
            source_version = line.split("|", 1)[1]
            continue
        if line.startswith("EVIDENCE_ROLE|"):
            evidence_role = line.split("|", 1)[1]
            continue
        if line.startswith("DEFAULT_CHAR_ISOVERED|"):
            fields = _fields(line, "DEFAULT_CHAR_ISOVERED")
            default_char_isovered = int(fields["value"])
            continue
        if line.startswith("TEMPLATE_DIRECT_CALLBACK_OVERRIDES|"):
            fields = _fields(line, "TEMPLATE_DIRECT_CALLBACK_OVERRIDES")
            template_overrides = int(fields["count"])
            continue
        if line.startswith("COUNT|placements|"):
            total_placements = int(line.rsplit("|", 1)[1])
            continue
        if line.startswith("FUNCTIONSET_OVERABILITY|"):
            fields = _fields(line, "FUNCTIONSET_OVERABILITY")
            functionset = fields["functionset"]
            classification = fields["classification"]
            if functionset in rules:
                raise ValueError(
                    f"duplicate NPC overability functionset: {functionset}"
                )
            rules[functionset] = VersionedNpcOverabilityRule(
                functionset=functionset,
                placement_count=int(fields["placements"]),
                classification=classification,
                initial_overable=_initial_value(classification),
                provenance=(
                    f"{SEMANTIC_SOURCE_VERSION}:"
                    f"NPC_OVERABILITY_LINEAGE_R1:{classification}"
                ),
            )
            continue
        if line == "RESOLUTION|RECOVERED25_NPC_OVERABILITY_LINEAGE_AUDITED":
            resolution = True

    if source_version is None:
        raise ValueError("NPC overability report lacks source version")
    if evidence_role is None:
        raise ValueError("NPC overability report lacks evidence role")
    if total_placements is None:
        raise ValueError("NPC overability report lacks placement count")
    if default_char_isovered is None:
        raise ValueError("NPC overability report lacks default flag")
    if template_overrides is None:
        raise ValueError("NPC overability report lacks template override count")
    if not resolution:
        raise ValueError("NPC overability report lacks audited resolution")

    profile = VersionedNpcOverabilityProfile(
        rules=rules,
        source_version=source_version,
        evidence_role=evidence_role,
        total_placements=total_placements,
        default_char_isovered=default_char_isovered,
        template_direct_callback_overrides=template_overrides,
    )
    if profile.unresolved_rules:
        raise ValueError(
            "recovered25 NPC overability report still contains open initial rules"
        )
    return profile


def load_recovered25_npc_overability_profile() -> VersionedNpcOverabilityProfile:
    return parse_versioned_npc_overability_profile(
        OVERABILITY_REPORT_REF.read_text(encoding="utf-8")
    )
