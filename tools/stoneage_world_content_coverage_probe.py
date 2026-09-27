#!/usr/bin/env python3
"""Build a version-tagged world-content coverage manifest for stable later maps.

The output intentionally records only derived floor-level coverage counts. It
does not retain NPC names, arguments, dialogue, coordinates, encounter IDs,
group IDs, enemy IDs, or proprietary map payloads.

All NPC/encounter semantics in this probe come from the recovered 2.5 server
specimen and therefore remain LATER_RECOVERED. Joining them to a stable map
candidate never promotes either side to Taiwan-v1 membership.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
from dataclasses import dataclass
from pathlib import Path

from tools.stoneage_encount_chain_probe import (
    configured_file,
    parse_encount,
    setup_values as encounter_setup_values,
)
from tools.stoneage_npc_world_graph_probe import (
    collect_server_map_ids,
    magic_kind,
    parse_create_blocks,
    parse_templates,
)
from tools.stoneage_world_map_library import (
    StableLaterMapManifest,
    parse_stable_later_map_manifest,
)


SOURCE_VERSION = "recovered25"
WARP_FUNCTIONSETS = frozenset({b"warp", b"warpman", b"fmwarpman"})


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


@dataclass(frozen=True)
class WorldContentFloorCoverage:
    floor_id: int
    path: str
    width: int
    height: int
    map_sha256: str
    server_map_present: bool
    npc_create_count: int
    warp_functionset_create_count: int
    encounter_row_count: int
    active_encounter_row_count: int

    def __post_init__(self) -> None:
        for name in (
            "npc_create_count",
            "warp_functionset_create_count",
            "encounter_row_count",
            "active_encounter_row_count",
        ):
            value = int(getattr(self, name))
            if value < 0:
                raise ValueError(f"{name} cannot be negative")
            object.__setattr__(self, name, value)
        if self.warp_functionset_create_count > self.npc_create_count:
            raise ValueError("warp-functionset count cannot exceed NPC create count")
        if self.active_encounter_row_count > self.encounter_row_count:
            raise ValueError(
                "active encounter count cannot exceed total encounter count"
            )
        object.__setattr__(self, "floor_id", int(self.floor_id))
        object.__setattr__(self, "server_map_present", bool(self.server_map_present))

    @property
    def has_npc_semantics(self) -> bool:
        return self.npc_create_count > 0

    @property
    def has_encounter_semantics(self) -> bool:
        return self.encounter_row_count > 0

    @property
    def has_warp_functionset_semantics(self) -> bool:
        return self.warp_functionset_create_count > 0


@dataclass(frozen=True)
class WorldContentCoverage:
    floors: tuple[WorldContentFloorCoverage, ...]
    server_map_id_count: int
    npc_effective_floor_count: int
    encounter_floor_count: int
    active_encounter_floor_count: int
    encounter_file_name: str

    def __post_init__(self) -> None:
        floors = tuple(self.floors)
        ids = [row.floor_id for row in floors]
        if len(ids) != len(set(ids)):
            raise ValueError("world-content coverage contains duplicate stable floors")
        object.__setattr__(self, "floors", floors)
        object.__setattr__(self, "server_map_id_count", int(self.server_map_id_count))
        object.__setattr__(
            self, "npc_effective_floor_count", int(self.npc_effective_floor_count)
        )
        object.__setattr__(
            self, "encounter_floor_count", int(self.encounter_floor_count)
        )
        object.__setattr__(
            self,
            "active_encounter_floor_count",
            int(self.active_encounter_floor_count),
        )

    def count(self, predicate) -> int:
        return sum(1 for row in self.floors if predicate(row))


def _first_template_by_name(npc_dir: Path):
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
    return first, parse_create_blocks(create_paths)


def _npc_floor_counts(
    npc_dir: Path,
    server_map_ids: set[int],
):
    first_template, creates = _first_template_by_name(npc_dir)
    npc_counts = collections.Counter()
    warp_counts = collections.Counter()

    for create in creates:
        floor = int(create["floorid"])
        if not create["born_defined"] or floor not in server_map_ids:
            continue

        resolved_templates = []
        for name, _has_arg in create["enemies"]:
            template = first_template.get(name.strip().lower())
            if template is not None:
                resolved_templates.append(template)
        if not resolved_templates:
            continue

        npc_counts[floor] += 1
        if any(
            template["functionset"].strip().lower() in WARP_FUNCTIONSETS
            for template in resolved_templates
        ):
            warp_counts[floor] += 1

    return npc_counts, warp_counts


def _encounter_floor_counts(data_dir: Path, setup: Path | None):
    config = encounter_setup_values(setup)
    encount = configured_file(
        data_dir,
        config,
        "encountfile",
        ["encount*.txt"],
    )
    if encount is None:
        raise ValueError("recovered data has no active encounter file candidate")
    _raw, rows, malformed, _widths = parse_encount(encount)
    if malformed:
        raise ValueError(
            f"active encounter file contains {malformed} malformed rows"
        )
    counts = collections.Counter(int(row["floor"]) for row in rows)
    active = collections.Counter(
        int(row["floor"]) for row in rows if int(row["zorder"]) > 0
    )
    return encount.name, counts, active


def analyze_world_content_coverage(
    *,
    manifest: StableLaterMapManifest,
    npc_dir: Path,
    data_dir: Path,
    map_dir: Path,
    setup: Path | None = None,
) -> WorldContentCoverage:
    server_map_ids, _server_map_files = collect_server_map_ids(map_dir)
    if not server_map_ids:
        raise ValueError("recovered server map set is empty")

    npc_counts, warp_counts = _npc_floor_counts(npc_dir, server_map_ids)
    encounter_name, encounter_counts, active_encounter_counts = (
        _encounter_floor_counts(data_dir, setup)
    )

    floors = tuple(
        WorldContentFloorCoverage(
            floor_id=candidate.floor_id,
            path=candidate.path,
            width=candidate.width,
            height=candidate.height,
            map_sha256=candidate.sha256,
            server_map_present=candidate.floor_id in server_map_ids,
            npc_create_count=npc_counts[candidate.floor_id],
            warp_functionset_create_count=warp_counts[candidate.floor_id],
            encounter_row_count=encounter_counts[candidate.floor_id],
            active_encounter_row_count=active_encounter_counts[candidate.floor_id],
        )
        for candidate in manifest.candidates
    )

    return WorldContentCoverage(
        floors=floors,
        server_map_id_count=len(server_map_ids),
        npc_effective_floor_count=len(npc_counts),
        encounter_floor_count=len(encounter_counts),
        active_encounter_floor_count=len(active_encounter_counts),
        encounter_file_name=encounter_name,
    )


def emit(
    coverage: WorldContentCoverage,
    *,
    lineage_report_sha256: str,
) -> None:
    print("StoneAge stable-map / recovered-2.5 world-content coverage — R1")
    print(
        "SCOPE|derived-floor-coverage-only|"
        "no-npc-names|no-arguments|no-dialogue|no-coordinates|"
        "no-encounter-identities|no-map-payload"
    )
    print(f"SEMANTIC_SOURCE_VERSION|{SOURCE_VERSION}")
    print(f"LINEAGE_REPORT_SHA256|{lineage_report_sha256}")
    print(
        "RULE|recovered25 world semantics remain LATER_RECOVERED and "
        "do not prove Taiwan-v1 membership"
    )
    print(
        "WARP_CLASSIFIER|template functionset literal in "
        "Warp,WarpMan,FMWarpMan|not all possible transition mechanics"
    )
    print(f"ACTIVE_ENCOUNT_FILE|{coverage.encounter_file_name}")
    print(f"COUNT|stable_floor_candidates|{len(coverage.floors)}")
    print(f"COUNT|server_map_ids|{coverage.server_map_id_count}")
    print(
        f"COUNT|npc_effective_floors_all_recovered25|"
        f"{coverage.npc_effective_floor_count}"
    )
    print(
        f"COUNT|encounter_floors_all_recovered25|"
        f"{coverage.encounter_floor_count}"
    )
    print(
        f"COUNT|active_encounter_floors_all_recovered25|"
        f"{coverage.active_encounter_floor_count}"
    )
    print(
        f"COUNT|stable_with_server_map|"
        f"{coverage.count(lambda row: row.server_map_present)}"
    )
    print(
        f"COUNT|stable_with_npc_semantics|"
        f"{coverage.count(lambda row: row.has_npc_semantics)}"
    )
    print(
        f"COUNT|stable_with_warp_functionset_semantics|"
        f"{coverage.count(lambda row: row.has_warp_functionset_semantics)}"
    )
    print(
        f"COUNT|stable_with_encounter_semantics|"
        f"{coverage.count(lambda row: row.has_encounter_semantics)}"
    )
    print(
        f"COUNT|stable_with_npc_and_encounter_semantics|"
        f"{coverage.count(lambda row: row.has_npc_semantics and row.has_encounter_semantics)}"
    )
    print(
        f"COUNT|stable_without_recovered25_world_semantics|"
        f"{coverage.count(lambda row: not row.has_npc_semantics and not row.has_encounter_semantics)}"
    )

    for row in coverage.floors:
        print(
            "FLOOR|"
            f"id={row.floor_id}|path={row.path}|"
            f"width={row.width}|height={row.height}|"
            f"map_sha256={row.map_sha256}|"
            f"server_map={int(row.server_map_present)}|"
            f"npc_create={row.npc_create_count}|"
            f"warp_functionset_create={row.warp_functionset_create_count}|"
            f"encounter_rows={row.encounter_row_count}|"
            f"active_encounter_rows={row.active_encounter_row_count}"
        )

    print("RESOLUTION|VERSIONED_WORLD_CONTENT_COVERAGE_CLASSIFIED")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lineage-report", type=Path, required=True)
    parser.add_argument("--npc-dir", type=Path, required=True)
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--map-dir", type=Path, required=True)
    parser.add_argument("--setup", type=Path)
    args = parser.parse_args()

    report_text = args.lineage_report.read_text(encoding="utf-8")
    manifest = parse_stable_later_map_manifest(report_text)
    coverage = analyze_world_content_coverage(
        manifest=manifest,
        npc_dir=args.npc_dir,
        data_dir=args.data_dir,
        map_dir=args.map_dir,
        setup=args.setup,
    )
    emit(coverage, lineage_report_sha256=sha256(args.lineage_report))


if __name__ == "__main__":
    main()
