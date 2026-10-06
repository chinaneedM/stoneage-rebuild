#!/usr/bin/env python3
"""Bundle-backed smoke for the concrete recovered25 local runtime stack.

The preservation bundle is consumed transiently. Output contains aggregate
closure markers only; raw recovered coordinates, item ids, filenames,
arguments and dialogue are not emitted.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from types import MappingProxyType

from tools.stoneage_enemy_spawn_model import EnemyBirthRolls
from tools.stoneage_recovered25_battlemodel_runtime_probe import (
    verify_files as verify_battlemodel_files, verify_ai_files, run_recovered_ai_goldens, run_runtime_golden, run_identity_pressure,
)
from tools.stoneage_attack_magic_action_model import (
    AttackMagicTargetRolls,
    EnemyAttackMagicActionRolls,
)
from tools.stoneage_attack_magic_state_model import (
    AttackMagicResistanceRuntime,
    AttackMagicRoundOverlay,
)
from tools.stoneage_battle_round_model import (
    BATTLE_COM_S_ATTACK_MAGIC,
    BATTLE_COM_WAIT,
    BattleCombatProfile,
    BattleCommand,
)
from tools.stoneage_enemy_ai_model import (
    SKILL as ENEMY_AI_SKILL,
    EnemyAiTarget,
    parse_normal_enemy_ai_options,
    resolve_common_normal_enemy_ai,
)
from tools.stoneage_local_runtime_session_coordinator import (
    InMemoryLocalPersistenceStore,
    LocalRuntimeSessionCoordinator,
)
from tools.stoneage_player_growth_model import base_derived_stats

from tools.stoneage_local_runtime_core import (
    LocalRuntimeSessionState,
    WorldRegionRequest,
    decode_local_runtime_session,
    encode_local_runtime_session,
    load_runtime_bootstrap_file,
)
from tools.stoneage_player_creation_model import build_creation_state
from tools.stoneage_petskill_core_model import (
    abduct_ai_threshold,
    parse_status_skill,
)
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


def _battle_ready_player_state() -> PersistentPlayerState:
    fields=build_creation_state(5,5,5,5,5,5,0,0)
    derived=base_derived_stats(
        int(fields["vital"]),
        int(fields["strength"]),
        int(fields["toughness"]),
        int(fields["dexterity"]),
    )
    fields.update({
        "name":"runtime-stack-attackmagic-witness",
        "hp":max(100000,int(derived["max_hp"])),
        "max_hp":max(100000,int(derived["max_hp"])),
        "attack":int(derived["attack_power"]),
        "defense":int(derived["defence_power"]),
        "quick":int(derived["quick"]),
    })
    return PersistentPlayerState(
        character=PlayerState(MappingProxyType(dict(fields)))
    )


def _first_weighted_roll(entries, wanted) -> int | None:
    cursor=0
    for value,raw_weight in entries:
        weight=max(0,int(raw_weight))
        if weight <= 0:
            continue
        if wanted(value):
            return cursor
        cursor+=weight
    return None


def _attack_magic_ai_mode_roll(options, skill_slot: int) -> int:
    skill_slot=int(skill_slot)
    if not 0 <= skill_slot < 7:
        raise ValueError("AttackMagic witness skill slot must be 0..6")
    weight=int(options.skill_weights[skill_slot])
    if weight <= 0:
        raise ValueError("AttackMagic witness skill slot has zero AI weight")
    return (
        int(options.attack_weight)
        + int(options.guard_weight)
        + int(options.magic_weight)
        + int(options.escape_weight)
        + sum(int(x) for x in options.skill_weights[:skill_slot])
    )


def _run_attack_magic_enemy_ai_witness(profile,stack):
    """Exercise one real recovered-data AI -> 2002 -> persistent-round path."""
    attack_skill_ids=set(int(x) for x in stack.attack_magic_runtime.entries)
    defect_areas=set(stack.encounter_runtime.specimen_defect_area_indices)
    chosen=None

    for area in stack.encounter_runtime.encounter_areas:
        if int(area.index) in defect_areas:
            continue
        try:
            eligible_groups=tuple(
                (group,int(weight))
                for group,weight in area.resolved_group_choices(
                    stack.encounter_runtime.groups,()
                )
                if int(weight)>0
            )
        except (KeyError,ValueError):
            continue
        for group,group_weight in eligible_groups:
            raw_enemy_slots=tuple(
                (int(enemy_id),int(weight))
                for enemy_id,weight in group.enemy_slots
                if (
                    int(enemy_id) in stack.encounter_runtime.enemies
                    and int(weight)>0
                )
            )
            for enemy_id,enemy_weight in raw_enemy_slots:
                variant=stack.encounter_runtime.enemies[enemy_id]
                if int(variant.tactics) != 1 or not str(variant.tactics_option):
                    continue
                template=stack.enemybase_runtime.templates.get(int(variant.tempno))
                if template is None:
                    continue
                slots=tuple(int(x) for x in template.skill_slot_ids)
                try:
                    options=parse_normal_enemy_ai_options(
                        str(variant.tactics_option)
                    )
                except ValueError:
                    continue
                if options.enemy_attack_ai_random_override is not None:
                    continue
                for skill_slot,skill_id in enumerate(slots):
                    if skill_id not in attack_skill_ids:
                        continue
                    if int(options.skill_weights[skill_slot]) <= 0:
                        continue
                    mode_roll=_attack_magic_ai_mode_roll(options,skill_slot)
                    decision=resolve_common_normal_enemy_ai(
                        str(variant.tactics_option),
                        (
                            EnemyAiTarget(
                                slot=0,
                                participant_id="player",
                                kind="player",
                                hp=100000,
                            ),
                        ),
                        mode_roll=mode_roll,
                        target_roll=0,
                    )
                    if (
                        decision is None
                        or decision.kind != ENEMY_AI_SKILL
                        or int(decision.skill_slot) != skill_slot
                        or int(decision.target_slot) != 0
                    ):
                        continue
                    group_roll=_first_weighted_roll(
                        eligible_groups,
                        lambda candidate: (
                            int(candidate.group_id)==int(group.group_id)
                        ),
                    )
                    selection_roll=_first_weighted_roll(
                        raw_enemy_slots,
                        lambda candidate: int(candidate)==int(enemy_id),
                    )
                    if group_roll is None or selection_roll is None:
                        continue
                    try:
                        footprint=stack.resolve_enemy_attack_magic_footprint(
                            skill_id=skill_id,
                            actor_slot=15,
                            target_slot=0,
                            alive_player_slots=(0,),
                        )
                    except (KeyError,ValueError):
                        continue
                    if (
                        not footprint.source_sort_portable
                        or footprint.source_target_order != (0,)
                    ):
                        continue
                    chosen=(
                        area,group,variant,template,skill_slot,skill_id,
                        int(group_roll),int(selection_roll),int(mode_roll),
                        footprint,
                    )
                    break
                if chosen is not None:
                    break
            if chosen is not None:
                break
        if chosen is not None:
            break

    if chosen is None:
        raise ValueError(
            "no executable recovered25 AttackMagic enemy-AI witness found"
        )

    (
        area,group,variant,template,skill_slot,skill_id,
        group_roll,selection_roll,mode_roll,footprint,
    )=chosen
    player_state=_battle_ready_player_state()
    session=LocalRuntimeSessionState(
        contract_id=profile.contract_id,
        world_profile=profile.runtime_world_profile,
        hometown_ordinal=1,
        player_position=MapPosition(
            int(area.floor),int(area.min_x),int(area.min_y)
        ),
        player_state=player_state,
        world_flags=frozenset({"attackmagic-preservation-witness"}),
    )
    requested=stack.request_encounter_group(
        session,group_roll=group_roll
    )
    if int(requested.group_id) != int(group.group_id):
        raise ValueError("AttackMagic witness group selection drift")

    coordinator=LocalRuntimeSessionCoordinator(
        stack=stack,
        persistence=InMemoryLocalPersistenceStore(),
    )
    context=coordinator.start_group_battle(
        session,
        requested,
        entry_count_roll=1,
        selection_rolls=(selection_roll,),
        birth_rolls=(
            EnemyBirthRolls(
                level_roll=0,
                birth_offsets=(0,0,0,0),
                spawn_allocation_rolls=(0,1,2,3,0,1,2,3,0,1),
            ),
        ),
    )
    if len(context.spawned_enemies) != 1:
        raise ValueError("AttackMagic witness did not spawn exactly one enemy")
    spawned=context.spawned_enemies[0]
    if int(spawned.variant.enemy_id) != int(variant.enemy_id):
        raise ValueError("AttackMagic witness enemy selection drift")
    enemy_id=str(spawned.participant.participant_id)

    overlay=AttackMagicRoundOverlay({
        "player":AttackMagicResistanceRuntime()
    })
    context=coordinator.begin_persistent_group_battle(
        context,
        slots={"player":0,enemy_id:15},
        attack_magic_overlay=overlay,
    )
    player_fields=player_state.character.fields
    profiles={
        "player":BattleCombatProfile(
            fixed_dex=max(0,int(player_fields["quick"])-20),
            fixed_luck=0,
            earth=int(player_fields["earth"]),
            water=int(player_fields["water"]),
            fire=int(player_fields["fire"]),
            wind=int(player_fields["wind"]),
        ),
        enemy_id:BattleCombatProfile(
            fixed_dex=max(0,int(spawned.participant.quick)-20),
            fixed_luck=0,
            earth=int(template.earth),
            water=int(template.water),
            fire=int(template.fire),
            wind=int(template.wind),
        ),
    }
    next_context,result=(
        coordinator
        .resolve_persistent_attack_guard_escape_wait_round_with_enemy_ai(
            context,
            player_side_commands={
                "player":BattleCommand(BATTLE_COM_WAIT),
            },
            enemy_mode_rolls={enemy_id:mode_roll},
            enemy_target_rolls={enemy_id:0},
            enemy_escape_rolls={},
            opponent_abio_by_participant_id={},
            initiative_random_subtracts={"player":0,enemy_id:0},
            profiles=profiles,
            attack_rolls={},
            defense_profile="newpower_70pct",
            attack_magic_rolls_by_attack_id={
                enemy_id:EnemyAttackMagicActionRolls(
                    0,{0:AttackMagicTargetRolls(100,0)}
                )
            },
        )
    )
    magic_events=tuple(
        event for event in result.round.events
        if (
            str(event.participant_id)==enemy_id
            and int(event.command1)==BATTLE_COM_S_ATTACK_MAGIC
        )
    )
    if len(magic_events) != 1:
        raise ValueError(
            "AttackMagic witness did not produce exactly one target event"
        )
    if magic_events[0].attack_magic_target_resolution is None:
        raise ValueError("AttackMagic witness lacks typed target resolution")
    if next_context.attack_magic_overlay != result.attack_magic_overlay_after:
        raise ValueError("AttackMagic witness overlay did not carry forward")
    if result.attack_magic_overlay_before != overlay:
        raise ValueError("AttackMagic witness overlay pre-state drift")

    return {
        "executed":1,
        "portable":int(bool(footprint.source_sort_portable)),
        "target_events":len(magic_events),
        "overlay_carried":1,
        "skill_slot":int(skill_slot),
        "round_turn":int(result.after.turn),
    }


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
    verify_battlemodel_files(server_data_dir, setup)
    verify_ai_files(server_data_dir, setup)
    battlemodel_goldens = run_runtime_golden(stack, position=seeds[1].position)
    run_recovered_ai_goldens(stack, position=seeds[1].position)
    battlemodel_rejections = run_identity_pressure(stack)
    if stack.attack_magic_runtime is None:
        raise ValueError("runtime stack lacks AttackMagic runtime index")
    if len(stack.attack_magic_runtime.entries) != 25:
        raise ValueError("unexpected recovered25 AttackMagic runtime count")
    attack_magic_ai_witness=_run_attack_magic_enemy_ai_witness(
        profile,stack
    )
    attack_magic_exact = stack.resolve_enemy_attack_magic_footprint(
        skill_id=stack.attack_magic_runtime.skill_id_for_magic(301),
        actor_slot=15,
        target_slot=0,
        alive_player_slots=tuple(range(10)),
    )
    if (
        attack_magic_exact.magic_id != 301
        or attack_magic_exact.source_target_order != (0,)
    ):
        raise ValueError("AttackMagic exact footprint witness drift")
    attack_magic_dynamic = stack.resolve_enemy_attack_magic_footprint(
        skill_id=stack.attack_magic_runtime.skill_id_for_magic(305),
        actor_slot=15,
        target_slot=0,
        alive_player_slots=(0,),
    )
    if (
        attack_magic_dynamic.magic_id != 305
        or attack_magic_dynamic.source_target_order != (0,)
    ):
        raise ValueError("AttackMagic dynamic portability witness drift")
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
        attack_magic_ai_witness,
        battlemodel_goldens,
        battlemodel_rejections,
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
        attack_magic_ai_witness,
        battlemodel_goldens,
        battlemodel_rejections,
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
    print(f"BATTLEMODEL_STACK_GOLDEN|cases={battlemodel_goldens}|templates=2|charsets=2|source_profiles=3")
    print(f"BATTLEMODEL_STACK_SELECTED_AI_CONTROL|cases={battlemodel_goldens}|controlled_tactics_option=1")
    print(f"BATTLEMODEL_STACK_IDENTITY_PRESSURE|rejections={battlemodel_rejections}")
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
    attack_magic_exact = stack.resolve_enemy_attack_magic_footprint(
        skill_id=stack.attack_magic_runtime.skill_id_for_magic(301),
        actor_slot=15,
        target_slot=0,
        alive_player_slots=tuple(range(10)),
    )
    attack_magic_dynamic = stack.resolve_enemy_attack_magic_footprint(
        skill_id=stack.attack_magic_runtime.skill_id_for_magic(305),
        actor_slot=15,
        target_slot=0,
        alive_player_slots=(0,),
    )
    print(
        f"COUNT|attackmagic_entries|{len(stack.attack_magic_runtime.entries)}"
    )
    print(
        "ATTACKMAGIC_NONPLAYER_ITEM_RUNTIME_ROLE|"
        f"{stack.attack_magic_runtime.nonplayer_item_role}"
    )
    print(
        "ATTACKMAGIC_EXACT_FOOTPRINT_WITNESS|"
        f"magic={attack_magic_exact.magic_id}|"
        f"targets={len(attack_magic_exact.target_membership)}|"
        f"portable={int(attack_magic_exact.source_sort_portable)}"
    )
    print(
        "ATTACKMAGIC_DYNAMIC_PORTABILITY_WITNESS|"
        f"magic={attack_magic_dynamic.magic_id}|alive=1|"
        f"targets={len(attack_magic_dynamic.target_membership)}|"
        f"portable={int(attack_magic_dynamic.source_sort_portable)}"
    )
    print(
        "ATTACKMAGIC_ENEMY_AI_ROUND_WITNESS|"
        f"{attack_magic_ai_witness['executed']}|"
        f"portable={attack_magic_ai_witness['portable']}|"
        f"target_events={attack_magic_ai_witness['target_events']}|"
        f"overlay_carried={attack_magic_ai_witness['overlay_carried']}|"
        f"round_turn={attack_magic_ai_witness['round_turn']}"
    )
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
        dual_same = 0
        dual_divergent = 0
        dual_decode_error = 0
        for skill_id in callback_ids:
            option_bytes = stack.petskill_runtime.skills[skill_id].option_bytes
            try:
                cp950_text = option_bytes.decode("cp950", "strict")
                big5_text = option_bytes.decode("big5", "strict")
            except UnicodeDecodeError:
                dual_decode_error += 1
                continue
            if cp950_text == big5_text:
                dual_same += 1
            else:
                dual_divergent += 1
        print(
            "PETSKILL_CALLBACK_COVERAGE|"
            f"callback={callback}|"
            f"unique_ids={len(callback_ids)}|"
            f"slot_uses={slot_uses}|"
            f"ascii_option_ids={ascii_ids}|"
            f"nonascii_option_ids={len(callback_ids)-ascii_ids}|"
            f"cp950_big5_same_ids={dual_same}|"
            f"cp950_big5_divergent_ids={dual_divergent}|"
            f"cp950_big5_decode_error_ids={dual_decode_error}"
        )
    noncommon_entries = tuple(
        entry
        for entry in referenced_skill_entries
        if not entry.stable_common_callback
    )
    noncommon_ids = {
        int(entry.skill_id)
        for entry in noncommon_entries
    }
    noncommon_slot_uses = sum(
        1
        for skill_id in all_skill_slot_ids
        if int(skill_id) in noncommon_ids
    )
    print(
        "COUNT|enemybase_referenced_noncommon_petskill_ids|"
        f"{len(noncommon_ids)}"
    )
    print(
        "COUNT|enemybase_noncommon_petskill_slot_uses|"
        f"{noncommon_slot_uses}"
    )
    noncommon_callbacks = sorted(
        {
            entry.function_name
            for entry in noncommon_entries
        }
    )
    for callback in noncommon_callbacks:
        callback_ids = {
            int(entry.skill_id)
            for entry in noncommon_entries
            if entry.function_name == callback
        }
        slot_uses = sum(
            1
            for skill_id in all_skill_slot_ids
            if int(skill_id) in callback_ids
        )
        field_all = sum(
            int(stack.petskill_runtime.skills[skill_id].field == 0)
            for skill_id in callback_ids
        )
        field_battle = sum(
            int(stack.petskill_runtime.skills[skill_id].field == 1)
            for skill_id in callback_ids
        )
        field_map = sum(
            int(stack.petskill_runtime.skills[skill_id].field == 2)
            for skill_id in callback_ids
        )
        field_other = len(callback_ids) - field_all - field_battle - field_map
        illegal_ids = sum(
            int(stack.petskill_runtime.skills[skill_id].illegal != 0)
            for skill_id in callback_ids
        )
        ascii_ids = sum(
            int(stack.petskill_runtime.skills[skill_id].option_bytes.isascii())
            for skill_id in callback_ids
        )
        dual_same = 0
        dual_divergent = 0
        dual_decode_error = 0
        for skill_id in callback_ids:
            option_bytes = stack.petskill_runtime.skills[skill_id].option_bytes
            try:
                cp950_text = option_bytes.decode("cp950", "strict")
                big5_text = option_bytes.decode("big5", "strict")
            except UnicodeDecodeError:
                dual_decode_error += 1
                continue
            if cp950_text == big5_text:
                dual_same += 1
            else:
                dual_divergent += 1
        print(
            "PETSKILL_NONCOMMON_CALLBACK_COVERAGE|"
            f"callback={callback}|"
            f"unique_ids={len(callback_ids)}|"
            f"slot_uses={slot_uses}|"
            f"field_all_ids={field_all}|"
            f"field_battle_ids={field_battle}|"
            f"field_map_ids={field_map}|"
            f"field_other_ids={field_other}|"
            f"illegal_ids={illegal_ids}|"
            f"ascii_option_ids={ascii_ids}|"
            f"nonascii_option_ids={len(callback_ids)-ascii_ids}|"
            f"cp950_big5_same_ids={dual_same}|"
            f"cp950_big5_divergent_ids={dual_divergent}|"
            f"cp950_big5_decode_error_ids={dual_decode_error}"
        )
    attackmagic_entries = tuple(
        entry
        for entry in noncommon_entries
        if entry.function_name == "PETSKILL_AttackMagic"
    )
    attackmagic_magic_markers = 0
    attackmagic_magic_numeric = []
    attackmagic_item_after_magic = 0
    attackmagic_item_numeric = []
    attackmagic_item_before_magic = 0
    attackmagic_pairs = []
    for entry in attackmagic_entries:
        option_text = entry.ascii_option()
        magic_pos = option_text.find("magic")
        if magic_pos >= 0:
            attackmagic_magic_markers += 1
            magic_tail = option_text[magic_pos + len("magic") + 1 :]
            match = re.match(r"\s*([+-]?\d+)", magic_tail)
            if match is not None:
                attackmagic_magic_numeric.append(int(match.group(1)))
            item_pos = option_text.find(
                "item",
                magic_pos + len("magic") + 1,
            )
            if item_pos >= 0:
                attackmagic_item_after_magic += 1
                item_tail = option_text[item_pos + len("item") + 1 :]
                match = re.match(r"\s*([+-]?\d+)", item_tail)
                if match is not None:
                    item_value = int(match.group(1))
                    attackmagic_item_numeric.append(item_value)
                    if len(attackmagic_magic_numeric) > 0:
                        attackmagic_pairs.append(
                            (attackmagic_magic_numeric[-1], item_value)
                        )
            pre_item = option_text.find("item", 0, magic_pos)
            if pre_item >= 0:
                attackmagic_item_before_magic += 1
        elif "item" in option_text:
            attackmagic_item_before_magic += 1
    if len(attackmagic_entries) != 25:
        raise ValueError(
            "recovered25 AttackMagic callback population drifted from 25 IDs"
        )
    attackmagic_pair_deltas = [
        int(item_value) - int(magic_value)
        for magic_value, item_value in attackmagic_pairs
    ]
    print(
        "PETSKILL_ATTACKMAGIC_PARSE|"
        f"unique_ids={len(attackmagic_entries)}|"
        f"magic_marker_ids={attackmagic_magic_markers}|"
        f"magic_numeric_ids={len(attackmagic_magic_numeric)}|"
        f"item_after_magic_ids={attackmagic_item_after_magic}|"
        f"item_numeric_ids={len(attackmagic_item_numeric)}|"
        f"item_before_magic_ids={attackmagic_item_before_magic}|"
        f"magic_min={min(attackmagic_magic_numeric) if attackmagic_magic_numeric else 'NONE'}|"
        f"magic_max={max(attackmagic_magic_numeric) if attackmagic_magic_numeric else 'NONE'}|"
        f"magic_distinct={len(set(attackmagic_magic_numeric))}|"
        f"item_min={min(attackmagic_item_numeric) if attackmagic_item_numeric else 'NONE'}|"
        f"item_max={max(attackmagic_item_numeric) if attackmagic_item_numeric else 'NONE'}|"
        f"item_distinct={len(set(attackmagic_item_numeric))}|"
        f"pair_numeric_ids={len(attackmagic_pairs)}|"
        f"pair_delta_min={min(attackmagic_pair_deltas) if attackmagic_pair_deltas else 'NONE'}|"
        f"pair_delta_max={max(attackmagic_pair_deltas) if attackmagic_pair_deltas else 'NONE'}|"
        f"pair_delta_distinct={len(set(attackmagic_pair_deltas))}"
    )
    status_entries = tuple(
        entry
        for entry in referenced_skill_entries
        if entry.function_name == "PETSKILL_StatusChange"
    )
    status_matched = 0
    status_turns = []
    status_attack_mod = 0
    status_defense_mod = 0
    for entry in status_entries:
        option_text = entry.unambiguous_cp950_big5_option()
        parsed = parse_status_skill(
            option_text,
            ("全", "毒", "麻", "眠", "石", "醉", "亂"),
        )
        if not parsed["matched"]:
            # One pinned descendant source normalizes the confusion glyph to
            # the simplified form; accept it only as the same index-6 token.
            parsed = parse_status_skill(
                option_text,
                ("全", "毒", "麻", "眠", "石", "醉", "乱"),
            )
        if parsed["matched"]:
            status_matched += 1
        status_turns.append(int(parsed["turn"]))
        if parsed["attack_percent"] is not None:
            status_attack_mod += 1
        if parsed["defense_percent"] is not None:
            status_defense_mod += 1
    if status_matched != len(status_entries):
        raise ValueError(
            "recovered25 StatusChange OPTION grammar is not fully closed"
        )
    print(
        "PETSKILL_STATUSCHANGE_PARSE|"
        f"unique_ids={len(status_entries)}|"
        f"matched_status_ids={status_matched}|"
        f"turn_min={min(status_turns) if status_turns else -1}|"
        f"turn_max={max(status_turns) if status_turns else -1}|"
        f"attack_modifier_ids={status_attack_mod}|"
        f"defense_modifier_ids={status_defense_mod}"
    )
    powerbalance_entries = tuple(
        entry
        for entry in referenced_skill_entries
        if entry.function_name == "PETSKILL_PowerBalance"
    )
    powerbalance_attack = 0
    powerbalance_defense = 0
    powerbalance_dex_extension = 0
    for entry in powerbalance_entries:
        option_text = entry.unambiguous_cp950_big5_option()
        powerbalance_attack += int("攻%" in option_text)
        powerbalance_defense += int("防%" in option_text)
        powerbalance_dex_extension += int("敏%" in option_text)
    print(
        "PETSKILL_POWERBALANCE_MARKERS|"
        f"unique_ids={len(powerbalance_entries)}|"
        f"attack_marker_ids={powerbalance_attack}|"
        f"defense_marker_ids={powerbalance_defense}|"
        f"dex_extension_marker_ids={powerbalance_dex_extension}"
    )
    mighty_entries = tuple(
        entry
        for entry in referenced_skill_entries
        if entry.function_name == "PETSKILL_Mighty"
    )
    mighty_multiplier = 0
    mighty_dodge = 0
    mighty_numeric_parse = 0
    for entry in mighty_entries:
        option_text = entry.unambiguous_cp950_big5_option()
        multiplier_match = re.search(
            r"倍\s*[+-]?(?:\d+(?:\.\d*)?|\.\d+)",
            option_text,
        )
        dodge_match = re.search(r"避\s*[+-]?\d+", option_text)
        mighty_multiplier += int("倍" in option_text)
        mighty_dodge += int("避" in option_text)
        mighty_numeric_parse += int(
            multiplier_match is not None and dodge_match is not None
        )
    if (
        mighty_multiplier != len(mighty_entries)
        or mighty_dodge != len(mighty_entries)
        or mighty_numeric_parse != len(mighty_entries)
    ):
        raise ValueError(
            "recovered25 Mighty OPTION marker/numeric grammar is not fully closed"
        )
    print(
        "PETSKILL_MIGHTY_MARKERS|"
        f"unique_ids={len(mighty_entries)}|"
        f"multiplier_marker_ids={mighty_multiplier}|"
        f"dodge_marker_ids={mighty_dodge}|"
        f"numeric_parse_ids={mighty_numeric_parse}"
    )
    guardian_entries = tuple(
        entry
        for entry in referenced_skill_entries
        if entry.function_name == "PETSKILL_Guardian"
    )
    guardian_attack_marker=0
    guardian_defense_marker=0
    guardian_defensive_com=0
    guardian_attack_values=[]
    guardian_defense_values=[]
    for entry in guardian_entries:
        option_text=entry.unambiguous_cp950_big5_option()
        attack=re.search(
            r"攻%\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+))",
            option_text,
        )
        defense=re.search(
            r"防%\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+))",
            option_text,
        )
        guardian_attack_marker += int("攻%" in option_text)
        guardian_defense_marker += int("防%" in option_text)
        marker_index=option_text.find("COM:")
        guardian_defensive_com += int(
            marker_index >= 0
            and "防御" in option_text[marker_index+4:]
        )
        if attack is not None:
            guardian_attack_values.append(float(attack.group(1)))
        if defense is not None:
            guardian_defense_values.append(float(defense.group(1)))
    if (
        len(guardian_entries) != 1
        or guardian_attack_marker != 1
        or guardian_defense_marker != 0
        or guardian_defensive_com != 0
        or guardian_attack_values != [-20.0]
        or guardian_defense_values
    ):
        raise ValueError(
            "recovered25 Guardian OPTION drifted outside closed attack-mode "
            "攻%-20 subset"
        )
    print(
        "PETSKILL_GUARDIAN_PARSE|"
        f"unique_ids={len(guardian_entries)}|"
        f"attack_marker_ids={guardian_attack_marker}|"
        f"defense_marker_ids={guardian_defense_marker}|"
        f"defensive_com_ids={guardian_defensive_com}|"
        f"attack_numeric_ids={len(guardian_attack_values)}|"
        f"defense_numeric_ids={len(guardian_defense_values)}|"
        f"attack_min={min(guardian_attack_values) if guardian_attack_values else 'NONE'}|"
        f"attack_max={max(guardian_attack_values) if guardian_attack_values else 'NONE'}|"
        f"defense_min={min(guardian_defense_values) if guardian_defense_values else 'NONE'}|"
        f"defense_max={max(guardian_defense_values) if guardian_defense_values else 'NONE'}"
    )

    steal_entries = tuple(
        entry
        for entry in referenced_skill_entries
        if entry.function_name == "PETSKILL_Steal"
    )
    steal_ascii_ids=sum(
        int(entry.option_bytes.isascii())
        for entry in steal_entries
    )
    if len(steal_entries) != 1 or steal_ascii_ids != 1:
        raise ValueError(
            "recovered25 Steal callback/OPTION population drifted"
        )
    print(
        "PETSKILL_STEAL_PARSE|"
        f"unique_ids={len(steal_entries)}|"
        f"ascii_ids={steal_ascii_ids}"
    )

    earthround_entries = tuple(
        entry
        for entry in referenced_skill_entries
        if entry.function_name == "PETSKILL_EarthRound"
    )
    earthround_attack_marker = 0
    earthround_attack_numeric = 0
    earthround_attack_percents = []
    for entry in earthround_entries:
        option_text = entry.unambiguous_cp950_big5_option()
        attack = re.search(r"攻%\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+))", option_text)
        earthround_attack_marker += int("攻%" in option_text)
        if attack is not None:
            earthround_attack_numeric += 1
            earthround_attack_percents.append(float(attack.group(1)))
    if (
        len(earthround_entries) != 1
        or earthround_attack_marker != 1
        or earthround_attack_numeric != 1
        or earthround_attack_percents != [90.0]
    ):
        raise ValueError(
            "recovered25 EarthRound OPTION drifted outside closed 攻%90 subset"
        )
    print(
        "PETSKILL_EARTHROUND_PARSE|"
        f"unique_ids={len(earthround_entries)}|"
        f"attack_marker_ids={earthround_attack_marker}|"
        f"attack_numeric_ids={earthround_attack_numeric}|"
        f"attack_percent_min={min(earthround_attack_percents) if earthround_attack_percents else 'NONE'}|"
        f"attack_percent_max={max(earthround_attack_percents) if earthround_attack_percents else 'NONE'}"
    )
    guardbreak_entries = tuple(
        entry
        for entry in referenced_skill_entries
        if entry.function_name == "PETSKILL_GuardBreak"
    )
    guardbreak_ascii = 0
    guardbreak_attack_marker = 0
    for entry in guardbreak_entries:
        guardbreak_ascii += int(entry.option_bytes.isascii())
        if entry.option_bytes.isascii():
            option_text = entry.option_bytes.decode("ascii")
            guardbreak_attack_marker += int("攻%" in option_text)
    if (
        len(guardbreak_entries) != 1
        or guardbreak_ascii != len(guardbreak_entries)
        or guardbreak_attack_marker != 0
    ):
        raise ValueError(
            "recovered25 GuardBreak OPTION is outside closed ASCII/no-attack-marker subset"
        )
    print(
        "PETSKILL_GUARDBREAK_OPTION|"
        f"unique_ids={len(guardbreak_entries)}|"
        f"ascii_ids={guardbreak_ascii}|"
        f"attack_marker_ids={guardbreak_attack_marker}"
    )
    charge_entries = tuple(
        entry
        for entry in referenced_skill_entries
        if entry.function_name == "PETSKILL_ChargeAttack"
    )
    charge_leading_int = 0
    charge_in_range = 0
    charge_attack_marker = 0
    charge_attack_numeric = 0
    charge_counts = []
    charge_attack_percents = []
    for entry in charge_entries:
        option_text = entry.unambiguous_cp950_big5_option()
        leading = re.match(r"\s*([+-]?\d+)", option_text)
        attack = re.search(r"攻%\s*([+-]?\d+)", option_text)
        if leading is not None:
            charge_leading_int += 1
            count = int(leading.group(1))
            charge_counts.append(count)
            charge_in_range += int(1 <= count <= 10)
        charge_attack_marker += int("攻%" in option_text)
        if attack is not None:
            charge_attack_numeric += 1
            charge_attack_percents.append(int(attack.group(1)))
    if (
        len(charge_entries) != 3
        or charge_leading_int != 3
        or charge_in_range != 3
        or charge_attack_marker != 3
        or charge_attack_numeric != 3
        or min(charge_counts, default=-1) != 1
        or max(charge_counts, default=-1) != 3
        or min(charge_attack_percents, default=-1) != 90
        or max(charge_attack_percents, default=-1) != 150
    ):
        raise ValueError(
            "recovered25 ChargeAttack OPTION grammar drifted outside "
            "closed 3-ID wait/attack-percent subset"
        )
    print(
        "PETSKILL_CHARGEATTACK_PARSE|"
        f"unique_ids={len(charge_entries)}|"
        f"leading_int_ids={charge_leading_int}|"
        f"in_range_count_ids={charge_in_range}|"
        f"attack_marker_ids={charge_attack_marker}|"
        f"attack_numeric_ids={charge_attack_numeric}|"
        f"count_min={min(charge_counts) if charge_counts else -1}|"
        f"count_max={max(charge_counts) if charge_counts else -1}|"
        f"attack_percent_min={min(charge_attack_percents) if charge_attack_percents else -1}|"
        f"attack_percent_max={max(charge_attack_percents) if charge_attack_percents else -1}"
    )
    continuation_entries = tuple(
        entry
        for entry in referenced_skill_entries
        if entry.function_name == "PETSKILL_ContinuationAttack"
    )
    continuation_ascii = 0
    continuation_leading_int = 0
    continuation_in_range = 0
    continuation_counts = []
    for entry in continuation_entries:
        continuation_ascii += int(entry.option_bytes.isascii())
        option_text = entry.option_bytes.decode("ascii")
        leading = re.match(r"\s*([+-]?\d+)", option_text)
        if leading is not None:
            continuation_leading_int += 1
            count = int(leading.group(1))
            continuation_counts.append(count)
            continuation_in_range += int(1 <= count <= 10)
    if (
        len(continuation_entries) != 4
        or continuation_ascii != 4
        or continuation_leading_int != 4
        or continuation_in_range != 4
        or min(continuation_counts, default=-1) != 2
        or max(continuation_counts, default=-1) != 5
        or len(set(continuation_counts)) != 4
    ):
        raise ValueError(
            "recovered25 ContinuationAttack OPTION grammar drifted outside "
            "closed four-ID ASCII count subset"
        )
    print(
        "PETSKILL_CONTINUATIONATTACK_PARSE|"
        f"unique_ids={len(continuation_entries)}|"
        f"ascii_ids={continuation_ascii}|"
        f"leading_int_ids={continuation_leading_int}|"
        f"in_range_count_ids={continuation_in_range}|"
        f"count_min={min(continuation_counts) if continuation_counts else -1}|"
        f"count_max={max(continuation_counts) if continuation_counts else -1}|"
        f"distinct_count={len(set(continuation_counts))}"
    )
    abduct_entries = tuple(
        entry
        for entry in referenced_skill_entries
        if entry.function_name == "PETSKILL_Abduct"
    )
    abduct_ascii = 0
    abduct_leading_int = 0
    abduct_positive_ai = 0
    abduct_ai_values = []
    for entry in abduct_entries:
        abduct_ascii += int(entry.option_bytes.isascii())
        if not entry.option_bytes.isascii():
            continue
        option_text = entry.option_bytes.decode("ascii")
        leading = re.match(r"\s*([+-]?\d+)", option_text)
        abduct_leading_int += int(leading is not None)
        value = int(abduct_ai_threshold(option_text))
        abduct_ai_values.append(value)
        abduct_positive_ai += int(value > 0)
    print(
        "PETSKILL_ABDUCT_PARSE|"
        f"unique_ids={len(abduct_entries)}|"
        f"ascii_ids={abduct_ascii}|"
        f"leading_int_ids={abduct_leading_int}|"
        f"positive_ai_ids={abduct_positive_ai}|"
        f"ai_min={min(abduct_ai_values) if abduct_ai_values else -1}|"
        f"ai_max={max(abduct_ai_values) if abduct_ai_values else -1}|"
        f"distinct_ai={len(set(abduct_ai_values))}"
    )
    merge_entries = tuple(
        entry
        for entry in referenced_skill_entries
        if entry.function_name == "PETSKILL_Merge"
    )
    merge_field_all = sum(int(entry.field == 0) for entry in merge_entries)
    merge_field_battle = sum(int(entry.field == 1) for entry in merge_entries)
    merge_field_map = sum(int(entry.field == 2) for entry in merge_entries)
    merge_field_other = sum(
        int(entry.field not in {0, 1, 2}) for entry in merge_entries
    )
    merge_illegal = sum(int(entry.illegal != 0) for entry in merge_entries)
    merge_ascii = sum(int(entry.option_bytes.isascii()) for entry in merge_entries)
    merge_empty_option = sum(
        int(len(entry.option_bytes) == 0) for entry in merge_entries
    )
    if (
        len(merge_entries) != 2
        or merge_field_all != 0
        or merge_field_battle != 0
        or merge_field_map != 2
        or merge_field_other != 0
        or merge_illegal != 2
        or merge_ascii != 2
        or merge_empty_option != 2
    ):
        raise ValueError(
            "recovered25 Merge rows drifted outside closed "
            "MAP/ILLEGAL/ASCII/empty-OPTION subset"
        )
    print(
        "PETSKILL_MERGE_PARSE|"
        f"unique_ids={len(merge_entries)}|"
        f"field_all_ids={merge_field_all}|"
        f"field_battle_ids={merge_field_battle}|"
        f"field_map_ids={merge_field_map}|"
        f"field_other_ids={merge_field_other}|"
        f"illegal_ids={merge_illegal}|"
        f"ascii_ids={merge_ascii}|"
        f"empty_option_ids={merge_empty_option}"
    )
    noguard_entries = tuple(
        entry
        for entry in referenced_skill_entries
        if entry.function_name == "PETSKILL_NoGuard"
    )
    noguard_dodge_marker = 0
    noguard_dodge_numeric = 0
    noguard_counter_simplified_marker = 0
    noguard_counter_traditional_marker = 0
    noguard_counter_numeric = 0
    noguard_critical_marker = 0
    noguard_critical_numeric = 0
    noguard_dodge_values = []
    noguard_counter_values = []
    noguard_critical_values = []
    for entry in noguard_entries:
        option_text = entry.unambiguous_cp950_big5_option()
        dodge = re.search(r"避%\s*([+-]?\d+)", option_text)
        counter = re.search(r"(?:击|擊)%\s*([+-]?\d+)", option_text)
        critical = re.search(r"心%\s*([+-]?\d+)", option_text)
        noguard_dodge_marker += int("避%" in option_text)
        noguard_counter_simplified_marker += int("击%" in option_text)
        noguard_counter_traditional_marker += int("擊%" in option_text)
        noguard_critical_marker += int("心%" in option_text)
        if dodge is not None:
            noguard_dodge_numeric += 1
            noguard_dodge_values.append(int(dodge.group(1)))
        if counter is not None:
            noguard_counter_numeric += 1
            noguard_counter_values.append(int(counter.group(1)))
        if critical is not None:
            noguard_critical_numeric += 1
            noguard_critical_values.append(int(critical.group(1)))
    if (
        len(noguard_entries) != 3
        or noguard_dodge_marker != 3
        or noguard_dodge_numeric != 3
        or noguard_counter_simplified_marker != 0
        or noguard_counter_traditional_marker != 3
        or noguard_counter_numeric != 3
        or noguard_critical_marker != 3
        or noguard_critical_numeric != 3
        or min(noguard_dodge_values, default=-1) != 30
        or max(noguard_dodge_values, default=-1) != 50
        or min(noguard_counter_values, default=-1) != 50
        or max(noguard_counter_values, default=-1) != 70
        or min(noguard_critical_values, default=-1) != 20
        or max(noguard_critical_values, default=-1) != 40
    ):
        raise ValueError(
            "recovered25 NoGuard OPTION grammar drifted outside closed "
            "traditional dodge/counter/critical subset"
        )
    print(
        "PETSKILL_NOGUARD_PARSE|"
        f"unique_ids={len(noguard_entries)}|"
        f"dodge_marker_ids={noguard_dodge_marker}|"
        f"dodge_numeric_ids={noguard_dodge_numeric}|"
        f"counter_simplified_marker_ids={noguard_counter_simplified_marker}|"
        f"counter_traditional_marker_ids={noguard_counter_traditional_marker}|"
        f"counter_numeric_ids={noguard_counter_numeric}|"
        f"critical_marker_ids={noguard_critical_marker}|"
        f"critical_numeric_ids={noguard_critical_numeric}|"
        f"dodge_min={min(noguard_dodge_values) if noguard_dodge_values else -1}|"
        f"dodge_max={max(noguard_dodge_values) if noguard_dodge_values else -1}|"
        f"counter_min={min(noguard_counter_values) if noguard_counter_values else -1}|"
        f"counter_max={max(noguard_counter_values) if noguard_counter_values else -1}|"
        f"critical_min={min(noguard_critical_values) if noguard_critical_values else -1}|"
        f"critical_max={max(noguard_critical_values) if noguard_critical_values else -1}"
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
