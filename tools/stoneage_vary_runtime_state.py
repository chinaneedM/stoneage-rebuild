#!/usr/bin/env python3
"""Deterministic battle-local runtime state for recovered25 PETSKILL_Vary."""

from __future__ import annotations

from dataclasses import dataclass, replace
from types import MappingProxyType
from typing import Mapping


CALLBACK_NAME = "PETSKILL_Vary"
RECOVERED25_VARY_ID = 600
VARY_WOLF_IMAGE = 101428
VARY_ACTOR_EFFECT = 101120
ALLOWED_TEMPNOS = frozenset({981, 982, 983, 984})

PROFILE_GAVIN_IRIS_ATTACK_QUICK = "gavin_iris_attack_quick"
PROFILE_BISMARCK_ATTACK_DEFENSE_QUICK = "bismarck_attack_defense_quick"
VARY_PROFILES = frozenset(
    {
        PROFILE_GAVIN_IRIS_ATTACK_QUICK,
        PROFILE_BISMARCK_ATTACK_DEFENSE_QUICK,
    }
)

ATTACK_PERCENT = 30.0
DEFENSE_PERCENT = -50.0
QUICK_PERCENT = 30.0


def _source_percent(base: int, percent: float) -> int:
    """C-shaped callback arithmetic: base + trunc(base * percent / 100)."""
    base = int(base)
    return base + int(base * float(percent) / 100.0)


def vary_visual_effect_enabled(profile: str) -> bool:
    profile = str(profile)
    if profile not in VARY_PROFILES:
        raise ValueError("Vary runtime profile is not an accepted descendant profile")
    return profile == PROFILE_GAVIN_IRIS_ATTACK_QUICK


@dataclass(frozen=True)
class VaryParticipantRuntime:
    """The work/base-image fields directly mutated by the Vary callback/lifetime."""

    profile: str
    tempno: int
    original_base_image: int
    base_image: int
    work_turn: int
    fixed_attack: int
    fixed_defense: int
    fixed_quick: int
    attack_power: int
    defense_power: int
    quick: int

    def __post_init__(self) -> None:
        profile = str(self.profile)
        if profile not in VARY_PROFILES:
            raise ValueError("Vary runtime profile is not an accepted descendant profile")
        tempno = int(self.tempno)
        if tempno not in ALLOWED_TEMPNOS:
            raise ValueError("Vary runtime actor TEMPNO is outside 981..984")
        for name in (
            "original_base_image",
            "base_image",
            "work_turn",
            "fixed_attack",
            "fixed_defense",
            "fixed_quick",
            "attack_power",
            "defense_power",
            "quick",
        ):
            object.__setattr__(self, name, int(getattr(self, name)))
        if self.work_turn < 0:
            raise ValueError("Vary WORKTURN cannot be negative")
        object.__setattr__(self, "profile", profile)
        object.__setattr__(self, "tempno", tempno)

    @property
    def active(self) -> bool:
        return int(self.base_image) == VARY_WOLF_IMAGE

    @property
    def blocks_recast(self) -> bool:
        return self.active

    @property
    def visual_effect_enabled(self) -> bool:
        return vary_visual_effect_enabled(self.profile)


@dataclass(frozen=True)
class VaryTurnAdvance:
    before_work_turn: int
    after_work_turn: int
    expired: bool
    visual_effect_enabled: bool


def create_vary_participant_runtime(
    *,
    profile: str,
    tempno: int,
    base_image: int,
    fixed_attack: int,
    fixed_defense: int,
    fixed_quick: int,
) -> VaryParticipantRuntime:
    return VaryParticipantRuntime(
        profile=str(profile),
        tempno=int(tempno),
        original_base_image=int(base_image),
        base_image=int(base_image),
        work_turn=0,
        fixed_attack=int(fixed_attack),
        fixed_defense=int(fixed_defense),
        fixed_quick=int(fixed_quick),
        attack_power=int(fixed_attack),
        defense_power=int(fixed_defense),
        quick=int(fixed_quick),
    )


def cast_vary(state: VaryParticipantRuntime) -> VaryParticipantRuntime:
    """Apply the callback mutation before the Vary action executes."""
    if not isinstance(state, VaryParticipantRuntime):
        raise TypeError("Vary state has wrong type")
    if state.blocks_recast:
        raise ValueError("PETSKILL_Vary recast is blocked while image 101428 is active")

    defense = int(state.defense_power)
    if state.profile == PROFILE_BISMARCK_ATTACK_DEFENSE_QUICK:
        defense = _source_percent(state.fixed_defense, DEFENSE_PERCENT)

    return replace(
        state,
        base_image=VARY_WOLF_IMAGE,
        work_turn=0,
        attack_power=_source_percent(state.fixed_attack, ATTACK_PERCENT),
        defense_power=defense,
        quick=_source_percent(state.fixed_quick, QUICK_PERCENT),
    )


def _expire_vary(state: VaryParticipantRuntime) -> VaryParticipantRuntime:
    defense = int(state.defense_power)
    if state.profile == PROFILE_BISMARCK_ATTACK_DEFENSE_QUICK:
        defense = int(state.fixed_defense)
    return replace(
        state,
        base_image=int(state.original_base_image),
        work_turn=0,
        attack_power=int(state.fixed_attack),
        defense_power=defense,
        quick=int(state.fixed_quick),
    )


def advance_vary_after_actor_action(
    state: VaryParticipantRuntime,
) -> tuple[VaryParticipantRuntime, VaryTurnAdvance | None]:
    """Mirror the post-action WORKTURN lifecycle.

    The initial Vary action is an actor action too, so callers invoke this once
    immediately after Vary execution. Active state therefore advances 0->1 on
    the cast action and expires when the sixth actor action advances 5->6.
    """
    if not isinstance(state, VaryParticipantRuntime):
        raise TypeError("Vary state has wrong type")
    if not state.active:
        return state, None
    before = int(state.work_turn)
    after = before + 1
    if after > 5:
        expired = _expire_vary(state)
        return expired, VaryTurnAdvance(
            before_work_turn=before,
            after_work_turn=0,
            expired=True,
            visual_effect_enabled=state.visual_effect_enabled,
        )
    advanced = replace(state, work_turn=after)
    return advanced, VaryTurnAdvance(
        before_work_turn=before,
        after_work_turn=after,
        expired=False,
        visual_effect_enabled=state.visual_effect_enabled,
    )


def teardown_vary(state: VaryParticipantRuntime) -> VaryParticipantRuntime:
    """Battle teardown restores the non-wolf base image and Vary-owned powers."""
    if not isinstance(state, VaryParticipantRuntime):
        raise TypeError("Vary state has wrong type")
    if not state.active:
        return state
    return _expire_vary(state)


@dataclass(frozen=True)
class VaryRuntimeOverlay:
    """Persistent battle-local Vary work state for currently transformed actors.

    Only active wolf states are carried. Expiry removes the actor from the
    overlay rather than retaining a second baseline copy.
    """

    runtime_by_participant_id: Mapping[str, VaryParticipantRuntime]

    def __post_init__(self) -> None:
        normalized={}
        for participant_id,state in self.runtime_by_participant_id.items():
            participant_id=str(participant_id)
            if not participant_id:
                raise ValueError("Vary overlay participant id must be non-empty")
            if participant_id in normalized:
                raise ValueError("Vary overlay participant ids must be unique")
            if not isinstance(state,VaryParticipantRuntime):
                raise TypeError("Vary overlay state has wrong type")
            if not state.active:
                raise ValueError("Vary overlay may carry active wolf states only")
            normalized[participant_id]=state
        object.__setattr__(
            self,
            "runtime_by_participant_id",
            MappingProxyType(normalized),
        )

    @classmethod
    def empty(cls) -> "VaryRuntimeOverlay":
        return cls({})

    def with_cast(
        self,
        participant_id: str,
        state: VaryParticipantRuntime,
    ) -> "VaryRuntimeOverlay":
        participant_id=str(participant_id)
        if participant_id in self.runtime_by_participant_id:
            raise ValueError("Vary recast blocked while actor is transformed")
        if not isinstance(state,VaryParticipantRuntime) or not state.active:
            raise ValueError("Vary overlay cast requires active post-callback state")
        values=dict(self.runtime_by_participant_id)
        values[participant_id]=state
        return VaryRuntimeOverlay(values)

    def advance_actor_action(
        self,
        participant_id: str,
    ) -> tuple["VaryRuntimeOverlay", VaryTurnAdvance | None]:
        participant_id=str(participant_id)
        if participant_id not in self.runtime_by_participant_id:
            return self,None
        next_state,tick=advance_vary_after_actor_action(
            self.runtime_by_participant_id[participant_id]
        )
        values=dict(self.runtime_by_participant_id)
        if next_state.active:
            values[participant_id]=next_state
        else:
            values.pop(participant_id,None)
        return VaryRuntimeOverlay(values),tick

    def retain_participants(
        self,
        participant_ids: set[str] | frozenset[str] | tuple[str, ...],
    ) -> "VaryRuntimeOverlay":
        allowed={str(value) for value in participant_ids}
        return VaryRuntimeOverlay({
            participant_id:state
            for participant_id,state in self.runtime_by_participant_id.items()
            if participant_id in allowed
        })

    def teardown(self) -> "VaryRuntimeOverlay":
        # Work-state restoration is represented by dropping all overlays; the
        # baseline battle/session participants remain untouched.
        return VaryRuntimeOverlay.empty()
