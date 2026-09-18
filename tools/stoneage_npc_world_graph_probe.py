#!/usr/bin/env python3
"""Probe StoneAge NPC template/create world-content graph without retaining payload text."""

import argparse
import collections
import hashlib
import struct
from pathlib import Path

TEMPLATE_MAGIC = b"NPCTEMPLATE"
CREATE_MAGIC = b"NPCCREATE"
DIRECT_FUNC_KEYS = {
    b"initfunc",
    b"walkprefunc",
    b"walkpostfunc",
    b"preoverfunc",
    b"postoverfunc",
    b"watchfunc",
    b"loopfunc",
    b"talkedfunc",
    b"dyingfunc",
    b"preattackedfunc",
    b"postattackedfunc",
    b"offfunc",
    b"lookedfunc",
    b"itemputfunc",
    b"specialtalkedfunc",
    b"windowtalkedfunc",
}


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def setup_values(path):
    out = {}
    if not path or not path.exists():
        return out
    for raw in path.read_bytes().splitlines():
        line = raw.split(b"#", 1)[0].strip()
        if b"=" not in line:
            continue
        k, v = line.split(b"=", 1)
        key = k.decode("ascii", "ignore").strip().lower()
        if key in {"npcdir", "filesearchnum", "npctemplatenum", "npccreatenum"}:
            out[key] = v.decode("utf-8", "replace").strip()
    return out


def source_candidate(path):
    name = path.name
    return not (name.endswith("~") or name.startswith("#") or name.lower().endswith(".bak"))


def magic_kind(path):
    if not source_candidate(path):
        return None
    try:
        first = path.open("rb").readline().rstrip(b"\r\n")
    except OSError:
        return None
    if first == TEMPLATE_MAGIC:
        return "template"
    if first == CREATE_MAGIC:
        return "create"
    return None


def iter_blocks(path):
    """Yield simple key/value blocks after the first magic line."""
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
            k, v = line.split(b"=", 1)
            block.append((k.strip().lower(), v.strip()))


def parse_templates(paths):
    blocks = []
    for path in paths:
        for entries in iter_blocks(path):
            fields = {}
            direct = set()
            item_rows = 0
            for k, v in entries:
                if k == b"itm":
                    item_rows += 1
                    continue
                fields[k] = v
                if k in DIRECT_FUNC_KEYS and v:
                    direct.add(k)
            name = fields.get(b"templatename", b"")
            blocks.append(
                {
                    "name": name,
                    "functionset": fields.get(b"functionset", b""),
                    "direct_funcs": direct,
                    "item_rows": item_rows,
                }
            )
    return blocks


def parse_create_blocks(paths):
    blocks = []
    for path in paths:
        for entries in iter_blocks(path):
            fields = {}
            enemies = []
            for k, v in entries:
                if k == b"enemy":
                    name, sep, arg = v.partition(b"|")
                    enemies.append((name.strip(), bool(sep and arg)))
                else:
                    fields[k] = v

            def as_int(key, default=0):
                try:
                    return int(fields.get(key, str(default).encode()).strip(), 10)
                except ValueError:
                    return default

            blocks.append(
                {
                    "floorid": as_int(b"floorid"),
                    "born_defined": b"borncenter" in fields or b"borncorner" in fields,
                    "move_defined": b"movecenter" in fields or b"movecorner" in fields,
                    "born_corner": b"borncorner" in fields,
                    "move_corner": b"movecorner" in fields,
                    "time": as_int(b"time"),
                    "createnum": as_int(b"createnum"),
                    "boundary": as_int(b"boundary"),
                    "ignoreinvincible": as_int(b"ignoreinvincible"),
                    "enemies": enemies,
                }
            )
    return blocks


def collect_server_map_ids(root):
    ids = set()
    files = 0
    if not root or not root.exists():
        return ids, files
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        files += 1
        try:
            head = p.open("rb").read(8)
        except OSError:
            continue
        if len(head) >= 8 and head[:6] == b"LS2MAP":
            ids.add(struct.unpack(">H", head[6:8])[0])
    return ids, files


def safe_ascii(value):
    if not value:
        return "<none>"
    text = value.decode("ascii", "replace")
    return "".join(c if 32 <= ord(c) < 127 else "?" for c in text)


def analyze(npc_dir, setup=None, map_dir=None):
    all_files = sorted((p for p in npc_dir.rglob("*") if p.is_file()), key=lambda p: str(p).lower())
    templates = []
    creates = []
    aggregate = hashlib.sha256()
    ext = collections.Counter()
    for p in all_files:
        kind = magic_kind(p)
        if not kind:
            continue
        rel = str(p.relative_to(npc_dir)).replace("\\", "/")
        aggregate.update(f"{kind}|{rel}|{p.stat().st_size}|{sha256(p)}\n".encode())
        ext[(kind, p.suffix.lower() or "<none>")] += 1
        (templates if kind == "template" else creates).append(p)

    tblocks = parse_templates(templates)
    cblocks = parse_create_blocks(creates)
    tnames = [b["name"] for b in tblocks if b["name"]]
    tname_counts = collections.Counter(tnames)
    tset = set(tnames)
    duplicate_names = {name for name, n in tname_counts.items() if n > 1}
    functionsets = collections.Counter(safe_ascii(b["functionset"]) for b in tblocks)
    direct_slots = collections.Counter()
    for b in tblocks:
        for key in b["direct_funcs"]:
            direct_slots[key.decode("ascii")] += 1

    map_ids, map_files = collect_server_map_ids(map_dir)
    counts = collections.Counter()
    counts["npc_files_total"] = len(all_files)
    counts["template_magic_files"] = len(templates)
    counts["create_magic_files"] = len(creates)
    counts["template_blocks"] = len(tblocks)
    counts["template_named_blocks"] = len(tnames)
    counts["template_unique_name_values"] = len(tset)
    counts["template_duplicate_name_values"] = sum(1 for _, n in tname_counts.items() if n > 1)
    counts["template_duplicate_extra_blocks"] = sum(n - 1 for n in tname_counts.values() if n > 1)
    counts["template_with_functionset"] = sum(1 for b in tblocks if b["functionset"])
    counts["template_with_direct_func_override"] = sum(1 for b in tblocks if b["direct_funcs"])
    counts["template_with_item_rows"] = sum(1 for b in tblocks if b["item_rows"])
    counts["create_blocks_raw"] = len(cblocks)
    counts["server_map_files_scanned"] = map_files
    counts["server_map_ids"] = len(map_ids)

    refs_total = 0
    resolved_total = 0
    arg_total = 0
    floors = []
    referenced_duplicate_names = set()
    resolved_per_block = collections.Counter()
    for key in (
        "create_unresolved_template_refs",
        "create_resolved_refs_over_8",
        "create_refs_to_duplicate_template_name",
        "create_blocks_with_duplicate_template_ref",
        "create_blocks_missing_floor",
    ):
        counts[key] = 0
    for b in cblocks:
        refs_total += len(b["enemies"])
        arg_total += sum(1 for _, has_arg in b["enemies"] if has_arg)
        resolved = sum(1 for name, _ in b["enemies"] if name in tset)
        duplicate_refs = sum(1 for name, _ in b["enemies"] if name in duplicate_names)
        unresolved = len(b["enemies"]) - resolved
        resolved_total += resolved
        counts["create_unresolved_template_refs"] += unresolved
        counts["create_refs_to_duplicate_template_name"] += duplicate_refs
        if duplicate_refs:
            counts["create_blocks_with_duplicate_template_ref"] += 1
            referenced_duplicate_names.update(
                name for name, _ in b["enemies"] if name in duplicate_names
            )
        resolved_per_block[resolved] += 1
        if b["born_defined"]:
            counts["create_with_born"] += 1
        if b["move_defined"]:
            counts["create_with_move"] += 1
        if b["born_corner"]:
            counts["create_with_borncorner"] += 1
        if b["move_corner"]:
            counts["create_with_movecorner"] += 1
        if b["boundary"]:
            counts["create_boundary_nonzero"] += 1
        if b["ignoreinvincible"]:
            counts["create_ignoreinvincible_nonzero"] += 1
        if b["time"] < 0:
            counts["create_negative_time"] += 1
        if resolved > 8:
            counts["create_resolved_refs_over_8"] += 1
        syntactic = b["born_defined"] and resolved > 0
        if syntactic:
            counts["create_blocks_pre_map_valid"] += 1
            floors.append(b["floorid"])
            if map_ids:
                if b["floorid"] in map_ids:
                    counts["create_blocks_effective_map_valid"] += 1
                else:
                    counts["create_blocks_missing_floor"] += 1

    counts["create_template_refs_total"] = refs_total
    counts["create_template_refs_resolved"] = resolved_total
    counts["create_refs_with_argument"] = arg_total
    counts["duplicate_template_names_referenced"] = len(referenced_duplicate_names)
    counts["unique_effective_floor_candidates"] = len(set(floors))

    cfg = setup_values(setup)
    return {
        "counts": counts,
        "extensions": ext,
        "functionsets": functionsets,
        "direct_slots": direct_slots,
        "resolved_per_block": resolved_per_block,
        "config": cfg,
        "floor_range": (min(floors), max(floors)) if floors else None,
        "aggregate": aggregate.hexdigest(),
    }


def emit(r):
    print("StoneAge recovered NPC/world-content graph probe — R1")
    print("No NPC names, dialogue, concrete arguments, coordinates, or original rows are stored in this report.")
    print("SCHEMA|recursive magic-file scan -> templates -> create refs -> map-floor validation")
    for k in ("npcdir", "filesearchnum", "npctemplatenum", "npccreatenum"):
        print(f"CONFIG|{k}|{r['config'].get(k, 'UNKNOWN')}")
    print(f"CORPUS_AGGREGATE_SHA256|{r['aggregate']}")
    for k in sorted(r["counts"]):
        print(f"COUNT|{k}|{r['counts'][k]}")
    for (kind, ext), n in sorted(r["extensions"].items()):
        print(f"MAGIC_EXTENSION|{kind}|{ext}|{n}")
    if r["floor_range"]:
        print(f"FLOOR_RANGE|min={r['floor_range'][0]}|max={r['floor_range'][1]}")
    for name, n in sorted(r["functionsets"].items()):
        print(f"FUNCTIONSET|{name}|{n}")
    for name, n in sorted(r["direct_slots"].items()):
        print(f"DIRECT_OVERRIDE_SLOT|{name}|{n}")
    for refs, n in sorted(r["resolved_per_block"].items()):
        print(f"RESOLVED_REFS_PER_CREATE|{refs}|{n}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--npc-dir", type=Path, required=True)
    ap.add_argument("--setup", type=Path)
    ap.add_argument("--map-dir", type=Path)
    args = ap.parse_args()
    emit(analyze(args.npc_dir, args.setup, args.map_dir))


if __name__ == "__main__":
    main()
