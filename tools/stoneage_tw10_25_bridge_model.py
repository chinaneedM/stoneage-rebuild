#!/usr/bin/env python3
"""Executable bridge objects from recovered 2.5 master data to the v1 model.

These objects deliberately expose only relationships supported by the bridge
schema. They do not claim that the recovered 2.5 rows are Taiwan v1.0 data.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from tools.stoneage_tw10_gameplay_model import TemplateRef
from tools.stoneage_pet_growth_model import (
    allocation_counts,
    individualize_growth_base,
    pack_growth_base,
    pet_rank_from_template_base,
)
from tools.stoneage_player_growth_model import base_derived_stats
from tools.stoneage_tw10_25_encounter_bridge import EnemyVariantBridge


def _required(row: Mapping[str, Any], key: str) -> Any:
    if key not in row:
        raise KeyError(f"missing bridge source field: {key}")
    return row[key]


def c_atoi(value: Any) -> int:
    """Model the fixed descendant loader's atoi treatment of table fields."""
    text = str(value).lstrip()
    if not text:
        return 0
    sign = 1
    if text[0] in "+-":
        if text[0] == "-":
            sign = -1
        text = text[1:]
    digits = []
    for ch in text:
        if not ch.isdigit():
            break
        digits.append(ch)
    return sign * int("".join(digits) or "0")


@dataclass(frozen=True)
class PetTemplateBridge:
    tempno: int
    graphic_id: int
    name: str | None
    ai: int
    earth: int
    water: int
    fire: int
    wind: int
    skill_slots: int
    skill_ids: tuple[int, ...]
    init_num: int | None = None
    base_vital: int | None = None
    base_strength: int | None = None
    base_toughness: int | None = None
    base_dexterity: int | None = None
    level_up_point: int | None = None
    size_class: int | None = None

    @classmethod
    def from_enemybase(cls, row: Mapping[str, Any]) -> "PetTemplateBridge":
        skills = tuple(
            int(row.get(f"PETSKILL{i}", 0))
            for i in range(1, 8)
            if int(row.get(f"PETSKILL{i}", 0)) > 0
        )
        slot_count = int(_required(row, "SLOT"))
        if not 0 <= len(skills) <= 7:
            raise ValueError("enemybase pet-skill bridge supports at most seven IDs")
        if slot_count < 0 or slot_count > 7:
            raise ValueError("enemybase SLOT outside v1 seven-slot client maximum")
        return cls(
            tempno=int(_required(row, "TEMPNO")),
            graphic_id=int(_required(row, "IMGNUMBER")),
            name=str(row["NAME"]) if row.get("NAME") not in (None, "") else None,
            ai=int(_required(row, "MODAI")),
            earth=int(_required(row, "EARTHAT")),
            water=int(_required(row, "WATERAT")),
            fire=int(_required(row, "FIREAT")),
            wind=int(_required(row, "WINDAT")),
            skill_slots=slot_count,
            skill_ids=skills,
            init_num=c_atoi(row["INITNUM"]) if row.get("INITNUM") is not None else None,
            base_vital=c_atoi(row["BASEVITAL"]) if row.get("BASEVITAL") is not None else None,
            base_strength=c_atoi(row["BASESTR"]) if row.get("BASESTR") is not None else None,
            base_toughness=c_atoi(row["BASETGH"]) if row.get("BASETGH") is not None else None,
            base_dexterity=c_atoi(row["BASEDEX"]) if row.get("BASEDEX") is not None else None,
            level_up_point=c_atoi(row["LVUPPOINT"]) if row.get("LVUPPOINT") is not None else None,
            size_class=(
                int(row["SIZE"]) if row.get("SIZE") not in (None, "") else None
            ),
        )

    @property
    def template_ref(self) -> TemplateRef:
        return TemplateRef("enemybase.TEMPNO", self.tempno)

    def directly_bridgeable_pet_state(self) -> dict[str, int]:
        """Only fields shown to be copied from template to runtime state."""
        return {
            "graphic_id": self.graphic_id,
            "ai": self.ai,
            "earth": self.earth,
            "water": self.water,
            "fire": self.fire,
            "wind": self.wind,
            "max_skill_slots": self.skill_slots,
        }

    def growth_inputs(self) -> dict[str, int | None]:
        """Formula inputs remain separate from direct client-state mappings."""
        return {
            "INITNUM": self.init_num,
            "BASEVITAL": self.base_vital,
            "BASESTR": self.base_strength,
            "BASETGH": self.base_toughness,
            "BASEDEX": self.base_dexterity,
            "LVUPPOINT": self.level_up_point,
            "SIZE": self.size_class,
        }


@dataclass(frozen=True)
class PetBirthBridgeState:
    template_ref: TemplateRef
    level: int
    pet_rank: int
    individualized_growth_base: tuple[int, int, int, int]
    alloc_point: int
    spawn_allocation_counts: tuple[int, int, int, int]
    internal_vital: int
    internal_strength: int
    internal_toughness: int
    internal_dexterity: int
    graphic_id: int
    ai: int
    earth: int
    water: int
    fire: int
    wind: int
    max_skill_slots: int
    skill_ids: tuple[int, ...]

    def combat_projection(self) -> dict[str, int]:
        """Stable descendant pre-equipment compliance projection."""
        derived = base_derived_stats(
            self.internal_vital,
            self.internal_strength,
            self.internal_toughness,
            self.internal_dexterity,
        )
        return {
            "max_hp": derived["max_hp"],
            "hp": derived["max_hp"],
            "attack": derived["attack_power"],
            "defense": derived["defence_power"],
            "quick": derived["quick"],
            "level": self.level,
            "graphic_id": self.graphic_id,
            "ai": self.ai,
            "earth": self.earth,
            "water": self.water,
            "fire": self.fire,
            "wind": self.wind,
            "max_skill_slots": self.max_skill_slots,
        }


def build_pet_birth_bridge(
    template: PetTemplateBridge,
    *,
    level: int,
    birth_offsets: Sequence[int],
    spawn_allocation_rolls: Sequence[int],
) -> PetBirthBridgeState:
    """Reproduce the convergent descendant enemy/pet birth arithmetic.

    This is BRIDGE_2_5 formula evidence, not a claim that Taiwan v1.0 server
    coefficients have been independently recovered.
    """
    required = (
        template.init_num,
        template.level_up_point,
        template.base_vital,
        template.base_strength,
        template.base_toughness,
        template.base_dexterity,
    )
    if any(value is None for value in required):
        raise ValueError("pet template is missing birth/growth inputs")
    level = int(level)
    if level < 1:
        raise ValueError("level must be >= 1")

    template_base = (
        int(template.base_vital),
        int(template.base_strength),
        int(template.base_toughness),
        int(template.base_dexterity),
    )
    rank = pet_rank_from_template_base(*template_base)
    individualized = individualize_growth_base(template_base, tuple(birth_offsets))
    packed = pack_growth_base(*individualized)
    counts = allocation_counts(tuple(spawn_allocation_rolls))
    current_base = tuple(base + bonus for base, bonus in zip(individualized, counts))
    scale = ((level - 1) * int(template.level_up_point)) + int(template.init_num)
    current = tuple(scale * value for value in current_base)

    return PetBirthBridgeState(
        template_ref=template.template_ref,
        level=level,
        pet_rank=rank,
        individualized_growth_base=individualized,
        alloc_point=packed,
        spawn_allocation_counts=counts,
        internal_vital=current[0],
        internal_strength=current[1],
        internal_toughness=current[2],
        internal_dexterity=current[3],
        graphic_id=template.graphic_id,
        ai=template.ai,
        earth=template.earth,
        water=template.water,
        fire=template.fire,
        wind=template.wind,
        max_skill_slots=template.skill_slots,
        skill_ids=template.skill_ids,
    )


@dataclass(frozen=True)
class ReconstructedPetBridgeState:
    """Composed server-bridge state projected onto the v1 S:K domain."""

    variant_ref: TemplateRef
    template_ref: TemplateRef
    pet_slot: int
    runtime_object_id: int | None
    birth: PetBirthBridgeState
    v1_fields: Mapping[str, Any]
    skill_ids: tuple[int, ...]

    def v1_pet_state_fields(self) -> dict[str, Any]:
        return dict(self.v1_fields)


def build_reconstructed_pet_state(
    variant: EnemyVariantBridge,
    template: PetTemplateBridge,
    *,
    pet_slot: int,
    level_roll: int,
    birth_offsets: Sequence[int],
    spawn_allocation_rolls: Sequence[int],
    mp: int,
    max_mp: int,
    exp: int,
    max_exp: int,
    rename_flag: int,
    free_name: str,
    name: str | None = None,
    runtime_object_id: int | None = None,
) -> ReconstructedPetBridgeState:
    """Compose enemy variant + pet template + birth formula into v1 S:K fields.

    The bridge deliberately requires unresolved runtime values as explicit
    inputs instead of importing later formulas into the Taiwan v1 baseline.
    """
    if int(variant.tempno) != int(template.tempno):
        raise ValueError(
            f"enemy.ID {variant.enemy_id} resolves TEMPNO {variant.tempno}, "
            f"not template {template.tempno}"
        )
    pet_slot = int(pet_slot)
    if not 0 <= pet_slot < 5:
        raise ValueError("pet_slot must be in 0..4")

    level = variant.choose_level(level_roll)
    birth = build_pet_birth_bridge(
        template,
        level=level,
        birth_offsets=birth_offsets,
        spawn_allocation_rolls=spawn_allocation_rolls,
    )
    projection = birth.combat_projection()
    resolved_name = template.name if name is None else str(name)
    if resolved_name is None:
        raise ValueError("pet name must come from enemybase NAME or explicit input")

    fields = {
        "update_mask": 1,
        "graphic_id": projection["graphic_id"],
        "hp": projection["hp"],
        "max_hp": projection["max_hp"],
        "mp": int(mp),
        "max_mp": int(max_mp),
        "exp": int(exp),
        "max_exp": int(max_exp),
        "level": projection["level"],
        "attack": projection["attack"],
        "defense": projection["defense"],
        "quick": projection["quick"],
        "ai": projection["ai"],
        "earth": projection["earth"],
        "water": projection["water"],
        "fire": projection["fire"],
        "wind": projection["wind"],
        "max_skill_slots": projection["max_skill_slots"],
        "rename_flag": int(rename_flag),
        "name": resolved_name,
        "free_name": str(free_name),
    }

    return ReconstructedPetBridgeState(
        variant_ref=variant.variant_ref,
        template_ref=template.template_ref,
        pet_slot=pet_slot,
        runtime_object_id=(
            None if runtime_object_id is None else int(runtime_object_id)
        ),
        birth=birth,
        v1_fields=fields,
        skill_ids=template.skill_ids,
    )


@dataclass(frozen=True)
class PetSkillTemplateBridge:
    skill_id: int
    field_context: int
    target_class: int
    name: str
    comment: str
    cost: int | None = None
    illegal: int | None = None
    function_name: str | None = None
    option: str | None = None

    @classmethod
    def from_petskill(cls, row: Mapping[str, Any]) -> "PetSkillTemplateBridge":
        return cls(
            skill_id=int(_required(row, "ID")),
            field_context=int(_required(row, "FIELD")),
            target_class=int(_required(row, "TARGET")),
            name=str(_required(row, "NAME")),
            comment=str(_required(row, "COMMENT")),
            cost=int(row["COST"]) if row.get("COST") is not None else None,
            illegal=int(row["ILLEGAL"]) if row.get("ILLEGAL") is not None else None,
            function_name=str(row["FUNCNAME"]) if row.get("FUNCNAME") is not None else None,
            option=str(row["OPTION"]) if row.get("OPTION") is not None else None,
        )

    @property
    def template_ref(self) -> TemplateRef:
        return TemplateRef("petskill.ID", self.skill_id)

    def client_view_fields(self) -> dict[str, Any]:
        """Exactly the five fields present in the v1 S:W record."""
        return {
            "skill_id": self.skill_id,
            "field_context": self.field_context,
            "target_class": self.target_class,
            "name": self.name,
            "comment": self.comment,
        }


CHAR_COLORWHITE = 0
CHAR_COLORYELLOW = 4
CHAR_COLORGREEN = 5
ITEM_DISH_TYPE = 20

ITEM_VIEW_FLAG_CANPETMAIL = 1 << 0
ITEM_VIEW_FLAG_CANMERGEFROM = 1 << 1
ITEM_VIEW_FLAG_DISH = 1 << 2


@dataclass(frozen=True)
class ItemInstanceBridge:
    template_ref: TemplateRef
    visible_name: str
    secondary_display_text: str
    color: int
    effect_text: str
    graphic_id: int
    field_context: int
    target_class: int
    level: int
    send_or_use_flags: int

    def client_view_fields(self) -> dict[str, Any]:
        return {
            "name": self.visible_name,
            "secondary_display_text": self.secondary_display_text,
            "color": self.color,
            "memo_or_effect_text": self.effect_text,
            "graphic_id": self.graphic_id,
            "field_context": self.field_context,
            "target_class": self.target_class,
            "level": self.level,
            "send_or_use_flags": self.send_or_use_flags,
        }


@dataclass(frozen=True)
class ItemTemplateBridge:
    template_id: int
    visible_name: str
    effect_text: str
    graphic_id: int
    field_context: int
    target_class: int
    level: int
    item_type: int | None = None
    can_pet_mail: bool = False
    can_merge_from: bool = False
    ordinary_name: str | None = None

    @classmethod
    def from_itemset(cls, row: Mapping[str, Any]) -> "ItemTemplateBridge":
        return cls(
            template_id=int(_required(row, "id")),
            visible_name=str(_required(row, "secretname")),
            effect_text=str(_required(row, "effectstring")),
            graphic_id=int(_required(row, "imagenumber")),
            field_context=int(_required(row, "fieldtype")),
            target_class=int(_required(row, "target")),
            level=int(_required(row, "level")),
            item_type=int(row["type"]) if row.get("type") not in (None, "") else None,
            can_pet_mail=bool(int(row["canpetmail"])) if row.get("canpetmail") not in (None, "") else False,
            can_merge_from=bool(int(row["canmergefrom"])) if row.get("canmergefrom") not in (None, "") else False,
            ordinary_name=str(row["name"]) if row.get("name") is not None else None,
        )

    @property
    def template_ref(self) -> TemplateRef:
        return TemplateRef("itemset.id", self.template_id)

    def instantiate(
        self,
        *,
        secondary_display_text: str = "",
        instance_cdkey: str = "",
        merge_flag: bool = False,
    ) -> ItemInstanceBridge:
        """Build the fixed-descendant base instance -> v1 item-view projection."""
        color = CHAR_COLORWHITE
        if str(instance_cdkey):
            color = CHAR_COLORGREEN
        elif merge_flag:
            color = CHAR_COLORYELLOW

        flags = 0
        if self.can_pet_mail:
            flags |= ITEM_VIEW_FLAG_CANPETMAIL
        if self.can_merge_from:
            flags |= ITEM_VIEW_FLAG_CANMERGEFROM
        if self.item_type == ITEM_DISH_TYPE:
            flags |= ITEM_VIEW_FLAG_DISH

        return ItemInstanceBridge(
            template_ref=self.template_ref,
            visible_name=self.visible_name,
            secondary_display_text=str(secondary_display_text),
            color=color,
            effect_text=self.effect_text,
            graphic_id=self.graphic_id,
            field_context=self.field_context,
            target_class=self.target_class,
            level=self.level,
            send_or_use_flags=flags,
        )

    def client_view_fields(
        self,
        *,
        secondary_display_text: str = "",
        instance_cdkey: str = "",
        merge_flag: bool = False,
    ) -> dict[str, Any]:
        """Compatibility helper returning the nine-field v1 item view."""
        return self.instantiate(
            secondary_display_text=secondary_display_text,
            instance_cdkey=instance_cdkey,
            merge_flag=merge_flag,
        ).client_view_fields()


@dataclass(frozen=True)
class NpcTemplateBridge:
    template_name: str
    functionset: str | None = None
    character_name: str | None = None
    image_number: int | None = None
    default_type: int | None = None

    @classmethod
    def from_template(cls, row: Mapping[str, Any]) -> "NpcTemplateBridge":
        return cls(
            template_name=str(_required(row, "TEMPLATENAME")),
            functionset=(
                str(row["FUNCTIONSET"]) if row.get("FUNCTIONSET") not in (None, "") else None
            ),
            character_name=(
                str(row["CHARNAME"]) if row.get("CHARNAME") not in (None, "") else None
            ),
            image_number=(
                int(row["IMAGENUMBER"]) if row.get("IMAGENUMBER") not in (None, "") else None
            ),
            default_type=(
                int(row["TYPE"]) if row.get("TYPE") not in (None, "") else None
            ),
        )

    @property
    def template_ref(self) -> TemplateRef:
        return TemplateRef("npc.templatename", self.template_name)


@dataclass(frozen=True)
class NpcCreateBridge:
    floor_id: int
    template_names: tuple[str, ...]
    create_num: int | None = None
    direction: int | None = None
    image_override: int | None = None
    name_override: str | None = None
    create_index: int | None = None

    @classmethod
    def from_create(
        cls,
        *,
        floor_id: int,
        template_names: Sequence[str],
        create_num: int | None = None,
        direction: int | None = None,
        image_override: int | None = None,
        name_override: str | None = None,
        create_index: int | None = None,
    ) -> "NpcCreateBridge":
        return cls(
            int(floor_id),
            tuple(str(x) for x in template_names),
            None if create_num is None else int(create_num),
            None if direction is None else int(direction),
            None if image_override is None else int(image_override),
            None if name_override in (None, "") else str(name_override),
            None if create_index is None else int(create_index),
        )


@dataclass(frozen=True)
class NpcRuntimeLink:
    runtime_object_id: int
    template_ref: TemplateRef
    floor_id: int | None = None

    @classmethod
    def link(
        cls,
        runtime_object_id: int,
        template: NpcTemplateBridge,
        *,
        floor_id: int | None = None,
    ) -> "NpcRuntimeLink":
        # The two identities are intentionally carried in different fields.
        return cls(
            int(runtime_object_id),
            template.template_ref,
            None if floor_id is None else int(floor_id),
        )


@dataclass(frozen=True)
class NpcRuntimeState:
    """Descendant-supported NPC runtime state before v1 wire serialization."""

    runtime_object_id: int
    template_ref: TemplateRef
    floor_id: int
    x: int
    y: int
    direction: int
    base_graphic_id: int
    name: str
    object_type: int
    level: int
    name_color: int
    self_title: str
    walkable: int
    height: int
    create_index: int | None = None

    def v1_world_character_fields(self) -> dict[str, Any]:
        """Project into exactly the 12-field Taiwan v1 C character record."""
        return {
            "object_type": self.object_type,
            "runtime_object_id": self.runtime_object_id,
            "x": self.x,
            "y": self.y,
            "direction": self.direction,
            "base_graphic_id": self.base_graphic_id,
            "level": self.level,
            "name_color": self.name_color,
            "name": self.name,
            "self_or_free_title": self.self_title,
            "walkable": self.walkable,
            "height": self.height,
        }

    def window_session_fields(
        self,
        *,
        window_type: int,
        button_mask_or_type: int,
        sequence_number: int,
        data: str,
    ) -> dict[str, Any]:
        """Build the five-value v1 WN receive/session view.

        The key invariant is that source_object_index is the allocated runtime
        object index, while sequence_number is an independent window state ID.
        """
        return {
            "window_type": int(window_type),
            "button_mask_or_type": int(button_mask_or_type),
            "sequence_number": int(sequence_number),
            "source_object_index": self.runtime_object_id,
            "data": str(data),
        }


def build_npc_runtime_bridge(
    template: NpcTemplateBridge,
    create: NpcCreateBridge,
    *,
    runtime_object_id: int,
    spawn_x: int,
    spawn_y: int,
    object_type: int,
    default_level: int,
    default_name_color: int,
    default_self_title: str = "",
    default_walkable: int = 0,
    default_height: int = 0,
) -> NpcRuntimeState:
    """Model the fixed descendant NPC generation -> v1-visible state boundary.

    Template/create data selects presentation and spawn inputs, but the object
    index is allocated only after the CHAR instance has been created. Fields
    not assigned by NPC generation remain explicit default-CHAR inputs.
    """
    if template.template_name not in create.template_names:
        raise ValueError("create rule does not reference this NPC template")
    if create.direction is None:
        raise ValueError("NPC create direction is required")
    graphic = (
        create.image_override
        if create.image_override is not None and create.image_override != -1
        else template.image_number
    )
    if graphic is None:
        raise ValueError("NPC template/create bridge has no image number")
    name = create.name_override or template.character_name
    if name is None:
        raise ValueError("NPC template/create bridge has no character name")

    return NpcRuntimeState(
        runtime_object_id=int(runtime_object_id),
        template_ref=template.template_ref,
        floor_id=create.floor_id,
        x=int(spawn_x),
        y=int(spawn_y),
        direction=int(create.direction),
        base_graphic_id=int(graphic),
        name=str(name),
        object_type=int(object_type),
        level=int(default_level),
        name_color=int(default_name_color),
        self_title=str(default_self_title),
        walkable=int(default_walkable),
        height=int(default_height),
        create_index=create.create_index,
    )
