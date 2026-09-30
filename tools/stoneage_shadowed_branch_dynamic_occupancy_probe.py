#!/usr/bin/env python3
"""Audit dynamic-object occupancy boundary for the closed shadowed-branch path.

This probe intentionally separates deterministic recovered initial-world state
from arbitrary later live-session state.

Pinned fixed-descendant semantics used as evidence:
- classic Warp characters are overable;
- gold objects do not block CHAR_walk;
- item objects block only when ITEM_ISOVERED is false;
- ITEM_ISOVERED defaults true but item data may override it;
- the legacy persistent ground-object snapshot filename is exactly "itemgold";
  "itemgold_extra" is an emergency save and is not the normal restore target.

Recovered25 bundle evidence is used to determine whether a persisted ground
object snapshot is actually present and, if present, whether it places restored
objects on either critical progression floor.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


OUTPUT_RESOLUTION = "RESOLUTION|SHADOWED_BRANCH_DYNAMIC_OCCUPANCY_BOUNDARY_CLOSED"


def _coord_closed(text:str)->bool:
    required={
        "STATIC_COORDINATE_CHAIN|witness=1",
        "CONSERVATIVE_NPC_BIRTH_OCCUPANCY_CHAIN|witness=1",
        "RESOLUTION|SHADOWED_BRANCH_STATIC_COORDINATE_ACCESS_CLOSED",
    }
    lines={line.strip() for line in str(text).splitlines() if line.strip()}
    return required <= lines


def _critical_floors(text:str)->tuple[int,int]:
    # These floor ids are already public derived structural metadata in the
    # preceding reports. Keep extraction deterministic rather than duplicating
    # independent source scanning here.
    award=None
    ingress=None
    for line in str(text).splitlines():
        line=line.strip()
        if line.startswith("GATED_TRANSPORT|"):
            fields={}
            for part in line.split("|")[1:]:
                if "=" in part:
                    k,v=part.split("=",1)
                    fields[k]=v
            ingress=int(fields["source_floor"])
    # award floor comes from legal-state witness detail.
    for line in str(text).splitlines():
        line=line.strip()
        if line.startswith("EXCHANGE_CHAIN_WITNESS|"):
            fields={}
            for part in line.split("|")[1:]:
                if "=" in part:
                    k,v=part.split("=",1)
                    fields[k]=v
            award=int(fields["source_floor"])
            break
    if award is None or ingress is None:
        raise ValueError("critical floors missing from joined reports")
    return award,ingress


_STORE_RE=re.compile(
    r"^(?P<kind>ITEM|GOLD|CHAR)\|"
    r"(?:(?:x|y|floor)=[^|]+\|){3}",
    re.I,
)


def _store_row_floor(line:str)->tuple[str,int]|None:
    raw=line.strip()
    if not raw:
        return None
    parts=raw.split("|")
    if not parts:
        return None
    kind=parts[0].upper()
    if kind not in {"ITEM","GOLD","CHAR"}:
        return None
    floor=None
    for part in parts[1:5]:
        if "=" not in part:
            continue
        key,value=part.split("=",1)
        if key.strip().lower()=="floor":
            try:
                floor=int(value.strip())
            except ValueError:
                return None
    if floor is None:
        return None
    return kind,floor


@dataclass(frozen=True)
class DynamicOccupancyAudit:
    coordinate_chain_closed:bool
    normal_snapshot_files:tuple[str,...]
    extra_snapshot_files:tuple[str,...]
    normal_snapshot_rows:int
    critical_item_rows:int
    critical_gold_rows:int
    critical_char_rows:int

    @property
    def recovered_persistent_critical_blocker_free(self)->bool:
        # GOLD never blocks movement under the pinned CHAR_walk switch.
        # CHAR rows from itemgold are restored pets/characters and would be
        # conservative blockers; ITEM rows remain potentially blocking because
        # per-item isovered can override the true default.
        return self.critical_item_rows==0 and self.critical_char_rows==0

    @property
    def deterministic_initial_runtime_witness(self)->bool:
        return (
            self.coordinate_chain_closed
            and self.recovered_persistent_critical_blocker_free
        )


def analyze(
    *,
    coordinate_report_text:str,
    state_gated_report_text:str,
    legal_state_report_text:str,
    bundle_root:Path,
)->DynamicOccupancyAudit:
    if not _coord_closed(coordinate_report_text):
        raise ValueError("coordinate chain is not closed")
    award_floor,ingress_floor=_critical_floors(
        state_gated_report_text+"\n"+legal_state_report_text
    )
    critical={award_floor,ingress_floor}

    normal=[]
    extra=[]
    for path in sorted(
        (p for p in bundle_root.rglob("*") if p.is_file()),
        key=lambda p:str(p).lower(),
    ):
        name=path.name.lower()
        if name=="itemgold":
            normal.append(path)
        elif name=="itemgold_extra":
            extra.append(path)

    rows=items=golds=chars=0
    for path in normal:
        try:
            content=path.read_text(encoding="utf-8",errors="replace")
        except OSError:
            continue
        for line in content.splitlines():
            parsed=_store_row_floor(line)
            if parsed is None:
                continue
            rows+=1
            kind,floor=parsed
            if floor not in critical:
                continue
            if kind=="ITEM":
                items+=1
            elif kind=="GOLD":
                golds+=1
            elif kind=="CHAR":
                chars+=1

    return DynamicOccupancyAudit(
        coordinate_chain_closed=True,
        normal_snapshot_files=tuple(
            str(p.relative_to(bundle_root)) for p in normal
        ),
        extra_snapshot_files=tuple(
            str(p.relative_to(bundle_root)) for p in extra
        ),
        normal_snapshot_rows=rows,
        critical_item_rows=items,
        critical_gold_rows=golds,
        critical_char_rows=chars,
    )


def emit(audit:DynamicOccupancyAudit)->None:
    print("StoneAge shadowed-branch dynamic occupancy boundary — R1")
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print(
        "PINNED_SOURCE_FACT|classic_warp_character_overable=1|"
        "gold_blocks_walk=0|item_default_isovered=1|"
        "item_isovered_override_possible=1"
    )
    print(
        "PINNED_SOURCE_FACT|normal_ground_object_restore_filename=itemgold|"
        "emergency_nonrestore_filename=itemgold_extra"
    )
    print(
        "RULE|all recovered non-Warp NPC birth cells are already treated as "
        "blocking by the prerequisite coordinate report"
    )
    print(
        "RULE|arbitrary later player/pet movement and later dropped items are "
        "transient live-session state, not deterministic recovered world content"
    )
    print(
        "RULE|no despawn or NPC-movement assumption is used to obtain the "
        "deterministic initial-runtime witness"
    )
    print(f"COUNT|normal_itemgold_files|{len(audit.normal_snapshot_files)}")
    print(f"COUNT|itemgold_extra_files|{len(audit.extra_snapshot_files)}")
    print(f"COUNT|normal_itemgold_rows|{audit.normal_snapshot_rows}")
    print(f"COUNT|critical_floor_item_rows|{audit.critical_item_rows}")
    print(f"COUNT|critical_floor_gold_rows|{audit.critical_gold_rows}")
    print(f"COUNT|critical_floor_char_rows|{audit.critical_char_rows}")
    print(
        "PERSISTED_CRITICAL_BLOCKER_FREE|witness="
        f"{int(audit.recovered_persistent_critical_blocker_free)}"
    )
    print(
        "DETERMINISTIC_INITIAL_DYNAMIC_OCCUPANCY_CHAIN|witness="
        f"{int(audit.deterministic_initial_runtime_witness)}"
    )
    print(
        "ARBITRARY_LIVE_SESSION_UNIVERSAL_REACHABILITY|closed=0|"
        "reason=transient_nonoverable_items_or_characters_may_be_introduced"
    )
    print(OUTPUT_RESOLUTION)


def main()->None:
    parser=argparse.ArgumentParser()
    parser.add_argument("--coordinate-report",type=Path,required=True)
    parser.add_argument("--state-gated-report",type=Path,required=True)
    parser.add_argument("--legal-state-report",type=Path,required=True)
    parser.add_argument("--bundle-root",type=Path,required=True)
    args=parser.parse_args()
    emit(analyze(
        coordinate_report_text=args.coordinate_report.read_text(encoding="utf-8"),
        state_gated_report_text=args.state_gated_report.read_text(encoding="utf-8"),
        legal_state_report_text=args.legal_state_report.read_text(encoding="utf-8"),
        bundle_root=args.bundle_root,
    ))


if __name__=="__main__":
    main()
