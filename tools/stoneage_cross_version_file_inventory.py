"""Read-only, offline SHA-256 cross-version inventory for StoneAge client specimens.

Only original-byte equality is reported. The tool does not install/run software,
copy assets, decide provenance, or infer server-side gameplay tables.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import stat
import zipfile

SOURCE_CLASSES = {"ACCEPTED_OFFICIAL_BASELINE", "PROVENANCE_SUPPORTED_CANDIDATE",
                  "MIXED_COMMUNITY_BRIDGE", "UNVERIFIED_CANDIDATE"}
MAX_ENTRY_BYTES = 4 * 1024 ** 3
MAX_SAMPLE_BYTES = 32 * 1024 ** 3


def normalize_name(name: str) -> str:
    name = name.replace("\\", "/")
    if not name or name.startswith("/") or "\x00" in name or any(ord(c) < 32 for c in name):
        raise ValueError("unsafe archive member path")
    parts = name.split("/")
    if any(p in ("", ".", "..") for p in parts) or ":" in parts[0]:
        raise ValueError("unsafe archive member path")
    return "/".join(parts)


def family(path: str) -> str:
    p = path.lower()
    n = PurePosixPath(p).name
    if n.startswith(("real_", "adrn_", "spr_", "spradrn_")) and n.endswith(".bin"):
        return "GRAPHICS_OR_ANIMATION_CONTAINER"
    if n.startswith(("battle_", "palet_")) or p.endswith((".sab", ".sap")):
        return "BATTLE_OR_PALETTE"
    if n.startswith(("sound_", "soundaddr_")) or p.endswith((".wav", ".mp3", ".ogg")):
        return "AUDIO"
    if p.endswith((".dat", ".map")) or "/map/" in "/" + p:
        return "POSSIBLE_MAP_OR_DATA"
    if p.endswith((".bmp", ".png", ".jpg", ".jpeg", ".gif")):
        return "LOOSE_IMAGE"
    if p.endswith((".exe", ".dll")):
        return "EXECUTABLE_DO_NOT_RUN"
    if any(x in n for x in ("npc", "quest", "pet", "enemy", "item", "skill")):
        return "NAMED_DATA_CANDIDATE_UNVERIFIED"
    return "OTHER"


def _sha_reader(reader) -> tuple[str, int]:
    h = hashlib.sha256()
    size = 0
    while True:
        chunk = reader.read(1024 * 1024)
        if not chunk:
            break
        size += len(chunk)
        if size > MAX_ENTRY_BYTES:
            raise ValueError("file exceeds safe inventory limit")
        h.update(chunk)
    return h.hexdigest(), size


def _members(root: Path, kind: str):
    if kind == "directory":
        if not root.is_dir() or root.is_symlink():
            raise ValueError("directory specimen missing or symlinked")
        for p in sorted(root.rglob("*")):
            if p.is_symlink():
                raise ValueError("symlink inside specimen refused")
            if p.is_file():
                if not p.resolve().is_relative_to(root.resolve()):
                    raise ValueError("file escapes specimen")
                name = normalize_name(p.relative_to(root).as_posix())
                with p.open("rb") as reader:
                    digest, size = _sha_reader(reader)
                yield name, digest, size
    elif kind == "zip":
        if not zipfile.is_zipfile(root):
            raise ValueError("ZIP specimen missing or unsupported")
        with zipfile.ZipFile(root) as zf:
            for info in sorted(zf.infolist(), key=lambda x: x.filename):
                name = normalize_name(info.filename.rstrip("/"))
                mode = (info.external_attr >> 16) & 0xFFFF
                if stat.S_ISLNK(mode):
                    raise ValueError("ZIP symlink refused")
                if info.is_dir():
                    continue
                if info.flag_bits & 1:
                    raise ValueError("encrypted ZIP not supported")
                if info.file_size > MAX_ENTRY_BYTES:
                    raise ValueError("ZIP entry exceeds safe inventory limit")
                with zf.open(info) as reader:
                    digest, size = _sha_reader(reader)
                if size != info.file_size:
                    raise ValueError("ZIP entry size mismatch")
                yield name, digest, size
    else:
        raise ValueError("supported specimen kinds: directory, zip")


def scan(spec: dict) -> dict:
    if spec.get("schema") != "stoneage.cross_version_input_r1":
        raise ValueError("unknown input schema")
    samples = spec.get("samples")
    if not isinstance(samples, list) or not samples:
        raise ValueError("at least one specimen required")
    ids = set()
    outputs = []
    groups = {}
    for s in samples:
        sid = s.get("sample_id")
        if not isinstance(sid, str) or not sid or sid in ids or len(sid) > 100:
            raise ValueError("empty, invalid or repeated sample ID")
        ids.add(sid)
        classification = s.get("source_class")
        if classification not in SOURCE_CLASSES:
            raise ValueError("unknown source class")
        if not isinstance(s.get("evidence_ref"), str) or not s["evidence_ref"].strip():
            raise ValueError("each specimen needs a provenance reference")
        root = Path(s["local_path"])
        kind = s.get("kind")
        files = []
        seen = set()
        total = 0
        for name, sha, size in _members(root, kind):
            alias = name.casefold()
            if alias in seen:
                raise ValueError("ambiguous duplicate case-insensitive path")
            seen.add(alias)
            total += size
            if total > MAX_SAMPLE_BYTES:
                raise ValueError("sample exceeds safe inventory limit")
            entry = {"path": name, "size": size, "sha256": sha, "family_hint": family(name)}
            files.append(entry)
            groups.setdefault((size, sha), []).append({"sample_id": sid, "path": name})
        files.sort(key=lambda x: x["path"])
        if not files:
            raise ValueError("specimen contains no regular files")
        manifest_hash = hashlib.sha256(json.dumps(
            [(x["path"], x["size"], x["sha256"]) for x in files],
            separators=(",", ":"), ensure_ascii=False).encode("utf-8")).hexdigest()
        outputs.append({"sample_id": sid, "source_class": classification,
                        "region": s.get("region"), "claimed_version": s.get("claimed_version"),
                        "evidence_ref": s["evidence_ref"], "kind": kind,
                        "file_count": len(files), "logical_file_bytes": total,
                        "manifest_sha256": manifest_hash, "files": files})
    duplicates = []
    for (size, sha), occurrences in sorted(groups.items(), key=lambda x: (x[0][0], x[0][1])):
        if len(occurrences) > 1:
            duplicates.append({"size": size, "sha256": sha, "occurrences": occurrences,
                               "cross_sample": len({x["sample_id"] for x in occurrences}) > 1})
    by_path = {}
    for sample in outputs:
        for f in sample["files"]:
            by_path.setdefault(f["path"].casefold(), []).append(
                (sample["sample_id"], f["sha256"], f["size"]))
    changed_paths = [
        {"normalized_path": path, "versions": [
            {"sample_id": sid, "sha256": sha, "size": size} for sid, sha, size in entries]}
        for path, entries in sorted(by_path.items())
        if len({sid for sid, _, _ in entries}) > 1
        and len({(sha, size) for _, sha, size in entries}) > 1
    ]
    return {"schema": "stoneage.cross_version_inventory_r1", "samples": outputs,
            "totals": {"samples": len(outputs),
                       "file_occurrences": sum(x["file_count"] for x in outputs),
                       "unique_exact_blobs": len(groups),
                       "cross_sample_duplicate_blobs": sum(
                           1 for x in duplicates if x["cross_sample"]),
                       "changed_same_path_count": len(changed_paths)},
            "exact_duplicate_groups": duplicates, "changed_same_path": changed_paths,
            "qualification": {"official_authenticity_inferred": False,
                              "semantic_identity_inferred": False,
                              "original_game_server_data_complete": False,
                              "proprietary_payload_exported": False}}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", type=Path, required=True, help="local JSON specimen list")
    ap.add_argument("--output", type=Path, required=True, help="metadata-only JSON output")
    a = ap.parse_args()
    result = scan(json.loads(a.input.read_text(encoding="utf-8")))
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8")
    print(json.dumps(result["totals"], sort_keys=True))


if __name__ == "__main__":
    main()
