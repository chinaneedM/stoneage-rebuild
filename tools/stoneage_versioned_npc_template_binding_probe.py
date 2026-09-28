#!/usr/bin/env python3
"""Derive anonymous/versioned NPC template bindings for stable-world placements.

No template names, NPC names, dialogue, arguments, or original rows are
emitted. Template-name namespaces are represented by SHA-256 identity keys.

Duplicate template names remain load-order ambiguous. The probe never chooses a
concrete duplicate definition merely because its local file traversal happens
to encounter that block first.
"""

from __future__ import annotations

import argparse
import hashlib
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

from tools.stoneage_npc_world_graph_probe import (
    collect_server_map_ids,
    iter_blocks,
    magic_kind,
)
from tools.stoneage_world_map_library import parse_stable_later_map_manifest


SOURCE_VERSION = "recovered25"
EVIDENCE_ROLE = "LATER_RECOVERED"


def _opaque_name_key(name: bytes) -> str:
    return hashlib.sha256(name.strip().lower()).hexdigest()


def _block_fingerprint(entries: list[tuple[bytes, bytes]]) -> str:
    digest = hashlib.sha256()
    for key, value in entries:
        digest.update(key.strip().lower())
        digest.update(b"\0")
        digest.update(value)
        digest.update(b"\n")
    return digest.hexdigest()


def _safe_token(value: bytes) -> str:
    if not value:
        return "<none>"
    text = value.decode("ascii", "replace").strip()
    return "".join(
        char if 32 <= ord(char) < 127 and char != "|" else "?"
        for char in text
    ) or "<none>"


@dataclass(frozen=True)
class TemplateVariant:
    name: bytes
    name_key: str
    functionset: str
    fingerprint: str


@dataclass(frozen=True)
class PlacementBinding:
    placement_id: int
    floor_id: int
    template_key: str
    variant_count: int
    functionsets: tuple[str, ...]
    binding_status: str
    classic_warp_geometry: bool

    @property
    def functionset_consensus(self) -> str:
        return (
            self.functionsets[0]
            if len(self.functionsets) == 1
            else "<ambiguous>"
        )


def _templates(npc_dir: Path) -> dict[bytes, tuple[TemplateVariant, ...]]:
    grouped: dict[bytes, list[TemplateVariant]] = defaultdict(list)
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
            for key, value in entries:
                fields[key] = value
            name = fields.get(b"templatename", b"").strip()
            if not name:
                continue
            lower_name = name.lower()
            grouped[lower_name].append(
                TemplateVariant(
                    name=lower_name,
                    name_key=_opaque_name_key(lower_name),
                    functionset=_safe_token(
                        fields.get(b"functionset", b"")
                    ),
                    fingerprint=_block_fingerprint(entries),
                )
            )
    return {
        key: tuple(value)
        for key, value in grouped.items()
    }


def _geometry_placement_rows(text: str) -> dict[int, dict[str, str]]:
    rows: dict[int, dict[str, str]] = {}
    for raw in str(text).splitlines():
        line = raw.strip()
        if not line.startswith("NPC_PLACEMENT|"):
            continue
        fields = {}
        for part in line.split("|")[1:]:
            key, value = part.split("=", 1)
            fields[key] = value
        placement_id = int(fields["placement"])
        if placement_id in rows:
            raise ValueError(
                f"duplicate geometry placement ID {placement_id}"
            )
        rows[placement_id] = fields
    return rows


def analyze(
    *,
    lineage_report: Path,
    geometry_report: Path,
    npc_dir: Path,
    map_dir: Path,
) -> tuple[
    tuple[PlacementBinding, ...],
    dict[str, tuple[TemplateVariant, ...]],
    Counter,
]:
    manifest = parse_stable_later_map_manifest(
        lineage_report.read_text(encoding="utf-8")
    )
    stable_floor_ids = {
        candidate.floor_id for candidate in manifest.candidates
    }
    server_map_ids, _map_files = collect_server_map_ids(map_dir)
    if not server_map_ids:
        raise ValueError("recovered server map set is empty")

    templates = _templates(npc_dir)
    geometry_rows = _geometry_placement_rows(
        geometry_report.read_text(encoding="utf-8")
    )

    create_paths = sorted(
        (
            path for path in npc_dir.rglob("*")
            if path.is_file() and magic_kind(path) == "create"
        ),
        key=lambda path: str(path).lower(),
    )

    bindings: list[PlacementBinding] = []
    placement_id = 0
    referenced: dict[str, tuple[TemplateVariant, ...]] = {}
    counts = Counter()

    for path in create_paths:
        for entries in iter_blocks(path):
            fields: dict[bytes, bytes] = {}
            refs: list[bytes] = []
            for key, value in entries:
                if key == b"enemy":
                    name, _separator, _argument = value.partition(b"|")
                    refs.append(name.strip().lower())
                else:
                    fields[key] = value

            try:
                floor_id = int(fields.get(b"floorid", b"0").strip(), 10)
            except ValueError:
                floor_id = 0
            has_birth = (
                b"borncenter" in fields or b"borncorner" in fields
            )
            if (
                floor_id not in stable_floor_ids
                or floor_id not in server_map_ids
                or not has_birth
            ):
                continue

            resolved = [name for name in refs if name in templates]
            if not resolved:
                continue

            if placement_id not in geometry_rows:
                raise ValueError(
                    f"binding placement {placement_id} absent from geometry"
                )
            geometry = geometry_rows[placement_id]
            if int(geometry["floor"]) != floor_id:
                raise ValueError(
                    f"binding floor drift for placement {placement_id}"
                )
            if int(geometry["resolved_templates"]) != len(resolved):
                raise ValueError(
                    f"resolved template-ref drift for placement {placement_id}"
                )
            if len(resolved) != 1:
                raise ValueError(
                    "R1 anonymous binding requires exactly one resolved "
                    f"template ref; placement={placement_id}, refs={len(resolved)}"
                )

            name = resolved[0]
            variants = templates[name]
            template_key = variants[0].name_key
            if any(v.name_key != template_key for v in variants):
                raise AssertionError("template identity hash drift")
            functionsets = tuple(
                sorted({variant.functionset for variant in variants})
            )
            if len(variants) == 1:
                status = "UNIQUE_NAME"
            elif len(functionsets) == 1:
                status = "DUPLICATE_NAME_SAME_FUNCTIONSET"
            else:
                status = "DUPLICATE_NAME_FUNCTIONSET_AMBIGUOUS"

            classic_warp = bool(
                int(geometry.get("classic_warp_refs", "0"))
            )
            binding = PlacementBinding(
                placement_id=placement_id,
                floor_id=floor_id,
                template_key=template_key,
                variant_count=len(variants),
                functionsets=functionsets,
                binding_status=status,
                classic_warp_geometry=classic_warp,
            )
            bindings.append(binding)
            referenced[template_key] = variants

            counts[f"binding_status:{status}"] += 1
            counts["stable_spawn_placements"] += 1
            if classic_warp:
                counts["classic_warp_geometry_placements"] += 1
                if len(variants) > 1:
                    counts[
                        "classic_warp_duplicate_template_bindings"
                    ] += 1
                if functionsets == ("Warp",):
                    counts[
                        "classic_warp_with_warp_functionset_consensus"
                    ] += 1
                elif "Warp" in functionsets:
                    counts[
                        "classic_warp_with_ambiguous_warp_functionset"
                    ] += 1
                else:
                    counts[
                        "classic_warp_without_warp_functionset_consensus"
                    ] += 1
            placement_id += 1

    if set(geometry_rows) != {
        binding.placement_id for binding in bindings
    }:
        missing = sorted(
            set(geometry_rows)
            - {binding.placement_id for binding in bindings}
        )
        extra = sorted(
            {binding.placement_id for binding in bindings}
            - set(geometry_rows)
        )
        raise ValueError(
            "anonymous template bindings do not cover geometry placements; "
            f"missing={missing}, extra={extra}"
        )

    counts["unique_referenced_template_identities"] = len(referenced)
    counts["duplicate_template_identities_referenced"] = sum(
        1 for variants in referenced.values() if len(variants) > 1
    )
    counts["placements_with_duplicate_template_name"] = sum(
        1 for binding in bindings if binding.variant_count > 1
    )
    counts["placements_with_functionset_ambiguity"] = sum(
        1 for binding in bindings if len(binding.functionsets) > 1
    )

    return tuple(bindings), referenced, counts


def emit(
    bindings: tuple[PlacementBinding, ...],
    referenced: dict[str, tuple[TemplateVariant, ...]],
    counts: Counter,
) -> None:
    print("StoneAge stable-world anonymous NPC template bindings — R1")
    print(
        "SCOPE|derived-anonymous-template-identity-only|"
        "no-template-names|no-npc-names|no-dialogue|no-arguments|"
        "no-original-rows"
    )
    print(f"SEMANTIC_SOURCE_VERSION|{SOURCE_VERSION}")
    print(f"EVIDENCE_ROLE|{EVIDENCE_ROLE}")
    print(
        "RULE|duplicate template-name definitions remain load-order "
        "ambiguous; no concrete duplicate variant is selected"
    )
    for key in sorted(counts):
        print(f"COUNT|{key}|{counts[key]}")

    placement_counts = Counter(
        binding.template_key for binding in bindings
    )
    for template_key in sorted(referenced):
        variants = referenced[template_key]
        functionsets = tuple(
            sorted({variant.functionset for variant in variants})
        )
        consensus = (
            functionsets[0]
            if len(functionsets) == 1
            else "<ambiguous>"
        )
        print(
            "TEMPLATE_IDENTITY|"
            f"key={template_key}|"
            f"variants={len(variants)}|"
            f"variant_fingerprints={len({v.fingerprint for v in variants})}|"
            f"functionset_consensus={consensus}|"
            f"functionset_variants={len(functionsets)}|"
            f"stable_placements={placement_counts[template_key]}"
        )

    for binding in bindings:
        print(
            "PLACEMENT_TEMPLATE|"
            f"placement={binding.placement_id}|"
            f"floor={binding.floor_id}|"
            f"template_key={binding.template_key}|"
            f"variants={binding.variant_count}|"
            f"functionset_consensus={binding.functionset_consensus}|"
            f"functionset_variants={len(binding.functionsets)}|"
            f"status={binding.binding_status}|"
            f"classic_warp_geometry={int(binding.classic_warp_geometry)}"
        )

    print("RESOLUTION|ANONYMOUS_NPC_TEMPLATE_BINDINGS_CLASSIFIED")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lineage-report", type=Path, required=True)
    parser.add_argument("--geometry-report", type=Path, required=True)
    parser.add_argument("--npc-dir", type=Path, required=True)
    parser.add_argument("--map-dir", type=Path, required=True)
    args = parser.parse_args()

    bindings, referenced, counts = analyze(
        lineage_report=args.lineage_report,
        geometry_report=args.geometry_report,
        npc_dir=args.npc_dir,
        map_dir=args.map_dir,
    )
    emit(bindings, referenced, counts)


if __name__ == "__main__":
    main()
