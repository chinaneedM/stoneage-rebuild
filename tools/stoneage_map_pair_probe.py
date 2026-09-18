#!/usr/bin/env python3
"""Compare recovered StoneAge .MAP single-layer files with .DAT three-layer map caches."""

import argparse
import hashlib
import struct
from pathlib import Path


def read_map_file(path: Path):
    data = path.read_bytes()
    if len(data) < 8:
        raise ValueError(f"{path}: shorter than 8-byte header")
    width, height = struct.unpack_from("<II", data, 0)
    cells = width * height
    expected = 8 + cells * 2
    if len(data) != expected:
        raise ValueError(f"{path}: size {len(data)} != expected {expected}")
    return width, height, data[8:]


def read_dat_file(path: Path):
    data = path.read_bytes()
    if len(data) < 8:
        raise ValueError(f"{path}: shorter than 8-byte header")
    width, height = struct.unpack_from("<II", data, 0)
    cells = width * height
    layer_size = cells * 2
    expected = 8 + layer_size * 3
    if len(data) != expected:
        raise ValueError(f"{path}: size {len(data)} != expected {expected}")
    start = 8
    tile = data[start : start + layer_size]
    parts = data[start + layer_size : start + layer_size * 2]
    event = data[start + layer_size * 2 : start + layer_size * 3]
    return width, height, tile, parts, event


def collect(map_dir: Path, suffix: str):
    out = {}
    for path in map_dir.rglob("*"):
        if path.is_file() and path.suffix.lower() == suffix:
            rel = path.relative_to(map_dir)
            key = str(rel.with_suffix("")).lower()
            out[key] = path
    return out


def analyze(map_dir: Path, sample_limit=20):
    maps = collect(map_dir, ".map")
    dats = collect(map_dir, ".dat")
    paired = sorted(set(maps) & set(dats))
    map_only = sorted(set(maps) - set(dats))
    dat_only = sorted(set(dats) - set(maps))

    counts = {
        "paired": len(paired),
        "map_only": len(map_only),
        "dat_only": len(dat_only),
        "header_match": 0,
        "tile_match": 0,
        "parts_match": 0,
        "event_match": 0,
        "map_matches_no_dat_layer": 0,
    }
    samples = []
    mismatches = []
    invalid_pairs = []
    aggregate = hashlib.sha256()

    for key in paired:
        mp = maps[key]
        dp = dats[key]
        try:
            mw, mh, map_payload = read_map_file(mp)
            dw, dh, tile, parts, event = read_dat_file(dp)
        except Exception as exc:
            invalid_pairs.append((key, mp.stat().st_size, dp.stat().st_size, str(exc)))
            continue
        header_match = (mw, mh) == (dw, dh)
        tile_match = map_payload == tile
        parts_match = map_payload == parts
        event_match = map_payload == event

        counts["header_match"] += int(header_match)
        counts["tile_match"] += int(tile_match)
        counts["parts_match"] += int(parts_match)
        counts["event_match"] += int(event_match)
        if not (tile_match or parts_match or event_match):
            counts["map_matches_no_dat_layer"] += 1

        row = (
            key,
            mw,
            mh,
            int(header_match),
            int(tile_match),
            int(parts_match),
            int(event_match),
            hashlib.sha256(map_payload).hexdigest(),
            hashlib.sha256(tile).hexdigest(),
            hashlib.sha256(parts).hexdigest(),
            hashlib.sha256(event).hexdigest(),
        )
        aggregate.update(("|".join(map(str, row)) + "\n").encode("ascii"))

        if len(samples) < sample_limit:
            samples.append(row)
        if (
            not header_match
            or not tile_match
            or parts_match
            or event_match
        ) and len(mismatches) < sample_limit:
            mismatches.append(row)

    return {
        "map_count": len(maps),
        "dat_count": len(dats),
        "counts": counts,
        "map_only": map_only,
        "dat_only": dat_only,
        "samples": samples,
        "mismatches": mismatches,
        "invalid_pairs": invalid_pairs,
        "aggregate_sha256": aggregate.hexdigest(),
    }


def emit(result, sample_limit=20):
    c = result["counts"]
    print("StoneAge recovered MAP/DAT relationship validation — R1")
    print("No proprietary map payload bytes are stored in this report.")
    print(f"MAP_COUNT|{result['map_count']}")
    print(f"DAT_COUNT|{result['dat_count']}")
    print(f"PAIRED_COUNT|{c['paired']}")
    print(f"MAP_ONLY_COUNT|{c['map_only']}")
    print(f"DAT_ONLY_COUNT|{c['dat_only']}")
    print(f"HEADER_MATCH_COUNT|{c['header_match']}")
    print(f"MAP_EQUALS_DAT_TILE_COUNT|{c['tile_match']}")
    print(f"MAP_EQUALS_DAT_PARTS_COUNT|{c['parts_match']}")
    print(f"MAP_EQUALS_DAT_EVENT_COUNT|{c['event_match']}")
    print(f"MAP_MATCHES_NO_DAT_LAYER_COUNT|{c['map_matches_no_dat_layer']}")
    print(f"INVALID_PAIR_COUNT|{len(result['invalid_pairs'])}")
    print(f"AGGREGATE_PAIR_SHA256|{result['aggregate_sha256']}")
    print("MAP_ONLY_SAMPLE|" + ",".join(result["map_only"][:sample_limit]))
    print("DAT_ONLY_SAMPLE|" + ",".join(result["dat_only"][:sample_limit]))
    print(
        "PAIR_SAMPLE|key|width|height|header_match|tile_match|parts_match|event_match|"
        "map_sha256|tile_sha256|parts_sha256|event_sha256"
    )
    for row in result["samples"][:sample_limit]:
        print("PAIR_SAMPLE|" + "|".join(map(str, row)))
    print(
        "PAIR_MISMATCH_SAMPLE|key|width|height|header_match|tile_match|parts_match|event_match|"
        "map_sha256|tile_sha256|parts_sha256|event_sha256"
    )
    for row in result["mismatches"][:sample_limit]:
        print("PAIR_MISMATCH_SAMPLE|" + "|".join(map(str, row)))
    print("INVALID_PAIR_SAMPLE|key|map_bytes|dat_bytes|reason")
    for row in result["invalid_pairs"][:sample_limit]:
        print("INVALID_PAIR_SAMPLE|" + "|".join(map(str, row)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--map-dir", type=Path, required=True)
    args = parser.parse_args()
    emit(analyze(args.map_dir))


if __name__ == "__main__":
    main()
