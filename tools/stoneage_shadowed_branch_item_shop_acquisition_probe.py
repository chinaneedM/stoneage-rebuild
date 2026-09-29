#!/usr/bin/env python3
"""Check whether the shadowed-branch WarpMan key item is sold by a reachable ItemShop.

The target item ID is recovered transiently from the unique ITEM equality atom
of the 811 -> orphan-branch WarpMan FREE condition.  The ID, shop ItemList
payloads, NPC names, filenames and coordinates are never emitted.

The fixed descendant ItemShop semantics are reproduced for acquisition
screening: ItemList accepts comma-separated IDs/ranges, skips undefined item
IDs, and stops after MAXSHOPITEM (33) valid entries.
"""

from __future__ import annotations

import argparse
import collections
from dataclasses import dataclass
from pathlib import Path

from tools.stoneage_ordered_runtime_world_reachability_probe import (
    load_ordered_runtime_reachability,
)
from tools.stoneage_shadowed_branch_warpman_satisfiability_probe import (
    ITEM,
    _assigned_data,
    _configured_itemset_paths,
    _field,
    _int_prefix,
    _item_ids,
    _warp_floors,
    parse_free_predicates,
)
from tools.stoneage_transport_usage_probe import (
    iter_blocks,
    magic_kind,
    template_map,
)


MAXSHOPITEM = 33
OUTPUT_RESOLUTION = "RESOLUTION|SHADOWED_BRANCH_KEY_ITEM_REACHABLE_SHOP_AUDITED"


@dataclass(frozen=True)
class ShopWitness:
    source_floor: int
    target_listed: bool
    target_effectively_visible: bool
    valid_entries_before_or_at_target: int | None
    buy_rate_class: str


@dataclass(frozen=True)
class ShopAudit:
    candidate_shops: tuple[ShopWitness, ...]
    missing_argument_files: int
    target_predicate_count: int

    @property
    def counts(self) -> dict[str, int]:
        out = collections.Counter({
            "candidate_shops": 0,
            "target_listed_shops": 0,
            "target_visible_shops": 0,
            "missing_argument_files": int(self.missing_argument_files),
            "target_predicate_count": int(self.target_predicate_count),
        })
        for row in self.candidate_shops:
            out["candidate_shops"] += 1
            out["target_listed_shops"] += int(row.target_listed)
            out["target_visible_shops"] += int(row.target_effectively_visible)
            out[f"buy_rate:{row.buy_rate_class}:shops"] += 1
        return dict(out)


def _template_function_names(
    npc_dir: Path,
    function_name: bytes,
) -> set[bytes]:
    files = sorted(
        (path for path in npc_dir.rglob("*") if path.is_file()),
        key=lambda path: str(path).lower(),
    )
    templates = template_map([
        path for path in files if magic_kind(path) == "template"
    ])
    return {
        name for name, definitions in templates.items()
        if len(definitions) == 1 and definitions[0] == function_name
    }


def _locate_key_item(npc_dir: Path) -> tuple[int, int]:
    reachability = load_ordered_runtime_reachability()
    reached = set(reachability.reached_floor_ids)
    targets = {row.floor_id for row in reachability.orphan_rows}
    warpman_names = _template_function_names(npc_dir, b"WarpMan")

    predicates = []
    missing = 0
    files = sorted(
        (path for path in npc_dir.rglob("*") if path.is_file()),
        key=lambda path: str(path).lower(),
    )
    for create_path in (
        path for path in files if magic_kind(path) == "create"
    ):
        for entries in iter_blocks(create_path):
            fields: dict[bytes, bytes] = {}
            enemies: list[bytes] = []
            for key, value in entries:
                if key == b"enemy":
                    enemies.append(value)
                else:
                    fields[key] = value
            try:
                floor = int(fields.get(b"floorid", b"0"))
            except ValueError:
                continue
            if floor not in reached:
                continue
            if b"borncenter" not in fields and b"borncorner" not in fields:
                continue
            for enemy in enemies:
                name, separator, arg = enemy.partition(b"|")
                if name.strip() not in warpman_names:
                    continue
                data = _assigned_data(npc_dir, arg if separator else b"")
                if data is None:
                    missing += 1
                    continue
                if not (set(_warp_floors(data)) & targets):
                    continue
                free = _field(data, b"FREE")
                if free is None:
                    continue
                for clause in parse_free_predicates(free):
                    for atom in clause:
                        if (
                            atom is not None
                            and atom.key == ITEM
                            and atom.operator == "="
                        ):
                            predicates.append(atom.operand)

    unique = sorted(set(predicates))
    if len(predicates) != 1 or len(unique) != 1:
        raise ValueError(
            "expected exactly one unique ITEM equality predicate on shadowed ingress"
        )
    return int(unique[0]), missing


def _buy_rate_class(data: bytes) -> str:
    value = _field(data, b"buy_rate")
    if value is None or not value.strip():
        return "DEFAULT_ONE"
    try:
        rate = float(value.decode("ascii", "strict").strip())
    except (ValueError, UnicodeDecodeError):
        return "UNPARSEABLE"
    if rate < 0:
        return "NEGATIVE"
    if rate == 0:
        return "ZERO"
    return "POSITIVE"


def _parse_range(token: bytes) -> tuple[int, int] | None:
    text = token.strip()
    if not text:
        return None
    if b"-" not in text:
        value = _int_prefix(text)
        if value is None:
            return None
        return int(value), int(value)
    left, right = text.split(b"-", 1)
    a = _int_prefix(left)
    b = _int_prefix(right)
    if a is None or b is None:
        return None
    lo, hi = sorted((int(a), int(b)))
    return lo, hi


def _shop_item_visibility(
    item_list: bytes,
    target_item_id: int,
    active_item_ids: frozenset[int],
) -> tuple[bool, bool, int | None]:
    target_listed = False
    valid_count = 0
    target_rank = None

    for raw in item_list.split(b","):
        bounds = _parse_range(raw)
        if bounds is None:
            continue
        lo, hi = bounds
        if lo <= target_item_id <= hi:
            target_listed = True

        # Reproduce ITEM_getNameFromNumber skip + MAXSHOPITEM truncation using
        # the configured item catalog as the validity domain.
        candidates = sorted(
            item_id for item_id in active_item_ids
            if lo <= item_id <= hi
        )
        for item_id in candidates:
            valid_count += 1
            if item_id == target_item_id and target_rank is None:
                target_rank = valid_count
            if valid_count >= MAXSHOPITEM:
                return (
                    target_listed,
                    target_rank is not None and target_rank <= MAXSHOPITEM,
                    target_rank,
                )

    return (
        target_listed,
        target_rank is not None and target_rank <= MAXSHOPITEM,
        target_rank,
    )


def analyze(npc_dir: Path, setup: Path, data_dir: Path) -> ShopAudit:
    target_item_id, missing_from_warp = _locate_key_item(npc_dir)
    item_paths = _configured_itemset_paths(setup, data_dir)
    active_item_ids = _item_ids(item_paths)
    if target_item_id not in active_item_ids:
        raise ValueError("shadowed-branch key item absent from active item catalog")

    reachability = load_ordered_runtime_reachability()
    reached = set(reachability.reached_floor_ids)
    itemshop_names = _template_function_names(npc_dir, b"ItemShop")

    rows = []
    missing = missing_from_warp
    files = sorted(
        (path for path in npc_dir.rglob("*") if path.is_file()),
        key=lambda path: str(path).lower(),
    )
    for create_path in (
        path for path in files if magic_kind(path) == "create"
    ):
        for entries in iter_blocks(create_path):
            fields: dict[bytes, bytes] = {}
            enemies: list[bytes] = []
            for key, value in entries:
                if key == b"enemy":
                    enemies.append(value)
                else:
                    fields[key] = value
            try:
                floor = int(fields.get(b"floorid", b"0"))
            except ValueError:
                continue
            if floor not in reached:
                continue
            if b"borncenter" not in fields and b"borncorner" not in fields:
                continue

            for enemy in enemies:
                name, separator, arg = enemy.partition(b"|")
                if name.strip() not in itemshop_names:
                    continue
                data = _assigned_data(npc_dir, arg if separator else b"")
                if data is None:
                    missing += 1
                    continue
                item_list = _field(data, b"ItemList")
                if item_list is None:
                    rows.append(
                        ShopWitness(
                            source_floor=floor,
                            target_listed=False,
                            target_effectively_visible=False,
                            valid_entries_before_or_at_target=None,
                            buy_rate_class=_buy_rate_class(data),
                        )
                    )
                    continue
                listed, visible, rank = _shop_item_visibility(
                    item_list,
                    target_item_id,
                    active_item_ids,
                )
                rows.append(
                    ShopWitness(
                        source_floor=floor,
                        target_listed=listed,
                        target_effectively_visible=visible,
                        valid_entries_before_or_at_target=rank,
                        buy_rate_class=_buy_rate_class(data),
                    )
                )

    return ShopAudit(
        candidate_shops=tuple(rows),
        missing_argument_files=missing,
        target_predicate_count=1,
    )


def emit(audit: ShopAudit) -> None:
    print("StoneAge shadowed-branch key-item reachable ItemShop audit — R1")
    print(
        "SCOPE|unique WarpMan ITEM equality predicate|"
        "classic-reachable recovered ItemShop inventory"
    )
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print(
        "RULE|target item ID, ItemList payloads, NPC names, filenames, "
        "coordinates and raw arguments are not emitted"
    )
    print(
        "RULE|visibility reproduces fixed descendant ItemShop ItemList range "
        "expansion, undefined-item skip and MAXSHOPITEM=33 truncation"
    )
    print(
        "RULE|shop visibility proves a normal purchase surface exists; "
        "it does not by itself prove economic affordability or prerequisite dialogue"
    )
    for key in sorted(audit.counts):
        print(f"COUNT|{key}|{audit.counts[key]}")

    witness_floors = sorted({
        row.source_floor
        for row in audit.candidate_shops
        if row.target_effectively_visible
    })
    print(f"COUNT|target_visible_source_floors|{len(witness_floors)}")
    if witness_floors:
        print(
            "TARGET_ITEM_SHOP_WITNESS|"
            f"reachable_source_floors={len(witness_floors)}|"
            "item_id_withheld=1|"
            "normal_purchase_surface=1"
        )
    else:
        print(
            "TARGET_ITEM_SHOP_WITNESS|"
            "reachable_source_floors=0|"
            "item_id_withheld=1|"
            "normal_purchase_surface=0"
        )
    print(OUTPUT_RESOLUTION)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--npc-dir", type=Path, required=True)
    parser.add_argument("--setup", type=Path, required=True)
    parser.add_argument("--data-dir", type=Path, required=True)
    args = parser.parse_args()
    emit(analyze(args.npc_dir, args.setup, args.data_dir))


if __name__ == "__main__":
    main()
