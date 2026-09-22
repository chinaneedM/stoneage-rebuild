#!/usr/bin/env python3
"""Stable common physical DamageReact core.

The three pinned descendant lineages agree on the unguarded base reaction
family and priority:
    VANISH > ABSROB > REFLEC > NONE

This module intentionally excludes ride-pet HP sharing and later guarded
TRAP/ACUPUNCTURE families. It models only the no-ride physical transaction
that is common across all three fixed sources.
"""

from __future__ import annotations

from dataclasses import dataclass, replace


DAMAGE_REACT_NONE = 0
DAMAGE_REACT_ABSROB = 1
DAMAGE_REACT_REFLEC = 2
DAMAGE_REACT_VANISH = 3

DAMAGE_REACT_NAME_BY_KIND = {
    DAMAGE_REACT_NONE: "none",
    DAMAGE_REACT_ABSROB: "absorb",
    DAMAGE_REACT_REFLEC: "reflect",
    DAMAGE_REACT_VANISH: "vanish",
}


@dataclass(frozen=True)
class BaseDamageReactState:
    absorb: int = 0
    reflect: int = 0
    vanish: int = 0

    def __post_init__(self) -> None:
        for name in ("absorb","reflect","vanish"):
            value=int(getattr(self,name))
            if value < 0:
                raise ValueError(f"{name} damage-react count cannot be negative")
            object.__setattr__(self,name,value)


@dataclass(frozen=True)
class BaseDamageReactResolution:
    state_before: BaseDamageReactState
    state_after: BaseDamageReactState
    selected_kind: int
    effective_kind: int
    raw_damage: int
    attacker_hp_before: int
    attacker_hp_after: int
    defender_hp_before: int
    defender_hp_after: int
    damage_target: str
    wakeup_target: str | None
    charge_consumed: bool
    reflect_blocked_by_throwing_weapon: bool

    def __post_init__(self) -> None:
        if self.damage_target not in {"none","attacker","defender"}:
            raise ValueError("damage_target must be none/attacker/defender")
        if self.wakeup_target not in {None,"attacker","defender"}:
            raise ValueError("wakeup_target must be attacker/defender/None")


@dataclass(frozen=True)
class BaseComboMemberDamageReactResolution:
    """One stable Combo member reaction before final aggregate settlement."""

    state_before: BaseDamageReactState
    state_after: BaseDamageReactState
    selected_kind: int
    effective_kind: int
    raw_damage: int
    accumulated_damage: int
    attacker_hp_before: int
    attacker_hp_after: int
    defender_hp_before: int
    defender_hp_after: int
    wakeup_target: str | None
    charge_consumed: bool
    reflect_blocked_by_throwing_weapon: bool

    def __post_init__(self) -> None:
        if self.wakeup_target not in {None,"attacker","defender"}:
            raise ValueError("wakeup_target must be attacker/defender/None")
        if int(self.accumulated_damage) < 0:
            raise ValueError("accumulated_damage cannot be negative")


def base_damage_react_kind(state: BaseDamageReactState) -> int:
    """Mirror BATTLE_GetDamageReact priority."""
    if not isinstance(state,BaseDamageReactState):
        raise TypeError("state must be BaseDamageReactState")
    if int(state.vanish)>0:
        return DAMAGE_REACT_VANISH
    if int(state.absorb)>0:
        return DAMAGE_REACT_ABSROB
    if int(state.reflect)>0:
        return DAMAGE_REACT_REFLEC
    return DAMAGE_REACT_NONE


def base_damage_react_active(state: BaseDamageReactState) -> bool:
    return base_damage_react_kind(state) != DAMAGE_REACT_NONE


def base_damage_react_blocks_main_continuation(
    attacker_state: BaseDamageReactState,
    defender_state: BaseDamageReactState,
) -> bool:
    """BATTLE_Attack disables continuation when either side has a reaction."""
    return (
        base_damage_react_active(attacker_state)
        or base_damage_react_active(defender_state)
    )


def apply_base_magic_def(
    state: BaseDamageReactState,
    *,
    kind: int,
    count: int,
) -> BaseDamageReactState:
    """Mirror BATTLE_MultiMagicDef's direct MagicDefTbl[kind]=count write."""
    if not isinstance(state,BaseDamageReactState):
        raise TypeError("state must be BaseDamageReactState")
    kind=int(kind)
    count=int(count)
    if count < 0:
        raise ValueError("magic-defense count cannot be negative")
    if kind == DAMAGE_REACT_ABSROB:
        return replace(state,absorb=count)
    if kind == DAMAGE_REACT_REFLEC:
        return replace(state,reflect=count)
    if kind == DAMAGE_REACT_VANISH:
        return replace(state,vanish=count)
    raise ValueError("common magic-defense kind must be ABSROB/REFLEC/VANISH")


def resolve_base_combo_member_damage_react(
    state: BaseDamageReactState,
    *,
    raw_damage: int,
    attacker_hp: int,
    attacker_max_hp: int,
    defender_hp: int,
    defender_max_hp: int,
    attacker_uses_throwing_weapon: bool = False,
) -> BaseComboMemberDamageReactResolution:
    """Mirror BATTLE_Combo's per-member reaction/accumulation split."""
    if not isinstance(state,BaseDamageReactState):
        raise TypeError("state must be BaseDamageReactState")
    raw_damage=int(raw_damage)
    attacker_hp=int(attacker_hp)
    attacker_max_hp=int(attacker_max_hp)
    defender_hp=int(defender_hp)
    defender_max_hp=int(defender_max_hp)
    if raw_damage < 0:
        raise ValueError("raw_damage cannot be negative")
    if not 0 <= attacker_hp <= attacker_max_hp:
        raise ValueError("attacker HP must be within max HP")
    if not 0 <= defender_hp <= defender_max_hp:
        raise ValueError("defender HP must be within max HP")

    selected=base_damage_react_kind(state)
    if raw_damage <= 0:
        return BaseComboMemberDamageReactResolution(
            state,state,selected,DAMAGE_REACT_NONE,0,0,
            attacker_hp,attacker_hp,defender_hp,defender_hp,
            None,False,False,
        )

    # Combo pre-fetches REFLEC before its throwing-weapon gate. When throwing
    # bypasses reflection, damage is deferred to the final aggregate and the
    # reflect charge remains, but the stale react kind still wakes attacker.
    if selected == DAMAGE_REACT_REFLEC and bool(attacker_uses_throwing_weapon):
        return BaseComboMemberDamageReactResolution(
            state,state,selected,DAMAGE_REACT_NONE,raw_damage,raw_damage,
            attacker_hp,attacker_hp,defender_hp,defender_hp,
            "attacker",False,True,
        )

    if selected == DAMAGE_REACT_NONE:
        return BaseComboMemberDamageReactResolution(
            state,state,selected,DAMAGE_REACT_NONE,raw_damage,raw_damage,
            attacker_hp,attacker_hp,defender_hp,defender_hp,
            "defender",False,False,
        )

    immediate=resolve_base_damage_react(
        state,
        raw_damage=raw_damage,
        attacker_hp=attacker_hp,
        attacker_max_hp=attacker_max_hp,
        defender_hp=defender_hp,
        defender_max_hp=defender_max_hp,
        attacker_uses_throwing_weapon=False,
    )
    return BaseComboMemberDamageReactResolution(
        immediate.state_before,
        immediate.state_after,
        immediate.selected_kind,
        immediate.effective_kind,
        raw_damage,
        0,
        immediate.attacker_hp_before,
        immediate.attacker_hp_after,
        immediate.defender_hp_before,
        immediate.defender_hp_after,
        immediate.wakeup_target,
        immediate.charge_consumed,
        False,
    )


def resolve_base_damage_react(
    state: BaseDamageReactState,
    *,
    raw_damage: int,
    attacker_hp: int,
    attacker_max_hp: int,
    defender_hp: int,
    defender_max_hp: int,
    attacker_uses_throwing_weapon: bool = False,
) -> BaseDamageReactResolution:
    """Resolve one no-ride physical BATTLE_DamageSub transaction.

    Important source properties:
    - raw damage <= 0 returns before any reaction is consumed;
    - REFLEC is bypassed by throwing weapons without consuming its charge;
    - ABSROB heals by the positive physical magnitude;
    - VANISH leaves HP unchanged;
    - the returned physical magnitude stays positive for ABSROB/VANISH/REFLEC,
      so later status checks must not infer eligibility from HP delta.
    """
    if not isinstance(state,BaseDamageReactState):
        raise TypeError("state must be BaseDamageReactState")
    raw_damage=int(raw_damage)
    attacker_hp=int(attacker_hp)
    attacker_max_hp=int(attacker_max_hp)
    defender_hp=int(defender_hp)
    defender_max_hp=int(defender_max_hp)
    if raw_damage < 0:
        raise ValueError("raw_damage cannot be negative")
    if attacker_max_hp < 0 or defender_max_hp < 0:
        raise ValueError("max HP cannot be negative")
    if not 0 <= attacker_hp <= attacker_max_hp:
        raise ValueError("attacker HP must be within max HP")
    if not 0 <= defender_hp <= defender_max_hp:
        raise ValueError("defender HP must be within max HP")

    selected=base_damage_react_kind(state)
    if raw_damage <= 0:
        return BaseDamageReactResolution(
            state_before=state,
            state_after=state,
            selected_kind=selected,
            effective_kind=DAMAGE_REACT_NONE,
            raw_damage=0,
            attacker_hp_before=attacker_hp,
            attacker_hp_after=attacker_hp,
            defender_hp_before=defender_hp,
            defender_hp_after=defender_hp,
            damage_target="none",
            wakeup_target=None,
            charge_consumed=False,
            reflect_blocked_by_throwing_weapon=False,
        )

    state_after=state
    attacker_after=attacker_hp
    defender_after=defender_hp
    effective=selected
    target="defender"
    wakeup="defender"
    consumed=False
    blocked_reflect=False

    if selected == DAMAGE_REACT_VANISH:
        state_after=replace(state,vanish=max(int(state.vanish)-1,0))
        target="none"
        wakeup=None
        consumed=True
    elif selected == DAMAGE_REACT_ABSROB:
        state_after=replace(state,absorb=max(int(state.absorb)-1,0))
        defender_after=min(defender_max_hp,defender_hp+raw_damage)
        target="none"
        wakeup=None
        consumed=True
    elif selected == DAMAGE_REACT_REFLEC:
        if bool(attacker_uses_throwing_weapon):
            effective=DAMAGE_REACT_NONE
            blocked_reflect=True
            defender_after=max(0,defender_hp-raw_damage)
        else:
            state_after=replace(state,reflect=max(int(state.reflect)-1,0))
            attacker_after=max(0,attacker_hp-raw_damage)
            target="attacker"
            wakeup="attacker"
            consumed=True
    else:
        defender_after=max(0,defender_hp-raw_damage)

    return BaseDamageReactResolution(
        state_before=state,
        state_after=state_after,
        selected_kind=selected,
        effective_kind=effective,
        raw_damage=raw_damage,
        attacker_hp_before=attacker_hp,
        attacker_hp_after=min(attacker_after,attacker_max_hp),
        defender_hp_before=defender_hp,
        defender_hp_after=min(defender_after,defender_max_hp),
        damage_target=target,
        wakeup_target=wakeup,
        charge_consumed=consumed,
        reflect_blocked_by_throwing_weapon=blocked_reflect,
    )
