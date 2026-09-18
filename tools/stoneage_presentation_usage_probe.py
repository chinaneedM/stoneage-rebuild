#!/usr/bin/env python3
"""Aggregate recovered SignBoard/TownPeople/Mic presentation usage."""

import argparse
import collections
import hashlib
from pathlib import Path

from tools.stoneage_npc_world_graph_probe import iter_blocks, magic_kind

TARGETS = ("SignBoard", "TownPeople", "Mic")


def template_map(files):
    mapping = collections.defaultdict(list)
    for path in files:
        for entries in iter_blocks(path):
            f = dict(entries)
            name = f.get(b"templatename")
            if name:
                mapping[name].append(f.get(b"functionset", b""))
    return mapping


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


def atoi(value):
    try:
        return int(value.strip())
    except Exception:
        return 0


def analyze(npc_dir):
    files = sorted(
        (p for p in npc_dir.rglob("*") if p.is_file()),
        key=lambda p: str(p).lower(),
    )
    mapping = template_map([p for p in files if magic_kind(p) == "template"])
    creates = [p for p in files if magic_kind(p) == "create"]

    name_to_kind = {}
    for name, defs in mapping.items():
        if len(defs) != 1:
            continue
        try:
            kind = defs[0].decode("ascii")
        except UnicodeDecodeError:
            continue
        if kind in TARGETS:
            name_to_kind[name] = kind

    counts = collections.Counter()
    town_variants = collections.Counter()
    sign_modes = collections.Counter()
    mic_modes = collections.Counter()
    aggregate = hashlib.sha256()

    for name, arg in create_refs(creates):
        kind = name_to_kind.get(name)
        if kind is None:
            continue

        counts[(kind, "refs")] += 1
        if not arg:
            counts[(kind, "noarg")] += 1
            data = b""
        else:
            filename = assigned_file(arg)
            if filename is None:
                counts[(kind, "inline")] += 1
                data = arg
            else:
                path = npc_dir / filename
                if not path.is_file():
                    counts[(kind, "missing_files")] += 1
                    continue
                counts[(kind, "resolved_files")] += 1
                data = merge_file(path)

        aggregate.update(
            kind.encode() + b"|" + str(len(data)).encode() + b"|" +
            hashlib.sha256(data).hexdigest().encode() + b"\n"
        )

        if kind == "TownPeople":
            variants = (data.count(b",") + 1) if data else 0
            town_variants[variants] += 1

        elif kind == "SignBoard":
            if b"%manorid:" in data:
                sign_modes["manor_placeholder"] += 1
            else:
                sign_modes["plain"] += 1

        elif kind == "Mic":
            if b"FREE" in data:
                mic_modes["free"] += 1
            if b"WIND" in data:
                mic_modes["wind"] += 1
            if b"|" in data:
                mic_modes["pipe_scoped"] += 1
                parts = data.split(b"|")
                mic_modes[("pipe_token_count", len(parts))] += 1
                fmfl = atoi(parts[7]) if len(parts) >= 8 else 0
                if fmfl != 0:
                    mic_modes["family_flag_nonzero"] += 1
                else:
                    mic_modes["family_flag_zero"] += 1
            else:
                mic_modes["no_pipe_mode"] += 1

    return {
        "counts": counts,
        "town_variants": town_variants,
        "sign_modes": sign_modes,
        "mic_modes": mic_modes,
        "aggregate": aggregate.hexdigest(),
    }


def emit(result):
    print("StoneAge recovered presentation NPC usage probe — R1")
    print(
        "No NPC/template names, file paths, dialogue, coordinates, manor IDs, "
        "or family IDs are stored."
    )
    print(
        "SCHEMA|SignBoard/TownPeople/Mic refs -> presentation-shape aggregate"
    )
    print("ARG_CORPUS_AGGREGATE_SHA256|" + result["aggregate"])

    for (kind, metric), n in sorted(result["counts"].items()):
        print(f"COUNT|{kind}|{metric}|{n}")

    for variants, n in sorted(result["town_variants"].items()):
        print(
            f"TOWNPEOPLE_VARIANTS|count={variants}|blocks={n}"
        )

    for mode, n in sorted(result["sign_modes"].items()):
        print(f"SIGNBOARD_MODE|{mode}|blocks={n}")

    for mode, n in sorted(
        result["mic_modes"].items(),
        key=lambda kv: str(kv[0]),
    ):
        if isinstance(mode, tuple):
            label, value = mode
            print(f"MIC_MODE|{label}={value}|blocks={n}")
        else:
            print(f"MIC_MODE|{mode}|blocks={n}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--npc-dir", type=Path, required=True)
    emit(analyze(ap.parse_args().npc_dir))


if __name__ == "__main__":
    main()
