#!/usr/bin/env python3
"""Audit gameplay coverage on recovered server-only warp destination floors.

The target floor set is taken from the closed missing-DAT payload report.
Only derived counts and classic Warp destination tuples are emitted; NPC names,
arguments unrelated to classic Warp, dialogue, encounter/group/enemy IDs, and
original server payloads are not retained.
"""

from __future__ import annotations

import argparse
import collections
from dataclasses import dataclass
from pathlib import Path

from tools.stoneage_map_delivery_model import (
    parse_server_only_payload_report,
)
from tools.stoneage_npc_world_graph_probe import (
    iter_blocks,
    magic_kind,
    parse_templates,
)
from tools.stoneage_world_content_coverage_probe import (
    _encounter_floor_counts,
)


WARP_FUNCTIONSETS = frozenset({b"warp", b"warpman", b"fmwarpman"})
CLASSIC_WARP_FUNCTIONSET = b"warp"
SOURCE_VERSION = "recovered25"
EVIDENCE_ROLE = "LATER_RECOVERED"


def _int(value: bytes | None, default: int = 0) -> int:
    if value is None:
        return default
    try:
        return int(value.strip(), 10)
    except ValueError:
        return default


def _first_templates_and_create_paths(npc_dir: Path):
    template_paths = []
    create_paths = []
    for path in sorted(
        (p for p in npc_dir.rglob("*") if p.is_file()),
        key=lambda p: str(p).lower(),
    ):
        kind = magic_kind(path)
        if kind == "template":
            template_paths.append(path)
        elif kind == "create":
            create_paths.append(path)

    first = {}
    for template in parse_templates(template_paths):
        name = template["name"].strip().lower()
        if name and name not in first:
            first[name] = template
    return first, tuple(create_paths)


def _classic_destination(argument: bytes) -> tuple[int, int, int] | None:
    parts = argument.split(b"|")
    if len(parts) < 3:
        return None
    try:
        return tuple(int(part.strip(), 10) for part in parts[:3])
    except ValueError:
        return None


@dataclass(frozen=True)
class ServerOnlyFloorGameplay:
    floor_id: int
    npc_create_count: int
    warp_create_count: int
    classic_warp_edges: tuple[tuple[int, int, int], ...]
    encounter_row_count: int
    active_encounter_row_count: int

    def __post_init__(self) -> None:
        if int(self.floor_id) < 0:
            raise ValueError("floor id cannot be negative")
        for value in (
            self.npc_create_count,
            self.warp_create_count,
            self.encounter_row_count,
            self.active_encounter_row_count,
        ):
            if int(value) < 0:
                raise ValueError("gameplay counts cannot be negative")
        if self.warp_create_count > self.npc_create_count:
            raise ValueError("warp create count exceeds NPC create count")
        if self.active_encounter_row_count > self.encounter_row_count:
            raise ValueError("active encounter count exceeds encounter count")
        object.__setattr__(
            self,
            "classic_warp_edges",
            tuple(tuple(int(v) for v in edge) for edge in self.classic_warp_edges),
        )


@dataclass(frozen=True)
class ServerOnlyFloorGameplayAudit:
    rows: tuple[ServerOnlyFloorGameplay, ...]
    encounter_file_name: str

    @property
    def counts(self) -> dict[str, int]:
        out = {
            "target_floors": len(self.rows),
            "floors_with_npc": sum(row.npc_create_count > 0 for row in self.rows),
            "floors_with_warp_functionset": sum(
                row.warp_create_count > 0 for row in self.rows
            ),
            "floors_with_classic_warp": sum(
                bool(row.classic_warp_edges) for row in self.rows
            ),
            "floors_with_encounter": sum(
                row.encounter_row_count > 0 for row in self.rows
            ),
            "floors_with_active_encounter": sum(
                row.active_encounter_row_count > 0 for row in self.rows
            ),
            "npc_create_count": sum(row.npc_create_count for row in self.rows),
            "warp_create_count": sum(row.warp_create_count for row in self.rows),
            "classic_warp_edges": sum(
                len(row.classic_warp_edges) for row in self.rows
            ),
            "encounter_rows": sum(
                row.encounter_row_count for row in self.rows
            ),
            "active_encounter_rows": sum(
                row.active_encounter_row_count for row in self.rows
            ),
        }
        return out


def analyze(
    *,
    payload_report_text: str,
    npc_dir: Path,
    data_dir: Path,
    setup: Path | None,
) -> ServerOnlyFloorGameplayAudit:
    payload = parse_server_only_payload_report(payload_report_text)
    targets = {row.floor_id for row in payload.rows}
    first_templates, create_paths = _first_templates_and_create_paths(npc_dir)

    npc_counts = collections.Counter()
    warp_counts = collections.Counter()
    classic_edges: dict[int, list[tuple[int, int, int]]] = collections.defaultdict(list)

    for path in create_paths:
        for entries in iter_blocks(path):
            fields: dict[bytes, bytes] = {}
            enemy_values: list[bytes] = []
            for key, value in entries:
                if key == b"enemy":
                    enemy_values.append(value)
                else:
                    fields[key] = value

            floor_id = _int(fields.get(b"floorid"))
            if floor_id not in targets:
                continue
            if b"borncenter" not in fields and b"borncorner" not in fields:
                continue

            resolved: list[tuple[dict, bytes]] = []
            for value in enemy_values:
                name, sep, arg = value.partition(b"|")
                template = first_templates.get(name.strip().lower())
                if template is not None:
                    resolved.append((template, arg if sep else b""))
            if not resolved:
                continue

            npc_counts[floor_id] += 1
            if any(
                template["functionset"].strip().lower() in WARP_FUNCTIONSETS
                for template, _arg in resolved
            ):
                warp_counts[floor_id] += 1

            for template, arg in resolved:
                if template["functionset"].strip().lower() != CLASSIC_WARP_FUNCTIONSET:
                    continue
                destination = _classic_destination(arg)
                if destination is not None:
                    classic_edges[floor_id].append(destination)

    encounter_name, encounter_counts, active_encounter_counts = (
        _encounter_floor_counts(data_dir, setup)
    )

    rows = tuple(
        ServerOnlyFloorGameplay(
            floor_id=floor_id,
            npc_create_count=npc_counts[floor_id],
            warp_create_count=warp_counts[floor_id],
            classic_warp_edges=tuple(classic_edges[floor_id]),
            encounter_row_count=int(encounter_counts.get(floor_id, 0)),
            active_encounter_row_count=int(active_encounter_counts.get(floor_id, 0)),
        )
        for floor_id in sorted(targets)
    )
    return ServerOnlyFloorGameplayAudit(
        rows=rows,
        encounter_file_name=encounter_name,
    )


def emit(audit: ServerOnlyFloorGameplayAudit) -> None:
    print("StoneAge server-only floor gameplay coverage audit — R1")
    print(
        "SCOPE|server-only recovered25 warp destinations|"
        "derived NPC/warp/encounter coverage only"
    )
    print(f"SEMANTIC_SOURCE_VERSION|{SOURCE_VERSION}")
    print(f"EVIDENCE_ROLE|{EVIDENCE_ROLE}")
    print(
        "RULE|coverage does not promote recovered25 floors into Taiwan-v1 membership"
    )
    print(f"ACTIVE_ENCOUNT_FILE|{audit.encounter_file_name}")
    for key in sorted(audit.counts):
        print(f"COUNT|{key}|{audit.counts[key]}")
    for row in audit.rows:
        print(
            "FLOOR|"
            f"floor={row.floor_id}|"
            f"npc_create_count={row.npc_create_count}|"
            f"warp_create_count={row.warp_create_count}|"
            f"classic_warp_edges={len(row.classic_warp_edges)}|"
            f"encounter_rows={row.encounter_row_count}|"
            f"active_encounter_rows={row.active_encounter_row_count}"
        )
        for destination in row.classic_warp_edges:
            print(
                "CLASSIC_WARP|"
                f"source_floor={row.floor_id}|"
                f"destination_floor={destination[0]}|"
                f"destination_x={destination[1]}|"
                f"destination_y={destination[2]}"
            )
    print("RESOLUTION|SERVER_ONLY_FLOOR_GAMEPLAY_COVERAGE_CLASSIFIED")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--payload-report", type=Path, required=True)
    parser.add_argument("--npc-dir", type=Path, required=True)
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--setup", type=Path)
    args = parser.parse_args()

    emit(
        analyze(
            payload_report_text=args.payload_report.read_text(encoding="utf-8"),
            npc_dir=args.npc_dir,
            data_dir=args.data_dir,
            setup=args.setup,
        )
    )


if __name__ == "__main__":
    main()
