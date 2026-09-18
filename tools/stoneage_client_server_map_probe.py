#!/usr/bin/env python3
"""Compare recovered client .MAP files with recovered server LS2MAP tile/object layers."""

import argparse
import collections
import hashlib
import struct
from pathlib import Path

SERVER_HEADER_SIZE = 44
MAGIC = b"LS2MAP"


def read_client_map(path: Path):
    data = path.read_bytes()
    if len(data) < 8:
        raise ValueError("client_map_too_short")
    width, height = struct.unpack_from("<II", data, 0)
    cells = width * height
    if len(data) != 8 + cells * 2:
        raise ValueError(f"client_map_bad_size:{len(data)}:{width}:{height}")
    values = struct.unpack_from(f"<{cells}H", data, 8) if cells else ()
    return width, height, values


def read_server_map(path: Path):
    data = path.read_bytes()
    if len(data) < SERVER_HEADER_SIZE or data[:6] != MAGIC:
        raise ValueError("not_ls2map")
    map_id = struct.unpack_from(">H", data, 6)[0]
    raw_name = data[8:40].split(b"\0", 1)[0]
    width = struct.unpack_from(">H", data, 40)[0]
    height = struct.unpack_from(">H", data, 42)[0]
    cells = width * height
    expected = SERVER_HEADER_SIZE + cells * 4
    if len(data) != expected:
        raise ValueError(f"server_map_bad_size:{len(data)}:{expected}:{width}:{height}")
    tile_off = SERVER_HEADER_SIZE
    obj_off = tile_off + cells * 2
    tile = struct.unpack_from(f">{cells}H", data, tile_off) if cells else ()
    obj = struct.unpack_from(f">{cells}H", data, obj_off) if cells else ()
    return map_id, raw_name, width, height, tile, obj


def collect_server_maps(root: Path, sample_limit=30):
    by_id = collections.defaultdict(list)
    invalid = []
    total_files = 0
    ls2_files = 0
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        total_files += 1
        try:
            parsed = read_server_map(path)
        except ValueError as exc:
            if str(exc) != "not_ls2map" and len(invalid) < sample_limit:
                invalid.append((str(path.relative_to(root)), path.stat().st_size, str(exc)))
            continue
        ls2_files += 1
        map_id, name, width, height, tile, obj = parsed
        by_id[map_id].append(
            {
                "path": path,
                "name": name,
                "width": width,
                "height": height,
                "tile": tile,
                "obj": obj,
            }
        )
    return by_id, total_files, ls2_files, invalid


def analyze(client_dir: Path, server_root: Path, sample_limit=25):
    server_by_id, server_total, server_ls2, server_invalid = collect_server_maps(
        server_root, sample_limit=sample_limit
    )
    client_maps = {}
    client_invalid = []
    for path in sorted(client_dir.glob("*.MAP"), key=lambda p: p.name):
        try:
            map_id = int(path.stem)
        except ValueError:
            if len(client_invalid) < sample_limit:
                client_invalid.append((path.name, path.stat().st_size, "non_numeric_stem"))
            continue
        try:
            client_maps[map_id] = (path,) + read_client_map(path)
        except ValueError as exc:
            if len(client_invalid) < sample_limit:
                client_invalid.append((path.name, path.stat().st_size, str(exc)))

    counts = collections.Counter()
    samples = []
    mismatches = []
    duplicate_server_ids = []
    aggregate = hashlib.sha256()

    for map_id, entries in sorted(server_by_id.items()):
        if len(entries) > 1:
            duplicate_server_ids.append(
                (map_id, tuple(str(e["path"].relative_to(server_root)) for e in entries))
            )

    matched_ids = sorted(set(client_maps) & set(server_by_id))
    for map_id in matched_ids:
        cpath, cw, ch, cvals = client_maps[map_id]
        entries = server_by_id[map_id]
        any_dim = False
        any_tile = False
        any_obj = False

        for entry in entries:
            if (cw, ch) != (entry["width"], entry["height"]):
                continue
            any_dim = True
            tile_match = tuple(cvals) == tuple(entry["tile"])
            obj_match = tuple(cvals) == tuple(entry["obj"])
            any_tile = any_tile or tile_match
            any_obj = any_obj or obj_match
            if tile_match:
                counts["client_map_equals_server_tile"] += 1
            if obj_match:
                counts["client_map_equals_server_obj"] += 1

            row = (
                map_id,
                cw,
                ch,
                str(entry["path"].relative_to(server_root)),
                int(tile_match),
                int(obj_match),
                hashlib.sha256(struct.pack(f"<{len(cvals)}H", *cvals)).hexdigest(),
                hashlib.sha256(struct.pack(f"<{len(entry['tile'])}H", *entry["tile"])).hexdigest(),
                hashlib.sha256(struct.pack(f"<{len(entry['obj'])}H", *entry["obj"])).hexdigest(),
            )
            aggregate.update(("|".join(map(str, row)) + "\n").encode("utf-8"))
            if len(samples) < sample_limit:
                samples.append(row)

        if any_dim:
            counts["matched_id_and_dimensions"] += 1
            if any_tile:
                counts["ids_with_any_tile_match"] += 1
            if any_obj:
                counts["ids_with_any_obj_match"] += 1
            if not any_tile and not any_obj:
                counts["ids_with_no_layer_match"] += 1
                if len(mismatches) < sample_limit:
                    mismatches.append((map_id, cw, ch, len(entries)))
        else:
            counts["matched_id_dimension_mismatch"] += 1
            if len(mismatches) < sample_limit:
                dims=";".join(f"{e['width']}x{e['height']}" for e in entries)
                mismatches.append((map_id, cw, ch, f"server:{dims}"))

    counts["client_map_count"] = len(client_maps)
    counts["server_file_count"] = server_total
    counts["server_ls2map_count"] = server_ls2
    counts["matched_id_count"] = len(matched_ids)
    counts["client_only_id_count"] = len(set(client_maps) - set(server_by_id))
    counts["server_only_id_count"] = len(set(server_by_id) - set(client_maps))
    counts["duplicate_server_id_count"] = len(duplicate_server_ids)

    return {
        "counts": counts,
        "client_invalid": client_invalid,
        "server_invalid": server_invalid,
        "duplicate_server_ids": duplicate_server_ids,
        "client_only_ids": sorted(set(client_maps) - set(server_by_id)),
        "server_only_ids": sorted(set(server_by_id) - set(client_maps)),
        "samples": samples,
        "mismatches": mismatches,
        "aggregate": aggregate.hexdigest(),
    }


def emit(r, sample_limit=25):
    print("StoneAge recovered client MAP / server LS2MAP crosscheck — R1")
    print("No proprietary map payload bytes are stored in this report.")
    for k in sorted(r["counts"]):
        print(f"COUNT|{k}|{r['counts'][k]}")
    print(f"AGGREGATE_COMPARE_SHA256|{r['aggregate']}")
    print("CLIENT_ONLY_ID_SAMPLE|" + ",".join(map(str, r["client_only_ids"][:sample_limit])))
    print("SERVER_ONLY_ID_SAMPLE|" + ",".join(map(str, r["server_only_ids"][:sample_limit])))
    print("DUPLICATE_SERVER_ID|map_id|paths")
    for map_id, paths in r["duplicate_server_ids"][:sample_limit]:
        print(f"DUPLICATE_SERVER_ID|{map_id}|{' ; '.join(paths)}")
    print("PAIR_SAMPLE|map_id|width|height|server_path|tile_match|obj_match|client_sha|tile_sha|obj_sha")
    for row in r["samples"][:sample_limit]:
        print("PAIR_SAMPLE|" + "|".join(map(str, row)))
    print("PAIR_MISMATCH|map_id|client_width|client_height|detail")
    for row in r["mismatches"][:sample_limit]:
        print("PAIR_MISMATCH|" + "|".join(map(str, row)))
    print("CLIENT_INVALID|path|bytes|reason")
    for row in r["client_invalid"][:sample_limit]:
        print("CLIENT_INVALID|" + "|".join(map(str, row)))
    print("SERVER_INVALID|path|bytes|reason")
    for row in r["server_invalid"][:sample_limit]:
        print("SERVER_INVALID|" + "|".join(map(str, row)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--client-map-dir", type=Path, required=True)
    ap.add_argument("--server-map-root", type=Path, required=True)
    args = ap.parse_args()
    emit(analyze(args.client_map_dir, args.server_map_root))


if __name__ == "__main__":
    main()
