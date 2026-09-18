#!/usr/bin/env python3
"""Rank recovered StoneAge NPC functionsets by secondary-argument usage without retaining payloads."""

import argparse
import collections
from pathlib import Path

from tools.stoneage_npc_world_graph_probe import iter_blocks, magic_kind


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


def safe_ascii(value):
    if not value:
        return "<none>"
    text = value.decode("ascii", "replace")
    return "".join(c if 32 <= ord(c) < 127 else "?" for c in text)


def assigned_file(arg):
    for token in arg.split(b"|"):
        if b"file" in token:
            parts = token.split(b":")
            if len(parts) >= 2:
                return parts[1].decode("utf-8", "replace")
    return None


def analyze(npc_dir):
    files = sorted((p for p in npc_dir.rglob("*") if p.is_file()), key=lambda p: str(p).lower())
    templates = [p for p in files if magic_kind(p) == "template"]
    creates = [p for p in files if magic_kind(p) == "create"]
    mapping = parse_template_map(templates)

    counts = collections.Counter()
    refs = collections.Counter()
    arg_refs = collections.Counter()
    file_refs = collections.Counter()
    inline_refs = collections.Counter()
    missing_files = collections.Counter()
    noarg_refs = collections.Counter()

    counts["template_name_values"] = len(mapping)
    counts["ambiguous_template_names"] = sum(1 for vals in mapping.values() if len(vals) != 1)

    for name, arg in iter_create_refs(creates):
        counts["create_refs_total"] += 1
        defs = mapping.get(name)
        if not defs:
            counts["create_refs_unresolved"] += 1
            continue
        if len(defs) != 1:
            counts["create_refs_ambiguous"] += 1
            continue

        fset = safe_ascii(defs[0])
        refs[fset] += 1
        if not arg:
            noarg_refs[fset] += 1
            continue

        arg_refs[fset] += 1
        fn = assigned_file(arg)
        if fn is None:
            inline_refs[fset] += 1
        else:
            file_refs[fset] += 1
            if not (npc_dir / fn).is_file():
                missing_files[fset] += 1

    counts["create_refs_resolved_unambiguous"] = sum(refs.values())
    counts["create_refs_with_argument_resolved_unambiguous"] = sum(arg_refs.values())
    counts["create_refs_file_argument_resolved_unambiguous"] = sum(file_refs.values())
    counts["create_refs_inline_argument_resolved_unambiguous"] = sum(inline_refs.values())
    counts["create_refs_no_argument_resolved_unambiguous"] = sum(noarg_refs.values())
    counts["secondary_argument_files_missing"] = sum(missing_files.values())

    return {
        "counts": counts,
        "refs": refs,
        "arg_refs": arg_refs,
        "file_refs": file_refs,
        "inline_refs": inline_refs,
        "missing_files": missing_files,
        "noarg_refs": noarg_refs,
    }


def emit(result):
    print("StoneAge recovered NPC secondary-argument queue probe — R1")
    print("No NPC/template names, paths, dialogue, coordinates, or argument payload values are stored.")
    print("SCHEMA|unambiguous template functionset -> create references -> argument transport only")
    for key in sorted(result["counts"]):
        print(f"COUNT|{key}|{result['counts'][key]}")

    all_sets = sorted(result["refs"])
    for fset in all_sets:
        print(
            "FUNCTIONSET_USAGE|{}|refs={}|arg={}|file={}|inline={}|noarg={}|missing_file={}".format(
                fset,
                result["refs"][fset],
                result["arg_refs"][fset],
                result["file_refs"][fset],
                result["inline_refs"][fset],
                result["noarg_refs"][fset],
                result["missing_files"][fset],
            )
        )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--npc-dir", type=Path, required=True)
    args = ap.parse_args()
    emit(analyze(args.npc_dir))


if __name__ == "__main__":
    main()
