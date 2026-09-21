#!/usr/bin/env python3
"""Minimal end-to-end in-process historical simulation slice.

This composes the already validated world, encounter and battle boundaries.
It intentionally leaves collision verdicts, RNG rolls, enemy birth rolls,
commands, AI and battle outcomes as explicit inputs.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from types import MappingProxyType
from typing import Mapping, Sequence

from tools.stoneage_encounter_frequency_model import (
    EncounterFrequencyDecision,
    EncounterFrequencyState,
    refresh_frequency_bounds,
    resolve_frequency_step,
)
from tools.stoneage_map_collision_model import (
    CollisionProfile,
    DynamicOccupant,
    StaticCollisionMap,
    ordinary_step_allowed,
)
from tools.stoneage_battle_core_model import (
    BattleCaptureInputs,
    BattleDropSettlement,
    DropAllocationRoll,
    settle_player_battle_drops,
)
from tools.stoneage_battle_command_model import (
    BattleRoundAction,
    parse_player_battle_command,
    prepare_player_round_action,
)
from tools.stoneage_battle_round_model import (
    BattleCombatProfile,
    BattleCommand,
    OrdinaryAttackRolls,
    OrdinaryCaptureContext,
    OrdinaryCaptureRolls,
    OrdinaryEscapeContext,
    OrdinaryEscapeRolls,
    ResolvedOrdinaryRound,
    prepare_battle_round,
    resolve_ordinary_round,
)
from tools.stoneage_battle_state_model import (
    FINISHED,
    PLAYER_ESCAPE,
    PersistentBattleState,
    PersistentCaptureResult,
    PersistentRoundResult,
    begin_persistent_battle,
    resolve_persistent_capture_transition,
    resolve_persistent_ordinary_round,
)
from tools.stoneage_enemy_spawn_model import (
    EnemyBirthRolls,
    SpawnedEnemy,
    materialize_spawn_plan,
    plan_enemy_spawns,
)
from tools.stoneage_combat_profile_bridge import group_battle_combat_profiles
from tools.stoneage_pet_growth_model import (
    PetLevelGrowthRolls,
    adjust_pet_variable_ai,
    resolve_pet_exp_growth_transition,
    unpack_growth_base,
)
from tools.stoneage_player_growth_model import (
    base_derived_stats,
    resolve_player_exp_transition,
)
from tools.stoneage_singleplayer_battle import (
    BattleOutcome,
    BattleParticipant,
    BattleReturn,
    BattleSession,
    apply_battle_outcome,
    begin_battle,
    begin_group_battle,
)
from tools.stoneage_singleplayer_domain import (
    EncounterRequest,
    EncounterRolls,
    GroupEncounterRequest,
    InventoryItem,
    InventorySlot,
    ItemTemplateId,
    MapPosition,
    PetActor,
    PetGrowthState,
    PetSlot,
    SinglePlayerHistoricalDomain,
)
from tools.stoneage_tw10_25_bridge_model import PetTemplateBridge, ReconstructedPetBridgeState
from tools.stoneage_tw10_25_encounter_bridge import active_encounter_area
from tools.stoneage_singleplayer_world import (
    HistoricalWorldTopology,
    WalkResolution,
    resolve_player_walk,
)


@dataclass(frozen=True)
class HistoricalRuntimeStep:
    tick_index: int
    walk: WalkResolution
    encounter: EncounterRequest | None
    frequency: EncounterFrequencyDecision | None = None
    group_encounter: GroupEncounterRequest | None = None


@dataclass
class SinglePlayerHistoricalRuntime:
    domain: SinglePlayerHistoricalDomain
    topology: HistoricalWorldTopology
    tick_index: int = 0
    encounter_frequency: EncounterFrequencyState = field(
        default_factory=EncounterFrequencyState
    )

    def walk_step(
        self,
        *,
        destination: MapPosition,
        entry_allowed: bool,
        encounter_rolls: EncounterRolls | None = None,
        action_is_walk: bool = True,
        map_objmove_ok: bool = True,
    ) -> HistoricalRuntimeStep:
        walk = resolve_player_walk(
            self.domain,
            self.topology,
            destination=destination,
            entry_allowed=entry_allowed,
            action_is_walk=action_is_walk,
            map_objmove_ok=map_objmove_ok,
        )
        self.tick_index += 1

        encounter = None
        group_encounter = None
        if (
            walk.moved
            and not walk.encounter_suppressed
            and encounter_rolls is not None
        ):
            group_encounter = self.domain.request_encounter_group(
                group_roll=encounter_rolls.group_roll,
            )
            encounter = self.domain.request_encounter(
                group_roll=encounter_rolls.group_roll,
                enemy_roll=encounter_rolls.enemy_roll,
                level_roll=encounter_rolls.level_roll,
            )

        return HistoricalRuntimeStep(
            tick_index=self.tick_index,
            walk=walk,
            encounter=encounter,
            group_encounter=group_encounter,
        )

    def walk_step_with_frequency(
        self,
        *,
        destination: MapPosition,
        entry_allowed: bool,
        frequency_roll: int,
        encounter_rolls: EncounterRolls,
        action_is_walk: bool = True,
        map_objmove_ok: bool = True,
    ) -> HistoricalRuntimeStep:
        walk = resolve_player_walk(
            self.domain,
            self.topology,
            destination=destination,
            entry_allowed=entry_allowed,
            action_is_walk=action_is_walk,
            map_objmove_ok=map_objmove_ok,
        )
        self.tick_index += 1

        if not walk.moved:
            return HistoricalRuntimeStep(
                tick_index=self.tick_index,
                walk=walk,
                encounter=None,
                frequency=None,
            )

        # Stable descendant CHAR_walk refreshes encounter bounds from the
        # departure coordinate after the move callbacks have run.
        source_area = active_encounter_area(
            self.domain.static.encounter_areas,
            floor=walk.previous_position.floor_id,
            x=walk.previous_position.x,
            y=walk.previous_position.y,
        )
        refreshed = refresh_frequency_bounds(
            self.encounter_frequency,
            source_area,
        )
        frequency = resolve_frequency_step(
            refreshed,
            roll=frequency_roll,
            encounter_enabled=not walk.encounter_suppressed,
            eligible=True,
        )
        self.encounter_frequency = frequency.after

        encounter = None
        group_encounter = None
        if frequency.encounter_triggered:
            group_encounter = self.domain.request_encounter_group(
                group_roll=encounter_rolls.group_roll,
            )
            encounter = self.domain.request_encounter(
                group_roll=encounter_rolls.group_roll,
                enemy_roll=encounter_rolls.enemy_roll,
                level_roll=encounter_rolls.level_roll,
            )

        return HistoricalRuntimeStep(
            tick_index=self.tick_index,
            walk=walk,
            encounter=encounter,
            frequency=frequency,
            group_encounter=group_encounter,
        )

    def walk_step_with_collision(
        self,
        *,
        collision_map: StaticCollisionMap,
        collision_profile: CollisionProfile,
        destination: MapPosition,
        destination_occupants: Sequence[DynamicOccupant] = (),
        is_flying: bool = False,
        encounter_rolls: EncounterRolls | None = None,
        action_is_walk: bool = True,
        map_objmove_ok: bool = True,
    ) -> HistoricalRuntimeStep:
        current = self.domain.world.player_position
        if current is None:
            raise ValueError("player position is required before collision resolution")
        decision = ordinary_step_allowed(
            collision_map,
            collision_profile,
            origin=current,
            destination=destination,
            destination_occupants=destination_occupants,
            is_flying=is_flying,
        )
        return self.walk_step(
            destination=destination,
            entry_allowed=decision.allowed,
            encounter_rolls=encounter_rolls,
            action_is_walk=action_is_walk,
            map_objmove_ok=map_objmove_ok,
        )

    def walk_step_with_collision_frequency(
        self,
        *,
        collision_map: StaticCollisionMap,
        collision_profile: CollisionProfile,
        destination: MapPosition,
        frequency_roll: int,
        encounter_rolls: EncounterRolls,
        destination_occupants: Sequence[DynamicOccupant] = (),
        is_flying: bool = False,
        action_is_walk: bool = True,
        map_objmove_ok: bool = True,
    ) -> HistoricalRuntimeStep:
        current = self.domain.world.player_position
        if current is None:
            raise ValueError("player position is required before collision resolution")
        decision = ordinary_step_allowed(
            collision_map,
            collision_profile,
            origin=current,
            destination=destination,
            destination_occupants=destination_occupants,
            is_flying=is_flying,
        )
        return self.walk_step_with_frequency(
            destination=destination,
            entry_allowed=decision.allowed,
            frequency_roll=frequency_roll,
            encounter_rolls=encounter_rolls,
            action_is_walk=action_is_walk,
            map_objmove_ok=map_objmove_ok,
        )

    def spawn_group_enemies(
        self,
        encounter: GroupEncounterRequest,
        *,
        templates: dict[int, PetTemplateBridge],
        entry_count_roll: int,
        selection_rolls: Sequence[int],
        birth_rolls: Sequence[EnemyBirthRolls],
    ) -> tuple[SpawnedEnemy, ...]:
        if self.domain.world.player_position != encounter.position:
            raise ValueError("group encounter position no longer matches world state")

        areas = [
            area
            for area in self.domain.static.encounter_areas
            if area.index == encounter.area_index
        ]
        if len(areas) != 1:
            raise ValueError(
                f"group encounter area {encounter.area_index} is not uniquely loaded"
            )
        if encounter.group_id not in self.domain.static.encounter_groups:
            raise KeyError(f"group encounter references missing group {encounter.group_id}")

        plan = plan_enemy_spawns(
            areas[0],
            self.domain.static.encounter_groups[encounter.group_id],
            self.domain.static.enemy_variants,
            templates,
            entry_count_roll=entry_count_roll,
            selection_rolls=selection_rolls,
        )
        if plan.actual_count > encounter.max_enemy_count:
            raise ValueError("spawn plan exceeds GroupEncounterRequest boundary")
        return materialize_spawn_plan(
            plan,
            templates,
            birth_rolls=birth_rolls,
        )

    def start_group_battle(
        self,
        encounter: GroupEncounterRequest,
        *,
        spawned_enemies: Sequence[SpawnedEnemy],
        allied_pet_slots: Sequence[int] = (),
        ride_pet_slot: int | None = None,
    ) -> BattleSession:
        return begin_group_battle(
            self.domain,
            encounter,
            enemies=tuple(spawn.participant for spawn in spawned_enemies),
            allied_pet_slots=allied_pet_slots,
            ride_pet_slot=ride_pet_slot,
        )

    def prepare_player_action(
        self,
        session: BattleSession,
        wire_command: str,
        *,
        initiative_random_subtract: int,
        error_status: bool = False,
    ) -> BattleRoundAction:
        command = parse_player_battle_command(wire_command)
        return prepare_player_round_action(
            session.player,
            command,
            initiative_random_subtract=initiative_random_subtract,
            error_status=error_status,
        )

    def build_group_battle_combat_profiles(
        self,
        session: BattleSession,
        *,
        spawned_enemies: Sequence[SpawnedEnemy],
        allied_pet_sources: Sequence[ReconstructedPetBridgeState] = (),
        player_weapon_critical: int,
    ) -> Mapping[str, BattleCombatProfile]:
        """Build battle profiles only from provenance-bearing runtime sources."""
        player_state = self.domain.persistent.character
        if player_state is None:
            raise ValueError("persistent player state is required for combat profiles")
        return group_battle_combat_profiles(
            session,
            player_state=player_state,
            player_weapon_critical=player_weapon_critical,
            spawned_enemies=spawned_enemies,
            allied_pet_sources=allied_pet_sources,
        )

    def start_persistent_battle_state(
        self,
        session: BattleSession,
        *,
        slots: Mapping[str, int],
    ) -> PersistentBattleState:
        """Promote a battle shell into persistent multi-round state."""
        return begin_persistent_battle(session, slots=slots)

    def resolve_persistent_capture(
        self,
        state: PersistentBattleState,
        *,
        attacker_id: str,
        target_id: str,
        inputs: BattleCaptureInputs,
        roll_1_100: int | None,
        captured_pet: PetActor | None = None,
    ) -> PersistentCaptureResult:
        """Resolve capture and atomically install the copied pet on success.

        The complete captured PetActor is required from a provenance-bearing
        adapter because this runtime does not guess unresolved MP, skill-view,
        EXP-threshold or other copied fields.
        """
        occupied=tuple(sorted(slot.value for slot in self.domain.persistent.pets))
        if tuple(sorted(inputs.occupied_pet_slots)) != occupied:
            raise ValueError("capture pet-slot occupancy drift")
        result=resolve_persistent_capture_transition(
            state,
            attacker_id=attacker_id,
            target_id=target_id,
            inputs=inputs,
            roll_1_100=roll_1_100,
        )
        if not result.resolution.success:
            return result
        if captured_pet is None:
            raise ValueError("successful capture requires a complete captured PetActor")
        if result.captured_target is None:
            raise ValueError("successful capture lacks captured target snapshot")
        slot=PetSlot(int(result.resolution.assigned_pet_slot))
        if captured_pet.slot != slot:
            raise ValueError("captured pet slot does not match source first-empty slot")
        if slot in self.domain.persistent.pets:
            raise ValueError("captured pet slot became occupied before persistence")
        target=result.captured_target
        if target.source_variant_id is None or target.source_template_id is None:
            raise ValueError("captured target lacks source identity")
        if captured_pet.variant_id.value != int(target.source_variant_id):
            raise ValueError("captured pet variant identity drift")
        if captured_pet.template_id.value != int(target.source_template_id):
            raise ValueError("captured pet template identity drift")
        for key,expected in (
            ("level",target.level),
            ("hp",target.hp),
            ("max_hp",target.max_hp),
        ):
            if key not in captured_pet.state:
                raise ValueError(f"captured pet state lacks copied {key}")
            if int(captured_pet.state[key]) != int(expected):
                raise ValueError(f"captured pet copied {key} drift")
        self.domain.persistent.pets[slot]=captured_pet
        return result

    def _validated_captured_pet(
        self,
        *,
        target: BattleParticipant,
        assigned_slot: int,
        captured_pet: PetActor,
        staged_pets: Mapping[PetSlot,PetActor],
    ) -> tuple[PetSlot,PetActor]:
        slot=PetSlot(int(assigned_slot))
        if captured_pet.slot != slot:
            raise ValueError("captured pet slot does not match source first-empty slot")
        if slot in staged_pets:
            raise ValueError("captured pet slot became occupied before persistence")
        if target.source_variant_id is None or target.source_template_id is None:
            raise ValueError("captured target lacks source identity")
        if captured_pet.variant_id.value != int(target.source_variant_id):
            raise ValueError("captured pet variant identity drift")
        if captured_pet.template_id.value != int(target.source_template_id):
            raise ValueError("captured pet template identity drift")
        for key,expected in (
            ("level",target.level),
            ("hp",target.hp),
            ("max_hp",target.max_hp),
        ):
            if key not in captured_pet.state:
                raise ValueError(f"captured pet state lacks copied {key}")
            if int(captured_pet.state[key]) != int(expected):
                raise ValueError(f"captured pet copied {key} drift")
        return slot,captured_pet

    def resolve_persistent_battle_round(
        self,
        state: PersistentBattleState,
        *,
        commands: Mapping[str, BattleCommand],
        initiative_random_subtracts: Mapping[str, int],
        profiles: Mapping[str, BattleCombatProfile],
        attack_rolls: Mapping[str, OrdinaryAttackRolls],
        defense_profile: str,
        capture_contexts: Mapping[str,OrdinaryCaptureContext] | None = None,
        capture_rolls: Mapping[str,OrdinaryCaptureRolls] | None = None,
        escape_contexts: Mapping[str,OrdinaryEscapeContext] | None = None,
        escape_rolls: Mapping[str,OrdinaryEscapeRolls] | None = None,
        captured_pets_by_target_id: Mapping[str,PetActor] | None = None,
        drop_rolls_by_enemy_id: Mapping[
            str,Sequence[DropAllocationRoll]
        ] | None = None,
        field_attr: str = "none",
        field_power: int = 0,
        tie_break_order: Sequence[str] | None = None,
    ) -> PersistentRoundResult:
        """Advance one deterministic round and persist successful captures atomically."""
        contexts=dict(capture_contexts or {})
        occupied=tuple(sorted(slot.value for slot in self.domain.persistent.pets))
        for participant_id,context in contexts.items():
            if tuple(sorted(context.occupied_pet_slots)) != occupied:
                raise ValueError(
                    f"capture pet-slot occupancy drift for {participant_id}"
                )

        result=resolve_persistent_ordinary_round(
            state,
            commands=commands,
            initiative_random_subtracts=initiative_random_subtracts,
            profiles=profiles,
            attack_rolls=attack_rolls,
            capture_contexts=contexts,
            capture_rolls=capture_rolls,
            escape_contexts=escape_contexts,
            escape_rolls=escape_rolls,
            drop_rolls_by_enemy_id=drop_rolls_by_enemy_id,
            defense_profile=defense_profile,
            field_attr=field_attr,
            field_power=field_power,
            tie_break_order=tie_break_order,
        )

        supplied={
            str(target_id):pet
            for target_id,pet in (captured_pets_by_target_id or {}).items()
        }
        successful=[]
        target_id_by_slot={
            int(slot):str(participant_id)
            for participant_id,slot in state.slots.items()
        }
        participants={
            str(participant.participant_id):participant
            for participant in (
                state.session.player,
                *state.session.allied_pets,
                *state.session.enemies,
            )
        }
        for event in result.round.events:
            resolution=event.capture_resolution
            if resolution is None or not resolution.success:
                continue
            if event.resolved_target_slot is None:
                raise ValueError("successful capture lacks resolved target slot")
            target_id=target_id_by_slot.get(int(event.resolved_target_slot))
            if target_id is None:
                raise ValueError("successful capture target slot has no participant")
            successful.append((target_id,resolution))

        expected_ids={target_id for target_id,_ in successful}
        supplied_ids=set(supplied)
        if supplied_ids != expected_ids:
            missing=sorted(expected_ids-supplied_ids)
            extra=sorted(supplied_ids-expected_ids)
            raise ValueError(
                f"captured pet mapping mismatch; missing={missing}, extra={extra}"
            )

        staged=dict(self.domain.persistent.pets)
        for target_id,resolution in successful:
            if target_id not in participants:
                raise ValueError(f"captured target {target_id} lacks source participant")
            if resolution.assigned_pet_slot is None:
                raise ValueError("successful capture lacks assigned pet slot")
            slot,pet=self._validated_captured_pet(
                target=participants[target_id],
                assigned_slot=resolution.assigned_pet_slot,
                captured_pet=supplied[target_id],
                staged_pets=staged,
            )
            staged[slot]=pet

        if successful:
            self.domain.persistent.pets.clear()
            self.domain.persistent.pets.update(staged)
        return result

    def _settle_persistent_battle_drops(
        self,
        state: PersistentBattleState,
    ) -> BattleDropSettlement:
        player_id=str(state.session.player.participant_id)
        if player_id not in state.pending_drop_items_by_player_entry_id:
            raise ValueError("terminal battle state is missing player drop buffer")
        settlement=settle_player_battle_drops(
            state.pending_drop_items_by_player_entry_id[player_id],
            tuple(slot.value for slot in self.domain.persistent.inventory),
            player_alive=int(state.hp_by_participant_id[player_id])>0,
            inventory_slot_count=20,
        )
        staged=dict(self.domain.persistent.inventory)
        for raw_slot,item in settlement.inventory_additions_by_slot.items():
            slot=InventorySlot(int(raw_slot))
            if slot in staged:
                raise ValueError(f"drop settlement selected occupied slot {slot.value}")
            staged[slot]=InventoryItem(
                slot=slot,
                template_id=ItemTemplateId(int(item.template_id)),
                view=MappingProxyType(dict(item.view or {})),
            )
        self.domain.persistent.inventory.clear()
        self.domain.persistent.inventory.update(staged)
        return settlement

    def _apply_persistent_battle_outcome(
        self,
        state: PersistentBattleState,
        outcome: BattleOutcome,
    ) -> BattleReturn:
        result=apply_battle_outcome(self.domain,state.session,outcome)
        self._settle_persistent_battle_drops(state)
        return result

    def finish_persistent_escape(
        self,
        state: PersistentBattleState,
    ) -> BattleReturn:
        """Return a successful escape to persistent state without battle profit.

        Stable BATTLE_Exit clears the escaping player's battle entry before the
        normal finish-profit scan. In the current single-player domain there is
        no pet-mail mode, so all five persistent pet slots are ordinary carried
        pets: active-pet terminal HP is retained, and any carried pet at HP <= 0
        is restored to HP 1 as in the stable player BATTLE_Exit branch.

        EXP, pending item drops and pending pet loyalty are deliberately not
        settled here. Battle-only status flags are not represented by this
        status-free domain and therefore require no persistent mutation.
        """
        if state.phase != FINISHED or state.result != PLAYER_ESCAPE:
            raise ValueError("escape settlement requires a terminal escape state")

        session=state.session
        player_id=str(session.player.participant_id)
        if player_id not in state.hp_by_participant_id:
            raise ValueError("escape state is missing player HP")
        player_hp=int(state.hp_by_participant_id[player_id])
        if player_hp <= 0:
            raise ValueError("successful escape requires a living player")

        active_pet_hp_by_slot: dict[int,int]={}
        for participant in session.allied_pets:
            if participant.source_pet_slot is None:
                raise ValueError(
                    f"allied participant {participant.participant_id} lacks source pet slot"
                )
            participant_id=str(participant.participant_id)
            if participant_id not in state.hp_by_participant_id:
                raise ValueError(
                    f"escape state is missing HP for {participant_id}"
                )
            active_pet_hp_by_slot[int(participant.source_pet_slot)]=int(
                state.hp_by_participant_id[participant_id]
            )

        pet_updates: dict[int,Mapping[str,int]]={}
        for pet_slot,pet in self.domain.persistent.pets.items():
            slot=int(pet_slot.value)
            if "hp" not in pet.state:
                raise ValueError(f"persistent pet slot {slot} lacks HP")
            hp=active_pet_hp_by_slot.get(slot,int(pet.state["hp"]))
            pet_updates[slot]={"hp":1 if hp <= 0 else hp}

        return apply_battle_outcome(
            self.domain,
            state.session,
            BattleOutcome(
                result=PLAYER_ESCAPE,
                player_updates={"hp":player_hp},
                pet_updates=pet_updates,
            ),
        )

    def _require_profit_settleable_terminal(
        self,
        state: PersistentBattleState,
    ) -> None:
        if state.phase != FINISHED or state.result is None:
            raise ValueError("cannot settle battle before termination")
        if state.result == PLAYER_ESCAPE:
            raise ValueError(
                "escaped battle must use the dedicated escape/recovery settlement seam"
            )

    def finish_persistent_battle(
        self,
        state: PersistentBattleState,
    ) -> BattleReturn:
        """Project terminal battle HP back into persistent single-player state.

        This boundary intentionally settles only state already produced by the
        validated battle state machine: result plus surviving player/allied-pet
        HP plus the already-earned three-slot item-drop buffer. The stable
        base descendants do not mutate character currency in BATTLE_GetExpGold;
        the later macro-gated _BATTLE_GOLD extension is intentionally excluded.
        EXP, capture/escape, death penalties and recovery remain separate seams.
        """
        self._require_profit_settleable_terminal(state)

        session = state.session
        player_id = session.player.participant_id
        if player_id not in state.hp_by_participant_id:
            raise ValueError("terminal battle state is missing player HP")

        pet_updates: dict[int, Mapping[str, int]] = {}
        for participant in session.allied_pets:
            if participant.source_pet_slot is None:
                raise ValueError(
                    f"allied participant {participant.participant_id} lacks source pet slot"
                )
            participant_id = participant.participant_id
            if participant_id not in state.hp_by_participant_id:
                raise ValueError(
                    f"terminal battle state is missing HP for {participant_id}"
                )
            pet_updates[int(participant.source_pet_slot)] = {
                "hp": int(state.hp_by_participant_id[participant_id])
            }

        return self._apply_persistent_battle_outcome(
            state,
            BattleOutcome(
                result=state.result,
                player_updates={
                    "hp": int(state.hp_by_participant_id[player_id]),
                },
                pet_updates=pet_updates,
            ),
        )

    def finish_persistent_battle_without_level_crossing(
        self,
        state: PersistentBattleState,
    ) -> BattleReturn:
        """Settle HP, below-threshold EXP, and already-earned pet kill loyalty."""
        self._require_profit_settleable_terminal(state)

        session = state.session
        player_id = session.player.participant_id
        if player_id not in state.hp_by_participant_id:
            raise ValueError("terminal battle state is missing player HP")
        if player_id not in state.pending_exp_by_participant_id:
            raise ValueError("terminal battle state is missing player pending EXP")

        character = self.domain.persistent.character
        if character is None:
            raise ValueError("persistent player state is required for EXP settlement")

        player_hp = int(state.hp_by_participant_id[player_id])
        player_updates: dict[str, int] = {"hp": player_hp}
        pet_updates: dict[int, dict[str, int]] = {}
        pet_growth_updates: dict[int, PetGrowthState] = {}

        player_can_receive_exp = player_hp > 0
        if player_can_receive_exp:
            pending = int(state.pending_exp_by_participant_id[player_id])
            if pending > 0:
                current_exp = int(character.fields["exp"])
                max_exp = int(character.fields["max_exp"])
                next_exp = current_exp + pending
                if max_exp <= current_exp or next_exp >= max_exp:
                    raise ValueError(
                        "pending EXP reaches unresolved level-up threshold"
                    )
                player_updates["exp"] = next_exp

        for participant in session.allied_pets:
            if participant.source_pet_slot is None:
                raise ValueError(
                    f"allied participant {participant.participant_id} lacks source pet slot"
                )
            participant_id = participant.participant_id
            if participant_id not in state.hp_by_participant_id:
                raise ValueError(
                    f"terminal battle state is missing HP for {participant_id}"
                )
            if participant_id not in state.pending_exp_by_participant_id:
                raise ValueError(
                    f"terminal battle state is missing pending EXP for {participant_id}"
                )
            if participant_id not in state.pending_pet_variable_ai_by_participant_id:
                raise ValueError(
                    f"terminal battle state is missing pet VARIABLEAI delta for {participant_id}"
                )

            slot = int(participant.source_pet_slot)
            pet_slot = PetSlot(slot)
            if pet_slot not in self.domain.persistent.pets:
                raise KeyError(f"missing persistent pet slot {slot}")
            pet = self.domain.persistent.pets[pet_slot]
            hp = int(state.hp_by_participant_id[participant_id])
            updates: dict[str, int] = {"hp": hp}

            loyalty_delta=int(
                state.pending_pet_variable_ai_by_participant_id[participant_id]
            )
            if loyalty_delta:
                if pet.growth is None:
                    raise ValueError(
                        f"pet slot {slot} lacks hidden growth identity for VARIABLEAI"
                    )
                pet_growth_updates[slot]=replace(
                    pet.growth,
                    variable_ai=adjust_pet_variable_ai(
                        pet.growth.variable_ai,
                        loyalty_delta,
                    ),
                )

            if player_can_receive_exp and hp > 0:
                pending = int(state.pending_exp_by_participant_id[participant_id])
                if pending > 0:
                    current_exp = int(pet.state["exp"])
                    max_exp = int(pet.state["max_exp"])
                    next_exp = current_exp + pending
                    if max_exp <= current_exp or next_exp >= max_exp:
                        raise ValueError(
                            "pending EXP reaches unresolved level-up threshold"
                        )
                    updates["exp"] = next_exp
            pet_updates[slot] = updates

        active_pet_ids={
            str(participant.participant_id)
            for participant in session.allied_pets
        }
        ride=session.ride_pet
        if ride is not None and str(ride.participant_id) not in active_pet_ids:
            if ride.source_pet_slot is None:
                raise ValueError("ride EXP recipient lacks source pet slot")
            participant_id=str(ride.participant_id)
            if participant_id not in state.pending_exp_by_participant_id:
                raise ValueError(
                    "terminal battle state is missing ride-pet pending EXP"
                )
            slot=int(ride.source_pet_slot)
            pet_slot=PetSlot(slot)
            if pet_slot not in self.domain.persistent.pets:
                raise KeyError(f"missing persistent ride pet slot {slot}")
            pet=self.domain.persistent.pets[pet_slot]
            hp=int(pet.state["hp"])
            pending=int(state.pending_exp_by_participant_id[participant_id])
            if player_can_receive_exp and hp>0 and pending>0:
                current_exp=int(pet.state["exp"])
                max_exp=int(pet.state["max_exp"])
                next_exp=current_exp+pending
                if max_exp<=current_exp or next_exp>=max_exp:
                    raise ValueError(
                        "ride-pet pending EXP reaches unresolved level-up threshold"
                    )
                pet_updates[slot]={"exp":next_exp}

        return self._apply_persistent_battle_outcome(
            state,
            BattleOutcome(
                result=state.result,
                player_updates=player_updates,
                pet_updates=pet_updates,
                pet_growth_updates=pet_growth_updates,
            ),
        )

    def finish_persistent_battle_with_player_progression(
        self,
        state: PersistentBattleState,
        *,
        player_exp_profile: str,
        next_player_max_exp_by_level: Mapping[int, int],
    ) -> BattleReturn:
        '''Compatibility boundary that keeps pet threshold crossing unresolved.'''
        return self.finish_persistent_battle_with_progression(
            state,
            player_exp_profile=player_exp_profile,
            next_player_max_exp_by_level=next_player_max_exp_by_level,
        )

    def finish_persistent_battle_with_progression(
        self,
        state: PersistentBattleState,
        *,
        player_exp_profile: str,
        next_player_max_exp_by_level: Mapping[int, int],
        pet_exp_profile: str | None = None,
        next_pet_max_exp_by_slot: Mapping[int, Mapping[int, int]] | None = None,
        pet_level_growth_rolls_by_slot: Mapping[
            int, Sequence[PetLevelGrowthRolls]
        ] | None = None,
    ) -> BattleReturn:
        '''Settle player and pet EXP through explicitly selected progression seams.

        Pet threshold crossing is accepted only when the caller supplies a
        versioned EXP profile, the post-crossing threshold values for that pet,
        and exactly one explicit 10+1 growth-roll bundle per level gained.
        No implicit RNG, auto-heal, visible-AI rewrite or later reward rule is
        introduced here.
        '''
        self._require_profit_settleable_terminal(state)

        session=state.session
        player_id=session.player.participant_id
        if player_id not in state.hp_by_participant_id:
            raise ValueError('terminal battle state is missing player HP')
        if player_id not in state.pending_exp_by_participant_id:
            raise ValueError('terminal battle state is missing player pending EXP')

        character=self.domain.persistent.character
        if character is None:
            raise ValueError('persistent player state is required for EXP settlement')

        player_hp=int(state.hp_by_participant_id[player_id])
        player_updates: dict[str,int]={'hp':player_hp}
        pet_updates: dict[int,dict[str,int]]={}
        pet_growth_updates: dict[int,PetGrowthState]={}
        player_can_receive_exp=player_hp>0

        if player_can_receive_exp:
            pending=int(state.pending_exp_by_participant_id[player_id])
            if pending>0:
                fields=character.fields
                transition=resolve_player_exp_transition(
                    int(fields['level']),
                    int(fields['exp']),
                    pending,
                    int(fields['max_exp']),
                    profile=player_exp_profile,
                    next_max_exp_by_level=next_player_max_exp_by_level,
                )
                player_updates.update({
                    'level':transition.end_level,
                    'exp':transition.end_exp,
                    'max_exp':transition.next_max_exp,
                })
                if transition.levels_gained>0:
                    required=(
                        'free_stat_points',
                        'charm',
                        'duel_point_like_state',
                    )
                    missing=[key for key in required if key not in fields]
                    if missing:
                        raise ValueError(
                            f'player level-up requires persistent fields {missing}'
                        )
                    player_updates['free_stat_points']=(
                        int(fields['free_stat_points'])
                        + transition.free_stat_points_delta
                    )
                    player_updates['charm']=min(
                        100,
                        int(fields['charm'])+transition.charm_delta,
                    )
                    player_updates['duel_point_like_state']=(
                        int(fields['duel_point_like_state'])
                        + transition.duel_point_delta
                    )

        pet_thresholds={
            int(slot): thresholds
            for slot,thresholds in (next_pet_max_exp_by_slot or {}).items()
        }
        pet_rolls={
            int(slot): tuple(rolls)
            for slot,rolls in (pet_level_growth_rolls_by_slot or {}).items()
        }

        for participant in session.allied_pets:
            if participant.source_pet_slot is None:
                raise ValueError(
                    f'allied participant {participant.participant_id} lacks source pet slot'
                )
            participant_id=participant.participant_id
            if participant_id not in state.hp_by_participant_id:
                raise ValueError(
                    f'terminal battle state is missing HP for {participant_id}'
                )
            if participant_id not in state.pending_exp_by_participant_id:
                raise ValueError(
                    f'terminal battle state is missing pending EXP for {participant_id}'
                )
            if participant_id not in state.pending_pet_variable_ai_by_participant_id:
                raise ValueError(
                    f'terminal battle state is missing pet VARIABLEAI delta for {participant_id}'
                )

            slot=int(participant.source_pet_slot)
            pet_slot=PetSlot(slot)
            if pet_slot not in self.domain.persistent.pets:
                raise KeyError(f'missing persistent pet slot {slot}')
            hp=int(state.hp_by_participant_id[participant_id])
            updates: dict[str,int]={'hp':hp}
            pet=self.domain.persistent.pets[pet_slot]
            loyalty_delta=int(
                state.pending_pet_variable_ai_by_participant_id[participant_id]
            )
            loyalty_variable_ai=(
                adjust_pet_variable_ai(
                    pet.growth.variable_ai,
                    loyalty_delta,
                )
                if loyalty_delta and pet.growth is not None
                else (pet.growth.variable_ai if pet.growth is not None else None)
            )
            if loyalty_delta and pet.growth is None:
                raise ValueError(
                    f'pet slot {slot} lacks hidden growth identity for VARIABLEAI'
                )
            if loyalty_delta and pet.growth is not None:
                pet_growth_updates[slot]=replace(
                    pet.growth,
                    variable_ai=loyalty_variable_ai,
                )

            if player_can_receive_exp and hp>0:
                pending=int(state.pending_exp_by_participant_id[participant_id])
                if pending>0:
                    current_exp=int(pet.state['exp'])
                    max_exp=int(pet.state['max_exp'])
                    next_exp=current_exp+pending
                    if max_exp<=current_exp:
                        raise ValueError('pet persistent EXP is already at or above max EXP')
                    if next_exp<max_exp:
                        updates['exp']=next_exp
                    else:
                        if pet_exp_profile is None:
                            raise ValueError(
                                'pet pending EXP reaches unresolved pet level-up threshold'
                            )
                        if pet.growth is None:
                            raise ValueError(
                                f'pet slot {slot} lacks hidden growth identity'
                            )
                        if slot not in pet_thresholds:
                            raise ValueError(
                                f'pet slot {slot} lacks explicit post-level EXP thresholds'
                            )
                        if slot not in pet_rolls:
                            raise ValueError(
                                f'pet slot {slot} lacks explicit level-up growth rolls'
                            )
                        growth=pet.growth
                        transition=resolve_pet_exp_growth_transition(
                            int(pet.state['level']),
                            current_exp,
                            pending,
                            max_exp,
                            profile=pet_exp_profile,
                            next_max_exp_by_level=pet_thresholds[slot],
                            growth_base=unpack_growth_base(growth.alloc_point),
                            rank=growth.pet_rank,
                            current_internal_stats=(
                                growth.internal_vital,
                                growth.internal_strength,
                                growth.internal_toughness,
                                growth.internal_dexterity,
                            ),
                            current_variable_ai=(
                                loyalty_variable_ai
                                if loyalty_variable_ai is not None
                                else growth.variable_ai
                            ),
                            level_rolls=pet_rolls[slot],
                        )
                        derived=base_derived_stats(
                            *transition.growth.end_internal_stats
                        )
                        updates.update({
                            'level':transition.end_level,
                            'exp':transition.end_exp,
                            'max_exp':transition.next_max_exp,
                            'max_hp':derived['max_hp'],
                            'attack':derived['attack_power'],
                            'defense':derived['defence_power'],
                            'quick':derived['quick'],
                            'hp':min(hp,derived['max_hp']),
                        })
                        pet_growth_updates[slot]=PetGrowthState(
                            pet_rank=growth.pet_rank,
                            alloc_point=growth.alloc_point,
                            internal_vital=transition.growth.end_internal_stats[0],
                            internal_strength=transition.growth.end_internal_stats[1],
                            internal_toughness=transition.growth.end_internal_stats[2],
                            internal_dexterity=transition.growth.end_internal_stats[3],
                            variable_ai=transition.growth.end_variable_ai,
                        )
            pet_updates[slot]=updates

        active_pet_ids={
            str(participant.participant_id)
            for participant in session.allied_pets
        }
        ride=session.ride_pet
        if ride is not None and str(ride.participant_id) not in active_pet_ids:
            if ride.source_pet_slot is None:
                raise ValueError('ride EXP recipient lacks source pet slot')
            participant_id=str(ride.participant_id)
            if participant_id not in state.pending_exp_by_participant_id:
                raise ValueError(
                    'terminal battle state is missing ride-pet pending EXP'
                )
            slot=int(ride.source_pet_slot)
            pet_slot=PetSlot(slot)
            if pet_slot not in self.domain.persistent.pets:
                raise KeyError(f'missing persistent ride pet slot {slot}')
            pet=self.domain.persistent.pets[pet_slot]
            hp=int(pet.state['hp'])
            pending=int(state.pending_exp_by_participant_id[participant_id])
            if player_can_receive_exp and hp>0 and pending>0:
                current_exp=int(pet.state['exp'])
                max_exp=int(pet.state['max_exp'])
                next_exp=current_exp+pending
                updates: dict[str,int]={}
                if max_exp<=current_exp:
                    raise ValueError(
                        'ride pet persistent EXP is already at or above max EXP'
                    )
                if next_exp<max_exp:
                    updates['exp']=next_exp
                else:
                    if pet_exp_profile is None:
                        raise ValueError(
                            'ride-pet pending EXP reaches unresolved pet level-up threshold'
                        )
                    if pet.growth is None:
                        raise ValueError(
                            f'ride pet slot {slot} lacks hidden growth identity'
                        )
                    if slot not in pet_thresholds:
                        raise ValueError(
                            f'ride pet slot {slot} lacks explicit post-level EXP thresholds'
                        )
                    if slot not in pet_rolls:
                        raise ValueError(
                            f'ride pet slot {slot} lacks explicit level-up growth rolls'
                        )
                    growth=pet.growth
                    transition=resolve_pet_exp_growth_transition(
                        int(pet.state['level']),
                        current_exp,
                        pending,
                        max_exp,
                        profile=pet_exp_profile,
                        next_max_exp_by_level=pet_thresholds[slot],
                        growth_base=unpack_growth_base(growth.alloc_point),
                        rank=growth.pet_rank,
                        current_internal_stats=(
                            growth.internal_vital,
                            growth.internal_strength,
                            growth.internal_toughness,
                            growth.internal_dexterity,
                        ),
                        current_variable_ai=growth.variable_ai,
                        level_rolls=pet_rolls[slot],
                    )
                    derived=base_derived_stats(
                        *transition.growth.end_internal_stats
                    )
                    updates.update({
                        'level':transition.end_level,
                        'exp':transition.end_exp,
                        'max_exp':transition.next_max_exp,
                        'max_hp':derived['max_hp'],
                        'attack':derived['attack_power'],
                        'defense':derived['defence_power'],
                        'quick':derived['quick'],
                        'hp':min(hp,derived['max_hp']),
                    })
                    pet_growth_updates[slot]=PetGrowthState(
                        pet_rank=growth.pet_rank,
                        alloc_point=growth.alloc_point,
                        internal_vital=transition.growth.end_internal_stats[0],
                        internal_strength=transition.growth.end_internal_stats[1],
                        internal_toughness=transition.growth.end_internal_stats[2],
                        internal_dexterity=transition.growth.end_internal_stats[3],
                        variable_ai=transition.growth.end_variable_ai,
                    )
                pet_updates[slot]=updates

        return self._apply_persistent_battle_outcome(
            state,
            BattleOutcome(
                result=state.result,
                player_updates=player_updates,
                pet_updates=pet_updates,
                pet_growth_updates=pet_growth_updates,
            ),
        )

    def resolve_ordinary_battle_round(
        self,
        session: BattleSession,
        *,
        commands: Mapping[str, BattleCommand],
        initiative_random_subtracts: Mapping[str, int],
        slots: Mapping[str, int],
        profiles: Mapping[str, BattleCombatProfile],
        attack_rolls: Mapping[str, OrdinaryAttackRolls],
        defense_profile: str,
        field_attr: str = "none",
        field_power: int = 0,
        tie_break_order: Sequence[str] | None = None,
    ) -> ResolvedOrdinaryRound:
        """Resolve one explicit attack/guard/wait round inside the battle shell."""
        participants = (
            session.player,
            *session.allied_pets,
            *session.enemies,
        )
        prepared = prepare_battle_round(
            participants,
            commands,
            initiative_random_subtracts,
            tie_break_order=tie_break_order,
        )
        return resolve_ordinary_round(
            prepared,
            slots=slots,
            profiles=profiles,
            attack_rolls=attack_rolls,
            defense_profile=defense_profile,
            field_attr=field_attr,
            field_power=field_power,
        )

    def start_battle(
        self,
        encounter: EncounterRequest,
        *,
        enemies: Sequence[BattleParticipant],
        allied_pet_slots: Sequence[int] = (),
        ride_pet_slot: int | None = None,
    ) -> BattleSession:
        return begin_battle(
            self.domain,
            encounter,
            enemies=enemies,
            allied_pet_slots=allied_pet_slots,
            ride_pet_slot=ride_pet_slot,
        )

    def finish_battle(
        self,
        session: BattleSession,
        outcome: BattleOutcome,
    ) -> BattleReturn:
        return apply_battle_outcome(self.domain, session, outcome)
