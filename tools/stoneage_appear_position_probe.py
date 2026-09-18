#!/usr/bin/env python3
"""Probe recovered StoneAge appear-position table without retaining rows."""

import argparse, collections, hashlib
from pathlib import Path


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def clean_lines(path):
    for raw in path.read_bytes().splitlines():
        line = raw.strip()
        if not line or line.startswith(b"#"):
            continue
        yield line


def c_atoi(token):
    s = token.decode("ascii", "ignore").lstrip()
    if not s:
        return 0
    sign = 1
    if s[0] in "+-":
        if s[0] == "-":
            sign = -1
        s = s[1:]
    digits = []
    for ch in s:
        if not ch.isdigit():
            break
        digits.append(ch)
    return sign * int("".join(digits)) if digits else 0


def setup_value(path, key):
    if not path or not path.exists():
        return None
    key = key.lower()
    for raw in path.read_bytes().splitlines():
        line = raw.split(b"#", 1)[0].strip()
        if b"=" not in line:
            continue
        k, v = line.split(b"=", 1)
        if k.decode("ascii", "ignore").strip().lower() == key:
            return v.decode("utf-8", "replace").strip()
    return None


def parse(path):
    rows = []
    field_counts = collections.Counter()
    malformed = 0
    for line in clean_lines(path):
        fields = line.replace(b"\t", b" ").split()
        field_counts[len(fields)] += 1
        if len(fields) < 3:
            malformed += 1
            continue
        floor, x, y = (c_atoi(v) for v in fields[:3])
        rows.append((floor, x, y))

    floor_counts = collections.Counter(f for f, _, _ in rows)
    triplet_counts = collections.Counter(rows)
    return {
        "rows": rows,
        "field_counts": field_counts,
        "malformed": malformed,
        "unique_floors": len(floor_counts),
        "duplicate_floor_values": sum(1 for n in floor_counts.values() if n > 1),
        "duplicate_floor_extra_rows": sum(n - 1 for n in floor_counts.values() if n > 1),
        "duplicate_triplet_values": sum(1 for n in triplet_counts.values() if n > 1),
        "duplicate_triplet_extra_rows": sum(n - 1 for n in triplet_counts.values() if n > 1),
    }


def emit(data_dir, setup=None):
    configured = setup_value(setup, "appearpositionfile")
    name = Path(configured.replace("\\", "/")).name if configured else "appear.txt"
    path = data_dir / name
    if not path.exists():
        raise SystemExit(f"appear file not found: {path}")

    d = parse(path)
    rows = d["rows"]

    print("StoneAge recovered appear-position probe — R1")
    print("No floor IDs, coordinates, comments, or original rows are stored in this report.")
    print(f"ACTIVE_APPEAR_CONFIG|{configured or 'UNKNOWN'}")
    print(f"FILE|{path.name}|bytes={path.stat().st_size}|sha256={sha256(path)}")
    print(f"VALID_ROWS|{len(rows)}")
    print(f"MALFORMED_ROWS|{d['malformed']}")
    for n, count in sorted(d["field_counts"].items()):
        print(f"FIELD_COUNT|{n}|{count}")
    print(f"UNIQUE_FLOORS|{d['unique_floors']}")
    print(f"DUPLICATE_FLOOR_VALUES|{d['duplicate_floor_values']}")
    print(f"DUPLICATE_FLOOR_EXTRA_ROWS|{d['duplicate_floor_extra_rows']}")
    print(f"DUPLICATE_TRIPLET_VALUES|{d['duplicate_triplet_values']}")
    print(f"DUPLICATE_TRIPLET_EXTRA_ROWS|{d['duplicate_triplet_extra_rows']}")
    if rows:
        floors = [r[0] for r in rows]
        xs = [r[1] for r in rows]
        ys = [r[2] for r in rows]
        print(f"FLOOR_STAT|min={min(floors)}|max={max(floors)}")
        print(f"X_STAT|min={min(xs)}|max={max(xs)}")
        print(f"Y_STAT|min={min(ys)}|max={max(ys)}")
        print(f"NEGATIVE_COORD_ROWS|{sum(1 for _,x,y in rows if x < 0 or y < 0)}")
        print(f"ZERO_COORD_ROWS|{sum(1 for _,x,y in rows if x == 0 or y == 0)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", type=Path, required=True)
    ap.add_argument("--setup", type=Path)
    a = ap.parse_args()
    emit(a.data_dir, a.setup)


if __name__ == "__main__":
    main()
