"""Read-only installed-client snapshot comparison for historical artifact intake.

This calculates exact file hashes and tree deltas. It never runs the program,
extracts an archive, patches files, or certifies publisher/version identity.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

MAX_FILES = 100000
MAX_PATH_CHARS = 1024


def scan_tree(folder: Path) -> dict:
    root = Path(folder)
    if not root.is_dir() or root.is_symlink():
        raise ValueError("Snapshot must be a real existing directory, not a symlink")
    files = {}
    folded = set()
    paths = sorted(root.rglob("*"), key=lambda p: p.relative_to(root).as_posix())
    for p in paths:
        rel = p.relative_to(root).as_posix()
        if len(rel) > MAX_PATH_CHARS or "\x00" in rel or "\n" in rel:
            raise ValueError("Unsupported relative file path")
        if p.is_symlink():
            raise ValueError("Symlinks forbidden in a purported snapshot: " + rel)
        if p.is_dir():
            continue
        if not p.is_file():
            raise ValueError("Special non-regular filesystem node: " + rel)
        if len(files) >= MAX_FILES:
            raise ValueError("Too many files in snapshot")
        folded_key = rel.casefold()
        if folded_key in folded:
            raise ValueError("Ambiguous Windows-case-colliding filenames: " + rel)
        folded.add(folded_key)
        sha = hashlib.sha256()
        length = 0
        with p.open("rb") as stream:
            while block := stream.read(1024 * 1024):
                sha.update(block)
                length += len(block)
        files[rel] = {"bytes": length, "sha256": sha.hexdigest()}
    if not files:
        raise ValueError("Empty snapshot cannot establish installed game content")
    manifest = json.dumps(files, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return {
        "manifest_sha256": hashlib.sha256(manifest.encode("utf-8")).hexdigest(),
        "file_count": len(files),
        "total_bytes": sum(v["bytes"] for v in files.values()),
        "files": files,
    }


def compare_trees(before: dict, after: dict) -> dict:
    old_files, new_files = before["files"], after["files"]
    b, a = set(old_files), set(new_files)
    added = sorted(a - b)
    removed = sorted(b - a)
    modified = sorted(k for k in a & b if old_files[k] != new_files[k])
    unchanged_count = len(a & b) - len(modified)
    return {
        "classification": "LOCAL_FILE_DIFF_NOT_RELEASE_OR_PUBLISHER_ATTESTATION",
        "source_version_verified": False,
        "official_publisher_verified": False,
        "complete_original_patch_sequence_verified": False,
        "original_pet_opcode127_runtime_verified": False,
        "before_manifest_sha256": before["manifest_sha256"],
        "after_manifest_sha256": after["manifest_sha256"],
        "before_file_count": before["file_count"],
        "after_file_count": after["file_count"],
        "added": added,
        "removed": removed,
        "modified": modified,
        "unchanged_count": unchanged_count,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--before", type=Path, required=True, help="Local read-only installed file tree")
    parser.add_argument("--after", type=Path, required=True, help="Local read-only installed file tree")
    args = parser.parse_args()
    result = compare_trees(scan_tree(args.before), scan_tree(args.after))
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
