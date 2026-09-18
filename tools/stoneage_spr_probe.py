#!/usr/bin/env python3
"""Read-only structural validator for StoneAge SPR/SPRADRN animation resources."""

import argparse
import collections
import hashlib
import struct
from pathlib import Path

SPRADRN_RECORD_SIZE = 12
ANIM_HEADER_SIZE = 12
FRAME_SIZE = 10
ADRN_RECORD_SIZE = 80
SPRSTART = 100000
SENTINEL_BITMAP = 0xFFFFFFFF


def load_spreadrn(path: Path):
    data = path.read_bytes()
    count = len(data) // SPRADRN_RECORD_SIZE
    rem = len(data) % SPRADRN_RECORD_SIZE
    rows = []
    for i in range(count):
        spr_no, offset, anim_size = struct.unpack_from(
            "<IIH", data, i * SPRADRN_RECORD_SIZE
        )
        rows.append(
            {
                "index": i,
                "spr_no": spr_no,
                "offset": offset,
                "anim_size": anim_size,
            }
        )
    return rows, rem


def load_adrn_bitmapnos(path: Path):
    data = path.read_bytes()
    if len(data) % ADRN_RECORD_SIZE:
        raise ValueError("ADRN length is not a multiple of 80")
    values = []
    for off in range(0, len(data), ADRN_RECORD_SIZE):
        values.append(struct.unpack_from("<I", data, off)[0])
    return set(values), len(values)


def analyze(
    spreadrn_path: Path,
    spr_path: Path,
    adrn_path: Path | None = None,
    sample_limit: int = 20,
):
    rows, remainder = load_spreadrn(spreadrn_path)
    spr_size = spr_path.stat().st_size
    counts = collections.Counter()
    dirs = collections.Counter()
    anim_nos = collections.Counter()
    sound_classes = collections.Counter()
    bitmap_classes = collections.Counter()
    failures = []
    samples = []
    boundaries = []
    sentinel_samples = []
    unresolved_bitmap_samples = []
    frame_bmp_min = None
    frame_bmp_max = None
    frame_total = 0
    animation_total = 0

    adrn_bitmapnos = None
    adrn_record_count = None
    if adrn_path is not None:
        adrn_bitmapnos, adrn_record_count = load_adrn_bitmapnos(adrn_path)

    sorted_by_offset = sorted(rows, key=lambda r: (r["offset"], r["index"]))
    next_offset = {}
    for a, b in zip(sorted_by_offset, sorted_by_offset[1:]):
        next_offset[a["index"]] = b["offset"]
    if sorted_by_offset:
        next_offset[sorted_by_offset[-1]["index"]] = spr_size

    with spr_path.open("rb") as f:
        for rec in rows:
            idx = rec["index"]
            off = rec["offset"]
            anim_count = rec["anim_size"]

            if rec["spr_no"] < SPRSTART:
                counts["sprno_below_sprstart"] += 1
            else:
                counts["sprno_at_or_above_sprstart"] += 1

            if off > spr_size:
                counts["offset_out_of_bounds"] += 1
                if len(failures) < sample_limit:
                    failures.append(
                        (idx, rec["spr_no"], off, anim_count, "offset_out_of_bounds")
                    )
                continue

            f.seek(off)
            ok = True
            local_frames = 0
            local_anims = 0
            cursor = off
            try:
                for anim_idx in range(anim_count):
                    hdr = f.read(ANIM_HEADER_SIZE)
                    if len(hdr) != ANIM_HEADER_SIZE:
                        raise ValueError("truncated_anim_header")
                    direction, anim_no, duration, frame_count = struct.unpack(
                        "<HHII", hdr
                    )
                    cursor += ANIM_HEADER_SIZE
                    local_anims += 1
                    animation_total += 1
                    dirs[direction] += 1
                    anim_nos[anim_no] += 1

                    remaining = spr_size - cursor
                    need = frame_count * FRAME_SIZE
                    if need > remaining:
                        raise ValueError(f"frame_span_out_of_bounds:{frame_count}")

                    for frame_idx in range(frame_count):
                        raw = f.read(FRAME_SIZE)
                        if len(raw) != FRAME_SIZE:
                            raise ValueError("truncated_frame")
                        bmp_no, pos_x, pos_y, sound_no = struct.unpack("<IhhH", raw)
                        cursor += FRAME_SIZE
                        local_frames += 1
                        frame_total += 1
                        frame_bmp_min = (
                            bmp_no if frame_bmp_min is None else min(frame_bmp_min, bmp_no)
                        )
                        frame_bmp_max = (
                            bmp_no if frame_bmp_max is None else max(frame_bmp_max, bmp_no)
                        )

                        if bmp_no == SENTINEL_BITMAP:
                            bitmap_classes["sentinel_ffffffff"] += 1
                            if len(sentinel_samples) < sample_limit:
                                sentinel_samples.append(
                                    (
                                        idx,
                                        rec["spr_no"],
                                        anim_idx,
                                        frame_idx,
                                        bmp_no,
                                        pos_x,
                                        pos_y,
                                        sound_no,
                                    )
                                )
                        elif adrn_bitmapnos is None:
                            bitmap_classes["not_crosschecked"] += 1
                        elif bmp_no in adrn_bitmapnos:
                            bitmap_classes["direct_adrn_bitmap_match"] += 1
                        else:
                            bitmap_classes["not_in_adrn_bitmap_set"] += 1
                            if len(unresolved_bitmap_samples) < sample_limit:
                                unresolved_bitmap_samples.append(
                                    (
                                        idx,
                                        rec["spr_no"],
                                        anim_idx,
                                        frame_idx,
                                        bmp_no,
                                    )
                                )

                        if sound_no < 10000:
                            sound_classes["sound_lt_10000"] += 1
                        elif sound_no < 10100:
                            sound_classes["effect_10000_10099"] += 1
                        else:
                            sound_classes["effect_ge_10100"] += 1
            except Exception as exc:
                ok = False
                counts["parse_failure"] += 1
                if len(failures) < sample_limit:
                    failures.append((idx, rec["spr_no"], off, anim_count, str(exc)))

            if ok:
                counts["parse_success"] += 1
                nxt = next_offset.get(idx, spr_size)
                if cursor == nxt:
                    counts["exact_next_offset"] += 1
                    relation = "exact"
                elif cursor < nxt:
                    counts["gap_before_next"] += 1
                    relation = f"gap:{nxt-cursor}"
                else:
                    counts["overlap_next"] += 1
                    relation = f"overlap:{cursor-nxt}"

                boundaries.append((idx, rec["spr_no"], off, cursor, nxt, relation))
                if len(samples) < sample_limit:
                    samples.append(
                        (
                            idx,
                            rec["spr_no"],
                            off,
                            anim_count,
                            local_anims,
                            local_frames,
                            cursor,
                            nxt,
                            relation,
                        )
                    )

    sprnos = [r["spr_no"] for r in rows]
    offsets = [r["offset"] for r in rows]
    sprno_groups = collections.defaultdict(list)
    offset_groups = collections.defaultdict(list)
    for rec in rows:
        sprno_groups[rec["spr_no"]].append(rec["index"])
        offset_groups[rec["offset"]].append(rec["index"])
    duplicate_sprno_groups = [
        (value, tuple(indices))
        for value, indices in sorted(sprno_groups.items())
        if len(indices) > 1
    ]
    duplicate_offset_groups = [
        (value, tuple(indices))
        for value, indices in sorted(offset_groups.items())
        if len(indices) > 1
    ]

    monotonic_offsets = sum(1 for a, b in zip(offsets, offsets[1:]) if b >= a)

    agg = hashlib.sha256()
    for row in boundaries:
        agg.update(("|".join(map(str, row)) + "\n").encode("ascii"))

    return {
        "spreadrn_bytes": spreadrn_path.stat().st_size,
        "spr_bytes": spr_size,
        "record_size": SPRADRN_RECORD_SIZE,
        "record_count": len(rows),
        "remainder": remainder,
        "sprno_min": min(sprnos) if sprnos else None,
        "sprno_max": max(sprnos) if sprnos else None,
        "offset_min": min(offsets) if offsets else None,
        "offset_max": max(offsets) if offsets else None,
        "duplicate_sprnos": len(sprnos) - len(set(sprnos)),
        "duplicate_offsets": len(offsets) - len(set(offsets)),
        "duplicate_sprno_groups": duplicate_sprno_groups,
        "duplicate_offset_groups": duplicate_offset_groups,
        "monotonic_offset_transitions": monotonic_offsets,
        "animation_total": animation_total,
        "frame_total": frame_total,
        "frame_bmp_min": frame_bmp_min,
        "frame_bmp_max": frame_bmp_max,
        "adrn_record_count": adrn_record_count,
        "counts": counts,
        "dirs": dirs,
        "anim_nos": anim_nos,
        "sound_classes": sound_classes,
        "bitmap_classes": bitmap_classes,
        "sentinel_samples": sentinel_samples,
        "unresolved_bitmap_samples": unresolved_bitmap_samples,
        "samples": samples,
        "failures": failures,
        "aggregate": agg.hexdigest(),
    }


def emit(r, sample_limit=20):
    print("StoneAge recovered SPR/SPRADRN probe — R2")
    print("No proprietary animation payload bytes are stored in this report.")
    for key in [
        "spreadrn_bytes",
        "spr_bytes",
        "record_size",
        "record_count",
        "remainder",
        "sprno_min",
        "sprno_max",
        "offset_min",
        "offset_max",
        "duplicate_sprnos",
        "duplicate_offsets",
        "monotonic_offset_transitions",
        "animation_total",
        "frame_total",
        "frame_bmp_min",
        "frame_bmp_max",
        "adrn_record_count",
    ]:
        print(f"{key.upper()}|{r[key]}")
    for k in sorted(r["counts"]):
        print(f"COUNT|{k}|{r['counts'][k]}")
    for k, v in sorted(r["bitmap_classes"].items()):
        print(f"BITMAP_CLASS|{k}|{v}")
    for k, v in sorted(r["sound_classes"].items()):
        print(f"SOUND_CLASS|{k}|{v}")
    for k, v in sorted(r["dirs"].items()):
        print(f"DIRECTION|{k}|{v}")
    print("TOP_ANIM_NO|anim_no|count")
    for k, v in r["anim_nos"].most_common(30):
        print(f"TOP_ANIM_NO|{k}|{v}")
    print(f"AGGREGATE_BOUNDARY_SHA256|{r['aggregate']}")

    print("DUPLICATE_SPRNO|spr_no|record_indices")
    for value, indices in r["duplicate_sprno_groups"][:sample_limit]:
        print(f"DUPLICATE_SPRNO|{value}|{','.join(map(str, indices))}")
    print("DUPLICATE_OFFSET|offset|record_indices")
    for value, indices in r["duplicate_offset_groups"][:sample_limit]:
        print(f"DUPLICATE_OFFSET|{value}|{','.join(map(str, indices))}")

    print(
        "SPR_SAMPLE|index|spr_no|offset|anim_size|parsed_anims|parsed_frames|"
        "end|next_offset|relation"
    )
    for row in r["samples"][:sample_limit]:
        print("SPR_SAMPLE|" + "|".join(map(str, row)))

    print("SENTINEL_FRAME|record_index|spr_no|anim_index|frame_index|bmp_no|pos_x|pos_y|sound_no")
    for row in r["sentinel_samples"][:sample_limit]:
        print("SENTINEL_FRAME|" + "|".join(map(str, row)))

    print("UNRESOLVED_BITMAP|record_index|spr_no|anim_index|frame_index|bmp_no")
    for row in r["unresolved_bitmap_samples"][:sample_limit]:
        print("UNRESOLVED_BITMAP|" + "|".join(map(str, row)))

    print("SPR_FAILURE|index|spr_no|offset|anim_size|reason")
    for row in r["failures"][:sample_limit]:
        print("SPR_FAILURE|" + "|".join(map(str, row)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spradrn", type=Path, required=True)
    ap.add_argument("--spr", type=Path, required=True)
    ap.add_argument("--adrn", type=Path)
    args = ap.parse_args()
    result = analyze(args.spradrn, args.spr, args.adrn)
    emit(result)
    if result["remainder"] or result["failures"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
