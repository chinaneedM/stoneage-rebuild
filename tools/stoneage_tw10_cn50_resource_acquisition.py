#!/usr/bin/env python3
"""Reacquire two qualified original carriers to compare actual CN5 vs TW1 records.

All original game bytes remain transient in CI. Emit only pinned, derived facts.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
from tools.stoneage_stoneage5_msi_probe import load_root, find_entry
from tools.stoneage_stoneage5_cab_probe import iso_file_slice
from tools.stoneage_stoneage5_full_cab_acquisition import (
    EXPECTED_SIZE, checked_layout, download_cab, extracted_inventory, hash_file)
from tools.stoneage_tw10_technical_probe import find_rows, extract_row
from tools.stoneage_tw10_cn50_record_resource_diff import compare_directories, stream_sha256

CN50_SOURCE = "research/recovered/STONEAGE-STONEAGE5-REAL-CAB-PAYLOAD-R1.json"
TW10_SOURCE = "research/recovered/STONEAGE-TW10-CLIENT-INVENTORY-R1.txt"
CN50_NAMES = {
    "adrn": "adrn_31.bin", "real": "real_31.bin",
    "spradrn": "spradrn_17.bin", "spr": "spr_17.bin",
}
TW10_NAMES = {
    "adrn": "StoneAge/data/adrn_1.bin", "real": "StoneAge/data/real_1.bin",
    "spradrn": "StoneAge/data/spradrn_1.bin", "spr": "StoneAge/data/spr_1.bin",
}
TW10_BIN_BYTES = 523449360


def expected_source(root):
    report = json.loads((root / CN50_SOURCE).read_text(encoding="utf8"))
    if (report["status"] != "REAL_FULL_CAB_EXTRACTED_AND_413_FILES_HASHED" or
        report["files"]["count"] != 413 or
        report["source"]["cab_size"] != EXPECTED_SIZE):
        raise ValueError("uncertified-cn50-source")
    source = {
        row["name"]: (row["size"], row["sha256"])
        for row in report["files"]["inventory"]
    }
    if len(source) != 413:
        raise ValueError("ambiguous-cn50-source")
    tw10 = {}
    for line in (root / TW10_SOURCE).read_text(encoding="utf8").splitlines():
        if line.startswith("CORE_FILE|"):
            row = dict(v.split("=", 1) for v in line.split("|")[1:] if "=" in v)
            tw10[row["path"]] = (int(row["size"]), row["sha256"])
    if len(tw10) != 383:
        raise ValueError("incomplete-original-tw10-manifest")
    return report, source, tw10


def validate_pinned_target(path, name, reference):
    if name not in reference:
        raise ValueError("unregistered-source-path")
    size, digest = reference[name]
    got_sha, got_size = hash_file(path)
    if (got_size, got_sha) != (size, digest):
        raise ValueError("actual-extracted-resource-does-not-match-source-pin:" + name)
    return {"file": name, "bytes": got_size, "sha256": got_sha}


def verified_tw10_extract(bin_path, target_dir, reference):
    if Path(bin_path).stat().st_size != TW10_BIN_BYTES:
        raise ValueError("tw10-disc-file-size-not-pinned")
    image, rows, layout, joliet = find_rows(str(bin_path))
    try:
        by_name = {r["path"]: r for r in rows if not r["is_dir"]}
        manifest = {}
        for key, name in TW10_NAMES.items():
            if name not in by_name:
                raise ValueError("missing-original-tw10-target:" + name)
            out = target_dir / (key + ".bin")
            extract_row(image, by_name[name], out)
            manifest[key] = validate_pinned_target(out, name, reference)
    finally:
        image.close()
    return manifest, {"layout": layout, "joliet": bool(joliet)}


def acquire_and_compare(bin_path, output):
    root = Path(__file__).resolve().parents[1]
    cn50_manifest, cn50_known, tw10_known = expected_source(root)
    meta, cue_name, cue_bytes, track, bin_row, bin_url, optical, entries = load_root()
    cab = find_entry(entries, "DATA1.CAB")
    if cab is None or int(cab["size"]) != EXPECTED_SIZE:
        raise ValueError("missing-real-cn50-cab")
    prefix, status, _ = iso_file_slice(bin_url, cab, track, 0, 65536)
    if status != 206:
        raise ValueError("cn50-no-range-source")
    header, files = checked_layout(prefix)
    with tempfile.TemporaryDirectory(prefix="stoneage-cn50-tw10-record-") as scratch:
        temp = Path(scratch)
        cabfile = temp / "DATA1.CAB"
        digest = download_cab(bin_url, cab, track, int(bin_row["size"]), cabfile)
        if digest != cn50_manifest["source"]["cab_sha256"]:
            raise ValueError("downloaded-cab-source-sha256-mismatch")
        with cabfile.open("rb") as f:
            if f.read(len(prefix)) != prefix:
                raise ValueError("original-cab-prefix-mismatch")
        expanded = temp / "cab"
        expanded.mkdir()
        run = subprocess.run(["cabextract", "-q", "-d", str(expanded), str(cabfile)],
                             capture_output=True, text=True, check=False, timeout=1500)
        if run.returncode != 0:
            raise ValueError("untrusted-cabextract-failed")
        rows = extracted_inventory(expanded, files)
        if len(rows) != 413:
            raise ValueError("incomplete-full-cab-record-extraction")
        for row in rows:
            if cn50_known.get(row["name"]) != (row["size"], row["sha256"]):
                raise ValueError("cn50-source-manifest-differs")
        # CAB entries use internal MSI file keys. Four container names are
        # literal CAB keys, all source-pinned individually.
        original_cn50 = {}
        for key, name in CN50_NAMES.items():
            original_cn50[key] = validate_pinned_target(expanded / name, name, cn50_known)
        old = temp / "tw10"
        old.mkdir()
        tw_manifest, tw_disc = verified_tw10_extract(bin_path, old, tw10_known)
        # Expose consistent short filenames without copying large original files.
        latest = temp / "cn50"
        latest.mkdir()
        for key, name in CN50_NAMES.items():
            (latest / (key + ".bin")).symlink_to(expanded / name)
        diff = compare_directories(old, latest)
        diff.update({
            "source_claims": {
                "TW10": {"class": "ACCEPTED_RETAIL_DISC_CLIENT", "files": tw_manifest,
                         "disc_image_bytes": TW10_BIN_BYTES, "disc_structure": tw_disc},
                "CN50": {"class": "PRESERVED_OPTICAL_INSTALLER_IDENTITY_PROVEN_BY_INTERNAL_MSI",
                         "official_clean_release_mastering_authenticated": False,
                         "cab_sha256": digest,
                         "files": original_cn50,
                         "carrier_catalogue_sha1_not_rehashed": bin_row.get("sha1")},
            },
            "result": "DERIVED_RECORD_LEVEL_DIFF_OF_REACQUIRED_ORIGINAL_RESOURCE_BYTES",
            "prerequisites": {
                "cn50_source_report": CN50_SOURCE,
                "tw10_original_manifest": TW10_SOURCE,
                "cn50_413_files_rehashed_again": True,
                "old_tw10_four_files_rehashed_again": True,
                "cn50_durable_original_bytes_stored": False,
                "tw10_durable_original_bytes_stored_here": False,
            },
        })
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(diff, ensure_ascii=False, sort_keys=True, indent=2)
                          + "\n", encoding="utf8")
        for name, family in diff["families"].items():
            c = family["comparison"]
            print(f"REAL_RECORD_DIFF|family={name}|original_ids={c['old_total_ids']}|"
                  f"new_ids={c['new_total_ids']}|shared_unique={c['common_unique_id_count']}|"
                  f"exact_payload={c['exact_payload_or_segment_count']}|"
                  f"changed_payload={c['changed_payload_or_segment_count']}|"
                  f"new_id_count={c['new_unique_ids_absent_in_old_count']}|"
                  f"missing_id_count={c['old_unique_ids_absent_in_new_count']}", flush=True)
        return diff


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tw-bin", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    acquire_and_compare(args.tw_bin, args.output)


if __name__ == "__main__":
    main()
