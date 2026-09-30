#!/usr/bin/env python3
"""Audit fresh-character Stone sufficiency for the shadowed-branch key item.

The earlier progression proof only showed that an award fee fits within the
legal carried-Stone cap. This probe asks the narrower fresh-start question:
does recovered25 initialize a new character with enough Stone to pay at least
one otherwise-valid ExChangeMan award record, without requiring any inferred
earning source?

If yes, the economic seam closes by conservation: a player may retain starting
Stone while leveling to the already-proven award domain. This does not assert
that every possible route is free of optional spending.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from tools.stoneage_ordered_runtime_world_reachability_probe import (
    load_ordered_runtime_reachability,
)
from tools.stoneage_shadowed_branch_item_shop_acquisition_probe import (
    _locate_key_item,
)
from tools.stoneage_shadowed_branch_key_item_exchange_probe import (
    _delstone_cost,
    _event_records,
    _item_terms,
    _level_witnesses,
    _values,
)
from tools.stoneage_shadowed_branch_progression_witness_probe import (
    _template_names,
)
from tools.stoneage_shadowed_branch_warpman_satisfiability_probe import (
    _assigned_data,
    _configured_maxlevel,
)
from tools.stoneage_transport_usage_probe import iter_blocks, magic_kind


OUTPUT_RESOLUTION = "RESOLUTION|SHADOWED_BRANCH_FRESH_START_STONE_AUDITED"


def _setup_unique_int(setup:Path,key:str)->int:
    wanted=key.strip().upper()
    values=[]
    for raw in setup.read_text(encoding="utf-8",errors="replace").splitlines():
        line=raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        left,right=line.split("=",1)
        if left.strip().upper()!=wanted:
            continue
        token=right.split("#",1)[0].strip()
        try:
            values.append(int(token,10))
        except ValueError as exc:
            raise ValueError(f"non-integer setup {wanted}") from exc
    if len(values)!=1:
        raise ValueError(f"expected exactly one setup {wanted}, found {len(values)}")
    return values[0]


@dataclass(frozen=True)
class FreshStartStoneAudit:
    initial_stone:int
    matching_award_records:int
    valid_fee_records:int
    minimum_fee:int|None
    initial_stone_sufficient_records:int

    @property
    def fresh_start_stone_witness(self)->bool:
        return (
            self.matching_award_records>0
            and self.valid_fee_records>0
            and self.minimum_fee is not None
            and self.initial_stone_sufficient_records>0
        )


def analyze(*,npc_dir:Path,setup:Path)->FreshStartStoneAudit:
    initial_stone=_setup_unique_int(setup,"GOLD")
    if initial_stone < 0:
        raise ValueError("negative new-player GOLD is unsupported")

    target,_missing=_locate_key_item(npc_dir)
    maxlevel=_configured_maxlevel(setup)
    reached=set(load_ordered_runtime_reachability().reached_floor_ids)
    exchange_names=_template_names(npc_dir,b"ExChangeMan")

    files=sorted(
        (p for p in npc_dir.rglob("*") if p.is_file()),
        key=lambda p:str(p).lower(),
    )

    matching=0
    valid_fees=[]
    sufficient=0

    for create in (p for p in files if magic_kind(p)=="create"):
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
                    rewards={
                        item
                        for value in _values(record,b"GetItem")
                        for item,_qty in _item_terms(value)
                    }
                    if target not in rewards:
                        continue
                    matching+=1

                    levels=_level_witnesses(record,maxlevel)
                    if not levels:
                        continue
                    delstone=_values(record,b"DelStone")
                    if not delstone:
                        fees=(0,)
                    else:
                        fees=tuple(
                            cost
                            for level in levels
                            for cost in (_delstone_cost(delstone[0],level),)
                            if cost is not None and cost>=0
                        )
                    if not fees:
                        continue
                    fee=min(fees)
                    valid_fees.append(fee)
                    if initial_stone >= fee:
                        sufficient+=1

    return FreshStartStoneAudit(
        initial_stone=initial_stone,
        matching_award_records=matching,
        valid_fee_records=len(valid_fees),
        minimum_fee=min(valid_fees) if valid_fees else None,
        initial_stone_sufficient_records=sufficient,
    )


def emit(audit:FreshStartStoneAudit)->None:
    print("StoneAge shadowed-branch fresh-start Stone audit — R1")
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print(
        "RULE|exact Stone amounts, item IDs, level thresholds, NPC names and "
        "raw arguments are withheld"
    )
    print(
        "RULE|new-character Stone is read from recovered setup.cf GOLD, matching "
        "the fixed-descendant new-player initialization path"
    )
    print(
        "RULE|fee sufficiency is tested only over already-valid award level "
        "states; optional player spending is not treated as mandatory"
    )
    print(f"COUNT|matching_award_records|{audit.matching_award_records}")
    print(f"COUNT|valid_fee_records|{audit.valid_fee_records}")
    print(
        "COUNT|initial_stone_sufficient_records|"
        f"{audit.initial_stone_sufficient_records}"
    )
    print(
        "FRESH_START_STONE|"
        f"positive={int(audit.initial_stone>0)}|"
        f"covers_minimum_valid_fee={int(audit.minimum_fee is not None and audit.initial_stone>=audit.minimum_fee)}|"
        "amounts_withheld=1"
    )
    print(
        "FRESH_START_ECONOMIC_CHAIN|witness="
        f"{int(audit.fresh_start_stone_witness)}"
    )
    print(OUTPUT_RESOLUTION)


def main()->None:
    parser=argparse.ArgumentParser()
    parser.add_argument("--npc-dir",type=Path,required=True)
    parser.add_argument("--setup",type=Path,required=True)
    args=parser.parse_args()
    emit(analyze(npc_dir=args.npc_dir,setup=args.setup))


if __name__=="__main__":
    main()
