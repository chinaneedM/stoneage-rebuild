#!/usr/bin/env python3
"""Derive anonymous non-text NPC template runtime profiles.

The probe exposes only numeric structural fields and opaque hashes for symbolic
graphic/type tokens. It does not emit template names, NPC display names,
dialogue, callback names, arguments, item payload rows, or original source
rows.
"""

from __future__ import annotations

import argparse
import hashlib
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

from tools.stoneage_npc_world_graph_probe import (
    DIRECT_FUNC_KEYS,
    iter_blocks,
    magic_kind,
)
from tools.stoneage_versioned_npc_template_binding_probe import (
    _block_fingerprint,
    _opaque_name_key,
    _safe_token,
)


SOURCE_VERSION = "recovered25"
EVIDENCE_ROLE = "LATER_RECOVERED"


def _atoi(value: bytes | None, default: int) -> int:
    if value is None:
        return int(default)
    try:
        return int(value.strip(), 10)
    except (ValueError, TypeError):
        return int(default)


def _range(value: bytes | None) -> tuple[int, int]:
    if value is None or not value.strip():
        return (0, 0)
    text = value.decode("ascii", "ignore")
    first, separator, second = text.partition(",")
    try:
        a = int(first.strip() or "0", 10)
    except ValueError:
        a = 0
    if not separator:
        return (a, a)
    try:
        b = int(second.strip() or "0", 10)
    except ValueError:
        b = 0
    return (min(a, b), max(a, b))


def _graphic_token(value: bytes | None, *, missing_default: str):
    if value is None or not value.strip():
        return missing_default, None, None
    token = value.strip()
    try:
        return "NUMERIC", int(token, 10), None
    except ValueError:
        return (
            "OPAQUE_SYMBOL",
            None,
            hashlib.sha256(token.lower()).hexdigest(),
        )


@dataclass(frozen=True)
class TemplateRuntimeProfile:
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
    hp_min: int
    hp_max: int
    mp_min: int
    mp_max: int
    strength_min: int
    strength_max: int
    toughness_min: int
    toughness_max: int
    flying: int
    loop_interval: int
    direct_override_count: int


def _referenced_identity_counts(binding_report: Path) -> dict[str, int]:
    out: dict[str, int] = {}
    for raw in binding_report.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line.startswith("TEMPLATE_IDENTITY|"):
            continue
        fields = dict(
            part.split("=", 1) for part in line.split("|")[1:]
        )
        out[fields["key"]] = int(fields["variants"])
    if not out:
        raise ValueError("template binding report has no identities")
    return out


def analyze(
    *,
    binding_report: Path,
    npc_dir: Path,
) -> tuple[tuple[TemplateRuntimeProfile, ...], Counter]:
    referenced = _referenced_identity_counts(binding_report)
    profiles: list[TemplateRuntimeProfile] = []
    variants_by_key: dict[str, int] = defaultdict(int)
    counts = Counter()

    paths = sorted(
        (
            path for path in npc_dir.rglob("*")
            if path.is_file() and magic_kind(path) == "template"
        ),
        key=lambda path: str(path).lower(),
    )

    for path in paths:
        for entries in iter_blocks(path):
            fields: dict[bytes, bytes] = {}
            direct_overrides = 0
            for key, value in entries:
                if key == b"itm":
                    continue
                fields[key] = value
                if key in DIRECT_FUNC_KEYS and value:
                    direct_overrides += 1

            name = fields.get(b"templatename", b"").strip()
            if not name:
                continue
            template_key = _opaque_name_key(name.lower())
            if template_key not in referenced:
                continue

            graphic_resolution, graphic_value, graphic_token_key = (
                _graphic_token(
                    fields.get(b"graphicname"),
                    missing_default="DEFAULT_ZERO",
                )
            )
            type_resolution, type_value, type_token_key = _graphic_token(
                fields.get(b"type"),
                missing_default="DEFAULT_SPR_PET001",
            )
            hp_min, hp_max = _range(fields.get(b"hp"))
            mp_min, mp_max = _range(fields.get(b"mp"))
            strength_min, strength_max = _range(fields.get(b"str"))
            toughness_min, toughness_max = _range(fields.get(b"tough"))

            profile = TemplateRuntimeProfile(
                template_key=template_key,
                variant_fingerprint=_block_fingerprint(entries),
                functionset=_safe_token(fields.get(b"functionset", b"")),
                make_at_nobody=_atoi(fields.get(b"makeatnobody"), 0),
                make_at_no_see=_atoi(fields.get(b"makeatnosee"), 0),
                graphic_resolution=graphic_resolution,
                graphic_value=graphic_value,
                graphic_token_key=graphic_token_key,
                type_resolution=type_resolution,
                type_value=type_value,
                type_token_key=type_token_key,
                hp_min=hp_min,
                hp_max=hp_max,
                mp_min=mp_min,
                mp_max=mp_max,
                strength_min=strength_min,
                strength_max=strength_max,
                toughness_min=toughness_min,
                toughness_max=toughness_max,
                flying=_atoi(fields.get(b"fly"), 0),
                loop_interval=_atoi(fields.get(b"loopfunctime"), -1),
                direct_override_count=direct_overrides,
            )
            profiles.append(profile)
            variants_by_key[template_key] += 1

            counts[
                f"graphic_resolution:{graphic_resolution}"
            ] += 1
            counts[f"type_resolution:{type_resolution}"] += 1
            counts[
                f"direct_override_count:{direct_overrides}"
            ] += 1
            if profile.flying:
                counts["profiles_flying_nonzero"] += 1
            if profile.make_at_nobody:
                counts["profiles_make_at_nobody_nonzero"] += 1
            if profile.make_at_no_see:
                counts["profiles_make_at_no_see_nonzero"] += 1

    if set(variants_by_key) != set(referenced):
        missing = sorted(set(referenced) - set(variants_by_key))
        extra = sorted(set(variants_by_key) - set(referenced))
        raise ValueError(
            "runtime profiles do not cover referenced identities; "
            f"missing={missing}, extra={extra}"
        )
    for key, expected in referenced.items():
        if variants_by_key[key] != expected:
            raise ValueError(
                f"runtime profile variant-count drift for {key}: "
                f"expected={expected}, actual={variants_by_key[key]}"
            )

    counts["referenced_template_identities"] = len(referenced)
    counts["runtime_profile_variants"] = len(profiles)
    counts["identities_with_multiple_variants"] = sum(
        1 for count in variants_by_key.values() if count > 1
    )
    return tuple(profiles), counts


def emit(
    profiles: tuple[TemplateRuntimeProfile, ...],
    counts: Counter,
) -> None:
    print("StoneAge stable-world anonymous NPC template runtime profiles — R1")
    print(
        "SCOPE|derived-nontext-template-runtime-structure|"
        "no-template-names|no-npc-names|no-dialogue|no-callback-names|"
        "no-arguments|no-item-payload|no-original-rows"
    )
    print(f"SEMANTIC_SOURCE_VERSION|{SOURCE_VERSION}")
    print(f"EVIDENCE_ROLE|{EVIDENCE_ROLE}")
    print(
        "RULE|numeric graphic/type tokens are preserved as integers; "
        "symbolic tokens remain opaque SHA-256 identities in R1"
    )
    for key in sorted(counts):
        print(f"COUNT|{key}|{counts[key]}")

    for profile in sorted(
        profiles,
        key=lambda row: (row.template_key, row.variant_fingerprint),
    ):
        print(
            "TEMPLATE_PROFILE|"
            f"template_key={profile.template_key}|"
            f"variant={profile.variant_fingerprint}|"
            f"functionset={profile.functionset}|"
            f"make_at_nobody={profile.make_at_nobody}|"
            f"make_at_no_see={profile.make_at_no_see}|"
            f"graphic_resolution={profile.graphic_resolution}|"
            f"graphic_value={'' if profile.graphic_value is None else profile.graphic_value}|"
            f"graphic_token_key={profile.graphic_token_key or ''}|"
            f"type_resolution={profile.type_resolution}|"
            f"type_value={'' if profile.type_value is None else profile.type_value}|"
            f"type_token_key={profile.type_token_key or ''}|"
            f"hp={profile.hp_min},{profile.hp_max}|"
            f"mp={profile.mp_min},{profile.mp_max}|"
            f"strength={profile.strength_min},{profile.strength_max}|"
            f"toughness={profile.toughness_min},{profile.toughness_max}|"
            f"flying={profile.flying}|"
            f"loop_interval={profile.loop_interval}|"
            f"direct_overrides={profile.direct_override_count}"
        )

    print("RESOLUTION|ANONYMOUS_NPC_TEMPLATE_RUNTIME_PROFILES_CLASSIFIED")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--binding-report", type=Path, required=True)
    parser.add_argument("--npc-dir", type=Path, required=True)
    args = parser.parse_args()

    profiles, counts = analyze(
        binding_report=args.binding_report,
        npc_dir=args.npc_dir,
    )
    emit(profiles, counts)


if __name__ == "__main__":
    main()
