#!/usr/bin/env python3
"""Audit static coordinate accessibility of the shadowed-branch progression seam.

The floor-level progression is already closed. This probe adds recovered25
server-authoritative LS2MAP + mapset collision evidence without exposing raw
NPC coordinates, item IDs or argument payloads.

It checks:
- a reachable ExChangeMan award NPC can be interacted with from a statically
  walkable cell (Chebyshev distance <= 2, matching fixed descendant distance);
- from such an interaction cell, the active classic Warp source that travels
  from the award floor to the WarpMan floor is statically reachable;
- from that Warp destination coordinate, a statically walkable interaction
  cell within distance <= 2 of the gated WarpMan is reachable.

Dynamic transient blockers are deliberately not modeled here. The result is a
static-coordinate accessibility proof, not a claim that every live world state
is obstruction-free.
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
from tools.stoneage_shadowed_branch_item_shop_acquisition_probe import (
    _locate_key_item,
)
from tools.stoneage_shadowed_branch_key_item_exchange_probe import (
    _event_records,
    _item_terms,
    _values,
)
from tools.stoneage_shadowed_branch_progression_witness_probe import (
    _award_records,
    _locate_ingress_gate,
    _template_names,
)
from tools.stoneage_shadowed_branch_warpman_satisfiability_probe import (
    _assigned_data,
    _configured_maxlevel,
    _field,
    _warp_floors,
)
from tools.stoneage_transport_usage_probe import iter_blocks, magic_kind
from tools.stoneage_versioned_world_geometry_probe import _rect_from_fields


OUTPUT_RESOLUTION = "RESOLUTION|SHADOWED_BRANCH_STATIC_COORDINATE_ACCESS_CLOSED"
TALK_DISTANCE = 2


@dataclass(frozen=True)
class SelectedStaticMap:
    floor_id:int
    width:int
    height:int
    walkable:tuple[bool,...]
    copy_status:str
    payload_sha256:str

    def allowed(self,x:int,y:int)->bool:
        if not (0 <= int(x) < self.width and 0 <= int(y) < self.height):
            return False
        return bool(self.walkable[int(y)*self.width+int(x)])


@dataclass(frozen=True)
class InteractionPlacement:
    floor_id:int
    birth_rect:tuple[int,int,int,int]


@dataclass(frozen=True)
class ClassicHop:
    source_floor:int
    source_x:int
    source_y:int
    destination_floor:int
    destination_x:int
    destination_y:int


@dataclass(frozen=True)
class CoordinateAccessAudit:
    award_placements:int
    warpman_placements:int
    classic_hops:int
    award_interaction_cells:int
    warpman_interaction_cells:int
    award_to_hop_steps:int|None
    landing_to_warpman_steps:int|None
    award_map_copy_status:str
    ingress_map_copy_status:str
    award_map_missing_metadata:int
    ingress_map_missing_metadata:int

    @property
    def closed(self)->bool:
        return (
            self.award_placements > 0
            and self.warpman_placements > 0
            and self.classic_hops > 0
            and self.award_interaction_cells > 0
            and self.warpman_interaction_cells > 0
            and self.award_to_hop_steps is not None
            and self.landing_to_warpman_steps is not None
            and self.award_map_missing_metadata == 0
            and self.ingress_map_missing_metadata == 0
        )


def _select_map(
    server_map_root:Path,
    mapset,
    floor_id:int,
)->tuple[SelectedStaticMap|None,int]:
    server_by_id,_total,_ls2,_invalid=collect_server_maps(
        server_map_root,sample_limit=0
    )
    entries=tuple(server_by_id.get(int(floor_id),()))
    if not entries:
        return None,-1

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
        return None,-2
    status="UNIQUE" if len(identities)==1 else "DUPLICATE_IDENTICAL"

    parsed=parse_ls2map(identities[0][3])
    if parsed.floor_id != int(floor_id):
        raise ValueError("LS2MAP embedded floor drift")
    missing=sorted(parsed.used_image_ids-set(mapset.images))
    if missing:
        return None,len(missing)

    values=[]
    for tile_id,obj_id in zip(parsed.tile_ids,parsed.object_ids):
        values.append(static_point_walkable(
            tile=mapset.images[tile_id],
            object_part=mapset.images[obj_id],
        ).allowed)
    return SelectedStaticMap(
        floor_id=parsed.floor_id,
        width=parsed.width,
        height=parsed.height,
        walkable=tuple(values),
        copy_status=status,
        payload_sha256=parsed.payload_sha256,
    ),0


def _neighbors(
    static_map:SelectedStaticMap,
    x:int,
    y:int,
):
    for dx in (-1,0,1):
        for dy in (-1,0,1):
            if dx==0 and dy==0:
                continue
            nx,ny=x+dx,y+dy
            if not static_map.allowed(nx,ny):
                continue
            if dx and dy:
                if not static_map.allowed(x+dx,y):
                    continue
                if not static_map.allowed(x,y+dy):
                    continue
            yield nx,ny


def _distance_to_any(
    static_map:SelectedStaticMap,
    starts:set[tuple[int,int]],
    goals:set[tuple[int,int]],
)->int|None:
    starts={
        (int(x),int(y)) for x,y in starts
        if 0 <= int(x) < static_map.width
        and 0 <= int(y) < static_map.height
    }
    goals={
        (int(x),int(y)) for x,y in goals
        if static_map.allowed(int(x),int(y))
    }
    if not starts or not goals:
        return None
    overlap=starts & goals
    if overlap:
        return 0
    queue=collections.deque((point,0) for point in sorted(starts))
    seen=set(starts)
    while queue:
        (x,y),depth=queue.popleft()
        for point in _neighbors(static_map,x,y):
            if point in seen:
                continue
            if point in goals:
                return depth+1
            seen.add(point)
            queue.append((point,depth+1))
    return None


def _interaction_cells(
    static_map:SelectedStaticMap,
    placements:tuple[InteractionPlacement,...],
)->set[tuple[int,int]]:
    goals=set()
    for placement in placements:
        x1,y1,x2,y2=placement.birth_rect
        npc_cells={
            (x,y)
            for x in range(x1,x2+1)
            for y in range(y1,y2+1)
        }
        for nx,ny in npc_cells:
            for dx in range(-TALK_DISTANCE,TALK_DISTANCE+1):
                for dy in range(-TALK_DISTANCE,TALK_DISTANCE+1):
                    distance=max(abs(dx),abs(dy))
                    if not 1 <= distance <= TALK_DISTANCE:
                        continue
                    point=(nx+dx,ny+dy)
                    if point in npc_cells:
                        continue
                    if static_map.allowed(*point):
                        goals.add(point)
    return goals


def _matching_award_placements(
    npc_dir:Path,
    accepted_records:set[tuple[int,bytes]],
)->tuple[InteractionPlacement,...]:
    exchange_names=_template_names(npc_dir,b"ExChangeMan")
    files=sorted(
        (p for p in npc_dir.rglob("*") if p.is_file()),
        key=lambda p:str(p).lower(),
    )
    out=[]
    for create in (p for p in files if magic_kind(p)=="create"):
        for entries in iter_blocks(create):
            fields={}; enemies=[]
            for key,value in entries:
                if key==b"enemy": enemies.append(value)
                else: fields[key]=value
            try: floor=int(fields.get(b"floorid",b"0"))
            except ValueError: continue
            birth=_rect_from_fields(
                fields,center_key=b"borncenter",corner_key=b"borncorner"
            )
            if birth is None:
                continue
            for enemy in enemies:
                name,sep,arg=enemy.partition(b"|")
                if name.strip() not in exchange_names:
                    continue
                data=_assigned_data(npc_dir,arg if sep else b"")
                if data is None:
                    continue
                if any(
                    (floor,record) in accepted_records
                    for record in _event_records(data)
                ):
                    out.append(InteractionPlacement(floor,birth))
    return tuple(out)

def _matching_warpman_placements(
    npc_dir:Path,
    *,
    ingress_source_floor:int,
    ingress_destination_floor:int,
    ingress_free:bytes,
)->tuple[InteractionPlacement,...]:
    warpman_names=_template_names(npc_dir,b"WarpMan")
    files=sorted(
        (p for p in npc_dir.rglob("*") if p.is_file()),
        key=lambda p:str(p).lower(),
    )
    out=[]
    for create in (p for p in files if magic_kind(p)=="create"):
        for entries in iter_blocks(create):
            fields={}; enemies=[]
            for key,value in entries:
                if key==b"enemy": enemies.append(value)
                else: fields[key]=value
            try: floor=int(fields.get(b"floorid",b"0"))
            except ValueError: continue
            if floor != int(ingress_source_floor):
                continue
            birth=_rect_from_fields(
                fields,center_key=b"borncenter",corner_key=b"borncorner"
            )
            if birth is None:
                continue
            for enemy in enemies:
                name,sep,arg=enemy.partition(b"|")
                if name.strip() not in warpman_names:
                    continue
                data=_assigned_data(npc_dir,arg if sep else b"")
                if data is None:
                    continue
                if int(ingress_destination_floor) not in set(_warp_floors(data)):
                    continue
                if (_field(data,b"FREE") or b"") != ingress_free:
                    continue
                out.append(InteractionPlacement(floor,birth))
    return tuple(out)

def _classic_hops(runtime,source_floor:int,destination_floor:int)->tuple[ClassicHop,...]:
    rows=[]
    for edge in runtime.topology.legacy_warps:
        if (
            int(edge.source.floor_id)==int(source_floor)
            and int(edge.destination.floor_id)==int(destination_floor)
        ):
            rows.append(ClassicHop(
                source_floor=int(edge.source.floor_id),
                source_x=int(edge.source.x),
                source_y=int(edge.source.y),
                destination_floor=int(edge.destination.floor_id),
                destination_x=int(edge.destination.x),
                destination_y=int(edge.destination.y),
            ))
    return tuple(rows)


def analyze(
    *,
    npc_dir:Path,
    setup_path:Path,
    server_map_root:Path,
    mapset_path:Path,
)->CoordinateAccessAudit:
    target_item,_missing=_locate_key_item(npc_dir)
    runtime_audit=load_ordered_runtime_reachability()
    reached=set(runtime_audit.reached_floor_ids)
    branch_ids={row.floor_id for row in runtime_audit.orphan_rows}
    maxlevel=_configured_maxlevel(setup_path)

    ingress,_ingress_missing=_locate_ingress_gate(
        npc_dir,
        reached=reached,
        orphan_ids=branch_ids,
    )
    accepted=_award_records(
        npc_dir,
        target_item=target_item,
        maxlevel=maxlevel,
        reached=reached,
    )
    accepted_records={(int(floor),record) for floor,record,_levels in accepted}
    awards=_matching_award_placements(npc_dir,accepted_records)
    warpmen=_matching_warpman_placements(
        npc_dir,
        ingress_source_floor=ingress.source_floor,
        ingress_destination_floor=ingress.destination_floor,
        ingress_free=ingress.free,
    )
    if not awards or not warpmen:
        raise ValueError("critical state-gated interaction placements missing")

    award_floors={int(floor) for floor,_record,_levels in accepted}
    ingress_floors={int(ingress.source_floor)}
    if len(award_floors)!=1 or len(ingress_floors)!=1:
        raise ValueError("critical interaction floor identity is not unique")
    award_floor=next(iter(award_floors))
    ingress_floor=next(iter(ingress_floors))
    hops=_classic_hops(runtime_audit.runtime,award_floor,ingress_floor)
    if not hops:
        raise ValueError("no active classic hop joins award floor to ingress floor")

    mapset=parse_mapset_collision_profile(mapset_path.read_bytes())
    award_map,award_missing=_select_map(
        server_map_root,mapset,award_floor
    )
    ingress_map,ingress_missing=_select_map(
        server_map_root,mapset,ingress_floor
    )
    if award_map is None or ingress_map is None:
        return CoordinateAccessAudit(
            award_placements=len(awards),
            warpman_placements=len(warpmen),
            classic_hops=len(hops),
            award_interaction_cells=0,
            warpman_interaction_cells=0,
            award_to_hop_steps=None,
            landing_to_warpman_steps=None,
            award_map_copy_status=(
                "MISSING" if award_missing==-1 else
                "DIVERGENT" if award_missing==-2 else
                "MISSING_METADATA"
            ),
            ingress_map_copy_status=(
                "MISSING" if ingress_missing==-1 else
                "DIVERGENT" if ingress_missing==-2 else
                "MISSING_METADATA"
            ),
            award_map_missing_metadata=max(0,award_missing),
            ingress_map_missing_metadata=max(0,ingress_missing),
        )

    award_goals=_interaction_cells(award_map,awards)
    warpman_goals=_interaction_cells(ingress_map,warpmen)

    best_award=None
    best_ingress=None
    for hop in hops:
        award_distance=_distance_to_any(
            award_map,
            starts=award_goals,
            goals={(hop.source_x,hop.source_y)},
        )
        ingress_distance=_distance_to_any(
            ingress_map,
            starts={(hop.destination_x,hop.destination_y)},
            goals=warpman_goals,
        )
        if award_distance is not None:
            best_award=(
                award_distance
                if best_award is None
                else min(best_award,award_distance)
            )
        if ingress_distance is not None:
            best_ingress=(
                ingress_distance
                if best_ingress is None
                else min(best_ingress,ingress_distance)
            )

    return CoordinateAccessAudit(
        award_placements=len(awards),
        warpman_placements=len(warpmen),
        classic_hops=len(hops),
        award_interaction_cells=len(award_goals),
        warpman_interaction_cells=len(warpman_goals),
        award_to_hop_steps=best_award,
        landing_to_warpman_steps=best_ingress,
        award_map_copy_status=award_map.copy_status,
        ingress_map_copy_status=ingress_map.copy_status,
        award_map_missing_metadata=award_missing,
        ingress_map_missing_metadata=ingress_missing,
    )


def emit(audit:CoordinateAccessAudit)->None:
    print("StoneAge shadowed-branch static coordinate accessibility — R1")
    print(
        "SCOPE|recovered25 LS2MAP + mapset static collision|"
        "award interaction -> classic hop -> WarpMan interaction"
    )
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print(
        "RULE|NPC/item identities, raw coordinates, map payloads and argument "
        "payloads are not emitted"
    )
    print(
        "RULE|interaction target cells use fixed descendant Chebyshev distance "
        "<=2; NPC-occupied cells themselves are excluded"
    )
    print(
        "RULE|dynamic transient blockers are outside this static-coordinate audit"
    )
    print(f"COUNT|award_placements|{audit.award_placements}")
    print(f"COUNT|warpman_placements|{audit.warpman_placements}")
    print(f"COUNT|classic_hops|{audit.classic_hops}")
    print(f"COUNT|award_interaction_cells|{audit.award_interaction_cells}")
    print(f"COUNT|warpman_interaction_cells|{audit.warpman_interaction_cells}")
    print(f"COUNT|award_map_missing_metadata|{audit.award_map_missing_metadata}")
    print(f"COUNT|ingress_map_missing_metadata|{audit.ingress_map_missing_metadata}")
    print(f"MAP_COPY|award_floor|{audit.award_map_copy_status}")
    print(f"MAP_COPY|ingress_floor|{audit.ingress_map_copy_status}")
    print(
        "PATH|award_interaction_to_classic_hop|"
        f"reachable={int(audit.award_to_hop_steps is not None)}|"
        f"steps={audit.award_to_hop_steps if audit.award_to_hop_steps is not None else -1}"
    )
    print(
        "PATH|classic_landing_to_warpman_interaction|"
        f"reachable={int(audit.landing_to_warpman_steps is not None)}|"
        f"steps={audit.landing_to_warpman_steps if audit.landing_to_warpman_steps is not None else -1}"
    )
    print(f"STATIC_COORDINATE_CHAIN|witness={int(audit.closed)}")
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
        setup_path=args.setup,
        server_map_root=args.server_map_root,
        mapset_path=args.mapset,
    ))


if __name__=="__main__":
    main()
