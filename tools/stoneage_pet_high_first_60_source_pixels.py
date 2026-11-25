"""Verify the bounded PET59 remainder against the saved Taiwanese 8.5 files."""

import argparse
from collections import Counter
import json
from pathlib import Path

from tools import stoneage_pet_high_first_tw85_pixels as pixels


ROOT = pixels.ROOT
PETS = ROOT / "research/pets"
COVERAGE = PETS / "PET-HIGH-FIRST-57-RESIDUAL-VISUAL-COVERAGE-R1.json"
REMAINDER = PETS / "PET-HIGH-FIRST-59-RESIDUAL-PIXEL-RECEIPTS-R1.json"
CARRIER = ROOT / "research/recovered/STONEAGE-WAYI85-MSI-CLIENT-PAYLOAD-R1.json"
TARGET = PETS / "PET-HIGH-FIRST-60-TW85-REMAINING-PIXELS-R1.json"
PINS = {
    **pixels.PINS,
    COVERAGE: "c291a0a597ba1b6270191c561f10401293df161e",
    REMAINDER: "f8083ef6db6f6b2ac057a7b4c440fad5c0dde3a4",
    CARRIER: "18a68c9d4275763ef0ed7a347cca940cffe0fee2",
}


def load(path):
    return json.loads(path.read_bytes())


def build_plan():
    for path, digest in PINS.items():
        if pixels.git_blob(path.read_bytes()) != digest:
            raise ValueError(f"archived input changed: {path.name}")
    pending = load(REMAINDER)["summary"]["groups_without_complete_sample_in_compared_receipts"]
    coverage = load(COVERAGE)
    groups = {}
    for row in coverage["rows"]:
        for group in row["tw85_physical_groups"]:
            index = group["group_index"]
            if index in pending:
                identity = (group["graphic"], group["segment_sha256"])
                if groups.setdefault(index, identity) != identity:
                    raise ValueError(f"conflicting SPR group identity: {index}")
    sequences = pixels.select_sequences(groups)
    frames = [frame[0] for seq in sequences for frame in seq["frames"] if frame[0] is not None]
    if ([seq["physical_group"] for seq in sequences] != pending or
            (len(sequences), len(frames), len(set(frames))) != (20, 160, 123)):
        raise ValueError("PET59 remaining sequence coverage changed")
    return {"portrait_alias_to_saved_tw85_native_rd_candidates": {}}, [], [], sequences


def summarize_carrier(acquisition):
    inspection = acquisition["inspection"]
    if (acquisition["status"] != "MSI_CLIENT_PAYLOAD_ACQUISITION_AND_INVENTORY_COMPLETE" or
            inspection["installed_or_executed"] is not False):
        raise ValueError("expected statically extracted MSI payload")
    return {
        "parts": [{k: part[k] for k in ("part", "filename", "bytes", "sha256")}
                  for part in acquisition["parts"]],
        "assembled_installer": acquisition["assembled_installer"],
        "msi_sha256": inspection["msi_sha256"],
    }


def verify(report, plan):
    pins = {str(path.relative_to(ROOT)): sha for path, sha in PINS.items()}
    if (report["schema"] != "stoneage.pet60.tw85_remaining_indexed_pixels.r1" or
            report["source_git_blobs"] != pins or
            report["carrier"] != summarize_carrier(load(CARRIER))):
        raise ValueError("exact archive or source attribution changed")
    if any(report[key] is not False for key in
           ("official_release_verified", "native_runtime_verified", "original_assets_published")):
        raise ValueError("unsupported publication, release, or runtime claim")
    observation = report["observations"]
    summary = pixels.verify(observation, plan)
    status = {int(bitmap): observation["observed_blocks"][str(index)]["status"]
              for bitmap, index in observation["frame_bitmap_to_adrn_index"].items()}
    bad_by_group = {}
    for sequence in plan[3]:
        bad = sorted({frame[0] for frame in sequence["frames"]
                      if frame[0] is not None and status[frame[0]] != "DUAL_DECODED_INDEX_PIXELS"})
        if bad:
            bad_by_group[str(sequence["physical_group"])] = bad
    return {
        "target_groups": summary["sampled_groups"],
        "complete_groups": summary["sampled_groups_fully_decoded"],
        "non_sentinel_positions": sum(frame[0] is not None for seq in plan[3] for frame in seq["frames"]),
        "unique_bitmaps": summary["sampled_physical_frame_blocks"],
        "block_status": dict(Counter(status.values())),
        "incomplete_groups_and_bitmaps": bad_by_group,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan-only", action="store_true")
    parser.add_argument("--source-dir", type=Path)
    parser.add_argument("--acquisition", type=Path)
    parser.add_argument("--receipt", type=Path, default=TARGET)
    args = parser.parse_args()
    if bool(args.source_dir) != bool(args.acquisition) or (args.plan_only and args.source_dir):
        parser.error("use --plan-only or provide both --source-dir and --acquisition")
    plan = build_plan()
    if args.plan_only:
        print(json.dumps({"groups": [seq["physical_group"] for seq in plan[3]],
                          "positions": 160, "unique_bitmaps": 123}, sort_keys=True))
        return
    if args.source_dir:
        acquisition = load(args.acquisition)
        carrier = summarize_carrier(acquisition)
        if carrier != summarize_carrier(load(CARRIER)):
            raise ValueError("downloaded carrier differs from the prior authenticated sample")
        report = {
            "schema": "stoneage.pet60.tw85_remaining_indexed_pixels.r1",
            "source_git_blobs": {str(path.relative_to(ROOT)): sha for path, sha in PINS.items()},
            "carrier": carrier,
            "observations": pixels.inspect(args.source_dir, plan),
            "official_release_verified": False,
            "native_runtime_verified": False,
            "original_assets_published": False,
        }
        summary = verify(report, plan)
        args.receipt.write_text(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                                encoding="utf-8")
    else:
        summary = verify(load(args.receipt), plan)
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
