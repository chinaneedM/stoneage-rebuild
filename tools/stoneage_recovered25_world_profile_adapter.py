#!/usr/bin/env python3
"""Recovered25 implementation adapter for the engine-neutral local runtime.

This layer consumes only committed provenance-safe world manifests by default.
Raw recovered NPC/WarpMan operands are derived only when a verified recovered25
bundle is explicitly supplied.  Those raw bindings remain in memory and are
not written into the public bootstrap contract.

The adapter therefore preserves three independent identities:
- historical foundation: Taiwan/Waei v1.0;
- runtime world profile: recovered25 / LATER_RECOVERED;
- local product runtime: engine-neutral, local-first DESIGN state.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any, Callable, Mapping

from tools.stoneage_local_runtime_core import (
    FreshStartSeed,
    LocalRuntimeSessionState,
    MaterializedWorldRegion,
    ResolvedTransitionBinding,
    RuntimeBootstrapProfile,
    StateGatedTransitionContract,
    TransitionGateDecision,
    WorldRegionRequest,
)
from tools.stoneage_ordered_runtime_world_topology import (
    OrderedMaterializableRuntimeTopology,
    load_ordered_materializable_runtime_topology,
)
from tools.stoneage_player_birth_model import birth_state
from tools.stoneage_shadowed_branch_fresh_start_dialogue_warp_bridge_probe import (
    WARPMAN,
    DialogueWarp,
    _collect_dialogue_warps,
    analyze as analyze_dialogue_bridges,
)
from tools.stoneage_shadowed_branch_fresh_start_warpman_bridge_item_surface_probe import (
    _requirements,
)
from tools.stoneage_state_gated_runtime_world_reachability_probe import (
    PROGRESSION_REPORT_REF,
    parse_progression_witness,
)
from tools.stoneage_singleplayer_domain import (
    ItemTemplateId,
    MapPosition,
    PersistentPlayerState,
)
from tools.stoneage_singleplayer_world import (
    LATER_RECOVERED,
    HistoricalMapDefinition,
)


RECOVERED25_PROFILE="recovered25"
SHADOWED_BRANCH_TRANSITION_ID="shadowed_branch_ingress"
HOMETOWN_TRANSITION_IDS={
    3:"fresh_start_hometown_3_bridge",
    4:"fresh_start_hometown_4_bridge",
}
SHADOWED_BRANCH_UNLOCK_FLAG=(
    "transition:shadowed_branch_ingress:progression_unlocked"
)


@dataclass(frozen=True)
class Recovered25RegionDescriptor:
    floor_id:int
    width:int
    height:int
    x1:int
    y1:int
    x2:int
    y2:int
    map_sha256:str
    content_role:str
    resource_role:str
    source_versions:tuple[str,...]
    evidence_refs:tuple[str,...]

    def __post_init__(self)->None:
        if self.content_role!=LATER_RECOVERED:
            raise ValueError("recovered25 region descriptor must remain LATER_RECOVERED")
        if not self.map_sha256:
            raise ValueError("recovered25 region descriptor requires map SHA-256")


@dataclass(frozen=True)
class Recovered25WorldProfileAdapter:
    profile:RuntimeBootstrapProfile
    runtime:OrderedMaterializableRuntimeTopology

    @classmethod
    def from_repository(
        cls,
        profile:RuntimeBootstrapProfile,
    )->"Recovered25WorldProfileAdapter":
        if profile.runtime_world_profile!=RECOVERED25_PROFILE:
            raise ValueError("adapter requires recovered25 runtime world profile")
        runtime=load_ordered_materializable_runtime_topology()
        adapter=cls(profile=profile,runtime=runtime)
        adapter._validate()
        return adapter

    @property
    def topology(self):
        return self.runtime.topology

    def _validate(self)->None:
        topology=self.runtime.topology
        if len(topology.maps)!=int(self.profile.materializable_floor_count):
            raise ValueError("bootstrap/materializable map count drift")
        if set(topology.maps)!=set(self.runtime.base.extension.materializable_floor_ids):
            raise ValueError("runtime topology/materializable floor-set drift")
        for floor_id,definition in topology.maps.items():
            provenance=definition.provenance
            if provenance is None:
                raise ValueError(f"recovered25 floor {floor_id} lacks provenance")
            if provenance.content_role!=LATER_RECOVERED:
                raise ValueError(
                    f"recovered25 floor {floor_id} was promoted beyond LATER_RECOVERED"
                )
            if provenance.claims_early_membership:
                raise ValueError(
                    f"recovered25 floor {floor_id} claims early membership"
                )

    def hometown_positions(self)->Mapping[int,MapPosition]:
        out={}
        for ordinal in range(1,5):
            row=birth_state(ordinal-1)
            position=MapPosition(
                int(row["elder_floor"]),
                int(row["elder_x"]),
                int(row["elder_y"]),
            )
            if not self.topology.is_valid_position(position):
                raise ValueError(
                    f"hometown {ordinal} lies outside recovered25 topology"
                )
            out[ordinal]=position
        return MappingProxyType(out)

    def map_definition(self,floor_id:int)->HistoricalMapDefinition:
        floor_id=int(floor_id)
        definition=self.topology.maps.get(floor_id)
        if definition is None:
            raise KeyError(f"floor {floor_id} is not materializable in recovered25")
        return definition

    def materialize_region(
        self,
        request:WorldRegionRequest,
    )->MaterializedWorldRegion:
        if request.world_profile!=self.profile.runtime_world_profile:
            raise ValueError("region request world-profile mismatch")
        definition=self.map_definition(request.floor_id)
        if (
            request.x1<0 or request.y1<0
            or request.x2>=definition.width
            or request.y2>=definition.height
        ):
            raise ValueError("region request exceeds recovered map bounds")
        provenance=definition.provenance
        if provenance is None:
            raise ValueError("materializable map unexpectedly lacks provenance")
        descriptor=Recovered25RegionDescriptor(
            floor_id=definition.floor_id,
            width=definition.width,
            height=definition.height,
            x1=int(request.x1),
            y1=int(request.y1),
            x2=int(request.x2),
            y2=int(request.y2),
            map_sha256=str(provenance.payload_sha256),
            content_role=provenance.content_role,
            resource_role=provenance.resource_role,
            source_versions=tuple(provenance.source_versions),
            evidence_refs=tuple(provenance.evidence_refs),
        )
        return MaterializedWorldRegion(
            request=request,
            payload=descriptor,
            provenance={
                "world_profile":self.profile.runtime_world_profile,
                "evidence_role":self.profile.runtime_world_evidence_role,
                "content_role":provenance.content_role,
                "resource_role":provenance.resource_role,
                "source_versions":tuple(provenance.source_versions),
                "evidence_refs":tuple(provenance.evidence_refs),
                "payload_sha256":provenance.payload_sha256,
                "payload_kind":"PROVENANCE_MAP_REGION_DESCRIPTOR",
            },
        )


@dataclass
class Recovered25FreshStartFactory:
    adapter:Recovered25WorldProfileAdapter
    player_state_factory:Callable[[int],PersistentPlayerState]

    def create_fresh_start(
        self,
        profile:RuntimeBootstrapProfile,
        hometown_ordinal:int,
    )->FreshStartSeed:
        if profile.contract_id!=self.adapter.profile.contract_id:
            raise ValueError("fresh-start bootstrap contract mismatch")
        ordinal=int(hometown_ordinal)
        route=profile.routes.get(ordinal)
        if route is None:
            raise ValueError(f"unknown fresh-start hometown ordinal {ordinal}")
        if not route.ordered:
            raise ValueError("fresh-start route is not closed")
        state=self.player_state_factory(ordinal)
        if not isinstance(state,PersistentPlayerState):
            raise TypeError("player_state_factory must return PersistentPlayerState")
        position=self.adapter.hometown_positions()[ordinal]
        return FreshStartSeed(
            contract_id=profile.contract_id,
            world_profile=profile.runtime_world_profile,
            hometown_ordinal=ordinal,
            position=position,
            player_state=state,
        )


def _anchor(rect:tuple[int,int,int,int],floor_id:int)->MapPosition:
    x1,y1,x2,y2=(int(v) for v in rect)
    return MapPosition(int(floor_id),min(x1,x2),min(y1,y2))


def _binding_provenance(kind:str)->Mapping[str,Any]:
    return {
        "source_profile":RECOVERED25_PROFILE,
        "evidence_role":LATER_RECOVERED,
        "binding_kind":str(kind),
        "raw_binding_persisted":False,
    }


def _dialogue_binding(
    *,
    transition_id:str,
    edge:DialogueWarp,
    predicate_payload:Mapping[str,Any],
    binding_kind:str,
)->ResolvedTransitionBinding:
    if edge.kind!=WARPMAN:
        raise ValueError("current gated binding requires WarpMan")
    return ResolvedTransitionBinding(
        transition_id=transition_id,
        source=_anchor(edge.source_rect,edge.source_floor),
        destination=MapPosition(
            int(edge.destination_floor),
            int(edge.destination_x),
            int(edge.destination_y),
        ),
        predicate_payload={
            **dict(predicate_payload),
            "interaction_kind":"DIALOGUE_WARPMAN",
            "source_rect":tuple(int(v) for v in edge.source_rect),
        },
        provenance=_binding_provenance(binding_kind),
    )


def derive_recovered25_transition_bindings(
    *,
    profile:RuntimeBootstrapProfile,
    npc_dir:Path,
    setup:Path,
    server_map_root:Path,
    mapset_path:Path,
    progression_report:Path=Path(PROGRESSION_REPORT_REF),
)->Mapping[str,ResolvedTransitionBinding]:
    """Derive raw recovered25 bindings transiently from a verified bundle."""

    if profile.runtime_world_profile!=RECOVERED25_PROFILE:
        raise ValueError("binding derivation requires recovered25 profile")

    spatial=analyze_dialogue_bridges(
        npc_dir=npc_dir,
        setup=setup,
        server_map_root=server_map_root,
        mapset_path=mapset_path,
    )
    by_ordinal={int(row.ordinal):row for row in spatial.rows}
    bindings={}

    for ordinal,transition_id in HOMETOWN_TRANSITION_IDS.items():
        row=by_ordinal.get(ordinal)
        if row is None:
            raise ValueError(f"missing dialogue-bridge row for hometown {ordinal}")
        if row.baseline_classic.reachable:
            raise ValueError(f"hometown {ordinal} unexpectedly became classic-reachable")
        if not row.baseline_warpman.reachable:
            raise ValueError(f"hometown {ordinal} lost selected WarpMan bridge")
        edges=row.baseline_warpman.edge_sequence
        if len(edges)!=1 or edges[0].kind!=WARPMAN:
            raise ValueError(
                f"hometown {ordinal} must have exactly one selected WarpMan edge"
            )
        requirements=_requirements(ordinal,edges)
        if len(requirements)!=1:
            raise ValueError("selected hometown bridge requirement count drift")
        req=requirements[0]
        if req.operator!="=":
            raise ValueError("selected hometown bridge is no longer ITEM equality")
        bindings[transition_id]=_dialogue_binding(
            transition_id=transition_id,
            edge=edges[0],
            predicate_payload={
                "gate_kind":"ITEM_EQ",
                "item_template_id":int(req.item_id),
                "operator":req.operator,
                "event_action_side_effect_fields":0,
            },
            binding_kind="SELECTED_FRESH_START_WARPMAN",
        )

    witness=parse_progression_witness(
        progression_report.read_text(encoding="utf-8")
    )
    dialogue_edges,_counts,_malformed,_missing=_collect_dialogue_warps(npc_dir)
    ingress=tuple(
        edge for edge in dialogue_edges
        if (
            edge.kind==WARPMAN
            and int(edge.source_floor)==int(witness.source_floor)
            and int(edge.destination_floor)==int(witness.destination_floor)
        )
    )
    signatures={
        (
            edge.source_floor,
            tuple(edge.source_rect),
            edge.destination_floor,
            edge.destination_x,
            edge.destination_y,
            edge.argument_data,
        )
        for edge in ingress
    }
    unique=tuple(
        next(
            edge for edge in ingress
            if (
                edge.source_floor,
                tuple(edge.source_rect),
                edge.destination_floor,
                edge.destination_x,
                edge.destination_y,
                edge.argument_data,
            )==signature
        )
        for signature in signatures
    )
    if len(unique)!=1:
        raise ValueError(
            "shadowed-branch gated ingress is not uniquely bindable from recovered25"
        )
    bindings[SHADOWED_BRANCH_TRANSITION_ID]=_dialogue_binding(
        transition_id=SHADOWED_BRANCH_TRANSITION_ID,
        edge=unique[0],
        predicate_payload={
            "gate_kind":"WORLD_FLAG",
            "required_world_flag":SHADOWED_BRANCH_UNLOCK_FLAG,
            "progression_witness_closed":True,
        },
        binding_kind="SHADOWED_BRANCH_PROGRESSION_WARPMAN",
    )

    expected=set(profile.transitions)
    if set(bindings)!=expected:
        raise ValueError(
            "derived transition binding set disagrees with bootstrap contract; "
            f"derived={sorted(bindings)}, expected={sorted(expected)}"
        )
    return MappingProxyType(bindings)


@dataclass(frozen=True)
class Recovered25TransitionBindingResolver:
    profile:RuntimeBootstrapProfile
    adapter:Recovered25WorldProfileAdapter
    bindings:Mapping[str,ResolvedTransitionBinding]

    def __post_init__(self)->None:
        bindings=dict(self.bindings)
        if set(bindings)!=set(self.profile.transitions):
            raise ValueError("binding resolver transition-set drift")
        for transition_id,binding in bindings.items():
            if binding.transition_id!=transition_id:
                raise ValueError("transition binding identity drift")
            if binding.provenance.get("source_profile")!=RECOVERED25_PROFILE:
                raise ValueError("transition binding lost recovered25 provenance")
            if not self.adapter.topology.is_valid_position(binding.source):
                raise ValueError(f"binding source outside topology: {transition_id}")
            if not self.adapter.topology.is_valid_position(binding.destination):
                raise ValueError(f"binding destination outside topology: {transition_id}")
        object.__setattr__(self,"bindings",MappingProxyType(bindings))

    def resolve_transition(
        self,
        contract:StateGatedTransitionContract,
    )->ResolvedTransitionBinding:
        if contract.transition_id not in self.profile.transitions:
            raise KeyError(f"transition not declared by bootstrap: {contract.transition_id}")
        if contract.unconditional:
            raise ValueError("state-gated contract cannot be unconditional")
        binding=self.bindings.get(contract.transition_id)
        if binding is None:
            raise KeyError(f"transition binding missing: {contract.transition_id}")
        return binding


@dataclass(frozen=True)
class Recovered25TransitionGateEvaluator:
    profile:RuntimeBootstrapProfile

    def evaluate_transition(
        self,
        contract:StateGatedTransitionContract,
        binding:ResolvedTransitionBinding,
        session:LocalRuntimeSessionState,
    )->TransitionGateDecision:
        if session.contract_id!=self.profile.contract_id:
            raise ValueError("transition session contract mismatch")
        if session.world_profile!=self.profile.runtime_world_profile:
            raise ValueError("transition session world-profile mismatch")
        if binding.transition_id!=contract.transition_id:
            raise ValueError("transition binding/contract identity mismatch")
        if contract.unconditional:
            raise ValueError("state-gated transition cannot be unconditional")

        gate_kind=str(binding.predicate_payload.get("gate_kind",""))
        if gate_kind=="ITEM_EQ":
            required=int(binding.predicate_payload["item_template_id"])
            held={
                int(item.template_id.value)
                for item in session.player_state.inventory.values()
            }
            allowed=required in held
            return TransitionGateDecision(
                allowed=allowed,
                reason=(
                    "required recovered25 bridge item is carried"
                    if allowed
                    else "required recovered25 bridge item is absent"
                ),
                consumed_state={},
            )

        if gate_kind=="WORLD_FLAG":
            flag=str(binding.predicate_payload["required_world_flag"])
            allowed=flag in session.world_flags
            return TransitionGateDecision(
                allowed=allowed,
                reason=(
                    "closed progression state flag is present"
                    if allowed
                    else "closed progression state flag is absent"
                ),
                consumed_state={},
            )

        raise ValueError(f"unsupported recovered25 transition gate kind: {gate_kind}")
