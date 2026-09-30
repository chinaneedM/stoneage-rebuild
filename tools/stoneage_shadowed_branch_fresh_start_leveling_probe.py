#!/usr/bin/env python3
"""Audit fresh-start repeatable positive-EXP leveling provenance.

This probe does not claim combat victory.  It proves the narrower progression
mechanism needed before a combat-feasibility audit:

- a coordinate-reachable state from a normal fresh-start hometown intersects a
  recovered random-encounter rectangle;
- that encounter has an effective positive-weight, item-ungated group;
- that group has an effective positive-weight enemy variant that can produce
  strictly positive battle EXP under fixed-descendant semantics;
- the recovered EXP table contains finite positive requirements from the birth
  level to at least one joint ExChangeMan/WarpMan legal level.

The fixed-descendant battle source clamps EXP from a defeated enemy to at least
1 once level-difference reduction applies; enemy variants with EXP=-1 call
ENEMY_getExp(), which itself returns at least 1 for a valid positive enemy
level.  Combat victory itself remains a separate boundary.
"""

from __future__ import annotations

import argparse
import collections
from dataclasses import dataclass
from pathlib import Path

from tools.stoneage_encount_chain_probe import (
    configured_file,
    parse_encount,
    parse_enemy,
    setup_values,
)
from tools.stoneage_encounter_chain_probe import parse_group_file
from tools.stoneage_exp_probe import parse_exp
from tools.stoneage_ordered_runtime_world_reachability_probe import (
    load_ordered_runtime_reachability,
)
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
from tools.stoneage_shadowed_branch_fresh_start_level_probe import (
    _setup_unique_int,
)
from tools.stoneage_shadowed_branch_item_shop_acquisition_probe import (
    _locate_key_item,
)
from tools.stoneage_shadowed_branch_key_item_exchange_probe import (
    _event_records,
    _level_witnesses,
    _record_award,
)
from tools.stoneage_shadowed_branch_legal_state_reachability_probe import (
    _warp_gate_levels,
)
from tools.stoneage_shadowed_branch_warpman_satisfiability_probe import (
    _assigned_data,
    _configured_maxlevel,
)
from tools.stoneage_transport_usage_probe import iter_blocks, magic_kind, template_map


OUTPUT_RESOLUTION = "RESOLUTION|SHADOWED_BRANCH_FRESH_START_LEVELING_SOURCE_AUDITED"


@dataclass(frozen=True)
class ReachableState:
    floor:int
    component:int


@dataclass(frozen=True)
class ExpSource:
    spawn_ordinal:int
    floor:int
    enemy_min_level:int
    enemy_max_level:int
    enemy_exp_mode:str
    enemy_can_spawn_at_or_below_birth:bool


@dataclass(frozen=True)
class LevelingAudit:
    birth_level:int
    minimum_joint_level:int|None
    exp_requirements_complete:bool
    exp_requirements_positive:bool
    sources:tuple[ExpSource,...]
    unresolved_map_floors:int

    @property
    def target_above_birth(self)->bool:
        return (
            self.minimum_joint_level is not None
            and self.minimum_joint_level > self.birth_level
        )

    @property
    def repeatable_positive_exp_exists(self)->bool:
        return bool(self.sources)

    @property
    def low_level_source_exists(self)->bool:
        return any(x.enemy_can_spawn_at_or_below_birth for x in self.sources)

    @property
    def leveling_reward_chain(self)->bool:
        return (
            self.target_above_birth
            and self.exp_requirements_complete
            and self.exp_requirements_positive
            and self.repeatable_positive_exp_exists
        )


def _joint_levels(npc_dir:Path,setup:Path)->tuple[int,...]:
    maxlevel=_configured_maxlevel(setup)
    gate,_missing=_warp_gate_levels(npc_dir,maxlevel)
    gate_levels=set(gate.joint_levels)
    target,_missing_item=_locate_key_item(npc_dir)
    reached=set(load_ordered_runtime_reachability().reached_floor_ids)

    files=sorted(
        (p for p in npc_dir.rglob("*") if p.is_file()),
        key=lambda p:str(p).lower(),
    )
    templates=template_map([p for p in files if magic_kind(p)=="template"])
    exchange_names={
        name for name,defs in templates.items()
        if len(defs)==1 and defs[0].strip().lower()==b"exchangeman"
    }

    joint=set()
    for create in (p for p in files if magic_kind(p)=="create"):
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
                name,sep,arg=enemy.partition(b"|")
                if name.strip() not in exchange_names:
                    continue
                data=_assigned_data(npc_dir,arg if sep else b"")
                if data is None:
                    continue
                for record in _event_records(data):
                    award=_record_award(record,target,floor,maxlevel)
                    if award is None or award.type_class!="ACCEPT":
                        continue
                    joint.update(set(_level_witnesses(record,maxlevel)) & gate_levels)
    return tuple(sorted(joint))


def _reachable_components(
    *,
    spawn:tuple[int,int,int],
    catalog,
    mapset,
    blockers:dict[int,frozenset[tuple[int,int]]],
    warps_by_floor:dict[int,tuple],
)->tuple[dict[int,set[int]],dict[int,FloorComponents|None],set[int]]:
    start_floor,start_x,start_y=map(int,spawn)
    navigators={}
    unresolved=set()
    admitted={start_floor:frozenset({(start_x,start_y)})}

    def navigator(floor:int):
        floor=int(floor)
        if floor in navigators:
            return navigators[floor]
        selected=_select_from_catalog(catalog,mapset,floor)
        if selected.static_map is None:
            unresolved.add(floor)
            navigators[floor]=None
            return None
        nav=FloorComponents(
            selected.static_map,
            blockers.get(floor,frozenset()),
            admitted_origins=admitted.get(floor,frozenset()),
        )
        navigators[floor]=nav
        return nav

    nav=navigator(start_floor)
    if nav is None:
        return {},navigators,unresolved
    component=nav.component((start_x,start_y))
    if component is None:
        return {},navigators,unresolved

    queue=collections.deque([(start_floor,component)])
    seen={(start_floor,component)}
    by_floor:dict[int,set[int]]=collections.defaultdict(set)
    by_floor[start_floor].add(component)

    while queue:
        floor,component=queue.popleft()
        nav=navigator(floor)
        if nav is None:
            continue
        for edge in warps_by_floor.get(floor,()):
            if nav.component((edge.source_x,edge.source_y))!=component:
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
            by_floor[edge.destination_floor].add(dest_component)
            queue.append(state)

    return dict(by_floor),navigators,unresolved


def _area_component_reachable(
    nav:FloorComponents,
    components:set[int],
    area:dict,
)->bool:
    x1,x2=sorted((int(area["x1"]),int(area["x2"])))
    y1,y2=sorted((int(area["y1"]),int(area["y2"])))
    x1=max(0,x1);y1=max(0,y1)
    x2=min(nav.map.width-1,x2);y2=min(nav.map.height-1,y2)
    if x1>x2 or y1>y2:
        return False
    for y in range(y1,y2+1):
        for x in range(x1,x2+1):
            component=nav.component((x,y))
            if component is not None and component in components:
                return True
    return False


def _normalized_level_range(enemy:dict)->tuple[int,int]:
    lo=int(enemy["lv_min"]); hi=int(enemy["lv_max"])
    if lo==0:
        lo=hi
    lo=min(lo,hi); hi=max(lo,hi)
    return lo,hi


def _positive_exp_mode(enemy:dict)->str|None:
    lo,hi=_normalized_level_range(enemy)
    if hi < 1:
        return None
    override=int(enemy["exp"])
    if override == -1:
        return "COMPUTED_MIN_ONE"
    if override > 0:
        return "POSITIVE_OVERRIDE"
    return None


def analyze(
    *,
    npc_dir:Path,
    data_dir:Path,
    setup:Path,
    server_map_root:Path,
    mapset_path:Path,
)->LevelingAudit:
    birth=_setup_unique_int(setup,"LV")
    if birth>160:
        birth=160
    joint=_joint_levels(npc_dir,setup)
    target=min(joint) if joint else None

    config=setup_values(setup)
    exp_path=configured_file(data_dir,config,"userexp",["exp*.txt"])
    if exp_path is None:
        raise ValueError("active recovered EXP file missing")
    exp_rows,exp_bad=parse_exp(exp_path)
    if exp_bad:
        raise ValueError("active recovered EXP file contains malformed rows")
    exp_values=[int(value) for _label,value in exp_rows]

    complete=False
    positive=False
    if target is not None and target>birth:
        # CHAR_LevelUpCheck requests the next-level threshold.  Require every
        # row from birth through target-1 to exist and be positive.
        needed=list(range(max(1,birth),target))
        complete=bool(needed) and all(level<=len(exp_values) for level in needed)
        positive=complete and all(exp_values[level-1]>0 for level in needed)

    ep=configured_file(data_dir,config,"encountfile",["encount*.txt"])
    gp=configured_file(data_dir,config,"groupfile",["group*.txt"])
    xp=configured_file(data_dir,config,"enemyfile",["enemy*.txt"])
    if not ep or not gp or not xp:
        raise ValueError("active encounter/group/enemy source missing")

    _eraw,encounters,enc_bad,_ew=parse_encount(ep)
    _xraw,enemies,enemy_bad,_xw,_prefix=parse_enemy(xp)
    if enc_bad or enemy_bad:
        raise ValueError("active encounter/enemy source malformed")
    enemy_by_id={int(row["id"]):row for row in enemies}

    parsed_groups=parse_group_file(gp,set(enemy_by_id))
    if parsed_groups["bad"]:
        raise ValueError("active group source malformed")
    groups_by_id={
        int(row["GROUP_ID"]):row for row in parsed_groups["loaded_rows"]
    }

    runtime=load_ordered_runtime_reachability().runtime
    edges=_warp_edges(runtime)
    warps_by_floor:dict[int,list]=collections.defaultdict(list)
    floor_ids={int(row["floor"]) for row in encounters}
    for edge in edges:
        warps_by_floor[edge.source_floor].append(edge)
        floor_ids.add(edge.source_floor);floor_ids.add(edge.destination_floor)
    for floor,_x,_y in NORMAL_HOMETOWN_SPAWNS:
        floor_ids.add(int(floor))
    frozen_warps={floor:tuple(rows) for floor,rows in warps_by_floor.items()}

    catalog=_server_catalog(server_map_root)
    mapset=parse_mapset_collision_profile(mapset_path.read_bytes())
    blockers=_conservative_npc_birth_blockers(npc_dir,floor_ids=floor_ids)

    sources=[]
    unresolved_all=set()
    # Only the two already-proven coordinate-valid normal hometowns are needed
    # for existential fresh-start provenance, but detect validity again rather
    # than hard-code an output report dependency.
    for ordinal,spawn in enumerate(NORMAL_HOMETOWN_SPAWNS,1):
        reachable,navigators,unresolved=_reachable_components(
            spawn=spawn,
            catalog=catalog,
            mapset=mapset,
            blockers=blockers,
            warps_by_floor=frozen_warps,
        )
        unresolved_all.update(unresolved)
        for area in encounters:
            floor=int(area["floor"])
            components=reachable.get(floor)
            if not components:
                continue
            if int(area["pmax"])<=0:
                continue
            nav=navigators.get(floor)
            if nav is None or not _area_component_reachable(nav,components,area):
                continue

            for group_id,group_weight in zip(
                area["groupids"],area["groupprobs"]
            ):
                group_id=int(group_id)
                group_weight=int(group_weight)
                if group_id<0 or group_weight<=0:
                    continue
                group=groups_by_id.get(group_id)
                if group is None:
                    continue
                # Avoid any inventory-state assumption for the leveling source.
                if int(group["APPEAR_ITEM"])!=-1 or int(group["NOT_APPEAR_ITEM"])!=-1:
                    continue
                for i in range(1,11):
                    enemy_id=int(group[f"ENEMY_ID{i}"])
                    weight=int(group[f"CREATE_PROB{i}"])
                    if enemy_id<0 or weight<=0:
                        continue
                    enemy=enemy_by_id.get(enemy_id)
                    if enemy is None or int(enemy["create_max"])<=0:
                        continue
                    mode=_positive_exp_mode(enemy)
                    if mode is None:
                        continue
                    lo,hi=_normalized_level_range(enemy)
                    sources.append(ExpSource(
                        spawn_ordinal=ordinal,
                        floor=floor,
                        enemy_min_level=lo,
                        enemy_max_level=hi,
                        enemy_exp_mode=mode,
                        enemy_can_spawn_at_or_below_birth=(lo<=birth),
                    ))

    # Deduplicate while preserving only derived characteristics.
    unique={}
    for row in sources:
        key=(
            row.spawn_ordinal,row.floor,row.enemy_min_level,row.enemy_max_level,
            row.enemy_exp_mode,row.enemy_can_spawn_at_or_below_birth,
        )
        unique.setdefault(key,row)

    return LevelingAudit(
        birth_level=birth,
        minimum_joint_level=target,
        exp_requirements_complete=complete,
        exp_requirements_positive=positive,
        sources=tuple(unique.values()),
        unresolved_map_floors=len(unresolved_all),
    )


def emit(audit:LevelingAudit)->None:
    print("StoneAge shadowed-branch fresh-start leveling-source audit — R1")
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print(
        "PINNED_SOURCE_FACT|defeated_enemy_exp_level_difference_floor=1|"
        "computed_enemy_exp_valid_level_floor=1"
    )
    print(
        "RULE|birth/target levels, EXP values, enemy/group ids, encounter "
        "coordinates and route floor ids are withheld"
    )
    print(
        "RULE|qualifying encounter source must be coordinate-reachable, have "
        "positive encounter/group/enemy weights, use an effective loaded group, "
        "require no appear/not-appear item gate, and resolve to a positive-EXP "
        "enemy variant"
    )
    print(
        "RULE|this closes reward-source mechanics only; it does not yet prove "
        "that the fresh character can win a qualifying battle"
    )
    print(f"COUNT|repeatable_positive_exp_sources|{len(audit.sources)}")
    print(
        "COUNT|sources_with_enemy_spawn_at_or_below_birth_level|"
        f"{sum(x.enemy_can_spawn_at_or_below_birth for x in audit.sources)}"
    )
    print(f"COUNT|source_hometowns|{len({x.spawn_ordinal for x in audit.sources})}")
    print(f"COUNT|unresolved_map_floors|{audit.unresolved_map_floors}")
    print(
        "LEVEL_TARGET|"
        f"above_birth={int(audit.target_above_birth)}|"
        f"exp_rows_complete={int(audit.exp_requirements_complete)}|"
        f"exp_rows_positive={int(audit.exp_requirements_positive)}|"
        "values_withheld=1"
    )
    print(
        "REPEATABLE_POSITIVE_EXP_SOURCE|witness="
        f"{int(audit.repeatable_positive_exp_exists)}"
    )
    print(
        "BIRTH_LEVEL_OR_LOWER_ENEMY_SOURCE|witness="
        f"{int(audit.low_level_source_exists)}"
    )
    print(
        "FRESH_START_LEVELING_REWARD_CHAIN|witness="
        f"{int(audit.leveling_reward_chain)}"
    )
    print(
        "COMBAT_VICTORY_FEASIBILITY|closed=0|"
        "reason=positive_exp_source_does_not_by_itself_prove_winnable_battle"
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
