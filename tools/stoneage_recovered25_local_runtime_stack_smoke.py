#!/usr/bin/env python3
"""Bundle-backed smoke for the concrete recovered25 local runtime stack.

The preservation bundle is consumed transiently. Output contains aggregate
closure markers only; raw recovered coordinates, item ids, filenames,
arguments and dialogue are not emitted.
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
from tools.stoneage_recovered25_local_runtime_stack import (
    Recovered25LocalRuntimeStack,
)
from tools.stoneage_recovered25_region_payload import (
    CLIENT_DAT_THREE_PLANE,
    SERVER_LS2MAP_TWO_PLANE,
    EngineNeutralMapRegion,
)
from tools.stoneage_recovered25_world_profile_adapter import (
    HOMETOWN_TRANSITION_IDS,
    SHADOWED_BRANCH_TRANSITION_ID,
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


OUTPUT_RESOLUTION = "RESOLUTION|RECOVERED25_LOCAL_RUNTIME_STACK_CLOSED"


def _player_state(_ordinal: int) -> PersistentPlayerState:
    fields = build_creation_state(5, 5, 5, 5, 5, 5, 0, 0)
    fields["name"] = "runtime-stack-smoke"
    return PersistentPlayerState(
        character=PlayerState(MappingProxyType(dict(fields)))
    )


def _session(profile, seed) -> LocalRuntimeSessionState:
    return LocalRuntimeSessionState(
        contract_id=profile.contract_id,
        world_profile=profile.runtime_world_profile,
        hometown_ordinal=seed.hometown_ordinal,
        player_position=seed.position,
        player_state=seed.player_state,
    )


def run(
    *,
    client_dat_dir: Path,
    npc_dir: Path,
    setup: Path,
    server_map_root: Path,
    mapset_path: Path,
):
    root = Path(__file__).resolve().parents[1]
    profile = load_runtime_bootstrap_file(
        root / "game" / "RUNTIME-BOOTSTRAP-RECOVERED25-R1.json"
    )
    stack = Recovered25LocalRuntimeStack.from_verified_bundle(
        profile=profile,
        player_state_factory=_player_state,
        client_dat_dir=client_dat_dir,
        npc_dir=npc_dir,
        setup=setup,
        server_map_root=server_map_root,
        mapset_path=mapset_path,
    )

    seeds = {ordinal: stack.create_fresh_start(ordinal) for ordinal in range(1, 5)}

    start_regions = {}
    for ordinal, seed in seeds.items():
        region = stack.materialize_player_position(_session(profile, seed))
        if not isinstance(region.payload, EngineNeutralMapRegion):
            raise TypeError("runtime stack did not return a concrete map region")
        start_regions[ordinal] = region

    representative_regions = []
    representatives = (
        min(stack.region_provider.plan.stable_dat_floor_ids),
        min(stack.region_provider.plan.supplemental_ls2map_floor_ids),
    )
    for floor_id in representatives:
        region = stack.materialize_region(
            WorldRegionRequest(
                floor_id=floor_id,
                x1=0,
                y1=0,
                x2=0,
                y2=0,
                world_profile=profile.runtime_world_profile,
            )
        )
        if not isinstance(region.payload, EngineNeutralMapRegion):
            raise TypeError("representative region is not concrete")
        representative_regions.append(region)

    representative_kinds = {
        region.payload.source_kind for region in representative_regions
    }
    if representative_kinds != {
        CLIENT_DAT_THREE_PLANE,
        SERVER_LS2MAP_TWO_PLANE,
    }:
        raise ValueError("runtime stack did not exercise both recovered map formats")

    allowed = 0
    for ordinal, transition_id in HOMETOWN_TRANSITION_IDS.items():
        binding = stack.resolve_transition(transition_id)
        required = int(binding.predicate_payload["item_template_id"])
        seed = seeds[ordinal]
        slot = InventorySlot(0)
        seed.player_state.inventory[slot] = InventoryItem(
            slot=slot,
            template_id=ItemTemplateId(required),
            view=MappingProxyType({}),
        )
        allowed += int(
            stack.evaluate_transition(
                transition_id,
                _session(profile, seed),
            ).allowed
        )

    ingress_binding = stack.resolve_transition(SHADOWED_BRANCH_TRANSITION_ID)
    clauses = ingress_binding.predicate_payload["free_clauses"]
    maxlevel = _configured_maxlevel(setup)
    chosen_level = None
    chosen_items = []
    for clause in clauses:
        level_atoms = [atom for atom in clause if atom["key"] == LEVEL]
        for level in range(1, maxlevel + 1):
            if not all(
                _compare(level, str(atom["operator"]), int(atom["operand"]))
                for atom in level_atoms
            ):
                continue
            candidate_items = []
            supported = True
            for atom in clause:
                if atom["key"] != ITEM:
                    continue
                op = str(atom["operator"])
                operand = int(atom["operand"])
                if op == "=":
                    candidate_items.append(operand)
                elif op == ">":
                    candidate_items.append(operand + 1)
                elif op == "<" and operand > 0:
                    candidate_items.append(operand - 1)
                else:
                    supported = False
                    break
            if supported:
                chosen_level = level
                chosen_items = candidate_items
                break
        if chosen_level is not None:
            break
    if chosen_level is None:
        raise ValueError("cannot construct legal shadowed-branch FREE witness")

    ingress_state = _player_state(1)
    fields = dict(ingress_state.character.fields)
    fields["level"] = chosen_level
    ingress_state.character = PlayerState(MappingProxyType(fields))
    for slot_index, item_id in enumerate(chosen_items):
        slot = InventorySlot(slot_index)
        ingress_state.inventory[slot] = InventoryItem(
            slot=slot,
            template_id=ItemTemplateId(item_id),
            view=MappingProxyType({}),
        )
    ingress_session = LocalRuntimeSessionState(
        contract_id=profile.contract_id,
        world_profile=profile.runtime_world_profile,
        hometown_ordinal=1,
        player_position=seeds[1].position,
        player_state=ingress_state,
    )
    allowed += int(
        stack.evaluate_transition(
            SHADOWED_BRANCH_TRANSITION_ID,
            ingress_session,
        ).allowed
    )

    saved = LocalRuntimeSessionState(
        contract_id=profile.contract_id,
        world_profile=profile.runtime_world_profile,
        hometown_ordinal=3,
        player_position=seeds[3].position,
        player_state=seeds[3].player_state,
        world_flags=frozenset({"runtime-stack-smoke"}),
    )
    restored = decode_local_runtime_session(
        encode_local_runtime_session(saved),
        expected_contract_id=profile.contract_id,
        expected_world_profile=profile.runtime_world_profile,
    )
    roundtrip = (
        restored.hometown_ordinal == saved.hometown_ordinal
        and restored.player_position == saved.player_position
        and restored.world_flags == saved.world_flags
    )
    return (
        profile,
        stack,
        seeds,
        start_regions,
        representative_regions,
        allowed,
        roundtrip,
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--client-dat-dir", type=Path, required=True)
    ap.add_argument("--npc-dir", type=Path, required=True)
    ap.add_argument("--setup", type=Path, required=True)
    ap.add_argument("--server-map-root", type=Path, required=True)
    ap.add_argument("--mapset", type=Path, required=True)
    a = ap.parse_args()
    profile, stack, seeds, start_regions, reps, allowed, roundtrip = run(
        client_dat_dir=a.client_dat_dir,
        npc_dir=a.npc_dir,
        setup=a.setup,
        server_map_root=a.server_map_root,
        mapset_path=a.mapset,
    )
    print("StoneAge recovered25 concrete local runtime stack — R1")
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print(
        "RULE|raw transition coordinates, item identities, arguments, dialogue "
        "and map payload bytes remain transient"
    )
    print(f"COUNT|materializable_floors|{len(stack.world_adapter.topology.maps)}")
    print(f"COUNT|state_gated_bindings|{len(stack.transition_resolver.bindings)}")
    print(f"COUNT|fresh_start_seeds|{len(seeds)}")
    print(f"COUNT|fresh_start_concrete_regions|{len(start_regions)}")
    print(f"COUNT|representative_payload_formats|{len({r.payload.source_kind for r in reps})}")
    print(f"COUNT|state_gated_allow_decisions|{allowed}")
    print(f"LOCAL_SESSION_ROUNDTRIP|witness={int(roundtrip)}")
    print(
        "PROVENANCE_SEPARATION|historical_foundation="
        f"{profile.historical_foundation}|runtime_world={profile.runtime_world_profile}|"
        f"evidence_role={profile.runtime_world_evidence_role}"
    )
    print(OUTPUT_RESOLUTION)


if __name__ == "__main__":
    main()
