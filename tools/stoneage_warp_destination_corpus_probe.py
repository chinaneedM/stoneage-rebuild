#!/usr/bin/env python3
"""Classify classic-warp destinations excluded from the stable-world floor set.

This audit answers a narrow question: when a recovered classic Warp points to a
floor outside the 761 stable map candidates, does the verified recovered-2.5
client still contain that DAT, did its bytes change across the recovered-2.5 /
archived-2003 lineage, and is the recovered-2.5 DAT merely asset-compatible
with the Taiwan-v1 resource profile?

None of those properties proves Taiwan-v1 historical membership.
No proprietary map payload bytes are emitted.
"""

from __future__ import annotations

import argparse
import collections
from dataclasses import dataclass
from pathlib import Path

from tools.stoneage_tw10_25_fieldmap_compat_probe import analyze_map
from tools.stoneage_tw10_hit_map_model import load_taiwan_v10_collision_profile


CHANGED = "CHANGED"
SAME_SHA_NONSTABLE = "SAME_SHA_NONSTABLE"
CLIENT_DAT_MISSING = "CLIENT_DAT_MISSING"
CLIENT_DAT_DUPLICATE = "CLIENT_DAT_DUPLICATE"
CLIENT_DAT_INVALID = "CLIENT_DAT_INVALID"


@dataclass(frozen=True)
class ChangedLineage:
    floor_id: int
    sha_recovered25: str
    sha_archived2003: str
    recovered25_compatible: bool
    archived2003_compatible: bool


@dataclass(frozen=True)
class OutsideWarpDestination:
    floor_id: int
    edge_refs: int
    status: str
    client_paths: tuple[str, ...]
    width: int | None = None
    height: int | None = None
    sha256: str | None = None
    recovered25_tw1_asset_compatible: bool | None = None
    archived2003_tw1_asset_compatible: bool | None = None

    def __post_init__(self) -> None:
        if int(self.floor_id) < 0:
            raise ValueError("floor id cannot be negative")
        if int(self.edge_refs) <= 0:
            raise ValueError("outside destination must have at least one edge")


@dataclass(frozen=True)
class OutsideWarpDestinationAudit:
    rows: tuple[OutsideWarpDestination, ...]
    total_classic_warp_edges: int
    outside_stable_edges: int

    @property
    def counts(self) -> collections.Counter:
        out = collections.Counter()
        out["classic_warp_edges"] = int(self.total_classic_warp_edges)
        out["outside_stable_edges"] = int(self.outside_stable_edges)
        out["outside_stable_destination_ids"] = len(self.rows)
        for row in self.rows:
            out[f"status:{row.status}:ids"] += 1
            out[f"status:{row.status}:edges"] += row.edge_refs
            if row.recovered25_tw1_asset_compatible is not None:
                state = int(row.recovered25_tw1_asset_compatible)
                out[f"recovered25_tw1_asset_compatible:{state}:ids"] += 1
                out[f"recovered25_tw1_asset_compatible:{state}:edges"] += (
                    row.edge_refs
                )
        return out


def _fields(line: str, prefix: str) -> dict[str, str]:
    parts = line.split("|")
    if not parts or parts[0] != prefix:
        raise ValueError(f"expected {prefix} record")
    result: dict[str, str] = {}
    for part in parts[1:]:
        if "=" not in part:
            raise ValueError(f"malformed {prefix} field: {part}")
        key, value = part.split("=", 1)
        if not key or key in result:
            raise ValueError(f"duplicate/blank {prefix} field: {key}")
        result[key] = value
    return result


def parse_outside_destinations(
    geometry_text: str,
) -> tuple[collections.Counter, int]:
    destinations = collections.Counter()
    total = 0
    declared_total: int | None = None
    declared_outside: int | None = None

    for raw in str(geometry_text).splitlines():
        line = raw.strip()
        if not line:
            continue
        if line == "COUNT|classic_warp_edges|0":
            declared_total = 0
            continue
        if line.startswith("COUNT|classic_warp_edges|"):
            declared_total = int(line.rsplit("|", 1)[1])
            continue
        if line.startswith("COUNT|classic_warp_destinations_stable|"):
            stable = int(line.rsplit("|", 1)[1])
            if declared_total is not None:
                declared_outside = declared_total - stable
            continue
        if not line.startswith("CLASSIC_WARP|"):
            continue
        total += 1
        fields = _fields(line, "CLASSIC_WARP")
        if "to" not in fields or "destination_stable" not in fields:
            raise ValueError("classic warp row lacks destination fields")
        if int(fields["destination_stable"]):
            continue
        destination = fields["to"].split(",", 1)[0]
        destinations[int(destination)] += 1

    if declared_total is not None and declared_total != total:
        raise ValueError(
            "classic warp detail count drift: "
            f"declared={declared_total}, actual={total}"
        )
    outside = sum(destinations.values())
    if declared_outside is not None and declared_outside != outside:
        raise ValueError(
            "outside-stable warp count drift: "
            f"declared={declared_outside}, actual={outside}"
        )
    return destinations, total


def parse_later_lineage(
    text: str,
) -> tuple[set[int], dict[int, ChangedLineage], dict[str, int]]:
    stable: set[int] = set()
    changed: dict[int, ChangedLineage] = {}
    counts: dict[str, int] = {}
    source_a: str | None = None
    source_b: str | None = None
    resolution = False

    for raw in str(text).splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("SOURCE_A|"):
            source_a = _fields(line, "SOURCE_A").get("label")
            continue
        if line.startswith("SOURCE_B|"):
            source_b = _fields(line, "SOURCE_B").get("label")
            continue
        if line.startswith("COUNT|"):
            parts = line.split("|")
            if len(parts) != 3:
                raise ValueError(f"malformed lineage COUNT: {line}")
            counts[parts[1]] = int(parts[2])
            continue
        if line.startswith("STABLE_COMPATIBLE|"):
            fields = _fields(line, "STABLE_COMPATIBLE")
            floor_id = int(Path(fields["path"]).stem)
            stable.add(floor_id)
            continue
        if line.startswith("CHANGED|"):
            fields = _fields(line, "CHANGED")
            floor_id = int(Path(fields["path"]).stem)
            if floor_id in changed:
                raise ValueError(f"duplicate changed floor {floor_id}")
            changed[floor_id] = ChangedLineage(
                floor_id=floor_id,
                sha_recovered25=fields["sha_a"].lower(),
                sha_archived2003=fields["sha_b"].lower(),
                recovered25_compatible=bool(int(fields["compat_a"])),
                archived2003_compatible=bool(int(fields["compat_b"])),
            )
            continue
        if line == "RESOLUTION|LATER_FIELDMAP_LINEAGE_CLASSIFIED":
            resolution = True

    if source_a != "recovered25" or source_b != "archived2003":
        raise ValueError(
            "later lineage source order is not recovered25 -> archived2003"
        )
    if not resolution:
        raise ValueError("later lineage lacks closed resolution marker")
    if counts.get("only_recovered25") != 0:
        raise ValueError(
            "cannot infer same-SHA counterpart while only_recovered25 != 0"
        )
    if counts.get("only_archived2003") != 0:
        raise ValueError(
            "cannot infer same-SHA counterpart while only_archived2003 != 0"
        )
    if counts.get("same_path_changed_sha256") != len(changed):
        raise ValueError("changed lineage detail count drift")
    if counts.get("same_sha256_and_tw1_compatible_both") != len(stable):
        raise ValueError("stable lineage detail count drift")
    return stable, changed, counts


def collect_numeric_dat_paths(root: Path) -> dict[int, tuple[Path, ...]]:
    grouped: dict[int, list[Path]] = collections.defaultdict(list)
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() != ".dat":
            continue
        try:
            floor_id = int(path.stem)
        except ValueError:
            continue
        grouped[floor_id].append(path)
    return {
        floor_id: tuple(sorted(paths, key=lambda p: str(p).lower()))
        for floor_id, paths in grouped.items()
    }


def classify(
    *,
    geometry_text: str,
    lineage_text: str,
    map_root: Path,
    profile_ids: set[int],
) -> OutsideWarpDestinationAudit:
    destination_refs, total = parse_outside_destinations(geometry_text)
    stable, changed, lineage_counts = parse_later_lineage(lineage_text)
    client_paths = collect_numeric_dat_paths(map_root)

    expected_valid_recovered = (
        lineage_counts["shared_paths"] + lineage_counts["only_recovered25"]
    )
    # The lineage source may contain invalid DAT files too, so this is only a
    # lower-bound sanity check on the numeric DAT inventory.
    if len(client_paths) < expected_valid_recovered:
        raise ValueError(
            "recovered25 client DAT inventory is smaller than lineage valid set"
        )

    rows: list[OutsideWarpDestination] = []
    for floor_id in sorted(destination_refs):
        if floor_id in stable:
            raise ValueError(
                f"geometry marks stable lineage floor {floor_id} as outside"
            )
        paths = client_paths.get(floor_id, ())
        relative = tuple(str(p.relative_to(map_root)) for p in paths)
        if not paths:
            rows.append(
                OutsideWarpDestination(
                    floor_id=floor_id,
                    edge_refs=destination_refs[floor_id],
                    status=CLIENT_DAT_MISSING,
                    client_paths=(),
                )
            )
            continue
        if len(paths) != 1:
            rows.append(
                OutsideWarpDestination(
                    floor_id=floor_id,
                    edge_refs=destination_refs[floor_id],
                    status=CLIENT_DAT_DUPLICATE,
                    client_paths=relative,
                )
            )
            continue

        path = paths[0]
        try:
            info = analyze_map(path, profile_ids)
        except Exception:
            rows.append(
                OutsideWarpDestination(
                    floor_id=floor_id,
                    edge_refs=destination_refs[floor_id],
                    status=CLIENT_DAT_INVALID,
                    client_paths=relative,
                )
            )
            continue

        if floor_id in changed:
            lineage = changed[floor_id]
            if info["sha256"].lower() != lineage.sha_recovered25:
                raise ValueError(
                    f"recovered25 SHA drift for changed floor {floor_id}"
                )
            if bool(info["compatible"]) != lineage.recovered25_compatible:
                raise ValueError(
                    f"recovered25 compatibility drift for floor {floor_id}"
                )
            status = CHANGED
            archived_compatible = lineage.archived2003_compatible
        else:
            # With both only-* counts at zero, a valid recovered25 path not in
            # CHANGED must have an archived2003 same-path counterpart with the
            # same SHA. If it were compatible with the same Taiwan-v1 profile,
            # it would be present in STABLE_COMPATIBLE.
            if bool(info["compatible"]):
                raise ValueError(
                    "non-stable same-SHA floor unexpectedly Taiwan-v1 "
                    f"asset-compatible: {floor_id}"
                )
            status = SAME_SHA_NONSTABLE
            archived_compatible = False

        rows.append(
            OutsideWarpDestination(
                floor_id=floor_id,
                edge_refs=destination_refs[floor_id],
                status=status,
                client_paths=relative,
                width=int(info["width"]),
                height=int(info["height"]),
                sha256=str(info["sha256"]).lower(),
                recovered25_tw1_asset_compatible=bool(info["compatible"]),
                archived2003_tw1_asset_compatible=archived_compatible,
            )
        )

    return OutsideWarpDestinationAudit(
        rows=tuple(rows),
        total_classic_warp_edges=total,
        outside_stable_edges=sum(destination_refs.values()),
    )


def emit(audit: OutsideWarpDestinationAudit) -> None:
    print("StoneAge outside-stable classic-warp destination audit — R1")
    print(
        "SCOPE|classic-Warp destinations excluded from stable-world candidates|"
        "recovered25-client-DAT+later-lineage+tw1-asset-compatibility"
    )
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print(
        "RULE|Taiwan-v1 asset compatibility is necessary-not-sufficient and "
        "does not prove Taiwan-v1 map membership"
    )
    for key in sorted(audit.counts):
        print(f"COUNT|{key}|{audit.counts[key]}")
    for row in audit.rows:
        fields = [
            f"floor={row.floor_id}",
            f"edge_refs={row.edge_refs}",
            f"status={row.status}",
            f"client_paths={','.join(row.client_paths)}",
        ]
        if row.width is not None:
            fields.extend(
                [
                    f"width={row.width}",
                    f"height={row.height}",
                    f"sha256={row.sha256}",
                    "recovered25_tw1_asset_compatible="
                    f"{int(bool(row.recovered25_tw1_asset_compatible))}",
                    "archived2003_tw1_asset_compatible="
                    f"{int(bool(row.archived2003_tw1_asset_compatible))}",
                ]
            )
        print("DESTINATION|" + "|".join(fields))
    print("RESOLUTION|OUTSIDE_STABLE_WARP_DESTINATIONS_CLASSIFIED")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--geometry-report", type=Path, required=True)
    parser.add_argument("--lineage-report", type=Path, required=True)
    parser.add_argument("--map-root", type=Path, required=True)
    parser.add_argument("--profile", type=Path, required=True)
    args = parser.parse_args()

    profile = load_taiwan_v10_collision_profile(args.profile)
    audit = classify(
        geometry_text=args.geometry_report.read_text(encoding="utf-8"),
        lineage_text=args.lineage_report.read_text(encoding="utf-8"),
        map_root=args.map_root,
        profile_ids=set(profile.by_map_number),
    )
    emit(audit)


if __name__ == "__main__":
    main()
