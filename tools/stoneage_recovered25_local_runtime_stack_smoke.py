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

from tools.stoneage_enemy_spawn_model import EnemyBirthRolls

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
from tools.stoneage_recovered25_collision_router import CLIENT_PROVIDER_KIND
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
    MapPosition,
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
    server_data_dir: Path,
    server_map_root: Path,
    mapset_path: Path,
    client_adrn_path: Path,
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
        server_data_dir=server_data_dir,
        server_map_root=server_map_root,
        mapset_path=mapset_path,
        client_adrn_path=client_adrn_path,
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

    if stack.encounter_runtime is None:
        raise ValueError("runtime stack lacks encounter runtime")
    if stack.enemybase_runtime is None:
        raise ValueError("runtime stack lacks enemybase runtime")
    if len(stack.enemybase_runtime.templates) != 988:
        raise ValueError("unexpected recovered25 enemybase template count")
    if stack.petskill_runtime is None:
        raise ValueError("runtime stack lacks pet-skill runtime")
    if len(stack.petskill_runtime.skills) != 147:
        raise ValueError("unexpected recovered25 pet-skill count")
    referenced_skill_ids = {
        int(skill_id)
        for template in stack.enemybase_runtime.templates.values()
        for skill_id in (
            template.skill_slot_ids
            if template.skill_slot_ids
            else template.skill_ids
        )
        if int(skill_id) > 0
    }
    unresolved_skill_ids = stack.petskill_runtime.unresolved_skill_ids(
        referenced_skill_ids
    )
    if unresolved_skill_ids:
        raise ValueError(
            "recovered25 enemybase references unresolved pet-skill IDs"
        )
    referenced_template_ids = (
        stack.enemybase_runtime.referenced_template_ids(
            stack.encounter_runtime
        )
    )
    unresolved_template_ids = (
        stack.enemybase_runtime.unresolved_template_ids(
            stack.encounter_runtime
        )
    )
    if unresolved_template_ids:
        raise ValueError(
            "stable encounter references unresolved enemybase templates"
        )
    encounter_adapter = stack.encounter_runtime
    if len(encounter_adapter.encounter_areas) != 402:
        raise ValueError("unexpected stable encounter-area count")
    if len(encounter_adapter.unresolved_positive_group_refs) != 23:
        raise ValueError("unexpected unresolved encounter-group defect count")
    if len(encounter_adapter.specimen_defect_area_indices) != 19:
        raise ValueError("unexpected affected encounter-area defect count")

    encounter_witness = None
    spawn_witness = None
    defect_areas = set(encounter_adapter.specimen_defect_area_indices)
    for area in encounter_adapter.encounter_areas:
        if area.index in defect_areas:
            continue
        choices = tuple(
            (group, weight)
            for group, weight in area.resolved_group_choices(
                encounter_adapter.groups,
                (),
            )
            if int(weight) > 0
        )
        if not choices:
            continue
        witness_state = _player_state(1)
        witness_session = LocalRuntimeSessionState(
            contract_id=profile.contract_id,
            world_profile=profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(
                int(area.floor),
                int(area.min_x),
                int(area.min_y),
            ),
            player_state=witness_state,
        )
        try:
            group_request = stack.request_encounter_group(
                witness_session,
                group_roll=0,
            )
            encounter_request = stack.request_encounter(
                witness_session,
                group_roll=0,
                enemy_roll=0,
                level_roll=0,
            )
        except (KeyError, ValueError):
            continue
        if group_request is None or encounter_request is None:
            continue
        try:
            spawned = stack.spawn_group_enemies(
                group_request,
                entry_count_roll=1,
                selection_rolls=(0,) * 100,
                birth_rolls=(
                    EnemyBirthRolls(
                        level_roll=0,
                        birth_offsets=(0, 0, 0, 0),
                        spawn_allocation_rolls=(
                            0, 1, 2, 3, 0, 1, 2, 3, 0, 1
                        ),
                    ),
                ),
            )
        except (KeyError, ValueError):
            continue
        if len(spawned) != 1:
            continue
        encounter_witness = (group_request, encounter_request)
        spawn_witness = spawned
        break
    if encounter_witness is None:
        raise ValueError("no legal recovered25 encounter runtime witness found")
    if spawn_witness is None:
        raise ValueError("no legal recovered25 spawn/birth runtime witness found")

    if stack.client_collision_provider is None or stack.collision_router is None:
        raise ValueError("runtime stack lacks full collision composition")
    client_witness = None
    for floor_id in sorted(stack.client_collision_provider.supported_floor_ids):
        hit_map = stack.client_collision_provider._hit_map(floor_id)
        found = False
        for y in range(hit_map.height):
            for x in range(hit_map.width):
                if hit_map.blocked_at(x, y):
                    continue
                for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if not (0 <= nx < hit_map.width and 0 <= ny < hit_map.height):
                        continue
                    if hit_map.blocked_at(nx, ny):
                        continue
                    origin = MapPosition(floor_id, x, y)
                    destination = MapPosition(floor_id, nx, ny)
                    routed = stack.collision_router.routed_step_verdict(
                        origin=origin,
                        destination=destination,
                    )
                    if (
                        routed.route.provider_kind == CLIENT_PROVIDER_KIND
                        and routed.decision.allowed
                    ):
                        client_witness = routed
                        found = True
                        break
                if found:
                    break
            if found:
                break
        if client_witness is not None:
            break
    if client_witness is None:
        raise ValueError("no legal client collision movement witness found")

    return (
        profile,
        stack,
        seeds,
        start_regions,
        representative_regions,
        allowed,
        roundtrip,
        client_witness,
        encounter_witness,
        spawn_witness,
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--client-dat-dir", type=Path, required=True)
    ap.add_argument("--npc-dir", type=Path, required=True)
    ap.add_argument("--setup", type=Path, required=True)
    ap.add_argument("--server-data-dir", type=Path, required=True)
    ap.add_argument("--server-map-root", type=Path, required=True)
    ap.add_argument("--mapset", type=Path, required=True)
    ap.add_argument("--client-adrn", type=Path, required=True)
    a = ap.parse_args()
    (
        profile,
        stack,
        seeds,
        start_regions,
        reps,
        allowed,
        roundtrip,
        client_witness,
        encounter_witness,
        spawn_witness,
    ) = run(
        client_dat_dir=a.client_dat_dir,
        npc_dir=a.npc_dir,
        setup=a.setup,
        server_data_dir=a.server_data_dir,
        server_map_root=a.server_map_root,
        mapset_path=a.mapset,
        client_adrn_path=a.client_adrn,
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
    coverage = stack.collision_router.coverage_counts()
    print(f"COUNT|collision_server_routed_floors|{coverage['server_routed_floors']}")
    print(
        "COUNT|collision_client_reconstruction_routed_floors|"
        f"{coverage['client_reconstruction_routed_floors']}"
    )
    print(
        "COUNT|collision_routed_floors|"
        f"{coverage['server_routed_floors'] + coverage['client_reconstruction_routed_floors']}"
    )
    print(f"COUNT|collision_unrouted_floors|{coverage['unrouted_floors']}")
    print(
        "CLIENT_COLLISION_PROFILE|"
        f"{client_witness.route.semantic_profile}|"
        f"exact_recovered25_binary_proof={int(bool(client_witness.route.exact_recovered25_binary_proof))}"
    )
    print("CLIENT_COLLISION_MOVEMENT_WITNESS|1")
    report_referenced_template_ids = stack.enemybase_runtime.referenced_template_ids(
        stack.encounter_runtime
    )
    report_unresolved_template_ids = stack.enemybase_runtime.unresolved_template_ids(
        stack.encounter_runtime
    )
    print(f"COUNT|enemybase_templates|{len(stack.enemybase_runtime.templates)}")
    report_referenced_skill_ids = {
        int(skill_id)
        for template in stack.enemybase_runtime.templates.values()
        for skill_id in (
            template.skill_slot_ids
            if template.skill_slot_ids
            else template.skill_ids
        )
        if int(skill_id) > 0
    }
    print(f"COUNT|petskill_entries|{len(stack.petskill_runtime.skills)}")
    referenced_skill_entries = tuple(
        stack.petskill_runtime.skills[skill_id]
        for skill_id in sorted(report_referenced_skill_ids)
    )
    basic_ai_callbacks = {
        "PETSKILL_None",
        "PETSKILL_NormalAttack",
        "PETSKILL_NormalGuard",
    }
    print(
        "COUNT|enemybase_referenced_petskill_ids|"
        f"{len(report_referenced_skill_ids)}"
    )
    print(
        "COUNT|enemybase_referenced_common_petskill_ids|"
        f"{sum(1 for entry in referenced_skill_entries if entry.stable_common_callback)}"
    )
    print(
        "COUNT|enemybase_referenced_basic_ai_petskill_ids|"
        f"{sum(1 for entry in referenced_skill_entries if entry.function_name in basic_ai_callbacks)}"
    )
    all_skill_slot_ids = tuple(
        int(skill_id)
        for template in stack.enemybase_runtime.templates.values()
        for skill_id in (
            template.skill_slot_ids
            if template.skill_slot_ids
            else template.skill_ids
        )
        if int(skill_id) > 0
    )
    print(
        "COUNT|enemybase_positive_petskill_slot_uses|"
        f"{len(all_skill_slot_ids)}"
    )
    print(
        "COUNT|enemybase_basic_ai_petskill_slot_uses|"
        f"{sum(1 for skill_id in all_skill_slot_ids if stack.petskill_runtime.skills[skill_id].function_name in basic_ai_callbacks)}"
    )
    common_callbacks = sorted(
        {
            entry.function_name
            for entry in referenced_skill_entries
            if entry.stable_common_callback
        }
    )
    for callback in common_callbacks:
        callback_ids = {
            int(entry.skill_id)
            for entry in referenced_skill_entries
            if entry.function_name == callback
        }
        slot_uses = sum(
            1
            for skill_id in all_skill_slot_ids
            if int(skill_id) in callback_ids
        )
        ascii_ids = sum(
            1
            for skill_id in callback_ids
            if all(byte < 128 for byte in stack.petskill_runtime.skills[skill_id].option_bytes)
        )
        print(
            "PETSKILL_CALLBACK_COVERAGE|"
            f"callback={callback}|"
            f"unique_ids={len(callback_ids)}|"
            f"slot_uses={slot_uses}|"
            f"ascii_option_ids={ascii_ids}|"
            f"nonascii_option_ids={len(callback_ids)-ascii_ids}"
        )
    print(
        "COUNT|enemybase_unresolved_petskill_ids|"
        f"{len(stack.petskill_runtime.unresolved_skill_ids(report_referenced_skill_ids))}"
    )
    print(
        "COUNT|stable_referenced_enemybase_templates|"
        f"{len(report_referenced_template_ids)}"
    )
    print(
        "COUNT|stable_unresolved_enemybase_templates|"
        f"{len(report_unresolved_template_ids)}"
    )
    print(
        "ENEMYBASE_NAME_ENCODING_STATUS|"
        f"{stack.enemybase_runtime.name_encoding_status}"
    )
    print(f"COUNT|stable_encounter_areas|{len(stack.encounter_runtime.encounter_areas)}")
    print(
        "COUNT|stable_unresolved_positive_group_refs|"
        f"{len(stack.encounter_runtime.unresolved_positive_group_refs)}"
    )
    print(
        "COUNT|stable_affected_encounter_areas|"
        f"{len(stack.encounter_runtime.specimen_defect_area_indices)}"
    )
    print("ENCOUNTER_GROUP_RUNTIME_WITNESS|1")
    print("ENCOUNTER_VARIANT_RUNTIME_WITNESS|1")
    print("ENEMY_SPAWN_BIRTH_RUNTIME_WITNESS|1")
    print(
        "PROVENANCE_SEPARATION|historical_foundation="
        f"{profile.historical_foundation}|runtime_world={profile.runtime_world_profile}|"
        f"evidence_role={profile.runtime_world_evidence_role}"
    )
    print(OUTPUT_RESOLUTION)


if __name__ == "__main__":
    main()
