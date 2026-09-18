#!/usr/bin/env python3
"""Cross-check recovered StoneAge effect callback tokens against fixed source dispatch tables.

This probe intentionally emits only aggregate coverage counts and classification hashes.
It does not publish original item/magic/pet-skill names, callback tokens, or table rows.
"""

import argparse
import collections
import hashlib
import re
from pathlib import Path

ITEM_CALLBACK_COLUMNS = {
    "initfunc": 6,
    "preoverfunc": 7,
    "postoverfunc": 8,
    "watchfunc": 9,
    "usefunc": 10,
    "attachfunc": 11,
    "detachfunc": 12,
    "dropfunc": 13,
    "pickupfunc": 14,
    "relifefunc": 15,
}


def clean_csv_rows(path):
    rows = []
    if not path or not path.exists():
        return rows
    for raw in path.read_bytes().splitlines():
        line = raw.strip()
        if not line or line.startswith(b"#"):
            continue
        rows.append([x.strip() for x in line.replace(b"\t", b" ").split(b",")])
    return rows


def setup_entries(path):
    out = {}
    if not path or not path.exists():
        return out
    for raw in path.read_bytes().splitlines():
        line = raw.split(b"#", 1)[0].strip()
        if b"=" not in line:
            continue
        k, v = line.split(b"=", 1)
        key = k.decode("ascii", "ignore").strip().lower()
        value = v.decode("utf-8", "replace").strip()
        out[key] = value
    return out


def basename(value):
    return Path(value.replace("\\", "/")).name if value else ""


def choose_active_file(data_dir, setup, *, kind):
    entries = setup_entries(setup)
    if kind == "item":
        names = [
            basename(v)
            for k, v in entries.items()
            if k.startswith("itemset") and basename(v).lower().startswith("itemset")
        ]
        default = "itemset.txt"
    elif kind == "magic":
        names = [basename(entries.get("magicfile", ""))]
        default = "magic.txt"
    elif kind == "petskill":
        names = [
            basename(v)
            for k, v in entries.items()
            if k in {"petskillfile1", "petskillfile2"}
        ]
        default = "petskill.txt"
    else:
        raise ValueError("unknown kind")

    names = [x for x in names if x]
    if names:
        chosen = collections.Counter(x.lower() for x in names).most_common(1)[0][0]
        for p in data_dir.iterdir():
            if p.is_file() and p.name.lower() == chosen:
                return p
    return data_dir / default


def token_text(raw):
    return raw.decode("utf-8", "replace").strip()


def item_callback_counters(path):
    rows = clean_csv_rows(path)
    out = {name: collections.Counter() for name in ITEM_CALLBACK_COLUMNS}
    for row in rows:
        for name, idx in ITEM_CALLBACK_COLUMNS.items():
            if idx < len(row) and row[idx]:
                out[name][token_text(row[idx])] += 1
    return rows, out


def single_callback_counter(path, column=2):
    rows = clean_csv_rows(path)
    out = collections.Counter()
    for row in rows:
        if column < len(row) and row[column]:
            out[token_text(row[column])] += 1
    return rows, out


def extract_table_region(text, marker):
    pos = text.find(marker)
    if pos < 0:
        raise ValueError(f"missing source table marker: {marker}")
    end = text.find("\n};", pos)
    if end < 0:
        end = text.find("\r\n};", pos)
    if end < 0:
        raise ValueError(f"unterminated source table: {marker}")
    return text[pos:end]


def parse_global_function_table(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    region = extract_table_region(text, "correspondStringAndFunctionTable[]")
    return set(re.findall(r'\{\s*\{\s*"([^"]+)"\s*\}', region))


def parse_named_function_table(path, marker):
    text = path.read_text(encoding="utf-8", errors="replace")
    region = extract_table_region(text, marker)
    return set(re.findall(r'\{\s*"([^"]+)"', region))


def source_dispatch_sets(args):
    return {
        "gavin": {
            "item": parse_global_function_table(args.gavin_function),
            "magic": parse_named_function_table(args.gavin_magic, "MAGIC_functbl[]"),
            "petskill": parse_named_function_table(args.gavin_petskill, "PETSKILL_functbl[]"),
        },
        "iris": {
            "item": parse_global_function_table(args.iris_function),
            "magic": parse_named_function_table(args.iris_magic, "MAGIC_functbl[]"),
            "petskill": parse_named_function_table(args.iris_petskill, "PETSKILL_functbl[]"),
        },
        "bismarck": {
            "item": parse_global_function_table(args.bismarck_function),
            "magic": parse_named_function_table(args.bismarck_magic, ("sMageicFunctionTable[]", "MAGIC_functbl[]")),
            "petskill": parse_named_function_table(args.bismarck_petskill, "PETSKILL_functbl[]"),
        },
    }


def coverage(counter, lineage_sets):
    tokens = set(counter)
    lineages = tuple(sorted(lineage_sets))
    cls = collections.Counter()
    row_cls = collections.Counter()
    per = {}
    digest = hashlib.sha256()

    for token in sorted(tokens):
        mask = tuple(int(token in lineage_sets[name]) for name in lineages)
        matched = sum(mask)
        label = "all" if matched == len(lineages) else ("none" if matched == 0 else "some")
        cls[label] += 1
        row_cls[label] += counter[token]
        digest.update((token + "|" + "".join(map(str, mask)) + "\n").encode("utf-8"))

    for name in lineages:
        matched_tokens = [t for t in tokens if t in lineage_sets[name]]
        per[name] = {
            "unique_matched": len(matched_tokens),
            "row_uses_matched": sum(counter[t] for t in matched_tokens),
            "declared_dispatch_tokens": len(lineage_sets[name]),
        }

    return {
        "unique": len(tokens),
        "row_uses": sum(counter.values()),
        "classes": cls,
        "row_classes": row_cls,
        "per": per,
        "classification_sha256": digest.hexdigest(),
    }


def analyze(args):
    sources = source_dispatch_sets(args)
    item_path = choose_active_file(args.data_dir, args.setup, kind="item")
    magic_path = choose_active_file(args.data_dir, args.setup, kind="magic")
    petskill_path = choose_active_file(args.data_dir, args.setup, kind="petskill")

    item_rows, item_slots = item_callback_counters(item_path)
    magic_rows, magic_tokens = single_callback_counter(magic_path, 2)
    petskill_rows, petskill_tokens = single_callback_counter(petskill_path, 2)

    item_sets = {name: s["item"] for name, s in sources.items()}
    magic_sets = {name: s["magic"] for name, s in sources.items()}
    petskill_sets = {name: s["petskill"] for name, s in sources.items()}

    return {
        "paths": {
            "item": item_path,
            "magic": magic_path,
            "petskill": petskill_path,
        },
        "row_counts": {
            "item": len(item_rows),
            "magic": len(magic_rows),
            "petskill": len(petskill_rows),
        },
        "item_slots": {
            slot: coverage(counter, item_sets)
            for slot, counter in item_slots.items()
        },
        "magic": coverage(magic_tokens, magic_sets),
        "petskill": coverage(petskill_tokens, petskill_sets),
    }


def emit_coverage(prefix, result):
    print(f"{prefix}|unique_tokens={result['unique']}|row_uses={result['row_uses']}|"
          f"all3_unique={result['classes'].get('all',0)}|"
          f"some_unique={result['classes'].get('some',0)}|"
          f"none_unique={result['classes'].get('none',0)}|"
          f"all3_rows={result['row_classes'].get('all',0)}|"
          f"some_rows={result['row_classes'].get('some',0)}|"
          f"none_rows={result['row_classes'].get('none',0)}|"
          f"classification_sha256={result['classification_sha256']}")
    for lineage, p in sorted(result["per"].items()):
        print(f"{prefix}_LINEAGE|{lineage}|declared_dispatch_tokens={p['declared_dispatch_tokens']}|"
              f"unique_matched={p['unique_matched']}|row_uses_matched={p['row_uses_matched']}")


def emit(args):
    r = analyze(args)
    print("StoneAge recovered effect-callback coverage probe — R1")
    print("No original names, callback tokens, descriptions, options, or data rows are stored in this report.")
    print("COVERAGE_BOUNDARY|declared fixed-source dispatch tables; preprocessor presence is not compiled-active proof")
    for kind in ("item", "magic", "petskill"):
        print(f"ACTIVE_FILE|{kind}|{r['paths'][kind].name}|rows={r['row_counts'][kind]}")
    for slot, result in r["item_slots"].items():
        emit_coverage(f"ITEM_SLOT|{slot}", result)
    emit_coverage("MAGIC", r["magic"])
    emit_coverage("PETSKILL", r["petskill"])


def add_source_args(ap, prefix):
    ap.add_argument(f"--{prefix}-function", type=Path, required=True)
    ap.add_argument(f"--{prefix}-magic", type=Path, required=True)
    ap.add_argument(f"--{prefix}-petskill", type=Path, required=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", type=Path, required=True)
    ap.add_argument("--setup", type=Path)
    for prefix in ("gavin", "iris", "bismarck"):
        add_source_args(ap, prefix)
    args = ap.parse_args()
    emit(args)


if __name__ == "__main__":
    main()
