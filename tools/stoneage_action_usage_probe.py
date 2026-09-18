#!/usr/bin/env python3
"""Aggregate recovered Action NPC argument usage without message payloads."""

import argparse
import collections
import hashlib
from pathlib import Path

from tools.stoneage_npc_world_graph_probe import iter_blocks, magic_kind

KEYS = (
    b"msgcol", b"normal", b"attack", b"damage", b"down", b"sit",
    b"hand", b"pleasure", b"angry", b"sad", b"guard", b"nod", b"throw",
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
        if len(defs) == 1 and defs[0] == b"Action"
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


def fields(data):
    out = {}
    for token in data.split(b"|"):
        key, sep, value = token.partition(b":")
        if sep:
            out[key.strip().lower()] = value.strip()
    return out


def atoi(value):
    if value is None:
        return None
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
    names = template_names([p for p in files if magic_kind(p) == "template"])
    creates = [p for p in files if magic_kind(p) == "create"]

    counts = collections.Counter()
    key_blocks = collections.Counter()
    msgcol_values = collections.Counter()
    message_lengths = collections.Counter()
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

        f = fields(data)
        for key in KEYS:
            if key in f:
                label = key.decode("ascii")
                key_blocks[label] += 1
                if key == b"msgcol":
                    msgcol_values[atoi(f[key])] += 1
                else:
                    # Only retain byte length; never retain message text.
                    message_lengths[(label, len(f[key]))] += 1

    return {
        "counts": counts,
        "key_blocks": key_blocks,
        "msgcol_values": msgcol_values,
        "message_lengths": message_lengths,
        "aggregate": aggregate.hexdigest(),
    }


def emit(result):
    print("StoneAge recovered Action NPC usage probe — R1")
    print(
        "No NPC/template names, file paths, message text, or original "
        "argument rows are stored."
    )
    print(
        "SCHEMA|Action refs -> merged args -> response-key/msgcol/length aggregate"
    )
    print("ARG_CORPUS_AGGREGATE_SHA256|" + result["aggregate"])
    for key, n in sorted(result["counts"].items()):
        print(f"COUNT|{key}|{n}")
    for key, n in sorted(result["key_blocks"].items()):
        print(f"KEY_BLOCK|{key}|{n}")
    for value, n in sorted(result["msgcol_values"].items()):
        print(f"MSGCOL_VALUE|value={value}|blocks={n}")
    for (key, length), n in sorted(result["message_lengths"].items()):
        print(f"MESSAGE_LENGTH|{key}|bytes={length}|blocks={n}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--npc-dir", type=Path, required=True)
    emit(analyze(ap.parse_args().npc_dir))


if __name__ == "__main__":
    main()
