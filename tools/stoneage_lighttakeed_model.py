#!/usr/bin/env python3
"""Pure Lighttakeed reaction-transfer layer over the accepted DamageReact core.

This module does not calculate BATTLE_AttackSeq damage.  It receives that
already-resolved raw physical magnitude and mirrors only the source ordering
that is unique to BATTLE_COM_S_LIGHTTAKE:

1. inspect the defender's highest-priority DamageReact;
2. if it matches the Lighttakeed OPTION marker, neutralize local react before
   ordinary DamageSub, so the defender's charge is not consumed;
3. run ordinary physical settlement with no active reaction;
4. after settlement, overwrite the attacker's matching work counter with the
   defender's still-current count (gavin/iris) or that count + 1 (Bismarck);
5. if an active reaction does not match, demote Lighttakeed and let the normal
   DamageReact transaction own consumption/effect, with no transfer.
"""

from __future__ import annotations

from dataclasses import dataclass, replace

from tools.stoneage_battle_damage_react_model import (
    DAMAGE_REACT_ABSROB,
    DAMAGE_REACT_NONE,
    DAMAGE_REACT_REFLEC,
    DAMAGE_REACT_VANISH,
    BaseDamageReactResolution,
    BaseDamageReactState,
    base_damage_react_kind,
    resolve_base_damage_react,
)


PROFILE_GAVIN_IRIS_COPY = "gavin_iris_copy"
PROFILE_BISMARCK_COPY_PLUS_ONE = "bismarck_copy_plus_one"
LIGHTTAKEED_PROFILES = frozenset({
    PROFILE_GAVIN_IRIS_COPY,
    PROFILE_BISMARCK_COPY_PLUS_ONE,
})
LIGHTTAKEED_MARKERS = frozenset({
    DAMAGE_REACT_ABSROB,
    DAMAGE_REACT_REFLEC,
    DAMAGE_REACT_VANISH,
})


@dataclass(frozen=True)
class LighttakeedResolution:
    profile: str
    marker_kind: int
    selected_reaction_kind: int
    matched_reaction: bool
    lighttake_case_executed: bool
    demoted_to_ordinary: bool
    transferred_count: int | None
    attacker_state_before: BaseDamageReactState
    attacker_state_after: BaseDamageReactState
    defender_state_before: BaseDamageReactState
    defender_state_after: BaseDamageReactState
    damage_react_resolution: BaseDamageReactResolution


def _counter_value(state: BaseDamageReactState, kind: int) -> int:
    if kind == DAMAGE_REACT_ABSROB:
        return int(state.absorb)
    if kind == DAMAGE_REACT_REFLEC:
        return int(state.reflect)
    if kind == DAMAGE_REACT_VANISH:
        return int(state.vanish)
    raise ValueError("Lighttakeed marker must be ABSROB/REFLEC/VANISH")


def _overwrite_counter(
    state: BaseDamageReactState,
    *,
    kind: int,
    value: int,
) -> BaseDamageReactState:
    value=int(value)
    if value < 0:
        raise ValueError("Lighttakeed transferred count cannot be negative")
    if kind == DAMAGE_REACT_ABSROB:
        return replace(state,absorb=value)
    if kind == DAMAGE_REACT_REFLEC:
        return replace(state,reflect=value)
    if kind == DAMAGE_REACT_VANISH:
        return replace(state,vanish=value)
    raise ValueError("Lighttakeed marker must be ABSROB/REFLEC/VANISH")


def resolve_lighttakeed_reaction(
    *,
    profile: str,
    marker_kind: int,
    attacker_state: BaseDamageReactState,
    defender_state: BaseDamageReactState,
    raw_damage: int,
    attacker_hp: int,
    attacker_max_hp: int,
    defender_hp: int,
    defender_max_hp: int,
    attacker_uses_throwing_weapon: bool = False,
) -> LighttakeedResolution:
    """Resolve the Lighttake-specific reaction seam for one physical hit."""

    profile=str(profile)
    marker_kind=int(marker_kind)
    if profile not in LIGHTTAKEED_PROFILES:
        raise ValueError("Lighttakeed source profile must be explicit")
    if marker_kind not in LIGHTTAKEED_MARKERS:
        raise ValueError("Lighttakeed marker must be ABSROB/REFLEC/VANISH")
    if not isinstance(attacker_state,BaseDamageReactState):
        raise TypeError("attacker_state must be BaseDamageReactState")
    if not isinstance(defender_state,BaseDamageReactState):
        raise TypeError("defender_state must be BaseDamageReactState")

    selected=base_damage_react_kind(defender_state)
    matched=selected == marker_kind and selected != DAMAGE_REACT_NONE

    if selected != DAMAGE_REACT_NONE and not matched:
        ordinary=resolve_base_damage_react(
            defender_state,
            raw_damage=int(raw_damage),
            attacker_hp=int(attacker_hp),
            attacker_max_hp=int(attacker_max_hp),
            defender_hp=int(defender_hp),
            defender_max_hp=int(defender_max_hp),
            attacker_uses_throwing_weapon=bool(attacker_uses_throwing_weapon),
        )
        return LighttakeedResolution(
            profile=profile,
            marker_kind=marker_kind,
            selected_reaction_kind=selected,
            matched_reaction=False,
            lighttake_case_executed=False,
            demoted_to_ordinary=True,
            transferred_count=None,
            attacker_state_before=attacker_state,
            attacker_state_after=attacker_state,
            defender_state_before=defender_state,
            defender_state_after=ordinary.state_after,
            damage_react_resolution=ordinary,
        )

    # With no active reaction, or with a matching reaction neutralized by the
    # Lighttake prelude, DamageSub receives react==0.  Settle on an empty
    # reaction state, while retaining the defender's real counters separately.
    ordinary=resolve_base_damage_react(
        BaseDamageReactState(),
        raw_damage=int(raw_damage),
        attacker_hp=int(attacker_hp),
        attacker_max_hp=int(attacker_max_hp),
        defender_hp=int(defender_hp),
        defender_max_hp=int(defender_max_hp),
        attacker_uses_throwing_weapon=bool(attacker_uses_throwing_weapon),
    )

    attacker_after=attacker_state
    transferred=None
    if matched:
        transferred=_counter_value(defender_state,marker_kind)
        if profile == PROFILE_BISMARCK_COPY_PLUS_ONE:
            transferred += 1
        attacker_after=_overwrite_counter(
            attacker_state,
            kind=marker_kind,
            value=transferred,
        )

    return LighttakeedResolution(
        profile=profile,
        marker_kind=marker_kind,
        selected_reaction_kind=selected,
        matched_reaction=matched,
        lighttake_case_executed=True,
        demoted_to_ordinary=False,
        transferred_count=transferred,
        attacker_state_before=attacker_state,
        attacker_state_after=attacker_after,
        defender_state_before=defender_state,
        defender_state_after=defender_state,
        damage_react_resolution=ordinary,
    )


__all__ = [
    "LIGHTTAKEED_MARKERS",
    "LIGHTTAKEED_PROFILES",
    "PROFILE_BISMARCK_COPY_PLUS_ONE",
    "PROFILE_GAVIN_IRIS_COPY",
    "LighttakeedResolution",
    "resolve_lighttakeed_reaction",
]
