#!/usr/bin/env python3
"""Join key-item acquisition, directed travel and WarpMan gate into one witness.

This probe deliberately proves a *legal player-state progression witness*, not
fresh-character economic provenance.  It joins:

stable/classic reachability
 -> reachable ExChangeMan award of the withheld key item
 -> a directed classic-Warp path from award floor to the WarpMan floor
 -> a non-decreasing player-level witness
 -> WarpMan 811 -> orphan-branch ingress
 -> classic-Warp closure reachable after entering the branch.

Raw item IDs, level thresholds, stone costs, NPC names, coordinates, dialogue
and original argument payloads are used transiently and never emitted.
"""

from __future__ import annotations

import argparse
import collections
from dataclasses import dataclass
from pathlib import Path

from tools.stoneage_ordered_runtime_world_reachability_probe import (
    load_ordered_runtime_reachability,
)
from tools.stoneage_shadowed_branch_item_shop_acquisition_probe import (
    _locate_key_item,
)
from tools.stoneage_shadowed_branch_key_item_exchange_probe import (
    FIXED_DESCENDANT_ZERO_TRANS_MAX_GOLD,
    _delstone_cost,
    _event_is_lv_only,
    _event_records,
    _item_terms,
    _level_witnesses,
    _record_award,
    _values,
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


OUTPUT_RESOLUTION = "RESOLUTION|SHADOWED_BRANCH_PROGRESSION_WITNESS_CLOSED"


@dataclass(frozen=True)
class IngressGate:
    source_floor: int
    destination_floor: int
    free: bytes


@dataclass(frozen=True)
class AwardProgression:
    floor_id: int
    affordable_level_count: int
    classic_hops_to_ingress: int | None
    same_level_witness: bool
    nondecreasing_level_witness: bool


@dataclass(frozen=True)
class BranchClosure:
    ingress_floor: int
    orphan_reached: tuple[int, ...]
    orphan_total: int
    returns_to_preexisting_reached: bool
    max_classic_depth_from_ingress: int


@dataclass(frozen=True)
class ProgressionAudit:
    ingress: IngressGate
    award_rows: tuple[AwardProgression, ...]
    warp_level_witness_count: int
    branch: BranchClosure
    missing_argument_files: int

    @property
    def combined_witness(self) -> bool:
        return any(
            row.classic_hops_to_ingress is not None
            and row.nondecreasing_level_witness
            for row in self.award_rows
        )

    @property
    def counts(self) -> dict[str, int]:
        return {
            "award_records": len(self.award_rows),
            "award_records_with_affordable_level_state": sum(
                row.affordable_level_count > 0 for row in self.award_rows
            ),
            "award_records_with_classic_path_to_ingress": sum(
                row.classic_hops_to_ingress is not None
                for row in self.award_rows
            ),
            "award_records_with_same_level_witness": sum(
                row.same_level_witness for row in self.award_rows
            ),
            "award_records_with_nondecreasing_level_witness": sum(
                row.nondecreasing_level_witness for row in self.award_rows
            ),
            "warp_level_witness_states": int(self.warp_level_witness_count),
            "combined_progression_witness": int(self.combined_witness),
            "branch_orphan_floors_reached": len(self.branch.orphan_reached),
            "branch_orphan_floors_total": int(self.branch.orphan_total),
            "branch_full_orphan_closure": int(
                len(self.branch.orphan_reached) == self.branch.orphan_total
            ),
            "branch_returns_to_preexisting_reached": int(
                self.branch.returns_to_preexisting_reached
            ),
            "missing_argument_files": int(self.missing_argument_files),
        }


def _adjacency(runtime) -> dict[int, tuple[int, ...]]:
    out: dict[int, set[int]] = collections.defaultdict(set)
    for edge in runtime.topology.legacy_warps:
        out[int(edge.source.floor_id)].add(int(edge.destination.floor_id))
    return {
        floor: tuple(sorted(destinations))
        for floor, destinations in out.items()
    }


def _shortest_floor_hops(runtime, start: int, target: int) -> int | None:
    start=int(start); target=int(target)
    if start == target:
        return 0
    graph=_adjacency(runtime)
    distance={start:0}
    queue=[start]
    for floor in queue:
        for destination in graph.get(floor,()):
            if destination in distance:
                continue
            distance[destination]=distance[floor]+1
            if destination==target:
                return distance[destination]
            queue.append(destination)
    return None


def _closure_from_ingress(
    runtime,
    *,
    ingress_floor: int,
    orphan_ids: set[int],
    preexisting_reached: set[int],
) -> BranchClosure:
    graph=_adjacency(runtime)
    depth={int(ingress_floor):0}
    queue=[int(ingress_floor)]
    returns=False
    for floor in queue:
        for destination in graph.get(floor,()):
            if destination in preexisting_reached:
                returns=True
            if destination in depth:
                continue
            depth[destination]=depth[floor]+1
            queue.append(destination)
    reached=tuple(sorted(orphan_ids & set(depth)))
    return BranchClosure(
        ingress_floor=int(ingress_floor),
        orphan_reached=reached,
        orphan_total=len(orphan_ids),
        returns_to_preexisting_reached=returns,
        max_classic_depth_from_ingress=max(depth.values(),default=0),
    )


def _template_names(
    npc_dir: Path,
    function_set: bytes,
) -> set[bytes]:
    files=sorted(
        (path for path in npc_dir.rglob("*") if path.is_file()),
        key=lambda path:str(path).lower(),
    )
    templates=template_map([
        path for path in files if magic_kind(path)=="template"
    ])
    wanted=function_set.strip().lower()
    return {
        name for name,definitions in templates.items()
        if len(definitions)==1
        and definitions[0].strip().lower()==wanted
    }


def _locate_ingress_gate(
    npc_dir: Path,
    *,
    reached: set[int],
    orphan_ids: set[int],
) -> tuple[IngressGate, int]:
    warpman_names=_template_names(npc_dir,b"WarpMan")
    files=sorted(
        (path for path in npc_dir.rglob("*") if path.is_file()),
        key=lambda path:str(path).lower(),
    )
    rows=[];missing=0
    for create in (path for path in files if magic_kind(path)=="create"):
        for entries in iter_blocks(create):
            fields={};enemies=[]
            for key,value in entries:
                if key==b"enemy":
                    enemies.append(value)
                else:
                    fields[key]=value
            try:
                floor=int(fields.get(b"floorid",b"0"))
            except ValueError:
                continue
            if floor not in reached:
                continue
            if b"borncenter" not in fields and b"borncorner" not in fields:
                continue
            for enemy in enemies:
                name,separator,arg=enemy.partition(b"|")
                if name.strip() not in warpman_names:
                    continue
                data=_assigned_data(npc_dir,arg if separator else b"")
                if data is None:
                    missing+=1
                    continue
                destinations=sorted(set(_warp_floors(data)) & orphan_ids)
                if not destinations:
                    continue
                free=_field(data,b"FREE")
                if free is None:
                    continue
                for destination in destinations:
                    rows.append(IngressGate(
                        source_floor=floor,
                        destination_floor=int(destination),
                        free=free,
                    ))
    unique={(row.source_floor,row.destination_floor,row.free):row for row in rows}
    if len(unique)!=1:
        raise ValueError(
            "expected exactly one unique reachable WarpMan orphan ingress"
        )
    return next(iter(unique.values())),missing


def _warp_level_witnesses(
    free: bytes,
    *,
    target_item: int,
    maxlevel: int,
) -> tuple[int, ...]:
    clauses=parse_free_predicates(free)
    levels=[]
    for level in range(1,int(maxlevel)+1):
        clause_ok=False
        for clause in clauses:
            atoms_ok=True
            has_target_item=False
            for atom in clause:
                if atom is None:
                    atoms_ok=False
                    break
                if atom.key==LEVEL:
                    if not _compare(level,atom.operator,atom.operand):
                        atoms_ok=False
                        break
                elif atom.key==ITEM:
                    if atom.operator=="=" and atom.operand==target_item:
                        has_target_item=True
                    else:
                        atoms_ok=False
                        break
                else:
                    atoms_ok=False
                    break
            if atoms_ok and has_target_item:
                clause_ok=True
                break
        if clause_ok:
            levels.append(level)
    return tuple(levels)


def _affordable_award_levels(
    record: bytes,
    *,
    target_item: int,
    maxlevel: int,
) -> tuple[int, ...]:
    award=_record_award(record,target_item,0,maxlevel)
    if award is None:
        return ()
    if award.type_class!="ACCEPT":
        return ()
    if award.target_required_by_event or award.target_deleted:
        return ()
    if award.other_item_prerequisite_refs or award.delpet_present:
        return ()
    if not _event_is_lv_only(record):
        return ()

    levels=_level_witnesses(record,maxlevel)
    delstone=_values(record,b"DelStone")
    if not delstone:
        return tuple(levels)
    if len(delstone)!=1:
        return ()

    affordable=[]
    for level in levels:
        cost=_delstone_cost(delstone[0],level)
        if (
            cost is not None
            and 0 <= cost <= FIXED_DESCENDANT_ZERO_TRANS_MAX_GOLD
        ):
            affordable.append(int(level))
    return tuple(affordable)


def _award_records(
    npc_dir: Path,
    *,
    target_item: int,
    maxlevel: int,
    reached: set[int],
) -> tuple[tuple[int,bytes,tuple[int,...]], ...]:
    exchange_names=_template_names(npc_dir,b"ExChangeMan")
    files=sorted(
        (path for path in npc_dir.rglob("*") if path.is_file()),
        key=lambda path:str(path).lower(),
    )
    rows=[]
    for create in (path for path in files if magic_kind(path)=="create"):
        for entries in iter_blocks(create):
            fields={};enemies=[]
            for key,value in entries:
                if key==b"enemy":
                    enemies.append(value)
                else:
                    fields[key]=value
            try:
                floor=int(fields.get(b"floorid",b"0"))
            except ValueError:
                continue
            if floor not in reached:
                continue
            if b"borncenter" not in fields and b"borncorner" not in fields:
                continue
            for enemy in enemies:
                name,separator,arg=enemy.partition(b"|")
                if name.strip() not in exchange_names:
                    continue
                data=_assigned_data(npc_dir,arg if separator else b"")
                if data is None:
                    continue
                for record in _event_records(data):
                    getitems=_values(record,b"GetItem")
                    reward_ids={
                        item
                        for value in getitems
                        for item,_quantity in _item_terms(value)
                    }
                    if target_item not in reward_ids:
                        continue
                    levels=_affordable_award_levels(
                        record,
                        target_item=target_item,
                        maxlevel=maxlevel,
                    )
                    rows.append((floor,record,levels))
    return tuple(rows)


def _has_nondecreasing_pair(
    acquisition_levels: tuple[int,...],
    warp_levels: tuple[int,...],
) -> bool:
    return any(
        acquisition <= warp
        for acquisition in acquisition_levels
        for warp in warp_levels
    )


def analyze(npc_dir: Path, setup: Path) -> ProgressionAudit:
    reachability=load_ordered_runtime_reachability()
    reached=set(reachability.reached_floor_ids)
    orphan_ids={row.floor_id for row in reachability.orphan_rows}
    maxlevel=_configured_maxlevel(setup)
    target_item,locate_missing=_locate_key_item(npc_dir)

    ingress,ingress_missing=_locate_ingress_gate(
        npc_dir,
        reached=reached,
        orphan_ids=orphan_ids,
    )
    warp_levels=_warp_level_witnesses(
        ingress.free,
        target_item=target_item,
        maxlevel=maxlevel,
    )
    if not warp_levels:
        raise ValueError("WarpMan ingress has no joined target-item level witness")

    awards=_award_records(
        npc_dir,
        target_item=target_item,
        maxlevel=maxlevel,
        reached=reached,
    )
    progress=[]
    for floor,_record,levels in awards:
        hops=_shortest_floor_hops(
            reachability.runtime,
            floor,
            ingress.source_floor,
        )
        progress.append(AwardProgression(
            floor_id=int(floor),
            affordable_level_count=len(levels),
            classic_hops_to_ingress=hops,
            same_level_witness=bool(set(levels) & set(warp_levels)),
            nondecreasing_level_witness=_has_nondecreasing_pair(
                levels,
                warp_levels,
            ),
        ))

    branch=_closure_from_ingress(
        reachability.runtime,
        ingress_floor=ingress.destination_floor,
        orphan_ids=orphan_ids,
        preexisting_reached=reached,
    )
    return ProgressionAudit(
        ingress=ingress,
        award_rows=tuple(progress),
        warp_level_witness_count=len(warp_levels),
        branch=branch,
        missing_argument_files=locate_missing+ingress_missing,
    )


def emit(audit: ProgressionAudit) -> None:
    print("StoneAge shadowed-branch joined progression witness — R1")
    print(
        "SCOPE|reachable exchange award -> directed classic Warp travel -> "
        "WarpMan gate -> post-ingress classic closure"
    )
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print(
        "RULE|item IDs, level thresholds, exact witness levels, stone costs, "
        "NPC names, coordinates, dialogue and raw arguments are withheld"
    )
    print(
        "RULE|player level is treated as non-decreasing between acquisition and "
        "WarpMan use; a same-level witness is reported separately"
    )
    print(
        "RULE|stone affordability proves a legal carried-gold state under the "
        "pinned zero-trans cap; how a fresh character earns that fee is outside "
        "this probe"
    )
    for key in sorted(audit.counts):
        print(f"COUNT|{key}|{audit.counts[key]}")

    hop_values=[
        row.classic_hops_to_ingress
        for row in audit.award_rows
        if row.classic_hops_to_ingress is not None
    ]
    print(
        "PROGRESSION_WITNESS|"
        f"acquisition_source_floors={len({row.floor_id for row in audit.award_rows})}|"
        f"ingress_source_floor={audit.ingress.source_floor}|"
        f"ingress_target_floor={audit.ingress.destination_floor}|"
        f"classic_path_after_acquisition={int(bool(hop_values))}|"
        f"min_classic_hops={min(hop_values) if hop_values else -1}|"
        f"same_level_witness={int(any(row.same_level_witness for row in audit.award_rows))}|"
        f"nondecreasing_level_witness={int(any(row.nondecreasing_level_witness for row in audit.award_rows))}|"
        f"combined_state_progression_witness={int(audit.combined_witness)}"
    )
    print(
        "POST_INGRESS_CLASSIC_CLOSURE|"
        f"ingress_floor={audit.branch.ingress_floor}|"
        f"orphan_reached={len(audit.branch.orphan_reached)}|"
        f"orphan_total={audit.branch.orphan_total}|"
        f"max_depth={audit.branch.max_classic_depth_from_ingress}|"
        f"returns_to_preexisting_reached={int(audit.branch.returns_to_preexisting_reached)}|"
        "floors="+(
            ",".join(map(str,audit.branch.orphan_reached))
            if audit.branch.orphan_reached else "NONE"
        )
    )
    print(OUTPUT_RESOLUTION)


def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument("--npc-dir",type=Path,required=True)
    parser.add_argument("--setup",type=Path,required=True)
    args=parser.parse_args()
    emit(analyze(args.npc_dir,args.setup))


if __name__=="__main__":
    main()
