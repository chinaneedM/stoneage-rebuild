#!/usr/bin/env python3
"""Recompute recovered25 floor reachability with validated state-gated transport.

Classic Warp reachability remains unchanged and separately reported.  This layer
adds only cross-floor transports whose prerequisite progression has a closed
legal-player-state witness.  It therefore computes *existential state-gated*
runtime reachability, not unconditional fresh-character reachability.
"""

from __future__ import annotations

import argparse
import collections
from dataclasses import dataclass
from pathlib import Path

from tools.stoneage_ordered_runtime_world_reachability_probe import (
    load_ordered_runtime_reachability,
)


PROGRESSION_REPORT_REF = (
    "research/recovered/STONEAGE-25-SHADOWED-BRANCH-PROGRESSION-R1.txt"
)
PROGRESSION_RESOLUTION = "RESOLUTION|SHADOWED_BRANCH_PROGRESSION_WITNESS_CLOSED"
OUTPUT_RESOLUTION = "RESOLUTION|STATE_GATED_RUNTIME_WORLD_REACHABILITY_CLOSED"


def _fields(line: str, prefix: str) -> dict[str, str]:
    parts=line.split("|")
    if not parts or parts[0] != prefix:
        raise ValueError(f"expected {prefix} row")
    out={}
    for part in parts[1:]:
        if "=" not in part:
            raise ValueError(f"malformed {prefix} field: {part}")
        key,value=part.split("=",1)
        if not key or key in out:
            raise ValueError(f"duplicate/blank {prefix} field")
        out[key]=value
    return out


@dataclass(frozen=True)
class GatedTransportWitness:
    source_floor:int
    destination_floor:int


def parse_progression_witness(text:str)->GatedTransportWitness:
    counts={}
    progression=None
    resolution=False
    for raw in str(text).splitlines():
        line=raw.strip()
        if not line:
            continue
        if line.startswith("COUNT|"):
            parts=line.split("|")
            if len(parts)==3:
                counts[parts[1]]=int(parts[2])
        elif line.startswith("PROGRESSION_WITNESS|"):
            progression=_fields(line,"PROGRESSION_WITNESS")
        elif line==PROGRESSION_RESOLUTION:
            resolution=True
    if not resolution:
        raise ValueError("progression report lacks closed resolution")
    if counts.get("combined_progression_witness") != 1:
        raise ValueError("progression report lacks combined witness")
    if counts.get("branch_full_orphan_closure") != 1:
        raise ValueError("progression report lacks full branch closure")
    if progression is None:
        raise ValueError("progression report lacks witness row")
    if int(progression.get("combined_state_progression_witness","0")) != 1:
        raise ValueError("progression witness row is not closed")
    if int(progression.get("classic_path_after_acquisition","0")) != 1:
        raise ValueError("acquisition cannot reach gated transport source")
    return GatedTransportWitness(
        source_floor=int(progression["ingress_source_floor"]),
        destination_floor=int(progression["ingress_target_floor"]),
    )


@dataclass(frozen=True)
class StateGatedReachabilityAudit:
    materializable_floor_ids:frozenset[int]
    classic_reached_floor_ids:frozenset[int]
    state_gated_reached_floor_ids:frozenset[int]
    resolved_supplemental_floor_ids:frozenset[int]
    gated_witness:GatedTransportWitness

    @property
    def newly_reached_floor_ids(self)->tuple[int,...]:
        return tuple(sorted(
            self.state_gated_reached_floor_ids-self.classic_reached_floor_ids
        ))

    @property
    def remaining_unreachable_floor_ids(self)->tuple[int,...]:
        return tuple(sorted(
            self.materializable_floor_ids-self.state_gated_reached_floor_ids
        ))

    @property
    def counts(self)->dict[str,int]:
        return {
            "materializable_floor_ids":len(self.materializable_floor_ids),
            "classic_reachable_floor_ids":len(self.classic_reached_floor_ids),
            "state_gated_transport_edges":1,
            "state_gated_reachable_floor_ids":len(
                self.state_gated_reached_floor_ids
            ),
            "newly_reachable_floor_ids":len(self.newly_reached_floor_ids),
            "remaining_unreachable_floor_ids":len(
                self.remaining_unreachable_floor_ids
            ),
            "resolved_supplemental_floor_ids":len(
                self.resolved_supplemental_floor_ids
            ),
            "classic_reachable_resolved_supplemental_floors":len(
                self.classic_reached_floor_ids
                & self.resolved_supplemental_floor_ids
            ),
            "state_gated_reachable_resolved_supplemental_floors":len(
                self.state_gated_reached_floor_ids
                & self.resolved_supplemental_floor_ids
            ),
        }


def _bfs(
    *,
    seeds:set[int],
    adjacency:dict[int,set[int]],
)->frozenset[int]:
    reached=set(int(x) for x in seeds)
    queue=collections.deque(sorted(reached))
    while queue:
        floor=queue.popleft()
        for destination in sorted(adjacency.get(floor,())):
            if destination in reached:
                continue
            reached.add(destination)
            queue.append(destination)
    return frozenset(reached)


def compute_state_gated_reachability(
    *,
    progression_text:str,
)->StateGatedReachabilityAudit:
    witness=parse_progression_witness(progression_text)
    classic=load_ordered_runtime_reachability()
    runtime=classic.runtime
    extension=runtime.base.extension
    materializable=set(extension.materializable_floor_ids)
    stable=set(extension.stable_world.by_floor)
    resolved=set(extension.resolved_by_floor)

    if witness.source_floor not in classic.reached_floor_ids:
        raise ValueError("gated transport source is not classic-reachable")
    if witness.destination_floor not in materializable:
        raise ValueError("gated transport destination is not materializable")

    adjacency:dict[int,set[int]]=collections.defaultdict(set)
    for edge in runtime.topology.legacy_warps:
        source=int(edge.source.floor_id)
        destination=int(edge.destination.floor_id)
        if source not in materializable or destination not in materializable:
            raise ValueError("classic Warp escaped materializable floor set")
        adjacency[source].add(destination)
    adjacency[witness.source_floor].add(witness.destination_floor)

    reached=_bfs(seeds=stable,adjacency=adjacency)
    escaped=set(reached)-materializable
    if escaped:
        raise ValueError(f"state-gated BFS escaped materializable set: {sorted(escaped)}")

    return StateGatedReachabilityAudit(
        materializable_floor_ids=frozenset(materializable),
        classic_reached_floor_ids=frozenset(classic.reached_floor_ids),
        state_gated_reached_floor_ids=reached,
        resolved_supplemental_floor_ids=frozenset(resolved),
        gated_witness=witness,
    )


def emit(audit:StateGatedReachabilityAudit)->None:
    print("StoneAge state-gated recovered25 runtime world reachability — R1")
    print(
        "SCOPE|ordered active classic Warp graph + validated existential "
        "state-gated transport witnesses"
    )
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print(
        "RULE|classic-only reachability remains separately reported; gated "
        "transport is not promoted to an unconditional map edge"
    )
    print(
        "RULE|state-gated reachability means at least one legal player state "
        "can traverse the edge; it is not a fresh-character progression proof"
    )
    for key in sorted(audit.counts):
        print(f"COUNT|{key}|{audit.counts[key]}")
    print(
        "GATED_TRANSPORT|"
        f"source_floor={audit.gated_witness.source_floor}|"
        f"destination_floor={audit.gated_witness.destination_floor}|"
        "progression_witness=1"
    )
    print(
        "NEWLY_REACHABLE|floors="+(
            ",".join(map(str,audit.newly_reached_floor_ids))
            if audit.newly_reached_floor_ids else "NONE"
        )
    )
    print(
        "REMAINING_UNREACHABLE|floors="+(
            ",".join(map(str,audit.remaining_unreachable_floor_ids))
            if audit.remaining_unreachable_floor_ids else "NONE"
        )
    )
    print(OUTPUT_RESOLUTION)


def main()->None:
    parser=argparse.ArgumentParser()
    parser.add_argument(
        "--progression-report",
        type=Path,
        default=Path(PROGRESSION_REPORT_REF),
    )
    args=parser.parse_args()
    emit(compute_state_gated_reachability(
        progression_text=args.progression_report.read_text(encoding="utf-8")
    ))


if __name__=="__main__":
    main()
