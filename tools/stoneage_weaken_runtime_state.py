#!/usr/bin/env python3
"""Explicit RNG bundle for one semantic recovered25 Weaken action."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True)
class WeakenActionRolls:
    retarget_draws_0_9: tuple[int,...] = ()
    hit_rolls_by_slot: Mapping[int,int] = field(default_factory=dict)

    def __post_init__(self) -> None:
        draws=tuple(int(value) for value in self.retarget_draws_0_9)
        if any(not 0 <= value <= 9 for value in draws):
            raise ValueError("Weaken retarget draws must be in 0..9")
        rolls={}
        for slot,value in self.hit_rolls_by_slot.items():
            slot=int(slot); value=int(value)
            if not 0 <= slot < 20:
                raise ValueError("Weaken hit-roll slot must be in 0..19")
            if not 1 <= value <= 100:
                raise ValueError("Weaken hit roll must be in 1..100")
            rolls[slot]=value
        object.__setattr__(self,"retarget_draws_0_9",draws)
        object.__setattr__(
            self,"hit_rolls_by_slot",MappingProxyType(rolls)
        )

    @property
    def is_empty(self) -> bool:
        return not self.retarget_draws_0_9 and not self.hit_rolls_by_slot
