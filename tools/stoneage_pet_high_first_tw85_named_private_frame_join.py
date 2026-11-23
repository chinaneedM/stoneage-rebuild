"""PET10: match previously privately decoded TW85 original frames to a later-proved local PC name.

This is a source-only historical crosswalk, NOT a new pixel decode or official
live species claim. Previously observed commercial PNGs stay outside public Git.
"""
from __future__ import annotations
import argparse
from copy import deepcopy
import json
from pathlib import Path
from tools.stoneage_pet_high_first_cn50_catalog import git_blob

ROOT = Path(__file__).resolve().parents[1]
INPUTS = {
    "pet09": ("research/pets/PET-HIGH-FIRST-TW85-VISUAL-ACTION-REFERENCES-R1.json", "3bcfbba98cfb915b14679ba472dbc554db297018"),
    "plan": ("research/recovered/tw85-rd-private-r30/PLAN-R30.json", "59bbb09d55c33076e1616499a2710c8de588dcee"),
    "source": ("research/recovered/tw85-rd-private-r30/SOURCE-R30.json", "9fb54267a59561ce8b1dfaa387b857f17a94a896"),
    "receipt": ("research/recovered/tw85-rd-private-r30/R30-PUBLIC-CUSTODY.json", "58f2c64cb795a7ef7c418f8b7733585bc0217dc0"),
}
TARGET = ROOT / "research/pets/PET-HIGH-FIRST-TW85-NAMED-PRIVATE-FRAMES-R1.json"
EXECUTABLES = ("sa.exe", "sb.exe", "sc.exe", "sd.exe")


def require(ok, description):
    if not ok:
        raise ValueError(description)


def load():
    out = {}
    for name, (path, sha) in INPUTS.items():
        f = ROOT / path
        require(f.is_file() and git_blob(f.read_bytes()) == sha, "source Git pin failed " + name)
        out[name] = json.loads(f.read_text(encoding="utf-8"))
    return out


def build(source_data=None):
    src = deepcopy(load() if source_data is None else source_data)
    p, plan, old, receipt = (src[k] for k in INPUTS)
    sample = plan["sample"]
    require(p["schema"] == "stoneage.pet.high_first_09.tw85_source_visual_action_reference.r1", "PET09 identity")
    require(plan["schema"] == "stoneage.tw85_original_private_rd_visual_sample_plan.r30", "R30 plan identity")
    require(old["schema"] == "stoneage.tw85_original_rd_private_gray_sample.r30", "R30 observed identity")
    require(receipt["schema"] == "stoneage.tw85_r30_source_private_visual_public_custody.r1", "R30 receipt")
    require(sample == old["sample"], "previous original plan differs from actual source record")
    require(plan["source_claim"] == old["source_claim"] ==
            "UNVERIFIED_COMMUNITY_PRESERVED_CLAIMED_TW85_SAME_557_FILE_MSI_CARRIER", "source carrier claim drift")
    require(receipt["status"] == "SOURCE_AND_PRIVATE_DECRYPTED_VISUAL_MATERIAL_ACCEPTED"
            and receipt["source_run"] == 40329157425
            and receipt["actual_original_rd_decoded_count"] == 8
            and receipt["source_index_hash_all_8_exact"] is True
            and receipt["pet_species_or_npc_identity_verified"] is False
            and receipt["client_original_program_executed"] is False
            and receipt["private_png_publicly_uploaded"] is False, "previous acceptance scope changed")
    require(old["observer_bounded_result"] ==
            "ACTUAL_SOURCE_RD_BYTES_DECODED_TO_ORIGINAL_INDEX_VALUES_IN_GRAY_PRIVATE_PREVIEW"
            and old["named_pet_or_avatar_verified"] is False, "old visual evidence was not a named pet")
    require((sample["original_spr_no"], sample["source_group_index"],
             sample["original_animation_index"], sample["original_direction_numeric"],
             sample["original_action_numeric"], sample["original_duration_word"]) ==
            (101501, 1185, 1, 0, 2, 1000), "original animation identity changed")
    rows = [x for x in p["records"] if x["tw85_original_spr_no_not_official_pet_id"] == 101501]
    require(len(rows) == 1, "named graphic missing or repeated")
    sprite = rows[0]
    matches = [g for g in sprite["original_physical_sprite_occurrences"]
               if g["original_source_group_index"] == sample["source_group_index"]]
    require(len(matches) == 1, "original physical group missing or repeated")
    group = matches[0]
    require(group["original_full_spr_segment_sha256"] == sample["source_group_full_spr_segment_sha256"],
            "R30 actual decoded original SPR SHA does not match native name SPR")
    require(group["all_frame_bitmap_references_qualified_in_same_saved_carrier"],
            "original frame bitmap references not source qualified")
    action = [x for x in group["raw_animation_index_frame_counts"]
              if x["original_raw_index"] == sample["original_animation_index"]]
    require(len(action) == 1 and action[0]["frame_positions"] == 8, "original raw animation frame count mismatch")
    lanes = sprite["original_native_program_routes"]
    require(set(lanes) == set(EXECUTABLES) and not sprite["cross_executable_name_conflict"],
            "original executable name lanes absent/conflicting")
    for filename in EXECUTABLES:
        one = lanes[filename]
        require((one["status"], one["local_album_slot"], one["original_first_i32"],
                 one["original_name_cp950"], one["source_portrait_alias"],
                 one["original_28b_record_sha256"], one["historical_official_live_release_verified"]) ==
                ("SOURCE_LOCAL_NAMED_ROUTE", 362, 305, "雷帝斯洛", 28429,
                 "345badea451ccb6a9f91c559532a9afe622409089b87daeaa6db1d2bf0d712bf", False),
                "original executable name route changed " + filename)
    portrait = p["portrait_alias_to_saved_tw85_native_rd_candidates"]["28429"]
    require(len(portrait) == 1 and len(portrait[0]["native_exact_candidates"]) == 1,
            "original portrait source ambiguity")
    x = portrait[0]
    native = x["native_exact_candidates"][0]
    require(x["physical_bitmapno"] == native["bitmapno"] == 303372
            and native["width"] == 96 and native["height"] == 104
            and x["saved_tw85_real_rd_sha256"] == native["rd_sha256"] ==
            "fa9ddb2acabd1a5bf03be3d6b08ee079ccf36badaaf70558d8d817aafc04523c"
            and x["patch_to_native_qualification"] == "EXACT_NATIVE_RECORD_AND_RD_STRUCTURE"
            and x["renderer_default_choice_proven"] is False, "portrait alias RD evidence changed")
    actual = sample["sample_frames"]
    decoded = old["frames"]
    require(len(actual) == len(decoded) == 8, "old actual pixel frames count changed")
    require([z["bitmapno"] for z in actual] ==
            receipt["original_bitmapnos"] == [z["bitmapno"] for z in decoded],
            "bitmap order drift")
    require([z["rd_block_sha256"] for z in actual] ==
            receipt["original_RD_sha256"] == [z["source_RD_sha256"] for z in decoded],
            "original RD content hash drift")
    require([z["private_png_sha256"] for z in decoded] ==
            receipt["private_grayscale_png_sha256"], "original private pixel evidence drift")
    frames = []
    for idx, (one, two) in enumerate(zip(actual, decoded, strict=True)):
        require(one["index_in_animation"] == two["index"] == idx
                and one["bitmapno"] == two["bitmapno"]
                and one["native_adrn_record_sha256"] == two["source_record_sha256"]
                and (one["width"], one["height"]) == (two["width"], two["height"])
                and (one["pos_x"], one["pos_y"], one["raw_sound_word"]) ==
                (two["original_sprite_x"], two["original_sprite_y"], two["raw_sound_word"]),
                "actual original frame record mismatch")
        require(len(two["private_png_sha256"]) == len(two["source_palette_index_sha256"]) == 64,
                "missing previously observed pixel hash")
        frames.append({
            "frame_index": idx, "original_bitmapno": one["bitmapno"],
            "source_width": one["width"], "source_height": one["height"],
            "source_adrn_sha256": one["native_adrn_record_sha256"],
            "source_rd_sha256": one["rd_block_sha256"],
            "previously_private_decoded_index_pixel_sha256": two["source_palette_index_sha256"],
            "previously_private_observed_gray_png_sha256": two["private_png_sha256"],
        })
    return {
        "schema": "stoneage.pet.high_first_10.tw85_named_previously_private_decoded_frames.r1",
        "date": "2026-11-23",
        "scope": "CLASSIC_PC_ONLY",
        "source_git_blob_pins": {key: {"path": info[0], "blob_sha": info[1]}
                                 for key, info in INPUTS.items()},
        "local_source_entry_key": "TW85-SOURCE-SPR-101501",
        "original_client_local_name_cp950": "雷帝斯洛",
        "original_executable_routes": {
            f: {"name": lanes[f]["original_name_cp950"],
                "slot": lanes[f]["local_album_slot"],
                "name_row_sha256": lanes[f]["original_28b_record_sha256"],
                "portrait_logical_alias": lanes[f]["source_portrait_alias"]}
            for f in EXECUTABLES},
        "original_spr_graphic_number_not_official_pet_id": sample["original_spr_no"],
        "original_spr_physical_index": sample["source_group_index"],
        "original_spr_full_segment_sha256": sample["source_group_full_spr_segment_sha256"],
        "raw_animation_index": sample["original_animation_index"],
        "raw_direction_word": sample["original_direction_numeric"],
        "raw_action_word": sample["original_action_numeric"],
        "raw_duration_word": sample["original_duration_word"],
        "previously_privately_decoded_original_frames": frames,
        "original_portrait_source": {
            "logical_alias": 28429, "physical_original_bitmapno": 303372,
            "source_rd_sha256": x["saved_tw85_real_rd_sha256"],
            "source_dimensions": [96, 104],
            "already_privately_decoded_portrait_pixels": False,
            "original_runtime_default_portrait_selector_proven": False,
        },
        "evidence_limits": {
            "earlier_private_pixel_observation_run": receipt["source_run"],
            "previous_original_palette_indices_privately_decoded_and_observed": 8,
            "new_original_pixels_decoded_in_pet10": 0,
            "original_private_images_published_in_git": False,
            "original_palette_rgb_and_alpha_verified": False,
            "original_native_gameplay_animation_executed": False,
            "actual_action_semantics_or_framerate_verified": False,
            "official_live_pet_species_or_release_confirmed": False,
            "same_operator_deployment_pet_master_present": False,
        },
        "historical_unverified_fields": {
            "official_pet_id": None, "birth_base_stat_and_growth": None,
            "elemental_attributes": None, "skills": None,
            "capturable_or_awarded": None, "capture_location": None,
            "release_date": None,
        },
    }


def main():
    cli = argparse.ArgumentParser()
    cli.add_argument("--mode", choices=("generate", "verify"), default="verify")
    args = cli.parse_args()
    expected = json.dumps(build(), ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.mode == "generate":
        TARGET.write_text(expected, encoding="utf-8")
    else:
        require(TARGET.read_text(encoding="utf-8") == expected, "PET10 source report changed")
    obj = json.loads(expected)
    print(json.dumps({"mode": args.mode, "name": obj["original_client_local_name_cp950"],
                      "preexisting_real_frames": len(obj["previously_privately_decoded_original_frames"]),
                      "new_decodes": 0, "official_issuance_verified": False},
                     ensure_ascii=False, sort_keys=True))

if __name__ == "__main__":
    main()
