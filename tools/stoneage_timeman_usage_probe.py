#!/usr/bin/env python3
"""Aggregate recovered TimeMan usage without retaining dialogue or graphic payloads."""

import argparse
import collections
import hashlib
from pathlib import Path

from tools.stoneage_npc_world_graph_probe import iter_blocks, magic_kind

TIME_TABLE = (
    (b"ALLNIGHT", 301, 700),
    (b"ALLNOON", 701, 300),
    (b"AM", 501, 125),
    (b"PM", 126, 500),
    (b"FORE", 701, 125),
    (b"AFTER", 126, 300),
    (b"EVNING", 301, 500),
    (b"MORNING", 501, 700),
    (b"FREE", 0, 1024),
)


def template_names(files):
    mapping = collections.defaultdict(list)
    for path in files:
        for entries in iter_blocks(path):
            fields = dict(entries)
            name = fields.get(b"templatename")
            if name:
                mapping[name].append(fields.get(b"functionset", b""))
    return {
        name for name, defs in mapping.items()
        if len(defs) == 1 and defs[0] == b"TimeMan"
    }


def create_refs(files):
    for path in files:
        for entries in iter_blocks(path):
            for key, value in entries:
                if key != b"enemy":
                    continue
                name, sep, arg = value.partition(b"|")
                yield name.strip(), (arg if sep else b"")


def assigned_file(arg):
    for token in arg.split(b"|"):
        key, sep, value = token.partition(b":")
        if sep and key.strip().lower() == b"file":
            return value.strip().decode("utf-8", "replace")
    return None


def merge_file(path):
    out = b""
    with path.open("rb") as f:
        for raw in f:
            line = raw.rstrip(b"\r\n")
            if out and not out.endswith(b"|"):
                out += b"|"
            out += line
    return out


def field(data, wanted):
    wanted = wanted.lower()
    for token in data.split(b"|"):
        key, sep, value = token.partition(b":")
        if sep and key.strip().lower() == wanted:
            return value.strip()
    return None


def resolve_time(value):
    if value is None:
        return None
    for name, born, dead in TIME_TABLE:
        if name in value:
            return name.decode("ascii"), born, dead
    return None


def message_count(value):
    if value is None:
        return 0
    return value.count(b",") + 1


def analyze(npc_dir):
    files = sorted(
        (p for p in npc_dir.rglob("*") if p.is_file()),
        key=lambda p: str(p).lower(),
    )
    templates = [p for p in files if magic_kind(p) == "template"]
    creates = [p for p in files if magic_kind(p) == "create"]
    names = template_names(templates)

    counts = collections.Counter()
    time_resolved = collections.Counter()
    message_counts = collections.Counter()
    change_modes = collections.Counter()
    aggregate = hashlib.sha256()

    for name, arg in create_refs(creates):
        if name not in names:
            continue
        counts["refs"] += 1
        filename = assigned_file(arg)
        if filename is None:
            counts["inline"] += 1
            data = arg
        else:
            path = npc_dir / filename
            if not path.is_file():
                counts["missing_files"] += 1
                continue
            counts["resolved_files"] += 1
            data = merge_file(path)

        aggregate.update(
            str(len(data)).encode() + b"|" +
            hashlib.sha256(data).hexdigest().encode() + b"\n"
        )

        time_value = field(data, b"time")
        resolved = resolve_time(time_value)
        if resolved is None:
            counts["missing_or_unknown_time"] += 1
        else:
            label, born, dead = resolved
            time_resolved[(label, born, dead)] += 1

        change = field(data, b"change_no")
        if change is None:
            change_modes["missing_defaults_hidden"] += 1
        elif b"CLS" in change:
            change_modes["cls_hidden"] += 1
        else:
            change_modes["numeric_alternate"] += 1

        for key in (b"main_msg", b"change_msg"):
            value = field(data, key)
            label = key.decode("ascii")
            if value is None:
                counts[label + "_missing"] += 1
            else:
                counts[label + "_present"] += 1
                message_counts[(label, message_count(value))] += 1

    return {
        "counts": counts,
        "time_resolved": time_resolved,
        "message_counts": message_counts,
        "change_modes": change_modes,
        "aggregate": aggregate.hexdigest(),
    }


def emit(result):
    print("StoneAge recovered TimeMan usage probe — R1")
    print(
        "No NPC/template names, file paths, dialogue text, or graphic numbers are stored."
    )
    print(
        "SCHEMA|TimeMan refs -> merged args -> time/change/message-shape aggregate"
    )
    print("ARG_CORPUS_AGGREGATE_SHA256|" + result["aggregate"])
    for key, n in sorted(result["counts"].items()):
        print(f"COUNT|{key}|{n}")
    for (label, born, dead), n in sorted(result["time_resolved"].items()):
        print(
            f"TIME_RESOLVED|{label}|born={born}|dead={dead}|blocks={n}"
        )
    for mode, n in sorted(result["change_modes"].items()):
        print(f"CHANGE_MODE|{mode}|blocks={n}")
    for (key, count), n in sorted(result["message_counts"].items()):
        print(f"MESSAGE_VARIANTS|{key}|count={count}|blocks={n}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--npc-dir", type=Path, required=True)
    emit(analyze(ap.parse_args().npc_dir))


if __name__ == "__main__":
    main()
