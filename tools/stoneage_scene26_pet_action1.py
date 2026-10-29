#!/usr/bin/env python3
"""SCENE26: rederive bounded pet action=1 sprite sequences from pinned, published R40 reports.

No original proprietary sprite, image, audio or server file is retrieved or executed.
"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = "research/recovered/STONEAGE-PRESERVED-PET-SPR-SOURCE-R40.json"
XREF = "research/recovered/STONEAGE-PRESERVED-PET-SPR-MATERIAL-R40.json"
OUT = "research/recovered/STONEAGE-SCENE26-PET-ACTION1-DERIVED-R1.json"
SRC_BLOB = "5b49d54d7cff2d79d3610db7ca4a37108f1f9e03"
XREF_BLOB = "cdcfc9fb9a07c60a3320528fdddcdfecdeb6b14d"
BASE_HEAD = "fd16de29f24934629559ba8c404e05c180d36259"
BASE_TREE = "1280a6585ec3f391a2e4366845427601670f1cbc"
EXPECTED_GRAPHICS = (100250, 100251, 100252)


def git_blob_sha(content: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(content)).encode() + b"\0" + content).hexdigest()


def load_pinned(relpath: str, expected_blob: str, root: Path = ROOT) -> dict:
    data = (root / relpath).read_bytes()
    if git_blob_sha(data) != expected_blob:
        raise ValueError(f"source Git blob changed: {relpath}")
    return json.loads(data.decode("utf-8"))


def derive(source: dict, cross: dict) -> dict:
    if source.get("schema") != "stoneage.preserved_pet_spr_source.r40":
        raise ValueError("unrecognized primary report schema")
    if source.get("source_scope") != cross.get("source_scope"):
        raise ValueError("source-scope disagreement")
    gs = source["material"]["selected_groups"]
    xs = cross["full_segment_comparisons"]
    if len(gs) != len(EXPECTED_GRAPHICS) or len(xs) != len(gs):
        raise ValueError("group count mismatch")
    groups, rows = [], []
    for i, expected in enumerate(EXPECTED_GRAPHICS):
        g, p = gs[i], xs[i]
        if g["spr_no"] != expected or p["spr_no"] != expected:
            raise ValueError("graphic ordering changed")
        if g["group_index"] != p["client_group_index"] or g["segment_sha256"] != p["segment_sha256"]:
            raise ValueError("cross-report group conflict")
        refs = {}
        for region in ("TW10", "CN50"):
            v = p["reference_occurrences"][region]
            if len(v) != 1 or not v[0]["exact_full_segment_equal"] or v[0]["index"] != g["group_index"] or v[0]["segment_sha256"] != g["segment_sha256"]:
                raise ValueError(f"cross-version equality unsupported: {expected}/{region}")
            refs[region] = {"index": v[0]["index"], "exact_full_segment_equal": True}
        animations = sorted((a for a in g["animations"] if a["anim_no"] == 1), key=lambda a: a["direction"])
        if len(animations) != 8 or [a["direction"] for a in animations] != list(range(8)):
            raise ValueError("missing/duplicate direction")
        seq = []
        for a in animations:
            frames = a["frames"]
            if a["frame_count"] != len(frames) or a["duration"] != 100 or not frames or any(
                len(f) != 4 or any(type(value) is not int for value in f) for f in frames
            ):
                raise ValueError("corrupt frame fields or duration")
            pattern = [frames[0][0]] * 3 + [frames[-1][0]] if i < 2 else [frames[0][0], frames[-1][0]]
            if [f[0] for f in frames] != pattern or any(f[3] != 0 for f in frames):
                raise ValueError("unexpected repeated-frame or sound pattern")
            seq.append({
                "direction": a["direction"], "source_animation_index": a["index"],
                "header_offset": a["header_offset"], "end_offset": a["end_offset"],
                "duration_word": a["duration"], "frames": frames
            })
        groups.append({
            "spr_no": g["spr_no"], "group_index": g["group_index"],
            "full_segment_sha256": g["segment_sha256"],
            "source_animation_count": g["anim_count"],
            "cross_reference_full_segment_equal": refs,
            "action_code": 1, "directions": seq
        })
        rows.extend((g["spr_no"], x) for x in seq)
    pixels = [f for _, seq in rows for f in seq["frames"]]
    result = {
        "schema": "stoneage.scene26.pet_action1.derived.r1",
        "baseline_main": BASE_HEAD, "baseline_tree": BASE_TREE,
        "material_scope": "PRESERVED_MIXED25_SOURCE_DERIVED_METADATA_NOT_ORIGINAL_RUNTIME",
        "source_R40": {"path": SRC, "git_blob": SRC_BLOB, "reported_source_scope": source["source_scope"]},
        "crossversion_R40": {"path": XREF, "git_blob": XREF_BLOB},
        "action_code": 1, "groups": groups,
        "counts": [
            {
                "spr_no": g["spr_no"], "directions": len(g["directions"]),
                "frame_occurrences": sum(len(a["frames"]) for a in g["directions"]),
                "distinct_bitmap_numbers": len({f[0] for a in g["directions"] for f in a["frames"]})
            } for g in groups
        ],
        "summary": {
            "group_count": len(groups), "direction_sequences": len(rows),
            "frame_occurrences": len(pixels),
            "distinct_bitmap_numbers": len({f[0] for f in pixels}),
            "zero_sound_field_occurrences": sum(f[3] == 0 for f in pixels)
        },
        "interpretation": {
            "source_animation_bytes_newly_acquired": False, "raw_sprite_pixels_read_this_package": False,
            "actual_original_visual_rendering": False, "original_action_name_authenticated": False,
            "original_native_duration_units_authenticated": False, "pet_species_identity_authenticated": False,
            "commercial_deployed_build_equivalence": False, "original_game_executed": False,
            "original_world_entered": False, "Stage_A": "SEVEN_PARTIAL_TWO_OPEN",
            "Stage_B_and_wiki": "GATED", "R79": "PAUSED_NON_BLOCKING",
            "overall_restoration_percentage": None
        }
    }
    if result["summary"] != {
        "group_count": 3, "direction_sequences": 24,
        "frame_occurrences": 80, "distinct_bitmap_numbers": 48,
        "zero_sound_field_occurrences": 80
    } or [x["frame_occurrences"] for x in result["counts"]] != [32, 32, 16]:
        raise ValueError("SCENE26 totals unexpectedly changed")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="assert publication equals strict source recomputation")
    args = parser.parse_args()
    value = derive(load_pinned(SRC, SRC_BLOB), load_pinned(XREF, XREF_BLOB))
    output = ROOT / OUT
    if args.check:
        if json.loads(output.read_text(encoding="utf-8")) != value:
            raise SystemExit("SCENE26 published record differs from pinned original-source derivation")
        print("SCENE26 source replay PASS: 3 groups, 24 directions, 80 frames, 48 bitmaps; no runtime/identity promotion")
    else:
        print(json.dumps(value, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
