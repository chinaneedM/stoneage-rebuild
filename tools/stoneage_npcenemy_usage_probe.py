#!/usr/bin/env python3
"""Aggregate recovered StoneAge NPCEnemy secondary-argument usage without payload values."""

import argparse
import collections
import hashlib
from pathlib import Path

from tools.stoneage_npc_world_graph_probe import iter_blocks, magic_kind

CORE_KEYS = (
    b"sktype", b"enemyno", b"steal", b"item", b"gym", b"dieact",
    b"warpfl", b"warpx", b"warpy", b"entype", b"onebattle", b"time",
    b"NEWTIME", b"Time_Msg", b"deniedmsg", b"noitem", b"B_evend",
    b"B_evnow", b"alreadymsg", b"endmsg", b"herobattlefield",
    b"startmsg", b"REPLACEMENT",
)
FREE_FAMILIES = (b"TRANS", b"ENDEV", b"NOWEV", b"ITEM", b"PET", b"LV")


def parse_template_map(paths):
    mapping = collections.defaultdict(list)
    for path in paths:
        for entries in iter_blocks(path):
            fields = {}
            for key, value in entries:
                fields[key] = value
            name = fields.get(b"templatename", b"")
            if name:
                mapping[name].append(fields.get(b"functionset", b""))
    return mapping


def iter_create_refs(paths):
    for path in paths:
        for entries in iter_blocks(path):
            for key, value in entries:
                if key != b"enemy":
                    continue
                name, sep, arg = value.partition(b"|")
                yield name.strip(), (arg if sep else b"")


def assigned_file(arg):
    for token in arg.split(b"|"):
        if b"file" in token:
            parts = token.split(b":")
            if len(parts) >= 2:
                return parts[1].decode("utf-8", "replace")
    return None


def merge_arg_file(path):
    merged = b""
    with path.open("rb") as f:
        for raw in f:
            line = raw.rstrip(b"\r\n")
            if merged and not merged.endswith(b"|"):
                merged += b"|"
            merged += line
    return merged


def field_value(data, key):
    for token in data.split(b"|"):
        if key in token:
            parts = token.split(b":")
            if len(parts) >= 2:
                return parts[1]
    return None


def c_atoi(value):
    s = value.lstrip()
    sign = 1
    if s[:1] in (b"+", b"-"):
        sign = -1 if s[:1] == b"-" else 1
        s = s[1:]
    n = 0
    found = False
    for ch in s:
        if not 48 <= ch <= 57:
            break
        found = True
        n = n * 10 + ch - 48
    return sign * n if found else 0


def list_values(value, delim=b","):
    if value is None or value == b"":
        return []
    return [part.strip() for part in value.split(delim)]


def normalized_mode(value, allowed, default=0):
    if value is None:
        return default
    n = c_atoi(value)
    return n if n in allowed else default


def classify_free_family(term):
    for family in FREE_FAMILIES:
        if family in term:
            return family.decode("ascii")
    return "OTHER"


def analyze(npc_dir):
    files = sorted((p for p in npc_dir.rglob("*") if p.is_file()), key=lambda p: str(p).lower())
    templates = [p for p in files if magic_kind(p) == "template"]
    creates = [p for p in files if magic_kind(p) == "create"]
    mapping = parse_template_map(templates)
    enemy_names = {name for name, defs in mapping.items() if len(defs) == 1 and defs[0] == b"NPCEnemy"}

    counts = collections.Counter()
    key_blocks = collections.Counter()
    mode_counts = collections.Counter()
    length_hist = collections.Counter()
    free_family_terms = collections.Counter()
    free_operator_terms = collections.Counter()
    aggregate = hashlib.sha256()

    for zero_key in (
        "create_refs_npcenemy", "argument_files_resolved", "argument_files_missing",
        "inline_arguments", "newnpcenemy_blocks", "over_segments_nonempty",
        "over_segments_newevent", "over_segments_with_free", "over_segments_with_warp",
        "over_segments_checkparty", "item_list_duplicate_value_blocks",
        "steal_without_item_blocks", "old_dieact_warp_missing_coordinate_blocks",
        "askbattle_prompt_blocks",
    ):
        counts[zero_key] = 0

    for name, arg in iter_create_refs(creates):
        if name not in enemy_names:
            continue
        counts["create_refs_npcenemy"] += 1
        fn = assigned_file(arg)
        if fn is not None:
            path = npc_dir / fn
            if not path.is_file():
                counts["argument_files_missing"] += 1
                continue
            data = merge_arg_file(path)
            counts["argument_files_resolved"] += 1
        else:
            data = arg
            counts["inline_arguments"] += 1

        aggregate.update(str(len(data)).encode() + b"|" + hashlib.sha256(data).hexdigest().encode() + b"\n")

        for key in CORE_KEYS:
            if field_value(data, key) is not None:
                key_blocks[key.decode("ascii")] += 1

        for i in range(1, 7):
            if field_value(data, f"askbattlemsg{i}".encode()) is not None:
                key_blocks[f"askbattlemsg{i}"] += 1
                if i == 1:
                    counts["askbattle_prompt_blocks"] += 1

        enemy_values = list_values(field_value(data, b"enemyno"))
        length_hist[("enemyno", len(enemy_values))] += 1

        item_values = list_values(field_value(data, b"item"))
        if item_values:
            length_hist[("item", len(item_values))] += 1
            if len(set(item_values)) != len(item_values):
                counts["item_list_duplicate_value_blocks"] += 1

        noitem_values = list_values(field_value(data, b"noitem"))
        if noitem_values:
            length_hist[("noitem", len(noitem_values))] += 1

        for key in (b"B_evend", b"B_evnow"):
            values = list_values(field_value(data, key))
            if values:
                length_hist[(key.decode("ascii"), len(values))] += 1

        entype = normalized_mode(field_value(data, b"entype"), {1, 2}, 0)
        mode_counts[{0: "encounter_walk_only", 1: "encounter_talk_only", 2: "encounter_walk_or_talk"}[entype]] += 1

        dieact = normalized_mode(field_value(data, b"dieact"), {1}, 0)
        mode_counts["dieact_warp" if dieact == 1 else "dieact_hide_and_revive"] += 1

        onebattle = normalized_mode(field_value(data, b"onebattle"), {1}, 0)
        mode_counts["onebattle_exclusive" if onebattle == 1 else "onebattle_not_exclusive"] += 1

        gym = c_atoi(field_value(data, b"gym") or b"-1")
        mode_counts["battle_gym_mode" if gym > 0 else "battle_normal_mode"] += 1

        steal = field_value(data, b"steal")
        if steal is not None:
            sval = c_atoi(steal)
            if sval == 0:
                mode_counts["steal_before_battle"] += 1
            elif sval == 1:
                mode_counts["steal_after_win"] += 1
            else:
                mode_counts["steal_other_value"] += 1
            if not item_values:
                counts["steal_without_item_blocks"] += 1

        if b"NEWNPCENEMY" in data:
            counts["newnpcenemy_blocks"] += 1
            segments = data.split(b"OVER")
            for segment in segments:
                if not segment.strip(b"| \t\r\n"):
                    continue
                counts["over_segments_nonempty"] += 1
                if b"NEWEVENT" not in segment:
                    continue
                counts["over_segments_newevent"] += 1
                free = field_value(segment, b"FREE")
                if free is not None:
                    counts["over_segments_with_free"] += 1
                    for branch in free.split(b","):
                        for term in branch.split(b"&"):
                            term = term.strip()
                            if not term:
                                continue
                            family = classify_free_family(term)
                            free_family_terms[family] += 1
                            if b"!=" in term:
                                free_operator_terms["!="] += 1
                            elif b"<" in term:
                                free_operator_terms["<"] += 1
                            elif b">" in term:
                                free_operator_terms[">"] += 1
                            elif b"=" in term:
                                free_operator_terms["="] += 1
                            else:
                                free_operator_terms["none"] += 1
                if field_value(segment, b"WARP") is not None:
                    counts["over_segments_with_warp"] += 1
                if field_value(segment, b"CHECKPARTY") is not None:
                    counts["over_segments_checkparty"] += 1
        elif dieact == 1:
            missing = sum(field_value(data, k) is None for k in (b"warpfl", b"warpx", b"warpy"))
            if missing:
                counts["old_dieact_warp_missing_coordinate_blocks"] += 1

    return {
        "counts": counts,
        "key_blocks": key_blocks,
        "mode_counts": mode_counts,
        "length_hist": length_hist,
        "free_family_terms": free_family_terms,
        "free_operator_terms": free_operator_terms,
        "aggregate": aggregate.hexdigest(),
    }


def emit(result):
    print("StoneAge recovered NPCEnemy secondary-argument usage probe — R1")
    print("No NPC/template names, file paths, dialogue, concrete IDs, coordinates, or original argument rows are stored.")
    print("SCHEMA|NPCEnemy refs -> secondary arg merge -> key/mode/list-shape/new-warp aggregate")
    print(f"ARG_CORPUS_AGGREGATE_SHA256|{result['aggregate']}")
    for key in sorted(result["counts"]):
        print(f"COUNT|{key}|{result['counts'][key]}")
    for key, n in sorted(result["key_blocks"].items()):
        print(f"KEY_BLOCK|{key}|{n}")
    for key, n in sorted(result["mode_counts"].items()):
        print(f"MODE_BLOCK|{key}|{n}")
    for (key, length), n in sorted(result["length_hist"].items()):
        print(f"LIST_LENGTH|{key}|length={length}|blocks={n}")
    for key, n in sorted(result["free_family_terms"].items()):
        print(f"FREE_FAMILY_TERM|{key}|{n}")
    for key, n in sorted(result["free_operator_terms"].items()):
        print(f"FREE_OPERATOR_TERM|{key}|{n}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--npc-dir", type=Path, required=True)
    args = ap.parse_args()
    emit(analyze(args.npc_dir))


if __name__ == "__main__":
    main()
