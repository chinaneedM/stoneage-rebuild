"""O5 public-only source contract: original preserved map + pet frame evidence.

This validates archived *derived* evidence, NOT source raster bytes or a
reconstructed historical game. Original binaries, images and NPC text remain
only in the user's private Library. Do not identify numerical pets as species.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "research/recovered/STONEAGE-O5-SAME-CARRIER-PET-PRIVATE-ACCEPTANCE-R1.json"
SCENE13 = ROOT / "research/recovered/STONEAGE-SCENE13-PET-ACTION0-R1.json"
SCENE15 = ROOT / "research/recovered/STONEAGE-SCENE15-DOORWAY-SOURCE-R1.json"
O4 = ROOT / "research/recovered/STONEAGE-O4-TWO-SCENE-PRIVATE-ACTUAL-ACCEPTANCE-R1.json"
EXPECTED_KEYS = [5000, 5001, 5002, 5005, 5007, 5009, 5015]
EXPECTED_GROUPS = [100250, 100251, 100252]
EXPECTED_POSITIONS = {"100250": 72, "100251": 72, "100252": 208}
EXPECTED_DAT = "62dbef1614ede0ba032ca9c69cbfdc3d43938e45baba78701885790937b86b90"


def require(value, message):
    if not value:
        raise ValueError(message)


def load():
    return tuple(json.loads(p.read_text(encoding="utf-8")) for p in (RECEIPT, SCENE13, SCENE15, O4))


def validate(o5, r13, r15, o4):
    """The PNG-identity join was performed privately; public CI replays metadata."""
    j = o5["source_join"]
    p = o5["pet_source"]
    b = o5["actual_private_browser"]
    h = o5["historical_limits"]
    require(o5["schema"] == "stoneage.o5_same_carrier_original_pet_observation.r1", "unrecognized O5 receipt")
    require(r13["scope"] == "PRESERVED_MIXED25_NOT_AUTHENTICATED_OFFICIAL_TW1", "incorrect pet source scope")
    require(j["scope"] == "PRESERVED_MIXED25_COMMUNITY_MODIFIED_NOT_OFFICIAL_TW1", "incorrect map source scope")
    require(j["floor_1001_map_DAT_sha256"] == r15["views"][0]["source_DAT_sha256"] == EXPECTED_DAT,
            "same preserved source DAT identity mismatch")
    require(j["matching_original_map_DAT_sha256"] is True, "map source actual private proof missing")
    require(j["original_identical_png_keys"] == EXPECTED_KEYS
            and all(str(k) in r15["resources"] for k in EXPECTED_KEYS),
            "O5 room original image key qualification drift")
    require(j["identical_png_sha256_count"] == 7 and j["all_seven_original_png_sha256_equal"] is True,
            "private original seven PNG SHA proof not recorded")
    require(j["not_authenticated_same_retail_game_world"] is True, "retail world claim promoted")

    require(p["action_code"] == r13["action"] == 0, "pet original source action code mismatch")
    groups = r13["groups"]
    require([g["graphic"] for g in groups] == p["original_spr_numeric_groups"] == EXPECTED_GROUPS,
            "pet original numeric groups mismatch")
    require(len(groups) == 3 and sum(len(g["animations"]) for g in groups) == 24,
            "pet direction animation membership mismatch")
    all_frames = []
    for g in groups:
        require([(a["direction"], a["action"]) for a in g["animations"]]
                == [(i, 0) for i in range(8)], "pet 8 original direction keys mismatch")
        frames = [f[0] for a in g["animations"] for f in a["frames"]]
        require(len(frames) == EXPECTED_POSITIONS[str(g["graphic"])] == p["frame_positions_by_group"][str(g["graphic"])],
                "pet original position counts mismatch")
        require(all(a["duration_word"] == p["duration_words_original_not_ms"][str(g["graphic"])]
                    for a in g["animations"]), "pet source duration words mismatch")
        all_frames.extend(frames)
    unique = set(all_frames)
    require(len(all_frames) == r13["frame_occurrences"] == p["frame_occurrences_total"] == 352,
            "pet 352 ordered source frame positions mismatch")
    require(len(unique) == r13["distinct_pet_bitmaps"] == p["unique_original_bitmap_pngs"] == 208,
            "pet original 208 unique bitmap membership mismatch")
    require(len(all_frames) - len(unique) == r13["repeated_positions"] == p["repeated_original_frame_positions"] == 144,
            "pet original repeat membership mismatch")
    require(unique == {row["bitmapno"] for row in r13["bitmaps"]},
            "pet source bitmap report IDs mismatch")
    require(all(len(row["PNG_sha256"]) == 64 for row in r13["bitmaps"]),
            "invalid source original PNG hash records")
    require(p["original_png_sha256_verified_in_private"] == len(unique),
            "private source raster authentication coverage drift")

    require(o4["original_map_dat_sha256"]["floor_1001"] == EXPECTED_DAT,
            "original O4 map 1001 identity drift")
    require(o4["independent_actual_pixel_replay"]["total_pixels_compared"] == b["preserved_O4_independent_map_pixels"] == 1442557,
            "O4 independently verified map pixels claim changed")
    require(o4["independent_actual_pixel_replay"]["pixels_diff_gt1"] == b["preserved_O4_independent_map_pixel_differences"] == 0,
            "O4 independently verified original map pixel proof changed")
    require(b["original_scene_png_subresources_loaded"] == 67 and b["original_pet_distinct_pngs_decode_success"] == 208
            and b["source_pet_frame_positions_visited"] == 352,
            "real private Chromium source pixel acceptance counts changed")
    require(b["original_O4_two_way_door_and_static_npc_tour_retained"] is True
            and b["modern_pet_panel_changes_map_state"] is False,
            "existing O4 world observer was changed by the O5 sprite panel")
    require(b["js_errors"] == b["external_http_requests"] == 0
            and b["new_O5_full_map_pixel_comparison_run"] is False,
            "unsafe public/private browser claim drift")

    require(len(o5["private_archives"]) == 2
            and [x["bytes"] for x in o5["private_archives"]] == [2666980, 975186]
            and all(len(x["sha256"]) == 64 for x in o5["private_archives"]),
            "two separately qualified private original source archive identities missing")
    po = o5["private_output"]
    require(po["saved_to_private_library"] is True and po["zip_bytes"] == 2905474
            and len(po["zip_sha256"]) == 64 and len(po["html_sha256"]) == 64,
            "private O5 output custody drift")
    require(po["raw_original_png_DAT_RD_NPC_HTML_in_public_git"] is False
            and o5["public_ci_reads_only_derived_metadata"] is True,
            "copyright/privacy original material boundary violated")
    require(not any(h.values()), "unsupported original native/official world claim promoted")
    require(r13["official_species_identity_authenticated"] is False
            and r13["same_deployed_build_proven"] is False
            and r13["original_world_entered"] is False,
            "source pet claims upgraded without original historical evidence")
    require(o5["stage_a"] == "7 PARTIAL + 2 OPEN"
            and o5["stage_b"] == o5["wiki"] == "GATED"
            and o5["r79"] == "PAUSED_NON_BLOCKING" and o5["overall_percent"] is None,
            "historical stage boundary altered")
    return {
        "O5_PUBLIC_DERIVED_SOURCE_ONLY_GATE": "PASS",
        "same_saved_map_DAT": EXPECTED_DAT,
        "source_original_PNG_SHA_joins_privately_verified": 7,
        "pet_numeric_groups": EXPECTED_GROUPS,
        "pet_direction_animations": 24,
        "pet_original_frame_occurrences": 352,
        "pet_unique_source_PNGs": 208,
        "private_original_browser_source_frames_replayed": b["source_pet_frame_positions_visited"],
        "original_client_executed_in_public_CI": False,
        "original_game_world_entered": False,
    }


def main():
    print(json.dumps(validate(*load()), ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
