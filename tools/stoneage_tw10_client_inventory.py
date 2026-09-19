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

        for label, table_path, expected_prefix in (
            ("battle", "stoneage/data/battletxt_1.txt", "stoneage/data/battlemap/"),
            ("sound", "stoneage/data/soundaddr_1.txt", "stoneage/data/se/"),
        ):
            table_row = by_path.get(table_path)
            if table_row is None:
                print(f"ADDRESS_TABLE|label={label}|missing=1")
                continue
            addr_rows = parse_address_table_bytes(row_bytes(img, table_row))
            names = collections.Counter(name for _, _, name in addr_rows)
            duplicate_refs = sum(max(0, count - 1) for count in names.values())
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
            print(
                f"ADDRESS_TABLE_MATCH|label={label}|present_any={len(present_any)}|"
                f"present_expected_dir={len(present_expected)}|"
                f"outside_expected_dir={len(outside_expected)}|missing_any={len(missing_any)}"
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
