#!/usr/bin/env python3
"""Audit fresh-character floor-level spatial reachability.

Pinned fixed-descendant source control:
- CHAR_createNewChar calls CHAR_getInitElderPosition();
- with the committed version.h control (_DELBORNPLACE and _MUSEUM disabled),
  hometown 0..3 yields the four normal elder floors;
- later compile-time variants can redirect new characters through 815/9000.

The recovered25 build flags are not inferred here. Instead every source-known
spawn-floor variant is tested against the recovered25 ordered active classic
Warp graph. If all variants reach the key-item award floor, the compile-mode
ambiguity is immaterial for floor-level fresh-start reachability.

Coordinates are intentionally deferred to the next coordinate-stage audit.
"""

from __future__ import annotations

import argparse
import collections
from dataclasses import dataclass
from pathlib import Path

from tools.stoneage_ordered_runtime_world_reachability_probe import (
    load_ordered_runtime_reachability,
)


OUTPUT_RESOLUTION = "RESOLUTION|SHADOWED_BRANCH_FRESH_START_FLOOR_REACHABILITY_AUDITED"

# Directly recovered from the pinned fixed-descendant CHAR_getInitElderPosition
# source. Coordinates are withheld from this floor-only derived report.
NORMAL_HOMETOWN_FLOORS = (1006, 2006, 3006, 4006)
LATER_VARIANT_FLOORS = (815, 9000)


def _award_floor(legal_state_text: str) -> int:
    floors=set()
    for raw in str(legal_state_text).splitlines():
        line=raw.strip()
        if not line.startswith("EXCHANGE_CHAIN_WITNESS|"):
            continue
        fields={}
        for part in line.split("|")[1:]:
            if "=" not in part:
                continue
            key,value=part.split("=",1)
            fields[key]=value
        floors.add(int(fields["source_floor"]))
    if len(floors)!=1:
        raise ValueError(f"expected one award floor, found {sorted(floors)}")
    return next(iter(floors))


def _adjacency(runtime) -> dict[int, tuple[int,...]]:
    out:dict[int,set[int]]=collections.defaultdict(set)
    for edge in runtime.topology.legacy_warps:
        out[int(edge.source.floor_id)].add(int(edge.destination.floor_id))
    return {floor:tuple(sorted(values)) for floor,values in out.items()}


def _shortest_path(
    graph:dict[int,tuple[int,...]],
    start:int,
    target:int,
)->tuple[int,...]|None:
    start=int(start); target=int(target)
    if start==target:
        return (start,)
    queue=collections.deque([start])
    previous={start:None}
    while queue:
        floor=queue.popleft()
        for destination in graph.get(floor,()):
            if destination in previous:
                continue
            previous[destination]=floor
            if destination==target:
                path=[target]
                node=target
                while previous[node] is not None:
                    node=previous[node]
                    path.append(node)
                return tuple(reversed(path))
            queue.append(destination)
    return None


@dataclass(frozen=True)
class SpawnFloorWitness:
    floor_id:int
    source_class:str
    path:tuple[int,...]|None

    @property
    def reachable(self)->bool:
        return self.path is not None

    @property
    def hops(self)->int|None:
        if self.path is None:
            return None
        return max(0,len(self.path)-1)


@dataclass(frozen=True)
class FreshStartFloorAudit:
    award_floor:int
    witnesses:tuple[SpawnFloorWitness,...]

    @property
    def normal_rows(self)->tuple[SpawnFloorWitness,...]:
        return tuple(x for x in self.witnesses if x.source_class=="NORMAL_HOMETOWN")

    @property
    def variant_rows(self)->tuple[SpawnFloorWitness,...]:
        return tuple(x for x in self.witnesses if x.source_class=="LATER_VARIANT")

    @property
    def normal_closed(self)->bool:
        return bool(self.normal_rows) and all(x.reachable for x in self.normal_rows)

    @property
    def all_source_known_closed(self)->bool:
        return bool(self.witnesses) and all(x.reachable for x in self.witnesses)


def analyze(*,legal_state_text:str)->FreshStartFloorAudit:
    runtime=load_ordered_runtime_reachability().runtime
    graph=_adjacency(runtime)
    target=_award_floor(legal_state_text)
    rows=[]
    for floor in NORMAL_HOMETOWN_FLOORS:
        rows.append(SpawnFloorWitness(
            floor_id=floor,
            source_class="NORMAL_HOMETOWN",
            path=_shortest_path(graph,floor,target),
        ))
    for floor in LATER_VARIANT_FLOORS:
        rows.append(SpawnFloorWitness(
            floor_id=floor,
            source_class="LATER_VARIANT",
            path=_shortest_path(graph,floor,target),
        ))
    return FreshStartFloorAudit(award_floor=target,witnesses=tuple(rows))


def emit(audit:FreshStartFloorAudit)->None:
    print("StoneAge shadowed-branch fresh-start floor reachability — R1")
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print(
        "PINNED_SOURCE_CONTROL|normal_hometowns=4|"
        "delbornplace_define_enabled=0|museum_define_enabled=0"
    )
    print(
        "RULE|four normal hometown floors and two later compile-time spawn "
        "variants are tested; spawn coordinates and intermediate floor ids "
        "are withheld from this report"
    )
    print(
        "RULE|testing later variants does not claim recovered25 enabled those "
        "compile options; it tests whether that ambiguity matters"
    )
    normal=audit.normal_rows
    variants=audit.variant_rows
    print(f"COUNT|normal_hometown_candidates|{len(normal)}")
    print(f"COUNT|normal_hometown_reachable|{sum(x.reachable for x in normal)}")
    print(f"COUNT|later_variant_candidates|{len(variants)}")
    print(f"COUNT|later_variant_reachable|{sum(x.reachable for x in variants)}")
    print(f"COUNT|all_source_known_candidates|{len(audit.witnesses)}")
    print(f"COUNT|all_source_known_reachable|{sum(x.reachable for x in audit.witnesses)}")
    for ordinal,row in enumerate(audit.witnesses,1):
        print(
            "SPAWN_FLOOR_WITNESS|"
            f"ordinal={ordinal}|class={row.source_class}|"
            f"reachable={int(row.reachable)}|"
            f"hops={row.hops if row.hops is not None else -1}|"
            "floor_id_withheld=1|intermediate_floors_withheld=1"
        )
    print(f"NORMAL_FRESH_START_FLOOR_CHAIN|witness={int(audit.normal_closed)}")
    print(
        "ALL_SOURCE_KNOWN_SPAWN_VARIANTS_FLOOR_CHAIN|witness="
        f"{int(audit.all_source_known_closed)}"
    )
    print(OUTPUT_RESOLUTION)


def main()->None:
    parser=argparse.ArgumentParser()
    parser.add_argument("--legal-state-report",type=Path,required=True)
    args=parser.parse_args()
    emit(analyze(
        legal_state_text=args.legal_state_report.read_text(encoding="utf-8")
    ))


if __name__=="__main__":
    main()
