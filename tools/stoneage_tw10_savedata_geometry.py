#!/usr/bin/env python3
"""Independent geometry check of the accepted TW 1.0 savedata R1 *metadata*.

No original file, program, ISO, or network access is used. Zero-run positions
are not mapped to fields, strings, records, or runtime persistence without
further binary/control-flow evidence.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from functools import reduce
from math import gcd
from pathlib import Path

PINNED_SAVEDATA_SHA256 = "5b26f54a9723cd2c5275f964457094fdf1fc33ca086cdaf55bb5350dfb04f3f9"
DEFAULT_SOURCE = Path(__file__).resolve().parents[1] / "research/recovered/STONEAGE-TW10-SAVEDATA-R1.txt"


@dataclass(frozen=True)
class Geometry:
    size: int
    digest: str
    zero_starts: tuple[int, ...]
    zero_lengths: tuple[int, ...]
    largest_start_divisor: int
    largest_gap_divisor: int
    positive_multiples_unmarked: tuple[int, ...]
    start_gaps: tuple[int, ...]


def _fields(line: str) -> dict[str, str]:
    parts = line.split("|")
    result = {}
    for part in parts[1:]:
        if "=" not in part:
            raise ValueError("invalid metadata field")
        key, value = part.split("=", 1)
        if not key or key in result:
            raise ValueError("missing/duplicate metadata key")
        result[key] = value
    return result


def geometry_from_text(text: str, expected_digest: str = PINNED_SAVEDATA_SHA256) -> Geometry:
    saved = []
    zeros = []
    spans = []
    for line in text.splitlines():
        if line.startswith("SAVEDATA|"):
            saved.append(_fields(line))
        elif line.startswith("ZERO_RUN|"):
            zeros.append(_fields(line))
        elif line.startswith("SAVEDATA_SPAN|"):
            spans.append(_fields(line))
    if len(saved) != 1 or len(spans) != 1:
        raise ValueError("require exactly one savedata summary and span")
    summary = saved[0]
    span = spans[0]
    if summary.get("sha256") != expected_digest:
        raise ValueError("unrecognized savedata hash")
    size = int(summary["size"])
    if size <= 0 or size > 4096:
        raise ValueError("unbounded file size")
    intervals = []
    for row in zeros:
        start, length = int(row["start"]), int(row["length"])
        if start < 0 or length < 1 or start + length > size:
            raise ValueError("invalid zero run")
        intervals.append((start, length))
    intervals.sort()
    for (a, length), (b, _) in zip(intervals, intervals[1:]):
        if a + length > b:
            raise ValueError("overlapping zero runs")
    total_zero = sum(length for _, length in intervals)
    if (len(intervals) != int(summary["zero_runs"])
            or total_zero != int(summary["zero_bytes"])
            or total_zero + int(summary["nonzero_bytes"]) != size):
        raise ValueError("summary inconsistent with runs")
    if int(span["first_nonzero"]) < 0 or int(span["last_nonzero"]) >= size:
        raise ValueError("nonzero span out of range")
    starts = tuple(a for a, _ in intervals)
    gaps = tuple(b - a for a, b in zip(starts, starts[1:]))
    common_start = reduce(gcd, starts, 0)
    common_gap = reduce(gcd, gaps, 0)
    if common_start == 0:
        missing = ()
    else:
        marked = set(starts)
        missing = tuple(i for i in range(common_start, size, common_start) if i not in marked)
    return Geometry(
        size=size,
        digest=summary["sha256"],
        zero_starts=starts,
        zero_lengths=tuple(length for _, length in intervals),
        largest_start_divisor=common_start,
        largest_gap_divisor=common_gap,
        positive_multiples_unmarked=missing,
        start_gaps=gaps,
    )


def format_geometry(g: Geometry) -> str:
    def csv(nums): return ",".join(map(str, nums)) if nums else "none"
    return "\n".join((
        "StoneAge TW v1.0 savedata *derived metadata* zero-run geometry — R1",
        "SCOPE|R1-derived-metadata-only|no-original-payload|no-native-execution",
        f"IDENTITY|savedata_sha256={g.digest}|size={g.size}",
        f"RUNS|count={len(g.zero_starts)}|starts={csv(g.zero_starts)}|lengths={csv(g.zero_lengths)}",
        f"MODULARITY|largest_positive_start_divisor={g.largest_start_divisor}|"
        f"largest_consecutive_start_gap_divisor={g.largest_gap_divisor}|"
        f"gaps={csv(g.start_gaps)}",
        f"UNMARKED_MULTIPLES|of_largest_start_divisor={csv(g.positive_multiples_unmarked)}",
        "BOUNDARY|Modular alignment of zeros is observed geometry, NOT a proven "
        "field width, record count, delimiter semantics, codec, or read/write path.",
        "RESOLUTION|TW10_SAVEDATA_ZERO_RUN_GEOMETRY_ONLY",
    ))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    args = ap.parse_args()
    print(format_geometry(geometry_from_text(args.source.read_text(encoding="utf-8"))))


if __name__ == "__main__":
    main()
