#!/usr/bin/env python3
"""Finite same-EventEnd evidence joins for five source-pinned later logging items.

No original NPC text, dialogue, source paths or commercial server code is
persisted. Same-record co-occurrence is a later configuration observation,
not an executable transaction or a Taiwan v1.0 quest proof.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path

from tools.stoneage_npc_world_graph_probe import iter_blocks, magic_kind
from tools.stoneage_transport_usage_probe import template_map
from tools.stoneage_quest_npc_item_binding_probe import (
    TARGET_IDS, BUNDLE_SHA256, argument_bytes, semantic_hits,
    validate_candidate_report, require,
)

PREVIOUS_BLOB = "7d771b2aa4f39646879659303f4926045ae730cc"
SOURCE_VERSION = "LATER_RECOVERED25"
MAX_SOURCE_RECORDS = 100
ROLES = (
    "EXCHANGE_DEL_CANDIDATE",
    "EXCHANGE_GET_CANDIDATE",
    "EXCHANGE_ITEM_PREDICATE",
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def event_record_roles(data: bytes):
    """Preserve original EventEnd delimiter; never join adjacent records."""
    for record in data.split(b"EventEnd"):
        roles = []
        for item, role, _record_hash in semantic_hits("exchangeman", record):
            require(role in ROLES, "unexpected ExChangeMan role")
            roles.append((item, role))
        if roles:
            yield sha256(record), tuple(sorted(roles))


def aggregate(npc_dir: Path, *, previous: dict | None = None):
    paths = sorted((p for p in npc_dir.rglob("*") if p.is_file()), key=lambda p: str(p).lower())
    mapping = template_map([p for p in paths if magic_kind(p) == "template"])
    functions = {name: values[0].strip().lower() for name, values in mapping.items() if len(values) == 1}
    counts = Counter()
    ledger = Counter()
    source_record_instances = Counter()
    for path in (p for p in paths if magic_kind(p) == "create"):
        for block in iter_blocks(path):
            for key, value in block:
                if key != b"enemy":
                    continue
                counts["create_enemy_references"] += 1
                template, sep, raw_arg = value.partition(b"|")
                template = template.strip()
                if template not in mapping:
                    counts["template_unresolved"] += 1
                    continue
                if template not in functions:
                    counts["template_ambiguous"] += 1
                    continue
                arg, transport = argument_bytes(npc_dir, raw_arg if sep else b"")
                counts["transport_" + transport] += 1
                if arg is None:
                    continue
                if functions[template] != b"exchangeman":
                    continue
                for record_hash, roles in event_record_roles(arg):
                    for item, role in roles:
                        ledger[(item, role)] += 1
                    source_record_instances[(record_hash, roles)] += 1
    if previous is not None:
        expected = Counter()
        for row in previous["typed_reference_classes"]:
            require(row["functionset"] == "exchangeman", "previous functionset drift")
            expected[(row["item_id"], row["role"])] += row["occurrences"]
        require(expected == ledger, "previous source-tested typed field ledger drift")
        old = previous["counts"]
        for key in ("create_enemy_references", "template_ambiguous",
                    "transport_FILE", "transport_INLINE", "transport_MISSING_FILE"):
            require(counts[key] == old[key], "previous source count drift: " + key)
    require(sum(ledger.values()) <= MAX_SOURCE_RECORDS * 8, "scope exceeded")
    require(len(source_record_instances) <= MAX_SOURCE_RECORDS, "record cap exceeded")
    records = []
    for (record_hash, roles), instances in sorted(source_record_instances.items()):
        items = sorted({item for item, _ in roles})
        actions = sorted(set(role for _, role in roles))
        records.append({
            "anonymous_record_sha256": record_hash,
            "item_role_pairs": [{"item_id": item, "role": role} for item, role in roles],
            "placement_instances": instances,
            "distinct_item_ids": len(items),
            "distinct_roles": len(actions),
            "multi_item_same_record": len(items) > 1,
            "multi_role_same_record": len(actions) > 1,
            "execution_witness": False,
        })
    return {
        "schema": "stoneage.quest_npc_flow_link.r1",
        "source_role": SOURCE_VERSION,
        "source_bundle_sha256": BUNDLE_SHA256,
        "previous_derived_git_blob": PREVIOUS_BLOB,
        "target_ids": list(TARGET_IDS),
        "counts": {
            "create_enemy_references": counts["create_enemy_references"],
            "ambiguous_template_references": counts["template_ambiguous"],
            "missing_secondary_argument_files": counts["transport_MISSING_FILE"],
            "typed_field_occurrences": sum(ledger.values()),
            "anonymous_typed_records": len(records),
            "typed_record_placement_instances": sum(x["placement_instances"] for x in records),
            "same_record_multi_item_patterns": sum(x["multi_item_same_record"] for x in records),
            "same_record_multi_role_patterns": sum(x["multi_role_same_record"] for x in records),
        },
        "same_eventend_records": records,
        "eventend_delimiter_respected": True,
        "different_records_are_not_one_transaction": True,
        "event_predicate_presence_is_not_satisfiability": True,
        "same_record_is_not_same_npc_quest_proof": True,
        "original_taiwan_v1_binding_proven": False,
        "original_server_executed": False,
        "full_npc_or_dialogue_recovered": False,
        "runtime_code_changed": False,
        "stage_a_accepted": False,
        "stage_b_gate": "GATED",
    }


def validate_report(data: dict):
    require(data["schema"] == "stoneage.quest_npc_flow_link.r1", "schema drift")
    require(data["source_role"] == SOURCE_VERSION, "source-role promotion")
    require(data["source_bundle_sha256"] == BUNDLE_SHA256, "bundle drift")
    require(data["previous_derived_git_blob"] == PREVIOUS_BLOB, "prior source drift")
    require(data["target_ids"] == list(TARGET_IDS), "target drift")
    for name in ("original_taiwan_v1_binding_proven", "original_server_executed",
                 "full_npc_or_dialogue_recovered", "runtime_code_changed", "stage_a_accepted"):
        require(data[name] is False, name + " promotion")
    for name in ("eventend_delimiter_respected", "different_records_are_not_one_transaction",
                 "event_predicate_presence_is_not_satisfiability", "same_record_is_not_same_npc_quest_proof"):
        require(data[name] is True, name + " guard lost")
    require(data["stage_b_gate"] == "GATED", "stage B promotion")
    records = data["same_eventend_records"]
    require(len(records) <= MAX_SOURCE_RECORDS, "record cap drift")
    require(data["counts"]["anonymous_typed_records"] == len(records), "record count drift")
    n = 0
    placements = 0
    multi_item = 0
    multi_role = 0
    unique = set()
    for row in records:
        h = row["anonymous_record_sha256"]
        require(len(h) == 64 and set(h) <= set("0123456789abcdef"), "record hash")
        require(h not in unique, "duplicate source record")
        unique.add(h)
        pairs = row["item_role_pairs"]
        canonical = sorted((p["item_id"],p["role"]) for p in pairs)
        require(canonical == [(p["item_id"],p["role"]) for p in pairs], "noncanonical roles")
        require(all(x in TARGET_IDS and y in ROLES for x,y in canonical), "foreign role")
        require(type(row["placement_instances"]) is int and row["placement_instances"] > 0, "placement")
        distinct_items = len({x for x,y in canonical})
        distinct_roles = len({y for x,y in canonical})
        require(row["distinct_item_ids"] == distinct_items and row["distinct_roles"] == distinct_roles, "role cardinality")
        require(row["multi_item_same_record"] is (distinct_items>1), "cross item mutation")
        require(row["multi_role_same_record"] is (distinct_roles>1), "multi role mutation")
        require(row["execution_witness"] is False, "execution promotion")
        n += len(pairs) * row["placement_instances"]
        placements += row["placement_instances"]
        multi_item += (distinct_items>1)
        multi_role += (distinct_roles>1)
    counts = data["counts"]
    require(counts["typed_field_occurrences"] == n, "typed ledger divergence")
    require(counts["typed_record_placement_instances"] == placements, "placement ledger divergence")
    require(counts["same_record_multi_item_patterns"] == multi_item, "multi item ledger divergence")
    require(counts["same_record_multi_role_patterns"] == multi_role, "multi role ledger divergence")
    return True


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--npc-dir", type=Path, required=True)
    p.add_argument("--prior-item-report", type=Path, default=Path("research/recovered/STONEAGE-QUEST-ITEM-CI-DERIVED-R1.json"))
    p.add_argument("--previous", type=Path, default=Path("research/recovered/STONEAGE-QUEST-NPC-ITEM-CI-DERIVED-R1.json"))
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    validate_candidate_report(json.loads(args.prior_item_report.read_bytes()))
    previous_raw = args.previous.read_bytes()
    require(git_blob(previous_raw) == PREVIOUS_BLOB, "previous derived blob mismatch")
    out = aggregate(args.npc_dir, previous=json.loads(previous_raw))
    validate_report(out)
    args.output.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(out["counts"], sort_keys=True))
    print("SOURCE_ROLE|LATER_RECOVERED25|no original executable or dialogue exported")


if __name__ == "__main__":
    main()
