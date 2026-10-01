#!/usr/bin/env python3
"""Recovered25 AttackMagic execution-facing runtime index.

This loader closes the local recovered data path:
petskill -> magic -> item-config cross-link -> attmagic side-pair.

The recovered petskill "item" number is retained as configuration provenance.
For non-player AttackMagic it is NOT treated as an authoritative existing-item
instance index: the fixed descendant DirectUse path may read it as such, but
the resulting mp value is execution-dead after the non-player branch.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Mapping, Sequence

from tools.stoneage_attack_magic_footprint_model import (
    footprint_target_set,
    matrix_from_attmagic_record,
    normalize_attack_magic_selector,
    source_sort_is_portable,
    source_sorted_targets,
)
from tools.stoneage_attack_magic_model import (
    ATTACK_MAGIC_TARGET_INDEX,
    parse_source_shaped_option,
    remap_attack_magic_target,
)
from tools.stoneage_attmagic_probe import parse_attmagic
from tools.stoneage_itemset_schema_probe import (
    INDEX as ITEM_INDEX,
    SCHEMA as ITEM_SCHEMA,
    clean_rows as clean_item_rows,
    setup_itemsets,
    to_int as item_int,
)
from tools.stoneage_magic_probe import parse as parse_magic
from tools.stoneage_recovered25_petskill_runtime import (
    load_recovered25_petskill_runtime,
)
from tools.stoneage_singleplayer_world import LATER_RECOVERED


SOURCE_VERSION = "recovered25"
ATTACK_SKILL_FUNC = "PETSKILL_AttackMagic"
ATTACK_MAGIC_FUNC = b"MAGIC_AttMagic"
ATTR_INDEX = {"地": 0, "水": 1, "火": 2, "風": 3, "风": 3}
NONPLAYER_ITEM_ROLE = "CONFIG_CROSSLINK_ONLY_MP_EXECUTION_DEAD"


def _active_itemset_path(data_dir: Path, setup: Path | None) -> Path:
    config = setup_itemsets(setup)
    configured = []
    for value in config.values():
        name = Path(value.replace("\\", "/")).name
        if name and (data_dir / name).is_file():
            configured.append(name)
    unique = tuple(dict.fromkeys(configured))
    if len(unique) > 1:
        raise ValueError(
            "configured itemset files resolve to multiple recovered files"
        )
    if unique:
        return data_dir / unique[0]
    fallback = data_dir / "itemset.txt"
    if fallback.is_file():
        return fallback
    raise ValueError("active recovered25 itemset file not found")


def _item_index(path: Path):
    by_id = {}
    for row in clean_item_rows(path):
        if len(row) != len(ITEM_SCHEMA):
            raise ValueError("active recovered25 itemset row width drift")
        item_id = item_int(row[ITEM_INDEX["id"]])
        if item_id is None:
            raise ValueError("active recovered25 item ID is not decimal")
        if item_id in by_id:
            raise ValueError(f"duplicate recovered25 item ID {item_id}")
        by_id[item_id] = row
    return by_id


def _parse_attack_option(raw: bytes) -> tuple[int, int, int]:
    try:
        cp950 = raw.decode("cp950", "strict")
        big5 = raw.decode("big5", "strict")
    except UnicodeDecodeError as exc:
        raise ValueError("attack-magic option is not strict CP950/Big5") from exc
    if cp950 != big5:
        raise ValueError("attack-magic option has CP950/Big5 divergence")
    parts = cp950.split("|")
    if len(parts) < 3:
        raise ValueError("attack-magic option lacks three pipe fields")
    attr_token = parts[0].strip()
    if attr_token not in ATTR_INDEX:
        raise ValueError("attack-magic option has unknown attribute token")
    try:
        power = int(parts[1].strip(), 10)
        magic_level = int(parts[2].strip(), 10)
    except ValueError as exc:
        raise ValueError("attack-magic option power/level is not decimal") from exc
    return ATTR_INDEX[attr_token], power, magic_level


@dataclass(frozen=True)
class Recovered25AttackMagicEntry:
    skill_id: int
    magic_id: int
    item_config_id: int
    item_magicusemp: int
    magic_idx: int
    element: int
    power: int
    magic_level: int
    attacker_side1_matrix: tuple[tuple[int, ...], ...]
    attacker_side0_matrix: tuple[tuple[int, ...], ...]

    def __post_init__(self) -> None:
        for name in (
            "skill_id",
            "magic_id",
            "item_config_id",
            "item_magicusemp",
            "magic_idx",
            "element",
            "power",
            "magic_level",
        ):
            object.__setattr__(self, name, int(getattr(self, name)))
        for name in ("attacker_side1_matrix", "attacker_side0_matrix"):
            matrix = tuple(
                tuple(int(value) for value in row)
                for row in getattr(self, name)
            )
            if len(matrix) != 3 or any(len(row) != 5 for row in matrix):
                raise ValueError("AttackMagic footprint matrix must be 3x5")
            object.__setattr__(self, name, matrix)
        if self.magic_id not in ATTACK_MAGIC_TARGET_INDEX:
            raise ValueError("AttackMagic magic ID is outside fixed target table")
        if self.element not in range(4):
            raise ValueError("AttackMagic element must be 0..3")
        if self.magic_idx < 0:
            raise ValueError("AttackMagic IDX cannot be negative")


@dataclass(frozen=True)
class Recovered25EnemyAttackMagicPlan:
    skill_id: int
    magic_id: int
    item_config_id: int
    item_runtime_role: str
    magic_idx: int
    element: int
    power: int
    magic_level: int
    actor_slot: int
    source_target_slot: int
    source_selector: int
    normalized_selector: int | None
    target_membership: tuple[int, ...]
    source_sort_portable: bool
    source_target_order: tuple[int, ...] | None


@dataclass(frozen=True)
class Recovered25AttackMagicRuntime:
    entries: Mapping[int, Recovered25AttackMagicEntry]
    itemset_file: str
    source_version: str = SOURCE_VERSION
    evidence_role: str = LATER_RECOVERED
    nonplayer_item_role: str = NONPLAYER_ITEM_ROLE

    def __post_init__(self) -> None:
        if self.source_version != SOURCE_VERSION:
            raise ValueError("AttackMagic runtime source-version drift")
        if self.evidence_role != LATER_RECOVERED:
            raise ValueError("AttackMagic runtime must remain LATER_RECOVERED")
        normalized = {int(key): value for key, value in self.entries.items()}
        for key, entry in normalized.items():
            if key != entry.skill_id:
                raise ValueError("AttackMagic runtime skill-key drift")
        if len(normalized) != 25:
            raise ValueError("recovered25 AttackMagic runtime must contain 25 rows")
        if {entry.magic_id for entry in normalized.values()} != set(
            ATTACK_MAGIC_TARGET_INDEX
        ):
            raise ValueError(
                "recovered25 AttackMagic runtime magic population drift"
            )
        object.__setattr__(self, "entries", MappingProxyType(normalized))
        object.__setattr__(self, "itemset_file", str(self.itemset_file))

    def skill_id_for_magic(self, magic_id: int) -> int:
        matches = tuple(
            entry.skill_id
            for entry in self.entries.values()
            if entry.magic_id == int(magic_id)
        )
        if len(matches) != 1:
            raise ValueError(f"magic {magic_id} is not uniquely indexed")
        return matches[0]

    def resolve_enemy_footprint(
        self,
        *,
        skill_id: int,
        actor_slot: int,
        target_slot: int,
        alive_player_slots: Sequence[int],
        retarget_rolls_0_9: Sequence[int] = (),
        require_exact_source_order: bool = True,
    ) -> Recovered25EnemyAttackMagicPlan:
        try:
            entry = self.entries[int(skill_id)]
        except KeyError as exc:
            raise KeyError(f"unknown recovered25 AttackMagic skill {skill_id}") from exc

        actor_slot = int(actor_slot)
        target_slot = int(target_slot)
        if not 10 <= actor_slot <= 19:
            raise ValueError(
                "recovered25 enemy AttackMagic actor_slot must be 10..19"
            )
        if not 0 <= target_slot <= 9:
            raise ValueError(
                "recovered25 enemy AttackMagic source target must be 0..9"
            )

        alive = tuple(
            sorted(
                {
                    int(slot)
                    for slot in alive_player_slots
                    if 0 <= int(slot) <= 9
                }
            )
        )
        selector = remap_attack_magic_target(
            entry.magic_id,
            target_slot,
        )
        normalized = normalize_attack_magic_selector(
            selector,
            alive_slots=alive,
            retarget_rolls_0_9=retarget_rolls_0_9,
        )
        targets = (
            ()
            if normalized is None
            else footprint_target_set(
                selector=normalized,
                matrix=entry.attacker_side1_matrix,
                alive_slots=alive,
            )
        )
        portable = source_sort_is_portable(targets)
        order = source_sorted_targets(targets) if portable else None
        if require_exact_source_order and not portable:
            raise ValueError(
                "AttackMagic target membership is known but historical "
                "SortLoc/qsort order is nonportable"
            )

        return Recovered25EnemyAttackMagicPlan(
            skill_id=entry.skill_id,
            magic_id=entry.magic_id,
            item_config_id=entry.item_config_id,
            item_runtime_role=self.nonplayer_item_role,
            magic_idx=entry.magic_idx,
            element=entry.element,
            power=entry.power,
            magic_level=entry.magic_level,
            actor_slot=actor_slot,
            source_target_slot=target_slot,
            source_selector=selector,
            normalized_selector=normalized,
            target_membership=targets,
            source_sort_portable=portable,
            source_target_order=order,
        )


def load_recovered25_attack_magic_runtime(
    *,
    data_dir: Path,
    setup: Path | None = None,
) -> Recovered25AttackMagicRuntime:
    data_dir = Path(data_dir)
    setup = Path(setup) if setup is not None else None
    if not data_dir.is_dir():
        raise ValueError("recovered25 AttackMagic data_dir must be a directory")

    petskills = load_recovered25_petskill_runtime(
        data_dir=data_dir,
        setup=setup,
    )
    attack_skills = tuple(
        entry
        for entry in petskills.skills.values()
        if entry.function_name == ATTACK_SKILL_FUNC
    )
    if len(attack_skills) != 25:
        raise ValueError("recovered25 AttackMagic skill population drift")

    _, parsed_magic, magic_bad, _, _ = parse_magic(data_dir / "magic.txt")
    if magic_bad:
        raise ValueError("recovered25 magic.txt contains malformed rows")
    magic_by_id = {}
    for fields, values in parsed_magic:
        magic_id = int(values["ID"])
        if magic_id in magic_by_id:
            raise ValueError(f"duplicate recovered25 magic ID {magic_id}")
        magic_by_id[magic_id] = (fields, values)

    item_path = _active_itemset_path(data_dir, setup)
    item_by_id = _item_index(item_path)

    records = parse_attmagic(data_dir / "attmagic.bin")
    if len(records) % 2:
        raise ValueError("recovered25 attmagic record count is not even")
    magic_index_count = len(records) // 2

    entries = {}
    seen_magic = set()
    for skill in attack_skills:
        parsed = parse_source_shaped_option(skill.ascii_option())
        if (
            parsed["magic"] is None
            or not parsed["item_marker_after_magic"]
            or parsed["item"] is None
        ):
            raise ValueError(
                f"AttackMagic skill {skill.skill_id} lacks numeric magic/item pair"
            )
        magic_id = int(parsed["magic"])
        item_id = int(parsed["item"])
        if magic_id in seen_magic:
            raise ValueError(f"duplicate AttackMagic magic ID {magic_id}")
        seen_magic.add(magic_id)

        magic = magic_by_id.get(magic_id)
        if magic is None:
            raise ValueError(f"missing recovered magic row {magic_id}")
        fields, values = magic
        if len(fields) < 4 or fields[2] != ATTACK_MAGIC_FUNC:
            raise ValueError(f"magic {magic_id} is not MAGIC_AttMagic")
        idx = values.get("IDX")
        if idx is None:
            raise ValueError(f"magic {magic_id} lacks AttackMagic IDX")
        idx = int(idx)
        if not 0 <= idx < magic_index_count:
            raise ValueError(f"magic {magic_id} AttackMagic IDX out of range")
        element, power, magic_level = _parse_attack_option(fields[3])

        item = item_by_id.get(item_id)
        if item is None:
            raise ValueError(f"missing recovered item config {item_id}")
        linked_magic = item_int(item[ITEM_INDEX["magicid"]])
        if linked_magic != magic_id:
            raise ValueError(
                f"item {item_id} magicid does not match magic {magic_id}"
            )
        magicusemp = item_int(item[ITEM_INDEX["magicusemp"]])
        if magicusemp is None:
            raise ValueError(f"item {item_id} magicusemp is not decimal")

        entries[int(skill.skill_id)] = Recovered25AttackMagicEntry(
            skill_id=skill.skill_id,
            magic_id=magic_id,
            item_config_id=item_id,
            item_magicusemp=magicusemp,
            magic_idx=idx,
            element=element,
            power=power,
            magic_level=magic_level,
            attacker_side1_matrix=matrix_from_attmagic_record(
                records[idx * 2]
            ),
            attacker_side0_matrix=matrix_from_attmagic_record(
                records[idx * 2 + 1]
            ),
        )

    return Recovered25AttackMagicRuntime(
        entries=entries,
        itemset_file=item_path.name,
    )
