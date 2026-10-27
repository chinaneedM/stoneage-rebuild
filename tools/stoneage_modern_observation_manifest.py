"""Metadata-only source-boundary contract for the modern *research* observer.

The real original game is NOT booted by this module. Raw regional encodings,
regional release/build facts and production Simplified Chinese display are
deliberately separate. No client/game/assets are bundled into public Git.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import struct
import wave

SCHEMA = "stoneage.modern_observation.metadata_r1"
UI_LANGUAGE = "zh-CN"
SOURCE_PROFILES = {
    "TW_WAEI_1_0": {"region": "TW", "label": "台湾 Waei/JSS 1.0", "status": "ACCEPTED_CLEAN_RETAIL_CLIENT"},
    "CN_MAINLAND": {"region": "CN", "label": "大陆版本", "status": "SPECIFIC_BUILD_REQUIRED"},
    "JP_JSS": {"region": "JP", "label": "日本版本", "status": "SPECIFIC_BUILD_REQUIRED"},
    "KR_KOREA": {"region": "KR", "label": "韩国版本", "status": "SPECIFIC_BUILD_REQUIRED"},
    "LATER_RECOVERED": {"region": "MIXED", "label": "后期社区保存材料", "status": "NOT_OFFICIAL_ORIGINAL_BY_DEFAULT"},
}
TYPES = {"map_png", "character_png", "pet_png", "wav"}
CLAIM = "OFFLINE_ASSET_PREVIEW_NOT_AUTHENTIC_GAMEPLAY"
CUSTODY = "USER_LOCAL_FILES_REQUIRE_INDEPENDENT_ORIGINAL_SOURCE_ATTESTATION"
MAX_SIZE = 100 * 1024 * 1024


def _must(condition: bool, problem: str) -> None:
    if not condition:
        raise ValueError(problem)


def file_fingerprint(path: Path, kind: str) -> dict:
    """Read local file only, recognize minimal PNG/WAV shape, never return bytes."""
    _must(kind in TYPES, "unsupported asset kind")
    path = path.expanduser().resolve(strict=True)
    _must(path.is_file() and 0 < path.stat().st_size <= MAX_SIZE, "unsafe asset file size")
    _must(path.suffix.lower() == (".wav" if kind == "wav" else ".png"), "unexpected asset suffix")
    sha = hashlib.sha256()
    with path.open("rb") as stream:
        signature = stream.read(32)
        stream.seek(0)
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            sha.update(chunk)
    meta = {"kind": kind, "filename": path.name, "size_bytes": path.stat().st_size,
            "sha256": sha.hexdigest(), "evidence_grade": CUSTODY}
    if kind == "wav":
        with wave.open(str(path), "rb") as f:
            _must(f.getnchannels() in (1, 2) and f.getframerate() > 0, "invalid WAV")
            meta["wav"] = {"channels": f.getnchannels(), "hz": f.getframerate(),
                           "frames": f.getnframes(), "sample_width": f.getsampwidth()}
    else:
        _must(signature.startswith(b"\x89PNG\r\n\x1a\n") and signature[12:16] == b"IHDR",
              "invalid PNG header")
        width, height = struct.unpack(">II", signature[16:24])
        _must(0 < width <= 8192 and 0 < height <= 8192 and width * height <= 8000000,
              "unbounded PNG dimensions")
        meta["png"] = {"width": width, "height": height}
    return meta


def report(profile: str, entries: list[tuple[str, Path]]) -> dict:
    _must(profile in SOURCE_PROFILES, "unknown source profile")
    _must(0 < len(entries) <= 64, "no files or too many files")
    _must(len({(kind, str(path)) for kind, path in entries}) == len(entries), "duplicate asset slot")
    files = [file_fingerprint(path, kind) for kind, path in entries]
    _must(len({(f["kind"], f["filename"]) for f in files}) == len(files),
          "ambiguous duplicated original filename")
    return {
        "schema": SCHEMA,
        "display_language": UI_LANGUAGE,
        "source_profile": profile,
        "source_metadata": SOURCE_PROFILES[profile],
        "observation_class": CLAIM,
        "files": files,
        "original_executable_launched": False,
        "original_world_entered": False,
        "original_server_data_authenticated": False,
        "asset_version_provenance_authenticated": False,
        "historical_NPC_pet_quest_binding_authenticated": False,
        "modern_rendered_movement": "MANUAL_VISUAL_REFERENCE_ONLY",
        "region_text_production_translation_verified": False,
    }


def validate_report(data: dict) -> None:
    _must(data["schema"] == SCHEMA and data["display_language"] == UI_LANGUAGE,
          "modern display language/schema contract")
    profile = data["source_profile"]
    _must(profile in SOURCE_PROFILES and data["source_metadata"] == SOURCE_PROFILES[profile],
          "source profile must never be recast")
    _must(data["observation_class"] == CLAIM and len(data["files"]) <= 64 and data["files"],
          "authentic client display promotion or invalid count")
    for false_field in ("original_executable_launched", "original_world_entered",
                        "original_server_data_authenticated", "asset_version_provenance_authenticated",
                        "historical_NPC_pet_quest_binding_authenticated",
                        "region_text_production_translation_verified"):
        _must(data[false_field] is False, "unsupported original/translation claim: " + false_field)
    _must(data["modern_rendered_movement"] == "MANUAL_VISUAL_REFERENCE_ONLY",
          "synthetic movement promoted to observed original")
    for file in data["files"]:
        _must(file["kind"] in TYPES and file["evidence_grade"] == CUSTODY, "source asset evidence promotion")
        _must(len(file["sha256"]) == 64 and all(c in "0123456789abcdef" for c in file["sha256"]),
              "invalid SHA256")


def main() -> None:
    parser = argparse.ArgumentParser(description="No-network, metadata-only regional original asset observer")
    parser.add_argument("--profile", choices=SOURCE_PROFILES, required=True)
    parser.add_argument("--map", type=Path)
    parser.add_argument("--character", type=Path, action="append", default=[])
    parser.add_argument("--pet", type=Path, action="append", default=[])
    parser.add_argument("--wav", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    options = parser.parse_args()
    original = []
    if options.map:
        original.append(("map_png", options.map))
    original.extend(("character_png", p) for p in options.character)
    original.extend(("pet_png", p) for p in options.pet)
    if options.wav:
        original.append(("wav", options.wav))
    result = report(options.profile, original)
    validate_report(result)
    dest = options.output.expanduser().resolve()
    root = Path(__file__).resolve().parents[1]
    _must(dest.suffix.lower() == ".json" and dest.parent.is_dir() and
          dest != root and root not in dest.parents,
          "metadata output must be outside public repository")
    with dest.open("x", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("PRIVATE_OBSERVATION_METADATA_WRITTEN=", str(dest))
    print("THIS_IS_NOT_ORIGINAL_GAME_EXECUTION_OR_AUTHENTIC_WORLD_ENTRY")


if __name__ == "__main__":
    main()
