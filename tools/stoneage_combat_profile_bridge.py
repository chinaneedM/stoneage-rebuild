#!/usr/bin/env python3
"""Evidence-bounded adapters into BattleCombatProfile.

This module closes only mappings supported by the stable server/status bridge:
- player v1 status dexterity -> WORKFIXDEX numeric value;
- player v1 status luck -> WORKFIXLUCK;
- player v1 status earth/water/fire/wind -> nonnegative WORKFIX attributes;
- reconstructed pet/enemy birth internal DEX -> WORKFIXDEX;
- reconstructed birth raw attributes -> CHAR_initcharWorkInt fixed-attribute
  projection, then the same nonnegative clamp used by BATTLE_GetAttr.

A generic persisted PetActor client-view is intentionally insufficient for
fixed DEX because its quick field is WORKQUICK, not WORKFIXDEX.
"""

from __future__ import annotations

from types import MappingProxyType
from typing import Mapping, Sequence

from tools.stoneage_battle_round_model import BattleCombatProfile
from tools.stoneage_enemy_spawn_model import SpawnedEnemy
from tools.stoneage_singleplayer_battle import BattleSession
from tools.stoneage_singleplayer_domain import PlayerState
from tools.stoneage_tw10_25_bridge_model import (
    PetBirthBridgeState,
    ReconstructedPetBridgeState,
)


def _required_int(values: Mapping[str, object], key: str, *, subject: str) -> int:
    if key not in values:
        raise ValueError(f"{subject} requires field {key}")
    return int(values[key])


def fixed_attribute_projection(
    earth: int,
    water: int,
    fire: int,
    wind: int,
) -> tuple[int, int, int, int]:
    """Mirror stable CHAR_initcharWorkInt + BATTLE_GetAttr clamping."""
    attrs = [int(earth), int(water), int(fire), int(wind)]
    for index in range(4):
        if attrs[index] > 0:
            attrs[(index + 2) % 4] = -attrs[index]
    return tuple(max(0, value) for value in attrs)


def player_combat_profile(
    state: PlayerState,
    *,
    weapon_critical: int,
) -> BattleCombatProfile:
    """Bridge a v1 player status record into the stable battle fixed profile.

    The descendant status producer sends CHAR_DEX/100 as the displayed
    dexterity field, while CHAR_initcharWorkInt sets WORKFIXDEX to
    CHAR_DEX*0.01. For integer stored CHAR_DEX these are the same numeric
    projection.

    Luck and four elements are sent from their WORKFIX fields directly.
    """
    fields = state.fields
    dexterity = _required_int(fields, "dexterity", subject="player combat profile")
    luck = _required_int(fields, "luck", subject="player combat profile")
    elements = tuple(
        _required_int(fields, key, subject="player combat profile")
        for key in ("earth", "water", "fire", "wind")
    )
    if dexterity < 0:
        raise ValueError("player dexterity cannot be negative")
    if any(value < 0 for value in elements):
        raise ValueError(
            "v1 player status elements must already be nonnegative WORKFIX values"
        )
    return BattleCombatProfile(
        fixed_dex=dexterity,
        fixed_luck=luck,
        earth=elements[0],
        water=elements[1],
        fire=elements[2],
        wind=elements[3],
        weapon_critical=int(weapon_critical),
    )


def birth_combat_profile(
    birth: PetBirthBridgeState,
) -> BattleCombatProfile:
    """Bridge reconstructed birth internals into an unmodified pet/enemy profile."""
    fixed_dex = int(int(birth.internal_dexterity) * 0.01)
    earth, water, fire, wind = fixed_attribute_projection(
        birth.earth,
        birth.water,
        birth.fire,
        birth.wind,
    )
    return BattleCombatProfile(
        fixed_dex=fixed_dex,
        fixed_luck=0,
        earth=earth,
        water=water,
        fire=fire,
        wind=wind,
        weapon_critical=0,
    )


def reconstructed_pet_combat_profile(
    state: ReconstructedPetBridgeState,
) -> BattleCombatProfile:
    return birth_combat_profile(state.birth)


def spawned_enemy_combat_profile(
    spawn: SpawnedEnemy,
) -> BattleCombatProfile:
    profile = birth_combat_profile(spawn.birth)
    if int(spawn.participant.quick) != int(profile.fixed_dex):
        raise ValueError(
            "spawn participant QUICK no longer matches birth WORKFIXDEX projection"
        )
    return profile


def group_battle_combat_profiles(
    session: BattleSession,
    *,
    player_state: PlayerState,
    player_weapon_critical: int,
    spawned_enemies: Sequence[SpawnedEnemy],
    allied_pet_sources: Sequence[ReconstructedPetBridgeState] = (),
) -> Mapping[str, BattleCombatProfile]:
    """Build profiles from provenance-bearing sources for one group battle."""
    profiles: dict[str, BattleCombatProfile] = {
        session.player.participant_id: player_combat_profile(
            player_state,
            weapon_critical=player_weapon_critical,
        )
    }

    pet_sources = tuple(allied_pet_sources)
    pet_by_slot = {int(source.pet_slot): source for source in pet_sources}
    if len(pet_by_slot) != len(pet_sources):
        raise ValueError("duplicate allied pet source slot")
    for participant in session.allied_pets:
        if participant.source_pet_slot is None:
            raise ValueError(
                f"allied participant {participant.participant_id} lacks source pet slot"
            )
        slot = int(participant.source_pet_slot)
        if slot not in pet_by_slot:
            raise ValueError(
                f"missing provenance-bearing reconstructed source for pet slot {slot}"
            )
        source = pet_by_slot[slot]
        if int(source.template_ref.template_id) != int(participant.source_template_id):
            raise ValueError(f"pet slot {slot} template identity drift")
        if int(source.variant_ref.template_id) != int(participant.source_variant_id):
            raise ValueError(f"pet slot {slot} variant identity drift")
        profiles[participant.participant_id] = reconstructed_pet_combat_profile(source)

    enemy_sources = tuple(spawned_enemies)
    spawn_by_id = {
        spawn.participant.participant_id: spawn
        for spawn in enemy_sources
    }
    if len(spawn_by_id) != len(enemy_sources):
        raise ValueError("duplicate spawned enemy participant id")
    for participant in session.enemies:
        if participant.participant_id not in spawn_by_id:
            raise ValueError(
                f"missing provenance-bearing spawn source for {participant.participant_id}"
            )
        spawn = spawn_by_id[participant.participant_id]
        if spawn.participant.source_variant_id != participant.source_variant_id:
            raise ValueError(
                f"enemy {participant.participant_id} variant identity drift"
            )
        if spawn.participant.source_template_id != participant.source_template_id:
            raise ValueError(
                f"enemy {participant.participant_id} template identity drift"
            )
        profiles[participant.participant_id] = spawned_enemy_combat_profile(spawn)

    expected = {
        participant.participant_id
        for participant in (
            session.player,
            *session.allied_pets,
            *session.enemies,
        )
    }
    if set(profiles) != expected:
        missing = sorted(expected - set(profiles))
        extra = sorted(set(profiles) - expected)
        raise ValueError(f"combat profile coverage mismatch; missing={missing}, extra={extra}")

    return MappingProxyType(profiles)
