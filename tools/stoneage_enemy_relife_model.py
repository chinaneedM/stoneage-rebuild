#!/usr/bin/env python3
"""Pure recovered ENEMYSKILL_ReLife effect model."""

from __future__ import annotations
from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

CALLBACK_NAME="ENEMYSKILL_ReLife"
COMMAND_NAME="BATTLE_COM_S_ENEMYRELIFE"

@dataclass(frozen=True)
class EnemyReLifeDeadEntry:
    participant_id: str
    slot: int
    hp: int
    max_hp: int
    is_die: bool = True
    is_attacked: bool = True
    battle_mode_ready: bool = True
    rescue_mode: bool = False
    ultimate_exited: bool = False

    def __post_init__(self) -> None:
        participant_id=str(self.participant_id)
        slot=int(self.slot)
        hp=int(self.hp)
        max_hp=int(self.max_hp)
        if not participant_id:
            raise ValueError("ReLife entry participant id must be non-empty")
        if not 10 <= slot < 20:
            raise ValueError("ReLife enemy entry slot must be in 10..19")
        if hp < 0 or max_hp <= 0 or hp > max_hp:
            raise ValueError("ReLife entry HP bounds are invalid")
        object.__setattr__(self,"participant_id",participant_id)
        object.__setattr__(self,"slot",slot)
        object.__setattr__(self,"hp",hp)
        object.__setattr__(self,"max_hp",max_hp)

    @property
    def eligible(self) -> bool:
        return bool(
            self.hp == 0
            and self.is_die
            and self.is_attacked
            and self.battle_mode_ready
            and not self.rescue_mode
            and not self.ultimate_exited
        )

@dataclass(frozen=True)
class EnemyReLifeRolls:
    dead_target_index: int | None = None
    revive_amount_roll: int | None = None

    @property
    def is_empty(self) -> bool:
        return self.dead_target_index is None and self.revive_amount_roll is None

@dataclass(frozen=True)
class EnemyReLifeResolution:
    success: bool
    fallback_to_attack: bool
    candidate_slots: tuple[int,...]
    selected_slot: int | None = None
    selected_participant_id: str | None = None
    base_power: int | None = None
    revive_amount: int | None = None
    hp_before: int | None = None
    hp_after: int | None = None
    cleared_die_flag: bool = False

def _normalized_entries(
    entries_by_slot: Mapping[int,EnemyReLifeDeadEntry],
) -> Mapping[int,EnemyReLifeDeadEntry]:
    values={}
    participant_ids=set()
    for raw_slot,entry in entries_by_slot.items():
        slot=int(raw_slot)
        if not isinstance(entry,EnemyReLifeDeadEntry):
            raise TypeError("ReLife entries must be EnemyReLifeDeadEntry")
        if slot != int(entry.slot):
            raise ValueError("ReLife entry mapping slot drift")
        if slot in values:
            raise ValueError("duplicate ReLife entry slot")
        if entry.participant_id in participant_ids:
            raise ValueError("duplicate ReLife participant identity")
        participant_ids.add(entry.participant_id)
        values[slot]=entry
    return MappingProxyType(values)

def resolve_enemy_relife_effect(
    *,
    adjusted_attack_target_slot: int,
    entries_by_slot: Mapping[int,EnemyReLifeDeadEntry],
    rolls: EnemyReLifeRolls,
    caster_mode_ready: bool = True,
) -> EnemyReLifeResolution:
    """Resolve the helper after ordinary COM2 TargetAdjust succeeded."""
    adjusted_attack_target_slot=int(adjusted_attack_target_slot)
    if not 0 <= adjusted_attack_target_slot < 10:
        raise ValueError("ReLife adjusted attack carrier must be player-side 0..9")
    if not isinstance(rolls,EnemyReLifeRolls):
        raise TypeError("ReLife rolls have wrong type")
    if not caster_mode_ready:
        if not rolls.is_empty:
            raise ValueError("inactive ReLife caster cannot consume effect RNG")
        return EnemyReLifeResolution(False,True,())

    entries=_normalized_entries(entries_by_slot)
    candidates=tuple(
        slot for slot in range(10,20)
        if slot in entries and entries[slot].eligible
    )
    if not candidates:
        if not rolls.is_empty:
            raise ValueError("ReLife no-candidate path cannot consume effect RNG")
        return EnemyReLifeResolution(False,True,())

    if rolls.dead_target_index is None:
        raise ValueError("ReLife target-selection draw is required")
    selected_index=int(rolls.dead_target_index)
    if not 0 <= selected_index < len(candidates):
        raise ValueError(
            f"ReLife target-selection draw must be in 0..{len(candidates)-1}"
        )
    selected_slot=int(candidates[selected_index])
    entry=entries[selected_slot]
    base_power=int(entry.max_hp)//2

    if base_power == 0:
        if rolls.revive_amount_roll is not None:
            raise ValueError("ReLife zero-power branch cannot consume amount RNG")
        revive_amount=int(entry.max_hp)
    else:
        if rolls.revive_amount_roll is None:
            raise ValueError("ReLife nonzero power requires amount RNG")
        lower=(base_power*9)//10
        upper=(base_power*11)//10
        amount=int(rolls.revive_amount_roll)
        if not lower <= amount <= upper:
            raise ValueError(f"ReLife amount draw must be in {lower}..{upper}")
        revive_amount=max(1,amount)

    hp_after=min(int(entry.max_hp),int(entry.hp)+int(revive_amount))
    return EnemyReLifeResolution(
        success=True,
        fallback_to_attack=False,
        candidate_slots=candidates,
        selected_slot=selected_slot,
        selected_participant_id=entry.participant_id,
        base_power=base_power,
        revive_amount=revive_amount,
        hp_before=int(entry.hp),
        hp_after=hp_after,
        cleared_die_flag=True,
    )
