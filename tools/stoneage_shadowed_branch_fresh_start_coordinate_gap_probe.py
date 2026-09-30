#!/usr/bin/env python3
"""Classify why normal hometown coordinate chains diverge from floor reachability.

The existing fresh-start coordinate audit proves only 2/4 normal hometowns can
reach the award interaction component although all 4/4 hometown floors have a
classic-Warp floor path.  This diagnostic keeps the same recovered LS2MAP,
mapset, diagonal movement and NPC-blocker semantics, then measures the closest
coordinate state to the award in the floor-only graph.

For a failed hometown, the closest frontier is classified without exposing
floor IDs or coordinates:
- CLASSIC_WARP_SOURCE_COMPONENT_DISCONNECTED: a floor-progressing Warp exists,
  but its source cell is not in the player's reachable walk component;
- CLASSIC_WARP_DESTINATION_INVALID: the source is reachable but its recovered
  destination cell is not a legal coordinate state;
- AWARD_LOCAL_COMPONENT_MISMATCH: the award floor is reached, but not the
  interaction component;
- MIXED_CLASSIC_FRONTIER / NO_CLASSIC_PROGRESS_EDGE / START_INVALID for the
  corresponding conservative boundary cases.

Both baseline conservative-NPC and static-only variants are reported so a
static topology gap is not misattributed to dynamic occupancy.
"""

from __future__ import annotations

import argparse
import collections
from dataclasses import dataclass
from pathlib import Path

from tools.stoneage_ordered_runtime_world_reachability_probe import (
    load_ordered_runtime_reachability,
)
from tools.stoneage_server_static_map import parse_mapset_collision_profile
from tools.stoneage_shadowed_branch_coordinate_access_probe import (
    _conservative_npc_birth_blockers,
    _interaction_cells,
    _matching_award_placements,
)
from tools.stoneage_shadowed_branch_fresh_start_coordinate_probe import (
    FloorComponents,
    NORMAL_HOMETOWN_SPAWNS,
    _select_from_catalog,
    _server_catalog,
    _warp_edges,
)
from tools.stoneage_shadowed_branch_item_shop_acquisition_probe import (
    _locate_key_item,
)
from tools.stoneage_shadowed_branch_progression_witness_probe import (
    _award_records,
)
from tools.stoneage_shadowed_branch_warpman_satisfiability_probe import (
    _configured_maxlevel,
)


OUTPUT_RESOLUTION=(
    "RESOLUTION|SHADOWED_BRANCH_FRESH_START_COORDINATE_GAP_CLASSIFIED"
)


@dataclass(frozen=True)
class GapWitness:
    ordinal:int
    reachable:bool
    reason:str
    min_floor_hops_remaining:int|None
    closest_frontier_source_disconnected:int
    closest_frontier_destination_invalid:int
    closest_frontier_usable:int
    award_floor_component_reached:bool


@dataclass(frozen=True)
class GapPair:
    baseline:GapWitness
    static_only:GapWitness


@dataclass(frozen=True)
class CoordinateGapAudit:
    rows:tuple[GapPair,...]


def _reverse_floor_distances(edges,award_floor:int)->dict[int,int]:
    incoming:dict[int,set[int]]=collections.defaultdict(set)
    for edge in edges:
        incoming[int(edge.destination_floor)].add(int(edge.source_floor))
    dist={int(award_floor):0}
    queue=collections.deque([int(award_floor)])
    while queue:
        floor=queue.popleft()
        for source in incoming.get(floor,()):
            if source in dist:
                continue
            dist[source]=dist[floor]+1
            queue.append(source)
    return dist


def _frontier_reason(
    *,
    min_remaining:int|None,
    source_disconnected:int,
    destination_invalid:int,
    usable:int,
    start_valid:bool,
)->str:
    if not start_valid:
        return "START_INVALID"
    if min_remaining==0:
        return "AWARD_LOCAL_COMPONENT_MISMATCH"
    if usable>0:
        return "INTERNAL_DIAGNOSTIC_INCONSISTENCY"
    if source_disconnected>0 and destination_invalid==0:
        return "CLASSIC_WARP_SOURCE_COMPONENT_DISCONNECTED"
    if destination_invalid>0 and source_disconnected==0:
        return "CLASSIC_WARP_DESTINATION_INVALID"
    if source_disconnected>0 or destination_invalid>0:
        return "MIXED_CLASSIC_FRONTIER"
    return "NO_CLASSIC_PROGRESS_EDGE"


def _one(
    *,
    ordinal:int,
    spawn:tuple[int,int,int],
    award_floor:int,
    award_goals:set[tuple[int,int]],
    floor_dist:dict[int,int],
    warps_by_floor:dict[int,tuple],
    catalog,
    mapset,
    blockers:dict[int,frozenset[tuple[int,int]]],
)->GapWitness:
    start_floor,start_x,start_y=map(int,spawn)
    navs={}
    admitted={start_floor:frozenset({(start_x,start_y)})}

    def nav(floor:int):
        floor=int(floor)
        if floor in navs:
            return navs[floor]
        selected=_select_from_catalog(catalog,mapset,floor)
        if selected.static_map is None:
            navs[floor]=None
            return None
        row=FloorComponents(
            selected.static_map,
            blockers.get(floor,frozenset()),
            admitted_origins=admitted.get(floor,frozenset()),
        )
        navs[floor]=row
        return row

    start_nav=nav(start_floor)
    start_component=(
        start_nav.component((start_x,start_y))
        if start_nav is not None else None
    )
    if start_component is None:
        return GapWitness(
            ordinal=ordinal,
            reachable=False,
            reason="START_INVALID",
            min_floor_hops_remaining=floor_dist.get(start_floor),
            closest_frontier_source_disconnected=0,
            closest_frontier_destination_invalid=0,
            closest_frontier_usable=0,
            award_floor_component_reached=False,
        )

    queue=collections.deque([(start_floor,start_component)])
    seen={(start_floor,start_component)}
    award_floor_component_reached=False
    while queue:
        floor,component=queue.popleft()
        current_nav=nav(floor)
        if current_nav is None:
            continue
        if floor==award_floor:
            award_floor_component_reached=True
            if any(current_nav.component(goal)==component for goal in award_goals):
                return GapWitness(
                    ordinal=ordinal,
                    reachable=True,
                    reason="CLOSED",
                    min_floor_hops_remaining=0,
                    closest_frontier_source_disconnected=0,
                    closest_frontier_destination_invalid=0,
                    closest_frontier_usable=0,
                    award_floor_component_reached=True,
                )
        for edge in warps_by_floor.get(floor,()):
            if current_nav.component(
                (int(edge.source_x),int(edge.source_y))
            ) != component:
                continue
            dest_nav=nav(int(edge.destination_floor))
            if dest_nav is None:
                continue
            dest_component=dest_nav.component(
                (int(edge.destination_x),int(edge.destination_y))
            )
            if dest_component is None:
                continue
            state=(int(edge.destination_floor),dest_component)
            if state in seen:
                continue
            seen.add(state)
            queue.append(state)

    finite=[floor_dist[floor] for floor,_comp in seen if floor in floor_dist]
    min_remaining=min(finite) if finite else None
    source_disconnected=0
    destination_invalid=0
    usable=0
    if min_remaining is not None and min_remaining>0:
        for floor,component in seen:
            if floor_dist.get(floor)!=min_remaining:
                continue
            current_nav=nav(floor)
            if current_nav is None:
                continue
            for edge in warps_by_floor.get(floor,()):
                dest_floor=int(edge.destination_floor)
                if floor_dist.get(dest_floor,min_remaining)>=min_remaining:
                    continue
                source_component=current_nav.component(
                    (int(edge.source_x),int(edge.source_y))
                )
                if source_component!=component:
                    source_disconnected+=1
                    continue
                dest_nav=nav(dest_floor)
                dest_component=(
                    dest_nav.component(
                        (int(edge.destination_x),int(edge.destination_y))
                    )
                    if dest_nav is not None else None
                )
                if dest_component is None:
                    destination_invalid+=1
                else:
                    usable+=1

    return GapWitness(
        ordinal=ordinal,
        reachable=False,
        reason=_frontier_reason(
            min_remaining=min_remaining,
            source_disconnected=source_disconnected,
            destination_invalid=destination_invalid,
            usable=usable,
            start_valid=True,
        ),
        min_floor_hops_remaining=min_remaining,
        closest_frontier_source_disconnected=source_disconnected,
        closest_frontier_destination_invalid=destination_invalid,
        closest_frontier_usable=usable,
        award_floor_component_reached=award_floor_component_reached,
    )


def analyze(
    *,
    npc_dir:Path,
    setup:Path,
    server_map_root:Path,
    mapset_path:Path,
)->CoordinateGapAudit:
    runtime_audit=load_ordered_runtime_reachability()
    runtime=runtime_audit.runtime
    reached=set(runtime_audit.reached_floor_ids)
    target,_missing=_locate_key_item(npc_dir)
    maxlevel=_configured_maxlevel(setup)
    accepted=_award_records(
        npc_dir,target_item=target,maxlevel=maxlevel,reached=reached
    )
    accepted_records={(int(floor),record) for floor,record,_levels in accepted}
    award_floors={int(floor) for floor,_record,_levels in accepted}
    if len(award_floors)!=1:
        raise ValueError("award floor identity is not unique")
    award_floor=next(iter(award_floors))
    awards=_matching_award_placements(npc_dir,accepted_records)
    if not awards:
        raise ValueError("award placements missing")

    catalog=_server_catalog(server_map_root)
    mapset=parse_mapset_collision_profile(mapset_path.read_bytes())
    award_selection=_select_from_catalog(catalog,mapset,award_floor)
    if award_selection.static_map is None:
        raise ValueError("award floor static map unavailable")
    award_goals=_interaction_cells(award_selection.static_map,awards)
    if not award_goals:
        raise ValueError("award interaction cells missing")

    edges=_warp_edges(runtime)
    floor_dist=_reverse_floor_distances(edges,award_floor)
    warps_by_floor:dict[int,list]=collections.defaultdict(list)
    floor_ids={award_floor}
    for edge in edges:
        warps_by_floor[int(edge.source_floor)].append(edge)
        floor_ids.add(int(edge.source_floor))
        floor_ids.add(int(edge.destination_floor))
    for floor,_x,_y in NORMAL_HOMETOWN_SPAWNS:
        floor_ids.add(int(floor))
    frozen={floor:tuple(rows) for floor,rows in warps_by_floor.items()}
    blockers=_conservative_npc_birth_blockers(npc_dir,floor_ids=floor_ids)

    rows=[]
    for ordinal,spawn in enumerate(NORMAL_HOMETOWN_SPAWNS,1):
        baseline=_one(
            ordinal=ordinal,
            spawn=spawn,
            award_floor=award_floor,
            award_goals=award_goals,
            floor_dist=floor_dist,
            warps_by_floor=frozen,
            catalog=catalog,
            mapset=mapset,
            blockers=blockers,
        )
        static=_one(
            ordinal=ordinal,
            spawn=spawn,
            award_floor=award_floor,
            award_goals=award_goals,
            floor_dist=floor_dist,
            warps_by_floor=frozen,
            catalog=catalog,
            mapset=mapset,
            blockers={},
        )
        rows.append(GapPair(baseline=baseline,static_only=static))
    return CoordinateGapAudit(rows=tuple(rows))


def emit(audit:CoordinateGapAudit)->None:
    print("StoneAge fresh-start coordinate gap classification — R1")
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print(
        "RULE|spawn floors/coordinates, award coordinates and frontier floor/"
        "coordinate identities are withheld"
    )
    print(
        "RULE|minimum remaining hops is measured in the floor-only classic-Warp "
        "graph from the closest coordinate-reachable component"
    )
    failed=0
    same_static=0
    for pair in audit.rows:
        b=pair.baseline
        s=pair.static_only
        if not b.reachable:
            failed+=1
            same_static+=int(
                not s.reachable
                and s.reason==b.reason
                and s.min_floor_hops_remaining==b.min_floor_hops_remaining
            )
        print(
            "FRESH_START_COORDINATE_GAP|"
            f"ordinal={b.ordinal}|"
            f"reachable={int(b.reachable)}|"
            f"reason={b.reason}|"
            f"min_floor_hops_remaining={b.min_floor_hops_remaining if b.min_floor_hops_remaining is not None else -1}|"
            f"source_disconnected={b.closest_frontier_source_disconnected}|"
            f"destination_invalid={b.closest_frontier_destination_invalid}|"
            f"usable_progress={b.closest_frontier_usable}|"
            f"award_floor_component_reached={int(b.award_floor_component_reached)}|"
            f"static_only_reachable={int(s.reachable)}|"
            f"static_only_reason={s.reason}|"
            f"static_only_min_floor_hops_remaining={s.min_floor_hops_remaining if s.min_floor_hops_remaining is not None else -1}"
        )
    print(f"COUNT|failed_hometowns|{failed}")
    print(f"COUNT|failed_hometowns_same_static_reason|{same_static}")
    print(OUTPUT_RESOLUTION)


def main()->None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--npc-dir",type=Path,required=True)
    ap.add_argument("--setup",type=Path,required=True)
    ap.add_argument("--server-map-root",type=Path,required=True)
    ap.add_argument("--mapset",type=Path,required=True)
    args=ap.parse_args()
    emit(analyze(
        npc_dir=args.npc_dir,
        setup=args.setup,
        server_map_root=args.server_map_root,
        mapset_path=args.mapset,
    ))


if __name__=="__main__":
    main()
