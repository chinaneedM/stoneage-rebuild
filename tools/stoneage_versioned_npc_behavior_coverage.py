#!/usr/bin/env python3
"""Placement-weighted behavior coverage for versioned recovered NPC world.

This registry answers a narrow reconstruction question: for the 3,856
stable-world create placements, is the functionset's generic core already
reconstructed, intentionally no-dispatch, explicitly deferred/versioned, or
unknown?

It does not claim Taiwan-v1 historical membership and does not execute
function-specific secondary content.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


CLOSED_ORDINARY_CORE = "CLOSED_ORDINARY_CORE"
NO_DISPATCH_PROFILE = "NO_DISPATCH_PROFILE"
DEFERRED_VERSIONED_PACKAGE = "DEFERRED_VERSIONED_PACKAGE"
UNCLASSIFIED = "UNCLASSIFIED"

CLOSED_FUNCTIONSETS = frozenset({
    "Warp",
    "WarpMan",
    "TownPeople",
    "SignBoard",
    "Mic",
    "NPCEnemy",
    "ExChangeMan",
    "ItemShop",
    "PetShop",
    "PetSkillShop",
    "PoolItemShop",
    "Healer",
    "WindowHealer",
    "SavePoint",
    "Bankman",
    "Action",
    "Charm",
    "TimeMan",
    "Windowman",
    "Dengon",
    "Quiz",
    "transmigration",
})

DEFERRED_FUNCTIONSETS = frozenset({
    "Familyman",
    "FmDengon",
    "FmHealer",
    "FmLetter",
    "FMPKCallMan",
    "FMPKMan",
    "FMWarpMan",
    "Raceman",
    "Scheduleman",
    "TranserMan",
})

CLOSURE_REFS = {
    "Warp": "STONEAGE-WARP-MAP-TRANSITION-CORE-R1",
    "WarpMan": "STONEAGE-WARP-MAP-TRANSITION-CORE-R1",
    "TownPeople": "STONEAGE-PRESENTATION-NPC-SEMANTICS-R1",
    "SignBoard": "STONEAGE-PRESENTATION-NPC-SEMANTICS-R1",
    "Mic": "STONEAGE-PRESENTATION-NPC-SEMANTICS-R1",
    "NPCEnemy": "STONEAGE-NPCENEMY-CORE-R1",
    "ExChangeMan": "STONEAGE-EXCHANGEMAN-MUTATION-CORE-R1",
    "ItemShop": "STONEAGE-ITEM-SHOP-CORE-R1",
    "PetShop": "STONEAGE-REMAINING-NPC-CORE-TRIAGE-R4",
    "PetSkillShop": "STONEAGE-REMAINING-NPC-CORE-TRIAGE-R4",
    "PoolItemShop": "STONEAGE-REMAINING-NPC-CORE-TRIAGE-R4",
    "Healer": "STONEAGE-HEALER-RECOVERY-CORE-R1",
    "WindowHealer": "STONEAGE-HEALER-RECOVERY-CORE-R1",
    "SavePoint": "STONEAGE-SAVEPOINT-ELDER-RETURN-CORE-R1",
    "Bankman": "STONEAGE-PERSONAL-BANK-PERSISTENCE-R1",
    "Action": "STONEAGE-ACTION-NPC-CORE-R1",
    "Charm": "STONEAGE-CHARM-CORE-R1",
    "TimeMan": "STONEAGE-TIMEMAN-CORE-R1",
    "Windowman": "STONEAGE-WINDOWMAN-CORE-R1",
    "Dengon": "STONEAGE-DENGON-DUELRANKING-PERSISTENCE-BOUNDARY-R1",
    "Quiz": "STONEAGE-QUIZ-CORE-R1",
    "transmigration": "STONEAGE-PLAYER-TRANSMIGRATION-CORE-R1",
}


def _fields(line: str, prefix: str) -> dict[str, str]:
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


@dataclass(frozen=True)
class FunctionsetCoverage:
    functionset: str
    placement_count: int
    category: str
    closure_ref: str | None

    def __post_init__(self) -> None:
        object.__setattr__(self, "placement_count", int(self.placement_count))
        if self.placement_count < 0:
            raise ValueError("placement_count cannot be negative")


@dataclass(frozen=True)
class VersionedNpcBehaviorCoverage:
    rows: tuple[FunctionsetCoverage, ...]
    total_placements: int

    def __post_init__(self) -> None:
        rows = tuple(self.rows)
        total = int(self.total_placements)
        if sum(row.placement_count for row in rows) != total:
            raise ValueError("behavior coverage placement total drift")
        object.__setattr__(self, "rows", rows)
        object.__setattr__(self, "total_placements", total)

    @property
    def category_counts(self) -> dict[str, int]:
        counts = Counter()
        for row in self.rows:
            counts[row.category] += row.placement_count
        return dict(counts)

    @property
    def unknown_functionsets(self) -> tuple[str, ...]:
        return tuple(
            row.functionset
            for row in self.rows
            if row.category == UNCLASSIFIED
        )

    @property
    def ordinary_or_no_dispatch_count(self) -> int:
        counts = self.category_counts
        return (
            counts.get(CLOSED_ORDINARY_CORE, 0)
            + counts.get(NO_DISPATCH_PROFILE, 0)
        )


def _profile_direct_overrides(profile_report: Path) -> dict[str, set[int]]:
    values: dict[str, set[int]] = defaultdict(set)
    for raw in profile_report.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line.startswith("TEMPLATE_PROFILE|"):
            continue
        fields = _fields(line, "TEMPLATE_PROFILE")
        values[fields["template_key"]].add(int(fields["direct_overrides"]))
    return values


def classify_functionset(functionset: str) -> tuple[str, str | None]:
    if functionset in CLOSED_FUNCTIONSETS:
        return CLOSED_ORDINARY_CORE, CLOSURE_REFS[functionset]
    if functionset == "<none>":
        return NO_DISPATCH_PROFILE, None
    if functionset in DEFERRED_FUNCTIONSETS:
        return DEFERRED_VERSIONED_PACKAGE, None
    return UNCLASSIFIED, None


def analyze(
    *,
    binding_report: Path,
    profile_report: Path,
) -> VersionedNpcBehaviorCoverage:
    direct_overrides = _profile_direct_overrides(profile_report)
    counts = Counter()
    none_template_keys = set()

    for raw in binding_report.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line.startswith("PLACEMENT_TEMPLATE|"):
            continue
        fields = _fields(line, "PLACEMENT_TEMPLATE")
        functionset = fields["functionset_consensus"]
        counts[functionset] += 1
        if functionset == "<none>":
            none_template_keys.add(fields["template_key"])

    if not counts:
        raise ValueError("binding report has no placement rows")

    for key in none_template_keys:
        if key not in direct_overrides:
            raise ValueError(
                f"no-functionset template {key} lacks runtime profile"
            )
        if direct_overrides[key] != {0}:
            raise ValueError(
                "no-functionset template has direct callback override; "
                f"template={key}, counts={sorted(direct_overrides[key])}"
            )

    rows = tuple(
        FunctionsetCoverage(
            functionset=functionset,
            placement_count=count,
            category=classify_functionset(functionset)[0],
            closure_ref=classify_functionset(functionset)[1],
        )
        for functionset, count in sorted(
            counts.items(), key=lambda item: (-item[1], item[0])
        )
    )
    return VersionedNpcBehaviorCoverage(
        rows=rows,
        total_placements=sum(counts.values()),
    )


def emit(coverage: VersionedNpcBehaviorCoverage) -> None:
    print("StoneAge stable-world NPC behavior coverage — R1")
    print(
        "SCOPE|placement-weighted-generic-functionset-core-coverage|"
        "no-dialogue|no-arguments|no-historical-membership-promotion"
    )
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print(f"COUNT|total_placements|{coverage.total_placements}")
    for category, count in sorted(coverage.category_counts.items()):
        print(f"COUNT|category:{category}|{count}")
    print(
        "COUNT|ordinary_or_no_dispatch|"
        f"{coverage.ordinary_or_no_dispatch_count}"
    )
    print(f"COUNT|unclassified_functionsets|{len(coverage.unknown_functionsets)}")
    for row in coverage.rows:
        print(
            "FUNCTIONSET_COVERAGE|"
            f"functionset={row.functionset}|"
            f"placements={row.placement_count}|"
            f"category={row.category}|"
            f"closure_ref={row.closure_ref or ''}"
        )
    print("RESOLUTION|VERSIONED_NPC_BEHAVIOR_COVERAGE_CLASSIFIED")


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--binding-report", type=Path, required=True)
    parser.add_argument("--profile-report", type=Path, required=True)
    args = parser.parse_args()
    emit(analyze(
        binding_report=args.binding_report,
        profile_report=args.profile_report,
    ))


if __name__ == "__main__":
    main()
