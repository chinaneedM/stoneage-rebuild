#!/usr/bin/env python3
"""Encounter-to-battle lifecycle boundary for the single-player reconstruction.

The recovered encounter chain selects identity and level. Exact enemy-count,
birth randoms, active allied pet selection, commands, AI, drops and final
battle result remain explicit caller inputs until their historical boundaries
are independently closed.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from types import MappingProxyType
from typing import Any, Mapping, Sequence

from tools.stoneage_battle_core_model import (
    early_action_value,
    effective_defense_newpower,
    effective_defense_preserved_old,
    physical_base_damage,
)
from tools.stoneage_singleplayer_domain import (
    EncounterRequest,
    GroupEncounterRequest,
    MapPosition,
    PetActor,
    PetSlot,
    PlayerState,
    SinglePlayerHistoricalDomain,
)
from tools.stoneage_tw10_25_bridge_model import (
    PetBirthBridgeState,
    PetTemplateBridge,
)
from tools.stoneage_tw10_25_encounter_bridge import EnemyVariantBridge


PLAYER_SIDE = "player"
ENEMY_SIDE = "enemy"


@dataclass(frozen=True)
class BattleParticipant:
    participant_id: str
    side: str
    kind: str
    level: int
    hp: int
    max_hp: int
    attack: int
    defense: int
    quick: int
    name: str
    fixed_vital: int | None = None
    source_variant_id: int | None = None
    source_template_id: int | None = None
    source_pet_slot: int | None = None

    def initiative(self, random_subtract: int) -> int:
        return early_action_value(self.quick, int(random_subtract))


@dataclass(frozen=True)
class BattleSession:
    origin_position: MapPosition
    encounter: EncounterRequest | GroupEncounterRequest
    player: BattleParticipant
    allied_pets: tuple[BattleParticipant, ...]
    enemies: tuple[BattleParticipant, ...]
    evidence_profile: str = "DESCENDANT_BATTLE_CORE_R1"


@dataclass(frozen=True)
class BattleOutcome:
    result: str
    player_updates: Mapping[str, Any]
    pet_updates: Mapping[int, Mapping[str, Any]]


@dataclass(frozen=True)
class BattleReturn:
    result: str
    world_position: MapPosition
    player: PlayerState
    pets: Mapping[PetSlot, PetActor]


def _require_int(fields: Mapping[str, Any], name: str) -> int:
    if name not in fields:
        raise ValueError(f"battle participant requires field {name}")
    return int(fields[name])


def _require_name(fields: Mapping[str, Any]) -> str:
    value = fields.get("name")
    if value is None:
        raise ValueError("battle participant requires name")
    return str(value)


def player_participant(state: PlayerState) -> BattleParticipant:
    fields = state.fields
    return BattleParticipant(
        participant_id="player",
        side=PLAYER_SIDE,
        kind="player",
        level=_require_int(fields, "level"),
        hp=_require_int(fields, "hp"),
        max_hp=_require_int(fields, "max_hp"),
        attack=_require_int(fields, "attack"),
        defense=_require_int(fields, "defense"),
        quick=_require_int(fields, "quick"),
        name=_require_name(fields),
        fixed_vital=(
            int(fields["vital"]) if fields.get("vital") is not None else None
        ),
    )


def allied_pet_participant(pet: PetActor) -> BattleParticipant:
    fields = pet.state
    return BattleParticipant(
        participant_id=f"pet:{pet.slot.value}",
        side=PLAYER_SIDE,
        kind="pet",
        level=_require_int(fields, "level"),
        hp=_require_int(fields, "hp"),
        max_hp=_require_int(fields, "max_hp"),
        attack=_require_int(fields, "attack"),
        defense=_require_int(fields, "defense"),
        quick=_require_int(fields, "quick"),
        name=_require_name(fields),
        source_variant_id=pet.variant_id.value,
        source_template_id=pet.template_id.value,
        source_pet_slot=pet.slot.value,
    )


def enemy_participant_from_spawn_state(
    variant: EnemyVariantBridge,
    template: PetTemplateBridge,
    birth: PetBirthBridgeState,
    *,
    spawn_index: int,
) -> BattleParticipant:
    spawn_index = int(spawn_index)
    if spawn_index < 0:
        raise ValueError("spawn_index must be >= 0")
    if variant.tempno != template.tempno:
        raise ValueError("enemy variant/template identity mismatch")
    if birth.template_ref.namespace != "enemybase.TEMPNO":
        raise ValueError("enemy birth uses unexpected template namespace")
    if int(birth.template_ref.template_id) != template.tempno:
        raise ValueError("enemy birth template does not match enemy template")
    if template.name is None:
        raise ValueError("enemy battle participant requires template name")

    projection = birth.combat_projection()
    return BattleParticipant(
        participant_id=f"enemy:{variant.enemy_id}:{spawn_index}",
        side=ENEMY_SIDE,
        kind="enemy",
        level=int(projection["level"]),
        hp=int(projection["hp"]),
        max_hp=int(projection["max_hp"]),
        attack=int(projection["attack"]),
        defense=int(projection["defense"]),
        quick=int(projection["quick"]),
        name=str(template.name),
        fixed_vital=int(birth.internal_vital),
        source_variant_id=variant.enemy_id,
        source_template_id=template.tempno,
    )


def enemy_participant_from_birth(
    encounter: EncounterRequest,
    variant: EnemyVariantBridge,
    template: PetTemplateBridge,
    birth: PetBirthBridgeState,
    *,
    spawn_index: int,
) -> BattleParticipant:
    spawn_index = int(spawn_index)
    if not 0 <= spawn_index < encounter.max_enemy_count:
        raise ValueError("spawn_index outside encounter enemy-count boundary")
    if variant.enemy_id != encounter.enemy_variant_id.value:
        raise ValueError("enemy variant does not match EncounterRequest")
    if variant.tempno != encounter.pet_template_id.value:
        raise ValueError("enemy template identity does not match EncounterRequest")
    if template.tempno != encounter.pet_template_id.value:
        raise ValueError("pet template does not match EncounterRequest")
    if int(birth.template_ref.template_id) != encounter.pet_template_id.value:
        raise ValueError("enemy birth template does not match EncounterRequest")
    if birth.level != encounter.level:
        raise ValueError("enemy birth level does not match EncounterRequest")
    return enemy_participant_from_spawn_state(
        variant,
        template,
        birth,
        spawn_index=spawn_index,
    )


def _allied_battle_participants(
    domain: SinglePlayerHistoricalDomain,
    allied_pet_slots: Sequence[int],
) -> tuple[BattleParticipant, ...]:
    allies = []
    seen_slots: set[int] = set()
    for raw_slot in allied_pet_slots:
        slot = PetSlot(int(raw_slot))
        if slot.value in seen_slots:
            raise ValueError(f"duplicate allied pet slot {slot.value}")
        seen_slots.add(slot.value)
        if slot not in domain.persistent.pets:
            raise KeyError(f"allied pet slot {slot.value} is not populated")
        allies.append(allied_pet_participant(domain.persistent.pets[slot]))
    return tuple(allies)


def begin_group_battle(
    domain: SinglePlayerHistoricalDomain,
    encounter: GroupEncounterRequest,
    *,
    enemies: Sequence[BattleParticipant],
    allied_pet_slots: Sequence[int] = (),
) -> BattleSession:
    position = domain.world.player_position
    if position is None:
        raise ValueError("world position is required before battle")
    if position != encounter.position:
        raise ValueError(
            "GroupEncounterRequest position no longer matches world position"
        )
    if domain.persistent.character is None:
        raise ValueError("player state is required before battle")

    enemy_tuple = tuple(enemies)
    if not enemy_tuple:
        raise ValueError("battle requires at least one enemy spawn")
    if len(enemy_tuple) > encounter.max_enemy_count:
        raise ValueError("enemy spawn count exceeds group encounter boundary")

    participant_ids: set[str] = set()
    for enemy in enemy_tuple:
        if enemy.side != ENEMY_SIDE or enemy.kind != "enemy":
            raise ValueError("enemy list contains a non-enemy participant")
        if enemy.participant_id in participant_ids:
            raise ValueError(f"duplicate battle participant id {enemy.participant_id}")
        participant_ids.add(enemy.participant_id)

    return BattleSession(
        origin_position=position,
        encounter=encounter,
        player=player_participant(domain.persistent.character),
        allied_pets=_allied_battle_participants(domain, allied_pet_slots),
        enemies=enemy_tuple,
    )


def begin_battle(
    domain: SinglePlayerHistoricalDomain,
    encounter: EncounterRequest,
    *,
    enemies: Sequence[BattleParticipant],
    allied_pet_slots: Sequence[int] = (),
) -> BattleSession:
    position = domain.world.player_position
    if position is None:
        raise ValueError("world position is required before battle")
    if position != encounter.position:
        raise ValueError("EncounterRequest position no longer matches world position")
    if domain.persistent.character is None:
        raise ValueError("player state is required before battle")

    enemy_tuple = tuple(enemies)
    if not enemy_tuple:
        raise ValueError("battle requires at least one explicit enemy spawn")
    if len(enemy_tuple) > encounter.max_enemy_count:
        raise ValueError("enemy spawn count exceeds EncounterRequest boundary")
    for enemy in enemy_tuple:
        if enemy.side != ENEMY_SIDE or enemy.kind != "enemy":
            raise ValueError("enemy list contains a non-enemy participant")
        if enemy.source_variant_id != encounter.enemy_variant_id.value:
            raise ValueError("battle enemy variant does not match EncounterRequest")
        if enemy.source_template_id != encounter.pet_template_id.value:
            raise ValueError("battle enemy template does not match EncounterRequest")
        if enemy.level != encounter.level:
            raise ValueError("battle enemy level does not match EncounterRequest")

    return BattleSession(
        origin_position=position,
        encounter=encounter,
        player=player_participant(domain.persistent.character),
        allied_pets=_allied_battle_participants(domain, allied_pet_slots),
        enemies=enemy_tuple,
    )


def preview_physical_damage(
    attacker: BattleParticipant,
    defender: BattleParticipant,
    *,
    random_value: int,
    defense_profile: str,
    stone: bool = False,
) -> int:
    """Apply the recovered descendant physical core with an explicit profile.

    The original JSS-era defense generation is unresolved, so callers must
    select either the compiled descendant newpower branch or the preserved old
    mixed-stat branch.
    """
    if defense_profile == "newpower_70pct":
        effective = effective_defense_newpower(defender.defense, stone=stone)
    elif defense_profile == "preserved_old_mixed":
        if defender.fixed_vital is None:
            raise ValueError(
                "preserved_old_mixed requires explicit defender fixed_vital"
            )
        effective = effective_defense_preserved_old(
            defender.defense,
            defender.quick,
            defender.fixed_vital,
            stone=stone,
        )
    else:
        raise ValueError(f"unknown defense profile: {defense_profile}")
    return physical_base_damage(attacker.attack, effective, int(random_value))


def _updated_existing_fields(
    current: Mapping[str, Any],
    updates: Mapping[str, Any],
    *,
    subject: str,
) -> Mapping[str, Any]:
    merged = dict(current)
    for key, value in updates.items():
        if key not in merged:
            raise ValueError(f"{subject} update introduces unknown field {key}")
        merged[key] = value
    return MappingProxyType(merged)


def apply_battle_outcome(
    domain: SinglePlayerHistoricalDomain,
    session: BattleSession,
    outcome: BattleOutcome,
) -> BattleReturn:
    """Return an explicit battle result to persistent world state.

    No victory, EXP, drop, death or healing rule is inferred here. Those values
    must already be present in the supplied outcome from a validated battle
    resolution layer.
    """
    if domain.world.player_position != session.origin_position:
        raise ValueError("world position changed while battle session was active")
    if domain.persistent.character is None:
        raise ValueError("player state disappeared during battle")

    player = PlayerState(
        _updated_existing_fields(
            domain.persistent.character.fields,
            outcome.player_updates,
            subject="player",
        )
    )
    domain.persistent.character = player

    for raw_slot, updates in outcome.pet_updates.items():
        slot = PetSlot(int(raw_slot))
        if slot not in domain.persistent.pets:
            raise KeyError(f"battle outcome references missing pet slot {slot.value}")
        pet = domain.persistent.pets[slot]
        domain.persistent.pets[slot] = replace(
            pet,
            state=_updated_existing_fields(
                pet.state,
                updates,
                subject=f"pet slot {slot.value}",
            ),
        )

    return BattleReturn(
        result=str(outcome.result),
        world_position=session.origin_position,
        player=domain.persistent.character,
        pets=MappingProxyType(dict(domain.persistent.pets)),
    )
