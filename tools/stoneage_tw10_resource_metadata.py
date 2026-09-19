#!/usr/bin/env python3
"""Export deterministic Taiwan StoneAge v1.0 graphics/animation metadata.

Consumes the accepted raw CD image transiently and writes only derived metadata.
No REAL/SPR/ADRN/SPRADRN payload bytes are retained.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import mmap
from pathlib import Path
import struct
import tempfile

from tools.stoneage_tw10_technical_probe import find_rows, extract_row

ADRN_RECORD_SIZE = 80
SPRADRN_RECORD_SIZE = 12
ANIM_HEADER_SIZE = 12
FRAME_SIZE = 10
SENTINEL_BITMAP = 0xFFFFFFFF

TARGETS = (
    "StoneAge/data/adrn_1.bin",
    "StoneAge/data/real_1.bin",
    "StoneAge/data/spradrn_1.bin",
    "StoneAge/data/spr_1.bin",
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


class DeterministicGzipTsv:
    def __init__(self, path: Path):
        self.path = path
        self.raw = None
        self.gz = None
        self.text = None

    def __enter__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.raw = self.path.open("wb")
        self.gz = gzip.GzipFile(
            filename="", mode="wb", fileobj=self.raw, compresslevel=9, mtime=0
        )
        self.text = io.TextIOWrapper(self.gz, encoding="utf-8", newline="\n")
        return self.text

    def __exit__(self, exc_type, exc, tb):
        if self.text is not None:
            self.text.flush()
            self.text.detach()
        if self.gz is not None:
            self.gz.close()
        if self.raw is not None:
            self.raw.close()


def parse_adrn_record(rec: bytes):
    if len(rec) != ADRN_RECORD_SIZE:
        raise ValueError("ADRN record must be 80 bytes")
    bitmapno, adder, size, xoff, yoff, width, height = struct.unpack_from(
        "<IIIiiii", rec, 0
    )
    return {
        "bitmapno": bitmapno,
        "adder": adder,
        "size": size,
        "xoff": xoff,
        "yoff": yoff,
        "width": width,
        "height": height,
        "attr_sha256": hashlib.sha256(rec[28:]).hexdigest(),
    }


def export_adrn(adrn_path: Path, real_path: Path, out_path: Path):
    adrn_size = adrn_path.stat().st_size
    real_size = real_path.stat().st_size
    if adrn_size % ADRN_RECORD_SIZE:
        raise ValueError("ADRN length is not divisible by 80")

    record_count = adrn_size // ADRN_RECORD_SIZE
    bitmap_seen = set()
    max_end = 0
    contiguous = 0
    prev_end = None
    flag_counts = {}
    special_dimensions = 0

    with adrn_path.open("rb") as af, real_path.open("rb") as rf, DeterministicGzipTsv(out_path) as out:
        mm = mmap.mmap(rf.fileno(), 0, access=mmap.ACCESS_READ)
        try:
            out.write(
                "index\tbitmapno\tadder\tsize\txoff\tyoff\twidth\theight\trd_flag\t"
                "rd_width\trd_height\trd_size_field\tattr_sha256\trd_block_sha256\n"
            )
            for index in range(record_count):
                rec = af.read(ADRN_RECORD_SIZE)
                row = parse_adrn_record(rec)
                bitmapno = row["bitmapno"]
                if bitmapno in bitmap_seen:
                    raise ValueError(f"duplicate v1.0 bitmap number: {bitmapno}")
                bitmap_seen.add(bitmapno)

                adder = row["adder"]
                size = row["size"]
                if size < 16 or adder + size > real_size:
                    raise ValueError(f"REAL span out of bounds at ADRN index {index}")
                block = mm[adder:adder + size]
                if block[:2] != b"RD":
                    raise ValueError(f"missing RD magic at ADRN index {index}")

                rd_flag = block[2]
                rd_width, rd_height, rd_size = struct.unpack_from("<iiI", block, 4)
                if rd_width != row["width"] or rd_height != row["height"]:
                    raise ValueError(f"RD/ADRN dimension mismatch at index {index}")
                if not (0 < row["width"] <= 16384 and 0 < row["height"] <= 16384):
                    special_dimensions += 1

                flag_counts[rd_flag] = flag_counts.get(rd_flag, 0) + 1
                if prev_end is not None:
                    if adder != prev_end:
                        raise ValueError(f"non-contiguous REAL span at ADRN index {index}")
                    contiguous += 1
                prev_end = adder + size
                max_end = max(max_end, prev_end)

                out.write(
                    f"{index}\t{bitmapno}\t{adder}\t{size}\t{row['xoff']}\t{row['yoff']}\t"
                    f"{row['width']}\t{row['height']}\t{rd_flag}\t{rd_width}\t{rd_height}\t"
                    f"{rd_size}\t{row['attr_sha256']}\t{hashlib.sha256(block).hexdigest()}\n"
                )
        finally:
            mm.close()

    if max_end != real_size:
        raise ValueError(f"REAL coverage incomplete: {max_end} != {real_size}")
    return {
        "records": record_count,
        "bitmapnos": len(bitmap_seen),
        "contiguous_transitions": contiguous,
        "real_bytes": real_size,
        "special_dimensions": special_dimensions,
        "flag_counts": flag_counts,
    }


def parse_spreadrn_record(rec: bytes):
    if len(rec) != SPRADRN_RECORD_SIZE:
        raise ValueError("SPRADRN record must be 12 bytes")
    spr_no, offset, anim_size, reserved = struct.unpack("<IIHH", rec)
    return spr_no, offset, anim_size, reserved


def export_spr(
    spreadrn_path: Path,
    spr_path: Path,
    group_out: Path,
    animation_out: Path,
    frame_out: Path,
):
    index_data = spreadrn_path.read_bytes()
    if len(index_data) % SPRADRN_RECORD_SIZE:
        raise ValueError("SPRADRN length is not divisible by 12")
    rows = [
        parse_spreadrn_record(index_data[i:i + SPRADRN_RECORD_SIZE])
        for i in range(0, len(index_data), SPRADRN_RECORD_SIZE)
    ]
    spr = spr_path.read_bytes()
    spr_size = len(spr)
    animation_total = 0
    frame_total = 0
    sentinel_total = 0
    exact_group_spans = 0

    with (
        DeterministicGzipTsv(group_out) as groups,
        DeterministicGzipTsv(animation_out) as animations,
        DeterministicGzipTsv(frame_out) as frames,
    ):
        groups.write(
            "index\tspr_no\toffset\tanim_count\treserved\tend_offset\tnext_offset\t"
            "segment_sha256\n"
        )
        animations.write(
            "group_index\tspr_no\tanim_index\toffset\tdirection\tanim_no\tduration\t"
            "frame_count\tend_offset\n"
        )
        frames.write(
            "group_index\tspr_no\tanim_index\tframe_index\toffset\tbmp_no\tpos_x\t"
            "pos_y\tsound_no\tsentinel\n"
        )

        for group_index, (spr_no, offset, anim_count, reserved) in enumerate(rows):
            next_offset = rows[group_index + 1][1] if group_index + 1 < len(rows) else spr_size
            if not (0 <= offset <= next_offset <= spr_size):
                raise ValueError(f"invalid SPR group span at index {group_index}")
            cursor = offset

            for anim_index in range(anim_count):
                anim_offset = cursor
                if cursor + ANIM_HEADER_SIZE > spr_size:
                    raise ValueError(f"truncated animation header at group {group_index}")
                direction, anim_no, duration, frame_count = struct.unpack_from(
                    "<HHII", spr, cursor
                )
                cursor += ANIM_HEADER_SIZE
                animation_total += 1

                for frame_index in range(frame_count):
                    frame_offset = cursor
                    if cursor + FRAME_SIZE > spr_size:
                        raise ValueError(f"truncated frame at group {group_index}")
                    bmp_no, pos_x, pos_y, sound_no = struct.unpack_from(
                        "<IhhH", spr, cursor
                    )
                    sentinel = int(bmp_no == SENTINEL_BITMAP)
                    sentinel_total += sentinel
                    frames.write(
                        f"{group_index}\t{spr_no}\t{anim_index}\t{frame_index}\t"
                        f"{frame_offset}\t{bmp_no}\t{pos_x}\t{pos_y}\t{sound_no}\t{sentinel}\n"
                    )
                    frame_total += 1
                    cursor += FRAME_SIZE

                animations.write(
                    f"{group_index}\t{spr_no}\t{anim_index}\t{anim_offset}\t{direction}\t"
                    f"{anim_no}\t{duration}\t{frame_count}\t{cursor}\n"
                )

            if cursor != next_offset:
                raise ValueError(
                    f"SPR group {group_index} does not end at next offset: {cursor} != {next_offset}"
                )
            exact_group_spans += 1
            groups.write(
                f"{group_index}\t{spr_no}\t{offset}\t{anim_count}\t{reserved}\t{cursor}\t"
                f"{next_offset}\t{hashlib.sha256(spr[offset:next_offset]).hexdigest()}\n"
            )

    return {
        "groups": len(rows),
        "animations": animation_total,
        "frames": frame_total,
        "sentinel_frames": sentinel_total,
        "exact_group_spans": exact_group_spans,
        "spr_bytes": spr_size,
    }


def write_manifest(out_dir: Path, source_paths: dict[str, Path], metrics: dict):
    manifest = out_dir / "MANIFEST-R1.txt"
    lines = [
        "StoneAge Taiwan v1.0 resource metadata export — R1",
        "SCOPE|accepted-retail-disc|derived-metadata-only|no-proprietary-payload",
    ]
    for name in sorted(source_paths):
        path = source_paths[name]
        lines.append(
            f"SOURCE|name={name}|bytes={path.stat().st_size}|sha256={sha256_file(path)}"
        )
    for key in sorted(metrics):
        lines.append(f"METRIC|{key}|{metrics[key]}")
    for path in sorted(out_dir.glob("*.tsv.gz")):
        lines.append(
            f"DATASET|name={path.name}|bytes={path.stat().st_size}|sha256={sha256_file(path)}"
        )
    manifest.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return manifest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bin", required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    args = ap.parse_args()

    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    img, rows, layout, joliet = find_rows(args.bin)
    td = tempfile.TemporaryDirectory()
    root = Path(td.name)
    try:
        by_path = {row["path"]: row for row in rows if not row["is_dir"]}
        paths = {}
        for target in TARGETS:
            row = by_path.get(target)
            if row is None:
                raise SystemExit(f"required resource missing: {target}")
            out = root / Path(target).name
            extract_row(img, row, out)
            paths[Path(target).name] = out

        adrn_metrics = export_adrn(
            paths["adrn_1.bin"],
            paths["real_1.bin"],
            out_dir / "ADRN-R1.tsv.gz",
        )
        spr_metrics = export_spr(
            paths["spradrn_1.bin"],
            paths["spr_1.bin"],
            out_dir / "SPR-GROUP-R1.tsv.gz",
            out_dir / "SPR-ANIMATION-R1.tsv.gz",
            out_dir / "SPR-FRAME-R1.tsv.gz",
        )
        metrics = {
            "filesystem_layout": layout,
            "joliet": int(joliet),
            **{f"adrn_{k}": v for k, v in adrn_metrics.items() if k != "flag_counts"},
            **{f"spr_{k}": v for k, v in spr_metrics.items()},
        }
        for flag, count in sorted(adrn_metrics["flag_counts"].items()):
            metrics[f"adrn_rd_flag_0x{flag:02x}"] = count

        manifest = write_manifest(out_dir, paths, metrics)
        print(manifest.read_text("utf-8"), end="")
    finally:
        img.close()
        td.cleanup()


if __name__ == "__main__":
    main()
