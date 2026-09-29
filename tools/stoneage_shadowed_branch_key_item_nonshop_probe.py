#!/usr/bin/env python3
"""Audit non-shop acquisition surfaces for the shadowed-branch key item.

The target item identity is recovered transiently from the unique WarpMan ITEM
equality predicate and is never emitted.

Two acquisition families are screened:
1. stable/reachable recovered encounter -> group -> enemy drop chains;
2. reachable NPC arguments carrying AddItem actions, with fixed-descendant
   Action_RunDoEventAction function-set coverage separated from generic token
   presence.

The result remains a provenance-safe acquisition audit, not a full quest solver.
"""

from __future__ import annotations

import argparse
import collections
from dataclasses import dataclass
from pathlib import Path

from tools.stoneage_encount_chain_probe import (
    analyze as analyze_encounter_chain,
)
from tools.stoneage_ordered_runtime_world_reachability_probe import (
    load_ordered_runtime_reachability,
)
from tools.stoneage_shadowed_branch_item_shop_acquisition_probe import (
    _locate_key_item,
)
from tools.stoneage_shadowed_branch_warpman_satisfiability_probe import (
    _assigned_data,
    _int_prefix,
)
from tools.stoneage_transport_usage_probe import (
    iter_blocks,
    magic_kind,
    template_map,
)


OUTPUT_RESOLUTION = "RESOLUTION|SHADOWED_BRANCH_KEY_ITEM_NONSHOP_ACQUISITION_AUDITED"

# Fixed descendant source files with direct Action_RunDoEventAction call sites.
ACTION_RUN_FUNCTIONSETS = frozenset({
    "warpman",
    "makepair",
    "npcenemy",
    "freepetskillshop",
})


@dataclass(frozen=True)
class DropWitness:
    floor_id: int
    group_gate_class: str
    probability_class: str


@dataclass(frozen=True)
class NpcRewardWitness:
    floor_id: int
    function_set: str
    action_run_covered: bool


@dataclass(frozen=True)
class AcquisitionAudit:
    drop_witnesses: tuple[DropWitness, ...]
    npc_reward_witnesses: tuple[NpcRewardWitness, ...]
    npc_additem_token_hits: int
    missing_argument_files: int

    @property
    def counts(self) -> dict[str, int]:
        out = collections.Counter({
            "drop_witnesses": len(self.drop_witnesses),
            "drop_source_floors": len({x.floor_id for x in self.drop_witnesses}),
            "npc_reward_witnesses": len(self.npc_reward_witnesses),
            "npc_reward_source_floors": len({
                x.floor_id for x in self.npc_reward_witnesses
            }),
            "npc_additem_token_hits": int(self.npc_additem_token_hits),
            "npc_action_run_covered_witnesses": sum(
                x.action_run_covered for x in self.npc_reward_witnesses
            ),
            "missing_argument_files": int(self.missing_argument_files),
        })
        for witness in self.drop_witnesses:
            out[f"drop_gate:{witness.group_gate_class}:witnesses"] += 1
            out[f"drop_probability:{witness.probability_class}:witnesses"] += 1
        for witness in self.npc_reward_witnesses:
            key = witness.function_set or "EMPTY"
            out[f"npc_function:{key}:witnesses"] += 1
        return dict(out)


def _template_function_map(npc_dir: Path) -> dict[bytes, str]:
    files = sorted(
        (path for path in npc_dir.rglob("*") if path.is_file()),
        key=lambda path: str(path).lower(),
    )
    templates = template_map([
        path for path in files if magic_kind(path) == "template"
    ])
    out = {}
    for name, definitions in templates.items():
        if len(definitions) == 1:
            out[name] = definitions[0].decode("ascii", "replace")
    return out


def _iter_additem_values(data: bytes):
    # NPC argument grammar is pipe-keyed; assigned files may contain multiple
    # action records, so scan every token rather than only the first key.
    normalized = data.replace(b"\r", b"\n")
    for line in normalized.split(b"\n"):
        for token in line.split(b"|"):
            if b":" not in token:
                continue
            key, value = token.split(b":", 1)
            if key.strip().lower() == b"additem":
                yield value.strip()


def _contains_item_id(value: bytes, target: int) -> bool:
    for part in value.split(b","):
        parsed = _int_prefix(part)
        if parsed is not None and int(parsed) == int(target):
            return True
    return False


def _group_gate_class(
    appear_item: int,
    not_appear_item: int,
    target_item: int,
) -> str:
    appear = int(appear_item)
    not_appear = int(not_appear_item)
    if appear == target_item:
        return "CIRCULAR_REQUIRES_TARGET"
    if appear > 0:
        return "REQUIRES_OTHER_ITEM"
    if not_appear == target_item:
        return "TARGET_ABSENCE_ALLOWED"
    if not_appear > 0:
        return "EXCLUDES_OTHER_ITEM"
    return "UNGATED"


def _drop_probability_class(probability: int) -> str:
    p = int(probability)
    if p <= 0:
        return "NONPOSITIVE"
    if p >= 1000:
        return "FIX_THOUSAND_CERTAIN_OR_OVER"
    return "POSITIVE"


def _drop_witnesses(
    *,
    data_dir: Path,
    setup: Path,
    target_item: int,
    reached_floors: set[int],
) -> tuple[DropWitness, ...]:
    chain = analyze_encounter_chain(data_dir, setup)
    if chain.get("missing"):
        raise ValueError("active encounter chain is incomplete")
    if chain["enc_bad"] or chain["group_bad"] or chain["enemy_bad"]:
        raise ValueError("active encounter chain contains malformed rows")

    groups = {}
    for row in chain["groups"]:
        groups.setdefault(int(row["id"]), row)
    enemies = {}
    for row in chain["enemies"]:
        enemies.setdefault(int(row["id"]), row)

    witnesses = []
    seen = set()
    for area in chain["enc"]:
        floor = int(area["floor"])
        if floor not in reached_floors:
            continue
        for group_id, group_weight in zip(
            area["groupids"], area["groupprobs"]
        ):
            if int(group_id) < 0 or int(group_weight) <= 0:
                continue
            group = groups.get(int(group_id))
            if group is None:
                continue
            gate_class = _group_gate_class(
                int(group["appear_item"]),
                int(group["notappear_item"]),
                target_item,
            )
            for enemy_id, enemy_weight in zip(
                group["enemyids"], group["enemyprobs"]
            ):
                if int(enemy_id) < 0 or int(enemy_weight) <= 0:
                    continue
                enemy = enemies.get(int(enemy_id))
                if enemy is None:
                    continue
                for item_id, item_prob in zip(
                    enemy["itemids"], enemy["itemprobs"]
                ):
                    if int(item_id) != target_item or int(item_prob) <= 0:
                        continue
                    key = (
                        floor,
                        int(group_id),
                        int(enemy_id),
                        int(item_prob),
                        gate_class,
                    )
                    if key in seen:
                        continue
                    seen.add(key)
                    witnesses.append(
                        DropWitness(
                            floor_id=floor,
                            group_gate_class=gate_class,
                            probability_class=_drop_probability_class(
                                int(item_prob)
                            ),
                        )
                    )
    return tuple(witnesses)


def _npc_reward_witnesses(
    *,
    npc_dir: Path,
    target_item: int,
    reached_floors: set[int],
) -> tuple[tuple[NpcRewardWitness, ...], int, int]:
    function_by_template = _template_function_map(npc_dir)
    files = sorted(
        (path for path in npc_dir.rglob("*") if path.is_file()),
        key=lambda path: str(path).lower(),
    )
    witnesses = []
    token_hits = 0
    missing = 0
    seen = set()

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
            if floor not in reached_floors:
                continue
            if b"borncenter" not in fields and b"borncorner" not in fields:
                continue

            for enemy in enemies:
                name, separator, arg = enemy.partition(b"|")
                template = name.strip()
                data = _assigned_data(npc_dir, arg if separator else b"")
                if data is None:
                    missing += 1
                    continue
                values = [
                    value for value in _iter_additem_values(data)
                    if _contains_item_id(value, target_item)
                ]
                if not values:
                    continue
                token_hits += len(values)
                function_set = function_by_template.get(template, "")
                normalized = function_set.strip().lower()
                key = (floor, template, normalized)
                if key in seen:
                    continue
                seen.add(key)
                witnesses.append(
                    NpcRewardWitness(
                        floor_id=floor,
                        function_set=normalized or "unknown",
                        action_run_covered=normalized in ACTION_RUN_FUNCTIONSETS,
                    )
                )

    return tuple(witnesses), token_hits, missing


def analyze(npc_dir: Path, setup: Path, data_dir: Path) -> AcquisitionAudit:
    target_item, locate_missing = _locate_key_item(npc_dir)
    reachability = load_ordered_runtime_reachability()
    reached = set(reachability.reached_floor_ids)

    drop = _drop_witnesses(
        data_dir=data_dir,
        setup=setup,
        target_item=target_item,
        reached_floors=reached,
    )
    rewards, token_hits, reward_missing = _npc_reward_witnesses(
        npc_dir=npc_dir,
        target_item=target_item,
        reached_floors=reached,
    )
    return AcquisitionAudit(
        drop_witnesses=drop,
        npc_reward_witnesses=rewards,
        npc_additem_token_hits=token_hits,
        missing_argument_files=locate_missing + reward_missing,
    )


def emit(audit: AcquisitionAudit) -> None:
    print("StoneAge shadowed-branch key-item non-shop acquisition audit — R1")
    print(
        "SCOPE|withheld key-item identity|reachable encounter drops + "
        "reachable NPC AddItem actions"
    )
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print(
        "RULE|target item ID, enemy/group IDs, NPC/template names, raw "
        "arguments, coordinates and filenames are not emitted"
    )
    print(
        "RULE|drop witness requires reachable floor + positive encounter group "
        "weight + positive group enemy weight + positive target ITEMPROB"
    )
    print(
        "RULE|NPC AddItem token presence is separated from fixed-descendant "
        "Action_RunDoEventAction function-set coverage"
    )
    for key in sorted(audit.counts):
        print(f"COUNT|{key}|{audit.counts[key]}")

    strong_drop = sum(
        witness.group_gate_class in {
            "UNGATED",
            "TARGET_ABSENCE_ALLOWED",
            "EXCLUDES_OTHER_ITEM",
        }
        for witness in audit.drop_witnesses
    )
    covered_reward = sum(
        witness.action_run_covered
        for witness in audit.npc_reward_witnesses
    )
    print(f"COUNT|strong_drop_witnesses|{strong_drop}")
    print(f"COUNT|fixed_source_covered_reward_witnesses|{covered_reward}")
    print(
        "ACQUISITION_SURFACE|"
        f"battle_drop={int(strong_drop > 0)}|"
        f"npc_reward={int(covered_reward > 0)}|"
        "item_id_withheld=1"
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
