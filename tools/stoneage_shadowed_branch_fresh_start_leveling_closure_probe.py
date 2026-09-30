#!/usr/bin/env python3
"""Join fresh-start leveling combat into an ordered route to the award NPC.

This is the sequencing layer that was intentionally missing from the separate
leveling-source and combat audits.  A qualifying witness must be one concrete
one-hit combat witness whose encounter rectangle contains a recovered walkable
cell that is:

1. coordinate-reachable from the same normal fresh-start hometown; and
2. able to continue, through the directed recovered classic-Warp coordinate
   graph, to a valid key-item award interaction cell.

The repeated-battle argument is existential rather than a balance claim.  The
fixed descendant awards at least one EXP for a defeated positive-EXP enemy even
after level-gap decay.  Level-up grants free stat points but does not force
their allocation, so leaving new points unspent preserves the STR/DEX values
used by the one-hit witness.  Ordinary PvE battle creation reads the player's
current world coordinate and ordinary battle exit returns the player using the
same stored coordinate; the witness therefore remains at the encounter source
between repetitions.
"""

from __future__ import annotations

import argparse
import collections
from dataclasses import dataclass
from pathlib import Path

from tools.stoneage_encount_chain_probe import (
    configured_file,
    parse_encount,
    setup_values,
)
from tools.stoneage_ordered_runtime_world_reachability_probe import (
    load_ordered_runtime_reachability,
)
from tools.stoneage_server_static_map import parse_mapset_collision_profile
from tools.stoneage_shadowed_branch_coordinate_access_probe import (
    _conservative_npc_birth_blockers,
    _interaction_cells,
    _matching_award_placements,
)
from tools.stoneage_shadowed_branch_fresh_start_combat_probe import (
    analyze as analyze_combat,
)
from tools.stoneage_shadowed_branch_fresh_start_coordinate_probe import (
    FloorComponents,
    NORMAL_HOMETOWN_SPAWNS,
    _select_from_catalog,
    _server_catalog,
    _warp_edges,
)
from tools.stoneage_shadowed_branch_fresh_start_leveling_probe import (
    _reachable_components,
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
    "RESOLUTION|SHADOWED_BRANCH_FRESH_START_LEVELING_TO_TARGET_CLOSED"
)


@dataclass(frozen=True)
class LevelingClosureAudit:
    combat_witness_variants:int
    ordered_source_to_award_witnesses:int
    ordered_source_hometowns:int
    ambiguous_encounter_keys:int
    unresolved_reverse_map_floors:int
    leveling_reward_chain:bool

    @property
    def leveling_to_target(self)->bool:
        return (
            self.leveling_reward_chain
            and self.ordered_source_to_award_witnesses > 0
        )


def _ordered_area_point(
    origin_nav:FloorComponents,
    origin_components:set[int],
    continuation_nav:FloorComponents,
    continuation_components:set[int],
    area:dict,
)->tuple[int,int]|None:
    """Find one encounter cell satisfying both directed sequencing halves."""
    x1,x2=sorted((int(area["x1"]),int(area["x2"])))
    y1,y2=sorted((int(area["y1"]),int(area["y2"])))
    x1=max(0,x1); y1=max(0,y1)
    x2=min(origin_nav.map.width-1,x2)
    y2=min(origin_nav.map.height-1,y2)
    if x1>x2 or y1>y2:
        return None
    for y in range(y1,y2+1):
        for x in range(x1,x2+1):
            p=(x,y)
            before=origin_nav.component(p)
            if before is None or before not in origin_components:
                continue
            after=continuation_nav.component(p)
            if after is not None and after in continuation_components:
                return p
    return None


def analyze(
    *,
    npc_dir:Path,
    data_dir:Path,
    setup:Path,
    server_map_root:Path,
    mapset_path:Path,
    coordinate_report_text:str,
)->LevelingClosureAudit:
    combat=analyze_combat(
        npc_dir=npc_dir,
        data_dir=data_dir,
        setup=setup,
        server_map_root=server_map_root,
        mapset_path=mapset_path,
        coordinate_report_text=coordinate_report_text,
    )

    config=setup_values(setup)
    enc_path=configured_file(data_dir,config,"encountfile",["encount*.txt"])
    if enc_path is None:
        raise ValueError("active encounter file missing")
    _raw,encounters,bad,_widths=parse_encount(enc_path)
    if bad:
        raise ValueError("active encounter file malformed")

    areas_by_key:dict[tuple[int,int],list[dict]]=collections.defaultdict(list)
    for area in encounters:
        areas_by_key[(int(area["floor"]),int(area["index"]))].append(area)
    ambiguous={
        key for key,rows in areas_by_key.items()
        if len(rows)!=1
    }

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

    edges=_warp_edges(runtime)
    incoming:dict[int,list]=collections.defaultdict(list)
    warps_by_floor:dict[int,list]=collections.defaultdict(list)
    floor_ids={award_floor}
    floor_ids.update(int(area["floor"]) for area in encounters)
    floor_ids.update(int(floor) for floor,_x,_y in NORMAL_HOMETOWN_SPAWNS)
    for edge in edges:
        incoming[int(edge.destination_floor)].append(edge)
        warps_by_floor[int(edge.source_floor)].append(edge)
        floor_ids.add(int(edge.source_floor))
        floor_ids.add(int(edge.destination_floor))
    frozen_warps={floor:tuple(rows) for floor,rows in warps_by_floor.items()}

    catalog=_server_catalog(server_map_root)
    mapset=parse_mapset_collision_profile(mapset_path.read_bytes())
    blockers=_conservative_npc_birth_blockers(npc_dir,floor_ids=floor_ids)

    reverse_navs:dict[int,FloorComponents|None]={}
    unresolved=set()

    def reverse_nav(floor:int):
        floor=int(floor)
        if floor in reverse_navs:
            return reverse_navs[floor]
        selected=_select_from_catalog(catalog,mapset,floor)
        if selected.static_map is None:
            unresolved.add(floor)
            reverse_navs[floor]=None
            return None
        nav=FloorComponents(
            selected.static_map,
            blockers.get(floor,frozenset()),
        )
        reverse_navs[floor]=nav
        return nav

    award_nav=reverse_nav(award_floor)
    if award_nav is None:
        raise ValueError("award floor map unavailable")
    award_goals=_interaction_cells(award_nav.map,awards)
    if not award_goals:
        raise ValueError("award interaction cells missing")

    can_reach:set[tuple[int,int]]=set()
    reverse_components:dict[int,set[int]]=collections.defaultdict(set)
    queue=collections.deque()
    for goal in award_goals:
        component=award_nav.component(goal)
        if component is None:
            continue
        state=(award_floor,component)
        if state not in can_reach:
            can_reach.add(state)
            reverse_components[award_floor].add(component)
            queue.append(state)
    if not queue:
        raise ValueError("no unblocked award interaction component")

    while queue:
        floor,component=queue.popleft()
        dest_nav=reverse_nav(floor)
        if dest_nav is None:
            continue
        for edge in incoming.get(floor,()):
            if dest_nav.component(
                (int(edge.destination_x),int(edge.destination_y))
            ) != component:
                continue
            source_nav=reverse_nav(int(edge.source_floor))
            if source_nav is None:
                continue
            source_component=source_nav.component(
                (int(edge.source_x),int(edge.source_y))
            )
            if source_component is None:
                continue
            state=(int(edge.source_floor),source_component)
            if state in can_reach:
                continue
            can_reach.add(state)
            reverse_components[state[0]].add(state[1])
            queue.append(state)

    origin_cache={}
    ordered=[]
    for witness in combat.one_hit_witnesses:
        key=(int(witness.source_floor),int(witness.source_encounter_index))
        if key in ambiguous:
            continue
        rows=areas_by_key.get(key,())
        if len(rows)!=1:
            continue
        ordinal=int(witness.spawn_ordinal)
        if ordinal<1 or ordinal>len(NORMAL_HOMETOWN_SPAWNS):
            continue
        if ordinal not in origin_cache:
            origin_cache[ordinal]=_reachable_components(
                spawn=NORMAL_HOMETOWN_SPAWNS[ordinal-1],
                catalog=catalog,
                mapset=mapset,
                blockers=blockers,
                warps_by_floor=frozen_warps,
            )
        reachable,navigators,_origin_unresolved=origin_cache[ordinal]
        floor=int(witness.source_floor)
        origin_components=reachable.get(floor)
        continuation_components=reverse_components.get(floor)
        if not origin_components or not continuation_components:
            continue
        origin_nav=navigators.get(floor)
        continuation_nav=reverse_nav(floor)
        if origin_nav is None or continuation_nav is None:
            continue
        point=_ordered_area_point(
            origin_nav,
            origin_components,
            continuation_nav,
            continuation_components,
            rows[0],
        )
        if point is not None:
            ordered.append((ordinal,floor,point))

    return LevelingClosureAudit(
        combat_witness_variants=len(combat.one_hit_witnesses),
        ordered_source_to_award_witnesses=len(ordered),
        ordered_source_hometowns=len({row[0] for row in ordered}),
        ambiguous_encounter_keys=len(ambiguous),
        unresolved_reverse_map_floors=len(unresolved),
        leveling_reward_chain=bool(combat.leveling_reward_chain),
    )


def emit(audit:LevelingClosureAudit)->None:
    print("StoneAge shadowed-branch fresh-start leveling-to-target audit — R1")
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print(
        "PINNED_SOURCE_FACT|defeated_enemy_exp_level_difference_floor=1|"
        "level_up_free_stat_allocation_optional=1|"
        "ordinary_pve_battle_preserves_world_position=1"
    )
    print(
        "RULE|birth/target levels, EXP values, encounter/enemy/group ids, "
        "source coordinates and route floor ids are withheld"
    )
    print(
        "RULE|ordered witness is one concrete one-hit source cell that is "
        "coordinate-reachable from its fresh-start hometown and has a directed "
        "recovered classic-Warp coordinate continuation to the award NPC"
    )
    print(
        "RULE|repetition is existential: reuse the same legal one-enemy, "
        "weak-enemy-roll, player-first and successful-hit outcomes; unspent "
        "level-up points preserve the witness STR/DEX while each kill remains "
        "positive EXP"
    )
    print(
        "PREREQUISITE_LEVELING_REWARD_CHAIN|witness="
        f"{int(audit.leveling_reward_chain)}"
    )
    print(f"COUNT|combat_witness_variants|{audit.combat_witness_variants}")
    print(
        "COUNT|ordered_source_to_award_witnesses|"
        f"{audit.ordered_source_to_award_witnesses}"
    )
    print(
        "COUNT|ordered_source_hometowns|"
        f"{audit.ordered_source_hometowns}"
    )
    print(
        "COUNT|ambiguous_encounter_keys|"
        f"{audit.ambiguous_encounter_keys}"
    )
    print(
        "COUNT|unresolved_reverse_map_floors|"
        f"{audit.unresolved_reverse_map_floors}"
    )
    print(
        "FRESH_START_LEVELING_TO_TARGET|witness="
        f"{int(audit.leveling_to_target)}"
    )
    print(
        "GUARANTEED_OR_EFFICIENT_LEVELING|closed=0|"
        "reason=existential_rng_sequence_only"
    )
    print(OUTPUT_RESOLUTION)


def main()->None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--npc-dir",type=Path,required=True)
    ap.add_argument("--data-dir",type=Path,required=True)
    ap.add_argument("--setup",type=Path,required=True)
    ap.add_argument("--server-map-root",type=Path,required=True)
    ap.add_argument("--mapset",type=Path,required=True)
    ap.add_argument("--coordinate-report",type=Path,required=True)
    args=ap.parse_args()
    emit(analyze(
        npc_dir=args.npc_dir,
        data_dir=args.data_dir,
        setup=args.setup,
        server_map_root=args.server_map_root,
        mapset_path=args.mapset,
        coordinate_report_text=args.coordinate_report.read_text(
            encoding="utf-8"
        ),
    ))


if __name__=="__main__":
    main()
