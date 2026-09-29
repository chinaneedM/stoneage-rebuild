#!/usr/bin/env python3
"""Audit source-order semantics for ambiguous recovered classic Warp cells.

Pinned descendant controls establish:
- map objects are appended to each cell's linked-list tail;
- overlap-event dispatch scans from the list head and stops at the first
  matching event object;
- NPC generation scans create indices in ascending order.

Recovered create-file ordering across files is *not* inferred because the
server discovers files through recursive unsorted readdir(). Therefore this
probe can deterministically order competing Warp records only when they reside
in the same create file. Cross-file conflicts remain unresolved.

The report stores only derived path/block/numeric Warp metadata.
"""

from __future__ import annotations

import argparse
import collections
from dataclasses import dataclass
from pathlib import Path

from tools.stoneage_npc_world_graph_probe import iter_blocks, magic_kind
from tools.stoneage_versioned_world_geometry_probe import (
    CLASSIC_WARP_FUNCTIONSET,
    _int,
    _rect_from_fields,
    _template_functionsets,
)
from tools.stoneage_warp_transition_model import parse_legacy_warp_arg


GEOMETRY_RESOLUTION = (
    "RESOLUTION|MATERIALIZABLE_RECOVERED_WORLD_WARP_GEOMETRY_CLOSED"
)
OUTPUT_RESOLUTION = "RESOLUTION|AMBIGUOUS_WARP_CREATE_ORDER_CLASSIFIED"

SAME_FILE_ORDERED = "SAME_FILE_ORDERED"
CROSS_FILE_UNORDERED = "CROSS_FILE_UNORDERED"


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


def _point3(value: str) -> tuple[int, int, int]:
    pieces = str(value).split(",")
    if len(pieces) != 3:
        raise ValueError(f"invalid point triple: {value}")
    return tuple(int(piece) for piece in pieces)  # type: ignore[return-value]


@dataclass(frozen=True)
class GeometryWarp:
    source: tuple[int, int, int]
    placement_id: int
    destination: tuple[int, int, int]
    conditional_time: bool


def parse_ambiguous_geometry(text: str) -> dict[tuple[int, int, int], tuple[GeometryWarp, ...]]:
    by_source: dict[tuple[int, int, int], list[GeometryWarp]] = collections.defaultdict(list)
    resolution = False

    for raw in str(text).splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("MATERIALIZABLE_WARP|"):
            fields = _fields(line, "MATERIALIZABLE_WARP")
            source = _point3(fields["source"])
            by_source[source].append(
                GeometryWarp(
                    source=source,
                    placement_id=int(fields["placement"]),
                    destination=_point3(fields["destination"]),
                    conditional_time=bool(int(fields["conditional_time"])),
                )
            )
            continue
        if line == GEOMETRY_RESOLUTION:
            resolution = True

    if not resolution:
        raise ValueError("materializable Warp geometry is not closed")

    ambiguous = {}
    for source, rows in by_source.items():
        signatures = {(row.destination, row.conditional_time) for row in rows}
        if len(signatures) > 1:
            ambiguous[source] = tuple(rows)
    return ambiguous


@dataclass(frozen=True)
class CreateWarpProvenance:
    placement_id: int
    source: tuple[int, int, int]
    destination: tuple[int, int, int]
    relative_path: str
    block_ordinal: int
    create_num: int
    respawn_time: int


def collect_create_warp_provenance(
    *,
    npc_dir: Path,
    represented_floor_ids: set[int],
) -> dict[int, CreateWarpProvenance]:
    functionsets = _template_functionsets(npc_dir)
    create_paths = sorted(
        (
            path
            for path in npc_dir.rglob("*")
            if path.is_file() and magic_kind(path) == "create"
        ),
        key=lambda path: str(path).lower(),
    )

    by_placement: dict[int, CreateWarpProvenance] = {}
    placement_id = 0

    for path in create_paths:
        block_ordinal = 0
        for entries in iter_blocks(path):
            block_ordinal += 1
            fields: dict[bytes, bytes] = {}
            enemies: list[tuple[bytes, bytes | None]] = []
            for key, value in entries:
                if key == b"enemy":
                    name, separator, arg = value.partition(b"|")
                    enemies.append(
                        (name.strip().lower(), arg if separator else None)
                    )
                else:
                    fields[key] = value

            floor_id = _int(fields.get(b"floorid"), 0)
            birth = _rect_from_fields(
                fields,
                center_key=b"borncenter",
                corner_key=b"borncorner",
            )
            if floor_id not in represented_floor_ids or birth is None:
                continue

            resolved = 0
            classic: list[tuple[int, int, int]] = []
            for template_name, arg in enemies:
                functionset = functionsets.get(template_name)
                if functionset is None:
                    continue
                resolved += 1
                if functionset != CLASSIC_WARP_FUNCTIONSET or arg is None:
                    continue
                parsed = parse_legacy_warp_arg(
                    arg.decode("utf-8", "replace")
                )
                if parsed is None:
                    continue
                classic.append(
                    tuple(int(v) for v in parsed["destination"])
                )

            if resolved <= 0:
                continue

            # Geometry R1 currently has single-cell classic Warp sources only.
            if classic and birth[0] == birth[2] and birth[1] == birth[3]:
                source = (floor_id, birth[0], birth[1])
                # One create placement can theoretically resolve multiple Warp
                # templates. Preserve only geometry rows actually addressable by
                # placement ID; duplicate placement->different destination would
                # itself be ambiguous and is rejected below.
                for destination in classic:
                    if placement_id in by_placement:
                        raise ValueError(
                            "one placement emitted multiple classic Warp "
                            f"destinations: {placement_id}"
                        )
                    by_placement[placement_id] = CreateWarpProvenance(
                        placement_id=placement_id,
                        source=source,
                        destination=destination,
                        relative_path=str(path.relative_to(npc_dir)).replace(
                            "\\", "/"
                        ),
                        block_ordinal=block_ordinal,
                        create_num=_int(fields.get(b"createnum"), 0),
                        respawn_time=_int(fields.get(b"time"), 0),
                    )

            placement_id += 1

    return by_placement


@dataclass(frozen=True)
class AmbiguousSourceOrder:
    source: tuple[int, int, int]
    candidates: tuple[CreateWarpProvenance, ...]
    classification: str
    first_placement_id: int | None

    def __post_init__(self) -> None:
        rows = tuple(self.candidates)
        if len(rows) < 2:
            raise ValueError("ambiguous source requires multiple candidates")
        if any(row.source != self.source for row in rows):
            raise ValueError("create provenance source drift")
        paths = {row.relative_path for row in rows}
        if self.classification == SAME_FILE_ORDERED:
            if len(paths) != 1:
                raise ValueError("same-file classification contains multiple files")
            if self.first_placement_id is None:
                raise ValueError("same-file group requires a first placement")
            first = min(rows, key=lambda row: row.block_ordinal)
            if first.placement_id != self.first_placement_id:
                raise ValueError("same-file first placement drift")
        elif self.classification == CROSS_FILE_UNORDERED:
            if len(paths) < 2:
                raise ValueError("cross-file classification has one file")
            if self.first_placement_id is not None:
                raise ValueError("cross-file group cannot select first placement")
        else:
            raise ValueError("unknown ambiguous create-order classification")
        object.__setattr__(self, "candidates", rows)


@dataclass(frozen=True)
class AmbiguousWarpCreateOrderAudit:
    rows: tuple[AmbiguousSourceOrder, ...]

    @property
    def counts(self) -> dict[str, int]:
        return {
            "ambiguous_sources": len(self.rows),
            "same_file_ordered_sources": sum(
                row.classification == SAME_FILE_ORDERED for row in self.rows
            ),
            "cross_file_unordered_sources": sum(
                row.classification == CROSS_FILE_UNORDERED for row in self.rows
            ),
            "ambiguous_candidate_records": sum(
                len(row.candidates) for row in self.rows
            ),
        }


def analyze(
    *,
    geometry_text: str,
    npc_dir: Path,
    represented_floor_ids: set[int],
) -> AmbiguousWarpCreateOrderAudit:
    ambiguous = parse_ambiguous_geometry(geometry_text)
    provenance = collect_create_warp_provenance(
        npc_dir=npc_dir,
        represented_floor_ids=represented_floor_ids,
    )

    rows = []
    for source in sorted(ambiguous):
        geometry_rows = ambiguous[source]
        candidates = []
        for row in geometry_rows:
            candidate = provenance.get(row.placement_id)
            if candidate is None:
                raise ValueError(
                    f"missing create provenance for placement {row.placement_id}"
                )
            if candidate.source != row.source:
                raise ValueError(
                    f"source drift for placement {row.placement_id}"
                )
            if candidate.destination != row.destination:
                raise ValueError(
                    f"destination drift for placement {row.placement_id}"
                )
            candidates.append(candidate)

        paths = {row.relative_path for row in candidates}
        if len(paths) == 1:
            block_ordinals = [row.block_ordinal for row in candidates]
            if len(block_ordinals) != len(set(block_ordinals)):
                raise ValueError("ambiguous candidates share create block ordinal")
            first = min(candidates, key=lambda row: row.block_ordinal)
            classification = SAME_FILE_ORDERED
            first_id = first.placement_id
        else:
            classification = CROSS_FILE_UNORDERED
            first_id = None

        rows.append(
            AmbiguousSourceOrder(
                source=source,
                candidates=tuple(candidates),
                classification=classification,
                first_placement_id=first_id,
            )
        )

    return AmbiguousWarpCreateOrderAudit(rows=tuple(rows))


def emit(audit: AmbiguousWarpCreateOrderAudit) -> None:
    print("StoneAge ambiguous classic-Warp create-order audit — R1")
    print(
        "SCOPE|materializable multi-destination source cells|"
        "recovered create path/block provenance + pinned descendant ordering control"
    )
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print(
        "CONTROL|event dispatch=head-to-tail first-match; map object insertion="
        "tail-append; NPC generation=create-index ascending"
    )
    print(
        "RULE|same-file block order can determine relative create order; "
        "cross-file order remains unresolved because create-file discovery is "
        "recursive unsorted readdir"
    )
    for key in sorted(audit.counts):
        print(f"COUNT|{key}|{audit.counts[key]}")

    for row in audit.rows:
        floor, x, y = row.source
        print(
            "AMBIGUOUS_SOURCE_ORDER|"
            f"source={floor},{x},{y}|classification={row.classification}|"
            f"first_placement={row.first_placement_id if row.first_placement_id is not None else 'NONE'}"
        )
        for candidate in row.candidates:
            df, dx, dy = candidate.destination
            print(
                "AMBIGUOUS_CANDIDATE_ORDER|"
                f"source={floor},{x},{y}|placement={candidate.placement_id}|"
                f"destination={df},{dx},{dy}|"
                f"create_path={candidate.relative_path}|"
                f"block_ordinal={candidate.block_ordinal}|"
                f"create_num={candidate.create_num}|"
                f"respawn_time={candidate.respawn_time}"
            )

    print(OUTPUT_RESOLUTION)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--geometry-report", type=Path, required=True)
    parser.add_argument("--npc-dir", type=Path, required=True)
    parser.add_argument(
        "--represented-floor",
        type=int,
        action="append",
        default=[],
    )
    parser.add_argument("--reachability-report", type=Path)
    args = parser.parse_args()

    represented = set(int(v) for v in args.represented_floor)
    if args.reachability_report is not None:
        for raw in args.reachability_report.read_text(
            encoding="utf-8"
        ).splitlines():
            line = raw.strip()
            if line.startswith("SUPPLEMENTAL_FLOOR|"):
                fields = _fields(line, "SUPPLEMENTAL_FLOOR")
                represented.add(int(fields["floor"]))

    # Geometry placement IDs were generated over all represented floor IDs.
    # The stable 761 floor IDs are recoverable from the materializable geometry
    # itself only as source/destination coverage incompletely, so callers should
    # pass the complete represented set. CLI workflow supplies it through a
    # dedicated plain numeric file when available; unit tests call analyze().
    if not represented:
        raise ValueError("represented floor set cannot be empty")

    emit(
        analyze(
            geometry_text=args.geometry_report.read_text(encoding="utf-8"),
            npc_dir=args.npc_dir,
            represented_floor_ids=represented,
        )
    )


if __name__ == "__main__":
    main()
