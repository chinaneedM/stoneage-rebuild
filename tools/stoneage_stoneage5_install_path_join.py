#!/usr/bin/env python3
"""Deterministic full-CAB file-key -> installed path and cross-version hash join."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_FILES = {
    "cn50_cab": "research/recovered/STONEAGE-STONEAGE5-REAL-CAB-PAYLOAD-R1.json",
    "cn50_msi": "research/recovered/STONEAGE-STONEAGE5-MSI-INVENTORY-R1.txt",
    "tw10": "research/recovered/STONEAGE-TW10-CLIENT-INVENTORY-R1.txt",
    "tw85": "research/recovered/STONEAGE-WAYI85-MSI-CLIENT-PAYLOAD-R1.json",
}
TW85_PREFIX = "Program Files/WAYI/石器時代 魔域大冒險/"


def msi_table(text: str, name: str) -> list[list[str]]:
    opener = "MSI_EXPORT_BEGIN|table=" + name + "\n"
    closer = "MSI_EXPORT_END|table=" + name
    start = text.find(opener)
    if start < 0:
        raise ValueError("missing-msi-table:" + name)
    end = text.find(closer, start + len(opener))
    if end < 0:
        raise ValueError("incomplete-msi-table:" + name)
    lines = text[start + len(opener):end].splitlines()
    if len(lines) < 4 or lines[2].split("\t")[0] != name:
        raise ValueError("incorrect-msi-table-header:" + name)
    return [line.split("\t") for line in lines[3:] if line.strip()]


def safe_rel(name: str) -> str:
    name = name.replace("\\", "/")
    parts = name.split("/")
    if (not name or name.startswith("/") or ":" in parts[0] or
            any(x in ("", ".", "..") for x in parts) or
            any(ord(c) < 32 for c in name)):
        raise ValueError("unsafe-msi-path")
    return "/".join(parts)


def directory_relative(key: str, directories: dict) -> str:
    parts = []
    visited = set()
    while key != "INSTALLDIR":
        if key in visited or key not in directories:
            raise ValueError("missing-or-outside-installer-directory")
        visited.add(key)
        parent, label = directories[key]
        label = label.split("|")[-1].split(":")[-1]
        if label != ".":
            parts.insert(0, safe_rel(label))
        key = parent
    return "/".join(parts)


def parse_msi_paths(text: str) -> dict:
    dirs = {
        row[0]: (row[1], row[2])
        for row in msi_table(text, "Directory")
        if len(row) >= 3
    }
    comps = {
        row[0]: row[2]
        for row in msi_table(text, "Component")
        if len(row) >= 3
    }
    files = {}
    paths = set()
    for row in msi_table(text, "File"):
        if len(row) < 8:
            raise ValueError("short-msi-file-row")
        file_key, component, long_name = row[:3]
        if file_key in files or component not in comps:
            raise ValueError("duplicate-key-or-missing-component")
        suffix = safe_rel(long_name.split("|")[-1])
        folder = directory_relative(comps[component], dirs)
        path = safe_rel("/".join(x for x in (folder, suffix) if x))
        folded = path.casefold()
        if folded in paths:
            raise ValueError("duplicate-installed-path")
        paths.add(folded)
        files[file_key] = {
            "installed_path": path,
            "msi_file_size": int(row[3]),
            "msi_sequence": int(row[7]),
        }
    if len(files) != 413 or set(x["msi_sequence"] for x in files.values()) != set(range(1, 414)):
        raise ValueError("not-413-contiguous-installer-sequence")
    return files


def load_tw10(text: str) -> dict:
    rows = {}
    for line in text.splitlines():
        if not line.startswith("CORE_FILE|"):
            continue
        values = dict(part.split("=", 1) for part in line.split("|")[1:] if "=" in part)
        path = values["path"]
        if not path.startswith("StoneAge/"):
            raise ValueError("unexpected-tw10-prefix")
        key = safe_rel(path[len("StoneAge/"):]).casefold()
        if key in rows:
            raise ValueError("duplicate-tw10-path")
        rows[key] = {"size": int(values["size"]), "sha256": values["sha256"], "original_path": path}
    if len(rows) != 383:
        raise ValueError("untrusted-tw10-manifest")
    return rows


def load_tw85(data: dict) -> dict:
    samples = data["inspection"]["inventory"]["samples"]
    if len(samples) != 1 or samples[0]["file_count"] != 557:
        raise ValueError("untrusted-tw85-manifest")
    rows = {}
    for row in samples[0]["files"]:
        path = row["path"]
        if not path.startswith(TW85_PREFIX):
            raise ValueError("unexpected-tw85-prefix")
        key = safe_rel(path[len(TW85_PREFIX):]).casefold()
        if key in rows:
            raise ValueError("duplicate-tw85-path")
        rows[key] = {"size": int(row["size"]), "sha256": row["sha256"], "original_path": path}
    if len(rows) != 557:
        raise ValueError("incomplete-tw85-manifest")
    return rows


def same_path_comparison(rows: list, other: dict) -> dict:
    matches, changes, missing = [], [], []
    for row in rows:
        key = row["installed_path"].casefold()
        prev = other.get(key)
        if not prev:
            missing.append(row["installed_path"])
        elif row["size"] == prev["size"] and row["sha256"] == prev["sha256"]:
            matches.append(row["installed_path"])
        else:
            changes.append({"path": row["installed_path"],
                            "current_size": row["size"],
                            "reference_size": prev["size"],
                            "current_sha256": row["sha256"],
                            "reference_sha256": prev["sha256"]})
    return {
        "shared_path_count": len(matches) + len(changes),
        "same_path_exact_count": len(matches),
        "same_path_changed_count": len(changes),
        "not_present_at_same_path_count": len(missing),
        "same_path_exact_paths": sorted(matches),
        "changed_path_evidence": sorted(changes, key=lambda x: x["path"]),
        "not_present_at_same_path": sorted(missing),
    }


def build(root: Path = ROOT) -> dict:
    raw = {key: (root / relative).read_bytes() for key, relative in SOURCE_FILES.items()}
    cab = json.loads(raw["cn50_cab"])
    tw85 = json.loads(raw["tw85"])
    if (cab["status"] != "REAL_FULL_CAB_EXTRACTED_AND_413_FILES_HASHED" or
            cab["files"]["count"] != 413 or len(cab["files"]["inventory"]) != 413 or
            cab["boundaries"]["original_binary_committed"] is not False):
        raise ValueError("cab-original-byte-acceptance-missing")
    msi = parse_msi_paths(raw["cn50_msi"].decode("utf-8"))
    rows = []
    for source in cab["files"]["inventory"]:
        key = source["name"]
        target = msi.get(key)
        if not target or int(source["size"]) != target["msi_file_size"]:
            raise ValueError("cab-to-msi-key-or-size-mismatch:" + key)
        rows.append({
            "cab_index": int(source["index"]),
            "cab_file_key": key,
            "installed_path": target["installed_path"],
            "msi_sequence": target["msi_sequence"],
            "size": int(source["size"]),
            "sha256": source["sha256"],
        })
    if len(rows) != 413 or len(set(x["installed_path"].casefold() for x in rows)) != 413:
        raise ValueError("incomplete-cab-to-msi-join")
    rows.sort(key=lambda x: x["cab_index"])
    comparisons = {
        "TW10": same_path_comparison(rows, load_tw10(raw["tw10"].decode("utf-8"))),
        "TW85": same_path_comparison(rows, load_tw85(tw85)),
    }
    a, b = comparisons["TW10"], comparisons["TW85"]
    if (a["shared_path_count"], a["same_path_exact_count"], a["same_path_changed_count"]) != (362, 361, 1):
        raise ValueError("tw10-join-contradicts-original-hashes")
    if (b["shared_path_count"], b["same_path_exact_count"], b["same_path_changed_count"]) != (407, 407, 0):
        raise ValueError("tw85-join-contradicts-original-hashes")
    if [x["path"] for x in a["changed_path_evidence"]] != ["StoneAge.exe"]:
        raise ValueError("unexpected-tw10-changed-path")
    if cab["cross_version_exact_byte_matches"]["TW10"] and len(cab["cross_version_exact_byte_matches"]["TW10"]) != 361:
        raise ValueError("tw10-hash-count-disagreement")
    if len(cab["cross_version_exact_byte_matches"]["TW85"]) != 407:
        raise ValueError("tw85-hash-count-disagreement")
    if len([x for x in rows if x["installed_path"].startswith("data/")]) != 409:
        raise ValueError("unexpected-data-directory-scope")
    return {
        "schema": "stoneage.stoneage5.real_cab_installed_path_join_r1",
        "status": "413_REAL_FILE_SHA_JOINED_TO_413_MSI_DESTINATION_PATHS",
        "source_pins": {
            key: {"repo_path": SOURCE_FILES[key], "size": len(data),
                  "sha256": hashlib.sha256(data).hexdigest()}
            for key, data in raw.items()
        },
        "cab_sha256": cab["source"]["cab_sha256"],
        "installed_files": rows,
        "comparisons": comparisons,
        "scope": {
            "unique_paths": 413,
            "data_subtree_files": 409,
            "official_clean_client_authenticated": False,
            "original_server_content_restored": False,
            "historical_client_binaries_committed": False,
            "map_world_field_asset_coverage_claimed": False,
            "content_address_equal_implies_same_pet_identity": False,
        },
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    report = build()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2,
                                      sort_keys=True) + "\n", encoding="utf-8")
    print(f"RESULT|{report['status']}|tw10_exact={report['comparisons']['TW10']['same_path_exact_count']}|"
          f"tw85_exact={report['comparisons']['TW85']['same_path_exact_count']}")


if __name__ == "__main__":
    main()
