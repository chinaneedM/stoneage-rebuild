#!/usr/bin/env python3
"""Deterministic validation of the legacy RD decoder against recovered ADRN/REAL bytes."""

import argparse
import hashlib
import struct
from pathlib import Path

from tools.stoneage_rd_codec import RDDecodeError, decode_rd_block

ADRN_RECORD_SIZE = 80
RD_HEADER_SIZE = 16


def signed32(value: int) -> int:
    return struct.unpack("<i", struct.pack("<I", value))[0]


def load_records(adrn_path: Path):
    records = []
    with adrn_path.open("rb") as f:
        index = 0
        while True:
            rec = f.read(ADRN_RECORD_SIZE)
            if not rec:
                break
            if len(rec) != ADRN_RECORD_SIZE:
                raise ValueError("truncated ADRN record")
            bitmapno, adder, size, xoff, yoff, width_u, height_u = struct.unpack_from(
                "<IIIiiII", rec, 0
            )
            records.append(
                {
                    "index": index,
                    "bitmapno": bitmapno,
                    "adder": adder,
                    "size": size,
                    "xoff": xoff,
                    "yoff": yoff,
                    "width_u": width_u,
                    "height_u": height_u,
                    "width_s": signed32(width_u),
                    "height_s": signed32(height_u),
                }
            )
            index += 1
    return records


def select_indices(records, prefix_count: int, stride: int, tail_count: int):
    selected = set()
    decodable = []

    for rec in records:
        w, h = rec["width_s"], rec["height_s"]
        if 0 < w <= 16384 and 0 < h <= 16384 and rec["size"] >= RD_HEADER_SIZE:
            decodable.append(rec["index"])

    selected.update(decodable[:prefix_count])
    selected.update(decodable[-tail_count:])

    if stride > 0:
        selected.update(decodable[::stride])

    return selected


def validate(adrn_path: Path, real_path: Path, prefix_count=4096, stride=4096, tail_count=64):
    records = load_records(adrn_path)
    selected = select_indices(records, prefix_count, stride, tail_count)

    successes = []
    failures = []
    skipped_special = []
    all_flag0 = []
    aggregate = hashlib.sha256()

    with real_path.open("rb") as real:
        for rec in records:
            real.seek(rec["adder"])
            header = real.read(RD_HEADER_SIZE)
            if len(header) < RD_HEADER_SIZE:
                failures.append((rec["index"], rec["bitmapno"], "truncated_header"))
                continue
            if header[:2] != b"RD":
                failures.append((rec["index"], rec["bitmapno"], "missing_rd_magic"))
                continue

            flag = header[2]
            if flag == 0:
                all_flag0.append(rec["index"])
                selected.add(rec["index"])

            if rec["index"] not in selected:
                continue

            if rec["width_s"] <= 0 or rec["height_s"] <= 0:
                skipped_special.append(
                    (rec["index"], rec["bitmapno"], rec["width_s"], rec["height_s"], flag)
                )
                continue

            real.seek(rec["adder"])
            block = real.read(rec["size"])
            try:
                rd_header, pixels = decode_rd_block(
                    block, authoritative_block_size=rec["size"]
                )
                if len(pixels) != rec["width_s"] * rec["height_s"]:
                    raise RDDecodeError("decoded pixel length does not match ADRN dimensions")
                digest = hashlib.sha256(pixels).hexdigest()
                row = (
                    rec["index"],
                    rec["bitmapno"],
                    rec["size"],
                    flag,
                    rec["width_s"],
                    rec["height_s"],
                    digest,
                )
                successes.append(row)
                aggregate.update(
                    ("|".join(map(str, row)) + "\n").encode("ascii")
                )
            except Exception as exc:
                failures.append(
                    (rec["index"], rec["bitmapno"], flag, rec["width_s"], rec["height_s"], str(exc))
                )

    return {
        "record_count": len(records),
        "selected_count": len(selected),
        "flag0_indices": all_flag0,
        "successes": successes,
        "failures": failures,
        "skipped_special": skipped_special,
        "aggregate_sha256": aggregate.hexdigest(),
    }


def emit(result, sample_limit=20):
    print("StoneAge recovered RD decode validation — R1")
    print("No decoded image bytes are stored in this report.")
    print(f"ADRN_RECORD_COUNT|{result['record_count']}")
    print(f"SELECTED_RECORDS|{result['selected_count']}")
    print(f"DECODE_SUCCESSES|{len(result['successes'])}")
    print(f"DECODE_FAILURES|{len(result['failures'])}")
    print(f"SKIPPED_SPECIAL_DIMENSIONS|{len(result['skipped_special'])}")
    print(f"FLAG0_RECORD_COUNT|{len(result['flag0_indices'])}")
    print("FLAG0_INDICES|" + ",".join(map(str, result["flag0_indices"])))
    print(f"AGGREGATE_SAMPLE_SHA256|{result['aggregate_sha256']}")
    print("SUCCESS_SAMPLE|index|bitmapno|block_size|flag|width|height|decoded_sha256")
    for row in result["successes"][:sample_limit]:
        print("SUCCESS_SAMPLE|" + "|".join(map(str, row)))
    print("FAILURE_SAMPLE|index|bitmapno|flag|width|height|reason")
    for row in result["failures"][:sample_limit]:
        print("FAILURE_SAMPLE|" + "|".join(map(str, row)))
    print("SPECIAL_SAMPLE|index|bitmapno|width|height|flag")
    for row in result["skipped_special"][:sample_limit]:
        print("SPECIAL_SAMPLE|" + "|".join(map(str, row)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--adrn", type=Path, required=True)
    parser.add_argument("--real", type=Path, required=True)
    parser.add_argument("--prefix-count", type=int, default=4096)
    parser.add_argument("--stride", type=int, default=4096)
    parser.add_argument("--tail-count", type=int, default=64)
    args = parser.parse_args()
    result = validate(
        args.adrn,
        args.real,
        prefix_count=args.prefix_count,
        stride=args.stride,
        tail_count=args.tail_count,
    )
    emit(result)
    if result["failures"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
