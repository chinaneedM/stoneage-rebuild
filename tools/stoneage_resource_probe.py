#!/usr/bin/env python3
"""Read-only structural probe for StoneAge ADRN/REAL image resources and client MAP files."""

import argparse
import collections
import mmap
import struct
from pathlib import Path

ADRN_RECORD_SIZE = 80
RD_HEADER_SIZE = 16


def analyze_real_adrn(adrn_path: Path, real_path: Path, sample_limit: int = 12):
    adrn_size = adrn_path.stat().st_size
    real_size = real_path.stat().st_size
    total = adrn_size // ADRN_RECORD_SIZE
    remainder = adrn_size % ADRN_RECORD_SIZE
    counts = collections.Counter()
    flags = collections.Counter()
    samples = []
    bad = []
    bitmap_seen = set()
    duplicate_bitmap = 0
    prev_adder = None
    prev_end = None
    nondecreasing = 0
    contiguous = 0
    gaps = 0
    overlaps = 0
    max_end = 0
    active = 0
    anomaly_samples = []
    duplicate_samples = []

    with adrn_path.open("rb") as af, real_path.open("rb") as rf:
        mm = mmap.mmap(rf.fileno(), 0, access=mmap.ACCESS_READ)
        try:
            for idx in range(total):
                rec = af.read(ADRN_RECORD_SIZE)
                if len(rec) != ADRN_RECORD_SIZE:
                    break

                bitmapno, adder, size, xoff, yoff, width, height = struct.unpack_from(
                    "<IIIiiii", rec, 0
                )

                if bitmapno in bitmap_seen:
                    duplicate_bitmap += 1
                    if len(duplicate_samples) < sample_limit:
                        duplicate_samples.append((idx, bitmapno))
                else:
                    bitmap_seen.add(bitmapno)

                if adder == 0 and size == 0:
                    counts["empty_offset_size"] += 1
                    continue

                active += 1
                if prev_adder is not None and adder >= prev_adder:
                    nondecreasing += 1
                if prev_end is not None:
                    if adder == prev_end:
                        contiguous += 1
                    elif adder > prev_end:
                        gaps += 1
                    else:
                        overlaps += 1
                prev_adder = adder
                prev_end = adder + size
                max_end = max(max_end, prev_end)

                in_bounds = (
                    size >= RD_HEADER_SIZE
                    and adder <= real_size
                    and adder + size <= real_size
                )
                if not in_bounds:
                    counts["out_of_bounds"] += 1
                    if len(bad) < sample_limit:
                        bad.append(
                            (idx, bitmapno, adder, size, width, height, "out_of_bounds")
                        )
                    continue

                counts["in_bounds"] += 1
                hdr = mm[adder : adder + RD_HEADER_SIZE]
                if len(hdr) < RD_HEADER_SIZE or hdr[:2] != b"RD":
                    counts["no_rd_magic"] += 1
                    if len(bad) < sample_limit:
                        bad.append(
                            (idx, bitmapno, adder, size, width, height, "no_rd_magic")
                        )
                    continue

                counts["rd_magic"] += 1
                flag = hdr[2]
                flags[f"0x{flag:02x}"] += 1
                rd_width_u, rd_height_u, rd_size = struct.unpack_from("<III", hdr, 4)
                rd_width_s, rd_height_s = struct.unpack_from("<ii", hdr, 4)

                size_matches = rd_size == size
                dimension_bits_match = (
                    rd_width_u == (width & 0xFFFFFFFF)
                    and rd_height_u == (height & 0xFFFFFFFF)
                )
                signed_dims_match = rd_width_s == width and rd_height_s == height
                plausible_dims = 0 < width <= 16384 and 0 < height <= 16384

                counts["size_match" if size_matches else "size_mismatch"] += 1
                counts[
                    "dimension_bits_match"
                    if dimension_bits_match
                    else "dimension_bits_mismatch"
                ] += 1
                counts[
                    "signed_dimension_match"
                    if signed_dims_match
                    else "signed_dimension_mismatch"
                ] += 1
                counts[
                    "plausible_dimensions"
                    if plausible_dims
                    else "special_or_implausible_dimensions"
                ] += 1

                if flag == 0 and plausible_dims:
                    logical_size = RD_HEADER_SIZE + width * height
                    counts[
                        "uncompressed_logical_size_match"
                        if logical_size == size
                        else "uncompressed_logical_size_mismatch"
                    ] += 1
                    if not size_matches:
                        counts["flag0_rd_size_field_mismatch"] += 1
                elif flag == 1 and not size_matches:
                    counts["flag1_size_mismatch"] += 1

                reasons = []
                if not size_matches:
                    reasons.append("rd_size_field_mismatch")
                if not dimension_bits_match:
                    reasons.append("dimension_bits_mismatch")
                if not plausible_dims:
                    reasons.append("special_or_implausible_dimensions")
                if reasons and len(anomaly_samples) < sample_limit:
                    anomaly_samples.append(
                        (
                            idx,
                            bitmapno,
                            adder,
                            size,
                            width,
                            height,
                            flag,
                            rd_width_s,
                            rd_height_s,
                            rd_size,
                            ",".join(reasons),
                        )
                    )

                if len(samples) < sample_limit:
                    samples.append(
                        (
                            idx,
                            bitmapno,
                            adder,
                            size,
                            xoff,
                            yoff,
                            width,
                            height,
                            flag,
                            rd_width_s,
                            rd_height_s,
                            rd_size,
                        )
                    )
        finally:
            mm.close()

    return {
        "adrn_size": adrn_size,
        "real_size": real_size,
        "record_size": ADRN_RECORD_SIZE,
        "record_count": total,
        "remainder": remainder,
        "active_records": active,
        "duplicate_bitmap_numbers": duplicate_bitmap,
        "nondecreasing_active_offsets": nondecreasing,
        "contiguous_active_offsets": contiguous,
        "gap_transitions": gaps,
        "overlap_transitions": overlaps,
        "max_referenced_end": max_end,
        "unreferenced_real_tail": max(0, real_size - max_end),
        "counts": counts,
        "flags": flags,
        "samples": samples,
        "bad": bad,
        "anomaly_samples": anomaly_samples,
        "duplicate_samples": duplicate_samples,
    }


def analyze_maps(map_dir: Path, sample_limit: int = 16):
    files = sorted(
        (
            path
            for path in map_dir.rglob("*")
            if path.is_file() and path.suffix.lower() == ".map"
        ),
        key=lambda p: str(p.relative_to(map_dir)).lower(),
    )
    counts = collections.Counter()
    dims = collections.Counter()
    exact_examples = []
    bad_examples = []
    total_bytes = 0

    for path in files:
        size = path.stat().st_size
        total_bytes += size
        if size < 8:
            counts["too_small"] += 1
            if len(bad_examples) < sample_limit:
                bad_examples.append((str(path.relative_to(map_dir)), size, None, None, "too_small"))
            continue

        with path.open("rb") as f:
            head = f.read(8)

        width, height = struct.unpack("<II", head)
        plausible = 0 < width <= 10000 and 0 < height <= 10000
        expected = 8 + width * height * 2 if plausible else None

        if plausible:
            counts["plausible_dimensions"] += 1
            dims[(width, height)] += 1
        else:
            counts["implausible_dimensions"] += 1

        if expected == size:
            counts["exact_8_plus_whx2"] += 1
            if len(exact_examples) < sample_limit:
                exact_examples.append((str(path.relative_to(map_dir)), size, width, height))
        else:
            counts["layout_mismatch"] += 1
            if len(bad_examples) < sample_limit:
                bad_examples.append((str(path.relative_to(map_dir)), size, width, height, expected))

    return {
        "file_count": len(files),
        "total_bytes": total_bytes,
        "counts": counts,
        "top_dimensions": dims.most_common(30),
        "exact_examples": exact_examples,
        "bad_examples": bad_examples,
    }


def emit(real_adrn, maps):
    print("StoneAge recovered resource probe — R1")
    print("Original proprietary bytes are not included in this report.")
    print()
    print("REAL/ADRN")
    print(f"ADRN_BYTES|{real_adrn['adrn_size']}")
    print(f"REAL_BYTES|{real_adrn['real_size']}")
    print(f"ADRN_RECORD_SIZE|{real_adrn['record_size']}")
    print(f"ADRN_RECORD_COUNT|{real_adrn['record_count']}")
    print(f"ADRN_REMAINDER|{real_adrn['remainder']}")
    print(f"ACTIVE_RECORDS|{real_adrn['active_records']}")
    print(f"DUPLICATE_BITMAP_NUMBERS|{real_adrn['duplicate_bitmap_numbers']}")
    print(
        f"NONDECREASING_ACTIVE_OFFSETS|{real_adrn['nondecreasing_active_offsets']}"
    )
    print(f"CONTIGUOUS_ACTIVE_OFFSETS|{real_adrn['contiguous_active_offsets']}")
    print(f"GAP_TRANSITIONS|{real_adrn['gap_transitions']}")
    print(f"OVERLAP_TRANSITIONS|{real_adrn['overlap_transitions']}")
    print(f"MAX_REFERENCED_END|{real_adrn['max_referenced_end']}")
    print(f"UNREFERENCED_REAL_TAIL|{real_adrn['unreferenced_real_tail']}")

    for key in sorted(real_adrn["counts"]):
        print(f"ADRN_{key.upper()}|{real_adrn['counts'][key]}")
    for key, value in sorted(real_adrn["flags"].items()):
        print(f"RD_FLAG|{key}|{value}")

    print(
        "ADRN_SAMPLE|index|bitmapno|adder|size|xoff|yoff|adrn_w|adrn_h|"
        "flag|rd_w|rd_h|rd_size"
    )
    for row in real_adrn["samples"]:
        print("ADRN_SAMPLE|" + "|".join(map(str, row)))

    print("ADRN_BAD_SAMPLE|index|bitmapno|adder|size|w|h|reason")
    for row in real_adrn["bad"]:
        print("ADRN_BAD_SAMPLE|" + "|".join(map(str, row)))

    print(
        "ADRN_ANOMALY_SAMPLE|index|bitmapno|adder|adrn_size|adrn_w|adrn_h|"
        "flag|rd_w|rd_h|rd_size|reason"
    )
    for row in real_adrn["anomaly_samples"]:
        print("ADRN_ANOMALY_SAMPLE|" + "|".join(map(str, row)))

    print("ADRN_DUPLICATE_BITMAP_SAMPLE|index|bitmapno")
    for row in real_adrn["duplicate_samples"]:
        print("ADRN_DUPLICATE_BITMAP_SAMPLE|" + "|".join(map(str, row)))

    print()
    print("MAP")
    print(f"MAP_FILE_COUNT|{maps['file_count']}")
    print(f"MAP_TOTAL_BYTES|{maps['total_bytes']}")
    for key in sorted(maps["counts"]):
        print(f"MAP_{key.upper()}|{maps['counts'][key]}")
    for (width, height), count in maps["top_dimensions"]:
        print(f"MAP_DIMENSION|{width}|{height}|{count}")

    print("MAP_EXACT_SAMPLE|filename|bytes|width|height")
    for row in maps["exact_examples"]:
        print("MAP_EXACT_SAMPLE|" + "|".join(map(str, row)))

    print("MAP_BAD_SAMPLE|filename|bytes|width|height|expected")
    for row in maps["bad_examples"]:
        print("MAP_BAD_SAMPLE|" + "|".join(map(str, row)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--adrn", type=Path, required=True)
    parser.add_argument("--real", type=Path, required=True)
    parser.add_argument("--map-dir", type=Path, required=True)
    args = parser.parse_args()
    emit(
        analyze_real_adrn(args.adrn, args.real),
        analyze_maps(args.map_dir),
    )


if __name__ == "__main__":
    main()
