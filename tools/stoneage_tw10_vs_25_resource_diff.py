#!/usr/bin/env python3
"""Direct Taiwan v1.0 -> preserved 2.5 resource inheritance diff.

Consumes verified transient files and emits derived comparison metrics only.
No proprietary resource bytes are committed.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import struct
import tempfile

from tools.stoneage_spr_probe import load_spreadrn
from tools.stoneage_tw10_technical_probe import find_rows, extract_row

ADRN_RECORD_SIZE = 80
TW_TARGETS = (
    "StoneAge/data/adrn_1.bin",
    "StoneAge/data/real_1.bin",
    "StoneAge/data/spradrn_1.bin",
    "StoneAge/data/spr_1.bin",
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def common_prefix_bytes(a: bytes, b: bytes) -> int:
    n = min(len(a), len(b))
    block = 1024 * 1024
    pos = 0
    while pos + block <= n and a[pos:pos+block] == b[pos:pos+block]:
        pos += block
    while pos < n and a[pos] == b[pos]:
        pos += 1
    return pos


def parse_adrn(path: Path):
    data = path.read_bytes()
    if len(data) % ADRN_RECORD_SIZE:
        raise ValueError("ADRN length is not a multiple of 80")
    rows = []
    for idx, off in enumerate(range(0, len(data), ADRN_RECORD_SIZE)):
        raw = data[off:off+ADRN_RECORD_SIZE]
        bitmapno, adder, size, xoff, yoff, width, height = struct.unpack_from("<IIIiiii", raw, 0)
        rows.append({
            "index": idx,
            "bitmapno": bitmapno,
            "adder": adder,
            "size": size,
            "xoff": xoff,
            "yoff": yoff,
            "width": width,
            "height": height,
            "raw": raw,
        })
    return rows


def segment(real: bytes, row):
    return real[row["adder"]:row["adder"] + row["size"]]


def compare_adrn(tw_adrn: Path, tw_real: Path, v25_adrn: Path, v25_real: Path):
    tw_rows = parse_adrn(tw_adrn)
    v_rows = parse_adrn(v25_adrn)
    tw_real_b = tw_real.read_bytes()
    v_real_b = v25_real.read_bytes()

    prefix_records = 0
    for a, b in zip(tw_rows, v_rows):
        if a["raw"] != b["raw"]:
            break
        prefix_records += 1

    v_by_bitmap = {}
    duplicates = set()
    for row in v_rows:
        if row["bitmapno"] in v_by_bitmap:
            duplicates.add(row["bitmapno"])
        else:
            v_by_bitmap[row["bitmapno"]] = row

    exact_raw = same_geometry = payload_equal = missing = 0
    changed_samples = []
    for a in tw_rows:
        b = v_by_bitmap.get(a["bitmapno"])
        if b is None:
            missing += 1
            if len(changed_samples) < 20:
                changed_samples.append((a["bitmapno"], "missing", a["index"], -1, a["size"], -1))
            continue
        if a["raw"] == b["raw"]:
            exact_raw += 1
        if (a["xoff"], a["yoff"], a["width"], a["height"]) == (
            b["xoff"], b["yoff"], b["width"], b["height"]
        ):
            same_geometry += 1
        equal_payload = segment(tw_real_b, a) == segment(v_real_b, b)
        if equal_payload:
            payload_equal += 1
        elif len(changed_samples) < 20:
            changed_samples.append(
                (a["bitmapno"], "payload_changed", a["index"], b["index"], a["size"], b["size"])
            )

    print(
        f"ADRN_DIFF|tw_records={len(tw_rows)}|v25_records={len(v_rows)}|"
        f"exact_prefix_records={prefix_records}|exact_raw_by_bitmap={exact_raw}|"
        f"same_geometry_by_bitmap={same_geometry}|payload_equal_by_bitmap={payload_equal}|"
        f"missing_in_v25={missing}|v25_duplicate_bitmapnos={len(duplicates)}"
    )
    print(
        f"REAL_DIFF|tw_bytes={len(tw_real_b)}|v25_bytes={len(v_real_b)}|"
        f"common_prefix_bytes={common_prefix_bytes(tw_real_b,v_real_b)}"
    )
    for bitmapno, kind, ai, bi, asz, bsz in changed_samples:
        print(
            f"ADRN_CHANGE_SAMPLE|bitmapno={bitmapno}|kind={kind}|tw_index={ai}|v25_index={bi}|"
            f"tw_size={asz}|v25_size={bsz}"
        )


def spr_segments(spreadrn_path: Path, spr_path: Path):
    rows, rem = load_spreadrn(spreadrn_path)
    if rem:
        raise ValueError("SPRADRN remainder")
    data = spr_path.read_bytes()
    by_offset = sorted(rows, key=lambda r:(r["offset"], r["index"]))
    next_offset = {}
    for a, b in zip(by_offset, by_offset[1:]):
        next_offset[a["index"]] = b["offset"]
    if by_offset:
        next_offset[by_offset[-1]["index"]] = len(data)
    out=[]
    for row in rows:
        end=next_offset[row["index"]]
        out.append({**row, "raw_segment":data[row["offset"]:end]})
    return out, data


def compare_spr(tw_spreadrn: Path, tw_spr: Path, v_spreadrn: Path, v_spr: Path):
    tw_rows, tw_data = spr_segments(tw_spreadrn, tw_spr)
    v_rows, v_data = spr_segments(v_spreadrn, v_spr)

    prefix_records=0
    for a,b in zip(tw_rows,v_rows):
        if (a["spr_no"],a["offset"],a["anim_size"],a["raw_segment"]) != (
            b["spr_no"],b["offset"],b["anim_size"],b["raw_segment"]
        ):
            break
        prefix_records += 1

    v_by_no={}
    duplicates=set()
    for row in v_rows:
        if row["spr_no"] in v_by_no:
            duplicates.add(row["spr_no"])
        else:
            v_by_no[row["spr_no"]]=row

    same_header=segment_equal=missing=0
    samples=[]
    for a in tw_rows:
        b=v_by_no.get(a["spr_no"])
        if b is None:
            missing += 1
            if len(samples)<20:
                samples.append((a["spr_no"],"missing",a["index"],-1,len(a["raw_segment"]),-1))
            continue
        if a["anim_size"] == b["anim_size"]:
            same_header += 1
        if a["raw_segment"] == b["raw_segment"]:
            segment_equal += 1
        elif len(samples)<20:
            samples.append(
                (a["spr_no"],"segment_changed",a["index"],b["index"],len(a["raw_segment"]),len(b["raw_segment"]))
            )

    print(
        f"SPR_DIFF|tw_records={len(tw_rows)}|v25_records={len(v_rows)}|"
        f"exact_prefix_records={prefix_records}|same_anim_count_by_sprno={same_header}|"
        f"segment_equal_by_sprno={segment_equal}|missing_in_v25={missing}|"
        f"v25_duplicate_sprnos={len(duplicates)}|tw_bytes={len(tw_data)}|v25_bytes={len(v_data)}|"
        f"common_prefix_bytes={common_prefix_bytes(tw_data,v_data)}"
    )
    for no,kind,ai,bi,asz,bsz in samples:
        print(
            f"SPR_CHANGE_SAMPLE|sprno={no}|kind={kind}|tw_index={ai}|v25_index={bi}|"
            f"tw_segment_bytes={asz}|v25_segment_bytes={bsz}"
        )


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--tw-bin", required=True)
    ap.add_argument("--v25-adrn", required=True)
    ap.add_argument("--v25-real", required=True)
    ap.add_argument("--v25-spradrn", required=True)
    ap.add_argument("--v25-spr", required=True)
    args=ap.parse_args()

    print("StoneAge Taiwan v1.0 vs preserved 2.5 resource diff — R1")
    print("SCOPE|verified-transient-bytes|derived-record-and-payload-comparison|no-payload-commit")

    img, rows, layout, joliet = find_rows(args.tw_bin)
    tmp=tempfile.TemporaryDirectory()
    root=Path(tmp.name)
    try:
        by_path={r["path"]:r for r in rows if not r["is_dir"]}
        for target in TW_TARGETS:
            row=by_path.get(target)
            if row is None:
                raise SystemExit(f"missing Taiwan target: {target}")
            extract_row(img,row,root/target)
        tw_adrn=root/"StoneAge/data/adrn_1.bin"
        tw_real=root/"StoneAge/data/real_1.bin"
        tw_spreadrn=root/"StoneAge/data/spradrn_1.bin"
        tw_spr=root/"StoneAge/data/spr_1.bin"
        print(
            f"TW_INPUT|layout={layout}|joliet={int(joliet)}|"
            f"adrn_sha256={sha256(tw_adrn.read_bytes())}|real_sha256={sha256(tw_real.read_bytes())}|"
            f"spradrn_sha256={sha256(tw_spreadrn.read_bytes())}|spr_sha256={sha256(tw_spr.read_bytes())}"
        )
        for label,p in (
            ("adrn",Path(args.v25_adrn)),("real",Path(args.v25_real)),
            ("spradrn",Path(args.v25_spradrn)),("spr",Path(args.v25_spr)),
        ):
            print(f"V25_INPUT|kind={label}|bytes={p.stat().st_size}|sha256={sha256(p.read_bytes())}")

        compare_adrn(tw_adrn,tw_real,Path(args.v25_adrn),Path(args.v25_real))
        compare_spr(tw_spreadrn,tw_spr,Path(args.v25_spradrn),Path(args.v25_spr))
    finally:
        img.close()
        tmp.cleanup()


if __name__=="__main__":
    main()
