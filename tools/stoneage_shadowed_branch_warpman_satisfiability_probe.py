#!/usr/bin/env python3
"""Audit whether the recovered shadowed-branch WarpMan FREE gate has domain witnesses.

The recovered argument operands are used transiently but never emitted.  The
report is deliberately weaker than a gameplay-reachability proof:

* LV predicates are checked against the recovered server MAXLEVEL domain.
* ITEM predicates are checked against IDs declared by configured active
  itemset files.
* An itemset witness proves only that a matching item definition exists.  It
  does not prove that the item is obtainable, co-obtainable, or legitimately
  carried by a player at the point of travel.

This keeps the next provenance seam explicit: acquisition/content evidence.
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
    "RESOLUTION|SHADOWED_BRANCH_WARPMAN_FREE_DOMAIN_AUDITED"
)
LEVEL = "LV"
ITEM = "ITEM"
SUPPORTED_KEYS = frozenset({LEVEL, ITEM})
SUPPORTED_OPERATORS = frozenset({"=", "!=", "<", ">"})


def _field(data: bytes, key: bytes) -> bytes | None:
    wanted = key.strip().lower()
    for token in data.split(b"|"):
        if b":" not in token:
            continue
        name, value = token.split(b":", 1)
        if name.strip().lower() == wanted:
            return value.strip()
    return None


def _int_prefix(value: bytes) -> int | None:
    text = value.strip()
    if not text:
        return None
    sign = 1
    if text[:1] in (b"+", b"-"):
        sign = -1 if text[:1] == b"-" else 1
        text = text[1:]
    total = 0
    found = False
    for ch in text:
        if not 48 <= ch <= 57:
            break
        found = True
        total = total * 10 + ch - 48
    return sign * total if found else None


@dataclass(frozen=True)
class Predicate:
    key: str
    operator: str
    operand: int

    def __post_init__(self) -> None:
        if self.operator not in SUPPORTED_OPERATORS:
            raise ValueError("unsupported comparison operator")


def _parse_predicate(raw: bytes) -> Predicate | None:
    text = raw.strip()
    if not text:
        return None
    operator = None
    left = right = None
    for candidate in (b"!=", b"<", b">", b"="):
        if candidate in text:
            left, right = text.split(candidate, 1)
            operator = candidate.decode("ascii")
            break
    if operator is None or left is None or right is None:
        return None

    left = left.strip()
    if b"-" in left:
        left = left.split(b"-", 1)[0].strip()
    key = left.decode("ascii", "replace").upper()
    # "*" and "^" are special item-count forms in descendant source and
    # deliberately require a separate semantic audit.
    if b"*" in right or b"^" in right:
        return None
    operand = _int_prefix(right)
    if not key or operand is None:
        return None
    return Predicate(key=key, operator=operator, operand=operand)


def parse_free_predicates(
    value: bytes,
) -> tuple[tuple[Predicate, ...], ...]:
    clauses = []
    for raw_clause in value.split(b","):
        atoms = []
        for raw_atom in raw_clause.split(b"&"):
            predicate = _parse_predicate(raw_atom)
            if predicate is None:
                if raw_atom.strip():
                    atoms.append(None)
                continue
            atoms.append(predicate)
        if atoms:
            clauses.append(tuple(atoms))
    return tuple(clauses)


def _compare(value: int, operator: str, operand: int) -> bool:
    if operator == "=":
        return value == operand
    if operator == "!=":
        return value != operand
    if operator == "<":
        return value < operand
    if operator == ">":
        return value > operand
    raise ValueError("unsupported comparison operator")


def _configured_maxlevel(setup: Path) -> int:
    found = []
    for raw in setup.read_bytes().splitlines():
        line = raw.split(b"#", 1)[0].strip()
        if b"=" not in line:
            continue
        key, value = line.split(b"=", 1)
        if key.strip().upper() != b"MAXLEVEL":
            continue
        parsed = _int_prefix(value)
        if parsed is not None and parsed > 0:
            found.append(parsed)
    if not found:
        raise ValueError("recovered setup.cf has no positive MAXLEVEL")
    if len(set(found)) != 1:
        raise ValueError("recovered setup.cf has conflicting MAXLEVEL values")
    return int(found[0])


def _configured_itemset_paths(setup: Path, data_dir: Path) -> tuple[Path, ...]:
    values = []
    for raw in setup.read_bytes().splitlines():
        line = raw.split(b"#", 1)[0].strip()
        if b"=" not in line:
            continue
        key, value = line.split(b"=", 1)
        name = key.strip().lower()
        if not (name.startswith(b"itemset") and name.endswith(b"file")):
            continue
        rel = value.decode("utf-8", "replace").strip().replace("\\", "/")
        if not rel:
            continue
        base = Path(rel).name
        path = data_dir / base
        values.append(path)
    unique = tuple(sorted(set(values), key=lambda path: str(path).lower()))
    if not unique:
        fallback = data_dir / "itemset.txt"
        if fallback.is_file():
            return (fallback,)
        raise ValueError("no configured recovered itemset file")
    missing = [path for path in unique if not path.is_file()]
    if missing:
        raise ValueError("configured recovered itemset file is missing")
    return unique


def _item_ids(paths: tuple[Path, ...]) -> frozenset[int]:
    ids = set()
    for path in paths:
        for raw in path.read_bytes().splitlines():
            line = raw.strip()
            if not line or line.startswith(b"#"):
                continue
            fields = [part.strip() for part in line.replace(b"\t", b" ").split(b",")]
            if len(fields) <= 16:
                continue
            parsed = _int_prefix(fields[16])
            if parsed is not None:
                ids.add(int(parsed))
    if not ids:
        raise ValueError("configured recovered itemset has no parseable IDs")
    return frozenset(ids)


def _assigned_data(npc_dir: Path, arg: bytes) -> bytes | None:
    filename = assigned_file(arg)
    if filename is None:
        return arg
    path = npc_dir / filename
    if not path.is_file():
        return None
    return merge_file(path)


def _warp_floors(data: bytes) -> tuple[int, ...]:
    value = _field(data, b"WARP")
    if value is None:
        return ()
    floors = []
    for point in value.split(b";")[:20]:
        first = point.split(b",", 1)[0]
        parsed = _int_prefix(first)
        if parsed is not None and parsed > 0:
            floors.append(int(parsed))
    return tuple(floors)


@dataclass(frozen=True)
class AtomWitness:
    key: str
    operator: str
    witness: bool | None

    @property
    def domain(self) -> str:
        if self.key == LEVEL:
            return "RECOVERED_LEVEL_DOMAIN"
        if self.key == ITEM:
            return "ACTIVE_ITEM_CATALOG"
        return "UNSUPPORTED"


@dataclass(frozen=True)
class ClauseWitness:
    atoms: tuple[AtomWitness, ...]
    satisfiable: bool

    def __post_init__(self) -> None:
        if not self.atoms:
            raise ValueError("domain clause cannot be empty")


@dataclass(frozen=True)
class IngressWitness:
    source_floor: int
    destination_floor: int
    clauses: tuple[ClauseWitness, ...]

    @property
    def satisfiable(self) -> bool:
        return any(clause.satisfiable for clause in self.clauses)


@dataclass(frozen=True)
class DomainAudit:
    rows: tuple[IngressWitness, ...]
    missing_argument_files: int
    configured_itemset_files: int
    item_catalog_size: int
    maxlevel_configured: bool

    @property
    def counts(self) -> dict[str, int]:
        out = collections.Counter({
            "unsupported_atoms": 0,
            "atoms_with_domain_witness": 0,
            "atoms_without_domain_witness": 0,
            "domain_satisfiable_rows": 0,
            "domain_satisfiable_clauses": 0,
            "atoms": 0,
            "clauses": 0,
        })
        out["ingress_rows"] = len(self.rows)
        out["missing_argument_files"] = int(self.missing_argument_files)
        out["configured_itemset_files"] = int(self.configured_itemset_files)
        out["item_catalog_nonempty"] = int(self.item_catalog_size > 0)
        out["maxlevel_configured"] = int(self.maxlevel_configured)
        for row in self.rows:
            out["clauses"] += len(row.clauses)
            out["domain_satisfiable_rows"] += int(row.satisfiable)
            for clause in row.clauses:
                out["domain_satisfiable_clauses"] += int(clause.satisfiable)
                for atom in clause.atoms:
                    out["atoms"] += 1
                    out[f"key:{atom.key}:atoms"] += 1
                    out[f"operator:{atom.operator}:atoms"] += 1
                    if atom.witness is None:
                        out["unsupported_atoms"] += 1
                    else:
                        out["atoms_with_domain_witness"] += int(atom.witness)
                        out["atoms_without_domain_witness"] += int(not atom.witness)
        return dict(out)


def _clause_witness(
    predicates: tuple[Predicate | None, ...],
    *,
    maxlevel: int,
    item_ids: frozenset[int],
) -> ClauseWitness:
    level_predicates = tuple(
        atom for atom in predicates
        if atom is not None and atom.key == LEVEL
    )
    level_joint = None
    if level_predicates:
        level_joint = any(
            all(_compare(level, atom.operator, atom.operand) for atom in level_predicates)
            for level in range(1, maxlevel + 1)
        )

    witnesses = []
    for atom in predicates:
        if atom is None:
            witnesses.append(AtomWitness("UNPARSEABLE", "?", None))
        elif atom.key == LEVEL:
            witnesses.append(
                AtomWitness(atom.key, atom.operator, bool(level_joint))
            )
        elif atom.key == ITEM:
            witnesses.append(
                AtomWitness(
                    atom.key,
                    atom.operator,
                    any(
                        _compare(item_id, atom.operator, atom.operand)
                        for item_id in item_ids
                    ),
                )
            )
        else:
            witnesses.append(AtomWitness(atom.key, atom.operator, None))

    satisfiable = bool(witnesses) and all(
        atom.witness is True for atom in witnesses
    )
    return ClauseWitness(atoms=tuple(witnesses), satisfiable=satisfiable)


def analyze(npc_dir: Path, setup: Path, data_dir: Path) -> DomainAudit:
    maxlevel = _configured_maxlevel(setup)
    itemset_paths = _configured_itemset_paths(setup, data_dir)
    item_ids = _item_ids(itemset_paths)

    reachability = load_ordered_runtime_reachability()
    reached = set(reachability.reached_floor_ids)
    target_set = {row.floor_id for row in reachability.orphan_rows}

    files = sorted(
        (path for path in npc_dir.rglob("*") if path.is_file()),
        key=lambda path: str(path).lower(),
    )
    templates = template_map([
        path for path in files if magic_kind(path) == "template"
    ])
    warpman_names = {
        name for name, definitions in templates.items()
        if len(definitions) == 1 and definitions[0] == b"WarpMan"
    }

    rows = []
    missing = 0
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
                source_floor = int(fields.get(b"floorid", b"0"))
            except ValueError:
                continue
            if source_floor not in reached:
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
                targets = sorted(set(_warp_floors(data)) & target_set)
                if not targets:
                    continue
                free = _field(data, b"FREE")
                if free is None:
                    clauses = ()
                else:
                    clauses = tuple(
                        _clause_witness(
                            clause,
                            maxlevel=maxlevel,
                            item_ids=item_ids,
                        )
                        for clause in parse_free_predicates(free)
                    )
                for destination_floor in targets:
                    rows.append(
                        IngressWitness(
                            source_floor=source_floor,
                            destination_floor=destination_floor,
                            clauses=clauses,
                        )
                    )

    return DomainAudit(
        rows=tuple(rows),
        missing_argument_files=missing,
        configured_itemset_files=len(itemset_paths),
        item_catalog_size=len(item_ids),
        maxlevel_configured=True,
    )


def emit(audit: DomainAudit) -> None:
    print("StoneAge shadowed-branch WarpMan FREE domain audit — R1")
    print(
        "SCOPE|reachable WarpMan ingress into ordered classic-Warp orphan branch|"
        "level-domain + active-item-catalog witness only"
    )
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print(
        "RULE|raw FREE operands, item IDs, argument payloads, dialogue, NPC names, "
        "coordinates and filenames are not emitted"
    )
    print(
        "RULE|catalog witness proves a matching configured item definition exists; "
        "it does not prove gameplay acquisition or co-obtainability"
    )
    print(
        "RULE|multiple ITEM atoms are independent existential carried-item checks; "
        "LV atoms share one player-level value"
    )
    for key in sorted(audit.counts):
        print(f"COUNT|{key}|{audit.counts[key]}")

    for row in audit.rows:
        atom_count = sum(len(clause.atoms) for clause in row.clauses)
        print(
            "WARPMAN_FREE_DOMAIN|"
            f"source_floor={row.source_floor}|"
            f"target_floor={row.destination_floor}|"
            f"clauses={len(row.clauses)}|"
            f"atoms={atom_count}|"
            f"domain_satisfiable={int(row.satisfiable)}|"
            "reachability_proof=NO_CATALOG_WITNESS_ONLY"
        )
        for clause_index, clause in enumerate(row.clauses, 1):
            for atom_index, atom in enumerate(clause.atoms, 1):
                witness = (
                    "UNKNOWN"
                    if atom.witness is None
                    else str(int(atom.witness))
                )
                print(
                    "ATOM_DOMAIN|"
                    f"source_floor={row.source_floor}|"
                    f"target_floor={row.destination_floor}|"
                    f"clause={clause_index}|atom={atom_index}|"
                    f"key={atom.key}|operator={atom.operator}|"
                    f"domain={atom.domain}|witness={witness}"
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
