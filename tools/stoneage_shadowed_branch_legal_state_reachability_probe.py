#!/usr/bin/env python3
"""Join key-item acquisition, WarpMan gating and branch topology.

This probe answers a narrower but decisive question: does recovered25 contain a
single *legal character-state* witness that can receive the withheld key item
from a reachable ExChangeMan, travel through the ordered active classic-Warp
floor graph to the gated WarpMan, satisfy that WarpMan's FREE level/item
condition, enter the shadowed branch, and then reach the branch floors through
active classic Warps?

It deliberately does not claim a new-game progression proof. In particular,
Stone affordability is checked against the legal fixed-descendant carry domain,
not reconstructed from an initial-zero wallet through every earning source.
"""

from __future__ import annotations

import argparse
import collections
from dataclasses import dataclass
from pathlib import Path

from tools.stoneage_ordered_runtime_world_reachability_probe import (
    load_ordered_runtime_reachability,
)
from tools.stoneage_shadowed_branch_key_item_exchange_probe import (
    FIXED_DESCENDANT_ZERO_TRANS_MAX_GOLD,
    _economic_domain,
    _event_records,
    _item_terms,
    _record_award,
    _values,
)
from tools.stoneage_shadowed_branch_item_shop_acquisition_probe import (
    _locate_key_item,
)
from tools.stoneage_shadowed_branch_warpman_satisfiability_probe import (
    ITEM,
    LEVEL,
    _assigned_data,
    _compare,
    _configured_maxlevel,
    _field,
    _warp_floors,
    parse_free_predicates,
)
from tools.stoneage_transport_usage_probe import (
    iter_blocks,
    magic_kind,
    template_map,
)


OUTPUT_RESOLUTION = "RESOLUTION|SHADOWED_BRANCH_LEGAL_STATE_REACHABILITY_AUDITED"
CARRIED_ITEM_CAPACITY = 15


@dataclass(frozen=True)
class WarpGate:
    source_floor: int
    destination_floor: int
    joint_levels: tuple[int, ...]


@dataclass(frozen=True)
class ExchangeWitness:
    source_floor: int
    joint_level_count: int
    reward_units: int
    keyword_present: bool
    eventno_class: str
    floor_path_length_to_ingress: int
    state_domain_satisfiable: bool


@dataclass(frozen=True)
class ReachabilityChainAudit:
    gate: WarpGate
    exchange_witnesses: tuple[ExchangeWitness, ...]
    branch_floor_ids: tuple[int, ...]
    branch_reached_from_entry: tuple[int, ...]
    missing_argument_files: int

    @property
    def counts(self) -> dict[str, int]:
        out = collections.Counter({
            "exchange_witnesses": len(self.exchange_witnesses),
            "state_domain_satisfiable_exchange_witnesses": sum(
                x.state_domain_satisfiable for x in self.exchange_witnesses
            ),
            "exchange_source_floors": len({
                x.source_floor for x in self.exchange_witnesses
            }),
            "branch_floor_ids": len(self.branch_floor_ids),
            "branch_reached_from_entry": len(self.branch_reached_from_entry),
            "branch_unreached_from_entry": (
                len(self.branch_floor_ids) - len(self.branch_reached_from_entry)
            ),
            "missing_argument_files": int(self.missing_argument_files),
            "warp_joint_level_values": len(self.gate.joint_levels),
        })
        for row in self.exchange_witnesses:
            out[f"eventno:{row.eventno_class}:witnesses"] += 1
            out["keyword_present_witnesses"] += int(row.keyword_present)
            out["inventory_domain_satisfiable_witnesses"] += int(
                0 < row.reward_units <= CARRIED_ITEM_CAPACITY
            )
            out["floor_path_witnesses"] += int(
                row.floor_path_length_to_ingress >= 0
            )
            out["joint_level_exchange_witnesses"] += int(
                row.joint_level_count > 0
            )
        return dict(out)


def _adjacency(runtime) -> dict[int, set[int]]:
    out: dict[int, set[int]] = collections.defaultdict(set)
    for edge in runtime.topology.legacy_warps:
        out[int(edge.source.floor_id)].add(int(edge.destination.floor_id))
    return out


def _distance(adjacency: dict[int, set[int]], start: int, goal: int) -> int:
    start = int(start)
    goal = int(goal)
    if start == goal:
        return 0
    queue = collections.deque([(start, 0)])
    seen = {start}
    while queue:
        floor, depth = queue.popleft()
        for dest in sorted(adjacency.get(floor, ())):
            if dest == goal:
                return depth + 1
            if dest in seen:
                continue
            seen.add(dest)
            queue.append((dest, depth + 1))
    return -1


def _reachable(adjacency: dict[int, set[int]], start: int) -> set[int]:
    queue = collections.deque([int(start)])
    seen = {int(start)}
    while queue:
        floor = queue.popleft()
        for dest in adjacency.get(floor, ()):
            if dest in seen:
                continue
            seen.add(dest)
            queue.append(dest)
    return seen


def _warp_gate_levels(npc_dir: Path, maxlevel: int) -> tuple[WarpGate, int]:
    audit = load_ordered_runtime_reachability()
    reached = set(audit.reached_floor_ids)
    branch = {row.floor_id for row in audit.orphan_rows}
    target_item, missing = _locate_key_item(npc_dir)

    files = sorted(
        (path for path in npc_dir.rglob("*") if path.is_file()),
        key=lambda path: str(path).lower(),
    )
    templates = template_map([
        path for path in files if magic_kind(path) == "template"
    ])
    warpman_names = {
        name for name, defs in templates.items()
        if len(defs) == 1 and defs[0].strip().lower() == b"warpman"
    }

    gates = []
    for create in (p for p in files if magic_kind(p) == "create"):
        for entries in iter_blocks(create):
            fields = {}
            enemies = []
            for key, value in entries:
                if key == b"enemy":
                    enemies.append(value)
                else:
                    fields[key] = value
            try:
                floor = int(fields.get(b"floorid", b"0"))
            except ValueError:
                continue
            if floor not in reached:
                continue
            if b"borncenter" not in fields and b"borncorner" not in fields:
                continue
            for enemy in enemies:
                name, sep, arg = enemy.partition(b"|")
                if name.strip() not in warpman_names:
                    continue
                data = _assigned_data(npc_dir, arg if sep else b"")
                if data is None:
                    missing += 1
                    continue
                destinations = sorted(set(_warp_floors(data)) & branch)
                if not destinations:
                    continue
                free = _field(data, b"FREE")
                if free is None:
                    continue
                clauses = parse_free_predicates(free)

                # Current recovered ingress is expected to use exactly the
                # withheld target item as its ITEM equality witness. Refuse to
                # generalize silently if the specimen changes.
                item_atoms = [
                    atom for clause in clauses for atom in clause
                    if atom is not None and atom.key == ITEM
                ]
                if len(item_atoms) != 1:
                    raise ValueError("expected one ITEM atom in shadowed ingress")
                item_atom = item_atoms[0]
                if item_atom.operator != "=" or item_atom.operand != target_item:
                    raise ValueError("shadowed ingress ITEM predicate drift")

                levels = []
                for level in range(1, maxlevel + 1):
                    clause_ok = False
                    for clause in clauses:
                        atoms_ok = True
                        for atom in clause:
                            if atom is None:
                                atoms_ok = False
                                break
                            if atom.key == LEVEL:
                                atoms_ok &= _compare(
                                    level, atom.operator, atom.operand
                                )
                            elif atom.key == ITEM:
                                atoms_ok &= (
                                    atom.operator == "="
                                    and atom.operand == target_item
                                )
                            else:
                                atoms_ok = False
                            if not atoms_ok:
                                break
                        if atoms_ok:
                            clause_ok = True
                            break
                    if clause_ok:
                        levels.append(level)
                for destination in destinations:
                    gates.append(
                        WarpGate(
                            source_floor=floor,
                            destination_floor=int(destination),
                            joint_levels=tuple(levels),
                        )
                    )

    if len(gates) != 1:
        raise ValueError("expected exactly one shadowed-branch WarpMan gate")
    if not gates[0].joint_levels:
        raise ValueError("shadowed WarpMan gate has no legal level witness")
    return gates[0], missing


def _eventno_class(record: bytes) -> str:
    values = _values(record, b"EventNo")
    if len(values) != 1:
        return "MISSING_OR_MULTIPLE"
    raw = values[0].strip()
    if b"-" in raw:
        return "NEGATIVE_SENTINEL"
    try:
        value = int(raw or b"0")
    except ValueError:
        return "UNPARSEABLE"
    return "NONNEGATIVE_FLAG" if value >= 0 else "NEGATIVE_SENTINEL"


def _event_gate_domain_satisfiable(event_class: str) -> bool:
    """Whether EventNo admits at least one legal player event-flag state.

    Fixed descendant npcutil.c treats shiftbit == -1 as an explicit ungated
    sentinel: NPC_EventCheckFlg returns FALSE and event setters ignore it.
    A nonnegative event flag likewise admits the ordinary "not completed yet"
    state.  Malformed/missing event numbers remain unsupported here.
    """
    return event_class in {"NEGATIVE_SENTINEL", "NONNEGATIVE_FLAG"}


def _reward_units(record: bytes, target: int) -> int:
    total = 0
    for value in _values(record, b"GetItem"):
        for item, qty in _item_terms(value):
            if int(item) == int(target):
                total += int(qty)
    return total


def _matching_exchange_records(
    npc_dir: Path,
    setup: Path,
    gate: WarpGate,
    adjacency: dict[int, set[int]],
) -> tuple[tuple[ExchangeWitness, ...], int]:
    target, missing = _locate_key_item(npc_dir)
    maxlevel = _configured_maxlevel(setup)
    reached = set(load_ordered_runtime_reachability().reached_floor_ids)

    files = sorted(
        (path for path in npc_dir.rglob("*") if path.is_file()),
        key=lambda path: str(path).lower(),
    )
    templates = template_map([
        path for path in files if magic_kind(path) == "template"
    ])
    exchange_names = {
        name for name, defs in templates.items()
        if len(defs) == 1 and defs[0].strip().lower() == b"exchangeman"
    }

    rows = []
    for create in (p for p in files if magic_kind(p) == "create"):
        for entries in iter_blocks(create):
            fields = {}
            enemies = []
            for key, value in entries:
                if key == b"enemy":
                    enemies.append(value)
                else:
                    fields[key] = value
            try:
                floor = int(fields.get(b"floorid", b"0"))
            except ValueError:
                continue
            if floor not in reached:
                continue
            if b"borncenter" not in fields and b"borncorner" not in fields:
                continue
            for enemy in enemies:
                name, sep, arg = enemy.partition(b"|")
                if name.strip() not in exchange_names:
                    continue
                data = _assigned_data(npc_dir, arg if sep else b"")
                if data is None:
                    missing += 1
                    continue
                for record in _event_records(data):
                    award = _record_award(record, target, floor, maxlevel)
                    if award is None or award.type_class != "ACCEPT":
                        continue

                    level_ok, affordable, _cost_class = _economic_domain(
                        record, maxlevel
                    )
                    if not level_ok:
                        continue
                    event_levels = set()
                    # _record_award already classifies current records as LV-only
                    # through level_domain_satisfiable. Re-evaluate by brute force
                    # using the same helper's economic predicate surface: a level
                    # is eligible if substituting it leaves all LV atoms true.
                    for level in range(1, maxlevel + 1):
                        # Reuse the private level witness helper lazily to avoid
                        # publishing operands in output.
                        from tools.stoneage_shadowed_branch_key_item_exchange_probe import _level_witnesses
                        if level in _level_witnesses(record, maxlevel):
                            event_levels.add(level)

                    joint = sorted(event_levels & set(gate.joint_levels))
                    reward_units = _reward_units(record, target)
                    distance = _distance(adjacency, floor, gate.source_floor)
                    event_class = _eventno_class(record)
                    keyword_present = bool(_values(record, b"KeyWord"))
                    state_ok = (
                        bool(joint)
                        and bool(affordable)
                        and not award.target_required_by_event
                        and not award.target_deleted
                        and award.other_item_prerequisite_refs == 0
                        and not award.delpet_present
                        and 0 < reward_units <= CARRIED_ITEM_CAPACITY
                        and _event_gate_domain_satisfiable(event_class)
                        and distance >= 0
                    )
                    rows.append(
                        ExchangeWitness(
                            source_floor=floor,
                            joint_level_count=len(joint),
                            reward_units=reward_units,
                            keyword_present=keyword_present,
                            eventno_class=event_class,
                            floor_path_length_to_ingress=distance,
                            state_domain_satisfiable=state_ok,
                        )
                    )

    return tuple(rows), missing


def analyze(npc_dir: Path, setup: Path) -> ReachabilityChainAudit:
    maxlevel = _configured_maxlevel(setup)
    gate, missing_gate = _warp_gate_levels(npc_dir, maxlevel)
    reach = load_ordered_runtime_reachability()
    adjacency = _adjacency(reach.runtime)

    exchange, missing_exchange = _matching_exchange_records(
        npc_dir, setup, gate, adjacency
    )

    branch = tuple(sorted(row.floor_id for row in reach.orphan_rows))
    branch_reach = _reachable(adjacency, gate.destination_floor)
    branch_reached = tuple(sorted(set(branch) & branch_reach))

    return ReachabilityChainAudit(
        gate=gate,
        exchange_witnesses=exchange,
        branch_floor_ids=branch,
        branch_reached_from_entry=branch_reached,
        missing_argument_files=missing_gate + missing_exchange,
    )


def emit(audit: ReachabilityChainAudit) -> None:
    print("StoneAge shadowed-branch legal-state reachability audit — R1")
    print(
        "SCOPE|reachable ExChangeMan key-item award -> ordered classic-Warp "
        "floor path -> gated WarpMan -> branch classic-Warp closure"
    )
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print(
        "RULE|all key-item IDs, level thresholds, Stone costs, event numbers, "
        "NPC names, coordinates, filenames and raw arguments are withheld"
    )
    print(
        "RULE|this is legal-state reachability, not a new-character progression "
        "proof; Stone is witnessed inside the legal carry domain rather than "
        "derived from an initial wallet"
    )
    print(
        "RULE|floor paths use ordered active classic-Warp connectivity; "
        "same-floor collision/pathfinding to individual NPC cells is not proven"
    )
    print(
        f"WARP_GATE|source_floor={audit.gate.source_floor}|"
        f"entry_floor={audit.gate.destination_floor}|"
        f"legal_level_values={len(audit.gate.joint_levels)}"
    )
    for key in sorted(audit.counts):
        print(f"COUNT|{key}|{audit.counts[key]}")
    for i, row in enumerate(audit.exchange_witnesses, 1):
        print(
            "EXCHANGE_CHAIN_WITNESS|"
            f"ordinal={i}|source_floor={row.source_floor}|"
            f"joint_level_values={row.joint_level_count}|"
            f"reward_units={row.reward_units}|"
            f"keyword_present={int(row.keyword_present)}|"
            f"eventno_class={row.eventno_class}|"
            f"classic_warp_hops_to_gate={row.floor_path_length_to_ingress}|"
            f"state_domain_satisfiable={int(row.state_domain_satisfiable)}"
        )
    print(
        "BRANCH_CLOSURE|"
        f"entry_floor={audit.gate.destination_floor}|"
        f"target_floors={len(audit.branch_floor_ids)}|"
        f"reachable_target_floors={len(audit.branch_reached_from_entry)}|"
        f"all_target_floors_reachable={int(set(audit.branch_floor_ids) == set(audit.branch_reached_from_entry))}"
    )
    print(
        "LEGAL_STATE_CHAIN|"
        f"witness={int(any(x.state_domain_satisfiable for x in audit.exchange_witnesses) and set(audit.branch_floor_ids) == set(audit.branch_reached_from_entry))}|"
        f"gold_cap_domain={FIXED_DESCENDANT_ZERO_TRANS_MAX_GOLD}|"
        "item_id_withheld=1"
    )
    print(OUTPUT_RESOLUTION)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--npc-dir", type=Path, required=True)
    parser.add_argument("--setup", type=Path, required=True)
    args = parser.parse_args()
    emit(analyze(args.npc_dir, args.setup))


if __name__ == "__main__":
    main()
