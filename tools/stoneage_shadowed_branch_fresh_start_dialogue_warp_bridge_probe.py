#!/usr/bin/env python3
"""Audit coordinate-level dialogue-warp bridges for failed fresh starts.

The classic-Warp coordinate model leaves two normal hometown starts outside the
award interaction component even though their floors have a floor-only route.
This probe asks a narrower question before reopening movement semantics:

Can recovered WarpMan or FMWarpMan placements provide a coordinate transition
from a component reachable by the fresh character into a component that then
reaches the award through classic Warp geometry?

This is deliberately a spatial-candidate audit. WarpMan dialogue facing,
FREE/action/fee requirements and FMWarpMan family/schedule state are not
promoted here. A positive result identifies the exact next gate to audit; it is
not yet a fresh-start legal-state closure.
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
    InteractionPlacement,
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
    _template_names,
)
from tools.stoneage_shadowed_branch_warpman_satisfiability_probe import (
    _assigned_data,
    _configured_maxlevel,
    _field,
)
from tools.stoneage_transport_usage_probe import iter_blocks, magic_kind
from tools.stoneage_versioned_world_geometry_probe import _rect_from_fields


WARPMAN="WarpMan"
FMWARPMAN="FMWarpMan"
OUTPUT_RESOLUTION=(
    "RESOLUTION|SHADOWED_BRANCH_FRESH_START_DIALOGUE_WARP_BRIDGE_AUDITED"
)


@dataclass(frozen=True)
class DialogueWarp:
    kind:str
    source_floor:int
    source_rect:tuple[int,int,int,int]
    destination_floor:int
    destination_x:int
    destination_y:int

    def __post_init__(self):
        if self.kind not in {WARPMAN,FMWARPMAN}:
            raise ValueError("unsupported dialogue-warp kind")


@dataclass(frozen=True)
class SearchResult:
    reachable:bool
    nonclassic_edges:int|None
    kind_sequence:tuple[str,...]


@dataclass(frozen=True)
class BridgePair:
    ordinal:int
    baseline_classic:SearchResult
    baseline_warpman:SearchResult
    baseline_all_dialogue:SearchResult
    static_classic:SearchResult
    static_warpman:SearchResult
    static_all_dialogue:SearchResult


@dataclass(frozen=True)
class DialogueBridgeAudit:
    rows:tuple[BridgePair,...]
    candidate_counts:dict[str,int]
    malformed_points:int
    missing_args:int


def _parse_points(value:bytes|None)->tuple[tuple[int,int,int],...]:
    if value is None:
        return ()
    out=[]
    for raw in value.split(b";"):
        parts=[part.strip() for part in raw.split(b",")]
        if len(parts)<3:
            continue
        try:
            floor,x,y=(int(parts[0]),int(parts[1]),int(parts[2]))
        except ValueError:
            continue
        if floor>0:
            out.append((floor,x,y))
    return tuple(out)


def _collect_dialogue_warps(
    npc_dir:Path,
)->tuple[tuple[DialogueWarp,...],dict[str,int],int,int]:
    names={
        WARPMAN:_template_names(npc_dir,b"WarpMan"),
        FMWARPMAN:_template_names(npc_dir,b"FMWarpMan"),
    }
    files=sorted(
        (path for path in npc_dir.rglob("*") if path.is_file()),
        key=lambda path:str(path).lower(),
    )
    out=[]
    counts=collections.Counter()
    malformed=0
    missing=0
    for create in (path for path in files if magic_kind(path)=="create"):
        for entries in iter_blocks(create):
            fields={}; enemies=[]
            for key,value in entries:
                if key==b"enemy":
                    enemies.append(value)
                else:
                    fields[key]=value
            try:
                source_floor=int(fields.get(b"floorid",b"0"))
            except ValueError:
                continue
            if source_floor<=0:
                continue
            rect=_rect_from_fields(
                fields,center_key=b"borncenter",corner_key=b"borncorner"
            )
            if rect is None:
                continue
            for enemy in enemies:
                template,sep,arg=enemy.partition(b"|")
                template=template.strip()
                kind=None
                for candidate in (WARPMAN,FMWARPMAN):
                    if template in names[candidate]:
                        kind=candidate
                        break
                if kind is None:
                    continue
                counts[f"{kind}:refs"]+=1
                data=_assigned_data(npc_dir,arg if sep else b"")
                if data is None:
                    missing+=1
                    counts[f"{kind}:missing_args"]+=1
                    continue
                counts[f"{kind}:resolved_args"]+=1
                values=(
                    (_field(data,b"WARP"),)
                    if kind==WARPMAN
                    else (_field(data,b"WARP1"),_field(data,b"WARP2"))
                )
                for value in values:
                    if value is None:
                        continue
                    raw_rows=[row for row in value.split(b";") if row.strip()]
                    points=_parse_points(value)
                    malformed+=max(0,len(raw_rows)-len(points))
                    for floor,x,y in points:
                        out.append(DialogueWarp(
                            kind=kind,
                            source_floor=source_floor,
                            source_rect=rect,
                            destination_floor=floor,
                            destination_x=x,
                            destination_y=y,
                        ))
                        counts[f"{kind}:candidate_edges"]+=1
    out.sort(key=lambda row:(
        row.kind,row.source_floor,row.source_rect,
        row.destination_floor,row.destination_x,row.destination_y,
    ))
    return tuple(out),dict(counts),malformed,missing


def _search(
    *,
    spawn:tuple[int,int,int],
    award_floor:int,
    award_goals:set[tuple[int,int]],
    classic_by_floor:dict[int,tuple],
    dialogue_by_floor:dict[int,tuple[DialogueWarp,...]],
    allowed_dialogue:frozenset[str],
    catalog,
    mapset,
    blockers:dict[int,frozenset[tuple[int,int]]],
)->SearchResult:
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
        return SearchResult(False,None,())

    start=(start_floor,start_component)
    distance={start:0}
    parent={}
    queue=collections.deque([start])

    def goal(state):
        floor,component=state
        if floor!=award_floor:
            return False
        current=nav(floor)
        return (
            current is not None
            and any(current.component(point)==component for point in award_goals)
        )

    final=None
    while queue:
        state=queue.popleft()
        floor,component=state
        if goal(state):
            final=state
            break
        current=nav(floor)
        if current is None:
            continue

        for edge in classic_by_floor.get(floor,()):
            if current.component((edge.source_x,edge.source_y))!=component:
                continue
            destination=nav(edge.destination_floor)
            if destination is None:
                continue
            dest_component=destination.component(
                (edge.destination_x,edge.destination_y)
            )
            if dest_component is None:
                continue
            nxt=(edge.destination_floor,dest_component)
            new=distance[state]
            if new < distance.get(nxt,10**9):
                distance[nxt]=new
                parent[nxt]=(state,None)
                queue.appendleft(nxt)

        if not allowed_dialogue:
            continue
        for edge in dialogue_by_floor.get(floor,()):
            if edge.kind not in allowed_dialogue:
                continue
            placement=InteractionPlacement(
                floor_id=edge.source_floor,
                birth_rect=edge.source_rect,
            )
            cells=_interaction_cells(current.map,(placement,))
            if not any(current.component(point)==component for point in cells):
                continue
            destination=nav(edge.destination_floor)
            if destination is None:
                continue
            dest_component=destination.component(
                (edge.destination_x,edge.destination_y)
            )
            if dest_component is None:
                continue
            nxt=(edge.destination_floor,dest_component)
            new=distance[state]+1
            if new < distance.get(nxt,10**9):
                distance[nxt]=new
                parent[nxt]=(state,edge.kind)
                queue.append(nxt)

    if final is None:
        return SearchResult(False,None,())

    kinds=[]
    cursor=final
    while cursor!=start:
        prev,kind=parent[cursor]
        if kind is not None:
            kinds.append(kind)
        cursor=prev
    kinds.reverse()
    return SearchResult(True,distance[final],tuple(kinds))


def analyze(
    *,
    npc_dir:Path,
    setup:Path,
    server_map_root:Path,
    mapset_path:Path,
)->DialogueBridgeAudit:
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

    classic=_warp_edges(runtime)
    classic_by_floor=collections.defaultdict(list)
    floor_ids={award_floor}
    for edge in classic:
        classic_by_floor[edge.source_floor].append(edge)
        floor_ids.add(edge.source_floor)
        floor_ids.add(edge.destination_floor)
    classic_by_floor={
        floor:tuple(rows) for floor,rows in classic_by_floor.items()
    }

    dialogue,counts,malformed,missing=_collect_dialogue_warps(npc_dir)
    dialogue_by_floor=collections.defaultdict(list)
    for edge in dialogue:
        dialogue_by_floor[edge.source_floor].append(edge)
        floor_ids.add(edge.source_floor)
        floor_ids.add(edge.destination_floor)
    dialogue_by_floor={
        floor:tuple(rows) for floor,rows in dialogue_by_floor.items()
    }
    for floor,_x,_y in NORMAL_HOMETOWN_SPAWNS:
        floor_ids.add(int(floor))
    blockers=_conservative_npc_birth_blockers(npc_dir,floor_ids=floor_ids)

    rows=[]
    models=(
        ("classic",frozenset()),
        ("warpman",frozenset({WARPMAN})),
        ("all",frozenset({WARPMAN,FMWARPMAN})),
    )
    for ordinal,spawn in enumerate(NORMAL_HOMETOWN_SPAWNS,1):
        baseline={}
        static={}
        for name,allowed in models:
            baseline[name]=_search(
                spawn=spawn,
                award_floor=award_floor,
                award_goals=award_goals,
                classic_by_floor=classic_by_floor,
                dialogue_by_floor=dialogue_by_floor,
                allowed_dialogue=allowed,
                catalog=catalog,
                mapset=mapset,
                blockers=blockers,
            )
            static[name]=_search(
                spawn=spawn,
                award_floor=award_floor,
                award_goals=award_goals,
                classic_by_floor=classic_by_floor,
                dialogue_by_floor=dialogue_by_floor,
                allowed_dialogue=allowed,
                catalog=catalog,
                mapset=mapset,
                blockers={},
            )
        rows.append(BridgePair(
            ordinal=ordinal,
            baseline_classic=baseline["classic"],
            baseline_warpman=baseline["warpman"],
            baseline_all_dialogue=baseline["all"],
            static_classic=static["classic"],
            static_warpman=static["warpman"],
            static_all_dialogue=static["all"],
        ))
    return DialogueBridgeAudit(
        rows=tuple(rows),
        candidate_counts=counts,
        malformed_points=malformed,
        missing_args=missing,
    )


def _fmt(result:SearchResult,prefix:str)->str:
    seq=">".join(result.kind_sequence) if result.kind_sequence else "NONE"
    return (
        f"{prefix}_reachable={int(result.reachable)}|"
        f"{prefix}_nonclassic_edges="
        f"{result.nonclassic_edges if result.nonclassic_edges is not None else -1}|"
        f"{prefix}_kind_sequence={seq}"
    )


def emit(audit:DialogueBridgeAudit)->None:
    print("StoneAge fresh-start dialogue-warp coordinate bridge audit — R1")
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print(
        "RULE|spawn floors/coordinates, NPC identities, warp coordinates and "
        "route details are withheld"
    )
    print(
        "RULE|WarpMan/FMWarpMan edges are spatial candidates only; dialogue "
        "facing, FREE/action/fee and family/schedule gates are not proven here"
    )
    print(
        "RULE|Bus is not a candidate component bridge: fixed-descendant route "
        "movement uses CHAR_walk and MAP_walkAble rather than coordinate warp"
    )
    print(f"COUNT|malformed_dialogue_warp_points|{audit.malformed_points}")
    print(f"COUNT|missing_dialogue_warp_args|{audit.missing_args}")
    for key in sorted(audit.candidate_counts):
        print(f"COUNT|{key}|{audit.candidate_counts[key]}")
    for row in audit.rows:
        print(
            "FRESH_START_DIALOGUE_BRIDGE|"
            f"ordinal={row.ordinal}|"
            +_fmt(row.baseline_classic,"classic")+"|"
            +_fmt(row.baseline_warpman,"warpman")+"|"
            +_fmt(row.baseline_all_dialogue,"all_dialogue")+"|"
            +_fmt(row.static_classic,"static_classic")+"|"
            +_fmt(row.static_warpman,"static_warpman")+"|"
            +_fmt(row.static_all_dialogue,"static_all_dialogue")
        )
    failed=[
        row for row in audit.rows if not row.baseline_classic.reachable
    ]
    warpman_closed=sum(row.baseline_warpman.reachable for row in failed)
    dialogue_closed=sum(row.baseline_all_dialogue.reachable for row in failed)
    static_warpman_closed=sum(row.static_warpman.reachable for row in failed)
    static_dialogue_closed=sum(
        row.static_all_dialogue.reachable for row in failed
    )
    print(f"COUNT|failed_classic_hometowns|{len(failed)}")
    print(f"COUNT|failed_hometowns_bridged_by_warpman_candidate|{warpman_closed}")
    print(f"COUNT|failed_hometowns_bridged_by_any_dialogue_candidate|{dialogue_closed}")
    print(
        "COUNT|failed_hometowns_static_bridged_by_warpman_candidate|"
        f"{static_warpman_closed}"
    )
    print(
        "COUNT|failed_hometowns_static_bridged_by_any_dialogue_candidate|"
        f"{static_dialogue_closed}"
    )
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
