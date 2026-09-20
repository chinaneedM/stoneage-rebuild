#!/usr/bin/env python3
"""Minimal end-to-end in-process historical simulation slice.

This composes the already validated world, encounter and battle boundaries.
It intentionally leaves collision verdicts, RNG rolls, enemy birth rolls,
commands, AI and battle outcomes as explicit inputs.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

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


@dataclass
class SinglePlayerHistoricalRuntime:
    domain: SinglePlayerHistoricalDomain
    topology: HistoricalWorldTopology
    tick_index: int = 0

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
