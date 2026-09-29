#!/usr/bin/env python3
"""Audit gate structure for recovered WarpMan ingress into the shadowed branch.

This probe starts from the already-closed 815-floor ordered classic-Warp
closure and looks only at effective recovered25 WarpMan instances whose WARP
candidate set enters one of the eleven shadowed supplemental floors.

It reports structural gate categories only. Raw FREE expressions, prices,
event/item identifiers, NPC/template names, argument filenames, messages and
coordinates are deliberately not emitted.
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


WARPMAN = b"WarpMan"

PLAIN_ALLFREE_DIALOGUE = "PLAIN_ALLFREE_DIALOGUE"
FREE_CONDITION_DIALOGUE = "FREE_CONDITION_DIALOGUE"
DIALOGUE_OR_PAYMENT = "DIALOGUE_OR_PAYMENT"
NEW_EVENT_GATED_DIALOGUE = "NEW_EVENT_GATED_DIALOGUE"
TIME_GATED_DIALOGUE = "TIME_GATED_DIALOGUE"
STRUCTURALLY_UNCLASSIFIED = "STRUCTURALLY_UNCLASSIFIED"

OUTPUT_RESOLUTION = "RESOLUTION|SHADOWED_BRANCH_WARPMAN_GATE_AUDITED"


def _int(value: bytes | None, default: int = 0) -> int:
    if value is None:
        return default
    try:
        return int(value.strip(), 10)
    except ValueError:
        return default


def _tokens(data: bytes) -> tuple[tuple[bytes, bytes], ...]:
    out = []
    for token in data.replace(b"\r", b"").replace(b"\n", b"|").split(b"|"):
        token = token.strip()
        if not token or b":" not in token:
            continue
        key, value = token.split(b":", 1)
        out.append((key.strip().lower(), value.strip()))
    return tuple(out)


def _values(tokens, key: bytes) -> tuple[bytes, ...]:
    wanted = key.lower()
    return tuple(value for name, value in tokens if name == wanted)


def _warp_floors(tokens) -> tuple[int, ...]:
    floors = []
    for value in _values(tokens, b"warp"):
        for point in value.split(b";")[:20]:
            parts = tuple(part.strip() for part in point.split(b","))
            if len(parts) < 3:
                continue
            try:
                floor_id = int(parts[0], 10)
            except ValueError:
                continue
            if floor_id > 0:
                floors.append(floor_id)
    return tuple(floors)


def _truthy_false(value: bytes) -> bool:
    return value.strip().upper() == b"FALSE"


@dataclass(frozen=True)
class WarpManGateAuditRow:
    source_floor: int
    target_floor: int
    classification: str
    target_candidate_count: int
    total_warp_candidates: int
    new_warpman: bool
    newtime_present: bool
    free_present: bool
    allfree_present: bool
    payment_path_present: bool
    money_present: bool
    checkparty_present: bool
    checkparty_explicit_false: bool
    talk_event_present: bool
    warp_msg_present: bool
    over_marker_present: bool

    def __post_init__(self) -> None:
        if int(self.source_floor) <= 0 or int(self.target_floor) <= 0:
            raise ValueError("WarpMan gate floor ids must be positive")
        if int(self.target_candidate_count) <= 0:
            raise ValueError("WarpMan gate row must target the branch")
        if int(self.total_warp_candidates) < int(self.target_candidate_count):
            raise ValueError("WarpMan candidate counts are inconsistent")
        allowed = {
            PLAIN_ALLFREE_DIALOGUE,
            FREE_CONDITION_DIALOGUE,
            DIALOGUE_OR_PAYMENT,
            NEW_EVENT_GATED_DIALOGUE,
            TIME_GATED_DIALOGUE,
            STRUCTURALLY_UNCLASSIFIED,
        }
        if self.classification not in allowed:
            raise ValueError("unknown WarpMan gate classification")


@dataclass(frozen=True)
class WarpManGateAudit:
    rows: tuple[WarpManGateAuditRow, ...]
    reference_counts: collections.Counter
    shadowed_branch_floor_ids: tuple[int, ...]

    @property
    def counts(self) -> dict[str, int]:
        out = {
            "shadowed_branch_floor_ids": len(self.shadowed_branch_floor_ids),
            "matching_warpman_instances": len(self.rows),
            "matching_source_floors": len({
                row.source_floor for row in self.rows
            }),
            "matching_target_floors": len({
                row.target_floor for row in self.rows
            }),
        }
        for classification in (
            PLAIN_ALLFREE_DIALOGUE,
            FREE_CONDITION_DIALOGUE,
            DIALOGUE_OR_PAYMENT,
            NEW_EVENT_GATED_DIALOGUE,
            TIME_GATED_DIALOGUE,
            STRUCTURALLY_UNCLASSIFIED,
        ):
            out[f"classification:{classification}:instances"] = sum(
                row.classification == classification for row in self.rows
            )
        out["WarpMan:refs"] = int(self.reference_counts["refs"])
        out["WarpMan:resolved_args"] = int(
            self.reference_counts["resolved_args"]
        )
        out["WarpMan:missing_args"] = int(
            self.reference_counts["missing_args"]
        )
        return out


def _classify(
    *,
    new_warpman: bool,
    newtime_present: bool,
    free_present: bool,
    allfree_present: bool,
    payment_path_present: bool,
    money_present: bool,
    talk_event_present: bool,
    warp_msg_present: bool,
    over_marker_present: bool,
) -> str:
    if newtime_present:
        return TIME_GATED_DIALOGUE
    if new_warpman or talk_event_present or warp_msg_present or over_marker_present:
        return NEW_EVENT_GATED_DIALOGUE
    if payment_path_present or money_present:
        return DIALOGUE_OR_PAYMENT
    if free_present and allfree_present:
        return PLAIN_ALLFREE_DIALOGUE
    if free_present:
        return FREE_CONDITION_DIALOGUE
    return STRUCTURALLY_UNCLASSIFIED


def analyze(npc_dir: Path) -> WarpManGateAudit:
    reachability = load_ordered_runtime_reachability()
    reached = reachability.reached_floor_ids
    shadowed = tuple(row.floor_id for row in reachability.orphan_rows)
    shadowed_set = set(shadowed)

    files = sorted(
        (path for path in npc_dir.rglob("*") if path.is_file()),
        key=lambda path: str(path).lower(),
    )
    templates = template_map([
        path for path in files if magic_kind(path) == "template"
    ])
    names = {
        name
        for name, definitions in templates.items()
        if len(definitions) == 1 and definitions[0] == WARPMAN
    }

    counts = collections.Counter()
    rows: list[WarpManGateAuditRow] = []

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

            source_floor = _int(fields.get(b"floorid"), 0)
            if source_floor <= 0 or source_floor not in reached:
                continue
            if b"borncenter" not in fields and b"borncorner" not in fields:
                continue

            for value in enemies:
                template_name, separator, arg = value.partition(b"|")
                if template_name.strip() not in names:
                    continue
                counts["refs"] += 1

                filename = assigned_file(arg if separator else b"")
                if filename is None:
                    data = arg if separator else b""
                else:
                    path = npc_dir / filename
                    if not path.is_file():
                        counts["missing_args"] += 1
                        continue
                    data = merge_file(path)
                counts["resolved_args"] += 1

                tokens = _tokens(data)
                floors = _warp_floors(tokens)
                target_floors = tuple(
                    floor_id for floor_id in floors if floor_id in shadowed_set
                )
                if not target_floors:
                    continue

                free_values = _values(tokens, b"free")
                checkparty_values = _values(tokens, b"checkparty")
                new_warpman = b"NEWWARPMAN" in data.upper()
                newtime_present = bool(_values(tokens, b"newtime"))
                allfree_present = any(
                    b"ALLFREE" in value.upper() for value in free_values
                )
                payment_path_present = bool(_values(tokens, b"paymsg"))
                money_present = bool(_values(tokens, b"money"))
                talk_event_present = b"TALKEVENT" in data.upper()
                warp_msg_present = bool(_values(tokens, b"warp_msg"))
                over_marker_present = b"OVER" in data.upper()

                classification = _classify(
                    new_warpman=new_warpman,
                    newtime_present=newtime_present,
                    free_present=bool(free_values),
                    allfree_present=allfree_present,
                    payment_path_present=payment_path_present,
                    money_present=money_present,
                    talk_event_present=talk_event_present,
                    warp_msg_present=warp_msg_present,
                    over_marker_present=over_marker_present,
                )

                for target_floor in sorted(set(target_floors)):
                    rows.append(
                        WarpManGateAuditRow(
                            source_floor=source_floor,
                            target_floor=target_floor,
                            classification=classification,
                            target_candidate_count=sum(
                                floor_id == target_floor
                                for floor_id in floors
                            ),
                            total_warp_candidates=len(floors),
                            new_warpman=new_warpman,
                            newtime_present=newtime_present,
                            free_present=bool(free_values),
                            allfree_present=allfree_present,
                            payment_path_present=payment_path_present,
                            money_present=money_present,
                            checkparty_present=bool(checkparty_values),
                            checkparty_explicit_false=any(
                                _truthy_false(value)
                                for value in checkparty_values
                            ),
                            talk_event_present=talk_event_present,
                            warp_msg_present=warp_msg_present,
                            over_marker_present=over_marker_present,
                        )
                    )

    return WarpManGateAudit(
        rows=tuple(rows),
        reference_counts=counts,
        shadowed_branch_floor_ids=shadowed,
    )


def emit(audit: WarpManGateAudit) -> None:
    print("StoneAge shadowed-branch WarpMan gate audit — R1")
    print(
        "SCOPE|reachable recovered25 WarpMan instances targeting the "
        "11-floor classic-Warp shadowed branch|structural gates only"
    )
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print(
        "RULE|raw FREE/event/payment expressions and proprietary argument "
        "content are not emitted"
    )
    for key in sorted(audit.counts):
        print(f"COUNT|{key}|{audit.counts[key]}")

    for row in sorted(
        audit.rows,
        key=lambda item: (
            item.source_floor,
            item.target_floor,
            item.classification,
        ),
    ):
        print(
            "WARPMAN_INGRESS_GATE|"
            f"source_floor={row.source_floor}|"
            f"target_floor={row.target_floor}|"
            f"classification={row.classification}|"
            f"target_candidate_count={row.target_candidate_count}|"
            f"total_warp_candidates={row.total_warp_candidates}|"
            f"new_warpman={int(row.new_warpman)}|"
            f"newtime_present={int(row.newtime_present)}|"
            f"free_present={int(row.free_present)}|"
            f"allfree_present={int(row.allfree_present)}|"
            f"payment_path_present={int(row.payment_path_present)}|"
            f"money_present={int(row.money_present)}|"
            f"checkparty_present={int(row.checkparty_present)}|"
            f"checkparty_explicit_false={int(row.checkparty_explicit_false)}|"
            f"talk_event_present={int(row.talk_event_present)}|"
            f"warp_msg_present={int(row.warp_msg_present)}|"
            f"over_marker_present={int(row.over_marker_present)}"
        )

    print(OUTPUT_RESOLUTION)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--npc-dir", type=Path, required=True)
    args = parser.parse_args()
    emit(analyze(args.npc_dir))


if __name__ == "__main__":
    main()
