#!/usr/bin/env python3
"""Guarded descendant enemy ReHP reference boundary.

This module models the convergent `_PRO_BATTLEENEMYSKILL` ReHP callback/effect
without pretending its guarded enum number is portable across descendants.
The recovered25 binary/build profile is not identified, so callers must choose
an evidenced descendant command profile explicitly or remain fail-closed.

The enemy-caster effect is source-shaped after BATTLE_TargetAdjust has already
succeeded.  Any default-opponent retarget RNG therefore belongs to the caller
and occurs before the RNG represented here.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from types import MappingProxyType
from typing import Mapping


CALLBACK_NAME = "ENEMYSKILL_ReHP"
COMMAND_NAME = "BATTLE_COM_S_ENEMYREHP"
PROFILE_GAVIN_IRIS = "gavin-iris-pinned"
PROFILE_BISMARCK = "bismarck-pinned"

# These values are profile-specific because guarded enum entries before ReHP
# differ between the pinned descendants.  They are not a recovered25 claim.
COMMAND_CODE_BY_PROFILE = MappingProxyType(
    {
        PROFILE_GAVIN_IRIS: 2014,
        PROFILE_BISMARCK: 2013,
    }
)


def enemy_rehp_command_code(profile: str) -> int:
    """Return an evidenced guarded command code; never guess a build profile."""

    profile = str(profile)
    try:
        return int(COMMAND_CODE_BY_PROFILE[profile])
    except KeyError as exc:
        raise ValueError(
            "enemy ReHP command code requires an evidenced descendant profile"
        ) from exc


@dataclass(frozen=True)
class EnemyReHpAllyState:
    """A valid enemy-side battle entry visible to BATTLE_E_ENEMYREHP."""

    participant_id: str
    slot: int
    hp: int
    max_hp: int

    def __post_init__(self) -> None:
        participant_id = str(self.participant_id)
        slot = int(self.slot)
        hp = int(self.hp)
        max_hp = int(self.max_hp)
        if not participant_id:
            raise ValueError("enemy ReHP ally id must be non-empty")
        if not 10 <= slot < 20:
            raise ValueError("enemy ReHP ally slot must be in 10..19")
        if max_hp < 0:
            raise ValueError("enemy ReHP max_hp cannot be negative")
        if not 0 <= hp <= max_hp:
            raise ValueError("enemy ReHP hp must be within max_hp")
        object.__setattr__(self, "participant_id", participant_id)
        object.__setattr__(self, "slot", slot)
        object.__setattr__(self, "hp", hp)
        object.__setattr__(self, "max_hp", max_hp)

    @property
    def eligible(self) -> bool:
        # Fixed source: HP > 0 && HP < WORKMAXHP * 2 / 3, with C integer math.
        return self.hp > 0 and self.hp < (self.max_hp * 2) // 3


@dataclass(frozen=True)
class EnemyReHpRolls:
    """Concrete RAND results, in fixed-source consumption order.

    target_index is RAND(0, eligible_count-1), base_power is
    RAND(100, target_max_hp), and heal_variance is the later
    BATTLE_MultiRecovery RAND(power*0.9, power*1.1) result after integer
    assignment.  Values that are not consumed must remain None.
    """

    target_index: int | None = None
    base_power: int | None = None
    heal_variance: int | None = None

    def __post_init__(self) -> None:
        for name in ("target_index", "base_power", "heal_variance"):
            value = getattr(self, name)
            if value is not None:
                object.__setattr__(self, name, int(value))

    @property
    def is_empty(self) -> bool:
        return (
            self.target_index is None
            and self.base_power is None
            and self.heal_variance is None
        )


@dataclass(frozen=True)
class EnemyReHpResolution:
    success: bool
    fallback_to_attack: bool
    adjusted_attack_target_slot: int
    eligible_slots: tuple[int, ...]
    healed_slot: int | None
    base_power: int | None
    reported_heal: int
    effective_heal: int
    hp_before: int | None
    hp_after: int | None
    allies_after: Mapping[int, EnemyReHpAllyState]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "allies_after",
            MappingProxyType(
                {int(slot): state for slot, state in self.allies_after.items()}
            ),
        )


def _normalize_allies(
    allies_by_slot: Mapping[int, EnemyReHpAllyState],
) -> dict[int, EnemyReHpAllyState]:
    normalized: dict[int, EnemyReHpAllyState] = {}
    for raw_slot, state in allies_by_slot.items():
        slot = int(raw_slot)
        if not isinstance(state, EnemyReHpAllyState):
            raise TypeError("enemy ReHP ally state has wrong type")
        if slot != state.slot:
            raise ValueError("enemy ReHP ally mapping key/slot mismatch")
        if slot in normalized:
            raise ValueError("duplicate enemy ReHP ally slot")
        normalized[slot] = state
    return normalized


def _require_unconsumed(rolls: EnemyReHpRolls) -> None:
    if not rolls.is_empty:
        raise ValueError("enemy ReHP failure path must not consume effect RNG")


def resolve_enemy_rehp_effect(
    *,
    adjusted_attack_target_slot: int,
    allies_by_slot: Mapping[int, EnemyReHpAllyState],
    rolls: EnemyReHpRolls,
    caster_mode_ready: bool = True,
) -> EnemyReHpResolution:
    """Resolve the enemy-caster branch after successful BATTLE_TargetAdjust.

    If the ReHP effect cannot run, the fixed dispatcher falls back to ordinary
    BATTLE_Attack against adjusted_attack_target_slot.  That fallback attack is
    intentionally not executed here.
    """

    adjusted = int(adjusted_attack_target_slot)
    if not 0 <= adjusted < 10:
        raise ValueError("enemy ReHP adjusted attack target must be in 0..9")
    if not isinstance(rolls, EnemyReHpRolls):
        raise TypeError("enemy ReHP rolls have wrong type")

    allies = _normalize_allies(allies_by_slot)
    eligible = tuple(slot for slot in range(10, 20) if slot in allies and allies[slot].eligible)

    if not bool(caster_mode_ready) or not eligible:
        _require_unconsumed(rolls)
        return EnemyReHpResolution(
            success=False,
            fallback_to_attack=True,
            adjusted_attack_target_slot=adjusted,
            eligible_slots=eligible,
            healed_slot=None,
            base_power=None,
            reported_heal=0,
            effective_heal=0,
            hp_before=None,
            hp_after=None,
            allies_after=allies,
        )

    if rolls.target_index is None:
        raise ValueError("enemy ReHP target-selection RAND result is required")
    target_index = int(rolls.target_index)
    if not 0 <= target_index < len(eligible):
        raise ValueError("enemy ReHP target-selection RAND result out of range")
    healed_slot = eligible[target_index]
    target = allies[healed_slot]

    # RAND(100, max_hp) is only source-safe when its lower bound does not exceed
    # its upper bound.  Do not invent reversed-range semantics for recovered25.
    if target.max_hp < 100:
        raise ValueError("enemy ReHP RAND(100,max_hp) reversed range is unresolved")
    if rolls.base_power is None:
        raise ValueError("enemy ReHP base-power RAND result is required")
    power = int(rolls.base_power)
    if not 100 <= power <= target.max_hp:
        raise ValueError("enemy ReHP base-power RAND result out of range")

    if rolls.heal_variance is None:
        raise ValueError("enemy ReHP MultiRecovery RAND result is required")
    reported = int(rolls.heal_variance)
    lower = (power * 9) // 10
    upper = (power * 11) // 10
    if not lower <= reported <= upper:
        raise ValueError("enemy ReHP MultiRecovery RAND result out of range")

    before = target.hp
    after = min(target.max_hp, before + reported)
    allies[healed_slot] = replace(target, hp=after)
    return EnemyReHpResolution(
        success=True,
        fallback_to_attack=False,
        adjusted_attack_target_slot=adjusted,
        eligible_slots=eligible,
        healed_slot=healed_slot,
        base_power=power,
        reported_heal=reported,
        effective_heal=after - before,
        hp_before=before,
        hp_after=after,
        allies_after=allies,
    )
