#!/usr/bin/env python3
"""Minimal end-to-end in-process historical simulation slice.

This composes the already validated world, encounter and battle boundaries.
It intentionally leaves collision verdicts, RNG rolls, enemy birth rolls,
commands, AI and battle outcomes as explicit inputs.
"""

from __future__ import annotations

from dataclasses import dataclass, field
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
from tools.stoneage_battle_command_model import (
    BattleRoundAction,
    parse_player_battle_command,
    prepare_player_round_action,
)
from tools.stoneage_battle_round_model import (
    BattleCombatProfile,
    BattleCommand,
    OrdinaryAttackRolls,
    ResolvedOrdinaryRound,
    prepare_battle_round,
    resolve_ordinary_round,
)
from tools.stoneage_battle_state_model import (
    FINISHED,
    PersistentBattleState,
    PersistentRoundResult,
    begin_persistent_battle,
    resolve_persistent_ordinary_round,
)
from tools.stoneage_enemy_spawn_model import (
    EnemyBirthRolls,
    SpawnedEnemy,
    materialize_spawn_plan,
    plan_enemy_spawns,
)
from tools.stoneage_combat_profile_bridge import group_battle_combat_profiles
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
    MapPosition,
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
    ) -> BattleSession:
        return begin_group_battle(
            self.domain,
            encounter,
            enemies=tuple(spawn.participant for spawn in spawned_enemies),
            allied_pet_slots=allied_pet_slots,
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

    def resolve_persistent_battle_round(
        self,
        state: PersistentBattleState,
        *,
        commands: Mapping[str, BattleCommand],
        initiative_random_subtracts: Mapping[str, int],
        profiles: Mapping[str, BattleCombatProfile],
        attack_rolls: Mapping[str, OrdinaryAttackRolls],
        defense_profile: str,
        field_attr: str = "none",
        field_power: int = 0,
        tie_break_order: Sequence[str] | None = None,
    ) -> PersistentRoundResult:
        """Advance one deterministic ordinary round and retain battle HP."""
        return resolve_persistent_ordinary_round(
            state,
            commands=commands,
            initiative_random_subtracts=initiative_random_subtracts,
            profiles=profiles,
            attack_rolls=attack_rolls,
            defense_profile=defense_profile,
            field_attr=field_attr,
            field_power=field_power,
            tie_break_order=tie_break_order,
        )

    def finish_persistent_battle(
        self,
        state: PersistentBattleState,
    ) -> BattleReturn:
        """Project terminal battle HP back into persistent single-player state.

        This boundary intentionally settles only state already produced by the
        validated battle state machine: result plus surviving player/allied-pet
        HP. Rewards, drops, EXP, money, capture/escape, death penalties and
        recovery remain separate evidence seams.
        """
        if state.phase != FINISHED or state.result is None:
            raise ValueError("cannot settle battle before termination")

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

        return apply_battle_outcome(
            self.domain,
            session,
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
        """Settle HP plus pending EXP only when no level threshold is crossed.

        Taiwan v1 exposes separate EXP/max-EXP fields, while descendant sources
        preserve two different level-transition regimes. Below the current
        max-EXP boundary both regimes agree on simple addition. Reaching or
        crossing that boundary is rejected until the historical progression
        profile is selected explicitly.
        """
        if state.phase != FINISHED or state.result is None:
            raise ValueError("cannot settle battle before termination")

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

        # Stable BATTLE_GetExpGold() returns immediately for a dead player.
        # Therefore its owned-pet EXP loop is also skipped on player defeat.
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

            slot = int(participant.source_pet_slot)
            hp = int(state.hp_by_participant_id[participant_id])
            updates: dict[str, int] = {"hp": hp}

            # Stable pet EXP application happens only from the living player's
            # result path and skips pets already marked dead.
            if player_can_receive_exp and hp > 0:
                pending = int(state.pending_exp_by_participant_id[participant_id])
                if pending > 0:
                    pet_slot = PetSlot(slot)
                    if pet_slot not in self.domain.persistent.pets:
                        raise KeyError(f"missing persistent pet slot {slot}")
                    pet = self.domain.persistent.pets[pet_slot]
                    current_exp = int(pet.state["exp"])
                    max_exp = int(pet.state["max_exp"])
                    next_exp = current_exp + pending
                    if max_exp <= current_exp or next_exp >= max_exp:
                        raise ValueError(
                            "pending EXP reaches unresolved level-up threshold"
                        )
                    updates["exp"] = next_exp
            pet_updates[slot] = updates

        return apply_battle_outcome(
            self.domain,
            session,
            BattleOutcome(
                result=state.result,
                player_updates=player_updates,
                pet_updates=pet_updates,
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
    ) -> BattleSession:
        return begin_battle(
            self.domain,
            encounter,
            enemies=enemies,
            allied_pet_slots=allied_pet_slots,
        )

    def finish_battle(
        self,
        session: BattleSession,
        outcome: BattleOutcome,
    ) -> BattleReturn:
        return apply_battle_outcome(self.domain, session, outcome)
