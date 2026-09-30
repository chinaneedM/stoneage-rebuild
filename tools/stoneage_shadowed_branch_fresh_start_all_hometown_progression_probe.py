#!/usr/bin/env python3
"""Prove ordered fresh-start progression from every normal hometown.

A qualifying route must include a recovered repeatable positive-EXP source
with a legal fresh-character one-hit victory witness before the final award.
For the two hometowns whose classic coordinate graph is disconnected, it must
also acquire the selected WarpMan ITEM from an affordable normal ItemShop and
then traverse exactly the recovered WarpMan bridge selected by the spatial
audit.  The state search itself enforces ordering; facts are not merely joined.
"""

from __future__ import annotations

import argparse
import collections
from dataclasses import dataclass
from pathlib import Path

from tools.stoneage_encount_chain_probe import configured_file,parse_encount,setup_values
from tools.stoneage_ordered_runtime_world_reachability_probe import load_ordered_runtime_reachability
from tools.stoneage_server_static_map import parse_mapset_collision_profile
from tools.stoneage_shadowed_branch_coordinate_access_probe import (
    InteractionPlacement,_conservative_npc_birth_blockers,_interaction_cells,
    _matching_award_placements,
)
from tools.stoneage_shadowed_branch_fresh_start_combat_probe import analyze as analyze_combat
from tools.stoneage_shadowed_branch_fresh_start_coordinate_probe import (
    FloorComponents,NORMAL_HOMETOWN_SPAWNS,_select_from_catalog,_server_catalog,_warp_edges,
)
from tools.stoneage_shadowed_branch_fresh_start_dialogue_warp_bridge_probe import (
    WARPMAN,DialogueWarp,analyze as analyze_bridges,
)
from tools.stoneage_shadowed_branch_fresh_start_stone_probe import analyze as analyze_fresh_stone
from tools.stoneage_shadowed_branch_fresh_start_warpman_bridge_item_surface_probe import _requirements
from tools.stoneage_shadowed_branch_fresh_start_warpman_bridge_shop_route_probe import (
    _adjacent_cells,_collect_target_shops,_target_item_cost,
)
from tools.stoneage_shadowed_branch_item_shop_acquisition_probe import _locate_key_item
from tools.stoneage_shadowed_branch_progression_witness_probe import _award_records
from tools.stoneage_shadowed_branch_warpman_satisfiability_probe import (
    _configured_itemset_paths,_configured_maxlevel,_item_ids,
)

OUTPUT_RESOLUTION="RESOLUTION|SHADOWED_BRANCH_FRESH_START_ALL_HOMETOWN_PROGRESSION_AUDITED"

@dataclass(frozen=True)
class HometownRoute:
    ordinal:int
    combat_witnesses:int
    requires_shop:bool
    requires_warpman:bool
    ordered:bool
    milestone_order:tuple[str,...]
    visited_states:int
    unresolved_map_floors:int

@dataclass(frozen=True)
class AllHometownAudit:
    rows:tuple[HometownRoute,...]
    shop_execution_prerequisites:bool
    leveling_reward_chain:bool
    downstream_progression:bool
    materializable_world_closed:bool

    @property
    def all_ordered(self)->bool:
        return len(self.rows)==len(NORMAL_HOMETOWN_SPAWNS) and all(r.ordered for r in self.rows)

    @property
    def all_full_world(self)->bool:
        return (
            self.all_ordered and self.shop_execution_prerequisites
            and self.leveling_reward_chain and self.downstream_progression
            and self.materializable_world_closed
        )

def _report_has(text:str,line:str)->bool:
    return any(raw.strip()==line for raw in str(text).splitlines())

def _synthetic_all_hometown_coordinate_report()->str:
    return "\n".join(
        f"FRESH_START_COORDINATE_WITNESS|ordinal={i}|reachable=1"
        for i in range(1,len(NORMAL_HOMETOWN_SPAWNS)+1)
    )

def _area_components(nav:FloorComponents,area:dict)->set[int]:
    x1,x2=sorted((int(area["x1"]),int(area["x2"])))
    y1,y2=sorted((int(area["y1"]),int(area["y2"])))
    x1=max(0,x1); y1=max(0,y1)
    x2=min(nav.map.width-1,x2); y2=min(nav.map.height-1,y2)
    out=set()
    if x1>x2 or y1>y2:
        return out
    for y in range(y1,y2+1):
        for x in range(x1,x2+1):
            c=nav.component((x,y))
            if c is not None:
                out.add(int(c))
    return out

def _route(
    *,ordinal:int,spawn:tuple[int,int,int],witnesses,
    areas_by_key:dict[tuple[int,int],tuple[dict,...]],
    award_floor:int,award_placements,shops,bridge:DialogueWarp|None,
    classic_by_floor:dict[int,tuple],catalog,mapset,
    blockers:dict[int,frozenset[tuple[int,int]]],
)->HometownRoute:
    start_floor,start_x,start_y=map(int,spawn)
    admitted={start_floor:frozenset({(start_x,start_y)})}
    navs={}; unresolved=set()

    def nav(floor:int):
        floor=int(floor)
        if floor in navs:
            return navs[floor]
        selected=_select_from_catalog(catalog,mapset,floor)
        if selected.static_map is None:
            unresolved.add(floor); navs[floor]=None; return None
        row=FloorComponents(
            selected.static_map,blockers.get(floor,frozenset()),
            admitted_origins=admitted.get(floor,frozenset()),
        )
        navs[floor]=row
        return row

    start_nav=nav(start_floor)
    start_component=start_nav.component((start_x,start_y)) if start_nav is not None else None
    if start_component is None:
        return HometownRoute(ordinal,len(witnesses),bridge is not None,bridge is not None,False,(),0,len(unresolved))

    witness_areas_by_floor=collections.defaultdict(list)
    for witness in witnesses:
        key=(int(witness.source_floor),int(witness.source_encounter_index))
        rows=areas_by_key.get(key,())
        if len(rows)==1:
            witness_areas_by_floor[key[0]].append(rows[0])

    shops_by_floor=collections.defaultdict(list)
    for shop in shops:
        shops_by_floor[int(shop.floor_id)].append(shop)

    cache={}
    def combat_here(floor:int,component:int)->bool:
        key=("combat",int(floor))
        if key not in cache:
            current=nav(floor); comps=set()
            if current is not None:
                for area in witness_areas_by_floor.get(int(floor),()):
                    comps.update(_area_components(current,area))
            cache[key]=comps
        return int(component) in cache[key]

    def shop_here(floor:int,component:int)->bool:
        key=("shop",int(floor))
        if key not in cache:
            current=nav(floor); comps=set()
            if current is not None:
                for shop in shops_by_floor.get(int(floor),()):
                    for point in _adjacent_cells(current.map,shop.birth_rect):
                        c=current.component(point)
                        if c is not None: comps.add(int(c))
            cache[key]=comps
        return int(component) in cache[key]

    award_components=None
    def award_here(floor:int,component:int)->bool:
        nonlocal award_components
        if int(floor)!=int(award_floor): return False
        if award_components is None:
            current=nav(award_floor); comps=set()
            if current is not None:
                for point in _interaction_cells(current.map,award_placements):
                    c=current.component(point)
                    if c is not None: comps.add(int(c))
            award_components=comps
        return int(component) in award_components

    bridge_components=None
    def bridge_here(floor:int,component:int)->bool:
        nonlocal bridge_components
        if bridge is None or int(floor)!=int(bridge.source_floor): return False
        if bridge_components is None:
            current=nav(bridge.source_floor); comps=set()
            if current is not None:
                placement=InteractionPlacement(
                    floor_id=int(bridge.source_floor),birth_rect=bridge.source_rect
                )
                for point in _interaction_cells(current.map,(placement,)):
                    c=current.component(point)
                    if c is not None: comps.add(int(c))
            bridge_components=comps
        return int(component) in bridge_components

    requires_bridge=bridge is not None
    start=(start_floor,int(start_component),False,not requires_bridge,not requires_bridge)
    queue=collections.deque([start]); seen={start}; parent={}; final=None

    def enqueue(state,previous,label):
        if state in seen: return
        seen.add(state); parent[state]=(previous,label); queue.append(state)

    while queue:
        state=queue.popleft()
        floor,component,combat_done,shop_done,bridge_done=state
        if combat_done and shop_done and bridge_done and award_here(floor,component):
            final=state; break

        if not combat_done and combat_here(floor,component):
            enqueue((floor,component,True,shop_done,bridge_done),state,"COMBAT")
        if requires_bridge and not shop_done and shop_here(floor,component):
            enqueue((floor,component,combat_done,True,bridge_done),state,"SHOP")

        current=nav(floor)
        if current is None: continue
        for edge in classic_by_floor.get(int(floor),()):
            if current.component((int(edge.source_x),int(edge.source_y)))!=component:
                continue
            dest=nav(int(edge.destination_floor))
            if dest is None: continue
            dc=dest.component((int(edge.destination_x),int(edge.destination_y)))
            if dc is None: continue
            enqueue(
                (int(edge.destination_floor),int(dc),combat_done,shop_done,bridge_done),
                state,None
            )

        if (
            requires_bridge and not bridge_done and combat_done and shop_done
            and bridge_here(floor,component)
        ):
            dest=nav(int(bridge.destination_floor))
            if dest is not None:
                dc=dest.component((int(bridge.destination_x),int(bridge.destination_y)))
                if dc is not None:
                    enqueue(
                        (int(bridge.destination_floor),int(dc),combat_done,shop_done,True),
                        state,"WARPMAN"
                    )

    milestones=[]
    if final is not None:
        cursor=final
        while cursor!=start:
            previous,label=parent[cursor]
            if label is not None: milestones.append(label)
            cursor=previous
        milestones.reverse()

    return HometownRoute(
        ordinal=int(ordinal),combat_witnesses=len(witnesses),
        requires_shop=requires_bridge,requires_warpman=requires_bridge,
        ordered=final is not None,milestone_order=tuple(milestones),
        visited_states=len(seen),unresolved_map_floors=len(unresolved),
    )

def analyze(
    *,npc_dir:Path,data_dir:Path,setup:Path,server_map_root:Path,
    mapset_path:Path,shop_report_text:str,progression_report_text:str,
    world_report_text:str,
)->AllHometownAudit:
    shop_prereq=_report_has(
        shop_report_text,
        "FRESH_START_ALL_FAILED_HOMETOWNS_WARPMAN_EXECUTION_PREREQUISITES|witness=1",
    )
    if not shop_prereq:
        raise ValueError("WarpMan shop/execution prerequisite report is not closed")

    combat=analyze_combat(
        npc_dir=npc_dir,data_dir=data_dir,setup=setup,
        server_map_root=server_map_root,mapset_path=mapset_path,
        coordinate_report_text=_synthetic_all_hometown_coordinate_report(),
        preserve_spawn_identity=True,
    )
    witnesses_by_ordinal=collections.defaultdict(list)
    for witness in combat.one_hit_witnesses:
        witnesses_by_ordinal[int(witness.spawn_ordinal)].append(witness)

    config=setup_values(setup)
    enc_path=configured_file(data_dir,config,"encountfile",["encount*.txt"])
    if enc_path is None: raise ValueError("active encounter file missing")
    _raw,encounters,bad,_widths=parse_encount(enc_path)
    if bad: raise ValueError("active encounter file malformed")
    temp=collections.defaultdict(list)
    for area in encounters:
        temp[(int(area["floor"]),int(area["index"]))].append(area)
    areas_by_key={k:tuple(v) for k,v in temp.items()}

    runtime_audit=load_ordered_runtime_reachability()
    runtime=runtime_audit.runtime
    reached=set(runtime_audit.reached_floor_ids)
    target,_missing=_locate_key_item(npc_dir)
    maxlevel=_configured_maxlevel(setup)
    accepted=_award_records(npc_dir,target_item=target,maxlevel=maxlevel,reached=reached)
    accepted_records={(int(floor),record) for floor,record,_levels in accepted}
    award_floors={int(floor) for floor,_record,_levels in accepted}
    if len(award_floors)!=1: raise ValueError("award floor identity is not unique")
    award_floor=next(iter(award_floors))
    award_placements=_matching_award_placements(npc_dir,accepted_records)
    if not award_placements: raise ValueError("award placements missing")

    bridge_audit=analyze_bridges(
        npc_dir=npc_dir,setup=setup,server_map_root=server_map_root,mapset_path=mapset_path
    )
    bridges={}; bridge_edges=[]
    for pair in bridge_audit.rows:
        if pair.baseline_classic.reachable:
            bridges[int(pair.ordinal)]=None
            continue
        edges=pair.baseline_warpman.edge_sequence
        if not pair.baseline_warpman.reachable or len(edges)!=1 or edges[0].kind!=WARPMAN:
            raise ValueError("failed hometown lacks one selected WarpMan bridge")
        bridges[int(pair.ordinal)]=edges[0]; bridge_edges.append(edges[0])

    requirements=[]
    for ordinal,edge in sorted((o,e) for o,e in bridges.items() if e is not None):
        requirements.extend(_requirements(ordinal,(edge,)))
    item_ids={int(req.item_id) for req in requirements}
    if len(item_ids)!=1: raise ValueError("selected bridge item identity is not unique")
    bridge_item=next(iter(item_ids))

    item_paths=_configured_itemset_paths(setup,data_dir)
    active_item_ids=_item_ids(item_paths)
    base_cost=_target_item_cost(item_paths,bridge_item)
    all_shops=_collect_target_shops(
        npc_dir=npc_dir,target_item=bridge_item,
        active_item_ids=active_item_ids,base_cost=base_cost,
    )
    stone=analyze_fresh_stone(npc_dir=npc_dir,setup=setup)
    if stone.minimum_fee is None: raise ValueError("award fee unavailable")
    shops=tuple(
        shop for shop in all_shops
        if shop.normal_buy_invocable
        and int(stone.initial_stone)>=int(shop.purchase_cost)+int(stone.minimum_fee)
    )
    if not shops: raise ValueError("no combined-budget bridge shop")

    classic=_warp_edges(runtime)
    classic_by_floor=collections.defaultdict(list)
    floor_ids={int(award_floor)}
    for edge in classic:
        classic_by_floor[int(edge.source_floor)].append(edge)
        floor_ids.add(int(edge.source_floor)); floor_ids.add(int(edge.destination_floor))
    classic_by_floor={f:tuple(v) for f,v in classic_by_floor.items()}
    for floor,_x,_y in NORMAL_HOMETOWN_SPAWNS: floor_ids.add(int(floor))
    for witness in combat.one_hit_witnesses: floor_ids.add(int(witness.source_floor))
    for shop in shops: floor_ids.add(int(shop.floor_id))
    for edge in bridge_edges:
        floor_ids.add(int(edge.source_floor)); floor_ids.add(int(edge.destination_floor))

    catalog=_server_catalog(server_map_root)
    mapset=parse_mapset_collision_profile(mapset_path.read_bytes())
    blockers=_conservative_npc_birth_blockers(npc_dir,floor_ids=floor_ids)

    rows=tuple(
        _route(
            ordinal=ordinal,spawn=spawn,
            witnesses=tuple(witnesses_by_ordinal.get(ordinal,())),
            areas_by_key=areas_by_key,award_floor=award_floor,
            award_placements=award_placements,shops=shops,
            bridge=bridges.get(ordinal),classic_by_floor=classic_by_floor,
            catalog=catalog,mapset=mapset,blockers=blockers,
        )
        for ordinal,spawn in enumerate(NORMAL_HOMETOWN_SPAWNS,1)
    )
    downstream=_report_has(progression_report_text,"COUNT|combined_progression_witness|1")
    world_closed=(
        _report_has(world_report_text,"COUNT|remaining_unreachable_floor_ids|0")
        and _report_has(world_report_text,"RESOLUTION|STATE_GATED_RUNTIME_WORLD_REACHABILITY_CLOSED")
    )
    return AllHometownAudit(
        rows=rows,shop_execution_prerequisites=shop_prereq,
        leveling_reward_chain=bool(combat.leveling_reward_chain),
        downstream_progression=downstream,materializable_world_closed=world_closed,
    )

def emit(audit:AllHometownAudit)->None:
    print("StoneAge all-hometown ordered fresh-start progression audit — R1")
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print("RULE|coordinates, item/enemy/NPC identities and raw route details are withheld")
    print("RULE|COMBAT is a coordinate-reachable repeatable positive-EXP source with a legal one-hit existential victory witness; finite repetition to the closed joint target uses the already-pinned leveling argument")
    print("RULE|bridge hometowns require COMBAT and SHOP before the selected WarpMan transition; direct hometowns require COMBAT before award interaction")
    print("RULE|combat and WarpMan destination outcomes remain existential legal RNG witnesses, not guarantee or pacing claims")
    print(
        "PREREQUISITE|"
        f"bridge_shop_execution={int(audit.shop_execution_prerequisites)}|"
        f"leveling_reward_chain={int(audit.leveling_reward_chain)}|"
        f"downstream_progression={int(audit.downstream_progression)}|"
        f"materializable_world_closed={int(audit.materializable_world_closed)}"
    )
    for row in audit.rows:
        print(
            "ALL_HOMETOWN_ORDERED_ROUTE|"
            f"ordinal={row.ordinal}|combat_witnesses={row.combat_witnesses}|"
            f"requires_shop={int(row.requires_shop)}|"
            f"requires_warpman={int(row.requires_warpman)}|ordered={int(row.ordered)}|"
            f"milestones={'>'.join(row.milestone_order) if row.milestone_order else 'NONE'}|"
            f"visited_states={row.visited_states}|unresolved_map_floors={row.unresolved_map_floors}"
        )
    print(f"FRESH_START_ALL_HOMETOWNS_ORDERED_PROGRESSION|witness={int(audit.all_ordered)}")
    print(f"ALL_HOMETOWNS_FULL_WORLD|closed={int(audit.all_full_world)}")
    print(OUTPUT_RESOLUTION)

def main()->None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--npc-dir",type=Path,required=True)
    ap.add_argument("--data-dir",type=Path,required=True)
    ap.add_argument("--setup",type=Path,required=True)
    ap.add_argument("--server-map-root",type=Path,required=True)
    ap.add_argument("--mapset",type=Path,required=True)
    ap.add_argument("--shop-report",type=Path,required=True)
    ap.add_argument("--progression-report",type=Path,required=True)
    ap.add_argument("--world-report",type=Path,required=True)
    a=ap.parse_args()
    emit(analyze(
        npc_dir=a.npc_dir,data_dir=a.data_dir,setup=a.setup,
        server_map_root=a.server_map_root,mapset_path=a.mapset,
        shop_report_text=a.shop_report.read_text(encoding="utf-8"),
        progression_report_text=a.progression_report.read_text(encoding="utf-8"),
        world_report_text=a.world_report.read_text(encoding="utf-8"),
    ))

if __name__=="__main__":
    main()
