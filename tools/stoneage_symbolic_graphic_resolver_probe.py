#!/usr/bin/env python3
"""Audit anonymous recovered NPC graphic/type symbols across fixed sources.

Promotion policy is intentionally conservative:
1. the anonymous token must exist in all three pinned descendant anim_tbl.h
   source families;
2. all three must map it to the same integer graphic ID;
3. that ID must exist in the accepted Taiwan-v1 SPR group metadata.

The report never emits the source token spelling.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


GAVIN_REF = "gavinlinasd/StoneAge@1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56"
IRISELIA_REF = "iriselia/StoneAge@9e6c8ce2cd8ed532a7157773acd1c61582c178b5"
BISMARCK_REF = "BismarckDD/Stoneage@2f736808ff4361f5429ee919b718c88fabb60346"
SOURCE_ORDER = ("gavin", "iriselia", "bismarck")

PROMOTED = "PROMOTED_DESCENDANT_CONSENSUS_V1_RESOURCE"
CONSENSUS_V1_MISSING = "DESCENDANT_CONSENSUS_V1_RESOURCE_MISSING"
SOURCE_CONFLICT = "SOURCE_MAPPING_CONFLICT"
SOURCE_INCOMPLETE = "SOURCE_MAPPING_INCOMPLETE"
SOURCE_ABSENT = "SOURCE_MAPPING_ABSENT"


_DEFINE_RE = re.compile(
    r"^\s*#\s*define\s+([A-Za-z_][A-Za-z0-9_]*)\s+"
    r"(-?(?:0[xX][0-9A-Fa-f]+|[0-9]+))(?:\s|/|$)"
)


def token_key(token: str) -> str:
    return hashlib.sha256(str(token).strip().lower().encode("ascii")).hexdigest()


def parse_anim_tbl(path: Path) -> dict[str, int]:
    """Return anonymous token SHA -> numeric #define value."""
    result: dict[str, int] = {}
    conflicts: set[str] = set()
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        match = _DEFINE_RE.match(raw)
        if not match:
            continue
        name, value_text = match.groups()
        value = int(value_text, 0)
        key = token_key(name)
        if key in result and result[key] != value:
            conflicts.add(key)
        else:
            result[key] = value
    for key in conflicts:
        result.pop(key, None)
    return result


def parse_v1_spr_ids(path: Path) -> set[int]:
    values: set[int] = set()
    with gzip.open(path, "rt", encoding="utf-8", newline="") as handle:
        header = handle.readline().rstrip("\n").split("\t")
        try:
            spr_col = header.index("spr_no")
        except ValueError as exc:
            raise ValueError("SPR group metadata lacks spr_no column") from exc
        for raw in handle:
            parts = raw.rstrip("\n").split("\t")
            if len(parts) <= spr_col:
                raise ValueError("malformed SPR group metadata row")
            values.add(int(parts[spr_col]))
    if not values:
        raise ValueError("Taiwan-v1 SPR group metadata is empty")
    return values


def _fields(line: str, prefix: str) -> dict[str, str]:
    parts = line.split("|")
    if not parts or parts[0] != prefix:
        raise ValueError(f"expected {prefix} record")
    return dict(part.split("=", 1) for part in parts[1:])


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


@dataclass(frozen=True)
class TokenAudit:
    use: TokenUse
    source_values: tuple[int | None, int | None, int | None]
    consensus_value: int | None
    v1_resource_present: bool
    status: str

    @property
    def promoted_value(self) -> int | None:
        return self.consensus_value if self.status == PROMOTED else None


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
        fields = _fields(line, "TEMPLATE_PROFILE")
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

    # Runtime-equivalent duplicate definitions must not introduce multiple
    # anonymous token choices for one template identity.
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
        fields = _fields(line, "PLACEMENT_TEMPLATE")
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


def classify_token(
    *,
    use: TokenUse,
    source_maps: dict[str, dict[str, int]],
    v1_spr_ids: set[int],
) -> TokenAudit:
    values = tuple(
        source_maps[name].get(use.token_key) for name in SOURCE_ORDER
    )
    present = [value for value in values if value is not None]
    consensus = None
    if len(present) == 3 and len(set(present)) == 1:
        consensus = present[0]
        in_v1 = consensus in v1_spr_ids
        status = PROMOTED if in_v1 else CONSENSUS_V1_MISSING
    elif not present:
        in_v1 = False
        status = SOURCE_ABSENT
    elif len(set(present)) > 1:
        in_v1 = False
        status = SOURCE_CONFLICT
    else:
        in_v1 = False
        status = SOURCE_INCOMPLETE
    return TokenAudit(
        use=use,
        source_values=values,
        consensus_value=consensus,
        v1_resource_present=in_v1,
        status=status,
    )


def analyze(
    *,
    profile_report: Path,
    binding_report: Path,
    gavin_anim: Path,
    iriselia_anim: Path,
    bismarck_anim: Path,
    tw10_spr_groups: Path,
) -> tuple[tuple[TokenAudit, ...], Counter]:
    uses = parse_opaque_uses(
        profile_report=profile_report,
        binding_report=binding_report,
    )
    source_maps = {
        "gavin": parse_anim_tbl(gavin_anim),
        "iriselia": parse_anim_tbl(iriselia_anim),
        "bismarck": parse_anim_tbl(bismarck_anim),
    }
    v1_ids = parse_v1_spr_ids(tw10_spr_groups)
    audits = tuple(
        classify_token(
            use=uses[key],
            source_maps=source_maps,
            v1_spr_ids=v1_ids,
        )
        for key in sorted(uses)
    )

    counts = Counter()
    counts["opaque_token_identities"] = len(audits)
    counts["opaque_graphic_token_identities"] = sum(
        bool(row.use.graphic_identity_count) for row in audits
    )
    counts["opaque_type_token_identities"] = sum(
        bool(row.use.type_identity_count) for row in audits
    )
    for row in audits:
        counts[f"status:{row.status}"] += 1
        counts["graphic_placements_total"] += row.use.graphic_placement_count
        counts["type_placements_total"] += row.use.type_placement_count
        if row.status == PROMOTED:
            counts["graphic_placements_promoted"] += (
                row.use.graphic_placement_count
            )
            counts["type_placements_promoted"] += row.use.type_placement_count
    return audits, counts


def emit(audits: tuple[TokenAudit, ...], counts: Counter) -> None:
    print("StoneAge anonymous symbolic graphic/type resolver audit — R1")
    print(
        "SCOPE|anonymous-token-hashes+numeric-mappings-only|"
        "no-token-spellings|no-proprietary-resource-payload"
    )
    print(f"SOURCE_REF|gavin|{GAVIN_REF}")
    print(f"SOURCE_REF|iriselia|{IRISELIA_REF}")
    print(f"SOURCE_REF|bismarck|{BISMARCK_REF}")
    print(
        "PROMOTION_RULE|all-three-fixed-descendants-same-id"
        "+taiwan-v1-spr-id-present"
    )
    for key in sorted(counts):
        print(f"COUNT|{key}|{counts[key]}")

    for row in audits:
        values = row.source_values
        print(
            "TOKEN_RESOLUTION|"
            f"key={row.use.token_key}|"
            f"surfaces={','.join(row.use.surfaces)}|"
            f"graphic_identities={row.use.graphic_identity_count}|"
            f"type_identities={row.use.type_identity_count}|"
            f"graphic_placements={row.use.graphic_placement_count}|"
            f"type_placements={row.use.type_placement_count}|"
            f"gavin={'' if values[0] is None else values[0]}|"
            f"iriselia={'' if values[1] is None else values[1]}|"
            f"bismarck={'' if values[2] is None else values[2]}|"
            f"consensus={'' if row.consensus_value is None else row.consensus_value}|"
            f"v1_spr_present={int(row.v1_resource_present)}|"
            f"status={row.status}"
        )
    print("RESOLUTION|SYMBOLIC_GRAPHIC_TYPE_RESOLVER_AUDITED")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile-report", type=Path, required=True)
    parser.add_argument("--binding-report", type=Path, required=True)
    parser.add_argument("--gavin-anim", type=Path, required=True)
    parser.add_argument("--iriselia-anim", type=Path, required=True)
    parser.add_argument("--bismarck-anim", type=Path, required=True)
    parser.add_argument("--tw10-spr-groups", type=Path, required=True)
    args = parser.parse_args()
    audits, counts = analyze(
        profile_report=args.profile_report,
        binding_report=args.binding_report,
        gavin_anim=args.gavin_anim,
        iriselia_anim=args.iriselia_anim,
        bismarck_anim=args.bismarck_anim,
        tw10_spr_groups=args.tw10_spr_groups,
    )
    emit(audits, counts)


if __name__ == "__main__":
    main()
