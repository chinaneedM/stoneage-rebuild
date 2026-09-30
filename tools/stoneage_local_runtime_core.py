#!/usr/bin/env python3
"""Engine-neutral local runtime core contracts for the StoneAge rebuild.

This module is DESIGN infrastructure.  It binds the version-tagged runtime
bootstrap contract to existing in-process historical domain/runtime models
without choosing a rendering engine or recreating legacy MMO services.

The important separation is:

- bootstrap contract: evidence/profile/invariant selection;
- content adapters: resolve versioned maps/NPCs/items/transition coordinates;
- local runtime core: authoritative deterministic state and mutations;
- presentation: engine-owned and replaceable.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping, Protocol, runtime_checkable

from tools.stoneage_singleplayer_domain import (
    MapPosition,
    PersistentPlayerState,
)
from tools.stoneage_singleplayer_persistence import (
    dump_persistent_state,
    load_persistent_state,
)


BOOTSTRAP_SCHEMA="stoneage.runtime-bootstrap.r1"
LOCAL_SESSION_SCHEMA="stoneage.local-runtime-session.r1"


def _nonempty(value:Any,label:str)->str:
    text=str(value).strip()
    if not text:
        raise ValueError(f"{label} must be non-empty")
    return text


@dataclass(frozen=True)
class FreshStartRouteContract:
    ordinal:int
    route_class:str
    requires_shop:bool
    requires_warpman:bool
    milestones:tuple[str,...]
    ordered:bool

    def __post_init__(self)->None:
        ordinal=int(self.ordinal)
        if ordinal<=0:
            raise ValueError("fresh-start ordinal must be positive")
        object.__setattr__(self,"ordinal",ordinal)
        object.__setattr__(self,"route_class",_nonempty(self.route_class,"route_class"))
        object.__setattr__(self,"milestones",tuple(_nonempty(x,"milestone") for x in self.milestones))
        if not bool(self.ordered):
            raise ValueError("runtime bootstrap accepts only closed ordered routes")


@dataclass(frozen=True)
class StateGatedTransitionContract:
    transition_id:str
    kind:str
    unconditional:bool
    source_profile:str
    raw:Mapping[str,Any]

    def __post_init__(self)->None:
        object.__setattr__(self,"transition_id",_nonempty(self.transition_id,"transition_id"))
        object.__setattr__(self,"kind",_nonempty(self.kind,"transition kind"))
        object.__setattr__(self,"source_profile",_nonempty(self.source_profile,"source_profile"))
        if bool(self.unconditional):
            raise ValueError("state-gated transition cannot be unconditional")
        object.__setattr__(self,"raw",MappingProxyType(dict(self.raw)))


@dataclass(frozen=True)
class RuntimeBootstrapProfile:
    schema_id:str
    contract_id:str
    historical_foundation:str
    runtime_world_profile:str
    runtime_world_evidence_role:str
    materializable_floor_count:int
    reachable_floor_count:int
    remaining_unreachable_floor_count:int
    routes:Mapping[int,FreshStartRouteContract]
    transitions:Mapping[str,StateGatedTransitionContract]
    raw:Mapping[str,Any]

    def __post_init__(self)->None:
        if self.schema_id!=BOOTSTRAP_SCHEMA:
            raise ValueError(f"unsupported bootstrap schema: {self.schema_id}")
        if self.historical_foundation!="taiwan-v1.0":
            raise ValueError("R1 historical foundation must remain taiwan-v1.0")
        if self.runtime_world_profile!="recovered25":
            raise ValueError("R1 runtime world profile must remain recovered25")
        if self.runtime_world_evidence_role!="LATER_RECOVERED":
            raise ValueError("recovered25 runtime world must remain LATER_RECOVERED")
        for value,label in (
            (self.materializable_floor_count,"materializable_floor_count"),
            (self.reachable_floor_count,"reachable_floor_count"),
            (self.remaining_unreachable_floor_count,"remaining_unreachable_floor_count"),
        ):
            if int(value)<0:
                raise ValueError(f"{label} must be non-negative")
        if int(self.reachable_floor_count)>int(self.materializable_floor_count):
            raise ValueError("reachable floor count exceeds materializable world")
        object.__setattr__(self,"routes",MappingProxyType(dict(self.routes)))
        object.__setattr__(self,"transitions",MappingProxyType(dict(self.transitions)))
        object.__setattr__(self,"raw",MappingProxyType(dict(self.raw)))


def load_runtime_bootstrap_contract(payload:Mapping[str,Any])->RuntimeBootstrapProfile:
    if payload.get("schema_id")!=BOOTSTRAP_SCHEMA:
        raise ValueError(f"unsupported bootstrap schema: {payload.get('schema_id')}")

    foundation=payload.get("historical_foundation")
    world_profile=payload.get("runtime_world_profile")
    world=payload.get("world")
    fresh=payload.get("fresh_start")
    transitions_raw=payload.get("state_gated_transitions")
    if not isinstance(foundation,Mapping):
        raise ValueError("historical_foundation must be an object")
    if not isinstance(world_profile,Mapping):
        raise ValueError("runtime_world_profile must be an object")
    if not isinstance(world,Mapping):
        raise ValueError("world must be an object")
    if not isinstance(fresh,Mapping):
        raise ValueError("fresh_start must be an object")
    if not isinstance(transitions_raw,list):
        raise ValueError("state_gated_transitions must be a list")

    if world_profile.get("historical_membership_in_taiwan_v1")!="UNPROVEN":
        raise ValueError("runtime contract must not promote recovered25 into Taiwan-v1 membership")
    if bool(world_profile.get("may_be_relabelled_as_taiwan_v1_content")):
        raise ValueError("runtime contract cannot relabel recovered25 as Taiwan-v1 content")

    route_rows=fresh.get("routes")
    if not isinstance(route_rows,list):
        raise ValueError("fresh_start.routes must be a list")
    routes={}
    for row in route_rows:
        if not isinstance(row,Mapping):
            raise ValueError("fresh-start route must be an object")
        route=FreshStartRouteContract(
            ordinal=int(row["ordinal"]),
            route_class=str(row["route_class"]),
            requires_shop=bool(row["requires_shop"]),
            requires_warpman=bool(row["requires_warpman"]),
            milestones=tuple(str(x) for x in row["milestones"]),
            ordered=bool(row["ordered"]),
        )
        if route.ordinal in routes:
            raise ValueError(f"duplicate fresh-start route ordinal {route.ordinal}")
        routes[route.ordinal]=route

    if int(fresh.get("normal_hometown_count",-1))!=len(routes):
        raise ValueError("normal hometown count does not match route table")
    if set(routes)!={1,2,3,4}:
        raise ValueError("R1 requires exactly hometown ordinals 1..4")
    if not bool(fresh.get("all_hometowns_ordered_progression")):
        raise ValueError("all-hometowns ordered progression must be closed")
    if not bool(fresh.get("all_hometowns_full_world")):
        raise ValueError("all-hometowns full world must be closed")

    transitions={}
    for row in transitions_raw:
        if not isinstance(row,Mapping):
            raise ValueError("state-gated transition must be an object")
        transition_id=_nonempty(row.get("id"),"state-gated transition id")
        source_profile=str(row.get("source_profile") or world_profile["profile"])
        transition=StateGatedTransitionContract(
            transition_id=transition_id,
            kind=str(row["kind"]),
            unconditional=bool(row["unconditional"]),
            source_profile=source_profile,
            raw=row,
        )
        if transition_id in transitions:
            raise ValueError(f"duplicate transition id {transition_id}")
        transitions[transition_id]=transition

    return RuntimeBootstrapProfile(
        schema_id=str(payload["schema_id"]),
        contract_id=_nonempty(payload["contract_id"],"contract_id"),
        historical_foundation=str(foundation["profile"]),
        runtime_world_profile=str(world_profile["profile"]),
        runtime_world_evidence_role=str(world_profile["evidence_role"]),
        materializable_floor_count=int(world["materializable_floor_count"]),
        reachable_floor_count=int(world["fresh_start_state_gated_reachable_floor_count"]),
        remaining_unreachable_floor_count=int(world["remaining_unreachable_floor_count"]),
        routes=routes,
        transitions=transitions,
        raw=payload,
    )


def load_runtime_bootstrap_file(path:Path)->RuntimeBootstrapProfile:
    try:
        payload=json.loads(Path(path).read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError("invalid runtime bootstrap JSON") from exc
    if not isinstance(payload,Mapping):
        raise ValueError("runtime bootstrap root must be an object")
    return load_runtime_bootstrap_contract(payload)


@dataclass(frozen=True)
class WorldRegionRequest:
    floor_id:int
    x1:int
    y1:int
    x2:int
    y2:int
    world_profile:str

    def __post_init__(self)->None:
        if int(self.floor_id)<0:
            raise ValueError("floor_id must be non-negative")
        if int(self.x2)<int(self.x1) or int(self.y2)<int(self.y1):
            raise ValueError("region bounds are inverted")
        object.__setattr__(self,"world_profile",_nonempty(self.world_profile,"world_profile"))


@dataclass(frozen=True)
class MaterializedWorldRegion:
    request:WorldRegionRequest
    payload:Any
    provenance:Mapping[str,Any]

    def __post_init__(self)->None:
        object.__setattr__(self,"provenance",MappingProxyType(dict(self.provenance)))


@dataclass(frozen=True)
class ResolvedTransitionBinding:
    transition_id:str
    source:MapPosition
    destination:MapPosition
    predicate_payload:Mapping[str,Any]
    provenance:Mapping[str,Any]

    def __post_init__(self)->None:
        object.__setattr__(self,"transition_id",_nonempty(self.transition_id,"transition_id"))
        object.__setattr__(self,"predicate_payload",MappingProxyType(dict(self.predicate_payload)))
        object.__setattr__(self,"provenance",MappingProxyType(dict(self.provenance)))


@dataclass(frozen=True)
class TransitionGateDecision:
    allowed:bool
    reason:str
    consumed_state:Mapping[str,Any]=MappingProxyType({})

    def __post_init__(self)->None:
        object.__setattr__(self,"reason",_nonempty(self.reason,"gate decision reason"))
        object.__setattr__(self,"consumed_state",MappingProxyType(dict(self.consumed_state)))


@dataclass(frozen=True)
class FreshStartSeed:
    contract_id:str
    world_profile:str
    hometown_ordinal:int
    position:MapPosition
    player_state:PersistentPlayerState

    def __post_init__(self)->None:
        object.__setattr__(self,"contract_id",_nonempty(self.contract_id,"contract_id"))
        object.__setattr__(self,"world_profile",_nonempty(self.world_profile,"world_profile"))
        ordinal=int(self.hometown_ordinal)
        if ordinal not in {1,2,3,4}:
            raise ValueError("hometown ordinal must be one of 1..4")
        object.__setattr__(self,"hometown_ordinal",ordinal)


@runtime_checkable
class VersionedWorldProfileProvider(Protocol):
    def materialize_region(self,request:WorldRegionRequest)->MaterializedWorldRegion:
        ...


@runtime_checkable
class TransitionBindingResolver(Protocol):
    def resolve_transition(
        self,
        contract:StateGatedTransitionContract,
    )->ResolvedTransitionBinding:
        ...


@runtime_checkable
class TransitionGateEvaluator(Protocol):
    def evaluate_transition(
        self,
        contract:StateGatedTransitionContract,
        binding:ResolvedTransitionBinding,
        session:"LocalRuntimeSessionState",
    )->TransitionGateDecision:
        ...


@runtime_checkable
class FreshStartFactory(Protocol):
    def create_fresh_start(
        self,
        profile:RuntimeBootstrapProfile,
        hometown_ordinal:int,
    )->FreshStartSeed:
        ...


@runtime_checkable
class LocalPersistenceStore(Protocol):
    def save(self,key:str,payload:str)->None:
        ...
    def load(self,key:str)->str|None:
        ...


@dataclass(frozen=True)
class LocalRuntimeSessionState:
    contract_id:str
    world_profile:str
    hometown_ordinal:int
    player_position:MapPosition
    player_state:PersistentPlayerState
    world_flags:frozenset[str]=frozenset()

    def __post_init__(self)->None:
        object.__setattr__(self,"contract_id",_nonempty(self.contract_id,"contract_id"))
        object.__setattr__(self,"world_profile",_nonempty(self.world_profile,"world_profile"))
        ordinal=int(self.hometown_ordinal)
        if ordinal not in {1,2,3,4}:
            raise ValueError("hometown ordinal must be one of 1..4")
        object.__setattr__(self,"hometown_ordinal",ordinal)
        object.__setattr__(
            self,
            "world_flags",
            frozenset(_nonempty(x,"world flag") for x in self.world_flags),
        )


def dump_local_runtime_session(state:LocalRuntimeSessionState)->dict[str,Any]:
    return {
        "schema":LOCAL_SESSION_SCHEMA,
        "contract_id":state.contract_id,
        "world_profile":state.world_profile,
        "hometown_ordinal":state.hometown_ordinal,
        "player_position":{
            "floor_id":int(state.player_position.floor_id),
            "x":int(state.player_position.x),
            "y":int(state.player_position.y),
        },
        "world_flags":sorted(state.world_flags),
        "player_state":dump_persistent_state(state.player_state),
    }


def encode_local_runtime_session(state:LocalRuntimeSessionState)->str:
    return json.dumps(
        dump_local_runtime_session(state),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",",":"),
    )


def load_local_runtime_session(
    payload:Mapping[str,Any],
    *,
    expected_contract_id:str|None=None,
    expected_world_profile:str|None=None,
)->LocalRuntimeSessionState:
    expected_keys={
        "schema","contract_id","world_profile","hometown_ordinal",
        "player_position","world_flags","player_state",
    }
    if set(payload)!=expected_keys:
        raise ValueError("local runtime session has unexpected shape")
    if payload["schema"]!=LOCAL_SESSION_SCHEMA:
        raise ValueError(f"unsupported local runtime session schema: {payload['schema']}")

    contract_id=_nonempty(payload["contract_id"],"contract_id")
    world_profile=_nonempty(payload["world_profile"],"world_profile")
    if expected_contract_id is not None and contract_id!=str(expected_contract_id):
        raise ValueError("local runtime session contract mismatch")
    if expected_world_profile is not None and world_profile!=str(expected_world_profile):
        raise ValueError("local runtime session world-profile mismatch")

    position=payload["player_position"]
    if not isinstance(position,Mapping) or set(position)!={"floor_id","x","y"}:
        raise ValueError("player_position has unexpected shape")
    flags=payload["world_flags"]
    if not isinstance(flags,list):
        raise ValueError("world_flags must be a list")
    player_payload=payload["player_state"]
    if not isinstance(player_payload,Mapping):
        raise ValueError("player_state must be an object")

    return LocalRuntimeSessionState(
        contract_id=contract_id,
        world_profile=world_profile,
        hometown_ordinal=int(payload["hometown_ordinal"]),
        player_position=MapPosition(
            int(position["floor_id"]),int(position["x"]),int(position["y"])
        ),
        player_state=load_persistent_state(player_payload),
        world_flags=frozenset(str(x) for x in flags),
    )


def decode_local_runtime_session(
    data:str,
    *,
    expected_contract_id:str|None=None,
    expected_world_profile:str|None=None,
)->LocalRuntimeSessionState:
    try:
        payload=json.loads(str(data))
    except json.JSONDecodeError as exc:
        raise ValueError("invalid local runtime session JSON") from exc
    if not isinstance(payload,Mapping):
        raise ValueError("local runtime session root must be an object")
    return load_local_runtime_session(
        payload,
        expected_contract_id=expected_contract_id,
        expected_world_profile=expected_world_profile,
    )
