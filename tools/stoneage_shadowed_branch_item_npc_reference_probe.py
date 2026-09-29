#!/usr/bin/env python3
"""Census reachable NPC argument semantics that reference the shadowed key item.

The key item ID is recovered transiently and withheld.  Output is limited to
technical NPC FunctionSet names, argument field keys and aggregate counts.
This is a discovery probe: a reference is not automatically an acquisition
proof.
"""

from __future__ import annotations

import argparse
import collections
import re
from dataclasses import dataclass
from pathlib import Path

from tools.stoneage_ordered_runtime_world_reachability_probe import (
    load_ordered_runtime_reachability,
)
from tools.stoneage_shadowed_branch_item_shop_acquisition_probe import (
    _locate_key_item,
)
from tools.stoneage_shadowed_branch_warpman_satisfiability_probe import (
    _assigned_data,
)
from tools.stoneage_transport_usage_probe import (
    iter_blocks,
    magic_kind,
    template_map,
)


OUTPUT_RESOLUTION = "RESOLUTION|SHADOWED_BRANCH_KEY_ITEM_NPC_REFERENCE_CENSUS_AUDITED"


def _safe_ascii(value: bytes) -> str:
    text = value.decode("ascii", "replace").strip()
    text = re.sub(r"[^A-Za-z0-9_.-]+", "_", text)
    return text[:80] or "EMPTY"


def _contains_integer_token(value: bytes, target: int) -> bool:
    pattern = rb"(?<![0-9])" + str(target).encode("ascii") + rb"(?![0-9])"
    return re.search(pattern, value) is not None


def _argument_fields(data: bytes) -> tuple[tuple[bytes, bytes], ...]:
    rows = []
    normalized = data.replace(b"\r", b"\n")
    for line in normalized.split(b"\n"):
        for token in line.split(b"|"):
            token = token.strip()
            if b":" not in token:
                continue
            key, value = token.split(b":", 1)
            key = key.strip()
            if key:
                rows.append((key, value.strip()))
    return tuple(rows)


@dataclass(frozen=True)
class ReferenceClass:
    function_set: str
    field_key: str
    create_rows: int
    source_floors: int


@dataclass(frozen=True)
class ReferenceAudit:
    classes: tuple[ReferenceClass, ...]
    matching_create_rows: int
    matching_field_occurrences: int
    missing_argument_files: int

    @property
    def counts(self) -> dict[str, int]:
        return {
            "reference_classes": len(self.classes),
            "matching_create_rows": self.matching_create_rows,
            "matching_field_occurrences": self.matching_field_occurrences,
            "missing_argument_files": self.missing_argument_files,
        }


def analyze(npc_dir: Path) -> ReferenceAudit:
    target_item_id, missing = _locate_key_item(npc_dir)
    reachability = load_ordered_runtime_reachability()
    reached = set(reachability.reached_floor_ids)

    files = sorted(
        (path for path in npc_dir.rglob("*") if path.is_file()),
        key=lambda path: str(path).lower(),
    )
    templates = template_map([
        path for path in files if magic_kind(path) == "template"
    ])
    functions = {
        name: definitions[0]
        for name, definitions in templates.items()
        if len(definitions) == 1
    }

    class_rows: dict[tuple[str, str], int] = collections.Counter()
    class_floors: dict[tuple[str, str], set[int]] = collections.defaultdict(set)
    matching_create_rows = 0
    matching_field_occurrences = 0

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
                function = functions.get(name.strip())
                if function is None:
                    continue
                data = _assigned_data(npc_dir, arg if separator else b"")
                if data is None:
                    missing += 1
                    continue

                matched_this_create = False
                for key, value in _argument_fields(data):
                    if not _contains_integer_token(value, target_item_id):
                        continue
                    matched_this_create = True
                    matching_field_occurrences += 1
                    cls = (_safe_ascii(function), _safe_ascii(key))
                    class_rows[cls] += 1
                    class_floors[cls].add(floor)
                if matched_this_create:
                    matching_create_rows += 1

    classes = tuple(
        ReferenceClass(
            function_set=function,
            field_key=field,
            create_rows=class_rows[(function, field)],
            source_floors=len(class_floors[(function, field)]),
        )
        for function, field in sorted(class_rows)
    )
    return ReferenceAudit(
        classes=classes,
        matching_create_rows=matching_create_rows,
        matching_field_occurrences=matching_field_occurrences,
        missing_argument_files=missing,
    )


def emit(audit: ReferenceAudit) -> None:
    print("StoneAge shadowed-branch key-item reachable NPC reference census — R1")
    print(
        "SCOPE|unique WarpMan ITEM equality target|"
        "classic-reachable recovered NPC create arguments"
    )
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print(
        "RULE|target item ID, NPC/template names, filenames, dialogue, "
        "coordinates and raw argument values are not emitted"
    )
    print(
        "RULE|a technical FunctionSet/field reference is a discovery lead, "
        "not an acquisition proof until its runtime semantics and gate are closed"
    )
    for key in sorted(audit.counts):
        print(f"COUNT|{key}|{audit.counts[key]}")
    for row in audit.classes:
        print(
            "NPC_KEY_ITEM_REFERENCE|"
            f"function={row.function_set}|"
            f"field={row.field_key}|"
            f"create_rows={row.create_rows}|"
            f"source_floors={row.source_floors}"
        )
    print(OUTPUT_RESOLUTION)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--npc-dir", type=Path, required=True)
    args = parser.parse_args()
    emit(analyze(args.npc_dir))


if __name__ == "__main__":
    main()
