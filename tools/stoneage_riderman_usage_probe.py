#!/usr/bin/env python3
"""Aggregate recovered Riderman conff usage without filenames/dialogue/item IDs."""

import argparse
import collections
import hashlib
from pathlib import Path

from tools.stoneage_npc_world_graph_probe import iter_blocks, magic_kind


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
        if len(defs) == 1 and defs[0] == b"Riderman"
    }


def create_refs(files):
    for path in files:
        for entries in iter_blocks(path):
            for key, value in entries:
                if key != b"enemy":
                    continue
                name, sep, arg = value.partition(b"|")
                yield name.strip(), (arg if sep else b"")


def arg_value(arg, wanted):
    wanted = wanted.lower()
    for token in arg.split(b"|"):
        key, sep, value = token.partition(b":")
        if sep and key.strip().lower() == wanted:
            return value.strip()
    return None


def read_config(path):
    rows = []
    current_win = None
    with path.open("rb") as f:
        for raw in f:
            line = raw.rstrip(b"\r\n")
            stripped = line.strip()
            if not stripped or stripped.startswith(b"#") or b"=" not in stripped:
                continue
            key, value = stripped.split(b"=", 1)
            key = key.strip().lower()
            value = value.strip()
            if key == b"winno":
                try:
                    current_win = int(value)
                except ValueError:
                    current_win = 0
            rows.append((current_win, key, value))
            if key == b"endwin":
                current_win = None
    return rows


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
    templates = [p for p in files if magic_kind(p) == "template"]
    creates = [p for p in files if magic_kind(p) == "create"]
    names = template_names(templates)

    counts = collections.Counter()
    key_refs = collections.Counter()
    takegold = collections.Counter()
    gotowin = collections.Counter()
    control_key = collections.Counter()
    win_refs = collections.Counter()
    config_hashes = set()
    aggregate = hashlib.sha256()

    for name, arg in create_refs(creates):
        if name not in names:
            continue
        counts["refs"] += 1
        if not arg:
            counts["noarg"] += 1
            continue
        counts["inline_arg"] += 1

        conff = arg_value(arg, b"conff")
        if not conff:
            counts["missing_conff_key"] += 1
            continue
        counts["conff_key"] += 1

        path = npc_dir / conff.decode("utf-8", "replace")
        if not path.is_file():
            counts["missing_conff_file"] += 1
            continue

        raw = path.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        config_hashes.add(digest)
        aggregate.update(
            str(len(raw)).encode() + b"|" + digest.encode() + b"\n"
        )
        counts["resolved_conff"] += 1

        rows = read_config(path)
        keys_seen = set()
        wins_seen = set()

        for winno, key, value in rows:
            keys_seen.add(key)
            if key == b"winno":
                w = atoi(value)
                wins_seen.add(w)
            elif key == b"takegold":
                takegold[(winno, atoi(value))] += 1
            elif key == b"gotowin":
                gotowin[(winno, atoi(value))] += 1
            elif key in (
                b"takeitem", b"giveitem",
                b"letter1", b"letter2", b"letter3", b"letter4",
                b"checkhaveitem", b"haveitemgotowin",
                b"checkdonthaveitem", b"donthaveitemgotowin",
            ):
                control_key[(winno, key.decode("ascii"))] += 1

        for key in keys_seen:
            key_refs[key.decode("ascii", "replace")] += 1
        for winno in wins_seen:
            win_refs[winno] += 1

    counts["distinct_conff_contents"] = len(config_hashes)

    return {
        "counts": counts,
        "key_refs": key_refs,
        "takegold": takegold,
        "gotowin": gotowin,
        "control_key": control_key,
        "win_refs": win_refs,
        "aggregate": aggregate.hexdigest(),
    }


def emit(result):
    print("StoneAge recovered Riderman conff usage probe — R1")
    print(
        "No NPC/template names, conff filenames, dialogue, item IDs, "
        "or original configuration rows are stored."
    )
    print(
        "SCHEMA|Riderman ref -> inline conff pointer -> "
        "window/control/tuition aggregate"
    )
    print("CONFF_CORPUS_AGGREGATE_SHA256|" + result["aggregate"])
    for key, n in sorted(result["counts"].items()):
        print(f"COUNT|{key}|{n}")
    for winno, n in sorted(result["win_refs"].items()):
        print(f"WINNO_PRESENT|winno={winno}|refs={n}")
    for key, n in sorted(result["key_refs"].items()):
        print(f"KEY_REF|{key}|refs={n}")
    for (winno, value), n in sorted(result["takegold"].items()):
        print(f"TAKEGOLD|winno={winno}|value={value}|refs={n}")
    for (winno, target), n in sorted(result["gotowin"].items()):
        print(f"GOTOWIN|from_winno={winno}|target={target}|lines={n}")
    for (winno, key), n in sorted(result["control_key"].items()):
        print(f"CONTROL_KEY|winno={winno}|key={key}|lines={n}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--npc-dir", type=Path, required=True)
    emit(analyze(ap.parse_args().npc_dir))


if __name__ == "__main__":
    main()
