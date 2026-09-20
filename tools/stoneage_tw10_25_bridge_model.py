#!/usr/bin/env python3
"""Executable bridge objects from recovered 2.5 master data to the v1 model.

These objects deliberately expose only relationships supported by the bridge
schema. They do not claim that the recovered 2.5 rows are Taiwan v1.0 data.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from tools.stoneage_tw10_gameplay_model import TemplateRef


def _required(row: Mapping[str, Any], key: str) -> Any:
    if key not in row:
        raise KeyError(f"missing bridge source field: {key}")
    return row[key]


@dataclass(frozen=True)
class PetTemplateBridge:
    tempno: int
    graphic_id: int
    ai: int
    earth: int
    water: int
    fire: int
    wind: int
    skill_slots: int
    skill_ids: tuple[int, ...]
    base_vital: int | float | None = None
    base_strength: int | float | None = None
    base_toughness: int | float | None = None
    base_dexterity: int | float | None = None
    level_up_point: int | float | None = None

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
            ai=int(_required(row, "MODAI")),
            earth=int(_required(row, "EARTHAT")),
            water=int(_required(row, "WATERAT")),
            fire=int(_required(row, "FIREAT")),
            wind=int(_required(row, "WINDAT")),
            skill_slots=slot_count,
            skill_ids=skills,
            base_vital=row.get("BASEVITAL"),
            base_strength=row.get("BASESTR"),
            base_toughness=row.get("BASETGH"),
            base_dexterity=row.get("BASEDEX"),
            level_up_point=row.get("LVUPPOINT"),
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

    def growth_inputs(self) -> dict[str, int | float | None]:
        """Formula inputs remain separate from direct client-state mappings."""
        return {
            "BASEVITAL": self.base_vital,
            "BASESTR": self.base_strength,
            "BASETGH": self.base_toughness,
            "BASEDEX": self.base_dexterity,
            "LVUPPOINT": self.level_up_point,
        }


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


@dataclass(frozen=True)
class ItemTemplateBridge:
    template_id: int
    visible_name: str
    effect_text: str
    graphic_id: int
    field_context: int
    target_class: int
    level: int
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
            ordinary_name=str(row["name"]) if row.get("name") is not None else None,
        )

    @property
    def template_ref(self) -> TemplateRef:
        return TemplateRef("itemset.id", self.template_id)

    def client_view_fields(
        self,
        *,
        secondary_runtime_text: str = "",
        color: int = 0,
        send_or_use_flags: int = 0,
    ) -> dict[str, Any]:
        """Build only the nine-field v1 item view payload.

        The later fixed server lineage sources the first string from
        ITEM_SECRETNAME, the second from a runtime paramshow buffer, and
        computes the flags value at runtime.
        """
        return {
            "name": self.visible_name,
            "secondary_or_secret_name": str(secondary_runtime_text),
            "color": int(color),
            "memo_or_effect_text": self.effect_text,
            "graphic_id": self.graphic_id,
            "field_context": self.field_context,
            "target_class": self.target_class,
            "level": self.level,
            "send_or_use_flags": int(send_or_use_flags),
        }


@dataclass(frozen=True)
class NpcTemplateBridge:
    template_name: str
    functionset: str | None = None

    @property
    def template_ref(self) -> TemplateRef:
        return TemplateRef("npc.templatename", self.template_name)


@dataclass(frozen=True)
class NpcCreateBridge:
    floor_id: int
    template_names: tuple[str, ...]
    create_num: int | None = None

    @classmethod
    def from_create(
        cls,
        *,
        floor_id: int,
        template_names: Sequence[str],
        create_num: int | None = None,
    ) -> "NpcCreateBridge":
        return cls(
            int(floor_id),
            tuple(str(x) for x in template_names),
            None if create_num is None else int(create_num),
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
