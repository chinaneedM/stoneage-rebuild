#!/usr/bin/env python3
"""Minimal end-to-end in-process historical simulation slice.

This composes the already validated world, encounter and battle boundaries.
It intentionally leaves collision verdicts, RNG rolls, enemy birth rolls,
commands, AI and battle outcomes as explicit inputs.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence

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
from tools.stoneage_singleplayer_battle import (
    BattleOutcome,
    BattleParticipant,
    BattleReturn,
    BattleSession,
    apply_battle_outcome,
    begin_battle,
)
from tools.stoneage_singleplayer_domain import (
    EncounterRequest,
    EncounterRolls,
    MapPosition,
    SinglePlayerHistoricalDomain,
)
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
        if (
            walk.moved
            and not walk.encounter_suppressed
            and encounter_rolls is not None
        ):
            encounter = self.domain.request_encounter(
                group_roll=encounter_rolls.group_roll,
                enemy_roll=encounter_rolls.enemy_roll,
                level_roll=encounter_rolls.level_roll,
            )

        return HistoricalRuntimeStep(
            tick_index=self.tick_index,
            walk=walk,
            encounter=encounter,
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
        if frequency.encounter_triggered:
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
