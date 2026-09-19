#!/usr/bin/env python3
"""Export deterministic Taiwan StoneAge v1.0 audio provenance metadata.

Consumes the accepted retail disc transiently and emits only structural/hash metadata.
No WAV or sound-container payload bytes are retained.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import struct
import tempfile

from tools.stoneage_tw10_technical_probe import find_rows, extract_row, parse_addr_table

TARGET_FILES = (
    "StoneAge/data/sound_1.bin",
    "StoneAge/data/soundaddr_1.txt",
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_wave(data: bytes):
    out = {
        "riff": 0,
        "wave": 0,
        "audio_format": "",
        "channels": "",
        "sample_rate": "",
        "byte_rate": "",
        "block_align": "",
        "bits_per_sample": "",
        "data_size": "",
        "data_sha256": "",
        "chunk_signature": "",
    }
    if len(data) < 12 or data[:4] != b"RIFF" or data[8:12] != b"WAVE":
        return out

    out["riff"] = 1
    out["wave"] = 1
    chunks = []
    pos = 12
    while pos + 8 <= len(data):
        cid = data[pos:pos + 4]
        size = struct.unpack_from("<I", data, pos + 4)[0]
        start = pos + 8
        end = start + size
        if end > len(data):
            chunks.append(f"{cid.decode('ascii', 'replace')}:{size}:truncated")
            break
        name = cid.decode("ascii", "replace")
        chunks.append(f"{name}:{size}")
        if cid == b"fmt " and size >= 16:
            vals = struct.unpack_from("<HHIIHH", data, start)
            (
                out["audio_format"],
                out["channels"],
                out["sample_rate"],
                out["byte_rate"],
                out["block_align"],
                out["bits_per_sample"],
            ) = vals
        elif cid == b"data":
            payload = data[start:end]
            out["data_size"] = size
            out["data_sha256"] = sha256_bytes(payload)
        pos = end + (size & 1)

    out["chunk_signature"] = ",".join(chunks)
    return out


def wave_fields(prefix: str, wave: dict) -> list[str]:
    keys = (
        "riff", "wave", "audio_format", "channels", "sample_rate",
        "byte_rate", "block_align", "bits_per_sample", "data_size",
        "data_sha256", "chunk_signature",
    )
    return [f"{prefix}_{key}={wave.get(key, '')}" for key in keys]


def sanitize(value) -> str:
    return str(value).replace("|", "%7C").replace("\n", " ").replace("\r", " ")


def row_bytes(img, row) -> bytes:
    return b"".join(img.iter_extent(row["lba"], row["size"]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bin", required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    img, rows, layout, joliet = find_rows(args.bin)
    td = tempfile.TemporaryDirectory()
    root = Path(td.name)
    try:
        by_path = {r["path"]: r for r in rows if not r["is_dir"]}
        for target in TARGET_FILES:
            row = by_path.get(target)
            if row is None:
                raise SystemExit(f"missing required audio resource: {target}")
            extract_row(img, row, root / target)

        table = parse_addr_table(root / "StoneAge/data/soundaddr_1.txt")
        container = (root / "StoneAge/data/sound_1.bin").read_bytes()
        loose_rows = sorted(
            [
                r for r in rows
                if not r["is_dir"] and r["path"].startswith("StoneAge/data/se/")
                and r["path"].lower().endswith(".wav")
            ],
            key=lambda r: r["path"].lower(),
        )
        bgm_rows = sorted(
            [
                r for r in rows
                if not r["is_dir"] and r["path"].startswith("StoneAge/data/bgm/")
                and r["path"].lower().endswith(".wav")
            ],
            key=lambda r: r["path"].lower(),
        )
        loose_by_name = {Path(r["path"]).name.lower(): r for r in loose_rows}
        indexed_names = {Path(name).name.lower() for _, _, name in table}

        args.out.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            "StoneAge Taiwan v1.0 audio reconstruction crosswalk — R1",
            f"SCOPE|accepted-retail-disc|derived-metadata-only|no-payload|layout={layout}|joliet={int(joliet)}",
            f"SOURCE|path=StoneAge/data/sound_1.bin|bytes={len(container)}|sha256={sha256_bytes(container)}",
            (
                "SOURCE|path=StoneAge/data/soundaddr_1.txt|"
                f"bytes={(root / 'StoneAge/data/soundaddr_1.txt').stat().st_size}|"
                f"sha256={sha256_file(root / 'StoneAge/data/soundaddr_1.txt')}"
            ),
        ]

        exact = 0
        same_payload = 0
        payload_diff = 0
        missing_loose = 0
        prev_end = 0

        for index, (offset, size, name) in enumerate(table):
            if offset != prev_end:
                raise ValueError(f"non-contiguous sound container at record {index}")
            if offset < 0 or size < 0 or offset + size > len(container):
                raise ValueError(f"sound container bounds error at record {index}")
            segment = container[offset:offset + size]
            prev_end = offset + size

            key = Path(name).name.lower()
            loose_row = loose_by_name.get(key)
            if loose_row is None:
                relation = "missing_loose"
                missing_loose += 1
                loose_data = b""
                loose_path = ""
                loose_size = ""
                loose_sha = ""
                loose_wave = parse_wave(b"")
            else:
                loose_data = row_bytes(img, loose_row)
                loose_path = loose_row["path"]
                loose_size = len(loose_data)
                loose_sha = sha256_bytes(loose_data)
                loose_wave = parse_wave(loose_data)
                if segment == loose_data:
                    relation = "exact_file"
                    exact += 1
                else:
                    seg_wave_for_relation = parse_wave(segment)
                    if (
                        seg_wave_for_relation["data_sha256"]
                        and seg_wave_for_relation["data_sha256"] == loose_wave["data_sha256"]
                    ):
                        relation = "variant_same_pcm"
                        same_payload += 1
                    else:
                        relation = "variant_pcm_diff"
                        payload_diff += 1

            seg_wave = parse_wave(segment)
            fields = [
                "INDEXED",
                f"index={index}",
                f"offset={offset}",
                f"size={size}",
                f"name={sanitize(Path(name).name)}",
                f"container_sha256={sha256_bytes(segment)}",
                f"loose_path={sanitize(loose_path)}",
                f"loose_size={loose_size}",
                f"loose_sha256={loose_sha}",
                f"relation={relation}",
            ]
            fields += wave_fields("container", seg_wave)
            fields += wave_fields("loose", loose_wave)
            lines.append("|".join(fields))

        if prev_end != len(container):
            raise ValueError(f"sound container tail remains: {len(container) - prev_end}")

        unindexed = [r for r in loose_rows if Path(r["path"]).name.lower() not in indexed_names]
        for row in unindexed:
            data = row_bytes(img, row)
            wave = parse_wave(data)
            fields = [
                "UNINDEXED_SFX",
                f"name={sanitize(Path(row['path']).name)}",
                f"path={sanitize(row['path'])}",
                f"size={len(data)}",
                f"sha256={sha256_bytes(data)}",
            ] + wave_fields("wave", wave)
            lines.append("|".join(fields))

        for row in bgm_rows:
            data = row_bytes(img, row)
            wave = parse_wave(data)
            fields = [
                "BGM",
                f"name={sanitize(Path(row['path']).name)}",
                f"path={sanitize(row['path'])}",
                f"size={len(data)}",
                f"sha256={sha256_bytes(data)}",
            ] + wave_fields("wave", wave)
            lines.append("|".join(fields))

        lines.insert(
            4,
            (
                f"SUMMARY|indexed={len(table)}|loose_sfx={len(loose_rows)}|bgm={len(bgm_rows)}|"
                f"exact_file={exact}|variant_same_pcm={same_payload}|"
                f"variant_pcm_diff={payload_diff}|missing_loose={missing_loose}|"
                f"unindexed_sfx={len(unindexed)}|container_bytes={len(container)}"
            ),
        )
        args.out.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
        print("\n".join(lines[:5]))
    finally:
        img.close()
        td.cleanup()


if __name__ == "__main__":
    main()
