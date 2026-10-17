#!/usr/bin/env python3
"""Bounded later-recovered NPC references for five logging-item candidates.

Source bytes are read only in CI and never emitted. This reports template/field
grammar, not an original Taiwan v1 quest binding or an executable server trace.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re

from tools.stoneage_npc_world_graph_probe import iter_blocks, magic_kind
from tools.stoneage_transport_usage_probe import template_map, assigned_file, merge_file
from tools.stoneage_quest_item_identity_probe import validate_derived

TARGET_IDS = (2465, 2478, 2481, 2484, 20197)
BUNDLE_SHA256 = "d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5"
MAX_WITNESSES = 250
MAX_ARGUMENT_BYTES = 2_000_000
ALLOWED_ROLES = {
    "EXCHANGE_GET_CANDIDATE", "EXCHANGE_DEL_CANDIDATE",
    "EXCHANGE_ITEM_PREDICATE", "ACTION_ADDITEM_CANDIDATE",
    "ITEMSHOP_CATALOG_ONLY", "STRUCTURED_FIELD_UNQUALIFIED",
}
ACTION_RUN_FUNCTIONSETS = {"warpman", "makepair", "npcenemy", "freepetskillshop"}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def exact_items(value):
    """Parse only exact item-id[,item-id*quantity] grammar, never substrings."""
    found = set()
    for token in value.split(b","):
        token = token.strip()
        if not re.fullmatch(rb"[+]?[0-9]+(?:\*[1-9][0-9]*)?", token):
            continue
        number = int(token.split(b"*", 1)[0])
        if number in TARGET_IDS:
            found.add(number)
    return found


def event_items(value):
    """Only ITEM equality/inequality atoms; FREE, LV and text are excluded."""
    out = set()
    for clause in value.split(b","):
        for atom in clause.split(b"&"):
            match = re.fullmatch(rb"\s*ITEM\s*(?:=|!=)\s*([0-9]+)(?:\*[1-9][0-9]*)?\s*", atom, re.I)
            if match:
                item = int(match.group(1))
                if item in TARGET_IDS:
                    out.add(item)
    return out


def fields(record):
    for line in record.replace(b"\r", b"\n").split(b"\n"):
        for token in line.split(b"|"):
            if b":" in token:
                key, value = token.split(b":", 1)
                key = key.strip().lower()
                if re.fullmatch(rb"[a-z][a-z0-9_]*", key):
                    yield key, value.strip()


def semantic_hits(functionset, argument):
    """Return (item, role, record hash) with conservative syntax-specific roles."""
    func = functionset.strip().lower()
    records = argument.split(b"EventEnd") if func == "exchangeman" else [argument]
    for record in records:
        for key, value in fields(record):
            matched = set()
            role = "STRUCTURED_FIELD_UNQUALIFIED"
            if func == "exchangeman" and key == b"getitem":
                matched, role = exact_items(value), "EXCHANGE_GET_CANDIDATE"
            elif func == "exchangeman" and key == b"delitem":
                matched, role = exact_items(value), "EXCHANGE_DEL_CANDIDATE"
            elif func == "exchangeman" and key == b"event":
                matched, role = event_items(value), "EXCHANGE_ITEM_PREDICATE"
            elif key == b"additem" and func in ACTION_RUN_FUNCTIONSETS:
                matched, role = exact_items(value), "ACTION_ADDITEM_CANDIDATE"
            elif func == "itemshop" and key in (b"item", b"items", b"itemid", b"itemlist"):
                # A catalog item reference is not task delivery.
                matched, role = exact_items(value), "ITEMSHOP_CATALOG_ONLY"
            elif key in (b"getitem", b"delitem", b"additem"):
                matched = exact_items(value)
            elif key == b"event":
                matched = event_items(value)
            for item in sorted(matched):
                yield item, role, digest(record)


def argument_bytes(npc_dir, arg):
    filename = assigned_file(arg)
    if filename is None:
        return arg, "INLINE"
    rel = Path(filename.replace("\\", "/"))
    if rel.is_absolute() or ".." in rel.parts:
        return None, "UNSAFE_PATH"
    path = (npc_dir / rel).resolve()
    if not path.is_relative_to(npc_dir.resolve()) or not path.is_file():
        return None, "MISSING_FILE"
    if path.stat().st_size > MAX_ARGUMENT_BYTES:
        return None, "OVERSIZE_FILE"
    return merge_file(path), "FILE"


def validate_candidate_report(item_report):
    validate_derived(item_report)
    left = item_report["tables"]["itemset.txt"]["candidates"]
    right = item_report["tables"]["itemset0710.txt"]["candidates"]
    left_ids = {row["numeric_fields"]["id"] for row in left}
    right_ids = {row["numeric_fields"]["id"] for row in right}
    require(left_ids == right_ids == set(TARGET_IDS), "five-candidate scope drift")
    require(item_report["tables"]["itemset.txt"]["selected_by_actual_setup"] is True, "unselected active table")


def analyze(npc_dir, item_report):
    validate_candidate_report(item_report)
    paths = sorted((p for p in npc_dir.rglob("*") if p.is_file()), key=lambda p: str(p).lower())
    templates = template_map([p for p in paths if magic_kind(p) == "template"])
    functions = {name: vals[0] for name, vals in templates.items() if len(vals) == 1}
    counts = Counter()
    hits = Counter()
    source_keys = defaultdict(set)
    records = set()
    for path in (p for p in paths if magic_kind(p) == "create"):
        for block in iter_blocks(path):
            for key, value in block:
                if key != b"enemy":
                    continue
                counts["create_enemy_references"] += 1
                name, sep, arg = value.partition(b"|")
                name = name.strip()
                if name not in templates:
                    counts["template_unresolved"] += 1
                    continue
                if name not in functions:
                    counts["template_ambiguous"] += 1
                    continue
                func = functions[name].decode("ascii", "replace").strip().lower()
                data, transport = argument_bytes(npc_dir, arg if sep else b"")
                counts["transport_" + transport] += 1
                if data is None:
                    continue
                if not data:
                    continue
                for item, role, record_hash in semantic_hits(func, data):
                    counts["typed_item_field_occurrences"] += 1
                    hits[(item, role, func)] += 1
                    witness = (item, role, func, record_hash)
                    records.add(witness)
                    source_keys[(item, role, func)].add(digest(name + b"|" + record_hash.encode()))
    require(set(ALLOWED_ROLES) >= {role for _, role, _ in hits}, "unclassified role")
    output = []
    for (item, role, func), number in sorted(hits.items()):
        output.append({
            "item_id": item,
            "role": role,
            "functionset": func[:60],
            "occurrences": number,
            "anonymous_record_count": len({h for i,r,f,h in records if (i,r,f)==(item,role,func)}),
            "anonymous_template_record_count": len(source_keys[(item,role,func)]),
            "source_class": "LATER_RECOVERED25_NPC_PARAMETER",
            "original_quest_binding_proven": False,
            "runtime_executed": False,
        })
    require(len(output) <= MAX_WITNESSES, "bounded typed result cap exceeded")
    return {
        "schema": "stoneage.quest_npc_item_binding.r1",
        "source_role": "LATER_RECOVERED25",
        "bundle_sha256": BUNDLE_SHA256,
        "target_ids": list(TARGET_IDS),
        "counts": dict(sorted(counts.items())),
        "typed_reference_classes": output,
        "coverage_limits": {
            "ambiguous_templates": counts["template_ambiguous"],
            "missing_argument_files": counts["transport_MISSING_FILE"],
            "unsafe_argument_paths": counts["transport_UNSAFE_PATH"],
            "oversize_argument_files": counts["transport_OVERSIZE_FILE"],
            "itemshop_not_quest_reward": True,
            "numeric_only_fields_excluded": True,
            "functions_not_automatically_equivalent": True,
        },
        "original_taiwan_1_0_npc_binding_proven": False,
        "actual_reward_or_removal_execution_proven": False,
        "complete_original_dialogue_recovered": False,
        "runtime_code_changed": False,
        "stage_a_accepted": False,
        "stage_b_gate": "GATED",
    }


def validate_output(result):
    require(result["schema"] == "stoneage.quest_npc_item_binding.r1", "schema drift")
    require(result["bundle_sha256"] == BUNDLE_SHA256, "bundle drift")
    require(result["target_ids"] == list(TARGET_IDS), "target mutation")
    for flag in ("original_taiwan_1_0_npc_binding_proven", "actual_reward_or_removal_execution_proven",
                 "complete_original_dialogue_recovered", "runtime_code_changed", "stage_a_accepted"):
        require(result[flag] is False, "source promotion: " + flag)
    require(result["stage_b_gate"] == "GATED", "stage B promotion")
    require(len(result["typed_reference_classes"]) <= MAX_WITNESSES, "bound drift")
    for row in result["typed_reference_classes"]:
        require(row["item_id"] in TARGET_IDS and row["role"] in ALLOWED_ROLES, "unqualified reference")
        require(row["source_class"] == "LATER_RECOVERED25_NPC_PARAMETER", "source role drift")
        require(row["original_quest_binding_proven"] is False and row["runtime_executed"] is False, "reference promotion")
        require(type(row["occurrences"]) is int and row["occurrences"] > 0, "count drift")
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--npc-dir", type=Path, required=True)
    parser.add_argument("--item-report", type=Path, default=Path("research/recovered/STONEAGE-QUEST-ITEM-CI-DERIVED-R1.json"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    item_report = json.loads(args.item_report.read_text(encoding="utf-8"))
    result = analyze(args.npc_dir, item_report)
    validate_output(result)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"qualified_classes": len(result["typed_reference_classes"]),
                      "typed_occurrences": result["counts"].get("typed_item_field_occurrences", 0),
                      "unresolved": result["counts"].get("template_unresolved", 0),
                      "ambiguous": result["counts"].get("template_ambiguous", 0),
                      "stage_b": "GATED"}))


if __name__ == "__main__":
    main()
