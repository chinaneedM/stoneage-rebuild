"""Battle-local SetMagicPet state and explicit MultiList RNG ownership."""

from __future__ import annotations

from dataclasses import dataclass, replace
from types import MappingProxyType
from typing import Mapping

from tools.stoneage_setmagicpet_model import (
    SetMagicPetOption,
    SetMagicPetSourceDomain,
    SetMagicPetTargetState,
    apply_setmagicpet_buff,
    recalculate_setmagicpet_fixed_stats,
    tick_setmagicpet_turns,
)


@dataclass(frozen=True)
class SetMagicPetActionRolls:
    """Only descendant BATTLE_MultiList dead-single retarget owns RNG."""

    retarget_draws_0_9: tuple[int,...] = ()

    def __post_init__(self) -> None:
        draws=tuple(int(value) for value in self.retarget_draws_0_9)
        if any(not 0 <= value <= 9 for value in draws):
            raise ValueError("SetMagicPet retarget draws must be in 0..9")
        object.__setattr__(self,"retarget_draws_0_9",draws)

    @property
    def is_empty(self) -> bool:
        return not self.retarget_draws_0_9


@dataclass(frozen=True)
class PreparedSetMagicPetPowers:
    """Post-SetMagicPet, pre-Weaken fixed powers prepared for one command."""

    attack: int
    defense: int
    dexterity: int

    def __post_init__(self) -> None:
        for name in ("attack","defense","dexterity"):
            value=int(getattr(self,name))
            if not 0 <= value < 2**31:
                raise ValueError(
                    "prepared SetMagicPet powers require nonnegative int32"
                )
            object.__setattr__(self,name,value)


@dataclass(frozen=True)
class SetMagicPetParticipantRuntime:
    """Source work counters plus already prepared current-command powers."""

    state: SetMagicPetTargetState = SetMagicPetTargetState()
    prepared_powers: PreparedSetMagicPetPowers | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.state,SetMagicPetTargetState):
            raise TypeError("SetMagicPet participant state has wrong type")
        if (
            self.prepared_powers is not None
            and not isinstance(self.prepared_powers,PreparedSetMagicPetPowers)
        ):
            raise TypeError("SetMagicPet prepared powers have wrong type")

    @property
    def blocks_new_magicpet_buff(self) -> bool:
        return self.state.blocks_new_magicpet_buff

    @property
    def supported_tgh_active(self) -> bool:
        return bool(self.state.tgh_turn > 0)

    def after_state(self,state:SetMagicPetTargetState):
        return replace(self,state=state)


@dataclass(frozen=True)
class SetMagicPetRoundOverlay:
    runtime_by_participant_id: Mapping[str,SetMagicPetParticipantRuntime]

    def __post_init__(self) -> None:
        normalized={}
        for participant_id,runtime in self.runtime_by_participant_id.items():
            participant_id=str(participant_id)
            if not participant_id:
                raise ValueError("SetMagicPet overlay participant id cannot be empty")
            if not isinstance(runtime,SetMagicPetParticipantRuntime):
                raise TypeError(
                    "SetMagicPet overlay values must be participant runtimes"
                )
            normalized[participant_id]=runtime
        object.__setattr__(
            self,"runtime_by_participant_id",MappingProxyType(normalized)
        )


@dataclass(frozen=True)
class SetMagicPetTurnTick:
    before: SetMagicPetTargetState
    after: SetMagicPetTargetState
    expired_kinds: tuple[str,...]


def tick_setmagicpet_runtime(
    runtime:SetMagicPetParticipantRuntime,
) -> tuple[SetMagicPetParticipantRuntime,SetMagicPetTurnTick | None]:
    """Mirror the SetDuck/STR/TGH/DEX BATTLE_StatusSeq countdown block."""
    if not isinstance(runtime,SetMagicPetParticipantRuntime):
        raise TypeError("SetMagicPet runtime has wrong type")
    before=runtime.state
    counters=(
        before.duck_turn,before.str_turn,before.tgh_turn,before.dex_turn
    )
    if not any(int(value)>0 for value in counters):
        return runtime,None
    after=tick_setmagicpet_turns(before)
    expired=tuple(
        kind
        for kind,old,new in (
            ("DUCK",before.duck_turn,after.duck_turn),
            ("STR",before.str_turn,after.str_turn),
            ("TGH",before.tgh_turn,after.tgh_turn),
            ("DEX",before.dex_turn,after.dex_turn),
        )
        if int(old)>0 and int(new)==0
    )
    return runtime.after_state(after),SetMagicPetTurnTick(before,after,expired)


def apply_setmagicpet_option(
    runtime:SetMagicPetParticipantRuntime,
    option:SetMagicPetOption,
) -> tuple[SetMagicPetParticipantRuntime,bool]:
    """Apply the non-HP source work-state branch to one resolved target."""
    if not isinstance(runtime,SetMagicPetParticipantRuntime):
        raise TypeError("SetMagicPet runtime has wrong type")
    if not isinstance(option,SetMagicPetOption):
        raise TypeError("SetMagicPet option has wrong type")
    if option.kind == "HP":
        raise SetMagicPetSourceDomain(
            "HP SetMagicPet execution is outside the positive ID-601 runtime"
        )
    result=apply_setmagicpet_buff(option,(runtime.state,))
    return runtime.after_state(result.targets[0]),bool(result.applied[0])


def prepare_setmagicpet_powers(
    *,
    baseline_attack:int,
    baseline_defense:int,
    baseline_quick:int,
    runtime:SetMagicPetParticipantRuntime,
) -> PreparedSetMagicPetPowers | None:
    """Prepare source-ordered magic-pet powers for the next command.

    The admitted runtime has no suit percentage/additive modifiers, riding or
    profession/wolf/fear modifiers. In this bounded domain baseline_defense is
    also the source's saved pre-suit mtgh basis. Only positively referenced
    recovered ID 601 (TGH) is executable; STR/DEX may appear as blocking input
    evidence but are not silently executed here.
    """
    if not isinstance(runtime,SetMagicPetParticipantRuntime):
        raise TypeError("SetMagicPet runtime has wrong type")
    state=runtime.state
    if state.str_turn>0 or state.dex_turn>0:
        raise SetMagicPetSourceDomain(
            "active STR/DEX SetMagicPet states are outside ID-601 runtime"
        )
    if state.tgh_turn<=0:
        return None
    stats=recalculate_setmagicpet_fixed_stats(
        fixed_str=int(baseline_attack),
        fixed_tough=int(baseline_defense),
        fixed_dex=int(baseline_quick),
        pre_suit_tough=int(baseline_defense),
        state=state,
    )
    return PreparedSetMagicPetPowers(
        stats.fixed_str,stats.fixed_tough,stats.fixed_dex
    )
