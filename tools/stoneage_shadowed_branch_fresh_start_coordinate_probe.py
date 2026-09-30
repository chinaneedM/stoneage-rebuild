#!/usr/bin/env python3
"""Close fresh-character coordinate reachability to the key-item award NPC.

Evidence layers remain explicit:
- spawn coordinates are the four normal hometown entries in the pinned fixed
  descendant CHAR_getInitElderPosition source; its committed version.h leaves
  _DELBORNPLACE and _MUSEUM disabled;
- movement and classic-Warp geometry come from recovered25;
- static collision comes from recovered25 LS2MAP + mapset;
- every recovered non-classic-Warp NPC birth cell is conservatively blocked.

The new character's own spawn cell is admitted as an initial state even if a
conservative NPC-birth mask overlaps it: CHAR_createNewChar sets that exact
position after MAP_checkCoordinates and does not perform target-cell dynamic
overability as an ordinary step would. Every subsequent entered cell obeys the
conservative occupancy mask.

No gated 811->820 edge is needed here: the goal is the earlier award interaction
on the classic-reachable floor.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
from dataclasses import dataclass
from pathlib import Path

from tools.stoneage_client_server_map_probe import collect_server_maps
from tools.stoneage_ordered_runtime_world_reachability_probe import (
    load_ordered_runtime_reachability,
)
from tools.stoneage_server_static_map import (
    parse_ls2map,
    parse_mapset_collision_profile,
    static_point_walkable,
)
from tools.stoneage_shadowed_branch_coordinate_access_probe import (
    SelectedStaticMap,
    _conservative_npc_birth_blockers,
    _interaction_cells,
    _matching_award_placements,
    _neighbors,
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


OUTPUT_RESOLUTION = (
    "RESOLUTION|SHADOWED_BRANCH_FRESH_START_COORDINATE_REACHABILITY_CLOSED"
)

# Pinned fixed-descendant CHAR_getInitElderPosition normal hometown positions.
NORMAL_HOMETOWN_SPAWNS = (
    (1006, 15, 22),
    (2006, 20, 16),
    (3006, 21, 16),
    (4006, 14, 20),
)


@dataclass(frozen=True)
class WarpEdge:
    source_floor:int
    source_x:int
    source_y:int
    destination_floor:int
    destination_x:int
    destination_y:int


@dataclass(frozen=True)
class MapSelection:
    static_map:SelectedStaticMap|None
    status:str
    missing_metadata:int


def _server_catalog(root:Path):
    by_id,_total,_ls2,_invalid=collect_server_maps(root,sample_limit=0)
    return by_id


def _select_from_catalog(
    catalog,
    mapset,
    floor_id:int,
)->MapSelection:
    entries=tuple(catalog.get(int(floor_id),()))
    if not entries:
        return MapSelection(None,"MISSING",0)

    identities=[]
    for entry in entries:
        raw=entry["path"].read_bytes()
        identities.append((
            hashlib.sha256(raw).hexdigest(),
            int(entry["width"]),
            int(entry["height"]),
            raw,
        ))
    hashes={row[0] for row in identities}
    dims={(row[1],row[2]) for row in identities}
    if len(hashes)>1 or len(dims)>1:
        return MapSelection(None,"DIVERGENT",0)

    parsed=parse_ls2map(identities[0][3])
    if parsed.floor_id != int(floor_id):
        raise ValueError("LS2MAP embedded floor drift")
    missing=sorted(parsed.used_image_ids-set(mapset.images))
    if missing:
        return MapSelection(None,"MISSING_METADATA",len(missing))

    walkable=tuple(
        static_point_walkable(
            tile=mapset.images[tile_id],
            object_part=mapset.images[obj_id],
        ).allowed
        for tile_id,obj_id in zip(parsed.tile_ids,parsed.object_ids)
    )
    return MapSelection(
        SelectedStaticMap(
            floor_id=parsed.floor_id,
            width=parsed.width,
            height=parsed.height,
            walkable=walkable,
            copy_status=(
                "UNIQUE" if len(identities)==1 else "DUPLICATE_IDENTICAL"
            ),
            payload_sha256=parsed.payload_sha256,
        ),
        "UNIQUE" if len(identities)==1 else "DUPLICATE_IDENTICAL",
        0,
    )


def _warp_edges(runtime)->tuple[WarpEdge,...]:
    return tuple(
        WarpEdge(
            source_floor=int(edge.source.floor_id),
            source_x=int(edge.source.x),
            source_y=int(edge.source.y),
            destination_floor=int(edge.destination.floor_id),
            destination_x=int(edge.destination.x),
            destination_y=int(edge.destination.y),
        )
        for edge in runtime.topology.legacy_warps
    )


class FloorComponents:
    """Lazy static+conservative-NPC connected-component classifier."""

    def __init__(
        self,
        static_map:SelectedStaticMap,
        blocked:frozenset[tuple[int,int]],
        *,
        admitted_origins:frozenset[tuple[int,int]]=frozenset(),
    ):
        self.map=static_map
        self.blocked=frozenset(
            point for point in blocked if point not in admitted_origins
        )
        self.labels:dict[tuple[int,int],int]={}
        self._next=1

    def component(self,point:tuple[int,int])->int|None:
        point=(int(point[0]),int(point[1]))
        x,y=point
        if not self.map.allowed(x,y) or point in self.blocked:
            return None
        if point in self.labels:
            return self.labels[point]

        label=self._next
        self._next+=1
        queue=collections.deque([point])
        self.labels[point]=label
        while queue:
            cx,cy=queue.popleft()
            for nxt in _neighbors(
                self.map,cx,cy,self.blocked
            ):
                if nxt in self.labels:
                    continue
                self.labels[nxt]=label
                queue.append(nxt)
        return label


@dataclass(frozen=True)
class SpawnCoordinateWitness:
    ordinal:int
    reachable:bool
    warp_hops:int|None
    traversed_floors:int
    unresolved_map_floors:int


@dataclass(frozen=True)
class FreshStartCoordinateAudit:
    award_floor:int
    award_interaction_cells:int
    static_only_witnesses:tuple[SpawnCoordinateWitness,...]
    witnesses:tuple[SpawnCoordinateWitness,...]

    @property
    def static_only_exists(self)->bool:
        return any(row.reachable for row in self.static_only_witnesses)

    @property
    def static_only_closed(self)->bool:
        return (
            len(self.static_only_witnesses)==len(NORMAL_HOMETOWN_SPAWNS)
            and all(row.reachable for row in self.static_only_witnesses)
        )

    @property
    def exists(self)->bool:
        return any(row.reachable for row in self.witnesses)

    @property
    def closed(self)->bool:
        return (
            len(self.witnesses)==len(NORMAL_HOMETOWN_SPAWNS)
            and all(row.reachable for row in self.witnesses)
        )


def _one_spawn(
    *,
    ordinal:int,
    spawn:tuple[int,int,int],
    award_floor:int,
    award_goals:set[tuple[int,int]],
    warps_by_floor:dict[int,tuple[WarpEdge,...]],
    catalog,
    mapset,
    blockers:dict[int,frozenset[tuple[int,int]]],
)->SpawnCoordinateWitness:
    start_floor,start_x,start_y=map(int,spawn)
    navigators={}
    unresolved=set()
    admitted_by_floor={start_floor:frozenset({(start_x,start_y)})}

    def navigator(floor:int):
        if floor in navigators:
            return navigators[floor]
        selected=_select_from_catalog(catalog,mapset,floor)
        if selected.static_map is None:
            unresolved.add(int(floor))
            navigators[floor]=None
            return None
        nav=FloorComponents(
            selected.static_map,
            blockers.get(int(floor),frozenset()),
            admitted_origins=admitted_by_floor.get(int(floor),frozenset()),
        )
        navigators[floor]=nav
        return nav

    start_nav=navigator(start_floor)
    if start_nav is None:
        return SpawnCoordinateWitness(
            ordinal=ordinal,
            reachable=False,
            warp_hops=None,
            traversed_floors=0,
            unresolved_map_floors=len(unresolved),
        )
    start_component=start_nav.component((start_x,start_y))
    if start_component is None:
        return SpawnCoordinateWitness(
            ordinal=ordinal,
            reachable=False,
            warp_hops=None,
            traversed_floors=1,
            unresolved_map_floors=len(unresolved),
        )

    queue=collections.deque([(start_floor,start_component,0)])
    seen={(start_floor,start_component)}
    touched={start_floor}

    while queue:
        floor,component,hops=queue.popleft()
        nav=navigator(floor)
        if nav is None:
            continue

        if floor==award_floor:
            if any(nav.component(goal)==component for goal in award_goals):
                return SpawnCoordinateWitness(
                    ordinal=ordinal,
                    reachable=True,
                    warp_hops=hops,
                    traversed_floors=len(touched),
                    unresolved_map_floors=len(unresolved),
                )

        for edge in warps_by_floor.get(floor,()):
            source_component=nav.component((edge.source_x,edge.source_y))
            if source_component!=component:
                continue
            dest_nav=navigator(edge.destination_floor)
            if dest_nav is None:
                continue
            dest_component=dest_nav.component(
                (edge.destination_x,edge.destination_y)
            )
            if dest_component is None:
                continue
            state=(edge.destination_floor,dest_component)
            if state in seen:
                continue
            seen.add(state)
            touched.add(edge.destination_floor)
            queue.append((edge.destination_floor,dest_component,hops+1))

    return SpawnCoordinateWitness(
        ordinal=ordinal,
        reachable=False,
        warp_hops=None,
        traversed_floors=len(touched),
        unresolved_map_floors=len(unresolved),
    )


def analyze(
    *,
    npc_dir:Path,
    setup:Path,
    server_map_root:Path,
    mapset_path:Path,
)->FreshStartCoordinateAudit:
    runtime_audit=load_ordered_runtime_reachability()
    runtime=runtime_audit.runtime
    reached=set(runtime_audit.reached_floor_ids)
    target,_missing=_locate_key_item(npc_dir)
    maxlevel=_configured_maxlevel(setup)
    accepted=_award_records(
        npc_dir,
        target_item=target,
        maxlevel=maxlevel,
        reached=reached,
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
        raise ValueError(
            f"award floor static map unavailable: {award_selection.status}"
        )
    award_goals=_interaction_cells(award_selection.static_map,awards)
    if not award_goals:
        raise ValueError("award interaction cells missing")

    edges=_warp_edges(runtime)
    warps_by_floor:dict[int,list[WarpEdge]]=collections.defaultdict(list)
    floor_ids={award_floor}
    floor_ids.update(floor for floor,_x,_y in NORMAL_HOMETOWN_SPAWNS)
    for edge in edges:
        warps_by_floor[edge.source_floor].append(edge)
        floor_ids.add(edge.source_floor)
        floor_ids.add(edge.destination_floor)
    frozen_warps={
        floor:tuple(rows) for floor,rows in warps_by_floor.items()
    }

    blockers=_conservative_npc_birth_blockers(
        npc_dir,
        floor_ids=floor_ids,
    )

    static_only_witnesses=tuple(
        _one_spawn(
            ordinal=ordinal,
            spawn=spawn,
            award_floor=award_floor,
            award_goals=award_goals,
            warps_by_floor=frozen_warps,
            catalog=catalog,
            mapset=mapset,
            blockers={},
        )
        for ordinal,spawn in enumerate(NORMAL_HOMETOWN_SPAWNS,1)
    )
    witnesses=tuple(
        _one_spawn(
            ordinal=ordinal,
            spawn=spawn,
            award_floor=award_floor,
            award_goals=award_goals,
            warps_by_floor=frozen_warps,
            catalog=catalog,
            mapset=mapset,
            blockers=blockers,
        )
        for ordinal,spawn in enumerate(NORMAL_HOMETOWN_SPAWNS,1)
    )
    return FreshStartCoordinateAudit(
        award_floor=award_floor,
        award_interaction_cells=len(award_goals),
        static_only_witnesses=static_only_witnesses,
        witnesses=witnesses,
    )


def emit(audit:FreshStartCoordinateAudit)->None:
    print("StoneAge shadowed-branch fresh-start coordinate reachability — R1")
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print(
        "PINNED_SOURCE_CONTROL|normal_hometowns=4|"
        "delbornplace_define_enabled=0|museum_define_enabled=0"
    )
    print(
        "RULE|spawn floors/coordinates, item ids, NPC names and intermediate "
        "route coordinates/floor ids are withheld"
    )
    print(
        "RULE|recovered25 LS2MAP + mapset collision, diagonal corner checks, "
        "active classic Warp coordinates and conservative non-Warp NPC birth "
        "blockers are all enforced"
    )
    print(
        "RULE|only each character's exact initialized spawn cell is admitted "
        "despite a possible conservative birth-mask overlap; later entered "
        "cells receive no such exception"
    )
    print(f"COUNT|normal_hometown_candidates|{len(audit.witnesses)}")
    print(
        "COUNT|normal_hometown_static_only_reachable|"
        f"{sum(x.reachable for x in audit.static_only_witnesses)}"
    )
    print(f"COUNT|normal_hometown_coordinate_reachable|{sum(x.reachable for x in audit.witnesses)}")
    print(f"COUNT|award_interaction_cells|{audit.award_interaction_cells}")
    for row in audit.static_only_witnesses:
        print(
            "FRESH_START_STATIC_ONLY_WITNESS|"
            f"ordinal={row.ordinal}|reachable={int(row.reachable)}|"
            f"warp_hops={row.warp_hops if row.warp_hops is not None else -1}|"
            f"traversed_floors={row.traversed_floors}|"
            f"unresolved_map_floors={row.unresolved_map_floors}|"
            "route_details_withheld=1"
        )
    for row in audit.witnesses:
        print(
            "FRESH_START_COORDINATE_WITNESS|"
            f"ordinal={row.ordinal}|reachable={int(row.reachable)}|"
            f"warp_hops={row.warp_hops if row.warp_hops is not None else -1}|"
            f"traversed_floors={row.traversed_floors}|"
            f"unresolved_map_floors={row.unresolved_map_floors}|"
            "route_details_withheld=1"
        )
    print(
        "FRESH_START_STATIC_ONLY_EXISTENTIAL_COORDINATE_CHAIN|witness="
        f"{int(audit.static_only_exists)}"
    )
    print(
        "FRESH_START_STATIC_ONLY_ALL_HOMETOWNS_COORDINATE_CHAIN|witness="
        f"{int(audit.static_only_closed)}"
    )
    print(
        "FRESH_START_EXISTENTIAL_COORDINATE_CHAIN|witness="
        f"{int(audit.exists)}"
    )
    print(
        "FRESH_START_ALL_HOMETOWNS_COORDINATE_CHAIN|witness="
        f"{int(audit.closed)}"
    )
    print(OUTPUT_RESOLUTION)


def main()->None:
    parser=argparse.ArgumentParser()
    parser.add_argument("--npc-dir",type=Path,required=True)
    parser.add_argument("--setup",type=Path,required=True)
    parser.add_argument("--server-map-root",type=Path,required=True)
    parser.add_argument("--mapset",type=Path,required=True)
    args=parser.parse_args()
    emit(analyze(
        npc_dir=args.npc_dir,
        setup=args.setup,
        server_map_root=args.server_map_root,
        mapset_path=args.mapset,
    ))


if __name__=="__main__":
    main()
