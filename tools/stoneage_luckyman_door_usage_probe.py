#!/usr/bin/env python3
"""Aggregate recovered LuckyMan/Door active shapes without payload text, IDs or names."""

import argparse
import collections
import hashlib
from pathlib import Path

TEMPLATE_MAGIC = b"NPCTEMPLATE"
CREATE_MAGIC = b"NPCCREATE"
TARGETS = (b"LuckyMan", b"Door")


def source_candidate(path):
    n = path.name.lower()
    return not (
        path.name.endswith("~") or path.name.startswith("#") or n.endswith(".bak")
    )


def magic_kind(path):
    if not source_candidate(path):
        return None
    try:
        with path.open("rb") as f:
            first = f.readline().rstrip(b"\r\n")
    except OSError:
        return None
    if first == TEMPLATE_MAGIC:
        return "template"
    if first == CREATE_MAGIC:
        return "create"
    return None


def iter_blocks(path):
    block = None
    with path.open("rb") as f:
        next(f, b"")
        for raw in f:
            line = raw.rstrip(b"\r\n")
            if not line or line.startswith(b"#"):
                continue
            if line.startswith(b"{"):
                block = []
                continue
            if line.startswith(b"}"):
                if block is not None:
                    yield block
                block = None
                continue
            if block is None or b"=" not in line:
                continue
            key, value = line.split(b"=", 1)
            block.append((key.strip().lower(), value.strip()))


def stable_target_names(files):
    mapping = collections.defaultdict(list)
    for path in files:
        for entries in iter_blocks(path):
            d = dict(entries)
            name = d.get(b"templatename")
            if name:
                mapping[name].append(d.get(b"functionset", b""))

    stable = {}
    ambiguous = set()
    duplicate_stable = collections.Counter()
    for name, defs in mapping.items():
        target_defs = [d for d in defs if d in TARGETS]
        if not target_defs:
            continue
        if all(d == target_defs[0] for d in defs):
            stable[name] = target_defs[0]
            if len(defs) > 1:
                duplicate_stable[target_defs[0]] += 1
        else:
            ambiguous.add(name)
    return stable, ambiguous, duplicate_stable


def refs(files):
    for path in files:
        for entries in iter_blocks(path):
            for key, value in entries:
                if key != b"enemy":
                    continue
                name, sep, arg = value.partition(b"|")
                yield name.strip(), arg if sep else b""


def assigned_file(arg):
    for token in arg.split(b"|"):
        left, sep, right = token.partition(b":")
        if sep and left.strip().lower() == b"file":
            return right.decode("utf-8", "replace").strip()
    return None


def merge_file(path):
    out = b""
    with path.open("rb") as f:
        for raw in f:
            line = raw.rstrip(b"\r\n")
            if not line or line.startswith(b"#"):
                continue
            if out and not out.endswith(b"|"):
                out += b"|"
            out += line
    return out


def named_fields(data):
    out = {}
    for token in data.split(b"|"):
        key, sep, value = token.partition(b":")
        if sep:
            out[key.strip().lower()] = value.strip()
    return out


def atoi(value):
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


def analyze(npc_dir):
    files = sorted(
        (p for p in npc_dir.rglob("*") if p.is_file()),
        key=lambda p: str(p).lower(),
    )
    templates = [p for p in files if magic_kind(p) == "template"]
    creates = [p for p in files if magic_kind(p) == "create"]
    stable, ambiguous, duplicate_stable = stable_target_names(templates)

    counts = collections.Counter()
    values = collections.Counter()
    shapes = collections.Counter()
    aggregate = hashlib.sha256()

    for target, n in duplicate_stable.items():
        counts[(target.decode("ascii"), "duplicate_stable_template_names")] = n

    for name, arg in refs(creates):
        if name in ambiguous:
            counts[("shared", "ambiguous_mixed_template_refs")] += 1
            continue
        target = stable.get(name)
        if target not in TARGETS:
            continue

        label = target.decode("ascii")
        counts[(label, "refs")] += 1
        filename = assigned_file(arg)
        if filename is not None:
            path = npc_dir / filename
            if not path.is_file():
                counts[(label, "missing_files")] += 1
                continue
            data = merge_file(path)
            counts[(label, "resolved_files")] += 1
        else:
            data = arg
            counts[(label, "inline")] += 1

        aggregate.update(
            label.encode()
            + b"|"
            + str(len(data)).encode()
            + b"|"
            + hashlib.sha256(data).hexdigest().encode()
            + b"\n"
        )

        if target == b"LuckyMan":
            fields = named_fields(data)
            for key in (b"stone", b"main_msg", b"nomoney"):
                if key in fields:
                    counts[(label, "key_" + key.decode("ascii"))] += 1

            stone = fields.get(b"stone")
            if stone is not None:
                if b"LV" in stone.upper():
                    parts = stone.split(b"*", 1)
                    multiplier = atoi(parts[1]) if len(parts) == 2 else 0
                    counts[(label, "stone_level_scaled")] += 1
                    values[(label, "stone_multiplier", multiplier)] += 1
                else:
                    counts[(label, "stone_constant")] += 1
                    values[(label, "stone_constant", atoi(stone))] += 1

            luck_keys = []
            for key, value in fields.items():
                if not key.startswith(b"luck"):
                    continue
                suffix = key[4:]
                if suffix and suffix.lstrip(b"+-").isdigit():
                    luck = atoi(suffix)
                    luck_keys.append(luck)
                    variants = 0 if value == b"" else len(value.split(b","))
                    shapes[(label, "luck_variants", variants)] += 1
                    values[(label, "luck_key", luck)] += 1
            shapes[(label, "luck_key_count", len(luck_keys))] += 1

        elif target == b"Door":
            tokens = data.split(b"|") if data else []
            shapes[(label, "token_count", len(tokens))] += 1
            for pos, metric in ((4, "switch_count"), (5, "close_seconds"),
                                (6, "soon_flag"), (7, "pass_flag")):
                if len(tokens) >= pos:
                    values[(label, metric, atoi(tokens[pos - 1]))] += 1

            if len(tokens) >= 1:
                open_graphic = atoi(tokens[0])
                if 11900 <= open_graphic <= 11915:
                    group = "key_group_a"
                elif 11916 <= open_graphic <= 11931:
                    group = "key_group_b"
                else:
                    group = "no_graphic_key_group"
                counts[(label, group)] += 1

            if len(tokens) < 8 or tokens[7] == b"":
                mode = "field8_absent"
            elif tokens[7].lower().startswith(b"title"):
                mode = "field8_title"
            elif tokens[7][:1].isdigit():
                mode = "field8_numeric_roomadmin"
            else:
                mode = "field8_other"
            counts[(label, mode)] += 1

            for pos in (9, 10, 11, 12, 13):
                if len(tokens) >= pos and tokens[pos - 1] != b"":
                    counts[(label, f"field{pos}_nonempty")] += 1

    return {
        "counts": counts,
        "values": values,
        "shapes": shapes,
        "aggregate": aggregate.hexdigest(),
    }


def emit(result):
    print("StoneAge recovered LuckyMan / Door usage probe — R1")
    print(
        "No NPC/template names, file paths, dialogue, door names/passwords, "
        "coordinates, item IDs or original argument rows are stored."
    )
    print("ARG_CORPUS_AGGREGATE_SHA256|" + result["aggregate"])
    for (target, metric), n in sorted(result["counts"].items()):
        print(f"COUNT|{target}|{metric}|{n}")
    for (target, metric, value), n in sorted(result["values"].items()):
        print(f"VALUE|{target}|{metric}|value={value}|blocks={n}")
    for (target, metric, value), n in sorted(result["shapes"].items()):
        print(f"SHAPE|{target}|{metric}|value={value}|blocks={n}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--npc-dir", type=Path, required=True)
    args = parser.parse_args()
    emit(analyze(args.npc_dir))


if __name__ == "__main__":
    main()
