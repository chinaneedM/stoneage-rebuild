#!/usr/bin/env python3
"""Audit whether recovered25 new-character level already satisfies the branch.

This is the level analogue of the fresh-start Stone audit.  It reads the
recovered setup.cf LV value used by the fixed-descendant _NEW_PLAYER_CF path,
then intersects that exact birth level with:

1. each reachable ExChangeMan award record's legal level domain; and
2. the unique shadowed-branch WarpMan gate's legal level domain.

If a matching award record contains the birth level in that joint domain, no
leveling/EXP provenance is needed for an existential fresh-start witness.
Raw level operands and the recovered birth level are deliberately withheld from
the derived report.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from tools.stoneage_ordered_runtime_world_reachability_probe import (
    load_ordered_runtime_reachability,
)
from tools.stoneage_shadowed_branch_fresh_start_stone_probe import (
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
from tools.stoneage_transport_usage_probe import (
    iter_blocks,
    magic_kind,
    template_map,
)


OUTPUT_RESOLUTION = "RESOLUTION|SHADOWED_BRANCH_FRESH_START_LEVEL_AUDITED"


@dataclass(frozen=True)
class FreshStartLevelAudit:
    birth_level:int
    matching_award_records:int
    joint_domain_records:int
    birth_level_joint_records:int
    gate_legal_levels:int

    @property
    def birth_level_positive(self)->bool:
        return self.birth_level > 0

    @property
    def direct_witness(self)->bool:
        return (
            self.birth_level_positive
            and self.matching_award_records > 0
            and self.joint_domain_records > 0
            and self.birth_level_joint_records > 0
            and self.gate_legal_levels > 0
        )


def analyze(*,npc_dir:Path,setup:Path)->FreshStartLevelAudit:
    birth_level=_setup_unique_int(setup,"LV")
    maxlevel=_configured_maxlevel(setup)
    if birth_level < 0:
        raise ValueError("negative new-player LV is unsupported")
    if birth_level > 160:
        # getNewplayerlv() caps configured LV at 160.
        birth_level=160

    gate,_missing_gate=_warp_gate_levels(npc_dir,maxlevel)
    gate_levels=set(int(x) for x in gate.joint_levels)

    target,_missing=_locate_key_item(npc_dir)
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

    matching=0
    joint_records=0
    birth_joint=0

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
                    award=_record_award(record,target,floor,maxlevel)
                    if award is None or award.type_class!="ACCEPT":
                        continue
                    matching+=1
                    award_levels=set(_level_witnesses(record,maxlevel))
                    joint=award_levels & gate_levels
                    if joint:
                        joint_records+=1
                    if birth_level in joint:
                        birth_joint+=1

    return FreshStartLevelAudit(
        birth_level=birth_level,
        matching_award_records=matching,
        joint_domain_records=joint_records,
        birth_level_joint_records=birth_joint,
        gate_legal_levels=len(gate_levels),
    )


def emit(audit:FreshStartLevelAudit)->None:
    print("StoneAge shadowed-branch fresh-start level audit — R1")
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print(
        "PINNED_SOURCE_CONTROL|new_player_cf_enabled=1|"
        "CHAR_LV_initialized_from=getNewplayerlv"
    )
    print(
        "RULE|recovered setup.cf LV is evaluated after fixed-descendant "
        "getNewplayerlv cap semantics; exact birth level and gate/award "
        "threshold operands are withheld"
    )
    print(
        "RULE|direct witness requires the same birth-level value to satisfy "
        "both a reachable key-item award level domain and the unique WarpMan "
        "gate level domain"
    )
    print(f"COUNT|matching_award_records|{audit.matching_award_records}")
    print(f"COUNT|joint_domain_records|{audit.joint_domain_records}")
    print(f"COUNT|birth_level_joint_records|{audit.birth_level_joint_records}")
    print(f"COUNT|gate_legal_level_values|{audit.gate_legal_levels}")
    print(
        "FRESH_START_LEVEL|"
        f"positive={int(audit.birth_level_positive)}|"
        f"direct_joint_domain_witness={int(audit.direct_witness)}|"
        "value_withheld=1"
    )
    print(
        "FRESH_START_DIRECT_LEVEL_CHAIN|witness="
        f"{int(audit.direct_witness)}"
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
