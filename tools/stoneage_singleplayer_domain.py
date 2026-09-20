#!/usr/bin/env python3
"""In-process historical domain boundary for the StoneAge single-player rebuild.

The reconstruction bridge/protocol modules remain evidence adapters. This
module exposes ordinary domain objects and services that a future engine can
call directly; it has no socket, packet, server-process, or transport
dependency.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping

from tools.stoneage_tw10_gameplay_model import CharacterState, TemplateRef
from tools.stoneage_tw10_25_bridge_model import (
    ItemInstanceBridge,
    NpcRuntimeState,
    PetSkillTemplateBridge,
    ReconstructedPetBridgeState,
)
from tools.stoneage_tw10_25_encounter_bridge import (
    EncounterAreaBridge,
    EnemyVariantBridge,
    GroupBridge,
    active_encounter_area,
    choose_enemy,
    choose_group,
    effective_enemy_count_limit,
)


def _positive_or_zero(value: int, label: str) -> int:
    value = int(value)
    if value < 0:
        raise ValueError(f"{label} must be >= 0")
    return value


def _template_id(ref: TemplateRef, namespace: str) -> int | str:
    if ref.namespace != namespace:
        raise ValueError(
            f"expected template namespace {namespace}, got {ref.namespace}"
        )
    return ref.template_id


@dataclass(frozen=True, order=True)
class RuntimeObjectId:
    value: int

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "value", _positive_or_zero(self.value, "runtime object id")
        )


@dataclass(frozen=True, order=True)
class InventorySlot:
    value: int

    def __post_init__(self) -> None:
        value = int(self.value)
        if not 0 <= value < 20:
            raise ValueError("inventory slot must be in 0..19")
        object.__setattr__(self, "value", value)


@dataclass(frozen=True, order=True)
class PetSlot:
    value: int

    def __post_init__(self) -> None:
        value = int(self.value)
        if not 0 <= value < 5:
            raise ValueError("pet slot must be in 0..4")
        object.__setattr__(self, "value", value)


@dataclass(frozen=True, order=True)
class ItemTemplateId:
    value: int


@dataclass(frozen=True, order=True)
class PetTemplateId:
    value: int


@dataclass(frozen=True, order=True)
class EnemyVariantId:
    value: int


@dataclass(frozen=True, order=True)
class NpcTemplateId:
    value: str


@dataclass(frozen=True)
class MapPosition:
    floor_id: int
    x: int
    y: int


@dataclass(frozen=True)
class PlayerState:
    """Engine-facing player snapshot, detached from wire serialization."""

    fields: Mapping[str, Any]

    @classmethod
    def from_v1_character(cls, state: CharacterState) -> "PlayerState":
        return cls(MappingProxyType(dict(state.status.values)))


@dataclass(frozen=True)
class InventoryItem:
    slot: InventorySlot
    template_id: ItemTemplateId
    view: Mapping[str, Any]


@dataclass(frozen=True)
class PetSkill:
    template_id: int
    view: Mapping[str, Any]


@dataclass(frozen=True)
class PetActor:
    slot: PetSlot
    variant_id: EnemyVariantId
    template_id: PetTemplateId
    runtime_object_id: RuntimeObjectId | None
    state: Mapping[str, Any]
    skills: tuple[PetSkill, ...]


@dataclass(frozen=True)
class WorldNpc:
    runtime_object_id: RuntimeObjectId
    template_id: NpcTemplateId
    position: MapPosition
    world_view: Mapping[str, Any]


@dataclass(frozen=True)
class NpcSession:
    sequence_number: int
    source_runtime_object_id: RuntimeObjectId
    window_type: int
    button_mask_or_type: int
    data: str


@dataclass(frozen=True)
class EncounterRequest:
    """Legacy single-variant encounter projection kept for compatibility."""

    area_index: int
    position: MapPosition
    group_id: int
    enemy_variant_id: EnemyVariantId
    pet_template_id: PetTemplateId
    level: int
    max_enemy_count: int


@dataclass(frozen=True)
class GroupEncounterRequest:
    """Group-level encounter boundary matching stable ENEMY_getEnemy ordering."""

    area_index: int
    position: MapPosition
    group_id: int
    max_enemy_count: int


@dataclass(frozen=True)
class HistoricalStaticData:
    """Static master/bridge data kept separate from mutable runtime state."""

    encounter_areas: tuple[EncounterAreaBridge, ...] = ()
    encounter_groups: Mapping[int, GroupBridge] = field(default_factory=dict)
    enemy_variants: Mapping[int, EnemyVariantBridge] = field(default_factory=dict)

    def __post_init__(self) -> None:
        groups = {int(key): value for key, value in self.encounter_groups.items()}
        enemies = {int(key): value for key, value in self.enemy_variants.items()}
        for key, group in groups.items():
            if key != group.group_id:
                raise ValueError(
                    f"encounter group key {key} does not match GROUP_ID {group.group_id}"
                )
        for key, enemy in enemies.items():
            if key != enemy.enemy_id:
                raise ValueError(
                    f"enemy variant key {key} does not match enemy.ID {enemy.enemy_id}"
                )
        object.__setattr__(self, "encounter_areas", tuple(self.encounter_areas))
        object.__setattr__(self, "encounter_groups", MappingProxyType(groups))
        object.__setattr__(self, "enemy_variants", MappingProxyType(enemies))


@dataclass
class PersistentPlayerState:
    character: PlayerState | None = None
    inventory: dict[InventorySlot, InventoryItem] = field(default_factory=dict)
    pets: dict[PetSlot, PetActor] = field(default_factory=dict)


@dataclass
class TransientWorldState:
    player_position: MapPosition | None = None
    npcs: dict[RuntimeObjectId, WorldNpc] = field(default_factory=dict)


@dataclass
class InteractionState:
    npc_sessions: dict[int, NpcSession] = field(default_factory=dict)


def adapt_item_instance(slot: int, instance: ItemInstanceBridge) -> InventoryItem:
    template_id = _template_id(instance.template_ref, "itemset.id")
    return InventoryItem(
        InventorySlot(slot),
        ItemTemplateId(int(template_id)),
        MappingProxyType(instance.client_view_fields()),
    )


def adapt_pet_state(
    state: ReconstructedPetBridgeState,
    skills: Mapping[int, PetSkillTemplateBridge],
) -> PetActor:
    variant_id = int(_template_id(state.variant_ref, "enemy.ID"))
    template_id = int(_template_id(state.template_ref, "enemybase.TEMPNO"))
    resolved_skills: list[PetSkill] = []
    for skill_id in state.skill_ids:
        skill_id = int(skill_id)
        if skill_id not in skills:
            raise KeyError(f"unresolved pet skill ID {skill_id}")
        skill = skills[skill_id]
        if skill.skill_id != skill_id:
            raise ValueError(
                f"pet skill key {skill_id} does not match petskill.ID {skill.skill_id}"
            )
        resolved_skills.append(
            PetSkill(
                skill_id,
                MappingProxyType(skill.client_view_fields()),
            )
        )
    runtime_object_id = (
        None
        if state.runtime_object_id is None
        else RuntimeObjectId(state.runtime_object_id)
    )
    return PetActor(
        PetSlot(state.pet_slot),
        EnemyVariantId(variant_id),
        PetTemplateId(template_id),
        runtime_object_id,
        MappingProxyType(state.v1_pet_state_fields()),
        tuple(resolved_skills),
    )


def adapt_npc_runtime(state: NpcRuntimeState) -> WorldNpc:
    template_id = _template_id(state.template_ref, "npc.templatename")
    return WorldNpc(
        RuntimeObjectId(state.runtime_object_id),
        NpcTemplateId(str(template_id)),
        MapPosition(state.floor_id, state.x, state.y),
        MappingProxyType(state.v1_world_character_fields()),
    )


def build_npc_session(
    npc: NpcRuntimeState,
    *,
    window_type: int,
    button_mask_or_type: int,
    sequence_number: int,
    data: str,
) -> NpcSession:
    fields = npc.window_session_fields(
        window_type=window_type,
        button_mask_or_type=button_mask_or_type,
        sequence_number=sequence_number,
        data=data,
    )
    return NpcSession(
        sequence_number=int(fields["sequence_number"]),
        source_runtime_object_id=RuntimeObjectId(fields["source_object_index"]),
        window_type=int(fields["window_type"]),
        button_mask_or_type=int(fields["button_mask_or_type"]),
        data=str(fields["data"]),
    )


@dataclass
class SinglePlayerHistoricalDomain:
    """Engine-facing aggregate for historical mechanics before redesign.

    Static master data, persistent player data, transient world data, and
    interaction/session state are separate. Calls are synchronous/in-process;
    historical wire records enter only through explicit adapter functions.
    """

    static: HistoricalStaticData = field(default_factory=HistoricalStaticData)
    persistent: PersistentPlayerState = field(default_factory=PersistentPlayerState)
    world: TransientWorldState = field(default_factory=TransientWorldState)
    interactions: InteractionState = field(default_factory=InteractionState)

    def set_player_from_v1(self, state: CharacterState) -> PlayerState:
        player = PlayerState.from_v1_character(state)
        self.persistent.character = player
        return player

    def put_item(self, slot: int, instance: ItemInstanceBridge) -> InventoryItem:
        item = adapt_item_instance(slot, instance)
        self.persistent.inventory[item.slot] = item
        return item

    def put_pet(
        self,
        state: ReconstructedPetBridgeState,
        skills: Mapping[int, PetSkillTemplateBridge],
    ) -> PetActor:
        pet = adapt_pet_state(state, skills)
        self.persistent.pets[pet.slot] = pet
        return pet

    def place_npc(self, state: NpcRuntimeState) -> WorldNpc:
        npc = adapt_npc_runtime(state)
        self.world.npcs[npc.runtime_object_id] = npc
        return npc

    def move_player(self, *, floor_id: int, x: int, y: int) -> MapPosition:
        position = MapPosition(int(floor_id), int(x), int(y))
        self.world.player_position = position
        return position

    def open_npc_session(
        self,
        npc: NpcRuntimeState,
        *,
        window_type: int,
        button_mask_or_type: int,
        sequence_number: int,
        data: str,
    ) -> NpcSession:
        session = build_npc_session(
            npc,
            window_type=window_type,
            button_mask_or_type=button_mask_or_type,
            sequence_number=sequence_number,
            data=data,
        )
        runtime_id = RuntimeObjectId(npc.runtime_object_id)
        if runtime_id not in self.world.npcs:
            raise KeyError(
                f"NPC runtime object {runtime_id.value} is not present in world state"
            )
        if session.source_runtime_object_id != runtime_id:
            raise ValueError("NPC session source identity does not match world NPC")
        self.interactions.npc_sessions[session.sequence_number] = session
        return session

    def request_encounter_group(
        self,
        *,
        group_roll: int,
    ) -> GroupEncounterRequest | None:
        position = self.world.player_position
        if position is None:
            raise ValueError("player position is required before encounter lookup")
        area = active_encounter_area(
            self.static.encounter_areas,
            floor=position.floor_id,
            x=position.x,
            y=position.y,
        )
        if area is None:
            return None

        inventory_template_ids = tuple(
            item.template_id.value for item in self.persistent.inventory.values()
        )
        group = choose_group(
            area,
            self.static.encounter_groups,
            inventory_template_ids=inventory_template_ids,
            roll=group_roll,
        )
        return GroupEncounterRequest(
            area_index=area.index,
            position=position,
            group_id=group.group_id,
            max_enemy_count=area.enemy_max_num,
        )

    def request_encounter(
        self,
        *,
        group_roll: int,
        enemy_roll: int,
        level_roll: int,
    ) -> EncounterRequest | None:
        position = self.world.player_position
        if position is None:
            raise ValueError("player position is required before encounter lookup")
        area = active_encounter_area(
            self.static.encounter_areas,
            floor=position.floor_id,
            x=position.x,
            y=position.y,
        )
        if area is None:
            return None

        inventory_template_ids = tuple(
            item.template_id.value for item in self.persistent.inventory.values()
        )
        group = choose_group(
            area,
            self.static.encounter_groups,
            inventory_template_ids=inventory_template_ids,
            roll=group_roll,
        )
        enemy = choose_enemy(
            group,
            self.static.enemy_variants,
            roll=enemy_roll,
        )
        level = enemy.choose_level(level_roll)
        return EncounterRequest(
            area_index=area.index,
            position=position,
            group_id=group.group_id,
            enemy_variant_id=EnemyVariantId(enemy.enemy_id),
            pet_template_id=PetTemplateId(enemy.tempno),
            level=level,
            max_enemy_count=effective_enemy_count_limit(area, (enemy,)),
        )

@dataclass(frozen=True)
class EncounterRolls:
    group_roll: int
    enemy_roll: int
    level_roll: int


@dataclass(frozen=True)
class SimulationTickResult:
    tick_index: int
    player_position: MapPosition | None
    world_object_ids: tuple[RuntimeObjectId, ...]
    inventory_slots: tuple[InventorySlot, ...]
    pet_slots: tuple[PetSlot, ...]
    active_npc_sequences: tuple[int, ...]
    encounter_request: EncounterRequest | None = None


@dataclass
class SinglePlayerSimulation:
    """Minimal deterministic simulation shell over the historical domain.

    A tick does not invent real-time mechanics. State-changing operations remain
    explicit domain calls, while optional encounter rolls let an engine-owned
    RNG drive the already reconstructed encounter selection path.
    """

    domain: SinglePlayerHistoricalDomain
    tick_index: int = 0

    def step(
        self,
        *,
        encounter_rolls: EncounterRolls | None = None,
    ) -> SimulationTickResult:
        self.tick_index += 1
        encounter = None
        if encounter_rolls is not None:
            encounter = self.domain.request_encounter(
                group_roll=encounter_rolls.group_roll,
                enemy_roll=encounter_rolls.enemy_roll,
                level_roll=encounter_rolls.level_roll,
            )
        return SimulationTickResult(
            tick_index=self.tick_index,
            player_position=self.domain.world.player_position,
            world_object_ids=tuple(sorted(self.domain.world.npcs)),
            inventory_slots=tuple(sorted(self.domain.persistent.inventory)),
            pet_slots=tuple(sorted(self.domain.persistent.pets)),
            active_npc_sequences=tuple(sorted(self.domain.interactions.npc_sessions)),
            encounter_request=encounter,
        )

