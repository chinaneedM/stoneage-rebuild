#!/usr/bin/env python3
"""Deterministic arbitration for the recovered floor-130 version fork.

This consumes only two derived reports:
- recovered25 duplicate-floor candidate audit;
- archived2003 -> recovered25 DAT lineage candidate audit.

It deliberately distinguishes temporal alignment from runtime Warp consistency
and refuses to collapse those two independent signals into an automatic winner.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Mapping


RECOVERED25_AUDIT_REF = (
    "research/recovered/STONEAGE-25-FLOOR-130-CANDIDATE-AUDIT-R1.txt"
)
LINEAGE_AUDIT_REF = (
    "research/recovered/"
    "STONEAGE-2003-25-FLOOR-130-CANDIDATE-LINEAGE-R1.txt"
)

ARCHIVED2003_ALIGNED = "ARCHIVED2003_ALIGNED"
RECOVERED25_ALIGNED = "RECOVERED25_ALIGNED"
WARP_RUNTIME_CONSISTENT = "WARP_RUNTIME_CONSISTENT"
WARP_RUNTIME_CONFLICTING = "WARP_RUNTIME_CONFLICTING"

PRESERVE_VERSION_FORK = "PRESERVE_VERSION_FORK"


def _fields(line: str, prefix: str) -> dict[str, str]:
    parts = line.split("|")
    if not parts or parts[0] != prefix:
        raise ValueError(f"expected {prefix} row")
    out: dict[str, str] = {}
    for part in parts[1:]:
        if "=" not in part:
            raise ValueError(f"malformed {prefix} field: {part}")
        key, value = part.split("=", 1)
        if not key or key in out:
            raise ValueError(f"duplicate/blank {prefix} field: {key}")
        out[key] = value
    return out


@dataclass(frozen=True)
class Floor130CandidateArbitration:
    path: str
    sha256: str
    temporal_alignment: str
    warp_consistency: str
    dat_static_exact: bool
    historical_static_exact: bool
    recovered25_static_exact: bool

    def __post_init__(self) -> None:
        if self.temporal_alignment not in {
            ARCHIVED2003_ALIGNED,
            RECOVERED25_ALIGNED,
        }:
            raise ValueError("invalid floor130 temporal alignment")
        if self.warp_consistency not in {
            WARP_RUNTIME_CONSISTENT,
            WARP_RUNTIME_CONFLICTING,
        }:
            raise ValueError("invalid floor130 Warp consistency")


@dataclass(frozen=True)
class Floor130Arbitration:
    floor_id: int
    candidates: tuple[Floor130CandidateArbitration, ...]
    resolution: str = PRESERVE_VERSION_FORK
    selected_path: str | None = None

    def __post_init__(self) -> None:
        if int(self.floor_id) != 130:
            raise ValueError("this arbitration is scoped to floor 130")
        rows = tuple(self.candidates)
        if len(rows) != 2:
            raise ValueError("floor130 arbitration requires exactly two candidates")
        if len({row.path for row in rows}) != 2:
            raise ValueError("duplicate floor130 candidate path")
        if len({row.sha256 for row in rows}) != 2:
            raise ValueError("floor130 candidates must remain byte-divergent")
        if self.resolution != PRESERVE_VERSION_FORK:
            raise ValueError("floor130 arbitration must preserve the version fork")
        if self.selected_path is not None:
            raise ValueError("floor130 version fork cannot select a default payload")
        object.__setattr__(self, "floor_id", 130)
        object.__setattr__(self, "candidates", rows)

    @property
    def by_path(self) -> Mapping[str, Floor130CandidateArbitration]:
        return MappingProxyType({row.path: row for row in self.candidates})


def _parse_recovered25(text: str) -> tuple[dict[str, dict[str, str]], str]:
    floor = None
    rows: dict[str, dict[str, str]] = {}
    resolution = None
    for raw in str(text).splitlines():
        line = raw.strip()
        if line.startswith("FLOOR|"):
            floor = int(line.split("|", 1)[1])
        elif line.startswith("CANDIDATE|"):
            fields = _fields(line, "CANDIDATE")
            rows[fields["path"]] = fields
        elif line.startswith("RESOLUTION|"):
            resolution = line
    if floor != 130:
        raise ValueError("recovered25 candidate audit is not floor 130")
    if len(rows) != 2:
        raise ValueError("recovered25 candidate detail count drift")
    if resolution is None or "selected_path=NONE" not in resolution:
        raise ValueError("recovered25 audit no longer preserves unresolved state")
    return rows, resolution


def _parse_lineage(text: str) -> dict[str, dict[str, str]]:
    floor = None
    rows: dict[str, dict[str, str]] = {}
    resolution = False
    for raw in str(text).splitlines():
        line = raw.strip()
        if line.startswith("FLOOR|"):
            floor = int(line.split("|", 1)[1])
        elif line.startswith("CANDIDATE_LINEAGE|"):
            fields = _fields(line, "CANDIDATE_LINEAGE")
            rows[fields["path"]] = fields
        elif line.startswith("RESOLUTION|DUPLICATE_FLOOR_LINEAGE_COMPARED|"):
            resolution = True
    if floor != 130:
        raise ValueError("lineage candidate audit is not floor 130")
    if len(rows) != 2:
        raise ValueError("lineage candidate detail count drift")
    if not resolution:
        raise ValueError("lineage candidate audit is not closed")
    return rows


def build_floor130_arbitration(
    *,
    recovered25_text: str,
    lineage_text: str,
) -> Floor130Arbitration:
    current, _ = _parse_recovered25(recovered25_text)
    lineage = _parse_lineage(lineage_text)
    if set(current) != set(lineage):
        raise ValueError("floor130 candidate path set drift")

    rows = []
    for path in sorted(current):
        now = current[path]
        history = lineage[path]
        if now["sha256"].lower() != history["sha256"].lower():
            raise ValueError(f"floor130 candidate SHA drift for {path}")

        changed_tile = int(history["changed_tile_cells"])
        changed_parts = int(history["changed_parts_cells"])
        if changed_tile <= 0 or changed_parts <= 0:
            raise ValueError("floor130 DAT lineage must contain real static changes")

        old_all = (
            int(history["changed_tile_match_historical"]) == changed_tile
            and int(history["changed_parts_match_historical"]) == changed_parts
            and int(history["changed_tile_match_recovered25"]) == 0
            and int(history["changed_parts_match_recovered25"]) == 0
            and int(history["changed_tile_match_neither"]) == 0
            and int(history["changed_parts_match_neither"]) == 0
        )
        new_all = (
            int(history["changed_tile_match_recovered25"]) == changed_tile
            and int(history["changed_parts_match_recovered25"]) == changed_parts
            and int(history["changed_tile_match_historical"]) == 0
            and int(history["changed_parts_match_historical"]) == 0
            and int(history["changed_tile_match_neither"]) == 0
            and int(history["changed_parts_match_neither"]) == 0
        )
        if old_all == new_all:
            raise ValueError(
                f"floor130 candidate {path} lacks unique temporal alignment"
            )
        temporal = (
            ARCHIVED2003_ALIGNED if old_all else RECOVERED25_ALIGNED
        )

        incoming_total = (
            int(now["incoming_warp_points_walkable"])
            + int(now["incoming_warp_points_blocked"])
            + int(now["incoming_warp_points_unknown"])
        )
        outgoing_total = (
            int(now["outgoing_warp_source_cells_walkable"])
            + int(now["outgoing_warp_source_cells_blocked"])
            + int(now["outgoing_warp_source_cells_unknown"])
        )
        if incoming_total <= 0 or outgoing_total <= 0:
            raise ValueError("floor130 Warp consistency lacks diagnostic points")

        all_walkable = (
            int(now["incoming_warp_points_walkable"]) == incoming_total
            and int(now["outgoing_warp_source_cells_walkable"]) == outgoing_total
            and int(now["incoming_warp_points_blocked"]) == 0
            and int(now["outgoing_warp_source_cells_blocked"]) == 0
            and int(now["incoming_warp_points_unknown"]) == 0
            and int(now["outgoing_warp_source_cells_unknown"]) == 0
        )
        all_blocked = (
            int(now["incoming_warp_points_blocked"]) == incoming_total
            and int(now["outgoing_warp_source_cells_blocked"]) == outgoing_total
            and int(now["incoming_warp_points_walkable"]) == 0
            and int(now["outgoing_warp_source_cells_walkable"]) == 0
            and int(now["incoming_warp_points_unknown"]) == 0
            and int(now["outgoing_warp_source_cells_unknown"]) == 0
        )
        if not (all_walkable or all_blocked):
            raise ValueError(
                f"floor130 candidate {path} has mixed/unknown Warp consistency"
            )

        rows.append(
            Floor130CandidateArbitration(
                path=path,
                sha256=now["sha256"].lower(),
                temporal_alignment=temporal,
                warp_consistency=(
                    WARP_RUNTIME_CONSISTENT
                    if all_walkable
                    else WARP_RUNTIME_CONFLICTING
                ),
                dat_static_exact=bool(int(now["dat_static_exact"])),
                historical_static_exact=bool(
                    int(history["historical_static_exact"])
                ),
                recovered25_static_exact=bool(
                    int(history["recovered25_static_exact"])
                ),
            )
        )

    alignments = {row.temporal_alignment for row in rows}
    consistencies = {row.warp_consistency for row in rows}
    if alignments != {ARCHIVED2003_ALIGNED, RECOVERED25_ALIGNED}:
        raise ValueError("floor130 temporal fork is no longer two-sided")
    if consistencies != {WARP_RUNTIME_CONSISTENT, WARP_RUNTIME_CONFLICTING}:
        raise ValueError("floor130 Warp consistency fork is no longer two-sided")
    if any(
        row.dat_static_exact
        or row.historical_static_exact
        or row.recovered25_static_exact
        for row in rows
    ):
        raise ValueError("floor130 now has an exact static match; re-arbitrate")

    return Floor130Arbitration(floor_id=130, candidates=tuple(rows))


def load_floor130_arbitration() -> Floor130Arbitration:
    return build_floor130_arbitration(
        recovered25_text=Path(RECOVERED25_AUDIT_REF).read_text(
            encoding="utf-8"
        ),
        lineage_text=Path(LINEAGE_AUDIT_REF).read_text(encoding="utf-8"),
    )
