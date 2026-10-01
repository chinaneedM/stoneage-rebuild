#!/usr/bin/env python3
"""Battle-local four-element resistance/training state for AttackMagic."""

from __future__ import annotations

from dataclasses import dataclass, replace
from types import MappingProxyType
from typing import Mapping

from tools.stoneage_attack_magic_damage_model import MagicExpState


FIELD_ELEMENT_BY_NAME = {
    "none": None,
    "earth": 0,
    "water": 1,
    "fire": 2,
    "wind": 3,
}


def attack_magic_field_element(field_attr: str) -> int | None:
    key=str(field_attr)
    if key not in FIELD_ELEMENT_BY_NAME:
        raise ValueError(f"unknown AttackMagic field attribute: {key}")
    return FIELD_ELEMENT_BY_NAME[key]


@dataclass(frozen=True)
class AttackMagicResistanceRuntime:
    """Defender resistance state plus battle modifiers.

    ``levels`` corresponds semantically to descendant CHAR_*_RESIST.
    ``exps`` corresponds to CHAR_*_DEFMAGIC_EXP (resistance training
    experience), not CHAR_*_EXP proficiency levels or CHAR_*_ATTMAGIC_EXP.
    """

    levels: tuple[int, int, int, int] = (0, 0, 0, 0)
    exps: tuple[int, int, int, int] = (0, 0, 0, 0)
    equipment_resistance: tuple[int, int, int, int] = (0, 0, 0, 0)
    equipment_quimagic: int = 0
    magic_defense_percent: int | None = None

    def __post_init__(self) -> None:
        levels=tuple(int(x) for x in self.levels)
        exps=tuple(int(x) for x in self.exps)
        equip=tuple(int(x) for x in self.equipment_resistance)
        if len(levels) != 4 or len(exps) != 4 or len(equip) != 4:
            raise ValueError("AttackMagic resistance runtime requires four elements")
        if any(not 0 <= x <= 100 for x in levels):
            raise ValueError("AttackMagic resistance levels must be in 0..100")
        if any(x < 0 for x in exps):
            raise ValueError("AttackMagic resistance experience cannot be negative")
        object.__setattr__(self,"levels",levels)
        object.__setattr__(self,"exps",exps)
        object.__setattr__(self,"equipment_resistance",equip)
        object.__setattr__(
            self,"equipment_quimagic",int(self.equipment_quimagic)
        )
        if self.magic_defense_percent is not None:
            object.__setattr__(
                self,
                "magic_defense_percent",
                int(self.magic_defense_percent),
            )

    def state_for(self, element: int) -> MagicExpState:
        element=int(element)
        if element not in range(4):
            raise ValueError("AttackMagic resistance element must be 0..3")
        opposed=(element+1)%4
        return MagicExpState(
            self.levels[element],
            self.exps[element],
            self.levels[opposed],
            self.exps[opposed],
        )

    def with_state(
        self,
        element: int,
        state: MagicExpState,
    ) -> "AttackMagicResistanceRuntime":
        element=int(element)
        if element not in range(4):
            raise ValueError("AttackMagic resistance element must be 0..3")
        opposed=(element+1)%4
        levels=list(self.levels)
        exps=list(self.exps)
        levels[element]=int(state.level)
        exps[element]=int(state.exp)
        levels[opposed]=int(state.opposed_level)
        exps[opposed]=int(state.opposed_exp)
        return replace(self,levels=tuple(levels),exps=tuple(exps))


@dataclass(frozen=True)
class AttackMagicRoundOverlay:
    resistance_by_participant_id: Mapping[
        str,AttackMagicResistanceRuntime
    ]

    def __post_init__(self) -> None:
        normalized={}
        for participant_id,runtime in self.resistance_by_participant_id.items():
            participant_id=str(participant_id)
            if not participant_id:
                raise ValueError("AttackMagic overlay participant id cannot be empty")
            if not isinstance(runtime,AttackMagicResistanceRuntime):
                raise TypeError(
                    "AttackMagic overlay values must be resistance runtimes"
                )
            normalized[participant_id]=runtime
        object.__setattr__(
            self,
            "resistance_by_participant_id",
            MappingProxyType(normalized),
        )
