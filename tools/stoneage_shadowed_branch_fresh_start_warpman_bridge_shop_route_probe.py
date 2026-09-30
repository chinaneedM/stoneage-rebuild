#!/usr/bin/env python3
"""Prove an ordered fresh-start shop route for selected WarpMan bridge items.

The preceding audits establish that the two classic-coordinate-failed normal
hometowns each have one selected recovered WarpMan edge and that both edges
require the same ITEM equality predicate.  This probe asks whether a fresh
character can, before using that WarpMan edge:

1. reach a recovered ItemShop that normally sells the required item;
2. purchase one copy using recovered ItemShop pricing semantics;
3. continue through the directed classic-Warp coordinate graph to an
   orientation-independent adjacent interaction cell of the selected WarpMan;
4. retain enough starting Stone for the later already-proven ExChangeMan fee.

Raw item IDs, prices, Stone amounts, shop/NPC identities, coordinates,
filenames and route floor IDs are intentionally withheld.
"""

from __future__ import annotations

import argparse
import collections
from dataclasses import dataclass
from pathlib import Path

from tools.stoneage_server_static_map import parse_mapset_collision_profile
from tools.stoneage_shadowed_branch_coordinate_access_probe import (
    _conservative_npc_birth_blockers,
)
from tools.stoneage_shadowed_branch_fresh_start_coordinate_probe import (
    FloorComponents,
    NORMAL_HOMETOWN_SPAWNS,
    _select_from_catalog,
    _server_catalog,
    _warp_edges,
)
from tools.stoneage_shadowed_branch_fresh_start_dialogue_warp_bridge_probe import (
    WARPMAN,
    DialogueWarp,
    analyze as analyze_bridges,
)
from tools.stoneage_shadowed_branch_fresh_start_leveling_probe import (
    _reachable_components,
)
from tools.stoneage_shadowed_branch_fresh_start_stone_probe import (
    analyze as analyze_fresh_stone,
)
from tools.stoneage_shadowed_branch_fresh_start_warpman_bridge_item_surface_probe import (
    _requirements,
)
from tools.stoneage_shadowed_branch_item_shop_acquisition_probe import (
    _shop_item_visibility,
    _template_function_names,
)
from tools.stoneage_shadowed_branch_warpman_satisfiability_probe import (
    _assigned_data,
    _configured_itemset_paths,
    _field,
    _int_prefix,
    _item_ids,
)
from tools.stoneage_ordered_runtime_world_reachability_probe import (
    load_ordered_runtime_reachability,
)
from tools.stoneage_transport_usage_probe import iter_blocks, magic_kind
from tools.stoneage_versioned_world_geometry_probe import _rect_from_fields


OUTPUT_RESOLUTION=(
    "RESOLUTION|SHADOWED_BRANCH_FRESH_START_WARPMAN_BRIDGE_SHOP_ROUTE_AUDITED"
)

FRESH_ITEM_CAPACITY=15
STARTER_ITEM_CONFIG_SLOTS=15
EVENT_ACTION_FIELDS=frozenset({
    "ADDGOLD","DELGOLD","DELITEM","ADDITEM","DELPET","NEWDELPET","ADDPET",
    "EVEND","EVNOW","EVENT_END","EVENT_NOW","EVCLR","CHANGEBBI",
    "SETLASTTALKELDER","TOXICATION","GMACTION","SHOWGMQUE","DELGMQUEPET",
    "GETGMPRIZE","CLEANGMQUE","CHECKNEWPLAYER","GETRANDITEM","ABULLSCORE",
    "CHECKSCORE","ADDPFSKILLPOINT","CLEANPROFESSION","PROFESSION",
    "TREASURE_EVENT","SETLEVEL","ADDEXPS","ADDSKILLPOINT","SETRIDETYPE",
    "NPC_POINT","WARPPOINT",
})


@dataclass(frozen=True)
class BridgeExecutionProfile:
    ordinal:int
    free_msg_present:bool
    event_action_fields:tuple[str,...]


@dataclass(frozen=True)
class ShopPlacement:
    floor_id:int
    birth_rect:tuple[int,int,int,int]
    purchase_cost:int
    normal_buy_invocable:bool
    limitshop:bool
    event_mode:bool
    express_mode:bool
    buy_keyword_present:bool


@dataclass(frozen=True)
class SpawnShopWitness:
    ordinal:int
    ordered_shop_count:int
    affordable_ordered_shop_count:int
    combined_budget_ordered_shop_count:int
    unresolved_map_floors:int

    @property
    def ordered(self)->bool:
        return self.ordered_shop_count>0

    @property
    def affordable(self)->bool:
        return self.affordable_ordered_shop_count>0

    @property
    def combined_budget(self)->bool:
        return self.combined_budget_ordered_shop_count>0


@dataclass(frozen=True)
class ShopRouteAudit:
    failed_classic_hometowns:int
    warpman_bridged_hometowns:int
    unique_required_items:int
    target_visible_shop_placements:int
    normal_purchase_shop_placements:int
    starting_stone_positive:bool
    award_fee_available:bool
    starter_item_config_keys_present:int
    starter_positive_item_configs:int
    guaranteed_empty_item_slots:int
    execution_profiles:tuple[BridgeExecutionProfile,...]
    witnesses:tuple[SpawnShopWitness,...]

    @property
    def all_ordered(self)->bool:
        return bool(self.witnesses) and all(row.ordered for row in self.witnesses)

    @property
    def all_affordable(self)->bool:
        return bool(self.witnesses) and all(row.affordable for row in self.witnesses)

    @property
    def all_combined_budget(self)->bool:
        return bool(self.witnesses) and all(row.combined_budget for row in self.witnesses)

    @property
    def inventory_slot_witness(self)->bool:
        return (
            self.starter_item_config_keys_present==STARTER_ITEM_CONFIG_SLOTS
            and self.guaranteed_empty_item_slots>0
        )

    @property
    def all_free_msg(self)->bool:
        return (
            len(self.execution_profiles)==self.warpman_bridged_hometowns
            and bool(self.execution_profiles)
            and all(row.free_msg_present for row in self.execution_profiles)
        )

    @property
    def action_stage_inert(self)->bool:
        return (
            len(self.execution_profiles)==self.warpman_bridged_hometowns
            and bool(self.execution_profiles)
            and all(not row.event_action_fields for row in self.execution_profiles)
        )

    @property
    def execution_prerequisites(self)->bool:
        return (
            self.all_ordered
            and self.all_affordable
            and self.all_combined_budget
            and self.inventory_slot_witness
            and self.all_free_msg
            and self.action_stage_inert
        )


def _starter_inventory(setup:Path)->tuple[int,int,int]:
    values={}
    for raw in setup.read_bytes().splitlines():
        line=raw.split(b"#",1)[0].strip()
        if not line or b"=" not in line:
            continue
        key,value=line.split(b"=",1)
        name=key.strip().upper()
        if not name.startswith(b"ITEM"):
            continue
        suffix=name[4:]
        if not suffix.isdigit():
            continue
        index=int(suffix)
        if not 1<=index<=STARTER_ITEM_CONFIG_SLOTS:
            continue
        raw_value=value.strip()
        parsed=0 if not raw_value else _int_prefix(raw_value)
        if parsed is None:
            raise ValueError("nonempty starter ITEM value is not parseable")
        if index in values and values[index]!=int(parsed):
            raise ValueError("conflicting starter ITEM values")
        values[index]=int(parsed)
    present=len(values)
    positive=sum(value>0 for value in values.values())
    guaranteed=(
        max(0,FRESH_ITEM_CAPACITY-positive)
        if present==STARTER_ITEM_CONFIG_SLOTS
        else 0
    )
    return present,positive,guaranteed


def _bridge_execution_profile(
    ordinal:int,
    data:bytes,
)->BridgeExecutionProfile:
    keys=set()
    for token in data.split(b"|"):
        token=token.strip()
        if b":" not in token:
            continue
        key,_value=token.split(b":",1)
        keys.add(key.strip().decode("ascii","replace").upper())
    actions=tuple(sorted(keys & EVENT_ACTION_FIELDS))
    return BridgeExecutionProfile(
        ordinal=int(ordinal),
        free_msg_present=(_field(data,b"FreeMsg") is not None),
        event_action_fields=actions,
    )


def _target_item_cost(paths:tuple[Path,...],target_item:int)->int:
    values=[]
    for path in paths:
        for raw in path.read_bytes().splitlines():
            line=raw.strip()
            if not line or line.startswith(b"#"):
                continue
            fields=[part.strip() for part in line.replace(b"\t",b" ").split(b",")]
            if len(fields)<=18:
                continue
            item_id=_int_prefix(fields[16])
            if item_id!=int(target_item):
                continue
            cost=0 if not fields[18] else _int_prefix(fields[18])
            if cost is None:
                raise ValueError("target item cost is not parseable")
            values.append(int(cost))
    if not values:
        raise ValueError("target item cost row missing")
    if len(set(values))!=1:
        raise ValueError("target item cost conflicts across active itemsets")
    return values[0]


def _buy_rate(data:bytes)->float|None:
    value=_field(data,b"buy_rate")
    if value is None or not value.strip():
        return 1.0
    try:
        return float(value.decode("ascii","strict").strip())
    except (ValueError,UnicodeDecodeError):
        return None


def _purchase_price(base_cost:int,rate:float)->int|None:
    if base_cost<0 or rate<0:
        return None
    return int(base_cost*rate)


def _normal_buy_shape(data:bytes)->tuple[bool,bool,bool,bool,bool]:
    upper=data.upper()
    limitshop=b"LIMITSHOP" in upper
    event_mode=b"EVENT" in upper
    express_mode=b"EXPRESS" in upper
    buy_msg=_field(data,b"buy_msg")
    buy_keyword=(
        buy_msg is not None
        and any(part.strip() for part in buy_msg.split(b","))
    )
    default_menu=not limitshop and not event_mode and not express_mode
    direct_keyword=not limitshop and buy_keyword
    return (
        bool(default_menu or direct_keyword),
        bool(limitshop),
        bool(event_mode),
        bool(express_mode),
        bool(buy_keyword),
    )


def _adjacent_cells(
    static_map,
    rect:tuple[int,int,int,int],
)->set[tuple[int,int]]:
    x1,y1,x2,y2=rect
    occupied={
        (x,y)
        for x in range(int(x1),int(x2)+1)
        for y in range(int(y1),int(y2)+1)
    }
    out=set()
    for x,y in occupied:
        for dx in (-1,0,1):
            for dy in (-1,0,1):
                if dx==0 and dy==0:
                    continue
                point=(x+dx,y+dy)
                if point in occupied:
                    continue
                if static_map.allowed(*point):
                    out.add(point)
    return out


def _collect_target_shops(
    *,
    npc_dir:Path,
    target_item:int,
    active_item_ids:frozenset[int],
    base_cost:int,
)->tuple[ShopPlacement,...]:
    names=_template_function_names(npc_dir,b"ItemShop")
    files=sorted(
        (path for path in npc_dir.rglob("*") if path.is_file()),
        key=lambda path:str(path).lower(),
    )
    out=[]
    for create in (path for path in files if magic_kind(path)=="create"):
        for entries in iter_blocks(create):
            fields={}; enemies=[]
            for key,value in entries:
                if key==b"enemy":
                    enemies.append(value)
                else:
                    fields[key]=value
            try:
                floor=int(fields.get(b"floorid",b"0"))
            except ValueError:
                continue
            if floor<=0:
                continue
            rect=_rect_from_fields(
                fields,center_key=b"borncenter",corner_key=b"borncorner"
            )
            if rect is None:
                continue
            for enemy in enemies:
                name,sep,arg=enemy.partition(b"|")
                if name.strip() not in names:
                    continue
                data=_assigned_data(npc_dir,arg if sep else b"")
                if data is None:
                    continue
                item_list=_field(data,b"ItemList")
                if item_list is None:
                    continue
                _listed,visible,_rank=_shop_item_visibility(
                    item_list,target_item,active_item_ids
                )
                if not visible:
                    continue
                rate=_buy_rate(data)
                if rate is None:
                    continue
                price=_purchase_price(base_cost,rate)
                if price is None:
                    continue
                invocable,limitshop,event_mode,express_mode,buy_keyword=(
                    _normal_buy_shape(data)
                )
                out.append(ShopPlacement(
                    floor_id=floor,
                    birth_rect=rect,
                    purchase_cost=price,
                    normal_buy_invocable=invocable,
                    limitshop=limitshop,
                    event_mode=event_mode,
                    express_mode=express_mode,
                    buy_keyword_present=buy_keyword,
                ))
    return tuple(out)


def _reverse_components(
    *,
    target_floor:int,
    target_cells:set[tuple[int,int]],
    incoming:dict[int,tuple],
    catalog,
    mapset,
    blockers:dict[int,frozenset[tuple[int,int]]],
)->tuple[dict[int,set[int]],dict[int,FloorComponents|None],set[int]]:
    navigators={}
    unresolved=set()

    def nav(floor:int):
        floor=int(floor)
        if floor in navigators:
            return navigators[floor]
        selected=_select_from_catalog(catalog,mapset,floor)
        if selected.static_map is None:
            unresolved.add(floor)
            navigators[floor]=None
            return None
        row=FloorComponents(
            selected.static_map,
            blockers.get(floor,frozenset()),
        )
        navigators[floor]=row
        return row

    target_nav=nav(target_floor)
    if target_nav is None:
        return {},navigators,unresolved

    by_floor:dict[int,set[int]]=collections.defaultdict(set)
    queue=collections.deque()
    seen=set()
    for point in target_cells:
        component=target_nav.component(point)
        if component is None:
            continue
        state=(int(target_floor),int(component))
        if state in seen:
            continue
        seen.add(state)
        by_floor[int(target_floor)].add(int(component))
        queue.append(state)

    while queue:
        floor,component=queue.popleft()
        dest_nav=nav(floor)
        if dest_nav is None:
            continue
        for edge in incoming.get(int(floor),()):
            if dest_nav.component(
                (int(edge.destination_x),int(edge.destination_y))
            )!=component:
                continue
            source_nav=nav(int(edge.source_floor))
            if source_nav is None:
                continue
            source_component=source_nav.component(
                (int(edge.source_x),int(edge.source_y))
            )
            if source_component is None:
                continue
            state=(int(edge.source_floor),int(source_component))
            if state in seen:
                continue
            seen.add(state)
            by_floor[state[0]].add(state[1])
            queue.append(state)

    return dict(by_floor),navigators,unresolved


def _ordered_shop_on_path(
    *,
    shop:ShopPlacement,
    forward:dict[int,set[int]],
    forward_navs:dict[int,FloorComponents|None],
    reverse:dict[int,set[int]],
    reverse_navs:dict[int,FloorComponents|None],
)->bool:
    forward_components=forward.get(int(shop.floor_id))
    reverse_components=reverse.get(int(shop.floor_id))
    if not forward_components or not reverse_components:
        return False
    fnav=forward_navs.get(int(shop.floor_id))
    rnav=reverse_navs.get(int(shop.floor_id))
    if fnav is None or rnav is None:
        return False
    for point in _adjacent_cells(fnav.map,shop.birth_rect):
        fc=fnav.component(point)
        rc=rnav.component(point)
        if (
            fc is not None and fc in forward_components
            and rc is not None and rc in reverse_components
        ):
            return True
    return False


def analyze(
    *,
    npc_dir:Path,
    data_dir:Path,
    setup:Path,
    server_map_root:Path,
    mapset_path:Path,
)->ShopRouteAudit:
    spatial=analyze_bridges(
        npc_dir=npc_dir,
        setup=setup,
        server_map_root=server_map_root,
        mapset_path=mapset_path,
    )
    failed=[row for row in spatial.rows if not row.baseline_classic.reachable]
    bridged=[row for row in failed if row.baseline_warpman.reachable]
    reqs=[]
    edge_by_ordinal={}
    for row in bridged:
        edges=row.baseline_warpman.edge_sequence
        if len(edges)!=1 or edges[0].kind!=WARPMAN:
            raise ValueError("expected one selected WarpMan bridge edge per failed start")
        edge_by_ordinal[int(row.ordinal)]=edges[0]
        reqs.extend(_requirements(row.ordinal,edges))
    item_ids={int(req.item_id) for req in reqs}
    if len(item_ids)!=1 or any(req.operator!="=" for req in reqs):
        raise ValueError("bridge requirements are not one shared ITEM equality")
    target_item=next(iter(item_ids))

    starter_present,starter_positive,guaranteed_empty=_starter_inventory(setup)
    execution_profiles=[]
    for ordinal in sorted(edge_by_ordinal):
        data=edge_by_ordinal[ordinal].argument_data
        if data is None:
            raise ValueError("selected WarpMan edge lacks argument data")
        execution_profiles.append(_bridge_execution_profile(ordinal,data))

    item_paths=_configured_itemset_paths(setup,data_dir)
    active_item_ids=_item_ids(item_paths)
    if target_item not in active_item_ids:
        raise ValueError("bridge item absent from active catalog")
    base_cost=_target_item_cost(item_paths,target_item)
    shops=_collect_target_shops(
        npc_dir=npc_dir,
        target_item=target_item,
        active_item_ids=active_item_ids,
        base_cost=base_cost,
    )
    normal_shops=tuple(shop for shop in shops if shop.normal_buy_invocable)

    stone=analyze_fresh_stone(npc_dir=npc_dir,setup=setup)
    initial_stone=int(stone.initial_stone)
    award_fee=stone.minimum_fee
    if award_fee is None:
        raise ValueError("already-proven award fee is unavailable")

    runtime=load_ordered_runtime_reachability().runtime
    edges=_warp_edges(runtime)
    by_floor:dict[int,list]=collections.defaultdict(list)
    incoming:dict[int,list]=collections.defaultdict(list)
    floor_ids=set()
    for edge in edges:
        by_floor[int(edge.source_floor)].append(edge)
        incoming[int(edge.destination_floor)].append(edge)
        floor_ids.add(int(edge.source_floor))
        floor_ids.add(int(edge.destination_floor))
    for floor,_x,_y in NORMAL_HOMETOWN_SPAWNS:
        floor_ids.add(int(floor))
    for shop in shops:
        floor_ids.add(int(shop.floor_id))
    for edge in edge_by_ordinal.values():
        floor_ids.add(int(edge.source_floor))
        floor_ids.add(int(edge.destination_floor))
    frozen_by_floor={floor:tuple(rows) for floor,rows in by_floor.items()}
    frozen_incoming={floor:tuple(rows) for floor,rows in incoming.items()}

    catalog=_server_catalog(server_map_root)
    mapset=parse_mapset_collision_profile(mapset_path.read_bytes())
    blockers=_conservative_npc_birth_blockers(
        npc_dir,floor_ids=floor_ids
    )

    witnesses=[]
    for pair in bridged:
        ordinal=int(pair.ordinal)
        spawn=NORMAL_HOMETOWN_SPAWNS[ordinal-1]
        bridge=edge_by_ordinal[ordinal]

        forward,forward_navs,forward_unresolved=_reachable_components(
            spawn=spawn,
            catalog=catalog,
            mapset=mapset,
            blockers=blockers,
            warps_by_floor=frozen_by_floor,
        )

        target_selection=_select_from_catalog(
            catalog,mapset,int(bridge.source_floor)
        )
        if target_selection.static_map is None:
            target_cells=set()
        else:
            target_cells=_adjacent_cells(
                target_selection.static_map,bridge.source_rect
            )
        reverse,reverse_navs,reverse_unresolved=_reverse_components(
            target_floor=int(bridge.source_floor),
            target_cells=target_cells,
            incoming=frozen_incoming,
            catalog=catalog,
            mapset=mapset,
            blockers=blockers,
        )

        ordered=[]
        affordable=[]
        combined=[]
        for shop in normal_shops:
            if not _ordered_shop_on_path(
                shop=shop,
                forward=forward,
                forward_navs=forward_navs,
                reverse=reverse,
                reverse_navs=reverse_navs,
            ):
                continue
            ordered.append(shop)
            if initial_stone>=shop.purchase_cost:
                affordable.append(shop)
            if initial_stone>=shop.purchase_cost+int(award_fee):
                combined.append(shop)

        witnesses.append(SpawnShopWitness(
            ordinal=ordinal,
            ordered_shop_count=len(ordered),
            affordable_ordered_shop_count=len(affordable),
            combined_budget_ordered_shop_count=len(combined),
            unresolved_map_floors=len(
                set(forward_unresolved)|set(reverse_unresolved)
            ),
        ))

    return ShopRouteAudit(
        failed_classic_hometowns=len(failed),
        warpman_bridged_hometowns=len(bridged),
        unique_required_items=len(item_ids),
        target_visible_shop_placements=len(shops),
        normal_purchase_shop_placements=len(normal_shops),
        starting_stone_positive=initial_stone>0,
        award_fee_available=award_fee is not None,
        starter_item_config_keys_present=starter_present,
        starter_positive_item_configs=starter_positive,
        guaranteed_empty_item_slots=guaranteed_empty,
        execution_profiles=tuple(execution_profiles),
        witnesses=tuple(witnesses),
    )


def emit(audit:ShopRouteAudit)->None:
    print("StoneAge fresh-start WarpMan bridge ItemShop route audit — R1")
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print(
        "PINNED_SOURCE_FACT|ItemShop purchase price=int(item_base_cost*buy_rate)|"
        "purchase_requires_available_inventory_slot=1"
    )
    print(
        "PINNED_SOURCE_FACT|fresh_item_capacity=15|starter_item_config_slots=15|"
        "fresh_inventory_initially_empty=1|starter_loop_adds_at_most_one_item_per_slot=1"
    )
    print(
        "PINNED_SOURCE_FACT|fresh_login_party_mode=NONE|ordinary_WarpMan_FREE_is_rechecked="
        "1|ordinary_WarpMan_FREE_success_requires_FreeMsg=1"
    )
    print(
        "RULE|required item ID, base/purchase prices, starting Stone, award fee, "
        "shop/NPC identities, coordinates and route floor IDs are withheld"
    )
    print(
        "RULE|normal purchase means recovered ItemList visibility plus a fixed-"
        "descendant normal buy invocation path; LIMITSHOP-only behavior is not "
        "promoted as a purchase witness"
    )
    print(
        "RULE|shop and WarpMan interaction endpoints use adjacent walkable cells "
        "(Chebyshev distance 1), so the route does not depend on the NPC facing "
        "the player at distance 2"
    )
    print(f"COUNT|failed_classic_hometowns|{audit.failed_classic_hometowns}")
    print(f"COUNT|warpman_bridged_hometowns|{audit.warpman_bridged_hometowns}")
    print(f"COUNT|unique_required_items|{audit.unique_required_items}")
    print(
        "COUNT|target_visible_shop_placements|"
        f"{audit.target_visible_shop_placements}"
    )
    print(
        "COUNT|normal_purchase_shop_placements|"
        f"{audit.normal_purchase_shop_placements}"
    )
    print(f"STARTING_STONE|positive={int(audit.starting_stone_positive)}|amount_withheld=1")
    print(f"AWARD_FEE|available={int(audit.award_fee_available)}|amount_withheld=1")
    print(
        "STARTER_INVENTORY|"
        f"config_keys_present={audit.starter_item_config_keys_present}|"
        f"positive_item_configs={audit.starter_positive_item_configs}|"
        f"guaranteed_empty_slots={audit.guaranteed_empty_item_slots}|"
        "item_ids_withheld=1"
    )
    for row in audit.execution_profiles:
        print(
            "FRESH_START_BRIDGE_EXECUTION|"
            f"ordinal={row.ordinal}|"
            f"free_msg_present={int(row.free_msg_present)}|"
            f"event_action_fields={len(row.event_action_fields)}|"
            f"event_action_kinds={','.join(row.event_action_fields) if row.event_action_fields else 'NONE'}"
        )
    for row in audit.witnesses:
        print(
            "FRESH_START_BRIDGE_SHOP|"
            f"ordinal={row.ordinal}|"
            f"ordered_shops={row.ordered_shop_count}|"
            f"affordable_ordered_shops={row.affordable_ordered_shop_count}|"
            f"combined_budget_ordered_shops={row.combined_budget_ordered_shop_count}|"
            f"unresolved_map_floors={row.unresolved_map_floors}|"
            "amounts_and_route_withheld=1"
        )
    print(
        "FRESH_START_ALL_FAILED_HOMETOWNS_ORDERED_SHOP_TO_WARPMAN|witness="
        f"{int(audit.all_ordered)}"
    )
    print(
        "FRESH_START_ALL_FAILED_HOMETOWNS_AFFORDABLE_BRIDGE_ITEM|witness="
        f"{int(audit.all_affordable)}"
    )
    print(
        "FRESH_START_ALL_FAILED_HOMETOWNS_STARTING_STONE_COVERS_SHOP_AND_AWARD|witness="
        f"{int(audit.all_combined_budget)}"
    )
    print(
        "FRESH_START_PURCHASE_INVENTORY_SLOT|witness="
        f"{int(audit.inventory_slot_witness)}"
    )
    print(
        "FRESH_START_SELECTED_WARPMAN_FREE_MSG|witness="
        f"{int(audit.all_free_msg)}"
    )
    print(
        "FRESH_START_SELECTED_WARPMAN_ACTION_STAGE_INERT|witness="
        f"{int(audit.action_stage_inert)}"
    )
    print(
        "FRESH_START_ALL_FAILED_HOMETOWNS_WARPMAN_EXECUTION_PREREQUISITES|witness="
        f"{int(audit.execution_prerequisites)}"
    )
    print(
        "RULE|execution prerequisite witness remains existential with respect to "
        "any recovered random WARP destination choice; it is not a guaranteed-RNG claim"
    )
    print(OUTPUT_RESOLUTION)


def main()->None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--npc-dir",type=Path,required=True)
    ap.add_argument("--data-dir",type=Path,required=True)
    ap.add_argument("--setup",type=Path,required=True)
    ap.add_argument("--server-map-root",type=Path,required=True)
    ap.add_argument("--mapset",type=Path,required=True)
    args=ap.parse_args()
    emit(analyze(
        npc_dir=args.npc_dir,
        data_dir=args.data_dir,
        setup=args.setup,
        server_map_root=args.server_map_root,
        mapset_path=args.mapset,
    ))


if __name__=="__main__":
    main()
