#!/usr/bin/env python3
"""Persistent battle-local FOXROUND state for bounded BecomeFox runtime."""
from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from tools.stoneage_becomefox_reference_model import (
    FOX_IMAGE,
    NO_FOX_ROUND,
    FoxState,
    RoundRecovery,
    apply_active_fox_action_powers,
    resolve_battle_exit,
    resolve_round_recovery,
)

PROFILE_GAVIN="gavin"
PROFILE_IRIS="iris"
PROFILE_BISMARCK="bismarck"
BECOMEFOX_SOURCE_PROFILES=frozenset({
    PROFILE_GAVIN,PROFILE_IRIS,PROFILE_BISMARCK,
})


def petin_accessor_profile(source_profile: str) -> str:
    profile=str(source_profile)
    if profile not in BECOMEFOX_SOURCE_PROFILES:
        raise ValueError("unknown BecomeFox source profile")
    return "work_int" if profile==PROFILE_BISMARCK else "ordinary_int"


def arrange_guard_active(source_profile: str) -> bool:
    profile=str(source_profile)
    if profile not in BECOMEFOX_SOURCE_PROFILES:
        raise ValueError("unknown BecomeFox source profile")
    return profile in {PROFILE_GAVIN,PROFILE_IRIS}


@dataclass(frozen=True)
class FoxParticipantRuntime:
    """One active target's source-profile-bound FOXROUND work state."""

    source_profile: str
    state: FoxState

    def __post_init__(self) -> None:
        profile=str(self.source_profile)
        if profile not in BECOMEFOX_SOURCE_PROFILES:
            raise ValueError("BecomeFox runtime source profile must be explicit")
        if not isinstance(self.state,FoxState):
            raise TypeError("BecomeFox runtime requires FoxState")
        if int(self.state.fox_round)==NO_FOX_ROUND:
            raise ValueError("persistent BecomeFox runtime may carry active FOXROUND only")
        if int(self.state.base_image)!=FOX_IMAGE:
            raise ValueError("active FOXROUND runtime must carry fox image")
        if int(self.state.ride_pet)!=-1:
            raise ValueError("bounded BecomeFox runtime excludes ride-bearing state")
        object.__setattr__(self,"source_profile",profile)

    @property
    def accessor_profile(self) -> str:
        return petin_accessor_profile(self.source_profile)

    def prepare_actor_action(self) -> "FoxParticipantRuntime":
        """Source action-time rewrite: fixed STR/TOUGH/DEX * 0.8."""
        return FoxParticipantRuntime(
            self.source_profile,
            apply_active_fox_action_powers(self.state),
        )

    def recover_after_actor_action(
        self,
        *,
        current_turn: int,
        battle_slot: int,
    ) -> tuple["FoxParticipantRuntime | None",RoundRecovery]:
        """Source post-action recovery; expiry actor already used reduced powers."""
        result=resolve_round_recovery(
            self.state,
            current_turn=int(current_turn),
            battle_slot=int(battle_slot),
        )
        if result.recovered:
            return None,result
        return FoxParticipantRuntime(self.source_profile,result.state),result

    def battle_exit_state(self) -> FoxState:
        return resolve_battle_exit(self.state)


@dataclass(frozen=True)
class BecomeFoxRuntimeOverlay:
    """Only currently active FOXROUND targets are persisted."""

    runtime_by_participant_id: Mapping[str,FoxParticipantRuntime]

    def __post_init__(self) -> None:
        normalized={}
        for raw_id,runtime in self.runtime_by_participant_id.items():
            participant_id=str(raw_id)
            if not participant_id:
                raise ValueError("BecomeFox overlay participant id must be non-empty")
            if participant_id in normalized:
                raise ValueError("BecomeFox overlay participant ids must be unique")
            if not isinstance(runtime,FoxParticipantRuntime):
                raise TypeError("BecomeFox overlay runtime has wrong type")
            normalized[participant_id]=runtime
        object.__setattr__(
            self,"runtime_by_participant_id",MappingProxyType(normalized)
        )

    @classmethod
    def empty(cls) -> "BecomeFoxRuntimeOverlay":
        return cls({})

    def with_transformed(
        self,
        participant_id: str,
        runtime: FoxParticipantRuntime,
    ) -> "BecomeFoxRuntimeOverlay":
        """Success may refresh an already-foxed target's FOXROUND marker."""
        participant_id=str(participant_id)
        if not participant_id:
            raise ValueError("BecomeFox target participant id required")
        if not isinstance(runtime,FoxParticipantRuntime):
            raise TypeError("BecomeFox transformed runtime has wrong type")
        values=dict(self.runtime_by_participant_id)
        values[participant_id]=runtime
        return BecomeFoxRuntimeOverlay(values)

    def prepare_actor_action(
        self,
        participant_id: str,
    ) -> tuple["BecomeFoxRuntimeOverlay",FoxParticipantRuntime | None]:
        participant_id=str(participant_id)
        current=self.runtime_by_participant_id.get(participant_id)
        if current is None:
            return self,None
        prepared=current.prepare_actor_action()
        values=dict(self.runtime_by_participant_id)
        values[participant_id]=prepared
        return BecomeFoxRuntimeOverlay(values),prepared

    def recover_after_actor_action(
        self,
        participant_id: str,
        *,
        current_turn: int,
        battle_slot: int,
    ) -> tuple["BecomeFoxRuntimeOverlay",RoundRecovery | None]:
        participant_id=str(participant_id)
        current=self.runtime_by_participant_id.get(participant_id)
        if current is None:
            return self,None
        next_runtime,recovery=current.recover_after_actor_action(
            current_turn=int(current_turn),
            battle_slot=int(battle_slot),
        )
        values=dict(self.runtime_by_participant_id)
        if next_runtime is None:
            values.pop(participant_id,None)
        else:
            values[participant_id]=next_runtime
        return BecomeFoxRuntimeOverlay(values),recovery

    def retain_participants(
        self,
        participant_ids,
    ) -> "BecomeFoxRuntimeOverlay":
        allowed={str(value) for value in participant_ids}
        return BecomeFoxRuntimeOverlay({
            participant_id:runtime
            for participant_id,runtime in self.runtime_by_participant_id.items()
            if participant_id in allowed
        })

    def teardown(self) -> "BecomeFoxRuntimeOverlay":
        return BecomeFoxRuntimeOverlay.empty()


__all__=[
    "BECOMEFOX_SOURCE_PROFILES",
    "PROFILE_GAVIN","PROFILE_IRIS","PROFILE_BISMARCK",
    "FoxParticipantRuntime","BecomeFoxRuntimeOverlay",
    "arrange_guard_active","petin_accessor_profile",
]
