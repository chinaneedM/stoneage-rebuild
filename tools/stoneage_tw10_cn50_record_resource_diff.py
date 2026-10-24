#!/usr/bin/env python3
"""Strict record-level version comparison of original StoneAge RD and SPR data.

Contains no model/quest/pet-name inference; emits derived hashes and bounded
diagnostic examples, never proprietary sprite, audio, image or animation bytes.
"""
from __future__ import annotations
from collections import Counter, defaultdict
import hashlib
import mmap
from pathlib import Path
import struct

ADRN_RECORD_SIZE = 80
SPRADRN_RECORD_SIZE = 12
ANIMATION_HEADER_SIZE = 12
FRAME_SIZE = 10


def stream_sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as source:
        while block := source.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def parse_adrn(adrn_path, real_path):
    adrn = Path(adrn_path).read_bytes()
    if len(adrn) % ADRN_RECORD_SIZE:
        raise ValueError("ADRN remainder")
    real_size = Path(real_path).stat().st_size
    digest = hashlib.sha256()
    rows = []
    problems = Counter()
    with Path(real_path).open("rb") as source:
        with mmap.mmap(source.fileno(), 0, access=mmap.ACCESS_READ) as memory:
            for index, offset in enumerate(range(0, len(adrn), ADRN_RECORD_SIZE)):
                record = adrn[offset:offset + ADRN_RECORD_SIZE]
                bitmap, address, size, xoff, yoff, width, height = struct.unpack_from(
                    "<IIIiiii", record)
                digest.update(record)
                if address == 0 and size == 0:
                    problems["empty_offset_size"] += 1
                    continue
                if size < 16 or address + size > real_size:
                    problems["invalid_record_bounds"] += 1
                    continue
                header = memory[address:address + 16]
                if header[:2] != b"RD":
                    problems["record_missing_RD_magic"] += 1
                    continue
                frame = memory[address:address + size]
                payload_sha = hashlib.sha256(frame).hexdigest()
                rows.append({
                    "index": index, "id": bitmap, "raw_sha256": hashlib.sha256(record).hexdigest(),
                    "payload_sha256": payload_sha, "size": size,
                    "geometry": [xoff, yoff, width, height],
                    "rd_flag": header[2],
                    "rd_size_match": struct.unpack_from("<I", header, 12)[0] == size,
                })
    return {
        "index_count": len(adrn) // ADRN_RECORD_SIZE,
        "valid_payload_rows": len(rows), "problems": dict(sorted(problems.items())),
        "index_sha256": digest.hexdigest(), "rows": rows
    }


def parse_spr(spradrn_path, spr_path):
    raw = Path(spradrn_path).read_bytes()
    if len(raw) % SPRADRN_RECORD_SIZE:
        raise ValueError("SPRADRN remainder")
    data = Path(spr_path).read_bytes()
    groups = []
    for idx, pos in enumerate(range(0, len(raw), SPRADRN_RECORD_SIZE)):
        spr_no, start, n_anim = struct.unpack_from("<IIH", raw, pos)
        groups.append((idx, spr_no, start, n_anim))
    sorted_offsets = sorted(groups, key=lambda row: (row[2], row[0]))
    end_by_index = {
        a[0]: b[2] for a, b in zip(sorted_offsets, sorted_offsets[1:])
    }
    if sorted_offsets:
        end_by_index[sorted_offsets[-1][0]] = len(data)
    problems = Counter()
    rows = []
    for idx, spr_no, start, n_anim in groups:
        end = end_by_index[idx]
        if start >= len(data) or end > len(data) or end < start:
            problems["out_of_bounds"] += 1
            continue
        if end == start:
            problems["zero_span"] += 1
            continue
        segment = data[start:end]
        cursor = 0
        frames = 0
        valid = True
        for _ in range(n_anim):
            if cursor + ANIMATION_HEADER_SIZE > len(segment):
                problems["truncated_anim_header"] += 1
                valid = False
                break
            direction, number, duration, count = struct.unpack_from("<HHII", segment, cursor)
            cursor += ANIMATION_HEADER_SIZE
            need = count * FRAME_SIZE
            if need > len(segment) - cursor:
                problems["invalid_frame_span"] += 1
                valid = False
                break
            cursor += need
            frames += count
        if not valid:
            continue
        if cursor != len(segment):
            problems["trailing_segment_bytes"] += 1
        rows.append({
            "index": idx, "id": spr_no, "segment_sha256": hashlib.sha256(segment).hexdigest(),
            "bytes": len(segment), "anim_count": n_anim, "frame_count": frames,
            "exact_segment_span": cursor == len(segment),
        })
    return {"index_count": len(groups), "valid_segments": len(rows),
            "problems": dict(sorted(problems.items())),
            "index_sha256": hashlib.sha256(raw).hexdigest(), "rows": rows}


def compare_id_rows(old_rows, new_rows, flavor, sample_cap=32):
    old = defaultdict(list)
    new = defaultdict(list)
    for entry in old_rows:
        old[entry["id"]].append(entry)
    for entry in new_rows:
        new[entry["id"]].append(entry)
    ambiguous_old = {key for key, val in old.items() if len(val) != 1}
    ambiguous_new = {key for key, val in new.items() if len(val) != 1}
    valid_old = set(old) - ambiguous_old
    valid_new = set(new) - ambiguous_new
    ambiguous_shared = set(old) & set(new) & (ambiguous_old | ambiguous_new)
    shared = sorted(valid_old & valid_new)
    missing = sorted(valid_old - set(new))
    added = sorted(valid_new - set(old))
    skipped = sorted(ambiguous_shared)
    exact_payload = 0
    same_geom = 0
    same_index_record = 0
    changed = []
    for key in shared:
        a, b = old[key][0], new[key][0]
        if flavor == "adrn":
            equal = a["payload_sha256"] == b["payload_sha256"]
            same_geom += a["geometry"] == b["geometry"]
            same_index_record += a["raw_sha256"] == b["raw_sha256"]
        elif flavor == "spr":
            equal = a["segment_sha256"] == b["segment_sha256"]
            same_geom += a["anim_count"] == b["anim_count"]
            same_index_record += a["frame_count"] == b["frame_count"]
        else:
            raise ValueError("unknown-flavor")
        exact_payload += equal
        if not equal and len(changed) < sample_cap:
            changed.append({"id": key, "old_index": a["index"], "new_index": b["index"],
                            "old_length": a.get("size",a.get("bytes")),
                            "new_length": b.get("size",b.get("bytes"))})
    def group_digest(values):
        h = hashlib.sha256()
        for value in values:
            h.update(str(value).encode("ascii") + b"\n")
        return h.hexdigest()
    return {
        "old_total_ids": len(old), "new_total_ids": len(new),
        "old_duplicate_ids": len(ambiguous_old),
        "new_duplicate_ids": len(ambiguous_new),
        "ambiguous_shared_id_count": len(ambiguous_shared),
        "common_unique_id_count": len(shared),
        "exact_payload_or_segment_count": exact_payload,
        "changed_payload_or_segment_count": len(shared)-exact_payload,
        "same_geometry_or_animation_count": same_geom,
        "same_index_descriptor_or_frame_count": same_index_record,
        "old_unique_ids_absent_in_new_count": len(missing),
        "new_unique_ids_absent_in_old_count": len(added),
        "common_unique_ids_sha256": group_digest(shared),
        "missing_old_ids_sha256": group_digest(missing),
        "new_ids_sha256": group_digest(added),
        "ambiguous_ids_sha256": group_digest(skipped),
        "missing_old_id_sample": missing[:sample_cap],
        "new_id_sample": added[:sample_cap],
        "changed_payload_samples": changed,
    }


def compare_directories(old, new):
    adrn_old = parse_adrn(old / "adrn.bin", old / "real.bin")
    adrn_new = parse_adrn(new / "adrn.bin", new / "real.bin")
    spr_old = parse_spr(old / "spradrn.bin", old / "spr.bin")
    spr_new = parse_spr(new / "spradrn.bin", new / "spr.bin")
    result = {
        "schema": "stoneage.tw10_cn50.record_level_resource_diff_r1",
        "families": {
            "bitmap_rd": {
                "old": {k: v for k, v in adrn_old.items() if k != "rows"},
                "new": {k: v for k, v in adrn_new.items() if k != "rows"},
                "comparison": compare_id_rows(adrn_old["rows"], adrn_new["rows"], "adrn"),
            },
            "animation_spr": {
                "old": {k: v for k, v in spr_old.items() if k != "rows"},
                "new": {k: v for k, v in spr_new.items() if k != "rows"},
                "comparison": compare_id_rows(spr_old["rows"], spr_new["rows"], "spr"),
            }
        },
        "evidence_boundaries": {
            "same_resource_id_is_not_a_pet_species_id": True,
            "same_payload_is_not_same_original_server_entity": True,
            "variant_resources_not_immediately_attributed_to_official_update": True,
            "original_server_npc_quest_growth_master_recovered": False,
            "complete_3d_models_demonstrated": False,
            "proprietary_bytes_emitted": False,
        }
    }
    return result
