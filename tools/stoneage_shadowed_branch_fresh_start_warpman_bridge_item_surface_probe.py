#!/usr/bin/env python3
"""Discover recovered acquisition/reference surfaces for selected fresh-start WarpMan ITEM gates."""
from __future__ import annotations
import argparse,collections
from dataclasses import dataclass
from pathlib import Path
from tools.stoneage_ordered_runtime_world_reachability_probe import load_ordered_runtime_reachability
from tools.stoneage_shadowed_branch_fresh_start_dialogue_warp_bridge_probe import WARPMAN,DialogueWarp,analyze as analyze_bridges
from tools.stoneage_shadowed_branch_item_npc_reference_probe import _argument_fields,_contains_integer_token,_safe_ascii
from tools.stoneage_shadowed_branch_key_item_nonshop_probe import _drop_witnesses,_npc_reward_witnesses
from tools.stoneage_shadowed_branch_warpman_satisfiability_probe import ITEM,_assigned_data,_configured_itemset_paths,_field,_item_ids,parse_free_predicates
from tools.stoneage_transport_usage_probe import iter_blocks,magic_kind,template_map

OUTPUT_RESOLUTION="RESOLUTION|SHADOWED_BRANCH_FRESH_START_WARPMAN_BRIDGE_ITEM_SURFACES_AUDITED"

@dataclass(frozen=True)
class Requirement:
    ordinal:int; edge_index:int; operator:str; item_id:int

def _requirements(ordinal:int,edges:tuple[DialogueWarp,...])->tuple[Requirement,...]:
    out=[]
    for edge_index,edge in enumerate(edges,1):
        if edge.kind!=WARPMAN or edge.argument_data is None: raise ValueError("invalid selected WarpMan edge")
        free=_field(edge.argument_data,b"FREE")
        clauses=parse_free_predicates(free or b"")
        if len(clauses)!=1 or len(clauses[0])!=1: raise ValueError("bridge gate not one predicate")
        atom=clauses[0][0]
        if atom is None or atom.key!=ITEM: raise ValueError("bridge gate not ITEM")
        out.append(Requirement(int(ordinal),int(edge_index),atom.operator,int(atom.operand)))
    return tuple(out)

def _references(npc_dir:Path,target:int,reached:set[int])->tuple[tuple[tuple[str,str],...],int]:
    files=sorted((p for p in npc_dir.rglob("*") if p.is_file()),key=lambda p:str(p).lower())
    templates=template_map([p for p in files if magic_kind(p)=="template"])
    functions={n:d[0] for n,d in templates.items() if len(d)==1}
    classes=set(); missing=0
    for create in (p for p in files if magic_kind(p)=="create"):
        for entries in iter_blocks(create):
            fields={}; enemies=[]
            for k,v in entries:
                if k==b"enemy": enemies.append(v)
                else: fields[k]=v
            try: floor=int(fields.get(b"floorid",b"0"))
            except ValueError: continue
            if floor not in reached or (b"borncenter" not in fields and b"borncorner" not in fields): continue
            for enemy in enemies:
                name,sep,arg=enemy.partition(b"|")
                function=functions.get(name.strip())
                if function is None: continue
                data=_assigned_data(npc_dir,arg if sep else b"")
                if data is None: missing+=1; continue
                for key,value in _argument_fields(data):
                    if _contains_integer_token(value,target):
                        classes.add((_safe_ascii(function),_safe_ascii(key)))
    return tuple(sorted(classes)),missing

def analyze(*,npc_dir:Path,setup:Path,data_dir:Path,server_map_root:Path,mapset_path:Path):
    spatial=analyze_bridges(npc_dir=npc_dir,setup=setup,server_map_root=server_map_root,mapset_path=mapset_path)
    failed=[r for r in spatial.rows if not r.baseline_classic.reachable]
    bridged=[r for r in failed if r.baseline_warpman.reachable]
    reqs=[]
    for row in bridged: reqs.extend(_requirements(row.ordinal,row.baseline_warpman.edge_sequence))
    reached=set(load_ordered_runtime_world_reachability().reached_floor_ids)
    catalog=_item_ids(_configured_itemset_paths(setup,data_dir))
    rows=[]; missing=0
    for req in reqs:
        drops=_drop_witnesses(data_dir=data_dir,setup=setup,target_item=req.item_id,reached_floors=reached)
        rewards,_hits,rm=_npc_reward_witnesses(npc_dir=npc_dir,target_item=req.item_id,reached_floors=reached)
        refs,xm=_references(npc_dir,req.item_id,reached)
        strong=[d for d in drops if d.group_gate_class in {"UNGATED","TARGET_ABSENCE_ALLOWED","EXCLUDES_OTHER_ITEM"}]
        covered=[r for r in rewards if r.action_run_covered]
        rows.append((req,req.item_id in catalog,len(strong),len({d.floor_id for d in strong}),len(covered),len({r.floor_id for r in covered}),refs))
        missing+=rm+xm
    return failed,bridged,reqs,rows,missing

def emit(result)->None:
    failed,bridged,reqs,rows,missing=result
    print("StoneAge fresh-start WarpMan bridge ITEM surface audit — R1")
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print("RULE|required item IDs, raw operands, NPC identities, filenames, dialogue and coordinates are withheld")
    print("RULE|reachable-floor sources are discovery evidence only; fresh-start coordinate ordering remains unproven")
    counts=collections.Counter()
    counts["failed_classic_hometowns"]=len(failed); counts["warpman_bridged_hometowns"]=len(bridged)
    counts["requirements"]=len(reqs); counts["unique_required_items"]=len({r.item_id for r in reqs}); counts["missing_argument_files"]=missing
    for req,catalog,strong,strongfloors,covered,coveredfloors,refs in rows:
        counts[f"operator:{req.operator}:requirements"]+=1
        counts["catalog_witness_requirements"]+=int(catalog)
        counts["strong_drop_requirements"]+=int(strong>0)
        counts["covered_additem_requirements"]+=int(covered>0)
        for f,k in refs: counts[f"reference:{f}:{k}:requirements"]+=1
    for k in sorted(counts): print(f"COUNT|{k}|{counts[k]}")
    for req,catalog,strong,strongfloors,covered,coveredfloors,refs in rows:
        print(f"FRESH_START_BRIDGE_ITEM|ordinal={req.ordinal}|edge={req.edge_index}|operator={req.operator}|catalog={int(catalog)}|strong_drop_rows={strong}|strong_drop_floors={strongfloors}|covered_additem_rows={covered}|covered_additem_floors={coveredfloors}|reference_classes={len(refs)}|item_id_withheld=1")
        for f,k in refs: print(f"FRESH_START_BRIDGE_ITEM_REFERENCE|ordinal={req.ordinal}|function={f}|field={k}")
    print(OUTPUT_RESOLUTION)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--npc-dir",type=Path,required=True); p.add_argument("--setup",type=Path,required=True); p.add_argument("--data-dir",type=Path,required=True)
    p.add_argument("--server-map-root",type=Path,required=True); p.add_argument("--mapset",type=Path,required=True)
    a=p.parse_args(); emit(analyze(npc_dir=a.npc_dir,setup=a.setup,data_dir=a.data_dir,server_map_root=a.server_map_root,mapset_path=a.mapset))
if __name__=="__main__": main()
