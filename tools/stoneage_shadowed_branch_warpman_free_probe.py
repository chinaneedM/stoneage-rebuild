#!/usr/bin/env python3
"""Classify the FREE-condition grammar on shadowed-branch WarpMan ingress.

Only condition key names, comparison operators and boolean structure are
emitted. Operand values, event/item/pet identifiers, dialogue, NPC names,
coordinates, filenames and full expressions are intentionally omitted.
"""

from __future__ import annotations

import argparse
import collections
from dataclasses import dataclass
from pathlib import Path

from tools.stoneage_ordered_runtime_world_reachability_probe import (
    load_ordered_runtime_reachability,
)
from tools.stoneage_transport_usage_probe import (
    assigned_file,
    iter_blocks,
    magic_kind,
    merge_file,
    template_map,
)


OUTPUT_RESOLUTION = (
    "RESOLUTION|SHADOWED_BRANCH_WARPMAN_FREE_GRAMMAR_AUDITED"
)

# Keys directly dispatched by fixed-descendant NPC_ActionFreeIfCheck.
# Feature-gated keys remain structurally recognized rather than assumed enabled.
KNOWN_CONDITION_KEYS = frozenset({
    "MT", "BOUNDTIME", "YEAR", "MON", "DAY", "HOUR", "MIN", "SEC",
    "DIYMAP", "FAME", "VIPPOINT", "VIP", "LV", "GOLD", "GLORY",
    "TRANS", "GTIME", "TIME", "PET", "ITEM", "EQUIT", "ENDEV",
    "EVEND", "NOWEV", "EVNOW", "PARTY", "REITEM", "REPET", "BBI",
    "FM", "DR", "DP", "CLASS", "SKILL", "SKNUM", "SKCP", "BOX",
    "PARTYCOUNT", "MANCOUNT", "WOMANCOUNT",
})


def _field(data: bytes, key: bytes) -> bytes | None:
    wanted = key.lower()
    for token in data.split(b"|"):
        if b":" not in token:
            continue
        name, value = token.split(b":", 1)
        if name.strip().lower() == wanted:
            return value.strip()
    return None


def _warp_floors(data: bytes) -> tuple[int, ...]:
    value = _field(data, b"WARP")
    if value is None:
        return ()
    floors = []
    for point in value.split(b";")[:20]:
        first = point.split(b",", 1)[0].strip()
        try:
            floor_id = int(first, 10)
        except ValueError:
            continue
        if floor_id > 0:
            floors.append(floor_id)
    return tuple(floors)


def _assigned_data(npc_dir: Path, arg: bytes) -> bytes | None:
    filename = assigned_file(arg)
    if filename is None:
        return arg
    path = npc_dir / filename
    if not path.is_file():
        return None
    return merge_file(path)


@dataclass(frozen=True)
class FreeAtom:
    key: str
    operator: str
    special_reduce: str | None

    def __post_init__(self) -> None:
        if self.operator not in {"=", "!=", "<", ">"}:
            raise ValueError("unsupported FREE comparison operator")
        if self.special_reduce not in {None, "STAR", "CARET"}:
            raise ValueError("invalid FREE special-reduce marker")


@dataclass(frozen=True)
class FreeClause:
    atoms: tuple[FreeAtom, ...]

    def __post_init__(self) -> None:
        if not self.atoms:
            raise ValueError("FREE clause cannot be empty")


@dataclass(frozen=True)
class FreeGrammarRow:
    source_floor: int
    target_floor: int
    clauses: tuple[FreeClause, ...]

    @property
    def atom_count(self) -> int:
        return sum(len(clause.atoms) for clause in self.clauses)

    @property
    def keys(self) -> tuple[str, ...]:
        return tuple(sorted({
            atom.key for clause in self.clauses for atom in clause.atoms
        }))

    @property
    def operators(self) -> tuple[str, ...]:
        return tuple(sorted({
            atom.operator
            for clause in self.clauses
            for atom in clause.atoms
        }))

    @property
    def unsupported_keys(self) -> tuple[str, ...]:
        return tuple(
            key for key in self.keys if key.upper() not in KNOWN_CONDITION_KEYS
        )


def _parse_atom(raw: bytes) -> FreeAtom | None:
    text = raw.strip()
    if not text:
        return None
    operator = None
    left = None
    right = None
    for candidate in (b"!=", b"<", b">", b"="):
        if candidate in text:
            left, right = text.split(candidate, 1)
            operator = candidate.decode("ascii")
            break
    if operator is None or left is None or right is None:
        return None

    left = left.strip()
    # NEW_WARPMAN optionally uses KEY-TEMP<op>VALUE. TEMP is an operand,
    # not part of the condition-dispatch key.
    if b"-" in left:
        left = left.split(b"-", 1)[0].strip()
    key = left.decode("ascii", "replace").upper()
    if not key:
        return None

    special = None
    if operator == "=":
        if b"*" in right:
            special = "STAR"
        elif b"^" in right:
            special = "CARET"
    return FreeAtom(key=key, operator=operator, special_reduce=special)


def parse_free_grammar(value: bytes) -> tuple[FreeClause, ...]:
    clauses = []
    for raw_clause in value.split(b","):
        atoms = []
        for raw_atom in raw_clause.split(b"&"):
            atom = _parse_atom(raw_atom)
            if atom is not None:
                atoms.append(atom)
        if atoms:
            clauses.append(FreeClause(atoms=tuple(atoms)))
    return tuple(clauses)


@dataclass(frozen=True)
class FreeGrammarAudit:
    rows: tuple[FreeGrammarRow, ...]
    missing_argument_files: int
    unparseable_free_rows: int

    @property
    def counts(self) -> dict[str, int]:
        out = collections.Counter()
        out["ingress_rows"] = len(self.rows)
        out["missing_argument_files"] = int(self.missing_argument_files)
        out["unparseable_free_rows"] = int(self.unparseable_free_rows)
        out["free_or_clauses"] = sum(len(row.clauses) for row in self.rows)
        out["free_atoms"] = sum(row.atom_count for row in self.rows)
        out["unsupported_condition_keys"] = sum(
            len(row.unsupported_keys) for row in self.rows
        )
        for row in self.rows:
            for key in row.keys:
                out[f"key:{key}:rows"] += 1
            for operator in row.operators:
                out[f"operator:{operator}:rows"] += 1
            for clause in row.clauses:
                if len(clause.atoms) > 1:
                    out["and_clauses"] += 1
        return dict(out)


def analyze(npc_dir: Path) -> FreeGrammarAudit:
    reachability = load_ordered_runtime_reachability()
    reached = set(reachability.reached_floor_ids)
    orphan_set = {row.floor_id for row in reachability.orphan_rows}

    files = sorted(
        (path for path in npc_dir.rglob("*") if path.is_file()),
        key=lambda path: str(path).lower(),
    )
    templates = template_map([
        path for path in files if magic_kind(path) == "template"
    ])
    names = {
        name for name, definitions in templates.items()
        if len(definitions) == 1 and definitions[0] == b"WarpMan"
    }

    rows = []
    missing = 0
    unparseable = 0
    for path in (p for p in files if magic_kind(p) == "create"):
        for entries in iter_blocks(path):
            fields: dict[bytes, bytes] = {}
            enemies: list[bytes] = []
            for key, value in entries:
                if key == b"enemy":
                    enemies.append(value)
                else:
                    fields[key] = value
            try:
                source_floor = int(fields.get(b"floorid", b"0"))
            except ValueError:
                continue
            if source_floor not in reached:
                continue
            if b"borncenter" not in fields and b"borncorner" not in fields:
                continue

            for enemy in enemies:
                name, sep, arg = enemy.partition(b"|")
                if name.strip() not in names:
                    continue
                data = _assigned_data(npc_dir, arg if sep else b"")
                if data is None:
                    missing += 1
                    continue
                targets = sorted(set(_warp_floors(data)) & orphan_set)
                if not targets:
                    continue
                free = _field(data, b"FREE")
                if free is None:
                    unparseable += 1
                    continue
                grammar = parse_free_grammar(free)
                if not grammar:
                    unparseable += 1
                    continue
                for target in targets:
                    rows.append(
                        FreeGrammarRow(
                            source_floor=source_floor,
                            target_floor=target,
                            clauses=grammar,
                        )
                    )

    return FreeGrammarAudit(
        rows=tuple(rows),
        missing_argument_files=missing,
        unparseable_free_rows=unparseable,
    )


def emit(audit: FreeGrammarAudit) -> None:
    print("StoneAge shadowed-branch WarpMan FREE grammar audit — R1")
    print(
        "SCOPE|WarpMan ingress into ordered classic-Warp orphan branch|"
        "condition keys/operators/boolean structure only"
    )
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print(
        "RULE|condition operands and original FREE expressions are not emitted"
    )
    for key in sorted(audit.counts):
        print(f"COUNT|{key}|{audit.counts[key]}")
    for row in audit.rows:
        keys = ",".join(row.keys)
        operators = ",".join(row.operators)
        specials = sorted({
            atom.special_reduce
            for clause in row.clauses
            for atom in clause.atoms
            if atom.special_reduce is not None
        })
        print(
            "WARPMAN_FREE_GRAMMAR|"
            f"source_floor={row.source_floor}|"
            f"target_floor={row.target_floor}|"
            f"or_clauses={len(row.clauses)}|"
            f"atoms={row.atom_count}|"
            f"keys={keys}|"
            f"operators={operators}|"
            f"and_clauses={sum(len(c.atoms) > 1 for c in row.clauses)}|"
            f"special_reduce={','.join(specials) if specials else 'NONE'}|"
            f"unsupported_keys={','.join(row.unsupported_keys) if row.unsupported_keys else 'NONE'}"
        )
    print(OUTPUT_RESOLUTION)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--npc-dir", type=Path, required=True)
    args = parser.parse_args()
    emit(analyze(args.npc_dir))


if __name__ == "__main__":
    main()
