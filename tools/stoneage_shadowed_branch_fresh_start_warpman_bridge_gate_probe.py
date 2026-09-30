#!/usr/bin/env python3
"""Classify the gate shape on WarpMan edges that bridge failed fresh starts.

The coordinate bridge audit proves that two normal hometown starts can reach
the award component if recovered WarpMan transitions are admitted.  This probe
does not yet declare those transitions legally usable.  It binds the exact
WarpMan edge selected by the spatial search back to its recovered argument
payload and emits only derived gate categories needed for the next closure.

Raw dialogue, operands, coordinates, filenames, NPC identities and destination
details are intentionally withheld.
"""

from __future__ import annotations

import argparse
import collections
from dataclasses import dataclass
from pathlib import Path

from tools.stoneage_shadowed_branch_fresh_start_dialogue_warp_bridge_probe import (
    WARPMAN,
    DialogueWarp,
    analyze as analyze_dialogue_bridges,
)
from tools.stoneage_shadowed_branch_warpman_gate_probe import (
    _field,
    _free_structure,
    _money_class,
    _ordinary_route_class,
)


OUTPUT_RESOLUTION=(
    "RESOLUTION|SHADOWED_BRANCH_FRESH_START_WARPMAN_BRIDGE_GATE_SHAPE_AUDITED"
)


@dataclass(frozen=True)
class BridgeGateRow:
    ordinal:int
    path_edge_index:int
    ordinary_route_class:str
    is_newwarpman:bool
    warp_msg_required:bool
    checkparty_present:bool
    checkparty_explicit_false:bool
    free_present:bool
    free_allfree:bool
    paymsg_present:bool
    normalmsg_present:bool
    money_class:str
    newtime_present:bool
    free_or_groups:int
    free_condition_atoms:int
    free_condition_kinds:tuple[str,...]


@dataclass(frozen=True)
class BridgeGateAudit:
    rows:tuple[BridgeGateRow,...]
    failed_classic_hometowns:int
    warpman_bridged_hometowns:int
    missing_argument_payloads:int

    @property
    def counts(self)->dict[str,int]:
        out=collections.Counter()
        out["failed_classic_hometowns"]=self.failed_classic_hometowns
        out["warpman_bridged_hometowns"]=self.warpman_bridged_hometowns
        out["selected_warpman_edges"]=len(self.rows)
        out["missing_argument_payloads"]=self.missing_argument_payloads
        for row in self.rows:
            out[f"ordinary_route:{row.ordinary_route_class}"]+=1
            out[f"money_class:{row.money_class}"]+=1
            out[f"warp_msg_required:{int(row.warp_msg_required)}"]+=1
            out[f"checkparty_present:{int(row.checkparty_present)}"]+=1
            out[f"newtime_present:{int(row.newtime_present)}"]+=1
            for kind in row.free_condition_kinds:
                out[f"free_kind:{kind}:edges"]+=1
        return dict(out)


def _classify_edge(
    ordinal:int,
    path_edge_index:int,
    edge:DialogueWarp,
)->BridgeGateRow|None:
    if edge.kind!=WARPMAN:
        raise ValueError("gate-shape audit accepts WarpMan bridge edges only")
    data=edge.argument_data
    if data is None:
        return None
    checkparty=_field(data,b"CHECKPARTY")
    free=_field(data,b"FREE")
    groups,atoms,kinds=_free_structure(data)
    upper=data.upper()
    return BridgeGateRow(
        ordinal=int(ordinal),
        path_edge_index=int(path_edge_index),
        ordinary_route_class=_ordinary_route_class(data),
        is_newwarpman=(b"NEWWARPMAN" in upper),
        warp_msg_required=(_field(data,b"warp_msg") is not None),
        checkparty_present=(checkparty is not None),
        checkparty_explicit_false=(
            checkparty is not None and b"FALSE" in checkparty.upper()
        ),
        free_present=(free is not None),
        free_allfree=(free is not None and b"ALLFREE" in free.upper()),
        paymsg_present=(_field(data,b"PayMsg") is not None),
        normalmsg_present=(
            _field(data,b"NomalMsg") is not None
            or _field(data,b"nomal_msg") is not None
        ),
        money_class=_money_class(data),
        newtime_present=(_field(data,b"NEWTIME") is not None),
        free_or_groups=groups,
        free_condition_atoms=atoms,
        free_condition_kinds=kinds,
    )


def analyze(
    *,
    npc_dir:Path,
    setup:Path,
    server_map_root:Path,
    mapset_path:Path,
)->BridgeGateAudit:
    spatial=analyze_dialogue_bridges(
        npc_dir=npc_dir,
        setup=setup,
        server_map_root=server_map_root,
        mapset_path=mapset_path,
    )
    failed=[row for row in spatial.rows if not row.baseline_classic.reachable]
    bridged=[row for row in failed if row.baseline_warpman.reachable]

    rows=[]
    missing=0
    for pair in bridged:
        edges=pair.baseline_warpman.edge_sequence
        if not edges:
            raise ValueError("WarpMan-bridged path has no selected dialogue edge")
        for index,edge in enumerate(edges,1):
            if edge.kind!=WARPMAN:
                raise ValueError("WarpMan-only bridge search selected another kind")
            classified=_classify_edge(pair.ordinal,index,edge)
            if classified is None:
                missing+=1
            else:
                rows.append(classified)

    return BridgeGateAudit(
        rows=tuple(rows),
        failed_classic_hometowns=len(failed),
        warpman_bridged_hometowns=len(bridged),
        missing_argument_payloads=missing,
    )


def emit(audit:BridgeGateAudit)->None:
    print("StoneAge fresh-start WarpMan bridge gate-shape audit — R1")
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print(
        "RULE|only WarpMan edges selected by the coordinate bridge search are "
        "classified; raw operands, dialogue, coordinates, filenames and NPC "
        "identities are withheld"
    )
    print(
        "RULE|gate shape is not a legal fresh-start proof; FREE predicates, "
        "fee sufficiency, dialogue/facing/action semantics and any party/time "
        "requirements remain separate until explicitly joined"
    )
    for key in sorted(audit.counts):
        print(f"COUNT|{key}|{audit.counts[key]}")
    for row in audit.rows:
        print(
            "FRESH_START_WARPMAN_BRIDGE_GATE|"
            f"ordinal={row.ordinal}|"
            f"path_edge_index={row.path_edge_index}|"
            f"ordinary_route={row.ordinary_route_class}|"
            f"newwarpman={int(row.is_newwarpman)}|"
            f"warp_msg_required={int(row.warp_msg_required)}|"
            f"checkparty_present={int(row.checkparty_present)}|"
            f"checkparty_explicit_false={int(row.checkparty_explicit_false)}|"
            f"free_present={int(row.free_present)}|"
            f"free_allfree={int(row.free_allfree)}|"
            f"paymsg_present={int(row.paymsg_present)}|"
            f"normalmsg_present={int(row.normalmsg_present)}|"
            f"money_class={row.money_class}|"
            f"newtime_present={int(row.newtime_present)}|"
            f"free_or_groups={row.free_or_groups}|"
            f"free_condition_atoms={row.free_condition_atoms}|"
            f"free_condition_kinds="
            f"{','.join(row.free_condition_kinds) if row.free_condition_kinds else 'NONE'}"
        )
    print(OUTPUT_RESOLUTION)


def main()->None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--npc-dir",type=Path,required=True)
    ap.add_argument("--setup",type=Path,required=True)
    ap.add_argument("--server-map-root",type=Path,required=True)
    ap.add_argument("--mapset",type=Path,required=True)
    args=ap.parse_args()
    emit(analyze(
        npc_dir=args.npc_dir,
        setup=args.setup,
        server_map_root=args.server_map_root,
        mapset_path=args.mapset,
    ))


if __name__=="__main__":
    main()
