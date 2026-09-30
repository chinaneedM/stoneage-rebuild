#!/usr/bin/env python3
"""Bundle-backed smoke test for the recovered25 local runtime adapter.

Raw recovered operands are used transiently.  Output intentionally contains only
aggregate closure markers and no coordinates, item IDs, filenames or dialogue.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from types import MappingProxyType

from tools.stoneage_local_runtime_core import (
    LocalRuntimeSessionState,
    WorldRegionRequest,
    decode_local_runtime_session,
    encode_local_runtime_session,
    load_runtime_bootstrap_file,
)
from tools.stoneage_player_creation_model import build_creation_state
from tools.stoneage_recovered25_world_profile_adapter import (
    HOMETOWN_TRANSITION_IDS,
    SHADOWED_BRANCH_TRANSITION_ID,
    Recovered25FreshStartFactory,
    Recovered25TransitionBindingResolver,
    Recovered25TransitionGateEvaluator,
    Recovered25WorldProfileAdapter,
    derive_recovered25_transition_bindings,
)
from tools.stoneage_shadowed_branch_warpman_satisfiability_probe import (
    ITEM,
    LEVEL,
    _compare,
    _configured_maxlevel,
)
from tools.stoneage_singleplayer_domain import (
    InventoryItem,
    InventorySlot,
    ItemTemplateId,
    PersistentPlayerState,
    PlayerState,
)


OUTPUT_RESOLUTION="RESOLUTION|RECOVERED25_LOCAL_RUNTIME_ADAPTER_SMOKE_CLOSED"


def _player_state(_ordinal:int)->PersistentPlayerState:
    fields=build_creation_state(5,5,5,5,5,5,0,0)
    fields["name"]="adapter-smoke"
    return PersistentPlayerState(
        character=PlayerState(MappingProxyType(dict(fields)))
    )


def run(
    *,
    npc_dir:Path,
    setup:Path,
    server_map_root:Path,
    mapset_path:Path,
):
    root=Path(__file__).resolve().parents[1]
    profile=load_runtime_bootstrap_file(
        root/"game"/"RUNTIME-BOOTSTRAP-RECOVERED25-R1.json"
    )
    adapter=Recovered25WorldProfileAdapter.from_repository(profile)
    bindings=derive_recovered25_transition_bindings(
        profile=profile,
        npc_dir=npc_dir,
        setup=setup,
        server_map_root=server_map_root,
        mapset_path=mapset_path,
    )
    resolver=Recovered25TransitionBindingResolver(
        profile=profile,
        adapter=adapter,
        bindings=bindings,
    )
    evaluator=Recovered25TransitionGateEvaluator(profile)
    factory=Recovered25FreshStartFactory(adapter,_player_state)

    seeds={}
    regions={}
    for ordinal in range(1,5):
        seed=factory.create_fresh_start(profile,ordinal)
        seeds[ordinal]=seed
        regions[ordinal]=adapter.materialize_region(WorldRegionRequest(
            floor_id=seed.position.floor_id,
            x1=seed.position.x,
            y1=seed.position.y,
            x2=seed.position.x,
            y2=seed.position.y,
            world_profile=profile.runtime_world_profile,
        ))

    allowed=0
    for ordinal,transition_id in HOMETOWN_TRANSITION_IDS.items():
        contract=profile.transitions[transition_id]
        binding=resolver.resolve_transition(contract)
        required=int(binding.predicate_payload["item_template_id"])
        seed=seeds[ordinal]
        seed.player_state.inventory[InventorySlot(0)]=InventoryItem(
            slot=InventorySlot(0),
            template_id=ItemTemplateId(required),
            view=MappingProxyType({}),
        )
        session=LocalRuntimeSessionState(
            contract_id=profile.contract_id,
            world_profile=profile.runtime_world_profile,
            hometown_ordinal=ordinal,
            player_position=seed.position,
            player_state=seed.player_state,
        )
        allowed+=int(
            evaluator.evaluate_transition(contract,binding,session).allowed
        )

    ingress_contract=profile.transitions[SHADOWED_BRANCH_TRANSITION_ID]
    ingress_binding=resolver.resolve_transition(ingress_contract)
    clauses=ingress_binding.predicate_payload["free_clauses"]
    maxlevel=_configured_maxlevel(setup)
    chosen_level=None
    chosen_items=[]
    for clause in clauses:
        level_atoms=[atom for atom in clause if atom["key"]==LEVEL]
        for level in range(1,maxlevel+1):
            if all(_compare(level,str(atom["operator"]),int(atom["operand"])) for atom in level_atoms):
                candidate_items=[]
                supported=True
                for atom in clause:
                    if atom["key"]!=ITEM:
                        continue
                    op=str(atom["operator"]); operand=int(atom["operand"])
                    if op=="=":
                        candidate_items.append(operand)
                    elif op==">":
                        candidate_items.append(operand+1)
                    elif op=="<" and operand>0:
                        candidate_items.append(operand-1)
                    else:
                        supported=False
                        break
                if supported:
                    chosen_level=level
                    chosen_items=candidate_items
                    break
        if chosen_level is not None:
            break
    if chosen_level is None:
        raise ValueError("cannot construct a legal in-memory FREE witness")

    ingress_state=_player_state(1)
    fields=dict(ingress_state.character.fields)
    fields["level"]=chosen_level
    ingress_state.character=PlayerState(MappingProxyType(fields))
    for slot,item_id in enumerate(chosen_items):
        s=InventorySlot(slot)
        ingress_state.inventory[s]=InventoryItem(
            slot=s,template_id=ItemTemplateId(item_id),view=MappingProxyType({})
        )
    ingress_session=LocalRuntimeSessionState(
        contract_id=profile.contract_id,
        world_profile=profile.runtime_world_profile,
        hometown_ordinal=1,
        player_position=seeds[1].position,
        player_state=ingress_state,
    )
    allowed+=int(
        evaluator.evaluate_transition(
            ingress_contract,ingress_binding,ingress_session
        ).allowed
    )

    saved=LocalRuntimeSessionState(
        contract_id=profile.contract_id,
        world_profile=profile.runtime_world_profile,
        hometown_ordinal=3,
        player_position=seeds[3].position,
        player_state=seeds[3].player_state,
        world_flags=frozenset({"adapter-smoke"}),
    )
    restored=decode_local_runtime_session(
        encode_local_runtime_session(saved),
        expected_contract_id=profile.contract_id,
        expected_world_profile=profile.runtime_world_profile,
    )
    roundtrip=(
        restored.hometown_ordinal==saved.hometown_ordinal
        and restored.player_position==saved.player_position
        and restored.world_flags==saved.world_flags
    )
    return profile,adapter,bindings,seeds,regions,allowed,roundtrip


def main()->None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--npc-dir",type=Path,required=True)
    ap.add_argument("--setup",type=Path,required=True)
    ap.add_argument("--server-map-root",type=Path,required=True)
    ap.add_argument("--mapset",type=Path,required=True)
    a=ap.parse_args()
    profile,adapter,bindings,seeds,regions,allowed,roundtrip=run(
        npc_dir=a.npc_dir,
        setup=a.setup,
        server_map_root=a.server_map_root,
        mapset_path=a.mapset,
    )
    print("StoneAge recovered25 local runtime adapter smoke — R1")
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print("RULE|raw transition coordinates, item identities, argument payloads and dialogue are transient and withheld")
    print(f"COUNT|materializable_floors|{len(adapter.topology.maps)}")
    print(f"COUNT|active_ordered_classic_warps|{len(adapter.topology.legacy_warps)}")
    print(f"COUNT|deferred_conditional_classic_warps|{len(adapter.runtime.base.deferred_conditional_warps)}")
    print(f"COUNT|dynamic_free_gate_bindings|{sum(binding.predicate_payload.get('gate_kind')=='FREE_CLAUSES' for binding in bindings.values())}")
    print(f"COUNT|state_gated_bindings|{len(bindings)}")
    print(f"COUNT|fresh_start_seeds|{len(seeds)}")
    print(f"COUNT|region_descriptors_materialized|{len(regions)}")
    print(f"COUNT|state_gated_allow_decisions|{allowed}")
    print(f"LOCAL_SESSION_ROUNDTRIP|witness={int(roundtrip)}")
    print(
        "PROVENANCE_SEPARATION|historical_foundation="
        f"{profile.historical_foundation}|runtime_world={profile.runtime_world_profile}|"
        f"evidence_role={profile.runtime_world_evidence_role}"
    )
    print(OUTPUT_RESOLUTION)


if __name__=="__main__":
    main()
