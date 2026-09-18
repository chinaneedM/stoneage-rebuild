#!/usr/bin/env python3
"""Probe recovered Dengon runtime files using record metadata only.

No filename/coordinate, player name, timestamp text, or message payload is
emitted. Only fixed-record structural metadata and ID counters are retained.
"""

import argparse
import collections
import hashlib
from pathlib import Path

LINE_COUNT = 1000
STRING_SIZE = 256
COUNTER_SIZE = 11
ENTRY_SIZE = COUNTER_SIZE + STRING_SIZE + 1
EXPECTED_FILE_SIZE = LINE_COUNT * ENTRY_SIZE


def parse_prefix(block):
    if len(block) < COUNTER_SIZE:
        return None
    prefix = block[:COUNTER_SIZE]
    if prefix[10:11] != b":":
        return None
    digits = prefix[:10]
    if not all(48 <= ch <= 57 for ch in digits):
        return None
    return int(digits)


def analyze(gmsv_dir):
    dengon = gmsv_dir / "Dengon"
    counts = collections.Counter()
    sizes = collections.Counter()
    max_ids = collections.Counter()
    aggregate = hashlib.sha256()

    if not dengon.is_dir():
        counts["directory_missing"] = 1
        return {
            "counts": counts,
            "sizes": sizes,
            "max_ids": max_ids,
            "aggregate": aggregate.hexdigest(),
        }

    files = sorted(p for p in dengon.iterdir() if p.is_file())
    counts["files"] = len(files)

    for path in files:
        data = path.read_bytes()
        sizes[len(data)] += 1
        aggregate.update(
            str(len(data)).encode() + b"|" +
            hashlib.sha256(data).hexdigest().encode() + b"\n"
        )

        if len(data) == EXPECTED_FILE_SIZE:
            counts["expected_size_files"] += 1
        else:
            counts["size_deviation_files"] += 1

        if len(data) == COUNTER_SIZE:
            stub_id = parse_prefix(data)
            if stub_id is not None:
                counts["counter_only_stub_files"] += 1
                if stub_id == 0:
                    counts["zero_counter_stub_files"] += 1
                else:
                    counts["nonzero_counter_stub_files"] += 1

        record_count = min(LINE_COUNT, len(data) // ENTRY_SIZE)
        valid = 0
        malformed = 0
        nonzero = 0
        max_id = 0
        for slot in range(record_count):
            start = slot * ENTRY_SIZE
            value = parse_prefix(data[start:start + ENTRY_SIZE])
            if value is None:
                malformed += 1
                continue
            valid += 1
            if value > 0:
                nonzero += 1
                if value > max_id:
                    max_id = value

        counts["records_examined"] += record_count
        counts["valid_counter_records"] += valid
        counts["malformed_counter_records"] += malformed
        counts["nonzero_counter_records"] += nonzero
        if nonzero:
            counts["active_files"] += 1
        else:
            counts["empty_files"] += 1
        max_ids[max_id] += 1

    return {
        "counts": counts,
        "sizes": sizes,
        "max_ids": max_ids,
        "aggregate": aggregate.hexdigest(),
    }


def emit(result):
    print("StoneAge recovered Dengon runtime structure probe — R1")
    print(
        "No board filenames/coordinates, messages, player names, or timestamp "
        "payloads are stored."
    )
    print(
        f"SCHEMA|Dengon runtime -> {LINE_COUNT} fixed slots x "
        f"{ENTRY_SIZE} bytes -> counter-only aggregate"
    )
    print("RUNTIME_CORPUS_AGGREGATE_SHA256|" + result["aggregate"])
    for key, value in sorted(result["counts"].items()):
        print(f"COUNT|{key}|{value}")
    for size, blocks in sorted(result["sizes"].items()):
        print(f"FILE_SIZE|bytes={size}|files={blocks}")
    for max_id, blocks in sorted(result["max_ids"].items()):
        print(f"MAX_ID|value={max_id}|files={blocks}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gmsv-dir", type=Path, required=True)
    emit(analyze(ap.parse_args().gmsv_dir))


if __name__ == "__main__":
    main()
