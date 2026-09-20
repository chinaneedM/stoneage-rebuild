#!/usr/bin/env python3
"""Schema-driven Taiwan StoneAge v1.0 reconstruction-side gameplay records.

This module intentionally does not import later descendant C structs. Historical
wire positions/types are loaded from STONEAGE-TW10-GAMEPLAY-SCHEMA-R1.json.
Optional server template references remain separate identities.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Mapping, Sequence


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA_PATH = REPO_ROOT / "research/clients/STONEAGE-TW10-GAMEPLAY-SCHEMA-R1.json"
DEFAULT_BRIDGE_PATH = REPO_ROOT / "research/clients/STONEAGE-TW10-25-GAMEPLAY-BRIDGE-R1.json"

BASE62_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def load_gameplay_schema(path: Path | str = DEFAULT_SCHEMA_PATH) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_gameplay_bridge(path: Path | str = DEFAULT_BRIDGE_PATH) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def a62_to_int(value: str) -> int:
    """Reproduce the early client a62toi digit convention.

    0-9 => 0..9, a-z => 10..35, A-Z => 36..61.
    A '-' changes the final sign as in the preserved client implementation.
    """
    text = str(value)
    ret = 0
    sign = 1
    for ch in text:
        ret *= 62
        if "0" <= ch <= "9":
            ret += ord(ch) - ord("0")
        elif "a" <= ch <= "z":
            ret += ord(ch) - ord("a") + 10
        elif "A" <= ch <= "Z":
            ret += ord(ch) - ord("A") + 36
        elif ch == "-":
            sign = -1
        else:
            return 0
    return ret * sign


_ESCAPE_DECODE = {
    "n": "\n",
    "c": ",",
    "z": "|",
    "y": "\\",
}


def unescape_legacy_string(value: str) -> str:
    """Decode the old client escape alphabet without inventing new escapes."""
    src = str(value)
    out: list[str] = []
    i = 0
    while i < len(src):
        ch = src[i]
        if ch != "\\":
            out.append(ch)
            i += 1
            continue
        i += 1
        if i >= len(src):
            # A dangling slash is malformed; retain it rather than silently
            # manufacturing a character.
            out.append("\\")
            break
        escaped = src[i]
        out.append(_ESCAPE_DECODE.get(escaped, escaped))
        i += 1
    return "".join(out)


def _record_width(spec: Mapping[str, Any]) -> int:
    if "record_width" in spec:
        return int(spec["record_width"])
    if "full_record_width" in spec:
        return int(spec["full_record_width"])
    raise ValueError("record spec has no width")


def decode_wire_value(wire_type: str, value: Any) -> Any:
    if wire_type in {"decimal_int", "decoded_int", "decimal_string_to_int"}:
        return int(value)
    if wire_type in {"base62_int", "base62_string_to_int"}:
        return a62_to_int(str(value))
    if wire_type == "escaped_string":
        return unescape_legacy_string(str(value))
    if wire_type == "decoded_string":
        return str(value)
    raise ValueError(f"unsupported wire type: {wire_type}")


@dataclass(frozen=True)
class DecodedRecord:
    record_name: str
    values: Mapping[str, Any]

    def __getitem__(self, key: str) -> Any:
        return self.values[key]


def decode_record(
    record_name: str,
    raw_values: Sequence[Any],
    *,
    schema: Mapping[str, Any] | None = None,
) -> DecodedRecord:
    schema = schema or load_gameplay_schema()
    records = schema["records"]
    if record_name not in records:
        raise KeyError(f"unknown v1 record: {record_name}")
    spec = records[record_name]
    expected = _record_width(spec)
    if len(raw_values) != expected:
        raise ValueError(
            f"{record_name} requires {expected} fields, got {len(raw_values)}"
        )
    fields = spec["fields"]
    decoded = {
        field["name"]: decode_wire_value(field["wire_type"], raw_values[index])
        for index, field in enumerate(fields)
    }
    return DecodedRecord(record_name, decoded)


@dataclass(frozen=True)
class TemplateRef:
    namespace: str
    template_id: int | str
    evidence: str = "BRIDGE_2_5"


@dataclass(frozen=True)
class CharacterState:
    status: DecodedRecord

    @classmethod
    def from_full_status(
        cls, raw_values: Sequence[Any], *, schema: Mapping[str, Any] | None = None
    ) -> "CharacterState":
        return cls(decode_record("status_player_full", raw_values, schema=schema))


@dataclass(frozen=True)
class PetState:
    pet_slot: int
    status: DecodedRecord
    template_ref: TemplateRef | None = None

    @classmethod
    def from_full_status(
        cls,
        pet_slot: int,
        raw_values: Sequence[Any],
        *,
        template_ref: TemplateRef | None = None,
        schema: Mapping[str, Any] | None = None,
    ) -> "PetState":
        return cls(
            int(pet_slot),
            decode_record("status_pet_full", raw_values, schema=schema),
            template_ref,
        )


@dataclass(frozen=True)
class ItemView:
    slot: int | None
    view: DecodedRecord
    template_ref: TemplateRef | None = None

    @classmethod
    def from_full_slot(
        cls,
        slot: int,
        raw_values: Sequence[Any],
        *,
        template_ref: TemplateRef | None = None,
        schema: Mapping[str, Any] | None = None,
    ) -> "ItemView":
        return cls(
            int(slot),
            decode_record("inventory_full_slot", raw_values, schema=schema),
            template_ref,
        )

    @classmethod
    def from_incremental(
        cls,
        raw_values: Sequence[Any],
        *,
        template_ref: TemplateRef | None = None,
        schema: Mapping[str, Any] | None = None,
    ) -> "ItemView":
        decoded = decode_record("inventory_incremental_record", raw_values, schema=schema)
        return cls(int(decoded["inventory_slot"]), decoded, template_ref)


@dataclass(frozen=True)
class PetSkillView:
    pet_slot: int
    skill_slot: int
    view: DecodedRecord
    template_ref: TemplateRef | None = None

    @classmethod
    def from_slot(
        cls,
        pet_slot: int,
        skill_slot: int,
        raw_values: Sequence[Any],
        *,
        template_ref: TemplateRef | None = None,
        schema: Mapping[str, Any] | None = None,
    ) -> "PetSkillView":
        return cls(
            int(pet_slot),
            int(skill_slot),
            decode_record("pet_skill_view_slot", raw_values, schema=schema),
            template_ref,
        )


@dataclass(frozen=True)
class WorldObject:
    variant: str
    view: DecodedRecord
    template_ref: TemplateRef | None = None

    @classmethod
    def from_character(
        cls,
        raw_values: Sequence[Any],
        *,
        template_ref: TemplateRef | None = None,
        schema: Mapping[str, Any] | None = None,
    ) -> "WorldObject":
        return cls(
            "character",
            decode_record("world_character_record", raw_values, schema=schema),
            template_ref,
        )

    @classmethod
    def from_ground_item(
        cls,
        raw_values: Sequence[Any],
        *,
        template_ref: TemplateRef | None = None,
        schema: Mapping[str, Any] | None = None,
    ) -> "WorldObject":
        return cls(
            "ground_item",
            decode_record("world_ground_item_record", raw_values, schema=schema),
            template_ref,
        )

    @classmethod
    def from_ground_money(
        cls,
        raw_values: Sequence[Any],
        *,
        schema: Mapping[str, Any] | None = None,
    ) -> "WorldObject":
        return cls(
            "ground_money",
            decode_record("world_ground_money_record", raw_values, schema=schema),
            None,
        )


@dataclass(frozen=True)
class NPCWindowSession:
    view: DecodedRecord

    @classmethod
    def from_transport(
        cls, raw_values: Sequence[Any], *, schema: Mapping[str, Any] | None = None
    ) -> "NPCWindowSession":
        return cls(decode_record("npc_window_session", raw_values, schema=schema))


def validate_bridge_against_schema(
    *,
    schema: Mapping[str, Any] | None = None,
    bridge: Mapping[str, Any] | None = None,
) -> None:
    """Fail when a bridge references a client field absent from the v1 schema."""
    schema = schema or load_gameplay_schema()
    bridge = bridge or load_gameplay_bridge()
    records = schema["records"]

    def ensure(record_name: str, field_name: str) -> None:
        if record_name not in records:
            raise ValueError(f"bridge references unknown record {record_name}")
        names = {f["name"] for f in records[record_name]["fields"]}
        if field_name not in names:
            raise ValueError(f"bridge references unknown field {record_name}.{field_name}")

    for group in bridge["bridges"].values():
        for mapping in group.get("mappings", []):
            target_fields = mapping.get("target_fields")
            if target_fields is not None:
                record_name = mapping["target_record"]
                for field_name in target_fields:
                    ensure(record_name, field_name)
                continue
            target_field = mapping.get("target_field")
            if target_field is None:
                continue
            if "target_record" in mapping:
                ensure(mapping["target_record"], target_field)
            for record_name in mapping.get("target_records", []):
                ensure(record_name, target_field)

        skill_bridge = group.get("skill_assignment_bridge")
        if skill_bridge:
            ensure(skill_bridge["target_record"], skill_bridge["target_field"])


if __name__ == "__main__":
    validate_bridge_against_schema()
