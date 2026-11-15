#!/usr/bin/env python3
"""Verify a privately held official archived GIF against PET21/PET22 known SHA.

This tool never downloads, copies, publishes, or logs the actual proprietary
image bytes. A successful check proves only file identity to an archived web
response, NOT an original game species/client ID or redistribution rights.
"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "research/recovered/STONEAGE-PET-MODULE-22-JP-124-ARCHIVED-IMAGE-RECOVERY-R1.json"
LIMIT = 256_000


def verify_private_file(ordinal, path, receipt):
    if not 1 <= ordinal <= 124:
        raise ValueError("official webpage ordinal outside range")
    matches = [r for r in receipt["records"] if r["web_ordinal"] == ordinal]
    if len(matches) != 1:
        raise ValueError("source receipt position missing or duplicated")
    source = matches[0]
    expected = source["best_archival_observation_sha256_or_null"]
    if expected is None:
        raise ValueError("no observed original GIF SHA for that webpage position")
    if path.stat().st_size > LIMIT:
        raise ValueError("private candidate file exceeds accepted image byte limit")
    body = path.read_bytes()
    if not (body.startswith((b"GIF87a", b"GIF89a")) and len(body) >= 10):
        raise ValueError("private candidate is not an original-format GIF")
    dimensions = [int.from_bytes(body[6:8], "little"), int.from_bytes(body[8:10], "little")]
    if dimensions != [60, 65]:
        raise ValueError("private candidate GIF dimensions mismatch source batch")
    digest = hashlib.sha256(body).hexdigest()
    if digest != expected:
        raise ValueError("private GIF SHA mismatch: NOT archived image identity")
    return {
        "status": "PRIVATE_ORIGINAL_WEB_GIF_SHA_MATCH_CONFIRMED",
        "operator_web_ordinal": ordinal,
        "original_gif_sha256": digest,
        "original_gif_bytes": len(body),
        "original_gif_dimensions": dimensions,
        "archive_capture": source["best_archival_observation_capture_or_null"],
        "client_sprite_or_pet_species_ID_verified": False,
        "public_media_license_verified": False,
        "file_uploaded_or_modified": False,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--ordinal", type=int, required=True)
    p.add_argument("--file", type=Path, required=True)
    args = p.parse_args()
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    print(json.dumps(verify_private_file(args.ordinal, args.file, receipt),
                     ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
