#!/usr/bin/env python3
"""Classify the recovered ExChangeMan records that award the shadowed key item.

The target item ID and every other numeric operand are transient.  Output keeps
only boolean structure, technical field names and aggregate prerequisite
classes so proprietary content payloads are not published.
"""

from __future__ import annotations

import argparse
import collections
import re
from dataclasses import dataclass
from pathlib import Path

from tools.stoneage_ordered_runtime_world_reachability_probe import (
    load_ordered_runtime_reachability,
)
from tools.stoneage_shadowed_branch_item_shop_acquisition_probe import (
    _locate_key_item,
)
from tools.stoneage_shadowed_branch_warpman_satisfiability_probe import (
    _assigned_data,
    _int_prefix,
)
from tools.stoneage_transport_usage_probe import (
    iter_blocks,
    magic_kind,
    template_map,
)


OUTPUT_RESOLUTION = "RESOLUTION|SHADOWED_BRANCH_KEY_ITEM_EXCHANGE_AWARD_AUDITED"


def _safe_key(value: bytes) -> str:
    text=value.decode("ascii","replace").strip().upper()
    text=re.sub(r"[^A-Z0-9_.-]+","_",text)
    return text[:64] or "EMPTY"


def _fields(record: bytes) -> tuple[tuple[bytes,bytes],...]:
    out=[]
    normalized=record.replace(b"\r",b"\n")
    for line in normalized.split(b"\n"):
        for token in line.split(b"|"):
            token=token.strip()
            if b":" not in token:
                continue
            key,value=token.split(b":",1)
            key=key.strip()
            if key:
                out.append((key,value.strip()))
    return tuple(out)


def _values(record: bytes,key: bytes) -> tuple[bytes,...]:
    wanted=key.lower()
    return tuple(value for name,value in _fields(record) if name.lower()==wanted)


def _item_terms(value: bytes) -> tuple[tuple[int,int],...]:
    out=[]
    for raw in value.split(b","):
        token=raw.strip()
        if not token:
            continue
        if b"*" in token:
            left,right=token.split(b"*",1)
            item=_int_prefix(left);qty=_int_prefix(right)
        else:
            item=_int_prefix(token);qty=1
        if item is not None:
            out.append((int(item),max(1,int(qty or 1))))
    return tuple(out)


def _event_atom(raw: bytes) -> tuple[str,str,int|None]:
    token=raw.strip()
    if not token:
        return ("EMPTY","?",None)
    if b"PET" in token.upper():
        return ("PET","SPECIAL",None)
    for op in (b"!=",b"<",b">",b"="):
        if op in token:
            left,right=token.split(op,1)
            key=_safe_key(left)
            # ITEM=123*2 uses the first numeric operand as item identity.
            operand=_int_prefix(right.split(b"*",1)[0])
            return (key,op.decode("ascii"),None if operand is None else int(operand))
    return (_safe_key(token),"?",None)


@dataclass(frozen=True)
class ExchangeAward:
    floor_id:int
    type_class:str
    field_keys:tuple[str,...]
    event_keys:tuple[str,...]
    event_operators:tuple[str,...]
    event_or_clauses:int
    event_atoms:int
    target_required_by_event:bool
    target_deleted:bool
    other_item_prerequisite_refs:int
    other_item_reward_refs:int
    delstone_present:bool
    delpet_present:bool
    eventno_present:bool


@dataclass(frozen=True)
class ExchangeAudit:
    awards:tuple[ExchangeAward,...]
    matching_create_rows:int
    missing_argument_files:int

    @property
    def counts(self)->dict[str,int]:
        out=collections.Counter({
            "matching_create_rows":self.matching_create_rows,
            "matching_award_records":len(self.awards),
            "source_floors":len({x.floor_id for x in self.awards}),
            "missing_argument_files":self.missing_argument_files,
            "target_required_by_event_records":sum(x.target_required_by_event for x in self.awards),
            "target_deleted_records":sum(x.target_deleted for x in self.awards),
            "records_with_other_item_prerequisites":sum(x.other_item_prerequisite_refs>0 for x in self.awards),
            "records_with_delstone":sum(x.delstone_present for x in self.awards),
            "records_with_delpet":sum(x.delpet_present for x in self.awards),
        })
        for row in self.awards:
            out[f"type:{row.type_class}:records"]+=1
            for key in row.event_keys:
                out[f"event_key:{key}:records"]+=1
        return dict(out)


def _event_records(data:bytes)->tuple[bytes,...]:
    # npc_exchangeman.c iterates getStringFromIndexWithDelim(argstr,"EventEnd",...)
    # so content between EventEnd delimiters is one candidate record.
    parts=data.split(b"EventEnd")
    return tuple(part.strip() for part in parts if part.strip())


def _record_award(record:bytes,target:int,floor:int)->ExchangeAward|None:
    getitems=_values(record,b"GetItem")
    if not getitems:
        return None
    reward_terms=tuple(term for value in getitems for term in _item_terms(value))
    if target not in {item for item,_qty in reward_terms}:
        return None

    event_values=_values(record,b"EVENT")
    event_or=0;event_atoms=0;event_keys=[];event_ops=[]
    target_required=False
    other_prereq=set()
    for value in event_values:
        for clause in value.split(b","):
            atoms=[atom for atom in clause.split(b"&") if atom.strip()]
            if not atoms:
                continue
            event_or+=1
            event_atoms+=len(atoms)
            for atom_raw in atoms:
                key,op,operand=_event_atom(atom_raw)
                event_keys.append(key);event_ops.append(op)
                if key=="ITEM" and operand is not None:
                    if operand==target:
                        target_required=True
                    else:
                        other_prereq.add(operand)

    target_deleted=False
    for value in _values(record,b"DelItem"):
        for item,_qty in _item_terms(value):
            if item==target:
                target_deleted=True
            else:
                other_prereq.add(item)

    other_rewards={
        item for item,_qty in reward_terms if item!=target
    }
    type_values=_values(record,b"TYPE")
    type_class=_safe_key(type_values[0]) if type_values else "UNSPECIFIED"
    keys=tuple(sorted({_safe_key(key) for key,_v in _fields(record)}))
    return ExchangeAward(
        floor_id=floor,
        type_class=type_class,
        field_keys=keys,
        event_keys=tuple(sorted(set(event_keys))),
        event_operators=tuple(sorted(set(event_ops))),
        event_or_clauses=event_or,
        event_atoms=event_atoms,
        target_required_by_event=target_required,
        target_deleted=target_deleted,
        other_item_prerequisite_refs=len(other_prereq),
        other_item_reward_refs=len(other_rewards),
        delstone_present=bool(_values(record,b"DelStone")),
        delpet_present=bool(_values(record,b"DelPet")),
        eventno_present=bool(_values(record,b"EventNo")),
    )


def analyze(npc_dir:Path)->ExchangeAudit:
    target,missing=_locate_key_item(npc_dir)
    reached=set(load_ordered_runtime_reachability().reached_floor_ids)
    files=sorted((p for p in npc_dir.rglob("*") if p.is_file()),key=lambda p:str(p).lower())
    templates=template_map([p for p in files if magic_kind(p)=="template"])
    exchange_names={
        name for name,defs in templates.items()
        if len(defs)==1 and defs[0].strip().lower()==b"exchangeman"
    }

    awards=[];matching_create_rows=0
    for create in (p for p in files if magic_kind(p)=="create"):
        for entries in iter_blocks(create):
            fields={};enemies=[]
            for key,value in entries:
                if key==b"enemy":enemies.append(value)
                else:fields[key]=value
            try:floor=int(fields.get(b"floorid",b"0"))
            except ValueError:continue
            if floor not in reached:continue
            if b"borncenter" not in fields and b"borncorner" not in fields:continue
            for enemy in enemies:
                name,sep,arg=enemy.partition(b"|")
                if name.strip() not in exchange_names:continue
                data=_assigned_data(npc_dir,arg if sep else b"")
                if data is None:
                    missing+=1;continue
                local=[]
                for record in _event_records(data):
                    row=_record_award(record,target,floor)
                    if row is not None:
                        local.append(row)
                if local:
                    matching_create_rows+=1
                    awards.extend(local)

    return ExchangeAudit(
        awards=tuple(awards),
        matching_create_rows=matching_create_rows,
        missing_argument_files=missing,
    )


def emit(audit:ExchangeAudit)->None:
    print("StoneAge shadowed-branch key-item ExChangeMan award audit — R1")
    print("SCOPE|reachable ExChangeMan EventEnd records awarding withheld key item")
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print("RULE|all item IDs, event numbers, gold values, pet IDs, dialogue, NPC names, coordinates and raw arguments are withheld")
    print("RULE|fixed descendant NPC_AcceptDel executes DelItem/DelStone/etc then GetItem -> NPC_EventAddItem")
    for key in sorted(audit.counts):
        print(f"COUNT|{key}|{audit.counts[key]}")
    for index,row in enumerate(audit.awards,1):
        print(
            "EXCHANGE_AWARD|"
            f"ordinal={index}|floor={row.floor_id}|type={row.type_class}|"
            f"event_or_clauses={row.event_or_clauses}|event_atoms={row.event_atoms}|"
            f"event_keys={','.join(row.event_keys) or 'NONE'}|"
            f"event_operators={','.join(row.event_operators) or 'NONE'}|"
            f"target_required_by_event={int(row.target_required_by_event)}|"
            f"target_deleted={int(row.target_deleted)}|"
            f"other_item_prerequisite_refs={row.other_item_prerequisite_refs}|"
            f"other_item_reward_refs={row.other_item_reward_refs}|"
            f"delstone_present={int(row.delstone_present)}|"
            f"delpet_present={int(row.delpet_present)}|"
            f"eventno_present={int(row.eventno_present)}|"
            f"field_keys={','.join(row.field_keys)}"
        )
    print(OUTPUT_RESOLUTION)


def main()->None:
    ap=argparse.ArgumentParser();ap.add_argument("--npc-dir",type=Path,required=True)
    args=ap.parse_args();emit(analyze(args.npc_dir))


if __name__=="__main__":main()
