#!/usr/bin/env python3
"""Probe recovered runtime ls2data.dat for anonymous graphic/type mappings.

This consumes the verified recovered-2.5 bundle transiently. It never emits
symbol spellings or original mapping rows; only anonymous SHA-256 token keys
and numeric IDs are retained.

A recovered mapping is evidence for the recovered25 runtime namespace only.
Presence of the mapped numeric ID in Taiwan-v1 SPR metadata is a separate
resource-compatibility fact and is not historical token-name membership proof.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class TokenUse:
    token_key: str
    graphic_identity_count: int
    type_identity_count: int
    graphic_placement_count: int
    type_placement_count: int

    @property
    def surfaces(self) -> tuple[str, ...]:
        out = []
        if self.graphic_identity_count:
            out.append("graphic")
        if self.type_identity_count:
            out.append("type")
        return tuple(out)


def _report_fields(line: str, prefix: str) -> dict[str, str]:
    parts = line.split("|")
    if not parts or parts[0] != prefix:
        raise ValueError(f"expected {prefix} record")
    out = {}
    for part in parts[1:]:
        if "=" not in part:
            raise ValueError(f"malformed {prefix} field: {part}")
        key, value = part.split("=", 1)
        out[key] = value
    return out


def parse_opaque_uses(
    *,
    profile_report: Path,
    binding_report: Path,
) -> dict[str, TokenUse]:
    identity_tokens: dict[str, dict[str, set[str]]] = defaultdict(
        lambda: {"graphic": set(), "type": set()}
    )
    for raw in profile_report.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line.startswith("TEMPLATE_PROFILE|"):
            continue
        fields = _report_fields(line, "TEMPLATE_PROFILE")
        template_key = fields["template_key"]
        if fields["graphic_resolution"] == "OPAQUE_SYMBOL":
            key = fields["graphic_token_key"]
            if not key:
                raise ValueError("opaque graphic profile lacks token key")
            identity_tokens[template_key]["graphic"].add(key)
        if fields["type_resolution"] == "OPAQUE_SYMBOL":
            key = fields["type_token_key"]
            if not key:
                raise ValueError("opaque type profile lacks token key")
            identity_tokens[template_key]["type"].add(key)

    for template_key, surfaces in identity_tokens.items():
        for surface, keys in surfaces.items():
            if len(keys) > 1:
                raise ValueError(
                    f"template {template_key} has multiple opaque {surface} tokens"
                )

    placement_counts = Counter()
    for raw in binding_report.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line.startswith("PLACEMENT_TEMPLATE|"):
            continue
        fields = _report_fields(line, "PLACEMENT_TEMPLATE")
        placement_counts[fields["template_key"]] += 1

    aggregate: dict[str, dict[str, int]] = defaultdict(
        lambda: {
            "graphic_identity_count": 0,
            "type_identity_count": 0,
            "graphic_placement_count": 0,
            "type_placement_count": 0,
        }
    )
    for template_key, surfaces in identity_tokens.items():
        placements = int(placement_counts[template_key])
        for surface in ("graphic", "type"):
            keys = surfaces[surface]
            if not keys:
                continue
            key = next(iter(keys))
            aggregate[key][f"{surface}_identity_count"] += 1
            aggregate[key][f"{surface}_placement_count"] += placements

    return {
        key: TokenUse(token_key=key, **values)
        for key, values in aggregate.items()
    }


def parse_v1_spr_ids(path: Path) -> set[int]:
    values: set[int] = set()
    with gzip.open(path, "rt", encoding="utf-8", newline="") as handle:
        header = handle.readline().rstrip("\n").split("\t")
        if "spr_no" not in header:
            raise ValueError("SPR group metadata lacks spr_no column")
        column = header.index("spr_no")
        for raw in handle:
            parts = raw.rstrip("\n").split("\t")
            if len(parts) <= column:
                raise ValueError("malformed SPR group metadata row")
            values.add(int(parts[column]))
    if not values:
        raise ValueError("Taiwan-v1 SPR group metadata is empty")
    return values


RECOVERED25_V1_RESOURCE = "RECOVERED25_MAPPING_V1_RESOURCE_COMPATIBLE"
RECOVERED25_V1_MISSING = "RECOVERED25_MAPPING_V1_RESOURCE_MISSING"
RECOVERED25_CONFLICT = "RECOVERED25_MAPPING_CONFLICT"
RECOVERED25_ABSENT = "RECOVERED25_MAPPING_ABSENT"


def _bytes_token_key(value: bytes) -> str:
    return hashlib.sha256(value.strip().lower()).hexdigest()


@dataclass(frozen=True)
class RuntimeMappingFile:
    path: Path
    declared_count: int
    mapping: dict[str, int]
    anonymous_mapping_sha256: str


@dataclass(frozen=True)
class RuntimeTokenAudit:
    use: TokenUse
    recovered_values: tuple[int, ...]
    consensus_value: int | None
    v1_resource_present: bool
    status: str

    @property
    def runtime_resolved_value(self) -> int | None:
        if self.status in {RECOVERED25_V1_RESOURCE, RECOVERED25_V1_MISSING}:
            return self.consensus_value
        return None


def parse_runtime_ls2data(path: Path) -> RuntimeMappingFile | None:
    """Parse count + 'token integer' runtime mapping files.

    Header stubs/C source fragments are ignored by returning None.
    """
    raw_lines = path.read_bytes().splitlines()
    lines = [line.strip() for line in raw_lines if line.strip()]
    if not lines:
        return None
    try:
        declared = int(lines[0], 10)
    except ValueError:
        return None
    if declared < 0 or len(lines) < declared + 1:
        return None

    mapping: dict[str, int] = {}
    conflicts: set[str] = set()
    canonical_rows: list[tuple[str, int]] = []
    for raw in lines[1 : declared + 1]:
        parts = raw.split()
        if len(parts) < 2:
            return None
        token = parts[0]
        try:
            value = int(parts[1], 10)
        except ValueError:
            return None
        key = _bytes_token_key(token)
        if key in mapping and mapping[key] != value:
            conflicts.add(key)
        else:
            mapping[key] = value
        canonical_rows.append((key, value))

    for key in conflicts:
        mapping.pop(key, None)

    digest = hashlib.sha256()
    for key, value in sorted(canonical_rows):
        digest.update(f"{key}|{value}\n".encode("ascii"))
    return RuntimeMappingFile(
        path=path,
        declared_count=declared,
        mapping=mapping,
        anonymous_mapping_sha256=digest.hexdigest(),
    )


def collect_runtime_mapping_files(root: Path) -> tuple[RuntimeMappingFile, ...]:
    out = []
    for path in sorted(
        (
            p for p in root.rglob("*")
            if p.is_file() and p.name.lower() == "ls2data.dat"
        ),
        key=lambda p: str(p).lower(),
    ):
        parsed = parse_runtime_ls2data(path)
        if parsed is not None:
            out.append(parsed)
    return tuple(out)


def classify(
    *,
    use: TokenUse,
    mapping_files: tuple[RuntimeMappingFile, ...],
    v1_spr_ids: set[int],
) -> RuntimeTokenAudit:
    values = sorted({
        file.mapping[use.token_key]
        for file in mapping_files
        if use.token_key in file.mapping
    })
    if not values:
        consensus = None
        present = False
        status = RECOVERED25_ABSENT
    elif len(values) > 1:
        consensus = None
        present = False
        status = RECOVERED25_CONFLICT
    else:
        consensus = values[0]
        present = consensus in v1_spr_ids
        status = (
            RECOVERED25_V1_RESOURCE
            if present
            else RECOVERED25_V1_MISSING
        )
    return RuntimeTokenAudit(
        use=use,
        recovered_values=tuple(values),
        consensus_value=consensus,
        v1_resource_present=present,
        status=status,
    )


def analyze(
    *,
    profile_report: Path,
    binding_report: Path,
    recovered_root: Path,
    tw10_spr_groups: Path,
) -> tuple[
    tuple[RuntimeMappingFile, ...],
    tuple[RuntimeTokenAudit, ...],
    Counter,
]:
    uses = parse_opaque_uses(
        profile_report=profile_report,
        binding_report=binding_report,
    )
    files = collect_runtime_mapping_files(recovered_root)
    v1_ids = parse_v1_spr_ids(tw10_spr_groups)
    audits = tuple(
        classify(
            use=uses[key],
            mapping_files=files,
            v1_spr_ids=v1_ids,
        )
        for key in sorted(uses)
    )
    counts = Counter()
    counts["runtime_mapping_files"] = len(files)
    counts["opaque_token_identities"] = len(audits)
    for row in audits:
        counts[f"status:{row.status}"] += 1
        counts["graphic_placements_total"] += row.use.graphic_placement_count
        counts["type_placements_total"] += row.use.type_placement_count
        if row.runtime_resolved_value is not None:
            counts["graphic_placements_runtime_resolved"] += (
                row.use.graphic_placement_count
            )
            counts["type_placements_runtime_resolved"] += (
                row.use.type_placement_count
            )
            if row.v1_resource_present:
                counts["graphic_placements_v1_resource_compatible"] += (
                    row.use.graphic_placement_count
                )
                counts["type_placements_v1_resource_compatible"] += (
                    row.use.type_placement_count
                )
    return files, audits, counts


def emit(
    files: tuple[RuntimeMappingFile, ...],
    audits: tuple[RuntimeTokenAudit, ...],
    counts: Counter,
    *,
    recovered_root: Path,
) -> None:
    print("StoneAge recovered-2.5 anonymous runtime graphic mapping audit — R1")
    print(
        "SCOPE|derived-runtime-mapping-only|no-token-spellings|"
        "no-original-ls2data-rows|no-proprietary-resource-payload"
    )
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print(
        "RULE|recovered ls2data mapping proves recovered25 runtime namespace; "
        "taiwan-v1 SPR presence is resource compatibility only"
    )
    for key in sorted(counts):
        print(f"COUNT|{key}|{counts[key]}")
    for index, file in enumerate(files):
        try:
            rel = file.path.relative_to(recovered_root)
            depth = len(rel.parts)
        except ValueError:
            depth = -1
        print(
            "MAPPING_FILE|"
            f"index={index}|declared={file.declared_count}|"
            f"anonymous_sha256={file.anonymous_mapping_sha256}|"
            f"relative_depth={depth}"
        )
    for row in audits:
        print(
            "TOKEN_RUNTIME_RESOLUTION|"
            f"key={row.use.token_key}|"
            f"surfaces={','.join(row.use.surfaces)}|"
            f"graphic_placements={row.use.graphic_placement_count}|"
            f"type_placements={row.use.type_placement_count}|"
            f"candidate_values={','.join(map(str,row.recovered_values))}|"
            f"consensus={'' if row.consensus_value is None else row.consensus_value}|"
            f"v1_spr_present={int(row.v1_resource_present)}|"
            f"status={row.status}"
        )
    print("RESOLUTION|RECOVERED25_RUNTIME_GRAPHIC_MAPPING_AUDITED")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile-report", type=Path, required=True)
    parser.add_argument("--binding-report", type=Path, required=True)
    parser.add_argument("--recovered-root", type=Path, required=True)
    parser.add_argument("--tw10-spr-groups", type=Path, required=True)
    args = parser.parse_args()
    files, audits, counts = analyze(
        profile_report=args.profile_report,
        binding_report=args.binding_report,
        recovered_root=args.recovered_root,
        tw10_spr_groups=args.tw10_spr_groups,
    )
    emit(
        files,
        audits,
        counts,
        recovered_root=args.recovered_root,
    )


if __name__ == "__main__":
    main()
