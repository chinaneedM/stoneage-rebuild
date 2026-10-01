#!/usr/bin/env python3
"""Battle-local Nocast state kept outside historical character save schemas."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from types import MappingProxyType
from typing import Mapping

from tools.stoneage_nocast_model import (
    NocastApplication,
    NocastTick,
    nocast_blocks_direct_magic,
)


@dataclass(frozen=True)
class NocastParticipantRuntime:
    """Explicit work/status inputs required by the guarded Nocast source path."""

    vital: int
    strength: int
    toughness: int
    dexterity: int
    mod_nocast: int = 0
    suit_resist: int = 0
    counter: int = 0
    nc_flag: int | None = None
    unmodeled_status_active: bool = False
    weaken_active_at_visit: bool = False
    barrier_active_at_visit: bool = False

    def __post_init__(self) -> None:
        for name in (
            "vital", "strength", "toughness", "dexterity",
            "mod_nocast", "suit_resist", "counter",
        ):
            object.__setattr__(self, name, int(getattr(self, name)))
        attrs=(self.vital,self.strength,self.toughness,self.dexterity)
        if any(value < 0 for value in attrs) or sum(attrs) <= 0:
            raise ValueError("Nocast participant stats require a positive nonnegative sum")
        if self.counter < 0:
            raise ValueError("Nocast counter cannot be negative")
        if self.nc_flag is not None:
            flag=int(self.nc_flag)
            if flag not in {0,1}:
                raise ValueError("Nocast NC flag must be 0, 1, or None")
            object.__setattr__(self,"nc_flag",flag)
        for name in (
            "unmodeled_status_active",
            "weaken_active_at_visit",
            "barrier_active_at_visit",
        ):
            object.__setattr__(self,name,bool(getattr(self,name)))

    def has_any_status(self, *, base_status_active: bool) -> bool:
        return bool(
            base_status_active
            or self.unmodeled_status_active
            or self.weaken_active_at_visit
            or self.barrier_active_at_visit
            or self.counter > 0
        )

    def after_application(
        self,
        application: NocastApplication,
    ) -> "NocastParticipantRuntime":
        if application.turn_written is None:
            return self
        return replace(
            self,
            counter=int(application.turn_written),
            nc_flag=application.nc_flag,
        )

    def after_tick(self, tick: NocastTick) -> "NocastParticipantRuntime":
        return replace(
            self,
            counter=int(tick.counter_after),
            nc_flag=tick.nc_flag,
        )


@dataclass(frozen=True)
class NocastRoundOverlay:
    runtime_by_participant_id: Mapping[str,NocastParticipantRuntime]

    def __post_init__(self) -> None:
        normalized={}
        for participant_id,runtime in self.runtime_by_participant_id.items():
            participant_id=str(participant_id)
            if not participant_id:
                raise ValueError("Nocast overlay participant id cannot be empty")
            if not isinstance(runtime,NocastParticipantRuntime):
                raise TypeError("Nocast overlay values must be participant runtimes")
            normalized[participant_id]=runtime
        object.__setattr__(
            self,
            "runtime_by_participant_id",
            MappingProxyType(normalized),
        )

    def blocks_direct_magic(self, participant_id: str) -> bool:
        participant_id=str(participant_id)
        if participant_id not in self.runtime_by_participant_id:
            raise KeyError(f"missing Nocast runtime for {participant_id}")
        return nocast_blocks_direct_magic(
            self.runtime_by_participant_id[participant_id].counter
        )


@dataclass(frozen=True)
class NocastActionRolls:
    """Explicit RNG consumed by one semantic Nocast action."""

    retarget_draws_0_9: tuple[int,...] = ()
    hit_rolls_by_slot: Mapping[int,int] = field(default_factory=dict)

    def __post_init__(self) -> None:
        draws=tuple(int(value) for value in self.retarget_draws_0_9)
        if any(not 0 <= value <= 9 for value in draws):
            raise ValueError("Nocast retarget draws must be in 0..9")
        rolls={}
        for slot,value in self.hit_rolls_by_slot.items():
            slot=int(slot); value=int(value)
            if not 0 <= slot < 20:
                raise ValueError("Nocast hit-roll slot must be in 0..19")
            if not 1 <= value <= 100:
                raise ValueError("Nocast hit roll must be in 1..100")
            rolls[slot]=value
        object.__setattr__(self,"retarget_draws_0_9",draws)
        object.__setattr__(
            self,"hit_rolls_by_slot",MappingProxyType(rolls)
        )

    @property
    def is_empty(self) -> bool:
        return not self.retarget_draws_0_9 and not self.hit_rolls_by_slot
