#!/usr/bin/env python3
"""Inventory the accepted Taiwan StoneAge v1.0 client without storing payload bytes."""

from __future__ import annotations

import argparse
import collections
import hashlib
from pathlib import Path

from tools.stoneage_tw10_technical_probe import find_rows


EXCLUDED_STONEAGE_PREFIXES = (
    "stoneage/人在江湖/",
    "stoneage/陶莉萍『好想再聽一遍』試聽/",
)

INSTALLER_NAMES = {
    "setup.exe", "setup.ini", "data1.cab", "data1.hdr", "data2.cab",
    "ikernel.ex_", "layout.bin", "setup.inx",
}
RUNTIME_NAMES = {"stoneage.exe", "sa_3.exe"}
BRANDING_NAMES = {"logo.bmp", "waei.bmp", "man.ico"}
MASTER_TERMS = ("pet", "item", "skill", "magic", "npc", "enemy", "quest", "shop")


def normalize(path: str) -> str:
    return path.replace("\\", "/").strip("/")


def is_excluded_bundle(path: str) -> bool:
    low = normalize(path).lower()
    return any(low.startswith(prefix) for prefix in EXCLUDED_STONEAGE_PREFIXES)


def is_core_client(path: str) -> bool:
    p = normalize(path)
    return p.lower().startswith("stoneage/") and not is_excluded_bundle(p)


def classify_path(path: str) -> str:
    p = normalize(path)
    low = p.lower()
    if is_excluded_bundle(p):
        return "excluded_bundle"
    if not low.startswith("stoneage/"):
        return "external_disc"
    rel = low[len("stoneage/"):]
    name = rel.rsplit("/", 1)[-1]
    if name in RUNTIME_NAMES:
        return "runtime_executable"
    if name in INSTALLER_NAMES:
        return "installer_support"
    if name in BRANDING_NAMES:
        return "branding_ui_shell"
    if rel in {"data/real_1.bin", "data/adrn_1.bin"}:
        return "graphics_world"
    if rel in {"data/spr_1.bin", "data/spradrn_1.bin"}:
        return "sprite_animation"
    if rel in {"data/battle_1.bin", "data/battletxt_1.txt"} or rel.startswith("data/battlemap/"):
        return "battle_map"
    if rel.startswith("data/bgm/"):
        return "audio_bgm"
    if rel in {"data/sound_1.bin", "data/soundaddr_1.txt"} or rel.startswith("data/se/"):
        return "audio_sfx"
    if rel.startswith("data/pal/"):
        return "palette"
    if rel == "data/savedata.dat":
        return "local_state"
    return "unclassified_core"


def is_field_map_file(path: str) -> bool:
    p = normalize(path).lower()
    if not is_core_client(path):
        return False
    rel = p[len("stoneage/"):]
    if rel.startswith("data/battlemap/"):
        return False
    if "/map/" in "/" + rel:
        return True
    name = rel.rsplit("/", 1)[-1]
    return name.startswith("map") and name.endswith(".dat")


def is_named_master_candidate(path: str) -> bool:
    if not is_core_client(path):
        return False
    rel = normalize(path).lower()[len("stoneage/"):]
    return any(term in rel for term in MASTER_TERMS)


def row_bytes(img, row) -> bytes:
    return b"".join(img.iter_extent(row["lba"], row["size"]))


def row_sha256(img, row) -> str:
    h = hashlib.sha256()
    for chunk in img.iter_extent(row["lba"], row["size"]):
        h.update(chunk)
    return h.hexdigest()


def parse_address_table_bytes(data: bytes):
    text = data.decode("utf-8", errors="replace")
    rows = []
    for token in text.split():
        parts = token.split(":", 2)
        if len(parts) != 3:
            continue
        try:
            offset = int(parts[0])
            size = int(parts[1])
        except ValueError:
            continue
        rows.append((offset, size, Path(parts[2]).name.lower()))
    return rows


def parse_sab_candidate(data: bytes):
    """Parse the lineage-backed SAB candidate: 4-byte header + BE uint16 cells."""
    if len(data) < 4 or (len(data) - 4) % 2:
        raise ValueError("SAB candidate length must be 4 + 2*n bytes")
    header = data[:4]
    payload = data[4:]
    be_values = tuple(
        int.from_bytes(payload[i:i + 2], "big")
        for i in range(0, len(payload), 2)
    )
    le_values = tuple(
        int.from_bytes(payload[i:i + 2], "little")
        for i in range(0, len(payload), 2)
    )
    return header, be_values, le_values


def split_palette_candidate(data: bytes):
    """Split the bytes consumed by descendant 224-triplet palette readers."""
    consumed = 224 * 3
    if len(data) < consumed:
        raise ValueError("palette candidate is shorter than 224 RGB/BGR triplets")
    return data[:consumed], data[consumed:]


def inventory(bin_path: Path):
    img, rows, layout, joliet = find_rows(bin_path)
    try:
        files = [row for row in rows if not row["is_dir"]]
        core = [row for row in files if is_core_client(row["path"])]
        excluded = [row for row in files if is_excluded_bundle(row["path"])]
        external = [
            row for row in files
            if not normalize(row["path"]).lower().startswith("stoneage/")
        ]

        categories = collections.Counter()
        category_bytes = collections.Counter()
        ext = collections.Counter()
        for row in core:
            category = classify_path(row["path"])
            categories[category] += 1
            category_bytes[category] += row["size"]
            suffix = Path(normalize(row["path"])).suffix.lower() or "<none>"
            ext[suffix] += 1

        field_maps = [row for row in core if is_field_map_file(row["path"])]
        masters = [row for row in core if is_named_master_candidate(row["path"])]

        print("StoneAge Taiwan v1.0 deterministic client inventory — R1")
        print("SCOPE|verified-retail-disc|derived-metadata-only|no-payload-bytes")
        print(
            f"DISC|layout={layout}|joliet={int(joliet)}|"
            f"files={len(files)}|core_client_files={len(core)}"
        )
        print(
            f"BOUNDARY_COUNTS|excluded_bundled_files={len(excluded)}|"
            f"external_disc_files={len(external)}|field_map_disc_files={len(field_maps)}|"
            f"named_master_candidates={len(masters)}"
        )
        print(f"CORE_CLIENT_BYTES|{sum(row['size'] for row in core)}")

        by_path = {normalize(row["path"]).lower(): row for row in core}
        basename_paths = collections.defaultdict(list)
        for row in core:
            p = normalize(row["path"])
            basename_paths[Path(p).name.lower()].append(p)

        adrn_row = by_path.get("stoneage/data/adrn_1.bin")
        adrn_bitmapnos = set()
        if adrn_row is not None:
            adrn_data = row_bytes(img, adrn_row)
            if len(adrn_data) % 80 == 0:
                adrn_bitmapnos = {
                    int.from_bytes(adrn_data[offset:offset + 4], "little")
                    for offset in range(0, len(adrn_data), 80)
                }

        battle_sab_rows = [
            row for row in core
            if normalize(row["path"]).lower().startswith("stoneage/data/battlemap/")
            and normalize(row["path"]).lower().endswith(".sab")
        ]
        sab_exact_804 = 0
        sab_header_sab = 0
        sab_tile_400 = 0
        sab_be_resolved = 0
        sab_le_resolved = 0
        sab_cells = 0
        for row in sorted(battle_sab_rows, key=lambda r: normalize(r["path"]).lower()):
            data = row_bytes(img, row)
            header, be_values, le_values = parse_sab_candidate(data)
            if len(data) == 804:
                sab_exact_804 += 1
            if header[:3] == b"SAB":
                sab_header_sab += 1
            if len(be_values) == 400:
                sab_tile_400 += 1
            be_resolved = sum(value in adrn_bitmapnos for value in be_values)
            le_resolved = sum(value in adrn_bitmapnos for value in le_values)
            sab_be_resolved += be_resolved
            sab_le_resolved += le_resolved
            sab_cells += len(be_values)
            ascii_header = "".join(
                chr(value) if 32 <= value < 127 else "."
                for value in header
            )
            print(
                f"BATTLE_SAB_RECORD|path={normalize(row['path'])}|size={len(data)}|"
                f"header_hex={header.hex()}|header_ascii={ascii_header}|"
                f"tile_count={len(be_values)}|be_min={min(be_values, default=-1)}|"
                f"be_max={max(be_values, default=-1)}|be_unique={len(set(be_values))}|"
                f"be_adrn_resolved={be_resolved}|le_adrn_resolved={le_resolved}|"
                f"payload_sha256={hashlib.sha256(data[4:]).hexdigest()}"
            )
        print(
            f"BATTLE_SAB_SUMMARY|files={len(battle_sab_rows)}|"
            f"exact_size_804={sab_exact_804}|header_sab={sab_header_sab}|"
            f"tile_count_400={sab_tile_400}|cells={sab_cells}|"
            f"be_adrn_resolved={sab_be_resolved}|le_adrn_resolved={sab_le_resolved}|"
            f"adrn_bitmapnos={len(adrn_bitmapnos)}"
        )

        palette_rows = [
            row for row in core
            if normalize(row["path"]).lower().startswith("stoneage/data/pal/")
            and normalize(row["path"]).lower().endswith(".sap")
        ]
        palette_exact_708 = 0
        palette_tail_hashes = set()
        for row in sorted(palette_rows, key=lambda r: normalize(r["path"]).lower()):
            data = row_bytes(img, row)
            consumed, tail = split_palette_candidate(data)
            if len(data) == 708:
                palette_exact_708 += 1
            tail_hash = hashlib.sha256(tail).hexdigest()
            palette_tail_hashes.add(tail_hash)
            print(
                f"PALETTE_RECORD|path={normalize(row['path'])}|size={len(data)}|"
                f"lineage_consumed_bytes={len(consumed)}|lineage_triplets={len(consumed) // 3}|"
                f"tail_bytes={len(tail)}|consumed_sha256={hashlib.sha256(consumed).hexdigest()}|"
                f"tail_sha256={tail_hash}"
            )
        print(
            f"PALETTE_SUMMARY|files={len(palette_rows)}|exact_size_708={palette_exact_708}|"
            f"lineage_consumed_bytes=672|lineage_triplets=224|"
            f"tail_bytes_if_708=36|distinct_tail_hashes={len(palette_tail_hashes)}"
        )

        for label, table_path, container_path, expected_prefix in (
            (
                "battle",
                "stoneage/data/battletxt_1.txt",
                "stoneage/data/battle_1.bin",
                "stoneage/data/battlemap/",
            ),
            (
                "sound",
                "stoneage/data/soundaddr_1.txt",
                "stoneage/data/sound_1.bin",
                "stoneage/data/se/",
            ),
        ):
            table_row = by_path.get(table_path)
            if table_row is None:
                print(f"ADDRESS_TABLE|label={label}|missing=1")
                continue
            addr_rows = parse_address_table_bytes(row_bytes(img, table_row))
            names = collections.Counter(name for _, _, name in addr_rows)
            duplicate_refs = sum(max(0, count - 1) for count in names.values())

            container_row = by_path.get(container_path)
            record_bytes = sum(size for _, size, _ in addr_rows)
            span_end = max((offset + size for offset, size, _ in addr_rows), default=0)
            contiguous = all(
                addr_rows[index][0]
                == addr_rows[index - 1][0] + addr_rows[index - 1][1]
                for index in range(1, len(addr_rows))
            )
            starts_zero = bool(addr_rows) and addr_rows[0][0] == 0
            container_size = container_row["size"] if container_row is not None else -1
            print(
                f"ADDRESS_TABLE_CONTAINER|label={label}|table_path={table_path}|"
                f"container_path={container_path}|records={len(addr_rows)}|"
                f"record_bytes={record_bytes}|span_end={span_end}|"
                f"container_size={container_size}|starts_zero={int(starts_zero)}|"
                f"contiguous={int(contiguous)}|"
                f"span_matches_container={int(container_row is not None and span_end == container_size)}"
            )

            record_categories = collections.Counter()
            record_category_bytes = collections.Counter()
            for index, (offset, size, name) in enumerate(addr_rows):
                paths = basename_paths.get(name, [])
                matched_rows = [by_path[p.lower()] for p in paths if p.lower() in by_path]
                categories_for_record = sorted(
                    {classify_path(row["path"]) for row in matched_rows}
                )
                category = ";".join(categories_for_record) if categories_for_record else "missing"
                record_categories[category] += 1
                record_category_bytes[category] += size
                path_text = ";".join(paths)
                file_sizes = ";".join(str(row["size"]) for row in matched_rows)
                file_hashes = ";".join(row_sha256(img, row) for row in matched_rows)
                print(
                    f"ADDRESS_RECORD|label={label}|index={index}|offset={offset}|size={size}|"
                    f"name={name}|match_count={len(matched_rows)}|category={category}|"
                    f"paths={path_text}|file_sizes={file_sizes}|sha256={file_hashes}"
                )
            for category in sorted(record_categories):
                print(
                    f"ADDRESS_TABLE_CATEGORY|label={label}|category={category}|"
                    f"records={record_categories[category]}|"
                    f"record_bytes={record_category_bytes[category]}"
                )
            present_any = set()
            present_expected = set()
            outside_expected = {}
            missing_any = []
            for name in names:
                paths = basename_paths.get(name, [])
                if paths:
                    present_any.add(name)
                expected = [p for p in paths if p.lower().startswith(expected_prefix)]
                if expected:
                    present_expected.add(name)
                elif paths:
                    outside_expected[name] = paths
                else:
                    missing_any.append(name)
            print(
                f"ADDRESS_TABLE|label={label}|records={len(addr_rows)}|"
                f"unique_names={len(names)}|duplicate_refs={duplicate_refs}"
            )
            expected_names = {
                Path(normalize(row["path"])).name.lower()
                for row in core
                if normalize(row["path"]).lower().startswith(expected_prefix)
            }
            unreferenced_expected = sorted(expected_names - set(names))
            print(
                f"ADDRESS_TABLE_MATCH|label={label}|present_any={len(present_any)}|"
                f"present_expected_dir={len(present_expected)}|"
                f"outside_expected_dir={len(outside_expected)}|missing_any={len(missing_any)}|"
                f"unreferenced_expected_dir={len(unreferenced_expected)}"
            )
            for name in unreferenced_expected:
                paths = basename_paths.get(name, [])
                print(
                    f"ADDRESS_TABLE_UNREFERENCED|label={label}|name={name}|"
                    f"paths={';'.join(paths)}"
                )
            for name, paths in sorted(outside_expected.items()):
                print(
                    f"ADDRESS_TABLE_OUTSIDE_DIR|label={label}|name={name}|"
                    f"paths={';'.join(paths)}"
                )
            for name in sorted(missing_any):
                print(f"ADDRESS_TABLE_MISSING|label={label}|name={name}")
            for name, count in sorted(names.items()):
                if count > 1:
                    print(
                        f"ADDRESS_TABLE_DUPLICATE|label={label}|name={name}|refs={count}"
                    )

        for category in sorted(categories):
            print(
                f"CATEGORY|name={category}|files={categories[category]}|"
                f"bytes={category_bytes[category]}"
            )
        for suffix, count in sorted(ext.items()):
            print(f"EXTENSION|name={suffix}|files={count}")

        for row in sorted(core, key=lambda r: normalize(r["path"]).lower()):
            path = normalize(row["path"])
            print(
                f"CORE_FILE|category={classify_path(path)}|path={path}|"
                f"size={row['size']}|sha256={row_sha256(img,row)}"
            )

        for row in sorted(field_maps, key=lambda r: normalize(r["path"]).lower()):
            print(f"FIELD_MAP_DISC_FILE|path={normalize(row['path'])}|size={row['size']}")
        for row in sorted(masters, key=lambda r: normalize(r["path"]).lower()):
            print(
                f"NAMED_MASTER_CANDIDATE|path={normalize(row['path'])}|"
                f"size={row['size']}"
            )

        print(
            "BOUNDARY_NOTE|field_map_disc_files counts ordinary map/cache files only; "
            "battleMap SAB files are classified separately."
        )
        print(
            "BOUNDARY_NOTE|named_master_candidates is filename-level evidence only; "
            "zero does not exclude tables embedded in executables/containers or supplied by servers."
        )
    finally:
        img.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bin", type=Path, required=True)
    args = ap.parse_args()
    inventory(args.bin)


if __name__ == "__main__":
    main()
