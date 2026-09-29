#!/usr/bin/env python3
"""Classify recovered WarpMan gating for shadowed-branch ingress candidates.

This focused audit follows the already-closed ordered classic-Warp reachability
and the recovered WarpMan argument shape. It emits only booleans/categories
needed to decide whether a configured ingress has an ordinary satisfiable
interaction path. Dialogue strings, item/event operands, money values,
coordinates, NPC/template names and filenames are not retained.
"""

from __future__ import annotations

import argparse
import collections
from dataclasses import dataclass
from pathlib import Path

from tools.stoneage_ordered_runtime_world_reachability_probe import (
    load_ordered_runtime_reachability,
)
from tools.stoneage_transport_usage_probe import (
    assigned_file,
    iter_blocks,
    magic_kind,
    merge_file,
    template_map,
)


OUTPUT_RESOLUTION = "RESOLUTION|SHADOWED_BRANCH_WARPMAN_GATING_AUDITED"

UNCONDITIONALLY_FREE = "UNCONDITIONALLY_FREE"
PAYABLE = "PAYABLE"
CONDITION_DEPENDENT = "CONDITION_DEPENDENT"
NO_ORDINARY_ROUTE_PROVEN = "NO_ORDINARY_ROUTE_PROVEN"

ABSENT = "ABSENT"
NEGATIVE_DISABLED = "NEGATIVE_DISABLED"
LEVEL_SCALED = "LEVEL_SCALED"
NONNEGATIVE_FIXED = "NONNEGATIVE_FIXED"
OTHER = "OTHER"


def _field(data: bytes, key: bytes) -> bytes | None:
    wanted = key.strip().lower()
    for token in data.split(b"|"):
        token = token.strip()
        if b":" not in token:
            continue
        name, value = token.split(b":", 1)
        if name.strip().lower() == wanted:
            return value.strip()
    return None


def _int_prefix(value: bytes | None) -> int | None:
    if value is None:
        return None
    text = value.strip()
    if not text:
        return None
    sign = 1
    if text[:1] in (b"+", b"-"):
        sign = -1 if text[:1] == b"-" else 1
        text = text[1:]
    total = 0
    found = False
    for char in text:
        if not 48 <= char <= 57:
            break
        total = total * 10 + char - 48
        found = True
    return sign * total if found else None


def _warp_floors(data: bytes) -> tuple[int, ...]:
    value = _field(data, b"WARP")
    if value is None:
        return ()
    floors = []
    for point in value.split(b";")[:20]:
        first = point.split(b",", 1)[0].strip()
        floor_id = _int_prefix(first)
        if floor_id is not None and floor_id > 0:
            floors.append(int(floor_id))
    return tuple(floors)


def _assigned_data(npc_dir: Path, arg: bytes) -> bytes | None:
    filename = assigned_file(arg)
    if filename is None:
        return arg
    path = npc_dir / filename
    if not path.is_file():
        return None
    return merge_file(path)


def _money_class(data: bytes) -> str:
    value = _field(data, b"MONEY")
    if value is None:
        return ABSENT
    upper = value.upper()
    if b"LV" in upper:
        return LEVEL_SCALED
    parsed = _int_prefix(value)
    if parsed is None:
        return OTHER
    if parsed < 0:
        return NEGATIVE_DISABLED
    return NONNEGATIVE_FIXED


@dataclass(frozen=True)
class WarpManIngressGate:
    source_floor: int
    destination_floor: int
    destination_count: int
    target_occurrences: int
    is_newwarpman: bool
    warp_msg_required: bool
    checkparty_present: bool
    checkparty_explicit_false: bool
    free_present: bool
    free_allfree: bool
    paymsg_present: bool
    normalmsg_present: bool
    money_class: str
    newtime_present: bool
    ordinary_route_class: str

    def __post_init__(self) -> None:
        if self.ordinary_route_class not in {
            UNCONDITIONALLY_FREE,
            PAYABLE,
            CONDITION_DEPENDENT,
            NO_ORDINARY_ROUTE_PROVEN,
        }:
            raise ValueError("invalid WarpMan ordinary-route class")
        if self.money_class not in {
            ABSENT,
            NEGATIVE_DISABLED,
            LEVEL_SCALED,
            NONNEGATIVE_FIXED,
            OTHER,
        }:
            raise ValueError("invalid WarpMan money class")
        if int(self.destination_count) <= 0:
            raise ValueError("WarpMan ingress requires destination evidence")
        if int(self.target_occurrences) <= 0:
            raise ValueError("WarpMan ingress target must occur in WARP set")


@dataclass(frozen=True)
class WarpManGateAudit:
    rows: tuple[WarpManIngressGate, ...]
    target_orphan_floors: tuple[int, ...]
    missing_argument_files: int

    @property
    def counts(self) -> dict[str, int]:
        out = collections.Counter()
        out["target_orphan_floors"] = len(self.target_orphan_floors)
        out["warpman_ingress_rows"] = len(self.rows)
        out["missing_argument_files"] = int(self.missing_argument_files)
        out["unique_ingress_destination_floors"] = len({
            row.destination_floor for row in self.rows
        })
        for row in self.rows:
            out[f"ordinary_route:{row.ordinary_route_class}"] += 1
            out[f"money_class:{row.money_class}"] += 1
            out[f"warp_msg_required:{int(row.warp_msg_required)}"] += 1
            out[f"newwarpman:{int(row.is_newwarpman)}"] += 1
        return dict(out)


def _ordinary_route_class(data: bytes) -> str:
    free = _field(data, b"FREE")
    if free is not None and b"ALLFREE" in free.upper():
        return UNCONDITIONALLY_FREE

    paymsg = _field(data, b"PayMsg")
    money = _money_class(data)
    if paymsg is not None and money in {
        NONNEGATIVE_FIXED,
        LEVEL_SCALED,
    }:
        return PAYABLE

    if free is not None:
        return CONDITION_DEPENDENT
    return NO_ORDINARY_ROUTE_PROVEN


def analyze(npc_dir: Path) -> WarpManGateAudit:
    reachability = load_ordered_runtime_reachability()
    reached = set(reachability.reached_floor_ids)
    target_orphans = tuple(row.floor_id for row in reachability.orphan_rows)
    target_set = set(target_orphans)

    files = sorted(
        (path for path in npc_dir.rglob("*") if path.is_file()),
        key=lambda path: str(path).lower(),
    )
    templates = template_map([
        path for path in files if magic_kind(path) == "template"
    ])
    warpman_names = {
        name for name, definitions in templates.items()
        if len(definitions) == 1 and definitions[0] == b"WarpMan"
    }

    rows: list[WarpManIngressGate] = []
    missing = 0
    for create_path in (
        path for path in files if magic_kind(path) == "create"
    ):
        for entries in iter_blocks(create_path):
            fields: dict[bytes, bytes] = {}
            enemies: list[bytes] = []
            for key, value in entries:
                if key == b"enemy":
                    enemies.append(value)
                else:
                    fields[key] = value
            try:
                source_floor = int(fields.get(b"floorid", b"0"))
            except ValueError:
                continue
            if source_floor not in reached:
                continue
            if b"borncenter" not in fields and b"borncorner" not in fields:
                continue

            for enemy in enemies:
                name, separator, arg = enemy.partition(b"|")
                if name.strip() not in warpman_names:
                    continue
                data = _assigned_data(
                    npc_dir,
                    arg if separator else b"",
                )
                if data is None:
                    missing += 1
                    continue
                destinations = _warp_floors(data)
                hits = collections.Counter(
                    floor_id for floor_id in destinations
                    if floor_id in target_set
                )
                if not hits:
                    continue

                checkparty = _field(data, b"CHECKPARTY")
                free = _field(data, b"FREE")
                upper_all = data.upper()
                for destination_floor, occurrences in sorted(hits.items()):
                    rows.append(
                        WarpManIngressGate(
                            source_floor=source_floor,
                            destination_floor=destination_floor,
                            destination_count=len(destinations),
                            target_occurrences=occurrences,
                            is_newwarpman=(b"NEWWARPMAN" in upper_all),
                            warp_msg_required=(
                                _field(data, b"warp_msg") is not None
                            ),
                            checkparty_present=checkparty is not None,
                            checkparty_explicit_false=(
                                checkparty is not None
                                and b"FALSE" in checkparty.upper()
                            ),
                            free_present=free is not None,
                            free_allfree=(
                                free is not None
                                and b"ALLFREE" in free.upper()
                            ),
                            paymsg_present=_field(data, b"PayMsg") is not None,
                            normalmsg_present=(
                                _field(data, b"NomalMsg") is not None
                                or _field(data, b"nomal_msg") is not None
                            ),
                            money_class=_money_class(data),
                            newtime_present=_field(data, b"NEWTIME") is not None,
                            ordinary_route_class=_ordinary_route_class(data),
                        )
                    )

    return WarpManGateAudit(
        rows=tuple(rows),
        target_orphan_floors=target_orphans,
        missing_argument_files=missing,
    )


def emit(audit: WarpManGateAudit) -> None:
    print("StoneAge shadowed-branch WarpMan gating audit — R1")
    print(
        "SCOPE|ordered-reachable WarpMan -> classic-Warp orphan floors|"
        "derived gate categories only"
    )
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print(
        "RULE|ordinary-route class describes recoverable interaction gating; "
        "it does not erase party, event-action, ticket or dialogue semantics"
    )
    for key in sorted(audit.counts):
        print(f"COUNT|{key}|{audit.counts[key]}")
    for row in sorted(
        audit.rows,
        key=lambda item: (item.source_floor, item.destination_floor),
    ):
        print(
            "WARPMAN_INGRESS_GATE|"
            f"source_floor={row.source_floor}|"
            f"destination_floor={row.destination_floor}|"
            f"destination_count={row.destination_count}|"
            f"target_occurrences={row.target_occurrences}|"
            f"newwarpman={int(row.is_newwarpman)}|"
            f"warp_msg_required={int(row.warp_msg_required)}|"
            f"checkparty_present={int(row.checkparty_present)}|"
            f"checkparty_explicit_false={int(row.checkparty_explicit_false)}|"
            f"free_present={int(row.free_present)}|"
            f"free_allfree={int(row.free_allfree)}|"
            f"paymsg_present={int(row.paymsg_present)}|"
            f"normalmsg_present={int(row.normalmsg_present)}|"
            f"money_class={row.money_class}|"
            f"newtime_present={int(row.newtime_present)}|"
            f"ordinary_route={row.ordinary_route_class}"
        )
    print(OUTPUT_RESOLUTION)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--npc-dir", type=Path, required=True)
    args = parser.parse_args()
    emit(analyze(args.npc_dir))


if __name__ == "__main__":
    main()
