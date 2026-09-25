#!/usr/bin/env python3
"""Recover only the early Stoneage-5 battle-container payload from DATA1.CAB.

The workflow creates a sparse transient CAB: only an 8 MiB prefix is fetched
from the 612 MB cabinet, while the logical file is truncated to the advertised
cabinet length so cabextract can seek safely.  Only small early files are
extracted; no proprietary payload is committed.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re

from tools.stoneage_stoneage5_cab_probe import iso_file_slice
from tools.stoneage_stoneage5_msi_probe import find_entry, load_root

DEFAULT_PREFIX = 8 * 1024 * 1024
V1_BATTLE_SIZE = 185892
V1_BATTLE_SHA256 = "d99be6475982cf6098b90ff5dfd81ab275ec8c9271fa83daceb95e3fd4bb8859"
V1_BATTLETXT_SIZE = 5792
V1_BATTLETXT_SHA256 = "5c4a38cc7c1f039e232611b5eac33514f67c4d8badbaf638ae9b852440237fc4"
TARGETS = ("soundaddr_3.txt", "battle_2.bin", "data_1.bin", "battletxt_2.txt")


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def prepare_sparse(path, prefix_bytes):
    meta, cue_name, cue_bytes, track, bin_row, bin_url, info, entries = load_root()
    cab = find_entry(entries, "DATA1.CAB")
    if cab is None:
        raise RuntimeError("DATA1.CAB-not-found")
    prefix_bytes = min(int(prefix_bytes), int(cab["size"]))
    body, status, content_range = iso_file_slice(
        bin_url, cab, track, 0, prefix_bytes
    )
    with open(path, "wb") as fh:
        fh.write(body)
        fh.truncate(int(cab["size"]))
    print(
        f"SPARSE_CAB|path={path}|logical_size={cab['size']}|fetched_prefix={len(body)}|"
        f"status={status}|content_range={content_range}|allocated_hint={os.stat(path).st_blocks * 512}"
    )


def decode_text(data):
    for enc in ("utf-8", "gb18030", "cp950", "latin1"):
        try:
            return enc, data.decode(enc)
        except UnicodeDecodeError:
            pass
    return "latin1", data.decode("latin1", "replace")


def analyze(directory):
    print("StoneAge Stoneage-5 bounded battle-payload analysis — R1")
    print(
        "SCOPE|8MiB-CAB-prefix+sparse-cab+selected-early-files|"
        "no-full-cab-download|derived-hashes-and-structure-only"
    )
    for name in TARGETS:
        path = os.path.join(directory, name)
        if not os.path.exists(path):
            print(f"TARGET_MISSING|name={name}")
            continue
        data = open(path, "rb").read()
        print(f"TARGET|name={name}|size={len(data)}|sha256={sha256(data)}")

        if name == "battle_2.bin":
            prefix = data[:V1_BATTLE_SIZE]
            tail = data[V1_BATTLE_SIZE:]
            print(
                f"V1_PREFIX|name=battle_2.bin|reference_size={V1_BATTLE_SIZE}|"
                f"reference_sha256={V1_BATTLE_SHA256}|prefix_sha256={sha256(prefix)}|"
                f"exact_match={int(len(prefix)==V1_BATTLE_SIZE and sha256(prefix)==V1_BATTLE_SHA256)}|"
                f"tail_bytes={len(tail)}|tail_sha256={sha256(tail)}"
            )
            if len(tail) % 804 == 0:
                print(f"TAIL_RECORDS|name=battle_2.bin|record_size=804|count={len(tail)//804}")

        if name == "battletxt_2.txt":
            prefix = data[:V1_BATTLETXT_SIZE]
            tail = data[V1_BATTLETXT_SIZE:]
            print(
                f"V1_PREFIX|name=battletxt_2.txt|reference_size={V1_BATTLETXT_SIZE}|"
                f"reference_sha256={V1_BATTLETXT_SHA256}|prefix_sha256={sha256(prefix)}|"
                f"exact_match={int(len(prefix)==V1_BATTLETXT_SIZE and sha256(prefix)==V1_BATTLETXT_SHA256)}|"
                f"tail_bytes={len(tail)}|tail_sha256={sha256(tail)}"
            )
            enc, text = decode_text(data)
            rows = re.findall(r"(\d+):(\d+):([^\s\x00]+)", text)
            print(f"BATTLETXT|encoding={enc}|entries={len(rows)}")
            for i, (off, size, fname) in enumerate(rows):
                if i < 4 or i >= max(0, len(rows)-6):
                    print(
                        f"BATTLE_ROW|index={i}|offset={off}|size={size}|file={fname}"
                    )
            if rows:
                contiguous = 1
                expected = 0
                for off, size, _fname in rows:
                    if int(off) != expected:
                        contiguous = 0
                        break
                    expected += int(size)
                print(
                    f"BATTLE_TABLE|contiguous={contiguous}|declared_end={expected}|"
                    f"battle_bin_size="
                    + str(os.path.getsize(os.path.join(directory, "battle_2.bin"))
                          if os.path.exists(os.path.join(directory, "battle_2.bin")) else -1)
                )
    print(
        "EVIDENCE_BOUNDARY|selected extracted bytes are transient and deleted by CI; "
        "the committed report contains only hashes, sizes, prefix-comparison results "
        "and parsed text-table structure."
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-cab")
    ap.add_argument("--prefix-bytes", type=int, default=DEFAULT_PREFIX)
    ap.add_argument("--analyze-dir")
    args = ap.parse_args()
    if bool(args.output_cab) == bool(args.analyze_dir):
        ap.error("choose exactly one of --output-cab or --analyze-dir")
    if args.output_cab:
        prepare_sparse(args.output_cab, args.prefix_bytes)
    else:
        analyze(args.analyze_dir)


if __name__ == "__main__":
    main()
