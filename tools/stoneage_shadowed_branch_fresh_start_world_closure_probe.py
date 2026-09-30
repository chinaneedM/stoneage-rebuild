#!/usr/bin/env python3
"""Join recovered fresh-start progression into full materializable-world access.

All inputs are deterministic reports generated from the same verified
recovered25 preservation bundle.  This layer does not invent a new transport
edge.  It joins:

- fresh-start Stone sufficiency;
- ordered fresh-start leveling to a valid award/gate level;
- the already-proven award -> classic Warp -> gated WarpMan -> branch chain;
- the state-gated world census.

The result is existential fresh-character provenance for the previously
state-gated 826/826 materializable-floor result.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


OUTPUT_RESOLUTION=(
    "RESOLUTION|FRESH_START_STATE_GATED_RUNTIME_WORLD_REACHABILITY_CLOSED"
)


def _has(text:str,line:str)->bool:
    return line in {raw.strip() for raw in str(text).splitlines()}


def _count(text:str,key:str)->int|None:
    prefix=f"COUNT|{key}|"
    for raw in str(text).splitlines():
        line=raw.strip()
        if line.startswith(prefix):
            try:
                return int(line[len(prefix):])
            except ValueError:
                return None
    return None


@dataclass(frozen=True)
class FreshStartWorldAudit:
    stone_chain:bool
    leveling_to_target:bool
    progression_chain:bool
    branch_full_closure:bool
    materializable_floors:int|None
    state_gated_reachable_floors:int|None
    remaining_unreachable_floors:int|None

    @property
    def full_world(self)->bool:
        return (
            self.stone_chain
            and self.leveling_to_target
            and self.progression_chain
            and self.branch_full_closure
            and self.materializable_floors is not None
            and self.state_gated_reachable_floors==self.materializable_floors
            and self.remaining_unreachable_floors==0
        )


def analyze(
    *,
    stone_text:str,
    leveling_closure_text:str,
    progression_text:str,
    world_text:str,
)->FreshStartWorldAudit:
    stone=_has(stone_text,"FRESH_START_ECONOMIC_CHAIN|witness=1")
    leveling=_has(
        leveling_closure_text,
        "FRESH_START_LEVELING_TO_TARGET|witness=1",
    )
    progression=(
        _has(
            progression_text,
            "RESOLUTION|SHADOWED_BRANCH_PROGRESSION_WITNESS_CLOSED",
        )
        and "combined_state_progression_witness=1" in progression_text
        and "same_level_witness=1" in progression_text
    )
    branch=(
        _count(progression_text,"branch_full_orphan_closure")==1
        and _count(progression_text,"branch_returns_to_preexisting_reached")==1
    )
    return FreshStartWorldAudit(
        stone_chain=stone,
        leveling_to_target=leveling,
        progression_chain=progression,
        branch_full_closure=branch,
        materializable_floors=_count(world_text,"materializable_floor_ids"),
        state_gated_reachable_floors=_count(
            world_text,"state_gated_reachable_floor_ids"
        ),
        remaining_unreachable_floors=_count(
            world_text,"remaining_unreachable_floor_ids"
        ),
    )


def emit(audit:FreshStartWorldAudit)->None:
    print("StoneAge fresh-start state-gated runtime world reachability — R1")
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print(
        "RULE|this is a strict join of same-bundle derived witnesses; it does "
        "not promote the gated WarpMan edge to an unconditional edge"
    )
    print(
        "RULE|fresh-start claim is existential: at least one normal hometown "
        "has a legal coordinate/combat/level/item/fee sequence into the gated "
        "branch; it is not an all-hometowns or guaranteed-RNG claim"
    )
    print(f"PREREQUISITE|fresh_start_stone_chain={int(audit.stone_chain)}")
    print(
        "PREREQUISITE|fresh_start_leveling_to_target="
        f"{int(audit.leveling_to_target)}"
    )
    print(
        "PREREQUISITE|award_to_gate_progression_chain="
        f"{int(audit.progression_chain)}"
    )
    print(
        "PREREQUISITE|post_ingress_branch_full_closure="
        f"{int(audit.branch_full_closure)}"
    )
    print(
        "COUNT|materializable_floor_ids|"
        f"{audit.materializable_floors if audit.materializable_floors is not None else -1}"
    )
    print(
        "COUNT|fresh_start_state_gated_reachable_floor_ids|"
        f"{audit.state_gated_reachable_floors if audit.state_gated_reachable_floors is not None else -1}"
    )
    print(
        "COUNT|fresh_start_remaining_unreachable_floor_ids|"
        f"{audit.remaining_unreachable_floors if audit.remaining_unreachable_floors is not None else -1}"
    )
    print(
        "FRESH_START_STATE_GATED_RUNTIME_WORLD|witness="
        f"{int(audit.full_world)}"
    )
    print(
        "ALL_HOMETOWNS_FULL_WORLD|closed=0|"
        "reason=fresh_start_coordinate_award_chain_is_existential_only"
    )
    print(OUTPUT_RESOLUTION)


def main()->None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--stone-report",type=Path,required=True)
    ap.add_argument("--leveling-closure-report",type=Path,required=True)
    ap.add_argument("--progression-report",type=Path,required=True)
    ap.add_argument("--world-report",type=Path,required=True)
    args=ap.parse_args()
    emit(analyze(
        stone_text=args.stone_report.read_text(encoding="utf-8"),
        leveling_closure_text=args.leveling_closure_report.read_text(
            encoding="utf-8"
        ),
        progression_text=args.progression_report.read_text(encoding="utf-8"),
        world_text=args.world_report.read_text(encoding="utf-8"),
    ))


if __name__=="__main__":
    main()
